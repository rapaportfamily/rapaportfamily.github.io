"""Rewrite all attribution references in the archive so that Dana, Doron and Daniel
Rapaport are credited as equal partners (children of Dov + Dalia), not just Doron.

Doctrine (per Dov 21 May 2026): the archive is by THE THREE SIBLINGS together,
in honour of their father Dov's 80th birthday.

This script does TARGETED phrase replacements — it does NOT touch:
- His proper name 'Doron Rapaport'
- His ID 'p_doron'
- Personal facts about him as an individual (birth, role, relations)
Only project-attribution + 'Doron's <project-thing>' patterns are rewritten.
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / 'platform' / 'data'

# Ordered list of (regex, replacement, description). Applied to every string.
REPLACEMENTS = [
    # Possessives — 'Doron's <X>' --> 'Dana, Doron and Daniel's <X>'
    # But skip already-corrected forms like 'Dana, Doron and Daniel's'
    (r"(?<![,a-zA-Z])Doron's", "Dana, Doron and Daniel's"),
    (r"the user \(Doron(?: Rapaport)?\)", "the user (Dana, Doron and Daniel)"),
    (r"Magda connects Doron with", "Magda connects Dana, Doron and Daniel with"),
    (r"łączy Dorona z", "łączy Danę, Dorona i Daniela z"),
    (r"met en contact Doron avec", "met en contact Dana, Doron et Daniel avec"),
    (r"מקשרת את דורון עם", "מקשרת את דנה, דורון ודניאל עם"),
    # Verb patterns
    (r"\bDoron leads\b", "Dana, Doron and Daniel lead"),
    (r"\bDoron leading\b", "Dana, Doron and Daniel leading"),
    (r"\bDoron started\b", "Dana, Doron and Daniel started"),
    (r"\bDoron asked\b", "Dana, Doron and Daniel asked"),
    (r"\bDoron requested\b", "Dana, Doron and Daniel requested"),
    (r"\bby Doron\b(?! Rapaport)(?! &)", "by Dana, Doron and Daniel"),
    (r"for Doron(?!\s+Rapaport)(?!,)", "for Dana, Doron and Daniel"),
    (r"\bDoron will\b", "Dana, Doron and Daniel will"),
    (r"\bDoron can\b", "Dana, Doron and Daniel can"),
    (r"\bDoron should\b", "Dana, Doron and Daniel should"),
    # The brothers / sister phrasing
    (r"this is Doron's project", "this is Dana, Doron and Daniel's project"),
    (r"Doron's family tree", "Dana, Doron and Daniel's family tree"),
    (r"Doron's research", "Dana, Doron and Daniel's research"),
    (r"Doron's archive", "Dana, Doron and Daniel's archive"),
]

# Files to process (everything under platform/data/ except messages.json which is private chat history)
TARGETS = [
    DATA / 'events.json',
    DATA / 'people.json',
    DATA / 'places.json',
    DATA / 'documents.json',
    DATA / 'hypotheses.json',
    DATA / 'research_center.json',
    DATA / 'ancestry.json',
    DATA / 'i18n' / 'en.json',
    DATA / 'i18n' / 'he.json',
    DATA / 'i18n' / 'pl.json',
    DATA / 'i18n' / 'fr.json',
]

def walk_strings(obj, fn, path=""):
    """Recursively walk a JSON structure, applying fn to every string."""
    if isinstance(obj, dict):
        return {k: walk_strings(v, fn, path + "." + k) for k, v in obj.items()}
    if isinstance(obj, list):
        return [walk_strings(x, fn, path + f"[{i}]") for i, x in enumerate(obj)]
    if isinstance(obj, str):
        return fn(obj, path)
    return obj

total_changes_per_file = {}

def apply_replacements(s, path=""):
    """Apply all regex replacements to a single string, tracking changes."""
    new_s = s
    for pat, repl in REPLACEMENTS:
        new_s = re.sub(pat, repl, new_s)
    if new_s != s:
        total_changes_per_file[current_file] = total_changes_per_file.get(current_file, 0) + 1
    return new_s

for path in TARGETS:
    if not path.exists():
        continue
    current_file = path.name
    data = json.loads(path.read_text(encoding='utf-8'))
    updated = walk_strings(data, apply_replacements)
    path.write_text(json.dumps(updated, ensure_ascii=False, indent=2), encoding='utf-8')

# Summary
print("=== Rewrite summary ===")
for f, n in total_changes_per_file.items():
    print(f"  {f:30} {n} string(s) updated")
if not total_changes_per_file:
    print("  (no strings matched any pattern)")
print()
print("Equal-partners doctrine applied: Dana, Doron and Daniel Rapaport are now")
print("credited as the joint authors of the archive (children of Dov + Dalia,")
print("in honour of Dov's 80th birthday August 2026).")
