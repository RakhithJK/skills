#!/usr/bin/env python3
"""
Web Monitor - Track changes on web pages and alert on conditions.

Commands:
  add     Add a new monitor
  remove  Remove a monitor by ID
  list    List all monitors
  check   Check one or all monitors for changes
  history Show recent snapshots for a monitor

Storage: ~/.web-monitor/monitors.json, ~/.web-monitor/snapshots/
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

STORE_DIR = Path(os.environ.get("WEB_MONITOR_DIR", Path.home() / ".web-monitor"))


def _extract_prices_from_jsonld(data):
    """Recursively extract prices from JSON-LD structured data."""
    prices = []
    if isinstance(data, list):
        for item in data:
            prices.extend(_extract_prices_from_jsonld(item))
    elif isinstance(data, dict):
        # Check for offers/price patterns
        if 'price' in data:
            try:
                prices.append(float(str(data['price']).replace(',', '')))
            except (ValueError, TypeError):
                pass
        if 'lowPrice' in data:
            try:
                prices.append(float(str(data['lowPrice']).replace(',', '')))
            except (ValueError, TypeError):
                pass
        if 'offers' in data:
            prices.extend(_extract_prices_from_jsonld(data['offers']))
        # Recurse into all dict values
        for v in data.values():
            if isinstance(v, (dict, list)):
                prices.extend(_extract_prices_from_jsonld(v))
    return prices
MONITORS_FILE = STORE_DIR / "monitors.json"
SNAPSHOTS_DIR = STORE_DIR / "snapshots"
MAX_SNAPSHOTS_PER_MONITOR = 20


def ensure_dirs():
    STORE_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)


def load_monitors():
    if MONITORS_FILE.exists():
        return json.loads(MONITORS_FILE.read_text())
    return {}


def save_monitors(monitors):
    ensure_dirs()
    MONITORS_FILE.write_text(json.dumps(monitors, indent=2))


def gen_id(url, label):
    slug = re.sub(r'[^a-z0-9]+', '-', (label or url).lower()).strip('-')[:40]
    short_hash = hashlib.md5(url.encode()).hexdigest()[:6]
    return f"{slug}-{short_hash}"


def fetch_url_browser(url):
    """Fallback: indicates JS-rendered site needs browser-based fetching via OpenClaw."""
    return None, "JS-rendered or Cloudflare-protected site. Use OpenClaw browser tool (snapshot/navigate) in cron job instead of this script for this URL."


def fetch_url(url, selector=None):
    """Fetch URL content. Tries curl first, falls back to web_fetch-style extraction."""
    try:
        result = subprocess.run(
            ["curl", "-sL", "--max-time", "30", "-A",
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", url],
            capture_output=True, text=True, timeout=35
        )
        if result.returncode != 0:
            return None, f"curl failed: {result.stderr[:200]}"
        html = result.stdout

        # Strip HTML tags for text comparison
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)

        # Extract JSON-LD structured data (reliable price source for e-commerce)
        json_ld_blocks = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.DOTALL | re.IGNORECASE)
        structured_prices = []
        for block in json_ld_blocks:
            try:
                data = json.loads(block)
                structured_prices.extend(_extract_prices_from_jsonld(data))
            except (json.JSONDecodeError, ValueError):
                pass

        # Also check meta tags for prices (og:price, product:price)
        meta_prices = re.findall(r'<meta[^>]*(?:property|name)=["\'](?:og:price:amount|product:price:amount|price)["\'][^>]*content=["\']([^"\']+)["\']', html, re.IGNORECASE)
        for mp in meta_prices:
            try:
                structured_prices.append(float(mp.replace(',', '')))
            except ValueError:
                pass

        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()

        # If content is too short (JS-rendered page), try playwright/node fetch
        if len(text) < 200 and not structured_prices:
            text2, err2 = fetch_url_browser(url)
            if text2:
                # Re-extract structured prices from browser HTML isn't possible,
                # but browser gives us rendered text which has visible prices
                return text2, None
            return None, f"Page returned minimal content ({len(text)} chars) - likely JS-rendered. Browser fallback also failed: {err2}"

        # Prepend structured prices to content so condition checker can find them
        if structured_prices:
            price_str = " ".join(f"STRUCTURED_PRICE:R{p:.2f}" for p in structured_prices)
            text = price_str + " " + text

        # If selector provided, try to extract just that part
        if selector:
            # Basic CSS-like extraction for common patterns
            pattern = None
            if selector.startswith('#'):
                pattern = rf'id="{re.escape(selector[1:])}"[^>]*>(.*?)</\w+>'
            elif selector.startswith('.'):
                pattern = rf'class="[^"]*{re.escape(selector[1:])}[^"]*"[^>]*>(.*?)</\w+>'
            if pattern:
                match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
                if match:
                    extracted = re.sub(r'<[^>]+>', ' ', match.group(1))
                    text = re.sub(r'\s+', ' ', extracted).strip()

        return text, None
    except Exception as e:
        return None, str(e)


def save_snapshot(monitor_id, content, content_hash):
    ensure_dirs()
    snap_dir = SNAPSHOTS_DIR / monitor_id
    snap_dir.mkdir(exist_ok=True)

    timestamp = datetime.now(timezone.utc).isoformat()
    snap = {
        "timestamp": timestamp,
        "hash": content_hash,
        "content": content[:10000],  # Cap stored content
    }

    snap_file = snap_dir / f"{int(time.time())}.json"
    snap_file.write_text(json.dumps(snap, indent=2))

    # Prune old snapshots
    snaps = sorted(snap_dir.glob("*.json"), key=lambda f: f.name, reverse=True)
    for old in snaps[MAX_SNAPSHOTS_PER_MONITOR:]:
        old.unlink()

    return snap


def get_latest_snapshot(monitor_id):
    snap_dir = SNAPSHOTS_DIR / monitor_id
    if not snap_dir.exists():
        return None
    snaps = sorted(snap_dir.glob("*.json"), key=lambda f: f.name, reverse=True)
    if not snaps:
        return None
    return json.loads(snaps[0].read_text())


def get_snapshots(monitor_id, limit=5):
    snap_dir = SNAPSHOTS_DIR / monitor_id
    if not snap_dir.exists():
        return []
    snaps = sorted(snap_dir.glob("*.json"), key=lambda f: f.name, reverse=True)
    results = []
    for s in snaps[:limit]:
        results.append(json.loads(s.read_text()))
    return results


# --- Commands ---

def cmd_add(args):
    monitors = load_monitors()
    mid = gen_id(args.url, args.label)

    monitor = {
        "id": mid,
        "url": args.url,
        "label": args.label or args.url,
        "selector": args.selector,
        "condition": args.condition,
        "interval_minutes": args.interval or 360,
        "created": datetime.now(timezone.utc).isoformat(),
        "enabled": True,
    }

    monitors[mid] = monitor
    save_monitors(monitors)

    # Take initial snapshot
    content, err = fetch_url(args.url, args.selector)
    if content:
        content_hash = hashlib.md5(content.encode()).hexdigest()
        save_snapshot(mid, content, content_hash)
        print(json.dumps({"status": "added", "monitor": monitor, "initial_snapshot": True}))
    else:
        print(json.dumps({"status": "added", "monitor": monitor, "initial_snapshot": False, "error": err}))


def cmd_remove(args):
    monitors = load_monitors()
    if args.id in monitors:
        removed = monitors.pop(args.id)
        save_monitors(monitors)
        # Clean up snapshots
        snap_dir = SNAPSHOTS_DIR / args.id
        if snap_dir.exists():
            for f in snap_dir.glob("*.json"):
                f.unlink()
            snap_dir.rmdir()
        print(json.dumps({"status": "removed", "monitor": removed}))
    else:
        print(json.dumps({"status": "error", "message": f"Monitor '{args.id}' not found"}))


def cmd_list(args):
    monitors = load_monitors()
    output = []
    for mid, m in monitors.items():
        latest = get_latest_snapshot(mid)
        m["last_checked"] = latest["timestamp"] if latest else None
        output.append(m)
    print(json.dumps(output, indent=2))


def cmd_check(args):
    monitors = load_monitors()
    results = []

    targets = {}
    if args.id:
        if args.id in monitors:
            targets[args.id] = monitors[args.id]
        else:
            print(json.dumps({"status": "error", "message": f"Monitor '{args.id}' not found"}))
            return
    else:
        targets = {k: v for k, v in monitors.items() if v.get("enabled", True)}

    for mid, m in targets.items():
        content, err = fetch_url(m["url"], m.get("selector"))
        if err:
            results.append({
                "id": mid,
                "label": m["label"],
                "status": "error",
                "error": err,
            })
            continue

        content_hash = hashlib.md5(content.encode()).hexdigest()
        previous = get_latest_snapshot(mid)

        changed = False
        condition_met = False
        diff_summary = None

        if previous:
            if content_hash != previous["hash"]:
                changed = True
                # Generate a simple diff summary
                old_words = set(previous.get("content", "").lower().split())
                new_words = set(content.lower().split())
                added = new_words - old_words
                removed = old_words - new_words
                diff_summary = {
                    "words_added": len(added),
                    "words_removed": len(removed),
                    "sample_added": list(added)[:20],
                    "sample_removed": list(removed)[:20],
                }
        else:
            changed = True
            diff_summary = {"note": "first snapshot"}

        # Check condition if set
        condition = m.get("condition")
        if condition and content:
            cond_lower = condition.lower()
            content_lower = content.lower()

            # Price condition: "price < 500" or "price below 500"
            price_match = re.search(r'price\s*(below|above|<|>|<=|>=)\s*[\$£€R]?\s*([\d,.]+)', cond_lower)
            if price_match:
                op = price_match.group(1)
                threshold = float(price_match.group(2).replace(',', ''))

                found_prices = []

                # Priority 1: Structured prices (JSON-LD, meta tags) - most reliable
                structured = re.findall(r'STRUCTURED_PRICE:R([\d,.]+)', content)
                for p in structured:
                    try:
                        found_prices.append(float(p.replace(',', '')))
                    except ValueError:
                        pass

                # Priority 2: Prices with explicit currency symbols (R 4,999 or R4999.00)
                if not found_prices:
                    currency_prices = re.findall(r'[R$£€]\s?([\d,]+(?:\.\d{2})?)', content)
                    for p in currency_prices:
                        try:
                            val = float(p.replace(',', ''))
                            if val >= 50:  # Reasonable price floor
                                found_prices.append(val)
                        except ValueError:
                            pass

                # Use the most likely product price (avoid random small/huge numbers)
                # For "below" conditions, check if ANY found price meets it
                # For reliability, require at least one price found
                if found_prices:
                    # Use the price closest to the threshold as most relevant
                    best_price = min(found_prices, key=lambda x: abs(x - threshold))
                    if op in ('below', '<') and best_price < threshold:
                        condition_met = True
                    elif op in ('above', '>') and best_price > threshold:
                        condition_met = True
                    elif op == '<=' and best_price <= threshold:
                        condition_met = True
                    elif op == '>=' and best_price >= threshold:
                        condition_met = True

            # Contains condition: "contains 'in stock'"
            contains_match = re.search(r"contains\s+['\"](.+?)['\"]", cond_lower)
            if contains_match:
                search_text = contains_match.group(1)
                if search_text in content_lower:
                    condition_met = True

            # Not contains: "not contains 'out of stock'"
            not_contains_match = re.search(r"not\s+contains\s+['\"](.+?)['\"]", cond_lower)
            if not_contains_match:
                search_text = not_contains_match.group(1)
                if search_text not in content_lower:
                    condition_met = True

        # Save new snapshot
        save_snapshot(mid, content, content_hash)

        result = {
            "id": mid,
            "label": m["label"],
            "url": m["url"],
            "status": "changed" if changed else "unchanged",
            "condition": condition,
            "condition_met": condition_met if condition else None,
            "diff": diff_summary,
            "content_preview": content[:500] if args.verbose else None,
            "checked_at": datetime.now(timezone.utc).isoformat(),
        }
        results.append(result)

    print(json.dumps(results, indent=2))


def cmd_history(args):
    snaps = get_snapshots(args.id, limit=args.limit or 5)
    print(json.dumps(snaps, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Web Monitor - Track web page changes")
    sub = parser.add_subparsers(dest="command", required=True)

    # add
    p_add = sub.add_parser("add", help="Add a new monitor")
    p_add.add_argument("url", help="URL to monitor")
    p_add.add_argument("--label", "-l", help="Human-friendly label")
    p_add.add_argument("--selector", "-s", help="CSS-like selector to narrow content (#id or .class)")
    p_add.add_argument("--condition", "-c", help="Alert condition (e.g. 'price below 500', 'contains \"in stock\"')")
    p_add.add_argument("--interval", "-i", type=int, help="Check interval in minutes (default: 360)")

    # remove
    p_rm = sub.add_parser("remove", help="Remove a monitor")
    p_rm.add_argument("id", help="Monitor ID")

    # list
    sub.add_parser("list", help="List all monitors")

    # check
    p_check = sub.add_parser("check", help="Check monitors for changes")
    p_check.add_argument("--id", help="Check specific monitor (default: all)")
    p_check.add_argument("--verbose", "-v", action="store_true", help="Include content preview")

    # history
    p_hist = sub.add_parser("history", help="Show snapshot history")
    p_hist.add_argument("id", help="Monitor ID")
    p_hist.add_argument("--limit", "-n", type=int, default=5, help="Number of snapshots")

    args = parser.parse_args()

    ensure_dirs()

    if args.command == "add":
        cmd_add(args)
    elif args.command == "remove":
        cmd_remove(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "check":
        cmd_check(args)
    elif args.command == "history":
        cmd_history(args)


if __name__ == "__main__":
    main()
