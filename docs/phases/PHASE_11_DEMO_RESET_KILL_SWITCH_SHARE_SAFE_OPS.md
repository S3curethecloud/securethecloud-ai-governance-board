# Phase 11 — Demo Reset / Kill Switch / Share-Safe Ops

## Status

Implementation Complete

## Purpose

Phase 11 makes the public AI Governance Board demo safer to share by adding protected reset controls and Fly.io public-demo lifecycle operations.

## Scope

Phase 11 adds:

- Protected seeded demo reset endpoint
- Fly secret-based reset token workflow
- Local reset validation procedure
- Public reset validation procedure
- Fly status, health, reset, off, on, and destroy controls
- Share-safe ops documentation
- README operations section
- Phase 11 evidence document

## Protected Reset Endpoint

```text
POST /api/demo/reset
```

Required owner-only header:

```text
X-Demo-Reset-Token
```

The endpoint restores the seeded in-memory AI governance demo records captured at application startup.

## Public Demo Boundary

This remains a simulated AI governance board.

No real patient data, customer data, regulated systems, clinical systems, production model runtimes, enterprise authorization systems, or production enforcement systems are connected.

## Fly Secret

The reset token must be configured as a Fly secret on the backend app:

```bash
fly secrets set DEMO_RESET_TOKEN="$DEMO_RESET_TOKEN" -a securethecloud-ai-governance-board-api
```

## Ops Controls

The following script was added:

```text
scripts/fly_demo_control.sh
```

Supported commands:

- `urls`
- `status`
- `health`
- `reset`
- `off`
- `on`
- `destroy`

## Completion Evidence

- Reset endpoint added
- Local reset token passthrough added to Docker Compose
- Fly demo control script added
- Share-safe ops documentation added
- README ops section added
- Phase 11 evidence document added
