### `mise`

Use mise to discover and run project tasks. Project tasks tagged `agent` are available to agents, subject to all other project instructions and task-specific restrictions.

You MUST ask the developer for permission before running any other mise task or directly invoking any project script.
Approved tasks and authorized workflows may run their configured scripts and child tasks; this does not authorize invoking those internals directly or bypassing this rule through a generic runner.
Adding the `agent` tag to any other task requires developer approval.

Run `mise tasks ls --no-global --hidden --tag agent` to inspect tagged task metadata.
Pass task arguments after `--`, for example `mise run <task> -- <arguments>`.

The following tasks are available to agents. This list includes task definitions within this repository and its vendored files:

<!-- [[[cog
import json
import shlex
import subprocess
from pathlib import Path

import cog

result = subprocess.run(
    ["mise", "tasks", "ls", "--json", "--no-global", "--hidden", "--tag", "agent"],
    check=True,
    capture_output=True,
    text=True,
)
project_root = Path.cwd().resolve()
tasks = [
    task
    for task in json.loads(result.stdout)
    if Path(task["source"]).resolve().is_relative_to(project_root)
]
for task in sorted(tasks, key=lambda task: task["name"]):
    command = shlex.join(["mise", "run", task["name"]])
    description = " ".join(task["description"].split())
    cog.outl(f"- `{command}` — {description}")
if not tasks:
    cog.outl("No mise tasks are tagged `agent` in this repository.")
]]] -->
<!-- [[[end]]] -->
