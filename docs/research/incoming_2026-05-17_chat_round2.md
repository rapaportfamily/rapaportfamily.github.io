# Incoming uploads — 17 May 2026 round 2 (CC session-protocol auto-process)

**Trigger**: Doron pushed a new WhatsApp chat export to Downloads (`WhatsApp Chat with Family tree 🌳 (1).zip`, 12.69 MB, 22:16:30 IDT)
**Window covered**: ~17 May 2026 21:00 → 22:45 IDT (~24 new messages from Basia, Doron, Dana, Dalia)
**Per protocol**: `docs/CC_SESSION_PROTOCOL.md` — pull, cross-reference, update, commit.

---

## What changed

| Metric | Before | After | Delta |
|---|---|---|---|
| Total messages | 195 | **219** | +24 |
| Attachments | 39 | **40** | +1 PDF (IPN paper) |
| Active authors today | 6 | 6 | (no new joins) |

## Key new content (cross-referenced against research)

### 1. ⚡ STRONG — Dalia confirms **Lota (David's sister)** existed
> "David had sister lota. i am sure." — דליה רפפורט, 22:41

**Cross-reference**: existing `p_lota` was tagged `family_oral` from Doron alone. Dalia (the primary oral-history holder) now independently confirms — upgrades the certainty even though still oral. People.json updated with `existence_confirmed_by_dalia` fact.

### 2. ⚡ STRONG — Doron confirms David's Betar membership AND departure preference
> "Lucia received and affidavit to go to USA. David as a Betar member wanted to go to Israel." — Doron Rapaport, 22:29

**Cross-reference**:
- Reinforces `h_betar_records` family_oral evidence — though Jabotinsky archive (online portion) returned no Rapaport match (see h_betar_records research round 2).
- NEW fact for Leah: she had a **USA emigration affidavit** — never previously recorded.
- NEW fact for David: explicit **Israel preference** as a Betar member.
- People.json updated for both.

### 3. 🆕 NEW HYPOTHESIS — Document anomaly: Lusia in Poland 1945-46, Dawid in Brussels (separation pattern)
Basia's observation (22:18):
> "In the documents we have from the period they were in Poland (1945-1946), only Lusia is listed, not Dawid. However, in Brussels, there is Dawid, but no Lusia."

This is a NEW research question — never tracked before. Added as **`h_lusia_dawid_paper_separation`** in hypotheses.json with three candidate explanations:
- Separate travel (Leah joined Brussels in time for Dov's 1946 birth)
- Differing intended destinations (USA vs Israel) — couple aligned later
- Records incomplete (less likely — pattern across two systems)

### 4. 🆕 NEW CONTEXT — Soviet "Passportization" in Przemyśl (IPN paper)
Basia attached IPN research paper #6066: *Represje NKWD wobec mieszkańców strefy przygranicznej 1939-1941*. Highlights the section on "Passportization" — the forced Soviet passport campaign in Przemyśl when Leah was there in 1939.

**Cross-reference**: Leah's `przemysl_job` fact in people.json said "Worked as teller / passport section in Przemyśl, 1939 (Soviet-occupied side)" — the IPN paper now provides the **historical mechanism** for what that "passport section" was. Doron confirms her stay was short: *"most of the war she was elsewhere and doing other things to escape"* — Basia confirms the short timing fits the brief passportization window.

People.json updated with a note pointing to the new IPN paper. The h_leah_shimon_survival hypothesis updated with a `round2` research note capturing all of this.

### 5. 🟡 SPECULATIVE — NKVD-adjacency hypothesis for Leah
Basia (22:18, delicately):
> "The issue of Jews in the NKVD is a delicate one... Perhaps Lusia, when she left in 1945, was also fleeing the NKVD? David's declaration of departure – Palestine or the U.S. – may indicate this."

This is a HYPOTHESIS — recorded but **not promoted to fact**. The IPN paper, formal IPN application, and ŻIH testimony will settle this one way or the other.

### 6. 🔁 OPERATIONAL — Basia recommends formal IPN application
Existing hypothesis `h_ipn_application` was MEDIUM priority. With this round 2 evidence (passportization context + document anomaly + Lota's existence + USA affidavit), it should escalate. Doron is the only one who can apply (family member requirement).

---

## Updates committed in this session

| File | Change |
|---|---|
| `source/_chat.txt` (LOCAL ONLY, gitignored) | replaced with new 87,879-byte export |
| `platform/data/messages.json` | re-parsed from new chat — 219 msgs, 40 attachments |
| `platform/assets/documents/represje-nkwd-...pdf` | new IPN research paper added |
| `platform/data/documents.json` | new `doc_ipn_passportization_paper` entry |
| `platform/data/people.json` | p_david: Betar+Israel preference (oral_doron_17may) · p_leah: USA affidavit, Przemyśl IPN context, 1945-46 separation anomaly · p_lota: Dalia confirmation |
| `platform/data/hypotheses.json` | NEW `h_lusia_dawid_paper_separation` · h_leah_shimon_survival round2 research note |

## What I did NOT do (needs human judgment)

- I did NOT upgrade any `family_oral` confidence to `documented` — that requires a primary source, not another oral statement (even a strong one from Dalia). Lota's existence is now `family_oral` corroborated, not `documented`.
- I did NOT translate the IPN paper from Polish — Basia can read it natively; CC can attempt machine translation if useful.
- I did NOT submit the formal IPN application — Doron must do this himself (family member requirement). Recommended next.

---

## Suggested next moves for Doron

1. **Read the IPN passportization paper** (now in `platform/assets/documents/`) — Basia highlighted the relevant section in the original
2. **File the IPN application** — escalated by today's evidence; ~6-month wait so start now
3. **Ask Dalia for any concrete detail about Lota** — full name, dates, last known year, anything that could find her in Yad Vashem testimonies
4. **Check the family's Brussels records** specifically for "Weitzner" or "Cizlik" — Leah may be there under another name
