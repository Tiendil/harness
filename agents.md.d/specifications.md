## Specifications

This index lists the available specifications and their goals.

<!-- [[[cog
import re
import tomllib
from pathlib import Path

import cog

with Path(".harness/config.toml").open("rb") as config_file:
    harness_config = tomllib.load(config_file)
goal_prefixes_to_remove = harness_config["agents_md"]["index_goal_prefixes_to_remove"]

for spec_path in sorted(Path("specs").rglob("*.md"), key=Path.as_posix):
    if not spec_path.is_file():
        continue

    goal_lines = None
    fence = None
    for line in spec_path.read_text(encoding="utf-8").splitlines():
        if fence is not None:
            if re.fullmatch(rf" {{0,3}}{re.escape(fence[0])}{{{len(fence)},}}[ \t]*", line):
                fence = None
        else:
            opening_fence = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
            heading = re.match(r"^ {0,3}(#{1,6})[ \t]+(.*?)(?:[ \t]+#+)?[ \t]*$", line)
            if opening_fence:
                fence = opening_fence.group(1)
            elif heading and len(heading.group(1)) <= 2:
                if goal_lines is not None:
                    break
                if heading.group(1) == "##" and heading.group(2) == "Goal of the document":
                    goal_lines = []
                continue
        if goal_lines is not None:
            goal_lines.append(line)

    goal = " ".join(line.strip() for line in goal_lines or [] if line.strip())
    if not goal:
        raise ValueError(f"{spec_path}: missing or empty 'Goal of the document' section")
    for prefix in sorted(goal_prefixes_to_remove, key=len, reverse=True):
        if goal.startswith(prefix):
            goal = goal.removeprefix(prefix)
            break
    cog.outl(f"- `{spec_path.as_posix()}` — {goal}")
]]] -->
<!-- [[[end]]] -->
