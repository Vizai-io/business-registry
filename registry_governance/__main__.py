"""CLI for registry governance validation and recovery exercises."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core import RULESET_PATH, rollback_drill, validate_ruleset


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate VizAI registry governance and exercise recovery."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root (default: current directory).",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate", help="Validate the main ruleset.")
    validate.add_argument(
        "--ruleset",
        type=Path,
        help="Ruleset path (default: governance/main-ruleset.json under root).",
    )
    drill = commands.add_parser(
        "rollback-drill",
        help="Exercise emergency unpublish and exact restoration in a temp copy.",
    )
    drill.add_argument(
        "--slug",
        help="Published entity slug (default: first canonical profile).",
    )
    drill.add_argument("--report", type=Path, help="Write the JSON drill report.")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    if args.command == "validate":
        path = args.ruleset or root / RULESET_PATH
        result = validate_ruleset(path)
    else:
        result = rollback_drill(root, args.slug)
        if args.report:
            args.report.write_text(
                json.dumps(result, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
