#!/usr/bin/env python3
"""Retired legacy intake-to-public-profile generator.

This command intentionally fails closed. The previous implementation copied raw
submission fields, including contact details, into a legacy public profile
shape. That bypassed the canonical entity-profile contract and the private
intake/publication approval boundary.
"""

import argparse


RETIREMENT_MESSAGE = """
This legacy generator is disabled by publication containment.

Do not transform raw intake records directly into public registry JSON.
Use the private Command Center intake and controlled publication workflow:
prepare registry/<entity-slug>/profile.json, validate it, rebuild indexes, and
obtain explicit human publication approval.
""".strip()


def generate_profile(_submission_data):
    """Fail closed for callers that imported the legacy helper."""
    raise RuntimeError(RETIREMENT_MESSAGE)


def main():
    parser = argparse.ArgumentParser(
        description="Retired: raw intake may not be converted directly to a public profile"
    )
    parser.add_argument("--input", help="Ignored legacy argument")
    parser.add_argument("--output", help="Ignored legacy argument")
    parser.parse_args()
    parser.error(RETIREMENT_MESSAGE)


if __name__ == "__main__":
    main()
