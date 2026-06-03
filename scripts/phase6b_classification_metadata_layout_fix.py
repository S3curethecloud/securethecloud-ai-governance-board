from pathlib import Path
import re

p = Path("frontend/app/page.tsx")
s = p.read_text()

# Replace compact metadata row if it exists.
patterns = [
    re.compile(
        r'''<div style=\{styles\.reviewMetaGrid\}>\s*
\s*<div>\s*<span>HIPAA-Style Review</span>\s*<strong>\{selectedSystem\.risk_assessment\.hipaa_review_required \? "required" : "not required"\}</strong>\s*</div>\s*
\s*<div>\s*<span>PHI Involved</span>\s*<strong>\{selectedSystem\.phi_involved \? "yes" : "no"\}</strong>\s*</div>\s*
\s*<div>\s*<span>Customer Data</span>\s*<strong>\{selectedSystem\.customer_data_involved \? "yes" : "no"\}</strong>\s*</div>\s*
\s*<div>\s*<span>Monitoring</span>\s*<strong>\{selectedSystem\.risk_assessment\.required_controls\.some\(.*?\) \? "required" : "standard"\}</strong>\s*</div>\s*
\s*</div>''',
        re.S,
    ),
    re.compile(
        r'''<div style=\{styles\.reviewMetaGrid\}>\s*
\s*<div>\s*<b>HIPAA-Style Review</b>\s*\{selectedSystem\.risk_assessment\.hipaa_review_required \? "required" : "not required"\}\s*</div>\s*
\s*<div>\s*<b>PHI Involved</b>\s*\{selectedSystem\.phi_involved \? "yes" : "no"\}\s*</div>\s*
\s*<div>\s*<b>Customer Data</b>\s*\{selectedSystem\.customer_data_involved \? "yes" : "no"\}\s*</div>\s*
\s*<div>\s*<b>Monitoring</b>\s*\{selectedSystem\.risk_assessment\.required_controls\.some\(.*?\) \? "required" : "standard"\}\s*</div>\s*
\s*</div>''',
        re.S,
    ),
]

replacement = '''<div style={styles.reviewMetaGrid}>
              <div style={styles.reviewMetaCard}>
                <span style={styles.metaLabel}>HIPAA-Style Review</span>
                <strong>{selectedSystem.risk_assessment.hipaa_review_required ? "required" : "not required"}</strong>
              </div>
              <div style={styles.reviewMetaCard}>
                <span style={styles.metaLabel}>PHI Involved</span>
                <strong>{selectedSystem.phi_involved ? "yes" : "no"}</strong>
              </div>
              <div style={styles.reviewMetaCard}>
                <span style={styles.metaLabel}>Customer Data</span>
                <strong>{selectedSystem.customer_data_involved ? "yes" : "no"}</strong>
              </div>
              <div style={styles.reviewMetaCard}>
                <span style={styles.metaLabel}>Monitoring</span>
                <strong>{selectedSystem.risk_assessment.required_controls.some((control) => control.toLowerCase().includes("monitoring")) ? "required" : "standard"}</strong>
              </div>
            </div>'''

changed = False
for pattern in patterns:
    s2, count = pattern.subn(replacement, s, count=1)
    if count:
        s = s2
        changed = True
        break

if not changed:
    print("Known compact metadata block not found. Adding styles only; inspect grep output manually.")
else:
    print("Replaced compact metadata block.")

# Add or normalize styles.
if "reviewMetaGrid:" not in s:
    marker = "  chipWrap:"
    insert = '''  reviewMetaGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(4, minmax(0, 1fr))",
    gap: 10,
    marginTop: 14
  },
  reviewMetaCard: {
    border: "1px solid #334155",
    borderRadius: 12,
    padding: 12,
    background: "rgba(2, 6, 23, .55)",
    display: "grid",
    gap: 4,
    minWidth: 0
  },
  metaLabel: {
    color: "#dbeafe",
    fontSize: 13,
    lineHeight: 1.2
  },
'''
    if marker not in s:
        raise SystemExit("style insertion marker not found")
    s = s.replace(marker, insert + marker)
else:
    # Ensure these companion styles exist.
    if "reviewMetaCard:" not in s:
        marker = "  reviewMetaGrid:"
        idx = s.find(marker)
        block_end = s.find("\n  ", idx + len(marker))
        add = '''  reviewMetaCard: {
    border: "1px solid #334155",
    borderRadius: 12,
    padding: 12,
    background: "rgba(2, 6, 23, .55)",
    display: "grid",
    gap: 4,
    minWidth: 0
  },
  metaLabel: {
    color: "#dbeafe",
    fontSize: 13,
    lineHeight: 1.2
  },
'''
        s = s[:block_end] + "\n" + add + s[block_end:]

# Add mobile override if there is already a mobile styles section pattern.
if "reviewMetaGrid: { ...styles.reviewMetaGrid, gridTemplateColumns: \"1fr\" }" not in s:
    s = s.replace(
        "reviewActionGrid: { ...styles.reviewActionGrid, gridTemplateColumns: \"1fr\" },",
        "reviewActionGrid: { ...styles.reviewActionGrid, gridTemplateColumns: \"1fr\" },\n    reviewMetaGrid: { ...styles.reviewMetaGrid, gridTemplateColumns: \"1fr\" },",
    )

p.write_text(s)
