from pathlib import Path
import re

p = Path("frontend/app/page.tsx")
s = p.read_text()

# 1. Make all record cards text visible, including button-rendered records.
s = re.sub(
    r'record:\s*\{\s*border:\s*"1px solid #334155",\s*borderRadius:\s*16,\s*padding:\s*16,\s*background:\s*"#020617",\s*cursor:\s*"pointer",\s*overflowWrap:\s*"anywhere"\s*\},',
    'record: { border: "1px solid #334155", borderRadius: 16, padding: 16, background: "#020617", cursor: "pointer", overflowWrap: "anywhere", color: "#eaf2ff", font: "inherit" },',
    s
)

# Fallback if the exact minified style differs.
if 'record: { border: "1px solid #334155", borderRadius: 16, padding: 16, background: "#020617", cursor: "pointer", overflowWrap: "anywhere", color: "#eaf2ff", font: "inherit" },' not in s:
    s = s.replace(
        'record: { border: "1px solid #334155", borderRadius: 16, padding: 16, background: "#020617", cursor: "pointer", overflowWrap: "anywhere" },',
        'record: { border: "1px solid #334155", borderRadius: 16, padding: 16, background: "#020617", cursor: "pointer", overflowWrap: "anywhere", color: "#eaf2ff", font: "inherit" },'
    )

# 2. Strengthen badge wrapping and sizing.
s = s.replace(
'''  badge: {
    border: "1px solid #38bdf8",
    maxWidth: "100%",
    overflowWrap: "anywhere",''',
'''  badge: {
    border: "1px solid #38bdf8",
    maxWidth: "100%",
    minWidth: 88,
    textAlign: "center",
    overflowWrap: "normal",
    wordBreak: "normal",'''
)

# 3. Keep record headers from squeezing badges too tightly.
s = s.replace(
'''  recordHead: { display: "flex", justifyContent: "space-between", gap: 12, alignItems: "flex-start" },''',
'''  recordHead: { display: "flex", justifyContent: "space-between", gap: 12, alignItems: "flex-start", flexWrap: "wrap" },'''
)

# 4. Make detail boxes readable: label above value.
s = re.sub(
    r'detailBox:\s*\{\s*border:\s*"1px solid #334155",\s*borderRadius:\s*12,\s*padding:\s*12\s*\},',
    'detailBox: { border: "1px solid #334155", borderRadius: 12, padding: 12, display: "grid", gap: 6, color: "#eaf2ff" },',
    s
)

if 'detailBox: { border: "1px solid #334155", borderRadius: 12, padding: 12, display: "grid", gap: 6, color: "#eaf2ff" },' not in s:
    s = s.replace(
        'detailBox: { border: "1px solid #334155", borderRadius: 12, padding: 12 },',
        'detailBox: { border: "1px solid #334155", borderRadius: 12, padding: 12, display: "grid", gap: 6, color: "#eaf2ff" },'
    )

# 5. Make small label text inside detail boxes muted and separated.
if 'detailBox span' not in s:
    s = s.replace(
'''        button {
          max-width: 100%;
        }''',
'''        button {
          max-width: 100%;
        }

        div[style] > span {
          line-height: 1.2;
        }'''
    )

# 6. Mobile and narrow desktop safety for Phase 4 buttons.
s = s.replace(
'''  reviewActionGrid: { display: "grid", gridTemplateColumns: "repeat(4, minmax(0, 1fr))", gap: 10, marginTop: 14 },''',
'''  reviewActionGrid: { display: "grid", gridTemplateColumns: "repeat(2, minmax(0, 1fr))", gap: 10, marginTop: 14 },'''
)

p.write_text(s)
