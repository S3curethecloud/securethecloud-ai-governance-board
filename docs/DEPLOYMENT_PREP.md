Public Deployment Prep
Status

Prepared, not deployed.

Intended Future Deployment

Frontend app placeholder:

securethecloud-ai-governance-board

Backend API app placeholder:

securethecloud-ai-governance-board-api
Required Before Public Sharing
Confirm README public demo boundary is accurate
Confirm no secrets are committed
Confirm seeded data is simulated only
Confirm backend health endpoint works
Confirm frontend loads
Confirm board evidence export works
Confirm board decision memo works
Add reset or kill-switch controls in Phase 11
Add screenshots after public deployment
Validation Commands
docker compose down
docker compose up --build -d

sleep 20

curl http://localhost:8010/health
curl http://localhost:8010/api/dashboard
curl -I http://localhost:3010
Safety Boundary

The public demo must not claim:

production compliance
legal certification
HIPAA certification
EU AI Act compliance certification
NIST certification
real clinical review
real patient data review
real model runtime enforcement
real enterprise authorization enforcement
