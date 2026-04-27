#!/usr/bin/env python3
"""
Generate index files for the registry.

This helps with discovery and querying without cloning the entire repo.
Discovery profiles are lightweight - just domain, name, verification status.
"""

import json
from pathlib import Path
from datetime import date
from collections import defaultdict


def generate_tier_index(tier_path, tier_name):
    """Generate index for a specific tier (verified/community/enterprise).
    
    With lightweight profiles, we store profiles flat in the tier directory.
    The category is read from each profile's 'category' field.
    """
    
    tier_data = {
        "tier": tier_name,
        "lastUpdated": str(date.today()),
        "lastIndexed": str(date.today()),
        "count": 0,
        "byCategory": defaultdict(lambda: {"count": 0, "profiles": []}),
        "profiles": []
    }

    if not tier_path.exists():
        print(f"  Tier directory does not exist: {tier_path}")
        return tier_data

    # Find all JSON files (excluding index.json)
    for profile_path in tier_path.glob("*.json"):
        if profile_path.name == "index.json":
            continue

        try:
            with open(profile_path, 'r') as f:
                profile = json.load(f)

            # Get category from profile (default to "other")
            category = profile.get("category", "other")
            
            # Extract key info for index
            profile_summary = {
                "file": profile_path.name,
                "domain": profile["businessIdentifier"]["primaryDomain"],
                "commonName": profile["businessIdentifier"]["commonName"],
                "legalName": profile["businessIdentifier"].get("legalName"),
                "category": category,
                "status": profile["verification"]["status"],
                "lastVerified": profile["verification"]["lastVerified"],
                "qualityScore": profile.get("verification", {}).get("qualityScore"),
            }
            
            tier_data["profiles"].append(profile_summary)
            tier_data["byCategory"][category]["count"] += 1
            tier_data["byCategory"][category]["profiles"].append({
                "file": profile_path.name,
                "domain": profile["businessIdentifier"]["primaryDomain"],
                "commonName": profile["businessIdentifier"]["commonName"],
            })
            tier_data["count"] += 1

        except Exception as e:
            print(f"  Error processing {profile_path}: {e}")
            continue

    # Sort profiles by common name
    tier_data["profiles"].sort(key=lambda p: p["commonName"].lower())
    
    # Convert defaultdict to regular dict for JSON serialization
    tier_data["byCategory"] = dict(tier_data["byCategory"])
    for cat_data in tier_data["byCategory"].values():
        cat_data["profiles"].sort(key=lambda p: p["commonName"].lower())

    # Write tier index
    index_path = tier_path / "index.json"
    with open(index_path, 'w') as f:
        json.dump(tier_data, f, indent=2)

    print(f"  Generated {index_path} ({tier_data['count']} profiles)")
    return tier_data


def generate_master_index(data_path, tier_data_map):
    """Generate master index across all tiers."""

    master = {
        "lastUpdated": str(date.today()),
        "lastIndexed": str(date.today()),
        "tiers": {},
        "totalProfiles": 0,
        "categories": set(),
        "byCategory": defaultdict(lambda: {"verified": 0, "community": 0, "enterprise": 0})
    }

    for tier_name, tier_data in tier_data_map.items():
        master["tiers"][tier_name] = tier_data["count"]
        master["totalProfiles"] += tier_data["count"]
        
        for category in tier_data.get("byCategory", {}).keys():
            master["categories"].add(category)
            master["byCategory"][category][tier_name] = tier_data["byCategory"][category]["count"]

    # Convert sets and defaultdicts
    master["categories"] = sorted(list(master["categories"]))
    master["byCategory"] = dict(master["byCategory"])

    # Write master index
    master_path = data_path / "index.json"
    with open(master_path, 'w') as f:
        json.dump(master, f, indent=2)

    print(f"\nGenerated master index: {master_path}")
    print(f"Total profiles: {master['totalProfiles']}")
    print(f"Categories: {master['categories']}")


def main():
    repo_root = Path(__file__).parent.parent.parent
    data_path = repo_root / "data"

    print("Generating indexes for discovery profiles...")
    
    tier_data_map = {}
    
    for tier in ["verified", "community", "enterprise"]:
        tier_path = data_path / tier
        print(f"\nProcessing tier: {tier}")
        
        if not tier_path.exists():
            print(f"  Creating directory: {tier_path}")
            tier_path.mkdir(parents=True, exist_ok=True)
        
        tier_data_map[tier] = generate_tier_index(tier_path, tier)

    # Generate master index
    print("\nGenerating master index...")
    generate_master_index(data_path, tier_data_map)

    print("\nIndex generation complete!")


if __name__ == "__main__":
    main()