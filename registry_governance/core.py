"""Policy-as-code checks and non-destructive recovery exercises."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any

from registry_supply_chain.core import MANIFEST_PATH, write_manifest
from registry_verify.verifier import verify_repository
from tools import build_indexes


RULESET_PATH = Path("governance/main-ruleset.json")
REQUIRED_STATUS_CHECKS = frozenset(
    {
        "verify-canonical-registry",
        "require-human-publication-approval",
        "governance-audit",
    }
)
REQUIRED_RULE_TYPES = frozenset(
    {
        "deletion",
        "non_fast_forward",
        "required_linear_history",
        "pull_request",
        "required_status_checks",
    }
)
PUBLIC_DIRECTORIES = ("schema", "registry", "provenance", "index", "manifest")
PUBLIC_ROOT_FILES = ("LICENSE", "LICENSE-DATA", "LICENSE-CODE", "NOTICE")
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _error(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def validate_ruleset_data(payload: Any) -> list[str]:
    """Return policy errors in an importable GitHub repository ruleset."""
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["Ruleset must be a JSON object."]

    _error(errors, payload.get("target") == "branch", "Target must be branch.")
    _error(
        errors,
        payload.get("enforcement") == "active",
        "Ruleset enforcement must be active.",
    )
    _error(
        errors,
        payload.get("bypass_actors") == [],
        "Standing ruleset bypass actors are prohibited.",
    )

    ref_name = (payload.get("conditions") or {}).get("ref_name") or {}
    _error(
        errors,
        ref_name.get("include") == ["~DEFAULT_BRANCH"],
        "Ruleset must target only ~DEFAULT_BRANCH.",
    )
    _error(
        errors,
        ref_name.get("exclude") == [],
        "Default-branch ruleset must not exclude refs.",
    )

    rules = payload.get("rules")
    if not isinstance(rules, list):
        return errors + ["Ruleset rules must be an array."]
    typed_rules: dict[str, dict[str, Any]] = {}
    for rule in rules:
        if not isinstance(rule, dict) or not isinstance(rule.get("type"), str):
            errors.append("Every ruleset rule must have a string type.")
            continue
        rule_type = rule["type"]
        if rule_type in typed_rules:
            errors.append(f"Duplicate ruleset rule type: {rule_type}.")
        typed_rules[rule_type] = rule

    missing = sorted(REQUIRED_RULE_TYPES - typed_rules.keys())
    if missing:
        errors.append("Missing required rules: " + ", ".join(missing) + ".")

    pull = (typed_rules.get("pull_request") or {}).get("parameters") or {}
    _error(
        errors,
        pull.get("required_approving_review_count", 0) >= 1,
        "Pull requests must require at least one approving review.",
    )
    required_flags = {
        "dismiss_stale_reviews_on_push": "Stale reviews must be dismissed.",
        "require_code_owner_review": "CODEOWNER review must be required.",
        "require_last_push_approval": "The latest push must be approved.",
        "required_review_thread_resolution": (
            "Review conversations must be resolved."
        ),
    }
    for key, message in required_flags.items():
        _error(errors, pull.get(key) is True, message)
    _error(
        errors,
        pull.get("allowed_merge_methods") == ["squash"],
        "Only squash merging may be allowed.",
    )

    status = (typed_rules.get("required_status_checks") or {}).get(
        "parameters"
    ) or {}
    _error(
        errors,
        status.get("strict_required_status_checks_policy") is True,
        "Required checks must use strict, up-to-date branch testing.",
    )
    _error(
        errors,
        status.get("do_not_enforce_on_create") is True,
        "Branch creation must remain possible before checks exist.",
    )
    check_items = status.get("required_status_checks") or []
    contexts = {
        item.get("context")
        for item in check_items
        if isinstance(item, dict) and isinstance(item.get("context"), str)
    }
    _error(
        errors,
        contexts == REQUIRED_STATUS_CHECKS,
        "Required status checks must be exactly: "
        + ", ".join(sorted(REQUIRED_STATUS_CHECKS))
        + ".",
    )
    return errors


def validate_ruleset(path: Path | str) -> dict[str, Any]:
    path = Path(path)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors = [f"Could not read ruleset: {exc}"]
    else:
        errors = validate_ruleset_data(payload)
    return {
        "schemaVersion": "1.0",
        "checkType": "github-main-ruleset",
        "path": path.as_posix(),
        "passed": not errors,
        "errors": errors,
    }


def _copy_public_repository(source: Path, target: Path) -> None:
    for directory in PUBLIC_DIRECTORIES:
        shutil.copytree(source / directory, target / directory)
    for filename in PUBLIC_ROOT_FILES:
        shutil.copy2(source / filename, target / filename)


def _hash_public_tree(root: Path) -> dict[str, str]:
    paths: list[Path] = []
    for directory in PUBLIC_DIRECTORIES:
        paths.extend(path for path in (root / directory).rglob("*") if path.is_file())
    paths.extend(root / filename for filename in PUBLIC_ROOT_FILES)
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(paths)
    }


def _contains_exact(value: Any, expected: str) -> bool:
    if value == expected:
        return True
    if isinstance(value, dict):
        return any(_contains_exact(item, expected) for item in value.values())
    if isinstance(value, list):
        return any(_contains_exact(item, expected) for item in value)
    return False


def _index_contains(root: Path, expected: str) -> bool:
    for path in sorted((root / "index").iterdir()):
        if path.suffix not in {".json", ".jsonl"}:
            continue
        if path.suffix == ".jsonl":
            values = [
                json.loads(line)
                for line in path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
        else:
            values = json.loads(path.read_text(encoding="utf-8"))
        if _contains_exact(values, expected):
            return True
    return False


def _rebuild(root: Path) -> None:
    entries = build_indexes.find_all_entries(root / "registry")
    outputs = build_indexes.build_outputs(entries)
    build_indexes.write_outputs(outputs, root / "index")
    write_manifest(root)


def _check(code: str, passed: bool, message: str) -> dict[str, Any]:
    return {"code": code, "passed": passed, "message": message}


def rollback_drill(root: Path | str, slug: str | None = None) -> dict[str, Any]:
    """Exercise unpublish and exact restoration in an isolated copy."""
    source = Path(root).resolve()
    checks: list[dict[str, Any]] = []
    if slug is None:
        slugs = sorted(
            path.parent.name
            for path in (source / "registry").glob("*/profile.json")
        )
        if not slugs:
            checks.append(
                _check(
                    "input.entity_exists",
                    False,
                    "Recovery drill requires at least one published entity.",
                )
            )
            return _drill_report("", checks)
        slug = slugs[0]
    if not SLUG_PATTERN.fullmatch(slug):
        checks.append(_check("input.slug", False, "Entity slug is not canonical."))
        return _drill_report(slug, checks)

    profile_source = source / "registry" / slug / "profile.json"
    receipt_source = source / "provenance" / slug / "publication-receipt.json"
    if not profile_source.is_file() or not receipt_source.is_file():
        checks.append(
            _check(
                "input.entity_exists",
                False,
                "Selected entity must have both a profile and publication receipt.",
            )
        )
        return _drill_report(slug, checks)

    source_hashes = _hash_public_tree(source)
    profile = json.loads(profile_source.read_text(encoding="utf-8"))
    domain = profile["businessIdentifier"]["primaryDomain"]

    with tempfile.TemporaryDirectory(prefix="vizai-governance-drill-") as temp:
        drill_root = Path(temp) / "repository"
        drill_root.mkdir()
        _copy_public_repository(source, drill_root)

        baseline = verify_repository(drill_root)
        checks.append(
            _check(
                "baseline.verify",
                baseline.passed,
                "Temporary baseline passes the authoritative verifier.",
            )
        )
        if not baseline.passed:
            return _drill_report(slug, checks)

        baseline_manifest = (drill_root / MANIFEST_PATH).read_bytes()
        profile_backup = (drill_root / "registry" / slug / "profile.json").read_bytes()
        receipt_backup = (
            drill_root / "provenance" / slug / "publication-receipt.json"
        ).read_bytes()

        shutil.rmtree(drill_root / "registry" / slug)
        shutil.rmtree(drill_root / "provenance" / slug)
        _rebuild(drill_root)

        contained = verify_repository(drill_root)
        checks.append(
            _check(
                "containment.verify",
                contained.passed,
                "Removal copy passes every authoritative verification gate.",
            )
        )
        absent = not _index_contains(drill_root, slug) and not _index_contains(
            drill_root, domain
        )
        checks.append(
            _check(
                "containment.index_absence",
                absent,
                "Removed entity slug and domain are absent from every index.",
            )
        )
        manifest = json.loads((drill_root / MANIFEST_PATH).read_text(encoding="utf-8"))
        removed_paths = {
            f"registry/{slug}/profile.json",
            f"provenance/{slug}/publication-receipt.json",
        }
        manifest_paths = {item["path"] for item in manifest["artifacts"]}
        checks.append(
            _check(
                "containment.manifest_absence",
                removed_paths.isdisjoint(manifest_paths),
                "Removed profile and receipt are absent from the manifest.",
            )
        )

        profile_target = drill_root / "registry" / slug / "profile.json"
        receipt_target = drill_root / "provenance" / slug / "publication-receipt.json"
        profile_target.parent.mkdir()
        receipt_target.parent.mkdir()
        profile_target.write_bytes(profile_backup)
        receipt_target.write_bytes(receipt_backup)
        _rebuild(drill_root)

        restored = verify_repository(drill_root)
        checks.append(
            _check(
                "rollback.verify",
                restored.passed,
                "Restored copy passes every authoritative verification gate.",
            )
        )
        checks.append(
            _check(
                "rollback.manifest_exact",
                (drill_root / MANIFEST_PATH).read_bytes() == baseline_manifest,
                "Rollback reproduces the exact baseline manifest bytes.",
            )
        )

    checks.append(
        _check(
            "source.immutable",
            _hash_public_tree(source) == source_hashes,
            "The source repository was not changed by the drill.",
        )
    )
    return _drill_report(slug, checks)


def _drill_report(slug: str, checks: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schemaVersion": "1.0",
        "drillType": "emergency-unpublish-and-rollback",
        "entitySlug": slug,
        "passed": bool(checks) and all(check["passed"] for check in checks),
        "checks": checks,
    }
