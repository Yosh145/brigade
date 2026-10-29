---
description: Dispatch a recipe to the brigade's prep cook (Haiku)
argument-hint: "<NN> [notes for the prep cook]"
---

Dispatch a recipe to the prep cook. Arguments: `$ARGUMENTS` (the recipe number first, then any notes).

1. Find `work/recipes/<NN>-*.md` from the project root. If there is none, or more than one, stop and say so. If its title
   line says `(cook, sonnet)`, say that it needs judgment and suggest `/brigade:cook <NN>` instead.
2. Call the Agent tool with:
   - `subagent_type: "brigade:prep"`, `run_in_background: true` (the agent sets its own low effort; pass none);
   - `description: "recipe <NN>: <its title, a few words>"` (the status line shows `prep <NN>` from it);
   - a prompt that gives: the recipe's absolute path; the project root; what the recipe can't know (each repo's HEAD
     commit, the current test counts, which cooks are running and on what); the notes, if any; and "reply with the
     recipe's report only".
3. Tell the user in one line what is cooking, then end the turn. Don't wait or poll: the report arrives as a
   notification.
4. When the report arrives, review it as head chef: every step done, and the numbers against the recipe's "Done when".
   A failed step is not fixed by the prep cook: decide whether it goes to a cook (with the log the report names, at most
   three rounds) or to the user. Write any new decision into `work/gates.md`, and tell the user in a few lines.
