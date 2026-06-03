from pathlib import Path

p = Path("frontend/app/page.tsx")
s = p.read_text()

if "setSubmitStatus(" not in s:
    raise SystemExit("setSubmitStatus is not present; nothing to patch")

# If a submitStatus state already exists, do nothing.
if "setSubmitStatus] = useState" in s or "setSubmitStatus ] = useState" in s:
    print("submitStatus state already exists")
    p.write_text(s)
    raise SystemExit(0)

# Add state inside the default component, near the first useState.
markers = [
    'export default function Home() {\n',
    'export default function Page() {\n',
]

inserted = False
for marker in markers:
    if marker in s:
        s = s.replace(
            marker,
            marker + '  const [submitStatus, setSubmitStatus] = useState("Ready for AI system intake.");\n',
            1,
        )
        inserted = True
        break

if not inserted:
    raise SystemExit("Could not find default component marker")

p.write_text(s)
print("Added submitStatus state for Phase 6 HIPAA review actions")
