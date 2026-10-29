# Privacy policy

brigade is a Claude Code plugin that runs entirely on your own computer. Its author collects no data of any kind.

- **No collection.** The plugin has no server, no analytics and no telemetry. Nothing you do with it is sent to the author or
  to anyone else.
- **What the hooks module keeps.** While a session runs, it keeps the ids of the brigade agents that are working and their
  recipe numbers, in memory, to show the status line. It forgets them when each agent finishes or the session ends. It
  writes nothing to disk and reads no files, credentials or environment variables.
- **The agents.** `brigade:cook` and `brigade:prep` are Claude Code subagents. They run on your own Claude account, like any
  other subagent, and what they send to Claude is handled under Anthropic's terms and privacy policy, not by this plugin.
- **Files it writes.** `/brigade:init` and `/brigade:recipe` ask Claude to write `KITCHEN.md`, `RUNBOOK.md`, `work/gates.md`
  and `work/recipes/*.md` in your own project. They stay there.

Questions: open an issue at https://github.com/Yosh145/brigade/issues.
