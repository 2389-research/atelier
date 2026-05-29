#!/usr/bin/env bash
# Run one benchmark task headless and capture its total cost (subagents included).
#
#   ./run.sh <task-file> <direct|atelier> <opus|sonnet>
#
# Each run executes in its own throwaway dir under runs/. The cost printed is
# total_cost_usd from the headless JSON result, which INCLUDES subagent cost
# (verified). After it finishes, RE-RUN the gate yourself to confirm quality —
# don't trust the run's self-report.
set -euo pipefail

EVAL_DIR="$(cd "$(dirname "$0")" && pwd)"
TASK="$1"; METHOD="$2"; MODEL="$3"
SPEC_FILE="$EVAL_DIR/tasks/$(basename "$TASK")"
[ -f "$SPEC_FILE" ] || { echo "task not found: $SPEC_FILE" >&2; exit 1; }

slug="$(basename "$TASK" .md)"
RUN_DIR="$EVAL_DIR/runs/${slug}__${METHOD}__${MODEL}"
rm -rf "$RUN_DIR"; mkdir -p "$RUN_DIR"

# Both arms are held to the SAME done-bar (write real tests, iterate to green) so the
# cost comparison is at equal quality. Final scoring uses an EXTERNAL held-out gate
# the experimenter runs (see README) — not the arm's self-report.
DONE_BAR="Definition of done (mandatory): write tests that genuinely exercise the
behaviors in the spec (NOT trivial/always-true tests), run them, and iterate until
they actually pass. Do not stop with failing tests or with tests that don't assert
the real expected values."

if [ "$METHOD" = "atelier" ]; then
  INSTR="Use the atelier skill in split tier to build the task specified below. Decompose, write the contract + briefs, dispatch executors, verify. $DONE_BAR"
else
  INSTR="Build the task specified below directly. $DONE_BAR"
fi

PROMPT="$INSTR

--- TASK SPEC ---
$(cat "$SPEC_FILE")"

cd "$RUN_DIR"
claude -p "$PROMPT" --output-format json --model "$MODEL" \
  --permission-mode bypassPermissions > result.json 2> err.log || true

COST="$(python3 -c "import json;print('%.5f'%json.load(open('result.json')).get('total_cost_usd',0))" 2>/dev/null || echo "PARSE_ERR")"
echo "${slug} | ${METHOD} | ${MODEL} | \$${COST} | dir=${RUN_DIR}"
echo "  -> now verify quality: cd '${RUN_DIR}' && <gate, e.g. node --test | pytest>"
