#!/bin/bash
# Discord Forum Context Poller
# Runs every 2 hours to check agent-hub threads for new activity
# and pre-loads context via memory QMDs

# Configuration - can be overridden via env vars
GUILD_ID="${DISCORD_GUILD_ID:-1470088164554182699}"
FORUM_CHANNEL_ID="${DISCORD_FORUM_CHANNEL_ID:-1472262592574787725}"
DISCORD_TOKEN="${DISCORD_TOKEN:-}"
CACHE_DIR="${OPENCLAW_WORKSPACE:-/home/deploy/.openclaw/workspace}/memory/discord-cache"
MEMORY_DIR="${OPENCLAW_WORKSPACE:-/home/deploy/.openclaw/workspace}/memory"

# Validate required config
if [ -z "$DISCORD_TOKEN" ]; then
  echo "Error: DISCORD_TOKEN not set. Set it via env var or configure in openclaw.json"
  exit 1
fi

mkdir -p "$CACHE_DIR"

# Get active threads from guild
RESPONSE=$(curl -s "https://discord.com/api/v9/guilds/$GUILD_ID/threads/active" \
  -H "Authorization: Bot $DISCORD_TOKEN" 2>/dev/null)

# Check for errors in response
if echo "$RESPONSE" | grep -q '"message"'; then
  echo "Error from Discord API: $RESPONSE"
  exit 1
fi

# Extract thread data using grep/sed (no jq available)
THREAD_IDS=$(echo "$RESPONSE" | grep -oP '"id":"[0-9]+"' | cut -d'"' -f4)
THREAD_NAMES=$(echo "$RESPONSE" | grep -oP '"name":"[^"]+"' | cut -d'"' -f4)
THREAD_MSG_IDS=$(echo "$RESPONSE" | grep -oP '"last_message_id":"[0-9]+"' | cut -d'"' -f4)

# Convert to arrays
IFS=$'\n' read -r -d '' -a ID_ARRAY <<< "$THREAD_IDS" || true
IFS=$'\n' read -r -d '' -a NAME_ARRAY <<< "$THREAD_NAMES" || true
IFS=$'\n' read -r -d '' -a MSG_ARRAY <<< "$THREAD_MSG_IDS" || true

# Process each thread
for i in "${!ID_ARRAY[@]}"; do
  thread_id="${ID_ARRAY[$i]}"
  thread_name="${NAME_ARRAY[$i]}"
  last_msg_id="${MSG_ARRAY[$i]}"
  
  [ -z "$thread_id" ] && continue
  
  CACHE_FILE="$CACHE_DIR/thread-$thread_id.json"
  LAST_KNOWN=$(cat "$CACHE_FILE" 2>/dev/null | grep -oP '"last_message_id":"[^"]*"' | cut -d'"' -f4 || echo "")
  
  # Check if there's new activity
  if [ "$last_msg_id" != "$LAST_KNOWN" ] && [ -n "$last_msg_id" ]; then
    echo "New activity in: $thread_name"
    
    # Search memory for context matching thread name
    # Convert thread name to lowercase and replace spaces with dashes
    CONTEXT_FILE="$MEMORY_DIR/${thread_name,,}.md"
    CONTEXT_FILE="${CONTEXT_FILE// /-}"  # replace spaces with dashes
    
    if [ -f "$CONTEXT_FILE" ]; then
      CONTEXT=$(cat "$CONTEXT_FILE")
      echo "{\"thread_id\":\"$thread_id\",\"thread_name\":\"$thread_name\",\"last_message_id\":\"$last_msg_id\",\"context_found\":true,\"context_file\":\"$CONTEXT_FILE\"}" > "$CACHE_FILE"
      echo "$CONTEXT" > "$CACHE_DIR/thread-$thread_id-context.txt"
    else
      # Try fuzzy match - look for file with thread name in it
      CONTEXT_FILE=$(find "$MEMORY_DIR" -maxdepth 1 -name "*.md" -exec grep -l "$thread_name" {} \; 2>/dev/null | head -1)
      if [ -n "$CONTEXT_FILE" ]; then
        CONTEXT=$(cat "$CONTEXT_FILE")
        echo "{\"thread_id\":\"$thread_id\",\"thread_name\":\"$thread_name\",\"last_message_id\":\"$last_msg_id\",\"context_found\":true,\"context_file\":\"$CONTEXT_FILE\"}" > "$CACHE_FILE"
        echo "$CONTEXT" > "$CACHE_DIR/thread-$thread_id-context.txt"
      else
        echo "{\"thread_id\":\"$thread_id\",\"thread_name\":\"$thread_name\",\"last_message_id\":\"$last_msg_id\",\"context_found\":false}" > "$CACHE_FILE"
      fi
    fi
    
    echo "  → Cached context for: $thread_name"
  fi
done

echo "Polling complete: $(date)"
