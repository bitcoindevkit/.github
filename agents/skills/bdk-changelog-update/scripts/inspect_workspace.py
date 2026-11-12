#!/usr/bin/env python3
"""Collect everything needed to rewrite a Cargo workspace's release changelogs.

For every crate with a CHANGELOG.md, this script:
  * reads the newest release heading and its compare URL,
  * derives the previous release tag and the new tag,
  * checks whether the previous tag is an ancestor of HEAD,
  * writes a per-crate commit digest,
  * marks which crates belong to the current release (same release date).

Output layout (default /tmp/opencode/bdk-changelog):
  context.json
  commits/<crate>.txt
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path

HEADING_RE = re.compile(
    r"^## \[(?P<version>[^\]]+)\]"
    r"\((?P<url>https://github\.com/(?P<repo>[^/]+/[^/]+)/compare/"
    r"(?P<prev>.+?)\.\.\.(?P<new>.+?))\)"
    r"(?: - (?P<date>\d{4}-\d{2}-\d{2}))?\s*$"
)

SHORT = {"bdk_chain": "chain", "bdk_core": "core", "bdk_bitcoind_rpc": "bitcoind_rpc",
         "bdk_electrum": "electrum", "bdk_esplora": "esplora",
         "bdk_file_store": "file_store", "bdk_testenv": "testenv"}


def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args], cwd=root, text=True, capture_output=True, check=check
    )


def run_git(root: Path, *args: str) -> str:
    return git(root, *args).stdout.strip()


def package_version(crate_dir: Path, workspace: dict) -> str:
    cargo = crate_dir / "Cargo.toml"
    data = tomllib.loads(cargo.read_text())
    version = data.get("package", {}).get("version", "")
    if version == {"workspace": True} or version is True:
        return str(workspace.get("package", {}).get("version", ""))
    if isinstance(version, dict) and version.get("workspace"):
        return str(workspace.get("package", {}).get("version", ""))
    return str(version)


def discover(root: Path) -> list[dict]:
    workspace = tomllib.loads((root / "Cargo.toml").read_text())
    entries: list[dict] = []

    release_plz = root / "release-plz.toml"
    if release_plz.exists():
        cfg = tomllib.loads(release_plz.read_text())
        for pkg in cfg.get("package", []):
            changelog = root / pkg["changelog_path"]
            entries.append(
                {
                    "package": pkg["name"],
                    "crate_dir": str(changelog.parent.relative_to(root)),
                    "changelog": str(changelog.relative_to(root)),
                }
            )

    if not entries:
        for member in workspace.get("workspace", {}).get("members", []):
            for crate_dir in sorted(root.glob(member)):
                changelog = crate_dir / "CHANGELOG.md"
                if not changelog.exists():
                    continue
                data = tomllib.loads((crate_dir / "Cargo.toml").read_text())
                entries.append(
                    {
                        "package": data["package"]["name"],
                        "crate_dir": str(crate_dir.relative_to(root)),
                        "changelog": str(changelog.relative_to(root)),
                    }
                )

    for entry in entries:
        entry["version"] = package_version(root / entry["crate_dir"], workspace)
    return entries


def newest_heading(changelog: Path) -> dict | None:
    for line in changelog.read_text().splitlines():
        match = HEADING_RE.match(line)
        if match:
            data = match.groupdict()
            data["heading"] = line
            return data
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="repository root or a path inside it")
    parser.add_argument("--out", default="/tmp/opencode/bdk-changelog")
    parser.add_argument("--date", help="release date to update (default: newest date found)")
    parser.add_argument("--only", help="comma-separated crate names to include")
    args = parser.parse_args()

    root = Path(run_git(Path(args.root).resolve(), "rev-parse", "--show-toplevel"))
    out = Path(args.out).resolve()
    commits_dir = out / "commits"
    commits_dir.mkdir(parents=True, exist_ok=True)

    warnings: list[str] = []
    entries: list[dict] = []

    for entry in discover(root):
        changelog = root / entry["changelog"]
        heading = newest_heading(changelog)
        if not heading:
            warnings.append(f"{entry['package']}: no release heading with a compare URL")
            continue

        entry.update(
            {
                "prev_tag": heading["prev"],
                "new_tag": heading["new"],
                "heading": heading["heading"],
                "date": heading.get("date") or "",
                "compare_repo": heading["repo"],
            }
        )

        if entry["compare_repo"] != "bitcoindevkit/bdk":
            warnings.append(
                f"{entry['package']}: compare URL points at {entry['compare_repo']}, "
                "rewrite it to bitcoindevkit/bdk"
            )

        if entry["new_tag"].rsplit("-", 1)[-1] != entry["version"]:
            warnings.append(
                f"{entry['package']}: new tag {entry['new_tag']} does not match "
                f"Cargo.toml version {entry['version']}"
            )

        ancestor = git(
            root, "merge-base", "--is-ancestor", entry["prev_tag"], "HEAD", check=False
        )
        entry["prev_is_ancestor"] = ancestor.returncode == 0
        if not entry["prev_is_ancestor"]:
            prefix = entry["prev_tag"].rsplit("-", 1)[0]
            merged = run_git(root, "tag", "--merged", "HEAD", "--sort=-creatordate")
            candidates = [t for t in merged.splitlines() if t.startswith(prefix + "-")][:5]
            entry["ancestor_tags"] = candidates
            warnings.append(
                f"{entry['package']}: {entry['prev_tag']} is not an ancestor of HEAD; "
                f"nearest ancestor tags: {', '.join(candidates) or 'none'}. "
                "Keep the release-plz baseline unless the user says otherwise."
            )

        if not entry["date"]:
            warnings.append(f"{entry['package']}: release heading has no date")

        entries.append(entry)

    dates = [e["date"] for e in entries if e.get("date")]
    target_date = args.date or (max(dates) if dates else "")
    only = {s.strip() for s in args.only.split(",")} if args.only else None

    for entry in entries:
        entry["needs_update"] = (
            entry.get("date") == target_date
            and (only is None or entry["package"] in only or str(entry["crate_dir"]) in only)
        )

    # Per-crate digests.
    for entry in entries:
        prev = entry["prev_tag"]
        crate_dir = str(entry["crate_dir"])
        path_log = run_git(
            root, "log", "--format=%h %s", f"{prev}..HEAD", "--", crate_dir
        )
        all_log = run_git(root, "log", "--format=%h %s", f"{prev}..HEAD")
        merge_log = "\n".join(
            line for line in all_log.splitlines() if re.search(r"Merge .*#\d+", line)
        )
        digest = (
            f"# {entry['package']} — {prev}..HEAD\n"
            f"# Heading: {entry['heading']}\n"
            f"# {len(all_log.splitlines())} commits in range; "
            f"{len(path_log.splitlines())} touch {crate_dir}\n\n"
            f"## Commits touching {crate_dir}\n\n{path_log or '(none)'}\n\n"
            f"## All commits in range (for crate-scoped commits outside the path)\n\n"
            f"{all_log}\n\n"
            f"## PR merges in range\n\n{merge_log or '(none)'}\n"
        )
        digest_path = commits_dir / f"{entry['package']}.txt"
        digest_path.write_text(digest)
        entry["commit_file"] = str(digest_path)
        entry["commit_count"] = len(all_log.splitlines())
        entry["path_commit_count"] = len(path_log.splitlines())

    context = {
        "root": str(root),
        "generated_at": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        "target_date": target_date,
        "crates": entries,
        "warnings": warnings,
    }
    (out / "context.json").write_text(json.dumps(context, indent=2) + "\n")

    print(f"root: {root}")
    print(f"out:  {out}")
    print(f"release date: {target_date or '(unknown)'}")
    print()
    print(f"{'crate':22} {'version':8} {'prev tag':18} {'anc':3} {'commits':>7} {'path':>5}  update")
    for entry in entries:
        print(
            f"{entry['package']:22} {entry['version']:8} {entry['prev_tag']:18} "
            f"{'yes' if entry['prev_is_ancestor'] else 'NO':3} "
            f"{entry['commit_count']:7} {entry['path_commit_count']:5}  "
            f"{'yes' if entry['needs_update'] else 'no'}"
        )

    if warnings:
        print("\nwarnings:")
        for warning in warnings:
            print(f"  - {warning}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
