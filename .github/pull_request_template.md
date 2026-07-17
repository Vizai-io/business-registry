## Registry publication controls

- [ ] No example, test, placeholder, or fictional company is being added below `registry/`.
- [ ] No private evidence, personal contact data, order information, credentials, or verification tokens are included.
- [ ] Every changed public claim has passed the private Truth Canon and evidence review.
- [ ] Registry publication consent is recorded privately and represented only by the public-safe `publication.consentReceipt` assertion.
- [ ] Every changed profile has a matching public-safe publication receipt with current byte and canonical hashes.
- [ ] Source lineage contains only non-sensitive references and digest-bearing inputs; no raw evidence or private snapshots are included.
- [ ] Generated indexes were rebuilt with `python tools/build_indexes.py`.
- [ ] The deterministic manifest was rebuilt with `python -m registry_supply_chain write-manifest`.
- [ ] `python -m registry_verify` passes.
- [ ] A human registry owner has reviewed the public artifact.
- [ ] Security, privacy, correction/removal, licensing, and ruleset controls are not weakened.
- [ ] For an emergency removal, the profile and receipt are both deleted and every generated artifact was rebuilt.

## Change summary

Describe the public change and its source workflow. Do not paste private evidence
or customer information into this pull request.

For a removal or dispute, include only a non-sensitive case reference and safe
action summary. Never paste private evidence into the pull request.
