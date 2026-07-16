# Registry Deployment and Scaling

The business registry is a reviewed public artifact repository. Command Center
and private VizAI systems own intake, evidence, consent, research, and
publication workflow state.

## Current Deployment

Source of truth:

```text
registry/<entity-slug>/profile.json
```

Distribution:

```text
index/
```

Publication flow:

```text
private intake
  -> approved public profile
  -> canonical validation
  -> generated indexes
  -> pull request
  -> human approval
  -> protected main
```

The public repository must never be used as the intake database or evidence
store.

## Repository Controls

Configure a `main` ruleset requiring:

- pull requests;
- at least one human approval;
- CODEOWNERS review;
- the canonical registry verification workflow;
- the Publication Freeze workflow;
- resolved conversations; and
- blocked force pushes and branch deletion.

Create and reserve the `human-approved-publication` label for registry owners.

## Build and Verify

```bash
python -m pip install -r tools/validation/requirements.txt
python tools/validation/validate-entity-profile.py registry/*/profile.json
python tools/validation/check-registry-duplicates.py
python tools/build_indexes.py
git diff --exit-code -- index
```

## Consumer Distribution

Git remains the transparent publication ledger and review surface. Consumers
can use:

- raw canonical profile URLs;
- `index/by-domain.json` for exact lookup;
- grouped discovery indexes;
- `index/businesses.jsonl` for bulk processing; and
- repository history for change tracking.

Cache indexes and avoid repeatedly enumerating the GitHub Contents API.

## Scaling Direction

For a substantially larger catalog:

1. keep canonical JSON and publication manifests in Git;
2. produce versioned snapshots in object storage;
3. replicate approved profiles into a query database;
4. serve search and exact lookup through an edge API;
5. maintain canonical entity URLs independent of storage implementation; and
6. preserve Git commit and artifact hashes in every replicated record.

Do not reintroduce storage tiers as source directories. Verification is record
state, not file placement.

Do not use Git LFS for the canonical JSON catalog; it weakens raw-file access
and human-readable review.

## Autonomous Agent Boundary

An agent may collect, deduplicate, research, draft, validate, regenerate
indexes, open a pull request, monitor checks, and prepare a rollback. It may not
publish private evidence or independently approve high-impact public changes.

See:

- [Publication Containment](docs/publication-containment.md)
- [Registry Governance](docs/registry-governance.md)
- [BR-02 Model Convergence](docs/migrations/br-02-model-convergence.md)
