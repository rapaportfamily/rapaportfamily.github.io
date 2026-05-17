/**
 * Budget meter for LLM-spending Cloud Functions.
 *
 * Resolution of decision D5 (17 May 2026): hard cap $30/month on combined LLM
 * spend across all ft_* functions. Admin UID (Doron) bypasses.
 *
 * Usage in a function:
 *
 *   const budget = require('./budget_meter');
 *   const estimate = budget.estimateTranslateCost(sourceTextLen);
 *   await budget.checkBudgetOrThrow('ft_translate_document', estimate, context);
 *   // ...do the LLM call...
 *   const actual = computeActualCost(claudeUsage, geminiUsage, gptUsage);
 *   await budget.recordSpend('ft_translate_document', actual);
 *
 * CC: complete the TODOs.
 */

const admin = require("firebase-admin");
const functions = require("firebase-functions");

const DEFAULT_CAP_USD = 30;
const ADMIN_UIDS = [
  // TODO(CC): replace with Doron's actual Firebase UID after he signs in for the first time
  // "<doron_firebase_uid>",
];

/**
 * Pricing per million tokens (USD). Update when models change.
 * Sources: anthropic.com/pricing, ai.google.dev/pricing, openai.com/pricing
 */
const PRICING = {
  "claude-opus-4-7":  { input: 15.0, output: 75.0 },
  "gemini-2.5-pro":   { input:  1.25, output: 10.0 },
  "gpt-4o":           { input:  2.50, output: 10.0 },
  "gemini-vision":    { input:  1.25, output: 10.0 },
};

function currentMonth() {
  const d = new Date();
  return `${d.getUTCFullYear()}-${String(d.getUTCMonth() + 1).padStart(2, "0")}`;
}

async function getCapUsd() {
  // TODO(CC): read from Secret Manager `family-llm-monthly-cap-usd`
  // For now, return default.
  return DEFAULT_CAP_USD;
}

async function getBillingDoc() {
  const db = admin.firestore();
  const month = currentMonth();
  const ref = db.collection("family_billing").doc(month);
  const snap = await ref.get();
  if (!snap.exists) {
    const cap = await getCapUsd();
    const initial = {
      month,
      total_usd: 0,
      by_function: {},
      cap_usd: cap,
      killed: false,
      last_updated: admin.firestore.FieldValue.serverTimestamp(),
    };
    await ref.set(initial);
    return { ref, data: initial };
  }
  return { ref, data: snap.data() };
}

/**
 * Throws functions.https.HttpsError('resource-exhausted', ...) if estimated
 * spend would exceed cap. Admin UIDs bypass.
 */
async function checkBudgetOrThrow(functionName, estimateUsd, context) {
  const isAdmin = context?.auth?.uid && ADMIN_UIDS.includes(context.auth.uid);
  if (isAdmin) return; // bypass

  const { data } = await getBillingDoc();
  if (data.killed) {
    throw new functions.https.HttpsError(
      "resource-exhausted",
      `Monthly LLM cap of $${data.cap_usd} reached. Reset on day 1 of next month, or ask admin to bypass.`
    );
  }
  if (data.total_usd + estimateUsd > data.cap_usd) {
    throw new functions.https.HttpsError(
      "resource-exhausted",
      `This call would bring monthly spend to $${(data.total_usd + estimateUsd).toFixed(2)}, ` +
      `exceeding cap of $${data.cap_usd}. Try again next month or contact admin.`
    );
  }
}

/**
 * Record actual spend after an LLM call completes.
 * Triggers email notifications at 50/75/90/100% thresholds.
 */
async function recordSpend(functionName, actualUsd) {
  const db = admin.firestore();
  const month = currentMonth();
  const ref = db.collection("family_billing").doc(month);

  const result = await db.runTransaction(async (tx) => {
    const snap = await tx.get(ref);
    const cap = (snap.exists ? snap.data().cap_usd : null) || await getCapUsd();
    const prevTotal = snap.exists ? (snap.data().total_usd || 0) : 0;
    const prevByFn = snap.exists ? (snap.data().by_function || {}) : {};

    const newTotal = prevTotal + actualUsd;
    const newByFn = {
      ...prevByFn,
      [functionName]: (prevByFn[functionName] || 0) + actualUsd,
    };
    const killed = newTotal >= cap;

    const update = {
      month,
      total_usd: newTotal,
      by_function: newByFn,
      cap_usd: cap,
      killed,
      last_updated: admin.firestore.FieldValue.serverTimestamp(),
    };
    tx.set(ref, update, { merge: true });

    return { prevTotal, newTotal, cap, killed };
  });

  // Threshold notifications
  const { prevTotal, newTotal, cap } = result;
  const thresholds = [0.5, 0.75, 0.9, 1.0];
  for (const t of thresholds) {
    const tUsd = cap * t;
    if (prevTotal < tUsd && newTotal >= tUsd) {
      // TODO(CC): send notification via Microsoft Graph (reuse RPA-PORT credentials
      // from Secret Manager). Subject e.g. "Family-tree LLM spend hit 75% ($22.50 of $30)".
      console.log(`BUDGET ALERT: crossed ${(t * 100).toFixed(0)}% threshold ($${tUsd.toFixed(2)})`);
    }
  }

  return result;
}

/**
 * Rough cost estimate for a translation call (3-AI consensus).
 * Used by checkBudgetOrThrow before the actual call.
 */
function estimateTranslateCost(sourceTextLen) {
  // Rough: 4 chars/token, 3 models, ~2x output of input
  const inputTokens = sourceTextLen / 4;
  const outputTokens = inputTokens * 2;

  let total = 0;
  for (const model of ["claude-opus-4-7", "gemini-2.5-pro", "gpt-4o"]) {
    const p = PRICING[model];
    total += (inputTokens / 1e6) * p.input + (outputTokens / 1e6) * p.output;
  }
  return total;
}

function estimateAssistantCost(corpusTokens, questionTokens, expectedAnswerTokens) {
  const inputTokens = corpusTokens + questionTokens;
  const outputTokens = expectedAnswerTokens;
  const p = PRICING["claude-opus-4-7"];
  return (inputTokens / 1e6) * p.input + (outputTokens / 1e6) * p.output;
}

module.exports = {
  checkBudgetOrThrow,
  recordSpend,
  estimateTranslateCost,
  estimateAssistantCost,
  currentMonth,
  PRICING,
};
