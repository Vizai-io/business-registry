"""CLI for deterministic registry manifests and release snapshots."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core import (
    MANIFEST_PATH,
    build_snapshot,
    manifest_errors,
    write_manifest,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build and verify VizAI registry supply-chain artifacts."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root (default: current directory).",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser(
        "write-manifest",
        help="Regenerate the committed deterministic registry manifest.",
    )
    commands.add_parser(
        "check-manifest",
        help="Fail when the committed manifest differs from public artifacts.",
    )
    snapshot = commands.add_parser(
        "snapshot",
        help="Build a reproducible snapshot and SHA256SUMS.",
    )
    snapshot.add_argument(
        "--output",
        type=Path,
        default=Path("dist"),
        help="Output directory (default: dist).",
    )
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    if args.command == "write-manifest":
        path = write_manifest(root)
        print(f"Wrote {path.relative_to(root).as_posix()}")
        return 0
    if args.command == "check-manifest":
        errors = manifest_errors(root)
        if errors:
            for error in errors:
                print(error, file=sys.stderr)
            return 1
        print(f"{MANIFEST_PATH.as_posix()} is current")
        return 0
    if args.command == "snapshot":
        output = args.output
        if not output.is_absolute():
            output = root / output
        result = build_snapshot(root, output)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
