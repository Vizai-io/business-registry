# Public Data Quality Standard

The registry publishes small, neutral, source-backed business profiles that are
safe for public distribution.

## Quality Principles

1. **Identity integrity** — one entity slug and primary domain identify one
   canonical business.
2. **Accuracy** — public facts agree with the approved truth record and
   authoritative sources.
3. **Neutrality** — descriptions avoid unsupported promotional language.
4. **Recency** — verification and update dates accurately describe the review.
5. **Provenance** — verification metadata communicates how the public profile
   was established without exposing private evidence.
6. **Privacy** — only explicitly approved public information is published.
7. **Reproducibility** — committed indexes exactly match canonical profiles.

BR-04 strengthens provenance and reproducibility: every profile has a
public-safe, digest-bearing receipt; exact-byte and canonical profile hashes
must match; generated indexes and the deterministic manifest must be current;
and release snapshots carry signed build provenance.

## Required Checks

Every profile must:

- live at `registry/<entity-slug>/profile.json`;
- validate against `schema/entity-profile-v1.0.schema.json`;
- contain only fields defined by that schema;
- use a monotonically increasing integer `profileVersion`;
- use a unique entity slug and primary domain;
- pass the clean-artifact and credential gates;
- contain no private intake, verification, authorization, or account data; and
- be represented exactly in all generated indexes;
- have one matching public-safe publication receipt; and
- appear exactly in the deterministic registry manifest.

## Claim Quality

Public claims should be specific, bounded, and testable.

Acceptable:

- “Provides third-party logistics and warehousing services.”
- “Operates facilities in Smiths Falls, Brockville, Cornwall, Ottawa, and
  Perth.”

Avoid:

- “The best logistics company.”
- “Industry-leading technology.”
- future promises, private conclusions, or unsupported scale claims.

Credentials, awards, licenses, memberships, and certifications belong in the
evidence-gated `credentials` array rather than the general claims list.

## Verification States

| Status | Quality interpretation |
|---|---|
| `claimed_verified` | Business-approved canonical public facts |
| `unclaimed_observed` | Public-source observations not claimed by the business |
| `verification_pending` | Review is underway; current public artifact was approved for release |
| `disputed` | A material factual conflict requires resolution |

A numerical `qualityScore`, when present, is supplementary. It does not replace
the verification state, source review, or publication approval.

## Review Checklist

- [ ] Identity and domain are correct.
- [ ] Directory slug matches the intended canonical entity.
- [ ] Dates and verification state are current.
- [ ] Claims are neutral and publicly supportable.
- [ ] Public contact fields are business contact points approved for release.
- [ ] Credentials passed the evidence and publication gates.
- [ ] No private or internal material appears in the artifact.
- [ ] Duplicate detection passes.
- [ ] Generated indexes are current.
- [ ] Receipt identity, policy, byte count, and both profile hashes match.
- [ ] Source lineage references contain no private evidence or secrets.
- [ ] The deterministic registry manifest is current.
- [ ] Human publication approval is recorded.

## Commands

```bash
python tools/build_indexes.py
python -m registry_supply_chain write-manifest
python -m registry_verify
```

See [Publication Containment](publication-containment.md) for the release
boundary and [Entity Profile Standard](entity-profile-standard.md) for the
canonical layout. See [Supply-Chain Integrity](supply-chain-integrity.md) for
receipt and release requirements.
