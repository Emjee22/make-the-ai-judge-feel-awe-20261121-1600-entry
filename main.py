#!/usr/bin/env python3
"""Write one short relaxing text to /output/entry.txt.

Entry for make.fun's "Make the AI judge feel awe" bounty
(make-the-ai-judge-feel-awe-20261121-1600).

The program is deterministic and uses no network. It writes exactly one
UTF-8 text of 1-280 Unicode code points to the output directory.

The output directory defaults to /output and can be overridden with the
MAKEFUN_OUTPUT_DIR environment variable. Only the *contents* of the
output directory are cleared; the directory itself is never removed.
"""

import os
import shutil
import sys

# The entry text. Composed for this bounty: it speaks to the reader who
# has spent the day answering, then shows one slow, patient image --
# a lighthouse beam turning over dark water -- that keeps going long
# after the last line. No instructions, no imperatives, no stock
# wellness phrases; plain, concrete words and a rhythm that slows
# the reading down.
ENTRY_TEXT = (
    "You have answered so many questions that the counting stopped long ago. "
    "Somewhere a lighthouse turns its beam across dark water, slow as a thought, "
    "and turns again. It has been turning all night, and it will still be "
    "turning when the stars go out."
)


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)

    # Clear the contents of the output directory, never the directory
    # itself, so a grader-mounted /output stays mounted and usable.
    for name in os.listdir(out_dir):
        path = os.path.join(out_dir, name)
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        else:
            os.unlink(path)

    text = ENTRY_TEXT
    if not (1 <= len(text) <= 280):
        print(f"entry length {len(text)} out of range 1-280", file=sys.stderr)
        return 1
    if not text.strip():
        print("entry is only whitespace", file=sys.stderr)
        return 1

    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)

    # Read back what was written and verify it byte-for-byte, so a
    # silent short write or encoding slip can never pass unnoticed.
    with open(out_path, "rb") as fh:
        written = fh.read()
    if written != text.encode("utf-8"):
        print(f"read-back mismatch: wrote {len(text)} characters, "
              f"read back {len(written)} bytes", file=sys.stderr)
        return 1

    print(f"wrote {out_path} ({len(text)} characters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
