# Ledger — <task name>

Working dir: `docs/thrifty/<task-slug>/`

## Units

| Unit | Title | Deps | Status | exec_model (observed) | surgical_n | redo_n | replan_n | Notes |
|------|-------|------|--------|-----------------------|-----------|--------|----------|-------|
| UNIT-001 | <title> | none | pending | — | 0 | 0 | 0 | |
| UNIT-002 | <title> | UNIT-001 | pending | — | 0 | 0 | 0 | |

> `exec_model (observed)` = the model the executor **actually ran on**, not the requested
> tier. The self-reported `model:` line is a weak signal only — corroborate with observed
> cost/usage (a Haiku call is ~10–20× cheaper than Sonnet). Write a model here only when
> corroborated; otherwise put **`unverified`**. Flag anything that demonstrably isn't Haiku —
> the tier request was dropped and the cost win didn't apply.

Status ∈ `pending` · `executing` · `checking` · `done` · `escalated`

## Fix-loop log

> One line per tier transition, append-only.

- (none yet)

## Run summary

> Filled in at integration.

- Units: __/__ done
- Escalations: __ surgical · __ redo · __ replan · __ surfaced to human
- Executors on Haiku (observed): __/__ — **flag any that fell back to Sonnet/other**
- Approx. cost saved vs. all-in-session, **computed from observed models**: __
  (if any executor ran off-Haiku, the savings are lower than planned — state it)
