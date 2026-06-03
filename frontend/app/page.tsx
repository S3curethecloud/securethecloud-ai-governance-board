"use client";

import { useEffect, useMemo, useState } from "react";
import type { CSSProperties } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8010";

type Dashboard = {
  total_ai_systems: number;
  pending_reviews: number;
  approved_systems: number;
  rejected_systems: number;
  high_risk_systems: number;
  prohibited_systems: number;
  phi_involved_systems: number;
  customer_data_systems: number;
  systems_requiring_monitoring: number;
  governance_coverage: number;
};

type RiskAssessment = {
  risk_score: number;
  risk_classification: string;
  ai_act_classification: string;
  decision: string;
  reason: string;
  risk_factors: string[];
  required_controls: string[];
  nist_mapping: Record<string, string[]>;
  hipaa_review_required: boolean;
  evidence_required: string[];
};

type AISystem = {
  system_id: string;
  system_name: string;
  business_owner: string;
  model_owner: string;
  department: string;
  domain: string;
  use_case: string;
  model_name: string;
  model_provider: string;
  deployment_environment: string;
  target_users: string;
  data_types: string[];
  phi_involved: boolean;
  customer_data_involved: boolean;
  automated_decisioning: boolean;
  clinical_or_patient_impact: boolean;
  financial_or_credit_impact: boolean;
  security_enforcement_impact: boolean;
  safety_critical: boolean;
  human_oversight: string;
  approval_status: string;
  submitted_at: string;
  risk_assessment: RiskAssessment;
  final_outcome: string;
};

type ModelRegistryEntry = {
  system_id: string;
  model_name: string;
  model_provider: string;
  model_owner: string;
  use_case: string;
  domain: string;
  risk_classification: string;
  approval_status: string;
  last_reviewed: string | null;
  monitoring_status: string;
};


type AISystemCreate = {
  system_name: string;
  business_owner: string;
  model_owner: string;
  department: string;
  domain: string;
  use_case: string;
  model_name: string;
  model_provider: string;
  deployment_environment: string;
  target_users: string;
  data_types: string[];
  phi_involved: boolean;
  customer_data_involved: boolean;
  automated_decisioning: boolean;
  clinical_or_patient_impact: boolean;
  financial_or_credit_impact: boolean;
  security_enforcement_impact: boolean;
  safety_critical: boolean;
  human_oversight: string;
  approval_status: string;
};

const boardModules = [
  ["Governance Committee", "Submitted systems, pending reviews, decisions, owners, and evidence.", "#22d3ee"],
  ["AI Model Registry", "Model owner, use case, provider, risk class, approval status, and monitoring.", "#6ee75f"],
  ["NIST AI RMF", "Govern, Map, Measure, and Manage review mapping.", "#38bdf8"],
  ["EU AI Act Classifier", "Minimal, limited, high-risk, and prohibited classification.", "#f59e0b"],
  ["HIPAA AI Review", "PHI detection, patient impact, approval workflow, and evidence package.", "#e879f9"]
];

const platformLayers = [
  ["AI System Intake", "Capture proposed AI systems before adoption or deployment."],
  ["Risk Scoring Engine", "Score AI systems based on data, impact, oversight, and environment."],
  ["Governance Review", "Route pending, high-risk, PHI, and prohibited systems to board review."],
  ["Regulatory Mapping", "Map systems to NIST AI RMF, EU AI Act style class, and HIPAA-style review."],
  ["Evidence Package", "Track required controls, review artifacts, and approval evidence."],
  ["Executive Oversight", "Show AI inventory posture, pending work, and governance coverage."]
];


const defaultForm: AISystemCreate = {
  system_name: "Clinical Intake Prioritization Assistant",
  business_owner: "Care Operations",
  model_owner: "AI Governance Team",
  department: "Healthcare",
  domain: "healthcare",
  use_case: "Prioritize patient intake messages for human care team review",
  model_name: "clinical-intake-priority-v1",
  model_provider: "internal",
  deployment_environment: "pilot",
  target_users: "care coordinators",
  data_types: ["PHI", "clinical notes"],
  phi_involved: true,
  customer_data_involved: false,
  automated_decisioning: true,
  clinical_or_patient_impact: true,
  financial_or_credit_impact: false,
  security_enforcement_impact: false,
  safety_critical: false,
  human_oversight: "human_in_loop",
  approval_status: "pending_review"
};

export default function Home() {
  const [dashboard, setDashboard] = useState<Dashboard | null>(null);
  const [systems, setSystems] = useState<AISystem[]>([]);
  const [registry, setRegistry] = useState<ModelRegistryEntry[]>([]);
  const [selectedSystemId, setSelectedSystemId] = useState<string | null>(null);
  const [status, setStatus] = useState("Loading AI governance telemetry...");
  const [form, setForm] = useState<AISystemCreate>(defaultForm);
  const [preview, setPreview] = useState<RiskAssessment | null>(null);
  const [submitStatus, setSubmitStatus] = useState("Ready for AI system intake.");
  const [reviewer, setReviewer] = useState("AI Governance Committee");
  const [reviewNote, setReviewNote] = useState("Reviewed for governance readiness, control evidence, and deployment risk.");
  const isMobile = useIsMobile();

  async function loadData() {
    const [dashboardRes, systemsRes, registryRes] = await Promise.all([
      fetch(`${API_BASE}/api/dashboard`, { cache: "no-store" }),
      fetch(`${API_BASE}/api/ai-systems`, { cache: "no-store" }),
      fetch(`${API_BASE}/api/model-registry`, { cache: "no-store" })
    ]);

    const nextSystems: AISystem[] = await systemsRes.json();

    setDashboard(await dashboardRes.json());
    setSystems(nextSystems);
    setRegistry(await registryRes.json());
    setSelectedSystemId((current) => current ?? nextSystems[0]?.system_id ?? null);
    setStatus("Live backend connected");
  }

  function updateForm<K extends keyof AISystemCreate>(key: K, value: AISystemCreate[K]) {
    setForm((current) => ({ ...current, [key]: value }));
  }

  function toggleDataType(value: string) {
    setForm((current) => {
      const exists = current.data_types.includes(value);
      return {
        ...current,
        data_types: exists
          ? current.data_types.filter((item) => item !== value)
          : [...current.data_types, value]
      };
    });
  }

  async function previewGovernance() {
    setSubmitStatus("Calculating governance preview...");

    const res = await fetch(`${API_BASE}/api/governance/preview`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form)
    });

    if (!res.ok) {
      setSubmitStatus("Governance preview failed.");
      return;
    }

    const nextPreview: RiskAssessment = await res.json();
    setPreview(nextPreview);
    setSubmitStatus(`Preview ready: ${nextPreview.decision.replaceAll("_", " ")} / ${nextPreview.risk_classification.replaceAll("_", " ")}`);
  }

  async function submitGovernedSystem() {
    setSubmitStatus("Submitting AI system for governance review...");

    const res = await fetch(`${API_BASE}/api/ai-systems`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form)
    });

    if (!res.ok) {
      setSubmitStatus("AI system submission failed.");
      return;
    }

    const created: AISystem = await res.json();
    setSubmitStatus(`Submitted: ${created.system_name} → ${created.final_outcome.replaceAll("_", " ")}`);
    setPreview(created.risk_assessment);
    await loadData();
    setSelectedSystemId(created.system_id);
  }

  async function submitCommitteeReview(systemId: string, action: string) {
    setSubmitStatus(`Submitting committee review: ${action.replaceAll("_", " ")}...`);

    const res = await fetch(`${API_BASE}/api/ai-systems/${systemId}/review`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        reviewer,
        action,
        note: reviewNote
      })
    });

    if (!res.ok) {
      setSubmitStatus("Committee review failed.");
      return;
    }

    const reviewed: AISystem = await res.json();
    setSubmitStatus(`Committee review recorded: ${reviewed.system_name} → ${reviewed.final_outcome.replaceAll("_", " ")}`);
    await loadData();
    setSelectedSystemId(reviewed.system_id);
  }

  useEffect(() => {
    loadData().catch((error) => setStatus(`Backend connection failed: ${error.message}`));
  }, []);

  const selectedSystem = useMemo(
    () => systems.find((system) => system.system_id === selectedSystemId) ?? systems[0],
    [systems, selectedSystemId]
  );

  const readinessPosture = useMemo(() => {
    if (!dashboard) {
      return "Loading";
    }

    if (dashboard.prohibited_systems > 0) {
      return "Board Attention Required";
    }

    if (dashboard.high_risk_systems > 0 || dashboard.phi_involved_systems > 0) {
      return "Governed Review Active";
    }

    if (dashboard.pending_reviews > 0) {
      return "Pending Review";
    }

    return "Demo Ready";
  }, [dashboard]);

  return (
    <main style={responsive(styles.page, isMobile && styles.pageMobile)}>
      <style jsx global>{`
        * {
          box-sizing: border-box;
        }

        html,
        body {
          margin: 0;
          max-width: 100%;
          overflow-x: hidden;
        }

        input,
        select,
        textarea,
        button {
          max-width: 100%;
        }

        @media (max-width: 980px) {
          body {
            background: #020617;
          }
        }
      `}</style>
      <section style={styles.shell}>
        <header style={responsive(styles.hero, isMobile && styles.heroMobile)}>
          <div>
            <div style={responsive(styles.brand, isMobile && styles.brandMobile)}>🛡️ SecureTheCloud</div>
            <p style={styles.kicker}>AI Governance Board</p>
            <h1 style={responsive(styles.title, isMobile && styles.titleMobile)}>
              {isMobile ? (
                <>
                  SecureTheCloud
                  <br />
                  AI Governance
                  <br />
                  Board
                </>
              ) : (
                "SecureTheCloud AI Governance Board"
              )}
            </h1>
            <p style={responsive(styles.subtitle, isMobile && styles.subtitleMobile)}>
              A simulated enterprise AI governance review platform for AI system intake, model registry,
              risk classification, regulatory mapping, approval evidence, and executive oversight.
            </p>
          </div>

          <div style={responsive(styles.doctrine, isMobile && styles.doctrineMobile)}>
            <strong>Core Principle</strong>
            <span>AI systems may be proposed, reviewed, risk-scored, mapped, approved, monitored, and governed.</span>
            <span>AI systems may not be deployed or connected to sensitive data without governance review and evidence.</span>
          </div>
        </header>

        <section style={responsive(styles.boundary, isMobile && styles.oneColumnGrid)}>
          <div style={styles.boundaryCard}>
            <strong>Client Demo Boundary</strong>
            <span>Simulated AI governance workflow. No real patient data, customer data, regulated systems, or production enforcement are connected.</span>
          </div>
          <div style={styles.boundaryCard}>
            <strong>Governance Story</strong>
            <span>Shows AI system intake, model registry, risk scoring, regulatory mapping, approval review, and evidence package readiness.</span>
          </div>
          <div style={styles.boundaryCard}>
            <strong>Leadership Signal</strong>
            <span>Designed to demonstrate AI governance program thinking, not just AI security engineering.</span>
          </div>
        </section>

        <section style={styles.fabric}>
          <h2 style={styles.sectionTitle}>AI Governance Operating Model</h2>
          <p style={styles.sectionSub}>Board-level governance services for enterprise AI system oversight.</p>

          <div style={responsive(styles.fabricGrid, isMobile && styles.oneColumnGrid)}>
            {boardModules.map(([name, desc, color]) => (
              <div key={name} style={{ ...styles.fabricCard, borderColor: color }}>
                <div style={{ ...styles.hex, color }}>⬡</div>
                <strong>{name}</strong>
                <span>{desc}</span>
              </div>
            ))}
          </div>
        </section>

        {dashboard && (
          <section style={responsive(styles.metrics, isMobile && styles.metricsMobile)}>
            <Metric label="AI Systems" value={dashboard.total_ai_systems} />
            <Metric label="Pending Reviews" value={dashboard.pending_reviews} />
            <Metric label="High Risk" value={dashboard.high_risk_systems} />
            <Metric label="PHI Involved" value={dashboard.phi_involved_systems} />
            <Metric label="Monitoring Required" value={dashboard.systems_requiring_monitoring} />
            <Metric label="Coverage" value={`${dashboard.governance_coverage}%`} />
          </section>
        )}

        <section style={responsive(styles.executive, isMobile && styles.executiveMobile)}>
          <div>
            <p style={styles.kicker}>Executive AI Governance View</p>
            <h2 style={styles.sectionTitleLeft}>AI System Risk & Review Center</h2>
            <p style={styles.sectionSubLeft}>
              Board-level visibility into proposed AI systems, pending reviews, high-risk inventory,
              PHI exposure, EU AI Act style classification, NIST AI RMF mapping, and governance evidence readiness.
            </p>
          </div>

          <div style={styles.posture}>
            <span>Governance Posture</span>
            <strong>{readinessPosture}</strong>
            <small>{status}</small>
          </div>
        </section>

        <section style={styles.layerSection}>
          <h2 style={styles.sectionTitle}>Governance Board Platform Layers</h2>
          <div style={responsive(styles.layerGrid, isMobile && styles.oneColumnGrid)}>
            {platformLayers.map(([name, desc]) => (
              <div key={name} style={responsive(styles.layerCard, isMobile && styles.layerCardMobile)}>
                <div style={styles.cube}>◇</div>
                <div>
                  <strong>{name}</strong>
                  <p>{desc}</p>
                  <span style={styles.ready}>Phase 2 Ready</span>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section style={responsive(styles.intakeGrid, isMobile && styles.oneColumnGrid)}>
          <div style={responsive(styles.panel, isMobile && styles.panelMobile)}>
            <p style={styles.kicker}>Phase 3 · AI System Intake</p>
            <h2 style={styles.panelTitle}>Submit AI System for Governance Review</h2>
            <p style={styles.muted}>
              Capture ownership, use case, deployment context, data exposure, impact flags, human oversight, and approval status before AI adoption.
            </p>

            <div style={responsive(styles.formGrid, isMobile && styles.oneColumnGrid)}>
              <Field label="AI System Name" value={form.system_name} onChange={(value) => updateForm("system_name", value)} />
              <Field label="Business Owner" value={form.business_owner} onChange={(value) => updateForm("business_owner", value)} />
              <Field label="Model Owner" value={form.model_owner} onChange={(value) => updateForm("model_owner", value)} />
              <Field label="Department" value={form.department} onChange={(value) => updateForm("department", value)} />
              <Field label="Model Name" value={form.model_name} onChange={(value) => updateForm("model_name", value)} />
              <Field label="Model Provider" value={form.model_provider} onChange={(value) => updateForm("model_provider", value)} />
            </div>

            <div style={responsive(styles.formGrid, isMobile && styles.oneColumnGrid)}>
              <SelectField
                label="Business Domain"
                value={form.domain}
                options={["healthcare", "financial_services", "security", "enterprise_internal", "consumer_platform", "research"]}
                onChange={(value) => updateForm("domain", value)}
              />
              <SelectField
                label="Deployment Environment"
                value={form.deployment_environment}
                options={["proposed", "sandbox", "pilot", "production"]}
                onChange={(value) => updateForm("deployment_environment", value)}
              />
              <SelectField
                label="Human Oversight"
                value={form.human_oversight}
                options={["none", "human_in_loop", "human_on_loop", "human_review_after"]}
                onChange={(value) => updateForm("human_oversight", value)}
              />
              <SelectField
                label="Approval Status"
                value={form.approval_status}
                options={["submitted", "pending_review", "approved", "rejected", "escalation_required"]}
                onChange={(value) => updateForm("approval_status", value)}
              />
            </div>

            <Field label="Target Users" value={form.target_users} onChange={(value) => updateForm("target_users", value)} />

            <label style={styles.label}>
              Use Case
              <textarea
                style={styles.textarea}
                value={form.use_case}
                onChange={(event) => updateForm("use_case", event.target.value)}
              />
            </label>

            <div style={styles.checkboxSection}>
              <strong>Data Types</strong>
              <div style={responsive(styles.checkGrid, isMobile && styles.oneColumnGrid)}>
                {["PHI", "clinical notes", "customer data", "transaction metadata", "engagement data", "internal policy documents", "biometric"].map((item) => (
                  <label key={item} style={styles.checkItem}>
                    <input
                      type="checkbox"
                      checked={form.data_types.includes(item)}
                      onChange={() => toggleDataType(item)}
                    />
                    {item}
                  </label>
                ))}
              </div>
            </div>

            <div style={styles.checkboxSection}>
              <strong>Impact Flags</strong>
              <div style={responsive(styles.checkGrid, isMobile && styles.oneColumnGrid)}>
                <BoolField label="PHI involved" checked={form.phi_involved} onChange={(value) => updateForm("phi_involved", value)} />
                <BoolField label="Customer data involved" checked={form.customer_data_involved} onChange={(value) => updateForm("customer_data_involved", value)} />
                <BoolField label="Automated decisioning" checked={form.automated_decisioning} onChange={(value) => updateForm("automated_decisioning", value)} />
                <BoolField label="Clinical / patient impact" checked={form.clinical_or_patient_impact} onChange={(value) => updateForm("clinical_or_patient_impact", value)} />
                <BoolField label="Financial / credit impact" checked={form.financial_or_credit_impact} onChange={(value) => updateForm("financial_or_credit_impact", value)} />
                <BoolField label="Security enforcement impact" checked={form.security_enforcement_impact} onChange={(value) => updateForm("security_enforcement_impact", value)} />
                <BoolField label="Safety critical" checked={form.safety_critical} onChange={(value) => updateForm("safety_critical", value)} />
              </div>
            </div>

            <div style={responsive(styles.buttonRow, isMobile && styles.oneColumnGrid)}>
              <button style={styles.secondaryButton} onClick={previewGovernance}>
                Preview Governance Decision
              </button>
              <button style={styles.primaryButton} onClick={submitGovernedSystem}>
                Submit to Governance Board
              </button>
            </div>

            <div style={styles.statusBox}>{submitStatus}</div>
          </div>

          <div style={responsive(styles.panel, isMobile && styles.panelMobile)}>
            <p style={styles.kicker}>Governance Preview</p>
            <h2 style={styles.panelTitle}>Risk, Classification & Required Controls</h2>
            <p style={styles.muted}>
              Preview evaluates the AI system before board submission.
            </p>

            {(preview ?? selectedSystem?.risk_assessment) && (
              <div style={styles.previewBox}>
                <div style={styles.recordHead}>
                  <strong>Governance Decision</strong>
                  <span style={classificationStyle((preview ?? selectedSystem!.risk_assessment).risk_classification)}>
                    {(preview ?? selectedSystem!.risk_assessment).risk_classification.replaceAll("_", " ").toUpperCase()}
                  </span>
                </div>

                <h3 style={styles.previewScore}>
                  {(preview ?? selectedSystem!.risk_assessment).risk_score}/100
                </h3>

                <p>
                  Decision: <b>{(preview ?? selectedSystem!.risk_assessment).decision.replaceAll("_", " ")}</b>
                </p>

                <p>
                  EU AI Act style class:{" "}
                  <b>{(preview ?? selectedSystem!.risk_assessment).ai_act_classification.replaceAll("_", " ")}</b>
                </p>

                <p>{(preview ?? selectedSystem!.risk_assessment).reason}</p>

                <div style={styles.evidenceBox}>
                  <strong>Risk Factors</strong>
                  <div style={styles.pillGrid}>
                    {(preview ?? selectedSystem!.risk_assessment).risk_factors.map((item) => (
                      <span key={item} style={styles.pill}>{item}</span>
                    ))}
                  </div>
                </div>

                <div style={styles.evidenceBox}>
                  <strong>Required Controls</strong>
                  <div style={styles.pillGrid}>
                    {(preview ?? selectedSystem!.risk_assessment).required_controls.map((item) => (
                      <span key={item} style={styles.pill}>{item}</span>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        </section>

        <section style={responsive(styles.reviewGrid, isMobile && styles.oneColumnGrid)}>
          <div style={responsive(styles.panel, isMobile && styles.panelMobile)}>
            <p style={styles.kicker}>Phase 4 · Governance Committee</p>
            <h2 style={styles.panelTitle}>Review Queue</h2>
            <p style={styles.muted}>
              Board-facing queue for systems requiring approval, controls, or escalation before deployment.
            </p>

            <div style={styles.stack}>
              {systems
                .filter((system) =>
                  ["submitted", "pending_review", "escalation_required", "controls_required"].includes(system.approval_status) ||
                  ["require_review", "require_controls", "escalation_required", "controls_required"].includes(system.final_outcome)
                )
                .map((system) => (
                  <button
                    key={system.system_id}
                    style={{
                      ...styles.record,
                      textAlign: "left",
                      borderColor: selectedSystem?.system_id === system.system_id ? "#22d3ee" : "#334155"
                    }}
                    onClick={() => setSelectedSystemId(system.system_id)}
                  >
                    <div style={styles.recordHead}>
                      <strong>{system.system_name}</strong>
                      <span style={classificationStyle(system.risk_assessment.risk_classification)}>
                        {system.risk_assessment.risk_classification.replaceAll("_", " ").toUpperCase()}
                      </span>
                    </div>
                    <p>{system.system_id}</p>
                    <p>
                      Owner: <b>{system.business_owner}</b> · Model owner: <b>{system.model_owner}</b>
                    </p>
                    <p>
                      Status: <b>{system.approval_status.replaceAll("_", " ")}</b> · Decision:{" "}
                      <b>{system.final_outcome.replaceAll("_", " ")}</b>
                    </p>
                  </button>
                ))}
            </div>
          </div>

          <div style={responsive(styles.panel, isMobile && styles.panelMobile)}>
            <p style={styles.kicker}>Board Decision</p>
            <h2 style={styles.panelTitle}>Committee Review Action</h2>
            <p style={styles.muted}>
              Record a simulated governance committee decision and refresh the evidence package.
            </p>

            {selectedSystem && (
              <div style={styles.selectedSystem}>
                <div style={styles.recordHead}>
                  <strong>{selectedSystem.system_name}</strong>
                  <span style={classificationStyle(selectedSystem.risk_assessment.risk_classification)}>
                    {selectedSystem.risk_assessment.risk_classification.replaceAll("_", " ").toUpperCase()}
                  </span>
                </div>

                <p>{selectedSystem.use_case}</p>

                <div style={responsive(styles.detailGrid, isMobile && styles.oneColumnGrid)}>
                  <div style={styles.detailBox}>
                    <span>Business Owner</span>
                    <b>{selectedSystem.business_owner}</b>
                  </div>
                  <div style={styles.detailBox}>
                    <span>Model Owner</span>
                    <b>{selectedSystem.model_owner}</b>
                  </div>
                  <div style={styles.detailBox}>
                    <span>Approval Status</span>
                    <b>{selectedSystem.approval_status.replaceAll("_", " ")}</b>
                  </div>
                  <div style={styles.detailBox}>
                    <span>Risk Score</span>
                    <b>{selectedSystem.risk_assessment.risk_score}/100</b>
                  </div>
                </div>

                <Field label="Reviewer" value={reviewer} onChange={setReviewer} />

                <label style={styles.label}>
                  Review Note
                  <textarea
                    style={styles.textarea}
                    value={reviewNote}
                    onChange={(event) => setReviewNote(event.target.value)}
                  />
                </label>

                <div style={responsive(styles.reviewActionGrid, isMobile && styles.oneColumnGrid)}>
                  <button style={styles.approveButton} onClick={() => submitCommitteeReview(selectedSystem.system_id, "approve")}>
                    Approve
                  </button>
                  <button style={styles.rejectButton} onClick={() => submitCommitteeReview(selectedSystem.system_id, "reject")}>
                    Reject
                  </button>
                  <button style={styles.secondaryButton} onClick={() => submitCommitteeReview(selectedSystem.system_id, "request_controls")}>
                    Request Controls
                  </button>
                  <button style={styles.escalateButton} onClick={() => submitCommitteeReview(selectedSystem.system_id, "escalate")}>
                    Escalate
                  </button>
                </div>
              </div>
            )}
          </div>
        </section>

        <section style={responsive(styles.workspace, isMobile && styles.oneColumnGrid)}>
          <div style={responsive(styles.panel, isMobile && styles.panelMobile)}>
            <p style={styles.kicker}>Governance Committee Workspace</p>
            <h2 style={styles.panelTitle}>Submitted AI Systems</h2>
            <p style={styles.muted}>Live seeded AI governance records from the Phase 1 backend.</p>

            <div style={styles.feed}>
              {systems.map((system) => (
                <article
                  key={system.system_id}
                  style={{
                    ...styles.record,
                    ...(selectedSystem?.system_id === system.system_id ? styles.selectedRecord : {})
                  }}
                  onClick={() => setSelectedSystemId(system.system_id)}
                >
                  <div style={styles.recordHead}>
                    <div>
                      <strong>{system.system_name}</strong>
                      <p>{system.system_id}</p>
                    </div>
                    <span style={classificationStyle(system.risk_assessment.risk_classification)}>
                      {system.risk_assessment.risk_classification.replaceAll("_", " ").toUpperCase()}
                    </span>
                  </div>
                  <p>{system.department} · {system.domain.replaceAll("_", " ")}</p>
                  <p>{system.use_case}</p>
                  <p>
                    Score: <b>{system.risk_assessment.risk_score}/100</b> · Decision:{" "}
                    <b>{system.risk_assessment.decision.replaceAll("_", " ")}</b>
                  </p>
                </article>
              ))}
            </div>
          </div>

          <div style={responsive(styles.panel, isMobile && styles.panelMobile)}>
            <p style={styles.kicker}>AI Model Registry</p>
            <h2 style={styles.panelTitle}>Model Inventory</h2>
            <p style={styles.muted}>Model ownership, use case, risk class, and monitoring posture.</p>

            <div style={styles.feed}>
              {registry.map((entry) => (
                <article key={entry.system_id} style={styles.record}>
                  <div style={styles.recordHead}>
                    <div>
                      <strong>{entry.model_name}</strong>
                      <p>{entry.model_provider}</p>
                    </div>
                    <span style={classificationStyle(entry.risk_classification)}>
                      {entry.risk_classification.replaceAll("_", " ").toUpperCase()}
                    </span>
                  </div>
                  <p>Owner: <b>{entry.model_owner}</b></p>
                  <p>Status: <b>{entry.approval_status.replaceAll("_", " ")}</b></p>
                  <p>Monitoring: <b>{entry.monitoring_status}</b></p>
                </article>
              ))}
            </div>
          </div>

          <div style={responsive({ ...styles.panel, ...styles.detailPanel }, isMobile && styles.panelMobile)}>
            <p style={styles.kicker}>Evidence Package Preview</p>
            <h2 style={styles.panelTitle}>Selected AI System Review</h2>

            {selectedSystem && (
              <>
                <div style={styles.selectedSystem}>
                  <div style={styles.recordHead}>
                    <div>
                      <strong>{selectedSystem.system_name}</strong>
                      <p>{selectedSystem.model_name} · {selectedSystem.model_provider}</p>
                    </div>
                    <span style={classificationStyle(selectedSystem.risk_assessment.ai_act_classification)}>
                      EU AI ACT: {selectedSystem.risk_assessment.ai_act_classification.replaceAll("_", " ").toUpperCase()}
                    </span>
                  </div>

                  <p>{selectedSystem.risk_assessment.reason}</p>

                  <div style={responsive(styles.detailGrid, isMobile && styles.oneColumnGrid)}>
                    <Detail label="Business Owner" value={selectedSystem.business_owner} />
                    <Detail label="Model Owner" value={selectedSystem.model_owner} />
                    <Detail label="Human Oversight" value={selectedSystem.human_oversight.replaceAll("_", " ")} />
                    <Detail label="Approval Status" value={selectedSystem.approval_status.replaceAll("_", " ")} />
                    <Detail label="PHI Involved" value={selectedSystem.phi_involved ? "yes" : "no"} />
                    <Detail label="HIPAA Review" value={selectedSystem.risk_assessment.hipaa_review_required ? "required" : "not required"} />
                  </div>
                </div>

                <div style={responsive(styles.mappingGrid, isMobile && styles.oneColumnGrid)}>
                  {Object.entries(selectedSystem.risk_assessment.nist_mapping).map(([fn, controls]) => (
                    <div key={fn} style={styles.mappingCard}>
                      <strong>{fn.toUpperCase()}</strong>
                      <ul>
                        {controls.map((control) => (
                          <li key={control}>{control}</li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>

                <div style={styles.evidenceBox}>
                  <strong>Evidence Required</strong>
                  <div style={styles.pillGrid}>
                    {selectedSystem.risk_assessment.evidence_required.map((item) => (
                      <span key={item} style={styles.pill}>{item}</span>
                    ))}
                  </div>
                </div>
              </>
            )}
          </div>
        </section>

        <footer style={styles.footer}>
          Simulated AI governance board · No real clinical, regulated, customer, or production systems are connected
        </footer>
      </section>
    </main>
  );
}

function responsive(...items: Array<CSSProperties | false | null | undefined>): CSSProperties {
  return Object.assign({}, ...items.filter(Boolean));
}

function useIsMobile() {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const update = () => setIsMobile(window.innerWidth <= 980);
    update();
    window.addEventListener("resize", update);
    return () => window.removeEventListener("resize", update);
  }, []);

  return isMobile;
}

function Field({
  label,
  value,
  onChange
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
}) {
  return (
    <label style={styles.label}>
      {label}
      <input style={styles.input} value={value} onChange={(event) => onChange(event.target.value)} />
    </label>
  );
}

function SelectField({
  label,
  value,
  options,
  onChange
}: {
  label: string;
  value: string;
  options: string[];
  onChange: (value: string) => void;
}) {
  return (
    <label style={styles.label}>
      {label}
      <select style={styles.input} value={value} onChange={(event) => onChange(event.target.value)}>
        {options.map((option) => (
          <option key={option} value={option}>
            {option.replaceAll("_", " ")}
          </option>
        ))}
      </select>
    </label>
  );
}

function BoolField({
  label,
  checked,
  onChange
}: {
  label: string;
  checked: boolean;
  onChange: (value: boolean) => void;
}) {
  return (
    <label style={styles.checkItem}>
      <input type="checkbox" checked={checked} onChange={(event) => onChange(event.target.checked)} />
      {label}
    </label>
  );
}

function Metric({ label, value }: { label: string; value: number | string }) {
  return (
    <div style={styles.metric}>
      <strong>{value}</strong>
      <span>{label}</span>
    </div>
  );
}

function Detail({ label, value }: { label: string; value: string }) {
  return (
    <div style={styles.detail}>
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function classificationStyle(value: string): CSSProperties {
  if (value === "prohibited") {
    return { ...styles.badge, borderColor: "#ef4444", color: "#fca5a5", background: "rgba(127,29,29,.42)" };
  }

  if (value === "high_risk") {
    return { ...styles.badge, borderColor: "#f59e0b", color: "#fcd34d", background: "rgba(69,26,3,.45)" };
  }

  if (value === "limited") {
    return { ...styles.badge, borderColor: "#38bdf8", color: "#bae6fd", background: "rgba(8,47,73,.45)" };
  }

  return { ...styles.badge, borderColor: "#22c55e", color: "#86efac", background: "rgba(20,83,45,.45)" };
}

const styles: Record<string, CSSProperties> = {
  page: {
    minHeight: "100vh",
    background: "radial-gradient(circle at top left,#132b46,#06111f 45%,#020617)",
    color: "#eaf2ff",
    fontFamily: "Inter, Arial, sans-serif",
    padding: 28
  },
  shell: { maxWidth: 1500, margin: "0 auto", overflowX: "hidden" },
  hero: {
    border: "1px solid #334155",
    borderRadius: 24,
    padding: 34,
    display: "flex",
    justifyContent: "space-between",
    gap: 24,
    background: "rgba(15,23,42,.78)",
    boxShadow: "0 24px 80px rgba(0,0,0,.35)"
  },
  brand: { fontSize: 24, fontWeight: 900, color: "#facc15", marginBottom: 18 },
  kicker: { color: "#67e8f9", textTransform: "uppercase", letterSpacing: 2, fontSize: 12, fontWeight: 800 },
  title: { fontSize: 56, lineHeight: 0.95, margin: "10px 0", fontWeight: 950 },
  subtitle: { color: "#cbd5e1", fontSize: 18, maxWidth: 850 },
  doctrine: {
    border: "1px solid #94a3b8",
    borderRadius: 16,
    padding: 18,
    minWidth: 360,
    display: "grid",
    gap: 10,
    background: "rgba(2,6,23,.6)"
  },
  boundary: { display: "grid", gridTemplateColumns: "repeat(3, minmax(0, 1fr))", gap: 14, marginTop: 18 },
  boundaryCard: {
    border: "1px solid #22d3ee",
    borderRadius: 16,
    padding: 16,
    background: "rgba(8,47,73,.28)",
    display: "grid",
    gap: 8
  },
  fabric: {
    marginTop: 18,
    border: "1px solid #475569",
    borderRadius: 22,
    padding: 22,
    background: "rgba(2,6,23,.6)"
  },
  sectionTitle: { textAlign: "center", textTransform: "uppercase", letterSpacing: 5, fontSize: 24, margin: 0 },
  sectionTitleLeft: { textTransform: "uppercase", letterSpacing: 4, fontSize: 24, margin: "4px 0" },
  sectionSub: { textAlign: "center", color: "#cbd5e1", marginTop: 6 },
  sectionSubLeft: { color: "#cbd5e1", marginTop: 6, maxWidth: 820 },
  fabricGrid: { display: "grid", gridTemplateColumns: "repeat(5, minmax(0, 1fr))", gap: 16, marginTop: 18 },
  fabricCard: {
    border: "2px solid",
    borderRadius: 12,
    padding: 18,
    background: "linear-gradient(135deg,rgba(8,47,73,.55),rgba(2,6,23,.8))",
    minHeight: 132,
    display: "grid",
    gap: 8
  },
  hex: { fontSize: 34 },
  metrics: { display: "grid", gridTemplateColumns: "repeat(6, minmax(0, 1fr))", gap: 14, marginTop: 18 },
  metric: {
    border: "1px solid #334155",
    borderRadius: 18,
    padding: 18,
    background: "rgba(15,23,42,.8)",
    display: "grid",
    gap: 6
  },
  executive: {
    marginTop: 18,
    border: "1px solid #475569",
    borderRadius: 22,
    padding: 22,
    background: "linear-gradient(135deg,rgba(15,23,42,.9),rgba(2,6,23,.72))",
    display: "flex",
    justifyContent: "space-between",
    gap: 18
  },
  posture: {
    minWidth: 320,
    border: "1px solid #6ee75f",
    borderRadius: 16,
    padding: 18,
    background: "rgba(20,83,45,.22)",
    display: "grid",
    gap: 8
  },
  layerSection: {
    marginTop: 18,
    border: "1px solid #475569",
    borderRadius: 22,
    padding: 22,
    background: "rgba(2,6,23,.6)"
  },
  layerGrid: { display: "grid", gridTemplateColumns: "repeat(3, minmax(0, 1fr))", gap: 14, marginTop: 18 },
  layerCard: {
    border: "1px solid #22d3ee",
    borderRadius: 14,
    padding: 18,
    display: "flex",
    gap: 14,
    background: "rgba(8,47,73,.28)"
  },
  cube: { color: "#6ee75f", fontSize: 36 },
  ready: {
    display: "inline-block",
    marginTop: 8,
    border: "1px solid #6ee75f",
    color: "#86efac",
    borderRadius: 999,
    padding: "4px 12px",
    fontSize: 12
  },
  reviewGrid: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 18, marginTop: 18 },
  reviewActionGrid: { display: "grid", gridTemplateColumns: "repeat(4, minmax(0, 1fr))", gap: 10, marginTop: 14 },
  approveButton: {
    border: "0",
    borderRadius: 12,
    background: "#22c55e",
    color: "#020617",
    padding: "14px 16px",
    fontWeight: 900,
    cursor: "pointer"
  },
  rejectButton: {
    border: "0",
    borderRadius: 12,
    background: "#f87171",
    color: "#020617",
    padding: "14px 16px",
    fontWeight: 900,
    cursor: "pointer"
  },
  escalateButton: {
    border: "0",
    borderRadius: 12,
    background: "#f59e0b",
    color: "#020617",
    padding: "14px 16px",
    fontWeight: 900,
    cursor: "pointer"
  },
  intakeGrid: { display: "grid", gridTemplateColumns: "1.25fr .9fr", gap: 18, marginTop: 18 },
  formGrid: { display: "grid", gridTemplateColumns: "repeat(2, minmax(0, 1fr))", gap: 12, marginTop: 14 },
  label: { display: "grid", gap: 6, color: "#dbeafe", fontSize: 13, fontWeight: 800, marginTop: 12 },
  input: {
    width: "100%",
    border: "1px solid #334155",
    borderRadius: 10,
    background: "#020617",
    color: "#eaf2ff",
    padding: "12px 14px",
    fontSize: 14,
    boxSizing: "border-box"
  },
  textarea: {
    width: "100%",
    minHeight: 86,
    border: "1px solid #334155",
    borderRadius: 10,
    background: "#020617",
    color: "#eaf2ff",
    padding: "12px 14px",
    fontSize: 14,
    boxSizing: "border-box"
  },
  checkboxSection: {
    border: "1px solid #334155",
    borderRadius: 14,
    padding: 14,
    marginTop: 14,
    background: "rgba(2,6,23,.45)"
  },
  checkGrid: { display: "grid", gridTemplateColumns: "repeat(2, minmax(0, 1fr))", gap: 10, marginTop: 10 },
  checkItem: { display: "flex", alignItems: "center", gap: 8, color: "#dbeafe", fontSize: 13, fontWeight: 700 },
  buttonRow: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginTop: 16 },
  primaryButton: {
    border: "0",
    borderRadius: 12,
    background: "#22d3ee",
    color: "#020617",
    padding: "14px 16px",
    fontWeight: 900,
    cursor: "pointer"
  },
  secondaryButton: {
    border: "1px solid #22d3ee",
    borderRadius: 12,
    background: "rgba(8,47,73,.4)",
    color: "#eaf2ff",
    padding: "14px 16px",
    fontWeight: 900,
    cursor: "pointer"
  },
  statusBox: {
    border: "1px solid #22d3ee",
    borderRadius: 12,
    padding: 12,
    color: "#67e8f9",
    background: "rgba(8,47,73,.32)",
    marginTop: 14,
    fontWeight: 800
  },
  previewBox: {
    border: "1px solid #22d3ee",
    borderRadius: 16,
    padding: 16,
    marginTop: 18,
    background: "#020617"
  },
  previewScore: { fontSize: 48, margin: "16px 0 6px", color: "#fcd34d" },
  workspace: { display: "grid", gridTemplateColumns: "1fr 1fr 1.45fr", gap: 18, marginTop: 18 },
  panel: {
    border: "1px solid #334155",
    borderRadius: 22,
    padding: 24,
    background: "rgba(15,23,42,.86)",
    minWidth: 0,
    overflow: "hidden"
  },
  detailPanel: { minHeight: 600 },
  panelTitle: { fontSize: 26, margin: "8px 0" },
  muted: { color: "#cbd5e1" },
  feed: { display: "grid", gap: 14, marginTop: 18 },
  record: { border: "1px solid #334155", borderRadius: 16, padding: 16, background: "#020617", cursor: "pointer", overflowWrap: "anywhere" },
  selectedRecord: { borderColor: "#22d3ee", boxShadow: "0 0 0 1px rgba(34,211,238,.35)" },
  recordHead: { display: "flex", justifyContent: "space-between", gap: 12, alignItems: "start" },
  badge: {
    border: "1px solid #38bdf8",
    maxWidth: "100%",
    overflowWrap: "anywhere",
    color: "#bae6fd",
    background: "rgba(8,47,73,.45)",
    borderRadius: 999,
    padding: "8px 12px",
    fontSize: 11,
    fontWeight: 900,
    whiteSpace: "normal"
  },
  selectedSystem: {
    border: "1px solid #22d3ee",
    overflowWrap: "anywhere",
    borderRadius: 16,
    padding: 16,
    marginTop: 18,
    background: "#020617"
  },
  detailGrid: { display: "grid", gridTemplateColumns: "repeat(3, minmax(0, 1fr))", gap: 10, marginTop: 14 },
  detail: { border: "1px solid #334155", borderRadius: 12, padding: 12, display: "grid", gap: 6 },
  mappingGrid: { display: "grid", gridTemplateColumns: "repeat(2, minmax(0, 1fr))", gap: 12, marginTop: 16 },
  mappingCard: {
    border: "1px solid #334155",
    borderRadius: 14,
    padding: 14,
    background: "#020617",
    color: "#cbd5e1"
  },
  evidenceBox: {
    border: "1px solid #6ee75f",
    borderRadius: 16,
    padding: 16,
    marginTop: 16,
    background: "rgba(20,83,45,.18)"
  },
  pillGrid: { display: "flex", flexWrap: "wrap", gap: 8, marginTop: 12 },
  pill: {
    border: "1px solid #334155",
    overflowWrap: "anywhere",
    borderRadius: 999,
    padding: "6px 10px",
    color: "#cbd5e1",
    background: "#020617",
    fontSize: 12
  },
  pageMobile: {
    padding: 12,
    overflowX: "hidden"
  },
  heroMobile: {
    flexDirection: "column",
    padding: 22
  },
  titleMobile: {
    fontSize: 34,
    lineHeight: 1.04,
    letterSpacing: "-1px",
    maxWidth: "100%",
    overflowWrap: "anywhere",
    wordBreak: "break-word"
  },
  doctrineMobile: {
    minWidth: 0,
    width: "100%"
  },
  subtitleMobile: {
    fontSize: 16,
    maxWidth: "100%",
    overflowWrap: "anywhere"
  },
  brandMobile: {
    fontSize: 22,
    overflowWrap: "anywhere"
  },
  oneColumnGrid: {
    gridTemplateColumns: "1fr"
  },
  metricsMobile: {
    gridTemplateColumns: "repeat(2, minmax(0, 1fr))"
  },
  executiveMobile: {
    flexDirection: "column"
  },
  panelMobile: {
    padding: 18,
    width: "100%"
  },
  cardMobile: {
    minHeight: "auto"
  },
  layerCardMobile: {
    alignItems: "flex-start"
  },
  footer: {
    marginTop: 18,
    border: "1px solid #334155",
    borderRadius: 14,
    padding: 14,
    textAlign: "center",
    color: "#cbd5e1",
    background: "rgba(15,23,42,.75)"
  }
};
