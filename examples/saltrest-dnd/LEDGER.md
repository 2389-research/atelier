# Ledger — The Bones of Saltrest

Working dir: `docs/atelier/saltrest/`

## Units

| Unit | Title | Deps | Status | surgical_n | redo_n | replan_n | Notes |
|------|-------|------|--------|-----------|--------|----------|-------|
| UNIT-001 | Hook & Saltrest | none | done | 1 | 0 | 0 | checker fixed: # -> ## heading + canon date ("day before") |
| UNIT-002 | NPCs & Factions | none | done | 1 | 0 | 0 | checker fixed: # -> ## heading |
| UNIT-003 | Kelpwater Cove + clock | none | done | 1 | 0 | 0 | checker fixed: heading levels; clock numbers verified vs contract |
| UNIT-004 | Resolution & rewards | UNIT-001, UNIT-002, UNIT-003 | done | 1 | 0 | 0 | checker fixed: "Lieutenants"->"Initiates"; clock numbers verified vs dungeon |

Status ∈ pending · executing · checking · done · escalated

## Fix-loop log
- UNIT-001: executor pass(self) -> checker caught # heading + canon date contradiction -> tier1 surgical (2 edits) -> pass
- UNIT-002: executor pass(self) -> checker caught # heading -> tier1 surgical -> pass
- UNIT-003: executor pass(self) -> checker caught heading levels -> tier1 surgical -> pass (flagged non-5e "Endurance" skill, advisory)
- UNIT-004: executor pass(self, read all 3 deps) -> checker caught "Lieutenants" naming slip -> tier1 surgical -> pass

## Run summary
- Units: 4/4 done. Assembled ADVENTURE.md (~5,200 words, playable).
- Escalations: 4 surgical (all heading/canon-consistency fixes the checkers caught despite executors self-reporting pass) · 0 redo · 0 replan · 0 to human.
- Cross-unit canon held: clock numbers (5/10 rounds, DC 15) consistent across dungeon + resolution; Coria's mercy motive consistent; one real date contradiction caught + fixed by checker.
- Integration nit (architect): NPC sub-entries rendered at H2 (##) instead of H3 (###) under Cast & Factions — cosmetic, normalize at integration if shipping.
- Pattern proven: architect pins canon -> Haiku writes in parallel -> Sonnet enforces consistency the executors missed.
