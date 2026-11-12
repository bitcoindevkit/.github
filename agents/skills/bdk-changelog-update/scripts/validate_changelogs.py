#!/usr/bin/env python3
"""Validate rewritten release sections.

Checks, per crate:
  * preamble and everything below the release section are unchanged from HEAD,
  * the compare URL points at bitcoindevkit/bdk,
  * section headings are non-empty and in the order Added/Changed/Fixed/Removed,
  * bullets have balanced parentheses and backticks,
  * every link targets bitcoindevkit/bdk pull/commit pages,
  * no fork links or trailing whitespace.

Exits non-zero when any error is found.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

COMPARE_RE = re.compile(
    r"^## \[(?P<version>[^\]]+)\]"
    r"\((?P<url>https://github\.com/(?P<repo>[^/]+/[^/]+)/compare/"
    r"(?P<prev>.+?)\.\.\.(?P<new>.+?))\)"
)
LINK_RE = re.compile(r"\]\((https://github\.com/[^)\s]+)\)")
ORDER = ["### Added", "### Changed", "### Fixed", "### Removed"]


def git_show(root: Path, rel: str) -> str | None:
    proc = subprocess.run(
        ["git", "show", f"HEAD:{rel}"], cwd=root, text=True, capture_output=True
    )
    return proc.stdout if proc.returncode == 0 else None


def first_heading(lines: list[str]) -> int:
    for index, line in enumerate(lines):
        if line.startswith("## "):
            return index
    return len(lines)


def section_bounds(lines: list[str], start: int | None = None) -> tuple[int, int]:
    if start is None:
        start = next(
            (i for i, line in enumerate(lines) if COMPARE_RE.match(line)), None
        )
        if start is None:
            raise ValueError("no release heading with a compare URL")
    end = next(
        (i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")),
        len(lines),
    )
    return start, end


def validate_section(lines: list[str], start: int, end: int) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    section = lines[start:end]

    heading = section[0]
    match = COMPARE_RE.match(heading)
    if match and match.group("repo") != "bitcoindevkit/bdk":
        errors.append(f"compare URL uses {match.group('repo')}, expected bitcoindevkit/bdk")
    if not match:
        errors.append("release heading has no valid compare URL")

    heading_positions = []
    for index, line in enumerate(section):
        if line.startswith("### "):
            heading_positions.append(index)
            nxt = next(
                (i for i in range(index + 1, len(section)) if section[i].startswith("### ")),
                len(section),
            )
            if not any(l.startswith("- ") for l in section[index + 1 : nxt]):
                errors.append(f"empty section: {line}")
            if line not in ORDER:
                warnings.append(f"unexpected section heading: {line}")

    ordered = [section[i] for i in heading_positions]
    expected = [h for h in ORDER if h in ordered]
    if ordered != expected:
        errors.append(f"section order is {ordered}, expected {expected}")

    bullets = [line for line in section if line.startswith("- ")]
    if not bullets:
        errors.append("release section has no bullets")

    for line in section:
        if line != line.rstrip():
            errors.append(f"trailing whitespace: {line[:60]!r}")
        if "\t" in line:
            errors.append(f"tab character: {line[:60]!r}")
        if "notmandatory" in line:
            errors.append(f"fork link: {line[:80]}")
        if line.startswith("- "):
            if line.count("(") != line.count(")"):
                errors.append(f"unbalanced parentheses: {line[:80]}")
            if line.count("`") % 2:
                errors.append(f"unbalanced backticks: {line[:80]}")
            urls = LINK_RE.findall(line)
            if not urls:
                warnings.append(f"bullet has no link: {line[:80]}")
            for url in urls:
                if not re.match(
                    r"https://github\.com/bitcoindevkit/bdk/(pull|commit)/", url
                ):
                    errors.append(f"unexpected link target: {url}")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument(
        "--context",
        default="/tmp/opencode/bdk-changelog/context.json",
        help="context.json from inspect_workspace.py",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="validate every changelog, not only those flagged needs_update",
    )
    args = parser.parse_args()

    root = Path(
        subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=Path(args.root).resolve(),
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
    )

    entries: list[dict] = []
    context_path = Path(args.context)
    if context_path.exists():
        context = json.loads(context_path.read_text())
        entries = [
            e
            for e in context["crates"]
            if args.all or e.get("needs_update", True)
        ]
    else:
        for changelog in sorted(root.glob("crates/*/CHANGELOG.md")):
            entries.append({"changelog": str(changelog.relative_to(root))})

    failures = 0
    for entry in entries:
        rel = entry["changelog"]
        changelog = root / rel
        if not changelog.exists():
            print(f"FAIL {rel}: file not found")
            failures += 1
            continue

        current_text = changelog.read_text()
        current = current_text.splitlines()
        head_text = git_show(root, rel)

        errors: list[str] = []
        warnings: list[str] = []

        try:
            start, end = section_bounds(current)
        except ValueError as exc:
            print(f"FAIL {rel}: {exc}")
            failures += 1
            continue

        section_errors, section_warnings = validate_section(current, start, end)
        errors.extend(section_errors)
        warnings.extend(section_warnings)

        if head_text is None:
            warnings.append("file is not in HEAD; skipped integrity check")
        else:
            head = head_text.splitlines()
            if current[: first_heading(current)] != head[: first_heading(head)]:
                errors.append("preamble differs from HEAD")

            if end < len(current):
                marker = current[end]
                try:
                    head_end = head.index(marker)
                except ValueError:
                    errors.append(f"tail marker not found in HEAD: {marker}")
                else:
                    if current[end:] != head[head_end:]:
                        errors.append(f"content below {marker!r} differs from HEAD")

        if errors:
            failures += 1
            print(f"FAIL {rel}")
            for error in errors:
                print(f"  error: {error}")
        else:
            print(f"PASS {rel} ({sum(1 for l in current[start:end] if l.startswith('- '))} bullets)")
        for warning in warnings:
            print(f"  warn: {warning}")

    print()
    if failures:
        print(f"{failures} changelog(s) failed validation")
        return 1
    print("all changelogs passed validation")
    return 0


if __name__ == "__main__":
    sys.exit(main())
