# Contributing to the VizAI Business Registry

This repository is a public publishing surface. Contributions must preserve the
boundary between private intake evidence and approved public business facts.

## Submit or Update a Business

Use the [private VizAI onboarding form](https://www.vizai.io/onboarding-form.html)
for a new business, a substantial profile update, or verification.

Do not open a public issue or direct pull request containing:

- personal or non-public contact information;
- authorization or domain-ownership evidence;
- credentials, tokens, DNS values, order numbers, or billing details;
- private research notes or unpublished drafts;
- any information the business has not approved for public release.

VizAI will turn the private intake record into a minimal public artifact,
validate it, and route it through human publication review.

## Request a Public Factual Correction

Use the
[correction request template](.github/ISSUE_TEMPLATE/correction-request.md)
only when the request can be supported entirely by public, authoritative
sources.

Include:

- the canonical profile path;
- the specific public statement that is incorrect;
- the proposed factual replacement; and
- links to official public evidence.

If the evidence is private or the request concerns authorization, verification,
ownership, contact data, a dispute, or removal, contact `hello@vizai.io`
instead of posting it publicly.

## Documentation and Tooling Contributions

Pull requests for documentation, schemas, validators, tests, and index tooling
are welcome. Business-profile pull requests are created only from the controlled
publication workflow.

All pull requests must:

- be narrowly scoped;
- contain no secrets, private evidence, or unapproved personal data;
- pass `python -m registry_verify`;
- include a verification-state-compatible public-safe consent assertion;
- identify any business-profile paths changed; and
- receive human approval before publication.

## Public Artifact Requirements

A publishable profile must:

- conform to `schema/entity-profile-v1.0.schema.json`;
- live at `registry/<entity-slug>/profile.json`;
- use a stable entity slug and primary domain;
- contain only facts approved for public release;
- use neutral, source-supported language;
- include accurate verification and update metadata;
- contain no credentials, private notes, or unpublished evidence; and
- have no duplicate domain or entity identity.

Fictional examples and test fixtures must never be placed under `registry/`.
Keep them in clearly named test-fixture locations and ensure production index
generation cannot discover them.

## Publication Workflow

1. Collect source material through private intake.
2. Prepare a minimal public profile artifact.
3. Rebuild indexes and run `python -m registry_verify`.
4. Open a pull request with the publication checklist completed.
5. Obtain explicit human approval and the `human-approved-publication` label.
6. Merge through the protected `main` branch.

Agents and automation may prepare, validate, and propose public artifacts. They
must not independently approve or merge a business-profile publication.

See [Publication Containment](docs/publication-containment.md) and
[Registry Governance](docs/registry-governance.md) for the controlling policy.

## Questions

- Private or sensitive matters: hello@vizai.io
- Technical repository questions:
  [GitHub issues](https://github.com/vizai-io/business-registry/issues)
