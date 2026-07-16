# Publication containment policy

Effective: 2026-07-16

The public registry remains under controlled-publication containment. Its
profile contract and authoritative verifier are converged; provenance
manifests, repository administration settings, and rollback exercises remain.

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

## Required repository setting

Repository administrators must configure a `main` ruleset that:

- creates and uses the `human-approved-publication` label;
- requires pull requests;
- requires at least one approval;
- requires CODEOWNERS review for `registry/`, `index/`, `schema/`, and workflow
  changes;
- requires all registry validation and Publication Freeze checks;
- requires conversation resolution;
- blocks force pushes and branch deletion;
- prevents bypass except for emergency removal by designated owners.

Until that ruleset is active, this document and the workflow provide visible
controls but cannot technically prevent an administrator from pushing directly
to `main`.

## Exit criteria

Containment can be replaced by controlled autonomy only after:

- one public entity-profile contract is authoritative;
- `python -m registry_verify` checks schema, semantics, privacy, consent
  receipt, duplicates, and index parity;
- publication receipts and deterministic hashes are included;
- repository rules are enforced;
- rollback and emergency-unpublish procedures are tested.
