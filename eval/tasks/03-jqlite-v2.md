# Benchmark 03 — jqlite v2 (large + pipes & builtins)

Build a Node ESM package `jqlite` (zero deps, `"type":"module"`, tests via
`node --test`): a tiny JSON path-query tool (a minimal jq). This is the large,
multi-module benchmark.

## Query language (v1)
A path is a dot/bracket chain over parsed JSON, e.g.:
`.users[0].name` · `.items[].price` · `.meta.tags[1]` · `.` (identity).
`[]` (no index) maps over every element of an array. Numeric indices select one
element. Out-of-range / missing keys yield `null` (or are skipped for `[]` mapping).

## Requirements (v1, each a natural module/unit)
- `src/lexer.js` — `tokenize(query) -> token[]` (dots, idents, `[`, `]`, ints, `[]`).
- `src/parser.js` — `parse(tokens) -> step[]` (a list of path steps: key | index | iterate).
- `src/evaluator.js` — `query(data, steps) -> result` applying steps to parsed JSON,
  with the mapping/indexing/null semantics above.
- `src/format.js` — `format(value) -> string` (pretty JSON; scalars bare).
- `src/cli.js` — `node src/cli.js '<query>' <file.json>` parses the file, runs the
  query, prints formatted output; parse errors / missing file exit non-zero.
- Tests in `test/` for the lexer, parser, evaluator (key, index, `[]` mapping,
  missing→null), formatter, and a CLI integration test over a fixture JSON you create.

## v2 additions — pipes and builtins
The query language gains the **pipe** operator `|` and two **builtins**: `length`
and `keys`.

- **Pipe** `q1 | q2 | …` — evaluate `q1`, then feed its result into `q2`, and so on.
  Streaming, jq-style: when a stage yields multiple values (because a `[]` iteration
  produced a stream), **each value flows independently** through the rest of the
  pipeline, and the final results are concatenated in order.
- **`length`** — array → element count; string → character length; object → number of
  keys; `null` → 0; number/boolean → throws a clear error.
- **`keys`** — object → its keys sorted ascending (a `string[]`); array → its indices
  `[0 … n-1]` (a `number[]`); anything else → throws a clear error.
- `src/lexer.js` gains a `|` token and bareword identifier tokens for the builtins
  (`length`, `keys`).
- `src/parser.js` produces a **pipeline**: a list of stages, where each stage is either
  a path (list of v1 steps) or a builtin. (Keep v1 single-path queries working — a
  pipeline of one path stage.)
- `src/evaluator.js` applies the stages left-to-right with the streaming semantics
  above; builtins operate on each incoming value.
- `src/cli.js` supports the full piped query, e.g.
  `node src/cli.js '.users[] | keys' data.json`.
- Tests additionally cover: lexer (`|`, builtin idents); parser (pipelines, builtins,
  v1 single-path still parses); evaluator (pipe streaming across a `[]` stage; `length`
  on array/string/object/null; `keys` on object/array; the error cases); and a CLI
  test for a piped query.

## Done =
`node --test` passes; `node src/cli.js '.users[].name' data.json` still works; and
`node src/cli.js '.users[] | keys' data.json` prints the keys of each user; bad query /
missing file exit non-zero.
