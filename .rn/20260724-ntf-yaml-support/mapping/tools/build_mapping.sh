#!/usr/bin/env bash
# build_mapping.sh
# Extract sections from current RST docs and input Markdown files.
# Outputs:
#   mapping/sections-current.csv
#   mapping/sections-input.csv
set -euo pipefail

# Resolve script and repo root
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SESSION_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
REPO_ROOT="$(cd "$SESSION_DIR/../.." && pwd)"

TOOLS_DIR="$SCRIPT_DIR"
MAPPING_DIR="$SESSION_DIR/mapping"
INPUT_DIR="$SESSION_DIR/input"
EXTRACT_PY="$TOOLS_DIR/extract_sections.py"

OUT_CURRENT="$MAPPING_DIR/sections-current.csv"
OUT_INPUT="$MAPPING_DIR/sections-input.csv"

# Temporary directory for extracted RST files
TMPDIR_RST="$(mktemp -d)"
trap 'rm -rf "$TMPDIR_RST"' EXIT

# Determine base commit (merge-base of origin/develop and HEAD)
BASE_COMMIT="$(git -C "$REPO_ROOT" merge-base origin/develop HEAD)"
echo "[build_mapping] base commit: $BASE_COMMIT" >&2

# -----------------------------------------------------------------------
# 1. Extract current RST files from git at base commit
# -----------------------------------------------------------------------
# File spec list: each entry is "actual_path:logical_path"
# logical_path = the git-relative path (used as src_file in CSV for reproducibility)
RST_FILE_SPECS=()
while IFS= read -r rel_path; do
    dest="$TMPDIR_RST/$rel_path"
    mkdir -p "$(dirname "$dest")"
    git -C "$REPO_ROOT" show "${BASE_COMMIT}:${rel_path}" > "$dest"
    RST_FILE_SPECS+=("${dest}:${rel_path}")
done < <(git -C "$REPO_ROOT" ls-tree -r --name-only "$BASE_COMMIT" \
    -- ja/development_tools/testing_framework/ \
    | grep '\.rst$' \
    | sort)

RST_COUNT="${#RST_FILE_SPECS[@]}"
echo "[build_mapping] RST files found: $RST_COUNT" >&2

if [ "$RST_COUNT" -eq 0 ]; then
    echo "ERROR: No RST files found at base commit $BASE_COMMIT" >&2
    exit 1
fi

# -----------------------------------------------------------------------
# 2. Extract current sections → sections-current.csv
# -----------------------------------------------------------------------
python3 "$EXTRACT_PY" current "$OUT_CURRENT" "${RST_FILE_SPECS[@]}"
echo "[build_mapping] Written: $OUT_CURRENT" >&2

# -----------------------------------------------------------------------
# 3. Collect input Markdown files (exclude design.md)
# -----------------------------------------------------------------------
MD_FILE_LIST=()
while IFS= read -r md_path; do
    MD_FILE_LIST+=("$md_path")
done < <(find "$INPUT_DIR" -name "*.md" ! -name "design.md" | sort)

MD_COUNT="${#MD_FILE_LIST[@]}"
echo "[build_mapping] MD files found: $MD_COUNT" >&2

if [ "$MD_COUNT" -eq 0 ]; then
    echo "ERROR: No Markdown files found in $INPUT_DIR" >&2
    exit 1
fi

# -----------------------------------------------------------------------
# 4. Extract input sections → sections-input.csv
# -----------------------------------------------------------------------
python3 "$EXTRACT_PY" input "$OUT_INPUT" "${MD_FILE_LIST[@]}"
echo "[build_mapping] Written: $OUT_INPUT" >&2

echo "[build_mapping] Done." >&2
