---
name: discord-context
description: Manage Discord forum thread context. Pre-loads QMD content into threads for AI context awareness.
metadata:
 {
   "openclaw": {
     "requires": { "bins": ["curl"] },
     "user-invocable": true
   }
 }
---

# discord-context

Manage Discord forum thread context. Pre-loads QMD content into threads for AI context awareness.

## Setup

Requires:
- Discord bot token configured in OpenClaw
- `curl` command available
- OpenClaw workspace at `~/.openclaw/workspace` (default)

The skill expects:
- Cache directory: `memory/discord-cache/`
- QMD files in: `memory/*.md`

## Slash Command

When the user invokes `/discord-context <args>`, handle it as follows:

### `/discord-context poll`
Execute the poll script and report results.
```
Run: node {baseDir}/scripts/discord-context-cli.js poll
```

### `/discord-context context`
List all cached threads with their context.
```
Run: node {baseDir}/scripts/discord-context-cli.js context
```

### `/discord-context context <thread_id>`
Show context for a specific thread.
```
Run: node {baseDir}/scripts/discord-context-cli.js context <thread_id>
```

### `/discord-context link <thread_id> <qmd_name>`
Link a QMD to a thread.
```
Run: node {baseDir}/scripts/discord-context-cli.js link <thread_id> <qmd_name>
```

### `/discord-context help`
Show this help text.

## Examples

```
/discord-context poll
/discord-context context
/discord-context context 1472595645192867983
/discord-context link 1472595645192867983 skills
```

## How It Works

1. **Polling** (cron every 2 hours): Checks agent-hub forum for new activity, loads matching QMD content
2. **Caching**: Context stored in `memory/discord-cache/thread-{id}-context.txt`
3. **Dump**: Posts cached context to thread on demand

## Thread → QMD Mapping

Threads map to QMDs by name (spaces → dashes):
- `Skills` → `memory/skills.md`
- `Mission Control` → `memory/mission-control.md`
- `Philosophy time` → `memory/philosophy-time.md`
- `DOCUMENTATION` → `memory/documentation.md`
- `Nightly Work` → `memory/nightly-work.md`
- `mc-refactor-14022026` → `memory/mc-refactor-14022026.md`

## Implementation Details

The skill includes:
- `scripts/discord-context-cli.js` — main CLI entry point
- `scripts/discord-context-poll.sh` — polling script (called by cron)

Cache directory: `memory/discord-cache/`

## Installation Notes

After installing:
1. Ensure your Discord bot has access to your forum channels
2. Configure the forum channel ID in the polling script if needed
3. Create QMD files in your memory/ folder matching your thread names
4. Set up a cron job to run poll every 2 hours (optional)
