# Benchmark 01 — wordfreq v2 (small + n-grams)

Build a small Node ESM package `wordfreq` (zero deps, `package.json` has
`"type":"module"`, tests via `node --test`). It analyzes a UTF-8 text file.

## Requirements (v1)
- `src/wordfreq.js` exports:
  - `tokenize(text) -> string[]` — lowercase words, split on non-letters, drop empties.
  - `topWords(text, n = 10) -> {word, count}[]` — the n most frequent words, count desc
    (ties broken alphabetically).
  - `stats(text) -> { total, unique }` — total word count and distinct-word count.
- `src/cli.js` — `node src/cli.js <file> [n]` prints the top-n words and the stats;
  missing file exits non-zero.
- Tests in `test/` covering tokenize (punctuation, case), topWords (ordering + ties),
  stats, and a CLI integration test against a small fixture you create.

## v2 additions — n-grams
- `src/wordfreq.js` additionally exports:
  - `ngrams(text, size) -> string[]` — the contiguous sequences of `size` tokens (from
    `tokenize`), each joined by a single space. e.g. size=2 over tokens `[a,b,c]` →
    `["a b","b c"]`. `size >= 1`. If there are fewer than `size` tokens, return `[]`.
  - `topNgrams(text, size, n = 10) -> {ngram, count}[]` — the n most frequent size-grams,
    count desc, ties broken alphabetically by the ngram string.
- `src/cli.js` gains a `--ngram <size>` flag: when present it prints the top-n
  size-grams (with counts) **instead of** the top words; the `[n]` positional still
  controls how many. Without `--ngram`, behavior is exactly as v1.
- Tests additionally cover `ngrams` (size 1/2/3, fewer-than-size → [], spacing) and
  `topNgrams` (ordering + ties), plus a CLI test exercising `--ngram 2`.

## Done =
`node --test` passes; `node src/cli.js <somefile>` prints output and exits 0;
`node src/cli.js --ngram 2 <somefile>` prints top bigrams; missing-file exits non-zero.
