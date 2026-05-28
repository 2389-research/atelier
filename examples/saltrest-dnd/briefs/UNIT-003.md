# UNIT-003 — Kelpwater Cove (the dungeon) + the clock

## Objective
Write the dungeon: the three-level sea-cave site, room by room, with stat blocks
and DCs, and define the ticking-clock mechanic precisely (the rest of the module
depends on your numbers).

## Inputs / context
- CONTRACT.md — the dungeon name/levels (Tide Cut, the Choir Gallery, the Vault),
  the Seraphine ledger, the Drowned Choir, and the clock spine you must specify.

## Approach
- Write a `## Kelpwater Cove` section with a short intro then one subsection per
  level (`### Tide Cut`, `### The Choir Gallery`, `### The Vault`):
  - For each room: a sensory description, what's there, and the mechanics — enemy
    stat references (`AC __, __ HP`, attacks), hazards, and skill checks
    (`DC __ <Ability> (<Skill>)`).
  - Give each level at least one source of pressure or escalation (not just empty
    rooms), so tension builds floor by floor.
- **Define the clock precisely** in the Vault: two Drowned Choir initiates
  (`AC 12, 22 HP`) press the Seraphine ledger into the water; each uninterrupted
  round it sinks ~1 inch; submerged after 5 rounds (`DC 15 Strength (Athletics)` to
  recover); pages dissolve after 10 rounds, closing the read-aloud path. State this
  as explicit round-by-round rules a GM can run.

## Constraints
- GM-facing, second person, present tense. D&D 5e stat conventions from the contract.
- Numbers you set for the clock are canon — UNIT-004 references them; keep them
  consistent with the contract (5 / 10 rounds, DC 15).
- Write only to `briefs/out/dungeon.md`.

## Acceptance criteria
- [ ] (assertional) `briefs/out/dungeon.md` has `## Kelpwater Cove` and the three level subsections (Tide Cut, Choir Gallery, Vault)
- [ ] (assertional, specificity) ≥3 explicit stat references in `AC/HP` form and ≥3 skill checks in `DC <n> <Ability> (<Skill>)` form; named features (the Seraphine ledger appears)
- [ ] (assertional, narrative_tension) the ticking clock is specified as explicit round-by-round rules (sink → submerge at 5 → dissolve at 10) with escalating consequence
- [ ] (assertional, player_agency) more than one way to engage the Vault confrontation (e.g. disrupt the initiates, grab the ledger, or fight) is described
- [ ] (assertional) clock numbers match the contract (5/10 rounds, DC 15); no canon contradictions

## Dependencies
none
