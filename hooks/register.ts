import type { EngineInterface, Register } from 'claude-code'

const HELP = `Brigade: the head chef (this session) writes recipes and decides; cooks do the work.
  /brigade:init [project]       set up a kitchen: KITCHEN.md, RUNBOOK.md, work/gates.md, work/recipes/00-template.md
  /brigade:recipe <task>        the head chef writes work/recipes/NN-<name>.md and picks its cook
  /brigade:cook <NN> [notes]    a Sonnet cook (brigade:cook) cooks recipe NN: code, tests, one commit per item
  /brigade:prep <NN> [notes]    a Haiku prep cook (brigade:prep) runs recipe NN: exact commands, short report
Cooks run in the background; the status line shows who is on the stove.
Rules for the cooks live in KITCHEN.md, decisions in work/gates.md, the recipe list in RUNBOOK.md.`

const ROLES: Record<string, string> = { 'brigade:cook': 'cook', 'brigade:prep': 'prep' }

// agentId -> what the status line shows for it ("cook 05")
const stove = new Map<string, string>()

function show($: EngineInterface) {
  $.ui.status(stove.size ? `brigade: ${[...stove.values()].join(' · ')}` : undefined)
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'brigade', description: 'How the brigade kitchen works' })
    show($)
    return next(e)
  })

  on('command.run', { command: 'brigade' }, async () => ({ text: HELP }))

  on('agent.spawn', async ($, e, next) => {
    const started = await next(e)
    const role = ROLES[e.subagentType]
    if (role && started.deny === undefined && started.agentId) {
      // the dispatch commands describe the task as "recipe NN: ..."
      const recipe = /\b(\d{2}[a-z]?)\b/.exec(e.description)?.[1]
      stove.set(started.agentId, recipe ? `${role} ${recipe}` : role)
      show($)
    }
    return started
  }).catch(($, e, next) => next(e)) // bookkeeping never blocks a spawn

  on('turn.complete', ($, e, next) => {
    if (e.agentId && stove.delete(e.agentId)) show($)
    return next(e)
  })
}
