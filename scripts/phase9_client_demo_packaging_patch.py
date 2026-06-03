from pathlib import Path
from textwrap import dedent

root = Path(".")
docs = root / "docs"
phases = docs / "phases"
screenshots = docs / "screenshots"

docs.mkdir(exist_ok=True)
phases.mkdir(parents=True, exist_ok=True)
screenshots.mkdir(parents=True, exist_ok=True)

readme = root / "README.md"

readme.write_text(dedent(r'''
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

''').strip() + "\n")

(docs / "CLIENT_DEMO_WALKTHROUGH.md").write_text(dedent(r'''

Client Demo Walkthrough
Demo URL

Local:

http://localhost:3010

Public demo URL will be added after deployment.

Client-Safe Opening

SecureTheCloud AI Governance Board is a simulated enterprise AI governance review platform.

It demonstrates how organizations can review proposed AI systems before adoption, deployment, sensitive-data access, or production use.

This demo does not connect to real patient data, customer data, regulated systems, production model runtimes, clinical systems, or enterprise authorization systems.

Five-Minute Walkthrough
1. Executive Overview

Show the board-level AI governance operating model.

Explain that the platform is designed around AI governance program questions:

Who owns the AI system?
What use case does it serve?
What data does it touch?
What risk class applies?
What controls are required?
What evidence proves the decision?
2. AI System Intake

Show the AI system intake form.

Highlight:

business owner
model owner
model provider
deployment environment
data types
PHI/customer data flags
patient, financial, safety, and security impact flags
3. Risk and Required Controls

Use preview to show:

risk score
risk classification
governance decision
risk factors
required controls
4. Committee Review

Show the review queue.

Explain that governance committee members can:

approve
reject
request controls
escalate
5. Regulatory Mapping

Show NIST AI RMF-style mapping:

Govern
Map
Measure
Manage

Show EU AI Act-style classification:

minimal
limited
high-risk
prohibited
6. HIPAA-Style Review

Show how PHI and patient-impact systems trigger additional review evidence.

7. Evidence Timeline

Show the board audit trail.

Explain that the governance decision can be reconstructed later.

8. Evidence Export and Board Memo

Show:

downloadable JSON evidence packet
copyable executive decision memo
public demo boundary
Closing Line

This lab demonstrates how an AI governance board can intake AI systems, classify risk, map regulatory evidence, route review, and generate board-ready evidence before enterprise AI adoption.
''').strip() + "\n")

(docs / "DEPLOYMENT_PREP.md").write_text(dedent(r'''

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
''').strip() + "\n")

(docs / "SCREENSHOTS.md").write_text(dedent(r'''

Screenshot Checklist

Add final screenshots before public launch.

Recommended Files
docs/screenshots/01-executive-overview.png
docs/screenshots/02-ai-system-intake.png
docs/screenshots/03-governance-review.png
docs/screenshots/04-nist-eu-hipaa-mapping.png
docs/screenshots/05-board-audit-trail.png
docs/screenshots/06-evidence-export-memo.png
Capture Guidance

Use screenshots that show:

the SecureTheCloud AI Governance Board title
client-safe demo boundary
governance operating model
AI system intake form
risk and required controls panel
committee review workspace
NIST AI RMF mapping
EU AI Act-style classification
HIPAA-style review
board audit trail
evidence export and board memo
''').strip() + "\n")

(phases / "PHASE_9_CLIENT_DEMO_PACKAGING_PUBLIC_DEPLOYMENT_PREP.md").write_text(dedent(r'''

Phase 9 — Client Demo Packaging & Public Deployment Prep
Status

Implementation Complete

Purpose

Phase 9 prepares the SecureTheCloud AI Governance Board repository for public demo deployment and client-safe sharing.

This phase is documentation and packaging only. It does not deploy the app.

Scope

Phase 9 adds:

Polished README introduction
Client-safe demo walkthrough
Correct claim / incorrect claim section
Local run instructions
Evidence export explanation
Executive decision memo explanation
Public deployment preparation notes
Screenshot placeholder checklist
Public demo safety boundary
Phase 9 evidence document
Public Demo Boundary

This is a simulated AI governance board.

No real patient data, customer data, regulated systems, clinical systems, production model runtimes, enterprise authorization systems, or production enforcement systems are connected.

Correct Claim

The platform demonstrates a governance control pattern for proposed AI systems:

intake
ownership capture
model registry context
risk scoring
regulatory mapping
governance committee review
HIPAA-style review
evidence timeline
board evidence export
executive decision memo
Incorrect Claims

The platform does not claim:

production compliance
legal certification
HIPAA certification
NIST certification
EU AI Act certification
clinical decision support approval
real enterprise authorization enforcement
production AI runtime governance
Artifacts Added
README.md
docs/CLIENT_DEMO_WALKTHROUGH.md
docs/DEPLOYMENT_PREP.md
docs/SCREENSHOTS.md
docs/phases/PHASE_9_CLIENT_DEMO_PACKAGING_PUBLIC_DEPLOYMENT_PREP.md
Validation

Recommended validation:

docker compose down
docker compose up --build -d

sleep 20

curl http://localhost:8010/health
curl http://localhost:8010/api/dashboard
curl -I http://localhost:3010
Completion Evidence
Client-safe README package added
Demo walkthrough added
Deployment prep notes added
Screenshot checklist added
Phase 9 evidence document added
No deployment performed
''').strip() + "\n")

(screenshots / ".keep").write_text("Add public demo screenshots here after deployment.\n")

print("Phase 9 client demo packaging and public deployment prep complete.")
