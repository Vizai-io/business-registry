#!/usr/bin/env python3
"""
Build index files for the VizAI Business Registry.

Generates multiple index formats for different access patterns:
- businesses.jsonl: All entries as JSON Lines
- by-domain.json: Fast lookup by domain
- by-location.json: Hierarchical by country/region/city
- by-service.json: Grouped by services offered
- by-industry.json: Grouped by industry category
"""

import json
from pathlib import Path
from collections import defaultdict
from datetime import date


def find_all_entries(registry_path):
    """Find all registry entry JSON files."""
    entries = []
    for json_path in registry_path.rglob("*.json"):
        if json_path.name == "index.json":
            continue
        try:
            with open(json_path, 'r') as f:
                entry = json.load(f)
            entry["_file"] = str(json_path.relative_to(registry_path))
            entries.append(entry)
        except Exception as e:
            print(f"Error reading {json_path}: {e}")
    return entries


def build_by_domain(entries):
    """Build domain-indexed lookup."""
    result = {}
    for entry in entries:
        if "domain" in entry:
            # Exclude internal _file field for clean output
            clean = {k: v for k, v in entry.items() if k != "_file"}
            result[entry["domain"]] = clean
    return result


def build_by_location(entries):
    """Build hierarchical location index."""
    location_index = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    
    for entry in entries:
        loc = entry.get("location", {})
        country = loc.get("country", "unknown")
        region = loc.get("region", "unknown")
        city = loc.get("city", "unknown")
        
        location_index[country][region][city].append({
            "registryId": entry.get("registryId"),
            "domain": entry.get("domain"),
            "name": entry.get("name"),
            "file": entry.get("_file")
        })
    
    # Convert defaultdicts to regular dicts for JSON
    result = {}
    for country, regions in location_index.items():
        result[country] = {}
        for region, cities in regions.items():
            result[country][region] = {}
            for city, businesses in cities.items():
                result[country][region][city] = businesses
    
    return result


def build_by_service(entries):
    """Build service-category index."""
    service_index = defaultdict(list)
    
    for entry in entries:
        services = entry.get("services", [])
        for service in services:
            service_index[service].append({
                "registryId": entry.get("registryId"),
                "domain": entry.get("domain"),
                "name": entry.get("name"),
                "location": entry.get("location"),
                "file": entry.get("_file")
            })
    
    return dict(service_index)


def build_by_industry(entries):
    """Build industry-category index."""
    industry_index = defaultdict(list)
    
    for entry in entries:
        industry = entry.get("industry", "other")
        industry_index[industry].append({
            "registryId": entry.get("registryId"),
            "domain": entry.get("domain"),
            "name": entry.get("name"),
            "location": entry.get("location"),
            "file": entry.get("_file")
        })
    
    return dict(industry_index)


def build_jsonl(entries):
    """Build JSON Lines format."""
    for entry in entries:
        # Remove internal _file field
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
    
    print("\nBuilding indexes...")
    
    # Build by-domain
    print("  Building by-domain.json...")
    by_domain = build_by_domain(entries)
    with open(index_path / "by-domain.json", 'w') as f:
        json.dump(by_domain, f, indent=2)
    
    # Build by-location
    print("  Building by-location.json...")
    by_location = build_by_location(entries)
    with open(index_path / "by-location.json", 'w') as f:
        json.dump(by_location, f, indent=2)
    
    # Build by-service
    print("  Building by-service.json...")
    by_service = build_by_service(entries)
    with open(index_path / "by-service.json", 'w') as f:
        json.dump(by_service, f, indent=2)
    
    # Build by-industry
    print("  Building by-industry.json...")
    by_industry = build_by_industry(entries)
    with open(index_path / "by-industry.json", 'w') as f:
        json.dump(by_industry, f, indent=2)
    
    # Build JSONL
    print("  Building businesses.jsonl...")
    with open(index_path / "businesses.jsonl", 'w') as f:
        for line in build_jsonl(entries):
            f.write(line + "\n")
    
    print(f"\nIndexes built successfully!")
    print(f"  by-domain.json: {len(by_domain)} entries")
    print(f"  by-location.json: {len(by_location)} countries")
    print(f"  by-service.json: {len(by_service)} services")
    print(f"  by-industry.json: {len(by_industry)} industries")
    print(f"  businesses.jsonl: {len(entries)} entries")


if __name__ == "__main__":
    main()