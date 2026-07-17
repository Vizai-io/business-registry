# Quick Start

This guide covers safe local validation and controlled publication for the
VizAI Business Registry.

## 1. Clone and Inspect

```bash
git clone https://github.com/vizai-io/business-registry.git
cd business-registry
```

Canonical public profiles live at:

```text
registry/<entity-slug>/profile.json
```

Generated lookup files live under `index/`.
Public-safe publication receipts live under `provenance/`.

## 2. Install Verifier Dependencies

```bash
python -m pip install -r requirements.txt
```

## 3. Run the Authoritative Verifier

```bash
python -m registry_verify
```

For a machine-readable report:

```bash
python -m registry_verify --report registry-verification-report.json
```

## 4. Rebuild Generated Artifacts

```bash
python tools/build_indexes.py
python -m registry_supply_chain write-manifest
python -m registry_verify
```

The generator must find only real, approved public profiles. Examples, tests,
and fixtures must never be stored under `registry/`. Every profile must have
exactly one receipt, and every receipt hash must match its committed profile.

## 5. Build a Reproducible Snapshot

```bash
python -m registry_supply_chain snapshot --output dist
```

The command produces a deterministic tarball, a copy of the registry manifest,
and `SHA256SUMS`. Published workflow artifacts can be verified with:

```bash
gh attestation verify registry-snapshot.tar.gz \
  --repo Vizai-io/business-registry
```

## 6. Publish Through a Pull Request

Business-profile changes follow this controlled path:

1. Collect submissions, evidence, and authorization privately.
2. Prepare only the minimal approved public profile.
3. Generate a public-safe receipt with source lineage and current hashes.
4. Regenerate indexes and the deterministic manifest.
5. Open a pull request and complete the publication checklist.
6. Obtain human review and the `human-approved-publication` label.
7. Merge through the protected `main` branch.

Agents may prepare and validate the branch. They may not independently approve
or merge public business-profile changes.

## Repository Configuration

Run `python -m registry_governance validate`, then follow
[Main Ruleset Activation](docs/ruleset-activation.md) to import the committed
ruleset after its three required workflows are present on `main`. The ruleset
requires:

- pull requests and at least one approval;
- CODEOWNERS review;
- the authoritative registry verification command;
- the Publication Freeze check;
- conversation resolution; and
- blocked force pushes and branch deletion.

Create the `human-approved-publication` repository label before enabling the
Publication Freeze check as required.

Exercise the emergency path without changing the repository:

```bash
python -m registry_governance rollback-drill --slug vizai \
  --report governance-drill-report.json
```

## Intake and Corrections

- New profiles, substantial updates, and verification:
  [private onboarding form](https://www.vizai.io/onboarding-form.html)
- Public factual corrections supported by public sources:
  [GitHub issues](https://github.com/vizai-io/business-registry/issues)
- Private evidence, disputes, removal, ownership, and verification:
  `hello@vizai.io`
- Security or accidental disclosure: follow [SECURITY.md](SECURITY.md)

Never place personal information, credentials, DNS verification values, order
details, authorization evidence, or unpublished material in a public issue,
pull request, commit, or profile.

See [Publication Containment](docs/publication-containment.md) for the governing
policy and [Supply-Chain Integrity](docs/supply-chain-integrity.md) for hashes,
receipts, snapshots, and attestations.
