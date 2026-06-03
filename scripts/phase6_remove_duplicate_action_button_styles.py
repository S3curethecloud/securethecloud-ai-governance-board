from pathlib import Path

p = Path("frontend/app/page.tsx")
s = p.read_text()

keys = [
    "approveButton",
    "rejectButton",
    "escalateButton",
    "controlButton",
    "secondaryButton",
    "primaryButton",
]

def find_positions(text: str, key: str):
    positions = []
    needle = f"\n  {key}: {{"
    start = 0
    while True:
        idx = text.find(needle, start)
        if idx == -1:
            break
        positions.append(idx)
        start = idx + len(needle)
    return positions

def find_property_end(text: str, start_idx: int) -> int:
    brace_start = text.find("{", start_idx)
    if brace_start == -1:
        raise SystemExit(f"Could not find opening brace at {start_idx}")

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
                while end < len(text) and text[end] in " \t\r\n":
                    end += 1
                if end < len(text) and text[end] == ",":
                    end += 1
                while end < len(text) and text[end] in " \t\r\n":
                    end += 1
                return end
        i += 1

    raise SystemExit(f"Could not find closing brace at {start_idx}")

total_removed = 0

for key in keys:
    positions = find_positions(s, key)
    print(f"{key}: found {len(positions)} block(s)")

    if len(positions) <= 1:
        continue

    # Keep the first definition. Remove later duplicates.
    for dup_start in reversed(positions[1:]):
        dup_end = find_property_end(s, dup_start)
        s = s[:dup_start] + "\n" + s[dup_end:]
        total_removed += 1

p.write_text(s)
print(f"Removed {total_removed} duplicate action button style block(s).")
