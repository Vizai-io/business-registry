# Correction, dispute, and removal procedure

Effective: 2026-07-16

This procedure separates transparent public corrections from cases that
require private evidence, identity review, or rapid containment.

## Choose the correct route

| Request | Route | Public content allowed |
|---|---|---|
| Non-sensitive factual correction supported by an official public source | GitHub correction issue template | Profile path, disputed fact, proposed fact, and public URLs |
| Ownership, identity, verification, or authorization issue | `hello@vizai.io` | None until approved for release |
| Privacy concern or personal-data request | `hello@vizai.io` | None |
| Business dispute or conflicting private evidence | `hello@vizai.io` | None |
| Removal or consent withdrawal | `hello@vizai.io` | None unless the requester approves a public statement |
| Secret, private-data leak, or control bypass | [Security policy](../SECURITY.md) | None |

Never place identity documents, authorization evidence, credentials, private
contact information, billing data, order references, or unpublished evidence
in an issue, pull request, commit, or discussion.

## Case lifecycle

1. **Received** - record the request privately and assign a case identifier.
2. **Triaged** - classify it as public correction, private correction, dispute,
   removal, security, or abuse.
3. **Contained when necessary** - for a credible privacy, consent, safety, or
   material-integrity risk, suspend or remove the current profile first.
4. **Reviewed** - establish requester authority and compare the minimum
   necessary evidence with the current publication.
5. **Decided** - correct, annotate, mark disputed, remove, or decline with a
   documented reason.
6. **Published** - merge only the minimal public change through the controlled
   publication workflow and rebuild all generated artifacts.
7. **Closed and monitored** - notify the requester through the intake channel
   and monitor caches and downstream replicas where practical.

Operational targets are acknowledgment within 3 business days and initial
triage within 5 business days. Urgent privacy, credential, or safety reports
are handled as soon as they are identified. These targets are not guarantees.

## Decision rules

- Prefer the most authoritative and current source.
- Do not treat a source URL alone as proof of ownership or consent.
- Preserve the stable entity slug when correcting the same business.
- Increase `profileVersion` for a corrected or restored public artifact.
- Use `disputed` only when a limited public profile remains safe and useful;
  otherwise unpublish while the matter is reviewed.
- Removal-only pull requests do not require the publication approval label.
- A restoration is a new publication and requires normal human approval.

## Public audit trail

The public commit should explain the artifact action without revealing private
case material. Use a private case identifier only if it is safe and useful.
Public receipts may record a workflow identity and digest, but never the raw
request or evidence.
