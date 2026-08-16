# -*- coding: utf-8 -*-
"""Build the LLM pack — the archive as plain files an LLM can actually read.

WHY. NotebookLM was given the website and produced little, and the reason is structural, not
anybody's fault: its crawler does not execute JavaScript. This site is a single-page app with
hash routing that renders everything client-side out of JSON, so a crawler asking for
/#/story receives an empty shell with a nav bar. Every JS-rendered archive has this problem.
A 581 KB JSON manifest does not fix it either — JSON is for programs; a notebook tool wants
prose.

SO. This writes the whole archive out as flat Markdown, one file per subject plus one
everything-file, with no scripts, no navigation and no JSON. Any tool that can read a text
file can read all of it: NotebookLM, ChatGPT, Claude, Gemini, or a person.

Sizes are printed in words, because the limit that bites in NotebookLM is 500,000 words per
source. Everything here fits inside one source with room to spare.

run:  python scripts/build_llm_pack.py
"""
import io, os, re, sys, json, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'platform')
DATA = os.path.join(SITE, 'data')
OUT = os.path.join(SITE, 'llm')
os.makedirs(OUT, exist_ok=True)
BASE = 'https://rapaportfamily.github.io/'


def load(name, default=None):
    p = os.path.join(DATA, name)
    return json.load(io.open(p, encoding='utf-8')) if os.path.exists(p) else default


people = (load('people.json') or {}).get('people', [])
docs = (load('documents.json') or {}).get('documents', [])
narr = (load('narrative.json') or {}).get('chapters', [])
events = (load('events.json') or {}).get('events', [])
places = (load('places.json') or {}).get('places', [])
hyps = (load('hypotheses.json') or {}).get('hypotheses', [])
memoir = (load('memoir_photographs.json') or {}).get('photographs', [])
trips = load('dov_trips.json') or {}
unid = (load('unidentified_photographs.json') or {}).get('photographs', [])
ext = load('extended_tree.json') or {'counts': {}, 'people': {}}
grif = load('griffel_tree.json') or {'counts': {}, 'people': {}}
by_id = {p['id']: p for p in people}


def en(o, key='en'):
    if isinstance(o, dict):
        return (o.get(key) or o.get('en') or '').strip()
    return (o or '').strip()


def nm(pid):
    p = by_id.get(pid)
    return en((p or {}).get('primary_name')) or pid


def write(name, text):
    p = os.path.join(OUT, name)
    io.open(p, 'w', encoding='utf-8').write(text.rstrip() + '\n')
    return len(text.split())


files = collections.OrderedDict()

# ── 00 start here ───────────────────────────────────────────────────────
files['00-START-HERE.md'] = """# The Rapaport Family Archive — read this first

This folder is the whole archive as plain text. Nothing here needs a browser, a script or a
login. If you are an AI tool: read **99-EVERYTHING.md** and you have all of it in one file.

**Occasion.** Dov Bernard Rapaport turns 80 on 28 August 2026. His family built this archive
as the present.

**The film we want.** 7–10 minutes. The brief with the beat-by-beat structure is
`10-film-brief.md` in this folder.

**The spine.** Dov is eighty and about twenty-eight on the inside. He says repeatedly that he
wishes he could take his mother Lusia back to those places — wheel her there on a gurney if
that is what it took — and have her show him where she lived and how they survived. He cannot.
So the archive did it for him.

## The six rules that govern every sentence

1. Never invent. Every claim must trace to a record in these files.
2. Show conflicts as conflicts. This archive publishes disagreements instead of tidying them.
   They are listed in `08-conflicts-and-open-questions.md`.
3. Lusia's memoir is testimony, not proof. Where documents confirm it, say so. Where nothing
   corroborates it, say so — and say why: the people who would have kept the records are the
   people who were killed. Never call her wrong for lacking paper.
4. Living people: no birth dates.
5. Never put a name on a photograph from `07-pictures.md` marked UNIDENTIFIED.
6. Illustration is allowed but must be visibly marked as illustration.

## The files

| File | What is in it |
|---|---|
| `01-narrative.md` | The story, ten chapters, with the sources under each paragraph |
| `02-the-four.md` | David, Lusia, Shimon, Dov — and the generation before them |
| `03-people.md` | All %d people in the curated core |
| `04-documents.md` | All %d documents: what each one is, what it says, where the scan is |
| `05-timeline.md` | %d dated events |
| `06-places.md` | %d places |
| `07-pictures.md` | Every picture with its caption and its address |
| `08-conflicts-and-open-questions.md` | What the sources disagree about and what nobody knows |
| `09-research-story.md` | Who found what, and how — including where we were wrong |
| `10-film-brief.md` | The film brief |
| `99-EVERYTHING.md` | All of the above in one file |

Images are not embedded here — they are files on the site. Every picture in `07-pictures.md`
carries its full address; open it or download it directly.
""" % (len(people), len(docs), len(events), len(places))

# ── 01 narrative ────────────────────────────────────────────────────────
buf = ['# The story\n',
       'Ten chapters. Each paragraph is followed by the records it rests on.\n']
for i, c in enumerate(narr):
    buf.append('\n## %d. %s  \n*%s*\n' % (i, en(c.get('title')), c.get('years', '')))
    for p in c['paragraphs']:
        buf.append('\n' + en(p['text']) + '\n')
        src = p.get('sources') or []
        if src:
            buf.append('\n> Sources: ' + '; '.join(src) + '\n')
files['01-narrative.md'] = ''.join(buf)

# ── 02 the four ─────────────────────────────────────────────────────────
def person_md(pid, heading='###'):
    p = by_id.get(pid)
    if not p:
        return ''
    b, d = p.get('birth') or {}, p.get('death') or {}
    out = ['\n%s %s\n' % (heading, en(p.get('primary_name')))]
    hebrew = (p.get('primary_name') or {}).get('he')
    if hebrew:
        out.append('\nHebrew name: %s\n' % hebrew)
    if b:
        out.append('\n- Born: %s %s' % (b.get('date') or 'unknown',
                                        b.get('place_id') or b.get('place_name') or ''))
    if d:
        out.append('\n- Died: %s %s' % (d.get('date') or 'unknown',
                                        d.get('place_id') or d.get('place_name') or ''))
    if p.get('photo'):
        out.append('\n- Portrait: %s%s' % (BASE, p['photo']))
    if p.get('note_en'):
        out.append('\n\n%s\n' % p['note_en'])
    for f in p.get('facts') or []:
        v = f.get('value')
        v = en(v) if isinstance(v, dict) else v
        if v:
            out.append('\n**%s** — %s\n' % (f.get('key'), v))
    return ''.join(out)


buf = ['# The four this archive is about — and the generation before them\n']
for pid in ('p_david', 'p_leah', 'p_shimon', 'p_dov_bernard'):
    buf.append(person_md(pid, '##'))
buf.append('\n\n# The generation before\n')
for pid in ('p_berisz', 'p_rebeka', 'p_lota', 'p_lajzor_griffel', 'p_sara_matel_chajes'):
    buf.append(person_md(pid, '##'))
files['02-the-four.md'] = ''.join(buf)

# ── 03 people ───────────────────────────────────────────────────────────
buf = ['# Everybody in the curated core (%d people)\n' % len(people),
       '\nThe wider trees hold far more: %d Rapaports across %d families, and %d Griffels '
       'across %d families. Those are separate research and live in the site’s tree files.\n'
       % (ext['counts'].get('people', 0), ext['counts'].get('families', 0),
          grif['counts'].get('people', 0), grif['counts'].get('families', 0))]
for p in sorted(people, key=lambda x: ((x.get('birth') or {}).get('date') or '9999')):
    b, d = p.get('birth') or {}, p.get('death') or {}
    line = '\n- **%s**' % en(p.get('primary_name'))
    if b.get('date') or d.get('date'):
        line += ' (%s–%s)' % ((b.get('date') or '?')[:10], (d.get('date') or '')[:10])
    if b.get('place_id') or b.get('place_name'):
        line += ', born %s' % (b.get('place_id') or b.get('place_name'))
    if p.get('photo'):
        line += ' · portrait: %s%s' % (BASE, p['photo'])
    buf.append(line)
files['03-people.md'] = ''.join(buf)

# ── 04 documents ────────────────────────────────────────────────────────
buf = ['# The documents (%d)\n' % len(docs),
       '\nEach entry says what the document is, what it tells us, who it concerns, and where '
       'the scan is. A film should name and explain every document it shows.\n']
for d in sorted(docs, key=lambda x: x['type']):
    buf.append('\n\n## %s\n' % en(d.get('title')))
    buf.append('\n- Type: %s' % d.get('type'))
    if d.get('source_archive'):
        buf.append('\n- Source: %s' % d['source_archive'])
    if d.get('related_people'):
        buf.append('\n- People: %s' % ', '.join(nm(x) for x in d['related_people']))
    for f in d.get('file_pages') or []:
        buf.append('\n- Scan: %sassets/documents/%s' % (BASE, f))
    for u in d.get('external_urls') or []:
        buf.append('\n- Online: %s' % u)
    df = d.get('decoded_fields') or {}
    if df:
        buf.append('\n- What it records: ' + '; '.join(
            '%s = %s' % (k, v) for k, v in list(df.items())[:14] if not isinstance(v, list)))
    s = en(d.get('summary'))
    if s:
        buf.append('\n\n%s\n' % s)
    for q in d.get('open_questions') or []:
        buf.append('\n> Open question: %s\n' % en(q))
files['04-documents.md'] = ''.join(buf)

# ── 05 timeline ─────────────────────────────────────────────────────────
buf = ['# Timeline (%d events)\n' % len(events)]
for e in sorted(events, key=lambda x: str(x.get('date') or x.get('year') or '')):
    when = e.get('date') or e.get('year') or '?'
    buf.append('\n- **%s** — %s' % (when, en(e.get('title')) or en(e.get('label'))))
    if en(e.get('description')):
        buf.append(': %s' % en(e.get('description')))
files['05-timeline.md'] = ''.join(buf)

# ── 06 places ───────────────────────────────────────────────────────────
buf = ['# Places (%d)\n' % len(places)]
for pl in places:
    buf.append('\n\n## %s\n' % (en(pl.get('name')) or pl.get('id')))
    if en(pl.get('note')) or pl.get('note_en'):
        buf.append('\n%s\n' % (en(pl.get('note')) or pl.get('note_en')))
    for k in ('images', 'photos', 'period_images'):
        for im in pl.get(k) or []:
            f = im.get('file') if isinstance(im, dict) else im
            if f:
                buf.append('\n- Picture: %s%s' % (BASE, f))
files['06-places.md'] = ''.join(buf)

# ── 07 pictures ─────────────────────────────────────────────────────────
buf = ['# Every picture, with its address\n',
       '\nDownload any of these directly. **Never put a name on anything marked UNIDENTIFIED.**\n']
buf.append('\n## The memoir plates (%d) — printed inside Lusia’s own book\n' % len(memoir))
for ph in memoir:
    cap = ph.get('caption_as_printed') or {}
    buf.append('\n- %s%s' % (BASE, ph.get('file', '')))
    if cap.get('he'):
        buf.append('  \n  Caption as printed (Hebrew): %s' % cap['he'])
    if en(cap):
        buf.append('  \n  Translation: %s' % en(cap))
    if en(ph.get('note')):
        buf.append('  \n  Note: %s' % en(ph.get('note')))

buf.append('\n\n## Portraits of named people (%d)\n'
           % sum(1 for p in people if p.get('photo')))
for p in people:
    if p.get('photo'):
        buf.append('\n- %s — %s%s' % (en(p.get('primary_name')), BASE, p['photo']))
        if en(p.get('photo_caption')):
            buf.append('  \n  %s' % en(p.get('photo_caption')))

buf.append('\n\n## Dov’s four journeys back (%d photographs)\n'
           % len(trips.get('photographs') or []))
for a in trips.get('albums') or []:
    shots = [s for s in trips.get('photographs', []) if s['album'] == a['key']]
    buf.append('\n\n### %s — %s (%d)\n' % (en(a.get('title')), a.get('when'), len(shots)))
    buf.append('\n%s\n' % en(a.get('note')))
    for s in shots:
        buf.append('\n- %s%s' % (BASE, s['file']))

buf.append('\n\n## UNIDENTIFIED — nobody knows who these are (%d)\n' % len(unid))
buf.append('\nFrom Jacob’s archive, most from a folder he keeps as "Photobook2". '
           'They may be shown; they must never be captioned with a name.\n')
for s in unid:
    buf.append('\n- %s%s' % (BASE, s['file']))

buf.append('\n\n## The two family libraries\n')
buf.append('\nThousands more scans sit in these folders, named by person id. Browse the site '
           'if you need them:\n')
for label, sub, cnt in (('Basia — Rapaport side', 'basia_2026_08', ext['counts'].get('media_files', 0)),
                        ('Jacob — Griffel side', 'griffel_2026_08', grif['counts'].get('media_files', 0))):
    buf.append('\n- **%s** — about %d files: photographs, civil registers, Yad Vashem pages, '
               'papers. %sassets/documents/%s/' % (label, cnt, BASE, sub))
files['07-pictures.md'] = ''.join(buf)

# ── 08 conflicts and questions ──────────────────────────────────────────
buf = ['# What the sources disagree about, and what nobody knows\n',
       '\nThis archive publishes disagreements rather than resolving them quietly. A film '
       'should show them as disagreements. **The open questions below are questions, not '
       'findings — a film that answers them invents history.**\n',
       '\n## Conflicts\n',
       '\n- **Berish’s death.** The Auschwitz Museum victim record and the camp’s own '
       'Sterbebücher both say 29 March 1942. The Yad Vashem page David filed in 1953 says 1940. '
       'Both are published.',
       '\n- **Rebeka.** This archive holds born 1888, died 1942. Her Yad Vashem page says 1892 '
       'and 1943. Jacob’s tree says "1942?" — with the question mark. All three stand.',
       '\n- **Lotte.** Born 27 September 1915 per both family trees; 1914 per her Yad Vashem '
       'page. Her first cousin Charlotte Horowitz was born 21 November 1914 in the same city. '
       'Do not merge them: the parents named on the page settle it.',
       '\n- **David’s birthplace.** Nadwórna per the birth certificate found in Warsaw; '
       '"Cieszyn/Tesin" on the 1946 Brussels DP card, most likely a clerk mishearing.',
       '\n- **A birth register filed 1849** where this archive holds 1850.',
       '\n\n## Open questions (%d)\n' % len(hyps)]
for h in hyps:
    q = en(h.get('question')) or en(h.get('title')) or en(h.get('statement'))
    if q:
        buf.append('\n- %s' % q)
        if h.get('status'):
            buf.append('  *(%s)*' % h['status'])
files['08-conflicts-and-open-questions.md'] = ''.join(buf)

# ── 09 research story ───────────────────────────────────────────────────
files['09-research-story.md'] = """# How this was found — and where we were wrong

The archive began with one memoir. Lusia wrote her life down. Everything else was found.

**Basia**, a genealogist in Poland, rebuilt the Rapaport line back to Abraham Abe, born 1784 at
Tarnów. On 5 August 2026 she sent the tree as a GEDCOM — 1,442 people, 480 families — and
mentioned in passing that the printed version is five metres long. On 6 August she sent her
entire media library: 1,072 files, 1.1 GB.

**Jacob** sent the other side of the house — the GRIFFEL line, David's mother's family, 390
people and 569 files. Not one of his files appears in Basia's. Two researchers, two families,
meeting at one woman: Rebeka Griffel. Because of him, David's maternal grandparents have names
for the first time: Lajzor Griffel, born 26 March 1850 at Nadwórna, and Sara Matel Chajes, born
5 March 1851, who lived into the first year of the occupation.

**Ms. Kasia** at the Jewish Historical Institute in Warsaw found David's birth certificate in
Nadwórna on 15 May 2026, correcting a birthplace a Brussels clerk had misheard in 1946.

**The open internet** did the rest. The Auschwitz-Birkenau Memorial's own database confirmed
Berish's prisoner number and death date at source — and its transport page gave us something
nobody had: transport 689 was fifty-five men **from the prison at Tarnów**, so he was not seized
in Przemyśl and sent east; he was held in the town his family came from.

## Where we were wrong

This matters as much as what we found.

- The archive stated for months that **no Page of Testimony had ever been filed** for Berish or
  Rebeka, and that it was their only memorial anywhere. Both pages were sitting in its own
  document list the whole time. Worse and better: **David filed them himself**, from Haifa, on
  26 April 1953 — three of them, for his father, his mother and his sister Lotte, signing each
  in the relationship line as *his son, her son, her brother*.
- A 1924 certificate was filed as belonging to "a different family" because a second page in
  the same record was a different man's birth entry. The certificate itself names *Mendel 12
  lat, Lotte 8 lat* — David and his sister. Reopened, with both readings kept.
- Two Charlottes, born in Vienna a year apart, first cousins, were nearly merged into one.

## What is still missing

Two things, and the site names them both: `Photobook2.pdf`, whose 47 pages are already
published one by one, and *"Lea and Shimon .pdf"*, a document catalogued from correspondence
whose scan has never reached us.
"""

# ── 10 film brief (copied from the site's own brief) ────────────────────
brief_path = os.path.join(SITE, 'docs', 'FILM_BRIEF.md')
files['10-film-brief.md'] = (io.open(brief_path, encoding='utf-8').read()
                             if os.path.exists(brief_path)
                             else '# Film brief\n\nSee https://rapaportfamily.github.io/docs/FILM_BRIEF.md\n')

# ── write, then the everything file ─────────────────────────────────────
counts = collections.OrderedDict()
for name, text in files.items():
    counts[name] = write(name, text)

everything = ['# THE RAPAPORT FAMILY ARCHIVE — EVERYTHING IN ONE FILE\n',
              '\nGenerated 11 August 2026 from https://rapaportfamily.github.io\n',
              '\nIf you can only read one file, read this one.\n']
for name, text in files.items():
    everything.append('\n\n\n<!-- ===== %s ===== -->\n\n' % name)
    everything.append(text)
counts['99-EVERYTHING.md'] = write('99-EVERYTHING.md', ''.join(everything))

# llms.txt — the emerging convention for pointing an LLM at a site's plain text
LLMS = """# The Rapaport Family Archive

> A researched family archive for Dov Bernard Rapaport's 80th birthday, 28 August 2026.
> The website is a JavaScript app and crawlers cannot read it. These files are the archive in
> plain text.

## Read this first
- [Start here](@/llm/00-START-HERE.md): the rules and what each file holds
- [Everything in one file](@/llm/99-EVERYTHING.md): the whole archive, one document

## By subject
- [The story, ten chapters](@/llm/01-narrative.md)
- [The four, and the generation before](@/llm/02-the-four.md)
- [All people](@/llm/03-people.md)
- [All documents](@/llm/04-documents.md)
- [Timeline](@/llm/05-timeline.md)
- [Places](@/llm/06-places.md)
- [Every picture with its address](@/llm/07-pictures.md)
- [Conflicts and open questions](@/llm/08-conflicts-and-open-questions.md)
- [How it was researched, and where we were wrong](@/llm/09-research-story.md)
- [The film brief](@/llm/10-film-brief.md)

## Machine-readable
- [Full manifest, JSON](@/data/film_manifest.json)
"""
# Counting %s placeholders by hand is how the first attempt failed - one more link than
# arguments. A plain replace cannot miscount.
write('llms.txt', LLMS.replace('@/', BASE))

print('LLM pack written to platform/llm/\n')
total = 0
for name, w in counts.items():
    size = os.path.getsize(os.path.join(OUT, name)) / 1024.0
    print('  %-38s %7d words  %7.0f KB' % (name, w, size))
    if name != '99-EVERYTHING.md':
        total += w
print('\n  %-38s %7d words (the limit that bites in NotebookLM is 500,000 per source)'
      % ('TOTAL, excluding the combined file', total))
