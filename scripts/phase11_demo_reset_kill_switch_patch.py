from pathlib import Path
from textwrap import dedent
import re
import stat

root = Path(".")
backend_main = root / "backend" / "app" / "main.py"
compose = root / "docker-compose.yml"
docs = root / "docs"
ops = docs / "ops"
phases = docs / "phases"
readme = root / "README.md"
scripts = root / "scripts"

ops.mkdir(parents=True, exist_ok=True)
phases.mkdir(parents=True, exist_ok=True)
scripts.mkdir(exist_ok=True)

# ---------------------------------------------------------------------
# Backend reset endpoint
# ---------------------------------------------------------------------
s = backend_main.read_text()

def ensure_fastapi_import(text: str, required: list[str]) -> str:
    pattern = re.compile(r"^from fastapi import ([^\n]+)$", re.MULTILINE)
    match = pattern.search(text)

    if not match:
        return "from fastapi import " + ", ".join(required) + "\n" + text

    current = [x.strip() for x in match.group(1).split(",")]
    for name in required:
        if name not in current:
            current.append(name)

    new_line = "from fastapi import " + ", ".join(current)
    return text[:match.start()] + new_line + text[match.end():]

s = ensure_fastapi_import(s, ["HTTPException", "Request"])

phase11_block = dedent(r'''
# ---------------------------------------------------------------------
# Phase 11 — Protected demo reset endpoint
# ---------------------------------------------------------------------
# This endpoint is for demo hygiene only. It restores the seeded in-memory
# AI governance records captured at application startup. It does not connect
# to real patient data, customer data, regulated systems, production model
# runtimes, clinical systems, or enterprise authorization systems.

import copy as _phase11_copy
import os as _phase11_os


def _phase11_find_ai_system_store():
    preferred_names = [
        "AI_SYSTEMS",
        "ai_systems",
        "AI_SYSTEM_RECORDS",
        "ai_system_records",
        "AI_SYSTEM_STORE",
        "ai_system_store",
        "SYSTEMS",
        "systems",
        "SEEDED_AI_SYSTEMS",
        "seeded_ai_systems",
    ]

    for name in preferred_names:
        value = globals().get(name)
        if isinstance(value, list):
            return value

    for value in globals().values():
        if not isinstance(value, list) or not value:
            continue

        first = value[0]

        if isinstance(first, dict) and (
            "system_id" in first or "system_name" in first or "model_name" in first
        ):
            return value

        if any(hasattr(first, attr) for attr in ("system_id", "system_name", "model_name")):
            return value

    raise RuntimeError("AI governance demo store was not found")


_PHASE11_DEMO_BASELINE = _phase11_copy.deepcopy(_phase11_find_ai_system_store())


@app.post("/api/demo/reset")
def phase11_demo_reset(request: Request):
    configured_token = _phase11_os.getenv("DEMO_RESET_TOKEN")

    if not configured_token:
        raise HTTPException(
            status_code=503,
            detail="Demo reset token is not configured",
        )

    supplied_token = request.headers.get("X-Demo-Reset-Token", "")

    if supplied_token != configured_token:
        raise HTTPException(
            status_code=403,
            detail="Invalid demo reset token",
        )

    store = _phase11_find_ai_system_store()
    store.clear()
    store.extend(_phase11_copy.deepcopy(_PHASE11_DEMO_BASELINE))

    return {
        "status": "reset",
        "reset_records": len(store),
        "message": "Seeded AI governance board demo records restored",
        "lab_mode": True,
        "public_demo_boundary": "Simulated AI governance workflow only. No real patient data, customer data, regulated systems, production model runtime, clinical decision systems, or enterprise authorization systems are connected.",
    }
''').strip()

if "/api/demo/reset" not in s:
    s = s.rstrip() + "\n\n\n" + phase11_block + "\n"
    backend_main.write_text(s)
    print("Added protected demo reset endpoint.")
else:
    print("Protected demo reset endpoint already present.")

# ---------------------------------------------------------------------
# docker-compose local reset token passthrough
# ---------------------------------------------------------------------
if compose.exists():
    c = compose.read_text()
    if "DEMO_RESET_TOKEN" not in c:
        if "  backend:\n" not in c:
            raise SystemExit("Could not find backend service in docker-compose.yml")
        c = c.replace(
            "  backend:\n",
            "  backend:\n"
            "    environment:\n"
            "      DEMO_RESET_TOKEN: ${DEMO_RESET_TOKEN:-local-dev-reset-token}\n",
            1,
        )
        compose.write_text(c)
        print("Added local DEMO_RESET_TOKEN environment passthrough.")
    else:
        print("docker-compose.yml already contains DEMO_RESET_TOKEN.")

# ---------------------------------------------------------------------
# Fly control script
# ---------------------------------------------------------------------
fly_control = scripts / "fly_demo_control.sh"
fly_control.write_text(dedent(r'''#!/usr/bin/env bash
set -euo pipefail

API_APP="${API_APP:-securethecloud-ai-governance-board-api}"
FRONTEND_APP="${FRONTEND_APP:-securethecloud-ai-governance-board}"
API_URL="https://${API_APP}.fly.dev"
FRONTEND_URL="https://${FRONTEND_APP}.fly.dev"

command="${1:-status}"

usage() {
  cat <<USAGE
Usage: scripts/fly_demo_control.sh <command>

Commands:
  urls          Show public demo URLs
  status        Show Fly status for frontend and backend
  health        Check public frontend/API health
  reset         Reset seeded public demo state using DEMO_RESET_TOKEN
  off           Scale frontend and backend to zero
  on            Scale backend and frontend back to one machine
  destroy       Permanently delete both Fly apps; requires CONFIRM_DESTROY=YES

Environment:
  API_APP       Defaults to securethecloud-ai-governance-board-api
  FRONTEND_APP  Defaults to securethecloud-ai-governance-board
  DEMO_RESET_TOKEN required for reset
USAGE
}

case "$command" in
  urls)
    echo "Frontend: ${FRONTEND_URL}"
    echo "Backend:  ${API_URL}"
    ;;

  status)
    echo "== Frontend status =="
    fly status -a "$FRONTEND_APP"
    echo
    echo "== Backend status =="
    fly status -a "$API_APP"
    ;;

  health)
    echo "== Backend health =="
    curl -sS "${API_URL}/health"
    echo
    echo "== Backend dashboard =="
    curl -sS "${API_URL}/api/dashboard"
    echo
    echo "== Frontend headers =="
    curl -I "${FRONTEND_URL}"
    ;;

  reset)
    : "${DEMO_RESET_TOKEN:?Set DEMO_RESET_TOKEN before running reset}"
    curl -sS -X POST "${API_URL}/api/demo/reset" \
      -H "X-Demo-Reset-Token: ${DEMO_RESET_TOKEN}"
    echo
    ;;

  off|stop)
    echo "Scaling public demo apps to zero..."
    fly scale count 0 -a "$FRONTEND_APP" --yes
    fly scale count 0 -a "$API_APP" --yes
    echo "Public demo scaled down."
    ;;

  on|start)
    echo "Scaling public demo apps back to one machine..."
    fly scale count 1 -a "$API_APP" --yes
    fly scale count 1 -a "$FRONTEND_APP" --yes
    echo "Public demo scaled up."
    ;;

  destroy|delete)
    if [[ "${CONFIRM_DESTROY:-NO}" != "YES" ]]; then
      echo "Refusing to destroy Fly apps."
      echo "Run with CONFIRM_DESTROY=YES only when you want to permanently delete the public demo apps."
      exit 1
    fi

    echo "Destroying frontend app: ${FRONTEND_APP}"
    fly apps destroy "$FRONTEND_APP" --yes

    echo "Destroying backend app: ${API_APP}"
    fly apps destroy "$API_APP" --yes

    echo "Fly demo apps destroyed."
    ;;

  help|-h|--help)
    usage
    ;;

  *)
    usage
    exit 1
    ;;
esac
'''))

mode = fly_control.stat().st_mode
fly_control.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
print("Wrote scripts/fly_demo_control.sh")

# ---------------------------------------------------------------------
# Ops documentation
# ---------------------------------------------------------------------
(ops / "SHARE_SAFE_OPS.md").write_text(dedent(r'''
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
''').strip() + "\n")

# ---------------------------------------------------------------------
# Phase evidence doc
# ---------------------------------------------------------------------
(phases / "PHASE_11_DEMO_RESET_KILL_SWITCH_SHARE_SAFE_OPS.md").write_text(dedent(r'''
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
''').strip() + "\n")

# ---------------------------------------------------------------------
# README ops section
# ---------------------------------------------------------------------
if readme.exists():
    r = readme.read_text()
else:
    r = "# SecureTheCloud AI Governance Board\n"

readme_section = dedent(r'''
## Share-Safe Demo Operations

The public demo includes protected reset and Fly lifecycle controls.

### Public Demo URLs

Frontend:

```text
https://securethecloud-ai-governance-board.fly.dev
```

Backend API:

```text
https://securethecloud-ai-governance-board-api.fly.dev
```

### Reset Seeded Demo State

The reset endpoint is protected by an owner reset token.

```bash
export DEMO_RESET_TOKEN="<owner reset token>"

curl -X POST "https://securethecloud-ai-governance-board-api.fly.dev/api/demo/reset" \
  -H "X-Demo-Reset-Token: $DEMO_RESET_TOKEN"
```

### Fly Demo Control

```bash
scripts/fly_demo_control.sh status
scripts/fly_demo_control.sh health
scripts/fly_demo_control.sh reset
scripts/fly_demo_control.sh off
scripts/fly_demo_control.sh on
```

Permanent deletion requires explicit confirmation:

```bash
CONFIRM_DESTROY=YES scripts/fly_demo_control.sh destroy
```

### Share-Safe Rule

Share only the frontend URL.

Do not share the reset token, Fly account access, or local environment variables.
''').strip()

if "## Share-Safe Demo Operations" not in r:
    readme.write_text(r.rstrip() + "\n\n" + readme_section + "\n")
    print("README ops section added.")
else:
    print("README ops section already present.")

print("Phase 11 demo reset / kill switch / share-safe ops patch complete.")
