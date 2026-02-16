---
name: memory-cache
description: High-performance temporary storage using Redis. Use to save context, cache expensive API results, or share state between agent sessions. Follows strict key naming conventions.
metadata: {"openclaw":{"requires":{"env":["REDIS_URL"]},"install":[{"id":"node","kind":"exec","command":"scripts/cache.py ping"}]}}
---

# Memory Cache

## Setup
1. Copy `.env.example` to `.env`.
2. Set `REDIS_URL` (e.g. `redis://localhost:6379/0`) or specific host/port variables.
3. On first run, `scripts/cache.py` initializes a venv and installs dependencies.

## Core Workflows

### 1. Key Operations
Set, get, or delete data in the cache. All keys must use the `mema:` prefix.
- **Usage**: `bash $WORKSPACE/skills/memory-cache/scripts/cache.py set mema:<category>:<name> <value> [--ttl N]`
- **Usage**: `bash $WORKSPACE/skills/memory-cache/scripts/cache.py get mema:<category>:<name>`

### 2. Search & Scan
Safe listing of keys using the Redis SCAN command.
- **Usage**: `bash $WORKSPACE/skills/memory-cache/scripts/cache.py scan [pattern]`

## Key Naming Standard
**Requirement**: All keys must follow `mema:<category>:<name>`.
- `mema:context:*` – Short-term session state.
- `mema:cache:*` – Volatile data/API results.
- `mema:state:*` – Cross-session persistence.

## Security & Reliability
- **Namespace Isolation**: Strictly enforces the `mema:` prefix to avoid collisions with other Redis databases.
- **Connection Safety**: Handles connection retries and timeouts gracefully via environment configuration.
