# DECISIONS FOR DORON — Rapaport Family Tree Platform

> Standing record of decisions Doron has made or needs to make. CC: do not ask Doron the same question twice — check here first. If a decision is needed, add it to "Open" section with options and a recommended default.

---

## Resolved

| # | Question | Resolution | Decided | By | Notes |
|---|---|---|---|---|---|
| D1 | Domain | **`rpa-port.family`** (register .family TLD) | 17 May 2026 | Doron | Use Cloudflare Registrar. Point to Firebase Hosting (rapaport-family site). Add to allowed redirects. |
| D3 | Dov Bernard access timing | **Wait until 28 August 2026** | 17 May 2026 | Doron | Create his Firebase Auth account now, role=viewer, but set `family_users.{uid}.enabled = false`. Flip manually on the morning of his birthday. The platform is a surprise. |
| D5 | Monthly API budget cap | **$30 USD / month hard cap** | 17 May 2026 | Doron | Implement a cost meter (see WO-13 below). Auto-disable LLM endpoints once month spend ≥ $30. Doron's admin UID bypasses the cap for emergencies. |
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
| D10 | How to deploy family Cloud Functions alongside RPA-PORT Python functions in the same Firebase project | (a) Set `"codebase": "family"` in family-tree `firebase.json`; deploy with `firebase deploy --only functions:family` — same project, isolated codebase, no business-code changes (b) Move family `functions/` into `rpa-port-platform/functions-family/` and deploy as a second codebase from RCB repo (c) Separate Firebase project entirely (`rpa-port-family`) for cleanest isolation | **(a)** — minimal change, the `family_*` collection prefix + `ft_*` function prefix + `codebase: "family"` give 3 layers of isolation without touching RCB | Before WO-0 deploy step |
| D11 | Firebase project ID for deployment | (a) `rpa-port-customs` — current live RCB project (memory confirms) (b) `rpa-port-prod` — what `README.md` and `ASSIGNMENT_FOR_CC.md` say (likely a CAI typo) (c) Different project altogether | **(a)** — README needs a one-line fix | Before any `firebase use` |

---

## How CC asks for new decisions

Append to the "Open" section with: question, 2–4 mutually exclusive options, recommended default, and date by which the answer is needed (work backward from gift date). Don't drip — batch. Doron's time budget on this project is **20 minutes/day**.

When a decision is resolved, move the row to "Resolved" with date and a one-sentence implementation note.
