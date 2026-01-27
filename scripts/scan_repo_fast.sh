#!/usr/bin/env bash
set -euo pipefail

REPO_PATH="${1:?Usage: scan_repo_fast.sh <repo_path> [out_dir]}"
OUT_DIR="${2:-.claude/tmp}"

mkdir -p "$OUT_DIR"

# Normalize path for Git Bash (works with /c/... and C:\... in most cases)
cd "$REPO_PATH"

# Excludes for huge/noisy dirs
EXCLUDES='node_modules|.git|dist|build|.next|.venv|venv|__pycache__|coverage|.turbo|.cache|.idea|.vscode'

# 1) Tree (depth 4)
if command -v tree >/dev/null 2>&1; then
  tree -L 4 -a -I "$EXCLUDES" > "$OUT_DIR/tree.txt" || true
else
  # Fallback if `tree` is not installed
  find . -maxdepth 4 -type d \
    | grep -Ev "/($EXCLUDES)(/|$)" \
    | sed 's|^\./||' \
    | sort > "$OUT_DIR/tree.txt"
fi

# 2) Key files we allow the model to inspect (bounded)
shopt -s nullglob
KEY_GLOBS=(
  "README.md" "README.*" "docs/README.*" "docs/**/*.md"
  "package.json" "pnpm-lock.yaml" "yarn.lock" "package-lock.json" "pnpm-workspace.yaml"
  "tsconfig.json" "vite.config.*" "next.config.*" "turbo.json"
  "pyproject.toml" "requirements.txt" "requirements/*.txt" "Pipfile" "poetry.lock"
  "Dockerfile" "docker-compose.yml" "docker-compose.yaml" "compose.yml" "compose.yaml"
  "Makefile" "justfile"
  ".env.example" ".env.*.example"
  ".github/workflows/*.yml" ".github/workflows/*.yaml"
)

: > "$OUT_DIR/scan_targets.txt"
for g in "${KEY_GLOBS[@]}"; do
  for f in $g; do
    if [[ -f "$f" ]]; then
      echo "$f" >> "$OUT_DIR/scan_targets.txt"
    fi
  done
done
sort -u "$OUT_DIR/scan_targets.txt" -o "$OUT_DIR/scan_targets.txt"

# 3) Quick stats (extensions)
git rev-parse --is-inside-work-tree >/dev/null 2>&1 && GIT_TRACKED=1 || GIT_TRACKED=0
if [[ "$GIT_TRACKED" -eq 1 ]]; then
  git ls-files \
    | grep -Ev "($EXCLUDES)" \
    | awk -F. 'NF>1 {print $NF}' \
    | tr '[:upper:]' '[:lower:]' \
    | sort | uniq -c | sort -nr \
    > "$OUT_DIR/ext_stats.txt"
else
  find . -type f \
    | grep -Ev "/($EXCLUDES)(/|$)" \
    | awk -F. 'NF>1 {print $NF}' \
    | tr '[:upper:]' '[:lower:]' \
    | sort | uniq -c | sort -nr \
    > "$OUT_DIR/ext_stats.txt"
fi

echo "OK" > "$OUT_DIR/scan_done.txt"
