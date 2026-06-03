from pathlib import Path
import re

api_url = "https://securethecloud-ai-governance-board-api.fly.dev"

page = Path("frontend/app/page.tsx")
s = page.read_text()

# Replace hardcoded localhost API base if present.
s = re.sub(
    r'const\s+API_BASE\s*=\s*["\']http://localhost:8010["\'];',
    'const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8010";',
    s,
)

page.write_text(s)

dockerfile = Path("frontend/Dockerfile")
d = dockerfile.read_text()

if "ARG NEXT_PUBLIC_API_BASE" not in d:
    d = d.replace(
        "COPY . .\n\nRUN npm run build",
        "COPY . .\n\nARG NEXT_PUBLIC_API_BASE\nENV NEXT_PUBLIC_API_BASE=${NEXT_PUBLIC_API_BASE}\n\nRUN npm run build",
    )

dockerfile.write_text(d)

flytoml = Path("frontend/fly.toml")
flytoml.write_text(f'''app = "securethecloud-ai-governance-board"
primary_region = "iad"

[build]
  [build.args]
    NEXT_PUBLIC_API_BASE = "{api_url}"

[http_service]
  internal_port = 3000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  processes = ["app"]

[[vm]]
  memory = "256mb"
  cpu_kind = "shared"
  cpus = 1
''')

print("Phase 10A frontend API base hotfix applied.")
