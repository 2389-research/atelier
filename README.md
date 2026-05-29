# atelier

**Tiered-delegation task execution for Claude Code.** A strong model plans, cheap
models execute in parallel, a mid model verifies — same quality, a fraction of the
strong-model cost and wall-clock.

> Offload each unit of work to the **weakest model that can do it correctly.**

## The idea

Most of the work in a task is pattern-following execution, not reasoning. atelier
concentrates the expensive model (Opus) on the parts that genuinely need judgment
— decomposition and every cross-cutting decision — and pushes execution down to a
fast cheap model (Haiku), with a mid model (Sonnet) verifying each piece against
explicit acceptance criteria.

```
architect (Opus)   plan: contract pins every cross-unit decision + per-unit briefs
      │
      ▼
executors (Haiku)  execute one brief each, in parallel where dependencies allow
      │
      ▼
checker (Sonnet)   verify each unit against its acceptance criteria; bounded fixes
      │
      ▼
architect (Opus)   integrate, final coherence pass, report
```

The enabler is **acceptance criteria as the trust contract**: as long as the
checker verifies each unit against concrete, written criteria, the cheap model's
output is trustworthy. This generalizes "tests as the source of truth" to any task,
code or not.

## Lineage

atelier generalizes three existing systems to arbitrary tasks:

- **speed-run** — offload first-pass generation to a fast model; the strong model
  does architecture and *surgical* fixes, never wholesale regeneration.
- **pipelines/local_code_gen** — a strong architect pins every cross-unit decision
  in a contract so the weak executor never makes a system-level choice.
- **Noospheric Orrery** — proof of the philosophy: Sonnet never extracts; Haiku
  does all the work; Sonnet writes and refines the spec until the cheap model
  reliably passes.

Where `local_code_gen` writes 600-line byte-pinned contracts for a tiny local
model (qwen3.6 / gemma), atelier deliberately sits well above that floor. **Haiku
is far stronger**, so the contract pins only what is *cross-unit AND genuinely
ambiguous* — the seams, not the interiors. Since Opus/Sonnet output is the
expensive part, terseness is the goal: pin the few decisions two capable units
would otherwise diverge on, and let Haiku infer the rest.

## Skills

| Skill | Role | Model | Runs as |
|-------|------|-------|---------|
| `atelier` | orchestrator | — | this session |
| `atelier-plan` | director's planning discipline | Opus | this session |
| `atelier-brief` | expand a unit spec into a brief *(split tier)* | Sonnet | dispatched subagent |
| `atelier-execute` | execute one unit | Haiku | dispatched subagent |
| `atelier-check` | verify + fix one unit | Sonnet | dispatched subagent |

## Planning tiers (who writes the briefs)

- **direct** — Opus writes the contract *and* every brief. Fewest moving parts, one
  translation boundary. Best for **few units / subtle, correctness-critical work**.
- **split** — Opus (director) writes the contract + terse unit specs; **Sonnet**
  brief-writers expand them in parallel (mirrors `local_code_gen`'s
  Opus-contract → Sonnet-sprint flow). The bulky brief-writing drops to the
  5×-cheaper tier and Opus's context stays lean. Best for **many units (≳ 6) /
  mechanical briefs / scale**.
- **hybrid** — Opus writes the 1–2 subtle units' briefs, Sonnet the routine rest.

Rough rule: direct below ~5 units, split above — but it's per-task, and the subtle
units can stay direct even in a split run. Authority follows the tier: Opus owns
the contract (cross-unit), the brief-writer owns its unit (within-unit), so a
within-unit fix routes to cheap Sonnet and only contract defects reach Opus.

## Usage

Say **"atelier"**, **"delegate this"**, or **"tiered build"** on a multi-part task.
The orchestrator will: frame the goal, plan (write `CONTRACT.md` + per-unit briefs
with acceptance criteria, confirmed with you), dispatch Haiku executors in parallel
where dependencies allow, run a Sonnet checker on each unit with a bounded tiered
fix loop, then do a final coherence pass and report.

Artifacts land in `docs/atelier/<task-slug>/` (`CONTRACT.md`, `briefs/`,
`LEDGER.md`) so a run is auditable and resumable.

### Decomposition modes

Not every task is "one file per agent." The architect picks a mode by how cohesive
the final artifact must be:

- **partition** — units own separate regions/files, run in **parallel**, architect
  merges. Best for separable outputs (code files, doc sections).
- **relay** — one shared artifact extended segment by segment, **sequentially**,
  each agent reading the artifact-so-far. Best for flowing prose (a story chapter).
- **layered** — role-specialized passes over the whole artifact (draft → continuity
  edit → polish), **sequentially**. Best for one seamless voice via multiple lenses.

A single artifact with no cross-unit seams skips the contract entirely — one brief,
one execute, one check (or just don't use atelier).

## Fix loop (bounded, terminates)

The checker diagnoses (`pass` / `local` / `execution` / `brief`); the orchestrator
decides and counts:

1. **surgical** (Sonnet, in place) — ≤ 2
2. **executor redo** (fresh Haiku + notes) — ≤ 1
3. **architect replan** (revise contract/brief) — ≤ 1
4. otherwise **surface to the human**

A regression guard rolls back any fix that breaks a previously-passing criterion.

## Design

See [`docs/superpowers/specs/2026-05-28-atelier-design.md`](docs/superpowers/specs/2026-05-28-atelier-design.md).

## Status

v0.1.0 — initial implementation. Not yet dogfooded; see the spec's validation plan.
