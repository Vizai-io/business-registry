# VizAI Entity Profile Schema

Version: `1.0`

Authoritative schema:
[`entity-profile-v1.0.schema.json`](entity-profile-v1.0.schema.json)

## Production Contract

Every published business is represented by exactly one file:

```text
registry/<entity-slug>/profile.json
```

No other business-profile shape or production source directory is supported.
The `entitySlug` value must match its directory name.

## Required Top-Level Fields

| Field | Purpose |
|---|---|
| `schemaVersion` | Contract version; currently `1.0` |
| `entitySlug` | Stable canonical entity identifier |
| `businessIdentifier` | Legal name, common name, and primary domain |
| `category` | Primary discovery category |
| `verification` | Public verification state and method |
| `metadata` | Publication and update dates |

Optional public sections are `profile`, `credentials`, and `profileVersion`.

## Verification Status

`verification.status` is the sole public trust-state field:

| Status | Meaning |
|---|---|
| `claimed_verified` | The business approved its canonical public profile |
| `unclaimed_observed` | Public facts were observed but are not business-claimed |
| `verification_pending` | Verification is in progress and the current artifact is approved for publication |
| `disputed` | A material factual dispute is under review |

The former storage and service `tier` field is not part of the entity-profile
contract.

Supported verification methods are:

- `customer-canon-approval`
- `domain-ownership`
- `email-verification`
- `manual-review`
- `public-source-review`

A `claimed_verified` profile must include a non-sensitive `canonVersion`.
Private proof, contact identities, authorization records, and evidence files
must not be embedded in the public profile.

## Public Profile Body

The optional `profile` object may contain approved public facts:

- business type, country, founding year, and ownership;
- scale and public locations;
- services and industries served;
- neutral public claims;
- public business contact points; and
- public social or directory profiles.

All objects use `additionalProperties: false`. Fields not defined by the
canonical schema are rejected.

## Credential Gate

Credentials such as awards, licenses, certifications, memberships, and
accreditations may appear only in `credentials`. Every published item must
contain:

```json
{
  "name": "Credential name",
  "evidenceStatus": "evidence_verified",
  "publicPublishAllowed": true
}
```

The evidence itself remains private.

## Validation

```bash
python tools/validation/validate-entity-profile.py registry/*/profile.json
python tools/validation/check-registry-duplicates.py
python tools/build_indexes.py
git diff --exit-code -- index
```

The canonical validator enforces the JSON schema, clean-artifact policy, and
credential publication gate. BR-03 will add the authoritative semantic and
machine-readable verification command.

## Retired Contracts

The following schemas are no longer production contracts:

- `business-profile-v1.0.json`
- `discovery-profile-v1.0.json`
- `registry-entry.schema.json`

See
[BR-02 Model Convergence](../docs/migrations/br-02-model-convergence.md)
for path and status migration guidance.
