# BDK changelog style guide

## Goal

Rewrite the newest release section of a crate's `CHANGELOG.md` so it is useful
to downstream users of the published crate: concise, accurate, and free of
release-plz noise.

release-plz sections are only a starting point. They routinely contain:

- commits from years before the previous release (wrong baseline),
- CI, docs, tests, formatting, clippy, and release bookkeeping,
- changes that belong to a different crate,
- intermediate APIs that were introduced and removed in the same cycle,
- duplicate entries for one user-visible change.

Rebuild the section from git history and verify names and behavior in the
source at `HEAD`.

## Source of truth

For crate `NAME` (directory `crates/NAME`), previous release tag `TAG`:

```bash
git log --oneline TAG..HEAD -- crates/NAME
git log --oneline TAG..HEAD            # crate-scoped commits outside the dir
```

Include a change only if it is in this range. Use `git show <sha>` and read
`crates/NAME/src` to confirm exactly what changed. For PR context:

```bash
gh pr view <number> --repo bitcoindevkit/bdk --json title,body,files
```

Merge subjects in the range look like `Merge bitcoindevkit/bdk#NNNN: ...`; the
number is the PR. For commits without a PR, link the commit hash.

## Include

- New, removed, renamed, or changed public APIs and behavior.
- User-visible bug fixes, including correctness and soundness fixes.
- Changed defaults, feature flags, error types, and trait implementations.
- MSRV bumps.
- Dependency bumps that change public types or required versions
  (`bitcoin`, `miniscript`, `esplora-client`, `electrum-client`, `electrsd`,
  or another workspace crate).
- Behavior changes users must handle when upgrading.

## Exclude

- CI, workflows, release automation, CODEOWNERS, repository housekeeping.
- Docs-only changes, README edits, comment typo fixes.
- Tests, benchmarks, formatting, clippy/style-only cleanups.
- Internal refactors with no observable change.
- Dependency bumps that do not affect users, including dev-dependencies
  (`criterion`, `electrsd` used only by tests).
- Example-only fixes, unless the example is part of the published crate's
  documented API.
- Changes that belong only to another crate's public API.
- Release bookkeeping: `chore: release`, "Bump version to ...", "update
  changelog", merge commits.
- Anything already published in an earlier release.

## Format

Keep the release heading release-plz generated, but make the compare link point
at `bitcoindevkit/bdk`:

```markdown
## [0.24.0](https://github.com/bitcoindevkit/bdk/compare/chain-0.23.2...chain-0.24.0) - 2026-11-03
```

Use Keep a Changelog headings, in this order, only when non-empty:

`### Added`, `### Changed`, `### Fixed`, `### Removed`

Bullets:

- One user-visible change per bullet.
- Imperative present tense, capitalized, no trailing period unless the bullet
  contains multiple sentences.
- Put identifiers, types, modules, and features in backticks.
- End with a traceability link:
  `([#2380](https://github.com/bitcoindevkit/bdk/pull/2380))` or
  `([abc1234](https://github.com/bitcoindevkit/bdk/commit/abc1234))`.
- Prefix breaking changes with `**Breaking:**`.
- Combine a feature with its immediate follow-up fixes when that reads better;
  describe the outcome, not the implementation history.
- Do not mention intermediate APIs that never shipped; describe the API that
  exists at `HEAD`.

Examples:

```markdown
- Add `CanonicalView`, a reusable canonical view of a `TxGraph` ([#2029](https://github.com/bitcoindevkit/bdk/pull/2029))
- **Breaking:** `LocalChain::insert_block` now returns `InsertBlockError` when the block does not connect to the current tip ([#2115](https://github.com/bitcoindevkit/bdk/pull/2115))
- Fix `batch_size` of 0 being treated as an empty scan ([#2360](https://github.com/bitcoindevkit/bdk/pull/2360))
- Raise MSRV to `1.85.0` ([#2055](https://github.com/bitcoindevkit/bdk/pull/2055))
```

Avoid commit-speak:

- Bad: `refactor(chain): split canonical_view into canonical,canonical_view_task`
- Good: "Split canonicalization into a reusable `CanonicalTask` and the
  `ChainQuery` trait; the old `CanonicalIter` APIs are removed"

## Size

Roughly 5-25 bullets per crate. Large crates can exceed this when genuinely
warranted, but be ruthless. A small release may need only 2-5 bullets. An
empty section heading must be deleted.

## Preserve

- The file title and preamble.
- Any existing `## Unreleased` stub.
- Everything below the release section, byte-for-byte.

If the preamble says "Do not edit it manually", leave it unless the user asks
to remove it.

## Verify

1. Every bullet maps to a commit/PR in the range.
2. Every backticked API name exists at `HEAD` in that crate or a re-exported
   dependency.
3. Every `**Breaking:**` claim is supported by the diff or the PR.
4. No older release section changed.
