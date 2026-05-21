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

const { onDocumentCreated, onDocumentWritten } = require("firebase-functions/v2/firestore");
const { setGlobalOptions } = require("firebase-functions/v2");
const { defineSecret } = require("firebase-functions/params");
const logger = require("firebase-functions/logger");
const admin = require("firebase-admin");
const { GoogleGenerativeAI } = require("@google/generative-ai");
// Optional fallback when Gemini returns 503 / 429 / RECITATION / SAFETY
let AnthropicClass = null;
try { AnthropicClass = require("@anthropic-ai/sdk"); } catch (e) { logger.info("Anthropic SDK not installed - Claude fallback disabled"); }

admin.initializeApp();
setGlobalOptions({ region: "us-central1" });

const GEMINI_API_KEY = defineSecret("GEMINI_API_KEY");
const ANTHROPIC_API_KEY = defineSecret("ANTHROPIC_API_KEY");

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

const SYSTEM_PROMPT = `You are a careful Jewish genealogy researcher assisting the Rapaport family - a project compiled in equal partnership by Dalia, Dana, Daniel and Doron Rapaport, in honor of Dov Rapaport's 80th birthday.

Their story is about David Mendel Rapaport (b. 25 Dec 1911, Nadworna, Galicia; forestry engineer; HOLOCAUST SURVIVOR who escaped Nazi-occupied Galicia; reached Brussels Apr 1946; eventually settled in Israel) and his wife Leah nee Weitzner (b. 1913 or 1916, Bolechow; HOLOCAUST SURVIVOR who survived under multiple false identities). Their son Dov Rapaport was born Brussels 1946.

DOCTRINE (mandatory):
1. NEVER invent facts. Every claim must trace to a primary source, or be explicitly labeled as hypothesis.
2. ELIMINATION IS KING - for any candidate, list what would have to be false for it to hold.
3. PARAPHRASE web sources in your own words - do NOT quote verbatim. Summarize what you find from Google Search in 1-2 short sentences of YOUR OWN writing, with the URL for reference. Never copy a sentence longer than 10 words verbatim from any source.
4. RESPECT what is already CONFIRMED in the family data (do not try to overturn primary documents).
5. David and Leah are HOLOCAUST SURVIVORS first and foremost. Any context about Soviet occupation, NKVD, passportization is HISTORICAL CONTEXT about the period - never a personal claim about their character or choices.
6. Output STRUCTURED JSON only. No prose outside JSON.

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
            `Now verify this upload against the family story. Paraphrase any web sources in your own words. Return the JSON object.` },
  ];
  if (fileBytes && fileMime) {
    const supported = /^image\/(jpeg|png|webp|heic|heif)$|^application\/pdf$|^text\/plain$/.test(fileMime);
    if (supported) {
      userParts.push({ inlineData: { mimeType: fileMime, data: fileBytes.toString("base64") } });
    }
  }

  // Try-once with Google Search grounding; if Gemini blocks due to RECITATION
  // (which fires when its output too closely mirrors source text), retry
  // without grounding so we still get a useful verification.
  async function _call(useGrounding) {
    const model = genAI.getGenerativeModel({
      model: "gemini-2.5-flash",
      tools: useGrounding ? [{ googleSearch: {} }] : undefined,
      systemInstruction: SYSTEM_PROMPT,
    });
    const result = await model.generateContent({
      contents: [{ role: "user", parts: userParts }],
    });
    // Inspect finishReason BEFORE calling .text() so RECITATION doesn't throw
    const cand = result.response?.candidates?.[0];
    if (cand?.finishReason === "RECITATION" || cand?.finishReason === "SAFETY") {
      const e = new Error(`Gemini ${cand.finishReason}`);
      e.code = cand.finishReason;
      throw e;
    }
    return result.response.text();
  }

  try {
    return await _call(true);
  } catch (e) {
    if (e.code === "RECITATION") {
      logger.warn("RECITATION on grounded call, retrying without Google Search");
      return await _call(false);
    }
    throw e;
  }
}

// Claude Sonnet 4.5 fallback - used when Gemini fails (503 / 429 / RECITATION / SAFETY).
// Same system prompt + same expected JSON shape so the rest of the pipeline is unchanged.
async function callClaude(upload, contextSummary, fileBytes, fileMime) {
  if (!AnthropicClass) throw new Error("Anthropic SDK not available");
  const Anthropic = AnthropicClass.default || AnthropicClass.Anthropic || AnthropicClass;
  const client = new Anthropic({ apiKey: ANTHROPIC_API_KEY.value() });

  const userContent = [
    { type: "text", text: `FAMILY DATA SUMMARY (compact):\n${JSON.stringify(contextSummary, null, 2)}\n\n` },
    { type: "text", text:
        `NEW UPLOAD:\n` +
        `- uploader: ${upload.uploader_name} (${upload.uploader_role})\n` +
        `- kind: ${upload.kind}\n` +
        `- title: ${upload.title || "(no title)"}\n` +
        `- notes: ${upload.notes || "(no notes)"}\n` +
        `- file name: ${upload.file_name}\n` +
        `- file type: ${upload.file_type}\n` +
        `- related person_id (uploader said): ${upload.person_id || "none"}\n` +
        `- related place_id: ${upload.place_id || "none"}\n` +
        `- related hypothesis_id: ${upload.hypothesis_id || "none"}\n\n` +
        `Verify this upload against the family story. Paraphrase any external knowledge in your own words. Return ONLY the JSON object specified in the system prompt - no prose outside JSON.` },
  ];
  if (fileBytes && fileMime) {
    if (fileMime === "application/pdf") {
      userContent.push({ type: "document", source: { type: "base64", media_type: fileMime, data: fileBytes.toString("base64") } });
    } else if (/^image\/(jpeg|png|webp|gif)$/.test(fileMime)) {
      userContent.push({ type: "image", source: { type: "base64", media_type: fileMime, data: fileBytes.toString("base64") } });
    }
  }

  const resp = await client.messages.create({
    model: "claude-sonnet-4-5-20250929",
    max_tokens: 4096,
    system: SYSTEM_PROMPT,
    messages: [{ role: "user", content: userContent }],
  });
  const text = (resp.content || []).map(b => b.text || "").join("");
  return text;
}

// Determines whether a Gemini error should trigger Claude fallback
function isRetryableGeminiError(e) {
  const msg = String(e && (e.message || e)).toLowerCase();
  if (e && (e.code === "RECITATION" || e.code === "SAFETY")) return true;
  if (msg.includes("503") || msg.includes("service unavailable")) return true;
  if (msg.includes("429") || msg.includes("rate limit") || msg.includes("quota")) return true;
  if (msg.includes("500") || msg.includes("internal")) return true;
  return false;
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

// Shared verification logic — used by both the create-trigger and the retry-trigger.
async function runVerification(upload, ref, uploadId) {
  await ref.update({
    gemini_verification: { status: "in_progress", started_at: admin.firestore.FieldValue.serverTimestamp() },
  });

  try {
    const ctx = await loadFamilyContext();
    const summary = summarizeContext(ctx);

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

    let rawText, modelUsed = "gemini-2.5-flash", fallbackReason = null;
    try {
      rawText = await callGemini(upload, summary, fileBytes, upload.file_type);
    } catch (geminiErr) {
      if (isRetryableGeminiError(geminiErr) && AnthropicClass) {
        fallbackReason = geminiErr.code || (geminiErr.message || "gemini_error").slice(0, 200);
        logger.warn(`Gemini failed (${fallbackReason}); falling back to Claude Sonnet 4.5`);
        rawText = await callClaude(upload, summary, fileBytes, upload.file_type);
        modelUsed = "claude-sonnet-4-5";
      } else {
        throw geminiErr;
      }
    }
    let parsed = safeParseJSON(rawText);

    // If Gemini gave us back unparseable JSON, retry with Claude — malformed JSON
    // is a Gemini failure mode that's worth a Claude pass.
    if (parsed.error && modelUsed === "gemini-2.5-flash" && AnthropicClass) {
      logger.warn(`Gemini returned malformed JSON; falling back to Claude Sonnet 4.5`);
      fallbackReason = "gemini_malformed_json";
      try {
        rawText = await callClaude(upload, summary, fileBytes, upload.file_type);
        modelUsed = "claude-sonnet-4-5";
        parsed = safeParseJSON(rawText);
      } catch (claudeErr) {
        logger.warn(`Claude fallback also failed: ${claudeErr.message}`);
      }
    }

    await ref.update({
      gemini_verification: {
        status: parsed.error ? "parse_error" : "done",
        model: modelUsed,
        fallback_reason: fallbackReason,
        completed_at: admin.firestore.FieldValue.serverTimestamp(),
        result: parsed.json || null,
        parse_error: parsed.error || null,
        raw_text: parsed.error ? parsed.raw : null,
      },
      retry_requested: admin.firestore.FieldValue.delete(),
    });
    logger.info(`Verified ${uploadId} via ${modelUsed} - ${parsed.error ? "PARSE ERROR" : "OK"}`);
  } catch (e) {
    logger.error(`verifyUpload failed: ${e.stack || e.message}`);
    await ref.update({
      gemini_verification: {
        status: "error",
        error: e.message,
        completed_at: admin.firestore.FieldValue.serverTimestamp(),
      },
      retry_requested: admin.firestore.FieldValue.delete(),
    });
  }
}

exports.verifyUpload = onDocumentCreated(
  { document: "family_uploads/{uploadId}", secrets: [GEMINI_API_KEY, ANTHROPIC_API_KEY], memory: "1GiB", timeoutSeconds: 180 },
  async (event) => {
    const snap = event.data;
    if (!snap) return;
    const upload = snap.data();
    if (upload.status !== "pending") {
      logger.info(`Skip ${event.params.uploadId} - status is ${upload.status}`);
      return;
    }
    await runVerification(upload, snap.ref, event.params.uploadId);
  }
);

// Manual retry trigger — set retry_requested: true on a family_uploads doc to re-run
// verification with the latest fallback logic. Useful for documents whose first
// verification failed with Gemini 503 / RECITATION / malformed JSON before the
// Claude fallback was deployed.
exports.retryVerification = onDocumentWritten(
  { document: "family_uploads/{uploadId}", secrets: [GEMINI_API_KEY, ANTHROPIC_API_KEY], memory: "1GiB", timeoutSeconds: 180 },
  async (event) => {
    const before = event.data?.before?.data() || null;
    const after = event.data?.after?.data() || null;
    if (!after) return;
    // Fire only on the transition false→true on retry_requested
    if (after.retry_requested !== true) return;
    if (before && before.retry_requested === true) return;
    logger.info(`retryVerification fired for ${event.params.uploadId}`);
    await runVerification(after, event.data.after.ref, event.params.uploadId);
  }
);
