# Submission Tools

Public repository submission tooling is intentionally disabled while
publication containment is active.

New businesses, substantial updates, verification evidence, authorization, and
private contact information must enter through the
[private VizAI onboarding form](https://www.vizai.io/onboarding-form.html).
They must not be posted in a GitHub issue, pull request, or public JSON file.

The controlled publication workflow:

1. stores intake and evidence in private systems;
2. prepares a minimal `registry/<entity-slug>/profile.json` artifact;
3. validates the canonical entity-profile schema and privacy boundary;
4. rebuilds generated indexes;
5. opens a reviewed publication pull request; and
6. requires explicit human approval before merge.

GitHub issues may be used only for non-sensitive factual corrections backed by
already-public authoritative sources.

See:

- [Contributing](../../CONTRIBUTING.md)
- [Publication Containment](../../docs/publication-containment.md)
- [Entity Profile Schema](../../schema/entity-profile-v1.0.schema.json)
