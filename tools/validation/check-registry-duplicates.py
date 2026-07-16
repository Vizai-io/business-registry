#!/usr/bin/env python3
"""Check canonical registry profiles for duplicate domains and entity slugs."""

import json
import sys
from collections import defaultdict
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parent.parent.parent
REGISTRY = REPOSITORY / "registry"


def canonical_profile_paths():
    json_paths = sorted(REGISTRY.rglob("*.json"))
    unexpected = []
    canonical = []
    for path in json_paths:
        relative = path.relative_to(REGISTRY)
        if len(relative.parts) == 2 and relative.name == "profile.json":
            canonical.append(path)
        else:
            unexpected.append(relative.as_posix())
    return canonical, unexpected


def duplicates(values):
    return {
        value: paths
        for value, paths in values.items()
        if len(paths) > 1
    }


def main():
    paths, unexpected = canonical_profile_paths()
    if unexpected:
        print("FAIL: non-canonical JSON exists below registry/:")
        for path in unexpected:
            print(f"  - {path}")
        return 1

    domains = defaultdict(list)
    slugs = defaultdict(list)
    for path in paths:
        profile = json.loads(path.read_text(encoding="utf-8"))
        relative = path.relative_to(REPOSITORY).as_posix()
        domain = profile.get("businessIdentifier", {}).get("primaryDomain")
        slug = profile.get("entitySlug")
        if domain:
            domains[domain.lower()].append(relative)
        if slug:
            slugs[slug].append(relative)

    duplicate_domains = duplicates(domains)
    duplicate_slugs = duplicates(slugs)

    print(f"Scanned {len(paths)} canonical entity profiles")
    print(
        f"Unique domains: {len(domains)} | "
        f"Duplicate domains: {len(duplicate_domains)}"
    )
    print(
        f"Unique entity slugs: {len(slugs)} | "
        f"Duplicate entity slugs: {len(duplicate_slugs)}"
    )

    if duplicate_domains or duplicate_slugs:
        for label, found in (
            ("domain", duplicate_domains),
            ("entity slug", duplicate_slugs),
        ):
            for value, files in sorted(found.items()):
                print(f"\nDuplicate {label}: {value}")
                for file in files:
                    print(f"  - {file}")
        return 1

    print("No duplicate canonical identities found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
