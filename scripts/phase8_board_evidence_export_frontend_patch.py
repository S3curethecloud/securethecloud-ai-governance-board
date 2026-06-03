from pathlib import Path

p = Path("frontend/app/page.tsx")
s = p.read_text()

if "Phase 8 · Board Evidence Export" in s:
    print("Phase 8 frontend panel already present.")
    raise SystemExit(0)

helper_marker = "const defaultForm"
helper = r'''
function buildBoardDecisionMemo(system: AISystem | null): string {
  if (!system) {
    return "No AI system selected.";
  }

  const risk = system.risk_assessment;
  const controls = risk.required_controls.length
    ? risk.required_controls.map((item) => `- ${item}`).join("\n")
    : "- Standard ownership and documentation controls";

  const evidence = risk.evidence_required.length
    ? risk.evidence_required.map((item) => `- ${item}`).join("\n")
    : "- Standard governance evidence retained";

  return [
    `Board Decision Memo — ${system.system_name}`,
    "",
    "Client-safe boundary:",
    "This is a production-shaped simulated AI governance board. It does not connect to real patient data, customer records, regulated production systems, production model runtime, enterprise authorization systems, or clinical decision systems.",
    "",
    "Executive summary:",
    `${system.system_name} was reviewed as a simulated AI governance board submission. The system received a risk score of ${risk.risk_score}/100, a risk classification of ${risk.risk_classification}, and an EU AI Act-style classification of ${risk.ai_act_classification}. The current governance outcome is ${system.final_outcome}.`,
    "",
    "Governance decision:",
    `Decision: ${system.final_outcome}`,
    `Approval status: ${system.approval_status}`,
    `Rationale: ${risk.reason}`,
    "",
    "Required controls:",
    controls,
    "",
    "Evidence required:",
    evidence,
    "",
    "NIST AI RMF mapping:",
    `Govern: ${risk.nist_mapping.govern.join("; ")}`,
    `Map: ${risk.nist_mapping.map.join("; ")}`,
    `Measure: ${risk.nist_mapping.measure.join("; ")}`,
    `Manage: ${risk.nist_mapping.manage.join("; ")}`,
    "",
    "Correct claim:",
    "This demo shows AI system intake, risk classification, regulatory mapping, committee review, evidence reconstruction, and board-ready decision memo generation in a simulated environment."
  ].join("\n");
}

function buildBoardEvidencePacket(system: AISystem | null) {
  if (!system) {
    return {};
  }

  const completeness = buildEvidenceCompleteness(system);

  return {
    packet_type: "board_ai_governance_evidence_export",
    generated_from: "SecureTheCloud AI Governance Board",
    public_demo_boundary: {
      lab_mode: true,
      safe_claim: "Production-shaped simulated AI governance board, not production enforcement.",
      not_connected_to: [
        "real patient data",
        "customer records",
        "regulated production systems",
        "production model runtime",
        "enterprise authorization systems",
        "clinical decision systems"
      ]
    },
    system: {
      system_id: system.system_id,
      system_name: system.system_name,
      business_owner: system.business_owner,
      model_owner: system.model_owner,
      department: system.department,
      domain: system.domain,
      use_case: system.use_case,
      model_name: system.model_name,
      model_provider: system.model_provider,
      deployment_environment: system.deployment_environment,
      target_users: system.target_users,
      data_types: system.data_types
    },
    risk_and_classification: {
      risk_score: system.risk_assessment.risk_score,
      risk_classification: system.risk_assessment.risk_classification,
      ai_act_classification: system.risk_assessment.ai_act_classification,
      risk_factors: system.risk_assessment.risk_factors,
      phi_involved: system.phi_involved,
      customer_data_involved: system.customer_data_involved,
      clinical_or_patient_impact: system.clinical_or_patient_impact,
      financial_or_credit_impact: system.financial_or_credit_impact,
      security_enforcement_impact: system.security_enforcement_impact,
      safety_critical: system.safety_critical
    },
    governance_decision: {
      decision: system.final_outcome,
      approval_status: system.approval_status,
      rationale: system.risk_assessment.reason
    },
    required_controls_summary: {
      required_controls: system.risk_assessment.required_controls,
      evidence_required: system.risk_assessment.evidence_required
    },
    nist_ai_rmf_mapping: system.risk_assessment.nist_mapping,
    evidence_timeline: buildBoardEvidenceTimeline(system),
    evidence_completeness: completeness,
    audit_readiness: {
      coverage_percent: completeness.coverage,
      evidence_ready: completeness.coverage === 100,
      reconstruction_summary: "Evidence packet reconstructs intake, risk scoring, regulatory mapping, HIPAA-style review, committee status, and final governance outcome."
    }
  };
}

function downloadTextFile(filename: string, content: string, mimeType: string) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
}

'''

if helper_marker not in s:
    raise SystemExit("Could not find const defaultForm marker.")

s = s.replace(helper_marker, helper + "\n" + helper_marker, 1)

section = r'''
      {selectedSystem && (
        <section
          style={{
            ...styles.phase8ExportGrid,
            gridTemplateColumns: isMobile ? "1fr" : "1fr 1fr"
          }}
        >
          <div style={styles.panel}>
            <p style={styles.kicker}>Phase 8 · Board Evidence Export</p>
            <h2>Evidence Package Export</h2>
            <p style={styles.lead}>
              Generates an audit-ready JSON packet for the selected AI system, including intake metadata,
              risk classification, NIST AI RMF mapping, required controls, evidence timeline, and final outcome.
            </p>

            <div style={styles.phase8ExportCard}>
              <div>
                <span style={styles.metaLabel}>Selected System</span>
                <strong>{selectedSystem.system_name}</strong>
              </div>
              <div>
                <span style={styles.metaLabel}>Risk / Outcome</span>
                <strong>
                  {selectedSystem.risk_assessment.risk_classification.replaceAll("_", " ")} ·{" "}
                  {selectedSystem.final_outcome.replaceAll("_", " ")}
                </strong>
              </div>
              <div>
                <span style={styles.metaLabel}>Evidence Coverage</span>
                <strong>{buildEvidenceCompleteness(selectedSystem).coverage}%</strong>
              </div>
            </div>

            <div style={styles.phase8ButtonGrid}>
              <button
                type="button"
                style={styles.primaryButton}
                onClick={() => {
                  const packet = JSON.stringify(buildBoardEvidencePacket(selectedSystem), null, 2);
                  downloadTextFile(`${selectedSystem.system_id}-board-evidence-packet.json`, packet, "application/json");
                }}
              >
                Download Evidence JSON
              </button>

              <button
                type="button"
                style={styles.secondaryButton}
                onClick={async () => {
                  const packet = JSON.stringify(buildBoardEvidencePacket(selectedSystem), null, 2);
                  await navigator.clipboard.writeText(packet);
                  setSubmitStatus("Board evidence JSON copied.");
                }}
              >
                Copy Evidence JSON
              </button>
            </div>

            <div style={styles.phase8JsonPreview}>
              <pre>{JSON.stringify(buildBoardEvidencePacket(selectedSystem), null, 2).slice(0, 1800)}...</pre>
            </div>
          </div>

          <div style={styles.panel}>
            <p style={styles.kicker}>Executive Decision Memo</p>
            <h2>Board Memo</h2>
            <p style={styles.lead}>
              Copyable board/risk committee memo explaining the governance decision, rationale, controls,
              and client-safe public demo boundary.
            </p>

            <div style={styles.phase8MemoCard}>
              <pre>{buildBoardDecisionMemo(selectedSystem)}</pre>
            </div>

            <div style={styles.phase8ButtonGrid}>
              <button
                type="button"
                style={styles.primaryButton}
                onClick={() => {
                  downloadTextFile(
                    `${selectedSystem.system_id}-board-decision-memo.txt`,
                    buildBoardDecisionMemo(selectedSystem),
                    "text/plain"
                  );
                }}
              >
                Download Board Memo
              </button>

              <button
                type="button"
                style={styles.secondaryButton}
                onClick={async () => {
                  await navigator.clipboard.writeText(buildBoardDecisionMemo(selectedSystem));
                  setSubmitStatus("Board decision memo copied.");
                }}
              >
                Copy Board Memo
              </button>
            </div>

            <div style={styles.phase8BoundaryBox}>
              <h3>Public Demo Boundary</h3>
              <p>
                Simulated AI governance workflow only. No real patient data, customer data, regulated systems,
                production model runtime, clinical decision systems, or enterprise authorization systems are connected.
              </p>
            </div>
          </div>
        </section>
      )}

'''

footer_marker = "      <footer"
if footer_marker not in s:
    raise SystemExit("Could not find footer insertion marker.")

s = s.replace(footer_marker, section + "\n" + footer_marker, 1)

style_marker = "  footer:"
styles = r'''
  phase8ExportGrid: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: 18,
    marginTop: 18
  },
  phase8ExportCard: {
    display: "grid",
    gap: 12,
    border: "1px solid #00d9ff",
    borderRadius: 16,
    padding: 16,
    background: "rgba(8, 47, 73, .26)",
    marginTop: 14
  },
  phase8ButtonGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(2, minmax(0, 1fr))",
    gap: 10,
    marginTop: 14
  },
  phase8JsonPreview: {
    border: "1px solid #334155",
    borderRadius: 16,
    padding: 14,
    background: "rgba(2, 6, 23, .72)",
    marginTop: 14,
    maxHeight: 320,
    overflow: "auto",
    whiteSpace: "pre-wrap",
    overflowWrap: "anywhere"
  },
  phase8MemoCard: {
    border: "1px solid #22c55e",
    borderRadius: 16,
    padding: 14,
    background: "rgba(20, 83, 45, .14)",
    marginTop: 14,
    maxHeight: 520,
    overflow: "auto",
    whiteSpace: "pre-wrap",
    overflowWrap: "anywhere"
  },
  phase8BoundaryBox: {
    border: "1px solid #00d9ff",
    borderRadius: 16,
    padding: 16,
    background: "rgba(8, 47, 73, .22)",
    marginTop: 14
  },

'''

if style_marker not in s:
    raise SystemExit("Could not find style insertion marker.")

s = s.replace(style_marker, styles + style_marker, 1)

p.write_text(s)
print("Added Phase 8 frontend Board Evidence Export panel.")
