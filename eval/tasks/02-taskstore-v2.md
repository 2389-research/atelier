# Benchmark 02 — taskstore v2 (medium + tags & due dates)

Build a Node ESM package `taskstore` (zero deps, `"type":"module"`, tests via
`node --test`): an in-memory task list with JSON persistence and a CLI.

## Requirements (v1)
- `src/model.js` — a task is `{ id, title, done, createdAt }`. Export
  `makeTask(title, id, now) -> task` and `validate(task) -> true | throws`.
- `src/store.js` — `createStore() -> store` plus pure-ish operations:
  `add(store, title)`, `get(store, id)`, `list(store)`, `complete(store, id)`,
  `filter(store, {done})`. Unknown id throws a clear error.
- `src/persist.js` — `save(store, storage)` / `load(storage) -> store`, where
  `storage` is an injected object with `getItem/setItem` (default in-memory); JSON
  round-trips faithfully. No direct filesystem/localStorage in the module body.
- `src/cli.js` — `node src/cli.js <add|list|done> [args]` against a JSON file;
  prints results; bad usage exits non-zero.
- Tests in `test/` for model validation, every store op (incl. the unknown-id error),
  a persist round-trip through a fake storage, and a CLI integration test.

## v2 additions — tags, due dates, richer filtering
- A task is now `{ id, title, done, createdAt, tags, dueDate }`:
  - `tags` — a `string[]` (default `[]`).
  - `dueDate` — an ISO-8601 date string or `null` (default `null`).
- `makeTask(title, id, now, { tags = [], dueDate = null } = {})` accepts the optional
  fields. `validate` additionally enforces: `tags` is an array of non-empty strings;
  `dueDate` is either `null` or a string that parses to a valid date (else throws a
  clear error).
- `add(store, title, { tags = [], dueDate = null } = {})` stores the new fields.
- `filter(store, { done, tag })` — `tag` (optional) keeps only tasks whose `tags`
  include it; when both `done` and `tag` are given, they combine with AND.
- New `overdue(store, now) -> task[]` — tasks that are NOT done AND have a non-null
  `dueDate` strictly before `now`, sorted by `dueDate` ascending.
- `persist` round-trips `tags` and `dueDate` faithfully.
- `src/cli.js`: `add <title> [--tag <t>]... [--due <ISO>]`; `list [--tag <t>] [--done]`;
  a new `overdue` subcommand prints overdue tasks. Bad usage exits non-zero.
- Tests additionally cover: validate rejecting bad `tags`/`dueDate`; add-with-tags/due;
  `filter` by tag (and combined with done); `overdue` (ordering; excludes done /
  no-due / future); persist round-trip of the new fields; and CLI `add --tag/--due`,
  `list --tag`, and `overdue`.

## Done =
`node --test` passes; the CLI add→list→done flow works; `add --tag x --due <ISO>`,
`list --tag x`, and `overdue` work against a temp JSON file; bad usage exits non-zero.
