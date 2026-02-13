---
name: seisoai
description: SeisoAI x402 protocol skill for OpenClaw/Claw agents. Execute paid requests with strict 402 challenge->pay->retry handling and queue-safe polling.
metadata: {"openclaw":{"homepage":"https://seisoai.com","emoji":":art:"}}
version: 1.4.0
last_synced: 2026-02-12
---

# SeisoAI x402 (OpenClaw)

Base URL: `https://seisoai.com`

## Purpose

Use this skill for paid requests on SeisoAI endpoints.

This skill is protocol-first:
- no account/session assumptions
- no browser CSRF assumptions
- deterministic 402 handling

## Supported route families for x402

Use task-specific endpoints such as:
- `/api/generate/*`
- `/api/audio/*`
- `/api/image-tools/*`
- `/api/model3d/*`
- `/api/training/*`
- `/api/workflows/*`
- `/api/prompt-lab/chat`
- `/api/extract-layers`

## Core x402 algorithm (mandatory)

1. Build request (`method`, `path`, `jsonBody`).
2. Send request without payment header.
3. If response is `402`:
   - read JSON body payment requirements
   - also read `PAYMENT-REQUIRED` header (base64 JSON) if present
4. Sign payment for the challenged resource.
   - always direct payment to the exact `accepts[].payTo` wallet from the challenge
   - never substitute or override destination wallet from local defaults
5. Retry the same request intent with exactly one header:
   - `payment-signature`, or
   - `x-payment`, or
   - `payment`
6. Handle paid response:
   - `2xx`: success
   - `402`: payment invalid/expired/insufficient -> regenerate payment and retry
   - `4xx/5xx`: follow error policy

## Payment signing boundary (mandatory)

1. Use only the runtime-managed payment signer provided by the OpenClaw host.
2. Never request, store, or derive raw private keys/seed phrases in this skill flow.
3. Never sign arbitrary payloads; only sign the x402 payment payload tied to the current 402 challenge.
4. If no authorized signer capability is available, fail closed and return: `payment signer unavailable`.
5. Do not auto-approve repeated payments; require a fresh sign operation for each new challenge.

## Invariants (do not violate)

1. Keep request intent identical between challenge and paid retry.
2. Do not mutate method/path semantics between retries.
3. Do not reuse stale or previously consumed payment signatures.
4. Treat successful queue submission as billable success.
5. Enforce destination wallet integrity: signed payment must target challenge `payTo`.

## Agent-native request patterns

Unpaid request:

```http
POST /api/generate/image
Host: seisoai.com
Content-Type: application/json

{"prompt":"cinematic mountain sunset","model":"flux-2","num_images":1}
```

Expected payment challenge shape:

```json
{
  "x402Version": 2,
  "error": "Payment required",
  "resource": { "url": "https://seisoai.com/api/generate/image" },
  "accepts": [
    {
      "scheme": "exact",
      "network": "eip155:8453",
      "asset": "USDC",
      "payTo": "0x...",
      "maxAmountRequired": "..."
    }
  ]
}
```

Paid retry:

```http
POST /api/generate/image
Host: seisoai.com
Content-Type: application/json
payment-signature: <signed-x402-payload>

{"prompt":"cinematic mountain sunset","model":"flux-2","num_images":1}
```

## Queue handling

When response indicates async/queued work:

1. Prefer explicit URLs returned by the endpoint.
2. If only `requestId` is returned for generate routes, poll:
   - `GET /api/generate/status/{requestId}`
   - `GET /api/generate/result/{requestId}`
3. Stop polling on terminal states (`COMPLETED`/`FAILED` or endpoint-specific equivalent).

## Error policy

- `400`: invalid input/schema -> fix payload fields/types.
- `402`: payment required/invalid/replayed -> regenerate payment and retry same intent.
- `404`: route/tool not found -> verify endpoint path.
- `429`: back off and retry with jitter.
- `500`: retry with bounded backoff; if repeated, downgrade model complexity.

## Common failure traps

1. Reusing a prior payment signature.
2. Changing payload intent between 402 challenge and paid retry.
3. Polling the wrong status/result route for queued jobs.
4. Treating 402 as fatal instead of payment handshake.
