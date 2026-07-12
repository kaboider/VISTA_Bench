#!/usr/bin/env python3
"""
Post-run analysis of a Codex CLI eval run.

Reads <run_dir>/logs/codex_events.jsonl and writes:
  - <run_dir>/logs/summary.json      machine-readable totals + per-turn/item breakdown
  - <run_dir>/logs/summary.md        human-readable summary
  - <run_dir>/logs/turns.csv         one row per completed turn
  - <run_dir>/logs/items.csv         one row per completed item
  - <run_dir>/logs/transcript.md     concatenated assistant text + command executions

Usage:
    python3 analyze_codex_run.py <run_dir>
"""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


def load_events(jsonl_path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    with jsonl_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return events


def load_meta(run_dir: Path) -> dict[str, Any]:
    meta_path = run_dir / "meta.json"
    if not meta_path.exists():
        return {}
    try:
        return json.loads(meta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def short(s: str, n: int = 160) -> str:
    s = " ".join((s or "").split())
    return s if len(s) <= n else s[: n - 1] + "…"


def analyze(events: list[dict[str, Any]], meta: dict[str, Any]) -> dict[str, Any]:
    thread_id = None
    turns: list[dict[str, Any]] = []
    items: list[dict[str, Any]] = []
    item_type_counts: Counter[str] = Counter()
    command_prefix_counts: Counter[str] = Counter()

    total_usage = {
        "input_tokens": 0,
        "cached_input_tokens": 0,
        "output_tokens": 0,
        "reasoning_output_tokens": 0,
    }

    current_turn: dict[str, Any] | None = None
    turn_idx = 0
    item_idx = 0

    for ev in events:
        ev_type = ev.get("type")
        if ev_type == "thread.started":
            thread_id = ev.get("thread_id")
            continue

        if ev_type == "turn.started":
            turn_idx += 1
            current_turn = {
                "turn": turn_idx,
                "started_ts": ev.get("_ts"),
                "started_elapsed_s": ev.get("_elapsed_s", 0.0) or 0.0,
                "completed_ts": None,
                "completed_elapsed_s": None,
                "duration_s": None,
                "assistant_messages": [],
                "command_executions": [],
                "completed_item_types": [],
                "usage": {},
            }
            continue

        if ev_type == "item.completed":
            item = ev.get("item", {}) or {}
            item_type = item.get("type") or "unknown"
            item_idx += 1
            item_type_counts[item_type] += 1
            normalized = {
                "seq": item_idx,
                "turn": turn_idx if current_turn else None,
                "event_ts": ev.get("_ts"),
                "elapsed_s": ev.get("_elapsed_s", 0.0) or 0.0,
                "item_id": item.get("id"),
                "item_type": item_type,
                "text": "",
                "text_chars": 0,
                "command": "",
                "command_prefix": "",
                "exit_code": None,
                "status": item.get("status"),
                "output_chars": 0,
                "output_excerpt": "",
            }
            if item_type == "agent_message":
                text = item.get("text", "") or ""
                normalized["text"] = text
                normalized["text_chars"] = len(text)
                if current_turn:
                    current_turn["assistant_messages"].append(text)
            elif item_type == "command_execution":
                command = item.get("command", "") or ""
                output = item.get("aggregated_output", "") or ""
                prefix = command.split()[0] if command.split() else ""
                normalized["command"] = command
                normalized["command_prefix"] = prefix
                normalized["exit_code"] = item.get("exit_code")
                normalized["output_chars"] = len(output)
                normalized["output_excerpt"] = short(output)
                if prefix:
                    command_prefix_counts[prefix] += 1
                if current_turn:
                    current_turn["command_executions"].append(
                        {
                            "command": command,
                            "exit_code": item.get("exit_code"),
                            "status": item.get("status"),
                            "output": output,
                        }
                    )
            else:
                if "text" in item and isinstance(item["text"], str):
                    normalized["text"] = item["text"]
                    normalized["text_chars"] = len(item["text"])
            items.append(normalized)
            if current_turn:
                current_turn["completed_item_types"].append(item_type)
            continue

        if ev_type == "turn.completed":
            usage = ev.get("usage", {}) or {}
            for key in total_usage:
                total_usage[key] += usage.get(key, 0) or 0
            if current_turn is not None:
                current_turn["completed_ts"] = ev.get("_ts")
                current_turn["completed_elapsed_s"] = ev.get("_elapsed_s", 0.0) or 0.0
                current_turn["duration_s"] = round(
                    current_turn["completed_elapsed_s"] - current_turn["started_elapsed_s"],
                    3,
                )
                current_turn["usage"] = {
                    "input_tokens": usage.get("input_tokens", 0),
                    "cached_input_tokens": usage.get("cached_input_tokens", 0),
                    "output_tokens": usage.get("output_tokens", 0),
                    "reasoning_output_tokens": usage.get("reasoning_output_tokens", 0),
                }
                turns.append(current_turn)
                current_turn = None

    final_message = ""
    for item in reversed(items):
        if item["item_type"] == "agent_message" and item["text"].strip():
            final_message = item["text"]
            break

    summary = {
        "thread_id": thread_id,
        "cli": meta.get("cli", "codex"),
        "model": meta.get("model"),
        "task": meta.get("task"),
        "variant": meta.get("variant"),
        "run_id": meta.get("run_id"),
        "turn_count": len(turns),
        "item_count": len(items),
        "assistant_message_count": item_type_counts.get("agent_message", 0),
        "command_execution_count": item_type_counts.get("command_execution", 0),
        "item_type_counts": dict(item_type_counts),
        "command_prefix_counts": dict(command_prefix_counts),
        "tokens": total_usage,
        "final_message_excerpt": short(final_message, 500),
        "wall_clock_first_to_last_turn_s": (
            round(
                (turns[-1]["completed_elapsed_s"] or 0.0) - (turns[0]["started_elapsed_s"] or 0.0),
                3,
            )
            if turns
            else 0.0
        ),
    }
    return {"summary": summary, "turns": turns, "items": items}


def write_outputs(run_dir: Path, analysis: dict[str, Any]) -> None:
    logs = run_dir / "logs"
    logs.mkdir(exist_ok=True)
    summary = analysis["summary"]
    turns = analysis["turns"]
    items = analysis["items"]

    (logs / "summary.json").write_text(
        json.dumps(analysis, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    with (logs / "turns.csv").open("w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "turn",
            "started_ts",
            "completed_ts",
            "started_elapsed_s",
            "completed_elapsed_s",
            "duration_s",
            "assistant_message_count",
            "command_execution_count",
            "completed_item_types",
            "input_tokens",
            "cached_input_tokens",
            "output_tokens",
            "reasoning_output_tokens",
        ]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for t in turns:
            usage = t.get("usage", {}) or {}
            w.writerow(
                {
                    "turn": t["turn"],
                    "started_ts": t["started_ts"],
                    "completed_ts": t["completed_ts"],
                    "started_elapsed_s": t["started_elapsed_s"],
                    "completed_elapsed_s": t["completed_elapsed_s"],
                    "duration_s": t["duration_s"],
                    "assistant_message_count": len(t.get("assistant_messages", [])),
                    "command_execution_count": len(t.get("command_executions", [])),
                    "completed_item_types": ",".join(t.get("completed_item_types", [])),
                    "input_tokens": usage.get("input_tokens", 0),
                    "cached_input_tokens": usage.get("cached_input_tokens", 0),
                    "output_tokens": usage.get("output_tokens", 0),
                    "reasoning_output_tokens": usage.get("reasoning_output_tokens", 0),
                }
            )

    with (logs / "items.csv").open("w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "seq",
            "turn",
            "event_ts",
            "elapsed_s",
            "item_id",
            "item_type",
            "text_chars",
            "command",
            "command_prefix",
            "exit_code",
            "status",
            "output_chars",
            "output_excerpt",
        ]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for item in items:
            w.writerow({k: item.get(k) for k in fieldnames})

    md_lines: list[str] = []
    md_lines.append("# Run summary\n")
    md_lines.append(f"- Run: `{summary['run_id']}`")
    md_lines.append(f"- Task / Variant: `{summary['task']}` / `{summary['variant']}`")
    md_lines.append(f"- Thread: `{summary['thread_id']}`")
    md_lines.append(f"- Model: `{summary['model']}`")
    md_lines.append(f"- Turns: {summary['turn_count']}")
    md_lines.append(f"- Items: {summary['item_count']}")
    md_lines.append(f"- Assistant messages: {summary['assistant_message_count']}")
    md_lines.append(f"- Command executions: {summary['command_execution_count']}")
    md_lines.append(
        f"- First→last turn wall time: {summary['wall_clock_first_to_last_turn_s']:.1f}s"
    )
    tk = summary["tokens"]
    md_lines.append(
        "\n## Token totals\n"
        f"- input: {tk['input_tokens']}\n"
        f"- cached_input: {tk['cached_input_tokens']}\n"
        f"- output: {tk['output_tokens']}\n"
        f"- reasoning_output: {tk['reasoning_output_tokens']}\n"
    )
    if summary["command_prefix_counts"]:
        md_lines.append("## Command prefixes")
        for name, cnt in sorted(
            summary["command_prefix_counts"].items(), key=lambda kv: (-kv[1], kv[0])
        ):
            md_lines.append(f"- {name}: {cnt}")
        md_lines.append("")
    md_lines.append("## Per-turn breakdown")
    md_lines.append(
        "| # | t_start (s) | dur (s) | msgs | cmds | in | cached | out | reason | items |"
    )
    md_lines.append("|---|------------:|--------:|-----:|-----:|---:|-------:|----:|-------:|------|")
    for t in turns:
        usage = t.get("usage", {}) or {}
        md_lines.append(
            f"| {t['turn']} | {t['started_elapsed_s']:.1f} | {t['duration_s']:.1f} | "
            f"{len(t.get('assistant_messages', []))} | {len(t.get('command_executions', []))} | "
            f"{usage.get('input_tokens', 0)} | {usage.get('cached_input_tokens', 0)} | "
            f"{usage.get('output_tokens', 0)} | {usage.get('reasoning_output_tokens', 0)} | "
            f"{','.join(t.get('completed_item_types', []))} |"
        )
    if summary["final_message_excerpt"]:
        md_lines.append("\n## Final message excerpt\n")
        md_lines.append(summary["final_message_excerpt"])
    (logs / "summary.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    tx: list[str] = ["# Transcript\n"]
    for t in turns:
        tx.append(
            f"\n---\n## Turn {t['turn']} "
            f"(t+{t['started_elapsed_s']:.1f}s, duration {t['duration_s']:.1f}s)\n"
        )
        for msg in t.get("assistant_messages", []):
            tx.append(f"### Assistant\n\n{msg}\n")
        for cmd in t.get("command_executions", []):
            tx.append(
                "### Command\n\n"
                f"```bash\n{cmd.get('command', '')}\n```\n\n"
                f"- exit_code: {cmd.get('exit_code')}\n"
                f"- status: {cmd.get('status')}\n"
            )
            output = cmd.get("output", "")
            if output:
                tx.append(f"\n```text\n{output}\n```\n")
    (logs / "transcript.md").write_text("\n".join(tx), encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: analyze_codex_run.py <run_dir>", file=sys.stderr)
        return 2
    run_dir = Path(sys.argv[1])
    events_path = run_dir / "logs" / "codex_events.jsonl"
    if not events_path.exists():
        print(f"No codex_events.jsonl at {events_path}", file=sys.stderr)
        return 1
    analysis = analyze(load_events(events_path), load_meta(run_dir))
    write_outputs(run_dir, analysis)
    s = analysis["summary"]
    tk = s["tokens"]
    print(
        "summary.json/.md, turns.csv, items.csv, transcript.md written. "
        f"turns={s['turn_count']} items={s['item_count']} "
        f"in={tk['input_tokens']} cached={tk['cached_input_tokens']} "
        f"out={tk['output_tokens']} reason={tk['reasoning_output_tokens']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
