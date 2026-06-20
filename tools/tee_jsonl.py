#!/usr/bin/env python3
"""
Read JSONL from stdin (one event per line, as emitted by `claude --output-format stream-json`
or `codex exec --json`).

For each event:
  - Append fields `_ts` (ISO-8601 wall clock) and `_elapsed_s` (seconds since this script started).
  - Write the augmented event to <log_path> (one JSON object per line).
  - Print a concise human-readable progress line to stderr (so the user can watch live).

Usage in pipeline:
    claude ... --output-format stream-json --verbose \
        | python3 tee_jsonl.py /path/to/events.jsonl
    codex exec --json ... \
        | python3 tee_jsonl.py /path/to/events.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


def short(s: str, n: int = 80) -> str:
    s = " ".join(s.split())
    return s if len(s) <= n else s[: n - 1] + "…"


def fmt_progress(ev: dict, elapsed: float) -> str | None:
    t = ev.get("type")
    if t == "thread.started":
        return f"[t+{elapsed:6.1f}s] thread  id={ev.get('thread_id')}"
    if t == "turn.started":
        return f"[t+{elapsed:6.1f}s] turn   started"
    if t == "turn.completed":
        usage = ev.get("usage", {}) or {}
        return (
            f"[t+{elapsed:6.1f}s] turn   done  "
            f"in={usage.get('input_tokens', 0)} "
            f"cached={usage.get('cached_input_tokens', 0)} "
            f"out={usage.get('output_tokens', 0)} "
            f"reason={usage.get('reasoning_output_tokens', 0)}"
        )
    if t == "item.started":
        item = ev.get("item", {}) or {}
        it = item.get("type")
        if it == "command_execution":
            return f"[t+{elapsed:6.1f}s] cmd    start {short(item.get('command', ''), 120)}"
        return f"[t+{elapsed:6.1f}s] item   start {it or '?'}"
    if t == "item.completed":
        item = ev.get("item", {}) or {}
        it = item.get("type")
        if it == "agent_message":
            return f"[t+{elapsed:6.1f}s] msg    {short(item.get('text', ''), 120)}"
        if it == "command_execution":
            return (
                f"[t+{elapsed:6.1f}s] cmd    exit={item.get('exit_code')} "
                f"{short(item.get('command', ''), 100)}"
            )
        return f"[t+{elapsed:6.1f}s] item   done  {it or '?'}"
    if t == "system" and ev.get("subtype") == "init":
        return f"[t+{elapsed:6.1f}s] init  model={ev.get('model')} tools={len(ev.get('tools', []))}"
    if t == "assistant":
        msg = ev.get("message", {}) or {}
        usage = msg.get("usage", {}) or {}
        inp = usage.get("input_tokens", 0)
        out = usage.get("output_tokens", 0)
        cr = usage.get("cache_read_input_tokens", 0)
        cc = usage.get("cache_creation_input_tokens", 0)
        parts: list[str] = []
        for blk in msg.get("content", []) or []:
            bt = blk.get("type")
            if bt == "text":
                parts.append(f"text({len(blk.get('text',''))}c)")
            elif bt == "thinking":
                parts.append(f"think({len(blk.get('thinking',''))}c)")
            elif bt == "tool_use":
                parts.append(f"tool={blk.get('name')}")
        body = " ".join(parts) or "(empty)"
        return (
            f"[t+{elapsed:6.1f}s] asst  "
            f"in={inp} out={out} cache_r={cr} cache_c={cc}  {short(body, 100)}"
        )
    if t == "user":
        msg = ev.get("message", {}) or {}
        for blk in msg.get("content", []) or []:
            if blk.get("type") == "tool_result":
                content = blk.get("content")
                if isinstance(content, list):
                    text = " ".join(
                        c.get("text", "") for c in content if isinstance(c, dict)
                    )
                else:
                    text = str(content or "")
                err = " ERR" if blk.get("is_error") else ""
                return f"[t+{elapsed:6.1f}s] tool_result{err}  {short(text, 100)}"
    if t == "result":
        # Gemini's result event uses a "stats" sub-object; Anthropic/Codex put
        # the same fields at the top level. Try both shapes.
        stats = ev.get("stats", {}) or {}
        if stats:
            return (
                f"[t+{elapsed:6.1f}s] DONE  "
                f"in={stats.get('input_tokens', 0)} "
                f"cached={stats.get('cached', 0)} "
                f"out={stats.get('output_tokens', 0)} "
                f"tool_calls={stats.get('tool_calls', 0)} "
                f"dur={stats.get('duration_ms', 0)/1000:.1f}s"
            )
        return (
            f"[t+{elapsed:6.1f}s] DONE  "
            f"turns={ev.get('num_turns')} "
            f"duration={ev.get('duration_ms', 0)/1000:.1f}s "
            f"api={ev.get('duration_api_ms', 0)/1000:.1f}s "
            f"cost=${ev.get('total_cost_usd', 0):.4f} "
            f"err={ev.get('is_error')}"
        )

    # ---------- Gemini CLI flat-event shapes ----------
    if t == "init" and "session_id" in ev:
        return f"[t+{elapsed:6.1f}s] init   model={ev.get('model')} session={short(ev.get('session_id',''), 36)}"
    if t == "tool_use" and "tool_name" in ev:
        params = ev.get("parameters", {}) or {}
        # Pick the most informative single field per common tool
        tool = ev.get("tool_name", "?")
        hint = (
            params.get("file_path")
            or params.get("absolute_path")
            or params.get("dir_path")
            or params.get("command")
            or params.get("title")
            or ""
        )
        if isinstance(hint, list):
            hint = " ".join(str(x) for x in hint)
        return f"[t+{elapsed:6.1f}s] tool   {tool:<22} {short(hint, 90)}"
    if t == "tool_result" and "tool_id" in ev:
        st = ev.get("status", "?")
        return f"[t+{elapsed:6.1f}s] tres   status={st}"
    if t == "message" and ev.get("role") == "assistant":
        # Gemini streams assistant text in many delta chunks. Don't spam — only
        # surface the *first* delta of a streaming run as "asst streaming…",
        # then the *non-delta* (final) message if one is emitted.
        if ev.get("delta"):
            # Suppress delta chunks individually; they're noise.
            return None
        text = ev.get("content", "") or ""
        return f"[t+{elapsed:6.1f}s] asst   {short(text, 100)}"

    return None


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser()
    ap.add_argument("log_path")
    ap.add_argument("--workspace")
    ap.add_argument("--snapshot-dir")
    ap.add_argument("--file-change-manifest")
    return ap.parse_args()


def maybe_capture_file_changes(
    ev: dict,
    workspace: Path | None,
    snapshot_dir: Path | None,
    manifest_path: Path | None,
    event_index: int,
) -> None:
    if not workspace or not snapshot_dir or not manifest_path:
        return
    if ev.get("type") not in ("item.started", "item.completed"):
        return
    item = ev.get("item", {}) or {}
    if item.get("type") != "file_change":
        return

    workspace = workspace.resolve()
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    changes = item.get("changes", []) or []
    item_id = item.get("id", f"item_{event_index}")
    phase = "before" if ev.get("type") == "item.started" else "after"

    with manifest_path.open("a", encoding="utf-8") as mf:
        for idx, change in enumerate(changes, start=1):
            raw_path = str(change.get("path", "") or "")
            kind = str(change.get("kind", "") or "update")
            p = Path(raw_path)
            if not p.is_absolute():
                p = workspace / p
            try:
                resolved = p.resolve(strict=False)
            except OSError:
                resolved = p

            try:
                rel_path = str(resolved.relative_to(workspace))
            except ValueError:
                rel_path = resolved.name or raw_path or f"change_{idx}"

            snapshot_rel = None
            # The agent mutates files concurrently (scaffold pivots, npm
            # install), so a path can vanish between is_file() and stat().
            # Treat any such race as "gone" rather than letting the
            # FileNotFoundError crash the logger and break codex's stdout pipe.
            try:
                exists_now = resolved.is_file()
                size_bytes = resolved.stat().st_size if exists_now else 0
            except OSError:
                exists_now = False
                size_bytes = 0
            if exists_now:
                snap_target = snapshot_dir / f"{event_index:05d}_{item_id}_{idx}" / rel_path
                snap_target.parent.mkdir(parents=True, exist_ok=True)
                try:
                    snap_target.write_bytes(resolved.read_bytes())
                    snapshot_rel = str(snap_target.relative_to(snapshot_dir))
                except OSError:
                    snapshot_rel = None

            rec = {
                "event_index": event_index,
                "item_id": item_id,
                "phase": phase,
                "ts": ev.get("_ts"),
                "elapsed_s": ev.get("_elapsed_s"),
                "raw_path": raw_path,
                "resolved_path": str(resolved),
                "rel_path": rel_path,
                "kind": kind,
                "exists_after": exists_now,
                "size_after_bytes": size_bytes,
                "snapshot_rel": snapshot_rel,
            }
            mf.write(json.dumps(rec, ensure_ascii=False) + "\n")


def write_baseline_snapshot(
    workspace: Path | None,
    snapshot_dir: Path | None,
    manifest_path: Path | None,
) -> None:
    if not workspace or not snapshot_dir or not manifest_path or not workspace.exists():
        return
    workspace = workspace.resolve()
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("a", encoding="utf-8") as mf:
        for p in sorted(x for x in workspace.rglob("*") if x.is_file()):
            rel_path = str(p.relative_to(workspace))
            snap_target = snapshot_dir / "00000_baseline" / rel_path
            snap_target.parent.mkdir(parents=True, exist_ok=True)
            try:
                snap_target.write_bytes(p.read_bytes())
            except OSError:
                continue
            rec = {
                "event_index": 0,
                "item_id": "baseline",
                "phase": "baseline",
                "ts": None,
                "elapsed_s": 0.0,
                "raw_path": str(p),
                "resolved_path": str(p.resolve(strict=False)),
                "rel_path": rel_path,
                "kind": "baseline",
                "exists_after": True,
                "size_after_bytes": p.stat().st_size,
                "snapshot_rel": str(snap_target.relative_to(snapshot_dir)),
            }
            mf.write(json.dumps(rec, ensure_ascii=False) + "\n")


def main() -> int:
    args = parse_args()
    log_path = Path(args.log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    workspace = Path(args.workspace).resolve() if args.workspace else None
    snapshot_dir = Path(args.snapshot_dir) if args.snapshot_dir else None
    manifest_path = Path(args.file_change_manifest) if args.file_change_manifest else None
    write_baseline_snapshot(workspace, snapshot_dir, manifest_path)

    started = time.monotonic()
    with log_path.open("w", encoding="utf-8") as fout:
        event_index = 0
        for raw in sys.stdin:
            line = raw.rstrip("\n")
            if not line.strip():
                continue
            elapsed = time.monotonic() - started
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                # Pass through unrecognised lines (e.g., warnings) as-is wrapped.
                ev = {"type": "_raw", "raw": line}
            ev["_ts"] = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
            ev["_elapsed_s"] = round(elapsed, 3)
            event_index += 1
            fout.write(json.dumps(ev, ensure_ascii=False) + "\n")
            fout.flush()
            # File-change snapshotting is best-effort telemetry; it must never
            # crash the tee, or codex's stdout pipe breaks and the whole run
            # dies mid-task. Swallow any error and keep streaming events.
            try:
                maybe_capture_file_changes(
                    ev,
                    workspace=workspace,
                    snapshot_dir=snapshot_dir,
                    manifest_path=manifest_path,
                    event_index=event_index,
                )
            except Exception as e:
                print(f"[tee_jsonl] file-change capture skipped: {e}",
                      file=sys.stderr, flush=True)
            msg = fmt_progress(ev, elapsed)
            if msg:
                print(msg, file=sys.stderr, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
