# CC SESSION PROTOCOL — Rapaport Family Tree

> Read at the **start of every CC session**. This is the "automation" Doron asked for: until a true server-side trigger is built, CC manually runs this check at every session.

---

## At session START, CC does the following (no prompting needed):

### 1. Pull all pending uploads from Firestore

```bash
# Need: gcloud auth + Firebase project access
PROJECT=rapaport-family-tree-4482
ACCESS_TOKEN=$(gcloud auth print-access-token)
curl -s "https://firestore.googleapis.com/v1/projects/${PROJECT}/databases/(default)/documents/family_uploads?pageSize=200" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "x-goog-user-project: ${PROJECT}" \
  | python -m json.tool > /tmp/pending_uploads.json
```

Filter for `status == "pending"` and process by `kind`:

| kind | Action |
|---|---|
| `photo` | Download file, OCR if applicable, identify what's in the image, propose cross-references |
| `pdf` | Download, extract text (German Kurrentschrift via Gemini Vision if needed), propose cross-references |
| `whatsapp_chat` | Download .txt, parse with `scripts/parse_whatsapp.py`, extract claims, propose additions to people/places/events/hypotheses |
| `whatsapp_chat_archive` | Download .zip, extract chat.txt + media, parse, merge media into pending review with reverse-references |
| `other` | Flag for Doron review only |

### 2. For each pending upload, cross-reference against existing data

For every place / date / name / address mentioned in a new upload, check:

- `platform/data/people.json` — does this confirm, contradict, or extend a `confidence: family_oral` fact to `confidence: documented`?
- `platform/data/places.json` — is this a place we haven't indexed yet?
- `platform/data/events.json` — does this add or refine a date?
- `platform/data/hypotheses.json` — does this resolve, narrow, or refute an open hypothesis (H1-H11)?

### 3. Write findings to `docs/research/incoming_<YYYY-MM-DD>.md`

For each upload processed:
- **Source**: uploader name, upload ID, original filename, file URL
- **Extracted claims**: bullet list, each with a confidence tag (`confirmed` / `documented` / `family_oral` / `hypothesis`)
- **Cross-reference impact**: which existing facts this corroborates / contradicts / extends
- **Recommended action**: approve as-is / approve with edit / reject / hold for Doron

### 4. Update the live data — atomically, with traceability

Where the upload provides primary-source confirmation, update `platform/data/*.json` and `platform/data/hypotheses.json`. Every change cites the upload as the source. Commit with message `[upload <id>] <one-line summary>`.

### 5. Then mark the Firestore doc as processed

Update `family_uploads/{id}` with `status: "cc_processed"` and `cc_summary: "..."` so the admin Review queue shows what CC concluded. Doron then approves or rejects.

---

## When CC doesn't run this protocol

If a session is short or one-off (a quick edit), CC may skip steps 4-5 but must STILL do step 1 and surface anything new in chat: *"By the way — there are N new uploads since the last session, want me to process them now?"*

---

## True server-side automation (future)

A Cloud Function `on_new_upload` (Firestore trigger on `family_uploads` create) could call the Claude API and run this whole protocol without CC needing to be in session. Setup cost: ~$5/mo + 2-3 hrs to wire. Defer until the family is actively uploading 3+ items/week.

---

## What was added on 2026-05-17 (this commit)

- Upload form now accepts `.txt` (chat exports) and `.zip` (chat + media)
- Each upload tagged with `kind: photo | pdf | whatsapp_chat | whatsapp_chat_archive | other`
- Storage rules extended to allow text/plain + zip MIME types
- This protocol document — CC reads at every session start
