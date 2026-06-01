# CC research — 2026-06-01 — Radomyśl + Edward Gelles + research-tool notes

After the WhatsApp-export ingest, I went looking for things Basia hasn't (yet) surfaced. Below is what I genuinely added, what I tried and got blocked on, and concrete next-step URLs for Doron / Basia.

---

## 1. NEW FACT — Moses Saul Rapaport on the Radomyśl Wielki Board of Trustees (1897-1905)

The JewishGen-hosted Radomyśl Wielki Yizkor Book, **Part I**, page text contains a single mention of the family in a community-leadership listing:

> "**Moshe Rappaport** served as a community leader (Board of Trustees) during 1897-1900 and again 1901-1905."

Source: [Radomysl Wielki Yizkor Book Part I, JewishGen](https://www.jewishgen.org/yizkor/radomysl/Rad002.html).

**Interpretation** (with the user's no-guessing rule):

- This Moshe Rappaport is almost-certainly our Moses Saul Rapaport, because:
  1. The descendants tree (Basia's 31 May 2026 chart) and the Yad Vashem PoT both name Berisz's father as Moses / Moshe Rapaport.
  2. Berisz was born in Radomyśl Wielki 1886, and his siblings 1882-1896 — meaning the father was head-of-household in that town across exactly the years 1897-1905.
  3. The Yizkor calls him a community leader; the descendants tree calls him *kupiec* (merchant) — both consistent with a well-established Jewish merchant heading the local community board.

- It is **possible** there was a different Moshe Rappaport on the board, so this is "very likely" not "verified" — added to `p_moses_saul_rapaport.facts` with `confidence: documented` and source `src_radomysl_yizkor_book_part_1`.

---

## 2. Confirmation that Edward Gelles's "Griffel of Nadworna" is the underlying source

I fetched the actual PDF from Balliol College Oxford archives:
[Griffel of Nadworna — Edward Gelles 2006, expanded 2020](http://archives.balliol.ox.ac.uk/Modern%20Papers/gelles/Griffel%20of%20Nadworna.pdf)

The document is a tabular pedigree. Entry #8 of the 10 children of Eliezer Griffel × Sarah Matel Chajes reads:

> "8 Rivka Griffel (b. 1888) m. Berish Rapaport"

That's the full Gelles entry — no parents for Berish, no dates, no places. Which is why Basia's discovery of Berisz's parents (Moses Saul + Menukha) and birthplace (Radomyśl Wielki 1886) is a genuine extension of the published record.

Other useful details from Gelles's pedigree (corroborates our other data):

- Eliezer "Zeida" Griffel: **1850 – 1918**
- Sarah Matel Chajes: **d. 1940**
- Eldest son Dawid Mendel Griffel: **1875 – 1941** m. Chawa Wahl (1877-1941)
- Edward Gelles's own mother **Regina Gelles née Griffel** (1900–1954) was Dawid Mendel's daughter, so a first cousin of David Memek Rapaport.
- Yehuda Nir (1930-2014, NYC), Pinhas Heyn, Joshua Blau (Hebrew U professor, b.1919), Clara Blau-Heyn (Hebrew U Botany, 1924-1998) are all also Griffel descendants — distant cousins of David Memek.

---

## 3. Searches that did NOT yield new facts (worth recording so we don't redo them)

| Target | Source attempted | Result |
|---|---|---|
| Berisz in Radomyśl Wielki Yizkor Part II | jewishgen.org/yizkor/radomysl/Rad005.html | not mentioned (Part II covers Holocaust survival stories only) |
| Berisz/Rebeka in Radomyśl post-war address list | Rad001.html | not present (consistent — they were murdered; David emigrated) |
| Rapaport on Radomyśl KehilaLinks page | jewishgen.org/kolbuszowa/radomysl wielki/radomysl1.html | not mentioned by name |
| Rapaport in Borowa 1929 directory | jewishgen.org/kolbuszowa/radomysl wielki/Borowa2.html | not present (Borowa is a different nearby town; Berisz had moved to Stanisławów by 1918) |
| Bernard Rapaport in Polish business directory 1929 | Google search | not found via search — would need direct JRI-Poland database query |
| Zwi Ayalon Nussbaum Israeli records | Google + various Israeli genealogy sites | no direct profile found |
| Turkel Tribe direct fetch | turkel.org.il | site exists ([confirmed link](http://turkel.org.il/GED2WWW/index.htm)) but my fetcher gets cert errors; a browser would work |
| Auschwitz Museum victim record #188161 | victims.auschwitz.org/victims/188161 | cert error; URL is in `doc_auschwitz_victim_188161` for browser access |
| Yad Vashem name database for our extended family | collections.yadvashem.org | cert errors throughout; needs browser |

---

## 4. The Turkel Tribe family tree exists (lead for Alte Leja's descendants)

The Vienna-based Turkel family — into which Alte Leja Rapaport married c.1907 — has a dedicated family-history website at **turkel.org.il** (last update 2025, registration form closed 2006, run by a Turkel-family descendant in Israel).

URLs (browser-accessible, my fetcher couldn't reach them due to SSL cert age):
- Index of names: http://turkel.org.il/GED2WWW/index.htm
- Dynamic family tree: http://turkel.org.il/DFT/index.html
- Advanced search: http://turkel.org.il/search.htm
- Email contacts: http://turkel.org.il/Links-em.htm
- Guestbook: http://turkel.org.il/geobook.html

Per a Google snippet of the site: *"The genealogy documents Turkels living in Podole/Galicia near Lwów (Lemberg) during the 19th century… moved to Vienna at the turn of the century."* That fits — Alte Leja (b.1882 Radomyśl Wielki) married into the Vienna-based Turkels, and her children Hertha Noa, Lotte, Israel Menachem, Mordechai (Max), Rachel/Rosie, Siegfried, Chana were all born or raised in Vienna addresses (Auersperggasse 9 and Rembrandtstrasse 3 per Basia's descendants tree).

**Action for Doron / Dana**: open turkel.org.il in a normal browser and search "Rapaport" + "Radomysl". If anyone there has the Alte Leja branch documented, that's the first cousin network of David Memek on his father's side.

---

## 5. Highest-leverage next-step targets for Basia / Doron

These are the items I tried and got blocked on by SSL/auth issues. They should be straightforward in a browser:

1. **victims.auschwitz.org/victims/188161** — get Berisz's actual Auschwitz arrival date, camp number, fate, and source documents.
2. **victims.auschwitz.org/transports/689** — see the full transport list (who was deported with Berisz, where it left from). This may reveal whether Rebecca was on the same transport.
3. **Yad Vashem Central Database** [collections.yadvashem.org/en/names](https://collections.yadvashem.org/en/names) — search surname "Rapaport" + place "Radomyśl Wielki" AND surname "Nussbaum" + place "Przemyśl". Likely additional PoTs for Berisz's siblings (Alte Leja, Jente, Freida Amalia) and Freida Amalia's children Michael & Rachel Rosenfeld.
4. **DÖW (Austrian Documentation Centre of Austrian Resistance)** [doew.at](https://www.doew.at) — search "Turkel" + Vienna. Their Shoah-Opfer database has 64,619 entries. Should find Israel Menachem Turkel (d.1942 Lviv) and Siegfried Turkl (d.1945 Belgium) at minimum.
5. **Kazerne Dossin (Belgian Holocaust memorial)** [kazernedossin.eu/en](https://kazernedossin.eu/en) — search "Turkl" + "Turkel" — Siegfried Turkl died in Belgium on 12 January 1945; he must be in their victim list.
6. **JRI-Poland Tarnów index** — Basia probably has account access; search "Moshe Saul Rapaport" against the Tarnów cemetery JOWBR transcription. The descendants tree mentioned two Moshe Saul Rapaport tombstones (one d.11/08/1933, one d.30/10/1931 from Dąbrowa).
7. **Edward Gelles "An Ancient Lineage" (2006), chapters 12-17 ("My mother's Family")** — full chapters about the Griffel line. Worth ordering or finding scanned PDF; not currently on Balliol's open archive (only "Facets" papers are public).

---

## 6. Suggestion for the live family-tree app

Since several research-note insights aren't yet visible on the SPA, consider adding a "Research notes" or "Discovery log" page that surfaces these markdown files. Otherwise Dalia/Dana/Daniel only see the cleaned data on the tree but can't follow the reasoning chain.
