# AGENTS.md

## Working References

Read files in this order before making any substantial change:

1. [ai-delivery-multiagent/AGENT.md](AGENT.md)
2. [ai-delivery-multiagent/TODO.md](TODO.md)
3. the actual code relevant to the task

## Role of Each File

- `AGENT.md`
  High-level project contract. This file captures the architecture decisions, IBM constraints, target structure, demo goals, and principles that must be preserved.
- `TODO.md`
  Living project backlog. This file captures what remains to be done, the recommended order, priorities, blocked tasks, and current progress.

## Maintenance Convention

For future Codex sessions:

- do not use `AGENTS.md` as a detailed backlog
- do not duplicate the full architecture in `TODO.md`
- keep `AGENT.md` relatively stable
- update `TODO.md` whenever an important task is completed, added, reprioritized, or blocked

## When to Modify `AGENT.md`

Modify `AGENT.md` only if one of the following actually changes:

- target architecture
- agent roles
- non-negotiable constraints
- expected repository structure
- product or demo strategy

## When to Modify `TODO.md`

Modify `TODO.md` when:

- a task is completed
- a task becomes blocked
- a new subtask appears
- a priority changes
- an estimate needs to be revised

## Practical Rule

If a future agent needs to move the project forward:

1. read `AGENT.md`
2. read `TODO.md`
3. choose the next `P0` or `P1` task
4. implement it
5. update `TODO.md`
6. modify `AGENT.md` only if a core decision changes
