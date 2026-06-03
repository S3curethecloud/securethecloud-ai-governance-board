# Share-Safe Demo Ops

## Public Demo URLs

Frontend:

```text
https://securethecloud-ai-governance-board.fly.dev
```

Backend API:

```text
https://securethecloud-ai-governance-board-api.fly.dev
```

## Public Demo Boundary

This is a simulated AI governance board.

No real patient data, customer data, regulated systems, clinical systems, production model runtimes, enterprise authorization systems, or production enforcement systems are connected.

## Protected Demo Reset

The backend exposes a protected reset endpoint:

```text
POST /api/demo/reset
```

Required header:

```text
X-Demo-Reset-Token: <owner reset token>
```

The reset token must be configured as a Fly secret:

```bash
fly secrets set DEMO_RESET_TOKEN="$DEMO_RESET_TOKEN" -a securethecloud-ai-governance-board-api
```

Reset public demo state:

```bash
curl -X POST "https://securethecloud-ai-governance-board-api.fly.dev/api/demo/reset" \
  -H "X-Demo-Reset-Token: $DEMO_RESET_TOKEN"
```

Expected response:

```json
{
  "status": "reset",
  "message": "Seeded AI governance board demo records restored"
}
```

## Local Reset Validation

```bash
export DEMO_RESET_TOKEN="local-dev-reset-token"

docker compose down
docker compose up --build -d

sleep 20

curl -X POST "http://localhost:8010/api/demo/reset" \
  -H "X-Demo-Reset-Token: $DEMO_RESET_TOKEN"
```

## Fly Demo Control Script

Show URLs:

```bash
scripts/fly_demo_control.sh urls
```

Check status:

```bash
scripts/fly_demo_control.sh status
```

Check public health:

```bash
scripts/fly_demo_control.sh health
```

Reset public demo:

```bash
export DEMO_RESET_TOKEN="<owner reset token>"
scripts/fly_demo_control.sh reset
```

Turn public demo off:

```bash
scripts/fly_demo_control.sh off
```

Turn public demo back on:

```bash
scripts/fly_demo_control.sh on
```

Permanently delete Fly apps:

```bash
CONFIRM_DESTROY=YES scripts/fly_demo_control.sh destroy
```

## Share Checklist

Before sharing the demo URL:

- Reset seeded demo state
- Confirm frontend loads
- Confirm backend health works
- Confirm dashboard telemetry loads
- Confirm public demo boundary language is visible
- Do not share the reset token
- Do not claim production compliance or production enforcement

## Safe Operating Rule

Share the frontend URL only.

Do not share the reset token, Fly account access, or any local environment variables.
