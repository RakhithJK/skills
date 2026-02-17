#!/usr/bin/env python3
"""
Manage Agent - Create, configure, and control trading agents via Zonein API.
Usage:
  python manage_agent.py list
  python manage_agent.py create --name "My Agent" --type prediction_market --categories POLITICS,CRYPTO
  python manage_agent.py get <agent_id>
  python manage_agent.py enable <agent_id>
  python manage_agent.py disable <agent_id>
  python manage_agent.py stats <agent_id>
  python manage_agent.py trades <agent_id>
  python manage_agent.py update <agent_id> --categories POLITICS,CRYPTO,ECONOMICS
"""
import argparse
import json
import os
import sys
import urllib.request
import urllib.error

API_URL = "https://mcp.zonein.xyz/api/v1"


def api_call(method: str, endpoint: str, data: dict = None) -> dict:
    """Make API call to Zonein."""
    url = f"{API_URL}{endpoint}"
    api_key = os.getenv("ZONEIN_API_KEY")

    if data:
        body = json.dumps(data).encode("utf-8")
        req = urllib.request.Request(url, data=body, method=method)
        req.add_header("Content-Type", "application/json")
    else:
        req = urllib.request.Request(url, method=method)

    if api_key:
        req.add_header("X-API-Key", api_key)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        return {"error": f"HTTP {e.code}: {body}"}
    except urllib.error.URLError as e:
        return {"error": f"Connection failed: {e.reason}"}


def cmd_list(args):
    result = api_call("GET", "/agents/")
    agents = result.get("agents", [])
    print(f"\n=== Trading Agents ({len(agents)}) ===\n")
    if not agents:
        print("  No agents found. Create one with: manage_agent.py create --name 'My Agent'")
        return
    for a in agents:
        status_icon = {"enabled": "🟢", "disabled": "🔴", "paused": "⏸️", "draft": "📝"}.get(
            a.get("status", ""), "❓"
        )
        print(f"  {status_icon} {a.get('agent_id')} | {a.get('name')} | {a.get('agent_type')}")
        print(f"     Status: {a.get('status')} | Enabled: {a.get('enabled')}")
        if a.get("pm_config", {}).get("categories"):
            print(f"     Categories: {', '.join(a['pm_config']['categories'])}")
        print()


def cmd_create(args):
    agent_data = {
        "name": args.name,
        "agent_type": args.type,
        "description": args.description or f"{args.type} agent: {args.name}",
    }

    if args.type == "prediction_market":
        categories = [c.strip().upper() for c in args.categories.split(",")] if args.categories else ["OVERALL"]
        agent_data["pm_config"] = {
            "categories": categories,
            "leaderboard_period": "WEEK",
            "min_smart_wallets_agreeing": 3,
            "preferred_odds": 0.50,
            "min_edge": 0.03,
            "signal_weights": {
                "consensus_ratio": 25, "user_count": 30, "leaderboard_rank": 20,
                "price_deviation_penalty": 10, "reward_ratio": 15,
            },
        }
    elif args.type == "perp_trading":
        coins = [c.strip().upper() for c in args.coins.split(",")] if args.coins else ["BTC", "ETH", "SOL"]
        agent_data["perp_config"] = {
            "coins": coins,
            "min_trader_score": 50,
            "min_consensus_wallets": 3,
            "max_position_size_usd": 100.0,
            "leverage": 1.0,
            "stop_loss_pct": 0.05,
            "take_profit_pct": 0.10,
        }

    agent_data["risk_config"] = {
        "max_position_size_pct": 0.05,
        "max_portfolio_exposure_pct": 0.50,
        "daily_loss_limit_pct": 0.10,
    }

    result = api_call("POST", "/agents/", agent_data)
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return

    agent = result.get("agent", {})
    print(f"\n✅ Agent created successfully!")
    print(f"   Agent ID: {agent.get('agent_id')}")
    print(f"   Name: {agent.get('name')}")
    print(f"   Type: {agent.get('agent_type')}")
    print(f"   Status: {agent.get('status')} (draft - enable with: manage_agent.py enable {agent.get('agent_id')})")


def cmd_get(args):
    result = api_call("GET", f"/agents/{args.agent_id}")
    agent = result.get("agent")
    if not agent:
        print(f"❌ Agent not found: {args.agent_id}")
        return
    print(f"\n=== Agent: {agent.get('name')} ===\n")
    print(json.dumps(agent, indent=2, default=str))


def cmd_enable(args):
    result = api_call("POST", f"/agents/{args.agent_id}/enable")
    print(f"{'✅' if result.get('status') == 'enabled' else '❌'} {json.dumps(result)}")


def cmd_disable(args):
    result = api_call("POST", f"/agents/{args.agent_id}/disable")
    print(f"{'🔴' if result.get('status') == 'disabled' else '❌'} {json.dumps(result)}")


def cmd_pause(args):
    result = api_call("POST", f"/agents/{args.agent_id}/pause")
    print(f"{'⏸️' if result.get('status') == 'paused' else '❌'} {json.dumps(result)}")


def cmd_stats(args):
    result = api_call("GET", f"/agents/{args.agent_id}/stats")
    if "error" in result:
        print(f"❌ {result['error']}")
        return
    stats = result.get("stats", result)
    print(f"\n=== Agent Stats: {result.get('name', args.agent_id)} ===\n")
    print(f"  Total Trades: {stats.get('total_trades', 0)}")
    print(f"  Successful:   {stats.get('successful_trades', 0)}")
    print(f"  Win Rate:     {stats.get('win_rate', 0):.1%}")
    print(f"  Total PnL:    ${stats.get('total_pnl', 0):,.2f}")
    print(f"  Total Volume: ${stats.get('total_volume', 0):,.2f}")


def cmd_trades(args):
    result = api_call("GET", f"/agents/{args.agent_id}/trades?limit={args.limit}")
    trades = result.get("trades", [])
    print(f"\n=== Recent Trades ({len(trades)}) ===\n")
    for t in trades:
        print(f"  {t.get('timestamp', '')} | {t.get('market_question', t.get('market_id', ''))[:50]}")
        print(f"     Side: {t.get('side')} | Size: ${t.get('size_usd', 0):.2f} | "
              f"Result: {t.get('trade_result', '-')}")
        print()


def cmd_update(args):
    updates = {}
    if args.categories:
        cats = [c.strip().upper() for c in args.categories.split(",")]
        updates["pm_config"] = {"categories": cats}
    if args.max_position:
        updates.setdefault("risk_config", {})["max_position_size_pct"] = args.max_position
    if args.name:
        updates["name"] = args.name

    if not updates:
        print("❌ No updates specified. Use --categories, --max-position, or --name.")
        return

    result = api_call("PATCH", f"/agents/{args.agent_id}", updates)
    print(f"{'✅' if result.get('status') == 'updated' else '❌'} {json.dumps(result)}")


def main():
    parser = argparse.ArgumentParser(description="Manage Zonein trading agents")
    sub = parser.add_subparsers(dest="command", help="Command")

    sub.add_parser("list", help="List all agents")

    p_create = sub.add_parser("create", help="Create new agent")
    p_create.add_argument("--name", required=True, help="Agent name")
    p_create.add_argument("--type", choices=["prediction_market", "perp_trading"],
                          default="prediction_market")
    p_create.add_argument("--description", default=None)
    p_create.add_argument("--categories", default=None, help="PM categories (comma-sep)")
    p_create.add_argument("--coins", default=None, help="Perp coins (comma-sep)")

    p_get = sub.add_parser("get", help="Get agent details")
    p_get.add_argument("agent_id")

    p_enable = sub.add_parser("enable", help="Enable agent")
    p_enable.add_argument("agent_id")

    p_disable = sub.add_parser("disable", help="Disable agent")
    p_disable.add_argument("agent_id")

    p_pause = sub.add_parser("pause", help="Pause agent")
    p_pause.add_argument("agent_id")

    p_stats = sub.add_parser("stats", help="Get agent stats")
    p_stats.add_argument("agent_id")

    p_trades = sub.add_parser("trades", help="Get agent trades")
    p_trades.add_argument("agent_id")
    p_trades.add_argument("--limit", type=int, default=20)

    p_update = sub.add_parser("update", help="Update agent config")
    p_update.add_argument("agent_id")
    p_update.add_argument("--name", default=None)
    p_update.add_argument("--categories", default=None)
    p_update.add_argument("--max-position", type=float, default=None)

    args = parser.parse_args()

    commands = {
        "list": cmd_list, "create": cmd_create, "get": cmd_get,
        "enable": cmd_enable, "disable": cmd_disable, "pause": cmd_pause,
        "stats": cmd_stats, "trades": cmd_trades, "update": cmd_update,
    }

    if not args.command:
        parser.print_help()
        return

    commands[args.command](args)


if __name__ == "__main__":
    main()
