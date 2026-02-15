#!/bin/bash
# Discord Context Skill - Command Handler

COMMAND="${1:-poll}"
ARG1="${2:-}"
ARG2="${3:-}"

GUILD_ID="1470088164554182699"
FORUM_CHANNEL_ID="1472262592574787725"
CACHE_DIR="/home/deploy/.openclaw/workspace/memory/discord-cache"
SCRIPT_DIR="/home/deploy/.openclaw/workspace/scripts"

case "$COMMAND" in
  poll)
    echo "Running context poll..."
    $SCRIPT_DIR/discord-context-poll.sh
    ;;
    
  context)
    if [ -z "$ARG1" ]; then
      echo "Usage: discord-context context [thread_id]"
      echo "Available cached threads:"
      ls -1 $CACHE_DIR/thread-*.json 2>/dev/null | while read f; do
        id=$(basename "$f" .json | sed 's/thread-//')
        name=$(grep -oP '"thread_name":"[^"]*"' "$f" 2>/dev/null | cut -d'"' -f4 || echo "?")
        echo "  $id ($name)"
      done
    else
      THREAD_ID="$ARG1"
      if [ -f "$CACHE_DIR/thread-$THREAD_ID-context.txt" ]; then
        echo "=== Context for thread $THREAD_ID ==="
        cat "$CACHE_DIR/thread-$THREAD_ID-context.txt"
      else
        echo "No cached context for thread $THREAD_ID"
      fi
    fi
    ;;
    
  link)
    if [ -z "$ARG1" ] || [ -z "$ARG2" ]; then
      echo "Usage: discord-context link <thread_id> <qmd_name>"
      echo "Example: discord-context link 1472595645192867983 skills"
    else
      THREAD_ID="$ARG1"
      QMD_NAME="$ARG2"
      QMD_FILE="/home/deploy/.openclaw/workspace/memory/${QMD_NAME}.md"
      
      if [ -f "$QMD_FILE" ]; then
        # Copy QMD content to thread cache
        cat "$QMD_FILE" > "$CACHE_DIR/thread-$THREAD_ID-context.txt"
        
        # Update metadata
        THREAD_NAME=$(grep -oP '"thread_name":"[^"]*"' "$CACHE_DIR/thread-$THREAD_ID.json" 2>/dev/null | cut -d'"' -f4 || echo "$QMD_NAME")
        echo "{\"thread_id\":\"$THREAD_ID\",\"thread_name\":\"$THREAD_NAME\",\"context_found\":true,\"context_file\":\"$QMD_FILE\",\"manually_linked\":true}" > "$CACHE_DIR/thread-$THREAD_ID.json"
        
        echo "✓ Linked $QMD_FILE to thread $THREAD_ID"
      else
        echo "Error: QMD not found: $QMD_FILE"
      fi
    fi
    ;;
    
  *)
    echo "Unknown command: $COMMAND"
    echo "Usage: discord-context <poll|context|link> [args]"
    ;;
esac
