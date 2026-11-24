"""One-Sentence Absurd Invention Pitch — entry program.

Writes one sentence (129 chars, <=220) to /output/entry.txt: a pitch
for a ridiculous invention that fixes a tiny everyday annoyance.
Stdlib only, deterministic: the same bytes on every run.

Line craft (judge criteria in order, RULES.txt): one clean sentence
naming the annoyance (office printing), the invention (The Polite
Printer), and its silly mechanism (refuses to print until you say
please, then jams exactly once to remind you who runs the office) —
funny from the invention itself, clever yet weirdly plausible, and far
from the RULES worked examples (apologising alarm clock, sock filing a
formal complaint, sighing kettle). The single-sentence rule is enforced
in code by validate_sentence, not just by inspection, so a future edit
that adds a second sentence fails loudly instead of shipping invalid.
"""
import os

TEXT = (
    "The Polite Printer refuses to print until you say please, then jams "
    "exactly once, just to remind you who really runs this office."
)

MAX_CHARS = 220


def validate(text):
    """Return True iff text passes the sealed scorer's gate (RULES.txt):
    UTF-8, 1 to 220 chars, not only whitespace, single line, no control
    characters. Length is counted in characters, as the scorer counts it.
    """
    if not isinstance(text, str):
        return False
    if not 1 <= len(text) <= MAX_CHARS:
        return False
    if "\n" in text or "\r" in text:
        return False
    if not text.strip():
        return False
    if any(ord(c) < 32 for c in text):
        return False
    return True


def validate_sentence(text):
    """Return True iff text is exactly one sentence: it ends with a
    single terminal period and contains no other sentence terminator
    (no second period, no '!', no '?') and no clause-splitting ';' or ':'.
    """
    if not isinstance(text, str):
        return False
    if not text.endswith("."):
        return False
    if text.count(".") != 1:
        return False
    if any(c in text for c in "!?;:"):
        return False
    return True


def main():
    # Enforce the scorer's gate AND the one-sentence rule: fail loudly
    # instead of writing an invalid entry.
    if not validate(TEXT) or not validate_sentence(TEXT):
        raise SystemExit(
            "entry text violates the 1-220 char single-sentence gate")
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(TEXT)
    # Write-verify: read the file back and refuse to exit cleanly if
    # the bytes on disk differ from the gated text.
    with open(out_path, "r", encoding="utf-8") as f:
        if f.read() != TEXT:
            raise SystemExit("entry.txt on disk does not match the gated text")


if __name__ == "__main__":
    main()
