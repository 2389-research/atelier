#!/usr/bin/env bash
# Run one benchmark task headless and capture its total cost (subagents included).
#
#   ./run.sh <task-file> <direct|atelier> <opus|sonnet>
#
# Each run executes in its own throwaway dir under runs/. The cost printed is
# total_cost_usd from the headless JSON result, which INCLUDES subagent cost
# (verified). After it finishes, RE-RUN the gate yourself to confirm quality —
# don't trust the run's self-report.
set -eo pipefail

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

case "$METHOD" in
  atelier)
    # the tuned protocol: atelier skill, split tier
    INSTR="Use the atelier skill in split tier to build the task specified below. Decompose, write the contract + briefs, dispatch executors, verify. $DONE_BAR"
    FLAGS=() ;;
  subagents)
    # ad-hoc delegation, NO atelier: skills off, but Task tool allowed. Controls for
    # "delegation" — does naive subagent use get the win without atelier's structure?
    INSTR="First plan your approach to the task below, then implement it. You MAY delegate parts of the work to subagents via the Task tool if you judge it helpful, and you may run those subagents on cheaper models (e.g. haiku) for simpler parts — there is no required structure, organize it however you see fit. No skills or slash commands are available. $DONE_BAR"
    FLAGS=(--disable-slash-commands) ;;
  direct|*)
    # clean baseline: single-agent Opus, NO skills, NO subagents (deterministic).
    INSTR="First plan your approach to the task below, then implement it directly yourself, in this one session. No skills, plugins, slash commands, or subagents are available — do not attempt to use any. $DONE_BAR"
    FLAGS=(--disable-slash-commands --disallowedTools Task) ;;
esac

PROMPT="$INSTR

--- TASK SPEC ---
$(cat "$SPEC_FILE")"

cd "$RUN_DIR"
claude -p "$PROMPT" --output-format json --model "$MODEL" \
  --permission-mode bypassPermissions "${FLAGS[@]}" > result.json 2> err.log || true

COST="$(python3 -c "import json;print('%.5f'%json.load(open('result.json')).get('total_cost_usd',0))" 2>/dev/null || echo "PARSE_ERR")"
TURNS="$(python3 -c "import json;print(json.load(open('result.json')).get('num_turns',''))" 2>/dev/null || echo "")"
# durable record (gate result filled in by the experimenter after verifying)
RESULTS_CSV="$EVAL_DIR/runs/results.csv"
[ -f "$RESULTS_CSV" ] || echo "task,method,model,cost_usd,num_turns,gate(fill_in),dir" > "$RESULTS_CSV"
echo "${slug},${METHOD},${MODEL},${COST},${TURNS},,${RUN_DIR}" >> "$RESULTS_CSV"
echo "${slug} | ${METHOD} | ${MODEL} | \$${COST} | turns=${TURNS} | dir=${RUN_DIR}"
echo "  -> now VERIFY: cd '${RUN_DIR}' && <gate: node --test | python -m pytest>  (then fill the gate column in runs/results.csv)"
