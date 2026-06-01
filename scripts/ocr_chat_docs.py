"""OCR every chat-referenced document via Tesseract (pol+eng+heb+deu).

For each unique chat attachment (in chronological message order):
- Run Tesseract with auto-detection of language (pol+eng+heb+deu)
- Save raw OCR to platform/data/ocr_cache/{filename}.txt
- Save metadata to platform/data/ocr_cache/{filename}.json (sha256, timestamp, language hint)

Outputs an index file `platform/data/ocr_cache/_index.json` keyed by filename.
"""
from __future__ import annotations

import json
import hashlib
import subprocess
import os
import sys
import re
from pathlib import Path
from datetime import datetime, timezone

REPO = Path(__file__).resolve().parents[1]
DOCS = REPO / "platform" / "assets" / "documents"
CACHE = REPO / "platform" / "data" / "ocr_cache"
TESS = "C:/Program Files/Tesseract-OCR/tesseract.exe"
TESSDATA = str(Path.home() / "tessdata")
LANGS = "pol+eng+heb+deu"

CACHE.mkdir(parents=True, exist_ok=True)

# Skip stickers + non-images + huge PDFs (tesseract can't do PDF natively)
SKIP_EXT = {".webp"}  # stickers
IMG_EXT = {".jpg", ".jpeg", ".png", ".gif", ".jfif", ".tif", ".tiff"}

def content_hash(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def ocr_image(img_path: Path) -> dict:
    """Run Tesseract on an image, return result dict."""
    out_txt = CACHE / (img_path.stem + ".txt")
    out_meta = CACHE / (img_path.stem + ".json")

    ch = content_hash(img_path)
    # Cache check
    if out_meta.exists():
        try:
            meta = json.loads(out_meta.read_text(encoding="utf-8"))
            if meta.get("content_hash") == ch:
                return {**meta, "from_cache": True}
        except Exception:
            pass

    # Run Tesseract
    try:
        proc = subprocess.run(
            [TESS, "--tessdata-dir", TESSDATA, "-l", LANGS, "--psm", "6", str(img_path), "-"],
            capture_output=True, timeout=120,
        )
        text = proc.stdout.decode("utf-8", errors="replace").strip()
        err = proc.stderr.decode("utf-8", errors="replace").strip()
    except subprocess.TimeoutExpired:
        text = ""
        err = "TIMEOUT"
    except Exception as e:
        text = ""
        err = f"ERROR: {e}"

    # Detect language hint
    he_chars = sum(1 for c in text if "֐" <= c <= "׿")
    latin_chars = sum(1 for c in text if c.isalpha() and ord(c) < 0x500)
    pl_chars = sum(1 for c in text if c in "ąćęłńóśźżĄĆĘŁŃÓŚŹŻ")
    de_chars = sum(1 for c in text if c in "äöüßÄÖÜẞ")
    total = he_chars + latin_chars
    lang_hint = "en"
    if total > 0:
        if he_chars / total > 0.5:
            lang_hint = "he"
        elif pl_chars > 3:
            lang_hint = "pl"
        elif de_chars > 3:
            lang_hint = "de"

    out_txt.write_text(text, encoding="utf-8")
    meta = {
        "filename": img_path.name,
        "content_hash": ch,
        "engine": "tesseract-5.4.0",
        "langs": LANGS,
        "lang_hint": lang_hint,
        "char_count": len(text),
        "ocr_at": datetime.now(timezone.utc).isoformat(),
        "stderr_excerpt": err[:300] if err else "",
        "text_path": f"ocr_cache/{out_txt.name}",
    }
    out_meta.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return meta


def load_chronological_attachments():
    """Return chronologically-sorted list of unique attachment filenames from chat."""
    msgs_path = REPO / "platform" / "data" / "messages.json"
    d = json.loads(msgs_path.read_text(encoding="utf-8"))
    seen = set()
    chrono = []
    for m in d["messages"]:
        att = m.get("attachment")
        if not att or not isinstance(att, dict):
            continue
        fn = att.get("filename")
        if not fn or fn in seen:
            continue
        seen.add(fn)
        chrono.append({
            "filename": fn,
            "timestamp": m.get("timestamp"),
            "author": m.get("author_normalized") or m.get("author"),
            "kind": att.get("kind"),
        })
    return chrono


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    chrono = load_chronological_attachments()
    print(f"Chronological chat attachments: {len(chrono)}")

    index = {"order": [], "by_filename": {}}
    processed = 0
    skipped = 0
    failed = 0

    for i, item in enumerate(chrono, 1):
        fn = item["filename"]
        ext = Path(fn).suffix.lower()

        # Skip stickers
        if ext in SKIP_EXT:
            print(f"  [{i}/{len(chrono)}] SKIP (sticker): {fn}")
            skipped += 1
            continue

        img_path = DOCS / fn
        if not img_path.exists():
            print(f"  [{i}/{len(chrono)}] SKIP (missing on disk): {fn}")
            skipped += 1
            continue

        if ext not in IMG_EXT:
            # PDFs — record placeholder, don't OCR (Claude can read these directly elsewhere)
            print(f"  [{i}/{len(chrono)}] PDF (no Tesseract): {fn}")
            index["order"].append(fn)
            index["by_filename"][fn] = {
                **item,
                "kind_resolved": "pdf",
                "ocr": None,
            }
            continue

        print(f"  [{i}/{len(chrono)}] OCR: {fn}")
        try:
            meta = ocr_image(img_path)
            processed += 1
            index["order"].append(fn)
            index["by_filename"][fn] = {**item, **meta}
        except Exception as e:
            print(f"      ERROR: {e}")
            failed += 1

    # Write index
    (CACHE / "_index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nDone. processed={processed} skipped={skipped} failed={failed}")
    print(f"Index: {CACHE / '_index.json'}")


if __name__ == "__main__":
    main()
