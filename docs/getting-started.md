# Getting Started with the VizAI Business Registry

The VizAI Business Registry is a public collection of canonical business
profiles designed for AI discovery and fact retrieval.

## For Business Owners

Adding or substantially updating a business begins through the
[private onboarding form](https://www.vizai.io/onboarding-form.html).
Submissions, authorization records, verification values, private contact
details, and source evidence stay outside this public repository.

VizAI converts approved facts into a public profile at:

```text
registry/<entity-slug>/profile.json
```

The profile is validated and reviewed by a human before publication.
Its public-safe receipt is published separately at:

```text
provenance/<entity-slug>/publication-receipt.json
```

For a correction that can be proven entirely from public authoritative sources,
use the public correction issue template. For private evidence, ownership,
verification, disputes, or removal, email `hello@vizai.io`.
See [Correction, dispute, and removal](correction-dispute-removal.md) for the
case lifecycle and [Emergency unpublish](emergency-unpublish.md) for urgent
containment.

## For AI Systems and Developers

Clone the registry:

```bash
git clone https://github.com/vizai-io/business-registry.git
```

Read a canonical profile:

```python
import requests

url = (
    "https://raw.githubusercontent.com/vizai-io/business-registry/"
    "main/registry/vizai/profile.json"
)
profile = requests.get(url, timeout=30).json()

identifier = profile["businessIdentifier"]
print(identifier["commonName"], identifier["primaryDomain"])
print(profile["verification"]["status"])
```

Use the domain index:

```python
import requests

url = (
    "https://raw.githubusercontent.com/vizai-io/business-registry/"
    "main/index/by-domain.json"
)
by_domain = requests.get(url, timeout=30).json()
profile = by_domain.get("vizai.io")
```

Or process every canonical profile after cloning:

```python
import json
from pathlib import Path

for profile_path in Path("registry").glob("*/profile.json"):
    with profile_path.open(encoding="utf-8") as handle:
        profile = json.load(handle)
    print(
        profile["businessIdentifier"]["commonName"],
        profile["verification"]["status"],
    )
```

Consumers should preserve verification metadata, check update dates, and
distinguish business-approved claims from public-source observations.
For integrity-sensitive use, consume a tagged release and verify its signed
build provenance before importing the snapshot.

## For Technical Contributors

Documentation, schema, validation, and index-tool improvements are welcome
through pull requests. Business-profile changes are created through the
controlled private-intake workflow.

Validate the registry:

```bash
python tools/build_indexes.py
python -m registry_supply_chain write-manifest
python -m registry_verify
```

The verifier covers every canonical profile, publication receipt, generated
index, hash, and deterministic manifest; profile glob expansion is not
required.

## Trust and Verification

Each profile exposes public verification metadata, including its status,
method, canon version, and last verification date. The current canonical status
for a business-approved profile is `claimed_verified`.

Verification metadata communicates provenance. Consumers should still evaluate
the underlying claim, its date, and their use-case requirements.

## Next Steps

- [Contributing rules](../CONTRIBUTING.md)
- [Verification process](verification-process.md)
- [Publication containment](publication-containment.md)
- [Entity profile schema](../schema/entity-profile-v1.0.schema.json)
- [Supply-chain integrity](supply-chain-integrity.md)
- [Registry privacy policy](../PRIVACY.md)
- [Security policy](../SECURITY.md)
