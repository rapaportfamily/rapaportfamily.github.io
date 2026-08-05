// ============================================================
// The Rapaport Family Archive — main app
// Vanilla JS, no build step. Hash routing. Multi-language.
// ============================================================

const State = {
  lang: 'en',
  i18n: {},
  data: {
    people: [],
    places: [],
    events: [],
    documents: [],
    hypotheses: [],
    messages: [],
  },
  byId: {
    people: {},
    places: {},
    events: {},
    documents: {},
    hypotheses: {},
  },
};

// ----------------------------------------
// Data loading
// ----------------------------------------
async function loadAll() {
  // Cache-bust on every load - data files update frequently
  const v = Date.now();
  const noCache = { cache: 'no-store' };
  const [en, he, pl, fr, people, places, events, documents, hypotheses, messages, research] = await Promise.all([
    fetch(`data/i18n/en.json?v=${v}`, noCache).then(r => r.json()),
    fetch(`data/i18n/he.json?v=${v}`, noCache).then(r => r.json()),
    fetch(`data/i18n/pl.json?v=${v}`, noCache).then(r => r.json()),
    fetch(`data/i18n/fr.json?v=${v}`, noCache).then(r => r.json()),
    fetch(`data/people.json?v=${v}`, noCache).then(r => r.json()),
    fetch(`data/places.json?v=${v}`, noCache).then(r => r.json()),
    fetch(`data/events.json?v=${v}`, noCache).then(r => r.json()),
    fetch(`data/documents.json?v=${v}`, noCache).then(r => r.json()),
    fetch(`data/hypotheses.json?v=${v}`, noCache).then(r => r.json()),
    fetch(`data/messages.json?v=${v}`, noCache).then(r => r.json()),
    fetch(`data/research_center.json?v=${v}`, noCache).then(r => r.json()).catch(() => ({ sections: [] })),
  ]);
  State.i18n = { en, he, pl, fr };
  State.data.people = people.people;
  State.data.places = places.places;
  State.data.events = events.events;
  State.data.documents = documents.documents;
  State.data.additional_files = documents.additional_files || [];
  State.data.hypotheses = hypotheses.hypotheses;
  State.data.messages = messages.messages || messages;
  State.data.research = research;

  for (const p of State.data.people) State.byId.people[p.id] = p;
  for (const p of State.data.places) State.byId.places[p.id] = p;
  for (const e of State.data.events) State.byId.events[e.id] = e;
  for (const d of State.data.documents) State.byId.documents[d.id] = d;
  for (const h of State.data.hypotheses) State.byId.hypotheses[h.id] = h;
}

// ----------------------------------------
// i18n helpers
// ----------------------------------------
function t(path) {
  const parts = path.split('.');
  let cur = State.i18n[State.lang];
  for (const p of parts) {
    if (!cur) return path;
    cur = cur[p];
  }
  return cur ?? path;
}
// Pick a multilingual field, falling back across languages
function ml(obj, fallbackOrder = ['en', 'he', 'pl', 'fr']) {
  if (!obj) return '';
  if (obj[State.lang]) return obj[State.lang];
  for (const l of fallbackOrder) if (obj[l]) return obj[l];
  return Object.values(obj)[0] || '';
}
// Dates arrive two ways: ISO from the records ("1911-12-25") and free text from
// the memoir, where the source is genuinely vague ("1950s", "circa 1958").
// Render the ISO ones in the reader's language; pass everything else through
// untouched — an approximate date must be allowed to look approximate.
function fmtDate(d) {
  if (!d) return t('ui.unknown');
  const s = String(d);
  // "1950s" is a real answer when the memoir gives no better one — but it has to
  // be sayable in Hebrew, Polish and French too, not left as an English suffix.
  const dec = s.match(/^(\d{4})s$/);
  if (dec) return t('ui.decade').replace('{decade}', dec[1]);
  const iso = s.match(/^(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?$/);
  if (!iso) return s;
  const [, y, m, day] = iso;
  if (!m) return y;
  try {
    const dt = new Date(Date.UTC(+y, +m - 1, +(day || 1)));
    return new Intl.DateTimeFormat(State.lang, {
      year: 'numeric', month: 'long', timeZone: 'UTC',
      ...(day ? { day: 'numeric' } : {})
    }).format(dt);
  } catch (e) {
    return s;
  }
}

// ----------------------------------------
// Language switching
// ----------------------------------------
function setLang(lang) {
  if (!State.i18n[lang]) return;
  State.lang = lang;
  const meta = State.i18n[lang].meta;
  document.documentElement.lang = lang;
  document.documentElement.dir = meta.dir;
  document.title = t('site.title');
  // Apply data-i18n
  document.querySelectorAll('[data-i18n]').forEach(el => {
    el.textContent = t(el.getAttribute('data-i18n'));
  });
  // Lang buttons
  document.querySelectorAll('.lang-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.lang === lang);
  });
  // Persist
  try { localStorage.setItem('rapaport_lang', lang); } catch (e) {}
  // Re-render current view
  router();
  updateNavScrollHint();
}

// The top bar is a single row in every language. Polish and French labels run
// wider than English, so when the row cannot fit it scrolls sideways and gets a
// soft edge fade to show there is more. Recomputed on load, language change and
// resize, because the labels change length with the language.
function updateNavScrollHint() {
  const inner = document.querySelector('.nav-inner');
  if (!inner) return;
  inner.classList.toggle('is-scrollable', inner.scrollWidth > inner.clientWidth + 1);
}
window.addEventListener('resize', updateNavScrollHint);

// ----------------------------------------
// Router
// ----------------------------------------
function router() {
  const hash = location.hash || '#/home';
  const path = hash.slice(2).split('/');
  const view = path[0] || 'home';
  // The browser percent-encodes anything non-ASCII in the hash, so a search for
  // "Liège" or "Radomyśl" reached the views as "Li%C3%A8ge" and matched nothing.
  let param = path[1];
  if (param) { try { param = decodeURIComponent(param); } catch (e) { /* malformed — use as-is */ } }

  document.querySelectorAll('.nav-inner a').forEach(a => {
    a.classList.toggle('active', a.dataset.nav === view);
  });

  const root = document.getElementById('view');
  root.innerHTML = '';

  switch (view) {
    case 'home': renderHome(root); break;
    case 'tree': renderTree(root); break;
    case 'timeline': renderTimeline(root); break;
    case 'journey': renderJourney(root); break;
    case 'story': renderStory(root); break;
    case 'people': renderPeople(root, param); break;
    case 'places': renderPlaces(root, param); break;
    case 'documents': renderDocuments(root, param); break;
    case 'hypotheses': renderHypotheses(root); break;
    case 'chat': renderChat(root); break;
    case 'research': renderResearch(root, param); break;
    case 'photographs': renderPhotographs(root); break;
    case 'about': renderAbout(root); break;
    default: renderHome(root);
  }
  window.scrollTo({ top: 0, behavior: 'instant' });
}

// ----------------------------------------
// Page header helper
// ----------------------------------------
function pageHeader(titleKey, leadKey) {
  return `
    <div class="page-header">
      <h1>${escapeHtml(t(titleKey))}</h1>
      <p class="lead">${escapeHtml(t(leadKey))}</p>
    </div>
  `;
}

// Half this archive is Polish, French and Hebrew. Searching "Liege" should find
// "Liège", and "Radomysl" should find "Radomyśl" — strip the diacritics from
// both the text and the query before comparing.
function foldText(v) {
  return String(v == null ? '' : v)
    .normalize('NFD').replace(/[̀-ͯ]/g, '')
    .replace(/[ł]/g, 'l').replace(/[Ł]/g, 'L')
    .toLowerCase();
}

// Tolerate hand-edited data: a field the renderer expects as a list may
// arrive as a single string, or be missing. Never let that blank a page.
function asList(v) {
  if (v == null) return [];
  return Array.isArray(v) ? v : [String(v)];
}

function escapeHtml(s) {
  if (s == null) return '';
  return String(s).replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}

// ----------------------------------------
// HOME
// ----------------------------------------
function renderHome(root) {
  const s = State.data;
  const recentDiscoveries = s.events.filter(e => e.type === 'discovery').sort((a,b) => b.date_sort.localeCompare(a.date_sort));
  const openHyps = s.hypotheses.filter(h => ['open','active_investigation'].includes(h.status));

  root.innerHTML = `
    <section class="home-hero">
      <div class="eyebrow">${escapeHtml(t('site.subtitle'))}</div>
      <h1>${escapeHtml(t('site.title'))}</h1>
      <p class="lead">${escapeHtml(t('home.lead'))}</p>
    </section>

    <div class="home-intro">
      <p>${escapeHtml(t('home.intro_p1'))}</p>
      <p>${escapeHtml(t('home.intro_p2'))}</p>
    </div>

    <h3 class="section-title">${escapeHtml(t('home.stats_title'))}</h3>
    <div class="stats-strip">
      <div class="stat-cell"><div class="stat-num">${s.people.length}</div><div class="stat-label">${escapeHtml(t('ui.people_count'))}</div></div>
      <div class="stat-cell"><div class="stat-num">${s.places.length}</div><div class="stat-label">${escapeHtml(t('ui.places_count'))}</div></div>
      <div class="stat-cell"><div class="stat-num">${s.events.length}</div><div class="stat-label">${escapeHtml(t('ui.events_count'))}</div></div>
      <div class="stat-cell"><div class="stat-num">${s.documents.length}</div><div class="stat-label">${escapeHtml(t('ui.documents_count'))}</div></div>
      <div class="stat-cell"><div class="stat-num">${s.hypotheses.length}</div><div class="stat-label">${escapeHtml(t('nav.hypotheses'))}</div></div>
      <div class="stat-cell"><div class="stat-num">${s.messages.length}</div><div class="stat-label">${escapeHtml(t('ui.messages_count'))}</div></div>
    </div>

    <h3 class="section-title">${escapeHtml(t('home.latest_finds_title'))}</h3>
    <div class="cards-grid">
      ${recentDiscoveries.slice(0,4).map(e => `
        <div class="card" data-action="event" data-id="${escapeHtml(e.id)}">
          <div class="card-meta">${escapeHtml(fmtDate(e.date))} · ${escapeHtml(t('confidence.' + (e.confidence || 'documented')))}</div>
          <h3>${escapeHtml(ml(e.title))}</h3>
          <div class="card-body">${escapeHtml(ml(e.description))}</div>
        </div>
      `).join('')}
    </div>

    <h3 class="section-title">${escapeHtml(t('home.open_questions_title'))}</h3>
    <div class="cards-grid">
      ${openHyps.slice(0,4).map(h => `
        <div class="card" data-action="hypothesis" data-id="${escapeHtml(h.id)}">
          <div class="card-meta">${escapeHtml(t('status.' + h.status))} · ${escapeHtml(h.priority)} ${escapeHtml(t('ui.priority').toLowerCase())}</div>
          <h3>${escapeHtml(ml(h.question))}</h3>
          <div class="card-footer">${escapeHtml(t('ui.show_more'))} →</div>
        </div>
      `).join('')}
    </div>

    <h3 class="section-title">${escapeHtml(t('home.explore_title'))}</h3>
    <div class="explore-grid">
      <a class="explore-tile" href="#/tree" data-link>
        <h4>${escapeHtml(t('nav.tree'))}</h4><p>${escapeHtml(t('home.explore_tree'))}</p>
      </a>
      <a class="explore-tile" href="#/timeline" data-link>
        <h4>${escapeHtml(t('nav.timeline'))}</h4><p>${escapeHtml(t('home.explore_timeline'))}</p>
      </a>
      <a class="explore-tile" href="#/documents" data-link>
        <h4>${escapeHtml(t('nav.documents'))}</h4><p>${escapeHtml(t('home.explore_docs'))}</p>
      </a>
      <a class="explore-tile" href="#/hypotheses" data-link>
        <h4>${escapeHtml(t('nav.hypotheses'))}</h4><p>${escapeHtml(t('home.explore_hypotheses'))}</p>
      </a>
      <a class="explore-tile" href="#/chat" data-link>
        <h4>${escapeHtml(t('nav.chat'))}</h4><p>${escapeHtml(t('home.explore_chat'))}</p>
      </a>
    </div>
  `;

  root.querySelectorAll('[data-action="event"]').forEach(el => {
    el.addEventListener('click', () => openEventModal(el.dataset.id));
  });
  root.querySelectorAll('[data-action="hypothesis"]').forEach(el => {
    el.addEventListener('click', () => location.hash = '#/hypotheses');
  });
}

// ----------------------------------------
// FAMILY TREE  (computed layout — every person in the archive)
// ----------------------------------------
// The layout is derived from the data, not hand-placed: generations come from
// the parent/child graph, couples are grouped into units, and each unit is
// centred over its children. People whose link into the tree is not yet
// documented are shown in their own labelled sections rather than dropped —
// no relationship is invented to make the drawing tidier.

const TREE = {
  BW: 170, BH: 54,   // person box
  HGAP: 14,          // gap between the two boxes of a couple
  UGAP: 40,          // gap between family units in the same row
  ROW: 124,          // vertical distance between generations
  PAD: 30,           // outer padding
  SECTION_GAP: 78,   // space above a section title
  TITLE_H: 30,       // height reserved for a section title
  GRID_GAP: 16,      // gap in the "no documented link yet" grids
  MIN_W: 900,
};

// Documented Holocaust survivors in the direct line (shaded in the legend).
const TREE_SURVIVORS = new Set(['p_david', 'p_leah', 'p_shimon', 'p_dov_bernard']);

// Roles → the section a person is filed under when no documented link exists.
const TREE_ROLE_GROUP = {
  dynasty_progenitor: 'dynasty',
  dynasty_ancestor: 'dynasty',
  dynasty_ancestor_galician: 'dynasty',
  documented_medieval_ancestor: 'dynasty',
  rabbinical_dynasty_ancestor: 'rabbinic',
  rabbinic_context_ancestor: 'rabbinic',
  righteous_gentile: 'righteous',
  living_cousin: 'living',
  living_cousin_in_law: 'living',
  living_cousin_paternal: 'living',
};
const TREE_GROUP_ORDER = ['dynasty', 'rabbinic', 'living', 'righteous', 'extended'];
function treeGroupOf(p) { return TREE_ROLE_GROUP[p.role] || 'extended'; }

// ---------- graph ----------
function buildFamilyGraph() {
  const byId = State.byId.people;
  const ids = State.data.people.map(p => p.id);
  const spouses = {}, par = {}, kids = {};
  ids.forEach(i => { spouses[i] = new Set(); par[i] = new Set(); kids[i] = new Set(); });

  for (const p of State.data.people) {
    const marry = (a, b) => {
      if (!byId[b] || a === b) return;
      spouses[a].add(b); spouses[b].add(a);
    };
    if (p.spouse_id) marry(p.id, p.spouse_id);
    for (const s of p.spouse_ids || []) marry(p.id, s);

    for (const key of ['father_id', 'mother_id']) {
      const v = p[key];
      if (v && byId[v] && v !== p.id) { par[p.id].add(v); kids[v].add(p.id); }
    }
    for (const c of p.children_ids || []) {
      if (byId[c] && c !== p.id) { par[c].add(p.id); kids[p.id].add(c); }
    }
  }
  return { ids, byId, spouses, par, kids };
}

function graphComponents(g) {
  const seen = new Set(), out = [];
  for (const start of g.ids) {
    if (seen.has(start)) continue;
    const stack = [start], members = [];
    seen.add(start);
    while (stack.length) {
      const id = stack.pop();
      members.push(id);
      for (const set of [g.spouses[id], g.par[id], g.kids[id]]) {
        for (const n of set) if (!seen.has(n)) { seen.add(n); stack.push(n); }
      }
    }
    out.push(members);
  }
  // Biggest component first — that is the documented family.
  out.sort((a, b) => b.length - a.length);
  return out;
}

// Parents strictly above children; spouses on the same row.
function assignGenerations(members, g) {
  const gen = {};
  members.forEach(id => { gen[id] = 0; });
  const inComp = new Set(members);
  for (let pass = 0; pass < members.length + 2; pass++) {
    let moved = false;
    for (const id of members) {
      for (const f of g.par[id]) {
        if (inComp.has(f) && gen[id] < gen[f] + 1) { gen[id] = gen[f] + 1; moved = true; }
      }
    }
    for (const id of members) {
      for (const s of g.spouses[id]) {
        if (!inComp.has(s)) continue;
        const m = Math.max(gen[id], gen[s]);
        if (gen[id] !== m || gen[s] !== m) { gen[id] = gen[s] = m; moved = true; }
      }
    }
    if (!moved) break;
  }
  return gen;
}

// ---------- units (a couple, or a single person) ----------
function buildUnits(members, g, gen) {
  const unitOf = {}, units = [];
  const ordered = members.slice().sort((a, b) => (gen[a] - gen[b]) || a.localeCompare(b));

  for (const id of ordered) {
    if (unitOf[id]) continue;
    const mates = [...g.spouses[id]]
      .filter(s => !unitOf[s] && gen[s] === gen[id] && members.includes(s))
      .sort();
    const unit = { id: 'u' + units.length, gen: gen[id], members: [id], childUnits: [], parentUnits: [] };
    if (mates.length) unit.members.push(mates[0]);
    unit.members.forEach(m => { unitOf[m] = unit; });
    unit.w = unit.members.length * TREE.BW + (unit.members.length - 1) * TREE.HGAP;
    units.push(unit);
  }

  // Link units to every documented parent unit — both sides of a marriage, so
  // a couple stays connected to both sets of parents.
  for (const unit of units) {
    for (const m of unit.members) {
      for (const p of g.par[m]) {
        const pu = unitOf[p];
        if (!pu || pu === unit) continue;
        if (!pu.childUnits.includes(unit)) pu.childUnits.push(unit);
        if (!unit.parentUnits.includes(pu)) unit.parentUnits.push(pu);
      }
    }
  }
  return { units, unitOf };
}

// ---------- horizontal placement ----------
// Two stages, both standard layered-graph technique:
//   1. order each generation row to reduce crossings (barycentre sweeps), so
//      relatives end up next to relatives;
//   2. hang rows under their parents, then apply the priority method so each
//      unit is pulled towards its own relatives without the drawing drifting
//      wider, and nothing ever overlaps.
function layoutUnits(units) {
  const GAP = TREE.UGAP;
  const rows = {};
  units.forEach(u => { (rows[u.gen] = rows[u.gen] || []).push(u); });
  const gens = Object.keys(rows).map(Number).sort((a, b) => a - b);
  gens.forEach(g => rows[g].sort((a, b) => a.members[0].localeCompare(b.members[0])));

  // --- 1. ordering ---
  const idx = new Map();
  const reindex = () => gens.forEach(g => rows[g].forEach((u, i) => idx.set(u, i)));
  reindex();
  const barycentre = (u, side) => {
    const ns = side === 'up' ? u.parentUnits : u.childUnits;
    const vals = ns.map(n => idx.get(n)).filter(v => v != null);
    return vals.length ? vals.reduce((a, b) => a + b, 0) / vals.length : null;
  };
  for (let sweep = 0; sweep < 8; sweep++) {
    const side = sweep % 2 ? 'down' : 'up';
    for (const g of (sweep % 2 ? gens.slice().reverse() : gens)) {
      const tagged = rows[g].map((u, i) => ({ u, i, b: barycentre(u, side) }));
      tagged.sort((p, q) => ((p.b == null ? p.i : p.b) - (q.b == null ? q.i : q.b)) || (p.i - q.i));
      rows[g] = tagged.map(o => o.u);
      reindex();
    }
  }

  // --- 2. initial x: hang each row under its parents, packed tight ---
  const centre = u => u.x + u.w / 2;
  const avgCentre = list => list.reduce((s, n) => s + centre(n), 0) / list.length;
  for (const g of gens) {
    const row = rows[g];
    let limit = -Infinity;
    row.forEach((u, i) => {
      const ps = u.parentUnits.filter(p => typeof p.x === 'number');
      const want = ps.length ? avgCentre(ps) - u.w / 2 : (i === 0 ? 0 : limit);
      u.x = Math.max(want, limit);
      limit = u.x + u.w + GAP;
    });
  }

  // --- 3. priority method: pull each unit towards its relatives, but a unit
  // may only push neighbours that are less constrained than itself, so the
  // drawing tightens instead of drifting wider (Sugiyama et al.). ---
  const shift = (row, i, delta, prio, self) => {
    const u = row[i];
    if (delta > 0) {
      const next = row[i + 1];
      if (next) {
        const slack = next.x - (u.x + u.w + GAP);
        if (slack < delta) {
          delta = prio.get(next) > prio.get(self)
            ? slack
            : slack + shift(row, i + 1, delta - slack, prio, self);
        }
      }
      u.x += Math.max(delta, 0);
      return Math.max(delta, 0);
    }
    let want = -delta;
    const prev = row[i - 1];
    if (prev) {
      const slack = u.x - (prev.x + prev.w + GAP);
      if (slack < want) {
        want = prio.get(prev) > prio.get(self)
          ? slack
          : slack + shift(row, i - 1, -(want - slack), prio, self);
      }
    }
    u.x -= Math.max(want, 0);
    return -Math.max(want, 0);
  };

  for (let pass = 0; pass < 10; pass++) {
    const down = pass % 2 === 0;
    const order = down ? gens.slice(1) : gens.slice(0, -1).reverse();
    for (const g of order) {
      const row = rows[g];
      const refs = u => (down ? u.parentUnits : u.childUnits).filter(n => typeof n.x === 'number');
      const prio = new Map(row.map(u => [u, refs(u).length]));
      const moves = row
        .map((u, i) => ({ u, i, want: refs(u).length ? avgCentre(refs(u)) - u.w / 2 : null }))
        .filter(m => m.want != null)
        .sort((a, b) => (prio.get(b.u) - prio.get(a.u)) || (Math.abs(b.want - b.u.x) - Math.abs(a.want - a.u.x)));
      for (const m of moves) {
        const i = row.indexOf(m.u);
        const delta = m.want - m.u.x;
        if (Math.abs(delta) > 0.5) shift(row, i, delta, prio, m.u);
      }
    }
  }

  const minX = Math.min(...units.map(u => u.x));
  units.forEach(u => { u.x -= minX; });
  const width = Math.max(...units.map(u => u.x + u.w));
  const maxGen = Math.max(...units.map(u => u.gen));
  return { width, maxGen };
}

// ---------- SVG helpers ----------
const SVGNS = 'http://www.w3.org/2000/svg';
function svgEl(name, attrs = {}) {
  const el = document.createElementNS(SVGNS, name);
  for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, v);
  return el;
}
function svgLine(parent, x1, y1, x2, y2, cls) {
  parent.appendChild(svgEl('line', { x1, y1, x2, y2, class: cls }));
}
function svgText(parent, x, y, text, cls) {
  const el = svgEl('text', { x, y, class: cls });
  el.textContent = text;
  parent.appendChild(el);
  return el;
}

function drawPersonBox(parent, person, x, y) {
  const g = svgEl('g', {
    class: 'person-box'
      + (person.id === 'p_dov_bernard' ? ' subject' : '')
      + (TREE_SURVIVORS.has(person.id) ? ' survivor' : '')
      + (person.death && person.death.date ? ' deceased' : ''),
    'data-person': person.id,
    transform: `translate(${x},${y})`,
    tabindex: '0',
    role: 'button',
  });
  g.appendChild(svgEl('rect', { class: 'person-rect', width: TREE.BW, height: TREE.BH, rx: 3 }));

  const full = ml(person.primary_name) || person.id;
  const title = svgEl('title');
  title.textContent = full + ' — ' + roleLabel(person.role || '');
  g.appendChild(title);

  svgText(g, TREE.BW / 2, 22, truncate(full, 24), 'person-name');
  // The People view stopped printing "?" against the 65 people whose birth date
  // we have never had; the tree kept doing it, so most living relatives read
  // "? –". An empty field is not a fact about a person. Show what we have.
  const b = person.birth && person.birth.date ? extractYear(person.birth.date) : '';
  const d = person.death && person.death.date ? extractYear(person.death.date) : '';
  let dates = '';
  if (b && d) dates = `${b} – ${d}`;
  else if (b) dates = `${b} –`;
  else if (d) dates = `– ${d}`;
  if (dates) svgText(g, TREE.BW / 2, 40, dates, 'person-dates');

  const open = () => openPersonModal(person.id);
  g.addEventListener('click', open);
  g.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); } });
  parent.appendChild(g);
  return g;
}

// ---------- one connected family, drawn as a tree ----------
function drawFamilyBlock(svg, members, g, yTop) {
  const gen = assignGenerations(members, g);
  const { units } = buildUnits(members, g, gen);
  const { width, maxGen } = layoutUnits(units);

  const lines = svgEl('g', { class: 'tree-lines' });
  const boxes = svgEl('g', { class: 'tree-boxes' });
  svg.appendChild(lines);
  svg.appendChild(boxes);

  const rowY = genIdx => yTop + genIdx * TREE.ROW;
  const centreX = unit => unit.x + unit.w / 2;

  // generation labels: the decades actually present in that row
  for (let gi = 0; gi <= maxGen; gi++) {
    const inRow = members.filter(id => gen[id] === gi);
    const years = inRow
      .map(id => {
        const raw = State.byId.people[id].birth && State.byId.people[id].birth.date;
        const m = raw ? String(raw).match(/\d{3,4}/) : null;
        return m ? parseInt(m[0], 10) : null;
      })
      .filter(y => y != null)
      .sort((a, b) => a - b);
    let label = `${t('tree.generation')} ${gi + 1}`;
    if (years.length) {
      const lo = Math.floor(years[0] / 10) * 10;
      const hi = Math.floor(years[years.length - 1] / 10) * 10;
      label += ` · ${lo}${hi > lo ? '–' + hi : ''}`;
    }
    svgText(lines, 0, rowY(gi) - 12, label, 'gen-label');
  }

  // spouse lines
  for (const unit of units) {
    if (unit.members.length < 2) continue;
    const y = rowY(unit.gen) + TREE.BH / 2;
    svgLine(lines, unit.x + TREE.BW, y, unit.x + TREE.BW + TREE.HGAP, y, 'spouse-line');
  }

  // parent → children buses (one per parent unit; both parent couples of a
  // married-in child are drawn, so in-law grandparents stay connected)
  for (const unit of units) {
    const children = unit.childUnits.filter(c => typeof c.x === 'number');
    if (!children.length) continue;
    const byRow = {};
    children.forEach(c => { (byRow[c.gen] = byRow[c.gen] || []).push(c); });
    for (const [rowStr, kidUnits] of Object.entries(byRow)) {
      const row = Number(rowStr);
      const busY = rowY(row) - TREE.ROW * 0.34;
      const px = centreX(unit);
      const xs = kidUnits.map(centreX);
      svgLine(lines, px, rowY(unit.gen) + TREE.BH, px, busY, 'tree-line');
      svgLine(lines, Math.min(px, ...xs), busY, Math.max(px, ...xs), busY, 'tree-line');
      kidUnits.forEach(c => svgLine(lines, centreX(c), busY, centreX(c), rowY(c.gen), 'tree-line'));
    }
  }

  for (const unit of units) {
    unit.members.forEach((id, i) => {
      drawPersonBox(boxes, State.byId.people[id], unit.x + i * (TREE.BW + TREE.HGAP), rowY(unit.gen));
    });
  }

  return { width, height: (maxGen + 1) * TREE.ROW - (TREE.ROW - TREE.BH) };
}

// ---------- people with no documented link: labelled grid ----------
function drawPeopleGrid(svg, ids, yTop, availableWidth) {
  const boxes = svgEl('g', { class: 'tree-boxes' });
  svg.appendChild(boxes);
  const perRow = Math.max(1, Math.floor((availableWidth + TREE.GRID_GAP) / (TREE.BW + TREE.GRID_GAP)));
  ids.forEach((id, i) => {
    const col = i % perRow, row = Math.floor(i / perRow);
    drawPersonBox(boxes, State.byId.people[id],
      col * (TREE.BW + TREE.GRID_GAP),
      yTop + row * (TREE.BH + TREE.GRID_GAP + 12));
  });
  const rows = Math.ceil(ids.length / perRow);
  return {
    width: Math.min(ids.length, perRow) * (TREE.BW + TREE.GRID_GAP) - TREE.GRID_GAP,
    height: rows * (TREE.BH + TREE.GRID_GAP + 12) - TREE.GRID_GAP - 12,
  };
}

function drawSectionTitle(svg, y, text, sub) {
  const g = svgEl('g');
  svg.appendChild(g);
  svgText(g, 0, y, text, 'tree-section-title');
  if (sub) svgText(g, 0, y + 17, sub, 'tree-section-sub');
  return sub ? 22 : 6;
}

// ---------- the whole page ----------
function buildFamilyTreeSVG() {
  const g = buildFamilyGraph();
  const comps = graphComponents(g);
  const main = comps[0] || [];
  const rest = comps.slice(1);

  // Everything outside the main tree, bucketed by role.
  const buckets = {};
  for (const comp of rest) {
    const counts = {};
    comp.forEach(id => {
      const k = treeGroupOf(State.byId.people[id]);
      counts[k] = (counts[k] || 0) + 1;
    });
    const key = Object.keys(counts).sort((a, b) => counts[b] - counts[a])[0];
    (buckets[key] = buckets[key] || { chains: [], singles: [] });
    if (comp.length > 1) buckets[key].chains.push(comp);
    else buckets[key].singles.push(comp[0]);
  }

  const svg = svgEl('svg', { class: 'tree-svg', xmlns: SVGNS });
  const canvas = svgEl('g', { class: 'tree-canvas' });
  svg.appendChild(canvas);

  let y = 0, width = TREE.MIN_W;
  const bump = w => { width = Math.max(width, w); };

  // 1) the documented family
  y += drawSectionTitle(canvas, y,
    `${t('tree.section_main')} · ${main.length} ${t('ui.people_count').toLowerCase()}`, null) + TREE.TITLE_H;
  const mainBox = drawFamilyBlock(canvas, main, g, y);
  bump(mainBox.width);
  y += mainBox.height + TREE.SECTION_GAP;

  // 2) the rest, grouped and clearly labelled as unlinked
  for (const key of TREE_GROUP_ORDER) {
    const bucket = buckets[key];
    if (!bucket) continue;
    const count = bucket.singles.length + bucket.chains.reduce((n, c) => n + c.length, 0);
    y += drawSectionTitle(canvas, y,
      `${t('tree.group_' + key)} · ${count} ${t('ui.people_count').toLowerCase()}`,
      t('tree.unlinked_note')) + TREE.TITLE_H;

    for (const chain of bucket.chains) {
      const box = drawFamilyBlock(canvas, chain, g, y);
      bump(box.width);
      y += box.height + TREE.GRID_GAP + 24;
    }
    if (bucket.singles.length) {
      const ordered = bucket.singles.slice().sort((a, b) => {
        const ya = (String((State.byId.people[a].birth || {}).date || '').match(/\d{3,4}/) || [9999])[0];
        const yb = (String((State.byId.people[b].birth || {}).date || '').match(/\d{3,4}/) || [9999])[0];
        return Number(ya) - Number(yb) || a.localeCompare(b);
      });
      const box = drawPeopleGrid(canvas, ordered, y, Math.max(width, TREE.MIN_W));
      bump(box.width);
      y += box.height;
    }
    y += TREE.SECTION_GAP;
  }

  const W = width + TREE.PAD * 2;
  const H = y - TREE.SECTION_GAP + TREE.PAD * 2;
  canvas.setAttribute('transform', `translate(${TREE.PAD},${TREE.PAD + 10})`);
  svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
  svg.dataset.w = W;
  svg.dataset.h = H;
  return svg;
}

// ---------- pan + zoom ----------
function wireTreeViewport(svg, host) {
  const W = Number(svg.dataset.w), H = Number(svg.dataset.h);
  const viewport = host.querySelector('.tree-viewport');
  const view = { x: 0, y: 0, w: W, h: H };
  const apply = () => svg.setAttribute('viewBox', `${view.x} ${view.y} ${view.w} ${view.h}`);

  // Fit the whole drawing into the viewport. If the element has not been laid
  // out yet (hidden tab, zero-size pane) show the full content box instead of
  // deriving a nonsense aspect ratio from a zero measurement.
  const fit = () => {
    const box = viewport.getBoundingClientRect();
    if (!(box.width > 40 && box.height > 40)) {
      view.x = 0; view.y = 0; view.w = W; view.h = H;
      apply();
      return;
    }
    const aspect = box.width / box.height;
    let w = W, h = W / aspect;
    if (h < H) { h = H; w = H * aspect; }
    view.x = (W - w) / 2; view.y = (H - h) / 2; view.w = w; view.h = h;
    apply();
  };

  const zoomAt = (factor, cx, cy) => {
    const box = svg.getBoundingClientRect();
    const px = box.width ? (cx - box.left) / box.width : 0.5;
    const py = box.height ? (cy - box.top) / box.height : 0.5;
    const fx = view.x + px * view.w, fy = view.y + py * view.h;
    const nw = Math.min(Math.max(view.w * factor, W / 14), W * 3);
    const nh = nw * (view.h / view.w);
    view.x = fx - px * nw; view.y = fy - py * nh;
    view.w = nw; view.h = nh;
    apply();
  };

  svg.addEventListener('wheel', e => {
    e.preventDefault();
    zoomAt(e.deltaY > 0 ? 1.12 : 0.89, e.clientX, e.clientY);
  }, { passive: false });

  let drag = null;
  svg.addEventListener('pointerdown', e => {
    if (e.target.closest('.person-box')) return;   // let clicks through to people
    drag = { x: e.clientX, y: e.clientY };
    svg.classList.add('grabbing');
    svg.setPointerCapture(e.pointerId);
  });
  svg.addEventListener('pointermove', e => {
    if (!drag) return;
    const box = svg.getBoundingClientRect();
    view.x -= (e.clientX - drag.x) * (view.w / (box.width || 1));
    view.y -= (e.clientY - drag.y) * (view.h / (box.height || 1));
    drag = { x: e.clientX, y: e.clientY };
    apply();
  });
  const endDrag = () => { drag = null; svg.classList.remove('grabbing'); };
  svg.addEventListener('pointerup', endDrag);
  svg.addEventListener('pointercancel', endDrag);
  svg.addEventListener('pointerleave', endDrag);

  host.querySelector('[data-tree="in"]').addEventListener('click', () => {
    const b = svg.getBoundingClientRect();
    zoomAt(0.8, b.left + b.width / 2, b.top + b.height / 2);
  });
  host.querySelector('[data-tree="out"]').addEventListener('click', () => {
    const b = svg.getBoundingClientRect();
    zoomAt(1.25, b.left + b.width / 2, b.top + b.height / 2);
  });
  // Opening view: 122 people fitted to a screen is unreadable, so start
  // centred on the person this archive is for, at a legible scale. "Fit"
  // gives the whole picture.
  const SPAN = 2100;
  const start = () => {
    const box = viewport.getBoundingClientRect();
    const subject = svg.querySelector('.person-box.subject');
    const m = subject && /translate\(([-\d.]+),([-\d.]+)\)/.exec(subject.getAttribute('transform'));
    if (!m) { fit(); return; }
    const cx = Number(m[1]) + TREE.BW / 2 + TREE.PAD;
    const cy = Number(m[2]) + TREE.BH / 2 + TREE.PAD + 10;
    const aspect = (box.width > 40 && box.height > 40) ? box.width / box.height : W / H;
    view.w = Math.min(SPAN, W);
    view.h = view.w / aspect;
    view.x = cx - view.w / 2;
    view.y = cy - view.h / 2;
    apply();
  };

  host.querySelector('[data-tree="fit"]').addEventListener('click', fit);
  host.querySelector('[data-tree="subject"]').addEventListener('click', start);

  start();
  // Re-run once the viewport actually has a size (first paint, hidden tab
  // becoming visible, orientation change) so the tree is never left mid-zoom.
  let settled = false;
  if (typeof ResizeObserver === 'function') {
    const ro = new ResizeObserver(() => {
      const box = viewport.getBoundingClientRect();
      if (!settled && box.width > 40 && box.height > 40) { settled = true; start(); }
    });
    ro.observe(viewport);
  }
  window.addEventListener('resize', () => { if (settled) start(); });
}

function renderTree(root) {
  root.innerHTML = `
    ${pageHeader('tree.title', 'tree.lead')}
    <div class="tree-wrap">
      <div class="tree-legend">
        <div class="legend-item"><span class="legend-swatch" style="background:var(--wine);border-color:var(--wine);"></span>${escapeHtml(t('tree.legend_subject'))}</div>
        <div class="legend-item"><span class="legend-swatch" style="background:var(--accent-wash);border-color:var(--gold);"></span>${escapeHtml(t('tree.legend_survivor'))}</div>
        <div class="legend-item"><span class="legend-swatch" style="background:var(--paper-soft);border-style:dashed;"></span>${escapeHtml(t('ui.died'))}</div>
        <div class="legend-item legend-count" id="tree-count"></div>
      </div>
      <div class="tree-toolbar">
        <button class="filter-btn" data-tree="out" aria-label="${escapeHtml(t('tree.zoom_out'))}">−</button>
        <button class="filter-btn" data-tree="in" aria-label="${escapeHtml(t('tree.zoom_in'))}">+</button>
        <button class="filter-btn" data-tree="subject">${escapeHtml(t('tree.centre_subject'))}</button>
        <button class="filter-btn" data-tree="fit">${escapeHtml(t('tree.fit'))}</button>
        <span class="tree-hint">${escapeHtml(t('tree.pan_hint'))}</span>
      </div>
      <div id="tree-svg-container" class="tree-viewport"></div>
    </div>
  `;

  const host = root.querySelector('.tree-wrap');
  const viewport = document.getElementById('tree-svg-container');
  const svg = buildFamilyTreeSVG();
  viewport.appendChild(svg);
  document.getElementById('tree-count').textContent =
    `${State.data.people.length} ${t('ui.people_count').toLowerCase()}`;
  wireTreeViewport(svg, host);
}

function truncate(s, n) {
  if (!s) return '';
  return s.length > n ? s.slice(0, n - 1) + '…' : s;
}
function extractYear(s) {
  if (!s) return '?';
  const m = String(s).match(/(\d{4})/);
  return m ? m[1] : s;
}

// ----------------------------------------
// THE JOURNEY  (memoir set against the documents)
// ----------------------------------------
// A schematic map — true relative positions from the real coordinates, no
// basemap invented — plus a leg-by-leg reading of what Lusia wrote against
// what the documents show. Where they disagree, both are shown.

const JOURNEY = {
  W: 1000, H: 620, PAD: 46,
  R: 6,              // node radius
  SPREAD: 3.6,       // parallel offset between people sharing a leg
};

let _journeyCache = null, _outlineCache = null;
// Everyone is shown until the reader decides otherwise.
const JourneyState = { people: new Set(['david', 'lusia', 'shimon', 'dov']) };

async function loadJourney() {
  if (!_journeyCache) {
    const v = Date.now();
    const [j, o] = await Promise.all([
      fetch(`data/journey.json?v=${v}`, { cache: 'no-store' }).then(r => r.json()),
      fetch(`data/map_outlines.json?v=${v}`, { cache: 'no-store' }).then(r => r.json()).catch(() => null),
    ]);
    _journeyCache = j; _outlineCache = o;
  }
  return _journeyCache;
}

// Equirectangular, narrowed by the cosine of the mean latitude so the shape is
// not stretched sideways. Framed on the countries, not just on the stops, so
// Poland, Belgium, France, Cyprus and Israel are all actually on the page.
function journeyProjection() {
  const b = (_outlineCache && _outlineCache._schema.bbox) || { lon_min: 2, lat_min: 30, lon_max: 37, lat_max: 53 };
  const k = Math.cos(((b.lat_min + b.lat_max) / 2) * Math.PI / 180);
  const x0 = b.lon_min * k, x1 = b.lon_max * k, y0 = b.lat_min, y1 = b.lat_max;
  const w = JOURNEY.W - JOURNEY.PAD * 2, h = JOURNEY.H - JOURNEY.PAD * 2;
  const s = Math.min(w / (x1 - x0), h / (y1 - y0));
  const ox = JOURNEY.PAD + (w - (x1 - x0) * s) / 2;
  const oy = JOURNEY.PAD + (h - (y1 - y0) * s) / 2;
  return ([lat, lon]) => [ox + (lon * k - x0) * s, oy + (y1 - lat) * s];
}

function drawCountries(svg, project) {
  if (!_outlineCache) return;
  const g = svgEl('g', { class: 'journey-land' });
  svg.appendChild(g);
  const highlight = new Set(_outlineCache._schema.highlight || []);
  for (const [name, rings] of Object.entries(_outlineCache.countries)) {
    const cls = 'country' + (highlight.has(name) ? ' country-key' : '');
    for (const ring of rings) {
      const d = ring.map(([lon, lat], i) =>
        `${i ? 'L' : 'M'}${project([lat, lon]).map(n => n.toFixed(1)).join(',')}`).join(' ') + ' Z';
      const path = svgEl('path', { d, class: cls });
      const title = svgEl('title');
      title.textContent = name;
      path.appendChild(title);
      g.appendChild(path);
    }
  }
}

// Where several people walk the same leg, fan the lines apart so all of them
// stay visible — and so the convergence on Haifa reads as four lines arriving.
function offsetPolyline(pts, shift) {
  if (shift === 0 || pts.length < 2) return pts;
  return pts.map((p, i) => {
    const a = pts[Math.max(0, i - 1)], b = pts[Math.min(pts.length - 1, i + 1)];
    const dx = b[0] - a[0], dy = b[1] - a[1];
    const len = Math.hypot(dx, dy) || 1;
    return [p[0] - (dy / len) * shift, p[1] + (dx / len) * shift];
  });
}

function buildJourneyMap(data) {
  const project = journeyProjection();
  const svg = svgEl('svg', {
    class: 'journey-map', viewBox: `0 0 ${JOURNEY.W} ${JOURNEY.H}`, xmlns: SVGNS,
    role: 'img', 'aria-label': t('journey.map_alt'),
  });
  svg.setAttribute('direction', 'ltr');       // geography does not flip with the language

  drawCountries(svg, project);
  const lines = svgEl('g', { class: 'journey-lines' });
  const nodes = svgEl('g', { class: 'journey-nodes' });
  svg.appendChild(lines); svg.appendChild(nodes);

  const byDate = ls => ls.slice().sort((a, b) => (a.date || '').localeCompare(b.date || ''));
  const ids = Object.keys(data.people);

  // one line per person, through the legs they were actually on
  ids.forEach((pid, i) => {
    const legs = byDate(data.legs.filter(l => (l.people || []).includes(pid)));
    if (legs.length < 2) return;
    const shift = (i - (ids.length - 1) / 2) * JOURNEY.SPREAD;
    const pts = offsetPolyline(legs.map(l => project(l.coords)), shift);
    const d = pts.map(([x, y], n) => `${n ? 'L' : 'M'}${x.toFixed(1)},${y.toFixed(1)}`).join(' ');
    const path = svgEl('path', {
      d, class: `journey-route route-${pid}`, 'data-person': pid,
      stroke: data.people[pid].colour,
    });
    if (data.people[pid].dash !== 'none') path.setAttribute('stroke-dasharray', data.people[pid].dash);
    lines.appendChild(path);
  });

  // one marker per place
  const seen = new Map();
  for (const l of byDate(data.legs)) {
    const cur = seen.get(l.place_id) || { coords: l.coords, years: [], legs: [], people: new Set() };
    if (!cur.years.includes(l.year)) cur.years.push(l.year);
    cur.legs.push(l);
    (l.people || []).forEach(p => cur.people.add(p));
    seen.set(l.place_id, cur);
  }
  for (const [placeId, info] of seen) {
    const [x, y] = project(info.coords);
    const g = svgEl('g', {
      class: 'journey-node', 'data-place': placeId,
      'data-people': [...info.people].join(' '), tabindex: '0', role: 'button',
    });
    g.appendChild(svgEl('circle', { cx: x, cy: y, r: JOURNEY.R, class: 'journey-dot' }));
    const place = State.byId.places[placeId];
    const name = place
      ? ml(place.names).split(' (')[0].split(' / ')[0].split(',')[0].trim()
      : placeId;
    nodes.appendChild(g);
    const cap = svgEl('g', { class: 'journey-caption' });
    cap.dataset.cx = x; cap.dataset.cy = y;
    const label = svgEl('text', { x: 0, y: 0, class: 'journey-label' });
    label.textContent = name;
    cap.appendChild(label);
    const yrs = svgEl('text', { x: 0, y: 13, class: 'journey-years' });
    yrs.textContent = info.years.join(' · ');
    cap.appendChild(yrs);
    cap.setAttribute('transform', `translate(${x},${y - 16})`);
    g.appendChild(cap);
    const title = svgEl('title');
    title.textContent = `${name} — ${info.legs.map(l => ml(l.title)).join(' / ')}`;
    g.appendChild(title);
    const jump = () => {
      const el = document.getElementById('leg-' + info.legs[0].id);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        el.classList.add('leg-flash');
        setTimeout(() => el.classList.remove('leg-flash'), 1400);
      }
    };
    g.addEventListener('click', jump);
    g.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); jump(); } });
  }
  return svg;
}

// Show only the selected people: their lines, and the places they were at.
function applyJourneyFilter(scope) {
  const sel = JourneyState.people;
  scope.querySelectorAll('.journey-route').forEach(p => {
    p.classList.toggle('is-hidden', !sel.has(p.dataset.person));
  });
  scope.querySelectorAll('.journey-node').forEach(n => {
    const who = (n.dataset.people || '').split(' ').filter(Boolean);
    n.classList.toggle('is-hidden', !who.some(w => sel.has(w)));
  });
  scope.querySelectorAll('.journey-leg').forEach(l => {
    const who = (l.dataset.people || '').split(' ').filter(Boolean);
    l.classList.toggle('is-hidden', !who.some(w => sel.has(w)));
  });
  scope.querySelectorAll('[data-person-toggle]').forEach(b => {
    const on = sel.has(b.dataset.personToggle);
    b.classList.toggle('on', on);
    b.setAttribute('aria-pressed', String(on));
  });
}

// Place names on a small map collide — Galicia alone puts five towns within a
// few dozen pixels, and Atlit sits almost on top of Haifa. Measure once the map
// is in the document and give each caption the first offset that clears
// everything already placed.
//
// Note: getBBox() on a <g> reports its children in the group's OWN coordinate
// space, i.e. before the group's own translate — so every caption measures the
// same and nothing can be compared. getBoundingClientRect() is in screen space
// and includes the transform, which is what this needs.
function resolveJourneyCaptions(svg) {
  const caps = [...svg.querySelectorAll('.journey-caption')];
  if (!caps.length) return;
  const OFFSETS = [
    [0, -18], [0, 32], [0, -42], [0, 50],
    [62, -4], [-62, -4], [68, 24], [-68, 24],
    [0, -62], [0, 68], [92, -4], [-92, -4],
  ];
  const rect = el => {
    const r = el.getBoundingClientRect();
    return { x: r.left, y: r.top, w: r.width, h: r.height };
  };
  const hit = (a, b) =>
    a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h;

  // Markers are obstacles too — a caption must never sit on a dot.
  const placed = [...svg.querySelectorAll('.journey-dot')].map(rect);
  // Widest captions first; they are the hardest to fit.
  const order = caps.slice().sort((a, b) => rect(b).width - rect(a).width);

  for (const cap of order) {
    const cx = Number(cap.dataset.cx), cy = Number(cap.dataset.cy);
    let chosen = OFFSETS[0];
    for (const off of OFFSETS) {
      cap.setAttribute('transform', `translate(${cx + off[0]},${cy + off[1]})`);
      if (!placed.some(p => hit(rect(cap), p))) { chosen = off; break; }
    }
    cap.setAttribute('transform', `translate(${cx + chosen[0]},${cy + chosen[1]})`);
    placed.push(rect(cap));
    if (Math.abs(chosen[0]) > 20 || Math.abs(chosen[1]) > 36) {
      svg.querySelector('.journey-lines').appendChild(svgEl('line', {
        x1: cx, y1: cy,
        x2: cx + chosen[0], y2: cy + chosen[1] + (chosen[1] > 0 ? -6 : 6),
        class: 'journey-leader',
      }));
    }
  }
}

// ----------------------------------------
// THE STORY — the whole thing read straight through, rather than as 45 separate
// timeline cards. Every paragraph shows the record it rests on, and the places
// where the memoir and the documents disagree are marked in the text instead of
// being quietly resolved.
// ----------------------------------------
let _storyCache = null;

async function loadStory() {
  if (!_storyCache) {
    _storyCache = await fetch(`data/narrative.json?v=${Date.now()}`, { cache: 'no-store' })
      .then(r => r.json());
  }
  return _storyCache;
}

// ----------------------------------------
// THE PHOTOGRAPHS  (the plates printed in Lusia's memoir)
// ----------------------------------------
// Separate from #/memoir, which upload-feature.js intercepts to render the whole
// book as a PDF flipbook. This page is the thirteen photographs pulled out of it
// — extracted, descreened, and shown under the caption the book prints beneath
// each one, with what the archive knows kept visibly apart from what the book
// says. Do NOT route this at #/memoir: the flipbook's own router runs on
// hashchange and would overwrite whatever this drew.
let _memoirCache = null;
async function loadMemoirPhotos() {
  if (!_memoirCache) {
    _memoirCache = await fetch(`data/memoir_photographs.json?v=${Date.now()}`, { cache: 'no-store' })
      .then(r => r.json());
  }
  return _memoirCache;
}

function renderPhotographs(root) {
  root.innerHTML = `${pageHeader('memoir.title', 'memoir.lead')}<div id="memoir-body"><p class="muted">${escapeHtml(t('ui.loading'))}</p></div>`;

  loadMemoirPhotos().then(data => {
    const body = document.getElementById('memoir-body');
    if (!body) return;

    body.innerHTML = `
      <p class="story-note">${escapeHtml(t('memoir.processing_note'))}</p>
      <div class="memoir-gallery">
        ${(data.photographs || []).map(ph => {
          // The book's caption is Hebrew. Show it as the book wrote it, and the
          // translation beside it — never instead of it.
          const printed = (ph.caption_as_printed || {});
          const asPrinted = printed.he || '';
          const translated = printed[State.lang] || printed.en || '';
          const showBoth = State.lang !== 'he' && asPrinted && translated;
          const people = (ph.people || [])
            .map(id => State.byId.people[id])
            .filter(Boolean);
          return `
            <figure class="memoir-plate">
              <a href="${escapeHtml(ph.file)}" target="_blank" rel="noopener">
                <img src="${escapeHtml(ph.file)}" alt="${escapeHtml(translated)}" loading="lazy">
              </a>
              <figcaption>
                <div class="memoir-page">${/^\d+$/.test(String(ph.page))
                  ? escapeHtml(t('memoir.page_label')) + ' ' + escapeHtml(String(ph.page))
                  : escapeHtml(t('memoir.back_cover'))}</div>
                <div class="memoir-printed" dir="rtl" lang="he">${escapeHtml(asPrinted)}</div>
                ${showBoth ? `<div class="memoir-translated" dir="auto">${escapeHtml(translated)}</div>` : ''}
                <p class="memoir-note" dir="auto">${escapeHtml(ml(ph.note))}</p>
                ${people.length ? `<div class="memoir-people">${people.map(p =>
                  `<button class="memoir-person" data-person="${escapeHtml(p.id)}">${escapeHtml(ml(p.primary_name))}</button>`
                ).join('')}</div>` : ''}
              </figcaption>
            </figure>`;
        }).join('')}
      </div>`;

    body.querySelectorAll('[data-person]').forEach(el => {
      el.addEventListener('click', () => openPersonModal(el.dataset.person));
    });
  }).catch(() => {
    const body = document.getElementById('memoir-body');
    if (body) body.innerHTML = `<p class="muted">${escapeHtml(t('ui.error') || 'Could not load the memoir photographs.')}</p>`;
  });
}

function renderStory(root) {
  root.innerHTML = `${pageHeader('story.title', 'story.lead')}<div id="story-body"><p class="muted">${escapeHtml(t('ui.loading'))}</p></div>`;

  loadStory().then(data => {
    const body = document.getElementById('story-body');
    if (!body) return;
    const kindLabel = { conflict: t('story.kind_conflict'), testimony: t('story.kind_testimony') };

    body.innerHTML = `
      <p class="story-note">${escapeHtml(ml(data.note))}</p>
      <nav class="story-toc">
        ${data.chapters.map(c => `<a href="#story-${escapeHtml(c.id)}">${escapeHtml(ml(c.title))}</a>`).join('')}
      </nav>
      ${data.chapters.map(c => `
        <section class="story-chapter" id="story-${escapeHtml(c.id)}">
          <h2>${escapeHtml(ml(c.title))}<span class="story-years">${escapeHtml(c.years || '')}</span></h2>
          ${c.paragraphs.map(p => `
            <div class="story-para${p.kind && p.kind !== 'fact' ? ' story-' + escapeHtml(p.kind) : ''}">
              ${p.kind && kindLabel[p.kind] ? `<span class="story-tag">${escapeHtml(kindLabel[p.kind])}</span>` : ''}
              <p>${escapeHtml(ml(p.text))}</p>
              ${(p.sources || []).length ? `<p class="story-src">${escapeHtml((p.sources || []).join(' · '))}</p>` : ''}
            </div>
          `).join('')}
        </section>
      `).join('')}
    `;
  }).catch(() => {
    const body = document.getElementById('story-body');
    if (body) body.innerHTML = `<p class="muted">${escapeHtml(t('ui.error') || 'Could not load the story.')}</p>`;
  });
}

function renderJourney(root) {
  root.innerHTML = `${pageHeader('journey.title', 'journey.lead')}<div id="journey-body"><p class="muted">${escapeHtml(t('ui.loading'))}</p></div>`;

  loadJourney().then(data => {
    const body = document.getElementById('journey-body');
    if (!body) return;

    const agreements = ['confirmed', 'corrected', 'memoir_only', 'context'];
    const people = Object.entries(data.people);

    body.innerHTML = `
      <p class="journey-hint">${escapeHtml(t('journey.pick_hint'))}</p>
      <div class="journey-people">
        ${people.map(([id, p]) => `
          <button class="person-toggle on" data-person-toggle="${escapeHtml(id)}"
                  aria-pressed="true" style="--person: ${escapeHtml(p.colour)}">
            <span class="person-line"></span>${escapeHtml(ml(p.name))}
          </button>
        `).join('')}
        <button class="person-toggle person-all" data-person-all>${escapeHtml(t('journey.show_all'))}</button>
      </div>
      <div class="journey-map-wrap" id="journey-map-wrap"></div>
      <div class="journey-key">
        ${agreements.map(a => `
          <span class="legend-item"><span class="badge agree-${a}">${escapeHtml(t('journey.agree_' + a))}</span></span>
        `).join('')}
      </div>
      <div class="journey-legs">
        ${data.legs.map(l => {
          const place = State.byId.places[l.place_id];
          const docs = (l.evidence.documents || []).map(id => State.byId.documents[id]).filter(Boolean);
          return `
          <article class="journey-leg" id="leg-${escapeHtml(l.id)}" data-people="${escapeHtml((l.people || []).join(' '))}">
            <div class="leg-rail">
              <span class="leg-year">${escapeHtml(l.year)}</span>
              <span class="leg-place">${escapeHtml(place ? ml(place.names).split(' (')[0] : '')}</span>
              <span class="leg-who">${(l.people || []).map(pid => `
                <i class="who-dot" style="--person:${escapeHtml((data.people[pid] || {}).colour || '#000')}"
                   title="${escapeHtml(ml((data.people[pid] || {}).name || {}))}"></i>`).join('')}</span>
            </div>
            <div class="leg-body">
              <div class="leg-head">
                <h3>${escapeHtml(ml(l.title))}</h3>
                <span class="badge agree-${escapeHtml(l.agreement)}">${escapeHtml(t('journey.agree_' + l.agreement))}</span>
              </div>
              <div class="leg-cols">
                <div class="leg-col leg-memoir">
                  <h4>${escapeHtml(t('journey.memoir_says'))}${l.memoir.page ? ` <span class="leg-page">${escapeHtml(t('journey.page'))} ${l.memoir.page}</span>` : ''}</h4>
                  <p>${escapeHtml(ml(l.memoir.says))}</p>
                </div>
                <div class="leg-col leg-evidence">
                  <h4>${escapeHtml(t('journey.documents_say'))}</h4>
                  <p>${escapeHtml(ml(l.evidence.says))}</p>
                  ${docs.length ? `<div class="leg-docs">${docs.map(d => `
                    <a href="#/documents/${escapeHtml(d.id)}" class="leg-doc" data-link>${escapeHtml(ml(d.title))}</a>
                  `).join('')}</div>` : `<p class="leg-nodoc">${escapeHtml(t('journey.no_document'))}</p>`}
                </div>
              </div>
              ${l.note ? `<p class="leg-note">${escapeHtml(ml(l.note))}</p>` : ''}
              ${l.open_question ? `<p class="leg-open"><a href="#/hypotheses" data-link>${escapeHtml(t('journey.still_open'))}</a></p>` : ''}
            </div>
          </article>`;
        }).join('')}
      </div>
    `;

    const map = buildJourneyMap(data);
    document.getElementById('journey-map-wrap').appendChild(map);
    // Only now that it is in the document can the captions be measured, so the
    // collision pass runs here rather than while building.
    resolveJourneyCaptions(map);

    // Pick a person to follow them alone; pick all four and they converge on Haifa.
    body.querySelectorAll('[data-person-toggle]').forEach(btn => {
      btn.addEventListener('click', () => {
        const id = btn.dataset.personToggle;
        if (JourneyState.people.has(id)) JourneyState.people.delete(id);
        else JourneyState.people.add(id);
        if (!JourneyState.people.size) Object.keys(data.people).forEach(k => JourneyState.people.add(k));
        applyJourneyFilter(body);
      });
    });
    body.querySelector('[data-person-all]').addEventListener('click', () => {
      Object.keys(data.people).forEach(k => JourneyState.people.add(k));
      applyJourneyFilter(body);
    });
    applyJourneyFilter(body);
  }).catch(err => {
    const body = document.getElementById('journey-body');
    if (body) body.innerHTML = `<p class="muted">${escapeHtml(String(err.message || err))}</p>`;
  });
}

// ----------------------------------------
// TIMELINE
// ----------------------------------------
const TimelineState = { filter: 'family' };

function renderTimeline(root) {
  root.innerHTML = `
    ${pageHeader('timeline.title', 'timeline.lead')}
    <div class="timeline-controls">
      <button class="filter-btn" data-tlfilter="all">${escapeHtml(t('timeline.filter_all'))}</button>
      <button class="filter-btn" data-tlfilter="family">${escapeHtml(t('timeline.filter_family'))}</button>
      <button class="filter-btn" data-tlfilter="context">${escapeHtml(t('timeline.filter_context'))}</button>
      <button class="filter-btn" data-tlfilter="discoveries">${escapeHtml(t('timeline.filter_discoveries'))}</button>
    </div>
    <div id="timeline-list" class="timeline"></div>
  `;

  document.querySelectorAll('[data-tlfilter]').forEach(b => {
    b.classList.toggle('active', b.dataset.tlfilter === TimelineState.filter);
    b.addEventListener('click', () => {
      TimelineState.filter = b.dataset.tlfilter;
      renderTimelineList();
      document.querySelectorAll('[data-tlfilter]').forEach(x => x.classList.toggle('active', x.dataset.tlfilter === TimelineState.filter));
    });
  });

  renderTimelineList();
}

function renderTimelineList() {
  const list = document.getElementById('timeline-list');
  let events = [...State.data.events].sort((a,b) => a.date_sort.localeCompare(b.date_sort));
  if (TimelineState.filter === 'family') events = events.filter(e => e.type !== 'context');
  else if (TimelineState.filter === 'context') {} // keep all
  else if (TimelineState.filter === 'discoveries') events = events.filter(e => e.type === 'discovery');
  // 'all' = all

  let currentDecade = null;
  const html = [];
  for (const e of events) {
    const year = parseInt(extractYear(e.date_sort));
    const decade = year ? Math.floor(year/10)*10 : null;
    if (decade !== currentDecade) {
      currentDecade = decade;
      // "1880s" is English. Use the same decade phrasing as the dates below it.
      html.push(`<div class="tl-decade-marker">${escapeHtml(t('ui.decade').replace('{decade}', currentDecade))}</div>`);
    }
    const place = e.place_id ? State.byId.places[e.place_id] : null;
    const people = (e.people_ids || []).map(pid => {
      const p = State.byId.people[pid];
      return p ? ml(p.primary_name) : null;
    }).filter(Boolean);
    html.push(`
      <div class="tl-event ${escapeHtml(e.type)}" data-event="${escapeHtml(e.id)}">
        <div class="tl-event-date">${escapeHtml(fmtDate(e.date))} · ${escapeHtml(t('event_type.' + e.type))}</div>
        <div class="tl-event-title">${escapeHtml(ml(e.title))}</div>
        <div class="tl-event-desc">${escapeHtml(ml(e.description))}</div>
        <div class="tl-event-meta">
          ${place ? `<span class="pill">📍 ${escapeHtml(ml(place.names))}</span>` : ''}
          ${people.length ? `<span class="pill">👤 ${escapeHtml(people.join(', '))}</span>` : ''}
          ${e.confidence ? `<span class="badge confidence-${escapeHtml(e.confidence)}">${escapeHtml(t('confidence.' + e.confidence))}</span>` : ''}
        </div>
      </div>
    `);
  }
  list.innerHTML = html.join('');
  list.querySelectorAll('.tl-event').forEach(el => {
    el.addEventListener('click', () => openEventModal(el.dataset.event));
  });
}

// ----------------------------------------
// PEOPLE
// ----------------------------------------
function renderPeople(root, paramId) {
  if (paramId && State.byId.people[paramId]) {
    openPersonModal(paramId);
  }
  // CHRONOLOGICAL ORDER: oldest at top, youngest at bottom.
  // Anyone without a birth year goes to a separate "no birth date yet" group
  // at the bottom (kept in role order so living relatives stay together).
  function birthYear(p) {
    const raw = p.birth?.date;
    if (!raw) return null;
    // Accept formats: "1911-12-25", "1502", "c.1280", "1928-09-08", etc.
    const m = String(raw).match(/-?\d{3,4}/);
    return m ? parseInt(m[0], 10) : null;
  }
  const withYear = [];
  const withoutYear = [];
  for (const p of State.data.people) {
    const y = birthYear(p);
    if (y == null) withoutYear.push(p);
    else withYear.push({ p, y });
  }
  withYear.sort((a, b) => a.y - b.y);
  const dated = withYear.map(o => o.p);

  // Within "no birth date yet" keep an intuitive role-grouping
  const roleOrder = ['subject_father','self','mother','sister','brother','spouse',
    'uncle','aunt','grandchild','cousin','first_cousin','first_cousin_once_removed',
    'second_cousin','third_cousin','living_cousin','living_cousin_in_law',
    'cousin_in_law','first_cousin_in_law','great_aunt','great_uncle'];
  withoutYear.sort((a, b) => (roleOrder.indexOf(a.role) === -1 ? 999 : roleOrder.indexOf(a.role)) -
                              (roleOrder.indexOf(b.role) === -1 ? 999 : roleOrder.indexOf(b.role)));

  const renderCard = (p) => `
    <div class="person-card" data-person="${escapeHtml(p.id)}">
      <div class="person-name-big">${escapeHtml(ml(p.primary_name))}</div>
      <div class="person-role">${escapeHtml(roleLabel(p.role))}</div>
      <div class="person-dates">
        ${escapeHtml(fmtDateRange(p))}
      </div>
      ${p.note_en ? `<div class="person-note" dir="auto">${escapeHtml(p.note_en)}</div>` : ''}
    </div>`;

  const lang = State.lang;
  const datedHeader = lang === 'he' ? 'בסדר כרונולוגי — מהמוקדם ביותר' : 'In chronological order — oldest first';
  const undatedHeader = lang === 'he' ? 'משפחה חיה (תאריכי לידה טרם נרשמו)' : 'Living family (birth dates pending)';

  root.innerHTML = `
    ${pageHeader('people_page.title', 'people_page.lead')}
    <h3 class="section-title" style="margin-top:1.5rem;">${escapeHtml(datedHeader)} <span style="font-family:var(--font-mono);font-size:0.8rem;color:var(--ink-faint);">(${dated.length})</span></h3>
    <div class="people-grid">${dated.map(renderCard).join('')}</div>
    ${withoutYear.length ? `
      <h3 class="section-title" style="margin-top:2.5rem;">${escapeHtml(undatedHeader)} <span style="font-family:var(--font-mono);font-size:0.8rem;color:var(--ink-faint);">(${withoutYear.length})</span></h3>
      <div class="people-grid">${withoutYear.map(renderCard).join('')}</div>
    ` : ''}
  `;
  root.querySelectorAll('[data-person]').forEach(el => {
    el.addEventListener('click', () => openPersonModal(el.dataset.person));
  });
}

function roleLabel(role) {
  return role.replace(/_/g, ' ');
}

// 65 of the 122 people have no recorded birth date — the living family, the
// rescuers, relatives known only from a marriage register. Printing "?" against
// each of them said nothing except that a field was empty, and the section
// heading already explains why. Show what we have; say nothing where we have
// nothing.
function fmtDateRange(p) {
  const b = p.birth?.date ? extractYear(p.birth.date) : '';
  const d = p.death?.date ? extractYear(p.death.date) : '';
  const bPlace = p.birth?.place_id ? ml(State.byId.places[p.birth.place_id]?.names) : '';
  let out = '';
  if (b && d) out = `${b} — ${d}`;
  else if (b) out = b;
  else if (d) out = `${t('ui.died')} ${d}`;
  if (bPlace) out = out ? `${out} · ${bPlace.split(' (')[0]}` : bPlace.split(' (')[0];
  return out;
}

function openPersonModal(id) {
  const p = State.byId.people[id];
  if (!p) return;
  const father = p.father_id ? State.byId.people[p.father_id] : null;
  const mother = p.mother_id ? State.byId.people[p.mother_id] : null;
  const spouse = p.spouse_id ? State.byId.people[p.spouse_id] : null;
  const children = (p.children_ids || []).map(cid => State.byId.people[cid]).filter(Boolean);
  const siblings = State.data.people.filter(x =>
    x.id !== p.id && ((p.father_id && x.father_id === p.father_id) || (p.mother_id && x.mother_id === p.mother_id))
  );

  const facts = p.facts || [];
  const birthPlace = p.birth?.place_id ? State.byId.places[p.birth.place_id] : null;
  const deathPlace = p.death?.place_id ? State.byId.places[p.death.place_id] : null;

  let html = `
    ${p.photo ? `<figure class="detail-portrait">
      <a href="${escapeHtml(p.photo)}" target="_blank" rel="noopener">
        <img src="${escapeHtml(p.photo)}" alt="${escapeHtml(ml(p.primary_name))}" loading="lazy">
      </a>
      ${p.photo_caption ? `<figcaption>${escapeHtml(ml(p.photo_caption))}</figcaption>` : ''}
      ${p.photo_credit ? `<figcaption class="muted" style="font-size:0.72rem;margin-top:0.35rem;">${escapeHtml(p.photo_credit)}</figcaption>` : ''}
    </figure>` : ''}
    <div class="detail-name">${escapeHtml(ml(p.primary_name))}</div>
    ${p.aliases?.length ? `<div class="detail-aliases">${escapeHtml(p.aliases.join(' · '))}</div>` : ''}
    <div class="muted" style="margin-bottom:1rem;font-family:var(--font-mono);font-size:0.78rem;text-transform:uppercase;letter-spacing:0.08em;">${escapeHtml(roleLabel(p.role))}</div>
    ${(() => {
      // Notes were written in English and rendered as-is, so a Hebrew reader got
      // an English paragraph in the middle of an RTL page. Prefer their own
      // language; fall back to English and say plainly that it is a fallback.
      const note = p['note_' + State.lang] || p.note_en;
      if (!note) return '';
      const isFallback = !p['note_' + State.lang] && State.lang !== 'en';
      return `<p dir="auto" style="font-family:var(--font-serif);font-size:1.05rem;line-height:1.6;color:var(--ink-soft);">${escapeHtml(note)}</p>` +
        (isFallback ? `<p class="muted" style="font-size:0.78rem;margin-top:-0.4rem;">${escapeHtml(t('ui.en_fallback'))}</p>` : '');
    })()}

    <div class="detail-section">
      <h4>${escapeHtml(t('ui.born'))} / ${escapeHtml(t('ui.died'))}</h4>
      ${p.birth ? `
        <div class="detail-fact">
          <div class="detail-fact-label">${escapeHtml(t('ui.born'))}</div>
          <div class="detail-fact-val">
            ${escapeHtml(fmtDate(p.birth.date))}${birthPlace ? ' · ' + escapeHtml(ml(birthPlace.names)) : ''}
            ${p.birth.confidence ? `<span class="badge confidence-${escapeHtml(p.birth.confidence)}">${escapeHtml(t('confidence.' + p.birth.confidence))}</span>` : ''}
          </div>
        </div>
      ` : ''}
      ${p.death ? `
        <div class="detail-fact">
          <div class="detail-fact-label">${escapeHtml(t('ui.died'))}</div>
          <div class="detail-fact-val">
            ${escapeHtml(fmtDate(p.death.date))}${deathPlace ? ' · ' + escapeHtml(ml(deathPlace.names)) : ''}
            ${p.death.confidence ? `<span class="badge confidence-${escapeHtml(p.death.confidence)}">${escapeHtml(t('confidence.' + p.death.confidence))}</span>` : ''}
          </div>
        </div>
      ` : ''}
    </div>

    <div class="detail-section">
      <h4>${escapeHtml(t('people_page.relationships'))}</h4>
      ${father ? `<div class="detail-fact"><div class="detail-fact-label">${escapeHtml(t('ui.father'))}</div><div class="detail-fact-val"><a href="#" data-person="${escapeHtml(father.id)}">${escapeHtml(ml(father.primary_name))}</a></div></div>` : ''}
      ${mother ? `<div class="detail-fact"><div class="detail-fact-label">${escapeHtml(t('ui.mother'))}</div><div class="detail-fact-val"><a href="#" data-person="${escapeHtml(mother.id)}">${escapeHtml(ml(mother.primary_name))}</a></div></div>` : ''}
      ${spouse ? `<div class="detail-fact"><div class="detail-fact-label">${escapeHtml(t('ui.spouse'))}</div><div class="detail-fact-val"><a href="#" data-person="${escapeHtml(spouse.id)}">${escapeHtml(ml(spouse.primary_name))}</a></div></div>` : ''}
      ${siblings.length ? `<div class="detail-fact"><div class="detail-fact-label">${escapeHtml(t('ui.siblings'))}</div><div class="detail-fact-val">${siblings.map(s => `<a href="#" data-person="${escapeHtml(s.id)}">${escapeHtml(ml(s.primary_name))}</a>`).join(' · ')}</div></div>` : ''}
      ${children.length ? `<div class="detail-fact"><div class="detail-fact-label">${escapeHtml(t('ui.children'))}</div><div class="detail-fact-val">${children.map(c => `<a href="#" data-person="${escapeHtml(c.id)}">${escapeHtml(ml(c.primary_name))}</a>`).join(' · ')}</div></div>` : ''}
    </div>

    ${facts.length ? `
      <div class="detail-section">
        <h4>${escapeHtml(t('people_page.facts'))}</h4>
        ${facts.map(f => `
          <div class="detail-fact">
            <div class="detail-fact-label">${escapeHtml(ml(f.label_ml || {}) || f.label || '')}</div>
            <div class="detail-fact-val" dir="auto">
              ${escapeHtml(f['value_' + State.lang] || f.value || ml(f.text || {}) || '')}
              ${f.confidence ? `<span class="badge confidence-${escapeHtml(f.confidence)}">${escapeHtml(t('confidence.' + f.confidence))}</span>` : ''}
            </div>
          </div>
        `).join('')}
      </div>
    ` : ''}
  `;

  showModal(html);
  // Wire up cross-links inside modal
  document.querySelectorAll('#modal [data-person]').forEach(el => {
    el.addEventListener('click', (e) => {
      e.preventDefault();
      openPersonModal(el.dataset.person);
    });
  });
}

// ----------------------------------------
// PLACES
// ----------------------------------------
function renderPlaces(root, paramId) {
  root.innerHTML = `
    ${pageHeader('places_page.title', 'places_page.lead')}
    <div class="places-grid">
      ${State.data.places.map(p => `
        <div class="place-card" data-place="${escapeHtml(p.id)}">
          <div class="person-name-big">${escapeHtml(ml(p.names))}</div>
          ${p.coords ? `<div class="place-coords">${p.coords[0].toFixed(4)}, ${p.coords[1].toFixed(4)}</div>` : ''}
          ${p.significance ? `<p dir="auto" style="margin-top:0.6em;font-size:0.92rem;color:var(--ink-soft);line-height:1.5;">${escapeHtml(p['significance_' + State.lang] || p.significance)}</p>` : ''}
          ${p.building_now ? `<div style="margin-top:0.5em;font-size:0.9rem;font-family:var(--font-mono);color:var(--accent);"><strong>${escapeHtml(t('nav.address_today'))}:</strong> ${escapeHtml(p.building_now)}</div>` : ''}
          ${p.era_context ? `
            <div class="place-eras">
              ${Object.entries(p.era_context).map(([period, txt]) => `
                <div class="place-era"><span class="place-era-period">${escapeHtml(period.replace(/_/g, '–'))}</span>${escapeHtml(txt)}</div>
              `).join('')}
            </div>
          ` : ''}
          ${placeImages(p)}
        </div>
      `).join('')}
    </div>
  `;

  root.querySelectorAll('.place-photo').forEach(el => {
    el.addEventListener('click', () => openPlacePhoto(el.dataset.place, +el.dataset.idx));
  });
}

// Photographs of the towns themselves. The split is the whole point: a picture
// taken while they lived there is evidence, and a picture of the same street in
// 2015 is not. They are never mixed, and every one states when it was taken —
// "date not stated" where the source gives none, rather than a plausible guess.
function placeImages(p) {
  const imgs = p.images || [];
  if (!imgs.length) return '';
  const cap = i => (State.lang === 'he' && i.caption_he) ? i.caption_he : (i.caption_en || '');
  const strip = (list, labelKey) => !list.length ? '' : `
    <div class="place-photo-group">
      <div class="place-photo-label">${escapeHtml(t(labelKey))}</div>
      <div class="place-photo-strip">
        ${list.map(i => `
          <button class="place-photo" data-place="${escapeHtml(p.id)}" data-idx="${imgs.indexOf(i)}"
                  title="${escapeHtml(cap(i))}">
            <img src="${escapeHtml(i.src)}" alt="${escapeHtml(cap(i))}" loading="lazy">
            <span class="place-photo-when">${escapeHtml(i.when || '')}</span>
          </button>`).join('')}
      </div>
    </div>`;
  return strip(imgs.filter(i => i.is_period), 'places_page.then')
       + strip(imgs.filter(i => !i.is_period), 'places_page.now');
}

function openPlacePhoto(placeId, idx) {
  const p = State.byId.places[placeId];
  const im = p && (p.images || [])[idx];
  if (!im) return;
  const cap = (State.lang === 'he' && im.caption_he) ? im.caption_he : (im.caption_en || '');
  showModal(`
    <div class="doc-kind" style="font-family:var(--font-mono);font-size:0.78rem;color:var(--wine);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.3em;">${escapeHtml(ml(p.names))} · ${escapeHtml(im.when || '')}</div>
    <img src="${escapeHtml(im.src)}" alt="${escapeHtml(cap)}" style="width:100%;height:auto;border-radius:var(--radius);margin:0.8rem 0;">
    <p dir="auto" style="font-family:var(--font-serif);line-height:1.6;">${escapeHtml(cap)}</p>
    ${im.credit ? `<p class="muted" style="font-size:0.78rem;">${escapeHtml(im.credit)}</p>` : ''}
    ${!im.is_period ? `<p class="muted" style="font-size:0.8rem;font-style:italic;">${escapeHtml(t('places_page.now_warning'))}</p>` : ''}
  `);
}

// ----------------------------------------
// DOCUMENTS
// ----------------------------------------
const DocState = { search: '', kind: 'all' };

function renderDocuments(root, paramId) {
  // All docs from documents.json + entries from additional_files (so every WhatsApp file appears)
  const fullDocs = State.data.documents.slice();
  const additional = State.data.additional_files || [];
  // Build pseudo-docs for additional files so they show up on the page
  const additionalDocs = additional.map((f, idx) => ({
    id: 'add_' + idx,
    file_pages: [f.file],
    kind: f.file.match(/\.pdf$/i) ? 'pdf' : f.file.match(/\.(jpg|jpeg|png|webp|gif)$/i) ? 'image' : 'file',
    type: 'whatsapp_attachment',
    title: { en: f.file },
    summary: { en: f.description || '' },
    _isAdditional: true,
  }));
  const allDocs = fullDocs.concat(additionalDocs);

  // Filter logic
  const q = (DocState.search || '').trim().toLowerCase();
  const kf = DocState.kind || 'all';
  const filtered = allDocs.filter(d => {
    if (kf !== 'all') {
      if (kf === 'image' && !(d.kind === 'image' || d.kind === 'composite')) return false;
      if (kf === 'pdf' && d.kind !== 'pdf') return false;
      if (kf === 'external' && d.kind !== 'external_source') return false;
      if (kf === 'attachment' && !d._isAdditional) return false;
    }
    if (!q) return true;
    const hay = foldText([
      ml(d.title), d.type, d.kind,
      ml(d.summary), d.source_archive,
      (d.file_pages || []).join(' '),
      Object.values(d.decoded_fields || {}).join(' '),
      Object.values(d.key_quotes || {}).join(' '),
    ].join(' '));
    return hay.includes(foldText(q));
  });

  const kindCounts = {
    all: allDocs.length,
    image: allDocs.filter(d => d.kind === 'image' || d.kind === 'composite').length,
    pdf: allDocs.filter(d => d.kind === 'pdf').length,
    external: allDocs.filter(d => d.kind === 'external_source').length,
    attachment: additionalDocs.length,
  };

  root.innerHTML = `
    ${pageHeader('documents.title', 'documents.lead')}
    <div class="docs-controls" style="display:flex;gap:0.6rem;flex-wrap:wrap;margin-bottom:1rem;align-items:center;">
      <input class="chat-search" type="search" id="docs-search" placeholder="${escapeHtml(t('ui.search'))}…" value="${escapeHtml(DocState.search)}" style="flex:1;min-width:200px;" />
      <button class="filter-btn ${kf==='all'?'active':''}" data-docfilter="all">${escapeHtml(t('ui.all') || 'All')} (${kindCounts.all})</button>
      <button class="filter-btn ${kf==='image'?'active':''}" data-docfilter="image">🖼️ ${kindCounts.image}</button>
      <button class="filter-btn ${kf==='pdf'?'active':''}" data-docfilter="pdf">📄 ${kindCounts.pdf}</button>
      <button class="filter-btn ${kf==='external'?'active':''}" data-docfilter="external">🔗 ${kindCounts.external}</button>
      <button class="filter-btn ${kf==='attachment'?'active':''}" data-docfilter="attachment">📎 ${kindCounts.attachment}</button>
    </div>
    <div class="documents-grid">
      ${filtered.map(d => {
        const thumb = pickDocThumb(d);
        const files = d.file_pages || [];
        const summary = ml(d.summary) || '';
        const summarySnip = summary ? (summary.length > 220 ? summary.slice(0, 220) + '…' : summary) : '';
        const fileCount = files.length;
        const typeLabel = (t('doc_type.' + d.type) !== 'doc_type.' + d.type) ? t('doc_type.' + d.type) : d.type;
        return `
          <div class="doc-card" data-doc="${escapeHtml(d.id)}">
            <div class="doc-thumb">
              ${thumb ? `<img src="${escapeHtml(thumb)}" alt="" loading="lazy" />` : `<div class="doc-thumb-placeholder">${escapeHtml(d.kind === 'pdf' ? '📄 PDF' : d.kind === 'external_source' ? '🔗' : d.kind || 'document')}</div>`}
              ${fileCount > 1 ? `<span class="doc-thumb-count">${fileCount} pages</span>` : ''}
            </div>
            <div class="doc-info">
              <div class="doc-kind">${escapeHtml(typeLabel)}${d.primary_language ? ' · ' + escapeHtml(d.primary_language.toUpperCase()) : ''}${d._isAdditional ? ' · 📎' : ''}</div>
              <h4 class="doc-title">${escapeHtml(ml(d.title) || files[0] || d.id)}</h4>
              ${summarySnip ? `<p class="doc-summary-snip">${escapeHtml(summarySnip)}</p>` : ''}
              ${files.length ? `<div class="doc-files-list">${files.slice(0, 3).map(f => `<span class="doc-file-chip">${escapeHtml(f.length > 36 ? f.slice(0, 33) + '…' : f)}</span>`).join('')}${files.length > 3 ? `<span class="doc-file-chip">+${files.length - 3}</span>` : ''}</div>` : ''}
            </div>
          </div>
        `;
      }).join('') || `<div style="padding:2rem;text-align:center;color:var(--muted);grid-column:1/-1;">${escapeHtml(t('ui.no_results'))}</div>`}
    </div>
  `;
  root.querySelectorAll('[data-doc]').forEach(el => {
    el.addEventListener('click', () => openDocModal(el.dataset.doc));
  });
  const searchEl = document.getElementById('docs-search');
  if (searchEl) {
    searchEl.addEventListener('input', e => {
      DocState.search = e.target.value;
      renderDocuments(root, paramId);
    });
  }
  root.querySelectorAll('[data-docfilter]').forEach(b => {
    b.addEventListener('click', () => {
      DocState.kind = b.dataset.docfilter;
      renderDocuments(root, paramId);
    });
  });
  if (paramId && State.byId.documents[paramId]) openDocModal(paramId);
}

function pickDocThumb(d) {
  // Prefer image; for PDFs we can't easily thumbnail so we use a placeholder.
  const f = (d.file_pages || [])[0];
  if (!f) return null;
  if (f.match(/\.(jpg|jpeg|png|webp|gif)$/i)) {
    return 'assets/documents/' + encodeURI(f);
  }
  return null;
}

function openDocModal(id) {
  const d = State.byId.documents[id];
  if (!d) return;

  // Build source preview (one or more images / PDFs)
  const files = d.file_pages || [];
  let sourceHTML = '<div class="doc-source-multi">';
  for (const f of files) {
    const path = 'assets/documents/' + encodeURI(f);
    if (f.match(/\.(jpg|jpeg|png|webp|gif)$/i)) {
      sourceHTML += `<div><img src="${escapeHtml(path)}" alt="${escapeHtml(f)}" data-file="${escapeHtml(f)}" /><div class="doc-source-caption">${escapeHtml(f)}</div></div>`;
    } else if (f.match(/\.pdf$/i)) {
      sourceHTML += `<div><embed src="${escapeHtml(path)}" type="application/pdf" /><div class="doc-source-caption">${escapeHtml(f)}</div></div>`;
    } else {
      sourceHTML += `<div class="doc-source-caption">${escapeHtml(f)}</div>`;
    }
  }
  sourceHTML += '</div>';

  // Translations tabs
  const tabs = ['en', 'he', 'pl', 'fr'];
  const langLabel = { en: 'EN', he: 'עב', pl: 'PL', fr: 'FR' };

  // Decoded fields, if any
  const decoded = d.decoded_fields || null;

  // Notes
  const notes = d.transcription_notes || d.notes || null;

  // t() returns the key itself when a string is missing, so `t(k) || fallback`
  // never falls back. Compare against the key, the way the card list does.
  const typeKey = 'doc_type.' + d.type;
  const typeLabel = t(typeKey) !== typeKey ? t(typeKey) : d.type;

  // The summary is the archive's reading of the document — what it says, and
  // in several records what it does NOT prove. Until now it only ever appeared
  // as a 220-character snippet on the card, so the reasoning was written and
  // never readable. Show it in full, and let it wrap in whatever language it is.
  const summary = ml(d.summary) || '';

  let html = `
    <div class="doc-kind" style="font-family:var(--font-mono);font-size:0.78rem;color:var(--wine);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.3em;">${escapeHtml(typeLabel)}</div>
    <h2 style="margin-bottom:0.3em;">${escapeHtml(ml(d.title))}</h2>
    ${d.source_archive ? `<p class="muted" style="font-style:italic;font-family:var(--font-serif);">${escapeHtml(d.source_archive)}</p>` : ''}
    ${summary ? `<div class="doc-summary" dir="auto" style="margin-top:1rem;white-space:pre-line;font-family:var(--font-serif);line-height:1.6;">${escapeHtml(summary)}</div>` : ''}

    <div class="doc-viewer" style="margin-top:1.5rem;">
      <div class="doc-source">${sourceHTML}</div>
      <div class="doc-meta">
        <div class="doc-translations-tabs">
          ${tabs.map(lng => `<button class="doc-tab ${lng === State.lang ? 'active' : ''}" data-doctab="${lng}">${langLabel[lng]}</button>`).join('')}
          ${decoded ? `<button class="doc-tab" data-doctab="decoded">${escapeHtml(t('documents.tab_decoded'))}</button>` : ''}
          ${notes ? `<button class="doc-tab" data-doctab="notes">${escapeHtml(t('documents.tab_notes'))}</button>` : ''}
        </div>
        <div id="doc-content-area"></div>
      </div>
    </div>
  `;
  showModal(html);

  // Some records were catalogued from the research chat before the scan itself
  // was filed — nine of the June 2026 finds are in that state. Say so plainly
  // instead of showing a broken image. Fixes itself when the file is added.
  document.querySelectorAll('#modal .doc-source img[data-file]').forEach(img => {
    img.addEventListener('error', () => {
      const holder = img.parentElement;
      if (!holder) return;
      img.remove();
      const note = document.createElement('div');
      note.className = 'doc-source-pending';
      note.innerHTML = `<strong>${escapeHtml(t('documents.file_pending'))}</strong>`;
      holder.prepend(note);
    });
  });

  // Initial render and tab handlers
  function renderTab(tab) {
    const area = document.getElementById('doc-content-area');
    if (!area) return;
    if (tab === 'decoded') {
      area.innerHTML = `
        <table class="doc-decoded-table">
          ${Object.entries(decoded).map(([k,v]) => `
            <tr><td>${escapeHtml(k.replace(/_/g, ' '))}</td><td>${escapeHtml(String(v))}</td></tr>
          `).join('')}
        </table>
      `;
    } else if (tab === 'notes') {
      const text = (typeof notes === 'object') ? (ml(notes) || JSON.stringify(notes, null, 2)) : notes;
      area.innerHTML = `<div class="doc-translation">${escapeHtml(text)}</div>`;
    } else {
      let txt = '';
      if (d.translations && d.translations[tab]) txt = d.translations[tab];
      else if (d.transcription && tab === d.primary_language) txt = (typeof d.transcription === 'string') ? d.transcription : ml(d.transcription);
      if (!txt) txt = t('documents.no_translation_yet');
      area.innerHTML = `<div class="doc-translation">${escapeHtml(txt)}</div>`;
    }
  }
  renderTab(State.lang);
  document.querySelectorAll('#modal [data-doctab]').forEach(b => {
    b.addEventListener('click', () => {
      document.querySelectorAll('#modal [data-doctab]').forEach(x => x.classList.toggle('active', x === b));
      renderTab(b.dataset.doctab);
    });
  });
}

// ----------------------------------------
// HYPOTHESES
// ----------------------------------------
// Several statuses in the data are whole sentences — "RESOLVED — Muszyna
// confirmed by memoir 2026-05-20" — and t() returns the key when there is no
// translation, so `t('status.' + s)` rendered the key itself. Show the sentence.
function statusLabel(s) {
  const k = 'status.' + s;
  return t(k) !== k ? t(k) : s;
}

function renderHypotheses(root) {
  // sort by priority then status
  const priOrder = { HIGH: 0, MEDIUM: 1, LOW: 2 };
  const hyps = [...State.data.hypotheses].sort((a,b) => (priOrder[a.priority] ?? 3) - (priOrder[b.priority] ?? 3));

  root.innerHTML = `
    ${pageHeader('hypotheses.title', 'hypotheses.lead')}
    <div class="hyp-list">
      ${hyps.map(h => `
        <article class="hyp-card">
          <div class="hyp-header">
            <h3 class="hyp-question">${escapeHtml(ml(h.question))}</h3>
            <div class="hyp-badges">
              ${h.priority ? `<span class="badge priority-${escapeHtml(h.priority)}">${escapeHtml(h.priority)}</span>` : ''}
              ${h.status ? `<span class="badge status-${escapeHtml(h.status)}">${escapeHtml(statusLabel(h.status))}</span>` : ''}
            </div>
          </div>
          ${h.answer ? `
            <div class="hyp-answer" dir="auto">
              <h4>${escapeHtml(t('hypotheses.answer'))}</h4>
              <p>${escapeHtml(ml(h.answer))}</p>
              ${asList(h.evidence).length ? `
                <ul class="hyp-evidence">${asList(h.evidence).map(e => `<li>${escapeHtml(e)}</li>`).join('')}</ul>
              ` : ''}
            </div>
          ` : ''}
          ${h.candidates?.length ? `
            <div class="candidates">
              ${h.candidates.map(c => `
                <div class="candidate verdict-${escapeHtml((c.verdict || '').replace(/ /g, '_'))}">
                  <div class="candidate-label">${escapeHtml(c.label || c.name || '')}</div>
                  ${c.verdict ? `<div class="evidence-header">${escapeHtml(t('ui.verdict'))}: ${escapeHtml(t('candidate_verdict.' + (c.verdict || 'candidate')))}</div>` : ''}
                  ${asList(c.evidence_for).length ? `
                    <div class="evidence-header">${escapeHtml(t('ui.evidence_for'))}</div>
                    <ul class="candidate-evidence for">
                      ${asList(c.evidence_for).map(e => `<li>${escapeHtml(e)}</li>`).join('')}
                    </ul>
                  ` : ''}
                  ${asList(c.evidence_against).length ? `
                    <div class="evidence-header">${escapeHtml(t('ui.evidence_against'))}</div>
                    <ul class="candidate-evidence against">
                      ${asList(c.evidence_against).map(e => `<li>${escapeHtml(e)}</li>`).join('')}
                    </ul>
                  ` : ''}
                </div>
              `).join('')}
            </div>
          ` : ''}
          ${asList(h.next_steps).length ? `
            <div class="hyp-next">
              <h4>${escapeHtml(t('ui.next_steps'))}</h4>
              <ul>${asList(h.next_steps).map(s => `<li>${escapeHtml(s)}</li>`).join('')}</ul>
            </div>
          ` : ''}
        </article>
      `).join('')}
    </div>
  `;
}

// ----------------------------------------
// CHAT
// ----------------------------------------
const ChatState = { search: '', attachmentsOnly: false };

function renderChat(root) {
  root.innerHTML = `
    ${pageHeader('chat.title', 'chat.lead')}
    <div class="chat-controls">
      <input class="chat-search" type="search" placeholder="${escapeHtml(t('ui.search'))}…" id="chat-search" value="${escapeHtml(ChatState.search)}" />
      <button class="filter-btn ${!ChatState.attachmentsOnly?'active':''}" data-chatfilter="all">${escapeHtml(t('chat.filter_all'))}</button>
      <button class="filter-btn ${ChatState.attachmentsOnly?'active':''}" data-chatfilter="attach">${escapeHtml(t('chat.filter_attachments'))}</button>
    </div>
    <div class="chat-list" id="chat-list"></div>
  `;
  document.getElementById('chat-search').addEventListener('input', e => {
    ChatState.search = e.target.value;
    renderChatList();
  });
  document.querySelectorAll('[data-chatfilter]').forEach(b => {
    b.addEventListener('click', () => {
      ChatState.attachmentsOnly = b.dataset.chatfilter === 'attach';
      renderChat(root);
    });
  });
  renderChatList();
}

function renderChatList() {
  const list = document.getElementById('chat-list');
  if (!list) return;
  let msgs = State.data.messages.slice().sort((a, b) => {
    const ta = a.timestamp || `${a.date || ''}T${a.time || ''}`;
    const tb = b.timestamp || `${b.date || ''}T${b.time || ''}`;
    return ta < tb ? -1 : ta > tb ? 1 : 0;
  });
  if (ChatState.attachmentsOnly) msgs = msgs.filter(m => m.attachment);
  const q = ChatState.search.trim().toLowerCase();
  if (q) msgs = msgs.filter(m =>
    (m.body || '').toLowerCase().includes(q) ||
    (m.author || '').toLowerCase().includes(q) ||
    (m.author_normalized || '').toLowerCase().includes(q) ||
    (typeof m.attachment === 'object' && m.attachment && (m.attachment.filename || '').toLowerCase().includes(q))
  );

  // Format ISO timestamp -> human-readable
  const fmtTime = (m) => {
    if (m.timestamp) {
      try {
        const d = new Date(m.timestamp);
        if (!isNaN(d)) {
          return d.toLocaleString(undefined, { year: 'numeric', month: 'short', day: '2-digit', hour: '2-digit', minute: '2-digit' });
        }
      } catch (e) {}
    }
    return `${m.date || ''} ${m.time || ''}`.trim();
  };

  // Attachment helper — handles both old (string) and new (object) attachment formats
  const renderAttachment = (att) => {
    if (!att) return '';
    let filename, kind;
    if (typeof att === 'string') { filename = att; kind = ''; }
    else { filename = att.filename || ''; kind = att.kind || ''; }
    if (!filename) return '';
    const href = 'assets/documents/' + encodeURI(filename);
    const ext = (filename.match(/\.([a-z0-9]+)$/i) || [,''])[1].toLowerCase();
    const isImg = ['jpg','jpeg','png','webp','gif'].includes(ext);
    const isPdf = ext === 'pdf';
    const isSticker = ext === 'webp' || kind === 'sticker';
    const icon = isImg ? '🖼️' : isPdf ? '📄' : isSticker ? '😊' : '📎';
    if (isImg) {
      return `<a class="msg-attachment msg-attachment-img" href="${escapeHtml(href)}" target="_blank" rel="noopener">
        <img src="${escapeHtml(href)}" alt="${escapeHtml(filename)}" loading="lazy" />
        <span class="msg-attachment-label">${escapeHtml(icon)} ${escapeHtml(filename)}</span>
      </a>`;
    }
    return `<a class="msg-attachment" href="${escapeHtml(href)}" target="_blank" rel="noopener">${escapeHtml(icon)} ${escapeHtml(filename)}</a>`;
  };

  list.innerHTML = msgs.length ? msgs.slice(0, 1000).map(m => {
    const displayName = m.author_normalized || m.author || t('ui.unknown');
    const initial = (displayName || '?').slice(0,1).toUpperCase();
    return `
      <div class="msg">
        <div class="msg-avatar">${escapeHtml(initial)}</div>
        <div class="msg-body">
          <div class="msg-head">
            <span class="msg-author">${escapeHtml(displayName)}</span>
            <span class="msg-date">${escapeHtml(fmtTime(m))}</span>
            ${(m.language || m.lang) ? `<span class="msg-lang-badge">${escapeHtml(m.language || m.lang)}</span>` : ''}
          </div>
          ${m.body ? `<div class="msg-text">${escapeHtml(m.body)}</div>` : ''}
          ${renderAttachment(m.attachment)}
        </div>
      </div>
    `;
  }).join('') : `<div style="padding:2rem;text-align:center;color:var(--muted);">${escapeHtml(t('ui.no_results'))}</div>`;
}

// ----------------------------------------
// ABOUT
// ----------------------------------------
function renderAbout(root) {
  root.innerHTML = `
    ${pageHeader('about.title', 'about.intro')}
    <div style="max-width:760px;">
      <h3 class="section-title">${escapeHtml(t('about.method_title'))}</h3>
      <p style="font-family:var(--font-serif);font-size:1.05rem;line-height:1.7;color:var(--ink-soft);">${escapeHtml(t('about.method_p1'))}</p>
      <p style="font-family:var(--font-serif);font-size:1.05rem;line-height:1.7;color:var(--ink-soft);">${escapeHtml(t('about.method_p2'))}</p>

      <h3 class="section-title">${escapeHtml(t('about.thanks_title'))}</h3>
      <p style="font-family:var(--font-serif);font-size:1.1rem;line-height:1.7;color:var(--ink-soft);font-style:italic;">${escapeHtml(t('about.thanks_p'))}</p>
    </div>
  `;
}

// ----------------------------------------
// RESEARCH CENTER
// ----------------------------------------
function renderResearch(root, param) {
  const r = State.data.research || { sections: [] };
  const lang = State.lang;
  const pickField = (obj, base) => obj[base + '_' + lang] || obj[base + '_en'] || obj[base] || '';

  const statusBadge = (status) => {
    const map = {
      confirmed: { en: 'Confirmed', he: 'מאומת', cls: 'confidence-documented' },
      likely:    { en: 'Likely',    he: 'סביר',   cls: 'confidence-family_oral' },
      lead:      { en: 'Lead',      he: 'כיוון חקירה', cls: 'confidence-claim' },
      anomaly:   { en: 'Anomaly',   he: 'אנומליה', cls: 'confidence-claim' },
    };
    const s = map[status] || map.lead;
    const label = lang === 'he' ? s.he : s.en;
    return `<span class="badge ${s.cls}">${escapeHtml(label)}</span>`;
  };

  // If param matches a known section id, treat as "jump to section" instead of search.
  const knownSectionIds = new Set((r.sections || []).map(s => s.id));
  const jumpToSection = knownSectionIds.has(param) ? param : null;
  const q = jumpToSection ? '' : (param || '').toLowerCase();

  let html = `
    <div class="page-header">
      <h1>${escapeHtml(lang === 'he' ? 'מרכז המחקר' : 'Research Center')}</h1>
      <p class="lead">${escapeHtml(lang === 'he' ? 'ממצאי המחקר העמוק על משפחת רפפורט-וייצנר — תיעוד, צילומים, ארכיונים, צאצאים חיים. הקליקו על כל פריט להרחבה.' : 'Deep research findings on the Rapaport-Weitzner family — documents, photographs, archives, living descendants. Click any card to expand.')}</p>
    </div>

    <div style="margin:0 0 1.5em 0;display:flex;gap:0.6em;flex-wrap:wrap;align-items:center;">
      <input type="text" id="rc-search" placeholder="${escapeHtml(lang === 'he' ? 'חיפוש בממצאי המחקר…' : 'Search research findings…')}" value="${escapeHtml(q)}" style="flex:1;min-width:240px;padding:0.6em 0.9em;border:1px solid var(--rule);border-radius:6px;font-family:var(--font-serif);font-size:1rem;">
      <span style="font-family:var(--font-mono);font-size:0.85rem;color:var(--ink-faint);">${escapeHtml(lang === 'he' ? 'נוצר' : 'Generated')}: ${escapeHtml(r.generated || '')}</span>
    </div>
  `;

  for (const section of r.sections || []) {
    const title = pickField(section, 'title');
    const intro = pickField(section, 'intro');
    const visibleCards = (section.cards || []).filter(c => {
      if (!q) return true;
      const hay = foldText([
        pickField(c, 'title'), pickField(c, 'summary'),
        c.quote_en || '', c.source || '', (c.urls || []).join(' ')
      ].join(' '));
      return hay.includes(foldText(q));
    });
    if (!visibleCards.length && q) continue;

    html += `
      <section data-section="${escapeHtml(section.id)}" id="rc-section-${escapeHtml(section.id)}" style="margin:2.2em 0;${jumpToSection === section.id ? 'background:var(--accent-wash);padding:1em;border-radius:6px;border:2px solid var(--accent);' : ''}">
        <h2 class="section-title" style="font-size:1.4rem;margin-bottom:0.3em;">${escapeHtml(title)}</h2>
        ${intro ? `<p style="font-family:var(--font-serif);color:var(--ink-soft);line-height:1.6;max-width:800px;margin-bottom:1em;">${escapeHtml(intro)}</p>` : ''}
        <div class="rc-cards">
    `;
    for (const c of visibleCards) {
      const t1 = pickField(c, 'title');
      const t2 = pickField(c, 'summary');
      const shipHist = pickField(c, 'ship_history');
      const searchTips = pickField(c, 'search_tips');
      const extraNotes = shipHist || searchTips
        ? `${shipHist ? `<p class="rc-extra"><em>${escapeHtml(shipHist)}</em></p>` : ''}${searchTips ? `<p class="rc-extra"><strong>${escapeHtml(lang === 'he' ? 'איך לחפש שם' : 'How to search by name')}:</strong> ${escapeHtml(searchTips)}</p>` : ''}`
        : '';
      const sourceLine = c.source ? `<div class="rc-meta"><strong>${escapeHtml(lang === 'he' ? 'מקור' : 'Source')}:</strong> ${escapeHtml(c.source)}</div>` : '';
      const quoteLine = c.quote_en ? `<blockquote class="rc-quote">"${escapeHtml(c.quote_en)}"</blockquote>` : '';
      const ctxLine = c.historical_context ? `<div class="rc-meta"><strong>${escapeHtml(lang === 'he' ? 'הקשר' : 'Context')}:</strong> ${escapeHtml(c.historical_context)}</div>` : '';
      const links = (c.urls || []).map(u => {
        const display = u.startsWith('mailto:') ? u.slice(7) : u.replace(/^https?:\/\//, '').replace(/\/$/, '');
        return `<a href="${escapeHtml(u)}" target="_blank" rel="noopener" class="rc-link">${escapeHtml(display.length > 60 ? display.slice(0, 60) + '…' : display)}</a>`;
      }).join('');
      const imageGallery = (c.images || []).map(img => {
        const cap = img['caption_' + lang] || img.caption_en || '';
        return `
          <figure class="rc-image">
            <a href="${escapeHtml(img.src)}" target="_blank" rel="noopener">
              <img src="${escapeHtml(img.src)}" alt="${escapeHtml(cap)}" loading="lazy">
            </a>
            <figcaption>${escapeHtml(cap)}${img.credit ? ` <span class="rc-credit">— ${escapeHtml(img.credit)}</span>` : ''}</figcaption>
          </figure>
        `;
      }).join('');
      let mapBlock = '';
      if (c.map && c.map.coords) {
        const [lat, lng] = c.map.coords;
        const mapsLabel = lang === 'he' ? 'מפת גוגל' : 'Google Maps';
        const svLabel   = lang === 'he' ? 'תצוגת רחוב' : 'Street View';
        const placeLabel = c.map.label || `${lat}, ${lng}`;
        mapBlock = `
          <div class="rc-map">
            <div class="rc-map-actions">
              <a href="${escapeHtml(c.map.google_maps)}" target="_blank" rel="noopener" class="rc-map-btn">📍 ${escapeHtml(mapsLabel)}</a>
              <a href="${escapeHtml(c.map.street_view)}" target="_blank" rel="noopener" class="rc-map-btn">🚶 ${escapeHtml(svLabel)}</a>
              <span class="rc-map-coords">${escapeHtml(placeLabel)} <span class="rc-credit">(${lat.toFixed(4)}, ${lng.toFixed(4)})</span></span>
            </div>
            <iframe class="rc-map-iframe" src="${escapeHtml(c.map.osm_embed)}" loading="lazy" referrerpolicy="no-referrer" title="OpenStreetMap"></iframe>
            ${c.map.google_streetview_embed ? `<div class="rc-streetview-label">${escapeHtml(lang === 'he' ? 'איך זה נראה היום — תצוגת רחוב של גוגל' : (lang === 'pl' ? 'Jak to wygląda dziś — Google Street View' : (lang === 'fr' ? 'Comment cela apparaît aujourd\'hui — Google Street View' : 'How it looks today — Google Street View')))}</div><iframe class="rc-map-iframe rc-streetview-iframe" src="${escapeHtml(c.map.google_streetview_embed)}" loading="lazy" referrerpolicy="no-referrer" title="Street View"></iframe>` : ''}
          </div>
        `;
      }
      // Pillar badge (3-column research framework — see headline_finds intro)
      const pillarLabels = {
        from_book:         { en: "📖 from the book", he: "📖 מהספר",          pl: "📖 z księgi",          fr: "📖 du livre" },
        memoir_vs_history: { en: "⚖️ memoir + history", he: "⚖️ יומן + היסטוריה", pl: "⚖️ pamiętnik + historia", fr: "⚖️ mémoire + histoire" },
        independent:       { en: "🔍 independent",   he: "🔍 ראיות עצמאיות",   pl: "🔍 niezależne",       fr: "🔍 indépendant" },
      };
      const pillarBadge = c.pillar && pillarLabels[c.pillar]
        ? `<span class="badge badge-pillar pillar-${c.pillar}">${escapeHtml(pillarLabels[c.pillar][lang] || pillarLabels[c.pillar].en)}</span>`
        : '';
      html += `
        <details class="rc-card" data-card="${escapeHtml(c.id)}">
          <summary>
            <div class="rc-card-summary">
              <div class="rc-card-title">${escapeHtml(t1)}</div>
              ${pillarBadge}
              ${statusBadge(c.status)}
            </div>
          </summary>
          <div class="rc-card-body">
            <p>${escapeHtml(t2)}</p>
            ${extraNotes}
            ${quoteLine}
            ${sourceLine}
            ${ctxLine}
            ${imageGallery ? `<div class="rc-images">${imageGallery}</div>` : ''}
            ${mapBlock}
            ${links ? `<div class="rc-links">${links}</div>` : ''}
          </div>
        </details>
      `;
    }
    html += `</div></section>`;
  }

  root.innerHTML = html;

  // Wire search box
  const searchInput = document.getElementById('rc-search');
  if (searchInput) {
    let debounce;
    searchInput.addEventListener('input', (e) => {
      clearTimeout(debounce);
      debounce = setTimeout(() => {
        const v = e.target.value.trim();
        location.hash = v ? `#/research/${encodeURIComponent(v)}` : '#/research';
      }, 250);
    });
    // Restore focus
    if (q) {
      searchInput.focus();
      searchInput.setSelectionRange(searchInput.value.length, searchInput.value.length);
    }
  }

  // If we were asked to jump to a section, scroll to it and auto-expand its cards.
  if (jumpToSection) {
    const target = document.getElementById('rc-section-' + jumpToSection);
    if (target) {
      target.querySelectorAll('details.rc-card').forEach(d => { d.open = true; });
      // Defer scroll until layout settles so iframes don't shift the target.
      setTimeout(() => target.scrollIntoView({ behavior: 'smooth', block: 'start' }), 60);
    }
  }
}

// ----------------------------------------
// EVENT MODAL
// ----------------------------------------
function openEventModal(id) {
  const e = State.byId.events[id];
  if (!e) return;
  const place = e.place_id ? State.byId.places[e.place_id] : null;
  const people = (e.people_ids || []).map(pid => State.byId.people[pid]).filter(Boolean);
  let html = `
    <div class="doc-kind" style="font-family:var(--font-mono);font-size:0.78rem;color:var(--wine);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.3em;">${escapeHtml(t('event_type.' + e.type))} · ${escapeHtml(fmtDate(e.date))}</div>
    <h2 style="margin-bottom:0.5em;">${escapeHtml(ml(e.title))}</h2>
    <p style="font-family:var(--font-serif);font-size:1.08rem;line-height:1.7;color:var(--ink-soft);">${escapeHtml(ml(e.description))}</p>
    ${place ? `<div class="detail-fact"><div class="detail-fact-label">${escapeHtml(t('ui.place'))}</div><div class="detail-fact-val">${escapeHtml(ml(place.names))}</div></div>` : ''}
    ${people.length ? `<div class="detail-fact"><div class="detail-fact-label">${escapeHtml(t('ui.people_in_event'))}</div><div class="detail-fact-val">${people.map(p => `<a href="#" data-person="${escapeHtml(p.id)}">${escapeHtml(ml(p.primary_name))}</a>`).join(' · ')}</div></div>` : ''}
    ${e.confidence ? `<div class="detail-fact"><div class="detail-fact-label">${escapeHtml(t('ui.confidence'))}</div><div class="detail-fact-val"><span class="badge confidence-${escapeHtml(e.confidence)}">${escapeHtml(t('confidence.' + e.confidence))}</span></div></div>` : ''}
    ${e.sources?.length ? `<div class="detail-fact"><div class="detail-fact-label">${escapeHtml(t('ui.sources'))}</div><div class="detail-fact-val">${
      // A source was printed as a bare id, which told the reader nothing and led
      // nowhere. Where the id is a document we actually hold, make it open.
      e.sources.map(s => {
        const d = State.byId.documents[s];
        return d
          ? `<a href="#" data-doc="${escapeHtml(d.id)}">${escapeHtml(ml(d.title) || d.id)}</a>`
          : `<span class="mono">${escapeHtml(s)}</span>`;
      }).join(' · ')
    }</div></div>` : ''}
    ${e.context_brief ? `<div class="event-brief">
      <div class="detail-fact-label">${escapeHtml(t('ui.background'))}</div>
      <p>${escapeHtml(ml(e.context_brief))}</p>
      ${(e.context_urls || []).map(u => `<a href="${escapeHtml(u.url)}" target="_blank" rel="noopener">${escapeHtml(u.label)}</a>`).join(' · ')}
    </div>` : ''}
  `;
  showModal(html);
  document.querySelectorAll('#modal [data-person]').forEach(el => {
    el.addEventListener('click', (ev) => { ev.preventDefault(); openPersonModal(el.dataset.person); });
  });
  document.querySelectorAll('#modal [data-doc]').forEach(el => {
    el.addEventListener('click', (ev) => { ev.preventDefault(); openDocModal(el.dataset.doc); });
  });
}

// ----------------------------------------
// MODAL plumbing
// ----------------------------------------
function showModal(html) {
  const m = document.getElementById('modal');
  document.getElementById('modal-content').innerHTML = html;
  m.hidden = false;
  document.body.style.overflow = 'hidden';
}
function closeModal() {
  document.getElementById('modal').hidden = true;
  document.body.style.overflow = '';
}
document.addEventListener('click', e => {
  if (e.target.closest('[data-close]')) closeModal();
});
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeModal();
});

// ----------------------------------------
// BOOTSTRAP
// ----------------------------------------
window.addEventListener('hashchange', router);

document.addEventListener('click', e => {
  const btn = e.target.closest('.lang-btn');
  if (btn) setLang(btn.dataset.lang);
});

// Mobile nav drawer — hamburger toggles, backdrop closes, links close
(function wireNavDrawer() {
  const closeDrawer = () => {
    const nav = document.querySelector('.primary-nav');
    const bd = document.getElementById('nav-backdrop');
    const btn = document.getElementById('nav-toggle');
    if (nav) nav.classList.remove('open');
    if (bd) { bd.classList.remove('open'); bd.hidden = true; }
    if (btn) btn.setAttribute('aria-expanded', 'false');
  };
  const openDrawer = () => {
    const nav = document.querySelector('.primary-nav');
    const bd = document.getElementById('nav-backdrop');
    const btn = document.getElementById('nav-toggle');
    if (nav) nav.classList.add('open');
    if (bd) { bd.hidden = false; bd.classList.add('open'); }
    if (btn) btn.setAttribute('aria-expanded', 'true');
  };
  document.addEventListener('click', e => {
    if (e.target.closest('#nav-toggle')) {
      const open = document.querySelector('.primary-nav')?.classList.contains('open');
      open ? closeDrawer() : openDrawer();
      return;
    }
    if (e.target.closest('#nav-backdrop')) { closeDrawer(); return; }
    // Clicking any nav link auto-closes the drawer (mobile UX)
    if (e.target.closest('.nav-inner a')) closeDrawer();
  });
  // Close drawer when language switches or route changes
  window.addEventListener('hashchange', closeDrawer);
  // Close on Escape key
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeDrawer(); });
})();

(async function init() {
  try {
    await loadAll();
  } catch (err) {
    document.getElementById('view').innerHTML = `<div style="padding:2rem;color:var(--wine);">Error loading data: ${escapeHtml(err.message)}</div>`;
    return;
  }
  // Restore language
  let lang = 'en';
  try { lang = localStorage.getItem('rapaport_lang') || 'en'; } catch (e) {}
  if (!State.i18n[lang]) lang = 'en';
  setLang(lang);
  if (!location.hash) location.hash = '#/home';
  else router();
})();
