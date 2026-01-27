#!/usr/bin/env bash
set -euo pipefail

REPO_PATH="${1:?Usage: build_scan_artifacts.sh <repo_path> <tmp_dir> [max_lines]}"
TMP_DIR="${2:?Usage: build_scan_artifacts.sh <repo_path> <tmp_dir> [max_lines]}"
MAX_LINES="${3:-200}"

mkdir -p "$TMP_DIR"
cd "$REPO_PATH"

OUT_MD="$TMP_DIR/scan_snippets.md"
OUT_EVID="$TMP_DIR/evidence.json"
OUT_FACTS="$TMP_DIR/facts.yaml"

# -----------------------------
# Helpers (keep deterministic)
# -----------------------------

yaml_escape() {
  # Minimal YAML escaping for simple scalar values
  local s="${1//$'\n'/ }"
  s="${s//\"/\\\"}"
  printf "%s" "$s"
}

has_file() {
  [[ -f "$1" ]] && echo "true" || echo "false"
}

now_utc() {
  # Portable-ish UTC timestamp
  date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date +"%Y-%m-%dT%H:%M:%S"
}

extract_env_keys() {
  local f="$1"
  # Extract env var keys from .env.example style files.
  # Ignore comments and empty lines.
  grep -E '^[A-Za-z_][A-Za-z0-9_]*=' "$f" \
    | sed -E 's/=.*$//' \
    | sort -u || true
}

extract_package_scripts_py() {
  # Uses python if available to reliably parse JSON.
  local file="$1"
  local indent="$2"
  python - "$file" "$indent" <<'PY'
import json, sys
path = sys.argv[1]
indent = sys.argv[2]
try:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception:
    sys.exit(0)

scripts = data.get("scripts", {}) or {}
for k in sorted(scripts.keys()):
    v = str(scripts[k]).replace('"','\\"')
    print(f"{indent}{k}: \"{v}\"")
PY
}

extract_package_scripts_fallback() {
  # Very naive fallback if python is not available.
  # Attempts to capture a few common script keys.
  local file="$1"
  local indent="$2"
  for key in dev start build test lint typecheck; do
    local line
    line=$(grep -nE "\"$key\"[[:space:]]*:" "$file" | head -n 1 || true)
    if [[ -n "$line" ]]; then
      # Extract between ":" and trailing comma/quote
      local val
      val=$(echo "$line" | sed -E 's/^[0-9]+:.*"'$key'"[[:space:]]*:[[:space:]]*"([^"]*)".*$/\1/')
      echo "${indent}${key}: \"$(yaml_escape "$val")\""
    fi
  done
}

detect_package_manager() {
  # Determine likely package manager based on lockfile presence.
  if [[ -f "pnpm-lock.yaml" ]]; then echo "pnpm"; return; fi
  if [[ -f "yarn.lock" ]]; then echo "yarn"; return; fi
  if [[ -f "package-lock.json" ]]; then echo "npm"; return; fi
  echo "unknown"
}

detect_language_stack() {
  # Lightweight signals from file presence
  local has_py has_node
  has_py=$(find . -maxdepth 4 -name "requirements.txt" -o -name "pyproject.toml" -o -name "runtime.txt" | head -n 1 || true)
  has_node=$(find . -maxdepth 4 -name "package.json" | head -n 1 || true)

  if [[ -n "$has_py" && -n "$has_node" ]]; then
    echo "python+node"
  elif [[ -n "$has_py" ]]; then
    echo "python"
  elif [[ -n "$has_node" ]]; then
    echo "node"
  else
    echo "unknown"
  fi
}

# -----------------------------
# Build scan_snippets.md + evidence.json
# -----------------------------

: > "$OUT_MD"
echo "[" > "$OUT_EVID"
FIRST=1

append_evidence () {
  local file="$1"
  local start="$2"
  local end="$3"
  if [[ $FIRST -eq 0 ]]; then echo "," >> "$OUT_EVID"; fi
  FIRST=0
  printf '  {"file":"%s","start_line":%s,"end_line":%s}' "$file" "$start" "$end" >> "$OUT_EVID"
}

echo "# Repository Scan Snippets" >> "$OUT_MD"
echo "" >> "$OUT_MD"

# tree/ext are expected from scan_repo_fast.sh
if [[ -f "$TMP_DIR/tree.txt" ]]; then
  echo "## Directory Tree" >> "$OUT_MD"
  echo '```' >> "$OUT_MD"
  cat "$TMP_DIR/tree.txt" >> "$OUT_MD"
  echo '```' >> "$OUT_MD"
  echo "" >> "$OUT_MD"
  append_evidence "tree.txt" 1 "$(wc -l < "$TMP_DIR/tree.txt" | tr -d ' ')"
fi

if [[ -f "$TMP_DIR/ext_stats.txt" ]]; then
  echo "## Extension Statistics" >> "$OUT_MD"
  echo '```' >> "$OUT_MD"
  head -n 120 "$TMP_DIR/ext_stats.txt" >> "$OUT_MD"
  echo '```' >> "$OUT_MD"
  echo "" >> "$OUT_MD"
  append_evidence "ext_stats.txt" 1 120
fi

if [[ -f "$TMP_DIR/scan_targets.txt" ]]; then
  while IFS= read -r f; do
    [[ -z "$f" ]] && continue
    [[ ! -f "$f" ]] && continue

    echo "" >> "$OUT_MD"
    echo "## File: ./$f" >> "$OUT_MD"
    echo "<!-- source: $f:L1-L${MAX_LINES} -->" >> "$OUT_MD"
    echo '```' >> "$OUT_MD"
    sed -n "1,${MAX_LINES}p" "$f" >> "$OUT_MD" || true
    echo '```' >> "$OUT_MD"

    append_evidence "$f" 1 "$MAX_LINES"
  done < "$TMP_DIR/scan_targets.txt"
fi

echo "" >> "$OUT_EVID"
echo "]" >> "$OUT_EVID"

# -----------------------------
# Build facts.yaml (machine-derived)
# -----------------------------

: > "$OUT_FACTS"

REPO_BASENAME="$(basename "$(pwd)")"
echo "repo:" >> "$OUT_FACTS"
echo "  id: \"$(yaml_escape "$REPO_BASENAME")\"" >> "$OUT_FACTS"
echo "  path: \"$(yaml_escape "$(pwd)")\"" >> "$OUT_FACTS"
echo "  scanned_at_utc: \"$(now_utc)\"" >> "$OUT_FACTS"
echo "  stack_signal: \"$(yaml_escape "$(detect_language_stack)")\"" >> "$OUT_FACTS"

echo "" >> "$OUT_FACTS"
echo "files:" >> "$OUT_FACTS"
echo "  has_readme: $(has_file "README.md")" >> "$OUT_FACTS"
echo "  has_architecture_doc: $(has_file "ARCHITECTURE.md")" >> "$OUT_FACTS"
echo "  has_docker_compose: $(has_file "docker-compose.yml")" >> "$OUT_FACTS"
echo "  has_procfile: $(has_file "Procfile")" >> "$OUT_FACTS"
echo "  has_build_sh: $(has_file "build.sh")" >> "$OUT_FACTS"

# Runtime hints (best-effort)
echo "" >> "$OUT_FACTS"
echo "runtime:" >> "$OUT_FACTS"
if [[ -f "runtime.txt" ]]; then
  echo "  runtime_txt: \"$(yaml_escape "$(head -n 1 runtime.txt)")\"" >> "$OUT_FACTS"
else
  echo "  runtime_txt: null" >> "$OUT_FACTS"
fi

# Docker compose quick parse (best-effort, no YAML parser)
echo "" >> "$OUT_FACTS"
echo "docker:" >> "$OUT_FACTS"
if [[ -f "docker-compose.yml" ]]; then
  echo "  compose_files:" >> "$OUT_FACTS"
  echo "    - \"docker-compose.yml\"" >> "$OUT_FACTS"
  echo "  services:" >> "$OUT_FACTS"
  # Extract service names under `services:` at 2-space indent: "  name:"
  awk '
    $0 ~ /^services:/ {in_services=1; next}
    in_services && $0 ~ /^[A-Za-z0-9_-]+:/ {in_services=0}
    in_services && $0 ~ /^  [A-Za-z0-9_-]+:/ {
      gsub(":","",$1); print $1
    }
  ' docker-compose.yml | sort -u | while read -r svc; do
    [[ -z "$svc" ]] && continue
    echo "    - name: \"$(yaml_escape "$svc")\"" >> "$OUT_FACTS"
  done
else
  echo "  compose_files: []" >> "$OUT_FACTS"
  echo "  services: []" >> "$OUT_FACTS"
fi

# Frontend package.json
echo "" >> "$OUT_FACTS"
echo "frontend:" >> "$OUT_FACTS"
if [[ -f "frontend/package.json" ]]; then
  echo "  has_package_json: true" >> "$OUT_FACTS"
  (cd frontend && echo "  package_manager: \"$(detect_package_manager)\"" ) >> "$OUT_FACTS"
  echo "  scripts:" >> "$OUT_FACTS"
  if command -v python >/dev/null 2>&1; then
    (cd frontend && extract_package_scripts_py "package.json" "    ") >> "$OUT_FACTS" || true
  else
    (cd frontend && extract_package_scripts_fallback "package.json" "    ") >> "$OUT_FACTS" || true
  fi
else
  echo "  has_package_json: false" >> "$OUT_FACTS"
  echo "  package_manager: \"unknown\"" >> "$OUT_FACTS"
  echo "  scripts: {}" >> "$OUT_FACTS"
fi

# Backend requirements / env keys
echo "" >> "$OUT_FACTS"
echo "backend:" >> "$OUT_FACTS"
if [[ -f "backend/requirements.txt" ]]; then
  echo "  has_requirements_txt: true" >> "$OUT_FACTS"
  echo "  requirements_top:" >> "$OUT_FACTS"
  head -n 25 backend/requirements.txt | sed 's/^/    - "/; s/$/"/' >> "$OUT_FACTS" || true
else
  echo "  has_requirements_txt: false" >> "$OUT_FACTS"
  echo "  requirements_top: []" >> "$OUT_FACTS"
fi

# Env keys aggregation (from any *.env.example files we know about)
echo "" >> "$OUT_FACTS"
echo "env:" >> "$OUT_FACTS"
echo "  example_files:" >> "$OUT_FACTS"
ENV_KEYS_TMP="$(mktemp)"
: > "$ENV_KEYS_TMP"

# Prefer scan_targets if present, but also include any .env.example files in repo
if [[ -f "$TMP_DIR/scan_targets.txt" ]]; then
  grep -E '\.env(\.example|\.example\..*)$|\.env\.example$' "$TMP_DIR/scan_targets.txt" | while read -r f; do
    [[ -f "$f" ]] && echo "$f"
  done >> "$ENV_KEYS_TMP.files" 2>/dev/null || true
fi
find . -maxdepth 5 -type f -name ".env.example" -o -name "*.env.example" 2>/dev/null >> "$ENV_KEYS_TMP.files" || true

sort -u "$ENV_KEYS_TMP.files" 2>/dev/null | while read -r f; do
  [[ -z "$f" ]] && continue
  # Strip leading ./ for nicer output
  f="${f#./}"
  echo "    - \"$(yaml_escape "$f")\"" >> "$OUT_FACTS"
  extract_env_keys "$f" >> "$ENV_KEYS_TMP.keys" || true
done

echo "  keys:" >> "$OUT_FACTS"
sort -u "$ENV_KEYS_TMP.keys" 2>/dev/null | while read -r k; do
  [[ -z "$k" ]] && continue
  echo "    - \"$(yaml_escape "$k")\"" >> "$OUT_FACTS"
done

rm -f "$ENV_KEYS_TMP" "$ENV_KEYS_TMP.files" "$ENV_KEYS_TMP.keys" 2>/dev/null || true

echo "OK" > "$TMP_DIR/artifacts_done.txt"
