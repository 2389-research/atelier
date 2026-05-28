# UNIT-001 — core stats module + unit tests

## Objective
Implement the `jsonl_stats` core module with the functions pinned in the contract,
plus unit tests that exercise them.

## Inputs / context
- CONTRACT.md (the function signatures under "Interfaces" are binding).
- No upstream units.

## Approach
- Create `jsonl_stats/__init__.py` exporting the public functions from `core.py`.
- Implement `core.py` per the pinned signatures:
  - `load_records`: open the file, parse each non-blank line with `json.loads`,
    return the list of dicts.
  - `count_records`: `len(records)`.
  - `field_coverage`: for each field appearing in any record, fraction of records
    that contain it (records_with_field / total_records). Empty input → `{}`.
  - `type_histogram`: per field, count `type(value).__name__` across records that
    contain the field.
  - `build_report`: assemble `{"count", "coverage", "types"}`.
- Write `tests/test_core.py` with pytest tests covering: a small in-memory record
  list, a field missing from some records (coverage < 1.0), and mixed value types.

## Constraints
- stdlib only (`json`). Do not read `tests/sample.jsonl` (that's UNIT-002); build
  test data inline in the test file.
- Match the pinned signatures exactly — UNIT-003 imports them.

## Acceptance criteria
- [ ] (runnable) `cd <project> && python -m pytest tests/test_core.py -q` exits 0 with ≥3 tests passing
- [ ] (assertional) `core.py` defines all five functions with the exact contract signatures
- [ ] (assertional) `field_coverage` returns fractions in [0.0, 1.0], not counts (a field present in 1 of 2 records → 0.5)
- [ ] (assertional) `type_histogram` uses `type(value).__name__` as the inner keys

## Dependencies
none
