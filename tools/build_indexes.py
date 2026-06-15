#!/usr/bin/env python3
"""
Build index files for the VizAI Business Registry.

Generates multiple index formats for different access patterns:
- businesses.jsonl: All entries as JSON Lines
- by-domain.json: Fast lookup by domain
- by-location.json: Hierarchical by country/region/city
- by-service.json: Grouped by services offered
- by-industry.json: Grouped by industry category
- by-status.json: Grouped by verification status

Source of truth: registry/<...>/*.json. This generator understands TWO entry
shapes and normalizes them (WP-13B / DEC-029):
  - entity-profile-v1.0  (entity-primary: registry/<slug>/profile.json) — the
    canonical Model C public profile. Fields nest under businessIdentifier /
    profile / verification / category.
  - registry-entry       (legacy geo records: registry/<cc>/<region>/<city>/*.json)
    with top-level domain / registryId / location / industry / services.
Legacy records remain indexed for compatibility; every index record carries a
`shape` field so the two are clearly distinguishable.
"""

import json
from pathlib import Path
from collections import defaultdict

COUNTRY_CODES = {
    "canada": "CA", "united states": "US", "usa": "US", "u.s.": "US", "us": "US",
    "united kingdom": "GB", "uk": "GB",
}


def country_code(val):
    if not val:
        return "unknown"
    v = str(val).strip()
    if len(v) == 2:
        return v.upper()
    return COUNTRY_CODES.get(v.lower(), v)


def is_entity_profile(entry):
    """entity-profile-v1.0 vs legacy registry-entry."""
    return (
        entry.get("schemaVersion") == "1.0"
        and "entitySlug" in entry
        and "businessIdentifier" in entry
    )


def normalize_entry(entry):
    """Return a shape-agnostic view used by all index builders."""
    file = entry.get("_file")
    if is_entity_profile(entry):
        bid = entry.get("businessIdentifier", {}) or {}
        prof = entry.get("profile", {}) or {}
        ver = entry.get("verification", {}) or {}
        country = country_code(prof.get("country"))
        locations = []
        for loc in prof.get("locations", []) or []:
            locations.append({
                "country": country,
                "region": loc.get("region", "unknown"),
                "city": loc.get("name", "unknown"),
            })
        if not locations:
            scale = prof.get("scale", {}) or {}
            locations.append({"country": country, "region": scale.get("region", "unknown"), "city": "unknown"})
        return {
            "shape": "entity-profile-v1.0",
            "registryId": entry.get("entitySlug"),
            "domain": bid.get("primaryDomain"),
            "name": bid.get("commonName") or bid.get("legalName"),
            "industry": entry.get("category", "other"),
            "services": prof.get("services", []) or [],
            "status": ver.get("status"),
            "locations": locations,
            "file": file,
        }
    # legacy registry-entry
    loc = entry.get("location", {}) or {}
    return {
        "shape": "registry-entry",
        "registryId": entry.get("registryId"),
        "domain": entry.get("domain"),
        "name": entry.get("name"),
        "industry": entry.get("industry", "other"),
        "services": entry.get("services", []) or [],
        "status": (entry.get("verification", {}) or {}).get("status"),
        "locations": [{
            "country": loc.get("country", "unknown"),
            "region": loc.get("region", "unknown"),
            "city": loc.get("city", "unknown"),
        }],
        "file": file,
    }


def summary(norm):
    """Compact record used in the grouped indexes."""
    return {
        "registryId": norm["registryId"],
        "domain": norm["domain"],
        "name": norm["name"],
        "shape": norm["shape"],
        "locations": norm["locations"],
        "file": norm["file"],
    }


def find_all_entries(registry_path):
    """Find all registry entry JSON files (forward-slash relative paths)."""
    entries = []
    for json_path in registry_path.rglob("*.json"):
        if json_path.name == "index.json":
            continue
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                entry = json.load(f)
            entry["_file"] = json_path.relative_to(registry_path).as_posix()
            entries.append(entry)
        except Exception as e:
            print(f"Error reading {json_path}: {e}")
    return entries


def build_by_domain(entries):
    """Domain -> full clean entry (native shape preserved)."""
    result = {}
    for entry in entries:
        norm = normalize_entry(entry)
        if norm["domain"]:
            result[norm["domain"]] = {k: v for k, v in entry.items() if k != "_file"}
    return result


def build_by_location(entries):
    """Hierarchical country/region/city index (multi-location aware)."""
    location_index = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for entry in entries:
        norm = normalize_entry(entry)
        for loc in norm["locations"]:
            location_index[loc["country"]][loc["region"]][loc["city"]].append({
                "registryId": norm["registryId"],
                "domain": norm["domain"],
                "name": norm["name"],
                "shape": norm["shape"],
                "file": norm["file"],
            })
    return {c: {r: dict(cities) for r, cities in regions.items()} for c, regions in location_index.items()}


def build_by_service(entries):
    """Service -> businesses."""
    service_index = defaultdict(list)
    for entry in entries:
        norm = normalize_entry(entry)
        for service in norm["services"]:
            service_index[service].append(summary(norm))
    return dict(service_index)


def build_by_industry(entries):
    """Industry/category -> businesses."""
    industry_index = defaultdict(list)
    for entry in entries:
        norm = normalize_entry(entry)
        industry_index[norm["industry"] or "other"].append(summary(norm))
    return dict(industry_index)


def build_by_status(entries):
    """Verification status -> businesses (WP-13B)."""
    status_index = defaultdict(list)
    for entry in entries:
        norm = normalize_entry(entry)
        status_index[norm["status"] or "unknown"].append({
            "registryId": norm["registryId"],
            "domain": norm["domain"],
            "name": norm["name"],
            "shape": norm["shape"],
            "file": norm["file"],
        })
    return dict(status_index)


def build_jsonl(entries):
    """All entries as JSON Lines (native clean shape)."""
    for entry in entries:
        output_entry = {k: v for k, v in entry.items() if k != "_file"}
        yield json.dumps(output_entry)


def main():
    script_dir = Path(__file__).parent
    registry_path = script_dir.parent / "registry"
    index_path = script_dir.parent / "index"
    index_path.mkdir(exist_ok=True)

    print("Finding all registry entries...")
    entries = find_all_entries(registry_path)
    print(f"Found {len(entries)} entries")
    shapes = defaultdict(int)
    for e in entries:
        shapes["entity-profile-v1.0" if is_entity_profile(e) else "registry-entry"] += 1
    print(f"  shapes: {dict(shapes)}")

    print("\nBuilding indexes...")
    builders = {
        "by-domain.json": build_by_domain,
        "by-location.json": build_by_location,
        "by-service.json": build_by_service,
        "by-industry.json": build_by_industry,
        "by-status.json": build_by_status,
    }
    outputs = {}
    for filename, builder in builders.items():
        print(f"  Building {filename}...")
        data = builder(entries)
        with open(index_path / filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        outputs[filename] = data

    print("  Building businesses.jsonl...")
    with open(index_path / "businesses.jsonl", 'w', encoding='utf-8') as f:
        for line in build_jsonl(entries):
            f.write(line + "\n")

    print("\nIndexes built successfully!")
    print(f"  by-domain.json: {len(outputs['by-domain.json'])} entries")
    print(f"  by-location.json: {len(outputs['by-location.json'])} countries")
    print(f"  by-service.json: {len(outputs['by-service.json'])} services")
    print(f"  by-industry.json: {len(outputs['by-industry.json'])} industries")
    print(f"  by-status.json: {len(outputs['by-status.json'])} statuses")
    print(f"  businesses.jsonl: {len(entries)} entries")


if __name__ == "__main__":
    main()
