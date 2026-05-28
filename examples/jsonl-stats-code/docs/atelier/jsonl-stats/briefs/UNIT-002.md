# UNIT-002 — test fixture

## Objective
Create the sample JSON Lines fixture used by the CLI integration test.

## Inputs / context
- CONTRACT.md (the "coverage" semantics — at least one field must be missing from
  some records so coverage exercises a fraction < 1.0).
- No upstream units.

## Approach
- Write `tests/sample.jsonl` with at least 5 records, one JSON object per line.
- Use mixed value types across records (int, str, float, bool, and at least one
  nested list or dict).
- At least one field must be present in some records but absent from others.

## Constraints
- Valid JSON Lines: exactly one JSON object per line, no trailing commas, UTF-8.
- Do not write any Python here — this unit owns only the data file.

## Acceptance criteria
- [ ] (runnable) `python -c "import json,sys; [json.loads(l) for l in open('tests/sample.jsonl') if l.strip()]"` exits 0 (every non-blank line is valid JSON)
- [ ] (assertional) ≥5 records
- [ ] (assertional) at least one field is missing from at least one record (so coverage < 1.0 for it)
- [ ] (assertional) value types include at least three of: int, str, float, bool, list/dict

## Dependencies
none
