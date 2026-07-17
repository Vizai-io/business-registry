# Security policy

## Supported versions

Security fixes are applied to `main` and, when practical, to the latest tagged
registry snapshot. Historical commits and older snapshots are immutable
publication records and are not maintained releases.

## Report a vulnerability privately

Do not open a public issue for a suspected vulnerability, exposed secret,
private-data disclosure, or publication-control bypass.

Use GitHub's private vulnerability reporting for this repository when the
**Report a vulnerability** button is available on the Security page. If it is
not available, email `hello@vizai.io` with the subject
`SECURITY: business-registry`.

Include only what is necessary to reproduce and assess the issue:

- the affected path, workflow, release, or commit;
- the impact and reasonable attack scenario;
- minimal reproduction steps or a proof of concept;
- whether any secret or private record may already be exposed; and
- a safe way to contact you.

Do not include live credentials, unrelated personal data, or destructive test
results. If sensitive material is already public, provide its location rather
than duplicating it.

## In scope

- disclosure of secrets or non-public intake/evidence data;
- bypasses of approval, ruleset, verifier, provenance, or attestation controls;
- unsafe parsing, archive, path, dependency, or workflow behavior;
- integrity failures that allow unreviewed or mismatched registry artifacts;
- a vulnerability in the public registry's release or replication tooling.

Public factual corrections, business disputes, removal requests, and ordinary
data-quality concerns are not security vulnerabilities. Use
[Correction, dispute, and removal](docs/correction-dispute-removal.md).

## Response targets

These are operational targets, not guarantees:

- acknowledge a complete report within 3 business days;
- complete initial severity and containment assessment within 5 business days;
- coordinate remediation and disclosure timing with the reporter; and
- publish a security advisory when public action is useful and safe.

VizAI asks reporters to avoid privacy violations, service disruption, social
engineering, and data destruction. Good-faith research that follows this
policy will be handled through coordinated disclosure.
