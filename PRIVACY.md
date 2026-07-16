# Registry privacy policy

Effective: 2026-07-16

This policy describes the public VizAI Business Registry repository. It is an
operational data-minimization policy, not a replacement for any privacy notice
that applies to VizAI's private services.

## Public data boundary

The registry publishes structured business facts approved for public release,
public-source observations, verification state, non-sensitive source lineage,
and integrity hashes. It is not a people directory, customer database, private
evidence store, or intake system.

The public repository must not contain:

- private or personal contact details;
- customer submissions, intake transcripts, or authorization records;
- credentials, tokens, DNS proof, billing or order information;
- raw research notes, unpublished evidence, or internal confidence analysis;
- sensitive dispute, ownership, or removal evidence.

Named people and business contact information may be published only when the
information is already intentionally public, relevant to the business profile,
and approved under the publication workflow. Prefer role-based business
contact channels over personal details.

## Private records

Private intake, evidence, consent, approval history, and case-management data
remain in VizAI-controlled systems outside this repository. Public receipts
contain assertions and digests, not the private source records themselves.
A hash proves integrity; it does not make the underlying private material
public.

## Retention and repository history

Git history and released snapshots are designed to be durable. Emergency
unpublication removes material from the current distribution and indexes, but
may not erase prior clones, caches, forks, or historical releases. Sensitive
material must therefore never be committed. If it is, use the private security
reporting path immediately so containment can include history and credential
response.

## Corrections, disputes, and removal

Use the public correction template only for non-sensitive facts supported by
public authoritative sources. Send privacy requests, disputes, removals,
ownership evidence, and any sensitive correction through the private route in
[Correction, dispute, and removal](docs/correction-dispute-removal.md).

VizAI records the minimum case information needed to assess and execute the
request. Publication may be suspended while identity, authority, safety, or
conflicting evidence is reviewed.

## Automated processing

Automation may collect public business facts, detect drift, draft changes, and
run quality checks. It may not independently override consent, approve a
high-impact publication, or expose private evidence. Human approval remains
required for additions and material changes to public profiles.

## Contact

- Sensitive privacy, dispute, or removal request: `hello@vizai.io`
- Public, non-sensitive factual correction: use the repository correction
  issue template
- Security or accidental disclosure: follow [SECURITY.md](SECURITY.md)
