// Memoir flip-book v2 — renders the ACTUAL PDF (lusia_memoir.pdf) using PDF.js,
// with side-by-side OCR'd Hebrew + English + Polish translations.
//
// No PNG copies — the PDF is the source of truth, the same scanned book the family has.
// PDF.js (Mozilla, Apache 2.0) loaded lazily from CDN on first visit.

export async function renderMemoir(root) {
  root.innerHTML = `<div class="page-pad"><h1 style="font-family:Georgia,serif;color:#6b1f1f;">📖 Loading memoir…</h1></div>`;

  // Load PDF.js v3 (UMD build — works as a regular <script> tag, no module gymnastics)
  if (!window.pdfjsLib) {
    try {
      await new Promise((resolve, reject) => {
        const s = document.createElement("script");
        s.src = "https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.min.js";
        s.onload = resolve;
        s.onerror = reject;
        document.head.appendChild(s);
      });
    } catch (e) {
      root.innerHTML = `<div class="page-pad"><h1>Memoir</h1><p>PDF.js failed to load: ${escapeHtml(e.message || e)}</p></div>`;
      return;
    }
  }
  const pdfjsLib = window.pdfjsLib;
  if (!pdfjsLib) {
    root.innerHTML = `<div class="page-pad"><h1>Memoir</h1><p>PDF.js library not available after load.</p></div>`;
    return;
  }
  pdfjsLib.GlobalWorkerOptions.workerSrc = "https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.worker.min.js";

  let meta = {}, pages = [];
  // Hard cache-bust at the call site so even an old service worker can't serve stale
  const bust = "?v=" + Date.now();
  try {
    const [metaResp, pagesResp] = await Promise.all([
      fetch("data/memoir.json" + bust, { cache: "no-store" }),
      fetch("data/memoir_pages.json" + bust, { cache: "no-store" }),
    ]);
    if (metaResp.ok) meta = await metaResp.json();
    if (pagesResp.ok) {
      pages = await pagesResp.json();
      console.log(`[memoir] loaded ${pages.length} pages, ${pages.filter(p => p.english).length} with English translation`);
    } else {
      console.error(`[memoir] memoir_pages.json HTTP ${pagesResp.status}`);
    }
  } catch (e) {
    console.error("[memoir] data load failed:", e);
  }

  const byPage = new Map((pages || []).map(p => [p.page, p]));
  // Strip any leading "platform/" prefix (legacy data files may include it; the SPA's base path already covers it)
  const pdfUrl = (meta.source_pdf || "assets/documents/lusia_memoir.pdf").replace(/^platform\//, "");

  root.innerHTML = `
    <div class="page-pad" style="max-width:1200px;margin:0 auto;">
      <header style="text-align:center;margin-bottom:1.2rem;">
        <h1 style="font-family:Georgia,serif;color:#6b1f1f;margin:0 0 0.3rem;">📖 ${escapeHtml(meta.title_he || "סיפורה של לוסיה")}</h1>
        <div style="font-size:0.95rem;color:#6b5440;font-style:italic;">${escapeHtml(meta.title_en || "The Story of Lusia")} · ${escapeHtml(meta.title_pl || "Historia Lusi")}</div>
        <div style="font-size:0.85rem;color:#6b5440;margin-top:0.4rem;">By ${escapeHtml(meta.author || "Leah (Lusia) Rapaport née Weitzner")} · loaded from the original scanned PDF</div>
      </header>
      <div id="m-controls" style="display:flex;justify-content:center;gap:0.6rem;margin-bottom:1rem;align-items:center;flex-wrap:wrap;">
        <button id="m-first" style="background:transparent;border:1.5px solid #6b1f1f;color:#6b1f1f;padding:0.35rem 0.6rem;border-radius:4px;cursor:pointer;">⏮ First</button>
        <button id="m-prev" style="background:#6b1f1f;color:#f8f3e8;border:none;padding:0.5rem 1rem;border-radius:4px;cursor:pointer;font-weight:600;">← Previous</button>
        <span id="m-pageinfo" style="font-family:Inter,sans-serif;color:#6b5440;min-width:80px;text-align:center;">Loading…</span>
        <button id="m-next" style="background:#6b1f1f;color:#f8f3e8;border:none;padding:0.5rem 1rem;border-radius:4px;cursor:pointer;font-weight:600;">Next →</button>
        <button id="m-last" style="background:transparent;border:1.5px solid #6b1f1f;color:#6b1f1f;padding:0.35rem 0.6rem;border-radius:4px;cursor:pointer;">Last ⏭</button>
        <select id="m-lang" style="padding:0.45rem;border:1px solid #cdb892;border-radius:4px;background:#fff;">
          <option value="he">עברית (original)</option>
          <option value="en" selected>English translation</option>
          <option value="pl">Polski tłumaczenie</option>
        </select>
        <a href="${escapeHtml(pdfUrl)}" target="_blank" style="font-size:0.85rem;color:#6b1f1f;text-decoration:underline;">📥 Download PDF</a>
      </div>
      <div id="m-stage" style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;align-items:start;">
        <div id="m-canvas-wrap" style="background:#fff;border:1px solid #cdb892;border-radius:6px;padding:0.6rem;box-shadow:0 6px 22px rgba(0,0,0,0.18);min-height:520px;display:flex;justify-content:center;align-items:flex-start;perspective:1500px;">
          <canvas id="m-canvas" style="max-width:100%;height:auto;display:block;transition:transform 0.45s ease;"></canvas>
        </div>
        <div id="m-text" style="background:#fff7e1;border:1px solid #cdb892;border-radius:6px;padding:1.2rem;min-height:520px;font-family:Georgia,serif;line-height:1.7;color:#2b1d10;">
          <div id="m-content"></div>
          <div id="m-meta" style="margin-top:1.2rem;padding-top:0.8rem;border-top:1px solid #cdb892;font-size:0.78rem;color:#6b5440;"></div>
        </div>
      </div>
      <div style="margin-top:1rem;text-align:center;font-size:0.78rem;color:#6b5440;">
        Tap the page to flip · ← → keys also work · text panel shows Hebrew OCR or AI translation
      </div>
    </div>`;

  const canvas = root.querySelector("#m-canvas");
  const ctx2d = canvas.getContext("2d");
  const info = root.querySelector("#m-pageinfo");
  const content = root.querySelector("#m-content");
  const metaEl = root.querySelector("#m-meta");
  const langSel = root.querySelector("#m-lang");
  const canvasWrap = root.querySelector("#m-canvas-wrap");

  // Load the PDF
  let pdf;
  try {
    const loadingTask = pdfjsLib.getDocument(pdfUrl);
    pdf = await loadingTask.promise;
  } catch (e) {
    info.textContent = "PDF failed to load";
    root.querySelector("#m-content").innerHTML = `<p style="color:#a04040;">${escapeHtml(e.message || e)}</p>`;
    return;
  }
  const N = pdf.numPages;
  let cur = 1;

  async function show(n, dir = "next") {
    cur = Math.max(1, Math.min(N, n));
    info.textContent = `${cur} / ${N}`;
    // Flip animation
    canvas.style.transform = dir === "next" ? "rotateY(-90deg)" : "rotateY(90deg)";
    setTimeout(() => { canvas.style.transform = ""; }, 250);
    try {
      const page = await pdf.getPage(cur);
      const viewport = page.getViewport({ scale: 1.5 });
      canvas.width = viewport.width;
      canvas.height = viewport.height;
      await page.render({ canvasContext: ctx2d, viewport }).promise;
    } catch (e) {
      console.warn("Page render failed:", e);
    }
    // Text panel
    const p = byPage.get(cur);
    const lang = langSel.value;
    const txt = p ? (p[lang] || "") : "";
    if (!p) {
      content.innerHTML = `<em style="color:#6b5440;">OCR still pending for this page.</em>`;
    } else if (!txt) {
      content.innerHTML = `<em style="color:#6b5440;">${lang === "he" ? "(no Hebrew text on this page)" : "(translation not available — Hebrew OCR was empty)"}</em>`;
    } else {
      const isHe = lang === "he";
      const dir2 = isHe ? "rtl" : "ltr";
      const fontFam = isHe ? "Heebo, Arial, sans-serif" : "Georgia, serif";
      content.innerHTML = `<div dir="${dir2}" style="font-family:${fontFam};white-space:pre-wrap;">${escapeHtml(txt)}</div>`;
    }
    metaEl.innerHTML = p ? [
      p.page_kind ? `<strong>Kind:</strong> ${escapeHtml(p.page_kind)}` : "",
      p.ocr_confidence ? `<strong>OCR confidence:</strong> ${escapeHtml(p.ocr_confidence)}` : "",
      p.ocr_notes ? `<strong>Notes:</strong> ${escapeHtml(p.ocr_notes)}` : "",
    ].filter(Boolean).join(" · ") : "";
  }

  root.querySelector("#m-first").onclick = () => show(1, "prev");
  root.querySelector("#m-prev").onclick = () => show(cur - 1, "prev");
  root.querySelector("#m-next").onclick = () => show(cur + 1, "next");
  root.querySelector("#m-last").onclick = () => show(N, "next");
  langSel.onchange = () => show(cur);
  canvas.style.cursor = "pointer";
  canvas.onclick = (e) => {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    // Hebrew is RTL — tap left side = next, right side = previous (matches book reading direction)
    if (x < rect.width / 2) show(cur + 1, "next");
    else show(cur - 1, "prev");
  };
  const keyHandler = (e) => {
    if (!canvas.isConnected) { window.removeEventListener("keydown", keyHandler); return; }
    if (e.key === "ArrowLeft") show(cur - 1, "prev");
    if (e.key === "ArrowRight") show(cur + 1, "next");
  };
  window.addEventListener("keydown", keyHandler);

  show(1);
}

function escapeHtml(s) {
  return String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]));
}
