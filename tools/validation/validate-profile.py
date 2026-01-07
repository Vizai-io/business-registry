#!/usr/bin/env python3
"""
VizAI Business Profile Validator

Validates business profile JSON files against the VizAI schema.
"""

import json
import sys
from pathlib import Path
from jsonschema import validate, ValidationError, Draft7Validator

def load_schema():
    """Load the VizAI Business Profile schema."""
    schema_path = Path(__file__).parent.parent.parent / "schema" / "business-profile-v1.0.json"
    with open(schema_path, 'r') as f:
        return json.load(f)

def validate_profile(profile_path):
    """Validate a business profile against the schema."""
    schema = load_schema()

    # Load the profile
    with open(profile_path, 'r') as f:
        profile = json.load(f)

    # Validate against schema
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
        print("Usage: python validate-profile.py <profile.json>")
        sys.exit(1)

    profile_path = sys.argv[1]

    if not Path(profile_path).exists():
        print(f"Error: File {profile_path} does not exist")
        sys.exit(1)

    valid = validate_profile(profile_path)
    sys.exit(0 if valid else 1)

if __name__ == "__main__":
    main()
