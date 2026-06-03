from pathlib import Path

p = Path("frontend/app/page.tsx")
s = p.read_text()

# Add reviewer state.
old = '''  const [submitStatus, setSubmitStatus] = useState("Ready for AI system intake.");
  const isMobile = useIsMobile();
'''
new = '''  const [submitStatus, setSubmitStatus] = useState("Ready for AI system intake.");
  const [reviewer, setReviewer] = useState("AI Governance Committee");
  const [reviewNote, setReviewNote] = useState("Reviewed for governance readiness, control evidence, and deployment risk.");
  const isMobile = useIsMobile();
'''
if old in s and "const [reviewer, setReviewer]" not in s:
    s = s.replace(old, new)

# Add review function before useEffect.
marker = '''  useEffect(() => {
    loadData().catch((error) => setStatus(`Backend connection failed: ${error.message}`));
  }, []);
'''
review_fn = '''  async function submitCommitteeReview(systemId: string, action: string) {
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

'''
if marker in s and "submitCommitteeReview" not in s:
    s = s.replace(marker, review_fn + marker)

# Insert review workspace before existing workspace.
marker = '''        <section style={responsive(styles.workspace, isMobile && styles.oneColumnGrid)}>'''
review_section = '''        <section style={responsive(styles.reviewGrid, isMobile && styles.oneColumnGrid)}>
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

''' + marker

if marker not in s:
    raise SystemExit("Workspace marker not found")

if "Phase 4 · Governance Committee" not in s:
    s = s.replace(marker, review_section)

# Add styles.
style_marker = '''  intakeGrid: { display: "grid", gridTemplateColumns: "1.25fr .9fr", gap: 18, marginTop: 18 },'''
style_insert = '''  reviewGrid: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 18, marginTop: 18 },
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
'''
if style_marker in s and "reviewGrid:" not in s:
    s = s.replace(style_marker, style_insert + style_marker)

p.write_text(s)
