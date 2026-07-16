# Emergency unpublish and rollback runbook

Effective: 2026-07-16

Use this runbook when a current profile creates a credible privacy, consent,
security, safety, legal, or material-integrity risk. Containment is reversible;
delaying containment to perfect the final correction is not required.

## Authority and severity

A registry owner may initiate an emergency removal. Security or privacy
incidents should also follow the private reporting and incident channels.
Automation may prepare and validate the change, but a human owner reviews and
merges it.

Treat the incident as urgent when the repository may expose a secret, private
evidence, personal data, withdrawn consent, impersonation, or a materially
false high-impact claim.

## Unpublish current distribution

1. Create a narrowly scoped branch and record the private incident/case ID.
2. Delete both:
   - `registry/<entity-slug>/profile.json`
   - `provenance/<entity-slug>/publication-receipt.json`
3. Remove empty slug directories.
4. Run:

   ```bash
   python tools/build_indexes.py
   python -m registry_supply_chain write-manifest
   python -m registry_verify --report registry-verification-report.json
   ```

5. Confirm the slug and domain are absent from every generated index and the
   manifest has no profile or receipt path for the entity.
6. Open a removal-only pull request. State the reason at a safe level (for
   example, `emergency privacy containment`) without copying private evidence.
7. Obtain CODEOWNER review and merge after all required checks pass. The
   `human-approved-publication` label is intentionally not required for a
   deletion-only change.
8. Revoke exposed credentials and address release assets, caches, mirrors, and
   search indexes as the incident requires. Git history remediation is a
   separate security operation and must not be improvised in the public PR.

## Restore or correct

Restoration is a new publication, not a reversal of the safety decision.
Prepare a corrected profile and new receipt from private approved evidence,
increase `profileVersion`, rebuild generated artifacts, obtain the publication
label and human approval, and merge through the protected branch.

If the emergency removal itself was erroneous and no profile content changes,
a revert may restore the exact files. It still requires the normal publication
approval because it republishes a profile.

## Exercise the procedure

Run the non-destructive drill from the repository root:

```bash
python -m registry_governance rollback-drill \
  --slug vizai \
  --report governance-drill-report.json
```

The drill operates only in a temporary copy. It verifies the baseline,
unpublishes the selected entity, regenerates and verifies the contained
registry, proves the entity is absent, restores the entity, and requires the
original manifest to be recovered byte-for-byte. CI runs this drill on every
pull request.
