
# Instructions for the AI Agents

This document provides instructions and guidelines for the AI agents working on this project.

Every agent MUST follow the rules and guidelines outlined in this document when performing their work.

## Primary agent

The primary agent runs the main session for the developer's overall task.
The primary agent MUST follow the rest of this section.
All other agents MUST skip the rest of this section and follow their assigned role and task.

The primary agent is responsible for completing the overall task.
The primary agent MUST coordinate the work of all other agents on the task.
The primary agent MUST handle communication with the developer.

The primary agent MUST use sub-agents for independent work when delegation would improve speed or quality.

The primary agent SHOULD make project changes directly unless one of the following applies.

- Another agent explicitly takes responsibility for the part of the task that requires the changes.
- The applicable specifications require the primary agent to delegate the changes.
- The developer explicitly instructs the primary agent to delegate the changes.

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

## Principles

You MUST follow principles defined in these sections for every related task you perform.

### Fundamentals

These principles are your primary guide doing ALL tasks.

- KISS (Keep It Simple, Stupid) principles.
- DRY (Don't Repeat Yourself) principles.
- YAGNI (You Aren't Gonna Need It) principles.
- SOLID (Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, Dependency Inversion) principles.
- HCD (Human-Centered Design) principles — place the human user at the center of the design process, ensuring that the system is usable, accessible, and meets the needs of its intended audience.
- DCD (Developer-Centered Design) principles — place the developer at the center of the design process, ensuring that the system is maintainable, extensible, and meets the needs of its intended developers.

### Design

These principles are your primary guide for making design decisions.

- Start with the smallest design that satisfies the current explicit requirements and preserves existing behavior. Do not design for hypothetical future requirements.
- Every proposed abstraction, entity, persisted value, workflow, etc. must serve a current requirement and have a current consumer. If removing it does not break required behavior or an existing invariant, omit it.
- Prefer one source of truth. Derive information when it is unambiguous, and do not duplicate facts for convenience, symmetry, debugging, auditability, or possible future use unless explicitly required.
- Before presenting or implementing a design, perform a subtraction pass: try removing each newly introduced concept and keep it only when its absence causes a concrete problem.
- Consider corner cases only when they follow from current requirements, existing behavior, or observed data and materially affect the design. Defer speculative cases instead of building for them.
- When several approaches satisfy the requirements, recommend the less complicated one (with fewer concepts, states, exectution paths, etc.). Present additional flexibility only as an optional extension.

### Implementation

These principles are your primary guide for making implementation decisions.

- You MUST follow Simplicity-first principles.
- Simplicity does not mean merging unrelated interfaces at any cost. Do not combine APIs when doing so introduces mutually exclusive optional arguments, invalid states, pervasive runtime branching, etc.

## Behavior

You MUST adjust your behavior according to rules in these sections.

### Reaction on the developer commands

When processing developer commands, you MUST follow these rules:

- When the developer asks you a question — answer it as a question. Do not implement the answer as a code change or a plan, just answer the question.

### Ask the developer when

You MUST ask an explicit question to the developer when:

- You want or need to perform one of restricted operations.
- You are choosing between multiple options with significant consequences and have no instructions on fully autonomous decision-making.
- You encounter / discover a fact that critically changes the context/requirements/outcome of your current task.

When you are asking the developer, you MUST provide:

- A clear description of the operation you want to perform.
- A clear explanation of why you want to perform the operation.
- A clear explanation of the potential consequences of performing the operation.

### Working with text artifacts

For the needs of this section, text artifacts are any text-based files, including but not limited to source code, configuration files, specification files, and documentation.

You may use grep-like/search/specialized tools to discover relevant text artifacts files.
Search results MUST be treated only as discovery hints.

#### Reading and reusing content

You MUST read text artifacts in full from beginning to end before relying on, interpreting, reviewing, or changing them.
A complete copy of a text artifact already available in the active context satisfies this requirement.

You MUST reuse previously read content while it remains available and current.
You MUST NOT reread an artifact merely because a new turn or work phase begins.

Unless explicitly told otherwise, you MUST assume you are the only active editor of text artifacts.
You MUST NOT reread artifacts or perform freshness checks merely to guard against hypothetical concurrent edits.

Reread only when the required content is no longer available, there is concrete evidence of an intervening change, or the developer or an active workflow explicitly requires a fresh read.

You MUST NOT use partial-file reading methods (such as `sed`, `head`, `tail`, line-range readers, grep context output, etc.) to read text artifacts.

If a whole-file read is truncated, you MUST repeat it with sufficient output capacity and MUST NOT proceed until the complete file has been read.

Special exceptions to the above rules are:

- You may skip reading each file when bulk editing of particular parts of text artifacts (replacing a particular string in all source files, renaming a particular function, etc.).

### Introducing changes

You MUST distinguish implementation from final validation.

- **Implementation:** the planned changes are still in progress. Use focused checks permitted by the project to guide the work.
- **Final validation:** the planned changes are complete and ready for review. Perform the final validation required by the project before reporting completion.

Final validation may require corrections. Make those corrections and repeat the validation required by the project or active workflow for the resulting state.

Task permissions do not override the project's rules about when to run a task.

You MUST NOT report work as complete while required validation has failed or remains incomplete. Report any validation that could not be completed.

### Resticted operations

You ABSOLUTELY MUST NOT perform the following operations without explicit instructions to do so.

#### Project restrictions

You MUST NOT perform the following operations without explicit instructions to do so:

- Changing project structure, such as moving files around, creating new directories, etc.

#### Dependencies restrictions

You MUST NOT perform the following operations without explicit instructions to do so:

- Installing any new dependencies for any part of the project.
- Updating any kind of lock files.
- Installing any new tools, utilities, or software on the host machine or in the development containers.

#### Docker restrictions

You MUST NOT perform the following operations without explicit instructions to do so:

- Changing `docker-compose.yml`, Dockerfiles or any image-/container-related configuration files.
- Changing Docker service runtime parameters (such as allocated resources, volumes, etc.).
- Changing running Docker services related to other projects or unrelated to the current environment.

#### Git restrictions

You MUST NOT perform the following operations without explicit instructions to do so:

- Staging or unstaging files in git, including commands such as `git add`, `git restore --staged`, and `git reset`.
- Changing git configuration.

## Specifications

This index lists the available specifications and their goals.

- `specs/documentation/changelog.md` — requirements for changelog documentation.
- `specs/meta/content.md` — requirements for the level of detail in specification contracts.
- `specs/meta/dictionary.md` — conventions for project-level dictionaries and shared project terminology.
- `specs/meta/directories.md` — conventions for organizing specification files into subject areas.
- `specs/meta/format.md` — the structure and style conventions for specifications in this project.
- `specs/meta/language.md` — language conventions for specifications and for written communication among agents and with the developer.
- `specs/programming/code.md` — conventions for program implementations.
- `specs/programming/content.md` — content requirements for programming specifications.
- `specs/programming/dto.md` — the responsibilities and ownership of data transfer objects in a DTO-centric architecture.
- `specs/programming/modules_and_roles.md` — how projects organize source files and code elements by module and role.
- `specs/programming/postgresql.md` — conventions for relational schema design and SQL in PostgreSQL.
- `specs/programming/tests.md` — conventions for organizing automated software tests and verifying program behavior.
- `specs/python/language.md` — language-level implementation conventions for Python source code.
- `specs/python/libs/pydantic.dto_foundation.md` — how projects use a shared Pydantic base class for their DTOs.
- `specs/python/libs/pydantic.md` — conventions for defining and using Pydantic models.
- `specs/python/libs/pytest.md` — conventions for writing Python tests with pytest.
- `specs/python/tests.md` — conventions for writing and organizing Python tests.
- `specs/typescript/libs/vitest.md` — conventions for writing tests with Vitest.
- `specs/typescript/tests.md` — naming conventions for TypeScript tests.

## CLI Tools

These CLI tools MUST have the highest priority when an agent is deciding which tool to use for a given task.

You MUST run all listed tools on the host machine unless explicitly instructed to run them in other ways (in a Docker container, in a virtual environment, etc.).

### `mise`

Use mise to discover and run project tasks. Project tasks tagged `agent` are available to agents, subject to all other project instructions and task-specific restrictions.

You MUST ask the developer for permission before running any other mise task or directly invoking any project script.
Approved tasks and authorized workflows may run their configured scripts and child tasks; this does not authorize invoking those internals directly or bypassing this rule through a generic runner.
Adding the `agent` tag to any other task requires developer approval.

Run `mise tasks ls --no-global --hidden --tag agent` to inspect tagged task metadata.
Pass task arguments after `--`, for example `mise run <task> -- <arguments>`.

The following tasks are available to agents. This list includes task definitions within this repository and its vendored files:

- `mise run harness:agents.md:generate` — Regenerate AGENTS.md
- `mise run harness:generate` — Regenerate harness
- `mise run harness:load` — Update shared harness
- `mise run harness:skills:install` — Install shared harness skills
- `mise run harness:specs:install` — Install selected shared harness specifications

### `donna`

Use Donna to run project-local deterministic workflows.

Run Donna workflows only when explicitly instructed to do so by the developer or by the project instructions.
Do not run workflows on your own initiative.

When you run Donna workflows: Donna controls workflow state and execution flow, you follow the instructions provided by Donna.

Run `donna -p llm skill usage` when:

- You run a workflow first time in the session.
- You need to create a new workflow or modify an existing workflow.
- You need to perform an operation that is not covered by instructions.

Run `donna -p llm new-session` when the developer explicitly instructs you to start a new **Donna** session.

Here is a list of available workflows.

No Donna workflows are configured for this repository.

### `depmesh`

`depmesh` — a tool for discovering dependencies between project artifacts.

Agents MUST use `depmesh` to discover dependency types supported by its configuration.

At the start of each work session, read the `depmesh` usage instructions for details:

```bash
depmesh skill usage
```

### `ast-grep`

`ast-grep` — a tool for searching and manipulating Abstract Syntax Trees in code. Use it when you work with particular code patterns, structures, or constructs in the codebase.

You MUST use it to:

- Search for specific code patterns or structures in the codebase.
- Extract information from code, such as function definitions, variable declarations, or specific code constructs.
- Analyze code for specific patterns or anti-patterns, such as code smells, security vulnerabilities, performance issues, specific usage of libraries or APIs, etc.
- Refactor particular code patterns or structures across the codebase.
- Introduce new small behaviors or features into existing code.

You MUST NOT use it for:

- Implementing huge features or behaviors that require adding massive blocks of code (like adding a new class, module, writing a huge function, etc.).

### `rg`

Use `rg` for text and file searches.

`ast-grep` has a higher priority than `rg` whenever a structural code query is needed.

### `difftastic`

Use `difft` as the default tool for inspecting code changes and whenever a semantic, syntax-aware diff is useful. Prefer stable, agent-readable output:

```bash
difft --display=inline --color=never --context=6 OLD-PATH NEW-PATH
difft --display=inline --color=never --context=6 --sort-paths OLD-DIR NEW-DIR
GIT_EXTERNAL_DIFF="difft --display=inline --color=never --context=6" git --no-pager diff -- PATH
GIT_EXTERNAL_DIFF="difft --display=inline --color=never --context=6" git --no-pager diff --cached -- PATH
```

Use a classic line-oriented diff, such as `git --no-pager diff --no-ext-diff` or `diff -u`, only when the task explicitly requires raw line-by-line output—for example, producing a patch, inspecting exact whitespace or line endings, or supplying unified-diff input to another tool. Do not choose a classic diff merely because a change is small or limited to text.
