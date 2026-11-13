---
name: bdk-changelog-update
description: Use when release-plz has generated or refreshed a rust crate CHANGELOG, or when asked to produce consistent, professional release notes for a repository rust crate since the previous release. Discovers each workspace crate's previous tag and new version, dispatches one subagent per rust crate, rebuilds sections from git commit history, and validates the result.
---

# Release Changelogs

Turn release-plz's raw output into concise, verified CHANGELOG release notes — one crate at a time, with one subagent per crate.

## Hard rules

- **Keep a Changelog style** follow the style guide in https://keepachangelog.com/en/1.0.0/
- **No release dates in headings.** Never append a date to a version heading.
  Remove any ` - YYYY-MM-DD` suffix already present in the changelog, including
  on older headings. The date the release PR is made is not the date of the
  release.
- **One subagent per crate**, dispatched in parallel.
- **Rebuild from history.** Use `git log <previous-tag>..HEAD`; never treat
  release-plz bullets as the source of truth.
- **Only rewrite the newest release section.** Preserve the preamble, any
  `## Unreleased` stub, and every older release byte-for-byte, except for
  stripping ` - YYYY-MM-DD` date suffixes from version headings.
- **User-facing changes only.** No CI, docs, tests, formatting, clippy,
  internal refactors, example-only fixes, dependency bumps, or release
  bookkeeping.
- **Link to the parent bitcoindevkit repository**, not the fork that ran release-plz.
- **Verify every claim.** Confirm API names against the source at `HEAD`, and
  every `**Breaking:**` against the diff or PR.
- **Do not commit, tag, or push.** Leave edits in the working tree unless the
  user explicitly asks otherwise.
- Never invent a change. If uncertain, omit it or ask the user.

## 1. Confirm the release state

```bash
git status --short
git log --oneline -5
```

You are in the right state when the changelogs contain a freshly generated
release section (release-plz's `chore: release` commit or its release PR).
If there is no new section, stop and ask the user to run release-plz first.

## 2. Inspect the workspace

```bash
python3 ~/.config/opencode/skills/bdk-changelog-update/scripts/inspect_workspace.py \
  --root . --out /tmp/opencode/bdk-changelog
```

The script finds each crate from `release-plz.toml` (falling back to workspace
members), reads the newest release heading and its compare URL, and writes:

- `/tmp/opencode/bdk-changelog/context.json` — machine-readable inputs
- `/tmp/opencode/bdk-changelog/commits/<crate>.txt` — commit digest per crate
  (path commits, full range, PR merges)

Only rewrite crates with `"needs_update": true` (the crate is part of the
pending release: the heading's new tag does not exist yet). Use
`--only crate1,crate2` to narrow further. `--date YYYY-MM-DD` remains only for
repositories whose headings still carry dates.

Review the warnings:

- **`prev_is_ancestor: false`** — patch releases on maintenance branches
  (e.g. `chain-0.23.4`) are often not ancestors of `master`. Keep the tag
  release-plz used in the compare URL as the baseline; do not diff against an
  unrelated tag. Mention the situation in your final report.
- **compare URL not `bitcoindevkit/bdk`** — release-plz ran on a fork. Fix it.
- **new tag does not match `Cargo.toml`** — release-plz and the manifest
  disagree; investigate before editing.

For context, read one or two current sections to see how the repository has
phrased similar changes.

## 3. Dispatch the subagents

Use the `general` agent, one call per crate, **all in one message** so they run
concurrently. Build each prompt verbatim from
`~/.config/opencode/skills/bdk-changelog-update/references/subagent-brief.md`,
substituting:

| Placeholder | Value |
|---|---|
| `{{root}}` | absolute repository root |
| `{{package}}` | crate package name (e.g. `bdk_chain`) |
| `{{crate_dir}}` | crate directory (e.g. `crates/chain`) |
| `{{changelog}}` | changelog path (e.g. `crates/chain/CHANGELOG.md`) |
| `{{prev_tag}}` | previous release tag from the compare URL |
| `{{heading}}` | the generated release heading (with any date already removed) |
| `{{commit_file}}` | digest path from `context.json` |
| `{{style_guide}}` | `.../references/changelog-style.md` |

Add any crate-specific warnings you found in step 2. Do not paraphrase the
brief; its exclusion rules and verification steps are what keep the results
consistent.

## 4. Review like an editor

The subagents will report the final section, uncertainties, and integrity
confirmation. Then:

1. Run the validator:
   ```bash
   python3 ~/.config/opencode/skills/bdk-changelog-update/scripts/validate_changelogs.py \
     --root . --context /tmp/opencode/bdk-changelog/context.json
   ```
   It checks preamble/tail integrity against `HEAD`, link targets, heading
   order, empty sections, balanced markup, and rejects any version heading that
   carries a ` - YYYY-MM-DD` date, including older ones.
2. **Spot-check every `**Breaking:**` claim and every backticked API name**
   with `grep -rn '<name>' crates/<crate>/src`, or codegraph. This is where
   plausible-sounding but wrong entries are caught.
3. Look for the failure modes below and fix them directly.
4. Re-run the validator until it passes.

## 5. Report

Keep it short:

- Table: crate, new version, number of bullets.
- The handful of substantive corrections you made during review.
- Any crates skipped and why.
- Confirm that preamble/older sections are unchanged and nothing was committed.
- If the preamble still says "Do not edit it manually", ask whether to remove
  it now that the file is hand-maintained.

## Known failure modes

These caused real problems on the first run; check for them explicitly.

- **Wrong baseline.** release-plz can include years-old commits because it
  failed to resolve the intended tag on the fork. If an entry predates the
  previous release, drop it.
- **Already-released work.** Batching, merkle proofs, `FilterIter`, and similar
  features were shipped in earlier patch releases. Check the previous section
  before including anything.
- **Intermediate APIs.** APIs introduced and removed within the same cycle
  (`CanonicalViewTx`, an early `min_confirmations` parameter) never shipped.
  Describe only what exists at `HEAD`.
- **Plausible names that do not exist.** Confirm exact identifiers:
  `get_block_infos` not `get_blocks_infos`, `mine_empty_block` not
  `mine_empty_blocks`, `spks_from_indexer` (a trait method, easy to miss with
  a `pub fn` grep).
- **False "type changed" claims.** Verify struct field types against the
  previous tag with `git show <tag>:path`; e.g. `TestEnv::bitcoind` did not
  change type when `electrsd` was bumped, even though the RPC client did.
- **Dependency duplication.** Do not copy a dependency's changelog into every
  dependent crate. Mention a new baseline only when it changes this crate's
  public types or required versions.
- **Dev-dependency noise.** `criterion`, `electrsd` in dev-dependencies, test
  fixtures, and benchmark-only commits are not user-facing.
- **Example-only fixes.** A Windows import fix in an example usually does not
  belong in the library changelog.
- **Fork links.** Replace `github.com/notmandatory/bdk/...` with
  `github.com/bitcoindevkit/bdk/...`.
- **Mixed formatting.** Use imperative bullets and inline links consistently
  within a section; do not hard-wrap one crate and single-line another unless
  the file's existing style demands it.

## Files

- `references/changelog-style.md` — the shared style guide given to subagents.
- `references/subagent-brief.md` — prompt template for one crate.
- `scripts/inspect_workspace.py` — discover releases and write commit digests.
- `scripts/validate_changelogs.py` — integrity and formatting checks.
