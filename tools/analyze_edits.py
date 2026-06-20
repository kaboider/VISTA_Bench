#!/usr/bin/env python3
"""
analyze_edits.py — per-action edit volume and diff-vs-rewrite ratio.

Supported inputs:
  - Claude: <run_dir>/logs/events.jsonl
  - Codex:  <run_dir>/logs/codex_events.jsonl plus local session logs,
            falling back to codex_file_changes.jsonl plus snapshots

Outputs written to <run_dir>/logs/:
  - edits.jsonl   one record per file-mutating action
  - edits.md      human summary + bottom-line verdict

For Claude we replay Write / Edit / MultiEdit / NotebookEdit tool calls.
For Codex we prefer the local session file's `apply_patch` records when
available, and fall back to file_change snapshots otherwise.

Usage:
    python3 analyze_edits.py <run_dir>
"""

from __future__ import annotations

import difflib
import json
import os
import sys
from pathlib import Path
from statistics import median
from typing import Any


SCAFFOLD_CACHE_DIR = Path(__file__).parent / "scaffold_cache"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def load_all_scaffold_caches() -> list[dict[str, Any]]:
    """Load every <key>.json under scaffold_cache/ except registry.json."""
    caches: list[dict[str, Any]] = []
    if not SCAFFOLD_CACHE_DIR.exists():
        return caches
    for p in sorted(SCAFFOLD_CACHE_DIR.glob("*.json")):
        if p.name == "registry.json":
            continue
        try:
            caches.append(json.loads(p.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, OSError):
            continue
    return caches


def detect_scaffold(blob: str, caches: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Return the scaffold cache whose match_patterns appear in `blob`, or None.

    `blob` is a flat string built from all shell/Bash commands the agent issued.
    Patterns are matched as case-sensitive substrings; first match wins.
    """
    for cache in caches:
        for pat in cache.get("match_patterns", []):
            if pat and pat in blob:
                return cache
    return None


def scaffold_file_set(cache: dict[str, Any] | None) -> set[str]:
    if not cache:
        return set()
    return set(cache.get("files", {}).keys())


def classify_write(
    file_path: str, scaffold_files: set[str], seen_writes: set[str]
) -> str:
    if file_path in scaffold_files:
        return "overwrite_scaffold"
    if file_path in seen_writes:
        return "overwrite_self"
    return "new"


def classify_edit(file_path: str, scaffold_files: set[str]) -> str:
    return "scaffold_edit" if file_path in scaffold_files else "agent_edit"


def line_count(s: str) -> int:
    if not s:
        return 0
    return s.count("\n") + (0 if s.endswith("\n") else 1)


def utf8_len(s: str) -> int:
    return len(s.encode("utf-8", errors="replace"))


def resolve_disk(workspace: Path, file_path: str) -> Path:
    p = Path(file_path)
    return p if p.is_absolute() else workspace / file_path


def disk_size(workspace: Path, file_path: str) -> int:
    p = resolve_disk(workspace, file_path)
    try:
        if p.is_file():
            return p.stat().st_size
    except OSError:
        pass
    return 0


def diff_stats(before: bytes, after: bytes) -> dict[str, int]:
    before_text = before.decode("utf-8", errors="replace")
    after_text = after.decode("utf-8", errors="replace")
    before_lines = before_text.splitlines(keepends=True)
    after_lines = after_text.splitlines(keepends=True)
    sm = difflib.SequenceMatcher(a=before_lines, b=after_lines)
    added_bytes = removed_bytes = 0
    added_lines = removed_lines = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ("replace", "delete"):
            chunk = "".join(before_lines[i1:i2])
            removed_bytes += utf8_len(chunk)
            removed_lines += len(before_lines[i1:i2])
        if tag in ("replace", "insert"):
            chunk = "".join(after_lines[j1:j2])
            added_bytes += utf8_len(chunk)
            added_lines += len(after_lines[j1:j2])
    return {
        "old_bytes": len(before),
        "new_bytes": len(after),
        "added_bytes": added_bytes,
        "removed_bytes": removed_bytes,
        "added_lines": added_lines,
        "removed_lines": removed_lines,
    }


def normalize_rel_path(path_str: str, workspace: Path) -> str:
    p = Path(path_str)
    if p.is_absolute():
        try:
            return str(p.resolve(strict=False).relative_to(workspace.resolve()))
        except ValueError:
            return str(p.resolve(strict=False))
    return str(p)


def patch_line_bytes(s: str) -> int:
    return utf8_len(s + "\n")


def parse_apply_patch_actions(patch_text: str) -> list[dict[str, Any]]:
    lines = patch_text.splitlines()
    actions: list[dict[str, Any]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("*** Add File: "):
            path = line[len("*** Add File: ") :]
            i += 1
            new_b = new_l = 0
            while i < len(lines) and not lines[i].startswith("*** "):
                if lines[i].startswith("+"):
                    new_b += patch_line_bytes(lines[i][1:])
                    new_l += 1
                i += 1
            actions.append(
                {
                    "tool": "Write",
                    "action_class": "write",
                    "file_path": path,
                    "kind": "create",
                    "old_bytes": 0,
                    "new_bytes": new_b,
                    "added_lines": new_l,
                    "removed_lines": 0,
                }
            )
            continue
        if line.startswith("*** Delete File: "):
            path = line[len("*** Delete File: ") :]
            actions.append(
                {
                    "tool": "Delete",
                    "action_class": "delete",
                    "file_path": path,
                    "kind": "delete",
                    "old_bytes": 0,
                    "new_bytes": 0,
                    "added_lines": 0,
                    "removed_lines": 0,
                }
            )
            i += 1
            continue
        if line.startswith("*** Update File: "):
            path = line[len("*** Update File: ") :]
            i += 1
            if i < len(lines) and lines[i].startswith("*** Move to: "):
                i += 1
            old_b = new_b = old_l = new_l = 0
            while i < len(lines) and not lines[i].startswith("*** "):
                cur = lines[i]
                if cur.startswith("+"):
                    new_b += patch_line_bytes(cur[1:])
                    new_l += 1
                elif cur.startswith("-"):
                    old_b += patch_line_bytes(cur[1:])
                    old_l += 1
                i += 1
            actions.append(
                {
                    "tool": "Edit",
                    "action_class": "edit",
                    "file_path": path,
                    "kind": "update",
                    "old_bytes": old_b,
                    "new_bytes": new_b,
                    "added_lines": new_l,
                    "removed_lines": old_l,
                }
            )
            continue
        i += 1
    return actions


def locate_codex_session_file(thread_id: str) -> Path | None:
    codex_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    sessions_root = codex_home / "sessions"
    if not sessions_root.exists():
        return None
    matches = sorted(sessions_root.rglob(f"*{thread_id}.jsonl"))
    return matches[-1] if matches else None


def load_codex_session_apply_patch_actions(
    run_dir: Path, workspace: Path
) -> tuple[list[dict[str, Any]], Path | None]:
    events_path = run_dir / "logs" / "codex_events.jsonl"
    if not events_path.exists():
        return [], None
    events = load_jsonl(events_path)
    thread_id = next((e.get("thread_id") for e in events if e.get("type") == "thread.started"), None)
    if not thread_id:
        return [], None
    session_path = locate_codex_session_file(str(thread_id))
    if not session_path or not session_path.exists():
        return [], None

    actions: list[dict[str, Any]] = []
    for rec in load_jsonl(session_path):
        if rec.get("type") != "response_item":
            continue
        payload = rec.get("payload", {}) or {}
        if payload.get("type") != "custom_tool_call" or payload.get("name") != "apply_patch":
            continue
        call_id = payload.get("call_id")
        patch_text = payload.get("input", "") or ""
        for sub_idx, act in enumerate(parse_apply_patch_actions(patch_text), start=1):
            actions.append(
                {
                    **act,
                    "ts": rec.get("timestamp"),
                    "call_id": call_id,
                    "sub_index": sub_idx,
                    "file_path": normalize_rel_path(act["file_path"], workspace),
                    "source_detail": "session_apply_patch",
                }
            )
    return actions, session_path


def _normalize_tool_input(canonical: str, ti: dict[str, Any]) -> dict[str, Any]:
    """Normalize tool inputs across CLIs into a single Claude-shaped dict.

    Gemini CLI uses snake_case Gemini-native parameter names (e.g.
    `absolute_path` instead of `file_path`, `old_str` / `new_str` for the
    `replace` tool).  Anthropic-shape names are passed through unchanged.
    """
    out = dict(ti)
    if canonical in ("Write", "Edit") and "file_path" not in out and "absolute_path" in out:
        out["file_path"] = out.get("absolute_path")
    if canonical == "Edit":
        # Gemini's `replace` tool uses old_str/new_str.
        if "old_string" not in out and "old_str" in out:
            out["old_string"] = out.get("old_str")
        if "new_string" not in out and "new_str" in out:
            out["new_string"] = out.get("new_str")
    if canonical == "Bash" and "command" not in out:
        # gemini-style sometimes uses {"command": [...]} or {"shell": "..."}
        if "shell" in out:
            out["command"] = out.get("shell")
    return out


# Maps every tool name we want to recognize -> canonical {"Write","Edit","Bash"}.
# Anything missing from this map is ignored (i.e. not file-mutating).
DEFAULT_TOOL_ALIASES: dict[str, str] = {
    # Claude / Anthropic
    "Write": "Write",
    "Edit": "Edit",
    "MultiEdit": "MultiEdit",
    "NotebookEdit": "NotebookEdit",
    "Bash": "Bash",
    # Gemini CLI (snake_case native names emitted via --output-format stream-json)
    "write_file": "Write",
    "edit_file": "Edit",
    "edit": "Edit",
    "replace": "Edit",
    "read_file": "ReadFile",          # not file-mutating; included to short-circuit
    "run_shell_command": "Bash",
    "shell": "Bash",
    # PascalCase aliases sometimes seen in older / wrapper builds (qwen-code etc).
    "WriteFile": "Write",
    "ReadFile": "ReadFile",
}


def analyze_anthropic_stream(
    events: list[dict[str, Any]],
    workspace: Path,
    scaffold_caches: list[dict[str, Any]] | None = None,
    *,
    source: str = "claude",
    tool_aliases: dict[str, str] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    """Parse an Anthropic-shaped stream-json event log.

    Used directly by Claude Code (events.jsonl).  Gemini CLI's flat events
    are converted to this shape by `_gemini_to_anthropic_envelope` first.
    Tool name differences across CLIs are handled via `tool_aliases`.
    """
    sizes: dict[str, int] = {}
    actions: list[dict[str, Any]] = []
    turn_idx = 0
    scaffold_caches = scaffold_caches or []
    aliases = tool_aliases or DEFAULT_TOOL_ALIASES

    # Pass 1: collect every shell command (whatever its tool is named) and detect a scaffold.
    shell_blob_parts: list[str] = []
    for ev in events:
        if ev.get("type") != "assistant":
            continue
        for blk in (ev.get("message", {}) or {}).get("content", []) or []:
            if blk.get("type") != "tool_use":
                continue
            canonical = aliases.get(blk.get("name") or "")
            if canonical != "Bash":
                continue
            ti_norm = _normalize_tool_input("Bash", blk.get("input", {}) or {})
            cmd = ti_norm.get("command", "") or ""
            if isinstance(cmd, list):
                cmd = " ".join(str(c) for c in cmd)
            if cmd:
                shell_blob_parts.append(cmd)
    scaffold_cache = detect_scaffold("\n".join(shell_blob_parts), scaffold_caches)
    scaffold_files = scaffold_file_set(scaffold_cache)
    seen_writes: set[str] = set()

    for ev in events:
        if ev.get("type") != "assistant":
            continue
        turn_idx += 1
        msg = ev.get("message", {}) or {}
        for blk in msg.get("content", []) or []:
            if blk.get("type") != "tool_use":
                continue
            raw_name = blk.get("name") or ""
            name = aliases.get(raw_name)
            if name is None or name == "ReadFile":
                continue  # not in our edit-tracking universe
            ti = _normalize_tool_input(name, blk.get("input", {}) or {})

            if name == "Write":
                fp = ti.get("file_path", "") or ""
                content = ti.get("content", "") or ""
                after_b = utf8_len(content)
                prev_b = sizes.get(fp, 0)
                is_new = fp not in sizes
                write_kind = classify_write(fp, scaffold_files, seen_writes)
                actions.append(
                    {
                        "source": source,
                        "turn": turn_idx,
                        "tool": raw_name or "Write",
                        "action_class": "write",
                        "write_kind": write_kind,
                        "file_path": fp,
                        "kind": "write",
                        "is_new_file": is_new and write_kind != "overwrite_scaffold",
                        "is_full_rewrite": True,
                        "old_bytes": prev_b,
                        "new_bytes": after_b,
                        "added_lines": line_count(content),
                        "removed_lines": None if is_new else "unknown",
                        "before_bytes": prev_b,
                        "after_bytes": after_b,
                        "change_bytes": max(prev_b, after_b),
                        "ratio": 1.0,
                        "scaffold_inferred": False,
                    }
                )
                sizes[fp] = after_b
                seen_writes.add(fp)

            elif name in ("Edit", "MultiEdit"):
                fp = ti.get("file_path", "") or ""
                sub = (
                    [
                        {
                            "old_string": ti.get("old_string", "") or "",
                            "new_string": ti.get("new_string", "") or "",
                        }
                    ]
                    if name == "Edit"
                    else (ti.get("edits", []) or [])
                )
                old_b = new_b = old_l = new_l = 0
                for e in sub:
                    o = e.get("old_string", "") or ""
                    n = e.get("new_string", "") or ""
                    old_b += utf8_len(o)
                    new_b += utf8_len(n)
                    old_l += line_count(o)
                    new_l += line_count(n)
                scaffold_inferred = False
                if fp in sizes:
                    prev_b = sizes[fp]
                else:
                    prev_b = disk_size(workspace, fp)
                    scaffold_inferred = True
                after_b = max(0, prev_b - old_b + new_b)
                change_b = max(old_b, new_b)
                actions.append(
                    {
                        "source": source,
                        "turn": turn_idx,
                        "tool": raw_name or name,
                        "action_class": "edit",
                        "edit_kind": classify_edit(fp, scaffold_files),
                        "file_path": fp,
                        "kind": "edit",
                        "is_new_file": False,
                        "is_full_rewrite": False,
                        "old_bytes": old_b,
                        "new_bytes": new_b,
                        "added_lines": new_l,
                        "removed_lines": old_l,
                        "before_bytes": prev_b,
                        "after_bytes": after_b,
                        "change_bytes": change_b,
                        "ratio": round((change_b / after_b) if after_b > 0 else 0.0, 4),
                        "sub_edit_count": len(sub),
                        "scaffold_inferred": scaffold_inferred,
                    }
                )
                sizes[fp] = after_b

            elif name == "NotebookEdit":
                fp = ti.get("notebook_path", "") or ""
                new = ti.get("new_source", "") or ""
                new_b = utf8_len(new)
                prev_b = sizes.get(fp, 0)
                after_b = prev_b + new_b
                actions.append(
                    {
                        "source": source,
                        "turn": turn_idx,
                        "tool": "NotebookEdit",
                        "action_class": "edit",
                        "edit_kind": classify_edit(fp, scaffold_files),
                        "file_path": fp,
                        "kind": "notebook_edit",
                        "is_new_file": fp not in sizes,
                        "is_full_rewrite": False,
                        "old_bytes": 0,
                        "new_bytes": new_b,
                        "added_lines": line_count(new),
                        "removed_lines": "unknown",
                        "before_bytes": prev_b,
                        "after_bytes": after_b,
                        "change_bytes": new_b,
                        "ratio": round((new_b / after_b) if after_b > 0 else 0.0, 4),
                        "scaffold_inferred": False,
                    }
                )
                sizes[fp] = after_b

    return actions, scaffold_cache


def analyze_claude(
    events: list[dict[str, Any]],
    workspace: Path,
    scaffold_caches: list[dict[str, Any]] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    """Backward-compat wrapper: parse a Claude events.jsonl stream."""
    return analyze_anthropic_stream(
        events, workspace, scaffold_caches, source="claude"
    )


def _gemini_to_anthropic_envelope(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Adapt Gemini CLI's flat stream-json events into Anthropic-shaped events.

    Gemini CLI emits records like:
        {"type": "tool_use", "tool_name": "write_file",
         "parameters": {"file_path": "...", "content": "..."},
         "tool_id": "...", "timestamp": "..."}

    Claude / wrapped-Qwen emit nested envelopes:
        {"type": "assistant",
         "message": {"role": "assistant",
                     "content": [{"type": "tool_use",
                                  "name": "WriteFile",
                                  "input": {...}}]}}

    `analyze_anthropic_stream` only knows how to walk the nested envelope, so
    we wrap each flat tool_use event into one assistant turn before delegating.
    Non-tool events are passed through unchanged.
    """
    out: list[dict[str, Any]] = []
    for ev in events:
        if not isinstance(ev, dict):
            continue
        t = ev.get("type")
        # Already in nested envelope shape — pass through
        if t in ("assistant", "user", "system", "result"):
            out.append(ev)
            continue
        # Flat tool_use event — wrap it
        if t == "tool_use" and ("tool_name" in ev or "name" in ev):
            tool_name = ev.get("tool_name") or ev.get("name") or ""
            tool_input = ev.get("parameters") or ev.get("input") or {}
            out.append(
                {
                    "type": "assistant",
                    "message": {
                        "role": "assistant",
                        "content": [
                            {
                                "type": "tool_use",
                                "name": tool_name,
                                "input": tool_input,
                            }
                        ],
                    },
                }
            )
            continue
        # Anything else (text deltas, telemetry, etc.) — ignore
    return out


def analyze_gemini(
    events: list[dict[str, Any]],
    workspace: Path,
    scaffold_caches: list[dict[str, Any]] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    """Parse a Gemini CLI gemini_events.jsonl stream.

    Gemini CLI's `--output-format stream-json` (>= v0.11) writes flat tool_use
    events; we adapt them to Anthropic shape and delegate to the shared parser.
    Tool names (`write_file`, `replace`, `run_shell_command`, ...) and parameter
    aliases (`absolute_path`, `old_str`/`new_str`) are already covered by
    DEFAULT_TOOL_ALIASES + _normalize_tool_input.
    """
    wrapped = _gemini_to_anthropic_envelope(events)
    return analyze_anthropic_stream(
        wrapped, workspace, scaffold_caches, source="gemini"
    )


def analyze_codex(
    run_dir: Path, scaffold_caches: list[dict[str, Any]] | None = None
) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    logs = run_dir / "logs"
    manifest_path = logs / "codex_file_changes.jsonl"
    snapshot_dir = logs / "codex_file_snapshots"
    changes = load_jsonl(manifest_path)
    workspace = run_dir / "workspace"
    scaffold_caches = scaffold_caches or []

    def read_snapshot(snapshot_rel: str | None) -> bytes:
        if not snapshot_rel:
            return b""
        try:
            return (snapshot_dir / snapshot_rel).read_bytes()
        except OSError:
            return b""

    state_by_path: dict[str, bytes] = {}
    for ch in changes:
        rel_path = ch.get("rel_path") or ch.get("raw_path") or "unknown"
        if ch.get("phase") == "baseline":
            state_by_path[rel_path] = read_snapshot(ch.get("snapshot_rel"))
    session_actions, session_path = load_codex_session_apply_patch_actions(run_dir, workspace)

    # Detect scaffold by scanning the raw codex session log for any of the
    # registered match_patterns. The session log contains every shell call
    # codex made, so scaffold commands appear there verbatim.
    scaffold_cache: dict[str, Any] | None = None
    if session_path and session_path.exists():
        try:
            session_blob = session_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            session_blob = ""
        scaffold_cache = detect_scaffold(session_blob, scaffold_caches)
    scaffold_files = scaffold_file_set(scaffold_cache)
    seen_writes: set[str] = set()

    if session_actions:
        actions: list[dict[str, Any]] = []
        for idx, act in enumerate(session_actions, start=1):
            rel_path = act["file_path"]
            before_b = len(state_by_path.get(rel_path, b""))
            extra_kind: dict[str, str] = {}
            if act["action_class"] == "write":
                after_b = act["new_bytes"]
                change_bytes = max(before_b, after_b)
                ratio = 1.0 if after_b > 0 else 0.0
                wk = classify_write(rel_path, scaffold_files, seen_writes)
                is_new_file = before_b == 0 and wk != "overwrite_scaffold"
                is_full_rewrite = True
                extra_kind["write_kind"] = wk
                seen_writes.add(rel_path)
            elif act["action_class"] == "delete":
                after_b = 0
                change_bytes = before_b
                ratio = 1.0 if before_b > 0 else 0.0
                is_new_file = False
                is_full_rewrite = False
                act["old_bytes"] = before_b
            else:
                after_b = max(0, before_b - act["old_bytes"] + act["new_bytes"])
                change_bytes = max(act["old_bytes"], act["new_bytes"])
                ratio = (change_bytes / after_b) if after_b > 0 else 0.0
                is_new_file = False
                is_full_rewrite = False
                extra_kind["edit_kind"] = classify_edit(rel_path, scaffold_files)

            actions.append(
                {
                    "source": "codex",
                    "source_detail": act.get("source_detail"),
                    "session_file": str(session_path) if session_path else None,
                    "seq": idx,
                    "tool": act["tool"],
                    "action_class": act["action_class"],
                    **extra_kind,
                    "file_path": rel_path,
                    "kind": act["kind"],
                    "call_id": act.get("call_id"),
                    "sub_index": act.get("sub_index"),
                    "ts": act.get("ts"),
                    "is_new_file": is_new_file,
                    "is_full_rewrite": is_full_rewrite,
                    "old_bytes": act["old_bytes"],
                    "new_bytes": act["new_bytes"],
                    "added_lines": act["added_lines"],
                    "removed_lines": act["removed_lines"],
                    "before_bytes": before_b,
                    "after_bytes": after_b,
                    "change_bytes": change_bytes,
                    "ratio": round(ratio, 4),
                    "scaffold_inferred": False,
                }
            )
            if act["action_class"] == "delete":
                state_by_path.pop(rel_path, None)
            elif act["action_class"] == "write":
                state_by_path[rel_path] = b"x" * after_b
            else:
                state_by_path[rel_path] = b"x" * after_b
        return actions, scaffold_cache

    actions = []
    for ch in changes:
        rel_path = ch.get("rel_path") or ch.get("raw_path") or "unknown"
        if ch.get("phase") != "after":
            continue

        idx = len(actions) + 1
        kind = ch.get("kind", "update")
        snapshot_rel = ch.get("snapshot_rel")
        before_bytes = state_by_path.get(rel_path, b"")
        after_bytes = read_snapshot(ch.get("snapshot_rel"))
        stats = diff_stats(before_bytes, after_bytes)
        before_size = len(before_bytes)
        after_size = len(after_bytes)

        extra_kind: dict[str, str] = {}
        if kind == "create":
            tool = "Write"
            action_class = "write"
            wk = classify_write(rel_path, scaffold_files, seen_writes)
            is_new_file = wk != "overwrite_scaffold"
            is_full_rewrite = True
            change_bytes = after_size
            ratio = 1.0 if after_size > 0 else 0.0
            extra_kind["write_kind"] = wk
            seen_writes.add(rel_path)
        elif kind == "delete":
            tool = "Delete"
            action_class = "delete"
            is_new_file = False
            is_full_rewrite = False
            change_bytes = before_size
            ratio = 1.0 if before_size > 0 else 0.0
        else:
            tool = "Edit"
            action_class = "edit"
            is_new_file = before_size == 0 and after_size > 0
            is_full_rewrite = False
            change_bytes = max(stats["added_bytes"], stats["removed_bytes"])
            ratio = (change_bytes / after_size) if after_size > 0 else 0.0
            extra_kind["edit_kind"] = classify_edit(rel_path, scaffold_files)

        actions.append(
            {
                "source": "codex",
                "source_detail": "snapshot_diff",
                "seq": idx,
                "event_index": ch.get("event_index"),
                "tool": tool,
                "action_class": action_class,
                **extra_kind,
                "file_path": rel_path,
                "kind": kind,
                "item_id": ch.get("item_id"),
                "ts": ch.get("ts"),
                "elapsed_s": ch.get("elapsed_s"),
                "is_new_file": is_new_file,
                "is_full_rewrite": is_full_rewrite,
                "old_bytes": stats["removed_bytes"] if tool == "Edit" else before_size,
                "new_bytes": stats["added_bytes"] if tool == "Edit" else after_size,
                "added_lines": stats["added_lines"],
                "removed_lines": stats["removed_lines"],
                "before_bytes": before_size,
                "after_bytes": after_size,
                "change_bytes": change_bytes,
                "ratio": round(ratio, 4),
                "snapshot_rel": snapshot_rel,
                "exists_after": ch.get("exists_after"),
                "scaffold_inferred": False,
            }
        )

        if kind == "delete":
            state_by_path.pop(rel_path, None)
        else:
            state_by_path[rel_path] = after_bytes

    return actions, scaffold_cache


def summarize(
    actions: list[dict[str, Any]], scaffold_cache: dict[str, Any] | None = None
) -> tuple[dict[str, Any], dict[str, dict[str, int]]]:
    write_actions = [a for a in actions if a["action_class"] == "write"]
    edit_actions = [a for a in actions if a["action_class"] == "edit"]
    delete_actions = [a for a in actions if a["action_class"] == "delete"]
    write_total_bytes = sum(a["new_bytes"] for a in write_actions)
    edit_total_added = sum(a["new_bytes"] for a in edit_actions)
    edit_total_removed = sum(a["old_bytes"] for a in edit_actions)
    delete_total_removed = sum(a["before_bytes"] for a in delete_actions)
    edit_ratios = [a["ratio"] for a in edit_actions if a["after_bytes"] > 0]
    files_touched = {a["file_path"] for a in actions}

    # Write breakdown by classification
    writes_new = [a for a in write_actions if a.get("write_kind") == "new"]
    writes_overwrite_scaffold = [a for a in write_actions if a.get("write_kind") == "overwrite_scaffold"]
    writes_overwrite_self = [a for a in write_actions if a.get("write_kind") == "overwrite_self"]
    writes_unclassified = [a for a in write_actions if not a.get("write_kind")]

    write_bytes_new = sum(a["new_bytes"] for a in writes_new)
    write_bytes_overwrite_scaffold = sum(a["new_bytes"] for a in writes_overwrite_scaffold)
    write_bytes_overwrite_self = sum(a["new_bytes"] for a in writes_overwrite_self)
    write_bytes_unclassified = sum(a["new_bytes"] for a in writes_unclassified)

    # Edit breakdown by classification
    edits_scaffold = [a for a in edit_actions if a.get("edit_kind") == "scaffold_edit"]
    edits_agent = [a for a in edit_actions if a.get("edit_kind") == "agent_edit"]
    edit_bytes_scaffold = sum(a["new_bytes"] for a in edits_scaffold)
    edit_bytes_agent = sum(a["new_bytes"] for a in edits_agent)

    # Legacy fields (kept for backward compat); under new classification,
    # "new files" excludes scaffold-overwrites.
    new_files = sum(1 for a in write_actions if a.get("is_new_file"))
    rewrite_files = sum(
        1
        for a in write_actions
        if not a.get("is_new_file") and a.get("write_kind") != "overwrite_scaffold"
    )

    per_file: dict[str, dict[str, int]] = {}
    for a in actions:
        fp = a["file_path"]
        d = per_file.setdefault(
            fp,
            {
                "writes": 0,
                "edits": 0,
                "deletes": 0,
                "bytes_via_write": 0,
                "bytes_via_edit": 0,
                "bytes_via_delete": 0,
                "is_scaffold": False,
            },
        )
        if a.get("write_kind") == "overwrite_scaffold" or a.get("edit_kind") == "scaffold_edit":
            d["is_scaffold"] = True
        if a["action_class"] == "write":
            d["writes"] += 1
            d["bytes_via_write"] += a["new_bytes"]
        elif a["action_class"] == "edit":
            d["edits"] += 1
            d["bytes_via_edit"] += a["new_bytes"]
        elif a["action_class"] == "delete":
            d["deletes"] += 1
            d["bytes_via_delete"] += a["before_bytes"]

    # Verdict is computed on AGENT-attributable bytes only (excludes scaffold overwrites).
    agent_write_bytes = write_bytes_new + write_bytes_overwrite_self + write_bytes_unclassified
    agent_edit_bytes = edit_total_added  # all edits remain attributable to the agent
    agent_total_bytes = agent_write_bytes + agent_edit_bytes
    if agent_total_bytes == 0:
        verdict = "no edits"
        rewrite_share = diff_share = 0.0
    else:
        rewrite_share = agent_write_bytes / agent_total_bytes
        diff_share = 1 - rewrite_share
        if rewrite_share >= 0.6:
            verdict = f"CREATE-heavy ({rewrite_share*100:.0f}% bytes via Write)"
        elif diff_share >= 0.6:
            verdict = f"DIFF-heavy ({diff_share*100:.0f}% bytes via Edit)"
        else:
            verdict = f"MIXED (Write {rewrite_share*100:.0f}% / Edit {diff_share*100:.0f}%)"

    summary: dict[str, Any] = {
        "source": actions[0]["source"] if actions else "unknown",
        "source_detail": actions[0].get("source_detail") if actions else None,
        "scaffold_detected": scaffold_cache.get("key") if scaffold_cache else None,
        "scaffold_command": scaffold_cache.get("command") if scaffold_cache else None,
        "scaffold_file_count": scaffold_cache.get("file_count") if scaffold_cache else 0,
        "total_actions": len(actions),
        "write_count": len(write_actions),
        "edit_count": len(edit_actions),
        "delete_count": len(delete_actions),
        "writes_new": len(writes_new),
        "writes_overwrite_scaffold": len(writes_overwrite_scaffold),
        "writes_overwrite_self": len(writes_overwrite_self),
        "writes_unclassified": len(writes_unclassified),
        "edits_scaffold": len(edits_scaffold),
        "edits_agent": len(edits_agent),
        "new_files": new_files,
        "files_rewritten_via_write": rewrite_files,
        "files_touched": len(files_touched),
        "write_total_bytes": write_total_bytes,
        "write_bytes_new": write_bytes_new,
        "write_bytes_overwrite_scaffold": write_bytes_overwrite_scaffold,
        "write_bytes_overwrite_self": write_bytes_overwrite_self,
        "write_bytes_unclassified": write_bytes_unclassified,
        "edit_added_bytes": edit_total_added,
        "edit_bytes_scaffold": edit_bytes_scaffold,
        "edit_bytes_agent": edit_bytes_agent,
        "edit_removed_bytes": edit_total_removed,
        "delete_removed_bytes": delete_total_removed,
        "agent_write_bytes": agent_write_bytes,
        "agent_edit_bytes": agent_edit_bytes,
        "rewrite_byte_share": round(rewrite_share, 4),
        "diff_byte_share": round(diff_share, 4),
        "verdict": verdict,
    }
    if edit_ratios:
        sorted_r = sorted(edit_ratios)
        n = len(sorted_r)
        summary["edit_ratio_median"] = round(median(sorted_r), 4)
        summary["edit_ratio_min"] = round(sorted_r[0], 4)
        summary["edit_ratio_p75"] = round(sorted_r[min(n - 1, int(n * 0.75))], 4) if n >= 4 else None
        summary["edit_ratio_p95"] = round(sorted_r[min(n - 1, int(n * 0.95))], 4) if n >= 20 else None
        summary["edit_ratio_max"] = round(sorted_r[-1], 4)
    return summary, per_file


def write_outputs(
    run_dir: Path,
    actions: list[dict[str, Any]],
    summary: dict[str, Any],
    per_file: dict[str, dict[str, int]],
) -> None:
    logs = run_dir / "logs"
    logs.mkdir(exist_ok=True)

    with (logs / "edits.jsonl").open("w", encoding="utf-8") as f:
        for a in actions:
            f.write(json.dumps(a, ensure_ascii=False) + "\n")

    md: list[str] = ["# Edit profile", ""]
    md.append(f"- Source: `{summary['source']}`")
    if summary.get("source_detail"):
        md.append(f"- Detail: `{summary['source_detail']}`")
    if summary.get("scaffold_detected"):
        md.append(
            f"- Scaffold detected: `{summary['scaffold_detected']}` "
            f"({summary['scaffold_file_count']} cached files) — overwrites of these files are NOT counted as agent Writes"
        )
    else:
        md.append("- Scaffold detected: *(none — all Writes counted as agent-attributable)*")
    md.append(f"**Verdict: {summary['verdict']}**")
    md.append("")
    md.append("## Totals")
    md.append("")
    md.append(f"- Total file-mutating actions: **{summary['total_actions']}**")
    md.append(
        f"  - Write: {summary['write_count']}  "
        f"(new: {summary['writes_new']}  |  "
        f"overwrite_scaffold: {summary['writes_overwrite_scaffold']}  |  "
        f"overwrite_self: {summary['writes_overwrite_self']}"
        + (f"  |  unclassified: {summary['writes_unclassified']}" if summary['writes_unclassified'] else "")
        + ")"
    )
    md.append(
        f"  - Edit-like: {summary['edit_count']}"
        + (
            f"  (scaffold_edit: {summary['edits_scaffold']}  |  agent_edit: {summary['edits_agent']})"
            if summary.get("scaffold_detected")
            else ""
        )
    )
    md.append(f"  - Delete: {summary['delete_count']}")
    md.append(f"- Distinct files touched: {summary['files_touched']}")
    md.append("")
    md.append("### Bytes")
    md.append("")
    md.append(f"- Write bytes (total):                 {summary['write_total_bytes']:,}")
    md.append(f"  - new                                {summary['write_bytes_new']:,}")
    md.append(f"  - overwrite_scaffold (excluded)      {summary['write_bytes_overwrite_scaffold']:,}")
    md.append(f"  - overwrite_self                     {summary['write_bytes_overwrite_self']:,}")
    if summary['write_bytes_unclassified']:
        md.append(f"  - unclassified (no scaffold detected) {summary['write_bytes_unclassified']:,}")
    md.append(f"- Edit bytes added (total):            {summary['edit_added_bytes']:,}")
    if summary.get("scaffold_detected"):
        md.append(f"  - scaffold_edit                      {summary['edit_bytes_scaffold']:,}")
        md.append(f"  - agent_edit                         {summary['edit_bytes_agent']:,}")
    md.append(f"- Edit bytes removed:                  {summary['edit_removed_bytes']:,}")
    if summary["delete_count"]:
        md.append(f"- Delete bytes removed:                {summary['delete_removed_bytes']:,}")
    md.append("")
    md.append(
        f"- **Agent-attributable** byte split: "
        f"Write {summary['rewrite_byte_share']*100:.0f}%  |  Edit {summary['diff_byte_share']*100:.0f}%  "
        f"(agent total = {summary['agent_write_bytes'] + summary['agent_edit_bytes']:,} B)"
    )
    if summary["source"] == "codex" and summary.get("source_detail") == "snapshot_diff":
        md.append("")
        md.append("Note: Codex byte counts are estimated from successive file snapshots captured at each `file_change` event.")
    elif summary["source"] == "codex" and summary.get("source_detail") == "session_apply_patch":
        md.append("")
        md.append("Note: Codex edit counts come from the local session file's `apply_patch` records; this is more precise than snapshot diffing for text edits.")
    if "edit_ratio_median" in summary:
        md.append("")
        md.append("## Edit-ratio distribution")
        md.append("")
        md.append("`change_bytes / after_bytes` for each edit-like action (small = targeted diff, near 1 = near-rewrite)")
        md.append("")
        md.append(f"- Min:    {summary['edit_ratio_min']:.3f}")
        md.append(f"- Median: {summary['edit_ratio_median']:.3f}")
        if summary.get("edit_ratio_p75") is not None:
            md.append(f"- p75:    {summary['edit_ratio_p75']:.3f}")
        if summary.get("edit_ratio_p95") is not None:
            md.append(f"- p95:    {summary['edit_ratio_p95']:.3f}")
        md.append(f"- Max:    {summary['edit_ratio_max']:.3f}")

    md.append("")
    md.append("## Per-file breakdown (top 20 by bytes touched)")
    md.append("")
    md.append("| File | Scaffold? | Writes | Edits | Deletes | Bytes (Write) | Bytes (Edit) | Bytes (Delete) |")
    md.append("|------|:---------:|-------:|------:|--------:|--------------:|-------------:|---------------:|")
    sorted_files = sorted(
        per_file.items(),
        key=lambda kv: -(
            kv[1]["bytes_via_write"] + kv[1]["bytes_via_edit"] + kv[1]["bytes_via_delete"]
        ),
    )
    for fp, s in sorted_files[:20]:
        short = fp
        if len(fp) > 60:
            short = ".../" + "/".join(Path(fp).parts[-3:])
        scaffold_mark = "✓" if s.get("is_scaffold") else ""
        md.append(
            f"| `{short}` | {scaffold_mark} | {s['writes']} | {s['edits']} | {s['deletes']} | "
            f"{s['bytes_via_write']:,} | {s['bytes_via_edit']:,} | {s['bytes_via_delete']:,} |"
        )

    (logs / "edits.md").write_text("\n".join(md) + "\n", encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: analyze_edits.py <run_dir>", file=sys.stderr)
        return 2
    run_dir = Path(sys.argv[1])
    logs = run_dir / "logs"
    claude_events = logs / "events.jsonl"
    codex_manifest = logs / "codex_file_changes.jsonl"
    gemini_events = logs / "gemini_events.jsonl"

    scaffold_caches = load_all_scaffold_caches()

    if claude_events.exists():
        actions, scaffold_cache = analyze_claude(
            load_jsonl(claude_events), run_dir / "workspace", scaffold_caches
        )
    elif gemini_events.exists():
        actions, scaffold_cache = analyze_gemini(
            load_jsonl(gemini_events), run_dir / "workspace", scaffold_caches
        )
    elif codex_manifest.exists():
        actions, scaffold_cache = analyze_codex(run_dir, scaffold_caches)
    else:
        print(
            f"No supported edit source found under {logs} "
            f"(expected events.jsonl, gemini_events.jsonl, or codex_file_changes.jsonl)",
            file=sys.stderr,
        )
        return 1

    summary, per_file = summarize(actions, scaffold_cache)
    write_outputs(run_dir, actions, summary, per_file)
    scaffold_note = (
        f"  scaffold={summary['scaffold_detected']}"
        if summary.get("scaffold_detected")
        else "  scaffold=none"
    )
    print(
        f"edits.jsonl/.md written. {summary['verdict']}{scaffold_note}  "
        f"(actions={summary['total_actions']}, files={summary['files_touched']})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
