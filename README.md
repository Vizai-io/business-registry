# VizAI Business Registry

**A public registry of structured, source-backed business discovery profiles**

The VizAI Business Registry helps AI systems, crawlers, and answer engines
identify businesses, understand what they offer, and assess how each public
profile was verified.

> **Publication containment is active.** New and changed business profiles are
> prepared through private intake, validated automatically, and published only
> after human approval. See
> [Publication Containment](docs/publication-containment.md).

## Public and Private Boundary

This repository is the public discovery layer. It contains only information
approved for public release.

- Public: canonical business profiles, generated indexes, schemas, validation
  tools, and non-sensitive factual correction requests.
- Private: intake responses, contact details not already public, authorization
  records, ownership-verification evidence, credentials, billing information,
  research notes, and unpublished drafts.

Private intake material must never be posted in a GitHub issue or pull request.

## Canonical Profile Model

Each published business lives at `registry/<entity-slug>/profile.json` and uses
the `entity-profile-v1.0` shape.

| Field | Description |
|---|---|
| `schemaVersion` | Public profile schema version |
| `entitySlug` | Stable registry identifier |
| `profileVersion` | Monotonically increasing public artifact version |
| `businessIdentifier` | Legal name, common name, and primary domain |
| `category` | Primary discovery category |
| `verification` | Public status, method, canon version, and date |
| `publication` | Public-safe policy version and consent receipt assertion |
| `profile` | Approved public facts, locations, services, industries, and claims |
| `metadata` | Publication and update dates |

The complete contract is in
[`schema/entity-profile-v1.0.schema.json`](schema/entity-profile-v1.0.schema.json).

## Usage

```python
import json
import requests

# Fetch all profiles as JSON Lines.
url = "https://raw.githubusercontent.com/vizai-io/business-registry/main/index/businesses.jsonl"
response = requests.get(url, timeout=30)
for line in response.text.strip().splitlines():
    profile = json.loads(line)
    business = profile["businessIdentifier"]
    print(business["commonName"], business["primaryDomain"])

# Fast domain lookup.
url = "https://raw.githubusercontent.com/vizai-io/business-registry/main/index/by-domain.json"
by_domain = requests.get(url, timeout=30).json()
vizai = by_domain.get("vizai.io")
```

## Directory Structure

```text
registry/
  <entity-slug>/
    profile.json

provenance/
  <entity-slug>/
    publication-receipt.json

index/
  businesses.jsonl
  by-domain.json
  by-location.json
  by-industry.json
  by-service.json
  by-status.json

schema/
  entity-profile-v1.0.schema.json
  publication-receipt-v1.0.schema.json
  registry-manifest-v1.0.schema.json

manifest/
  registry-manifest.json

registry_verify/
  __main__.py
  verifier.py

registry_supply_chain/
  __main__.py
  core.py

registry_governance/
  __main__.py
  core.py

governance/
  main-ruleset.json

tests/
  fixtures/
  test_registry_verify.py

tools/
  build_indexes.py
```

The `registry/` directory is the profile source of truth. Every profile has a
public-safe companion receipt under `provenance/`. Files in `index/` and the
deterministic manifest are generated and must not be edited by hand.

## Authoritative Verification

Install the pinned format-validation dependency and run the single verifier:

```bash
python -m pip install -r requirements.txt
python -m registry_verify
```

To also create the complete machine-readable report:

```bash
python -m registry_verify --report registry-verification-report.json
```

The command validates schema formats, semantic rules, clean-artifact policy,
credential evidence, consent assertions, privacy, unique identities, canonical
layout, publication receipts, exact and canonical profile hashes, the
deterministic manifest, and all generated indexes.

Regenerate the public distribution manifest after profiles, receipts, indexes,
or schemas change:

```bash
python -m registry_supply_chain write-manifest
python -m registry_supply_chain check-manifest
```

Build a reproducible bulk snapshot with:

```bash
python -m registry_supply_chain snapshot --output dist
```

Validate the version-controlled repository rules and exercise emergency
unpublish/rollback in an isolated copy with:

```bash
python -m registry_governance validate
python -m registry_governance rollback-drill --slug vizai
```

## Verification Status

Profiles use explicit public statuses such as:

| Status | Meaning |
|---|---|
| `claimed_verified` | The business approved its canonical public profile |
| `unclaimed_observed` | Public-source profile not yet claimed by the business |
| `verification_pending` | Verification is in progress and publication is approved |
| `disputed` | A material factual dispute is under review |

Verification metadata describes the basis for confidence; it is not a
substitute for source review.

## Adding or Updating a Business

Business submissions and verification material go through the
[private VizAI onboarding form](https://www.vizai.io/onboarding-form.html).
VizAI prepares the public artifact and opens the controlled publication pull
request.

GitHub issues are only for non-sensitive factual corrections supported by
public, authoritative source links. Do not include private contact information,
authorization evidence, credentials, order details, or unpublished material.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution workflow.

## Current Registry

- Canonical public profiles: 2
- Public-safe publication receipts: 2
- Deterministically hashed public artifacts: 17
- Claimed and verified: 2
- Fictional/example profiles in production: 0

## Related

- [Entity Profile Schema](schema/entity-profile-v1.0.schema.json)
- [Entity Profile Standard](docs/entity-profile-standard.md)
- [Authoritative Verifier](docs/authoritative-verifier.md)
- [Supply-Chain Integrity](docs/supply-chain-integrity.md)
- [BR-02 Model Convergence](docs/migrations/br-02-model-convergence.md)
- [Registry Governance](docs/registry-governance.md)
- [Publication Containment](docs/publication-containment.md)
- [Privacy Policy](PRIVACY.md)
- [Security Policy](SECURITY.md)
- [Correction, Dispute, and Removal](docs/correction-dispute-removal.md)
- [Emergency Unpublish and Rollback](docs/emergency-unpublish.md)
- [Main Ruleset Activation](docs/ruleset-activation.md)

## License

Registry data and documentation use
[CC BY 4.0](LICENSE-DATA). Software, tests, and automation use the
[MIT License](LICENSE-CODE). See [NOTICE](NOTICE) for the path-level boundary
and requested attribution.

## Contact

- General: hello@vizai.io
- Verification: [vizai.io/packages](https://www.vizai.io/packages.html)
- Public factual corrections:
  [GitHub issues](https://github.com/vizai-io/business-registry/issues)

---

**VizAI** - Helping businesses control how AI describes them
