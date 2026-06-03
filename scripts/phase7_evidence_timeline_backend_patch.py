from pathlib import Path

p = Path("backend/app/main.py")
s = p.read_text()

if "@app.get(\"/api/ai-systems/{system_id}/evidence-timeline\")" in s:
    print("Phase 7 evidence timeline endpoint already present.")
    raise SystemExit(0)

if "HTTPException" not in s.split("from fastapi import", 1)[1].split("\n", 1)[0]:
    s = s.replace("from fastapi import FastAPI", "from fastapi import FastAPI, HTTPException")

if "from datetime import datetime, timezone" not in s:
    s = "from datetime import datetime, timezone\n" + s

endpoint = r'''

# ---------------------------------------------------------------------------
# Phase 7: Evidence Package Timeline & Board Audit Trail
# ---------------------------------------------------------------------------

def _phase7_to_dict(value):
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if isinstance(value, dict):
        return value
    return getattr(value, "__dict__", {})


def _phase7_get(value, key, default=None):
    if isinstance(value, dict):
        return value.get(key, default)
    return getattr(value, key, default)


def _phase7_find_ai_system_store():
    existing_finder = globals().get("_find_ai_system_store")
    if callable(existing_finder):
        try:
            found = existing_finder()
            if found:
                return found
        except Exception:
            pass

    for value in globals().values():
        if isinstance(value, list) and value:
            first = value[0]
            first_dict = _phase7_to_dict(first)
            if "system_id" in first_dict and "risk_assessment" in first_dict:
                return value

    return []


def _phase7_find_ai_system(system_id: str):
    for system in _phase7_find_ai_system_store():
        if _phase7_get(system, "system_id") == system_id:
            return system
    return None


def _phase7_bool_label(value) -> str:
    return "yes" if bool(value) else "no"


def _phase7_build_evidence_timeline(system):
    risk = _phase7_get(system, "risk_assessment", {})
    risk_dict = _phase7_to_dict(risk)
    nist = risk_dict.get("nist_mapping", {}) or {}

    system_name = _phase7_get(system, "system_name", "Unknown AI System")
    system_id = _phase7_get(system, "system_id", "unknown")
    domain = _phase7_get(system, "domain", "unknown")
    department = _phase7_get(system, "department", "unknown")
    owner = _phase7_get(system, "business_owner", "unknown")
    model_owner = _phase7_get(system, "model_owner", "unknown")
    model_name = _phase7_get(system, "model_name", "unknown")
    approval_status = _phase7_get(system, "approval_status", "unknown")
    final_outcome = _phase7_get(system, "final_outcome", risk_dict.get("decision", "unknown"))

    risk_score = risk_dict.get("risk_score", 0)
    risk_classification = risk_dict.get("risk_classification", "unknown")
    ai_act_classification = risk_dict.get("ai_act_classification", "unknown")
    hipaa_required = risk_dict.get("hipaa_review_required", False)

    data_types = _phase7_get(system, "data_types", []) or []
    risk_factors = risk_dict.get("risk_factors", []) or []
    controls = risk_dict.get("required_controls", []) or []
    evidence = risk_dict.get("evidence_required", []) or []

    committee_status = "recorded" if approval_status in {
        "approved",
        "rejected",
        "controls_required",
        "escalated",
    } else "pending"

    return [
        {
            "step": "01",
            "title": "AI System Intake",
            "status": "captured",
            "detail": f"{system_name} submitted for governance review in {domain}.",
            "evidence": [
                f"System ID: {system_id}",
                f"Business owner: {owner}",
                f"Model owner: {model_owner}",
                f"Model: {model_name}",
                f"Department: {department}",
            ],
        },
        {
            "step": "02",
            "title": "Risk Assessment",
            "status": risk_classification,
            "detail": f"Risk score calculated as {risk_score}/100 with classification {risk_classification}.",
            "evidence": risk_factors if risk_factors else ["No major risk factors identified"],
        },
        {
            "step": "03",
            "title": "NIST AI RMF Mapping",
            "status": "mapped",
            "detail": "Govern, Map, Measure, and Manage evidence mapped for board review.",
            "evidence": [
                f"Govern: {len(nist.get('govern', []))} evidence point(s)",
                f"Map: {len(nist.get('map', []))} evidence point(s)",
                f"Measure: {len(nist.get('measure', []))} evidence point(s)",
                f"Manage: {len(nist.get('manage', []))} evidence point(s)",
            ],
        },
        {
            "step": "04",
            "title": "EU AI Act-Style Classification",
            "status": ai_act_classification,
            "detail": f"System classified as {ai_act_classification} for simulated EU AI Act-style review.",
            "evidence": [
                f"Risk class: {risk_classification}",
                f"Decision: {risk_dict.get('decision', 'unknown')}",
                f"Required controls: {len(controls)}",
            ],
        },
        {
            "step": "05",
            "title": "HIPAA-Style Review",
            "status": "required" if hipaa_required else "not required",
            "detail": "PHI and patient-impact review evaluated for healthcare governance readiness.",
            "evidence": [
                f"PHI involved: {_phase7_bool_label(_phase7_get(system, 'phi_involved', False))}",
                f"Clinical / patient impact: {_phase7_bool_label(_phase7_get(system, 'clinical_or_patient_impact', False))}",
                f"HIPAA-style review required: {_phase7_bool_label(hipaa_required)}",
            ],
        },
        {
            "step": "06",
            "title": "Committee Decision",
            "status": committee_status,
            "detail": f"Governance committee status is {approval_status}.",
            "evidence": [
                f"Approval status: {approval_status}",
                f"Current final outcome: {final_outcome}",
            ],
        },
        {
            "step": "07",
            "title": "Final Governance Outcome",
            "status": final_outcome,
            "detail": f"Final governed AI system outcome: {final_outcome}.",
            "evidence": evidence if evidence else ["Standard ownership and documentation evidence retained"],
        },
    ]


def _phase7_build_completeness(system):
    risk = _phase7_to_dict(_phase7_get(system, "risk_assessment", {}))
    nist = risk.get("nist_mapping", {}) or {}
    evidence = risk.get("evidence_required", []) or []

    checks = [
        ("System intake record", bool(_phase7_get(system, "system_id"))),
        ("Business owner identified", bool(_phase7_get(system, "business_owner"))),
        ("Model owner identified", bool(_phase7_get(system, "model_owner"))),
        ("Risk score calculated", risk.get("risk_score") is not None),
        ("Risk classification assigned", bool(risk.get("risk_classification"))),
        ("NIST Govern mapped", bool(nist.get("govern"))),
        ("NIST Map mapped", bool(nist.get("map"))),
        ("NIST Measure mapped", bool(nist.get("measure"))),
        ("NIST Manage mapped", bool(nist.get("manage"))),
        ("EU AI Act-style class assigned", bool(risk.get("ai_act_classification"))),
        ("HIPAA-style review evaluated", risk.get("hipaa_review_required") is not None),
        ("Evidence requirements listed", bool(evidence)),
        ("Final outcome recorded", bool(_phase7_get(system, "final_outcome", risk.get("decision")))),
    ]

    complete_count = sum(1 for _, complete in checks if complete)
    return {
        "complete": complete_count,
        "total": len(checks),
        "coverage_percent": round((complete_count / len(checks)) * 100),
        "items": [
            {
                "name": name,
                "status": "complete" if complete else "missing",
            }
            for name, complete in checks
        ],
    }


@app.get("/api/ai-systems/{system_id}/evidence-timeline")
def get_ai_system_evidence_timeline(system_id: str):
    system = _phase7_find_ai_system(system_id)

    if not system:
        raise HTTPException(status_code=404, detail="AI system not found")

    risk = _phase7_to_dict(_phase7_get(system, "risk_assessment", {}))
    completeness = _phase7_build_completeness(system)

    return {
        "system_id": _phase7_get(system, "system_id"),
        "system_name": _phase7_get(system, "system_name"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "final_outcome": _phase7_get(system, "final_outcome", risk.get("decision")),
        "risk_classification": risk.get("risk_classification"),
        "ai_act_classification": risk.get("ai_act_classification"),
        "hipaa_review_required": risk.get("hipaa_review_required"),
        "timeline": _phase7_build_evidence_timeline(system),
        "completeness": completeness,
        "auditor_reconstruction": {
            "summary": "Board/auditor-ready reconstruction of AI system intake, risk scoring, regulatory mapping, committee review, and final governance outcome.",
            "coverage": f"{completeness['coverage_percent']}%",
            "evidence_ready": completeness["coverage_percent"] == 100,
        },
    }
'''

s = s.rstrip() + endpoint + "\n"
p.write_text(s)
print("Added Phase 7 evidence timeline endpoint.")
