#!/usr/bin/env bash
#
# run_eval_claude.sh — thin wrapper around run_eval.sh, fixed to --cli claude.
# Same flag surface as run_eval.sh (e.g. --task, --variant, --model).
#
# Auth: log in once with `claude /login` for Max-plan token.
#
exec "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_eval.sh" --cli claude "$@"
