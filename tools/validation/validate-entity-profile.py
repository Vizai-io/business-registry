#!/usr/bin/env python3
"""
VizAI Entity Profile Validator (Model C, DEC-029).

Validates a public entity profile (registry/<slug>/profile.json) with three gates:
  1. Schema       — entity-profile-v1.0.schema.json (structure, enums, forbidden fields)
  2. Clean artifact (DEC-028) — raw-text scan for internal/working-file leakage
  3. Evidence gate (DEC-027)  — any public credential must be evidence_verified + public

Usage:
  python validate-entity-profile.py registry/wills-transfer/profile.json
Exit code 0 = all gates pass; 1 = any gate fails.
"""

import json
import re
import sys
from pathlib import Path
from jsonschema import validate, ValidationError

SCHEMA_PATH = Path(__file__).parent.parent.parent / "schema" / "entity-profile-v1.0.schema.json"

# DEC-028: high-signal markers that should NEVER appear in a clean public profile.
# These indicate a working/governance file leaked into public exposure.
FORBIDDEN_MARKERS = [
    "do_not_publish", "do not publish",
    "held_from_this_publication", "held from this publication",
    "needs evidence", "no_evidence_provided", "evidence_requested",
    "evidence_received", "expired_or_stale", "evidence_register",
    "evidence ledger", "evidenceledger",
    "truth_canon", "truthcanon", "truth canon",
    "pending_facts", "pendingfacts",
    "verification_worksheet", "verification_log", "worksheet",
    "onboarding-response", "onboarding_response",
    "publication_plan", "implementation_note", "implementation note",
    "reconfirm", "internal note", "internalnote", "internal-note",
    "working file", "golden rule", "blueprint-driven",
]
# Regex markers (BDE packet/decision vocabulary)
FORBIDDEN_REGEX = [r"\bWP-\d", r"\bDEC-\d{2,}"]

# DEC-027: legacy/ungated claim containers that must not carry claims in a public profile.
UNGATED_CLAIM_KEYS = ["certifications", "memberships", "awards"]


def load_schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def gate_schema(profile, profile_path):
    try:
        validate(instance=profile, schema=load_schema())
        print(f"  [schema]    PASS")
        return True
    except ValidationError as e:
        print(f"  [schema]    FAIL: {e.message}")
        print(f"              at: {' -> '.join(str(p) for p in e.path) or '(root)'}")
        return False


def gate_clean_artifact(raw_text):
    lower = raw_text.lower()
    hits = [m for m in FORBIDDEN_MARKERS if m in lower]
    for rx in FORBIDDEN_REGEX:
        found = re.findall(rx, raw_text)
        hits.extend(found)
    if hits:
        print(f"  [clean]     FAIL (DEC-028): forbidden markers found: {sorted(set(hits))}")
        return False
    print(f"  [clean]     PASS")
    return True


def gate_evidence(profile):
    ok = True
    # Gated credentials block: every item must be evidence_verified + public
    for i, cred in enumerate(profile.get("credentials", []) or []):
        if cred.get("evidenceStatus") != "evidence_verified" or cred.get("publicPublishAllowed") is not True:
            print(f"  [evidence]  FAIL (DEC-027): credentials[{i}] '{cred.get('name','?')}' "
                  f"not evidence_verified+public")
            ok = False
    # Legacy ungated containers must be empty/absent
    for key in UNGATED_CLAIM_KEYS:
        val = profile.get(key)
        if val:
            print(f"  [evidence]  FAIL (DEC-027): ungated '{key}' present with claims — "
                  f"move to evidence-gated 'credentials' or the private Needs-Evidence list")
            ok = False
    if ok:
        print(f"  [evidence]  PASS")
    return ok


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate-entity-profile.py <profile.json> [<profile.json> ...]")
        sys.exit(1)

    overall = True
    for arg in sys.argv[1:]:
        p = Path(arg)
        print(f"Validating: {p}")
        if not p.exists():
            print(f"  ERROR: file not found")
            overall = False
            continue
        raw = p.read_text(encoding="utf-8")
        try:
            profile = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"  [json]      FAIL: {e}")
            overall = False
            continue

        r1 = gate_schema(profile, p)
        r2 = gate_clean_artifact(raw)
        r3 = gate_evidence(profile)
        passed = r1 and r2 and r3
        print(f"  RESULT: {'PASS' if passed else 'FAIL'}\n")
        overall = overall and passed

    print("ALL ENTITY PROFILES VALID" if overall else "ENTITY PROFILE VALIDATION FAILED")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()
