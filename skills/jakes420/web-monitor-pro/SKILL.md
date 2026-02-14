---
name: web-monitor
description: "Monitor web pages for changes, price drops, stock availability, and custom conditions. Use when a user asks to watch/track/monitor a URL, get notified about price changes, check if something is back in stock, or track any website for updates. Also handles listing, removing, and checking existing monitors."
metadata:
  {
    "openclaw":
      {
        "emoji": "👁️",
        "requires": { "bins": ["python3", "curl"] },
      },
  }
---

# Web Monitor

Track changes on any web page. Get alerted on price drops, stock changes, content updates, or custom conditions.

## Setup

No API keys needed. Uses `curl` for fetching and stores data in `~/.web-monitor/`.

## Core Script

All operations use `scripts/monitor.py`:

```bash
python3 scripts/monitor.py <command> [args]
```

## Commands

### Add a monitor

```bash
python3 scripts/monitor.py add "https://example.com/product" \
  --label "Product Name" \
  --condition "price below 500" \
  --interval 360
```

Options:
- `--label/-l` — Human-friendly name
- `--selector/-s` — CSS-like selector to narrow content (`#price` or `.stock-status`)
- `--condition/-c` — Alert condition (see below)
- `--interval/-i` — Check interval in minutes (default: 360)

### Check monitors

```bash
python3 scripts/monitor.py check              # Check all
python3 scripts/monitor.py check --id <id>     # Check one
python3 scripts/monitor.py check --verbose     # Include content preview
```

Returns JSON with `status` (changed/unchanged), `condition_met`, and `diff` summary.

### List monitors

```bash
python3 scripts/monitor.py list
```

### Remove a monitor

```bash
python3 scripts/monitor.py remove <id>
```

### View history

```bash
python3 scripts/monitor.py history <id> --limit 5
```

## Condition Syntax

- `price below 500` or `price < 500` — Price threshold (supports R, $, etc.)
- `price above 1000` or `price > 1000`
- `contains 'in stock'` — Text presence check
- `not contains 'out of stock'` — Text absence check

## Automation with Cron

Set up a cron job to check monitors periodically and alert the user:

```
Task: Check all web monitors. Run: python3 <skill_dir>/scripts/monitor.py check
Report any monitors where status is "changed" or "condition_met" is true.
If nothing changed, say so briefly or stay silent.
```

Recommended schedule: every 6 hours (`0 */6 * * *`).

## Tips

- For JS-heavy sites (Takealot, Amazon), use `web_fetch` tool as an alternative to get rendered content, then compare manually
- The script stores up to 20 snapshots per monitor for history
- Content is capped at 10KB per snapshot to keep storage reasonable
- Use `--selector` to focus on a specific element and reduce noise from unrelated page changes (timestamps, ads, etc.)
- When the user says "watch this" or "let me know when", create a monitor + cron job
