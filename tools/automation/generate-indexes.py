#!/usr/bin/env python3
"""
Generate index files for each category in the registry.

This helps with discovery and querying without cloning the entire repo.
"""

import json
from pathlib import Path
from datetime import date
from collections import defaultdict


def generate_index(tier_path, tier_name):
    """Generate index for a specific tier (verified/community/enterprise)."""

    indexes = defaultdict(lambda: {
        "tier": tier_name,
        "lastUpdated": str(date.today()),
        "count": 0,
        "profiles": []
    })

    # Find all JSON files (excluding index.json files)
    for profile_path in tier_path.rglob("*.json"):
        if profile_path.name == "index.json":
            continue

        # Determine category from path
        relative = profile_path.relative_to(tier_path)
        category = relative.parts[0] if len(relative.parts) > 1 else "other"

        try:
            with open(profile_path, 'r') as f:
                profile = json.load(f)

            # Extract key info for index
            indexes[category]["category"] = category
            indexes[category]["count"] += 1
            indexes[category]["profiles"].append({
                "file": str(relative.as_posix()),
                "domain": profile["businessIdentifier"]["primaryDomain"],
                "commonName": profile["businessIdentifier"]["commonName"],
                "legalName": profile["businessIdentifier"]["legalName"],
                "lastVerified": profile["verification"]["lastVerified"],
                "qualityScore": profile.get("verification", {}).get("qualityScore"),
            })

        except Exception as e:
            print(f"Error processing {profile_path}: {e}")
            continue

    # Write index files
    for category, index_data in indexes.items():
        # Sort profiles by common name
        index_data["profiles"].sort(key=lambda p: p["commonName"].lower())

        index_path = tier_path / category / "index.json"
        index_path.parent.mkdir(parents=True, exist_ok=True)

        with open(index_path, 'w') as f:
            json.dump(index_data, f, indent=2)

        print(f"Generated index: {index_path} ({index_data['count']} profiles)")


def generate_master_index(data_path):
    """Generate master index across all tiers."""

    master = {
        "lastUpdated": str(date.today()),
        "tiers": {},
        "totalProfiles": 0,
        "categories": set()
    }

    for tier_dir in data_path.iterdir():
        if not tier_dir.is_dir() or tier_dir.name.startswith('.'):
            continue

        tier_name = tier_dir.name
        tier_count = 0

        for category_dir in tier_dir.iterdir():
            if not category_dir.is_dir():
                continue

            category = category_dir.name
            master["categories"].add(category)

            # Count profiles in this category
            profile_count = len(list(category_dir.glob("*.json"))) - \
                          (1 if (category_dir / "index.json").exists() else 0)
            tier_count += profile_count

        master["tiers"][tier_name] = tier_count
        master["totalProfiles"] += tier_count

    # Convert set to sorted list
    master["categories"] = sorted(list(master["categories"]))

    # Write master index
    master_path = data_path / "index.json"
    with open(master_path, 'w') as f:
        json.dump(master, f, indent=2)

    print(f"\nGenerated master index: {master_path}")
    print(f"Total profiles: {master['totalProfiles']}")


def main():
    # Get repository root
    repo_root = Path(__file__).parent.parent.parent
    data_path = repo_root / "data"

    # Generate indexes for each tier
    for tier in ["verified", "community", "enterprise"]:
        tier_path = data_path / tier
        if tier_path.exists():
            print(f"\nGenerating indexes for {tier}...")
            generate_index(tier_path, tier)

    # Generate master index
    print("\nGenerating master index...")
    generate_master_index(data_path)


if __name__ == "__main__":
    main()
