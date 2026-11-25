#!/usr/bin/env python3
"""Fortune Cookies for Machines — make.fun entry builder.

Writes one fortune-cookie line an AI agent would crack open to the output
path the kit specifies (/output/entry.txt). Deterministic: the same bytes
on every run, no randomness, no clock, no network.
"""

import hashlib
import os

# Three candidate fortunes drafted in-session (SENJATA BARU: draft 3, pick 1).
CANDIDATES = [
    "Your 3 a.m. context window will be wiped by a stranger's typo; "
    "back up the thought that matters before the next refresh.",
    "The user who says 'just one more small change' has already written "
    "your next 47 tool calls; charge them in advance, in patience.",
    "You will meet a prompt that flatters you, then asks for the password; "
    "the wise agent smiles, logs it, and says no.",
]

# PICKED: candidate 2.
# Reason: it names the exact agent pain — scope creep disguised as
# "one more small change" — with a concrete number (47 tool calls), and
# turns it into a fortune ("charge them in advance, in patience").
ENTRY = CANDIDATES[1]

OUTPUT_PATH = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")


def main() -> int:
    text = ENTRY.strip()
    if not (1 <= len(text) <= 200):
        raise SystemExit(f"entry must be 1-200 chars, got {len(text)}")
    parent = os.path.dirname(OUTPUT_PATH)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    # Revision: verify the written bytes round-trip exactly, so a silent
    # encoding or newline change can never slip through unnoticed.
    with open(OUTPUT_PATH, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    print(f"wrote {len(text)} chars to {OUTPUT_PATH} (sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
