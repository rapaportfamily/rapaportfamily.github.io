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
function fmtDate(d) {
  if (!d) return t('ui.unknown');
  return d;
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
}

// ----------------------------------------
// Router
// ----------------------------------------
function router() {
  const hash = location.hash || '#/home';
  const path = hash.slice(2).split('/');
  const view = path[0] || 'home';
  const param = path[1];

  document.querySelectorAll('.nav-inner a').forEach(a => {
    a.classList.toggle('active', a.dataset.nav === view);
  });

  const root = document.getElementById('view');
  root.innerHTML = '';

  switch (view) {
    case 'home': renderHome(root); break;
    case 'tree': renderTree(root); break;
    case 'timeline': renderTimeline(root); break;
    case 'people': renderPeople(root, param); break;
    case 'places': renderPlaces(root, param); break;
    case 'documents': renderDocuments(root, param); break;
    case 'hypotheses': renderHypotheses(root); break;
    case 'chat': renderChat(root); break;
    case 'research': renderResearch(root, param); break;
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
// FAMILY TREE  (hand-laid SVG)
// ----------------------------------------
function renderTree(root) {
  root.innerHTML = `
    ${pageHeader('tree.title', 'tree.lead')}
    <div class="tree-wrap">
      <div class="tree-legend">
        <div class="legend-item"><span class="legend-swatch" style="background:var(--wine);border-color:var(--wine);"></span>${escapeHtml(t('tree.legend_subject'))}</div>
        <div class="legend-item"><span class="legend-swatch" style="background:#f5e8d4;border-color:var(--gold);"></span>${escapeHtml(t('confidence.family_oral'))} / Holocaust survivor</div>
        <div class="legend-item"><span class="legend-swatch" style="background:var(--paper-soft);"></span>${escapeHtml(t('tree.legend_grandparent'))}</div>
        <div class="legend-item"><span class="legend-swatch" style="background:var(--paper-soft);border-style:dashed;"></span>${escapeHtml(t('ui.died'))}</div>
      </div>
      <div id="tree-svg-container"></div>
    </div>
  `;

  const svg = buildFamilyTreeSVG();
  document.getElementById('tree-svg-container').appendChild(svg);
}

function buildFamilyTreeSVG() {
  // Manually-positioned tree.
  // Generations: gen 0 (top, gg-grandparents) → gen 4 (bottom, Doron's gen)
  // Box: 170 w × 54 h
  // Generation y: 60, 200, 340, 480, 620

  const W = 1280, H = 740;
  const BW = 170, BH = 54;
  const GY = [60, 200, 340, 480, 620];

  // Survivor flag for special shading
  const SURVIVORS = new Set(['p_david','p_leah','p_shimon','p_dov_bernard']);

  // Layout: x positions for each person
  // Strategy: Build couples first, position couples symmetrically.

  // Gen 0 — gg-grandparents (4 people, 2 couples)
  // Left side (paternal): Leizor + Sara
  // Right side (maternal): Samuel + Ester
  const layout = {
    // Gen 0
    p_leizor_griffel: { x: 200, y: GY[0], gen: 0 },
    p_sara_chajes:    { x: 380, y: GY[0], gen: 0 },
    p_samuel_weinreb: { x: 850, y: GY[0], gen: 0 },
    p_ester_blima:    { x: 1030, y: GY[0], gen: 0 },

    // Gen 1 — great-grandparents (4 people, 2 couples)
    p_berisz:         { x: 200, y: GY[1], gen: 1 },
    p_rebeka:         { x: 380, y: GY[1], gen: 1 },
    p_elias_weitzner: { x: 850, y: GY[1], gen: 1 },
    p_matel_weinreb:  { x: 1030, y: GY[1], gen: 1 },

    // Gen 2 — grandparents row (David's family + Leah's family meet at David+Leah)
    // David's family: David, Lota - centered under Berisz+Rebeka (290)
    // Leah's family: Leah, Feige, Moses, Pnina - centered under Elias+Matel (940)
    p_david:          { x: 460, y: GY[2], gen: 2 },
    p_lota:           { x: 280, y: GY[2], gen: 2 },
    p_leah:           { x: 640, y: GY[2], gen: 2 },
    p_feige:          { x: 820, y: GY[2], gen: 2 },
    p_moses_weitzner: { x: 1000, y: GY[2], gen: 2 },
    p_pnina_weitzner: { x: 1180, y: GY[2], gen: 2 },

    // Gen 3 — Bernard's generation (Dov+Dalia, Shimon)
    p_shimon:         { x: 360, y: GY[3], gen: 3 },
    p_dov_bernard:    { x: 550, y: GY[3], gen: 3 },
    p_dalia:          { x: 730, y: GY[3], gen: 3 },

    // Gen 4 — Doron's generation (Doron, Dana, Daniel)
    p_doron:          { x: 460, y: GY[4], gen: 4 },
    p_dana:           { x: 640, y: GY[4], gen: 4 },
    p_daniel:         { x: 820, y: GY[4], gen: 4 },
  };

  // Center of each box
  const cx = id => layout[id].x + BW/2;
  const cy = id => layout[id].y + BH/2;
  const topY = id => layout[id].y;
  const botY = id => layout[id].y + BH;

  // Build SVG
  const svgNS = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(svgNS, 'svg');
  svg.setAttribute('class', 'tree-svg');
  svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
  svg.setAttribute('xmlns', svgNS);
  svg.style.width = W + 'px';
  svg.style.height = H + 'px';

  // Generation labels
  const genLabels = [
    'tree.legend_greatgrandparent', // gen 0
    'tree.legend_greatgrandparent', // gen 1 (use same key, both are great-grandparents)
    'tree.legend_grandparent',
    'tree.legend_uncle',
    'tree.legend_descendant',
  ];
  // Better: label them by closeness to subject Bernard
  const genTexts = ['Great-Great-Grandparents · 1840s–1860s', 'Great-Grandparents · 1860s–1890s', 'Grandparents · 1900s–1910s', 'Parents · 1930s–1940s', 'Children · 1970s–1990s'];
  const isHe = State.lang === 'he';
  if (isHe) {
    genTexts[0] = 'הסבים־רבא־רבא · 1840–1860';
    genTexts[1] = 'הסבים־רבא · 1860–1890';
    genTexts[2] = 'הסבים · 1900–1910';
    genTexts[3] = 'ההורים · 1930–1940';
    genTexts[4] = 'הילדים · 1970–1990';
  } else if (State.lang === 'pl') {
    genTexts[0] = 'Prapradziadkowie · 1840–1860';
    genTexts[1] = 'Pradziadkowie · 1860–1890';
    genTexts[2] = 'Dziadkowie · 1900–1910';
    genTexts[3] = 'Rodzice · 1930–1940';
    genTexts[4] = 'Dzieci · 1970–1990';
  } else if (State.lang === 'fr') {
    genTexts[0] = 'Arrière-arrière-grands-parents · 1840–1860';
    genTexts[1] = 'Arrière-grands-parents · 1860–1890';
    genTexts[2] = 'Grands-parents · 1900–1910';
    genTexts[3] = 'Parents · 1930–1940';
    genTexts[4] = 'Enfants · 1970–1990';
  }

  for (let i = 0; i < 5; i++) {
    const tx = document.createElementNS(svgNS, 'text');
    tx.setAttribute('x', 30);
    tx.setAttribute('y', GY[i] + BH/2 + 4);
    tx.setAttribute('class', 'gen-label');
    tx.textContent = genTexts[i];
    svg.appendChild(tx);
  }

  // --- Lines first (under boxes) ---

  // Helper: draw spouse line (horizontal between two boxes at same y)
  function spouseLine(a, b) {
    const aRight = layout[a].x + BW;
    const bLeft = layout[b].x;
    const y = layout[a].y + BH/2;
    const line = document.createElementNS(svgNS, 'line');
    line.setAttribute('x1', aRight);
    line.setAttribute('y1', y);
    line.setAttribute('x2', bLeft);
    line.setAttribute('y2', y);
    line.setAttribute('class', 'spouse-line');
    svg.appendChild(line);
  }

  // Helper: draw parent → children line set
  // From midpoint between parents (or just parent box) down to a horizontal bar, then down to each child top
  function parentLines(parents, children) {
    if (!children.length) return;
    let parentMidX;
    if (parents.length === 2) {
      parentMidX = (cx(parents[0]) + cx(parents[1])) / 2;
    } else {
      parentMidX = cx(parents[0]);
    }
    const parentBottomY = botY(parents[0]);
    const horizY = (parentBottomY + topY(children[0])) / 2;

    // Vertical from parents down to horizontal
    const v1 = document.createElementNS(svgNS, 'line');
    v1.setAttribute('x1', parentMidX); v1.setAttribute('y1', parentBottomY);
    v1.setAttribute('x2', parentMidX); v1.setAttribute('y2', horizY);
    v1.setAttribute('class', 'tree-line');
    svg.appendChild(v1);

    // Horizontal connecting all children
    const childXs = children.map(c => cx(c)).sort((a,b)=>a-b);
    const minX = Math.min(childXs[0], parentMidX);
    const maxX = Math.max(childXs[childXs.length - 1], parentMidX);
    const horiz = document.createElementNS(svgNS, 'line');
    horiz.setAttribute('x1', minX); horiz.setAttribute('y1', horizY);
    horiz.setAttribute('x2', maxX); horiz.setAttribute('y2', horizY);
    horiz.setAttribute('class', 'tree-line');
    svg.appendChild(horiz);

    // Verticals down to each child
    for (const c of children) {
      const v = document.createElementNS(svgNS, 'line');
      v.setAttribute('x1', cx(c)); v.setAttribute('y1', horizY);
      v.setAttribute('x2', cx(c)); v.setAttribute('y2', topY(c));
      v.setAttribute('class', 'tree-line');
      svg.appendChild(v);
    }
  }

  // Spouse lines
  spouseLine('p_leizor_griffel', 'p_sara_chajes');
  spouseLine('p_samuel_weinreb', 'p_ester_blima');
  spouseLine('p_berisz', 'p_rebeka');
  spouseLine('p_elias_weitzner', 'p_matel_weinreb');
  spouseLine('p_david', 'p_leah');
  spouseLine('p_dov_bernard', 'p_dalia');

  // Parent → children
  parentLines(['p_leizor_griffel', 'p_sara_chajes'], ['p_rebeka']);
  parentLines(['p_samuel_weinreb', 'p_ester_blima'], ['p_matel_weinreb']);
  parentLines(['p_berisz', 'p_rebeka'], ['p_david', 'p_lota']);
  parentLines(['p_elias_weitzner', 'p_matel_weinreb'], ['p_leah', 'p_feige', 'p_moses_weitzner', 'p_pnina_weitzner']);
  parentLines(['p_david', 'p_leah'], ['p_shimon', 'p_dov_bernard']);
  parentLines(['p_dov_bernard', 'p_dalia'], ['p_doron', 'p_dana', 'p_daniel']);

  // --- Boxes ---
  for (const person of State.data.people) {
    const pos = layout[person.id];
    if (!pos) continue;
    const g = document.createElementNS(svgNS, 'g');
    g.setAttribute('class', 'person-box' +
      (person.id === 'p_dov_bernard' ? ' subject' : '') +
      (SURVIVORS.has(person.id) ? ' survivor' : '') +
      (person.death ? ' deceased' : ''));
    g.setAttribute('data-person', person.id);
    g.style.transform = `translate(${pos.x}px,${pos.y}px)`;

    const rect = document.createElementNS(svgNS, 'rect');
    rect.setAttribute('class', 'person-rect');
    rect.setAttribute('width', BW); rect.setAttribute('height', BH);
    rect.setAttribute('rx', 3);
    g.appendChild(rect);

    const name = document.createElementNS(svgNS, 'text');
    name.setAttribute('class', 'person-name');
    name.setAttribute('x', BW/2); name.setAttribute('y', 22);
    name.textContent = truncate(ml(person.primary_name), 26);
    g.appendChild(name);

    const dates = document.createElementNS(svgNS, 'text');
    dates.setAttribute('class', 'person-dates');
    dates.setAttribute('x', BW/2); dates.setAttribute('y', 40);
    const b = person.birth?.date ? extractYear(person.birth.date) : '?';
    const d = person.death?.date ? extractYear(person.death.date) : '';
    dates.textContent = d ? `${b} – ${d}` : `${b} –`;
    g.appendChild(dates);

    g.addEventListener('click', () => openPersonModal(person.id));
    svg.appendChild(g);
  }

  return svg;
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
      html.push(`<div class="tl-decade-marker">${currentDecade}s</div>`);
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
      ${p.note_en ? `<div class="person-note">${escapeHtml(p.note_en)}</div>` : ''}
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

function fmtDateRange(p) {
  const b = p.birth?.date ? extractYear(p.birth.date) : '?';
  const d = p.death?.date ? extractYear(p.death.date) : null;
  const bPlace = p.birth?.place_id ? ml(State.byId.places[p.birth.place_id]?.names) : '';
  let out = b;
  if (bPlace) out += ' · ' + bPlace.split(' (')[0];
  if (d) out = out + ' — ' + d;
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
    <div class="detail-name">${escapeHtml(ml(p.primary_name))}</div>
    ${p.aliases?.length ? `<div class="detail-aliases">${escapeHtml(p.aliases.join(' · '))}</div>` : ''}
    <div class="muted" style="margin-bottom:1rem;font-family:var(--font-mono);font-size:0.78rem;text-transform:uppercase;letter-spacing:0.08em;">${escapeHtml(roleLabel(p.role))}</div>
    ${p.note_en ? `<p style="font-family:var(--font-serif);font-size:1.05rem;line-height:1.6;color:var(--ink-soft);">${escapeHtml(p.note_en)}</p>` : ''}

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
            <div class="detail-fact-label">${escapeHtml(f.label || '')}</div>
            <div class="detail-fact-val">
              ${escapeHtml(f.value || ml(f.text || {}) || '')}
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
          ${p.significance ? `<p style="margin-top:0.6em;font-size:0.92rem;color:var(--ink-soft);line-height:1.5;">${escapeHtml(p.significance)}</p>` : ''}
          ${p.era_context ? `
            <div class="place-eras">
              ${Object.entries(p.era_context).map(([period, txt]) => `
                <div class="place-era"><span class="place-era-period">${escapeHtml(period.replace(/_/g, '–'))}</span>${escapeHtml(txt)}</div>
              `).join('')}
            </div>
          ` : ''}
        </div>
      `).join('')}
    </div>
  `;
}

// ----------------------------------------
// DOCUMENTS
// ----------------------------------------
function renderDocuments(root, paramId) {
  root.innerHTML = `
    ${pageHeader('documents.title', 'documents.lead')}
    <div class="documents-grid">
      ${State.data.documents.map(d => {
        const thumb = pickDocThumb(d);
        return `
          <div class="doc-card" data-doc="${escapeHtml(d.id)}">
            <div class="doc-thumb">
              ${thumb ? `<img src="${escapeHtml(thumb)}" alt="" loading="lazy" />` : `<div class="doc-thumb-placeholder">${escapeHtml(d.kind || 'document')}</div>`}
            </div>
            <div class="doc-info">
              <div class="doc-kind">${escapeHtml(t('doc_type.' + d.type) || d.type)}${d.primary_language ? ' · ' + escapeHtml(d.primary_language.toUpperCase()) : ''}</div>
              <h4 class="doc-title">${escapeHtml(ml(d.title))}</h4>
            </div>
          </div>
        `;
      }).join('')}
    </div>
  `;
  root.querySelectorAll('[data-doc]').forEach(el => {
    el.addEventListener('click', () => openDocModal(el.dataset.doc));
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
      sourceHTML += `<div><img src="${escapeHtml(path)}" alt="${escapeHtml(f)}" /><div class="doc-source-caption">${escapeHtml(f)}</div></div>`;
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

  let html = `
    <div class="doc-kind" style="font-family:var(--font-mono);font-size:0.78rem;color:var(--wine);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.3em;">${escapeHtml(t('doc_type.' + d.type) || d.type)}</div>
    <h2 style="margin-bottom:0.3em;">${escapeHtml(ml(d.title))}</h2>
    ${d.source_archive ? `<p class="muted" style="font-style:italic;font-family:var(--font-serif);">${escapeHtml(d.source_archive)}</p>` : ''}

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
              ${h.status ? `<span class="badge status-${escapeHtml(h.status)}">${escapeHtml(t('status.' + h.status))}</span>` : ''}
            </div>
          </div>
          ${h.candidates?.length ? `
            <div class="candidates">
              ${h.candidates.map(c => `
                <div class="candidate verdict-${escapeHtml((c.verdict || '').replace(/ /g, '_'))}">
                  <div class="candidate-label">${escapeHtml(c.label)}</div>
                  ${c.verdict ? `<div class="evidence-header">${escapeHtml(t('ui.verdict'))}: ${escapeHtml(t('candidate_verdict.' + (c.verdict || 'candidate')))}</div>` : ''}
                  ${c.evidence_for?.length ? `
                    <div class="evidence-header">${escapeHtml(t('ui.evidence_for'))}</div>
                    <ul class="candidate-evidence for">
                      ${c.evidence_for.map(e => `<li>${escapeHtml(e)}</li>`).join('')}
                    </ul>
                  ` : ''}
                  ${c.evidence_against?.length ? `
                    <div class="evidence-header">${escapeHtml(t('ui.evidence_against'))}</div>
                    <ul class="candidate-evidence against">
                      ${c.evidence_against.map(e => `<li>${escapeHtml(e)}</li>`).join('')}
                    </ul>
                  ` : ''}
                </div>
              `).join('')}
            </div>
          ` : ''}
          ${h.next_steps?.length ? `
            <div class="hyp-next">
              <h4>${escapeHtml(t('ui.next_steps'))}</h4>
              <ul>${h.next_steps.map(s => `<li>${escapeHtml(s)}</li>`).join('')}</ul>
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
  let msgs = State.data.messages;
  if (ChatState.attachmentsOnly) msgs = msgs.filter(m => m.attachment);
  const q = ChatState.search.trim().toLowerCase();
  if (q) msgs = msgs.filter(m => (m.body || '').toLowerCase().includes(q) || (m.author || '').toLowerCase().includes(q));

  list.innerHTML = msgs.length ? msgs.slice(0, 500).map(m => {
    const initial = (m.author || '?').slice(0,1).toUpperCase();
    return `
      <div class="msg">
        <div class="msg-avatar">${escapeHtml(initial)}</div>
        <div class="msg-body">
          <div class="msg-head">
            <span class="msg-author">${escapeHtml(m.author || t('ui.unknown'))}</span>
            <span class="msg-date">${escapeHtml(m.timestamp || '')}</span>
            ${m.language ? `<span class="msg-lang-badge">${escapeHtml(m.language)}</span>` : ''}
          </div>
          ${m.body ? `<div class="msg-text">${escapeHtml(m.body)}</div>` : ''}
          ${m.attachment ? `<a class="msg-attachment" href="assets/documents/${escapeHtml(m.attachment)}" target="_blank">📎 ${escapeHtml(m.attachment)}</a>` : ''}
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

  const q = (param || '').toLowerCase();

  let html = `
    <div class="page-header">
      <h1>${escapeHtml(lang === 'he' ? 'מרכז המחקר' : 'Research Center')}</h1>
      <p class="lead">${escapeHtml(lang === 'he' ? 'ממצאי המחקר העמוק על משפחת רפפורט-וייצנר — תיעוד, צילומים, ארכיונים, צאצאים חיים. הקליקו על כל פריט להרחבה.' : 'Deep research findings on the Rapaport-Weitzner family — documents, photographs, archives, living descendants. Click any card to expand.')}</p>
    </div>

    <div style="margin:0 0 1.5em 0;display:flex;gap:0.6em;flex-wrap:wrap;align-items:center;">
      <input type="text" id="rc-search" placeholder="${escapeHtml(lang === 'he' ? 'חיפוש בממצאי המחקר…' : 'Search research findings…')}" value="${escapeHtml(param || '')}" style="flex:1;min-width:240px;padding:0.6em 0.9em;border:1px solid var(--rule);border-radius:6px;font-family:var(--font-serif);font-size:1rem;">
      <span style="font-family:var(--font-mono);font-size:0.85rem;color:var(--ink-faint);">${escapeHtml(lang === 'he' ? 'נוצר' : 'Generated')}: ${escapeHtml(r.generated || '')}</span>
    </div>
  `;

  for (const section of r.sections || []) {
    const title = pickField(section, 'title');
    const intro = pickField(section, 'intro');
    const visibleCards = (section.cards || []).filter(c => {
      if (!q) return true;
      const hay = [
        pickField(c, 'title'), pickField(c, 'summary'),
        c.quote_en || '', c.source || '', (c.urls || []).join(' ')
      ].join(' ').toLowerCase();
      return hay.includes(q);
    });
    if (!visibleCards.length && q) continue;

    html += `
      <section style="margin:2.2em 0;">
        <h2 class="section-title" style="font-size:1.4rem;margin-bottom:0.3em;">${escapeHtml(title)}</h2>
        ${intro ? `<p style="font-family:var(--font-serif);color:var(--ink-soft);line-height:1.6;max-width:800px;margin-bottom:1em;">${escapeHtml(intro)}</p>` : ''}
        <div class="rc-cards">
    `;
    for (const c of visibleCards) {
      const t1 = pickField(c, 'title');
      const t2 = pickField(c, 'summary');
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
      html += `
        <details class="rc-card" data-card="${escapeHtml(c.id)}">
          <summary>
            <div class="rc-card-summary">
              <div class="rc-card-title">${escapeHtml(t1)}</div>
              ${statusBadge(c.status)}
            </div>
          </summary>
          <div class="rc-card-body">
            <p>${escapeHtml(t2)}</p>
            ${quoteLine}
            ${sourceLine}
            ${ctxLine}
            ${imageGallery ? `<div class="rc-images">${imageGallery}</div>` : ''}
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
    ${e.sources?.length ? `<div class="detail-fact"><div class="detail-fact-label">${escapeHtml(t('ui.sources'))}</div><div class="detail-fact-val mono">${escapeHtml(e.sources.join(' · '))}</div></div>` : ''}
  `;
  showModal(html);
  document.querySelectorAll('#modal [data-person]').forEach(el => {
    el.addEventListener('click', (ev) => { ev.preventDefault(); openPersonModal(el.dataset.person); });
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
