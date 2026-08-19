# -*- coding: utf-8 -*-
"""Build the film pack PDF — text AND pictures in one source.

WHY THIS EXISTS. The Markdown pack solved half the problem. NotebookLM imports Markdown text
correctly, but its own documentation is explicit: images are NOT imported from Markdown
sources, and image URLs written in Markdown are not displayed. PDF sources, by contrast,
support both text and images. NotebookLM's Video Overview builds its slides from what it can
see in the sources — so a film made from the Markdown alone would carry this family's story
with none of this family's faces in it.

So this writes one PDF that carries the narrative, the documents and the pictures together,
each picture captioned with what it is, who is in it and where it came from. That is the file
to upload to any notebook or video tool.

ENGLISH ONLY, on purpose. Embedding Hebrew in a generated PDF needs a bidirectional layout
engine and an RTL-capable font, and a half-rendered Hebrew caption in a memorial film is worse
than none. The Hebrew lives on the site and in the Markdown pack, and this file says so.

run:  python scripts/build_film_pdf.py
"""
import io, os, re, sys, json, textwrap
import fitz

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'platform')
DATA = os.path.join(SITE, 'data')
OUT = os.path.join(SITE, 'llm', 'RAPAPORT-FILM-PACK.pdf')

W, H, M = 595, 842, 48                      # A4 portrait, 48pt margins
FS, LH = 9.5, 13.0
MAXPX, QUAL = 1100, 72


def load(n, d=None):
    p = os.path.join(DATA, n)
    return json.load(io.open(p, encoding='utf-8')) if os.path.exists(p) else d


people = (load('people.json') or {}).get('people', [])
docs = (load('documents.json') or {}).get('documents', [])
narr = (load('narrative.json') or {}).get('chapters', [])
memoir = (load('memoir_photographs.json') or {}).get('photographs', [])
trips = load('dov_trips.json') or {}
hyps = (load('hypotheses.json') or {}).get('hypotheses', [])
by_id = {p['id']: p for p in people}


def en(o):
    return ((o.get('en') or '') if isinstance(o, dict) else (o or '')).strip()


def ascii_only(s):
    """The built-in PDF fonts are Latin-1. Anything outside it is transliterated rather than
    dropped, so a Polish town keeps its shape instead of turning into a black square."""
    if not s:
        return ''
    rep = {'’': "'", '‘': "'", '“': '"', '”': '"', '—': ' - ',
           '–': '-', '…': '...', ' ': ' ',
           'ł': 'l', 'Ł': 'L', 'ś': 's', 'Ś': 'S', 'ż': 'z', 'ź': 'z', 'Ż': 'Z', 'Ź': 'Z',
           'ą': 'a', 'ę': 'e', 'ć': 'c', 'ń': 'n', 'ó': 'o', 'Ó': 'O', 'Ą': 'A', 'Ę': 'E',
           'ü': 'u', 'ö': 'o', 'ä': 'a', 'é': 'e', 'è': 'e', 'ç': 'c', 'ß': 'ss', 'í': 'i',
           'á': 'a', 'ú': 'u', 'ý': 'y', 'č': 'c', 'š': 's', 'ř': 'r', 'ě': 'e', 'ů': 'u'}
    for a, b in rep.items():
        s = s.replace(a, b)
    return ''.join(c if 32 <= ord(c) < 256 else '' for c in s)


class Doc(object):
    def __init__(self):
        self.d = fitz.open()
        self.new_page()

    def new_page(self):
        self.p = self.d.new_page(width=W, height=H)
        self.y = M

    def room(self, need):
        if self.y + need > H - M:
            self.new_page()

    def text(self, s, size=FS, bold=False, gap=4, indent=0):
        s = ascii_only(s)
        if not s:
            return
        font = 'hebo' if bold else 'helv'
        width = int((W - 2 * M - indent) / (size * 0.5))
        for line in textwrap.wrap(s, max(20, width)) or ['']:
            self.room(LH)
            self.p.insert_text((M + indent, self.y), line, fontname=font, fontsize=size)
            self.y += size * 1.35
        self.y += gap

    def rule(self):
        self.room(12)
        self.p.draw_line(fitz.Point(M, self.y), fitz.Point(W - M, self.y))
        self.y += 10

    def image(self, path, caption, credit=''):
        full = path if os.path.isabs(path) else os.path.join(SITE, path)
        if not os.path.exists(full):
            self.text('[missing: %s]' % path, size=8)
            return False
        try:
            pix = fitz.Pixmap(full)
            if pix.n > 4:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            iw, ih = pix.width, pix.height
        except Exception as e:
            self.text('[unreadable: %s - %s]' % (os.path.basename(path), type(e).__name__), size=8)
            return False
        boxw = W - 2 * M
        boxh = min(330.0, boxw * ih / float(iw))
        boxw2 = boxh * iw / float(ih)
        self.room(boxh + 40)
        rect = fitz.Rect(M, self.y, M + min(boxw, boxw2), self.y + boxh)
        try:
            self.p.insert_image(rect, filename=full, keep_proportion=True)
        except Exception:
            return False
        self.y += boxh + 6
        self.text(caption, size=8.5, bold=True, gap=1)
        if credit:
            self.text(credit, size=7.5, gap=8)
        else:
            self.y += 6
        return True


d = Doc()

# ── cover ───────────────────────────────────────────────────────────────
d.text('THE RAPAPORT FAMILY ARCHIVE', size=20, bold=True, gap=10)
d.text('Film pack - text and pictures in one file', size=12, gap=16)
d.rule()
d.text('For Dov Bernard Rapaport, eighty on 28 August 2026.', size=11, gap=10)
d.text('Upload THIS FILE to whatever tool makes the film. It is a PDF on purpose: notebook '
       'tools import text and images from PDFs, but they do NOT import images from Markdown or '
       'from a website, so a film built from the text alone would tell this family\'s story '
       'with none of this family\'s faces in it.', gap=10)
d.text('This file is English only. Embedding Hebrew properly needs a right-to-left layout '
       'engine, and a half-rendered Hebrew caption in a memorial film is worse than none. The '
       'Hebrew, Polish and French versions live on the site and in the Markdown pack at '
       'https://rapaportfamily.github.io/llm/', gap=14)
d.rule()
d.text('THE SIX RULES', size=12, bold=True, gap=6)
for i, r in enumerate([
    'Never invent. Every claim must trace to a record in this file.',
    'Show conflicts as conflicts. This archive publishes disagreements rather than tidying '
    'them away.',
    "Lusia's memoir is testimony, not proof. Where documents confirm it, say so. Where nothing "
    'corroborates it, say so - and say why: the people who would have kept the records are the '
    'people who were killed.',
    'Living people: no birth dates.',
    'Never put a name on any picture captioned UNIDENTIFIED.',
    'Illustration is allowed but must be visibly marked as illustration.',
    'A document is not a face. Every portrait was checked by eye on 19 August 2026 and 40 of '
    'the 74 pictures the trees carried as portraits turned out to be passports, certificates, '
    'Yad Vashem pages, a gravestone, a missing-persons card. This file prints verified faces '
    'only.'], 1):
    d.text('%d. %s' % (i, r), indent=12, gap=3)

# ── the story ───────────────────────────────────────────────────────────
d.new_page()
d.text('THE STORY', size=16, bold=True, gap=10)
for i, c in enumerate(narr):
    d.text('%d. %s   (%s)' % (i, en(c.get('title')), c.get('years', '')), size=12, bold=True, gap=5)
    for para in c['paragraphs']:
        d.text(en(para['text']), gap=6)
    d.y += 4

# ── the pictures, with captions ─────────────────────────────────────────
d.new_page()
d.text('THE PICTURES', size=16, bold=True, gap=8)
d.text('Every image below is a real photograph or a real document held by this family. '
       'Captions say what each one is. Use them.', gap=12)

d.text('Portraits', size=13, bold=True, gap=8)
for p in people:
    # Only portraits a human has actually looked at. Four documents were printed as
    # faces in the first build of this PDF, which is how the error was found.
    if not p.get('photo') or not p.get('photo_verified'):
        continue
    cap = '%s' % en(p.get('primary_name'))
    b, dt = (p.get('birth') or {}).get('date'), (p.get('death') or {}).get('date')
    if b or dt:
        cap += '  (%s - %s)' % (b or '?', dt or '')
    note = en(p.get('photo_caption'))
    d.image(p['photo'], cap, note or (p.get('photo_credit') or ''))

d.new_page()
d.text('The memoir plates - printed inside Lusia\'s own book', size=13, bold=True, gap=8)
for ph in memoir:
    cap = en(ph.get('caption_as_printed')) or 'Plate from the memoir'
    d.image(ph.get('file', ''), cap, en(ph.get('note'))[:200])

d.new_page()
d.text('The documents that matter most', size=13, bold=True, gap=8)
order = {'high': 0, 'medium': 1}
key_docs = [x for x in docs if x.get('film_priority')] + [
    x for x in docs if x['id'] in ('doc_david_dp_card', 'doc_auschwitz_victim_188161',
                                   'doc_berish_sterbebucher_1942', 'doc_lotte_yv_pot_53075',
                                   'doc_bernard_dov_yv_pot', 'doc_regina_rivka_yv_pot',
                                   'doc_david_birth_nadworna',
                                   'doc_berisz_swiadectwo_kwalifikacyjne_1924',
                                   'doc_david_gimnazjum_stanislawow')]
seen = set()
for doc in key_docs:
    if doc['id'] in seen:
        continue
    seen.add(doc['id'])
    d.text(en(doc.get('title')), size=11, bold=True, gap=4)
    s = en(doc.get('summary'))
    if s:
        d.text(s[:1100], size=8.5, gap=6)
    for f in (doc.get('file_pages') or [])[:3]:
        p = os.path.join('assets', 'documents', f)
        d.image(p, 'Document: ' + en(doc.get('title'))[:90],
                doc.get('source_archive', '')[:150])
    d.y += 6

d.new_page()
d.text('Dov went back - his four journeys, 2015 to 2019', size=13, bold=True, gap=8)
for a in trips.get('albums') or []:
    shots = [s for s in trips.get('photographs', []) if s['album'] == a['key']]
    d.text('%s - %s  (%d photographs, %d shown here)'
           % (en(a.get('title')), a.get('when'), len(shots), min(6, len(shots))),
           size=11, bold=True, gap=4)
    d.text(en(a.get('note')), size=8.5, gap=6)
    for s in shots[:6]:
        d.image(s['file'], '%s, %s' % (en(a.get('title')), a.get('when')),
                'Dov Rapaport with his son Doron')

# ── what nobody knows ───────────────────────────────────────────────────
d.new_page()
d.text('WHAT THE SOURCES DISAGREE ABOUT', size=16, bold=True, gap=8)
for line in [
    "Berish's death: the Auschwitz Museum and the camp Sterbebucher both say 29 March 1942; "
    "the Yad Vashem page David filed in 1953 says 1940. Both are published.",
    "Rebeka: this archive holds born 1888 died 1942; her Yad Vashem page says 1892 and 1943; "
    "Jacob's tree says 1942 with a question mark. All three stand.",
    "Lotte: born 27 September 1915 per the trees, 1914 per her Yad Vashem page. Her cousin "
    "Charlotte Horowitz was born 21 November 1914 in the same city. Do not merge them.",
    "David's birthplace: Nadworna per the birth certificate; Cieszyn on his 1946 DP card. "
    "Lusia's card says she was born in HAIFA, PALESTINE - she was born in Bolechow. Two cards, "
    "two wrong birthplaces, and on hers the destination is Palestine.",
]:
    d.text('- ' + line, indent=8, gap=6)

d.text('OPEN QUESTIONS - these are questions, not findings', size=13, bold=True, gap=6)
d.text('A film that answers them invents history. A film that ends on them tells the truth '
       'about what this family still does not know.', size=9, gap=8)
for h in hyps:
    q = en(h.get('question')) or en(h.get('title')) or en(h.get('statement'))
    if q:
        d.text('- ' + q, indent=8, gap=4)

d.d.save(OUT, deflate=True, garbage=3)
size = os.path.getsize(OUT) / 1e6
print('wrote %s' % OUT)
print('  %d pages, %.1f MB  (NotebookLM accepts up to 200 MB per source)'
      % (d.d.page_count, size))
