#!/usr/bin/env python3

"""
Usage:

    python3 clean_md.py input.md > output.md

Or:

    cat input.md | python clean_md.py

What it does:

- Removes id="..." from fenced code blocks
- Removes "text" and "markdown" language tags entirely
- Preserves all other language tags
- Supports fences of any length:
      ```
      ````
      `````
"""

import re
import sys


FENCE_RE = re.compile(
    r'^(`{3,})([a-zA-Z0-9_-]+)?(?:\s+id="[^"]*")?\s*$'
)


def clean_fences(content: str) -> str:
    lines = []

    for line in content.splitlines():
        m = FENCE_RE.match(line)

        if not m:
            lines.append(line)
            continue

        fence = m.group(1)
        lang = m.group(2)

        # Remove text/markdown tags entirely
        if lang in ("text", "markdown"):
            lines.append(fence)

        # Preserve other language tags
        elif lang:
            lines.append(f"{fence}{lang}")

        # Plain fence
        else:
            lines.append(fence)

    return "\n".join(lines)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = f.read()

            cleaned = clean_fences(data)

            # overwrite original file
            with open(path, "w", encoding="utf-8") as f:
                f.write(cleaned)

            print(f"Success: cleaned '{path}'")

        except FileNotFoundError:
            print(f"Error: input file not found: '{path}'")

        except PermissionError:
            print(f"Error: permission denied: '{path}'")

        except Exception as e:
            print(f"Error: {e}")

    else:
        data = sys.stdin.read()
        print(clean_fences(data))