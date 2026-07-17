# Publication containment policy

Effective: 2026-07-16

The public registry remains under controlled-publication containment. Its
profile contract, authoritative verifier, provenance receipts, deterministic
manifest, attested snapshot build, version-controlled ruleset, and automated
rollback exercise are active. GitHub-side ruleset activation remains after the
stacked controls land on `main`.

## Current rules

1. Example, test, placeholder, and fictional businesses must never exist below
   `registry/` or appear in generated indexes.
2. Business submissions, verification requests, ownership proof, purchase
   references, contact details, and private evidence must use VizAI's private
   intake workflow. They must not be posted in public GitHub issues or pull
   requests.
3. Public GitHub issues may contain only non-sensitive factual corrections and
   links to already-public authoritative evidence.
4. Automated agents may prepare and validate a publication branch, but may not
   merge a new or modified public profile.
5. A maintainer must review the artifact and apply the
   `human-approved-publication` label before the publication-freeze check will
   pass.
6. Registry changes must be submitted through a pull request. Direct publishing
   to `main` remains prohibited by policy and must be enforced with a GitHub
   repository ruleset.
7. Removal-only pull requests are allowed without the publication label so
   false, unsafe, or consent-withdrawn records can be contained quickly.
8. Every profile requires a matching public-safe publication receipt, and both
   profile and receipt changes activate the Publication Freeze check.
9. Every public distribution snapshot must be reproducible and carry
   GitHub-verifiable signed build provenance.

## Required repository setting

Repository administrators must configure a `main` ruleset that:

- creates and uses the `human-approved-publication` label;
- requires pull requests;
- requires no second-person approval or CODEOWNER review while VizAI operates
  this repository with one maintainer;
- requires all registry validation and Publication Freeze checks;
- requires conversation resolution;
- blocks force pushes and branch deletion;
- has no standing bypass actors. Emergency removal uses a deletion-only pull
  request, so review and validation remain in force without the publication
  approval label.

For additions and modifications, the solo maintainer's explicit
`human-approved-publication` label is the human review boundary. The ruleset
must be upgraded to independent approval and required CODEOWNER review when a
second human maintainer is available.

The validated definition is committed at `governance/main-ruleset.json`.
Administrators must follow [Main Ruleset Activation](ruleset-activation.md)
after all required workflows exist on `main`. Until it is active on GitHub,
the repository cannot technically prevent an administrator from pushing
directly to `main`.

## Exit criteria

Containment can be replaced by controlled autonomy only after:

- one public entity-profile contract is authoritative;
- `python -m registry_verify` checks schema, semantics, privacy, consent
  receipt, duplicates, and index parity;
- publication receipts and deterministic hashes are included (implemented in
  BR-04);
- repository rules are enforced;
- rollback and emergency-unpublish procedures are tested (implemented in
  BR-05 and continuously exercised by Governance Audit).
