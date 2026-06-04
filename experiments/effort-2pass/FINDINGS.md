# Effort & 2-pass planning — experiment notes (parked, NOT the default)

Exploration of whether constraining the planner (low `--effort`) and/or adding a
**draft → refine** planning pass makes `atelier-dispatch` cheaper or more reliable.

**Bottom line:** the **default-effort, single-pass** dispatch (now on `main` with
force-Haiku-exec + retry) remains the best *general* config. The low-effort 2-pass
variant here is **more consistent but only wins in a small fraction of cases**
(reasoning-dense specs where the default plan happens to draw expensive). It is parked
here as an optional escape hatch, not promoted to default.

## What the variant is
- **`--effort low`** on the Sonnet calls. (Confirmed it functions in headless `--bare`:
  it cut a plan from ~84k → ~6.7k output tokens, ~$0.81 → ~$0.10. Note: `--effort medium`
  and `MAX_THINKING_TOKENS` were effectively no-ops in our setup.)
- **2-pass planning:** a cheap **draft** (Sonnet, low) then a **refine** pass (Sonnet,
  low) that pins cross-sprint conventions and fleshes briefs. Then Haiku executes, with
  the bounded Sonnet fix loop.
- Harness: `run_2pass.py` (parameterize the task + gate).

## Key findings (in order of confidence)

1. **Default-effort planning is HIGH variance.** Same spec (`03-jqlite-v2`), the basic
   plan cost **$0.268 one run, $0.703 another — a 2.6× swing.** This dwarfs most
   per-task config differences and means **single runs are not trustworthy**; real
   claims need medians over N replicates.

2. **The 2-pass's real value is variance reduction, not magnitude.** Its plan cost is
   **flat ~$0.28** regardless of spec; it caps the expensive-plan tail. It "wins" mainly
   when the default plan happens to draw expensive.

3. **The crossover is reasoning-density-driven, not size-driven.** `03-jqlite-v2`
   (parser/streaming — reasoning-dense) blew the default plan up and the 2-pass won;
   `06-ledger-v2` (equally "large" but mechanical CRUD + tree rollup) kept the default
   plan cheap and it was a **tie**. So "large → 2-pass" is wrong; "reasoning-dense
   (parser/compiler/algorithm) → default plan tends to balloon → 2-pass competitive" is
   closer — but see #1: even the balloon is partly noise.

4. **`--effort low` is a net loss on simple/mechanical specs.** It over-decomposes (more
   sprints → more exec), and the plan savings are tiny when the plan was already cheap.
   On the original 01–03 suite it was *worse* than default.

5. **Cost-driver corrections (vs earlier assumptions):**
   - Haiku exec scales with **sprint count** (per-sprint output + thinking), NOT with
     contract-input size. So forcing finer decomposition *raises* cost.
   - **Contract slicing** (send each sprint only its needed sections) works mechanically
     (~14% of contract per sprint, 0 fallbacks) but barely moved cost — input wasn't the
     driver. Correct hygiene, not a cost lever here.
   - The **fix loop can't repair structural/layout problems** (it only rewrites file
     contents) — e.g. a Go module nested under a `go.work` vs a root `go test ./...` gate
     looked like a failure though the code was correct.

## Data (single runs — treat as noisy, see #1)

### v2 edits — basic (default single-pass) vs 2-pass (low)
| v2 task | basic plan | basic total | 2-pass plan | 2-pass total | winner |
|---|---|---|---|---|---|
| 01-wordfreq-v2 (small) | $0.180 | $0.332 | $0.276 | $0.595 | basic −44% |
| 02-taskstore-v2 (medium) | $0.343 | $0.551 | $0.274 | $0.821 | basic −33% |
| 03-jqlite-v2 (large, parser) run1 | $0.703 | $1.190 | $0.276 | $0.646 | 2-pass −46% |
| 03-jqlite-v2 (large, parser) run2 | $0.268 | $0.842 | — | — | (2-pass −24% vs run2) |
| 06-ledger-v2 (large, CRUD) | $0.248 | $0.809 | $0.335 | $0.775 | ~tie |

### Original suite — prev atelier (default) vs low-effort vs Opus
| task | prev atelier (default) | low-effort | Opus-from-spec |
|---|---|---|---|
| 01-wordfreq | $0.164 | $0.288 | $0.456 |
| 02-taskstore | $0.267 | $0.265 | $0.599 |
| 03-jqlite | $0.263 | $0.469 | $0.962 |
| 04-pysummary (Py) | $0.215 | $0.172 | $0.473 |
| 06-ledger (Py) | $0.366 | $0.551 | $0.741 |
| 07-taskgraph (Go) | $0.240 | $0.447 | $0.987 |

Default-effort ≈ 36% of Opus across the suite; low-effort ≈ 52%. **Default wins.**

## Recommendation
- Keep `main` as-is (default-effort single-pass + force-Haiku + retry).
- Treat low-effort / 2-pass as an **opt-in** for reasoning-dense specs only.
- Before any firm claim: run **N replicates → medians + spread** (the variance is too
  high for single runs).
