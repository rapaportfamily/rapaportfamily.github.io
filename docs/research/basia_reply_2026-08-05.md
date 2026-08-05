# Reply to Basia — 5 August 2026

**Draft for Doron to send (WhatsApp from now on, per Basia's note).**
Her message covered six points; this answers each, and answers the one question she actually
asked — point 5.

**The one thing to ask for above all else: a GEDCOM export.** See §6.

---

## Draft

Dear Basia,

Thank you — and no apology needed for the size of it. Five metres is not absurd, it is the answer.

**1. Mrs Maniewska.** Thank you for chasing it. I am not expecting much either, and there is no
hurry. So that the question is ready and narrow whenever she returns: what we want to know is
whether **Lota Rapaport, married name Szmid**, appears anywhere in the Ładoś material as a victim
of the forged-passport fraud. My grandmother's memoir (page 41) says Lota and her husband bought a
forged document certifying them as United States residents, for $10,000, in the Lwów ghetto in
1942–43, and that the sellers informed on them to the Gestapo. Both were arrested and never
returned. **No Page of Testimony was ever filed for her, anywhere** — not Yad Vashem, not USHMM,
not JewishGen, not Bełżec. If Mrs Maniewska has nothing, that is still worth knowing, and I will
record it as a closed question rather than an open one.

**2. The A0 boards.** Yes — please. My father's eightieth birthday is **28 August**, so a printed
board is not just documentation, it is the gift. If you have to choose one line to prepare first,
make it the direct line down to my father, Dov Bernard. I will handle printing here in Israel.

**3. The Lurie Legacy overlaps.** Thank you, I will study them. One thing I will ask in advance,
because it is how this archive is built: where those trees reach back to Davidic descent, I mark it
as **tradition** rather than as documented descent, and keep it clearly separated from the lines we
can put a record behind. It is not scepticism about the work — it is so that the documented part
cannot be weakened by association if someone later challenges the traditional part.

**4. Griffel.** Good. Rebeka née Griffel is my great-grandmother, so that line matters as much as
the Rapaport one.

**5. Your question — Luś's siblings' descendants. No, I have not contacted them, and here is
exactly where I stand, in case it helps you place people.**

Lusia had three siblings, all of whom emigrated with their parents around 1933:

- **Feige (Tzipora)** — married **Israel Englard** (correctly Englard, not Englander), born 26 June
  1905 in Przeworsk, son of Kiwe and Rebeka; they married in Bolechów in 1932. **Children: Ruth and
  Akiva.**
- **Moses (Mojżesz)** — born 1916 Bolechów. **No descendants recorded at all.**
- **Pnina** — known only by her Hebrew name. Probably born 1917–1920; the Bolechów birth register
  stops on 5 May 1918, which likely explains why no record of her has been found. **No descendants
  recorded.**

Two new things since we last spoke, both of which touch your Weitzner/Weinreb line:

- **A photograph in the memoir names one of them.** On page 65 there is a picture of my father and
  his brother Shimon with a cousin, and the printed caption names him: **"Akiva Eldar"**. Eldar is
  very likely the Hebraised form of Englard — which would make him Feige's son — but I have not
  proved that and I am not recording it as fact yet.
- **A Weitzner from Bolechów I cannot place.** Searching the USHMM database for surname Weitzner
  with birthplace Bolechów returns exactly one person in the entire database: **WEITZNER, BASIE**,
  in a record set called *"[Particulars of Illegal Immigrants]"*, collection RG-17, Illegal
  Immigration to Palestine. No birth date is shown. She is not Lusia — Lusia came legally, on the
  ship *Kedma*, in 1948. **Does a Basie fit anywhere in the Weitzner tree you have built?** I am
  requesting the scanned document from USHMM to get her parents' names.

**6. What to send, and in which format.** All of it, please — but if you can add one thing that is
not on your list, it is worth more than the rest:

> **A GEDCOM export from Ahnenblatt.** In the program: *File → Export → GEDCOM*.

The reason is practical. The PDFs and the edited charts are for people to read, and I want those
too. But a GEDCOM carries every person, every date and every source **as data**, so it merges into
our archive with the sources still attached, instead of being re-typed by hand out of a picture —
which is how mistakes enter a family tree. So: the GEDCOM first, then the HTML website version, the
A0 chart PDFs, and the source-file directories. The `.ahn` base files too, if they are easy to zip.

**And on your husband's diagnosis of the photographs — he is right, and it is the paths.**
Ahnenblatt does not store pictures inside the file; it stores the *location* of each picture on the
disk. Move the photos, rename a folder, or send the file to someone else's computer, and every link
breaks while the tree itself looks perfectly fine. Two things fix it permanently:

1. Keep every photograph in **one folder sitting beside the `.ahn` file**, and set Ahnenblatt to
   use **relative paths** rather than absolute ones (it is an option in the program settings).
2. When you send anything to me, **zip the whole directory** — the `.ahn` file and the picture
   folder together, with their structure intact. Then the links survive the journey.

Please thank him from me. And thank you — my father turns eighty on the 28th, and none of this
would exist without your work.

With warm regards,
Doron

---

## Notes for me, not for Basia

- **Attachments did not arrive** in what was forwarded to me — the test A0 board, the marked-up
  Lurie trees, and the Weitzner working version are all referenced but not present. Ask Doron to
  push them through WhatsApp.
- **The real prize is the GEDCOM.** Everything else she listed is human-readable output. A GEDCOM
  is machine-readable and can be diffed against `people.json` — 124 people here against a five-metre
  tree there. That comparison is where new names come from.
- **Do not ingest a GEDCOM blindly.** House rule stands: her confidence is not our confidence. Merge
  as `documented` only where a source is attached, otherwise `family_oral` or `hypothesis`.
- **The Davidic-descent point matters.** *The Lurie Legacy* traces to Rashi and onward to Davidic
  descent. Keep at `tradition`, exactly as the Rapaport-Kohen priestly lineage is kept.
