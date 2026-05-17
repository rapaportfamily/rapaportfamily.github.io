# CC Heartbeat — Rapaport Family Tree

> Updated by Claude Code at the end of every session. Mirror of `rpa-port-platform/CC_HEARTBEAT.md` protocol.

---

## Session 0 — Bootstrap handoff
**Date**: 17 May 2026
**Author**: CAI (web Claude)
**Status**: Foundation delivered, CC has not yet started.

### What CAI delivered in this handoff package
- Working static SPA (9 views, 4 languages, RTL Hebrew)
- 22 people, 14 places, 20 events, 30 documents, 11 hypotheses, 195 messages — structured and seeded
- Firebase scaffolding: `firebase.json`, `firestore.rules`, `firestore.indexes.json`
- Cloud Functions stub at `functions/index.js`
- Migration script at `scripts/migrate_to_firestore.py`
- Three docs: `ASSIGNMENT_FOR_CC.md`, `RESEARCH_LOG.md`, `DATA_MODEL.md`

### What CC starts with (WO-0)
1. Create repo `doronrpa-hub/rapaport-family-tree`
2. Initial commit of this package
3. `firebase init` against existing rpa-port project (Firestore, Functions, Hosting:rapaport-family)
4. Deploy hosting-only to verify routing
5. Update this file with session 1 entry

### Blockers awaiting Doron's decision
See `docs/DECISIONS_FOR_DORON.md`.

**Resolved 17 May 2026 (same day as handoff):**
- D1 — Domain: `rpa-port.family` (register .family TLD via Cloudflare Registrar)
- D3 — Dov Bernard access: wait until 28 Aug 2026 (his 80th birthday). Create account now with `enabled: false`.
- D5 — Monthly API cap: $30 USD/month hard cap. WO-13 enforces.

**Target reveal: 28 August 2026.**

Open decisions: D2 (other reviewers), D4 (photo provenance), D6 (paid Lwów researcher), D7 (physical deliverables), D8 (post-reveal visibility), D9 (backup retention).

### Cost so far
$0 — all built in CAI conversation. CC's first work order should also be near-zero (just deployment).

---

<!-- CC: append new session entries below this line. Format:

## Session N — <topic>
**Date**: <iso>
**WOs touched**: WO-X, WO-Y
**What got done**:
- ...
**Evidence (screenshots / Firestore queries / commits)**:
- commit abc1234
**Next session**:
- ...
**Decisions needed from Doron**:
- ...
**Cost this session**: $X.XX

-->

## Session 1 — WO-0 bootstrap (repo + initial commit + audit)
**Date**: 2026-05-17
**WOs touched**: WO-0
**Author**: CC (home PC, Opus 4.7)

**What got done**:
- Created private repo `doronrpa-hub/rapaport-family-tree` via `gh repo create`
- Extracted both handoff zips (`rapaport-family-tree.zip` + `rapaport-handoff-docs.zip`), merged into flat repo root (stripped `familytree/` wrapper)
- Initial commit + push to `main` — 67 files, includes 30 source-document scans (~13 MB)
- Audited the handoff against `rpa-port-platform/firebase.json` — found 2 blocking issues for Doron (D10, D11)

**Evidence**:
- Repo: https://github.com/doronrpa-hub/rapaport-family-tree
- Initial commit pushed cleanly (`git push -u origin main` succeeded, branch tracking set)
- Working tree: `C:\Users\User\rapaport-family-tree\` (on Doron's home PC)

**WO-0 status — what I could NOT do autonomously, needs Doron**:
| Step | Why blocked |
|---|---|
| `firebase init` against rpa-port project | Interactive prompts (`firebase login`, project picker); also overwrites existing `firebase.json` |
| Create hosting site `rapaport-family` | `firebase hosting:sites:create rapaport-family` — Doron needs to run from a logged-in shell |
| Deploy hosting-only to verify routing | Depends on the two above |
| Apply Firestore rules to live project | Per warning in `firestore.rules` lines 104-111, family rules must be MERGED into `rpa-port-platform/firestore.rules` before deploy — deploying this file standalone leaves business collections rule-less. See D11. |
| Custom domain `rpa-port.family` | Cloudflare Registrar work — Doron's account |

**Commands Doron should run from `rpa-port-platform/` shell** (after resolving D10 + D11):
```bash
# (1) Confirm project ID
firebase use rpa-port-customs    # NOT rpa-port-prod (README typo, see D11)

# (2) Create the hosting site
firebase hosting:sites:create rapaport-family
firebase target:apply hosting rapaport-family rapaport-family

# (3) Deploy hosting only (from rapaport-family-tree/ working dir)
cd C:\Users\User\rapaport-family-tree
firebase deploy --only hosting:rapaport-family
```

**Next session (WO-0 wrap + WO-1)**:
- After Doron unblocks D10/D11: verify hosting URL serves the SPA correctly in 4 languages with RTL flip
- Begin WO-1: complete `scripts/migrate_to_firestore.py` and run idempotent migration of the 7 JSON seed files to `family_*` collections
- Wire a one-shot test against Firebase emulator before touching prod

**Decisions needed from Doron**: D10, D11 added to `docs/DECISIONS_FOR_DORON.md` (functions codebase collision; project ID typo confirmation)

**Cost this session**: $0.00 — no LLM API calls; only file ops, `gh` API, and git pushes.
