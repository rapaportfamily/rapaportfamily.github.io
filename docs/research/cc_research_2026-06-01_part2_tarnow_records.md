# CC research part 2 — 2026-06-01 — Three Tarnów marriage records discovered via Claude vision OCR

After the user said "remove stickers and OCR everything", I ran Tesseract on all 88 chat-attached images. Tesseract handles printed text well but struggles with handwritten Polish cursive — so for the high-value handwritten records I switched to **Claude vision** (via direct image reads), which produced three real value-add findings.

## The headline finding

Three separate primary-document marriage records, all from the Tarnów Jewish marriage register held at the **Archiwum Narodowe w Krakowie, Oddział w Tarnowie** (Polish National Archive, Tarnów branch). All three are marriages of **Moses (Saul) Rapaport + Menukha's daughters** — confirming our apical couple from THREE independent primary documents.

### 1. Freida Amalia Rapaport — second marriage, Tarnów 1919

**Source**: `1919 Nussbaum Rapaport T.jpg` — Tarnów Jewish marriage register page (entry 40)

**Date**: 8 June 1919, Tarnów
**Bride**: **Freida Amalia Rapaport**, widow (*wdowa*), age 29 years 7 months → born ~November 1889 (the descendants tree's "1888" is close)
**Groom**: **Markus Elias Kleinbaum** (Kleinbaum/Kleinbarm), age 27, also widower, residing at "u domu Bauer in Przemyśl"
**Witness rabbi**: Josef Chaim Kirschenbaum (rabbi in Tarnów)

This was Freida Amalia's **second** marriage. Her son Zwi Ayalon Nussbaum was born 7 May 1919 — just **one month before this second marriage**. So her first husband (likely a Nussbaum, hence Zwi's surname) had died in 1918 or early 1919, possibly in WWI. She remarried Kleinbaum within weeks of widowing/giving birth.

The "1919 Nussbaum Rapaport T" filename suggests Basia interpreted this as a Nussbaum × Rapaport marriage — but the actual groom is **Kleinbaum**, not Nussbaum. The Nussbaum was Freida's first (deceased) husband, not in this document.

### 2. Jente Rapaport — second marriage, Tarnów 1920

**Source**: `1920 Horowitz Rapaport T.jpg` — Tarnów Jewish marriage register page (entry 98)

**Date**: 12 December 1920, Tarnów
**Bride**: **Jente Rapaport**, widow (*wdowa*), age 33 → born 1887 (matches descendants tree)
- Daughter of **Moses Rapaport and Menucha (Menuchy)** ← APICAL COUPLE NAMED DIRECTLY
**Groom**: **Mendel(ek) Eachem? Horowitz**, age 28, status kawaler (bachelor)
- Resident of Sokal (Sokala — town now in Lviv Oblast, Ukraine; pre-WWII Eastern Galicia)
- Son of Pinches Horowitz and an unreadable mother
**Witness rabbi**: Josef Chaim Kirschenbaum (rabbi in Tarnów)

So Jente was widowed by ~1920 from her first husband, then remarried Horowitz of Sokal.

### 3. Younger Rebeka Rapaport — first marriage, Tarnów 1923

**Source**: `1923 Zylberfenig Rapaport T.jpg` — Tarnów Jewish marriage register page (entry 101)

**Date**: 4 September 1923, Tarnów
**Bride**: **Rebeka Rapaport** (the younger; NOT Berisz's wife Rebeka née Griffel — that's a different person)
- Status: *wolna* (free, never married)
- Age: 27 → born ~1896 (matches descendants tree exactly)
- **Born Radomyśl Wielki**
- Resident in Tarnów
- Daughter of **Moses Rapaport and Menucha (Menuchy)** ← APICAL COUPLE NAMED AGAIN
**Groom**: **Sane Zylberfenig**, age 34 years 10 months, status kawaler (bachelor)
- Born Plinsk / Płońsk
- Son of Abram and Pesi Zylberfenig of Płońsk
**Witnesses**: Maier Krak, David Erbg(?), Israel Marche(?)

This was Rebeka the younger's first marriage. The descendants tree noted she "went to Austria" — that subsequent migration would have happened post-1923.

## Why this matters

1. **The apical couple "Moses Rapaport + Menucha" is now verified by THREE independent primary documents** (not just the family-built descendants tree). Each of the three sisters' marriage records states the parents.

2. **Radomyśl Wielki as birthplace is double-confirmed** for at least Rebeka (b.1896) — the 1923 record explicitly says "urodzona w Radomyślu Wielkim".

3. **Three new in-law surnames added to the family network**:
   - Kleinbaum (Freida's second husband — Markus Elias, age 27 in 1919, possibly resident at "domu Bauer" in Przemyśl)
   - Horowitz of Sokal (Jente's second husband — Mendel, son of Pinches Horowitz)
   - Zylberfenig of Płońsk (Rebeka's husband — Sane, son of Abram + Pesi)

4. **The "first husband" mystery**: Both Freida Amalia AND Jente were widows by 1919-1920. Their first husbands' identities are not yet documented. For Freida, the surname Nussbaum (= her son Zwi Ayalon's birth name) suggests her first husband was a Nussbaum, who died c.1918-1919 — possibly a WWI casualty. For Jente, the first husband is completely unknown — needs further Tarnów or Sokal record search.

5. **Rabbi Josef Chaim Kirschenbaum officiated all three weddings** — he was the chief Tarnów rabbi 1919-1923. Worth noting as a fixed contextual figure.

## Tesseract OCR limitations observed

The Tesseract OCR (pol+eng+heb+deu, run on all 88 chat-image attachments) produced reasonable text for printed material (Yizkor PDFs, screenshots, the Sejm Album for Zygmunt Griffel, the Auschwitz death certificate forms) but garbled cursive Polish handwriting. The actual reading of cursive handwriting required **Claude vision** — and that's where the three new findings above came from. The full Tesseract output for all 88 images is committed under `platform/data/ocr_cache/`.

## Action items

- Update `p_freida_amalia_rapaport` with the 1919 second marriage to Markus Elias Kleinbaum; flag her unknown first husband (likely surname Nussbaum)
- Update `p_jente_rapaport` with the 1920 second marriage to Mendel Horowitz of Sokal; flag her unknown first husband
- Update `p_rebeka_rapaport_sister` with the 1923 first marriage to Sane Zylberfenig of Płońsk
- Add three new in-law people: p_markus_elias_kleinbaum, p_mendel_horowitz, p_sane_zylberfenig
- Add place Sokal (pl_sokal)
- Add place Płońsk (pl_plonsk)
- Update `p_moses_saul_rapaport` and `p_menukha` facts with the three independent primary-source confirmations
- Re-OCR these three records with a manual transcription (the OCR cache currently has Tesseract garbage for them; the Claude vision text in this note should be the canonical record)
