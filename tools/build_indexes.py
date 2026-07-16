#!/usr/bin/env python3
"""Build public indexes from canonical VizAI entity profiles.

Production source of truth:
    registry/<entity-slug>/profile.json

No legacy record shape or alternate source directory is accepted.
"""

import json
from collections import defaultdict
from pathlib import Path


def _profile_path_is_canonical(path, registry_path):
    relative = path.relative_to(registry_path)
    return len(relative.parts) == 2 and relative.name == "profile.json"


def find_all_entries(registry_path):
    """Load every canonical profile and reject alternate registry layouts."""
    registry_path = Path(registry_path)
    json_paths = sorted(registry_path.rglob("*.json"))
    unexpected = [
        path.relative_to(registry_path).as_posix()
        for path in json_paths
        if not _profile_path_is_canonical(path, registry_path)
    ]
    if unexpected:
        formatted = "\n  - ".join(unexpected)
        raise ValueError(
            "Non-canonical JSON found below registry/. "
            "Only registry/<entity-slug>/profile.json is supported:\n"
            f"  - {formatted}"
        )

    entries = []
    for json_path in json_paths:
        with json_path.open("r", encoding="utf-8") as handle:
            entry = json.load(handle)
        if not (
            entry.get("schemaVersion") == "1.0"
            and entry.get("entitySlug")
            and entry.get("businessIdentifier")
        ):
            raise ValueError(
                f"{json_path.relative_to(registry_path).as_posix()} "
                "is not an entity-profile-v1.0 record"
            )
        entry["_file"] = json_path.relative_to(registry_path).as_posix()
        entries.append(entry)

    return sorted(entries, key=lambda entry: entry["entitySlug"])


def country_code(value):
    if not value:
        return "unknown"
    normalized = str(value).strip()
    if len(normalized) == 2:
        return normalized.upper()
    known = {
        "canada": "CA",
        "united states": "US",
        "usa": "US",
        "u.s.": "US",
        "us": "US",
        "united kingdom": "GB",
        "uk": "GB",
    }
    return known.get(normalized.lower(), normalized)


def normalize_entry(entry):
    """Return canonical fields used by grouped indexes."""
    identifier = entry["businessIdentifier"]
    profile = entry.get("profile", {}) or {}
    verification = entry["verification"]
    country = country_code(profile.get("country"))

    locations = [
        {
            "country": country,
            "region": location.get("region", "unknown"),
            "city": location.get("name", "unknown"),
        }
        for location in profile.get("locations", []) or []
    ]
    if not locations:
        scale = profile.get("scale", {}) or {}
        locations = [
            {
                "country": country,
                "region": scale.get("region", "unknown"),
                "city": "unknown",
            }
        ]

    return {
        "entitySlug": entry["entitySlug"],
        "domain": identifier["primaryDomain"],
        "name": identifier.get("commonName") or identifier["legalName"],
        "category": entry["category"],
        "services": profile.get("services", []) or [],
        "status": verification["status"],
        "locations": locations,
        "file": entry["_file"],
    }


def summary(normalized):
    return {
        "entitySlug": normalized["entitySlug"],
        "domain": normalized["domain"],
        "name": normalized["name"],
        "locations": normalized["locations"],
        "file": normalized["file"],
    }


def clean_entry(entry):
    return {key: value for key, value in entry.items() if key != "_file"}


def build_by_domain(entries):
    return {
        normalize_entry(entry)["domain"]: clean_entry(entry)
        for entry in entries
    }


def build_by_location(entries):
    grouped = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for entry in entries:
        normalized = normalize_entry(entry)
        for location in normalized["locations"]:
            grouped[location["country"]][location["region"]][location["city"]].append(
                {
                    "entitySlug": normalized["entitySlug"],
                    "domain": normalized["domain"],
                    "name": normalized["name"],
                    "file": normalized["file"],
                }
            )
    return {
        country: {
            region: dict(cities)
            for region, cities in regions.items()
        }
        for country, regions in grouped.items()
    }


def build_by_service(entries):
    grouped = defaultdict(list)
    for entry in entries:
        normalized = normalize_entry(entry)
        for service in normalized["services"]:
            grouped[service].append(summary(normalized))
    return dict(grouped)


def build_by_industry(entries):
    grouped = defaultdict(list)
    for entry in entries:
        normalized = normalize_entry(entry)
        grouped[normalized["category"]].append(summary(normalized))
    return dict(grouped)


def build_by_status(entries):
    grouped = defaultdict(list)
    for entry in entries:
        normalized = normalize_entry(entry)
        grouped[normalized["status"]].append(
            {
                "entitySlug": normalized["entitySlug"],
                "domain": normalized["domain"],
                "name": normalized["name"],
                "file": normalized["file"],
            }
        )
    return dict(grouped)


def build_jsonl(entries):
    return [
        json.dumps(clean_entry(entry), separators=(",", ":"), sort_keys=True)
        for entry in entries
    ]


def build_outputs(entries):
    """Build every committed index in memory."""
    return {
        "by-domain.json": build_by_domain(entries),
        "by-location.json": build_by_location(entries),
        "by-service.json": build_by_service(entries),
        "by-industry.json": build_by_industry(entries),
        "by-status.json": build_by_status(entries),
        "businesses.jsonl": build_jsonl(entries),
    }


def write_outputs(outputs, index_path):
    index_path = Path(index_path)
    index_path.mkdir(exist_ok=True)
    for filename, data in outputs.items():
        output_path = index_path / filename
        if filename.endswith(".jsonl"):
            output_path.write_text(
                "".join(f"{line}\n" for line in data),
                encoding="utf-8",
                newline="\n",
            )
        else:
            output_path.write_text(
                json.dumps(data, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
                newline="\n",
            )


def main():
    repository = Path(__file__).resolve().parent.parent
    entries = find_all_entries(repository / "registry")
    outputs = build_outputs(entries)
    write_outputs(outputs, repository / "index")

    print(f"Built canonical indexes from {len(entries)} entity profiles")
    print(f"  domains: {len(outputs['by-domain.json'])}")
    print(f"  countries: {len(outputs['by-location.json'])}")
    print(f"  services: {len(outputs['by-service.json'])}")
    print(f"  categories: {len(outputs['by-industry.json'])}")
    print(f"  statuses: {len(outputs['by-status.json'])}")


if __name__ == "__main__":
    main()
