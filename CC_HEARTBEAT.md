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
