# Incoming uploads processed — 2026-06-01 (autonomous CC session)

> Per `docs/CC_SESSION_PROTOCOL.md`. CC pulled all `family_uploads` from Firestore, found **7 uploads** still flagged `status: pending` (Gemini auto-verification had run on some, errored on others, but none had been marked `cc_processed`). All seven are processed below. Compiled by Dalia, Dana, Daniel & Doron Rapaport's research assistant (CC).

**Doctrine reminder**: David Mendel & Leah (Lusia) Rapaport were **Holocaust survivors**. The CKŻP cards below are post-war survivor-registration documents — testimony to their survival, not records of any wrongdoing. No invented facts; every claim is sourced or labelled.

---

## Headline finding

The single most valuable item was hiding behind a Gemini error. The upload **"Lea and Shimon .pdf"** had failed Gemini auto-verification with a `RECITATION` block, so it sat unprocessed. Read directly, it turned out to be the **two long-awaited CKŻP (Central Committee of Polish Jews) survivor-registration cards** that Basia had been requesting from Warsaw — the subject of hypothesis `h_zip_documents` (previously `blocked_waiting_archive`).

Both cards are *"Karta informacyjna o osobach ocalałych"* (information card on survivors), Wydział Ewidencji i Statystyki, **filed at the Katowice committee on 1 July 1946**:

| Card | Person | Born | Place | Parents | Last address |
|---|---|---|---|---|---|
| Nr **151738** (red 3564) | Lusia Rappoport | **8.4.1916** | **Bolechów** | Eljan, Matylda | Katowice |
| Nr **151337** (red 2665) | Szymon Rappoport | **22.6.1937** | **Lwów** | Dawid, Lusia | Katowice |

Provenance is sound: the CKŻP Records & Statistics Department compiled ~280,000–300,000 such cards across Poland 1944–47, primarily to reunite families; the central file has been held at the **Emanuel Ringelblum Jewish Historical Institute (ŻIH), Warsaw** since 1951 (EHRI; USHMM). Upper-Silesian sub-committees (Katowice, Gliwice, Bielsko-Biała) were major repatriation/Bricha staging points in 1946.

### What this resolves / changes

1. **`h_zip_documents` → RESOLVED.** The cards are in hand.
2. **`h_leah_dob` → probable_answer.** Lusia's *own* card gives **8 April 1916, Bolechów** (parents Eljan/Matylda). The **day + month (8 April)** are now unanimous across every source. The **year** is 1916 in three independent later sources (this CKŻP card + ŻIH index + Haifa Chevra Kadisha) versus the single 1913 Bolechów civil birth certificate. Caution kept: age-understatement at marriage would actually favour 1913, so the year is not declared finally settled. See `h_leah_dob_2026-06-01.md`.
3. **Shimon's birthplace corrected to Lwów.** The legible card states field 3 = born 22.6.1937 in **Lwów**, *not* "Mosina" as family memory held. `p_shimon.birth.place_id` changed `pl_mosina_disputed → pl_lwow`. **TENSION FLAGGED FOR DORON:** a June-1937 Lwów birth predates the February-1938 Muszyna marriage in Lusia's memoir — the marriage date (1935 vs 1938) and Shimon's birthplace need reconciling.
4. **`h_lusia_dawid_paper_separation` strengthened.** Both cards place **mother + son together in Katowice on 1 July 1946** — the predicted "Lusia in Polish records, registered with CKŻP" leg, now documented. Since Dov was born in Brussels later in 1946, their westward Bricha leg falls in the **second half of 1946**.

Data updated: new document `doc_lea_ckzp`; `doc_szymon_ckzp` re-described with the legible Lwów/Katowice details; `p_leah` and `p_shimon` birth blocks; hypotheses `h_leah_dob`, `h_zip_documents`, `h_lusia_dawid_paper_separation`, `h_mosina_location`.

---

## All 7 uploads — disposition

### 1. `aYoirGSgaPvA18H9qSAm` — "Lea and Shimon .pdf" (Daniel) — **the two CKŻP cards**
- **Gemini status**: `error` — "Candidate was blocked due to RECITATION". Processed by CC directly.
- **Action**: documented as `doc_lea_ckzp` (new) + `doc_szymon_ckzp` (updated). See headline above.
- **Recommended status**: `cc_processed` → Doron to approve.

### 2. `4hFR7pAuFl3lYDTJjQWN` — "Griffel Chajes family Nadworna indexes.png" (Daniel)
- **Gemini status**: `done`. A **JRI-Poland index** screenshot for Griffel/Chajes of Nadwórna.
- **Extracted (documented)**: Nadwórna Jewish vital-record funds confirmed — **births 1877-1896 = Sygnatura 941**, **deaths 1877-1896 = Sygnatura 946**. Griffel children indexed (Süssel/Zissel 1878, Schaje 1883, Simcie 1890; infant deaths Rechil 1883, Simcie 1891). A cluster of **Chajes** children with mother "Sura CHAJES" appears in Sygnatura 941 — a broader Chajes presence in Nadwórna.
- **Cross-reference**: the Griffel family is already richly documented in the tree via Edward Gelles (`src_gelles_griffel_nadworna_pdf`); this index **adds the archival signatures** that source those entries. Advances `h_griffel_chajes_family`.
- **Recommended status**: `cc_processed`.

### 3. `ElUEJykulI1sHqenTTKU` — "Gmail - ODP_ Dawid Rapaport i Lusia Weitzner.PDF" (Daniel)
- **Gemini status**: `error` (503 high demand). Processed by CC via text extraction.
- **What it is**: email thread between **Barbara Sieińska**, the **JHI/ŻIH Jewish Genealogy & Family Heritage Center** (Katarzyna), and Doron, 18–19 May 2026.
- **Extracted (documented)**: JHI **confirmed the family tree is genuine** ("confirmation of the accuracy of the material from the source"). New details: **Leizor (Eliezer) Griffel was a *Schaechter* (shochet / ritual slaughterer) and a Hausbesitzer (house-owner) in Kolomyia**, at least in the 1880s; there were **two men named Lajzor Griffel** (father "senior" + son) in the industrial registers; the **Leizor × Sara Chajes marriage record** exists ("S 1892 ... Nadwórna"); **Rechel and Simcie** are two Griffel children who **died in childhood** and are absent from the tree. Birth-record *akta* list (all Nadwórna): Machla 1873, Dawid 1875, stillborn 1877, Zissel 1878, Eisig Chaim 1879, Rachel 1881, Chaja 1883, Leibisch 1885, Beniamin 1887, Rebeca 1888.
- **NEW LEAD (hypothesis)**: Barbara — *"I believe the sawmill in Mosina we are looking for belonged to the Griffels, but I still need to sort out the materials."* First link between the "Mosina" place mystery and the Griffel family.
- **Recommended status**: `cc_processed`. Advances `h_griffel_chajes_family` + `h_mosina_location`.

### 4. `KPmyxEBTxjwGBrRVJMjE` — "Facets of my Family History. Part 2.pdf" (Daniel)
- **Gemini status**: `error` (503). Processed by CC via text extraction.
- **What it is**: **Edward Gelles, *Facets of my Family History*, Part 2 (chapters 13–20)** — full text of the canonical source already cited as `src_gelles_griffel_nadworna_pdf`. Chapter 13 "Some Griffel cousins" + chapter 14 "The Chayes family" confirm the 10-children list (incl. "Rivka Griffel b.1888 m. Berish Rapaport") and the Chajes rabbinic descent (Taz / Bach lineage).
- **Action**: no new entities needed (already in tree); the upload is the primary text underpinning the existing Griffel/Chajes data.
- **Recommended status**: `cc_processed`.

### 5. `3eXByT1gs9KM3YTdFunc` — "Family tree from Rapaport institute" (IMG-...WA0006.jpg, Daniel)
- **Gemini status**: `done`. A partial Rapaport family tree from an online genealogical compilation ("Rapaport institute" — likely Geni/WikiTree-style).
- **Useful (later generations)**: David d. 29 Aug 1990 + Leah d. 1996 at 111 Hanasi Blvd, Haifa; David's roles "Manager / Customs broker"; Shimon journalist/PR, m. Tamar **Bugin** 17 Apr 1967 Tel Aviv; Dov b. 28 Aug 1946, Customs Broker, m. **Dalya Goldfish** (b.1952) 16 Jan 1974 Haifa. *Most of these are already in the tree, often in richer form (e.g. David's death already has cemetery/grave/Chevra-Kadisha detail).*
- **Contradictions (NOT accepted)**: the tree's PATERNAL deep ancestry and birthplaces ("Mosina" near Poznań; David's father "Dov #19288"; Leah born "Stanislavov"; marriage "1935 Mosina") contradict the documented Nadwórna paternal line and Bolechów. Treated as an unreliable third-party compilation. Note: its claimed Dov-marriage "16 Jan 1974 Haifa" also conflicts with the **Ketubah** (upload #6) which gives **16 May 1975 Brussels** — flagged for Doron.
- **Recommended status**: `cc_processed` with the contradictions logged, not merged.

### 6. `J6umO2vWJO5b1prLSU0O` — "Wedding certificate Dalia and Dov" (IMG-...WA0001.jpg, Daniel)
- **Gemini status**: `done`. The **Ketubah** of Dov & Dalia.
- **Extracted (documented)**: Dov's Hebrew name **Dov ben Menachem David**; David Mendel's Hebrew name includes **Menachem** (with *z"l* — deceased by 1975, consistent with his 1990 death... note: *z"l* here simply marks the father's name form); Dalia's father **Dov Yosef**; married **Sivan 6, 5735 = 16 May 1975, in Brussels**. (Internal quirk: the Ketubah says "on Shabbat" but Sivan 6 5735 was a Friday — minor.)
- **Recommended status**: `cc_processed`. Optional future: add Hebrew names to `p_dov_bernard` / `p_david` (deferred — living-person / honoree data; left for Doron to confirm).

### 7. `9Iq5Fay0GhuCJVkZ8sr8` — "Screenshot ... Chrome.jpg" / "פרסום הלויה של סבא דויד בעיתון" (Dana)
- **Gemini status**: `parse_error` (empty). Processed by CC directly.
- **What it is**: a National Library of Israel (nli.org.il) screenshot of **Ma'ariv, 30 August 1990, page 12** — the death-notice page, with multiple "דוד רפפורט" memorial notices. Corroborates David's death **29 August 1990** (already documented via Haifa Chevra Kadisha).
- **Recommended status**: `cc_processed`. Could be added as a press source confirming the death date.

---

## Items flagged for Doron

1. **Shimon born Lwów (June 1937) vs Muszyna marriage (Feb 1938)** — please help reconcile the marriage date and Shimon's birthplace/order of events.
2. **Dov & Dalia marriage**: Ketubah = 16 May 1975 Brussels; the online tree said 16 Jan 1974 Haifa. Which is correct (civil vs religious; or one is an error)?
3. **Leah's birth year** 1913 vs 1916 — the civil record says 1913; three later records say 1916. Do you have any family document that settles the year?
4. Optional: file a **Page of Testimony** for Rebeka Griffel-Rapaport (none on record — noted previously).

## Tool/limits notes
- Web search found **no open-web corroboration** of the Griffel "Mosina sawmill" lead (only modern sawmills surfaced); Galician timber/industrial registers are gated — Barbara's archive work is the path.
- The two PDFs that errored on Gemini with **503 / RECITATION** are a recurring pattern: the auto-verifier silently drops archival documents. Recommend a manual CC pass on any upload whose `gemini_verification.status != "done"`.
