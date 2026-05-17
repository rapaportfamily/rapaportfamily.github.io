# Get a free Gemini API key (5 minutes)

This unlocks the auto-verification feature: every doc you upload gets read by Gemini, which searches the web for corroborating evidence and writes a verification report — all free, up to 1500 requests/day.

---

## Step-by-step

### 1. Open Google AI Studio

In your Chrome (already signed in as **doronrpa@gmail.com**), open:

> **https://aistudio.google.com/apikey**

If it asks you to accept terms — click **"I accept"** at the bottom. (Google AI Studio is free, no credit card needed.)

### 2. You should see a page titled "API keys"

There will be either:
- An empty page with a big blue **"Create API key"** button, or
- A list of existing keys with a **"+ Create API key"** button at the top

Click that button.

### 3. Choose a project

A small popup will ask "Create API key in which project?"

- If you see a project called **"Rapaport Family Tree"** or **"rapaport-family-tree-4482"** in the list — pick it.
- Otherwise pick the default suggested project, OR choose "Create API key in new project" — either works.

Click **"Create API key"**.

### 4. Copy the key

The key looks like a long string starting with `AIza` — for example:

```
AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Tap the **copy icon** next to it to copy the whole string to clipboard.

### 5. Paste it here in chat

Just paste the key as your next message. I'll handle everything else — storing it securely in Firebase, deploying the Cloud Function that calls Gemini, wiring it into the upload review queue.

---

## What if it doesn't work?

| What you see | What to do |
|---|---|
| "You don't have access to this feature in your region" | Tell me — there's a workaround using a different Google API |
| "API key creation failed" | Try again in a fresh tab; sometimes the first attempt times out |
| You don't see "Create API key" button | You may need to first agree to Google's AI terms — look for an "I accept" / "Get started" button |
| The page is in Hebrew | That's fine — same flow, button is "צור מפתח API" |

---

## What I'll do with it

1. **Store as Firebase secret** (`firebase functions:secrets:set GEMINI_API_KEY`) — never committed to git, never visible to anyone but the Cloud Function
2. **Deploy a Cloud Function** that fires on every new upload to `family_uploads`
3. **Cloud Function calls Gemini 2.5 Flash** with:
   - The uploaded file (Vision for photos, text for chat exports, OCR for PDFs)
   - The family research context (people, places, events, hypotheses)
   - Google Search grounding ON — Gemini autonomously searches the web for confirming/contradicting evidence
4. **Writes verification report** to the Firestore doc — visible in your admin review queue as a "🤖 Gemini says…" card with: what this confirms / contradicts / adds / what to search next
5. **Sets a 1000-req/day cap** so we stay under the free tier — safety cap costs nothing even at worst case
