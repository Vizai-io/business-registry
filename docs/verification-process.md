# Verification Process

VizAI verification separates private proof from the public registry artifact.
The registry publishes the result and its public metadata, not the underlying
private evidence.

## Private Verification Record

Verification may use:

- control of a business domain or approved website;
- an authorized business contact;
- official public sources and business-provided source material;
- human review of identity, accuracy, and consent; and
- a recorded approval of the canonical public profile.

DNS values, tokens, email challenges, authorization records, contact details,
order information, and analyst notes remain in private VizAI-controlled systems.
They must never be posted in GitHub.

## Public Verification Metadata

A published profile may expose:

- `status`;
- `method`;
- `canonVersion`; and
- `lastVerified`.

For example:

```json
{
  "verification": {
    "status": "claimed_verified",
    "method": "customer-canon-approval",
    "canonVersion": "1.0",
    "lastVerified": "2026-06-13"
  }
}
```

This metadata states the public verification outcome without revealing the
private proof.

## Workflow

1. The business submits information through a private intake channel.
2. VizAI creates or updates the private truth record.
3. Evidence and domain or identity checks are reviewed.
4. A minimal public profile is prepared.
5. The business or authorized reviewer approves the public canon when required.
6. Automated checks validate schema, privacy boundary, duplicates, and indexes.
7. A human registry owner reviews the publication pull request.
8. The `human-approved-publication` label releases the Publication Freeze gate.
9. The protected `main` branch is updated through pull request merge.

Agents may assist with steps 2 through 7, but cannot supply the final human
publication approval or merge the profile autonomously.

## Updates

- Public-source factual correction: use the public correction issue template
  and provide only official public URLs.
- Substantial update or re-verification: use the private onboarding workflow.
- Private evidence, ownership, authorization, dispute, or removal:
  email `hello@vizai.io`.

Small and large changes are both subject to the public/private boundary. A
seemingly harmless update can still reveal private information when copied from
an intake record without review.

## Maintaining Verification

Verification should be revisited when:

- the primary domain changes;
- the business rebrands, merges, or restructures;
- material services, locations, or legal identity change;
- the business disputes the published canon;
- sources materially conflict; or
- the verification date exceeds the applicable review policy.

A stale or disputed profile should move to the appropriate public status rather
than retaining an unsupported verification claim.

## Start Verification

- Private onboarding: https://www.vizai.io/onboarding-form.html
- Service information: https://www.vizai.io/packages.html
- Sensitive questions: hello@vizai.io
