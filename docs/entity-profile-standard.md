# Entity Profile Standard

Version: `1.0`

## Canonical Location

Each business has one public artifact:

```text
registry/<entity-slug>/profile.json
```

Example:

```text
registry/vizai/profile.json
```

The directory slug, `entitySlug`, and primary domain form the canonical public
identity. Alternate geo-based records and tier-based copies are prohibited.

## Minimal Profile

```json
{
  "schemaVersion": "1.0",
  "entitySlug": "example-business",
  "profileVersion": 1,
  "businessIdentifier": {
    "legalName": "Example Business Inc.",
    "commonName": "Example Business",
    "primaryDomain": "example-business.test"
  },
  "category": "professional-services",
  "verification": {
    "status": "unclaimed_observed",
    "method": "public-source-review",
    "lastVerified": "2026-07-16"
  },
  "publication": {
    "policyVersion": "1.0",
    "consentReceipt": {
      "status": "not-required-public-observation",
      "reference": "public-observation"
    }
  },
  "metadata": {
    "dateAdded": "2026-07-16",
    "lastUpdated": "2026-07-16"
  }
}
```

This example is documentation only and must never be copied below `registry/`
as a production entity.

`profileVersion` is required and increases whenever the public profile artifact
changes. The matching publication receipt uses the same value and receipt ID
`publication:<entity-slug>:<profileVersion>`.

## Identity Rules

- `entitySlug` uses lowercase letters, numbers, and single hyphens.
- `businessIdentifier.primaryDomain` contains a hostname, not a URL.
- A primary domain may identify only one canonical entity.
- A legal name or domain change must be resolved in the private truth workflow
  before the public identity is changed.

## Public-Safe Content

Only approved public facts belong in the profile. The public artifact must not
contain:

- intake responses or private research notes;
- authorization records or ownership proof;
- DNS values, tokens, credentials, or secrets;
- billing, order, or customer-account data;
- unpublished evidence or internal workflow fields; or
- personal contact information that was not approved as a public business
  contact point.

## Generated Distribution

`tools/build_indexes.py` derives the following artifacts from canonical
profiles:

- `index/businesses.jsonl`
- `index/by-domain.json`
- `index/by-location.json`
- `index/by-industry.json`
- `index/by-service.json`
- `index/by-status.json`

Generated indexes are not source-of-truth and must never be edited manually.
The deterministic distribution manifest is regenerated after profiles,
receipts, schemas, or indexes change:

```bash
python -m registry_supply_chain write-manifest
```

## Publication

All additions and changes follow private intake, artifact preparation,
validation, pull-request review, explicit human approval, and protected merge.
See [Publication Containment](publication-containment.md).
See [Supply-Chain Integrity](supply-chain-integrity.md) for the companion
receipt, hashes, source lineage, and release attestation contract.

Run the complete profile and repository gate with:

```bash
python -m registry_verify
```
