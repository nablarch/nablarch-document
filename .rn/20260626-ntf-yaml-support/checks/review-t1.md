# review-t1 Completion Check

## Completion Criteria

| Criterion | Self-check | Evidence |
|---|---|---|
| `bash reviews/tools/build_inventory.sh` を2回実行して同一のCSVが生成される（冪等） | OK | diff 結果: before/after/input の全3ファイルで差分なし（空diff） |
| 3本のCSVの行数が Evidence に記録されている | OK | before=2685, after=3632, input=492 |
| 抽出対象ファイル数が対象ディレクトリの rst / md 実ファイル数と一致 | OK | rst(before/base)=47 files, rst(after/current)=50 files; md(input)=10 files。inventory-before.csv のユニークファイル数=47（Python csv.DictReader で検証）、inventory-after.csv のユニークファイル数=50、inventory-input.csv のユニークファイル数=10 — すべて実ファイル数と一致 |

## Overall Verdict

- Self-check: OK
