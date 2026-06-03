from pathlib import Path

p = Path("backend/app/main.py")
s = p.read_text()

if "class GovernanceReviewRequest" not in s:
    insert = '''
class GovernanceReviewRequest(BaseModel):
    reviewer: str = "AI Governance Committee"
    action: str
    note: str = ""
'''
    marker = "@app.get(\"/health\")"
    if marker not in s:
        raise SystemExit("Health endpoint marker not found")
    s = s.replace(marker, insert + "\n\n" + marker)

endpoint = '''
def _find_ai_system_store():
    for value in globals().values():
        if isinstance(value, list) and value:
            first = value[0]
            if isinstance(first, dict) and "system_id" in first:
                return value
            if hasattr(first, "system_id"):
                return value
    return None


def _record_get(record, key, default=None):
    if isinstance(record, dict):
        return record.get(key, default)
    return getattr(record, key, default)


def _record_set(record, key, value):
    if isinstance(record, dict):
        record[key] = value
        return
    try:
        setattr(record, key, value)
    except Exception:
        pass


def _append_control(record, control):
    risk_assessment = _record_get(record, "risk_assessment")
    if risk_assessment is None:
        return

    controls = _record_get(risk_assessment, "required_controls", [])
    if control not in controls:
        controls = list(controls) + [control]

    if isinstance(risk_assessment, dict):
        risk_assessment["required_controls"] = controls
    else:
        try:
            risk_assessment.required_controls = controls
        except Exception:
            pass


@app.patch("/api/ai-systems/{system_id}/review")
def review_ai_system(system_id: str, review: GovernanceReviewRequest):
    store = _find_ai_system_store()

    if store is None:
        raise HTTPException(status_code=500, detail="AI system store not found")

    target = None
    for record in store:
        if _record_get(record, "system_id") == system_id:
            target = record
            break

    if target is None:
        raise HTTPException(status_code=404, detail="AI system not found")

    action = review.action.strip().lower()
    reviewer = review.reviewer.strip() or "AI Governance Committee"
    note = review.note.strip()

    if action == "approve":
        approval_status = "approved"
        final_outcome = "approved"
        review_reason = "Governance committee approved the AI system with evidence retained."
    elif action == "reject":
        approval_status = "rejected"
        final_outcome = "rejected"
        review_reason = "Governance committee rejected the AI system pending redesign or resubmission."
    elif action == "request_controls":
        approval_status = "controls_required"
        final_outcome = "controls_required"
        review_reason = "Governance committee requires additional controls before approval."
        _append_control(target, "Committee-requested control remediation")
    elif action == "escalate":
        approval_status = "escalation_required"
        final_outcome = "escalation_required"
        review_reason = "Governance committee escalated the AI system for senior review."
        _append_control(target, "Senior governance review")
    else:
        raise HTTPException(status_code=400, detail="Unsupported review action")

    _record_set(target, "approval_status", approval_status)
    _record_set(target, "final_outcome", final_outcome)
    _record_set(target, "reviewer", reviewer)
    _record_set(target, "reviewer_action", action)
    _record_set(target, "reviewer_note", note)
    _record_set(target, "reviewed_at", datetime.now(timezone.utc).isoformat())

    risk_assessment = _record_get(target, "risk_assessment")
    if risk_assessment is not None:
        if isinstance(risk_assessment, dict):
            risk_assessment["decision"] = final_outcome
            risk_assessment["reason"] = review_reason
        else:
            try:
                risk_assessment.decision = final_outcome
                risk_assessment.reason = review_reason
            except Exception:
                pass

    return target
'''

if '@app.patch("/api/ai-systems/{system_id}/review")' not in s:
    s = s.rstrip() + "\n\n" + endpoint.strip() + "\n"

p.write_text(s)
