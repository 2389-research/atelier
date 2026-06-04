# Benchmark 06 — ledger v2 (complex Python + account hierarchies)

Build a Python package `ledger` (stdlib only, tests via `pytest`): a **double-entry
bookkeeping** engine with a chart of accounts, balanced journal entries, account
balances, a trial balance, and derived financial reports.

## Domain rules (v1 — the real logic)
- Five account types: `ASSET`, `LIABILITY`, `EQUITY`, `INCOME`, `EXPENSE`.
- **Normal balance side**: debit-normal = {ASSET, EXPENSE}; credit-normal =
  {LIABILITY, EQUITY, INCOME}. An account's balance = (sum of debits − sum of credits)
  if debit-normal, else (sum of credits − sum of debits).
- A **journal entry** is a dated description plus ≥2 postings; each posting is
  `(account, debit, credit)` with exactly one of debit/credit > 0, the other 0. Valid
  only if `sum(debits) == sum(credits)` and total > 0. Integer cents (no floats).

## Requirements (v1, each a natural module/unit)
- `ledger/accounts.py` — `AccountType`, `normal_side(type) -> "debit"|"credit"`,
  `Account(code, name, type)`, and `ChartOfAccounts` with `add(account)` /
  `get(code) -> Account` (unknown code raises a clear error).
- `ledger/journal.py` — `Posting(account_code, debit, credit)`, `Entry(date,
  description, postings)`, `validate(entry) -> True | raises` (one-side-only + balanced).
- `ledger/book.py` — `Book(chart)` with `post(entry)`, `balance(code) -> int` (signed
  per normal side), `balances() -> dict[code,int]`, `trial_balance() ->
  {"debits","credits","balanced"}`. Posting to an unknown code raises.
- `ledger/reports.py` — `balance_sheet(book) -> {"assets","liabilities","equity","balanced"}`
  and `income_statement(book) -> {"income","expenses","net_income"}`. PIN (the one
  genuinely ambiguous v1 decision): balance-sheet `equity` = sum of equity-account
  balances **PLUS net income** (income − expenses); `balanced` is
  `assets == liabilities + equity`.
- `ledger/__main__.py` — `python -m ledger <file.json>` loads `{"accounts":[...],
  "entries":[...]}`, posts all, prints trial balance + both reports; bad input exits
  non-zero with a stderr message.
- `tests/` (pytest): normal-side mapping; entry validation; per-account balance sign;
  trial balance; balance sheet `assets == liabilities + equity`; income net; unknown
  account error; CLI integration over a fixture.

## v2 additions — account hierarchies & rolled-up balances
- `Account` gains an optional `parent` (a parent account's `code`, or `None`).
  `ChartOfAccounts.add` validates: if `parent` is set it must already exist **and have
  the same `AccountType`** as the child (else raises a clear error); a parent chain that
  would form a **cycle** raises.
- `Book.balance(code, rollup=False) -> int` — `rollup=False` (default) is the account's
  own signed balance (v1 behavior, unchanged). `rollup=True` is the account's own
  balance **plus** the rolled-up balances of all its descendants (recursively),
  combined on that account's normal side.
- `Book.rolled_balances() -> dict[code, int]` — rolled-up balance for every account.
- `ledger/reports.py`: `balance_sheet` and `income_statement` now sum the **rolled-up
  balances of top-level (parent-less) accounts only**, per type — so a parent and its
  children are **never double-counted**. The v1 equity/net-income pin is unchanged, and
  `assets == liabilities + equity` must still hold for any well-formed book (flat or
  hierarchical). `trial_balance` is **unchanged** (own balances; no double counting).
- `ledger/__main__.py` additionally prints the chart as an indented tree, each account
  with its rolled-up balance.
- tests additionally cover: parent validation (missing parent raises; type-mismatch
  raises; cycle raises); rollup balance (parent = own + descendants, across ≥2 levels);
  reports use top-level rolled-up balances with **no double-counting** (a book with
  parent+child accounts still satisfies `assets == liabilities + equity`);
  `trial_balance` unchanged under hierarchy; and CLI tree output.

## Done =
`python -m pytest` passes; `python -m ledger <fixture.json>` prints a balanced trial
balance, the account tree with rolled-up balances, and both reports, exiting 0;
malformed input / unbalanced entry exits non-zero.
