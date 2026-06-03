from pathlib import Path

p = Path("frontend/app/page.tsx")
s = p.read_text()

# Add HIPAA review submit helper before useEffect.
use_effect_marker = '''  useEffect(() => {'''

hipaa_function = '''  async function submitHipaaReview(systemId: string, action: string, note: string) {
    setSubmitStatus(`Submitting HIPAA-style review: ${action.replaceAll("_", " ")}...`);

    const res = await fetch(`${API_BASE}/api/ai-systems/${systemId}/review`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        reviewer: "HIPAA AI Review Board",
        action,
        note
      })
    });

    if (!res.ok) {
      setSubmitStatus("HIPAA-style review failed.");
      return;
    }

    const reviewed: AISystem = await res.json();
    setSubmitStatus(`HIPAA-style review recorded: ${reviewed.system_name} → ${reviewed.final_outcome.replaceAll("_", " ")}`);
    await loadData();
    setSelectedSystemId(reviewed.system_id);
  }

'''

if "submitHipaaReview(" not in s:
    if use_effect_marker not in s:
        raise SystemExit("useEffect marker not found")
    s = s.replace(use_effect_marker, hipaa_function + use_effect_marker)


# Add HIPAA system memo before readiness posture.
readiness_marker = '''  const readinessPosture = useMemo(() => {'''

hipaa_memo = '''  const hipaaSystems = useMemo(
    () =>
      systems.filter(
        (system) =>
          system.risk_assessment.hipaa_review_required ||
          system.phi_involved ||
          system.clinical_or_patient_impact ||
          system.data_types.some((item) => item.toLowerCase().includes("phi") || item.toLowerCase().includes("clinical"))
      ),
    [systems]
  );

  const hipaaSelected = useMemo(
    () => hipaaSystems.find((system) => system.system_id === selectedSystemId) ?? hipaaSystems[0],
    [hipaaSystems, selectedSystemId]
  );

'''

if "const hipaaSystems = useMemo" not in s:
    if readiness_marker not in s:
        raise SystemExit("readiness marker not found")
    s = s.replace(readiness_marker, hipaa_memo + readiness_marker)


# Add Phase 6 UI before the existing Phase 4 review grid.
review_grid_marker = '''        <section style={responsive(styles.reviewGrid, isMobile && styles.oneColumnGrid)}>'''

hipaa_section = '''        <section style={responsive(styles.hipaaGrid, isMobile && styles.oneColumnGrid)}>
          <div style={responsive(styles.panel, isMobile && styles.panelMobile)}>
            <p style={styles.kicker}>Phase 6 · HIPAA AI Review Board</p>
            <h2 style={styles.panelTitle}>PHI & Patient Impact Review Queue</h2>
            <p style={styles.muted}>
              Board-facing queue for AI systems involving PHI, clinical notes, patient impact, or HIPAA-style governance review.
            </p>

            {hipaaSystems.length === 0 ? (
              <div style={styles.emptyState}>No HIPAA-style AI reviews are currently required.</div>
            ) : (
              <div style={styles.queueList}>
                {hipaaSystems.map((system) => (
                  <button
                    key={system.system_id}
                    type="button"
                    onClick={() => setSelectedSystemId(system.system_id)}
                    style={{
                      ...styles.queueButton,
                      ...(hipaaSelected?.system_id === system.system_id ? styles.activeQueueButton : {})
                    }}
                  >
                    <div style={styles.recordHead}>
                      <strong>{system.system_name}</strong>
                      <span style={classificationStyle(system.risk_assessment.risk_classification)}>
                        {system.risk_assessment.risk_classification.replaceAll("_", " ").toUpperCase()}
                      </span>
                    </div>
                    <p>{system.system_id}</p>
                    <p>
                      PHI: <b>{system.phi_involved ? "yes" : "no"}</b> · Clinical impact:{" "}
                      <b>{system.clinical_or_patient_impact ? "yes" : "no"}</b>
                    </p>
                    <p>
                      Decision: <b>{system.risk_assessment.decision.replaceAll("_", " ")}</b>
                    </p>
                  </button>
                ))}
              </div>
            )}
          </div>

          <div style={responsive(styles.panel, isMobile && styles.panelMobile)}>
            <p style={styles.kicker}>Privacy / Clinical Governance</p>
            <h2 style={styles.panelTitle}>HIPAA-Style Review Action</h2>
            <p style={styles.muted}>
              Record a simulated PHI-sensitive AI review decision and refresh the evidence package.
            </p>

            {hipaaSelected ? (
              <div style={styles.selectedSystem}>
                <div style={styles.recordHead}>
                  <strong>{hipaaSelected.system_name}</strong>
                  <span style={classificationStyle(hipaaSelected.risk_assessment.risk_classification)}>
                    {hipaaSelected.risk_assessment.risk_classification.replaceAll("_", " ").toUpperCase()}
                  </span>
                </div>

                <p>{hipaaSelected.use_case}</p>

                <div style={responsive(styles.detailGrid, isMobile && styles.oneColumnGrid)}>
                  <div style={styles.detailBox}>
                    <span>PHI Involved</span>
                    <b>{hipaaSelected.phi_involved ? "yes" : "no"}</b>
                  </div>
                  <div style={styles.detailBox}>
                    <span>Clinical Impact</span>
                    <b>{hipaaSelected.clinical_or_patient_impact ? "yes" : "no"}</b>
                  </div>
                  <div style={styles.detailBox}>
                    <span>HIPAA Review</span>
                    <b>{hipaaSelected.risk_assessment.hipaa_review_required ? "required" : "not required"}</b>
                  </div>
                  <div style={styles.detailBox}>
                    <span>Human Oversight</span>
                    <b>{hipaaSelected.human_oversight.replaceAll("_", " ")}</b>
                  </div>
                </div>

                <div style={styles.evidencePanel}>
                  <h3 style={styles.mappingTitle}>Data Types</h3>
                  <div style={styles.chipWrap}>
                    {hipaaSelected.data_types.map((item) => (
                      <span key={item} style={styles.chip}>{item}</span>
                    ))}
                  </div>
                </div>

                <div style={styles.evidencePanel}>
                  <h3 style={styles.mappingTitle}>HIPAA-Style Evidence</h3>
                  <div style={styles.chipWrap}>
                    {hipaaSelected.risk_assessment.evidence_required.map((item) => (
                      <span key={item} style={styles.chip}>{item}</span>
                    ))}
                  </div>
                </div>

                <div style={styles.evidencePanel}>
                  <h3 style={styles.mappingTitle}>Required Controls</h3>
                  <div style={styles.chipWrap}>
                    {hipaaSelected.risk_assessment.required_controls.map((item) => (
                      <span key={item} style={styles.chip}>{item}</span>
                    ))}
                  </div>
                </div>

                <div style={responsive(styles.actionGrid, isMobile && styles.oneColumnGrid)}>
                  <button
                    style={styles.approveButton}
                    onClick={() =>
                      submitHipaaReview(
                        hipaaSelected.system_id,
                        "approve",
                        "HIPAA-style AI review approved with documented ownership, human oversight, and evidence package."
                      )
                    }
                  >
                    Approve Review
                  </button>
                  <button
                    style={styles.controlButton}
                    onClick={() =>
                      submitHipaaReview(
                        hipaaSelected.system_id,
                        "request_controls",
                        "PHI minimization, patient-impact evidence, and human oversight controls required before approval."
                      )
                    }
                  >
                    Request PHI Controls
                  </button>
                  <button
                    style={styles.escalateButton}
                    onClick={() =>
                      submitHipaaReview(
                        hipaaSelected.system_id,
                        "escalate",
                        "Escalated for privacy, clinical safety, and governance board review."
                      )
                    }
                  >
                    Escalate Privacy Review
                  </button>
                </div>
              </div>
            ) : (
              <div style={styles.emptyState}>Select a PHI-sensitive AI system to review.</div>
            )}
          </div>
        </section>

'''

if "HIPAA AI Review Board" not in s:
    if review_grid_marker not in s:
        raise SystemExit("review grid marker not found")
    s = s.replace(review_grid_marker, hipaa_section + review_grid_marker)


# Add styles.
style_marker = '''  regulatoryGrid: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 18, marginTop: 18 },'''

style_insert = '''  hipaaGrid: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 18, marginTop: 18 },
  queueList: { display: "grid", gap: 12, marginTop: 16 },
  queueButton: {
    border: "1px solid #334155",
    borderRadius: 16,
    background: "#020617",
    color: "#eaf2ff",
    padding: 16,
    textAlign: "left",
    cursor: "pointer",
    width: "100%",
    overflowWrap: "anywhere"
  },
  activeQueueButton: {
    borderColor: "#22d3ee",
    boxShadow: "0 0 0 1px rgba(34, 211, 238, .25)"
  },
  emptyState: {
    border: "1px dashed #475569",
    borderRadius: 16,
    padding: 18,
    color: "#cbd5e1",
    marginTop: 16,
    textAlign: "center"
  },
  actionGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(3, minmax(0, 1fr))",
    gap: 10,
    marginTop: 16
  },
  approveButton: {
    border: "0",
    borderRadius: 12,
    padding: "14px 16px",
    background: "#22c55e",
    color: "#020617",
    fontWeight: 900,
    cursor: "pointer"
  },
  controlButton: {
    border: "1px solid #22d3ee",
    borderRadius: 12,
    padding: "14px 16px",
    background: "#082f49",
    color: "#eaf2ff",
    fontWeight: 900,
    cursor: "pointer"
  },
  escalateButton: {
    border: "0",
    borderRadius: 12,
    padding: "14px 16px",
    background: "#f59e0b",
    color: "#020617",
    fontWeight: 900,
    cursor: "pointer"
  },
'''

if "hipaaGrid:" not in s:
    if style_marker not in s:
        raise SystemExit("regulatoryGrid style marker not found")
    s = s.replace(style_marker, style_insert + style_marker)

p.write_text(s)
