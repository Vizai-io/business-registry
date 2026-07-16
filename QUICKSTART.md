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

## 2. Install Validation Dependency

```bash
python -m pip install jsonschema
```

## 3. Validate Canonical Profiles

```bash
python tools/validation/validate-entity-profile.py \
  registry/vizai/profile.json \
  registry/wills-transfer/profile.json

python tools/validation/check-registry-duplicates.py
```

On PowerShell:

```powershell
$profiles = Get-ChildItem registry -Recurse -Filter profile.json |
  ForEach-Object { $_.FullName }
python tools/validation/validate-entity-profile.py $profiles
python tools/validation/check-registry-duplicates.py
```

## 4. Rebuild Generated Indexes

```bash
python tools/build_indexes.py
git diff -- index
```

The generator must find only real, approved public profiles. Examples, tests,
and fixtures must never be stored under `registry/`.

## 5. Publish Through a Pull Request

Business-profile changes follow this controlled path:

1. Collect submissions, evidence, and authorization privately.
2. Prepare only the minimal approved public profile.
3. Validate the profile and regenerate all indexes.
4. Open a pull request and complete the publication checklist.
5. Obtain human review and the `human-approved-publication` label.
6. Merge through the protected `main` branch.

Agents may prepare and validate the branch. They may not independently approve
or merge public business-profile changes.

## Repository Configuration

The `main` ruleset should require:

- pull requests and at least one approval;
- CODEOWNERS review;
- entity-profile validation;
- duplicate detection;
- generated-index consistency;
- the Publication Freeze check;
- conversation resolution; and
- blocked force pushes and branch deletion.

Create the `human-approved-publication` repository label before enabling the
Publication Freeze check as required.

## Intake and Corrections

- New profiles, substantial updates, and verification:
  [private onboarding form](https://www.vizai.io/onboarding-form.html)
- Public factual corrections supported by public sources:
  [GitHub issues](https://github.com/vizai-io/business-registry/issues)
- Private evidence, disputes, removal, ownership, and verification:
  `hello@vizai.io`

Never place personal information, credentials, DNS verification values, order
details, authorization evidence, or unpublished material in a public issue,
pull request, commit, or profile.

See [Publication Containment](docs/publication-containment.md) for the governing
policy.
