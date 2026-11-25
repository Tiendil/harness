## Writing tests

When you implement or change tests, you MUST treat the code under test as untrusted, including the logic it encodes.

When you implement or change tests, you MUST check for changes in the code under test and review any changes you find.

If you doubt the correctness of the code under test, you MUST consult other agents, the developer, or both to clarify the expected behavior of that code.

Before adapting tests to a change in the code under test, you MUST assess how the change affects behavior.
If existing behavior breaks, you SHOULD verify whether a change in requirements calls for the observed behavior and whether a bug in the code under test caused the break.
