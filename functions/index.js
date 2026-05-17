/**
 * Rapaport Family Tree — Cloud Functions
 *
 * Reuses RPA-PORT Firebase project but with ft_* function prefix and family_*
 * Firestore collections. Strict isolation from business code.
 *
 * Functions:
 *   - ft_translate_document    : HTTPS callable, 3-AI consensus translation
 *   - ft_research_assistant    : HTTPS callable, embedded AI Q&A
 *   - ft_audit_log_writer      : Firestore trigger, write audit entries
 *   - ft_seed_users            : HTTPS callable, admin-only, seed user custom claims
 *
 * CC: this is a stub. Fill in TODOs.
 */

const functions = require("firebase-functions");
const admin = require("firebase-admin");

admin.initializeApp();
const db = admin.firestore();

// ───────────────────────────────────────────────────────────────────
// Auth guards
// ───────────────────────────────────────────────────────────────────

function requireFamilyAuth(context) {
  if (!context.auth) {
    throw new functions.https.HttpsError("unauthenticated", "Sign-in required");
  }
  if (context.auth.token.family !== true) {
    throw new functions.https.HttpsError("permission-denied", "Not a family member");
  }
}

function requireFamilyRole(context, allowedRoles) {
  requireFamilyAuth(context);
  const role = context.auth.token.family_role;
  if (!allowedRoles.includes(role)) {
    throw new functions.https.HttpsError(
      "permission-denied",
      `Role required: ${allowedRoles.join(" or ")}; you have: ${role}`
    );
  }
}

// ───────────────────────────────────────────────────────────────────
// ft_translate_document
// ───────────────────────────────────────────────────────────────────

exports.ft_translate_document = functions
  .region("europe-west1")
  .runWith({ timeoutSeconds: 540, memory: "1GB", secrets: ["ANTHROPIC_API_KEY", "GEMINI_API_KEY", "OPENAI_API_KEY"] })
  .https.onCall(async (data, context) => {
    requireFamilyAuth(context);

    const { doc_id, target_lang, force_refresh = false } = data;
    if (!doc_id || !target_lang) {
      throw new functions.https.HttpsError("invalid-argument", "doc_id and target_lang required");
    }
    if (!["en", "he", "pl", "fr"].includes(target_lang)) {
      throw new functions.https.HttpsError("invalid-argument", "target_lang must be en|he|pl|fr");
    }

    // Check cache
    const cacheId = `${doc_id}_${target_lang}_consensus`;
    const cacheRef = db.collection("family_translations").doc(cacheId);
    if (!force_refresh) {
      const cached = await cacheRef.get();
      if (cached.exists) return cached.data();
    }

    // Load source document
    const docRef = db.collection("family_documents").doc(doc_id);
    const docSnap = await docRef.get();
    if (!docSnap.exists) {
      throw new functions.https.HttpsError("not-found", `Document not found: ${doc_id}`);
    }
    const doc = docSnap.data();

    // Determine source text. Order of preference:
    //   1. Existing translation in primary_language
    //   2. decoded_fields stringified
    //   3. Trigger OCR via ft_ocr_document (TODO)
    let sourceText = null;
    if (doc.translations?.[doc.primary_language]?.text) {
      sourceText = doc.translations[doc.primary_language].text;
    } else if (doc.decoded_fields) {
      sourceText = JSON.stringify(doc.decoded_fields, null, 2);
    } else {
      throw new functions.https.HttpsError(
        "failed-precondition",
        `No source text for ${doc_id}. Run OCR first.`
      );
    }

    // TODO(CC): Implement 3-AI consensus call.
    // Pattern mirrors lib/ai_consensus.py from rpa-port-platform.
    // Steps:
    //   1. Build a translation prompt that preserves names, dates, places, archaic
    //      spellings (Galician/Yiddish forms must NOT be modernized).
    //   2. Call Claude opus-4-7, Gemini 2.5 Pro, GPT-4o in parallel.
    //   3. Reconcile via majority-vote on tokens; flag divergences.
    //   4. Return consensus + individual versions.
    const translations = await tripleTranslate(sourceText, doc.primary_language, target_lang, doc);

    // Persist
    const result = {
      id: cacheId,
      doc_id,
      target_lang,
      version: "consensus",
      individual_versions: translations.individual,
      consensus_text: translations.consensus,
      consensus_method: "majority_vote_with_name_preservation",
      divergences: translations.divergences,
      human_reviewed: false,
      reviewer_uid: null,
      cost_usd: translations.cost_usd,
      created_at: admin.firestore.FieldValue.serverTimestamp(),
      created_by: context.auth.uid,
    };
    await cacheRef.set(result);

    // Audit
    await db.collection("family_audit").add({
      ts: admin.firestore.FieldValue.serverTimestamp(),
      uid: context.auth.uid,
      collection: "family_translations",
      doc_id: cacheId,
      action: "create",
      summary: `3-AI consensus translation of ${doc_id} → ${target_lang}`,
    });

    return result;
  });

// TODO(CC): Implement this. Skeleton:
async function tripleTranslate(sourceText, sourceLang, targetLang, docMeta) {
  // const claudeResult = await callClaude(sourceText, sourceLang, targetLang, docMeta);
  // const geminiResult = await callGemini(sourceText, sourceLang, targetLang, docMeta);
  // const gptResult = await callGPT(sourceText, sourceLang, targetLang, docMeta);
  // const consensus = reconcile([claudeResult, geminiResult, gptResult]);
  // return { individual: {...}, consensus, divergences, cost_usd };

  // PLACEHOLDER:
  return {
    individual: {
      "claude-opus-4-7": { text: "TODO", ts: new Date().toISOString() },
      "gemini-2.5-pro":  { text: "TODO", ts: new Date().toISOString() },
      "gpt-4o":          { text: "TODO", ts: new Date().toISOString() },
    },
    consensus: "TODO: implement 3-AI consensus pipeline",
    divergences: [],
    cost_usd: 0.0,
  };
}

// ───────────────────────────────────────────────────────────────────
// ft_research_assistant
// ───────────────────────────────────────────────────────────────────

exports.ft_research_assistant = functions
  .region("europe-west1")
  .runWith({ timeoutSeconds: 300, memory: "512MB", secrets: ["ANTHROPIC_API_KEY"] })
  .https.onCall(async (data, context) => {
    requireFamilyAuth(context);

    const { question, ui_lang = "en", conversation_history = [] } = data;
    if (!question) {
      throw new functions.https.HttpsError("invalid-argument", "question required");
    }

    // Load full corpus
    const [people, places, events, documents, hypotheses] = await Promise.all([
      db.collection("family_people").get(),
      db.collection("family_places").get(),
      db.collection("family_events").get(),
      db.collection("family_documents").get(),
      db.collection("family_hypotheses").get(),
    ]);

    const corpus = {
      people: people.docs.map(d => d.data()),
      places: places.docs.map(d => d.data()),
      events: events.docs.map(d => d.data()),
      documents: documents.docs.map(d => ({ ...d.data(), translations: undefined })), // skip translations to save tokens
      hypotheses: hypotheses.docs.map(d => d.data()),
    };

    // TODO(CC): Call Claude opus-4-7 with system prompt + corpus + question.
    // System prompt should enforce:
    //  - Cite doc IDs inline for every claim
    //  - Mark confidence: hypothesis where applicable
    //  - Never invent facts
    //  - Respond in ui_lang
    const answer = `TODO: implement. Corpus loaded: ${corpus.people.length} people, ${corpus.events.length} events.`;

    return { answer, ui_lang, sources_cited: [] };
  });

// ───────────────────────────────────────────────────────────────────
// ft_audit_log_writer
// ───────────────────────────────────────────────────────────────────

// Note: actual audit writes happen in client code + functions above.
// This trigger is a safety net — log any direct admin SDK writes that bypassed normal flow.
exports.ft_audit_safety_net = functions
  .region("europe-west1")
  .firestore.document("family_{collection}/{docId}")
  .onWrite(async (change, context) => {
    const { collection, docId } = context.params;

    // Skip the audit collection itself (would infinite loop)
    if (collection === "audit") return null;

    // Skip if this write came from a function that already audited
    // (we can't distinguish reliably; rely on dedup by hash in actual audit collection)

    // Just log presence — actual hashing happens in app code
    return null;
  });

// ───────────────────────────────────────────────────────────────────
// ft_seed_users (admin-only setup)
// ───────────────────────────────────────────────────────────────────

exports.ft_seed_users = functions
  .region("europe-west1")
  .https.onCall(async (data, context) => {
    requireFamilyRole(context, ["admin"]);

    const { email, role = "viewer", display_name, languages_preferred = ["en"] } = data;
    if (!email) {
      throw new functions.https.HttpsError("invalid-argument", "email required");
    }
    if (!["admin", "reviewer", "researcher", "viewer"].includes(role)) {
      throw new functions.https.HttpsError("invalid-argument", "invalid role");
    }

    // Get or create user
    let user;
    try {
      user = await admin.auth().getUserByEmail(email);
    } catch (e) {
      user = await admin.auth().createUser({ email, displayName: display_name });
    }

    // Set custom claims
    await admin.auth().setCustomUserClaims(user.uid, {
      family: true,
      family_role: role,
    });

    // Persist in family_users
    await db.collection("family_users").doc(user.uid).set({
      uid: user.uid,
      email,
      display_name: display_name || email,
      role,
      languages_preferred,
      added_at: admin.firestore.FieldValue.serverTimestamp(),
      added_by: context.auth.uid,
    }, { merge: true });

    return { uid: user.uid, email, role };
  });
