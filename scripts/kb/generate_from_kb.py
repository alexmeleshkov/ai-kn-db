#!/usr/bin/env python3
"""
DEPRECATED: KB-driven project generator (v1 - stack-based scaffolding).

This script is deprecated in favor of the two-agent workflow:
- kb-generation-coordinator: Plans tasks and validates outputs
- kb-code-generator: Executes pure 1:1 generation from KB files

The new workflow generates code directly from modules.md, architecture.md, and
other KB files WITHOUT using generic scaffolding or stack references.

This file is kept for reference but should NOT be used for new projects.
Use the /create skill instead, which invokes the agent workflow.

---

OLD FUNCTIONALITY (no longer used):
- Reads docs/kb/projects/*/meta.yaml
- Selects best-matching KB project for a user prompt (simple token overlap)
- Resolves stack_ref -> docs/kb/stacks/<stack_id>/stack.yaml (NO LONGER EXISTS)
- Executes stack scaffold steps (CLI commands + template copy)
- Optionally runs stack smoke test (docker compose)

Repository rule: file contents and code comments must be in English.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import yaml

# Import preference extraction and style injection modules
# COMMENTED OUT FOR MVP - Style injection removed per tech-lead decision
# from extract_preferences import extract_preferences, preferences_to_dict
# from inject_styles import inject_styles

RE_WORD = re.compile(r"[a-zA-Z0-9]+")


def die(msg: str, code: int = 1) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(code)


def run(cmd: str, cwd: Path, env: dict[str, str] | None = None) -> None:
    print(f"==> run: {cmd}")
    subprocess.run(cmd, cwd=str(cwd), env=env, shell=True, check=True)


def tokens(text: str) -> set[str]:
    return {m.group(0).lower() for m in RE_WORD.finditer(text or "")}


def flatten_text(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True)


def find_stack_ref(meta: Any) -> str | None:
    def walk(x: Any) -> Iterable[str]:
        if isinstance(x, dict):
            for v in x.values():
                yield from walk(v)
        elif isinstance(x, list):
            for v in x:
                yield from walk(v)
        elif isinstance(x, str):
            yield x

    for s in walk(meta):
        if "stack-" in s:
            m = re.search(r"(stack-[a-zA-Z0-9\-]+)", s)
            if m:
                return m.group(1)
    return None


@dataclass
class Project:
    project_id: str
    meta_path: Path
    meta: dict[str, Any]
    score: int = 0


def load_projects(repo_root: Path) -> list[Project]:
    projects_dir = repo_root / "docs" / "kb" / "projects"
    if not projects_dir.exists():
        die("docs/kb/projects not found")

    out: list[Project] = []
    for meta_path in projects_dir.glob("*/meta.yaml"):
        if meta_path.parent.name == "_template":
            continue
        meta = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
        if isinstance(meta, dict):
            out.append(Project(project_id=meta_path.parent.name, meta_path=meta_path, meta=meta))
    if not out:
        die("No KB projects found (expected docs/kb/projects/*/meta.yaml)")
    return out


def select_project(projects: list[Project], prompt: str) -> Project:
    pt = tokens(prompt)
    best = projects[0]
    for p in projects:
        blob = flatten_text(p.meta).lower()
        p.score = sum(1 for t in pt if t in blob)
        if p.score > best.score:
            best = p
    return best


def load_stack(repo_root: Path, stack_id: str) -> dict[str, Any]:
    stack_path = repo_root / "docs" / "kb" / "stacks" / stack_id / "stack.yaml"
    if not stack_path.exists():
        die(f"Stack not found: {stack_path}")
    stack = yaml.safe_load(stack_path.read_text(encoding="utf-8")) or {}
    if not isinstance(stack, dict):
        die("Invalid stack.yaml (expected a YAML mapping)")
    return stack


def copy_tree(src: Path, dst: Path) -> None:
    if not src.exists():
        die(f"Template path not found: {src}")
    shutil.copytree(src, dst, dirs_exist_ok=True)


def extract_code_patterns(project_path: Path) -> dict[str, str]:
    """
    Extract code patterns from KB project's modules.md.

    Returns dict mapping file paths to code content.
    Example: {"backend/app/services/llm.py": "from anthropic import..."}
    """
    modules_md = project_path / "modules.md"
    if not modules_md.exists():
        return {}

    content = modules_md.read_text(encoding="utf-8")
    patterns = {}

    # Regex: match **Location**: path followed by code block
    location_pattern = r'\*\*Location\*\*:\s*([^\n]+)'

    # Find all locations
    locations = list(re.finditer(location_pattern, content))

    for i, match in enumerate(locations):
        file_path = match.group(1).strip()
        start_pos = match.end()

        # Determine end position (next location or end of file)
        end_pos = locations[i + 1].start() if i + 1 < len(locations) else len(content)
        section = content[start_pos:end_pos]

        # Find code block in this section
        code_block = re.search(r'```(?:python|typescript|tsx?|javascript|jsx)\n(.*?)```',
                              section, re.DOTALL)
        if code_block:
            patterns[file_path] = code_block.group(1).strip()

    return patterns


def inject_code_patterns(project_dir: Path, patterns: dict[str, str]) -> int:
    """
    Inject code patterns from modules.md into generated stub files.

    Returns number of files updated.
    """
    updated = 0

    for file_path, code_content in patterns.items():
        target_file = project_dir / file_path

        if not target_file.exists():
            print(f"  ! {file_path} (not found, skipping)")
            continue

        # Write the extracted code to the file
        try:
            target_file.parent.mkdir(parents=True, exist_ok=True)
            target_file.write_text(code_content, encoding="utf-8")
            print(f"  ✓ {file_path}")
            updated += 1
        except Exception as e:
            print(f"  ! {file_path} (error: {e})")

    return updated


def apply_stack(repo_root: Path, stack: dict[str, Any], project_dir: Path) -> None:
    scaffold = stack.get("scaffold", {})
    steps = scaffold.get("steps", [])
    if not isinstance(steps, list) or not steps:
        die("stack.yaml has no scaffold.steps")

    for step in steps:
        if not isinstance(step, dict):
            continue

        cwd_tpl = step.get("cwd", "{project_dir}")
        cwd_path = Path(str(cwd_tpl).format(project_dir=str(project_dir))).resolve()

        cmd = step.get("command")
        if cmd:
            env = os.environ.copy()
            env["NPM_CONFIG_YES"] = "true"
            env["CI"] = "1"
            run(str(cmd), cwd=cwd_path, env=env)

        copy_from = step.get("copy_from")
        if copy_from:
            src = repo_root / str(copy_from)
            copy_tree(src, project_dir)


def run_smoke_test(stack: dict[str, Any], project_dir: Path) -> None:
    smoke = stack.get("smoke_test", {})
    cmds = smoke.get("commands", [])
    if not isinstance(cmds, list) or not cmds:
        print("==> smoke_test: none")
        return

    print("==> smoke_test: start")
    for cmd in cmds:
        run(str(cmd), cwd=project_dir)
    print("==> smoke_test: ok")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--run-smoke", action="store_true", default=False)
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    projects = load_projects(repo_root)
    chosen = select_project(projects, args.prompt)

    stack_id: Any = chosen.meta.get("stack_ref") or chosen.meta.get("stack") or find_stack_ref(chosen.meta)
    if isinstance(stack_id, dict):
        stack_id = stack_id.get("ref") or stack_id.get("id")

    if not isinstance(stack_id, str) or not stack_id.startswith("stack-"):
        die("Could not determine stack_ref from meta.yaml")

    print(f"==> selected_kb_project: {chosen.project_id} (score={chosen.score})")
    print(f"==> stack_ref: {stack_id}")

    stack = load_stack(repo_root, stack_id)
    apply_stack(repo_root, stack, out_dir)

    # Inject code patterns from modules.md
    print("==> injecting code patterns from KB")
    kb_project_path = repo_root / "docs" / "kb" / "projects" / chosen.project_id
    patterns = extract_code_patterns(kb_project_path)
    print(f"==> extracted {len(patterns)} code patterns from modules.md")
    if patterns:
        updated = inject_code_patterns(out_dir, patterns)
        print(f"==> injected code into {updated}/{len(patterns)} files")
    else:
        print("==> no code patterns found in modules.md (keeping stubs)")

    # COMMENTED OUT FOR MVP - Style injection removed per tech-lead decision
    # Inject style preferences after scaffolding
    # print("==> extracting style preferences from prompt")
    # preferences = extract_preferences(args.prompt)
    # prefs_dict = preferences_to_dict(preferences)
    # print(f"==> preferences: colors={list(prefs_dict['colors'].keys())}, fonts={list(prefs_dict['fonts'].keys())}")
    # inject_styles(out_dir, prefs_dict)

    if args.run_smoke:
        run_smoke_test(stack, out_dir)
    else:
        print("==> smoke_test: skipped")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
