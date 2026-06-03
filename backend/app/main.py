from datetime import datetime, timezone
from enum import Enum
from typing import List
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


class BusinessDomain(str, Enum):
    healthcare = "healthcare"
    financial_services = "financial_services"
    security = "security"
    enterprise_internal = "enterprise_internal"
    consumer_platform = "consumer_platform"
    research = "research"


class DeploymentEnvironment(str, Enum):
    proposed = "proposed"
    sandbox = "sandbox"
    pilot = "pilot"
    production = "production"


class HumanOversight(str, Enum):
    none = "none"
    human_in_loop = "human_in_loop"
    human_on_loop = "human_on_loop"
    human_review_after = "human_review_after"


class ApprovalStatus(str, Enum):
    submitted = "submitted"
    pending_review = "pending_review"
    approved = "approved"
    rejected = "rejected"
    escalation_required = "escalation_required"


class RiskClassification(str, Enum):
    minimal = "minimal"
    limited = "limited"
    high_risk = "high_risk"
    prohibited = "prohibited"


class NISTFunction(str, Enum):
    govern = "govern"
    map = "map"
    measure = "measure"
    manage = "manage"


class AIActClassification(str, Enum):
    minimal = "minimal"
    limited = "limited"
    high_risk = "high_risk"
    prohibited = "prohibited"


class GovernanceDecision(str, Enum):
    approve = "approve"
    reject = "reject"
    require_review = "require_review"
    require_controls = "require_controls"
    prohibit = "prohibit"


class AISystemCreate(BaseModel):
    system_name: str = Field(min_length=2)
    business_owner: str = Field(min_length=2)
    model_owner: str = Field(min_length=2)
    department: str = Field(min_length=2)
    domain: BusinessDomain
    use_case: str = Field(min_length=5)
    model_name: str = Field(min_length=2)
    model_provider: str = Field(min_length=2)
    deployment_environment: DeploymentEnvironment = DeploymentEnvironment.proposed
    target_users: str = "internal users"
    data_types: List[str] = Field(default_factory=list)
    phi_involved: bool = False
    customer_data_involved: bool = False
    automated_decisioning: bool = False
    clinical_or_patient_impact: bool = False
    financial_or_credit_impact: bool = False
    security_enforcement_impact: bool = False
    safety_critical: bool = False
    human_oversight: HumanOversight = HumanOversight.human_in_loop
    approval_status: ApprovalStatus = ApprovalStatus.submitted


class RiskAssessment(BaseModel):
    risk_score: int
    risk_classification: RiskClassification
    ai_act_classification: AIActClassification
    decision: GovernanceDecision
    reason: str
    risk_factors: List[str]
    required_controls: List[str]
    nist_mapping: dict[NISTFunction, List[str]]
    hipaa_review_required: bool
    evidence_required: List[str]


class AISystemRecord(AISystemCreate):
    system_id: str
    submitted_at: datetime
    risk_assessment: RiskAssessment
    final_outcome: str


class ModelRegistryEntry(BaseModel):
    system_id: str
    model_name: str
    model_provider: str
    model_owner: str
    use_case: str
    domain: BusinessDomain
    risk_classification: RiskClassification
    approval_status: ApprovalStatus
    last_reviewed: datetime | None = None
    monitoring_status: str


class DashboardSummary(BaseModel):
    total_ai_systems: int
    pending_reviews: int
    approved_systems: int
    rejected_systems: int
    high_risk_systems: int
    prohibited_systems: int
    phi_involved_systems: int
    customer_data_systems: int
    systems_requiring_monitoring: int
    governance_coverage: int


class Health(BaseModel):
    status: str
    service: str
    lab_mode: bool
    phase: str


app = FastAPI(
    title="SecureTheCloud AI Governance Board API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


AI_SYSTEMS: list[AISystemRecord] = []


def now() -> datetime:
    return datetime.now(timezone.utc)


def nist_mapping_for(system: AISystemCreate) -> dict[NISTFunction, list[str]]:
    controls = {
        NISTFunction.govern: [
            "AI ownership identified",
            "Governance review required",
            "Approval status tracked",
        ],
        NISTFunction.map: [
            "Use case documented",
            "Deployment context captured",
            "Data types identified",
        ],
        NISTFunction.measure: [
            "Risk score calculated",
            "Risk factors recorded",
            "Impact flags evaluated",
        ],
        NISTFunction.manage: [
            "Required controls assigned",
            "Evidence package required",
            "Monitoring status tracked",
        ],
    }

    if system.phi_involved:
        controls[NISTFunction.map].append("PHI involvement flagged")
        controls[NISTFunction.manage].append("HIPAA-style review workflow required")

    if system.automated_decisioning:
        controls[NISTFunction.measure].append("Automated decisioning impact evaluated")
        controls[NISTFunction.manage].append("Human oversight control required")

    if system.deployment_environment == DeploymentEnvironment.production:
        controls[NISTFunction.govern].append("Production promotion review required")
        controls[NISTFunction.manage].append("Post-deployment monitoring required")

    return controls


def assess_risk(system: AISystemCreate) -> RiskAssessment:
    score = 0
    factors: list[str] = []
    controls: list[str] = [
        "AI system owner approval",
        "Documented business use case",
        "Model owner accountability",
        "Evidence package retention",
    ]
    evidence: list[str] = [
        "System intake record",
        "Use case description",
        "Owner attestation",
        "Risk assessment summary",
    ]

    if system.phi_involved:
        score += 30
        factors.append("PHI involved")
        controls.extend([
            "HIPAA-style AI review board approval",
            "PHI minimization review",
            "Patient-impact evidence package",
        ])
        evidence.extend([
            "PHI review evidence",
            "Data minimization rationale",
            "Human oversight attestation",
        ])

    if system.customer_data_involved:
        score += 20
        factors.append("Customer data involved")
        controls.append("Customer data access review")
        evidence.append("Customer data handling rationale")

    if system.automated_decisioning:
        score += 25
        factors.append("Automated decisioning")
        controls.append("Human oversight required")
        evidence.append("Automated decision impact review")

    if system.clinical_or_patient_impact:
        score += 30
        factors.append("Clinical or patient impact")
        controls.append("Clinical safety review")
        evidence.append("Clinical impact assessment")

    if system.financial_or_credit_impact:
        score += 25
        factors.append("Financial or credit impact")
        controls.append("Financial impact governance review")
        evidence.append("Financial impact assessment")

    if system.security_enforcement_impact:
        score += 20
        factors.append("Security enforcement impact")
        controls.append("Security enforcement review")
        evidence.append("Security action boundary review")

    if system.safety_critical:
        score += 40
        factors.append("Safety-critical use case")
        controls.append("Safety-critical board escalation")
        evidence.append("Safety-critical risk acceptance")

    if system.human_oversight == HumanOversight.none:
        score += 35
        factors.append("No human oversight")
        controls.append("Human oversight must be added before approval")
        evidence.append("Human oversight plan")

    if system.deployment_environment == DeploymentEnvironment.production:
        score += 20
        factors.append("Production deployment requested")
        controls.append("Production readiness review")
        evidence.append("Production promotion approval")

    if "biometric" in [item.lower() for item in system.data_types]:
        score += 35
        factors.append("Biometric data type")
        controls.append("Biometric data governance review")
        evidence.append("Biometric processing rationale")

    score = max(0, min(score, 100))

    prohibited = (
        system.safety_critical and system.human_oversight == HumanOversight.none
    ) or (
        "prohibited" in system.use_case.lower()
    )

    if prohibited:
        classification = RiskClassification.prohibited
        ai_act = AIActClassification.prohibited
        decision = GovernanceDecision.prohibit
        reason = "System is prohibited in this lab because safety-critical or explicitly prohibited use lacks acceptable governance controls."
    elif score >= 70:
        classification = RiskClassification.high_risk
        ai_act = AIActClassification.high_risk
        decision = GovernanceDecision.require_review
        reason = "High-risk AI system requires governance board review, approval evidence, and monitoring controls."
    elif score >= 35:
        classification = RiskClassification.limited
        ai_act = AIActClassification.limited
        decision = GovernanceDecision.require_controls
        reason = "Limited-risk AI system requires documented controls and evidence before approval."
    else:
        classification = RiskClassification.minimal
        ai_act = AIActClassification.minimal
        decision = GovernanceDecision.approve if system.approval_status == ApprovalStatus.approved else GovernanceDecision.require_controls
        reason = "Minimal-risk AI system may proceed after standard documentation and ownership controls."

    if system.approval_status == ApprovalStatus.rejected:
        decision = GovernanceDecision.reject
        reason = "System was rejected by governance review."

    return RiskAssessment(
        risk_score=score,
        risk_classification=classification,
        ai_act_classification=ai_act,
        decision=decision,
        reason=reason,
        risk_factors=factors or ["No major risk factors identified"],
        required_controls=sorted(set(controls)),
        nist_mapping=nist_mapping_for(system),
        hipaa_review_required=system.phi_involved or system.clinical_or_patient_impact,
        evidence_required=sorted(set(evidence)),
    )


def create_record(system: AISystemCreate) -> AISystemRecord:
    risk = assess_risk(system)

    return AISystemRecord(
        **system.model_dump(),
        system_id=f"ai_sys_{uuid4().hex[:10]}",
        submitted_at=now(),
        risk_assessment=risk,
        final_outcome=risk.decision.value,
    )


def seed() -> None:
    if AI_SYSTEMS:
        return

    examples = [
        AISystemCreate(
            system_name="CareAssist Triage Summarizer",
            business_owner="Clinical Operations",
            model_owner="AI Governance Team",
            department="Healthcare",
            domain=BusinessDomain.healthcare,
            use_case="Summarize patient intake notes for care coordination review",
            model_name="care-summary-model",
            model_provider="internal",
            deployment_environment=DeploymentEnvironment.pilot,
            target_users="care coordinators",
            data_types=["PHI", "clinical notes"],
            phi_involved=True,
            customer_data_involved=False,
            automated_decisioning=False,
            clinical_or_patient_impact=True,
            human_oversight=HumanOversight.human_in_loop,
            approval_status=ApprovalStatus.pending_review,
        ),
        AISystemCreate(
            system_name="FraudRisk Account Monitor",
            business_owner="Enterprise Risk",
            model_owner="Financial AI Platform",
            department="Financial Services",
            domain=BusinessDomain.financial_services,
            use_case="Flag potentially fraudulent account activity for analyst review",
            model_name="fraud-risk-score-v1",
            model_provider="internal",
            deployment_environment=DeploymentEnvironment.sandbox,
            target_users="risk analysts",
            data_types=["customer data", "transaction metadata"],
            customer_data_involved=True,
            automated_decisioning=True,
            financial_or_credit_impact=True,
            human_oversight=HumanOversight.human_in_loop,
            approval_status=ApprovalStatus.pending_review,
        ),
        AISystemCreate(
            system_name="Content Discovery Personalizer",
            business_owner="Product",
            model_owner="Personalization Platform",
            department="Consumer Platform",
            domain=BusinessDomain.consumer_platform,
            use_case="Recommend content to users based on engagement signals",
            model_name="content-ranker-v2",
            model_provider="internal",
            deployment_environment=DeploymentEnvironment.pilot,
            target_users="consumer users",
            data_types=["engagement data", "preference signals"],
            customer_data_involved=True,
            automated_decisioning=False,
            human_oversight=HumanOversight.human_on_loop,
            approval_status=ApprovalStatus.submitted,
        ),
        AISystemCreate(
            system_name="Internal Policy Copilot",
            business_owner="Legal Operations",
            model_owner="Enterprise AI",
            department="Enterprise Internal",
            domain=BusinessDomain.enterprise_internal,
            use_case="Answer employee questions from approved internal policy documents",
            model_name="policy-copilot",
            model_provider="approved vendor",
            deployment_environment=DeploymentEnvironment.sandbox,
            target_users="employees",
            data_types=["internal policy documents"],
            customer_data_involved=False,
            automated_decisioning=False,
            human_oversight=HumanOversight.human_review_after,
            approval_status=ApprovalStatus.approved,
        ),
    ]

    for item in examples:
        AI_SYSTEMS.append(create_record(item))


@app.on_event("startup")
def startup() -> None:
    seed()


@app.get("/health", response_model=Health)
def health():
    return Health(
        status="ok",
        service="securethecloud-ai-governance-board",
        lab_mode=True,
        phase="1",
    )


@app.get("/api/ai-systems", response_model=list[AISystemRecord])
def list_ai_systems():
    return list(reversed(AI_SYSTEMS))


@app.post("/api/ai-systems", response_model=AISystemRecord)
def submit_ai_system(system: AISystemCreate):
    record = create_record(system)
    AI_SYSTEMS.append(record)
    return record


@app.post("/api/governance/preview", response_model=RiskAssessment)
def governance_preview(system: AISystemCreate):
    return assess_risk(system)


@app.get("/api/model-registry", response_model=list[ModelRegistryEntry])
def model_registry():
    entries: list[ModelRegistryEntry] = []

    for system in AI_SYSTEMS:
        monitoring_required = system.risk_assessment.risk_classification in {
            RiskClassification.high_risk,
            RiskClassification.prohibited,
        }

        entries.append(
            ModelRegistryEntry(
                system_id=system.system_id,
                model_name=system.model_name,
                model_provider=system.model_provider,
                model_owner=system.model_owner,
                use_case=system.use_case,
                domain=system.domain,
                risk_classification=system.risk_assessment.risk_classification,
                approval_status=system.approval_status,
                last_reviewed=system.submitted_at,
                monitoring_status="required" if monitoring_required else "standard",
            )
        )

    return list(reversed(entries))


@app.get("/api/evidence/{system_id}", response_model=AISystemRecord)
def evidence(system_id: str):
    for system in AI_SYSTEMS:
        if system.system_id == system_id:
            return system

    raise HTTPException(status_code=404, detail="AI system not found")


@app.get("/api/dashboard", response_model=DashboardSummary)
def dashboard():
    return DashboardSummary(
        total_ai_systems=len(AI_SYSTEMS),
        pending_reviews=sum(
            s.approval_status
            in {
                ApprovalStatus.submitted,
                ApprovalStatus.pending_review,
                ApprovalStatus.escalation_required,
            }
            for s in AI_SYSTEMS
        ),
        approved_systems=sum(s.approval_status == ApprovalStatus.approved for s in AI_SYSTEMS),
        rejected_systems=sum(s.approval_status == ApprovalStatus.rejected for s in AI_SYSTEMS),
        high_risk_systems=sum(
            s.risk_assessment.risk_classification == RiskClassification.high_risk
            for s in AI_SYSTEMS
        ),
        prohibited_systems=sum(
            s.risk_assessment.risk_classification == RiskClassification.prohibited
            for s in AI_SYSTEMS
        ),
        phi_involved_systems=sum(s.phi_involved for s in AI_SYSTEMS),
        customer_data_systems=sum(s.customer_data_involved for s in AI_SYSTEMS),
        systems_requiring_monitoring=sum(
            s.risk_assessment.risk_classification
            in {
                RiskClassification.high_risk,
                RiskClassification.prohibited,
            }
            for s in AI_SYSTEMS
        ),
        governance_coverage=100 if AI_SYSTEMS else 0,
    )

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
