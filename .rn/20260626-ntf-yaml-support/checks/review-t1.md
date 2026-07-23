# review-t1 Completion Check

## Completion Criteria

| Criterion | Self-check | Evidence |
|---|---|---|
| `bash reviews/tools/build_inventory.sh` を2回実行して同一のCSVが生成される（冪等） | OK | diff 結果: before/after/input の全3ファイルで差分なし（空diff）— 2回目も同一 |
| 3本のCSVの行数が Evidence に記録されている | OK | before=2582, after=3291, input=331（Python `csv.reader` によるレコード数カウント・ヘッダー除く） |
| 抽出対象ファイル数が対象ディレクトリの rst / md 実ファイル数と一致 | OK | rst(before/base)=47 files, rst(after/current)=50 files; md(input)=10 files。inventory-before.csv のユニークファイル数=47（Python csv.DictReader で検証）、inventory-after.csv のユニークファイル数=50、inventory-input.csv のユニークファイル数=10 — すべて実ファイル数と一致 |

## T1 差し戻し修正 Evidence（2026-07-23）

### 修正内容

1. **build_inventory.sh カウント方法修正**: `tail -n +2 | wc -l` を Python `csv.reader` によるレコード数カウントに変更。改行を含むセルの複数行カウント誤りを解消。
2. **extract_rst.py ネストコードブロック対応**: アドモニション（`tip`/`note`/`important` 等）本文収集ループ内で、ネストされた `.. code-block::` を検出・抽出するロジックを追加。

### kind別件数（Python csv.DictReader 実測値）

| kind | before | after |
|---|---|---|
| heading | 492 | 753 |
| toctree | 18 | 27 |
| para | 1620 | 1931 |
| admonition | 110 | 117 |
| table | 94 | 94 |
| code | 161 | 282 |
| figure | 87 | 87 |
| **合計** | **2582** | **3291** |

### code 件数検証

- **after CSV code 件数**: 282件（指定の160件以上を満たす）
- **before CSV code 件数**: 161件（修正前154件 + 漏れ7件 = 161件）
- `01_entityUnitTestWithBeanValidation.rst` L104, L333, L503 が before CSV に含まれることを Python csv.DictReader で確認済み

### 冪等確認

- 2回連続実行: before/after/input 全3ファイルで `diff` 結果が空（差分なし）

## Overall Verdict

- Self-check: OK
