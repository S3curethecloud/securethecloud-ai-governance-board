from pathlib import Path

p = Path("frontend/app/page.tsx")
s = p.read_text()

needle = "\n  approveButton: {"
positions = []
start = 0

while True:
    idx = s.find(needle, start)
    if idx == -1:
        break
    positions.append(idx)
    start = idx + len(needle)

print(f"Found {len(positions)} approveButton style block(s).")

if len(positions) <= 1:
    print("No duplicate approveButton style block found.")
    raise SystemExit(0)

def find_property_end(text: str, start_idx: int) -> int:
    brace_start = text.find("{", start_idx)
    if brace_start == -1:
        raise SystemExit("Could not find opening brace for approveButton style block")

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

                # Include trailing comma if present.
                while end < len(text) and text[end] in " \t\r\n":
                    end += 1
                if end < len(text) and text[end] == ",":
                    end += 1

                # Include trailing whitespace/newline after the property.
                while end < len(text) and text[end] in " \t\r\n":
                    end += 1

                return end

        i += 1

    raise SystemExit("Could not find closing brace for approveButton style block")

# Keep the first approveButton style block. Remove later duplicates from the end backward.
for dup_start in reversed(positions[1:]):
    dup_end = find_property_end(s, dup_start)
    s = s[:dup_start] + "\n" + s[dup_end:]

p.write_text(s)
print(f"Removed {len(positions) - 1} duplicate approveButton style block(s).")
