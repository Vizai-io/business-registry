#!/usr/bin/env python3
"""
Validate registry entries against the VizAI Registry Entry schema.

Checks:
- Valid JSON
- Required fields present
- Format validation (domain, dates)
- Schema compliance
"""

import json
import sys
from pathlib import Path
from jsonschema import validate, ValidationError


def load_schema():
    """Load the registry entry schema."""
    schema_path = Path(__file__).parent.parent / "schema" / "registry-entry.schema.json"
    with open(schema_path, 'r') as f:
        return json.load(f)


def validate_entry(entry_path, schema):
    """Validate a single registry entry."""
    errors = []
    
    # Check required fields
    required = ["registryId", "domain", "name", "location", "profileUrl", "verification", "metadata"]
    with open(entry_path, 'r') as f:
        entry = json.load(f)
    
    for field in required:
        if field not in entry:
            errors.append(f"Missing required field: {field}")
    
    if errors:
        return False, errors
    
    # Validate location structure
    location = entry.get("location", {})
    for field in ["country", "region", "city"]:
        if field not in location:
            errors.append(f"Missing location.{field}")
    
    # Validate verification structure
    verification = entry.get("verification", {})
    for field in ["status", "lastVerified"]:
        if field not in verification:
            errors.append(f"Missing verification.{field}")
    
    # Schema validation
    try:
        validate(instance=entry, schema=schema)
    except ValidationError as e:
        errors.append(f"Schema error: {e.message}")
    
    return len(errors) == 0, errors


def validate_all(registry_path, schema):
    """Validate all registry entries."""
    all_valid = True
    validated = 0
    
    for json_path in registry_path.rglob("*.json"):
        if json_path.name == "index.json":
            continue
        
        validated += 1
        valid, errors = validate_entry(json_path, schema)
        
        if valid:
            print(f"[VALID] {json_path}")
        else:
            print(f"[INVALID] {json_path}")
            for error in errors:
                print(f"  - {error}")
            all_valid = False
    
    return all_valid, validated


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Usage: python validate_registry.py [entry.json]")
        print("")
        print("Options:")
        print("  [entry.json]   Validate a single entry (optional)")
        print("                 If omitted, validates all entries")
        sys.exit(0)
    
    schema = load_schema()
    script_dir = Path(__file__).parent
    registry_path = script_dir.parent / "registry"
    
    if len(sys.argv) > 1:
        # Validate single entry
        entry_path = Path(sys.argv[1])
        print(f"Validating {entry_path}...")
        valid, errors = validate_entry(entry_path, schema)
        
        if valid:
            print("[VALID] Entry is valid!")
            sys.exit(0)
        else:
            print("[INVALID] Entry has errors:")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)
    else:
        # Validate all entries
        print("Validating all registry entries...")
        valid, count = validate_all(registry_path, schema)
        
        if valid:
            print(f"\nAll {count} entries are valid!")
            sys.exit(0)
        else:
            print("\nSome entries have validation errors.")
            sys.exit(1)


if __name__ == "__main__":
    main()