import { expect, test } from 'claude-code/testing'

// What the engine fills in for a spawn from the main session's Agent tool.
const SPAWN = {
  prompt: 'p',
  tool_use_id: 'tu',
  provider: { plugin: 'engine', tier: 'core' },
  parentModel: 'opus',
  background: true,
  fork: false,
} as const

test('the status line shows the cooks on the stove until each one finishes', async ($, on) => {
  // Nothing sits beneath the plugin: each hook here stands for the engine.
  const lines: (string | undefined)[] = []
  let started = 0
  on('ui.status', (_, e) => (lines.push(e.text), { value: undefined }))
  on('agent.spawn', () => ({ model: 'm', agentId: `a${++started}` }))
  on('turn.complete', (_, e) => ({ text: e.answer }))

  await $.agent.spawn({ ...SPAWN, description: 'recipe 05: port glow cards', subagentType: 'brigade:cook' })
  await $.agent.spawn({ ...SPAWN, description: 'recipe 10: build and check', subagentType: 'brigade:prep' })
  await $.agent.spawn({ ...SPAWN, description: 'look around', subagentType: 'Explore' })
  expect(lines.at(-1)).toBe('brigade: cook 05 · prep 10')

  const done = { answer: 'report', durationMs: 1, isAborted: false, turnId: 't', reason: 'answer' } as const
  await $.turn.complete({ ...done, agentId: 'a1' })
  expect(lines.at(-1)).toBe('brigade: prep 10')

  await $.turn.complete({ ...done, agentId: 'a3' })
  expect(lines.at(-1)).toBe('brigade: prep 10')

  await $.turn.complete({ ...done, agentId: 'a2' })
  expect(lines.at(-1)).toBe(undefined)
  expect(lines.length).toBe(4)
})
