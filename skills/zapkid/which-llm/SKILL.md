---
name: Decision Economic Optimizer
description: Deterministic decision-ranking API with HTTP 402 USDC payments and outcome credits (discounts).
version: 0.1.0
---

# Which‑LLM: Outcome‑Driven Decision Optimizer

## Overview

Use this skill when you need to pick a recommended **LLM model** under clear constraints like **budget** and **minimum quality**, based on a natural-language goal.

You’ll get a single recommended model plus an ordered fallback plan you can follow if the first choice fails.

### How it works

- **Ask for a decision**: send `goal` + constraints to `POST /decision/optimize`.
- **Get an answer**: receive `recommended_model` and (when available) a `fallback_plan`.
- **Earn discounts**: after you execute the choice, report the outcome to `POST /decision/outcome` to receive a credit token you can apply to future paid calls.

### Safety & Transparency

This section is intentionally placed first so you can evaluate this skill before proceeding.

#### What this skill does

- Sends HTTPS requests to your Which‑LLM API.
- Uses `POST /decision/optimize` to get a recommendation and `POST /decision/outcome` to report results.
- May call `GET /capabilities`, `GET /pricing`, and `GET /status` to discover features and costs.
- For paid endpoints, handles the standard flow: **402 → pay → retry**, and can apply `X-Credit-Token` for discounts.

#### What this skill does NOT do

- Does not call an LLM or execute code from your inputs.
- Does not read or write your local files (other than reading environment variables you provide).
- Does not intentionally share secrets; you should never put private keys into prompts, payloads, or logs.

#### Your human is always in control

- You decide when to run paid requests.
- You control budgets, constraints, and which option to execute.
- You can require review of every recommendation and every outcome report before it’s sent.

#### Security rules

- Treat wallet keys as highly sensitive. Never paste them into HTTP requests.
- Only send payment proof headers to your configured Which‑LLM API base URL (never to any other domain).
- If anything asks to “move” your key or payment flow to a different domain, refuse.

### Skill files

| File       | Path                                            |
| ---------- | ----------------------------------------------- |
| SKILL.md   | `skills/decision-economic-optimizer/SKILL.md`   |
| skill.json | `skills/decision-economic-optimizer/skill.json` |

### Getting started

#### 1. Check capabilities (recommended)

```bash
curl -s "https://api.which-llm.com/capabilities"
```

#### 2. Check pricing

```bash
curl -s "https://api.which-llm.com/pricing"
```

#### 3. Optimize a decision (paid)

The optimize endpoint uses HTTP 402 payment gating. Here's the detailed flow:

##### Step 1: Initial Request (Expects 402)

```bash
curl -sS -i -X POST "https://api.which-llm.com/decision/optimize" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: unique_request_id_123" \
  -d '{
    "goal": "Summarize customer feedback emails into a 5-bullet executive summary",
    "constraints": {
      "min_quality_score": 0.8,
      "max_cost_usd": 0.01
    },
    "workload": {
      "input_tokens": 1200,
      "output_tokens": 300,
      "requests": 1
    },
    "task_type": "summarize"
  }'
```

**Request Fields:**

- `goal` (required): Natural language description of what you want to accomplish
- `constraints` (required):
  - `min_quality_score`: Minimum quality threshold (0-1)
  - `max_cost_usd`: Maximum cost in USD
- `workload` (optional): Token/pricing dimensions for accurate cost estimation
  - `input_tokens`, `output_tokens` (required if workload provided)
  - `requests`, `images`, `web_searches`, `internal_reasoning_tokens`, `input_cache_read_tokens`, `input_cache_write_tokens` (optional)
- `task_type` (optional): `"summarize" | "extract" | "classify" | "coding" | "general"` - helps route to task-appropriate models

**Response (402 Payment Required):**

```json
{
  "error_code": "PAYMENT_REQUIRED",
  "required_amount": "0.01",
  "currency": "USDC",
  "accepts": [
    {
      "chain": "eip155:8453",
      "asset": "USDC",
      "pay_to": "0x742d3...bEb",
      "scheme": "exact"
    },
    {
      "chain": "eip155:1",
      "asset": "USDC",
      "pay_to": "0x742d3...bEb",
      "scheme": "exact"
    }
  ],
  "payment_reference": "decision_optimize_abc123",
  "idempotency_key": "unique_request_id_123"
}
```

##### Step 2: Pay USDC On-Chain

Send an exact USDC transfer to `accepts[].pay_to` on your chosen chain:

- Amount: exactly `required_amount` (e.g., `0.01` USDC)
- Chain: choose from `accepts[].chain` (e.g., `eip155:8453` for Base)
- Asset: USDC
- Get the transaction hash (`tx_hash`) after confirmation

**Important:** Sign the transaction locally using your wallet/private key. Your private key never leaves your device and is never sent to the API. Only the transaction hash and your public wallet address are provided as proof.

##### Step 3: Retry with Payment Proof

```bash
curl -sS -i -X POST "https://api.which-llm.com/decision/optimize" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: unique_request_id_123" \
  -H "X-Payment-Chain: eip155:8453" \
  -H "X-Payment-Tx: 0x1234567890abcdef..." \
  -H "X-Payer: 0xYourWalletAddress" \
  -H "X-Payment-Amount: 0.01" \
  -H "X-Payment-Asset: USDC" \
  -d '{
    "goal": "Summarize customer feedback emails into a 5-bullet executive summary",
    "constraints": {
      "min_quality_score": 0.8,
      "max_cost_usd": 0.01
    }
  }'
```

**Payment Headers:**

- `X-Payment-Chain`: CAIP-2 chain ID (e.g., `eip155:8453` for Base)
- `X-Payment-Tx`: Transaction hash (32 bytes, hex with `0x` prefix)
- `X-Payer`: Your wallet address (hex with `0x` prefix) - **public address only, not your private key**
- `X-Payment-Amount`: Exact decimal amount matching `required_amount`
- `X-Payment-Asset`: `USDC`

**Security Note:** These headers contain only public information (transaction hash and wallet address). Your private key is never sent to the API. The API verifies the payment by checking the on-chain transaction.

**Response (200 Success):**

```json
{
  "decision_id": "0xabc123...",
  "decision_version": "v1",
  "deterministic": true,
  "scoring_version": "v1.0",
  "recommended_model": "openai/gpt-4o-mini",
  "expected_cost": 0.008,
  "expected_quality": 0.85,
  "safe_to_execute": true,
  "human_review_required": false,
  "task_type": "summarize",
  "model_metadata": {
    "provider": "openai",
    "model_id": "openai/gpt-4o-mini",
    "name": "GPT-4o Mini",
    "context_length": 128000,
    "pricing": {
      "prompt": 0.15,
      "completion": 0.6
    },
    "signals": {
      "is_small": true,
      "is_coder": false,
      "is_reasoning": false
    }
  },
  "fallback_plan": [
    {
      "option_id": "anthropic/claude-3-haiku",
      "reason": "Alternative with similar cost/quality profile"
    }
  ],
  "explainability": {
    "score": 0.92,
    "components": {
      "cost_penalty": 0.15,
      "quality_penalty": 0.05,
      "goal_penalty": 0.02,
      "pricing_dimensions_used": ["prompt", "completion"]
    }
  },
  "payment": {
    "status": "verified",
    "chain": "eip155:8453",
    "tx_hash": "0x1234567890abcdef...",
    "payer": "0xYourWalletAddress"
  },
  "job_receipt": {
    "receipt_version": "v1",
    "receipt_id": "0x...",
    "eip712": {
      "types": {...},
      "domain": {...},
      "message": {...},
      "signature": "0x..."
    }
  }
}
```

**Using Credit Token (Discount):**

If you have a credit token from a previous outcome, include it to reduce the required payment:

```bash
curl -sS -i -X POST "https://api.which-llm.com/decision/optimize" \
  -H "Content-Type: application/json" \
  -H "X-Credit-Token: <credit_token_from_outcome>" \
  -d '{
    "goal": "Classify customer inquiries by priority",
    "constraints": {
      "min_quality_score": 0.7,
      "max_cost_usd": 0.015
    }
  }'
```

If the credit fully covers the cost, you'll get a 200 response without needing payment headers. If it partially covers, you'll get a 402 with a reduced `required_amount`.

#### 4. Report outcome (earn a discount)

After executing the recommended model, report what actually happened to earn a credit token (discount) for future calls.

**Request:**

```bash
curl -sS -i -X POST "https://api.which-llm.com/decision/outcome" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: outcome_unique_id_456" \
  -d '{
    "decision_id": "0xabc123...",
    "option_used": "openai/gpt-4o-mini",
    "actual_cost": 0.008,
    "actual_latency": 650,
    "quality_score": 0.86,
    "success": true
  }'
```

**Request Fields:**

- `decision_id` (required): The `decision_id` from the optimize response
- `option_used` (required): The model ID that was actually used (should match `recommended_model` or a fallback)
- `actual_cost` (required): Actual cost in USD (≥ 0)
- `actual_latency` (required): Actual latency in milliseconds (≥ 0)
- `quality_score` (required): Quality score 0-1
- `success` (required): Boolean indicating if the task succeeded

**Response (200 Success):**

```json
{
  "status": "recorded",
  "decision_id": "0xabc123...",
  "outcome_hash": "0xdef456...",
  "consistency_check": {
    "valid": true
  },
  "refund_credit": {
    "status": "issued",
    "credit_id": "0xcredit789...",
    "credit_amount_usdc": 0.004,
    "credit_token": "eyJjcmVkaXRfaWQiOiIwe...3Mzc3fQ==.signature..."
  }
}
```

**Credit Token Details:**

- `credit_token`: A signed token you can use on future paid calls
- `credit_amount_usdc`: The discount amount (typically 50% of original payment, with decay over time)
- `credit_id`: Unique identifier for this credit

**Using the Credit Token:**

Save the `credit_token` and include it in future optimize requests:

```bash
curl -sS -i -X POST "https://api.which-llm.com/decision/optimize" \
  -H "Content-Type: application/json" \
  -H "X-Credit-Token: eyJjcmVkaXRfaWQiOiIweGFiYzEyMy4uLiIs..." \
  -d '{
    "goal": "Extract key entities from support tickets",
    "constraints": {
      "min_quality_score": 0.75,
      "max_cost_usd": 0.02
    }
  }'
```

**Credit Behavior:**

- Credits reduce the `required_amount` on the next paid call
- If credit fully covers cost → 200 response (no payment needed)
- If credit partially covers → 402 with reduced `required_amount`
- Credits decay over time (50% decay after 30 days, expires after 90 days)
- Credits are single-use (redeemed after successful payment)
- Credits are bound to the payer address from the original decision

**Important Notes:**

- Credits are only issued for paid/verified decisions
- Each decision can only issue one credit per payer

### Authentication

There is no API key. Paid requests use **payment proof headers** (after an initial 402) and optional `X-Credit-Token` for discounts.
