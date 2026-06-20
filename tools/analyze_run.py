#!/usr/bin/env python3
"""
Post-run analysis of a Claude CLI eval run.

Reads <run_dir>/logs/events.jsonl (produced by tee_jsonl.py) and writes:
  - <run_dir>/logs/summary.json      machine-readable totals + per-turn breakdown
  - <run_dir>/logs/summary.md        human-readable summary
  - <run_dir>/logs/turns.csv         one row per assistant turn for spreadsheet analysis
  - <run_dir>/logs/transcript.md     concatenated text + thinking + tool calls

Usage:
    python3 analyze_run.py <run_dir>
"""

from __future__ import annotations

import csv
import json
import sys
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


def safe(d: dict | None, *keys, default=None):
    cur: Any = d or {}
    for k in keys:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(k)
        if cur is None:
            return default
    return cur


def analyze(events: list[dict[str, Any]]) -> dict[str, Any]:
    init = next(
        (e for e in events if e.get("type") == "system" and e.get("subtype") == "init"),
        None,
    )
    result = next((e for e in events if e.get("type") == "result"), None)

    turns: list[dict[str, Any]] = []
    last_t = 0.0
    cumulative = {
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
    }
    tool_counts: dict[str, int] = {}

    turn_idx = 0
    for ev in events:
        if ev.get("type") != "assistant":
            continue
        msg = ev.get("message", {}) or {}
        usage = msg.get("usage", {}) or {}
        text_chars = 0
        think_chars = 0
        tools_in_turn: list[str] = []
        text_snippets: list[str] = []
        thinking_snippets: list[str] = []
        for blk in msg.get("content", []) or []:
            bt = blk.get("type")
            if bt == "text":
                t = blk.get("text", "")
                text_chars += len(t)
                text_snippets.append(t)
            elif bt == "thinking":
                t = blk.get("thinking", "")
                think_chars += len(t)
                thinking_snippets.append(t)
            elif bt == "tool_use":
                name = blk.get("name", "?")
                tools_in_turn.append(name)
                tool_counts[name] = tool_counts.get(name, 0) + 1
        elapsed = ev.get("_elapsed_s", 0.0) or 0.0
        delta = max(0.0, elapsed - last_t)
        last_t = elapsed
        turn_idx += 1
        turns.append(
            {
                "turn": turn_idx,
                "ts": ev.get("_ts"),
                "elapsed_s": elapsed,
                "delta_s": round(delta, 3),
                "stop_reason": msg.get("stop_reason"),
                "input_tokens": usage.get("input_tokens", 0),
                "output_tokens": usage.get("output_tokens", 0),
                "cache_read_input_tokens": usage.get("cache_read_input_tokens", 0),
                "cache_creation_input_tokens": usage.get(
                    "cache_creation_input_tokens", 0
                ),
                "service_tier": usage.get("service_tier"),
                "text_chars": text_chars,
                "thinking_chars": think_chars,
                "tools": tools_in_turn,
                "text": "\n".join(text_snippets),
                "thinking": "\n".join(thinking_snippets),
            }
        )
        for k in cumulative:
            cumulative[k] += usage.get(k, 0) or 0

    summary = {
        "session_id": safe(init, "session_id"),
        "model": safe(init, "model"),
        "permission_mode": safe(init, "permissionMode"),
        "tools_available_count": len(safe(init, "tools", default=[]) or []),
        "num_turns": safe(result, "num_turns"),
        "duration_ms": safe(result, "duration_ms"),
        "duration_api_ms": safe(result, "duration_api_ms"),
        "is_error": safe(result, "is_error"),
        "total_cost_usd": safe(result, "total_cost_usd"),
        "result_text_excerpt": (safe(result, "result") or "")[:500],
        "tokens": {
            **cumulative,
            "total_input_billable": cumulative["input_tokens"]
            + cumulative["cache_creation_input_tokens"],
        },
        "tool_call_counts": tool_counts,
        "turn_count": len(turns),
        "wall_clock_first_to_last_assistant_s": (
            round(turns[-1]["elapsed_s"] - turns[0]["elapsed_s"], 3) if turns else 0
        ),
    }
    return {"summary": summary, "turns": turns}


def write_outputs(run_dir: Path, analysis: dict[str, Any]) -> None:
    logs = run_dir / "logs"
    logs.mkdir(exist_ok=True)
    summary = analysis["summary"]
    turns = analysis["turns"]

    # JSON
    (logs / "summary.json").write_text(
        json.dumps(analysis, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # CSV (one row per assistant turn)
    csv_path = logs / "turns.csv"
    fieldnames = [
        "turn",
        "ts",
        "elapsed_s",
        "delta_s",
        "stop_reason",
        "input_tokens",
        "output_tokens",
        "cache_read_input_tokens",
        "cache_creation_input_tokens",
        "text_chars",
        "thinking_chars",
        "tools",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for t in turns:
            row = {k: t.get(k) for k in fieldnames}
            row["tools"] = ",".join(t.get("tools") or [])
            w.writerow(row)

    # Markdown summary
    md_lines: list[str] = []
    md_lines.append(f"# Run summary\n")
    md_lines.append(f"- Session: `{summary['session_id']}`")
    md_lines.append(f"- Model: `{summary['model']}`")
    md_lines.append(f"- Permission mode: `{summary['permission_mode']}`")
    md_lines.append(f"- Turns: {summary['num_turns']}")
    md_lines.append(
        f"- Total wall time: {(summary['duration_ms'] or 0)/1000:.1f}s "
        f"(API time {(summary['duration_api_ms'] or 0)/1000:.1f}s)"
    )
    md_lines.append(f"- Total cost (CLI estimate): ${summary['total_cost_usd'] or 0:.4f}")
    md_lines.append(f"- Errored: {summary['is_error']}")
    tk = summary["tokens"]
    md_lines.append(
        f"\n## Token totals\n"
        f"- input: {tk['input_tokens']}\n"
        f"- output: {tk['output_tokens']}\n"
        f"- cache_creation: {tk['cache_creation_input_tokens']}\n"
        f"- cache_read: {tk['cache_read_input_tokens']}\n"
    )
    if summary["tool_call_counts"]:
        md_lines.append("## Tool call counts")
        for name, cnt in sorted(
            summary["tool_call_counts"].items(), key=lambda kv: -kv[1]
        ):
            md_lines.append(f"- {name}: {cnt}")
        md_lines.append("")
    md_lines.append("## Per-turn breakdown")
    md_lines.append(
        "| # | t (s) | Δs | in | out | cache_r | text_c | think_c | tools | stop |"
    )
    md_lines.append("|---|------:|---:|---:|---:|--------:|------:|-------:|------|------|")
    for t in turns:
        md_lines.append(
            f"| {t['turn']} | {t['elapsed_s']:.1f} | {t['delta_s']:.1f} | "
            f"{t['input_tokens']} | {t['output_tokens']} | {t['cache_read_input_tokens']} | "
            f"{t['text_chars']} | {t['thinking_chars']} | {','.join(t['tools'])} | "
            f"{t['stop_reason'] or ''} |"
        )
    (logs / "summary.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    # Transcript (text + thinking + tools)
    tx: list[str] = ["# Transcript\n"]
    for t in turns:
        tx.append(f"\n---\n## Turn {t['turn']} (t+{t['elapsed_s']:.1f}s, +{t['delta_s']:.1f}s)\n")
        if t["thinking"]:
            tx.append(f"### Thinking\n\n```\n{t['thinking']}\n```\n")
        if t["text"]:
            tx.append(f"### Assistant text\n\n{t['text']}\n")
        if t["tools"]:
            tx.append(f"### Tool calls: {', '.join(t['tools'])}\n")
    (logs / "transcript.md").write_text("\n".join(tx), encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: analyze_run.py <run_dir>", file=sys.stderr)
        return 2
    run_dir = Path(sys.argv[1])
    events_path = run_dir / "logs" / "events.jsonl"
    if not events_path.exists():
        print(f"No events.jsonl at {events_path}", file=sys.stderr)
        return 1
    events = load_events(events_path)
    analysis = analyze(events)
    write_outputs(run_dir, analysis)
    s = analysis["summary"]
    tk = s["tokens"]
    print(
        f"summary.json/.md/.csv/transcript.md written. "
        f"turns={s['num_turns']} "
        f"wall={(s['duration_ms'] or 0)/1000:.1f}s "
        f"in={tk['input_tokens']} out={tk['output_tokens']} "
        f"cache_r={tk['cache_read_input_tokens']} "
        f"cost=${s['total_cost_usd'] or 0:.4f}",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
