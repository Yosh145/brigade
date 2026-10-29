---
description: Dispatch a recipe to the brigade's cook (Sonnet)
argument-hint: "<NN> [notes for the cook]"
---

Dispatch a recipe to the cook. Arguments: `$ARGUMENTS` (the recipe number first, then any notes).

1. Find `work/recipes/<NN>-*.md` from the project root. If there is none, or more than one, stop and say so. If its title
   line says `(prep, haiku)`, say that it is a prep recipe and suggest `/brigade:prep <NN>` instead.
2. Call the Agent tool with:
   - `subagent_type: "brigade:cook"`, `run_in_background: true`;
   - `description: "recipe <NN>: <its title, a few words>"` (the status line shows `cook <NN>` from it);
   - `isolation: "worktree"` when another cook is running in the same repo (two cooks committing in one checkout
     collide); otherwise leave it out;
   - a prompt that gives: the recipe's absolute path; the project root; what the recipe can't know (each repo's HEAD
     commit, the current test counts, which other cooks are running and on what); the notes, if any; and "reply with the
     recipe's report only".
3. Tell the user in one line what is cooking, then end the turn. Don't wait or poll: the report arrives as a
   notification.
4. When the report arrives, review it as head chef: check its numbers against the recipe's "Done when", look at the
   commits' diffstat (not the diff), and write any new decision into `work/gates.md`. Tell the user in a few lines.
   A worktree cook's commits are on its own branch: say so and offer to merge them. A failure goes back to a cook with
   its log, at most three rounds; then take it to the user.
