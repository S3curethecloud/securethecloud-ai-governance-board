from pathlib import Path
import re

p = Path("backend/app/main.py")
s = p.read_text()

# Add safe imports without depending on exact existing import formatting.
if "HTTPException" not in s:
    if re.search(r"from fastapi import .+", s):
        s = re.sub(
            r"from fastapi import ([^\n]+)",
            lambda m: m.group(0) if "HTTPException" in m.group(1) else f"from fastapi import {m.group(1)}, HTTPException",
            s,
            count=1,
        )
    else:
        s = "from fastapi import HTTPException\n" + s

if "BaseModel" not in s:
    s = "from pydantic import BaseModel\n" + s

if "timezone" not in s:
    s = "from datetime import datetime, timezone\n" + s
elif "datetime.now(timezone.utc)" not in s and "from datetime import datetime" not in s:
    s = "from datetime import datetime, timezone\n" + s

endpoint = r'''
class GovernanceReviewRequest(BaseModel):
    reviewer: str = "AI Governance Committee"
    action: str
    note: str = ""


def _phase4_record_get(record, key, default=None):
    if isinstance(record, dict):
        return record.get(key, default)
    return getattr(record, key, default)


def _phase4_record_set(record, key, value):
    if isinstance(record, dict):
        record[key] = value
        return

    try:
        setattr(record, key, value)
    except Exception:
        # Some Pydantic models may not allow undeclared fields.
        pass


def _phase4_risk_get(risk, key, default=None):
    if isinstance(risk, dict):
        return risk.get(key, default)
    return getattr(risk, key, default)


def _phase4_risk_set(risk, key, value):
    if isinstance(risk, dict):
        risk[key] = value
        return

    try:
        setattr(risk, key, value)
    except Exception:
        pass


def _phase4_find_ai_system_store():
    candidates = []

    for name, value in globals().items():
        if not isinstance(value, list) or not value:
            continue

        first = value[0]

        if isinstance(first, dict) and "system_id" in first:
            candidates.append((name, value))
            continue

        if hasattr(first, "system_id"):
            candidates.append((name, value))

    if not candidates:
        return None

    # Prefer obvious AI system stores if present.
    for name, value in candidates:
        lowered = name.lower()
        if "system" in lowered or "ai" in lowered:
            return value

    return candidates[0][1]


def _phase4_append_control(record, control):
    risk = _phase4_record_get(record, "risk_assessment")
    if risk is None:
        return

    controls = list(_phase4_risk_get(risk, "required_controls", []))

    if control not in controls:
        controls.append(control)

    _phase4_risk_set(risk, "required_controls", controls)


@app.patch("/api/ai-systems/{system_id}/review")
def review_ai_system(system_id: str, review: GovernanceReviewRequest):
    store = _phase4_find_ai_system_store()

    if store is None:
        raise HTTPException(status_code=500, detail="AI system store not found")

    target = None

    for record in store:
        if _phase4_record_get(record, "system_id") == system_id:
            target = record
            break

    if target is None:
        raise HTTPException(status_code=404, detail="AI system not found")

    action = review.action.strip().lower()
    reviewer = review.reviewer.strip() or "AI Governance Committee"
    note = review.note.strip()

    if action == "approve":
        approval_status = "approved"
        final_outcome = "approve"
        reason = "Governance committee approved the AI system with evidence retained."
    elif action == "reject":
        approval_status = "rejected"
        final_outcome = "reject"
        reason = "Governance committee rejected the AI system pending redesign or resubmission."
    elif action == "request_controls":
        approval_status = "controls_required"
        final_outcome = "require_controls"
        reason = "Governance committee requires additional controls before approval."
        _phase4_append_control(target, "Committee-requested control remediation")
    elif action == "escalate":
        approval_status = "escalation_required"
        final_outcome = "require_review"
        reason = "Governance committee escalated the AI system for senior review."
        _phase4_append_control(target, "Senior governance review")
    else:
        raise HTTPException(status_code=400, detail="Unsupported review action")

    _phase4_record_set(target, "approval_status", approval_status)
    _phase4_record_set(target, "final_outcome", final_outcome)
    _phase4_record_set(target, "reviewer", reviewer)
    _phase4_record_set(target, "reviewer_action", action)
    _phase4_record_set(target, "reviewer_note", note)
    _phase4_record_set(target, "reviewed_at", datetime.now(timezone.utc).isoformat())

    risk = _phase4_record_get(target, "risk_assessment")

    if risk is not None:
        _phase4_risk_set(risk, "decision", final_outcome)
        _phase4_risk_set(risk, "reason", reason)

    return target
'''

if '@app.patch("/api/ai-systems/{system_id}/review")' not in s:
    s = s.rstrip() + "\n\n" + endpoint.strip() + "\n"

p.write_text(s)
