/**
 * Rapaport Family Tree — Cloud Functions
 *
 * verifyUpload — Firestore trigger on family_uploads/{id} create
 *   - Reads the upload + family research context
 *   - Calls Gemini 2.5 Flash with Google Search grounding
 *   - Asks Gemini to verify against the family story (confirms / contradicts / adds / suggested searches)
 *   - Writes verification report back to the upload doc, so the admin review queue shows it
 *
 * The Gemini API key is stored as a Firebase secret (GEMINI_API_KEY) — never in source.
 * Set with: firebase functions:secrets:set GEMINI_API_KEY
 */

const { onDocumentCreated } = require("firebase-functions/v2/firestore");
const { setGlobalOptions } = require("firebase-functions/v2");
const { defineSecret } = require("firebase-functions/params");
const logger = require("firebase-functions/logger");
const admin = require("firebase-admin");
const { GoogleGenerativeAI } = require("@google/generative-ai");

admin.initializeApp();
setGlobalOptions({ region: "us-central1" });

const GEMINI_API_KEY = defineSecret("GEMINI_API_KEY");

// Public read URLs for the static research data (GitHub Pages)
const SITE = "https://doronrpa-hub.github.io/rapaport-family-tree";
const DATA_URLS = {
  people:      `${SITE}/data/people.json`,
  places:      `${SITE}/data/places.json`,
  events:      `${SITE}/data/events.json`,
  hypotheses:  `${SITE}/data/hypotheses.json`,
  documents:   `${SITE}/data/documents.json`,
};

async function loadFamilyContext() {
  const ctx = {};
  for (const [key, url] of Object.entries(DATA_URLS)) {
    try {
      const r = await fetch(url);
      ctx[key] = await r.json();
    } catch (e) {
      logger.warn(`Failed to load ${key}: ${e.message}`);
      ctx[key] = null;
    }
  }
  return ctx;
}

function summarizeContext(ctx) {
  // Compact, model-friendly summary — full JSON would burn tokens.
  const people = (ctx.people?.people || []).map(p => ({
    id: p.id,
    name: p.primary_name?.en || p.id,
    birth: p.birth?.date,
    birth_place: p.birth?.place_id,
    role: p.role,
    note: p.note_en,
    facts: (p.facts || []).map(f => `${f.key}: ${f.value} (${f.confidence})`),
  }));
  const places = (ctx.places?.places || []).map(p => ({
    id: p.id,
    names: p.primary_name || p.names,
    note: p.notes_en,
  }));
  const events = (ctx.events?.events || []).map(e => ({
    id: e.id, date: e.date, type: e.type, title: e.title,
  }));
  const hypotheses = (ctx.hypotheses?.hypotheses || []).map(h => ({
    id: h.id,
    question: h.question?.en,
    status: h.status,
    context: h.context,
    candidates: (h.candidates || []).map(c => c.label),
  }));
  return { people, places, events, hypotheses };
}

const SYSTEM_PROMPT = `You are a careful Jewish genealogy researcher assisting the Rapaport family.
Their research story is about David Mendel Rapaport (b. 25 Dec 1911, Nadworna, Galicia; forestry engineer; survived the Holocaust; reached Brussels Apr 1946; transported to Israel via Cyprus camps) and his wife Leah nee Weitzner (b. 1913 or 1916, Bolechow). Their son Dov Rapaport was born Brussels 1946 - for whom this archive is an 80th-birthday gift.

DOCTRINE (mandatory):
1. NEVER invent facts. Every claim must trace to a primary source you can cite, or be explicitly labeled as hypothesis.
2. ELIMINATION IS KING - for any candidate, list what would have to be false for it to hold.
3. CITE SOURCES - when you use Google Search to corroborate, name the URL and quote the verbatim sentence.
4. RESPECT what is already CONFIRMED in the family data (do not try to overturn primary documents).
5. Output STRUCTURED JSON only. No prose outside JSON.

YOUR TASK:
You will receive (a) the family data summary and (b) a new upload (file + uploader notes).
Read the upload carefully. Use Google Search to find external corroborating or contradicting evidence.
Then return a single JSON object with EXACTLY these fields:

{
  "what_it_is": "1-sentence factual description of the upload (in English)",
  "confirms": [ { "fact": "existing family-data fact this confirms", "id_ref": "person/place/event/hypothesis id" } ],
  "contradicts": [ { "fact": "existing family-data fact this contradicts", "id_ref": "...", "evidence": "what in the upload contradicts it" } ],
  "adds": [ { "claim": "new fact this upload adds", "confidence": "documented | hypothesis | family_oral", "related_id": "id of related person/place/event if any" } ],
  "external_searches": [ { "query": "what you searched", "url": "result URL", "quote": "verbatim quote from result", "relevance": "how this relates" } ],
  "suggested_next_steps": [ "what Doron should do next based on this" ],
  "overall_assessment": "1-2 sentences: is this upload trustworthy? does it move the research forward?",
  "warnings": [ "any red flag - e.g. possibly fake, mis-attributed, low quality scan" ]
}

Return ONLY the JSON object. Do not wrap in markdown fences. Do not add commentary.`;

async function callGemini(upload, contextSummary, fileBytes, fileMime) {
  const genAI = new GoogleGenerativeAI(GEMINI_API_KEY.value());
  const model = genAI.getGenerativeModel({
    model: "gemini-2.5-flash",
    tools: [{ googleSearch: {} }],
    systemInstruction: SYSTEM_PROMPT,
  });

  const userParts = [
    { text: `FAMILY DATA SUMMARY (compact):\n${JSON.stringify(contextSummary, null, 2)}\n\n` },
    { text: `NEW UPLOAD:\n` +
            `- uploader: ${upload.uploader_name} (${upload.uploader_role})\n` +
            `- kind: ${upload.kind}\n` +
            `- title: ${upload.title || "(no title)"}\n` +
            `- notes: ${upload.notes || "(no notes)"}\n` +
            `- file name: ${upload.file_name}\n` +
            `- file type: ${upload.file_type}\n` +
            `- related person_id (uploader said): ${upload.person_id || "none"}\n` +
            `- related place_id: ${upload.place_id || "none"}\n` +
            `- related hypothesis_id: ${upload.hypothesis_id || "none"}\n\n` +
            `Now verify this upload against the family story. Return the JSON object.` },
  ];

  // Attach the file (image or text) if we have bytes
  if (fileBytes && fileMime) {
    const supported = /^image\/(jpeg|png|webp|heic|heif)$|^application\/pdf$|^text\/plain$/.test(fileMime);
    if (supported) {
      userParts.push({
        inlineData: { mimeType: fileMime, data: fileBytes.toString("base64") },
      });
    }
  }

  const result = await model.generateContent({
    contents: [{ role: "user", parts: userParts }],
  });
  return result.response.text();
}

function safeParseJSON(text) {
  // Gemini sometimes wraps in ```json ... ``` despite instructions - strip it
  const cleaned = text
    .replace(/^```(?:json)?\s*/i, "")
    .replace(/\s*```\s*$/, "")
    .trim();
  try {
    return { json: JSON.parse(cleaned), error: null };
  } catch (e) {
    // Fallback: try to find the largest {...} block
    const m = cleaned.match(/\{[\s\S]*\}/);
    if (m) {
      try { return { json: JSON.parse(m[0]), error: null }; } catch (e2) { /* fallthrough */ }
    }
    return { json: null, error: e.message, raw: cleaned.slice(0, 4000) };
  }
}

exports.verifyUpload = onDocumentCreated(
  { document: "family_uploads/{uploadId}", secrets: [GEMINI_API_KEY], memory: "1GiB", timeoutSeconds: 120 },
  async (event) => {
    const snap = event.data;
    if (!snap) return;
    const upload = snap.data();
    const ref = snap.ref;

    if (upload.status !== "pending") {
      logger.info(`Skip ${event.params.uploadId} - status is ${upload.status}`);
      return;
    }

    await ref.update({
      gemini_verification: { status: "in_progress", started_at: admin.firestore.FieldValue.serverTimestamp() },
    });

    try {
      const ctx = await loadFamilyContext();
      const summary = summarizeContext(ctx);

      // Download the uploaded file (small files inline; skip huge ones)
      let fileBytes = null;
      const fileSize = upload.file_size || 0;
      if (upload.file_url && fileSize < 8 * 1024 * 1024) {
        try {
          const r = await fetch(upload.file_url);
          if (r.ok) fileBytes = Buffer.from(await r.arrayBuffer());
        } catch (e) {
          logger.warn(`Failed to fetch file: ${e.message}`);
        }
      }

      const rawText = await callGemini(upload, summary, fileBytes, upload.file_type);
      const parsed = safeParseJSON(rawText);

      await ref.update({
        gemini_verification: {
          status: parsed.error ? "parse_error" : "done",
          model: "gemini-2.5-flash",
          completed_at: admin.firestore.FieldValue.serverTimestamp(),
          result: parsed.json || null,
          parse_error: parsed.error || null,
          raw_text: parsed.error ? parsed.raw : null,
        },
      });
      logger.info(`Verified ${event.params.uploadId} - ${parsed.error ? "PARSE ERROR" : "OK"}`);
    } catch (e) {
      logger.error(`verifyUpload failed: ${e.stack || e.message}`);
      await ref.update({
        gemini_verification: {
          status: "error",
          error: e.message,
          completed_at: admin.firestore.FieldValue.serverTimestamp(),
        },
      });
    }
  }
);
