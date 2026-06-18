#!/usr/bin/env bash
#
# run_eval_codex.sh — thin wrapper around run_eval.sh, fixed to --cli codex.
# Same flag surface as run_eval.sh (e.g. --task, --variant, --model).
#
# Auth: `codex /login` (OAuth, subscription) — OR set OPENAI_API_KEY.
#
exec "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_eval.sh" --cli codex "$@"
