# DECISIONS FOR DORON — Rapaport Family Tree Platform

> Standing record of decisions Doron has made or needs to make. CC: do not ask Doron the same question twice — check here first. If a decision is needed, add it to "Open" section with options and a recommended default.

---

## Resolved

| # | Question | Resolution | Decided | By | Notes |
|---|---|---|---|---|---|
| D1 | Domain | **`rpa-port.family`** (register .family TLD) | 17 May 2026 | Doron | Use Cloudflare Registrar. Point to Firebase Hosting (rapaport-family site). Add to allowed redirects. |
| D3 | Dov Bernard access timing | **Wait until 28 August 2026** | 17 May 2026 | Doron | Create his Firebase Auth account now, role=viewer, but set `family_users.{uid}.enabled = false`. Flip manually on the morning of his birthday. The platform is a surprise. |
| D5 | Monthly API budget cap | **$30 USD / month hard cap** | 17 May 2026 | Doron | Implement a cost meter (see WO-13 below). Auto-disable LLM endpoints once month spend ≥ $30. Doron's admin UID bypasses the cap for emergencies. |
| D10 | Family Cloud Functions deployment | **(c) Separate Firebase project entirely** | 17 May 2026 | Doron | Totally separated from RPA-PORT business. New Firebase project `rapaport-family` (or similar). No shared rules, no shared functions, no shared collections — full hard isolation. Native app possible after screens are done. |
| TARGET | Reveal date | **28 August 2026** (Dov Bernard's 80th birthday) | 17 May 2026 | Doron | Frozen snapshot must be taken before this date. |

---

## Open

| # | Question | Options | Recommended default | Needed by |
|---|---|---|---|---|
| D2 | Translation reviewers besides Doron | (a) Dalia HE + Basia PL + Kasia FR (b) Doron only (c) other combo | (a) | Before WO-3 ships |
| D4 | Photo provenance audit | (a) Treat all `source/` photos as private until cleared (b) Allow Basia/Kasia photos based on WhatsApp consent (c) Ask each researcher individually | (a) | Before any public visibility |
| D6 | Commission paid Lwów-archive researcher for "Mosina" mystery | (a) Yes via JewishGen Ukraine SIG ~$200–400 (b) No — wait for Basia (c) Decide in June | (c) | End of May |
| D7 | Physical deliverables for the party | (a) A2 framed tree poster only (b) A2 + printed photo book (c) A2 + book + 5-min MP4 reveal video | (b) | Order by 1 August |
| D8 | Public visibility after 28 Aug | (a) Stay private (family-only) forever (b) Open to extended Rapaport cousins via Rapaport Research Institute graph (c) Open public-read, signed-in for editing | (a), revisit in September | After reveal |
| D9 | Backup retention | (a) 90 days rolling + quarterly snapshots 5y (b) Forever (it's family heritage) (c) Custom | (b) for the frozen 1 Aug snapshot, (a) for live data | Before first deploy |
<!-- D10 resolved (c), see Resolved table. D11 obsoleted by D10 — new project, not rpa-port-customs. -->
| D12 | Documents storage strategy | (a) Firebase Hosting static (current — 30 files committed to git) (b) Firestore-as-link store (file metadata in `family_documents`, files in Cloud Storage, URLs in Firestore) — matches "links from Firestore" pattern used elsewhere | **(b)** per Doron's direction "links can be from Firestore as we did for other things" | Before WO-2 |
| D13 | Native app | (a) Web-only forever (b) Add native app (React Native / Capacitor) after screens done — defer until after Aug 28 reveal | **(a) until reveal, then (b)** per Doron "we can even make an app after we finish the screens" | After 28 Aug 2026 |

---

## How CC asks for new decisions

Append to the "Open" section with: question, 2–4 mutually exclusive options, recommended default, and date by which the answer is needed (work backward from gift date). Don't drip — batch. Doron's time budget on this project is **20 minutes/day**.

When a decision is resolved, move the row to "Resolved" with date and a one-sentence implementation note.
