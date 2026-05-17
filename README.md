# Rapaport Family Tree

> A multilingual research and presentation platform tracing the journey of David and Leah Rapaport — Holocaust survivors who reached Brussels in 1946 — built as an 80th-birthday gift for their son Dov Bernard, 28 August 2026.

**Compiled by**: Dalia, Dana, Daniel & Doron Rapaport (equal partners)
**Status**: In development. Foundation built; Firebase migration in progress.
**Languages**: Hebrew (primary), English, Polish, French — RTL-aware throughout.

---

## What this is

A private genealogy platform for the Rapaport family research circle:

- 22 people across 5 generations, with multilingual names and full source citations
- 30 primary documents (birth certificates, the Brussels DP card, CKŻP cards, research reports)
- A timeline from 1888 to 2026
- 14 places with their historical names per period (Nadwórna → Надвірна, Bolechów → Болехів)
- 195 WhatsApp messages from the active research circle, structured and searchable
- 11 open hypotheses with candidate solutions, evidence pro/con, and next steps

The whole thing speaks four languages and flips to RTL when you choose Hebrew. The data is sourced — every claim traces to a document or a message; nothing is invented.

## Architecture

| Layer | Tech |
|---|---|
| Front-end | Vanilla JS SPA, no build step (Crimson Pro / Heebo / Inter via Google Fonts) |
| Hosting | Firebase Hosting (same project as RPA-PORT, separate site) |
| Database | Firestore, `family_*` collection namespace |
| Functions | Cloud Functions, Node 20, `ft_*` prefix |
| Auth | Firebase Auth + custom claims (`family: true`, role-based) |
| AI | 3-AI consensus (Claude opus-4-7 + Gemini 2.5 Pro + GPT-4o) for translation |
| Maps | Leaflet + OpenStreetMap |

**Privacy boundary**: family data lives in the same Firebase project as Doron's customs business but is hard-isolated by Firestore rules — business UIDs cannot read or write any `family_*` collection.

## Repo layout

```
rapaport-family-tree/
├── platform/              # Static SPA (Firebase Hosting public dir)
│   ├── index.html
│   ├── assets/
│   │   ├── css/style.css
│   │   ├── js/app.js
│   │   └── documents/      # 37 source documents (PDFs, JPGs)
│   └── data/               # JSON seed data (migrated to Firestore in WO-1)
│       ├── people.json
│       ├── places.json
│       ├── events.json
│       ├── documents.json
│       ├── hypotheses.json
│       ├── messages.json
│       └── i18n/{en,he,pl,fr}.json
├── functions/             # Cloud Functions
│   ├── index.js
│   └── package.json
├── scripts/
│   ├── parse_whatsapp.py        # WhatsApp export → messages.json
│   └── migrate_to_firestore.py  # JSON → family_* collections
├── docs/
│   ├── ASSIGNMENT_FOR_CC.md     # Work orders for Claude Code
│   ├── RESEARCH_LOG.md          # What is known, confirmed, open
│   └── DATA_MODEL.md            # Schema reference
├── firebase.json
├── firestore.rules
├── firestore.indexes.json
└── README.md
```

## Quick start (local)

```bash
# Static dev server (no Firebase needed)
cd platform
python3 -m http.server 8123
# → open http://localhost:8123

# Firebase emulator suite (after WO-1 migration)
firebase emulators:start
# → Firestore: localhost:8080, Functions: 5001, Hosting: 5000
```

## Deployment

```bash
# Bootstrap (one-time)
firebase login
firebase use rpa-port-prod
firebase target:apply hosting rapaport-family <site-id>

# Migrate seed data to Firestore (idempotent)
python3 scripts/migrate_to_firestore.py --project rpa-port-prod --confirm

# Deploy
firebase deploy --only hosting:rapaport-family,firestore:rules,firestore:indexes,functions
```

## The research circle

| Name | Role |
|---|---|
| Doron Rapaport | Family lead, builder |
| Dalia Rapaport | Mother, primary oral-history source |
| Dov Bernard Rapaport | The subject — Doron's father, born Brussels 1946 |
| Dana & Daniel Rapaport | Doron's siblings |
| Magda | Connector |
| Basia | Polish genealogist (lead field researcher) |
| Kasia | French-language expert (Brussels records) |
| Ms. Kasia at ŻIH Warsaw | Found David's true birthplace, 15 May 2026 |

## Doctrine

1. **Hebrew is the primary delivery language.** Build for RTL first.
2. **Never invent facts.** Every claim cites a `source_id` or carries `confidence: hypothesis`.
3. **3-AI consensus** for any text shown to a human reader.
4. **Elimination is king.** Before accepting a hypothesis, list what would have to be false for it to hold.

## Next steps

See `docs/ASSIGNMENT_FOR_CC.md` for the 13 prioritized work orders.

## License

Private. Not for redistribution. Photos and documents may have third-party rights — do not republish without source clearance.
