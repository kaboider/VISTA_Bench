#!/usr/bin/env python3
"""
preload_scaffolds.py — pre-generate scaffolds for c1 and c3 task folders.

For each c1/pick_*/<task>/description.md and c3/<task>/description.md, detect
which scaffold command appears in the description text (matched against
tools/scaffold_cache/registry.json `match_patterns`), then **cd into
<task>/workspace/ and run the scaffold command in place** — exactly mimicking
what an agent would do (cd to its workspace, then `npx create-...`).

At eval run time, run_eval.sh with `--preload` rsyncs the entire
<task>/workspace/ tree into _runs/<run_id>/workspace/, giving the agent a
ready-to-modify framework skeleton.

Filtered out: node_modules/, .git/, lockfiles, .DS_Store — same exclude list
as build_scaffold_cache.py (we only want the bytes the agent will modify).

Usage:
    python3 preload_scaffolds.py                       # all c1+c3 tasks
    python3 preload_scaffolds.py --variants c3         # only c3
    python3 preload_scaffolds.py --tasks 4_forum       # only this task across c1+c3
    python3 preload_scaffolds.py --variants c1 --tasks 4_forum 1_newsletter
    python3 preload_scaffolds.py --force               # regenerate even if workspace/ exists
    python3 preload_scaffolds.py --list                # show what would happen, don't run
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).parent.parent
REGISTRY_PATH = Path(__file__).parent / "scaffold_cache" / "registry.json"

EXCLUDE_DIR_NAMES = {
    "node_modules", ".git", ".turbo", ".next", ".nuxt", ".output",
    ".vercel", "dist", "build",
}
EXCLUDE_FILE_NAMES = {
    "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lockb",
    ".DS_Store",
}


def load_registry() -> dict[str, dict]:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))["scaffolds"]


def detect_scaffold(description_text: str, scaffolds: dict) -> str | None:
    """Match description text against scaffold match_patterns. First hit wins."""
    for key, entry in scaffolds.items():
        for pat in entry.get("match_patterns", []):
            if pat and pat in description_text:
                return key
    return None


def _flatten_subdir(target_dir: Path, subdir_name: str) -> None:
    """If scaffold created target_dir/<subdir_name>/, move its contents up to target_dir."""
    sub = target_dir / subdir_name
    if not sub.exists() or not sub.is_dir():
        return
    for item in list(sub.iterdir()):
        dest = target_dir / item.name
        if dest.exists():
            # Conflict (e.g. another file/dir with same name) — leave both,
            # the cleanup pass below will sort excluded ones out.
            continue
        shutil.move(str(item), str(dest))
    try:
        sub.rmdir()
    except OSError:
        pass  # not empty for some reason; leave it


def _cleanup_excluded(target_dir: Path) -> None:
    """Walk target_dir and remove node_modules/, .git/, lockfiles, etc.

    Some scaffolds (eleventy, refine) actually run `npm install` and produce
    a node_modules tree even with our --no-install hints; strip it.

    Silently no-ops if target_dir doesn't exist (some scaffolds — nuxi when
    handed '.' — delete or rename their cwd).
    """
    if not target_dir.exists() or not target_dir.is_dir():
        return
    # Top-level excluded dirs (cheap path)
    for p in list(target_dir.iterdir()):
        if p.is_dir() and p.name in EXCLUDE_DIR_NAMES:
            shutil.rmtree(p, ignore_errors=True)
    # Recursive sweep for nested excluded names + lockfiles
    for p in list(target_dir.rglob("*")):
        try:
            if p.is_dir() and p.name in EXCLUDE_DIR_NAMES:
                shutil.rmtree(p, ignore_errors=True)
            elif p.is_file() and p.name in EXCLUDE_FILE_NAMES:
                p.unlink()
        except OSError:
            pass


def run_scaffold_in_dir(scaffold_entry: dict, target_dir: Path,
                        timeout_s: int = 120) -> tuple[bool, int]:
    """Run the scaffold command from inside `target_dir`, mimicking the
    agent's real workflow (cd into workspace, then `npx create-X myapp`).

    Substitutes `{project}` = `myapp` so scaffold creates a `myapp/` subdir,
    then `_flatten_subdir` lifts the contents up to `target_dir/` so the
    final layout is flat (matches what `_runs/<id>/workspace/` should look
    like at agent run time).

    Why `myapp` instead of `.` (in-place):
        Some scaffolds (nuxi, refine) refuse `.` or prompt to "Override its
        contents", which hangs / aborts. Using a project name + flatten works
        universally across Next/Vite/Astro/Svelte/Remix/Nuxt/T3/Eleventy/
        Refine/Django and is also what an agent typically does (they pick a
        name like 'myapp' or 'frontend' rather than `.`).

    `_cleanup_excluded` strips node_modules/ / .git/ / lockfiles that some
    scaffolds create regardless of --no-install hints.

    Returns (ok, n_files_kept). Tolerates non-zero exit if files were produced
    (e.g. create-react-router exits 1 on benign git-init warning).
    """
    target_dir.mkdir(parents=True, exist_ok=True)

    cmd = scaffold_entry["command"].format(project="myapp")
    rel = target_dir.relative_to(ROOT) if str(target_dir).startswith(str(ROOT)) else target_dir
    print(f"  $ (cd {rel} && {cmd})")

    env = os.environ.copy()
    env.setdefault("CI", "1")
    env.setdefault("npm_config_yes", "true")

    try:
        with open(os.devnull, "rb") as devnull:
            proc = subprocess.run(
                cmd, shell=True, cwd=target_dir, check=False,
                stdin=devnull, capture_output=True, text=True,
                timeout=timeout_s, env=env,
            )
    except subprocess.TimeoutExpired:
        print(f"  FAILED: timeout after {timeout_s}s")
        return False, 0

    # Defensive: a misbehaving scaffold (nuxi with '.', some refine paths)
    # may have deleted/renamed target_dir entirely. Recreate so cleanup has
    # something to walk.
    if not target_dir.exists():
        print(f"  WARN: target_dir was removed during scaffold run — recreating")
        target_dir.mkdir(parents=True, exist_ok=True)

    # Flatten any nested project subdir up to target_dir.
    _flatten_subdir(target_dir, "myapp")

    _cleanup_excluded(target_dir)

    files = [p for p in target_dir.rglob("*") if p.is_file()]
    if proc.returncode != 0 and not files:
        tail = (proc.stderr or proc.stdout or "")[-1500:]
        print(f"  FAILED: exit={proc.returncode}\n{tail}")
        return False, 0
    if proc.returncode != 0 and files:
        print(f"  WARN: non-zero exit ({proc.returncode}) but {len(files)} files produced — proceeding")

    return True, len(files)


def find_task_folders(variants: list[str]) -> list[Path]:
    """Yield each task's folder under the chosen variants."""
    out: list[Path] = []
    for v in variants:
        if v == "c1":
            # c1 has pick_A/B/C subfolders, then per-task folders
            base = ROOT / "c1"
            if not base.exists():
                continue
            for pick in sorted(base.glob("pick_*")):
                if not pick.is_dir():
                    continue
                for t in sorted(pick.iterdir()):
                    if t.is_dir() and (t / "description.md").is_file():
                        out.append(t)
        else:
            base = ROOT / v
            if not base.exists():
                continue
            for t in sorted(base.iterdir()):
                if t.is_dir() and (t / "description.md").is_file():
                    out.append(t)
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variants", nargs="+", default=["c1", "c3"],
                        choices=["c1", "c3"],
                        help="which variants to preload (default: c1 + c3)")
    parser.add_argument("--tasks", nargs="+", default=None,
                        help="filter by task name (e.g. 4_forum 1_newsletter)")
    parser.add_argument("--force", action="store_true",
                        help="regenerate even if workspace/ exists")
    parser.add_argument("--list", action="store_true",
                        help="show planned actions, do not run scaffolds")
    parser.add_argument("--timeout", type=int, default=120,
                        help="per-scaffold timeout seconds (default: 120)")
    args = parser.parse_args()

    scaffolds = load_registry()
    task_folders = find_task_folders(args.variants)
    if args.tasks:
        wanted = set(args.tasks)
        task_folders = [t for t in task_folders if t.name in wanted]

    if not task_folders:
        print("[preload] no matching task folders", file=sys.stderr)
        return 1

    print(f"[preload] {len(task_folders)} task folder(s) to process "
          f"(variants={args.variants}, tasks={args.tasks or 'all'})")
    print()

    succ = fail = skip = no_match = 0
    t_start = time.time()

    for task_dir in task_folders:
        rel = task_dir.relative_to(ROOT)
        scaffold_dir = task_dir / "workspace"

        if scaffold_dir.exists() and not args.force:
            n = sum(1 for _ in scaffold_dir.rglob("*") if _.is_file())
            print(f"[{rel}] cached ({n} files) — skip (use --force to regenerate)")
            skip += 1
            continue

        desc = (task_dir / "description.md").read_text(encoding="utf-8", errors="replace")
        key = detect_scaffold(desc, scaffolds)

        if key is None:
            print(f"[{rel}] no scaffold command detected in description — skipping")
            no_match += 1
            continue

        entry = scaffolds[key]
        if args.list:
            print(f"[{rel}] would scaffold: {key}  ({entry.get('description','')})")
            continue

        print(f"[{rel}] scaffold: {key}  ({entry.get('description','')})")

        # Wipe any existing partial scaffold before regenerating
        if scaffold_dir.exists():
            shutil.rmtree(scaffold_dir)

        ok, n = run_scaffold_in_dir(entry, scaffold_dir, timeout_s=args.timeout)
        if ok:
            print(f"  ok: {n} files in {scaffold_dir.relative_to(ROOT)}")
            succ += 1
        else:
            fail += 1
            if scaffold_dir.exists():
                shutil.rmtree(scaffold_dir, ignore_errors=True)
        print()

    elapsed = time.time() - t_start
    print("=" * 60)
    print(f" Done in {elapsed:.0f}s")
    print(f"   ok:                 {succ}")
    print(f"   failed:             {fail}")
    print(f"   already cached:     {skip}")
    print(f"   no scaffold in desc: {no_match}")
    print("=" * 60)
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
