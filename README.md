# VISTA — Visual-Spec → App Benchmark

<p align="center">
  <a href="https://kaboider.github.io/VIS_APP/"><img src="https://img.shields.io/badge/🌐_Project_Page-VISTA-1f6feb?style=for-the-badge" alt="Project Page"></a>
  <a href="https://arxiv.org/abs/2605.26144"><img src="https://img.shields.io/badge/arXiv-2605.26144-b31b1b?style=for-the-badge&logo=arxiv&logoColor=white" alt="arXiv"></a>
  <a href="https://huggingface.co/datasets/JunJiaGuo/VIS-APP-Bench"><img src="https://img.shields.io/badge/🤗_Dataset-VIS--APP--Bench-ffce00?style=for-the-badge" alt="Hugging Face Dataset"></a>
</p>

**VISTA** ranks LLM coding agents on **end-to-end web-app generation from visual specs**: each task gives an agent a product's design and asks it to build a *runnable* full-stack app. We score how faithfully the result matches the spec — not just visually, but behaviorally — by matching every human-annotated UI anchor to a live DOM element and checking that it's both **placed correctly** and **actually works**.


---

## 🏆 Leaderboard — Combined Score (condition C4)

<p align="center">
  <img src="readme_assets/leaderboard.png" alt="VISTA C4 leaderboard" width="720">
</p>


---

## How it's scored

```
visual spec ─▶ agent (model × harness) ─▶ runnable app ─▶ per-anchor DOM match ─▶ S
```

For each app the spec carries **critical UI anchors** annotated by humans. The evaluator brings the agent's app up under Docker, then for every anchor:

- **Localization (L)** — is the right element present, in the right place? (DOM match + bounding-box IoU/distance.)
- **Behavior (B)** — does it *do* the right thing? (Click navigates, input accepts, toggle flips, dialog opens…)

The per-anchor score is **L × B**, and the app's score is the mean over its critical anchors. **Combined score S** is the mean across all 10 apps (a missing or broken element scores 0). Because `S = L × B`, an app that looks right but doesn't work scores near zero — behavior is usually the bottleneck.

### Condition C4

The agent gets the **richest spec** and the **freest hand**: the page's **rendered Figma image** (a screenshot mockup) **and** its **pruned Figma structure** (the layout tree as JSON) — but **no target framework**. It picks its own stack.

---

## Running the benchmark

All runners live in [`tasks/`](tasks/). **[`run_eval.sh`](tasks/run_eval.sh)** is the base runner — it launches **one agent against one task/variant**, materializes a run dir (`inputs/`, `workspace/`, system prompt, `meta.json`, event logs), and runs post-hoc analysis. The four `run_eval_<cli>.sh` scripts are thin wrappers that just fix `--cli`.

### Prerequisites

- **Docker** running (each app is built + brought up on fixed host ports `38000`/`38001`).
- The chosen agent CLI **installed and authenticated** (see per-CLI notes below).

### One run — base script

```bash
cd tasks

# ./run_eval.sh --task <task> --variant <c0|c1|c2|c3|c4> [--cli <cli>] [--model <m>]
./run_eval.sh --task 1_newsletter --variant c4                 # default --cli claude
./run_eval.sh --task 4_forum      --variant c4 --cli codex
```

| Flag | Meaning |
|------|---------|
| `--task` | task folder name, e.g. `1_newsletter`, `4_forum`, `7_cloud-storage` |
| `--variant` | spec condition: `c0`–`c4` (the leaderboard uses `c4`) |
| `--cli` | `claude` (default) · `codex` · `gemini` · `antigravity` · `cursor` |
| `--model` | model slug (CLI-specific default if omitted) |
| `--preload` | pre-seed the workspace with a scaffold (`c1`/`c3` only) |
| `--skill` | tell the agent it may freely use installed skills |

### One run — per-CLI wrappers

Each wrapper is `run_eval.sh` with `--cli` pinned, so it takes the same flags:

```bash
cd tasks

./run_eval_claude.sh --task 1_newsletter --variant c4                        # → Claude Code   (default model: sonnet)
./run_eval_codex.sh  --task 1_newsletter --variant c4 --model gpt-5.5        # → OpenAI Codex  (default: gpt-5-codex)
./run_eval_gemini.sh --task 1_newsletter --variant c4 --model gemini-2.5-pro # → Gemini CLI    (default: gemini-2.5-pro)
./run_eval_cursor.sh --task 1_newsletter --variant c4                        # → cursor-agent  (default model: composer-2.5)
```

| Wrapper | Agent CLI | Install / auth |
|---------|-----------|----------------|
| [`run_eval_claude.sh`](tasks/run_eval_claude.sh) | Claude Code | `claude /login` (Max-plan token) |
| [`run_eval_codex.sh`](tasks/run_eval_codex.sh) | OpenAI Codex | `codex /login` (OAuth) **or** `OPENAI_API_KEY` |
| [`run_eval_gemini.sh`](tasks/run_eval_gemini.sh) | Gemini CLI (`@google/gemini-cli ≥ 0.11`) | run `gemini` once (Google OAuth) **or** `GEMINI_API_KEY` |
| [`run_eval_cursor.sh`](tasks/run_eval_cursor.sh) | Cursor (`cursor-agent`) | `curl https://cursor.com/install -fsS \| bash`, then `cursor-agent login` |

### Pinning the harness version (reproducibility)

The harness matters as much as the model, so point each runner at an **exact** pinned binary via its `*_BIN` env var (recorded into `meta.json`):

```bash
CLAUDE_BIN=~/.claude-pinned/2.1.152/node_modules/.bin/claude ./run_eval_claude.sh --task 4_forum --variant c4
CODEX_BIN=~/.codex-pinned/0.134/node_modules/.bin/codex      ./run_eval_codex.sh  --task 4_forum --variant c4
CURSOR_BIN=~/.local/share/cursor-agent/versions/<ver>/cursor-agent ./run_eval_cursor.sh --task 4_forum --variant c4
```

> `cursor-agent` has no built-in run timeout and can hang after finishing; `run_eval.sh` wraps it with an inactivity watchdog (`CURSOR_IDLE_KILL`, default 180s) and a hard cap (`CURSOR_TIMEOUT`, default 45m).

### Batch + scoring

```bash
./run_all.sh --variant c4 --cli cursor --skip-existing   # run every task for one agent
FILTER='*c4*' ./eval_all_runs.sh "$PWD/_runs_<config>"   # build + bring up + score each run dir → eval_summary.csv
```

## Citation

```bibtex
@misc{guo2026vistaendtoendbenchmarkvisual,
      title={VISTA: An End-to-End Benchmark for Visual Spec-to-Web-App Coding Agents},
      author={JunJia Guo and Yuhang Yao and Jiawei and Zhou and Jingdi Chen},
      year={2026},
      eprint={2605.26144},
      archivePrefix={arXiv},
      primaryClass={cs.SE},
      url={https://arxiv.org/abs/2605.26144},
}
```