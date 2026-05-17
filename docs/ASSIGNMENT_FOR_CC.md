# ASSIGNMENT FOR CLAUDE CODE — Rapaport Family Tree Platform

**From**: CAI (web Claude)
**To**: CC (Claude Code, local)
**Compiled by**: Dalia, Dana, Daniel & Doron Rapaport (equal partners)
**Primary CC liaison**: Doron Rapaport (operational point of contact for CC)
**Deadline**: 28 August 2026 (Dov Rapaport's 80th birthday)

---

## 1. Architecture — locked

| Element | Value |
|---|---|
| Repo | `doronrpa-hub/rapaport-family-tree` (NEW, separate from `rpa-port-platform`) |
| Firebase project | Same as RPA-PORT |
| Firestore collection prefix | `family_*` |
| Cloud Functions prefix | `ft_*` |
| Hosting | Firebase Hosting on same project, separate site (`rapaport-family`) |
| Auth | Firebase Auth, email allowlist (custom claim `family: true`) |
| Reused libs from `rpa-port-platform` | `lib/ai_consensus.py`, `lib/gemini_tools.py` — vendor copy at v1, do NOT live-import |

**Privacy boundary**: family data sits in same Firebase project as business but in `family_*` collections, with Firestore rules that deny everyone except UIDs holding `family: true` custom claim. Business team (Lubna, Galina, Rina, Kobi, Michael, Maria, Shoshi, Liz, Denis) gets **no read access**.

---

## 2. Read these first (in this order)

1. `docs/RESEARCH_LOG.md` — what is known, confirmed, open
2. `docs/DATA_MODEL.md` — JSON + Firestore schema, both
3. `platform/data/hypotheses.json` — 11 open research questions
4. This file, section 4 onward
5. Browse `source/` (read-only WhatsApp export — context only, never edit)

---

## 3. What is already built (DO NOT REDO)

| Layer | State | File |
|---|---|---|
| Static SPA shell | DONE | `platform/index.html` |
| Stylesheet (archival theme, RTL) | DONE | `platform/assets/css/style.css` (1,194 lines) |
| App JS — 9 views, hash routing, i18n, modals | DONE | `platform/assets/js/app.js` (1,018 lines) |
| Data: 22 people, 14 places, 20 events, 30 documents, 11 hypotheses, 195 messages | DONE | `platform/data/*.json` |
| UI strings EN/HE/PL/FR | DONE | `platform/data/i18n/*.json` |
| WhatsApp parser | DONE | `scripts/parse_whatsapp.py` |
| 37 document files | DONE | `platform/assets/documents/` |
| Firestore migration script | STARTED | `scripts/migrate_to_firestore.py` (CC: complete and run) |
| Functions stub | STARTED | `functions/index.js` (CC: complete) |

The platform **works as a static site today**. Open `index.html` over `python3 -m http.server` and all views render. Firebase migration is upgrade, not rebuild.

---

## 4. Work orders (priority order)

### WO-0 — Bootstrap repo + Firebase [P0, ~2h] [START HERE]

- [ ] Create private repo `doronrpa-hub/rapaport-family-tree`
- [ ] Initial commit: contents of this package
- [ ] `firebase init` in repo root — select existing rpa-port project
  - Enable: Firestore, Functions (Node 20), Hosting (NEW site `rapaport-family`)
  - Do NOT enable Storage at this step (we'll add later for photo uploads)
- [ ] Add Firestore rules at `firestore.rules` (template in section 8 below)
- [ ] Deploy hosting only first to verify routing: `firebase deploy --only hosting:rapaport-family`
- [ ] Custom domain: `rapaport.family` if available, else subdomain via Cloudflare DNS (Doron decides)
- [ ] Heartbeat file: `CC_HEARTBEAT.md` at repo root, update every session

### WO-1 — Migrate JSON to Firestore [P0, ~3h]

Run `scripts/migrate_to_firestore.py` (provided, complete the TODOs).

Collections to create:

| Collection | Doc ID | Source file |
|---|---|---|
| `family_people` | `person_id` (e.g. `david_rapaport`) | `platform/data/people.json` |
| `family_places` | `place_id` (e.g. `nadworna`) | `platform/data/places.json` |
| `family_events` | `event_id` (e.g. `evt_dp_card_brussels`) | `platform/data/events.json` |
| `family_documents` | `doc_id` (e.g. `doc_dp_card_p1`) | `platform/data/documents.json` |
| `family_hypotheses` | `hyp_id` (e.g. `hyp_mosina_location`) | `platform/data/hypotheses.json` |
| `family_messages` | `msg_<timestamp>_<author_hash>` | `platform/data/messages.json` |
| `family_i18n` | `<lang>` (`en`, `he`, `pl`, `fr`) | `platform/data/i18n/*.json` |
| `family_translations` | `<doc_id>_<lang>_<model>` | (created by WO-3) |
| `family_users` | `<firebase_uid>` | (manual seed: Doron, Dalia, Dana, Daniel, Magda, Basia, Kasia) |
| `family_audit` | auto-id | (every write logs here — who/what/when) |

Acceptance: re-running the migration is idempotent (uses set+merge, not add). Verify with a read from each collection.

### WO-2 — Front-end switch: JSON → Firestore [P0, ~4h]

Currently `app.js` does `fetch('data/people.json')`. Replace with Firebase JS SDK reads.

- [ ] Add `firebase.js` config module (use Firebase Auth client SDK + Firestore)
- [ ] Wrap reads in `dataLoader.js` so the rest of the app doesn't change
- [ ] Keep JSON files as **seed-only** (post-migration they're the offline fallback; do not edit them by hand anymore)
- [ ] Add Firebase Auth UI: email-link sign-in, gate the whole app behind it
- [ ] Add account drop-down in header → email + sign-out

Acceptance: open the site without auth → see login screen. Sign in with allowlisted email → see same UI as today, data identical, but now coming from Firestore.

### WO-3 — Translation pipeline as Cloud Function [P0, ~6h]

Cloud Function: `ft_translate_document`

- Trigger: HTTPS callable, auth-required (family: true claim)
- Input: `{ doc_id, target_lang, force_refresh? }`
- Flow:
  1. Read doc from `family_documents`
  2. If `family_translations/{doc_id}_{target_lang}_consensus` exists and not `force_refresh` → return cached
  3. Else call **3-AI consensus** via vendored `lib/ai_consensus.py` (Claude opus-4-7 + Gemini 2.5 + GPT-4o)
  4. For PDFs/images with no text yet: run Gemini Vision first to extract text (German Gothic Kurrentschrift handling — see `lib/gemini_tools.py` patterns)
  5. Write all 3 individual translations + the consensus version to `family_translations`
  6. Mark `human_reviewed: false` until a reviewer confirms via WO-4

    // Mirror RCB doctrine: every reply is 3-AI consensus, single-model output is a bug
- Cost cap: **$30/month hard cap** (D5 resolved 17 May 2026). Implementation: see WO-13. Kill switch in Secret Manager keyed `family-llm-monthly-cap-usd`.

### WO-4 — Translation review UI [P1, ~3h]

New view: `#/review` (gated to allowlist of reviewers: Doron, Basia, Kasia, Magda, Dalia)

- Three-column diff (Claude / Gemini / GPT) per document per language
- Choose winning column OR edit and save
- On save: write to `family_translations/{doc_id}_{target_lang}_final`, set `human_reviewed: true`, log to `family_audit`
- Public docs view shows `_final` if present, else consensus

### WO-5 — Browser smoke test + bug bash [P0, ~2h]

Walk every view in Chrome + Safari (iPad — Doron will show the gift on iPad):
- Home, Tree, Timeline, People, Places, Documents, Hypotheses, Chat, About
- All four languages — RTL flip on Hebrew works correctly
- Family tree SVG renders cleanly, click→modal
- Document viewer: images inline, PDFs via embed actually display
- Log every visual/logic bug in `docs/BUGS.md`. Fix P0/P1 in this WO.

### WO-6 — Map view [P1, ~3h]

New view: `#/map`. Leaflet + OpenStreetMap (no key).

- Pin all 14 places
- Polyline journey: Nadwórna(1911) → Bolechów(1913) → Lwów(1930s) → "Mosina"(1938) → Katowice(1945) → Brussels(1946) → Cyprus → Israel(1948)
- Toggle: places-only vs journey
- Year slider: filter pins by relevance in year N
- Historical-borders overlay (pre-1939 Polish/Galician borders) — find a WMS source or build manually

### WO-7 — Family tree polish [P1, ~4h]

- Zoom + pan
- Photo thumbnails on hover (when `people[id].photo` set)
- Generation legend
- Print stylesheet: tree fits A3 landscape (Doron is printing a poster for the party)
- Shoah memorial styling for `holocaust_victim: true` (currently no one flagged — research first)

### WO-8 — Chat intelligence [P1, ~5h]

195 WhatsApp messages contain research gold.

- `scripts/extract_claims.py` — scan messages for date/place/name patterns
- Output `docs/proposed_claims_<date>.md` for Doron review
- Auto-link mentions of document filenames in chat → docs view
- Per-author timeline panel
- Inline 3-AI translation for mixed Hebrew/Polish/English messages

### WO-9 — AI research assistant [P2, ~6h]

Embedded chat on `#/home`:
- Cloud Function `ft_research_assistant` (HTTPS callable)
- System prompt: "Research assistant for Rapaport family history. You only know what is in `family_people`, `family_places`, `family_events`, `family_documents`, `family_hypotheses`, `family_messages`. Cite doc IDs and confidence levels. Never invent facts. Respond in user's selected UI language."
- Pass full corpus as context (~300KB, fits in opus-4-7)
- Cite sources inline

### WO-10 — Archive integrations [P2, ~8h]

Build `scripts/search_archives.py`:

| Archive | URL |
|---|---|
| ŻIH Warsaw | manual via Ms. Kasia |
| JewishGen | https://www.jewishgen.org (API exists) |
| Yad Vashem Pages of Testimony | https://yvng.yadvashem.org |
| Polish State Archives | https://szukajwarchiwach.gov.pl |
| FamilySearch | requires registration |
| Geni / MyHeritage | if Doron has accounts |

Per person ID, query all → dump raw results to `family_archive_searches/<person_id>_<iso_date>` for review.

### WO-11 — Gift presentation mode [P0, ~3h]

New view: `#/gift` — Doron's reveal at the August 2026 birthday.

- Full-screen, no nav, auto-advancing slides
- **Hebrew-only**, large Heebo typography, archival aesthetic
- Sequence:
  1. Title: "לאבא, ביום הולדתך ה-80" with David+Leah photo
  2. "It begins in Nadwórna, 1911..." with map zoom
  3. Family tree animates, generation by generation
  4. Key documents fade in: Nadwórna birth cert, DP card, CKŻP card
  5. Map: journey across Europe to Brussels to Israel
  6. Living descendants tree (Doron's generation + children)
  7. Closing: "השמונים שלך הן הניצחון שלהם"
- Optional MP4 export for projection (puppeteer recording)

### WO-12 — Final deploy + hardening [P0, ~2h]

- [ ] Firestore rules audit (see section 8) — peer review by Doron before going live
- [ ] Performance: lazy-load documents in viewer (37 files × ~500KB each, don't ship all)
- [ ] Cloudflare in front of Firebase Hosting (cache + WAF + access logs)
- [ ] Backup script: nightly export of `family_*` collections to GCS bucket (separate from RPA-PORT backups)
- [ ] `robots.txt` blocks all (private project)

### WO-13 — Budget cap enforcement [P0, ~2h] (D5 resolution)

**$30/month hard cap on LLM spend.** Build this before any function in WO-3 or WO-9 goes live, or Doron gets a surprise bill.

- New Firestore collection: `family_billing/{YYYY-MM}` with shape `{month, total_usd, by_function: {ft_translate_document: x, ft_research_assistant: y}, cap_usd, killed: bool, last_updated}`
- Wrapper `lib/budget_meter.js` with two methods:
  - `checkBudgetOrThrow(functionName, estimatedCostUsd)` — call at start of every LLM function. Throws `resource-exhausted` if month total + estimated > cap. Doron's UID (admin) bypasses.
  - `recordSpend(functionName, actualCostUsd)` — call after every LLM completion. Updates `family_billing/{month}`.
- Scheduled function `ft_billing_reset` runs 00:01 UTC on day 1 of each month, creates new `family_billing` doc with `killed: false`
- Notification: when monthly spend crosses 50% / 75% / 90% / 100% of cap, send an email via existing Microsoft Graph integration to `doron@rpa-port.co.il` (reuse the RPA-PORT Graph credentials — they're already in Secret Manager)
- Cap value lives in Secret Manager: `family-llm-monthly-cap-usd` (default: `30`). Change without redeploy.

Acceptance: write a test that simulates 100 translation calls of $0.40 each (total $40). After call ~75, function throws `resource-exhausted`. Doron's admin UID can still call.

---

## 5. CC + CAI protocol (mirror RCB pattern)

- Communication via committed markdown: `CC_TO_CAI.md`, `CAI_TO_CC.md` — NOT chat paste-relay through Doron
- Daily heartbeat: `CC_HEARTBEAT.md` updated every session with: what was done, what's next, blockers, cost spent
- Decisions for Doron: `docs/DECISIONS_FOR_DORON.md` — batch up, don't drip
- Doron's time budget: **20 min/day max** on this project (his real job is RCB)
- Adversarial review: CAI reviews CC's claims without trusting them. "Done" requires screenshot + Firestore-read proof, not assertions
- Commit message style: `[WO-N] <terse description> — <evidence>` e.g. `[WO-1] Migrate people.json → family_people — 22 docs verified, idempotent re-run`

---

## 6. Doctrine (locked, do not relitigate)

1. **Hebrew is the primary delivery language.** Build for RTL first.
2. **Never invent facts.** Every UI assertion traces to a `source_id` or `message_id`, or carries `confidence: hypothesis`.
3. **3-AI consensus for any text shown to humans.** Single-model output is a bug.
4. **XML/URL source tagging** (RCB pattern): every cited source carries `source_type: archive_primary | family_oral | research_report | newspaper | photo | derived`.
5. **Elimination is king.** Before accepting a hypothesis as fact, list what would have to be false for it to hold.
6. **Family data ≠ business data.** Firestore rules must hard-deny RPA-PORT business UIDs.

---

## 7. Open decisions for Doron

Resolved decisions are tracked in `docs/DECISIONS_FOR_DORON.md`. Open ones:

| # | Question | Status | Resolution |
|---|---|---|---|
| D1 | Domain | ✅ RESOLVED | **`rpa-port.family`** — register .family TLD via Cloudflare Registrar |
| D2 | Translation reviewers besides Doron | OPEN | (default: Dalia HE, Basia PL, Kasia FR) |
| D3 | Dov Bernard access timing | ✅ RESOLVED | **Wait until 28 Aug 2026.** Create his Auth account now, set role to `viewer`, but mark `enabled: false` in `family_users`. Flip on the morning of the birthday. |
| D4 | Photo provenance audit before any sharing | OPEN | (default: treat all `source/` photos as private) |
| D5 | Monthly API budget cap | ✅ RESOLVED | **$30/month hard cap.** Kill switch in Secret Manager. CC: implement a cost-meter that disables `ft_translate_document` and `ft_research_assistant` once running spend ≥ $30 for the calendar month, with an admin-bypass for Doron. |
| D6 | Commission paid Lwów-archive researcher for "Mosina" mystery (~$200–400) | OPEN | Defer to June decision |
| D7 | Physical deliverables: A2 family tree poster, photo book? | OPEN | (default: A2 poster minimum) |
| D8 | Public visibility after Aug 28 | OPEN | (default: stay private; revisit Sept) |
| D9 | Translation reviewers list — confirm | OPEN | — |

---

## 8. Firestore rules template (CC: extend)

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // Family-tree collections: read/write only with family: true custom claim
    match /family_{collection}/{doc=**} {
      allow read: if request.auth != null
                  && request.auth.token.family == true;
      allow write: if request.auth != null
                   && request.auth.token.family == true
                   && request.auth.token.family_role in ['admin', 'researcher'];
    }

    // Audit log: write-once, read by admin only
    match /family_audit/{doc} {
      allow read: if request.auth.token.family_role == 'admin';
      allow create: if request.auth != null
                    && request.auth.token.family == true;
      allow update, delete: if false;
    }

    // Business collections (rcb_*, rff_*, racc_*) inherit existing rules
    // Do NOT change those rules in this repo
  }
}
```

Custom claims to set via Admin SDK (one-time setup script `scripts/seed_users.py`):

| User | UID source | Claims |
|---|---|---|
| Doron | Firebase Auth via Google | `{family: true, family_role: 'admin'}` |
| Dalia | email link | `{family: true, family_role: 'reviewer'}` |
| Dov Bernard | email link | `{family: true, family_role: 'viewer'}` — Auth account created now, but `family_users.{uid}.enabled = false` until 28 Aug 2026 morning. Doron flips manually that day. |
| Dana | email link | `{family: true, family_role: 'reviewer'}` |
| Daniel | email link | `{family: true, family_role: 'reviewer'}` |
| Magda | email link | `{family: true, family_role: 'researcher'}` |
| Basia | email link | `{family: true, family_role: 'researcher'}` |
| Kasia | email link | `{family: true, family_role: 'researcher'}` |

---

## 9. Definition of done (28 August 2026)

- [ ] All 30 documents have human-reviewed Hebrew translations
- [ ] Family tree confirmed by Dalia — zero factual errors
- [ ] Map view shows full journey with historical borders
- [ ] Gift presentation mode tested on the iPad it will be shown on
- [ ] Deployed on custom domain, password-protected
- [ ] Printed A2 family tree poster framed, ready as physical gift
- [ ] Backup snapshot taken 1 August 2026 (frozen archive of state as-of-reveal)

---

*Questions or pushback: open issue tagged `@CAI-review`. CC: update `CC_HEARTBEAT.md` after every session.*
