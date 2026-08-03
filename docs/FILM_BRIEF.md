# Notes for whoever makes the film

Written 3 August 2026, for a future model or filmmaker working from this archive.
Read this before you write a line of script.

---

## THE ONE RULE

**Everything in this archive is marked for how well it is known. Keep those marks.**

A story about the Shoah that invents detail does harm, because the invented detail is exactly what
a denier will later point at. This family's archive was built on a hard rule — every claim names
its source, or is labelled testimony, or is labelled unresolved — and the rule survived several
occasions when breaking it would have made a better sentence.

The machine-readable version of that rule:

| Marking in the data | What you may do with it |
|---|---|
| `confidence: confirmed` | State it. A document says so. |
| `confidence: documented` | State it, with the source named on screen if it carries weight. |
| `confidence: family_oral` | Attribute it. "Lusia said…", not "It happened that…" |
| `kind: testimony` (in `narrative.json`) | This is memoir only. No document corroborates it. Show it as remembered, not as filmed fact. |
| `kind: conflict` | The sources disagree. **Do not resolve it for the audience.** The disagreement is part of the story. |

If you need a scene that the evidence does not support, invent it openly — a title card, a
different visual grammar, an acknowledged reconstruction. Do not smuggle it in.

---

## WHERE THE MATERIAL IS

| File | What it holds |
|---|---|
| `platform/data/narrative.json` | **Start here.** Nine chapters, 23 paragraphs, four languages, every paragraph carrying its source and a `kind` marker. This is the spine. |
| `platform/data/events.json` | 45 dated events, 1888–2026, each with confidence and sources |
| `platform/data/journey.json` | The migration route as legs, with per-person tracks and coordinates — Nadwórna → Muszyna → Lwów → Katowice → Brussels → Sète → Cyprus → Atlit → Haifa |
| `platform/data/people.json` | 124 people, with facts, confidence levels, and two portraits |
| `platform/data/documents.json` | 57 curated documents with transcriptions and decoded fields |
| `platform/data/memoir_pages.json` | Lusia's ninety pages, the primary voice |
| `platform/data/research_center.json` | 157 cards — how each thing was found, including the failures |
| `docs/research/` | The raw ingest notes, in date order |

**Do not use `memoir_timeline_verified.json` as verification.** It is named misleadingly and there
is a `_warning` at the top of the file explaining why.

---

## THE STORY, AS IT ACTUALLY RUNS

Nine chapters, in `narrative.json`. The shape is not a rise or a fall; it is **a family taken
apart and reassembled two continents away, with two separations in the middle that nobody in the
family ever described.**

1. **Radomyśl Wielki** — a paternal line that was a dead end for a year, cracked in May 2026 by a
   passport application found in an archive.
2. **Nadwórna, 1911** — David is born. The town is half Jewish. It will be emptied.
3. **Bolechów** — Lusia is born. In 1933 her parents leave for Palestine and she stays. *She will
   not see them for fifteen years.*
4. **The marriage, 1935** — and Shimon, born Lwów 1937.
5. **The war** — the ghetto, the wooden wagon, false identities, a three-year-old kept in a crate
   for two and a half years. **Almost none of this has a document. Almost nobody who could have
   written it down survived.**
6. **Katowice, 1946** — and the first separation.
7. **Brussels, 1946** — Dov is born.
8. **Sète, the Theodor Herzl, Cyprus, 1947** — and the second separation.
9. **Haifa** — reunion, forty more years, two graves side by side.

### The two separations — this is your third act structure

Neither is in the memoir. Both come from reading two documents against each other, which nobody had
done until August 2026.

**First:** David was registered as a Displaced Person in **Brussels on 9 April 1946**. Lusia and
Shimon filed survivor cards at **Katowice on 1 July 1946** — three months later, still in Poland.
He went ahead. The memoir says only *"the family reaches Brussels and stays in a hotel."*

**Second:** In April 1947 David and nine-year-old Shimon sail from Sète and are captured and
interned in Cyprus. Lusia is left in Brussels with a seven-month-old baby, and waits **more than a
year**. The Haifa burial register records her year of immigration as 1948 and his as 1946 — the
separation is written into their own graves.

**The baby is Dov. The film is being made for his eightieth birthday.**

---

## MOMENTS THAT ARE ALREADY CINEMA

Each of these is documented. None is invented.

- **The wrong town.** David's Brussels DP card says he was born in "Cieszyn" — four hundred
  kilometres from Nadwórna. A French clerk misheard. *Here the document is wrong and the family's
  memory is right*, which is the thesis of the whole archive in one line.
- **The crate.** Shimon, three years old, kept in a box for two and a half years so he would not be
  seen or heard. He grew up to be a journalist. Testimony only.
- **The wedding that was three years earlier than anyone remembered.** The memoir says Muszyna,
  February 1938. The register says Bolechów, 10 February 1935. And the register *repairs* the
  memoir: under her date, Shimon is born eight months before his parents marry.
- **A school assignment.** In 1986 a granddaughter, Hadas, asked her teacher for help with
  homework. The teacher, Esther Weiss, sat down and interviewed Lusia. **Ninety pages.** Without
  that homework, this entire film has no first act.
- **The last page matches the first.** Lusia's burial record names her father Eliyahu and her
  mother Matilda — the same two people her memoir opens with, sixty years earlier, in another
  language.
- **Two cousins, one year.** Yehudit Shlomit born Haifa, 25 April 1946. Dov born Brussels, 28
  August 1946. Four months and one sea apart, while Dov's father was behind wire in Cyprus. In June
  2026 she got in touch: she had been looking for this branch of the family for years.
- **A son names his father.** In 1996, filling in a government form, Zwi Nussbaum wrote his
  father's name — Eliahu Mordechai — seventy-seven years after the man died. Until August 2026 this
  archive did not know it.
- **No Page of Testimony.** Berisz and Rebeka were murdered and **nobody ever filed a memorial page
  for them at Yad Vashem.** David and Lusia lived forty-five years after the war and did not do it.
  This archive is their only written memorial anywhere in the world. *That is your ending, or your
  opening.*

---

## WHAT YOU MAY NOT SAY

- **Do not resolve Leah's birth year.** 1913 in the civil register; 1916 on her own survivor card,
  the ŻIH index and the burial register. Unresolved, and the family was asked.
- **Do not resolve Zwi's birthplace.** He said Tarnów twice, in 1945 and 1996. The birth register
  says Przemyśl. A clerk noted "1919 only acc. to ppt".
- **Do not claim Isak Goldfischer as family.** A 2026 research pass called him a "USHMM-confirmed
  relative" on the strength of a shared surname and town. He was removed. He is a stranger unless a
  document says otherwise.
- **Do not date the deaths of Berisz and Rebeka precisely.** Berisz is associated with Auschwitz
  victim number 188161; that reading has been sent to the Arolsen Archives for confirmation and has
  not come back.
- **Do not put words in Dov's mouth.** He is alive, he is the reason this exists, and nobody has
  interviewed him for it.

---

## THE VISUAL MATERIAL THAT EXISTS

- **Twelve period photographs** of the actual towns, in `platform/assets/research_images/period/` —
  Nadwórna's market square in 1928 and its town centre in 1932, the railway station, Bolechów in
  1915, Muszyna over the Poprad, Krynica's pump room, Tarnów, Famagusta 1945, a Haganah ship at
  Haifa in 1947. All public domain, all captioned with date and archive.
- **Lwów from the town hall, 1942–45** — the Jewish quarter destroyed, only the roofless Meforshei
  ha-Yam synagogue standing. *This is the city they were hiding in, photographed while they were in
  it.*
- **Two portraits**, cropped from a 1945 citizenship application: Zwi Nussbaum and Inge née
  Rosenbusch. Identity-document photographs, sepia, small.
- **The documents themselves** — the DP card, the CKŻP cards, the Tarnów marriage deeds, the
  ketubah, the 31-page citizenship file, the burial register.
- **What does not exist:** no photograph of Moses Saul or of Szabse has been found, and the search
  for one is recorded as a failure rather than left open. No wartime photographs of David, Lusia or
  Shimon are held here.

---

## THE VOICE

The archive's own register is plain, specific, and unsentimental — it lets the facts carry the
weight, because they do. Numbers are used exactly: 53,510 Jews behind wire in Cyprus, 2,641 aboard
the Theodor Herzl, 2,000 children born in the camps, ninety pages, graves 102ד and 102ג.

Two sentences from the archive that set the tone:

> "These are not weak claims. They are the parts of a life that no clerk was ever going to write
> down, and for most of them no clerk survives who could have."

> "The last page of the record matches the first page of the testimony."

---

## STILL OPEN, IF YOU ARE MAKING THIS LATER

Some of these may have been answered after August 2026. Check the Research Center before assuming.

- The Arolsen Archives inquiry for David, Lea, Szymon, Berisz and Rebeka — drafted, not yet sent
- The German compensation (BEG) files — David and Lusia went to West Berlin around 1958 and were
  paid; the file should exist and would be the largest body of their own testimony anywhere
- Dov's Brussels birth registration — only he can request it
- Shimon's Ma'ariv bylines, in the JPress newspaper archive
- Leah's birth year
- Five document references with no file behind them
