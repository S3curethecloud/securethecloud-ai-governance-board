# SecureTheCloud AI Governance Board

A simulated enterprise AI governance review platform for AI system intake, model registry review, risk classification, regulatory mapping, committee approval, evidence package reconstruction, and executive decision memo generation.

This project demonstrates how an organization can govern proposed AI systems before adoption, deployment, sensitive-data access, or production use.

## Client-Safe Demo Summary

SecureTheCloud AI Governance Board is a production-shaped lab, not a production enforcement system.

It shows how AI governance teams can:

- Intake proposed AI systems before deployment
- Capture business owner, model owner, department, use case, model provider, target users, data types, and deployment context
- Score AI system risk based on data exposure, PHI, patient impact, automated decisioning, financial impact, safety impact, and security impact
- Map AI system evidence to NIST AI RMF-style Govern, Map, Measure, and Manage categories
- Classify systems using EU AI Act-style categories: minimal, limited, high-risk, and prohibited
- Route systems through governance committee review
- Run HIPAA-style review for PHI and patient-impact use cases
- Reconstruct board/auditor-ready evidence timelines
- Generate evidence export packets and executive decision memos

## Correct Claim

This is a simulated AI governance board and evidence system.

It demonstrates the governance control pattern safely:

> AI systems should be reviewed, risk-scored, classified, mapped, approved, monitored, and supported by evidence before enterprise adoption.

## Incorrect Claims

Do not claim this lab is:

- A production AI governance system
- A legal, compliance, HIPAA, EU AI Act, or NIST certification tool
- Connected to real patient data
- Connected to customer records
- Connected to regulated production systems
- Connected to production model runtimes
- Connected to clinical decision systems
- Enforcing real enterprise authorization decisions
- Providing legal, clinical, regulatory, or compliance advice

## Public Demo Boundary

The demo uses seeded simulated AI governance records only.

No real clinical, patient, customer, regulated, production, authorization, model runtime, or enterprise systems are connected.

## Demo Walkthrough

A strong five-minute walkthrough:

1. Start at the executive overview.
   - Explain that this is a board-level AI governance operating model.
   - Point out the governance committee, model registry, NIST AI RMF, EU AI Act-style classifier, HIPAA-style review, and evidence package layers.

2. Show the AI system intake form.
   - Explain that proposed AI systems are captured before adoption or deployment.
   - Highlight ownership, use case, model provider, deployment environment, data types, impact flags, and approval status.

3. Preview a governance decision.
   - Show risk score, classification, required controls, and risk factors.
   - Explain that the platform makes governance decisions explainable before approval.

4. Show the committee review workspace.
   - Explain how pending, high-risk, PHI, or control-required systems can be approved, rejected, escalated, or sent back for controls.

5. Show regulatory mapping and HIPAA-style review.
   - Explain NIST AI RMF-style Govern, Map, Measure, Manage mapping.
   - Show EU AI Act-style classification and HIPAA-style evidence requirements.

6. Show the board audit trail.
   - Walk through intake, risk assessment, NIST mapping, EU AI Act-style classification, HIPAA-style review, committee decision, and final outcome.

7. Show the evidence export and board memo.
   - Explain that the platform generates board/auditor-ready JSON evidence and a copyable executive decision memo.

## Why This Matters

Most AI programs do not fail only because of model quality. They fail because organizations cannot answer basic governance questions:

- Who owns this AI system?
- What data does it touch?
- What business process does it affect?
- Is PHI, customer data, financial impact, safety impact, or automated decisioning involved?
- What risk class applies?
- What controls are required?
- Who approved it?
- What evidence proves the review happened?
- Can the decision be reconstructed later for audit, board review, or regulatory inquiry?

This lab demonstrates a control-plane pattern for answering those questions.

## Local Run

```bash
docker compose down
docker compose up --build -d

sleep 20

curl http://localhost:8010/health
curl http://localhost:8010/api/dashboard
curl -I http://localhost:3010

Open:

http://localhost:3010
Backend API Examples

Health:

curl http://localhost:8010/health

Dashboard:

curl http://localhost:8010/api/dashboard

List AI systems:

curl http://localhost:8010/api/ai-systems

Board evidence export:

SYSTEM_ID=$(curl -s http://localhost:8010/api/ai-systems | python3 -c 'import sys,json; data=json.load(sys.stdin); print(data[0]["system_id"])')

curl "http://localhost:8010/api/ai-systems/$SYSTEM_ID/board-evidence-export" | python3 -m json.tool

Board decision memo:

curl "http://localhost:8010/api/ai-systems/$SYSTEM_ID/board-decision-memo" | python3 -m json.tool
Evidence Export

The board evidence export demonstrates an audit-ready JSON payload containing:

AI system metadata
Ownership and use case
Deployment context
Risk score and classification
EU AI Act-style classification
HIPAA-style review flag
Required controls
Required evidence
NIST AI RMF-style mapping
Evidence timeline
Evidence completeness
Final governance outcome
Public demo safety boundary
Executive Decision Memo

The board memo gives a copyable executive summary for board, risk, audit, compliance, or governance stakeholders.

It explains:

What system was reviewed
What risk score was assigned
What classification was applied
What governance decision was reached
What controls are required
What evidence supports the decision
Why the demo is simulated and client-safe
Screenshot Placeholders

Recommended screenshots to add later:

docs/screenshots/01-executive-overview.png
docs/screenshots/02-ai-system-intake.png
docs/screenshots/03-governance-review.png
docs/screenshots/04-nist-eu-hipaa-mapping.png
docs/screenshots/05-board-audit-trail.png
docs/screenshots/06-evidence-export-memo.png
Public Deployment Prep

Deployment is intentionally not part of Phase 9.

Future Fly.io app names can follow this pattern:

securethecloud-ai-governance-board
securethecloud-ai-governance-board-api

Future deployment should preserve:

Public demo boundary language
No real data connections
No production enforcement claims
No secrets committed to Git
Reset or kill-switch plan before public sharing
Current Phase

Phase 9 prepares the repository for public demo deployment.

Next phases:

Phase 10 — Fly.io Public Demo Deployment
Phase 11 — Demo Reset / Kill Switch / Share-Safe Ops

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

## Public Demo

Frontend:

```text
https://securethecloud-ai-governance-board.fly.dev

Backend API:

https://securethecloud-ai-governance-board-api.fly.dev
How to Review This Demo

Recommended review path:

Open the public frontend demo.
Start with the executive overview and governance operating model.
Review the AI system intake workflow.
Preview a governance decision and required controls.
Open the governance committee review workspace.
Review NIST AI RMF-style mapping and EU AI Act-style classification.
Review the HIPAA-style AI review board workflow.
Inspect the board audit trail.
Use the Board Evidence Export panel to download or copy the audit-ready JSON evidence packet and executive board decision memo.
Portfolio Screenshots
Screenshot	Description
docs/screenshots/01-executive-overview.png	Executive overview and governance operating model
docs/screenshots/02-ai-system-intake.png	AI system intake and governance preview
docs/screenshots/03-governance-review.png	Governance committee review workspace
docs/screenshots/04-nist-eu-hipaa-mapping.png	NIST AI RMF, EU AI Act-style, and HIPAA-style review panels
docs/screenshots/05-board-audit-trail.png	Evidence timeline and board audit trail
docs/screenshots/06-evidence-export-memo.png	Evidence export and executive decision memo
docs/screenshots/07-mobile-responsive.png	Mobile responsive demo view
Share-Safe Summary

This is a simulated, production-shaped AI governance board.

It is safe to share as a portfolio/client demo because it does not connect to real patient data, customer records, regulated production systems, production model runtimes, clinical decision systems, enterprise authorization systems, or production enforcement systems.

Correct claim:

SecureTheCloud AI Governance Board demonstrates AI system intake, risk classification, governance committee review, regulatory mapping, evidence reconstruction, and board-ready evidence export in a simulated environment.
