"""Command-line entry point for ``python -m registry_verify``."""

import argparse
import json
import sys
from pathlib import Path

from .verifier import render_text, verify_repository


def build_parser():
    parser = argparse.ArgumentParser(
        description="Run every authoritative VizAI registry verification gate."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root to verify (default: current directory).",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Console output format (default: text).",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="Also write the complete machine-readable JSON report to this path.",
    )
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    report = verify_repository(args.root)
    payload = report.to_dict()

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    if args.format == "json":
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(render_text(report))

    return 0 if report.passed else 1


if __name__ == "__main__":
    sys.exit(main())
