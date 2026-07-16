import copy
import json
import unittest
from pathlib import Path

from registry_governance.core import (
    REQUIRED_STATUS_CHECKS,
    rollback_drill,
    validate_ruleset,
    validate_ruleset_data,
)


REPOSITORY = Path(__file__).resolve().parent.parent
RULESET = REPOSITORY / "governance" / "main-ruleset.json"


class RulesetPolicyTests(unittest.TestCase):
    def load_ruleset(self):
        return json.loads(RULESET.read_text(encoding="utf-8"))

    def test_committed_ruleset_passes_governance_policy(self):
        result = validate_ruleset(RULESET)
        self.assertTrue(result["passed"], result["errors"])

    def test_bypass_actor_is_rejected(self):
        payload = self.load_ruleset()
        payload["bypass_actors"] = [
            {"actor_id": 1, "actor_type": "OrganizationAdmin", "bypass_mode": "always"}
        ]
        errors = validate_ruleset_data(payload)
        self.assertTrue(any("bypass" in error.lower() for error in errors))

    def test_pull_request_control_weakening_is_rejected(self):
        payload = self.load_ruleset()
        pull = next(rule for rule in payload["rules"] if rule["type"] == "pull_request")
        pull["parameters"]["require_code_owner_review"] = False
        pull["parameters"]["required_approving_review_count"] = 0
        errors = validate_ruleset_data(payload)
        self.assertTrue(any("CODEOWNER" in error for error in errors))
        self.assertTrue(any("approving review" in error for error in errors))

    def test_required_check_drift_is_rejected(self):
        payload = copy.deepcopy(self.load_ruleset())
        status = next(
            rule for rule in payload["rules"] if rule["type"] == "required_status_checks"
        )
        status["parameters"]["required_status_checks"] = [
            {"context": next(iter(REQUIRED_STATUS_CHECKS))}
        ]
        errors = validate_ruleset_data(payload)
        self.assertTrue(any("status checks" in error for error in errors))


class RecoveryDrillTests(unittest.TestCase):
    def test_drill_selects_a_canonical_profile_by_default(self):
        result = rollback_drill(REPOSITORY)
        self.assertTrue(result["passed"], result["checks"])
        self.assertEqual(result["entitySlug"], "vizai")

    def test_vizai_unpublish_and_exact_rollback_passes(self):
        result = rollback_drill(REPOSITORY, "vizai")
        self.assertTrue(result["passed"], result["checks"])
        self.assertEqual(
            {check["code"] for check in result["checks"]},
            {
                "baseline.verify",
                "containment.verify",
                "containment.index_absence",
                "containment.manifest_absence",
                "rollback.verify",
                "rollback.manifest_exact",
                "source.immutable",
            },
        )

    def test_noncanonical_slug_is_rejected_without_mutation(self):
        result = rollback_drill(REPOSITORY, "../vizai")
        self.assertFalse(result["passed"])
        self.assertEqual(result["checks"][0]["code"], "input.slug")


if __name__ == "__main__":
    unittest.main()
