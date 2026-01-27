---
name: kb-import
description: Import an existing codebase into the KB using a bounded, low-token scan (structure + key config files only).
argument-hint: "<path-to-repo> <project-id>"
allowed-tools: Bash, Read, Glob, Grep
context: fork
---

You must keep token usage low. Do NOT read source code files broadly.

Inputs:
- $ARGUMENTS: <repo_path> <project_id>

Hard rules:
1) Never run recursive Grep over the whole repository.
2) Never read arbitrary .ts/.js/.py files unless explicitly required, and at most 2 small files.
3) Only inspect files listed in `.claude/tmp/scan_targets.txt`, and only via `Bash` with `sed -n '1,200p'` (first 200 lines).
4) Ignore large directories (node_modules, dist, build, .next, .git, venv, etc.).
5) If information is missing after bounded scan, write it under "Unknowns" instead of exploring further.

Steps:

A) Run the fast scan script (bounded):
   `.claude/skills/kb-import/scripts/scan_repo_fast.sh <repo_path> .claude/tmp`

B) Build consolidated snippets + evidence + facts in ONE Bash call:
   `.claude/skills/kb-import/scripts/build_scan_artifacts.sh <repo_path> .claude/tmp 200`

   This must produce:
   - `.claude/tmp/scan_snippets.md` containing:
     - `tree.txt`
     - `ext_stats.txt`
     - for each path in `scan_targets.txt`: first 200 lines
     - and per-section source markers like:
       `<!-- source: <file>:L1-L200 -->`
   Optionally also produce:
   - `.claude/tmp/evidence.json` (machine-friendly map of sources)

C) Read ONLY `.claude/tmp/scan_snippets.md`.
   Do not read arbitrary source files directly.
   If needed, you may read at most 2 additional small files explicitly listed in `scan_targets.txt`.

D) Generate KB entry under:
   `docs/kb/projects/<project_id>/`
   using the template from `docs/kb/projects/_template/`.

   Fill all KB files:
   - meta.yaml (domain_tags, capabilities, stack_ref, pattern_refs, run commands)
   - business.md
   - architecture.md
   - modules.md
   - tech.md
   - features.md

   Evidence-driven requirement:
   - Every non-trivial claim must cite at least one source marker from `scan_snippets.md`
     (e.g. `Sources: ARCHITECTURE.md:L1-L200; README.md:L1-L200`).
   - If a claim cannot be supported from snippets, put it under an "Unknowns" section
     and do not present it as fact.
   - Do NOT invent metrics, costs, production settings, or counts unless they appear in snippets.

E) Create pattern candidates inbox:
   `docs/kb/patterns/_inbox/<project_id>.md`
   based only on observed conventions from snippets (no deep code reading).
   Each pattern must include "Evidence" lines pointing to snippet sources.

Output:
- List created/updated file paths.
- List Unknowns / Missing prerequisites.
- Print token-saving note: "Bounded scan used only scan_snippets.md".
