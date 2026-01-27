#!/bin/bash
# Fast repository scanner - bounded token usage
# Usage: scan_repo_fast.sh <repo_path> <output_dir>

REPO_PATH="$1"
OUTPUT_DIR="$2"

if [ -z "$REPO_PATH" ] || [ -z "$OUTPUT_DIR" ]; then
    echo "Usage: $0 <repo_path> <output_dir>"
    exit 1
fi

if [ ! -d "$REPO_PATH" ]; then
    echo "Error: Repository path does not exist: $REPO_PATH"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "Scanning repository: $REPO_PATH"
echo "Output directory: $OUTPUT_DIR"

# 1. Generate directory tree (max 500 lines)
echo "Generating directory tree..."
cd "$REPO_PATH" || exit 1
tree -L 4 -I 'node_modules|dist|build|.next|.git|venv|__pycache__|*.pyc|.venv|vendor|target' --dirsfirst 2>/dev/null | head -n 500 > "$OUTPUT_DIR/tree.txt" || \
    find . -maxdepth 4 -type d \( -name node_modules -o -name dist -o -name build -o -name .next -o -name .git -o -name venv -o -name __pycache__ -o -name .venv -o -name vendor -o -name target \) -prune -o -type f -print | sort | head -n 500 > "$OUTPUT_DIR/tree.txt"

# 2. File extension statistics
echo "Generating extension statistics..."
find . -type f \( -name node_modules -o -name dist -o -name build -o -name .next -o -name .git -o -name venv -o -name __pycache__ -o -name .venv -o -name vendor -o -name target \) -prune -o -type f -print | \
    grep -E '\.[a-zA-Z0-9]+$' | \
    sed 's/.*\.//' | \
    sort | uniq -c | sort -rn | head -n 30 > "$OUTPUT_DIR/ext_stats.txt"

# 3. Identify key files to scan (max 20 files)
echo "Identifying scan targets..."
SCAN_TARGETS="$OUTPUT_DIR/scan_targets.txt"
> "$SCAN_TARGETS"

# Priority files (config, docs, entry points)
for pattern in "package.json" "tsconfig.json" "pyproject.toml" "setup.py" "Cargo.toml" "go.mod" "pom.xml" "build.gradle" \
               "README.md" "README.txt" "ARCHITECTURE.md" "CONTRIBUTING.md" \
               "docker-compose.yml" "Dockerfile" ".env.example" "config.yaml" "config.json" \
               "main.py" "app.py" "index.js" "index.ts" "main.go" "main.rs" "App.tsx" "App.jsx"; do
    find . -maxdepth 3 -name "$pattern" -type f 2>/dev/null | head -n 1 >> "$SCAN_TARGETS"
done

# Remove empty lines and duplicates
sed -i '/^$/d' "$SCAN_TARGETS" 2>/dev/null || sed -i '' '/^$/d' "$SCAN_TARGETS" 2>/dev/null
sort -u "$SCAN_TARGETS" -o "$SCAN_TARGETS"

echo "Scan complete!"
echo "Files to scan: $(wc -l < "$SCAN_TARGETS")"
