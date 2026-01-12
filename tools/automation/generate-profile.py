#!/usr/bin/env python3
"""
Generate a business profile JSON from parsed submission data.

Usage:
    python generate-profile.py --input submission.json --output profile.json
"""

import json
import argparse
from datetime import date
from pathlib import Path


def generate_profile(submission_data):
    """Generate a complete business profile from submission data."""

    profile = {
        "schemaVersion": "1.0",
        "businessIdentifier": {
            "legalName": submission_data.get("legalName"),
            "commonName": submission_data.get("commonName", submission_data.get("legalName")),
            "primaryDomain": submission_data.get("primaryDomain"),
        },
        "description": {
            "elevator": submission_data.get("elevator"),
            "detailed": submission_data.get("detailed"),
        },
        "verification": {
            "status": "community",
            "tier": "community",
            "method": "self-reported",
            "lastVerified": str(date.today()),
        },
        "metadata": {
            "dateAdded": str(date.today()),
            "lastUpdated": str(date.today()),
            "submittedBy": submission_data.get("submittedBy", "Community"),
        }
    }

    # Add optional fields if present
    if submission_data.get("aliases"):
        profile["businessIdentifier"]["aliases"] = submission_data["aliases"]

    if submission_data.get("identifiers"):
        profile["businessIdentifier"]["identifiers"] = submission_data["identifiers"]

    if submission_data.get("yearFounded"):
        profile["description"]["yearFounded"] = int(submission_data["yearFounded"])

    if submission_data.get("founding"):
        profile["description"]["founding"] = submission_data["founding"]

    # Add location if provided
    if submission_data.get("headquarters"):
        profile["location"] = {
            "headquarters": submission_data["headquarters"]
        }

    # Add contact if provided
    if submission_data.get("email") or submission_data.get("phone"):
        profile["contact"] = {}
        if submission_data.get("email"):
            profile["contact"]["email"] = submission_data["email"]
        if submission_data.get("phone"):
            profile["contact"]["phone"] = submission_data["phone"]

    # Add offerings if provided
    if submission_data.get("offerings"):
        profile["offerings"] = submission_data["offerings"]

    # Add sources if provided
    if submission_data.get("sources"):
        profile["sources"] = submission_data["sources"]
    else:
        # Default to website source
        profile["sources"] = [{
            "type": "official-website",
            "url": f"https://{submission_data.get('primaryDomain')}",
            "accessed": str(date.today()),
            "description": "Company website"
        }]

    return profile


def main():
    parser = argparse.ArgumentParser(description="Generate business profile JSON")
    parser.add_argument("--input", required=True, help="Input submission JSON file")
    parser.add_argument("--output", required=True, help="Output profile JSON file")

    args = parser.parse_args()

    # Load submission data
    with open(args.input, 'r') as f:
        submission = json.load(f)

    # Generate profile
    profile = generate_profile(submission)

    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(profile, f, indent=2)

    print(f"Profile generated: {output_path}")


if __name__ == "__main__":
    main()
