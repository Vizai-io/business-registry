import copy
import json
import shutil
import tarfile
import tempfile
import unittest
from datetime import date, datetime, timezone
from pathlib import Path

from jsonschema import Draft7Validator, FormatChecker

from registry_supply_chain.core import (
    build_snapshot,
    canonical_json_sha256,
    raw_sha256,
    write_manifest,
)
from registry_verify.verifier import (
    verify_profile,
    verify_receipt,
    verify_repository,
)
from tools import build_indexes


REPOSITORY = Path(__file__).resolve().parent.parent
FIXTURES = REPOSITORY / "tests" / "fixtures" / "profiles"
RECEIPT_FIXTURES = REPOSITORY / "tests" / "fixtures" / "receipts"
SCHEMA = json.loads(
    (REPOSITORY / "schema" / "entity-profile-v1.0.schema.json").read_text(
        encoding="utf-8"
    )
)
VALIDATOR = Draft7Validator(SCHEMA, format_checker=FormatChecker())
RECEIPT_SCHEMA = json.loads(
    (REPOSITORY / "schema" / "publication-receipt-v1.0.schema.json").read_text(
        encoding="utf-8"
    )
)
RECEIPT_VALIDATOR = Draft7Validator(
    RECEIPT_SCHEMA,
    format_checker=FormatChecker(),
)
TODAY = date(2026, 7, 16)
NOW = datetime(2026, 7, 16, 23, 59, tzinfo=timezone.utc)


def load_fixture(name):
    path = FIXTURES / name
    return json.loads(path.read_text(encoding="utf-8"))


def verify_fixture(name, file="registry/fixture-co/profile.json"):
    profile = load_fixture(name)
    raw = json.dumps(profile)
    return verify_profile(profile, raw, file, VALIDATOR, today=TODAY)


def failed_codes(result):
    return {check.code for check in result.checks if not check.passed}


def load_receipt_fixture(name):
    path = RECEIPT_FIXTURES / name
    return json.loads(path.read_text(encoding="utf-8"))


def verify_receipt_fixture(
    name,
    profile_name="valid-claimed.json",
    slug="fixture-co",
):
    receipt = load_receipt_fixture(name)
    profile_path = FIXTURES / profile_name
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    return verify_receipt(
        receipt,
        json.dumps(receipt),
        f"provenance/{slug}/publication-receipt.json",
        RECEIPT_VALIDATOR,
        profile,
        profile_path,
        now=NOW,
    )


class ProfileGateTests(unittest.TestCase):
    def test_valid_claimed_profile_passes_every_gate(self):
        result = verify_fixture("valid-claimed.json")
        self.assertTrue(result.passed)
        self.assertEqual(
            {check.gate for check in result.checks},
            {
                "json",
                "schema",
                "semantic",
                "clean",
                "credential",
                "consent",
                "privacy",
            },
        )

    def test_valid_unclaimed_profile_uses_public_observation_assertion(self):
        result = verify_fixture(
            "valid-unclaimed.json",
            file="registry/observed-co/profile.json",
        )
        self.assertTrue(result.passed)

    def test_format_and_domain_normalization_fail(self):
        codes = failed_codes(verify_fixture("invalid-format.json"))
        self.assertIn("schema.invalid", codes)
        self.assertIn("semantic.domain_normalization", codes)
        self.assertIn("semantic.https_required", codes)

    def test_claimed_profile_requires_recorded_consent(self):
        codes = failed_codes(verify_fixture("invalid-consent.json"))
        self.assertIn("consent.recorded_required", codes)

    def test_secret_pattern_fails_privacy_gate(self):
        codes = failed_codes(verify_fixture("invalid-privacy.json"))
        self.assertIn("privacy.github_pat", codes)
        self.assertIn("privacy.labeled_commercial_data", codes)

    def test_internal_markers_fail_clean_gate(self):
        codes = failed_codes(verify_fixture("invalid-clean.json"))
        self.assertIn("clean.internal_marker", codes)

    def test_invalid_credential_fails_schema_and_credential_gate(self):
        codes = failed_codes(verify_fixture("invalid-credential.json"))
        self.assertIn("schema.invalid", codes)
        self.assertIn("credential.evidence_status", codes)
        self.assertIn("credential.publication_permission", codes)
        self.assertIn("credential.date_chronology", codes)

    def test_chronology_year_and_folder_slug_are_enforced(self):
        result = verify_fixture(
            "invalid-chronology.json",
            file="registry/wrong-slug/profile.json",
        )
        codes = failed_codes(result)
        self.assertIn("semantic.slug_parity", codes)
        self.assertIn("semantic.date_chronology", codes)
        self.assertIn("semantic.year_founded", codes)

    def test_semantic_bounds_duplicates_and_status_method_are_enforced(self):
        codes = failed_codes(verify_fixture("invalid-semantic.json"))
        self.assertIn("semantic.empty_string", codes)
        self.assertIn("semantic.string_too_long", codes)
        self.assertIn("semantic.duplicate_array_item", codes)
        self.assertIn("semantic.empty_array", codes)
        self.assertIn("semantic.status_method", codes)

    def test_schema_invalid_types_are_reported_without_crashing_other_gates(self):
        result = verify_fixture("invalid-types.json")
        self.assertFalse(result.passed)
        self.assertIn("schema.invalid", failed_codes(result))
        self.assertEqual(
            {check.gate for check in result.checks},
            {
                "json",
                "schema",
                "semantic",
                "clean",
                "credential",
                "consent",
                "privacy",
            },
        )


class ReceiptGateTests(unittest.TestCase):
    def test_valid_canon_receipt_passes_every_gate(self):
        result = verify_receipt_fixture("valid-canon.json")
        self.assertTrue(result.passed)
        self.assertEqual(
            {check.gate for check in result.checks},
            {
                "receipt-json",
                "receipt-schema",
                "provenance",
                "integrity",
                "receipt-privacy",
            },
        )

    def test_valid_public_source_receipt_passes(self):
        result = verify_receipt_fixture(
            "valid-public-source.json",
            profile_name="valid-unclaimed.json",
            slug="observed-co",
        )
        self.assertTrue(result.passed)

    def test_invalid_source_approval_and_chronology_fail(self):
        codes = failed_codes(verify_receipt_fixture("invalid-provenance.json"))
        self.assertIn("provenance.canon_repository", codes)
        self.assertIn("provenance.canon_version", codes)
        self.assertIn("provenance.approval_required", codes)
        self.assertIn("provenance.canon_lineage", codes)
        self.assertIn("provenance.future_timestamp", codes)
        self.assertIn("provenance.approval_chronology", codes)

    def test_profile_hash_and_policy_tampering_fail(self):
        codes = failed_codes(verify_receipt_fixture("invalid-integrity.json"))
        self.assertIn("integrity.profileversion_parity", codes)
        self.assertIn("integrity.byte_count", codes)
        self.assertIn("integrity.raw_hash", codes)
        self.assertIn("integrity.canonical_hash", codes)
        self.assertIn("integrity.publication_parity", codes)
        self.assertIn("integrity.canon_version_parity", codes)

    def test_secret_pattern_fails_receipt_privacy(self):
        codes = failed_codes(verify_receipt_fixture("invalid-privacy.json"))
        self.assertIn("privacy.github_pat", codes)


class RepositoryGateTests(unittest.TestCase):
    def make_receipt(self, profile, profile_path):
        slug = profile["entitySlug"]
        version = profile["profileVersion"]
        source = {
            "type": "historical-registry-migration",
            "system": "business-registry",
            "repository": "Vizai-io/business-registry",
            "commitSha": "a" * 40,
            "lineage": [
                {
                    "kind": "registry-history",
                    "sourceClass": "approved-publication",
                    "reference": f"registry:{slug}:profile:{version}",
                    "observedAt": "2026-01-15T12:00:00Z",
                    "contentDigest": canonical_json_sha256(profile),
                }
            ],
        }
        canon_version = profile.get("verification", {}).get("canonVersion")
        if canon_version:
            source["canonVersion"] = canon_version
        return {
            "schemaVersion": "1.0",
            "receiptId": f"publication:{slug}:{version}",
            "entitySlug": slug,
            "profileVersion": version,
            "artifact": {
                "path": f"registry/{slug}/profile.json",
                "mediaType": "application/json",
                "bytes": profile_path.stat().st_size,
                "sha256": raw_sha256(profile_path),
                "canonicalJsonSha256": canonical_json_sha256(profile),
            },
            "source": source,
            "publication": profile["publication"],
            "approval": {
                "status": "historical-migration",
                "preparedAt": "2026-01-15T12:00:00Z",
                "approvedAt": "2026-01-15T12:00:00Z",
                "workflow": "git-maintainer-publication-history",
            },
        }

    def make_repository(self, profiles):
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        (root / "schema").mkdir()
        (root / "registry").mkdir()
        (root / "index").mkdir()
        (root / "provenance").mkdir()
        (root / "manifest").mkdir()
        for filename in ("LICENSE", "LICENSE-CODE", "LICENSE-DATA", "NOTICE"):
            shutil.copy2(REPOSITORY / filename, root / filename)
        for schema_name in (
            "entity-profile-v1.0.schema.json",
            "publication-receipt-v1.0.schema.json",
            "registry-manifest-v1.0.schema.json",
        ):
            shutil.copy2(
                REPOSITORY / "schema" / schema_name,
                root / "schema" / schema_name,
            )
        for profile in profiles:
            slug = profile["entitySlug"]
            folder = root / "registry" / slug
            folder.mkdir()
            profile_path = folder / "profile.json"
            profile_path.write_text(
                json.dumps(profile, indent=2) + "\n",
                encoding="utf-8",
                newline="\n",
            )
            receipt_folder = root / "provenance" / slug
            receipt_folder.mkdir()
            receipt = self.make_receipt(profile, profile_path)
            (receipt_folder / "publication-receipt.json").write_text(
                json.dumps(receipt, indent=2) + "\n",
                encoding="utf-8",
                newline="\n",
            )
        entries = build_indexes.find_all_entries(root / "registry")
        build_indexes.write_outputs(
            build_indexes.build_outputs(entries),
            root / "index",
        )
        write_manifest(root)
        return temporary, root

    def test_repository_detects_duplicate_domain(self):
        first = load_fixture("valid-claimed.json")
        second = copy.deepcopy(first)
        second["entitySlug"] = "fixture-two"
        second["businessIdentifier"]["legalName"] = "Fixture Two Inc."
        second["businessIdentifier"]["commonName"] = "Fixture Two"
        second["publication"]["consentReceipt"]["reference"] = (
            "canon:fixture-two:1.0"
        )
        temporary, root = self.make_repository([first, second])
        self.addCleanup(temporary.cleanup)

        report = verify_repository(root)
        codes = {
            check.code for check in report.repository_checks if not check.passed
        }
        self.assertIn("identity.duplicate_domain", codes)
        self.assertFalse(report.passed)

    def test_repository_detects_index_drift(self):
        temporary, root = self.make_repository(
            [load_fixture("valid-claimed.json")]
        )
        self.addCleanup(temporary.cleanup)
        (root / "index" / "by-domain.json").write_text("{}\n", encoding="utf-8")

        report = verify_repository(root)
        codes = {
            check.code for check in report.repository_checks if not check.passed
        }
        self.assertIn("index.drift", codes)
        self.assertFalse(report.passed)

    def test_repository_rejects_noncanonical_registry_layout(self):
        temporary, root = self.make_repository(
            [load_fixture("valid-claimed.json")]
        )
        self.addCleanup(temporary.cleanup)
        legacy_folder = root / "registry" / "ca" / "on"
        legacy_folder.mkdir(parents=True)
        (legacy_folder / "legacy.json").write_text("{}\n", encoding="utf-8")

        report = verify_repository(root)
        codes = {
            check.code for check in report.repository_checks if not check.passed
        }
        self.assertIn("layout.noncanonical_json", codes)
        self.assertIn("index.build_failed", codes)
        self.assertFalse(report.passed)

    def test_repository_requires_one_receipt_per_profile(self):
        temporary, root = self.make_repository(
            [load_fixture("valid-claimed.json")]
        )
        self.addCleanup(temporary.cleanup)
        (root / "provenance" / "fixture-co" / "publication-receipt.json").unlink()
        write_manifest(root)

        report = verify_repository(root)
        codes = {
            check.code for check in report.repository_checks if not check.passed
        }
        self.assertIn("provenance.receipt_missing", codes)
        self.assertFalse(report.passed)

    def test_repository_rejects_orphan_receipt(self):
        temporary, root = self.make_repository(
            [load_fixture("valid-claimed.json")]
        )
        self.addCleanup(temporary.cleanup)
        receipt = load_receipt_fixture("valid-canon.json")
        receipt["entitySlug"] = "orphan"
        receipt["receiptId"] = "publication:orphan:1"
        receipt["artifact"]["path"] = "registry/orphan/profile.json"
        folder = root / "provenance" / "orphan"
        folder.mkdir()
        (folder / "publication-receipt.json").write_text(
            json.dumps(receipt, indent=2) + "\n",
            encoding="utf-8",
        )
        write_manifest(root)

        report = verify_repository(root)
        codes = {
            check.code for check in report.repository_checks if not check.passed
        }
        self.assertIn("provenance.receipt_orphaned", codes)
        self.assertFalse(report.passed)

    def test_repository_detects_profile_byte_tampering(self):
        temporary, root = self.make_repository(
            [load_fixture("valid-claimed.json")]
        )
        self.addCleanup(temporary.cleanup)
        profile_path = root / "registry" / "fixture-co" / "profile.json"
        profile_path.write_text(
            profile_path.read_text(encoding="utf-8") + "\n",
            encoding="utf-8",
        )

        report = verify_repository(root)
        receipt_codes = {
            check.code
            for receipt in report.receipts
            for check in receipt.checks
            if not check.passed
        }
        self.assertIn("integrity.byte_count", receipt_codes)
        self.assertIn("integrity.raw_hash", receipt_codes)
        self.assertFalse(report.passed)

    def test_repository_detects_manifest_drift(self):
        temporary, root = self.make_repository(
            [load_fixture("valid-claimed.json")]
        )
        self.addCleanup(temporary.cleanup)
        manifest_path = root / "manifest" / "registry-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["artifacts"][0]["sha256"] = "sha256:" + ("0" * 64)
        manifest_path.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        report = verify_repository(root)
        codes = {
            check.code for check in report.repository_checks if not check.passed
        }
        self.assertIn("manifest.drift", codes)
        self.assertFalse(report.passed)

    def test_release_snapshot_is_byte_reproducible(self):
        temporary, root = self.make_repository(
            [load_fixture("valid-claimed.json")]
        )
        self.addCleanup(temporary.cleanup)
        first = root / "release-one"
        second = root / "release-two"
        build_snapshot(root, first)
        build_snapshot(root, second)

        first_snapshot = first / "registry-snapshot.tar.gz"
        second_snapshot = second / "registry-snapshot.tar.gz"
        self.assertEqual(first_snapshot.read_bytes(), second_snapshot.read_bytes())
        self.assertEqual(
            (first / "SHA256SUMS").read_bytes(),
            (second / "SHA256SUMS").read_bytes(),
        )
        with tarfile.open(first_snapshot, "r:gz") as archive:
            members = archive.getmembers()
        self.assertEqual(
            [member.name for member in members],
            sorted(member.name for member in members),
        )
        self.assertTrue(all(member.mtime == 0 for member in members))

    def test_machine_report_has_stable_contract(self):
        temporary, root = self.make_repository(
            [load_fixture("valid-claimed.json")]
        )
        self.addCleanup(temporary.cleanup)

        payload = verify_repository(root).to_dict()
        self.assertTrue(payload["passed"])
        self.assertEqual(payload["schemaVersion"], "1.1")
        self.assertEqual(payload["verifierVersion"], "1.1.0")
        self.assertEqual(payload["summary"]["profiles"], 1)
        self.assertEqual(payload["summary"]["provenanceReceipts"], 1)
        self.assertGreater(payload["summary"]["manifestArtifacts"], 0)
        self.assertEqual(len(payload["receipts"]), 1)
        self.assertEqual(payload["summary"]["failedChecks"], 0)


if __name__ == "__main__":
    unittest.main()
