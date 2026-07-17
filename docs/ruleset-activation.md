# Main ruleset activation

The version-controlled ruleset is
[`governance/main-ruleset.json`](../governance/main-ruleset.json). It is an
importable GitHub repository ruleset targeting the default branch.

## Safety preconditions

Do not activate the ruleset until all of the following are true on `main`:

- `.github/workflows/validate-registry.yml` is present;
- `.github/workflows/publication-freeze.yml` runs on every pull request;
- `.github/workflows/governance-audit.yml` is present;
- a pull request has produced the three required check contexts;
- the `human-approved-publication` label exists;
- CODEOWNERS resolves to the write-enabled `Vizai-io` maintainer account; and
- an administrator has confirmed the repository allows squash merges.

Requiring checks before their workflows exist on the default branch can block
all pull requests. This is why BR-05 commits the active definition first but
defers the GitHub-side import until the stacked BR-03, BR-04, and BR-05 changes
are merged.

## Validate and import

1. Run `python -m registry_governance validate`.
2. Open **Settings > Rules > Rulesets > New branch ruleset**.
3. Choose **Import a ruleset** and import `governance/main-ruleset.json`.
4. Review the target (`~DEFAULT_BRANCH`), empty bypass list, pull-request
   controls, and exact required check names.
5. Save the ruleset as **Active**.
6. Open a documentation-only test pull request and confirm direct pushes,
   force pushes, deletion, unresolved conversations, and failed checks are
   blocked.

The same payload can be applied through GitHub's repository rulesets REST API
by a token with repository Administration write permission. Never embed that
token in this repository or CI logs.

## Required controls

- pull request before merge;
- no required approving review, CODEOWNER review, stale-review dismissal, or
  latest-push approval while the repository has one maintainer;
- resolved review conversations;
- strict required status checks;
- linear history with squash merges only;
- blocked force pushes and default-branch deletion;
- no standing bypass actors.

Emergency removal remains possible through a deletion-only pull request. The
Publication Freeze workflow skips the publication label for deletion-only
changes, while the review and validation rules remain in force.

## Solo-maintainer boundary

The solo policy does not treat automation as a human reviewer. New or modified
business profiles still require the write-enabled maintainer to inspect the
artifact and apply `human-approved-publication`; the Publication Freeze check
enforces that explicit action. Code and documentation changes require the full
CI suite but do not require a second account to approve them.

When a second human maintainer is added, update this policy through a pull
request to require one independent approval, CODEOWNER review, stale-review
dismissal, and latest-push approval before changing the live ruleset.
