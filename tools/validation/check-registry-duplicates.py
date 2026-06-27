#!/usr/bin/env python3
"""
Whole-repo duplicate detection for the VizAI Business Registry (DEC-029 / WP-13).

Scans BOTH data/** and registry/** (not just data/**, which the legacy CI did).
Reads the primary domain from either nested (businessIdentifier.primaryDomain) or
flat (domain) layouts, so it works across the lightweight, registry-entry, and
entity-profile schemas during the migration window.

Known-pending duplicates (e.g. the VizAI record that exists in both data/verified/
and registry/ca/on/toronto/) are reported as KNOWN and do not fail the build — they
are slated for resolution in the registry migration (WP-13 follow-on). NEW duplicates
fail the build.
"""

import json
import sys
from pathlib import Path
from collections import defaultdict

REPO = Path(__file__).parent.parent.parent

# Domains with a known, documented duplicate pending migration. Not a build failure.
# (vizai.io retired: canonicalized to a single registry/vizai/profile.json; the two legacy
#  records [data/verified/vizai.json + registry/ca/on/toronto/vizai.json] were removed.)
KNOWN_PENDING_DUPLICATES = {}


def primary_domain(entry):
    return (
        entry.get("domain")
        or entry.get("businessIdentifier", {}).get("primaryDomain")
    )


def scan(dir_name):
    found = defaultdict(list)
    base = REPO / dir_name
    if not base.exists():
        return found
    for path in base.rglob("*.json"):
        if path.name == "index.json":
            continue
        try:
            entry = json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  warn: could not read {path}: {e}")
            continue
        dom = primary_domain(entry)
        if dom:
            found[dom.lower()].append(str(path.relative_to(REPO)))
    return found


def main():
    domains = defaultdict(list)
    for d in ("data", "registry"):
        for dom, files in scan(d).items():
            domains[dom].extend(files)

    duplicates = {dom: files for dom, files in domains.items() if len(files) > 1}

    print(f"Scanned {sum(len(v) for v in domains.values())} entries across data/ and registry/")
    print(f"Unique domains: {len(domains)} | Duplicated domains: {len(duplicates)}\n")

    if not duplicates:
        print("No duplicate domains found.")
        sys.exit(0)

    new_dups = False
    for dom, files in sorted(duplicates.items()):
        if dom in KNOWN_PENDING_DUPLICATES:
            print(f"[KNOWN] {dom}")
            print(f"        {KNOWN_PENDING_DUPLICATES[dom]}")
        else:
            print(f"[NEW DUPLICATE] {dom}")
            new_dups = True
        for f in files:
            print(f"          - {f}")
        print()

    if new_dups:
        print("FAIL: new duplicate domain(s) detected.")
        sys.exit(1)
    print("PASS: only known-pending duplicates present (tracked for migration).")
    sys.exit(0)


if __name__ == "__main__":
    main()
