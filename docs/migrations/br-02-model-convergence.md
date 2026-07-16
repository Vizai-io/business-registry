# BR-02 Model Convergence

Effective: 2026-07-16

BR-02 makes entity-profile v1 the only production contract in the VizAI
Business Registry.

## Supported Surface

| Concern | Supported value |
|---|---|
| Profile path | `registry/<entity-slug>/profile.json` |
| Schema | `schema/entity-profile-v1.0.schema.json` |
| Authoritative verifier | `python -m registry_verify` |
| Index generator | `tools/build_indexes.py` |
| Generated distribution | `index/` |
| CI | `.github/workflows/validate-registry.yml` |

## Retired Paths

The following production models were deleted:

- `data/verified/`
- `data/community/`
- `data/enterprise/`
- geo-based `registry/<country>/<region>/<city>/<id>.json`
- `schema/business-profile-v1.0.json`
- `schema/discovery-profile-v1.0.json`
- `schema/registry-entry.schema.json`
- `tools/validate_registry.py`
- `tools/validation/validate-profile.py`
- `tools/validation/validate-entity-profile.py`
- `tools/validation/check-registry-duplicates.py`
- `tools/automation/generate-indexes.py`
- `tools/automation/generate-profile.py`

Their final source remains available in Git history. They must not be restored
as production paths.

## Field Migration

| Retired field/model | Canonical replacement |
|---|---|
| `registryId` | `entitySlug` |
| top-level `domain` | `businessIdentifier.primaryDomain` |
| top-level `name` | `businessIdentifier.commonName` |
| top-level `industry` | `category` |
| top-level `services` | `profile.services` |
| geo `location` object | `profile.country` plus `profile.locations[]` |
| `description` / `offerings` | approved facts under `profile` |
| storage or service `tier` | no public replacement |
| `verified` | `claimed_verified` when business-approved |
| `community` | `unclaimed_observed` unless a stronger state is established |
| `pending` | `verification_pending` |

`disputed` is the canonical state for a material public factual dispute.

## Consumer Migration

Consumers should stop enumerating tier directories and instead:

1. use `index/by-domain.json` for exact domain lookup;
2. use grouped files under `index/` for discovery;
3. fetch canonical profiles from `registry/<entity-slug>/profile.json`; and
4. use `verification.status` rather than a service tier as the trust signal.

No runtime redirect is possible for removed raw GitHub file paths. This
migration note and Git history are the compatibility record.
