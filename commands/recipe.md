---
description: Head chef writes a recipe in work/recipes/ for a cook or a prep cook
argument-hint: "<task>"
---

As head chef, write a recipe for: $ARGUMENTS

1. Read `KITCHEN.md`, `work/gates.md`, `RUNBOOK.md` and `work/recipes/00-template.md`. If they are missing, say so and
   suggest `/brigade:init`. Name the file `work/recipes/NN-<short-name>.md`, NN the next free two-digit number (a
   follow-up to recipe 03 may be `03b`).
2. Find out what the cook will need before writing: read the code the task touches, enough to name the files, the hook
   points and the expected numbers. A recipe written blind passes the thinking to a cheaper model.
3. Pick the cook honestly:
   - **prep (Haiku)** only if every step is an exact command with a result that checks itself;
   - **cook (Sonnet)** for code, investigation, or anything that needs reading and adapting;
   - the head chef keeps the gate decisions and the reviews.

   Split a task that mixes the two into two recipes.
4. Fill the template. Every decision goes in the recipe (hook points, rules, expected numbers, what "done" means): a cook
   must never have to choose between designs. Name the files where details go, so the report stays short.
5. Mark whether it reruns as is, is a template, or is a one-off, and add a row to RUNBOOK.md's recipe table.
6. Show the user the recipe's path, goal and cook in two or three lines. Don't dispatch it unless asked
   (`/brigade:cook NN` or `/brigade:prep NN`).
