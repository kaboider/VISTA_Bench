#!/usr/bin/env bash
#
# run_eval_cursor.sh — thin wrapper around run_eval.sh, fixed to --cli cursor.
# Same flag surface as run_eval.sh (e.g. --task, --variant, --model).
#
# Auth: run `cursor-agent login` once (subscription OAuth) — OR set CURSOR_API_KEY.
# Default model: composer-2.5  (override with --model, e.g. --model composer-2.5-fast).
# Install: curl https://cursor.com/install -fsS | bash   (lands at ~/.local/bin/cursor-agent)
#
exec "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_eval.sh" --cli cursor "$@"
