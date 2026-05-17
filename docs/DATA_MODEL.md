# DATA MODEL — Rapaport Family Tree Platform

This document is the **schema of truth**. Every JSON file under `platform/data/` and every Firestore collection under `family_*` follows the shapes defined here. CC: if you need to add a field, update this doc in the same commit.

---

## 1. Dual representation: JSON + Firestore

The platform was built with portable JSON files as the source of truth. After WO-1 the data lives in Firestore; the JSON files become **seed-only / offline fallback**.

| Stage | Authority |
|---|---|
| Pre-WO-1 (current) | JSON files in `platform/data/` |
| Post-WO-1 | Firestore `family_*` collections — JSON files no longer hand-edited |

Same shape, two stores. The seed script `scripts/migrate_to_firestore.py` walks the JSON and writes to Firestore preserving keys.

---

## 2. Core principles

1. **Every fact carries a `confidence`** — one of: `confirmed`, `documented`, `family_oral`, `hypothesis`, `ruled_out`
2. **Every fact carries a `sources` array** — list of document IDs or message IDs that support it (empty array allowed only for `family_oral`)
3. **Multilingual fields** — any user-visible string is an object `{en, he, pl, fr}`, all four required (use `null` if not yet translated, never empty string)
4. **IDs are stable, human-readable, snake_case** — never auto-generated UUIDs for entity types. Auto-IDs only for `family_audit` log entries.
5. **No deletions** — flag with `status: archived` instead. Soft-delete only. (Genealogy data is too easily lost.)
6. **Audit every write** — `family_audit` gets one entry per Firestore write: `{uid, collection, doc_id, action, before_hash, after_hash, ts}`

---

## 3. Collections

### 3.1 `family_people`

```json
{
  "id": "david_rapaport",
  "names": {
    "primary": {
      "en": "David Mendel Rapaport",
      "he": "דוד מנדל רפפורט",
      "pl": "Dawid Mendel Rapaport",
      "fr": "David Mendel Rapaport"
    },
    "aliases": [
      {"text": "Dawid Mendel Rappaport", "context": "Polish docs"},
      {"text": "דוד רפפורט", "context": "Israeli docs"}
    ]
  },
  "role": "paternal_grandfather",
  "generation": 3,
  "birth": {
    "date": "1911-12-25",
    "date_confidence": "confirmed",
    "place_id": "nadworna",
    "place_confidence": "confirmed",
    "sources": ["doc_david_birth_nadworna", "doc_dp_card_p1"]
  },
  "death": {
    "date": null,
    "place_id": null,
    "sources": []
  },
  "father_id": "berisz_rapaport",
  "mother_id": "rebeka_griffel",
  "spouse_ids": ["leah_weitzner"],
  "children_ids": ["shimon_rapaport", "dov_bernard_rapaport"],
  "facts": [
    {
      "type": "occupation",
      "value": {"en": "Forestry engineer", "he": "מהנדס יערן", "pl": "Inżynier leśnictwa", "fr": "Ingénieur forestier"},
      "confidence": "documented",
      "sources": ["doc_dp_card_p1"]
    },
    {
      "type": "languages_spoken",
      "value": ["pl", "it", "de", "cs", "ru"],
      "confidence": "family_oral",
      "sources": []
    },
    {
      "type": "political_affiliation",
      "value": {"en": "Betar Poland (revisionist Zionist youth)", "he": "ביתר פולין"},
      "confidence": "family_oral",
      "sources": []
    },
    {
      "type": "citizenship_status",
      "value": {"en": "Stripped of Polish citizenship 1942", "he": "אזרחותו הפולנית נשללה ב-1942"},
      "confidence": "documented",
      "sources": ["doc_dp_card_p2"]
    }
  ],
  "holocaust_survivor": true,
  "holocaust_victim": false,
  "photos": ["photo_david_prewar"],
  "status": "active",
  "created_at": "2026-05-15T10:00:00Z",
  "updated_at": "2026-05-17T13:00:00Z",
  "updated_by": "doron"
}
```

**Roles** (controlled vocabulary): `subject` (Dov Bernard), `paternal_grandfather`, `paternal_grandmother`, `maternal_grandfather`, `maternal_grandmother`, `great_grandfather`, `great_grandmother`, `gg_grandfather`, `gg_grandmother`, `father`, `mother`, `sibling`, `child`, `aunt`, `uncle`, `cousin`, `descendant`, `ancestor_unconfirmed`

**Generations** (integer, Dov Bernard = generation 4):
- 1 = great-great-grandparents (e.g. Samuel Weinreb)
- 2 = great-grandparents (e.g. Elias Weitzner, Berisz Rapaport)
- 3 = grandparents (David, Leah)
- 4 = parents (Dov Bernard, Dalia) — **subject's generation**
- 5 = children (Doron, Dana, Daniel)
- 6 = grandchildren

### 3.2 `family_places`

```json
{
  "id": "nadworna",
  "names": {
    "en": "Nadwórna",
    "he": "נדבורנה",
    "pl": "Nadwórna",
    "fr": "Nadwórna",
    "yi": "נאדבארנע",
    "de": "Nadwórna",
    "uk": "Надвірна",
    "modern": "Надвірна, Ukraine"
  },
  "coordinates": {"lat": 48.6356, "lng": 24.5733},
  "country_current": "UA",
  "region_current": "Ivano-Frankivsk Oblast",
  "era_context": [
    {
      "period": "austro_hungarian",
      "years": "1772-1918",
      "country": "Austria-Hungary",
      "region": "Galicia",
      "lang_official": "de+pl",
      "note_en": "Jewish community ~3,000, town center had multiple synagogues",
      "note_he": "..."
    },
    {
      "period": "polish_2nd_republic",
      "years": "1918-1939",
      "country": "Poland",
      "region": "Stanisławów Voivodeship",
      "lang_official": "pl",
      "note_en": "Period of David's birth and youth"
    },
    {
      "period": "soviet_occupation",
      "years": "1939-1941",
      "country": "USSR",
      "lang_official": "ru+uk"
    },
    {
      "period": "german_occupation",
      "years": "1941-1944",
      "country": "Nazi Germany (Distrikt Galizien, GG)",
      "note_en": "Ghetto established. Mass shootings 1942. David and Leah escaped in a railway wagon hidden between logs."
    },
    {
      "period": "modern",
      "years": "1991-present",
      "country": "Ukraine",
      "lang_official": "uk"
    }
  ],
  "significance": {
    "en": "Birthplace of David Rapaport. Confirmed 15 May 2026 by Ms. Kasia at ŻIH Warsaw, overturning DP card record of Cieszyn.",
    "he": "..."
  },
  "related_people": ["david_rapaport", "rebeka_griffel", "berisz_rapaport", "leizor_griffel", "sara_chajes"],
  "related_documents": ["doc_david_birth_nadworna"],
  "status": "active"
}
```

### 3.3 `family_events`

```json
{
  "id": "evt_david_birth",
  "date_sort": "1911-12-25",
  "date_display": {"en": "25 December 1911", "he": "25 בדצמבר 1911", "pl": "25 grudnia 1911", "fr": "25 décembre 1911"},
  "date_confidence": "confirmed",
  "type": "birth",
  "title": {
    "en": "Birth of David Mendel Rapaport",
    "he": "לידת דוד מנדל רפפורט",
    "pl": "Narodziny Dawida Mendla Rapaporta",
    "fr": "Naissance de David Mendel Rapaport"
  },
  "description": {
    "en": "...",
    "he": "...",
    "pl": "...",
    "fr": "..."
  },
  "place_id": "nadworna",
  "people_ids": ["david_rapaport", "berisz_rapaport", "rebeka_griffel"],
  "document_ids": ["doc_david_birth_nadworna"],
  "category": "family",
  "confidence": "confirmed",
  "sources": ["doc_david_birth_nadworna"]
}
```

**Types** (controlled): `birth`, `death`, `marriage`, `migration`, `escape`, `arrest`, `registration`, `discovery` (research milestones), `context` (world-historical context — pogroms, wars, laws affecting the family)
**Categories** (controlled): `family`, `context`, `discovery` (a research breakthrough — e.g. 15 May 2026 Nadwórna find)

### 3.4 `family_documents`

```json
{
  "id": "doc_dp_card_p1",
  "filename": "Karta David Rapaport 1 strona.pdf",
  "kind": "scan",
  "type": "displaced_persons_card",
  "pages": 1,
  "primary_language": "fr",
  "languages_present": ["fr", "de"],
  "source_archive": "Brussels DP processing center, 9 April 1946",
  "source_provenance": {
    "en": "Provided by Kasia via WhatsApp, originally from Belgian state archives",
    "obtained_date": "2026-05-04",
    "obtained_from": "kasia"
  },
  "titles": {
    "en": "David Rapaport — Brussels DP Card, page 1",
    "he": "דוד רפפורט — כרטיס עקור בריסל, עמוד 1",
    "pl": "Karta osoby przesiedlonej Dawida Rapaporta, strona 1",
    "fr": "Carte de personne déplacée — David Rapaport, page 1"
  },
  "decoded_fields": {
    "name": "RAPAPORT David Mendel",
    "born": "25.12.1911 Cieszyn (CONFLICT: actual = Nadwórna, per ŻIH)",
    "father": "Berisz",
    "mother": "Rebeka Griffel",
    "nationality": "ex-Polonaise, déchue 1942",
    "profession": "Ingénieur forestier",
    "languages": "Polonais, italien, allemand, tchèque, russe",
    "registration_date": "9 avril 1946",
    "registration_place": "Bruxelles"
  },
  "translations": {
    "en": {"text": "...", "translator": "claude-opus-4-7+gemini+gpt-consensus", "translated_at": "2026-05-04", "human_reviewed": false},
    "he": {"text": "...", "translator": null, "translated_at": null, "human_reviewed": false},
    "pl": null,
    "fr": {"text": "<original>", "translator": null, "translated_at": null, "human_reviewed": true}
  },
  "related_people": ["david_rapaport"],
  "related_events": ["evt_brussels_registration"],
  "related_places": ["brussels", "nadworna"],
  "status": "active",
  "open_questions": ["Why does this card say Cieszyn? Is it David's own statement, a transcription error, or a deliberate substitution?"]
}
```

**Kinds**: `scan` (image of original), `transcription` (text version), `photo`, `map`, `newspaper`, `report` (research report), `derived` (generated from primary sources)
**Types**: `birth_certificate`, `marriage_certificate`, `death_certificate`, `displaced_persons_card`, `registration_card`, `passport`, `visa`, `newspaper_clipping`, `correspondence`, `research_report`, `oral_history`, `photo_portrait`, `photo_location`, `map`

### 3.5 `family_hypotheses`

```json
{
  "id": "hyp_mosina_location",
  "priority": "HIGH",
  "status": "active_investigation",
  "title": {
    "en": "Where is 'Mosina' — David and Leah's marriage location?",
    "he": "..."
  },
  "context": {
    "en": "Family memoir reports David+Leah married in 'Mosina' in February 1938. Greater Poland Mosina (near Poznań) is ruled out — too far west, no Galician-Jewish presence.",
    "he": "..."
  },
  "candidates": [
    {
      "id": "candidate_morszyn",
      "name": "Morszyn",
      "evidence_for": ["Spa town in Galicia (modern Morshyn, UA)", "Reachable from both Bolechów and Nadwórna", "Jewish community pre-war"],
      "evidence_against": ["No marriage records survive from this location"],
      "confidence": 0.35
    },
    {
      "id": "candidate_muszyna",
      "name": "Muszyna",
      "evidence_for": ["Polish-Slovak border, possible if family was already moving"],
      "evidence_against": ["Far from both birthplaces", "Small Jewish community"],
      "confidence": 0.15
    },
    {
      "id": "candidate_mszana_dolna",
      "name": "Mszana Dolna",
      "evidence_for": ["Closer Polish phonetics to 'Mosina'"],
      "evidence_against": ["West of Carpathians, not the family region"],
      "confidence": 0.15
    },
    {
      "id": "candidate_dolina",
      "name": "Dolina (Leah's mother's hometown)",
      "evidence_for": ["Family connections", "Plausible marriage location at bride's family origin"],
      "evidence_against": ["Memoir explicitly says 'Mosina' not 'Dolina'"],
      "confidence": 0.35
    }
  ],
  "next_steps": [
    "Basia: search Polish marriage registries 1938 for variants of 'Mosina'",
    "Ms. Kasia: cross-check with Lwów district records",
    "Consider commissioning JewishGen Ukraine SIG paid researcher"
  ],
  "related_people": ["david_rapaport", "leah_weitzner"],
  "related_places": ["morszyn", "muszyna", "dolina"],
  "related_events": ["evt_marriage_1938"],
  "verdict": null,
  "created_at": "2026-05-13",
  "updated_at": "2026-05-15"
}
```

**Priority**: `HIGH`, `MEDIUM`, `LOW`
**Status**: `open`, `active_investigation`, `blocked_waiting_archive`, `resolved`, `abandoned`

### 3.6 `family_messages`

```json
{
  "id": "msg_2026-05-15_14-32-08_basia",
  "timestamp": "2026-05-15T14:32:08+02:00",
  "author": "Basia",
  "author_normalized": "basia",
  "body": "Found it! David's birth certificate is in Nadwórna, not Cieszyn...",
  "language_detected": "en",
  "attachment": {
    "filename": "Dawid Mendel Rapaport birth Nadworna 1911.jpg",
    "doc_id": "doc_david_birth_nadworna"
  },
  "mentions_people": ["david_rapaport"],
  "mentions_places": ["nadworna", "cieszyn"],
  "mentions_documents": ["doc_david_birth_nadworna"],
  "tags": ["breakthrough"],
  "thread_id": null
}
```

### 3.7 `family_translations`

```json
{
  "id": "doc_dp_card_p1_he_consensus",
  "doc_id": "doc_dp_card_p1",
  "target_lang": "he",
  "version": "consensus",
  "individual_versions": {
    "claude-opus-4-7": {"text": "...", "ts": "2026-05-20T10:00:00Z"},
    "gemini-2.5-pro": {"text": "...", "ts": "2026-05-20T10:00:00Z"},
    "gpt-4o": {"text": "...", "ts": "2026-05-20T10:00:00Z"}
  },
  "consensus_text": "...",
  "consensus_method": "majority_vote_with_name_preservation",
  "human_reviewed": false,
  "reviewer_uid": null,
  "reviewer_notes": null,
  "diff_resolved": null,
  "cost_usd": 0.08
}
```

Final reviewed version stored at `doc_dp_card_p1_he_final` (separate doc, only created on save from review UI).

### 3.8 `family_users`

```json
{
  "uid": "<firebase_auth_uid>",
  "email": "doron@rpa-port.co.il",
  "display_name": "Doron Rapaport",
  "role": "admin",
  "languages_preferred": ["en", "he"],
  "languages_reviewer": ["he", "en"],
  "added_at": "2026-05-18",
  "added_by": "system",
  "last_login": "..."
}
```

**Roles**: `admin` (Doron only), `reviewer` (can approve translations, edit facts), `researcher` (can add documents/messages, propose facts), `viewer` (read-only — Dov Bernard pre-reveal status)

### 3.9 `family_audit`

```json
{
  "id": "<auto>",
  "ts": "2026-05-18T10:00:00Z",
  "uid": "doron_uid",
  "collection": "family_people",
  "doc_id": "david_rapaport",
  "action": "update",
  "before_hash": "sha256:...",
  "after_hash": "sha256:...",
  "summary": "Added language_proficiency fact, confidence:family_oral"
}
```

Write-once. Never updated, never deleted. Forms the genealogy provenance chain.

### 3.10 `family_i18n`

```json
{
  "id": "he",
  "version": "1.0.0",
  "updated_at": "2026-05-17",
  "strings": {
    "nav.home": "ראשי",
    "nav.tree": "אילן יוחסין",
    "...": "..."
  }
}
```

---

## 4. ID conventions

| Entity | Pattern | Example |
|---|---|---|
| Person | `<firstname>_<lastname>` | `david_rapaport`, `leah_weitzner` |
| Place | `<city_slug>` | `nadworna`, `bolechow`, `lwow` |
| Event | `evt_<descriptor>` | `evt_david_birth`, `evt_brussels_registration` |
| Document | `doc_<descriptor>` | `doc_dp_card_p1`, `doc_david_birth_nadworna` |
| Hypothesis | `hyp_<topic>` | `hyp_mosina_location`, `hyp_leah_dob` |
| Message | `msg_<iso_ts>_<author>` | `msg_2026-05-15_14-32-08_basia` |
| Translation | `<doc_id>_<lang>_<version>` | `doc_dp_card_p1_he_consensus` |
| User | Firebase Auth UID | (auto) |
| Audit | Auto | (auto) |

All slugs: lowercase, ASCII, underscore-separated, transliterate diacritics (Nadwórna → `nadworna`, Bolechów → `bolechow`, Mszana Dolna → `mszana_dolna`).

---

## 5. Indexing requirements (Firestore composite indexes)

| Collection | Fields | Reason |
|---|---|---|
| `family_events` | `date_sort` asc | Timeline view chronology |
| `family_events` | `category` asc, `date_sort` asc | Filtered timeline |
| `family_events` | `place_id` asc, `date_sort` asc | Place-specific timeline |
| `family_documents` | `type` asc, `primary_language` asc | Document grid filters |
| `family_messages` | `timestamp` asc | Chat chronology |
| `family_messages` | `author_normalized` asc, `timestamp` asc | Per-author timeline |
| `family_hypotheses` | `priority` asc, `status` asc | Hypothesis prioritization |
| `family_audit` | `uid` asc, `ts` desc | Per-user audit trail |
| `family_audit` | `collection` asc, `doc_id` asc, `ts` desc | Per-doc audit history |

CC: create via `firebase deploy --only firestore:indexes` after writing `firestore.indexes.json`.

---

## 6. Backup + DR

- Nightly export of `family_*` to GCS bucket `gs://rpa-port-family-backups/` (separate from business backups for clean separation)
- Retention: 90 days rolling + 1 snapshot per quarter retained 5 years
- **One-time frozen snapshot on 1 August 2026** — the gift-time archive. Never deleted.

---

*Schema changes require updating this doc in the same commit.*
