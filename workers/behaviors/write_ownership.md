## Write ownership

Agents MAY read any repository file.
Agents without the write baton MUST use read-only access and run only read-only commands, except as needed to create or update their own task-local temporary files.

Any agent MAY create and update its own task-local temporary files under `.session/`, such as research reports.
Commands run under this exception MUST limit writes to those files and the directories needed to create them.

The agent responsible for completing the overall task (for example, the `default` or `primary` agent, depending on the harness) starts with the write baton.
Only one agent MAY hold the baton at a time.
The holder MAY make repository changes within the applicable project rules.

The holder MAY delegate the write baton to another agent.
Before transferring the baton, the holder MUST finish or stop any running commands that can still make changes requiring the baton.
On transfer, the sender MUST switch to read-only mode and the recipient becomes the holder.

An agent that receives the baton by delegation MUST return it to the agent that delegated it as soon as the work requiring write access ends.
