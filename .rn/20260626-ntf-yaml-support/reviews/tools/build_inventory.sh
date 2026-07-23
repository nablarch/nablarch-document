#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------------------
# build_inventory.sh
# リポジトリルート（nablarch-document/）から実行すること
# ---------------------------------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REVIEWS_DIR="${SCRIPT_DIR}/.."   # .rn/20260626-ntf-yaml-support/reviews
TOOLS_DIR="${SCRIPT_DIR}"

# リポジトリルートを特定
REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "${REPO_ROOT}"

echo "=== build_inventory.sh ==="
echo "REPO_ROOT : ${REPO_ROOT}"
echo "REVIEWS_DIR: ${REVIEWS_DIR}"

# ---------------------------------------------------------------------------
# BASE コミットの取得
# ---------------------------------------------------------------------------
BASE="$(git merge-base origin/develop HEAD)"
echo "BASE commit: ${BASE}"

# ---------------------------------------------------------------------------
# 1. inventory-before.csv（変更前 / base コミット時点）
# ---------------------------------------------------------------------------
TMP_BEFORE="$(mktemp -d)"
trap 'rm -rf "${TMP_BEFORE}"' EXIT

echo ""
echo "--- Extracting base RST files into ${TMP_BEFORE} ---"

# base コミットの対象 RST ファイルを一時ディレクトリに書き出す
while IFS= read -r fpath; do
    dest="${TMP_BEFORE}/${fpath}"
    mkdir -p "$(dirname "${dest}")"
    git show "${BASE}:${fpath}" > "${dest}" 2>/dev/null || true
done < <(git ls-tree -r "${BASE}" --name-only | grep "^ja/development_tools/testing_framework/.*\.rst$")

RST_FILE_COUNT="$(find "${TMP_BEFORE}" -name '*.rst' | wc -l | tr -d ' ')"
echo "Base RST files staged: ${RST_FILE_COUNT}"

python3 "${TOOLS_DIR}/extract_rst.py" "${TMP_BEFORE}/ja/development_tools/testing_framework" \
    "${REVIEWS_DIR}/inventory-before.csv" \
    "${TMP_BEFORE}"

# ---------------------------------------------------------------------------
# 2. inventory-after.csv（PR後・現作業ツリー）
# ---------------------------------------------------------------------------
echo ""
echo "--- Extracting after RST (current working tree) ---"

python3 "${TOOLS_DIR}/extract_rst.py" \
    "${REPO_ROOT}/ja/development_tools/testing_framework" \
    "${REVIEWS_DIR}/inventory-after.csv"

# ---------------------------------------------------------------------------
# 3. inventory-input.csv（input MD）
# ---------------------------------------------------------------------------
echo ""
echo "--- Extracting input MD ---"

MD_FILE_COUNT="$(find "${REPO_ROOT}/.rn/20260626-ntf-yaml-support/input" -name '*.md' | wc -l | tr -d ' ')"
echo "Input MD files: ${MD_FILE_COUNT}"

python3 "${TOOLS_DIR}/extract_md.py" \
    "${REPO_ROOT}/.rn/20260626-ntf-yaml-support/input" \
    "${REVIEWS_DIR}/inventory-input.csv"

# ---------------------------------------------------------------------------
# 4. 行数サマリ
# ---------------------------------------------------------------------------
count_rows() {
    local csv_file="$1"
    # Python の csv モジュールでレコード数をカウントする（改行を含むセルを正しく扱う）
    python3 -c "
import csv, sys
with open(sys.argv[1], encoding='utf-8') as f:
    print(sum(1 for _ in csv.reader(f)) - 1)  # ヘッダー行を除く
" "${csv_file}"
}

BEFORE_ROWS="$(count_rows "${REVIEWS_DIR}/inventory-before.csv")"
AFTER_ROWS="$(count_rows "${REVIEWS_DIR}/inventory-after.csv")"
INPUT_ROWS="$(count_rows "${REVIEWS_DIR}/inventory-input.csv")"

echo ""
echo "=== Summary ==="
printf "inventory-before.csv: %s rows\n" "${BEFORE_ROWS}"
printf "inventory-after.csv:  %s rows\n" "${AFTER_ROWS}"
printf "inventory-input.csv:  %s rows\n" "${INPUT_ROWS}"
echo ""
echo "rst files (after/current): $(find "${REPO_ROOT}/ja/development_tools/testing_framework" -name '*.rst' | wc -l | tr -d ' ')"
echo "md files (input):          ${MD_FILE_COUNT}"
