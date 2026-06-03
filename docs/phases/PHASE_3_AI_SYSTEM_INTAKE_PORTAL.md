# Phase 3 — AI System Intake Portal

Status: Implementation Complete

## Goal

Add an interactive AI system intake portal where proposed AI systems can be submitted for governance review, risk scoring, regulatory mapping, and evidence capture.

## Implemented

- AI system intake form
- Business owner and model owner fields
- Domain and department fields
- Use case and model metadata fields
- Deployment environment field
- Data type flags
- PHI involved flag
- Customer data involved flag
- Automated decisioning flag
- Clinical / patient impact flag
- Financial / credit impact flag
- Security enforcement impact flag
- Safety-critical flag
- Human oversight selector
- Approval status selector
- Live governance preview
- Submit governed AI system action
- Dashboard refresh after submission
- Model registry refresh after submission
- Evidence package refresh after submission

## Backend Endpoints Used

- POST /api/governance/preview
- POST /api/ai-systems
- GET /api/dashboard
- GET /api/ai-systems
- GET /api/model-registry

## Boundary

This is a simulated AI governance intake workflow.

It does not provide production authorization, legal compliance advice, SOC 2 certification, HIPAA compliance certification, EU AI Act compliance certification, real clinical decision support, real regulated-system access, real patient data processing, or production enforcement authority.
