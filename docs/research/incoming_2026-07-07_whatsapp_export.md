# Incoming — WhatsApp export through 7 July 2026 (5th ingest)

**Source**: full "Family tree 🌳" export, range **4 May → 7 July 2026** (855 messages, 216 media files).
Previous ingest stopped at 15 June / 840 messages.
**Ingested by**: CC, 2 August 2026.
**Raw**: `source/whatsapp-2026-08-02/` (gitignored).

Twenty-five messages are new, and all but one cluster falls on a single evening — **7 July**. Every claim below cites the chat date and author. Nothing is invented.

---

## A. The headline: Szabse Rapaport was the rabbi of Dąbrowa Tarnowska

`h_moses_saul_parents` has stood at *open* since 15 June, on the strength of one Tarnów death record (1933/152) naming Mojżesz Rapaport's parents as **Szabse + Ita Feigi**. On 7 July two independent things arrived within minutes of each other.

**Basia, from the archives** (21:40, 21:47):

> "I looked through the records at the notary's office in Tarnów, and they convinced me that Szabse was your ancestor."

She then set out the Dąbrowa Tarnowska rabbinate year by year, 1884–1897, from the records she has been reading:

| Year | Rabbi in Dąbrowa |
|---|---|
| **1884** | **Szabse Rapaport, until 20 April** · Majer Rapaport, from Łuków, from 19 May · Hirsch Weiss, from 19 September |
| 1885–1897 | Hirsz Weiss, then Markus Twerski, then Nuchim Weidenfeld (from ~28 Oct 1897) |

She flags one oddity herself: the 1886 entry has "Hersz Weiss" written over a **crossed-out "Szabsa Rapaport"** — which she reads as the scribe duplicating an earlier line, not as evidence Szabse was still serving.

**Dana, from MyHeritage** (21:38–21:39), the same evening and independently:

> "In Hebrew the translation is schabse and figa/yete and their son yitzhak Haim"

*Figa / Yete* against the *Ita Feigi* of the 1933 death record — the same given names, differently transliterated.

### Why this matters beyond the name

Berisz's 1924 passport application registers his commune as **Dąbrowa Tarnowska**, not Radomyśl and not Nadwórna. That has sat in the file since 23 May flagged as "an unexplained subtlety". It is no longer unexplained: Dąbrowa is where his grandfather had been rabbi. A family's registered commune following its rabbinic seat is ordinary, and the two records now corroborate each other.

**Status moved `open` → `probable_answer`.** Not *resolved*: no document yet names Moses Saul's father outright. Basia's own rule is the right one to hold to here —

> "I've adopted the principle that the original deeds are most important, followed by reliable indexes, and the trees posted online are only helpful… I don't include anything I can't find evidence for, either directly or indirectly."

### New threads this opens

- **Nuchem Weidenfeld**, rabbi in Dąbrowa from 1897, is described by JewishGen as **Szabse's grandson**. Basia is developing that line — and corrects the JewishGen claim that he directly succeeded Szabse: Hirsz Weiss and Markus Twerski came between them.
- **Yitzhak Haim Rapaport**, named in the MyHeritage record as Szabse's son — Dana asks whether he is Moses Saul's brother ("This is his brother so we might relat !!", 21:44). Unestablished.
- **Tablica potomków Abraham Abe Rapaport.pdf** — a descendants table Basia sent at 21:41, not yet read against our tree.

### What was searched and NOT found

- No photograph of Moses Saul or of Szabse. Basia, 22:18: *"I'm sure I didn't find Mosze. I don't think there was a Shabtai from Dabrowa either."*
- Szabse's gravestone carries **a new Hebrew plaque**; Basia has seen the photograph but it is not in our files.
- **Lota — still nothing.** *"the institution is silent; it's the holiday season… I was hoping to ask them about Lotte. Because I don't have anything new here."* She remains the least documented person in the archive.

---

## B. What the export added to the archive itself

**Media**: 115 files we did not hold, now in `platform/assets/documents/` (235 files total).

**Seven previously broken document links are now real files** — records catalogued in June from chat filenames alone, with no scan behind them:

| Document | File now supplied |
|---|---|
| `doc_szymon_paja_marriage_1913_sambor` | `M 1913 Simon Rapaport.jpg`, `U 1912 Lea Rapaport.jpg` |
| `doc_alte_leja_turkel_marriage_1909_tarnopol` | `1909 Akt ślubu…pdf`, `M_1909_…_TP.jpg` |
| `doc_mojzesz_rapaport_death_1933_tarnow` | `Z_1933_Mojżesz Rapaport_T.jpg` |
| `doc_zwi_nussbaum_birth_1919` | `1919 Akt urodzenia Zwi Nussbaum.pdf` |
| `doc_liege_jews_list_1941` | `Szewa Horowitz Liege 1941.pdf` |

That last one matters: it is the 1941 list of Jews in Liège, the document that proves Jente survived.

**Five references remain without a file** — the scans have never been shared:
`Lea and Shimon .pdf` (the ŻIH survivor cards), `U_1920_Szewa Horowitz_T.jpg`,
`Liege Szewa Horowitz marriage.pdf`, `U_1915_Charlotte_Rapaport_1915.png`,
`103378_Krynica_1904_nr_11_PDF.pdf`.

**Other primary material newly in hand**, not previously on disk:

- `1919 Akt ślubu Freida Amalia Rapaport.pdf`, `1920 Akt ślubu Jente Rapaport i Meschulem Horowitz.pdf`, `1923 Akt ślubu Rebeca Rapaport Sane Zylberfenig.pdf` — the three Tarnów sister-marriages, until now known only from Basia's transcriptions
- `Tablica potomków Saul Horowitz.pdf`, `Tablica potomków Abraham Abe Rapaport.pdf` — two new descendant tables
- `Descendant List of Arieh Leib Türkel.docx`, `Descendant List of Moses Rappaport.docx`
- `Meshulam Horowitz Yad Vashem.jpg`, `Yad Vashem Shmuel Rosenfeld.pdf`
- a 31-page numbered scan sequence, `0001-000.jpg` … `0031-000.jpg`, unlabelled in the chat — **needs identifying**

Two Word files arrived with no extension (`DOC-20260602-WA0023/24`); both turned out to be the June state-of-knowledge brief in Polish and English — our own T46/T47 deliverables, shared back into the group. Renamed `.docx` so they open.

---

## Data changes applied

- `messages.json` — 840 → **855**, now through 7 July. Every one of the 222 attachment references resolves to a file on disk (previously 2 did not).
- `documents.json` — `additional_files` 21 → **157**, each described from its own chat message rather than a guess.
- `hypotheses.json` — `h_moses_saul_parents` → `probable_answer`, with the rabbinate evidence, the Dąbrowa explanation and five next steps.
- 115 media files copied into `platform/assets/documents/`.

## Still open after this batch

1. A document naming Moses Saul's father outright — the Dąbrowa rabbinate records are the place to look.
2. Yitzhak Haim Rapaport ≟ Moses Saul's brother.
3. Nuchem Weidenfeld's descent from Szabse.
4. Identify the 31-page scan sequence.
5. Lota Rapaport — a full year of asking, still nothing.
6. The five scans still missing, above.
