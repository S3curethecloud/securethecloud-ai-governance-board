#!/usr/bin/env bash
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
