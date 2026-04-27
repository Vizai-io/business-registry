#!/usr/bin/env python3
"""
VizAI Discovery Profile Validator

Validates discovery profile JSON files against the VizAI schema.
Discovery profiles are the lightweight public reference layer.
"""

import json
import sys
from pathlib import Path
from jsonschema import validate, ValidationError

def load_schema(schema_type="discovery"):
    """Load the VizAI schema.
    
    Args:
        schema_type: "discovery" for lightweight profiles, "business" for full profiles
    """
    if schema_type == "discovery":
        schema_path = Path(__file__).parent.parent.parent / "schema" / "discovery-profile-v1.0.json"
    else:
        schema_path = Path(__file__).parent.parent.parent / "schema" / "business-profile-v1.0.json"
    
    with open(schema_path, 'r') as f:
        return json.load(f)

def validate_profile(profile_path, schema_type="discovery"):
    """Validate a discovery profile against the schema."""
    schema = load_schema(schema_type)

    with open(profile_path, 'r') as f:
        profile = json.load(f)

    try:
        validate(instance=profile, schema=schema)
        print(f"[VALID] {profile_path} is valid!")
        return True
    except ValidationError as e:
        print(f"[INVALID] {profile_path} is invalid:")
        print(f"  Error: {e.message}")
        print(f"  Path: {' -> '.join(str(p) for p in e.path)}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate-profile.py <profile.json> [--business-schema]")
        print("")
        print("Options:")
        print("  --business-schema   Use full business profile schema instead of discovery")
        sys.exit(1)

    profile_path = sys.argv[1]
    schema_type = "discovery"
    
    if len(sys.argv) > 2 and sys.argv[2] == "--business-schema":
        schema_type = "business"

    if not Path(profile_path).exists():
        print(f"Error: File {profile_path} does not exist")
        sys.exit(1)

    valid = validate_profile(profile_path, schema_type)
    sys.exit(0 if valid else 1)

if __name__ == "__main__":
    main()
