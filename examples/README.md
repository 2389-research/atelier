# atelier examples

Real dogfood runs, captured verbatim. Each was produced by the architect (Opus)
writing the contract + briefs, Haiku subagents executing units, and Sonnet
subagents checking against acceptance criteria.

## `jsonl-stats-code/` — code task (partition mode, runnable criteria)

A small Python package (`jsonl_stats`) built across three units: core stats module
+ tests, a JSONL fixture, and a CLI + integration test. UNIT-001 and UNIT-002 ran
in parallel; UNIT-003 depended on both. All acceptance criteria were **runnable**
(pytest, CLI exit codes). Final: 16 tests pass.

Run it: `cd jsonl-stats-code && python -m pytest -q && python -m jsonl_stats tests/sample.jsonl`

The atelier artifacts are under `docs/atelier/jsonl-stats/` (CONTRACT, briefs,
LEDGER). The ledger also records a separate fault-injection check: a planted
`field_coverage` bug (returning counts not fractions) was caught by the checker,
diagnosed `local`, and surgically fixed with the regression guard.

## `saltrest-dnd/` — creative writing (partition mode, assertional criteria)

A playable D&D 5e adventure ("The Bones of Saltrest"), assembled from four units:
hook, NPCs, dungeon (with a ticking-clock mechanic), and resolution paths. The
contract pinned all canon (named entities, the 5/10-round clock, the three
resolution paths) so four independently-written units stayed consistent.

`ADVENTURE.md` is the assembled module. The `LEDGER.md` fix-loop log is the
interesting part: every Haiku executor self-reported "pass," but the Sonnet
checkers independently caught four real defects — three heading-level errors and a
**canon contradiction** (a date that disagreed with the contract) — and fixed each
surgically. That gap between executor self-report and independent verification is
exactly what the checker tier exists to close.

> Note: these used the **partition** mode (separable sections). For a continuous
> prose chapter, prefer **relay** or **layered** mode — see the main README.
