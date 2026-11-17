
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
