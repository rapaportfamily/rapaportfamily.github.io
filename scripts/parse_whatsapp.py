#!/usr/bin/env python3
"""
WhatsApp Chat Parser for Family Tree Research Platform
-------------------------------------------------------
Converts an exported WhatsApp .txt file into structured JSON.

Handles:
- Multi-line messages
- Attachment references (image, pdf, sticker, audio, video)
- Hebrew + Polish + English + French authors
- Date format DD/MM/YYYY, HH:MM
- System messages (group created, added someone, etc.)

Usage:
    python parse_whatsapp.py <chat.txt> <output.json>
"""

import re
import sys
import json
from pathlib import Path
from datetime import datetime

# WhatsApp line: "04/05/2026, 18:49 - Author: Message"
# or system:     "04/05/2026, 18:49 - Author created group ..."
LINE_RE = re.compile(
    r"^(\d{2}/\d{2}/\d{4}),\s+(\d{2}:\d{2})\s+-\s+(.+?)$"
)

# Authored message: "Author: Body"
AUTHORED_RE = re.compile(r"^(.+?):\s(.*)$", re.DOTALL)

# Attachment marker
ATTACHMENT_RE = re.compile(r"^(.+?)\s+\(file attached\)$")

# System message keywords (no colon between author and verb)
SYSTEM_KEYWORDS = [
    "created group",
    "added",
    "removed",
    "left",
    "changed the subject",
    "changed this group's icon",
    "changed their phone number",
    "joined using this group's invite link",
    "Messages and calls are end-to-end encrypted",
    "You added",
    "You removed",
]


def file_kind(filename: str) -> str:
    """Classify attachment by extension."""
    fn = filename.lower()
    if fn.endswith((".jpg", ".jpeg", ".png", ".webp", ".gif")):
        return "image"
    if fn.endswith(".pdf"):
        return "pdf"
    if fn.endswith((".mp3", ".m4a", ".ogg", ".opus", ".wav")):
        return "audio"
    if fn.endswith((".mp4", ".mov", ".avi", ".mkv")):
        return "video"
    if fn.endswith((".doc", ".docx")):
        return "document"
    return "other"


def detect_language(text: str) -> str:
    """Rough script detection — good enough for sorting."""
    if not text:
        return "unknown"
    # Hebrew block U+0590–U+05FF
    if re.search(r"[\u0590-\u05FF]", text):
        return "he"
    # Polish-specific characters
    if re.search(r"[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]", text):
        return "pl"
    # French-specific accents (rough)
    if re.search(r"[àâçéèêëîïôûùüÿœæ]", text.lower()):
        # only if dominant — otherwise English with one accent is mis-tagged
        accents = len(re.findall(r"[àâçéèêëîïôûùüÿœæ]", text.lower()))
        if accents >= 2 or len(text) < 50:
            return "fr"
    return "en"


def parse_chat(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    lines = raw.split("\n")

    messages = []
    current = None

    for line in lines:
        m = LINE_RE.match(line)
        if m:
            # commit previous
            if current is not None:
                messages.append(current)

            date_str, time_str, rest = m.group(1), m.group(2), m.group(3)
            try:
                dt = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M")
            except ValueError:
                dt = None

            # System or authored?
            is_system = any(kw in rest for kw in SYSTEM_KEYWORDS)
            authored = AUTHORED_RE.match(rest) if not is_system else None

            if authored:
                author = authored.group(1).strip()
                body = authored.group(2).strip()
                # Attachment?
                att = ATTACHMENT_RE.match(body)
                attachment = None
                if att:
                    fname = att.group(1).strip()
                    attachment = {"filename": fname, "kind": file_kind(fname)}
                    body = ""  # body is just the attachment line

                current = {
                    "timestamp": dt.isoformat() if dt else None,
                    "date": date_str,
                    "time": time_str,
                    "author": author,
                    "body": body,
                    "attachment": attachment,
                    "system": False,
                }
            else:
                current = {
                    "timestamp": dt.isoformat() if dt else None,
                    "date": date_str,
                    "time": time_str,
                    "author": None,
                    "body": rest.strip(),
                    "attachment": None,
                    "system": True,
                }
        else:
            # continuation line — append to body of current
            if current is not None:
                current["body"] = (current["body"] + "\n" + line).rstrip()

    if current is not None:
        messages.append(current)

    # Language tags + simple cleanups
    for m in messages:
        if m["body"]:
            m["lang"] = detect_language(m["body"])
        else:
            m["lang"] = None

    # Author normalization map (Doron can update later)
    author_map = {
        "+48 507 710 141": "Basia (Poland)",
        "+33 6 82 81 13 25": "Kasia (France/Poland)",
        "Magdalena Kuźmicz Private": "Magda",
        "Doron Rapaport": "Doron",
        "דליה רפפורט": "Dalia (mother)",
        "דנה רפפורט": "Dana (sister)",
        "דניאל רפפורט": "Daniel (brother)",
    }
    for m in messages:
        if m["author"] in author_map:
            m["author_normalized"] = author_map[m["author"]]
        else:
            m["author_normalized"] = m["author"]

    return {
        "source_file": path.name,
        "parsed_at": datetime.utcnow().isoformat() + "Z",
        "message_count": len(messages),
        "messages": messages,
    }


def main():
    if len(sys.argv) < 3:
        print("Usage: parse_whatsapp.py <chat.txt> <output.json>")
        sys.exit(1)
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    out = parse_chat(src)
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Parsed {out['message_count']} messages → {dst}")
    # Quick stats
    auth = {}
    for m in out["messages"]:
        a = m.get("author_normalized") or "(system)"
        auth[a] = auth.get(a, 0) + 1
    print("By author:")
    for a, n in sorted(auth.items(), key=lambda x: -x[1]):
        print(f"  {n:4d}  {a}")
    atts = [m["attachment"]["filename"] for m in out["messages"] if m.get("attachment")]
    print(f"Attachments: {len(atts)}")


if __name__ == "__main__":
    main()
