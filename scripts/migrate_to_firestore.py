#!/usr/bin/env python3
"""
Migrate JSON seed data to Firestore family_* collections.

Idempotent: re-running upserts (set with merge), never duplicates.
Logs every write to family_audit.

Usage:
    # First time: set up Application Default Credentials
    gcloud auth application-default login

    # Then run from repo root
    python3 scripts/migrate_to_firestore.py --project rpa-port-prod --confirm

    # Dry run (default, no writes)
    python3 scripts/migrate_to_firestore.py --project rpa-port-prod

CC: complete the TODOs marked below before running for real.
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# TODO(CC): pip install firebase-admin in the functions/ env or a venv
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
except ImportError:
    print("ERROR: firebase-admin not installed. Run: pip install firebase-admin")
    sys.exit(1)


REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "platform" / "data"
I18N_DIR = DATA_DIR / "i18n"

# Mapping: source JSON file → Firestore collection → ID field
COLLECTION_MAP = [
    {"file": "people.json",     "collection": "family_people",     "id_field": "id"},
    {"file": "places.json",     "collection": "family_places",     "id_field": "id"},
    {"file": "events.json",     "collection": "family_events",     "id_field": "id"},
    {"file": "documents.json",  "collection": "family_documents",  "id_field": "id"},
    {"file": "hypotheses.json", "collection": "family_hypotheses", "id_field": "id"},
    {"file": "messages.json",   "collection": "family_messages",   "id_field": "id"},
]

I18N_LANGUAGES = ["en", "he", "pl", "fr"]


def hash_doc(d: dict) -> str:
    """Stable hash for audit trail."""
    return hashlib.sha256(
        json.dumps(d, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def normalize_records(raw, id_field: str):
    """
    Accept either a list of records or a dict with a top-level 'items'/'people'/etc. key.
    Yield (doc_id, record) tuples.
    """
    if isinstance(raw, list):
        records = raw
    elif isinstance(raw, dict):
        # Common wrappers
        for key in ("items", "people", "places", "events", "documents", "hypotheses", "messages", "records"):
            if key in raw and isinstance(raw[key], list):
                records = raw[key]
                break
        else:
            # Treat as a single record
            records = [raw]
    else:
        raise ValueError(f"Unexpected JSON shape: {type(raw)}")

    for rec in records:
        if id_field not in rec:
            raise ValueError(f"Record missing id field '{id_field}': {rec.get('name', rec)}")
        yield rec[id_field], rec


def upsert_with_audit(db, collection: str, doc_id: str, data: dict, actor_uid: str, dry_run: bool):
    """Write to Firestore + append family_audit entry."""
    coll_ref = db.collection(collection)
    doc_ref = coll_ref.document(doc_id)

    # Get current state for audit
    snapshot = doc_ref.get()
    before_hash = hash_doc(snapshot.to_dict()) if snapshot.exists else None
    after_hash = hash_doc(data)

    if before_hash == after_hash:
        return "unchanged"

    if dry_run:
        return "would_write"

    # Stamp updated metadata
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    data["updated_by"] = actor_uid

    # Write
    doc_ref.set(data, merge=True)

    # Audit
    audit_ref = db.collection("family_audit").document()
    audit_ref.set({
        "ts": datetime.now(timezone.utc).isoformat(),
        "uid": actor_uid,
        "collection": collection,
        "doc_id": doc_id,
        "action": "create" if before_hash is None else "update",
        "before_hash": before_hash,
        "after_hash": after_hash,
        "summary": f"Migration seed from JSON",
    })

    return "created" if before_hash is None else "updated"


def migrate_i18n(db, actor_uid: str, dry_run: bool):
    """i18n strings: one Firestore doc per language."""
    results = []
    for lang in I18N_LANGUAGES:
        path = I18N_DIR / f"{lang}.json"
        if not path.exists():
            print(f"  ⚠️  Missing i18n file: {path}")
            continue

        strings = load_json(path)
        doc = {
            "id": lang,
            "version": "1.0.0",
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "strings": strings,
        }
        result = upsert_with_audit(db, "family_i18n", lang, doc, actor_uid, dry_run)
        results.append((lang, result))
        print(f"  {lang}: {result}")
    return results


def migrate_collection(db, file_name: str, collection: str, id_field: str, actor_uid: str, dry_run: bool):
    path = DATA_DIR / file_name
    if not path.exists():
        print(f"  ❌  Missing source file: {path}")
        return []

    raw = load_json(path)
    results = {"created": 0, "updated": 0, "unchanged": 0, "would_write": 0}
    count = 0
    for doc_id, record in normalize_records(raw, id_field):
        result = upsert_with_audit(db, collection, doc_id, record, actor_uid, dry_run)
        results[result] = results.get(result, 0) + 1
        count += 1

    print(f"  {collection}: {count} records | " +
          " | ".join(f"{k}: {v}" for k, v in results.items() if v))
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, help="Firebase project ID (e.g. rpa-port-prod)")
    parser.add_argument("--confirm", action="store_true", help="Actually write (default: dry run)")
    parser.add_argument("--actor", default="migration_script", help="UID to record in audit log")
    parser.add_argument("--credentials", default=None, help="Path to service account JSON (default: ADC)")
    args = parser.parse_args()

    dry_run = not args.confirm

    # Initialize Firebase Admin
    if args.credentials:
        cred = credentials.Certificate(args.credentials)
        firebase_admin.initialize_app(cred, {"projectId": args.project})
    else:
        # Application Default Credentials
        firebase_admin.initialize_app(options={"projectId": args.project})

    db = firestore.client()

    mode = "DRY RUN (no writes)" if dry_run else "LIVE WRITE"
    print(f"\n{'='*60}")
    print(f"Rapaport Family Tree — Firestore Migration")
    print(f"Project: {args.project}")
    print(f"Mode: {mode}")
    print(f"Actor: {args.actor}")
    print(f"{'='*60}\n")

    print("[1/2] Migrating entity collections")
    print("-" * 60)
    for spec in COLLECTION_MAP:
        migrate_collection(db, spec["file"], spec["collection"], spec["id_field"], args.actor, dry_run)

    print("\n[2/2] Migrating i18n string tables")
    print("-" * 60)
    migrate_i18n(db, args.actor, dry_run)

    print(f"\n{'='*60}")
    if dry_run:
        print("Dry run complete. Re-run with --confirm to write.")
    else:
        print("Migration complete. Check Firestore console.")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
