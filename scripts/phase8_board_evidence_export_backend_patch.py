from pathlib import Path

p = Path("backend/app/main.py")
s = p.read_text()

if '@app.get("/api/ai-systems/{system_id}/board-evidence-export")' in s:
    print("Phase 8 backend endpoints already present.")
    raise SystemExit(0)

# Ensure HTTPException import exists.
if "from fastapi import" in s:
    line = s.split("from fastapi import", 1)[1].split("\n", 1)[0]
    if "HTTPException" not in line:
        s = s.replace("from fastapi import FastAPI", "from fastapi import FastAPI, HTTPException")
else:
    s = "from fastapi import FastAPI, HTTPException\n" + s

# Ensure datetime import exists.
if "from datetime import datetime, timezone" not in s:
    s = "from datetime import datetime, timezone\n" + s

endpoint = r'''

# ---------------------------------------------------------------------------
# Phase 8: Board Evidence Export & Executive Decision Memo
# ---------------------------------------------------------------------------

def _phase8_to_dict(value):
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if isinstance(value, dict):
        return value
    return getattr(value, "__dict__", {})


def _phase8_get(value, key, default=None):
    if isinstance(value, dict):
        return value.get(key, default)
    return getattr(value, key, default)


def _phase8_find_ai_system_store():
    existing_finder = globals().get("_phase7_find_ai_system_store") or globals().get("_find_ai_system_store")
    if callable(existing_finder):
        try:
            found = existing_finder()
            if found:
                return found
        except Exception:
            pass

    for value in globals().values():
        if isinstance(value, list) and value:
            first = _phase8_to_dict(value[0])
            if "system_id" in first and "risk_assessment" in first:
                return value

    return []


def _phase8_find_ai_system(system_id: str):
    for system in _phase8_find_ai_system_store():
        if _phase8_get(system, "system_id") == system_id:
            return system
    return None


def _phase8_bool_label(value) -> str:
    return "yes" if bool(value) else "no"


def _phase8_timeline(system):
    existing_builder = globals().get("_phase7_build_evidence_timeline")
    if callable(existing_builder):
        try:
            return existing_builder(system)
        except Exception:
            pass

    risk = _phase8_to_dict(_phase8_get(system, "risk_assessment", {}))
    return [
        {
            "step": "01",
            "title": "AI System Intake",
            "status": "captured",
            "detail": f"{_phase8_get(system, 'system_name', 'AI system')} submitted for governance review.",
            "evidence": [
                f"System ID: {_phase8_get(system, 'system_id', 'unknown')}",
                f"Business owner: {_phase8_get(system, 'business_owner', 'unknown')}",
                f"Model owner: {_phase8_get(system, 'model_owner', 'unknown')}",
            ],
        },
        {
            "step": "02",
            "title": "Risk Assessment",
            "status": risk.get("risk_classification", "unknown"),
            "detail": f"Risk score calculated as {risk.get('risk_score', 0)}/100.",
            "evidence": risk.get("risk_factors", []) or ["No major risk factors identified"],
        },
        {
            "step": "03",
            "title": "Final Governance Outcome",
            "status": _phase8_get(system, "final_outcome", risk.get("decision", "unknown")),
            "detail": f"Final governed AI system outcome: {_phase8_get(system, 'final_outcome', risk.get('decision', 'unknown'))}.",
            "evidence": risk.get("evidence_required", []) or ["Standard governance evidence retained"],
        },
    ]


def _phase8_completeness(system):
    existing_builder = globals().get("_phase7_build_completeness")
    if callable(existing_builder):
        try:
            return existing_builder(system)
        except Exception:
            pass

    risk = _phase8_to_dict(_phase8_get(system, "risk_assessment", {}))
    nist = risk.get("nist_mapping", {}) or {}
    checks = [
        ("System intake record", bool(_phase8_get(system, "system_id"))),
        ("Business owner identified", bool(_phase8_get(system, "business_owner"))),
        ("Model owner identified", bool(_phase8_get(system, "model_owner"))),
        ("Risk score calculated", risk.get("risk_score") is not None),
        ("Risk classification assigned", bool(risk.get("risk_classification"))),
        ("NIST Govern mapped", bool(nist.get("govern"))),
        ("NIST Map mapped", bool(nist.get("map"))),
        ("NIST Measure mapped", bool(nist.get("measure"))),
        ("NIST Manage mapped", bool(nist.get("manage"))),
        ("EU AI Act-style class assigned", bool(risk.get("ai_act_classification"))),
        ("Final outcome recorded", bool(_phase8_get(system, "final_outcome", risk.get("decision")))),
    ]
    complete = sum(1 for _, done in checks if done)
    return {
        "complete": complete,
        "total": len(checks),
        "coverage_percent": round((complete / len(checks)) * 100),
        "items": [{"name": name, "status": "complete" if done else "missing"} for name, done in checks],
    }


def _phase8_decision_rationale(system):
    risk = _phase8_to_dict(_phase8_get(system, "risk_assessment", {}))
    outcome = _phase8_get(system, "final_outcome", risk.get("decision", "unknown"))
    risk_score = risk.get("risk_score", 0)
    risk_class = risk.get("risk_classification", "unknown")
    ai_act = risk.get("ai_act_classification", "unknown")
    hipaa_required = risk.get("hipaa_review_required", False)

    return {
        "decision": outcome,
        "rationale": risk.get(
            "reason",
            f"Governance outcome is {outcome} based on score {risk_score}/100, risk class {risk_class}, classification {ai_act}, and required control evidence.",
        ),
        "risk_score": risk_score,
        "risk_classification": risk_class,
        "ai_act_classification": ai_act,
        "hipaa_review_required": hipaa_required,
        "approval_status": _phase8_get(system, "approval_status", "unknown"),
        "monitoring_required": _phase8_get(system, "final_outcome", "") in {"require_review", "require_controls", "escalate"} or bool(hipaa_required),
    }


def _phase8_required_controls_summary(system):
    risk = _phase8_to_dict(_phase8_get(system, "risk_assessment", {}))
    controls = sorted(set(risk.get("required_controls", []) or []))
    evidence = sorted(set(risk.get("evidence_required", []) or []))

    return {
        "required_controls": controls,
        "evidence_required": evidence,
        "control_count": len(controls),
        "evidence_count": len(evidence),
    }


def _phase8_public_demo_boundary():
    return {
        "lab_mode": True,
        "safe_claim": "Production-shaped simulated AI governance board, not production enforcement.",
        "not_connected_to": [
            "real patient data",
            "customer records",
            "regulated production systems",
            "production model runtime",
            "enterprise authorization systems",
            "clinical decision systems",
        ],
    }


def _phase8_build_evidence_packet(system):
    risk = _phase8_to_dict(_phase8_get(system, "risk_assessment", {}))
    nist = risk.get("nist_mapping", {}) or {}
    completeness = _phase8_completeness(system)
    rationale = _phase8_decision_rationale(system)
    controls = _phase8_required_controls_summary(system)

    return {
        "packet_type": "board_ai_governance_evidence_export",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "public_demo_boundary": _phase8_public_demo_boundary(),
        "system": {
            "system_id": _phase8_get(system, "system_id"),
            "system_name": _phase8_get(system, "system_name"),
            "business_owner": _phase8_get(system, "business_owner"),
            "model_owner": _phase8_get(system, "model_owner"),
            "department": _phase8_get(system, "department"),
            "domain": _phase8_get(system, "domain"),
            "use_case": _phase8_get(system, "use_case"),
            "model_name": _phase8_get(system, "model_name"),
            "model_provider": _phase8_get(system, "model_provider"),
            "deployment_environment": _phase8_get(system, "deployment_environment"),
            "target_users": _phase8_get(system, "target_users"),
            "data_types": _phase8_get(system, "data_types", []),
        },
        "risk_and_classification": {
            "risk_score": risk.get("risk_score"),
            "risk_classification": risk.get("risk_classification"),
            "ai_act_classification": risk.get("ai_act_classification"),
            "risk_factors": risk.get("risk_factors", []),
            "phi_involved": _phase8_get(system, "phi_involved", False),
            "customer_data_involved": _phase8_get(system, "customer_data_involved", False),
            "clinical_or_patient_impact": _phase8_get(system, "clinical_or_patient_impact", False),
            "financial_or_credit_impact": _phase8_get(system, "financial_or_credit_impact", False),
            "security_enforcement_impact": _phase8_get(system, "security_enforcement_impact", False),
            "safety_critical": _phase8_get(system, "safety_critical", False),
        },
        "governance_decision": rationale,
        "required_controls_summary": controls,
        "nist_ai_rmf_mapping": {
            "govern": nist.get("govern", []),
            "map": nist.get("map", []),
            "measure": nist.get("measure", []),
            "manage": nist.get("manage", []),
        },
        "evidence_timeline": _phase8_timeline(system),
        "evidence_completeness": completeness,
        "audit_readiness": {
            "coverage_percent": completeness["coverage_percent"],
            "evidence_ready": completeness["coverage_percent"] == 100,
            "reconstruction_summary": "Evidence packet reconstructs AI system intake, risk scoring, regulatory mapping, HIPAA-style review, committee status, and final governance outcome.",
        },
    }


def _phase8_build_decision_memo(system):
    packet = _phase8_build_evidence_packet(system)
    sys = packet["system"]
    decision = packet["governance_decision"]
    controls = packet["required_controls_summary"]
    risk = packet["risk_and_classification"]
    completeness = packet["evidence_completeness"]

    return {
        "memo_type": "executive_ai_governance_decision_memo",
        "generated_at": packet["generated_at"],
        "title": f"Board Decision Memo — {sys['system_name']}",
        "audience": "AI governance board, risk committee, compliance, audit, and executive stakeholders",
        "public_demo_boundary": packet["public_demo_boundary"],
        "executive_summary": (
            f"{sys['system_name']} was reviewed as a simulated AI governance board submission. "
            f"The system received a risk score of {risk['risk_score']}/100, "
            f"a risk classification of {risk['risk_classification']}, "
            f"and an EU AI Act-style classification of {risk['ai_act_classification']}. "
            f"The current governance outcome is {decision['decision']}."
        ),
        "decision": decision,
        "required_controls_summary": controls,
        "evidence_completeness": {
            "complete": completeness["complete"],
            "total": completeness["total"],
            "coverage_percent": completeness["coverage_percent"],
        },
        "recommended_board_position": (
            "Approve with standard ownership evidence."
            if decision["decision"] == "approve"
            else "Do not proceed until required controls, evidence, or review actions are completed."
        ),
        "client_safe_claim": "This memo is generated from a simulated governance workflow and does not represent production approval, legal advice, clinical review, or compliance certification.",
    }


@app.get("/api/ai-systems/{system_id}/board-evidence-export")
def get_board_evidence_export(system_id: str):
    system = _phase8_find_ai_system(system_id)
    if not system:
        raise HTTPException(status_code=404, detail="AI system not found")
    return _phase8_build_evidence_packet(system)


@app.get("/api/ai-systems/{system_id}/board-decision-memo")
def get_board_decision_memo(system_id: str):
    system = _phase8_find_ai_system(system_id)
    if not system:
        raise HTTPException(status_code=404, detail="AI system not found")
    return _phase8_build_decision_memo(system)
'''

s = s.rstrip() + endpoint + "\n"
p.write_text(s)
print("Added Phase 8 board evidence export and decision memo endpoints.")
