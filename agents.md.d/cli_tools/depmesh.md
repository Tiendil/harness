
### `depmesh`

`depmesh` — a tool for discovering dependencies between project artifacts.

Agents MUST use `depmesh` to discover dependency types supported by its configuration.

The `governed_by` relation identifies the specifications that govern an artifact.
Agents MUST read each returned specification in full before making decisions about the artifact, reviewing it, or changing it.
Agents MUST follow the applicable requirements in those specifications.

At the start of each work session, read the `depmesh` usage instructions for details:

```bash
depmesh skill usage
```
