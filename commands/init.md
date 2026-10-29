---
description: Set up a brigade kitchen in this project (KITCHEN.md, RUNBOOK.md, work/gates.md, work/recipes/)
argument-hint: "[what this project's work is]"
---

Set up a brigade kitchen in the current project. The project's work: $ARGUMENTS

Never overwrite: a file that exists is kept and reported. Fill the `<…>` placeholders from what you can find out (the
project's CLAUDE.md, README, build files, git repos), and ask the user only for what you can't. Then show the user
KITCHEN.md's hard rules and ask them to confirm or correct them: the cooks will obey them over anything else.

### `KITCHEN.md`

```markdown
# Kitchen rules

Every cook reads this first. These rules bind over anything a recipe or another file says.

## Hard rules
- Never write to: <installed apps, inputs, other projects, system folders>.
- Read only: <inputs, upstream releases, earlier versions>.
- Commits go only into: <repos>, one per recipe item, ending with: <the attribution line>.
- <line endings, formatting, generated files that must not be hand-edited>

## Commands
- Build: <command>
- Test: <command>
- Check: <command>

## Scratch
Large output and logs go in <folder inside the project>, never in /tmp.
```

### `RUNBOOK.md`

```markdown
# Runbook

## Who does what

| Role | Who | Does |
|---|---|---|
| Head chef | the main session | Writes recipes and decides gates; reviews short reports, diffstats and report tools, not file dumps. Does not cut vegetables |
| Sous chef | `brigade:cook` (Sonnet) | One recipe: code with tests, one commit per item, a report of 20 lines or fewer |
| Prep cook | `brigade:prep` (Haiku) | Exact commands, builds, checks, log summaries, a report of 15 lines or fewer; stops at judgment calls |

## The recipes (`work/recipes/`)

| # | Recipe | Who | Next time |
|---|---|---|---|

## The next round, step by step

(Filled in as recipes prove reusable.)
```

### `work/gates.md`

```markdown
# Gates: the head chef's decisions

| Gate | Fact | Decision | Feeds |
|---|---|---|---|
```

### `work/recipes/00-template.md`

```markdown
# Recipe NN: <title> (prep, haiku | cook, sonnet)

Reruns as is | Template: <what to change next time> | One-off.

## Goal
<one or two sentences: the state of things when this is done>

## Inputs
<files, repos, commits, earlier reports>

## Steps
<prep: exact commands, in order, each with what it should print>
<cook: the hook points, the rules, the decisions already made in work/gates.md>

## Done when
<tests passing (counts), numbers expected, files written>

## Report
At most <15 | 20> lines: <the numbers, commits, paths and questions wanted>. Details go into <file>.

## Out of scope
<what not to touch, even if it looks wrong>
```
