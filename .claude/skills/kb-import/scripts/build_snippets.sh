#!/usr/bin/env bash
set -euo pipefail

REPO_PATH="${1:?Usage: build_snippets.sh <repo_path> <tmp_dir> [max_lines]}"
TMP_DIR="${2:?Usage: build_snippets.sh <repo_path> <tmp_dir> [max_lines]}"
MAX_LINES="${3:-160}"

cd "$REPO_PATH"

OUT_MD="$TMP_DIR/scan_snippets.md"
OUT_JSON="$TMP_DIR/evidence.json"

: > "$OUT_MD"
echo "[" > "$OUT_JSON"
FIRST=1

append_evidence () {
  local file="$1"
  local start="$2"
  local end="$3"
  # JSON entry
  if [[ $FIRST -eq 0 ]]; then echo "," >> "$OUT_JSON"; fi
  FIRST=0
  printf '  {"file":"%s","start_line":%s,"end_line":%s}' "$file" "$start" "$end" >> "$OUT_JSON"
}

echo "# Repository scan snippets" >> "$OUT_MD"
echo "" >> "$OUT_MD"

# tree
if [[ -f "$TMP_DIR/tree.txt" ]]; then
  echo "## Directory tree" >> "$OUT_MD"
  echo '```' >> "$OUT_MD"
  cat "$TMP_DIR/tree.txt" >> "$OUT_MD"
  echo '```' >> "$OUT_MD"
  echo "" >> "$OUT_MD"
  append_evidence "$TMP_DIR/tree.txt" 1 "$(wc -l < "$TMP_DIR/tree.txt" | tr -d ' ')"
fi

# ext stats
if [[ -f "$TMP_DIR/ext_stats.txt" ]]; then
  echo "## File extension stats" >> "$OUT_MD"
  echo '```' >> "$OUT_MD"
  head -n 80 "$TMP_DIR/ext_stats.txt" >> "$OUT_MD"
  echo '```' >> "$OUT_MD"
  echo "" >> "$OUT_MD"
  append_evidence "$TMP_DIR/ext_stats.txt" 1 80
fi

# key files
if [[ -f "$TMP_DIR/scan_targets.txt" ]]; then
  echo "## Key files (first lines only)" >> "$OUT_MD"
  echo "" >> "$OUT_MD"

  while IFS= read -r f; do
    [[ -z "$f" ]] && continue
    [[ ! -f "$f" ]] && continue

    echo "### $f" >> "$OUT_MD"
    echo "<!-- source: $f:L1-L${MAX_LINES} -->" >> "$OUT_MD"
    echo '```' >> "$OUT_MD"
    sed -n "1,${MAX_LINES}p" "$f" >> "$OUT_MD" || true
    echo '```' >> "$OUT_MD"
    echo "" >> "$OUT_MD"

    append_evidence "$f" 1 "$MAX_LINES"
  done < "$TMP_DIR/scan_targets.txt"
fi

echo "" >> "$OUT_JSON"
echo "]" >> "$OUT_JSON"

echo "OK" > "$TMP_DIR/snippets_done.txt"
