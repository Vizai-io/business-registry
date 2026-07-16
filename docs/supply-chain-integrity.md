# Supply-Chain Integrity

BR-04 makes every public profile traceable to a public-safe publication receipt
and makes the registry distribution byte-verifiable.

## Artifact Chain

```text
private Canon or public-source review
  -> digest-bearing source lineage
  -> canonical profile
  -> public-safe publication receipt
  -> generated indexes
  -> deterministic registry manifest
  -> reproducible release snapshot
  -> signed SLSA build-provenance attestation
```

Private evidence, raw crawl snapshots, personal approver identities, consent
documents, and internal notes remain outside this repository.

## Publication Receipts

Every profile at:

```text
registry/<entity-slug>/profile.json
```

has exactly one companion receipt at:

```text
provenance/<entity-slug>/publication-receipt.json
```

The receipt records:

- entity slug and monotonic profile version;
- exact profile byte count and SHA-256;
- canonical JSON SHA-256 compatible with the VizAI publication boundary;
- source system, repository, and full source commit SHA;
- one or more digest-bearing lineage inputs;
- public-safe policy and consent assertions;
- preparation and approval timestamps; and
- a workflow identity, never a personal approver identity.

The authoritative contract is
[`schema/publication-receipt-v1.0.schema.json`](../schema/publication-receipt-v1.0.schema.json).

### Lineage Types

`vizai-discovery-canon`
: A new publication prepared from an approved private Canon. The receipt
  identifies `Vizai-io/vizai-discovery`, the Canon version, the source commit,
  and digest-bearing Canon, snapshot, document, or review inputs.

`public-source-review`
: An approved unclaimed publication based entirely on public sources. It does
  not assert a private Canon version.

`historical-registry-migration`
: A pre-BR-04 publication whose prior Git history is the strongest available
  public lineage. This status is explicit so the registry never invents
  crawler evidence or approval records that were not captured historically.

Crawl lineage includes a content digest and an opaque snapshot reference.
`publicUrl` is optional; when present it must be a credential-free HTTPS URL
without a query string or fragment.

## Hashes

Receipts use two complementary hashes:

| Field | Meaning |
|---|---|
| `artifact.sha256` | SHA-256 over the exact committed profile bytes |
| `artifact.canonicalJsonSha256` | SHA-256 over recursively sorted, compact UTF-8 JSON |

Exact-byte hashes detect formatting and newline changes. Canonical JSON hashes
provide key-order-independent parity with the VizAI publishing boundary.

The canonicalization identifier is `vizai-canonical-json-v1`:

- object keys sorted recursively;
- array order preserved;
- UTF-8 encoding;
- no insignificant whitespace; and
- no non-finite numeric values.

The entity schema permits integers but not floating-point fields, avoiding
cross-language number-normalization ambiguity.

## Deterministic Manifest

[`manifest/registry-manifest.json`](../manifest/registry-manifest.json)
inventories the public distribution surface:

- `LICENSE`, `LICENSE-DATA`, `LICENSE-CODE`, and `NOTICE`;
- canonical schemas;
- profiles;
- publication receipts; and
- generated indexes.

Build or check it with:

```bash
python -m registry_supply_chain write-manifest
python -m registry_supply_chain check-manifest
```

`.gitattributes` forces LF line endings for text files so raw-byte hashes remain
stable across Windows, macOS, and Linux checkouts.

The manifest intentionally contains no generation timestamp, branch name, or
workflow run ID. The same public artifacts therefore produce identical
manifest bytes.

## Reproducible Snapshot

Build the release bundle with:

```bash
python -m registry_supply_chain snapshot --output dist
```

Outputs:

- `dist/registry-snapshot.tar.gz`;
- `dist/registry-manifest.json`; and
- `dist/SHA256SUMS`.

Archive paths are sorted and tar metadata is normalized to a zero timestamp,
numeric owner `0`, empty owner names, and mode `0644`. Identical source
artifacts produce identical snapshot bytes.

## Signed Build Provenance

On every push to `main`, tag matching `registry-v*`, or manual dispatch, the
`Build and Attest Registry Snapshot` workflow:

1. runs the authoritative verifier;
2. checks the committed manifest;
3. builds the reproducible snapshot;
4. signs SLSA build provenance for the snapshot and manifest through
   GitHub artifact attestations; and
5. preserves the portable Sigstore bundle with the release assets.

A `registry-v*` tag also creates or refreshes the GitHub release. The build job
has only `contents: read`, `id-token: write`, and `attestations: write`.
Release write permission is isolated to the tag-only release job.

GitHub documents that `actions/attest` uses the OIDC token to obtain a
short-lived Sigstore signing certificate and stores the resulting attestation:

- https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations
- https://github.com/actions/attest

Verify a downloaded asset:

```bash
gh attestation verify registry-snapshot.tar.gz \
  --repo Vizai-io/business-registry
```

Then compare the downloaded files with `SHA256SUMS` and inspect
`registry-manifest.json` before consuming the snapshot.

Tagged releases also contain `registry-snapshot.sigstore.json`, the portable
Sigstore bundle emitted by the attestation action.

## Controlled Publication Sequence

For every new or changed profile:

```bash
python tools/build_indexes.py
python -m registry_supply_chain write-manifest
python -m registry_verify
python -m unittest discover -s tests -v
```

Profile and receipt changes both activate Publication Freeze and require the
`human-approved-publication` label. Agents may create the artifact chain and
open the pull request, but may not approve or merge a public publication.
