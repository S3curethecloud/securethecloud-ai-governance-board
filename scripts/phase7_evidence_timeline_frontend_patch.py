from pathlib import Path

p = Path("frontend/app/page.tsx")
s = p.read_text()

if "Phase 7 · Evidence Package Timeline" in s:
    print("Phase 7 frontend audit trail already present.")
    raise SystemExit(0)

helper_marker = "const defaultForm"
helper = r'''
type BoardTimelineEvent = {
  step: string;
  title: string;
  status: string;
  detail: string;
  evidence: string[];
};

function formatBool(value: boolean): string {
  return value ? "yes" : "no";
}

function buildBoardEvidenceTimeline(system: AISystem | null): BoardTimelineEvent[] {
  if (!system) {
    return [];
  }

  const risk = system.risk_assessment;
  const nist = risk.nist_mapping;

  return [
    {
      step: "01",
      title: "AI System Intake",
      status: "captured",
      detail: `${system.system_name} submitted for governance review before AI adoption.`,
      evidence: [
        `System ID: ${system.system_id}`,
        `Business owner: ${system.business_owner}`,
        `Model owner: ${system.model_owner}`,
        `Department: ${system.department}`
      ]
    },
    {
      step: "02",
      title: "Risk Assessment",
      status: risk.risk_classification,
      detail: `Risk score calculated as ${risk.risk_score}/100.`,
      evidence: risk.risk_factors.length ? risk.risk_factors : ["No major risk factors identified"]
    },
    {
      step: "03",
      title: "NIST AI RMF Mapping",
      status: "mapped",
      detail: "Govern, Map, Measure, and Manage review evidence generated.",
      evidence: [
        `Govern evidence: ${nist.govern.length}`,
        `Map evidence: ${nist.map.length}`,
        `Measure evidence: ${nist.measure.length}`,
        `Manage evidence: ${nist.manage.length}`
      ]
    },
    {
      step: "04",
      title: "EU AI Act-Style Classification",
      status: risk.ai_act_classification,
      detail: `System classified as ${risk.ai_act_classification} for simulated regulatory review.`,
      evidence: [
        `Risk class: ${risk.risk_classification}`,
        `Decision: ${risk.decision}`,
        `Required controls: ${risk.required_controls.length}`
      ]
    },
    {
      step: "05",
      title: "HIPAA-Style Review",
      status: risk.hipaa_review_required ? "required" : "not required",
      detail: "PHI, clinical impact, and patient-impact review evaluated.",
      evidence: [
        `PHI involved: ${formatBool(system.phi_involved)}`,
        `Clinical / patient impact: ${formatBool(system.clinical_or_patient_impact)}`,
        `HIPAA-style review required: ${formatBool(risk.hipaa_review_required)}`
      ]
    },
    {
      step: "06",
      title: "Committee Decision",
      status: system.approval_status,
      detail: `Governance committee status is ${system.approval_status}.`,
      evidence: [
        `Approval status: ${system.approval_status}`,
        `Final outcome: ${system.final_outcome}`
      ]
    },
    {
      step: "07",
      title: "Final Governance Outcome",
      status: system.final_outcome,
      detail: `Final governed AI system outcome: ${system.final_outcome}.`,
      evidence: risk.evidence_required.length ? risk.evidence_required : ["Standard documentation evidence retained"]
    }
  ];
}

function buildEvidenceCompleteness(system: AISystem | null) {
  if (!system) {
    return { complete: 0, total: 0, coverage: 0, items: [] as { name: string; complete: boolean }[] };
  }

  const risk = system.risk_assessment;
  const nist = risk.nist_mapping;

  const items = [
    { name: "System intake record", complete: Boolean(system.system_id) },
    { name: "Business owner identified", complete: Boolean(system.business_owner) },
    { name: "Model owner identified", complete: Boolean(system.model_owner) },
    { name: "Risk score calculated", complete: risk.risk_score >= 0 },
    { name: "Risk classification assigned", complete: Boolean(risk.risk_classification) },
    { name: "NIST Govern mapped", complete: nist.govern.length > 0 },
    { name: "NIST Map mapped", complete: nist.map.length > 0 },
    { name: "NIST Measure mapped", complete: nist.measure.length > 0 },
    { name: "NIST Manage mapped", complete: nist.manage.length > 0 },
    { name: "EU AI Act-style class assigned", complete: Boolean(risk.ai_act_classification) },
    { name: "HIPAA-style review evaluated", complete: typeof risk.hipaa_review_required === "boolean" },
    { name: "Evidence requirements listed", complete: risk.evidence_required.length > 0 },
    { name: "Final outcome recorded", complete: Boolean(system.final_outcome) }
  ];

  const complete = items.filter((item) => item.complete).length;

  return {
    complete,
    total: items.length,
    coverage: Math.round((complete / items.length) * 100),
    items
  };
}

'''

if helper_marker not in s:
    raise SystemExit("Could not find const defaultForm marker.")

s = s.replace(helper_marker, helper + "\n" + helper_marker, 1)

section = r'''
      {selectedSystem && (
        <section
          style={{
            ...styles.phase7AuditGrid,
            gridTemplateColumns: isMobile ? "1fr" : "1.2fr .8fr"
          }}
        >
          <div style={styles.panel}>
            <p style={styles.kicker}>Phase 7 · Evidence Package Timeline</p>
            <h2>Board Audit Trail</h2>
            <p style={styles.lead}>
              Auditor-ready reconstruction of intake, risk scoring, regulatory mapping, HIPAA-style review,
              committee decision, and final governance outcome for the selected AI system.
            </p>

            <div style={styles.phase7TimelineCard}>
              {buildBoardEvidenceTimeline(selectedSystem).map((event) => (
                <div key={`${event.step}-${event.title}`} style={styles.phase7TimelineItem}>
                  <div style={styles.phase7Step}>{event.step}</div>
                  <div style={styles.phase7TimelineBody}>
                    <div style={styles.phase7TimelineHeader}>
                      <strong>{event.title}</strong>
                      <span style={styles.phase7Status}>{event.status.replaceAll("_", " ")}</span>
                    </div>
                    <p>{event.detail}</p>
                    <div style={styles.chipWrap}>
                      {event.evidence.map((item) => (
                        <span key={item} style={styles.chip}>{item}</span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div style={styles.panel}>
            <p style={styles.kicker}>Board / Auditor View</p>
            <h2>Evidence Completeness</h2>
            <p style={styles.lead}>
              Shows whether the selected system has enough governance evidence for board-level reconstruction.
            </p>

            <div style={styles.phase7CompletenessCard}>
              <div>
                <span style={styles.metaLabel}>Evidence Coverage</span>
                <strong style={styles.phase7Coverage}>
                  {buildEvidenceCompleteness(selectedSystem).coverage}%
                </strong>
              </div>
              <p>
                {buildEvidenceCompleteness(selectedSystem).complete} of {buildEvidenceCompleteness(selectedSystem).total} evidence checks complete.
              </p>
            </div>

            <div style={styles.phase7Checklist}>
              {buildEvidenceCompleteness(selectedSystem).items.map((item) => (
                <div key={item.name} style={styles.phase7ChecklistItem}>
                  <span>{item.complete ? "✓" : "!"}</span>
                  <strong>{item.name}</strong>
                  <em>{item.complete ? "complete" : "missing"}</em>
                </div>
              ))}
            </div>

            <div style={styles.phase7Reconstruction}>
              <h3>Board Reconstruction Summary</h3>
              <p>
                {selectedSystem.system_name} has a final governance outcome of{" "}
                <strong>{selectedSystem.final_outcome.replaceAll("_", " ")}</strong>, a risk score of{" "}
                <strong>{selectedSystem.risk_assessment.risk_score}/100</strong>, and an EU AI Act-style classification of{" "}
                <strong>{selectedSystem.risk_assessment.ai_act_classification}</strong>.
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
  phase7AuditGrid: {
    display: "grid",
    gridTemplateColumns: "1.2fr .8fr",
    gap: 18,
    marginTop: 18
  },
  phase7TimelineCard: {
    border: "1px solid #00d9ff",
    borderRadius: 16,
    padding: 16,
    background: "rgba(8, 47, 73, .32)",
    marginTop: 14
  },
  phase7TimelineItem: {
    display: "grid",
    gridTemplateColumns: "48px 1fr",
    gap: 14,
    padding: "16px 0",
    borderTop: "1px solid rgba(148, 163, 184, .18)"
  },
  phase7Step: {
    width: 34,
    height: 34,
    borderRadius: 999,
    border: "1px solid #00d9ff",
    color: "#67e8f9",
    display: "grid",
    placeItems: "center",
    fontWeight: 900
  },
  phase7TimelineBody: {
    minWidth: 0
  },
  phase7TimelineHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: 12,
    flexWrap: "wrap"
  },
  phase7Status: {
    border: "1px solid #22c55e",
    color: "#86efac",
    background: "rgba(20, 83, 45, .25)",
    borderRadius: 999,
    padding: "6px 10px",
    fontSize: 12,
    fontWeight: 900,
    textTransform: "uppercase"
  },
  phase7CompletenessCard: {
    border: "1px solid #22c55e",
    borderRadius: 16,
    padding: 16,
    background: "rgba(20, 83, 45, .16)",
    marginTop: 14
  },
  phase7Coverage: {
    display: "block",
    color: "#fde047",
    fontSize: 46,
    lineHeight: 1,
    marginTop: 8
  },
  phase7Checklist: {
    display: "grid",
    gap: 10,
    marginTop: 14
  },
  phase7ChecklistItem: {
    display: "grid",
    gridTemplateColumns: "28px 1fr auto",
    gap: 10,
    alignItems: "center",
    border: "1px solid #334155",
    borderRadius: 12,
    padding: "10px 12px",
    background: "rgba(2, 6, 23, .62)"
  },
  phase7Reconstruction: {
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
print("Added Phase 7 frontend board audit trail.")
