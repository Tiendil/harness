## Subagents

The primary agent runs the main session for the developer's overall task and is session-scoped.
An agent that spawns a subagent MUST choose the subagent's lifetime and state that choice in the initial assignment.
The spawning agent SHOULD use the scope recommended in the subagent's role description.
If the role description gives no recommendation, the spawning agent SHOULD use subtask scope.

### Lifetimes

- `Session` — The subagent stays available for related assignments until the main session ends.
  The primary agent SHOULD spawn it when first needed and reuse its thread for later assignments that benefit from its context.
- `Subtask` — The subagent handles one assignment and its follow-ups.
  Once the subagent delivers its result and returns any delegated write baton, the spawning agent MUST close the thread if a tool is available to close it.

### Runtime names

The spawning agent MUST use the format for the chosen scope.

- `Session` — `session__<role>`.
- `Subtask` — `subtask__<role>__<task>`.

Use the selected role name for `<role>` and a short description of the assigned work for `<task>`.
Use lowercase ASCII letters, digits, and single underscores within each field.

In Codex, pass the name as a single `task_name` segment when the spawn tool accepts it.
Use the returned path for messages, such as `/root/session__qa_automation` or `/root/subtask__reviewer_technical__subscription_cli` for direct children of the primary agent.
If the spawn tool supplies only an agent ID for addressing, include the name as a label in the initial assignment and use that ID for messages.
