from pathlib import Path

p = Path("frontend/app/page.tsx")
s = p.read_text()

marker = '''        <section style={responsive(styles.reviewGrid, isMobile && styles.oneColumnGrid)}>'''

section = '''        {selectedSystem && (
          <section style={responsive(styles.regulatoryGrid, isMobile && styles.oneColumnGrid)}>
            <div style={responsive(styles.panel, isMobile && styles.panelMobile)}>
              <p style={styles.kicker}>Phase 5 · Regulatory Mapping</p>
              <h2 style={styles.panelTitle}>NIST AI RMF Mapping Console</h2>
              <p style={styles.muted}>
                Governance evidence mapped across Govern, Map, Measure, and Manage for the selected AI system.
              </p>

              <div style={responsive(styles.nistGrid, isMobile && styles.oneColumnGrid)}>
                {["govern", "map", "measure", "manage"].map((fn) => (
                  <div key={fn} style={styles.mappingBox}>
                    <h3 style={styles.mappingTitle}>{fn.toUpperCase()}</h3>
                    <ul style={styles.cleanList}>
                      {(selectedSystem.risk_assessment.nist_mapping[fn] ?? []).map((item) => (
                        <li key={item}>{item}</li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            </div>

            <div style={responsive(styles.panel, isMobile && styles.panelMobile)}>
              <p style={styles.kicker}>Phase 5 · AI Act / HIPAA-Style Review</p>
              <h2 style={styles.panelTitle}>Classification & Evidence Package</h2>
              <p style={styles.muted}>
                Explains why the selected system receives its risk classification and what evidence is required.
              </p>

              <div style={styles.selectedSystem}>
                <div style={styles.recordHead}>
                  <strong>{selectedSystem.system_name}</strong>
                  <span style={classificationStyle(selectedSystem.risk_assessment.ai_act_classification)}>
                    EU AI ACT: {selectedSystem.risk_assessment.ai_act_classification.replaceAll("_", " ").toUpperCase()}
                  </span>
                </div>

                <p>
                  Risk class: <b>{selectedSystem.risk_assessment.risk_classification.replaceAll("_", " ")}</b>
                </p>
                <p>
                  Decision: <b>{selectedSystem.risk_assessment.decision.replaceAll("_", " ")}</b>
                </p>
                <p>{selectedSystem.risk_assessment.reason}</p>

                <div style={responsive(styles.detailGrid, isMobile && styles.oneColumnGrid)}>
                  <div style={styles.detailBox}>
                    <span>HIPAA-Style Review</span>
                    <b>{selectedSystem.risk_assessment.hipaa_review_required ? "required" : "not required"}</b>
                  </div>
                  <div style={styles.detailBox}>
                    <span>PHI Involved</span>
                    <b>{selectedSystem.phi_involved ? "yes" : "no"}</b>
                  </div>
                  <div style={styles.detailBox}>
                    <span>Customer Data</span>
                    <b>{selectedSystem.customer_data_involved ? "yes" : "no"}</b>
                  </div>
                  <div style={styles.detailBox}>
                    <span>Monitoring</span>
                    <b>
                      {["high_risk", "prohibited"].includes(selectedSystem.risk_assessment.risk_classification)
                        ? "required"
                        : "standard"}
                    </b>
                  </div>
                </div>

                <div style={styles.evidencePanel}>
                  <h3 style={styles.mappingTitle}>Risk Factors</h3>
                  <div style={styles.chipWrap}>
                    {selectedSystem.risk_assessment.risk_factors.map((factor) => (
                      <span key={factor} style={styles.chip}>{factor}</span>
                    ))}
                  </div>
                </div>

                <div style={styles.evidencePanel}>
                  <h3 style={styles.mappingTitle}>Required Controls</h3>
                  <div style={styles.chipWrap}>
                    {selectedSystem.risk_assessment.required_controls.map((control) => (
                      <span key={control} style={styles.chip}>{control}</span>
                    ))}
                  </div>
                </div>

                <div style={styles.evidencePanel}>
                  <h3 style={styles.mappingTitle}>Evidence Required</h3>
                  <div style={styles.chipWrap}>
                    {selectedSystem.risk_assessment.evidence_required.map((evidence) => (
                      <span key={evidence} style={styles.chip}>{evidence}</span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </section>
        )}

'''

if marker not in s:
    raise SystemExit("Phase 4 review grid marker not found")

if "NIST AI RMF Mapping Console" not in s:
    s = s.replace(marker, section + marker)

style_marker = '''  reviewGrid: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 18, marginTop: 18 },'''

style_insert = '''  regulatoryGrid: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 18, marginTop: 18 },
  nistGrid: { display: "grid", gridTemplateColumns: "repeat(2, minmax(0, 1fr))", gap: 14, marginTop: 16 },
  mappingBox: {
    border: "1px solid #334155",
    borderRadius: 16,
    padding: 16,
    background: "#020617",
    color: "#eaf2ff",
    overflowWrap: "anywhere"
  },
  mappingTitle: {
    margin: "0 0 10px",
    color: "#eaf2ff",
    fontSize: 16,
    letterSpacing: ".05em"
  },
  cleanList: {
    margin: 0,
    paddingLeft: 18,
    color: "#eaf2ff",
    lineHeight: 1.35
  },
  evidencePanel: {
    border: "1px solid #14532d",
    borderRadius: 16,
    padding: 16,
    background: "rgba(20, 83, 45, .18)",
    marginTop: 14
  },
  chipWrap: {
    display: "flex",
    flexWrap: "wrap",
    gap: 8
  },
  chip: {
    border: "1px solid #334155",
    background: "#020617",
    color: "#eaf2ff",
    borderRadius: 999,
    padding: "7px 10px",
    fontSize: 12,
    fontWeight: 800,
    maxWidth: "100%",
    overflowWrap: "anywhere"
  },
'''

if style_marker not in s:
    raise SystemExit("reviewGrid style marker not found")

if "regulatoryGrid:" not in s:
    s = s.replace(style_marker, style_insert + style_marker)

# Update platform layer badge from Phase 2 Ready to Phase 5 Ready for regulatory mapping if desired.
s = s.replace(">Phase 2 Ready</span>", ">Phase 5 Ready</span>")

p.write_text(s)
