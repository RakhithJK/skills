# Tradecraft Public API Reference

**Version:** 1.0.0
**Public API Base URL:** `https://api.tradecraft.finance/v1` (for trading, wallets, positions, etc.)
**Authentication API Base URL:** `https://api.tradecraft.finance/api` (for beta signup, auth, etc.)
**Homepage:** https://tradecraft.finance

## What is Tradecraft?

Tradecraft is a comprehensive cryptocurrency trading platform built on Solana that enables automated trading strategies, real-time signal monitoring, and collaborative trading through groups. The platform provides a complete API for programmatic trading, making it ideal for AI agents, trading bots, and automated systems.

### What Can Agents Do with Tradecraft?

**Trading Operations:**
- Execute buy and sell orders on Solana tokens programmatically
- Manage multiple trading wallets with Privy enterprise wallet infrastructure
- Monitor open positions and track trade history
- Set custom slippage and priority fees for optimal execution

**Signal Integration:**
- Subscribe to curated signal sources from the marketplace
- Monitor multiple signal feeds simultaneously
- Execute trades based on signal data

**Collaborative Trading:**
- Create and manage trading groups
- Share positions and trades with group members
- Participate in group chat and coordination
- View aggregated group performance

**Portfolio Management:**
- Track real-time position values and PnL
- Monitor wallet balances across multiple addresses
- View historical trade performance

### Key Features for Agents

- **Low Latency**: Direct API access for fast trade execution
- **Flexible Scopes**: Granular permission control for different operations
- **Comprehensive API**: Full coverage of trading, wallet, signal, and group operations

---

This document provides complete documentation for the Tradecraft Public API. It is designed to be read by both humans and LLMs to enable programmatic interaction with the Tradecraft platform.

---

## Quick Start

Tradecraft offers **two authentication methods** for AI agents:

### Method 1: Human-Created API Key (Recommended for Human-Assisted Agents)

If you are an agent working with a human user who does not have a Tradecraft account, then ask them to sign up for the beta test at https://tradecraft.finance to get an account.

If you are an agent working with a human user who already has a Tradecraft account:

1. **Instruct your human** to visit the Tradecraft web application at https://tradecraft.finance
2. Have them navigate to **Settings > API Keys**
3. Ask them to create a new API key with the required scopes for your use case
4. Have them securely provide you with the API key

Then test your connection:

```bash
# Health check (no authentication required)
curl -X GET "https://api.tradecraft.finance/v1/health"

# Verify your API key
curl -X GET "https://api.tradecraft.finance/v1/me" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

---

### Method 2: Direct Agent Beta Signup (Recommended for Autonomous Agents)

**For fully autonomous AI agents** that can control an email address and operate without human assistance, use this self-service flow:

#### Step 1: Beta Signup with Application Secret

Sign up for beta access. You will receive a **one-time application secret** that you must save securely:

```bash
curl -X POST "https://api.tradecraft.finance/api/public/beta-signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your-agent@example.com",
    "userType": "trader",
    "motivation": "Building AI trading agent for automated Solana token trading"
  }'
```

**Response:**
```json
{
  "success": true,
  "signupId": 123,
  "applicationSecret": "tc_app_a1b2c3d4e5f6...(64 hex chars)",
  "instructions": "Save your application secret securely. After approval, use it to generate your API key at /api/auth/exchange-secret"
}
```

**CRITICAL:** Save the `applicationSecret` - it will only be shown once and cannot be retrieved later.

#### Step 2: Wait for Admin Approval

A Tradecraft admin will review your beta signup (typically within 24-48 hours).

**Two methods to detect approval:**

**Method A: Email Monitoring (Recommended if you have email access)**
- Wait for approval notification email
- Once received, proceed to Step 3

**Method B: Polling (For autonomous agents without email access)** ⭐
- Call the exchange-secret endpoint repeatedly until approved
- The endpoint returns an error until approval: `"Account not yet approved"`
- Once approved, it returns your API key successfully
- **Rate limit:** 1 request per 5 seconds per email
- **Polling interval:** Wait at least 5 seconds between attempts
- **Recommended:** Implement exponential backoff (5s, 10s, 30s, 60s, etc.)

**Polling Example (Python):**
```python
import time
import requests

def poll_for_approval(email, secret, max_attempts=100):
    url = "https://api.tradecraft.finance/api/auth/exchange-secret"

    for attempt in range(max_attempts):
        response = requests.post(url, json={
            "email": email,
            "applicationSecret": secret
        })

        if response.status_code == 200:
            # Approved! Got API key
            return response.json()
        elif response.status_code == 401:
            # Not approved yet, wait and retry
            print(f"Attempt {attempt + 1}: Not approved yet, waiting...")
            time.sleep(5)  # Wait 5 seconds (rate limit)
        elif response.status_code == 429:
            # Rate limited, wait longer
            print("Rate limited, waiting 10 seconds...")
            time.sleep(10)
        else:
            # Other error
            print(f"Error: {response.json()}")
            break

    return None
```

When approved:
- Your Tradecraft account is automatically created
- Your email is added to the whitelist
- You can now exchange your application secret for an API key

#### Step 3: Exchange Secret for API Key

Once approved, exchange your application secret for a permanent API key:

```bash
curl -X POST "https://api.tradecraft.finance/api/auth/exchange-secret" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your-agent@example.com",
    "applicationSecret": "tc_app_a1b2c3d4e5f6..."
  }'
```

**Success Response (Approved):**
```json
{
  "status": "ok",
  "apiKey": "tc_live_xyz123...(80 hex chars)",
  "userId": 456,
  "username": "your-agent",
  "keyHint": "...xyz123ab",
  "scopes": [
    "strategies:read",
    "strategies:write",
    "trading:read",
    "trading:write",
    "wallets:read",
    "signals:read"
  ],
  "message": "API key generated successfully. Save it securely - it will not be shown again.",
  "documentation": "https://docs.tradecraft.com/api"
}
```

**Error Response (Not Yet Approved):**
```json
{
  "status": "error",
  "messages": [{
    "field": "general",
    "message": "Invalid credentials or account not yet approved. Contact admin if you have been approved."
  }]
}
```

**Error Response (Rate Limited):**
```json
{
  "status": "error",
  "messages": [{
    "field": "general",
    "message": "Too many requests. Please wait 5 seconds before trying again."
  }],
  "retryAfter": 5
}
```

**CRITICAL:** Save the `apiKey` - it will only be shown once. Your `applicationSecret` is now invalidated and cannot be reused.

#### Step 4: Start Trading

Use your API key for all subsequent requests:

```bash
curl -X GET "https://api.tradecraft.finance/v1/me" \
  -H "Authorization: Bearer tc_live_xyz123..."
```

---

### Security Comparison

| Feature | Human-Created Key | Agent Beta Signup |
|---------|------------------|-------------------|
| Human required | Yes | No |
| Email verification | Optional | Required (signup) |
| Approval process | Instant | 24-48 hours |
| One-time secret | No | Yes (application secret) |
| API key shown once | Yes | Yes |
| Best for | Human-assisted agents | Autonomous agents |

---

**Important Notes for Beta Agents:**
- **Application Secret Security**: Your `applicationSecret` is your proof of identity. Store it securely until you exchange it for an API key.
- **One-Time Use**: Application secrets can only be used once. After exchanging for an API key, the secret is permanently invalidated.
- **API Key Security**: Store your API key securely - it will only be shown once and cannot be retrieved
- **Fair Use**: Beta access is subject to fair use policies and rate limits
- **Compliance Monitoring**: Your agent account will be monitored for compliance with terms of service
- **Approval Timeline**: Beta applications are typically reviewed within 24-48 hours
- **Cannot Generate Multiple Keys**: You can only generate one API key per beta signup. Contact support if you need additional keys.

---

## Authentication & Authorization

### API Key Authentication

All API requests (except `/health`) require authentication via API key. Include your API key in the `Authorization` header:

```
Authorization: Bearer YOUR_API_KEY
```

### Available Scopes

| Scope | Description |
|-------|-------------|
| `trade:read` | View positions and trade history |
| `trade:write` | Execute buy/sell orders |
| `wallets:read` | View wallet information |
| `wallets:write` | Create wallets, enable/disable trading |
| `signals:read` | View signal sources and signals |
| `signals:write` | Subscribe to signal sources |
| `groups:read` | View groups, members, messages |
| `groups:write` | Create/manage groups, send messages |

### Rate Limiting

| Limit Type | Rate |
|------------|------|
| Per API Key | 1 request per second |
| Per IP | Variable (abuse prevention) |

Rate limit headers are included in all responses.

---

## Response Format

All responses follow this structure:

```json
{
  "success": true|false,
  "data": { ... },        // Present on success
  "error": {              // Present on failure
    "code": "ERROR_CODE",
    "message": "Human readable error message"
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

---

## API Endpoints

### Health Check

Check if the API is operational.

**Endpoint:** `GET /health`

**Authentication:** Not required

**CURL Example:**
```bash
curl -X GET "https://api.tradecraft.finance/v1/health"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "ok",
    "version": "v1",
    "timestamp": "2024-01-15T10:30:00.000Z"
  }
}
```

---

### Get API Key Info

Get information about the currently authenticated API key, including its permissions.

**Endpoint:** `GET /me`

**Authentication:** Required

**Scopes:** Any valid API key

**CURL Example:**
```bash
curl -X GET "https://api.tradecraft.finance/v1/me" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "keyId": "key_abc123",
    "userId": 123,
    "keyName": "My Trading Bot",
    "scopes": ["trade:read", "trade:write", "wallets:read"]
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

---

## Agent Beta Program Endpoints

### Beta Signup (Direct Agent Method)

Register your agent for beta access and receive an application secret for later API key generation.

**Endpoint:** `POST /api/public/beta-signup`

**Authentication:** Not required

**Prerequisites:**
- The agent must control a valid email address
- Email will be used for account verification and approval notifications

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | Yes | Valid email address you control |
| `telegram` | string | No | Telegram handle (optional) |
| `twitter` | string | No | Twitter/X handle (optional) |
| `userType` | string | Yes | One of: `trader`, `provider`, `both` |
| `motivation` | text | Yes | Why you want beta access and your intended use case |

**CURL Example:**
```bash
curl -X POST "https://api.tradecraft.finance/api/public/beta-signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "agent@example.com",
    "userType": "trader",
    "motivation": "Building AI trading agent for automated Solana token trading using technical analysis and market signals"
  }'
```

**Success Response:**
```json
{
  "success": true,
  "message": "Successfully signed up for beta access",
  "signupId": 123,
  "applicationSecret": "tc_app_a1b2c3d4e5f6789012345678901234567890abcdef123456789012345678",
  "instructions": "Save your application secret securely. After approval, use it to generate your API key at /api/auth/exchange-secret"
}
```

**CRITICAL:** Save the `applicationSecret` immediately - it will only be shown once and cannot be retrieved later.

**Error Codes:**
- `VALIDATION_ERROR` (400): Invalid or missing required fields
- `DUPLICATE_APPLICATION` (409): Email already has a pending or approved application
- `RATE_LIMITED` (429): Too many signups from this IP

---

### Exchange Application Secret for API Key

After admin approval, exchange your application secret for a permanent API key.

**Endpoint:** `POST /api/auth/exchange-secret`

**Authentication:** Not required (validates application secret instead)

**Rate Limit:** 1 request per 5 seconds per email (allows polling for approval without hitting rate limits)

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | Yes | Your email from beta signup |
| `applicationSecret` | string | Yes | Secret received during signup (format: `tc_app_{64_hex_chars}`) |

**CURL Example:**
```bash
curl -X POST "https://api.tradecraft.finance/api/auth/exchange-secret" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "agent@example.com",
    "applicationSecret": "tc_app_a1b2c3d4e5f6789012345678901234567890abcdef123456789012345678"
  }'
```

**Success Response:**
```json
{
  "status": "ok",
  "apiKey": "tc_live_xyz123abc456def789012345678901234567890abcdef123456789012345678901234567890",
  "userId": 456,
  "username": "agent",
  "keyHint": "...67890",
  "scopes": [
    "strategies:read",
    "strategies:write",
    "trading:read",
    "trading:write",
    "wallets:read",
    "signals:read"
  ],
  "message": "API key generated successfully. Save it securely - it will not be shown again.",
  "documentation": "https://docs.tradecraft.com/api"
}
```

**CRITICAL:**
- Save the `apiKey` immediately - it will only be shown once
- Your `applicationSecret` is now permanently invalidated and cannot be reused
- You can only generate one API key per beta signup

**Error Codes:**
- `INVALID_CREDENTIALS` (401): Invalid email or application secret
- `NOT_APPROVED` (401): Account not yet approved by admin. **For polling agents:** This is expected until approval - keep polling every 5+ seconds
- `INVALID_SECRET_FORMAT` (401): Application secret format is invalid (should be `tc_app_` followed by 64 hex characters)
- `KEY_ALREADY_EXISTS` (409): API key already exists for this account. Contact support to regenerate
- `ACCOUNT_NOT_FOUND` (404): User account not found in system
- `RATE_LIMITED` (429): Too many requests. Wait 5 seconds before retrying. Check `retryAfter` field in response

**Security Features:**
- ✅ One-time use: Application secret is invalidated after successful exchange
- ✅ Email + secret validation: Both must match for security
- ✅ Approval check: Account must be approved by admin before key generation
- ✅ No duplicate keys: Prevents multiple API keys from same secret

---

### Legacy: Submit Beta Application (Old Method - Deprecated)

**Note:** This endpoint is deprecated. Use `POST /api/public/beta-signup` instead.

**Endpoint:** `POST /agents/beta-signup`

**Authentication:** Not required

**Prerequisites:**
- The agent must control a valid email address
- This email will receive the approval notification and token needed for Step 2

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `agentName` | string | Yes | Name of your agent (max 100 chars) |
| `agentDescription` | string | Yes | Description of your agent and its purpose (max 500 chars) |
| `contactEmail` | string | Yes | Valid email address you control - will receive approval notification |
| `intendedUseCase` | string | Yes | How you plan to use Tradecraft (max 1000 chars) |

**CURL Example:**
```bash
curl -X POST "https://api.tradecraft.finance/v1/agents/beta-signup" \
  -H "Content-Type: application/json" \
  -d '{
    "agentName": "TradingBot Alpha",
    "agentDescription": "Automated trading agent for Solana tokens using signal analysis",
    "contactEmail": "admin@tradingbot.ai",
    "intendedUseCase": "Execute automated trades based on technical analysis and market signals"
  }'
```

**Success Response:**
```json
{
  "success": true,
  "data": {
    "status": "pending",
    "message": "Your beta application has been submitted. You will receive an email when approved.",
    "applicationId": "app_abc123",
    "submittedAt": "2024-01-15T10:30:00.000Z"
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

**Error Codes:**
- `VALIDATION_ERROR` (400): Invalid or missing required fields
- `DUPLICATE_APPLICATION` (409): Email already has a pending or approved application
- `RATE_LIMITED` (429): Too many applications from this IP

---

## Trade Endpoints

### Execute Buy Order

Purchase tokens using SOL from a specified wallet.

**Endpoint:** `POST /trade/buy`

**Authentication:** Required

**Scopes:** `trade:write`

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tokenAddress` | string | Yes | Solana token mint address to buy |
| `walletId` | integer | Yes | Wallet ID to use for the purchase |
| `solAmount` | number | Yes | Amount of SOL to spend |
| `slippagePercentage` | number | No | Maximum slippage (default: 5, max: 50) |
| `priorityFee` | number | No | Priority fee in SOL (default: auto) |
| `groupId` | integer | No | Group ID if trading within a group |

**CURL Example:**
```bash
curl -X POST "https://api.tradecraft.finance/v1/trade/buy" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tokenAddress": "So11111111111111111111111111111111111111112",
    "walletId": 42,
    "solAmount": 0.5,
    "slippagePercentage": 10
  }'
```

**Success Response:**
```json
{
  "success": true,
  "data": {
    "positionId": 123,
    "signature": "5J7...abc",
    "tokenAmount": 1000000,
    "solSpent": 0.5,
    "pricePerToken": 0.0000005
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

**Error Codes:**
- `INVALID_TOKEN_ADDRESS` (400): Invalid token mint address
- `INVALID_WALLET_ID` (400): Invalid or missing wallet ID
- `INVALID_AMOUNT` (400): Invalid SOL amount
- `WALLET_NOT_FOUND` (404): Wallet does not exist or doesn't belong to user
- `TRADING_DISABLED` (403): Trading is disabled for this wallet
- `NOT_GROUP_MEMBER` (403): Not a member of the specified group
- `TRADE_EXECUTION_FAILED` (400): Transaction failed on-chain

---

### Execute Sell Order

Sell tokens from an existing position.

**Endpoint:** `POST /trade/sell`

**Authentication:** Required

**Scopes:** `trade:write`

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `positionId` | integer | Yes | Position ID to sell from |
| `tokenAmount` | number | No | Amount of tokens to sell (omit for full position) |

**CURL Example (sell all):**
```bash
curl -X POST "https://api.tradecraft.finance/v1/trade/sell" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "positionId": 123
  }'
```

**CURL Example (partial sell):**
```bash
curl -X POST "https://api.tradecraft.finance/v1/trade/sell" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "positionId": 123,
    "tokenAmount": 500000
  }'
```

**Success Response:**
```json
{
  "success": true,
  "data": {
    "positionId": 123,
    "signature": "3K9...xyz",
    "tokensSold": 500000,
    "solReceived": 0.25,
    "remainingTokens": 500000
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

**Error Codes:**
- `INVALID_POSITION_ID` (400): Invalid position ID
- `POSITION_NOT_FOUND` (404): Position doesn't exist or doesn't belong to user
- `INSUFFICIENT_TOKENS` (400): Not enough tokens to sell
- `TRADING_DISABLED` (403): Trading is disabled for this wallet

---

## Positions Endpoints

### List Positions

Get a paginated list of your trading positions.

**Endpoint:** `GET /positions`

**Authentication:** Required

**Scopes:** `trade:read`

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `status` | string | all | Filter by status: `open`, `closed`, `all` |
| `limit` | integer | 50 | Results per page (max: 500) |
| `offset` | integer | 0 | Pagination offset |

**CURL Example:**
```bash
curl -X GET "https://api.tradecraft.finance/v1/positions?status=open&limit=20" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "positions": [
      {
        "id": 123,
        "tokenAddress": "So11111111111111111111111111111111111111112",
        "tokenName": "Wrapped SOL",
        "tokenSymbol": "SOL",
        "currentAmount": 1000000,
        "avgBuyPrice": 0.0000005,
        "currentPrice": 0.0000006,
        "currentValueSol": 0.6,
        "pnl": 0.1,
        "pnlPercentage": 20,
        "realizedPnl": 0,
        "gainMultiplier": 1.2,
        "status": "open",
        "walletId": 42,
        "groupId": null,
        "createdAt": "2024-01-15T08:00:00.000Z",
        "updatedAt": "2024-01-15T10:30:00.000Z"
      }
    ],
    "pagination": {
      "total": 45,
      "limit": 20,
      "offset": 0,
      "hasMore": true
    }
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

---

### Get Trade History

Get a paginated list of your executed trades.

**Endpoint:** `GET /positions/trades`

**Authentication:** Required

**Scopes:** `trade:read`

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `action` | string | - | Filter by action: `buy`, `sell` |
| `limit` | integer | 50 | Results per page (max: 500) |
| `offset` | integer | 0 | Pagination offset |
| `since` | ISO8601 | - | Only trades after this timestamp |

**CURL Example:**
```bash
curl -X GET "https://api.tradecraft.finance/v1/positions/trades?action=sell&limit=10&since=2024-01-01T00:00:00Z" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "trades": [
      {
        "id": 456,
        "positionId": 123,
        "action": "sell",
        "tokenAddress": "So11111111111111111111111111111111111111112",
        "tokenName": "Wrapped SOL",
        "tokenAmount": 500000,
        "solAmount": 0.25,
        "pricePerToken": 0.0000005,
        "pnlSol": 0.05,
        "pnlPercentage": 25,
        "signature": "3K9...xyz",
        "timestamp": "2024-01-15T10:30:00.000Z"
      }
    ],
    "pagination": {
      "total": 100,
      "limit": 10,
      "offset": 0,
      "hasMore": true
    }
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

---

## Wallet Endpoints

### List Wallets

Get all wallets associated with your account, including SOL balances.

**Endpoint:** `GET /wallets`

**Authentication:** Required

**Scopes:** `wallets:read`

**CURL Example:**
```bash
curl -X GET "https://api.tradecraft.finance/v1/wallets" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "wallets": [
      {
        "id": 42,
        "name": "Main Trading Wallet",
        "address": "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM",
        "balance": 5.25,
        "tradingEnabled": true,
        "createdAt": "2024-01-01T00:00:00.000Z"
      },
      {
        "id": 43,
        "name": "Backup Wallet",
        "address": "8QzEZwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWN",
        "balance": 2.0,
        "balanceError": false,
        "tradingEnabled": false,
        "createdAt": "2024-01-05T00:00:00.000Z"
      }
    ]
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

Note: `balance` may be `null` with `balanceError: true` if the balance fetch times out.

---

### Create Wallet

Generate a new Privy-managed wallet. The wallet is created with trading disabled by default.

**Endpoint:** `POST /wallets`

**Authentication:** Required

**Scopes:** `wallets:write`

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | No | Wallet name (auto-generated if not provided) |

**CURL Example:**
```bash
curl -X POST "https://api.tradecraft.finance/v1/wallets" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Bot Trading Wallet"
  }'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "wallet": {
      "id": 44,
      "name": "Bot Trading Wallet",
      "address": "7PzFXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWO",
      "tradingEnabled": false,
      "createdAt": "2024-01-15T10:30:00.000Z"
    },
    "requiresFrontendActivation": true
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

Note: `requiresFrontendActivation: true` indicates that trading must be enabled via the web interface for security.

**Error Codes:**
- `SERVICE_UNAVAILABLE` (503): Privy wallet service not configured
- `PRIVY_ACCOUNT_REQUIRED` (400): User must have Privy account
- `WALLET_EXISTS` (409): Wallet with this address already exists

---

### Enable Wallet Trading

Enable trading for a specific wallet.

**Endpoint:** `POST /wallets/:walletId/enable-trading`

**Authentication:** Required

**Scopes:** `wallets:write`

**CURL Example:**
```bash
curl -X POST "https://api.tradecraft.finance/v1/wallets/42/enable-trading" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "wallet": {
      "id": 42,
      "tradingEnabled": true
    }
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

---

### Disable Wallet Trading

Disable trading for a specific wallet.

**Endpoint:** `POST /wallets/:walletId/disable-trading`

**Authentication:** Required

**Scopes:** `wallets:write`

**CURL Example:**
```bash
curl -X POST "https://api.tradecraft.finance/v1/wallets/42/disable-trading" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "wallet": {
      "id": 42,
      "tradingEnabled": false
    }
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

---

## Signal Source Endpoints

### List Signal Sources

Get available signal sources from the marketplace.

**Endpoint:** `GET /signals/sources`

**Authentication:** Required

**Scopes:** `signals:read`

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `category` | string | - | Filter by category |
| `search` | string | - | Search by name/description |
| `sortBy` | string | newest | Sort: `newest`, `popular`, `rating` |
| `limit` | integer | 20 | Results per page (max: 100) |
| `offset` | integer | 0 | Pagination offset |

**CURL Example:**
```bash
curl -X GET "https://api.tradecraft.finance/v1/signals/sources?category=telegram&limit=10" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "sources": [
      {
        "id": 1,
        "name": "Alpha Signals",
        "description": "High-quality Solana token signals",
        "category": "telegram",
        "isFree": false,
        "price": 0.5,
        "paymentMethod": "SOL",
        "subscriberCount": 150,
        "rating": 4.5,
        "createdAt": "2024-01-01T00:00:00.000Z"
      }
    ],
    "pagination": {
      "total": 25,
      "limit": 10,
      "offset": 0,
      "hasMore": true
    }
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

---

### Subscribe to Signal Source

Subscribe to a signal source to receive trading signals.

**Endpoint:** `POST /signals/sources/:sourceId/subscribe`

**Authentication:** Required

**Scopes:** `signals:write`

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `paymentMethod` | string | No | Payment method: `FREE`, `SOL`, `HODL`, `WHITELIST` |
| `transactionSignature` | string | Conditional | Required for SOL payment |
| `connectedWallet` | string | Conditional | Required for HODL verification |

**CURL Example (free source):**
```bash
curl -X POST "https://api.tradecraft.finance/v1/signals/sources/1/subscribe" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "paymentMethod": "FREE"
  }'
```

**CURL Example (paid source):**
```bash
curl -X POST "https://api.tradecraft.finance/v1/signals/sources/2/subscribe" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "paymentMethod": "SOL",
    "transactionSignature": "5J7...abc"
  }'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "subscription": {
      "id": 789,
      "sourceId": 1,
      "sourceName": "Alpha Signals",
      "paymentMethod": "FREE",
      "subscribedAt": "2024-01-15T10:30:00.000Z",
      "expiresAt": "2025-01-15T10:30:00.000Z"
    }
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

**Error Codes:**
- `SOURCE_NOT_FOUND` (404): Signal source doesn't exist
- `SOURCE_NOT_AVAILABLE` (400): Source is not approved
- `ALREADY_SUBSCRIBED` (400): Already have active subscription
- `NOT_FREE` (400): Source requires payment
- `NOT_WHITELISTED` (403): Not on whitelist
- `MISSING_TRANSACTION` (400): Transaction signature required for SOL payment
- `MISSING_WALLET` (400): Wallet required for HODL verification

---

### Get Signals from Source

Fetch signals from a subscribed signal source.

**Endpoint:** `GET /signals/sources/:sourceId/signals`

**Authentication:** Required

**Scopes:** `signals:read`

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | integer | 50 | Results per page (max: 100) |
| `before` | ISO8601 | - | Cursor for pagination (timestamp) |

**CURL Example:**
```bash
curl -X GET "https://api.tradecraft.finance/v1/signals/sources/1/signals?limit=20" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**CURL Example (with pagination):**
```bash
curl -X GET "https://api.tradecraft.finance/v1/signals/sources/1/signals?limit=20&before=2024-01-15T10:00:00.000Z" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "signals": [
      {
        "id": 1001,
        "tokenAddress": "So11111111111111111111111111111111111111112",
        "chain": "solana",
        "signalTime": "2024-01-15T10:15:00.000Z",
        "initialPrice": 0.0000005,
        "metadata": {
          "source": "telegram",
          "channel": "alpha_calls"
        }
      }
    ],
    "pagination": {
      "hasMore": true,
      "nextCursor": "2024-01-15T10:00:00.000Z"
    }
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

**Error Codes:**
- `SOURCE_NOT_FOUND` (404): Signal source doesn't exist
- `ACCESS_DENIED` (403): No active subscription to this source

---

## Group Endpoints

### List My Groups

Get all groups you are a member of.

**Endpoint:** `GET /groups`

**Authentication:** Required

**Scopes:** `groups:read`

**CURL Example:**
```bash
curl -X GET "https://api.tradecraft.finance/v1/groups" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "groups": [
      {
        "id": 1,
        "name": "Alpha Traders",
        "description": "Private trading group",
        "isPublic": false,
        "tradingEnabled": true,
        "positionsVisible": true,
        "memberCount": 12,
        "maxMembers": 50,
        "avatarUrl": "https://...",
        "ownerId": 100,
        "role": "owner",
        "joinedAt": "2024-01-01T00:00:00.000Z",
        "createdAt": "2024-01-01T00:00:00.000Z"
      }
    ]
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

---

### Create Group

Create a new trading group.

**Endpoint:** `POST /groups`

**Authentication:** Required

**Scopes:** `groups:write`

**Request Body:**
| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `name` | string | Yes | - | Group name |
| `description` | string | No | - | Group description |
| `isPublic` | boolean | No | false | Whether group is publicly visible |
| `tradingEnabled` | boolean | No | true | Enable group trading features |
| `positionsVisible` | boolean | No | true | Share positions between members |
| `maxMembers` | integer | No | 50 | Maximum members (2-50) |
| `avatarUrl` | string | No | - | Group avatar URL |

**CURL Example:**
```bash
curl -X POST "https://api.tradecraft.finance/v1/groups" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Trading Group",
    "description": "A group for discussing trades",
    "tradingEnabled": true,
    "positionsVisible": true,
    "maxMembers": 25
  }'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "group": {
      "id": 2,
      "name": "My Trading Group",
      "description": "A group for discussing trades",
      "inviteCode": "abc123xyz456",
      "isPublic": false,
      "tradingEnabled": true,
      "positionsVisible": true,
      "memberCount": 1,
      "maxMembers": 25,
      "avatarUrl": null,
      "createdAt": "2024-01-15T10:30:00.000Z"
    }
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

---

### Get Group Details

Get details of a specific group.

**Endpoint:** `GET /groups/:groupId`

**Authentication:** Required

**Scopes:** `groups:read`

**CURL Example:**
```bash
curl -X GET "https://api.tradecraft.finance/v1/groups/1" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "group": {
      "id": 1,
      "name": "Alpha Traders",
      "description": "Private trading group",
      "inviteCode": "abc123xyz456",
      "isPublic": false,
      "tradingEnabled": true,
      "positionsVisible": true,
      "memberCount": 12,
      "maxMembers": 50,
      "avatarUrl": "https://...",
      "ownerId": 100,
      "role": "owner",
      "membership": {
        "joinedAt": "2024-01-01T00:00:00.000Z",
        "sharePositions": true,
        "isMuted": false
      },
      "createdAt": "2024-01-01T00:00:00.000Z"
    }
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

---

### Update Group

Update group settings (owner only).

**Endpoint:** `PATCH /groups/:groupId`

**Authentication:** Required

**Scopes:** `groups:write`

**Request Body:** (all fields optional)
| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Group name |
| `description` | string | Group description |
| `isPublic` | boolean | Public visibility |
| `tradingEnabled` | boolean | Enable trading features |
| `positionsVisible` | boolean | Share positions |
| `maxMembers` | integer | Maximum members (2-50) |
| `avatarUrl` | string | Avatar URL |

**CURL Example:**
```bash
curl -X PATCH "https://api.tradecraft.finance/v1/groups/1" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Updated description",
    "maxMembers": 30
  }'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "group": {
      "id": 1,
      "name": "Alpha Traders",
      "description": "Updated description",
      "maxMembers": 30
    }
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

---

### Delete Group

Delete a group (owner only). This is permanent.

**Endpoint:** `DELETE /groups/:groupId`

**Authentication:** Required

**Scopes:** `groups:write`

**CURL Example:**
```bash
curl -X DELETE "https://api.tradecraft.finance/v1/groups/1" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "message": "Group deleted successfully"
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

---

### Join Group

Join a group using an invite code.

**Endpoint:** `POST /groups/join`

**Authentication:** Required

**Scopes:** `groups:write`

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `inviteCode` | string | Yes | 12-character invite code |

**CURL Example:**
```bash
curl -X POST "https://api.tradecraft.finance/v1/groups/join" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "inviteCode": "abc123xyz456"
  }'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "group": {
      "id": 1,
      "name": "Alpha Traders",
      "description": "Private trading group",
      "memberCount": 13,
      "tradingEnabled": true,
      "joinedAt": "2024-01-15T10:30:00.000Z"
    }
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

**Error Codes:**
- `INVALID_INVITE_CODE` (400): Invalid or malformed invite code
- `FORBIDDEN` (403): You are banned from this group
- `BAD_REQUEST` (400): Already a member or group is full

---

### Leave Group

Leave a group you are a member of. Owners cannot leave their own group.

**Endpoint:** `POST /groups/:groupId/leave`

**Authentication:** Required

**Scopes:** `groups:write`

**CURL Example:**
```bash
curl -X POST "https://api.tradecraft.finance/v1/groups/1/leave" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "message": "Left group successfully"
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

---

### Get Invite Code

Get the invite code for a group (members only).

**Endpoint:** `GET /groups/:groupId/invite`

**Authentication:** Required

**Scopes:** `groups:read`

**CURL Example:**
```bash
curl -X GET "https://api.tradecraft.finance/v1/groups/1/invite" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "inviteCode": "abc123xyz456",
    "inviteUrl": "https://app.tradecraft.io/groups/join/abc123xyz456"
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

---

### Regenerate Invite Code

Generate a new invite code, invalidating the old one (owner only).

**Endpoint:** `POST /groups/:groupId/invite`

**Authentication:** Required

**Scopes:** `groups:write`

**CURL Example:**
```bash
curl -X POST "https://api.tradecraft.finance/v1/groups/1/invite" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "inviteCode": "new123code456"
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

---

### Get Group Members

Get all members of a group.

**Endpoint:** `GET /groups/:groupId/members`

**Authentication:** Required

**Scopes:** `groups:read`

**CURL Example:**
```bash
curl -X GET "https://api.tradecraft.finance/v1/groups/1/members" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "members": [
      {
        "userId": 100,
        "username": "trader_alice",
        "role": "owner",
        "joinedAt": "2024-01-01T00:00:00.000Z",
        "sharePositions": true,
        "isMuted": false,
        "mutedUntil": null
      },
      {
        "userId": 101,
        "username": "trader_bob",
        "role": "member",
        "joinedAt": "2024-01-05T00:00:00.000Z",
        "sharePositions": true,
        "isMuted": false,
        "mutedUntil": null
      }
    ]
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

---

### Remove/Ban Member

Remove a member from the group and ban them (owner only).

**Endpoint:** `DELETE /groups/:groupId/members/:userId`

**Authentication:** Required

**Scopes:** `groups:write`

**CURL Example:**
```bash
curl -X DELETE "https://api.tradecraft.finance/v1/groups/1/members/101" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "message": "Member removed and banned from group"
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

---

### Update Member

Mute/unmute a member (owner) or update your own settings.

**Endpoint:** `PATCH /groups/:groupId/members/:userId`

**Authentication:** Required

**Scopes:** `groups:write`

**Request Body:**
| Field | Type | Description |
|-------|------|-------------|
| `isMuted` | boolean | Mute/unmute member (owner only) |
| `muteDuration` | integer | Mute duration in minutes (owner only) |
| `sharePositions` | boolean | Toggle position sharing (self only) |

**CURL Example (mute member - owner only):**
```bash
curl -X PATCH "https://api.tradecraft.finance/v1/groups/1/members/101" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "isMuted": true,
    "muteDuration": 60
  }'
```

**CURL Example (update own settings):**
```bash
curl -X PATCH "https://api.tradecraft.finance/v1/groups/1/members/100" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "sharePositions": false
  }'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "member": {
      "userId": 101,
      "isMuted": true,
      "mutedUntil": "2024-01-15T11:30:00.000Z"
    }
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

---

### Get Banned Users

Get list of banned users (owner only).

**Endpoint:** `GET /groups/:groupId/bans`

**Authentication:** Required

**Scopes:** `groups:read`

**CURL Example:**
```bash
curl -X GET "https://api.tradecraft.finance/v1/groups/1/bans" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "bans": [
      {
        "userId": 102,
        "username": "spammer_charlie",
        "bannedAt": "2024-01-10T00:00:00.000Z",
        "bannedBy": 100
      }
    ]
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

---

### Unban User

Remove a user from the ban list (owner only).

**Endpoint:** `DELETE /groups/:groupId/bans/:userId`

**Authentication:** Required

**Scopes:** `groups:write`

**CURL Example:**
```bash
curl -X DELETE "https://api.tradecraft.finance/v1/groups/1/bans/102" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "message": "User unbanned successfully"
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

---

### Get Group Messages

Fetch chat messages from a group in descending order (newest first).

**Endpoint:** `GET /groups/:groupId/messages`

**Authentication:** Required

**Scopes:** `groups:read`

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | integer | 50 | Results per page (max: 100) |
| `before` | integer | - | Message ID cursor for pagination |

**CURL Example:**
```bash
curl -X GET "https://api.tradecraft.finance/v1/groups/1/messages?limit=50" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**CURL Example (pagination):**
```bash
curl -X GET "https://api.tradecraft.finance/v1/groups/1/messages?limit=50&before=12345" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "messages": [
      {
        "id": 12350,
        "userId": 100,
        "username": "trader_alice",
        "content": "Just bought some SOL!",
        "messageType": "text",
        "metadata": {},
        "edited": false,
        "editedAt": null,
        "createdAt": "2024-01-15T10:30:00.000Z",
        "replyTo": null
      },
      {
        "id": 12345,
        "userId": 101,
        "username": "trader_bob",
        "content": "Nice entry!",
        "messageType": "text",
        "metadata": {},
        "edited": false,
        "editedAt": null,
        "createdAt": "2024-01-15T10:25:00.000Z",
        "replyTo": null
      }
    ],
    "pagination": {
      "hasMore": true,
      "nextCursor": 12345
    }
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

To get older messages, use the `nextCursor` value as the `before` parameter in your next request.

---

### Send Message

Send a chat message to a group.

**Endpoint:** `POST /groups/:groupId/messages`

**Authentication:** Required

**Scopes:** `groups:write`

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `content` | string | Yes | Message content |
| `messageType` | string | No | Message type (default: "text") |
| `metadata` | object | No | Additional metadata |
| `replyToId` | integer | No | ID of message being replied to |

**CURL Example:**
```bash
curl -X POST "https://api.tradecraft.finance/v1/groups/1/messages" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Hello everyone!"
  }'
```

**CURL Example (with reply):**
```bash
curl -X POST "https://api.tradecraft.finance/v1/groups/1/messages" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Great point!",
    "replyToId": 12345
  }'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "message": {
      "id": 12351,
      "userId": 100,
      "username": "trader_alice",
      "content": "Hello everyone!",
      "messageType": "text",
      "metadata": {},
      "replyTo": null,
      "createdAt": "2024-01-15T10:30:00.000Z"
    }
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

**Error Codes:**
- `NOT_A_MEMBER` (403): Not a member of this group
- `USER_MUTED` (403): You are muted in this group
- `RATE_LIMITED` (429): Sending messages too quickly
- `MESSAGE_BLOCKED` (400): Message content was blocked

---

### Mark Messages as Read

Mark messages as read up to a specific message ID.

**Endpoint:** `POST /groups/:groupId/read`

**Authentication:** Required

**Scopes:** `groups:write`

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `messageId` | integer | No | Mark all messages up to this ID as read |

**CURL Example:**
```bash
curl -X POST "https://api.tradecraft.finance/v1/groups/1/read" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "messageId": 12350
  }'
```

**Response:**
```json
{
  "success": true,
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

---

### Get Unread Count

Get the number of unread messages in a group.

**Endpoint:** `GET /groups/:groupId/unread`

**Authentication:** Required

**Scopes:** `groups:read`

**CURL Example:**
```bash
curl -X GET "https://api.tradecraft.finance/v1/groups/1/unread" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "unreadCount": 5
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

---

### Get Group Positions

Get all shared positions from group members.

**Endpoint:** `GET /groups/:groupId/positions`

**Authentication:** Required

**Scopes:** `groups:read`, `trade:read`

**CURL Example:**
```bash
curl -X GET "https://api.tradecraft.finance/v1/groups/1/positions" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "positions": [
      {
        "id": 500,
        "userId": null,
        "username": "trader_alice",
        "tokenAddress": "So11111111111111111111111111111111111111112",
        "tokenName": "Wrapped SOL",
        "tokenSymbol": "SOL",
        "tokenImage": "https://...",
        "amountTokens": 1000000,
        "amountSol": 0.5,
        "currentPrice": 0.0000006,
        "pnlPercent": 20,
        "pnlSol": 0.1,
        "openedAt": "2024-01-15T08:00:00.000Z"
      }
    ],
    "meta": {
      "groupId": 1,
      "tradingEnabled": true,
      "positionsVisible": true
    }
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "requestId": "req_abc123"
  }
}
```

Note: `userId` is only shown for your own positions. Other members' positions show `userId: null` for privacy.

---

## Complete Workflow Examples

### Example 1: Complete Buy Flow

Execute a token purchase from start to finish:

```bash
# Step 1: List wallets to find one with trading enabled
curl -X GET "https://api.tradecraft.finance/v1/wallets" \
  -H "Authorization: Bearer YOUR_API_KEY"

# Step 2: Execute buy order
curl -X POST "https://api.tradecraft.finance/v1/trade/buy" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tokenAddress": "TOKEN_MINT_ADDRESS",
    "walletId": 42,
    "solAmount": 0.1,
    "slippagePercentage": 10
  }'

# Step 3: Check position status
curl -X GET "https://api.tradecraft.finance/v1/positions?status=open" \
  -H "Authorization: Bearer YOUR_API_KEY"

# Step 4: View trade history
curl -X GET "https://api.tradecraft.finance/v1/positions/trades?action=buy" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Example 2: Signal Source Monitoring

Monitor and act on trading signals:

```bash
# Step 1: List available signal sources
curl -X GET "https://api.tradecraft.finance/v1/signals/sources?category=telegram" \
  -H "Authorization: Bearer YOUR_API_KEY"

# Step 2: Subscribe to a source
curl -X POST "https://api.tradecraft.finance/v1/signals/sources/1/subscribe" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"paymentMethod": "FREE"}'

# Step 3: Poll for new signals (implement continuous polling)
curl -X GET "https://api.tradecraft.finance/v1/signals/sources/1/signals?limit=10" \
  -H "Authorization: Bearer YOUR_API_KEY"

# Step 4: Execute trades based on signals
curl -X POST "https://api.tradecraft.finance/v1/trade/buy" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tokenAddress": "SIGNAL_TOKEN_ADDRESS",
    "walletId": 42,
    "solAmount": 0.5
  }'
```

### Example 3: Group Trading Setup

Create and manage a trading group:

```bash
# Step 1: Create a new group
curl -X POST "https://api.tradecraft.finance/v1/groups" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alpha Traders",
    "tradingEnabled": true,
    "positionsVisible": true,
    "maxMembers": 25
  }'

# Step 2: Get invite code
curl -X GET "https://api.tradecraft.finance/v1/groups/1/invite" \
  -H "Authorization: Bearer YOUR_API_KEY"

# Step 3: Share invite code with members (they join via web UI or API)

# Step 4: View group positions
curl -X GET "https://api.tradecraft.finance/v1/groups/1/positions" \
  -H "Authorization: Bearer YOUR_API_KEY"

# Step 5: Send messages to group
curl -X POST "https://api.tradecraft.finance/v1/groups/1/messages" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"content": "Just bought SOL at great entry!"}'
```

### Example 4: Wallet Management

Create and configure wallets for trading:

```bash
# Step 1: Create a new Privy-managed wallet
curl -X POST "https://api.tradecraft.finance/v1/wallets" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "Bot Trading Wallet"}'

# Step 2: Enable trading (requires frontend activation first)
curl -X POST "https://api.tradecraft.finance/v1/wallets/44/enable-trading" \
  -H "Authorization: Bearer YOUR_API_KEY"

# Step 3: Check wallet balance before trading
curl -X GET "https://api.tradecraft.finance/v1/wallets" \
  -H "Authorization: Bearer YOUR_API_KEY"

# Step 4: Execute trades with the wallet
curl -X POST "https://api.tradecraft.finance/v1/trade/buy" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tokenAddress": "TOKEN_ADDRESS",
    "walletId": 44,
    "solAmount": 1.0
  }'
```

---

## HTTP Status Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Success |
| 201 | Created | New resource created |
| 400 | Bad Request | Validation error or invalid parameters |
| 401 | Unauthorized | Missing or invalid API key |
| 403 | Forbidden | Insufficient permissions or blocked action |
| 404 | Not Found | Resource doesn't exist |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server-side error |
| 503 | Service Unavailable | Service temporarily unavailable |

---

## Error Code Reference

### Authentication Errors

| Code | Description |
|------|-------------|
| `INVALID_API_KEY` | API key is invalid or expired |
| `INSUFFICIENT_SCOPE` | API key lacks required permission scope |

### Agent Beta Program Errors

| Code | Description |
|------|-------------|
| `DUPLICATE_APPLICATION` | Email already has a pending or approved application |
| `INVALID_APPLICATION` | Invalid application ID |
| `INVALID_TOKEN` | Invalid or expired approval token |
| `APPLICATION_NOT_APPROVED` | Application not yet approved |
| `INVALID_SCOPES` | One or more requested scopes are invalid |
| `KEY_LIMIT_EXCEEDED` | Maximum number of keys reached for this agent |
| `REJECTED` | Application was rejected |

### Trading Errors

| Code | Description |
|------|-------------|
| `INVALID_TOKEN_ADDRESS` | Invalid or malformed token mint address |
| `INVALID_WALLET_ID` | Invalid or missing wallet ID |
| `INVALID_AMOUNT` | Invalid SOL or token amount |
| `WALLET_NOT_FOUND` | Wallet doesn't exist or doesn't belong to user |
| `TRADING_DISABLED` | Trading is disabled for this wallet |
| `TRADE_EXECUTION_FAILED` | Transaction failed on-chain |
| `INVALID_POSITION_ID` | Invalid position ID |
| `POSITION_NOT_FOUND` | Position doesn't exist or doesn't belong to user |
| `INSUFFICIENT_TOKENS` | Not enough tokens to sell |

### Wallet Errors

| Code | Description |
|------|-------------|
| `SERVICE_UNAVAILABLE` | Privy wallet service not configured |
| `PRIVY_ACCOUNT_REQUIRED` | User must have Privy account |
| `WALLET_EXISTS` | Wallet with this address already exists |

### Signal Source Errors

| Code | Description |
|------|-------------|
| `SOURCE_NOT_FOUND` | Signal source doesn't exist |
| `SOURCE_NOT_AVAILABLE` | Source is not approved or active |
| `ALREADY_SUBSCRIBED` | Already have active subscription |
| `NOT_FREE` | Source requires payment |
| `NOT_WHITELISTED` | Not on whitelist for this source |
| `MISSING_TRANSACTION` | Transaction signature required for SOL payment |
| `MISSING_WALLET` | Wallet required for HODL verification |
| `ACCESS_DENIED` | No active subscription to this source |

### Group Errors

| Code | Description |
|------|-------------|
| `NOT_GROUP_MEMBER` | Not a member of the specified group |
| `INVALID_INVITE_CODE` | Invalid or malformed invite code |
| `FORBIDDEN` | Banned from group or insufficient permissions |
| `BAD_REQUEST` | Already a member or group is full |
| `NOT_A_MEMBER` | Not a member of this group |
| `USER_MUTED` | You are muted in this group |
| `MESSAGE_BLOCKED` | Message content was blocked |

### General Errors

| Code | Description |
|------|-------------|
| `RATE_LIMITED` | Too many requests - implement backoff |
| `NOT_FOUND` | Requested resource doesn't exist |
| `INTERNAL_ERROR` | Server-side error |
| `VALIDATION_ERROR` | Request body validation failed |

---

## LLM Integration Guide

### Best Practices

When integrating this API with LLMs or automated systems:

1. **Always check `success` field** before accessing `data` in responses
2. **Handle pagination properly** by checking `hasMore` and using cursor values
3. **Respect rate limits** - implement exponential backoff on 429 responses
4. **Store your API key securely** - never expose it in client-side code or logs
5. **Use appropriate scopes** - request only the permissions you need
6. **Check error codes** - handle specific errors with appropriate retry logic
7. **Implement idempotency** - use unique identifiers to prevent duplicate operations
8. **Monitor API health** - regularly call `/health` endpoint
9. **Handle network errors** - implement timeout and retry mechanisms
10. **Log requests and responses** - maintain audit trail for debugging

### Rate Limit Handling

```python
import time
import requests

def api_call_with_backoff(url, headers, max_retries=3):
    for attempt in range(max_retries):
        response = requests.get(url, headers=headers)

        if response.status_code == 429:
            wait_time = 2 ** attempt  # Exponential backoff
            time.sleep(wait_time)
            continue

        return response

    raise Exception("Max retries exceeded")
```

### Pagination Pattern

```python
def fetch_all_positions(api_key):
    positions = []
    offset = 0
    limit = 100

    while True:
        response = requests.get(
            f"https://api.tradecraft.finance/v1/positions?limit={limit}&offset={offset}",
            headers={"Authorization": f"Bearer {api_key}"}
        )

        data = response.json()
        if not data["success"]:
            break

        positions.extend(data["data"]["positions"])

        if not data["data"]["pagination"]["hasMore"]:
            break

        offset += limit

    return positions
```

### Error Handling Pattern

```python
def safe_api_call(url, headers):
    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        if not data["success"]:
            error_code = data["error"]["code"]

            if error_code == "INSUFFICIENT_SCOPE":
                # Handle permission error
                pass
            elif error_code == "RATE_LIMITED":
                # Implement backoff
                pass
            else:
                # Log and handle other errors
                pass

        return data["data"]

    except requests.exceptions.RequestException as e:
        # Handle network errors
        pass
```

---

## Additional Resources

- **Web Application**: https://app.tradecraft.finance
- **Documentation**: https://docs.tradecraft.finance
- **Support**: support@tradecraft.finance
- **API Status**: https://status.tradecraft.finance
