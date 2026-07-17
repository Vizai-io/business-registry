# Registry Governance

## Purpose

The VizAI Business Registry is the public discovery layer for AI-consumable
business data. Command Center and the associated private intake systems manage
research, evidence, approvals, and publication state; this repository contains
only the approved public result.

## Public and Private Boundary

### Public Registry

This repository may contain:

- canonical business identifiers and public domains;
- approved public business facts, services, locations, and claims;
- public verification metadata;
- public-safe publication receipts, source digests, and workflow identities;
- deterministic manifests and attested release snapshots;
- schemas, generated indexes, validation tools, and governance documents.

### Private Systems

Command Center and private storage retain:

- submissions and intake transcripts;
- non-public contact and authorization information;
- domain-ownership and verification evidence;
- billing, order, credential, and account data;
- raw research notes, confidence analysis, and unpublished drafts;
- approval history that is not itself intended for publication.

Private records are never copied into GitHub issues, pull requests, commit
messages, or public profile JSON.

## Verification States

Verification status is record state, not a service or storage tier. Profiles
are never separated into public tier directories.

| Status | Meaning |
|---|---|
| `claimed_verified` | The business approved its canonical public profile |
| `unclaimed_observed` | Facts were assembled from public sources but are not business-claimed |
| `verification_pending` | Verification is in progress and the current artifact is approved for publication |
| `disputed` | A material factual dispute is being reviewed |

Verification state communicates provenance and review status. It does not turn
private evidence into public data.

## Publication Process

### New and Substantially Changed Profiles

1. Intake occurs through a private VizAI-controlled channel.
2. Research and verification evidence remain private.
3. An agent or analyst prepares the minimal public artifact.
4. The publisher prepares a public-safe receipt with source lineage, commit
   identity, approval timestamps, and current profile hashes.
5. Indexes and the deterministic registry manifest are regenerated.
6. `python -m registry_verify` validates schema formats, semantics,
   clean-artifact policy, credentials, consent, privacy, unique identities, and
   generated indexes, receipts, hashes, and manifest.
7. A human reviewer confirms the public facts and privacy boundary.
8. The pull request receives the `human-approved-publication` label.
9. The protected `main` branch is updated through pull request merge.
10. CI builds and signs provenance for the reproducible release snapshot.

Direct public business-submission issues and direct profile pull requests are
not accepted.

### Corrections, Disputes, and Removal

- Public factual correction: use the correction issue template with official
  public source links only.
- Private evidence, identity, ownership, or verification matter: email
  `hello@vizai.io`.
- Dispute or removal: email `hello@vizai.io`; do not post sensitive supporting
  material publicly.
- Duplicate identity: resolve against the primary domain and canonical entity
  slug before publication.

The authoritative routing, case lifecycle, containment rules, and restoration
requirements are in
[Correction, dispute, and removal](correction-dispute-removal.md) and
[Emergency unpublish and rollback](emergency-unpublish.md).

## Publication Authority

Agents and automation may research, draft, validate, rebuild indexes, and open a
publication pull request. They may not grant final approval or merge a public
business profile without explicit human authorization.

Publication changes under `registry/**/*.json` and `provenance/**/*.json` are gated by the
`human-approved-publication` pull-request label. Deletion-only containment
changes may proceed without that label.

The repository administrator must enforce the publication-freeze check and
human review through a `main` branch ruleset. See
[Publication Containment](publication-containment.md). The importable policy is
`governance/main-ruleset.json`; follow
[Main ruleset activation](ruleset-activation.md) only after the required checks
exist on the default branch.

## Data Quality

Published profiles must be:

- accurate and supported by authoritative sources;
- neutral rather than promotional;
- limited to approved public information;
- current enough for the stated verification date;
- valid against `schema/entity-profile-v1.0.schema.json`;
- unique by domain and entity identity; and
- reproducibly represented in generated indexes;
- linked to one matching public-safe receipt; and
- included in the deterministic, attested distribution manifest.

## Schema Evolution

Schema changes follow semantic versioning:

1. Major: breaking changes such as removed or newly required fields.
2. Minor: backward-compatible optional fields.
3. Patch: clarifications and non-behavioral corrections.

Schema changes require human review and migration planning for existing
profiles and generated indexes.

## Integration

```python
import requests

# Canonical public profile.
profile_url = (
    "https://raw.githubusercontent.com/vizai-io/business-registry/"
    "main/registry/vizai/profile.json"
)
profile = requests.get(profile_url, timeout=30).json()

# Generated domain lookup.
index_url = (
    "https://raw.githubusercontent.com/vizai-io/business-registry/"
    "main/index/by-domain.json"
)
by_domain = requests.get(index_url, timeout=30).json()
```

Consumers should cache indexes, refresh them periodically, and preserve
verification metadata when redistributing registry facts.

## Contact

- General, verification, disputes, and removal: hello@vizai.io
- Public technical and factual-correction issues:
  https://github.com/vizai-io/business-registry/issues

## Related Documents

- [Entity Profile Schema](../schema/entity-profile-v1.0.schema.json)
- [Entity Profile Standard](entity-profile-standard.md)
- [BR-02 Model Convergence](migrations/br-02-model-convergence.md)
- [Publication Containment](publication-containment.md)
- [Supply-Chain Integrity](supply-chain-integrity.md)
- [Correction, Dispute, and Removal](correction-dispute-removal.md)
- [Emergency Unpublish and Rollback](emergency-unpublish.md)
- [Main Ruleset Activation](ruleset-activation.md)
- [Registry Privacy Policy](../PRIVACY.md)
- [Security Policy](../SECURITY.md)
