"""Inject OCR text from cache into documents.json entries.

For each document referenced in documents.json:
- Find any file_pages that have OCR text in ocr_cache/
- Set transcription field with the OCR text (combined if multi-page)
- Set ocr_meta field with engine + lang_hint + content_hash

Also: sort additional_files chronologically per messages.json.
"""
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DOCS = REPO / "platform" / "data" / "documents.json"
MSGS = REPO / "platform" / "data" / "messages.json"
CACHE = REPO / "platform" / "data" / "ocr_cache"

# Map filename -> (text, meta)
def load_cache():
    cache = {}
    if not (CACHE / "_index.json").exists():
        return cache
    idx = json.loads((CACHE / "_index.json").read_text(encoding="utf-8"))
    for fn, info in idx.get("by_filename", {}).items():
        text_path = info.get("text_path")
        if text_path:
            full = REPO / "platform" / "data" / text_path
            if full.exists():
                txt = full.read_text(encoding="utf-8")
                cache[fn] = {
                    "text": txt,
                    "meta": info,
                }
    return cache


def chronological_order_from_chat(d_msgs):
    """Map filename -> first-seen-timestamp."""
    first_ts = {}
    for m in d_msgs["messages"]:
        att = m.get("attachment")
        if not att or not isinstance(att, dict):
            continue
        fn = att.get("filename")
        if not fn:
            continue
        ts = m.get("timestamp") or ""
        if fn not in first_ts or ts < first_ts[fn]:
            first_ts[fn] = ts
    return first_ts


def main():
    docs = json.loads(DOCS.read_text(encoding="utf-8"))
    msgs = json.loads(MSGS.read_text(encoding="utf-8"))
    cache = load_cache()
    print(f"OCR cache entries: {len(cache)}")

    first_ts = chronological_order_from_chat(msgs)

    # Inject OCR into documents
    injected = 0
    for doc in docs["documents"]:
        files = doc.get("file_pages") or []
        ocr_parts = []
        engines = set()
        langs = set()
        for f in files:
            if f in cache:
                ocr_parts.append(f"--- {f} ---\n{cache[f]['text']}")
                m = cache[f]["meta"]
                engines.add(m.get("engine", ""))
                langs.add(m.get("lang_hint", ""))
        if ocr_parts:
            existing = doc.get("transcription")
            new_text = "\n\n".join(ocr_parts)
            # Keep existing transcription if it's better (longer); add OCR as transcription_ocr
            if existing and isinstance(existing, str) and len(existing) > 200:
                doc["transcription_ocr"] = new_text
            else:
                doc["transcription"] = new_text
            doc["ocr_meta"] = {
                "engines": sorted(engines),
                "lang_hints": sorted(langs),
                "files_ocrd": [f for f in files if f in cache],
            }
            injected += 1

    print(f"docs with OCR injected: {injected}")

    # Inject OCR + chronological order into additional_files
    additional_with_ts = []
    for entry in docs.get("additional_files", []):
        fn = entry.get("file", "")
        ts = first_ts.get(fn, "")
        entry["timestamp"] = ts
        if fn in cache:
            entry["transcription"] = cache[fn]["text"]
            entry["ocr_meta"] = {
                "engine": cache[fn]["meta"].get("engine"),
                "lang_hint": cache[fn]["meta"].get("lang_hint"),
            }
        additional_with_ts.append((ts, entry))
    additional_with_ts.sort(key=lambda x: (x[0] or "9999",))
    docs["additional_files"] = [e for _, e in additional_with_ts]

    DOCS.write_text(json.dumps(docs, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"documents.json updated. additional_files now sorted chronologically.")
    print(f"  total docs: {len(docs['documents'])}")
    print(f"  total additional_files: {len(docs['additional_files'])}")


if __name__ == "__main__":
    main()
