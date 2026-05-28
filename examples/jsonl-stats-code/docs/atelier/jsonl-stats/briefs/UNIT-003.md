# UNIT-003 — CLI + integration test

## Objective
Add a command-line entry point that prints a stats report for a JSONL file, plus
an integration test that runs it against the fixture.

## Inputs / context
- CONTRACT.md (the report dict shape and the core function signatures).
- UNIT-001 output: `jsonl_stats/core.py` (import `load_records`, `build_report`).
- UNIT-002 output: `tests/sample.jsonl` (the integration test reads this).

## Approach
- Create `jsonl_stats/__main__.py` so `python -m jsonl_stats <path>` works:
  - parse one positional arg `path` with `argparse`,
  - call `load_records(path)` then `build_report(records)`,
  - print a readable report: the record count, each field's coverage as a
    percentage, and the type histogram. Exit 0 on success.
  - On a missing file, print an error to stderr and exit with a non-zero code.
- Write `tests/test_cli.py`: use `subprocess` to run
  `[sys.executable, "-m", "jsonl_stats", "tests/sample.jsonl"]`, assert exit code 0
  and that the record count from the fixture appears in stdout.

## Constraints
- stdlib only (`argparse`, `subprocess`, `sys`). Import core via the package, do
  not reimplement stats logic here.
- Run the CLI as a module (`python -m jsonl_stats`), not a loose script.

## Acceptance criteria
- [ ] (runnable) `cd <project> && python -m jsonl_stats tests/sample.jsonl` exits 0 and prints a count line
- [ ] (runnable) `cd <project> && python -m pytest tests/test_cli.py -q` exits 0 with the integration test passing
- [ ] (runnable) `cd <project> && python -m jsonl_stats /no/such/file.jsonl` exits non-zero
- [ ] (assertional) `__main__.py` imports stats logic from `jsonl_stats.core`, does not reimplement it

## Dependencies
UNIT-001, UNIT-002
