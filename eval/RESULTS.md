# atelier eval — results

Fill one row per (task × method) from `/status` at the end of each fresh session.
`Total $` = Session Total cost (includes subagents). `opus/sonnet/haiku $` = the
`Usage by model` rows (for atelier this is the tier split incl. subagents). "Tests" =
did the task's gate pass.

## Experiment 1 — cost / quality

| Task | Size | Method | Total $ | opus $ | sonnet $ | haiku $ | Tests pass | Escalations | Notes |
|------|------|--------|---------|--------|----------|---------|------------|-------------|-------|
| 01-wordfreq | small | direct-opus | $0.499 | 0.499 | — | — | 18/18 ✓ | n/a | single-agent, no skills |
| 01-wordfreq | small | opus+subagents | $0.505 | 0.505 | — | — | 17/17 ✓ | n/a | **0 Task calls** — given permission, didn't delegate |
| 01-wordfreq | small | direct-sonnet | _pending_ | — | | — | | n/a | |
| 01-wordfreq | small | atelier-split | $1.856 | | | | 12/12 ✓ | 0 | full split-tier headless, 3/3 units; **3.7× direct** (small = worst case) |
| 01-wordfreq | small | atelier-dispatch | $0.624 | 0.446 (orch) | — | 0.178 (disp) | 35/35 ✓ | 0 | JSONL-dispatch headless; **3× cheaper than subagent**, ~1.25× direct; orch fixed cost dominates at small size |
| 02-taskstore | medium | direct-opus | | | — | — | | n/a | |
| 02-taskstore | medium | direct-sonnet | | — | | — | | n/a | |
| 02-taskstore | medium | atelier-split | | | | | | | |
| 03-jqlite | large | direct-opus | | | — | — | | n/a | |
| 03-jqlite | large | direct-sonnet | | — | | — | | n/a | |
| 03-jqlite | large | atelier-split | | | | | | | |

### Generality probes (vary stack/type; run once each, not on the size curve)
| Task | Type | Method | Model(s) | Total $ | Total tokens | Quality (gate) | Notes |
|------|------|--------|----------|---------|--------------|----------------|-------|
| 04-pysummary | Python code | direct-opus | opus | | | pytest | |
| 04-pysummary | Python code | atelier-split | opus+sonnet+haiku | | | pytest | |
| 05-comparison-brief | non-code | direct-opus | opus | | | checklist | |
| 05-comparison-brief | non-code | atelier-split | opus+sonnet+haiku | | | checklist | |

### Read-out (fill after the table)
- atelier-split vs direct-opus, $ by size: small ___% · medium ___% · large ___%
- atelier-split vs direct-sonnet (the honest bar), $ by size: ___ / ___ / ___
- Does the win grow with size? (the core hypothesis): __________
- Any quality gaps (tasks where a method failed tests): __________

## Experiment 2 — simmer refinement trajectory

| Round | Prompt change (ASI) | Eval subset | atelier $ (before→after) | Quality held? | Keep/rollback |
|-------|---------------------|-------------|--------------------------|---------------|---------------|
| 0 (baseline) | — | 01 (+02) | | — | — |
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

Held-out check (run once at end, simmer never saw it): 03-jqlite — cost ___, tests ___.
