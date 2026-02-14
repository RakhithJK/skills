#!/usr/bin/env python3
"""
Zonein MCP API Client — OpenClaw Skill Script

SECURITY MANIFEST:
  Environment variables accessed: ZONEIN_API_KEY (only)
  External endpoints called: https://mcp.zonein.xyz/api/v1/* (only)
  Local files read: none
  Local files written: none

Usage:
  python3 scripts/zonein.py <command> [options]

Commands:
  signals          — PM smart money trading signals
  leaderboard      — PM leaderboard (top traders by PnL)
  consensus        — PM consensus positions
  trader <wallet>  — PM trader profile + performance
  perp-signals     — Perp trading signals (HyperLiquid)
  perp-traders     — Perp smart money traders
  perp-top         — Perp top performers by PnL
  perp-categories  — Perp trader categories
  perp-coins       — Perp coin distribution
  perp-trader <addr> — Perp trader details
  agents           — List your trading agents
  status           — Check API key status
"""

import sys
import os
import json
import argparse

try:
    import urllib.request
    import urllib.error
    import urllib.parse
except ImportError:
    pass

API_BASE = "https://mcp.zonein.xyz/api/v1"


def get_api_key():
    """Get ZONEIN_API_KEY from environment."""
    key = os.environ.get("ZONEIN_API_KEY", "")
    if not key:
        # Try reading from openclaw config
        config_paths = [
            os.path.expanduser("~/.openclaw/openclaw.json"),
            os.path.expanduser("~/.openclaw/.env"),
        ]
        for p in config_paths:
            if os.path.exists(p) and p.endswith(".json"):
                try:
                    with open(p, "r") as f:
                        cfg = json.load(f)
                    key = (cfg.get("skills", {}).get("entries", {})
                           .get("zonein", {}).get("apiKey", ""))
                    if key:
                        break
                except Exception:
                    pass
    if not key:
        print(json.dumps({"error": "ZONEIN_API_KEY not set. Get your key at https://app.zonein.xyz/pm"}))
        sys.exit(1)
    return key


def api_request(path, params=None):
    """Make authenticated GET request to Zonein API."""
    key = get_api_key()
    url = f"{API_BASE}{path}"
    if params:
        query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
        if query:
            url = f"{url}?{query}"

    req = urllib.request.Request(url, headers={
        "X-API-Key": key,
        "Accept": "application/json",
    })

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            err = json.loads(body)
        except Exception:
            err = {"detail": body}
        print(json.dumps({"error": f"HTTP {e.code}", "detail": err.get("detail", body)}))
        sys.exit(1)
    except urllib.error.URLError as e:
        print(json.dumps({"error": f"Connection failed: {e.reason}"}))
        sys.exit(1)


def cmd_signals(args):
    """PM smart money trading signals."""
    params = {"limit": args.limit}
    if args.categories:
        params["categories"] = args.categories
    if args.period:
        params["period"] = args.period
    if args.min_wallets:
        params["min_wallets"] = args.min_wallets
    data = api_request("/pm/signals", params)
    print(json.dumps(data, indent=2))


def cmd_leaderboard(args):
    """PM leaderboard."""
    params = {
        "period": args.period,
        "category": args.category,
        "limit": args.limit,
    }
    data = api_request("/pm/leaderboard", params)
    print(json.dumps(data, indent=2))


def cmd_consensus(args):
    """PM consensus positions."""
    params = {"min_bettors": args.min_bettors}
    data = api_request("/pm/consensus", params)
    print(json.dumps(data, indent=2))


def cmd_trader(args):
    """PM trader profile."""
    data = api_request(f"/pm/trader/{args.wallet}")
    print(json.dumps(data, indent=2))


def cmd_perp_signals(args):
    """Perp trading signals."""
    params = {"limit": args.limit}
    if args.min_wallets:
        params["min_wallets"] = args.min_wallets
    if args.min_score:
        params["min_score"] = args.min_score
    data = api_request("/perp/signals", params)
    print(json.dumps(data, indent=2))


def cmd_perp_traders(args):
    """Perp smart traders."""
    params = {"limit": args.limit}
    if args.min_score:
        params["min_score"] = args.min_score
    if args.categories:
        params["categories"] = args.categories
    data = api_request("/perp/traders", params)
    print(json.dumps(data, indent=2))


def cmd_perp_top(args):
    """Perp top performers."""
    params = {"limit": args.limit, "time_period": args.period}
    data = api_request("/perp/traders/top", params)
    print(json.dumps(data, indent=2))


def cmd_perp_categories(args):
    """Perp categories."""
    data = api_request("/perp/categories")
    print(json.dumps(data, indent=2))


def cmd_perp_coins(args):
    """Perp coin distribution."""
    data = api_request("/perp/coins")
    print(json.dumps(data, indent=2))


def cmd_perp_trader(args):
    """Perp trader details."""
    data = api_request(f"/perp/trader/{args.address}")
    print(json.dumps(data, indent=2))


def cmd_agents(args):
    """List trading agents."""
    data = api_request("/agents/")
    print(json.dumps(data, indent=2))


def cmd_status(args):
    """Check API key status."""
    data = api_request("/auth/api-key/status")
    print(json.dumps(data, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="Zonein Smart Money Intelligence API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", help="Available commands")

    # --- PM Signals ---
    p = sub.add_parser("signals", help="PM smart money trading signals")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--categories", type=str, default=None, help="Comma-separated: POLITICS,CRYPTO,SPORTS")
    p.add_argument("--period", type=str, default="WEEK", help="DAY, WEEK, MONTH, ALL")
    p.add_argument("--min-wallets", type=int, default=None)
    p.set_defaults(func=cmd_signals)

    # --- PM Leaderboard ---
    p = sub.add_parser("leaderboard", help="PM leaderboard")
    p.add_argument("--period", type=str, default="WEEK", help="DAY, WEEK, MONTH, ALL")
    p.add_argument("--category", type=str, default="OVERALL", help="OVERALL, POLITICS, SPORTS, CRYPTO, etc.")
    p.add_argument("--limit", type=int, default=20)
    p.set_defaults(func=cmd_leaderboard)

    # --- PM Consensus ---
    p = sub.add_parser("consensus", help="PM consensus positions")
    p.add_argument("--min-bettors", type=int, default=3)
    p.set_defaults(func=cmd_consensus)

    # --- PM Trader ---
    p = sub.add_parser("trader", help="PM trader profile by wallet")
    p.add_argument("wallet", type=str)
    p.set_defaults(func=cmd_trader)

    # --- Perp Signals ---
    p = sub.add_parser("perp-signals", help="Perp trading signals")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--min-wallets", type=int, default=None)
    p.add_argument("--min-score", type=float, default=None)
    p.set_defaults(func=cmd_perp_signals)

    # --- Perp Traders ---
    p = sub.add_parser("perp-traders", help="Perp smart traders")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--min-score", type=float, default=None)
    p.add_argument("--categories", type=str, default=None, help="Comma-separated category filter")
    p.set_defaults(func=cmd_perp_traders)

    # --- Perp Top ---
    p = sub.add_parser("perp-top", help="Perp top performers by PnL")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--period", type=str, default="month", help="day, week, month")
    p.set_defaults(func=cmd_perp_top)

    # --- Perp Categories ---
    p = sub.add_parser("perp-categories", help="Perp trader categories")
    p.set_defaults(func=cmd_perp_categories)

    # --- Perp Coins ---
    p = sub.add_parser("perp-coins", help="Perp coin distribution")
    p.set_defaults(func=cmd_perp_coins)

    # --- Perp Trader ---
    p = sub.add_parser("perp-trader", help="Perp trader details by address")
    p.add_argument("address", type=str)
    p.set_defaults(func=cmd_perp_trader)

    # --- Agents ---
    p = sub.add_parser("agents", help="List trading agents")
    p.set_defaults(func=cmd_agents)

    # --- Status ---
    p = sub.add_parser("status", help="Check API key status")
    p.set_defaults(func=cmd_status)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
