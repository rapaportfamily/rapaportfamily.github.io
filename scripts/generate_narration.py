"""Generate a two-person podcast-style narration of Lusia's memoir.

Two voices:
  HOST    — warm, curious, asks the questions a listener would ask
  STORYTELLER — speaks Lusia's experience in first or third person from the memoir

Output:
  platform/data/memoir_narration_en.md   (English script)
  platform/data/memoir_narration_he.md   (Hebrew script)
  platform/data/memoir_narration_pl.md   (Polish script)

Each script is structured as:
  - Cold open (HOST sets the scene)
  - One conversation per memoir section / chapter
  - Closing (HOST reflects)

This is the SCRIPT only. Audio generation (Google TTS / ElevenLabs) is Phase 3.

Calls Gemini for the script generation. Each language gets its own call so
the script reads natively in each language (not just a translation).
"""
import json
import os
import re
import sys
import time
from pathlib import Path

import google.generativeai as genai

REPO = Path(__file__).resolve().parent.parent
PAGES_JSON = REPO / "platform" / "data" / "memoir_pages.json"
META_JSON  = REPO / "platform" / "data" / "memoir.json"
KEY_PATH   = Path(r"C:\Users\User\AppData\Local\Temp\_gk.txt")

if not PAGES_JSON.exists():
    print(f"[ERR] {PAGES_JSON} missing — run OCR first", file=sys.stderr)
    sys.exit(1)
if not KEY_PATH.exists():
    print(f"[ERR] {KEY_PATH} missing", file=sys.stderr)
    sys.exit(1)

genai.configure(api_key=KEY_PATH.read_text(encoding="utf-8").strip())
model = genai.GenerativeModel("gemini-2.5-flash")

pages = json.loads(PAGES_JSON.read_text(encoding="utf-8"))
pages.sort(key=lambda p: p.get("page", 0))
meta = json.loads(META_JSON.read_text(encoding="utf-8")) if META_JSON.exists() else {}

# Build a single corpus per language
def corpus(lang: str) -> str:
    out = []
    for p in pages:
        txt = p.get(lang, "")
        if not txt: continue
        out.append(f"[page {p.get('page')}] {txt}")
    return "\n\n".join(out)

LANG_NAMES = {"en": "English", "he": "Hebrew (modern Israeli, RTL)", "pl": "Polish"}

PROMPT_TEMPLATE = """You are scripting a two-voice audio narration of a Holocaust-survivor memoir, in {lang_name}.

THE MEMOIR is "סיפורה של לוסיה" (The Story of Lusia) by Leah/Lusia Rapaport née Weitzner, a Polish-Jewish Holocaust survivor who escaped Nazi-occupied Galicia and reached Brussels in 1946 before settling in Israel. She is the paternal grandmother of the Rapaport family that this archive serves (Dalia, Dana, Daniel, Doron — equal partners). The memoir is being preserved as an 80th-birthday gift for her son Dov Rapaport.

THE TWO VOICES:
  HOST — warm, curious, contemporary. Asks the questions a grandchild listener would ask. Speaks in {lang_name}.
  STORYTELLER — speaks Lusia's words and experiences with quiet dignity. Sometimes first-person quoting the memoir, sometimes narrating in third person. {lang_name}.

DOCTRINE:
- NEVER invent facts. If the memoir says X, the script says X. If the memoir is silent, the script is silent.
- Lusia and David are HOLOCAUST SURVIVORS first and foremost. Honour her words.
- Hebrew place names: keep Hebrew spellings (Nadwórna, Bolechów, Lwów) but render them in {lang_name} orthography where natural.
- Two-voice format: alternate HOST: and STORYTELLER: line by line, with blank lines between.
- Aim for ~25-35 minutes of speech total (= roughly 4000-5500 words for English).
- Structure: Cold open → Childhood → Marriage to David → War and survival → Escape and Brussels → Closing.
- If a passage is illegible or missing, skip it gracefully (don't fake content).

OUTPUT FORMAT (plain text, {lang_name}):
  Title line
  Cold open (HOST speaks first)
  Then alternating HOST: / STORYTELLER: blocks
  End with a HOST reflection

Memoir text follows below. Use ALL of it — don't summarize. Stay close to her language.

=== MEMOIR ({lang_name}) ===
{corpus}
=== END MEMOIR ===

Now write the full narration script in {lang_name}. Plain text only, no markdown headers."""

OUT_FILES = {
    "en": REPO / "platform" / "data" / "memoir_narration_en.md",
    "he": REPO / "platform" / "data" / "memoir_narration_he.md",
    "pl": REPO / "platform" / "data" / "memoir_narration_pl.md",
}

for lang_code, out_path in OUT_FILES.items():
    if out_path.exists():
        print(f"[skip] {out_path.name} exists — delete to regenerate")
        continue
    c = corpus(lang_code)
    if len(c) < 500:
        print(f"[skip] {lang_code}: corpus too small ({len(c)} chars)")
        continue
    print(f"[gen] {lang_code} ({len(c):,} corpus chars)... ", end="", flush=True)
    prompt = PROMPT_TEMPLATE.format(lang_name=LANG_NAMES[lang_code], corpus=c)
    try:
        resp = model.generate_content(prompt, generation_config={"temperature": 0.6, "max_output_tokens": 16000})
        out_path.write_text(resp.text, encoding="utf-8")
        print(f"OK {len(resp.text):,} chars -> {out_path}")
    except Exception as e:
        print(f"FAIL {e}")
    time.sleep(5)

print("[done] narration scripts generated")
