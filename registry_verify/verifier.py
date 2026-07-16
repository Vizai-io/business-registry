"""Authoritative repository verifier for the VizAI Business Registry."""

from __future__ import annotations

import json
import re
import tempfile
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse

from jsonschema import Draft7Validator, FormatChecker

from tools import build_indexes


VERIFIER_VERSION = "1.0.0"
REPORT_SCHEMA_VERSION = "1.0"

FORBIDDEN_MARKERS = (
    "do_not_publish",
    "do not publish",
    "held_from_this_publication",
    "held from this publication",
    "needs evidence",
    "no_evidence_provided",
    "evidence_requested",
    "evidence_received",
    "expired_or_stale",
    "evidence_register",
    "evidence ledger",
    "evidenceledger",
    "truth_canon",
    "truthcanon",
    "truth canon",
    "pending_facts",
    "pendingfacts",
    "verification_worksheet",
    "verification_log",
    "worksheet",
    "onboarding-response",
    "onboarding_response",
    "publication_plan",
    "implementation_note",
    "implementation note",
    "reconfirm",
    "internal note",
    "internalnote",
    "internal-note",
    "working file",
    "golden rule",
    "blueprint-driven",
)
FORBIDDEN_MARKER_PATTERNS = (
    re.compile(r"\bWP-\d", re.IGNORECASE),
    re.compile(r"\bDEC-\d{2,}", re.IGNORECASE),
)
FORBIDDEN_PRIVATE_KEYS = {
    "apikey",
    "authorization",
    "authorizationproof",
    "billing",
    "billingdetails",
    "customeremail",
    "dnstoken",
    "dnsvalue",
    "evidencedocument",
    "evidenceurl",
    "internalnotes",
    "ordernumber",
    "password",
    "passphrase",
    "privateevidence",
    "privatenotes",
    "purchaseorder",
    "secret",
    "submitter",
    "submitteremail",
    "submittername",
    "verificationtoken",
}
SECRET_PATTERNS = (
    ("privacy.private_key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("privacy.openai_key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("privacy.github_token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("privacy.github_pat", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b")),
    ("privacy.aws_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    (
        "privacy.jwt",
        re.compile(
            r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"
        ),
    ),
    (
        "privacy.dns_verification",
        re.compile(r"\b(?:vizai-)?verification\s*=\s*[^\s]+", re.IGNORECASE),
    ),
)
PRIVATE_TEXT_PATTERNS = (
    (
        "privacy.labeled_password",
        re.compile(r"\b(?:password|passphrase)\s*[:=]\s*\S+", re.IGNORECASE),
    ),
    (
        "privacy.labeled_token",
        re.compile(
            r"\b(?:api key|verification token|dns txt|dns value)\s*[:=]\s*\S+",
            re.IGNORECASE,
        ),
    ),
    (
        "privacy.labeled_commercial_data",
        re.compile(
            r"\b(?:order number|purchase reference|billing account)\s*[:=]\s*\S+",
            re.IGNORECASE,
        ),
    ),
)

STATUS_METHODS = {
    "claimed_verified": {
        "customer-canon-approval",
        "domain-ownership",
        "email-verification",
        "manual-review",
    },
    "unclaimed_observed": {"public-source-review", "manual-review"},
    "verification_pending": {
        "domain-ownership",
        "email-verification",
        "manual-review",
        "public-source-review",
    },
    "disputed": {
        "customer-canon-approval",
        "domain-ownership",
        "email-verification",
        "manual-review",
        "public-source-review",
    },
}
EXPECTED_INDEX_FILES = {
    "businesses.jsonl",
    "by-domain.json",
    "by-industry.json",
    "by-location.json",
    "by-service.json",
    "by-status.json",
}


@dataclass(frozen=True)
class CheckResult:
    gate: str
    code: str
    passed: bool
    message: str
    file: str | None = None
    json_path: str | None = None

    def to_dict(self):
        payload = {
            "gate": self.gate,
            "code": self.code,
            "passed": self.passed,
            "message": self.message,
        }
        if self.file:
            payload["file"] = self.file
        if self.json_path:
            payload["jsonPath"] = self.json_path
        return payload


@dataclass
class ProfileResult:
    file: str
    entity_slug: str | None = None
    checks: list[CheckResult] = field(default_factory=list)

    @property
    def passed(self):
        return bool(self.checks) and all(check.passed for check in self.checks)

    def to_dict(self):
        return {
            "file": self.file,
            "entitySlug": self.entity_slug,
            "passed": self.passed,
            "checks": [check.to_dict() for check in self.checks],
        }


@dataclass
class VerificationReport:
    repository: str
    generated_at: str
    profiles: list[ProfileResult]
    repository_checks: list[CheckResult]

    @property
    def checks(self):
        profile_checks = [
            check for profile in self.profiles for check in profile.checks
        ]
        return profile_checks + self.repository_checks

    @property
    def passed(self):
        return bool(self.checks) and all(check.passed for check in self.checks)

    def to_dict(self):
        failed = [check for check in self.checks if not check.passed]
        return {
            "schemaVersion": REPORT_SCHEMA_VERSION,
            "verifierVersion": VERIFIER_VERSION,
            "generatedAt": self.generated_at,
            "repository": self.repository,
            "passed": self.passed,
            "summary": {
                "profiles": len(self.profiles),
                "checks": len(self.checks),
                "passedChecks": len(self.checks) - len(failed),
                "failedChecks": len(failed),
                "indexArtifacts": len(EXPECTED_INDEX_FILES),
            },
            "profiles": [profile.to_dict() for profile in self.profiles],
            "repositoryChecks": [
                check.to_dict() for check in self.repository_checks
            ],
        }


def _check(
    gate: str,
    code: str,
    passed: bool,
    message: str,
    file: str | None = None,
    json_path: str | None = None,
):
    return CheckResult(
        gate=gate,
        code=code,
        passed=passed,
        message=message,
        file=file,
        json_path=json_path,
    )


def _gate_checks(
    gate: str,
    success_code: str,
    success_message: str,
    errors: Iterable[tuple[str, str, str | None]],
    file: str,
):
    errors = list(errors)
    if not errors:
        return [_check(gate, success_code, True, success_message, file=file)]
    return [
        _check(gate, code, False, message, file=file, json_path=json_path)
        for code, message, json_path in errors
    ]


def _json_path(parts: Iterable[Any]):
    rendered = "$"
    for part in parts:
        if isinstance(part, int):
            rendered += f"[{part}]"
        else:
            rendered += f".{part}"
    return rendered


def _walk(value: Any, path: tuple[Any, ...] = ()):
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from _walk(child, path + (key,))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk(child, path + (index,))


def _mapping(value: Any):
    return value if isinstance(value, dict) else {}


def _load_schema(root: Path):
    path = root / "schema" / "entity-profile-v1.0.schema.json"
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft7Validator.check_schema(schema)
    return path, schema


def _schema_errors(profile: dict[str, Any], validator: Draft7Validator):
    errors = []
    for error in sorted(
        validator.iter_errors(profile),
        key=lambda item: tuple(str(part) for part in item.absolute_path),
    ):
        errors.append(
            (
                "schema.invalid",
                error.message,
                _json_path(error.absolute_path),
            )
        )
    return errors


def _string_limit(path: tuple[Any, ...]):
    last_key = next(
        (part for part in reversed(path) if isinstance(part, str)),
        "",
    )
    if last_key in {"website", "linkedin", "facebook"}:
        return 2048
    if "claims" in path:
        return 1000
    if last_key in {"businessType", "ownership"}:
        return 500
    if last_key == "reference":
        return 128
    return 200


def _semantic_errors(
    profile: dict[str, Any],
    file: str,
    today: date,
):
    errors: list[tuple[str, str, str | None]] = []
    parts = Path(file).parts
    slug = profile.get("entitySlug")
    if len(parts) != 3 or parts[0] != "registry" or parts[2] != "profile.json":
        errors.append(
            (
                "semantic.path_layout",
                "Profile must live at registry/<entity-slug>/profile.json.",
                None,
            )
        )
    elif parts[1] != slug:
        errors.append(
            (
                "semantic.slug_parity",
                f"Directory slug '{parts[1]}' does not match entitySlug '{slug}'.",
                "$.entitySlug",
            )
        )

    for path, value in _walk(profile):
        json_path = _json_path(path)
        if isinstance(value, str):
            if not value.strip():
                errors.append(
                    (
                        "semantic.empty_string",
                        "Strings must not be empty or whitespace-only.",
                        json_path,
                    )
                )
            elif value != value.strip():
                errors.append(
                    (
                        "semantic.untrimmed_string",
                        "Strings must not contain leading or trailing whitespace.",
                        json_path,
                    )
                )
            elif len(value) > _string_limit(path):
                errors.append(
                    (
                        "semantic.string_too_long",
                        f"String exceeds the {_string_limit(path)} character limit.",
                        json_path,
                    )
                )
        elif isinstance(value, list):
            if not value:
                errors.append(
                    (
                        "semantic.empty_array",
                        "Arrays must be omitted rather than published empty.",
                        json_path,
                    )
                )
            if len(value) > 100:
                errors.append(
                    (
                        "semantic.array_too_large",
                        "Public arrays may contain at most 100 items.",
                        json_path,
                    )
                )
            normalized = []
            for item in value:
                if isinstance(item, str):
                    normalized.append(("string", item.strip().casefold()))
                elif isinstance(item, dict):
                    normalized.append(
                        ("object", json.dumps(item, sort_keys=True))
                    )
            if len(normalized) != len(set(normalized)):
                errors.append(
                    (
                        "semantic.duplicate_array_item",
                        "Arrays must not contain duplicate public values.",
                        json_path,
                    )
                )

    identifier = _mapping(profile.get("businessIdentifier"))
    domain = identifier.get("primaryDomain", "")
    if isinstance(domain, str):
        normalized_domain = domain.strip().lower().rstrip(".")
        if (
            domain != normalized_domain
            or domain.startswith("www.")
            or "://" in domain
            or "/" in domain
        ):
            errors.append(
                (
                    "semantic.domain_normalization",
                    "primaryDomain must be lowercase, scheme-free, path-free, "
                    "without a trailing dot or leading www.",
                    "$.businessIdentifier.primaryDomain",
                )
            )

    for path, value in _walk(profile):
        if not isinstance(value, str) or not path:
            continue
        key = path[-1]
        if key in {"website", "linkedin", "facebook"}:
            parsed = urlparse(value)
            if parsed.scheme != "https" or not parsed.netloc:
                errors.append(
                    (
                        "semantic.https_required",
                        "Public web and social URLs must use an absolute HTTPS URL.",
                        _json_path(path),
                    )
                )

    verification = _mapping(profile.get("verification"))
    status = verification.get("status")
    method = verification.get("method")
    if status in STATUS_METHODS and method not in STATUS_METHODS[status]:
        errors.append(
            (
                "semantic.status_method",
                f"Verification method '{method}' is incompatible with status '{status}'.",
                "$.verification.method",
            )
        )
    if status == "claimed_verified" and not verification.get("canonVersion"):
        errors.append(
            (
                "semantic.canon_required",
                "claimed_verified profiles require canonVersion.",
                "$.verification.canonVersion",
            )
        )
    if status == "unclaimed_observed":
        for field_name in ("canonVersion", "customerApprovalDate"):
            if field_name in verification:
                errors.append(
                    (
                        "semantic.unclaimed_claim_metadata",
                        f"unclaimed_observed profiles must not contain {field_name}.",
                        f"$.verification.{field_name}",
                    )
                )

    parsed_dates: dict[str, date] = {}
    metadata = _mapping(profile.get("metadata"))
    date_paths = {
        "dateAdded": metadata.get("dateAdded"),
        "lastUpdated": metadata.get("lastUpdated"),
        "lastVerified": verification.get("lastVerified"),
        "customerApprovalDate": verification.get("customerApprovalDate"),
    }
    for name, value in date_paths.items():
        if not value or not isinstance(value, str):
            continue
        try:
            parsed_dates[name] = date.fromisoformat(value)
        except ValueError:
            continue
        if parsed_dates[name] > today:
            errors.append(
                (
                    "semantic.future_date",
                    f"{name} must not be in the future.",
                    (
                        f"$.metadata.{name}"
                        if name in {"dateAdded", "lastUpdated"}
                        else f"$.verification.{name}"
                    ),
                )
            )
    if (
        parsed_dates.get("dateAdded")
        and parsed_dates.get("lastUpdated")
        and parsed_dates["dateAdded"] > parsed_dates["lastUpdated"]
    ):
        errors.append(
            (
                "semantic.date_chronology",
                "metadata.dateAdded must be on or before metadata.lastUpdated.",
                "$.metadata",
            )
        )
    if (
        parsed_dates.get("lastVerified")
        and parsed_dates.get("lastUpdated")
        and parsed_dates["lastVerified"] > parsed_dates["lastUpdated"]
    ):
        errors.append(
            (
                "semantic.date_chronology",
                "verification.lastVerified must be on or before metadata.lastUpdated.",
                "$.verification.lastVerified",
            )
        )
    if (
        parsed_dates.get("customerApprovalDate")
        and parsed_dates.get("lastUpdated")
        and parsed_dates["customerApprovalDate"] > parsed_dates["lastUpdated"]
    ):
        errors.append(
            (
                "semantic.date_chronology",
                "customerApprovalDate must be on or before metadata.lastUpdated.",
                "$.verification.customerApprovalDate",
            )
        )

    founded = _mapping(profile.get("profile")).get("yearFounded")
    if (
        isinstance(founded, int)
        and not isinstance(founded, bool)
        and not 1000 <= founded <= today.year
    ):
        errors.append(
            (
                "semantic.year_founded",
                f"yearFounded must be between 1000 and {today.year}.",
                "$.profile.yearFounded",
            )
        )
    return errors


def _clean_errors(raw_text: str):
    errors = []
    lower = raw_text.lower()
    hits = sorted({marker for marker in FORBIDDEN_MARKERS if marker in lower})
    regex_hits = sorted(
        {
            match.group(0)
            for pattern in FORBIDDEN_MARKER_PATTERNS
            for match in pattern.finditer(raw_text)
        }
    )
    if hits or regex_hits:
        errors.append(
            (
                "clean.internal_marker",
                "Forbidden internal workflow markers found: "
                + ", ".join(hits + regex_hits),
                None,
            )
        )
    return errors


def _credential_errors(profile: dict[str, Any], today: date):
    errors = []
    for index, credential in enumerate(profile.get("credentials", []) or []):
        if not isinstance(credential, dict):
            continue
        prefix = f"$.credentials[{index}]"
        if credential.get("evidenceStatus") != "evidence_verified":
            errors.append(
                (
                    "credential.evidence_status",
                    "Published credentials must be evidence_verified.",
                    f"{prefix}.evidenceStatus",
                )
            )
        if credential.get("publicPublishAllowed") is not True:
            errors.append(
                (
                    "credential.publication_permission",
                    "Published credentials require publicPublishAllowed=true.",
                    f"{prefix}.publicPublishAllowed",
                )
            )
        issue = credential.get("issueDate")
        expiry = credential.get("expiryOrRenewalDate")
        if issue:
            try:
                if date.fromisoformat(issue) > today:
                    errors.append(
                        (
                            "credential.future_issue_date",
                            "Credential issueDate must not be in the future.",
                            f"{prefix}.issueDate",
                        )
                    )
            except (TypeError, ValueError):
                pass
        if issue and expiry:
            try:
                if date.fromisoformat(issue) > date.fromisoformat(expiry):
                    errors.append(
                        (
                            "credential.date_chronology",
                            "Credential issueDate must not follow expiryOrRenewalDate.",
                            prefix,
                        )
                    )
            except (TypeError, ValueError):
                pass
    return errors


def _consent_errors(profile: dict[str, Any]):
    errors = []
    publication = _mapping(profile.get("publication"))
    receipt = _mapping(publication.get("consentReceipt"))
    receipt_status = receipt.get("status")
    reference = receipt.get("reference")
    status = _mapping(profile.get("verification")).get("status")

    if not publication:
        return [
            (
                "consent.missing",
                "Every public profile requires a publication consent assertion.",
                "$.publication",
            )
        ]
    if status == "unclaimed_observed":
        if receipt_status != "not-required-public-observation":
            errors.append(
                (
                    "consent.unclaimed_status",
                    "unclaimed_observed profiles must use "
                    "not-required-public-observation.",
                    "$.publication.consentReceipt.status",
                )
            )
        if reference != "public-observation":
            errors.append(
                (
                    "consent.unclaimed_reference",
                    "Unclaimed public-source profiles use the non-sensitive "
                    "reference 'public-observation'.",
                    "$.publication.consentReceipt.reference",
                )
            )
    elif receipt_status != "recorded":
        errors.append(
            (
                "consent.recorded_required",
                f"{status} profiles require a recorded consent receipt assertion.",
                "$.publication.consentReceipt.status",
            )
        )
    if isinstance(reference, str) and "@" in reference:
        errors.append(
            (
                "consent.personal_identifier",
                "Consent references must not expose an email address or person.",
                "$.publication.consentReceipt.reference",
            )
        )
    return errors


def _privacy_errors(profile: dict[str, Any], raw_text: str):
    errors = []
    for path, value in _walk(profile):
        if path and isinstance(path[-1], str):
            normalized_key = re.sub(r"[^a-z0-9]", "", path[-1].lower())
            if normalized_key in FORBIDDEN_PRIVATE_KEYS:
                errors.append(
                    (
                        "privacy.forbidden_key",
                        f"Private or intake field '{path[-1]}' is prohibited.",
                        _json_path(path),
                    )
                )
    for code, pattern in SECRET_PATTERNS:
        if pattern.search(raw_text):
            errors.append(
                (
                    code,
                    "Secret, token, private key, or verification value detected.",
                    None,
                )
            )
    for code, pattern in PRIVATE_TEXT_PATTERNS:
        if pattern.search(raw_text):
            errors.append(
                (
                    code,
                    "Labeled private, verification, or commercial data detected.",
                    None,
                )
            )

    publication = _mapping(profile.get("publication"))
    receipt_status = _mapping(publication.get("consentReceipt")).get("status")
    if _mapping(profile.get("profile")).get("contact") and receipt_status != "recorded":
        errors.append(
            (
                "privacy.contact_requires_consent",
                "Public contact fields require a recorded consent assertion.",
                "$.profile.contact",
            )
        )
    return errors


def verify_profile(
    profile: dict[str, Any],
    raw_text: str,
    file: str,
    validator: Draft7Validator,
    today: date | None = None,
):
    """Verify one parsed profile and return all gate results."""
    today = today or date.today()
    result = ProfileResult(file=file, entity_slug=profile.get("entitySlug"))
    result.checks.append(
        _check("json", "json.valid", True, "Valid JSON object.", file=file)
    )
    result.checks.extend(
        _gate_checks(
            "schema",
            "schema.valid",
            "Conforms to entity-profile v1 with format checking.",
            _schema_errors(profile, validator),
            file,
        )
    )
    result.checks.extend(
        _gate_checks(
            "semantic",
            "semantic.valid",
            "Semantic identity, normalization, bounds, and chronology rules pass.",
            _semantic_errors(profile, file, today),
            file,
        )
    )
    result.checks.extend(
        _gate_checks(
            "clean",
            "clean.valid",
            "No internal workflow markers detected.",
            _clean_errors(raw_text),
            file,
        )
    )
    result.checks.extend(
        _gate_checks(
            "credential",
            "credential.valid",
            "Credential evidence and publication gates pass.",
            _credential_errors(profile, today),
            file,
        )
    )
    result.checks.extend(
        _gate_checks(
            "consent",
            "consent.valid",
            "Public-safe consent assertion is compatible with verification state.",
            _consent_errors(profile),
            file,
        )
    )
    result.checks.extend(
        _gate_checks(
            "privacy",
            "privacy.valid",
            "No private fields, tokens, or secret patterns detected.",
            _privacy_errors(profile, raw_text),
            file,
        )
    )
    return result


def _identity_checks(parsed_profiles: list[tuple[str, dict[str, Any]]]):
    domains = defaultdict(list)
    slugs = defaultdict(list)
    for file, profile in parsed_profiles:
        domain = _mapping(profile.get("businessIdentifier")).get("primaryDomain")
        slug = profile.get("entitySlug")
        if isinstance(domain, str):
            domains[domain.casefold()].append(file)
        if isinstance(slug, str):
            slugs[slug].append(file)

    checks = []
    duplicates_found = False
    for label, values in (("domain", domains), ("entity_slug", slugs)):
        duplicates = {
            value: files for value, files in values.items() if len(files) > 1
        }
        if duplicates:
            duplicates_found = True
            for value, files in sorted(duplicates.items()):
                checks.append(
                    _check(
                        "identity",
                        f"identity.duplicate_{label}",
                        False,
                        f"Duplicate {label.replace('_', ' ')} '{value}': "
                        + ", ".join(files),
                    )
                )
    if not duplicates_found:
        checks.append(
            _check(
                "identity",
                "identity.unique",
                True,
                f"{len(slugs)} entity slugs and {len(domains)} domains are unique.",
            )
        )
    return checks


def _index_checks(root: Path):
    checks = []
    index_path = root / "index"
    try:
        entries = build_indexes.find_all_entries(root / "registry")
        outputs = build_indexes.build_outputs(entries)
        with tempfile.TemporaryDirectory(prefix="registry-verify-") as temp:
            expected_path = Path(temp)
            build_indexes.write_outputs(outputs, expected_path)
            actual_files = {
                path.name
                for path in index_path.iterdir()
                if path.suffix in {".json", ".jsonl"}
            }
            missing = EXPECTED_INDEX_FILES - actual_files
            unexpected = actual_files - EXPECTED_INDEX_FILES
            for filename in sorted(missing):
                checks.append(
                    _check(
                        "index",
                        "index.missing",
                        False,
                        f"Generated index is missing: index/{filename}.",
                    )
                )
            for filename in sorted(unexpected):
                checks.append(
                    _check(
                        "index",
                        "index.unexpected",
                        False,
                        f"Unexpected generated index exists: index/{filename}.",
                    )
                )
            for filename in sorted(EXPECTED_INDEX_FILES & actual_files):
                expected = (expected_path / filename).read_bytes()
                actual = (index_path / filename).read_bytes()
                if expected != actual:
                    checks.append(
                        _check(
                            "index",
                            "index.drift",
                            False,
                            f"index/{filename} differs from the canonical in-memory build.",
                            file=f"index/{filename}",
                        )
                    )
    except Exception as error:
        checks.append(
            _check(
                "index",
                "index.build_failed",
                False,
                f"Could not generate canonical indexes: {error}",
            )
        )
    if not checks:
        checks.append(
            _check(
                "index",
                "index.current",
                True,
                f"All {len(EXPECTED_INDEX_FILES)} generated indexes are current.",
            )
        )
    return checks


def verify_repository(root: Path | str = "."):
    """Run every authoritative verification gate for a repository."""
    root = Path(root).resolve()
    generated_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    repository_checks: list[CheckResult] = []
    profile_results: list[ProfileResult] = []

    required_directories = ("registry", "schema", "index")
    missing_directories = [
        name for name in required_directories if not (root / name).is_dir()
    ]
    if missing_directories:
        repository_checks.append(
            _check(
                "layout",
                "layout.missing_directory",
                False,
                "Missing required directories: " + ", ".join(missing_directories),
            )
        )
        return VerificationReport(
            repository=str(root),
            generated_at=generated_at,
            profiles=profile_results,
            repository_checks=repository_checks,
        )

    try:
        _, schema = _load_schema(root)
        validator = Draft7Validator(schema, format_checker=FormatChecker())
        repository_checks.append(
            _check(
                "schema",
                "schema.contract_valid",
                True,
                "Authoritative Draft 7 schema is valid.",
                file="schema/entity-profile-v1.0.schema.json",
            )
        )
    except Exception as error:
        repository_checks.append(
            _check(
                "schema",
                "schema.contract_invalid",
                False,
                f"Could not load the authoritative schema: {error}",
                file="schema/entity-profile-v1.0.schema.json",
            )
        )
        return VerificationReport(
            repository=str(root),
            generated_at=generated_at,
            profiles=profile_results,
            repository_checks=repository_checks,
        )

    json_paths = sorted((root / "registry").rglob("*.json"))
    canonical_paths = []
    unexpected_paths = []
    for path in json_paths:
        relative = path.relative_to(root)
        parts = relative.parts
        if len(parts) == 3 and parts[0] == "registry" and parts[2] == "profile.json":
            canonical_paths.append(path)
        else:
            unexpected_paths.append(relative.as_posix())

    if unexpected_paths:
        for file in unexpected_paths:
            repository_checks.append(
                _check(
                    "layout",
                    "layout.noncanonical_json",
                    False,
                    "Only registry/<entity-slug>/profile.json is supported.",
                    file=file,
                )
            )
    else:
        repository_checks.append(
            _check(
                "layout",
                "layout.canonical",
                True,
                f"All {len(canonical_paths)} registry JSON files use the canonical layout.",
            )
        )

    if not canonical_paths:
        repository_checks.append(
            _check(
                "layout",
                "layout.no_profiles",
                False,
                "The registry contains no canonical profiles.",
            )
        )

    parsed_profiles = []
    for path in canonical_paths:
        file = path.relative_to(root).as_posix()
        raw_text = path.read_text(encoding="utf-8")
        try:
            profile = json.loads(raw_text)
        except json.JSONDecodeError as error:
            profile_results.append(
                ProfileResult(
                    file=file,
                    checks=[
                        _check(
                            "json",
                            "json.invalid",
                            False,
                            f"Invalid JSON: {error}",
                            file=file,
                        )
                    ],
                )
            )
            continue
        if not isinstance(profile, dict):
            profile_results.append(
                ProfileResult(
                    file=file,
                    checks=[
                        _check(
                            "json",
                            "json.not_object",
                            False,
                            "A canonical profile must be a JSON object.",
                            file=file,
                        )
                    ],
                )
            )
            continue
        parsed_profiles.append((file, profile))
        profile_results.append(
            verify_profile(profile, raw_text, file, validator)
        )

    repository_checks.extend(_identity_checks(parsed_profiles))
    repository_checks.extend(_index_checks(root))

    return VerificationReport(
        repository=str(root),
        generated_at=generated_at,
        profiles=profile_results,
        repository_checks=repository_checks,
    )


def render_text(report: VerificationReport):
    """Render a concise human-readable verification summary."""
    status = "PASS" if report.passed else "FAIL"
    payload = report.to_dict()
    summary = payload["summary"]
    lines = [
        f"Registry verification {status}",
        (
            f"Profiles: {summary['profiles']} | Checks: {summary['checks']} | "
            f"Failed: {summary['failedChecks']}"
        ),
    ]
    for profile in report.profiles:
        profile_status = "PASS" if profile.passed else "FAIL"
        lines.append(f"[{profile_status}] {profile.file}")
    failed = [check for check in report.checks if not check.passed]
    if failed:
        lines.append("")
        lines.append("Failures:")
        for check in failed:
            location = check.file or "repository"
            if check.json_path:
                location += f" {check.json_path}"
            lines.append(
                f"- [{check.gate}] {check.code} ({location}): {check.message}"
            )
    else:
        lines.append("All authoritative gates passed.")
    return "\n".join(lines)
