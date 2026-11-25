#!/usr/bin/env python3
"""Validate AGENTS.md fragment selections from the current repository root."""

import sys
import tomllib
from collections import Counter
from pathlib import Path

FRAGMENT_ROOTS = (
    Path("agents.md.d"),
    Path(".harness/agents.md.d"),
    Path(".vendor/shared-harness/agents.md.d"),
)


def fail(errors: list[str]) -> int:
    print("AGENTS.md fragment validation failed:", file=sys.stderr)
    for error in errors:
        print(f"\n{error}", file=sys.stderr)
    return 1


def main() -> int:
    config_path = Path(".harness/config.toml")
    try:
        with config_path.open("rb") as config_file:
            config = tomllib.load(config_file)
    except (OSError, tomllib.TOMLDecodeError) as error:
        return fail([f"Cannot read {config_path}: {error}"])

    agents_md = config.get("agents_md")
    if not isinstance(agents_md, dict):
        return fail([f"{config_path} must contain an [agents_md] table."])

    selections: dict[str, list[str]] = {}
    errors: list[str] = []
    for field in ("fragments", "skipped_fragments"):
        values = agents_md.get(field)
        if not isinstance(values, list) or any(not isinstance(value, str) for value in values):
            errors.append(f"agents_md.{field} must be an array of fragment paths.")
        else:
            selections[field] = [Path(value).as_posix() for value in values]
    if errors:
        return fail(errors)

    for field, paths in selections.items():
        duplicates = sorted(path for path, count in Counter(paths).items() if count > 1)
        if duplicates:
            errors.append(f"Duplicate entries in agents_md.{field}:\n" + "\n".join(f"- {path}" for path in duplicates))

    accessible = {
        path.as_posix()
        for directory in FRAGMENT_ROOTS
        for path in directory.rglob("*.md")
        if path.is_file()
    }
    included = set(selections["fragments"])
    skipped = set(selections["skipped_fragments"])

    overlap = sorted(included & skipped)
    if overlap:
        errors.append("Fragments cannot be both included and skipped:\n" + "\n".join(f"- {path}" for path in overlap))

    unavailable = sorted((included | skipped) - accessible)
    if unavailable:
        errors.append(
            "Configured paths are not accessible Markdown fragments under the fragment roots:\n"
            + "\n".join(f"- {path}" for path in unavailable)
            + "\nFragment roots: "
            + ", ".join(str(directory) for directory in FRAGMENT_ROOTS)
        )

    undecided = sorted(accessible - included - skipped)
    if undecided:
        errors.append(
            "Unclassified fragments require a developer decision:\n"
            + "\n".join(f"- {path}" for path in undecided)
            + "\nAsk the developer whether each path belongs in agents_md.fragments or "
            "agents_md.skipped_fragments. Do not classify new fragments automatically."
        )

    if errors:
        return fail(errors)

    print(f"Validated {len(included)} included and {len(skipped)} skipped AGENTS.md fragments.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
