"""Record and check the source files used by a full harness apply."""

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
import tomllib
from enum import StrEnum
from pathlib import Path
from typing import Any, assert_never


class Mode(StrEnum):
    CHECK = "check"
    RECORD = "record"


FORMAT_VERSION = 1
LOCK_PATH = Path(".harness/version.lock")
APPLY_HINT = "Run mise run harness:initialize and commit the resulting harness changes."


def agent_task_sources(project_root: Path) -> set[Path]:
    result = subprocess.run(
        ["mise", "tasks", "ls", "--json", "--no-global", "--hidden", "--tag", "agent"],
        cwd=project_root,
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    )
    sources = set()
    for task in json.loads(result.stdout):
        source = Path(task["source"]).resolve()
        if source.is_relative_to(project_root):
            sources.add(source)
    return sources


def installed_sources(config: dict[str, Any], harness_root: Path) -> set[Path]:
    specifications = config.get("specifications", {}).get("specs", [])
    if "specifications" not in config:
        specifications = config.get("specs", [])
    sources = {harness_root / "specs" / name for name in specifications}
    workflows = config.get("workflows", {}).get("fragments", [])
    sources.update(harness_root / "workflows" / name for name in workflows)

    for name in config.get("skills", []):
        skill = harness_root / ".agents/skills" / name
        if skill.is_dir():
            sources.update(path for path in skill.rglob("*") if path.is_file())
        else:
            sources.add(skill)
    return sources


def source_hashes(project_root: Path, harness_root: Path) -> dict[str, str]:
    config_path = project_root / ".harness/config.toml"
    with config_path.open("rb") as config_file:
        config = tomllib.load(config_file)

    sources = {
        config_path,
        harness_root / ".harness/AGENTS.md.tera",
        harness_root / ".harness/codex/config.toml",
        project_root / ".harness/codex/config.toml",
    }
    agents_md = config["agents_md"]
    sources.update(project_root / name for name in agents_md["fragments"])
    sources.update(project_root / name for name in agents_md.get("embedded_specs", []))
    specifications_root = project_root / config.get("specifications", {}).get("root", "specs")
    sources.update(path for path in specifications_root.rglob("*.md") if path.is_file())

    for role in config.get("roles", {}).get("role", []):
        description = role["description"]
        if isinstance(description, dict):
            sources.add(project_root / description["file"])
        sources.update(project_root / name for name in role["fragments"])

    if harness_root != project_root:
        sources.update(installed_sources(config, harness_root))

    for name in ("mise.toml", ".miserc.toml"):
        path = project_root / name
        if path.is_file():
            sources.add(path)
    sources.update(agent_task_sources(project_root))

    hashes = {}
    for path in sorted(sources):
        name = path.relative_to(project_root).as_posix()
        with path.open("rb") as source_file:
            hashes[name] = hashlib.file_digest(source_file, "sha256").hexdigest()
    return hashes


def check_lock(lock_path: Path, current: dict[str, str]) -> int:
    try:
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ValueError(f"{LOCK_PATH} is missing. {APPLY_HINT}") from error

    if not isinstance(lock, dict) or lock.get("format_version") != FORMAT_VERSION:
        raise ValueError(f"Unsupported format in {LOCK_PATH}. {APPLY_HINT}")
    recorded = lock.get("files")
    if not isinstance(recorded, dict) or not all(isinstance(digest, str) for digest in recorded.values()):
        raise ValueError(f"Invalid file hashes in {LOCK_PATH}. {APPLY_HINT}")

    if current == recorded:
        print(f"{LOCK_PATH} matches {len(current)} harness sources.")
        return 0

    print(f"Harness sources differ from {LOCK_PATH}:", file=sys.stderr)
    for name in sorted(current.keys() - recorded.keys()):
        print(f"  Added: {name}", file=sys.stderr)
    for name in sorted(recorded.keys() - current.keys()):
        print(f"  Removed: {name}", file=sys.stderr)
    for name in sorted(current.keys() & recorded.keys()):
        if current[name] != recorded[name]:
            print(f"  Changed: {name}", file=sys.stderr)
    print(APPLY_HINT, file=sys.stderr)
    return 1


def record_lock(lock_path: Path, hashes: dict[str, str]) -> None:
    lock = {"format_version": FORMAT_VERSION, "files": hashes}
    content = json.dumps(lock, indent=2, sort_keys=True) + "\n"
    with tempfile.NamedTemporaryFile(dir=lock_path.parent, mode="w", encoding="utf-8", delete=False) as output:
        temporary = Path(output.name)
        try:
            output.write(content)
            output.close()
            temporary.replace(lock_path)
        finally:
            temporary.unlink(missing_ok=True)
    print(f"Recorded {len(hashes)} harness sources in {LOCK_PATH}.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", type=Mode, choices=list(Mode))
    mode: Mode = parser.parse_args().mode

    project_root = Path.cwd()
    harness_root = Path(__file__).resolve().parents[1]
    lock_path = project_root / LOCK_PATH
    hashes = source_hashes(project_root, harness_root)
    match mode:
        case Mode.CHECK:
            return check_lock(lock_path, hashes)
        case Mode.RECORD:
            record_lock(lock_path, hashes)
            return 0
    assert_never(mode)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (KeyError, OSError, TypeError, ValueError, subprocess.CalledProcessError) as error:
        sys.exit(f"Could not process {LOCK_PATH}: {error}")
