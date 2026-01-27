#!/usr/bin/env python3
"""
KB-driven project generator.

- Reads docs/kb/projects/*/meta.yaml
- Selects best-matching KB project for a user prompt (simple token overlap)
- Resolves stack_ref -> docs/kb/stacks/<stack_id>/stack.yaml
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

    if args.run_smoke:
        run_smoke_test(stack, out_dir)
    else:
        print("==> smoke_test: skipped")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
