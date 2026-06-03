from pathlib import Path

p = Path("frontend/app/page.tsx")
s = p.read_text()

# Add preWrap style to pre blocks in Phase 8.
s = s.replace(
    '<pre>{JSON.stringify(buildBoardEvidencePacket(selectedSystem), null, 2).slice(0, 1800)}...</pre>',
    '<pre style={styles.preWrap}>{JSON.stringify(buildBoardEvidencePacket(selectedSystem), null, 2).slice(0, 1800)}...</pre>'
)

s = s.replace(
    '<pre>{buildBoardDecisionMemo(selectedSystem)}</pre>',
    '<pre style={styles.preWrap}>{buildBoardDecisionMemo(selectedSystem)}</pre>'
)

# Make Phase 8 metadata rows visually separate label and value.
s = s.replace(
'''              <div>
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
              </div>''',
'''              <div style={styles.phase8MetaRow}>
                <span style={styles.metaLabel}>Selected System</span>
                <strong>{selectedSystem.system_name}</strong>
              </div>
              <div style={styles.phase8MetaRow}>
                <span style={styles.metaLabel}>Risk / Outcome</span>
                <strong>
                  {selectedSystem.risk_assessment.risk_classification.replaceAll("_", " ")} ·{" "}
                  {selectedSystem.final_outcome.replaceAll("_", " ")}
                </strong>
              </div>
              <div style={styles.phase8MetaRow}>
                <span style={styles.metaLabel}>Evidence Coverage</span>
                <strong>{buildEvidenceCompleteness(selectedSystem).coverage}%</strong>
              </div>'''
)

# Insert missing styles before footer style.
style_marker = "  footer:"
insert = '''  phase8MetaRow: {
    display: "grid",
    gap: 4,
    alignItems: "start",
    minWidth: 0
  },
  preWrap: {
    margin: 0,
    whiteSpace: "pre-wrap",
    overflowWrap: "anywhere",
    wordBreak: "break-word",
    fontSize: 12,
    lineHeight: 1.45
  },

'''

if "phase8MetaRow:" not in s:
    if style_marker not in s:
        raise SystemExit("footer style marker not found")
    s = s.replace(style_marker, insert + style_marker, 1)

p.write_text(s)
print("Applied Phase 8A board export UX polish.")
