import copy
import json
import shutil
import tempfile
import unittest
from datetime import date
from pathlib import Path

from jsonschema import Draft7Validator, FormatChecker

from registry_verify.verifier import verify_profile, verify_repository
from tools import build_indexes


REPOSITORY = Path(__file__).resolve().parent.parent
FIXTURES = REPOSITORY / "tests" / "fixtures" / "profiles"
SCHEMA = json.loads(
    (REPOSITORY / "schema" / "entity-profile-v1.0.schema.json").read_text(
        encoding="utf-8"
    )
)
VALIDATOR = Draft7Validator(SCHEMA, format_checker=FormatChecker())
TODAY = date(2026, 7, 16)


def load_fixture(name):
    path = FIXTURES / name
    return json.loads(path.read_text(encoding="utf-8"))


def verify_fixture(name, file="registry/fixture-co/profile.json"):
    profile = load_fixture(name)
    raw = json.dumps(profile)
    return verify_profile(profile, raw, file, VALIDATOR, today=TODAY)


def failed_codes(result):
    return {check.code for check in result.checks if not check.passed}


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


class RepositoryGateTests(unittest.TestCase):
    def make_repository(self, profiles):
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        (root / "schema").mkdir()
        (root / "registry").mkdir()
        (root / "index").mkdir()
        shutil.copy2(
            REPOSITORY / "schema" / "entity-profile-v1.0.schema.json",
            root / "schema" / "entity-profile-v1.0.schema.json",
        )
        for profile in profiles:
            slug = profile["entitySlug"]
            folder = root / "registry" / slug
            folder.mkdir()
            (folder / "profile.json").write_text(
                json.dumps(profile, indent=2) + "\n",
                encoding="utf-8",
            )
        entries = build_indexes.find_all_entries(root / "registry")
        build_indexes.write_outputs(
            build_indexes.build_outputs(entries),
            root / "index",
        )
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

    def test_machine_report_has_stable_contract(self):
        temporary, root = self.make_repository(
            [load_fixture("valid-claimed.json")]
        )
        self.addCleanup(temporary.cleanup)

        payload = verify_repository(root).to_dict()
        self.assertTrue(payload["passed"])
        self.assertEqual(payload["schemaVersion"], "1.0")
        self.assertEqual(payload["verifierVersion"], "1.0.0")
        self.assertEqual(payload["summary"]["profiles"], 1)
        self.assertEqual(payload["summary"]["failedChecks"], 0)


if __name__ == "__main__":
    unittest.main()
