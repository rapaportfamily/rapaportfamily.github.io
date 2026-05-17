// Firebase init for the Rapaport Family Tree platform.
// Used by the upload + admin-queue features. Read-only browsing of the static
// JSON data does NOT touch Firebase.
//
// The firebaseConfig values below are safe to commit publicly:
//   - apiKey is a *project identifier*, not a credential
//   - Authorization comes from Firestore + Storage security rules + Anonymous Auth
//   - The site is already gated by the magic-link JWT (assets/js/auth-gate.js)

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-app.js";
import { getAuth, signInAnonymously, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-auth.js";
import { getFirestore, collection, addDoc, query, where, orderBy, getDocs, doc, updateDoc, deleteDoc, serverTimestamp } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-firestore.js";
import { getStorage, ref as storageRef, uploadBytes, getDownloadURL, deleteObject } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-storage.js";

export const firebaseConfig = {
  projectId: "rapaport-family-tree-4482",
  appId: "1:1033066063501:web:ed4ecf3d3b2e55d76c64c4",
  storageBucket: "rapaport-family-tree-4482.firebasestorage.app",
  apiKey: "AIzaSyDg6HJ2iiffK8P6ym335HAafB6e96pNpUU",
  authDomain: "rapaport-family-tree-4482.firebaseapp.com",
  messagingSenderId: "1033066063501",
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);
export const storage = getStorage(app);

// Re-export the bits the rest of the app needs (so app.js stays import-flat).
export {
  signInAnonymously, onAuthStateChanged,
  collection, addDoc, query, where, orderBy, getDocs, doc, updateDoc, deleteDoc, serverTimestamp,
  storageRef, uploadBytes, getDownloadURL, deleteObject,
};

/**
 * Ensure we have an anonymous Firebase UID for the current page session.
 * The user's *real* identity comes from window.__rftAuth (set by the magic-link gate).
 * Firebase Anonymous Auth just gives us an ephemeral UID so security rules can
 * gate writes to "any signed-in browser" — which combined with the magic-link
 * gate means "any browser that loaded the site with a valid token".
 */
export async function ensureFirebaseAuth() {
  return new Promise((resolve, reject) => {
    const unsub = onAuthStateChanged(auth, async (user) => {
      if (user) { unsub(); resolve(user); return; }
      try { await signInAnonymously(auth); } catch (e) { unsub(); reject(e); }
    });
  });
}
