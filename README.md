![brigade: a wireframe chef's toque beside the roles of the kitchen: head chef (Opus), cook (Sonnet), prep (Haiku)](docs/header.png)

# brigade

A model-routing kitchen for multi-agent work in Claude Code. The main session is the **head chef**: it writes recipes (task
briefs in `work/recipes/`), decides gates (`work/gates.md`) and reviews short reports.

Basically, "lower effort" models get delegated to lower effort tasks, where higher level details get delegated to higher effort models.

- `brigade:cook` (Sonnet) cooks one recipe: code with tests, one commit per item, a report of 20 lines or fewer.
- `brigade:prep` (Haiku, low effort) runs exact commands (setup, builds, checks, log summaries) and stops at judgment calls.

## Commands

- `/brigade:init [project]`: writes `KITCHEN.md` (the hard rules every cook reads first), `RUNBOOK.md`, `work/gates.md`
  and `work/recipes/00-template.md`, never overwriting, and asks you to confirm the hard rules.
- `/brigade:recipe <task>`: the head chef reads the code, writes the next recipe and picks its cook honestly.
- `/brigade:cook <NN> [notes]` and `/brigade:prep <NN> [notes]`: dispatch recipe NN in the background; the head chef
  reviews the report when it arrives. A second cook in the same repo gets its own worktree.
- `/brigade`: a short help.

While cooks run, the status line shows who is on the stove (`brigade: cook 05 · prep 10`).

## Hooks

The mod has one hooks module, `hooks/register.ts`, with four hooks. None of them reads files, credentials or environment
variables, sends data anywhere, or blocks or rewrites anything Claude Code does. The agents (`agents/*.md`) and commands
(`commands/*.md`) are plain markdown prompts.

**`session.start`**
- What the hook does: registers the `/brigade` help command when a session starts.
- What the hook changes: adds `/brigade` to the session's slash commands. Nothing else.

**`command.run`** (only for `/brigade`)
- What the hook does: answers `/brigade` with a short help text.
- What the hook changes: nothing. Other commands never reach it.

**`agent.spawn`**
- What the hook does: when a `brigade:cook` or `brigade:prep` agent starts, notes the agent's id and the recipe number from
  its description, in memory.
- What the hook changes: only the mod's own status line (`brigade: cook 05 · prep 10`). Every spawn, brigade's and every
  other, is passed on unchanged, and an error in this hook never stops one.

**`turn.complete`**
- What the hook does: when an agent it noted finishes, forgets it.
- What the hook changes: only the mod's own status line, cleared when no cook is left. Every turn's answer is passed on
  unchanged.

## Install

At the prompt of a Claude Code terminal session:

```
/plugin install brigade --marketplace Yosh145/brigade
```

Answer `y` to add the marketplace, then pick a scope. From a shell: `claude plugin install brigade --marketplace Yosh145/brigade`.
In the desktop app: click + next to the prompt box, then Plugins, Add marketplace with `Yosh145/brigade`, then Add plugin.

MIT licensed.
