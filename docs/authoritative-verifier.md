# Authoritative Registry Verifier

BR-03 replaces fragmented validation commands with:

```bash
python -m registry_verify
```

## Gates

Each canonical profile receives seven gates:

| Gate | Checks |
|---|---|
| `json` | Parseability and top-level object shape |
| `schema` | Draft 7 schema plus active format checking |
| `semantic` | Folder/slug parity, normalized domain, HTTPS URLs, bounded non-empty values, status/method compatibility, chronology, and duplicate array values |
| `clean` | Internal worksheet and workflow-marker leakage |
| `credential` | Evidence status, publication permission, and credential chronology |
| `consent` | Verification-compatible public-safe consent assertion |
| `privacy` | Forbidden intake fields, tokens, keys, secrets, DNS values, and unconsented public contacts |

Repository gates additionally enforce:

- canonical file layout;
- unique entity slugs and primary domains; and
- byte-for-byte parity for all six generated indexes.

## Human Output

```bash
python -m registry_verify
```

The command exits `0` only when every gate passes. Failures include stable check
codes, file paths, and JSON paths.

## Machine-Readable Output

Write a JSON report while retaining human console output:

```bash
python -m registry_verify --report registry-verification-report.json
```

Or emit JSON to standard output:

```bash
python -m registry_verify --format json
```

Report schema version `1.0` includes verifier version, timestamp, summary,
per-profile checks, and repository checks.

## Test Suite

```bash
python -m unittest discover -s tests -v
```

Fixtures cover valid claimed and unclaimed profiles plus negative cases for
format validation, consent, privacy, internal markers, credentials,
chronology, slug parity, duplicate identity, and index drift.

## CI

The canonical workflow runs the verifier and tests on every pull request and
every push to `main`. The JSON report is preserved as a workflow artifact even
when verification fails.
