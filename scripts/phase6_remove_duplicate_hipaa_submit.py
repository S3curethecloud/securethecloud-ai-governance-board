from pathlib import Path

p = Path("frontend/app/page.tsx")
s = p.read_text()

needle = "  async function submitHipaaReview("
positions = []
start = 0

while True:
    idx = s.find(needle, start)
    if idx == -1:
        break
    positions.append(idx)
    start = idx + len(needle)

if len(positions) <= 1:
    print(f"Found {len(positions)} submitHipaaReview function(s); no duplicate removal needed.")
    raise SystemExit(0)

def find_function_end(text: str, start_idx: int) -> int:
    brace_start = text.find("{", start_idx)
    if brace_start == -1:
        raise SystemExit("Could not find opening brace for duplicate function")

    depth = 0
    i = brace_start

    while i < len(text):
        ch = text[i]

        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i + 1

                # Remove trailing whitespace/newlines after the function.
                while end < len(text) and text[end] in " \t\r\n":
                    end += 1

                return end

        i += 1

    raise SystemExit("Could not find closing brace for duplicate function")

# Keep the first function. Remove later duplicate functions from the end backward.
for dup_start in reversed(positions[1:]):
    dup_end = find_function_end(s, dup_start)
    s = s[:dup_start] + s[dup_end:]

p.write_text(s)
print(f"Removed {len(positions) - 1} duplicate submitHipaaReview function(s).")
