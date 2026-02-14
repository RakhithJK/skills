---
name: zonein
version: 1.2.0
description: |
  Fetch live smart money signals from Polymarket and HyperLiquid via Zonein API.
  Use PROACTIVELY when user asks about:
  (1) Prediction market signals, whales, smart bettors
  (2) Crypto perp trading signals, long/short sentiment
  (3) Leaderboard, top traders, wallet tracking
  (4) Trading agents management
  (5) Market overview, crypto sentiment, smart money flow
  Always use the bundled script — never call the API with inline code.
homepage: https://zonein.xyz
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["python3"],"env":["ZONEIN_API_KEY"]},"primaryEnv":"ZONEIN_API_KEY","files":["scripts/*"],"installer":{"instructions":"1. Go to https://app.zonein.xyz/pm\n2. Log in with your refcode\n3. Click 'Get API Key' button\n4. Copy the key and paste it below"}}}
---

# Zonein — Smart Money Intelligence

Fetch live trading intelligence from Polymarket and HyperLiquid smart money wallets using the bundled script.

## Setup (credentials)

### Get Your API Key

1. Go to **https://app.zonein.xyz/pm**
2. Log in with your account (you need a referral code to register)
3. Click the **"Get API Key"** button
4. Copy your API key (starts with `zn_`)

### Set API Key in OpenClaw

**Option A — Gateway Dashboard (recommended):**
1. Open your **OpenClaw Gateway Dashboard**
2. Go to **`/skills`** in the sidebar
3. Find **"zonein"** in Workspace Skills → click **Enable**
4. Enter your `ZONEIN_API_KEY` and save

**Option B — Environment variable:**
```bash
export ZONEIN_API_KEY="zn_your_key_here"
```

**Option C — The script also reads from `~/.openclaw/openclaw.json`** automatically (skills.entries.zonein.apiKey).

## Commands

All commands use the bundled Python script. **Always use these commands — never write inline API calls.**

### Prediction Market (Polymarket)

**Smart money signals** (what top Polymarket traders are betting on):
```bash
python3 skills/zonein/scripts/zonein.py signals --limit 10
python3 skills/zonein/scripts/zonein.py signals --categories POLITICS,CRYPTO --limit 10
python3 skills/zonein/scripts/zonein.py signals --period MONTH --min-wallets 5
```

**Leaderboard** (top traders by PnL):
```bash
python3 skills/zonein/scripts/zonein.py leaderboard --period WEEK --limit 10
python3 skills/zonein/scripts/zonein.py leaderboard --category POLITICS --period MONTH
```

**Consensus** (positions where multiple smart bettors agree):
```bash
python3 skills/zonein/scripts/zonein.py consensus --min-bettors 5
```

**Trader profile** (by wallet address):
```bash
python3 skills/zonein/scripts/zonein.py trader 0x1234...
```

### Perp Trading (HyperLiquid)

**Perp signals** (what smart money traders are long/short on):
```bash
python3 skills/zonein/scripts/zonein.py perp-signals --limit 10
python3 skills/zonein/scripts/zonein.py perp-signals --min-wallets 5 --min-score 60
```

**Smart traders** (HyperLiquid whale wallets):
```bash
python3 skills/zonein/scripts/zonein.py perp-traders --limit 10
python3 skills/zonein/scripts/zonein.py perp-traders --min-score 70 --categories swing_trading
```

**Top performers** (by PnL):
```bash
python3 skills/zonein/scripts/zonein.py perp-top --period week --limit 5
```

**Coin distribution** (long vs short by coin):
```bash
python3 skills/zonein/scripts/zonein.py perp-coins
```

**Categories & trader details:**
```bash
python3 skills/zonein/scripts/zonein.py perp-categories
python3 skills/zonein/scripts/zonein.py perp-trader 0xabc...
```

### Agents & Status

```bash
python3 skills/zonein/scripts/zonein.py agents
python3 skills/zonein/scripts/zonein.py status
```

## Quick Reference

| User asks... | Command |
|-------------|---------|
| "What's happening in the market?" | `signals --limit 5` + `perp-signals --limit 5` |
| "Show me PM signals for politics" | `signals --categories POLITICS --limit 10` |
| "What are whales doing on crypto?" | `perp-signals --limit 10` |
| "Top Polymarket traders this week" | `leaderboard --period WEEK --limit 10` |
| "Which coins are smart money long?" | `perp-coins` |
| "Best perp traders this month" | `perp-top --period month --limit 10` |
| "Track wallet 0x..." | `trader 0x...` or `perp-trader 0x...` |
| "Where is smart money flowing?" | `signals --limit 10` + `perp-signals --limit 10` + `perp-coins` |

## Operational Flows

### Market Overview

When user asks about market conditions, run these in sequence:
1. `signals --limit 5` — top PM signals
2. `perp-signals --limit 5` — top perp signals
3. `perp-coins` — coin long/short sentiment
4. Summarize: which markets have strong agreement, which coins whales are bullish/bearish on

### Trading Signals

1. Ask: prediction markets, perp, or both?
2. Run the relevant command(s)
3. Present top signals sorted by consensus strength
4. Explain each signal, e.g.: "5 top-100 traders all say YES on 'Will BTC hit $100k?' — current price 42c"

### Track a Wallet

1. `trader <wallet>` — Polymarket profile
2. `perp-trader <address>` — HyperLiquid profile
3. Present: performance, open positions, win rate

## Output Fields

### PM Signal
- `direction` — YES or NO
- `consensus` — 0 to 1 (1 = everyone agrees)
- `total_wallets` — how many smart traders hold this
- `best_rank` — best leaderboard position
- `cur_yes_price` / `cur_no_price` — current prices

### Perp Signal
- `coin` — token (BTC, ETH, SOL, HYPE...)
- `direction` — LONG or SHORT
- `consensus` — agreement ratio (0-1)
- `long_wallets` / `short_wallets` — traders per side
- `long_value` / `short_value` — USD per side
- `best_trader_score` — credibility score

### Periods & Categories
- **PM Periods:** DAY, WEEK, MONTH, ALL
- **PM Categories:** OVERALL, POLITICS, SPORTS, CRYPTO, CULTURE, ECONOMICS, TECH, FINANCE
- **Perp Periods:** day, week, month

## How to Present Results

### PM Signal
```
🔮 [market_title]
Smart money says: [YES/NO] | Agreement: [X]%
[N] top traders holding | Best ranked: #[rank]
Current price: YES [price] / NO [price]
```

### Perp Signal
```
📊 $[COIN]
Smart money says: [LONG/SHORT] | Agreement: [X]%
[N] whale traders | Top score: [score]
Long: $[X] | Short: $[X]
```

## Important

- Signals show what smart money is doing — not guaranteed outcomes
- Past performance does not predict future results
- Never invest more than you can afford to lose
- Always use the bundled script. Never construct raw API calls with curl or inline Python.

## External Endpoints

| URL | Data Sent |
|-----|-----------|
| `https://mcp.zonein.xyz/api/v1/*` | API key (X-API-Key header) + query parameters |

## Security & Privacy

- Only your API key leaves the machine (sent to mcp.zonein.xyz)
- No personal data is sent beyond the key
- All data is read-only (the script only makes GET requests)

## Trust Statement

By using this skill, your API key and query parameters are sent to https://mcp.zonein.xyz. Only install if you trust Zonein.

## Links

- **Dashboard:** https://app.zonein.xyz/pm/
- **Perp Dashboard:** https://app.zonein.xyz/perp/
- **API Docs:** https://mcp.zonein.xyz/docs
