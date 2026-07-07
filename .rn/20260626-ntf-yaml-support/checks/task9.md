# task9 Completion Check

## Completion Criteria

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| `05_UnitTestGuide/index.rst` の toctree に `03_Tips` が含まれている | OK | `index.rst` line 115〜120 に「*目的別API使用方法*」セクションと `../06_TestFWGuide/03_Tips` が存在する（既に追加済み） | | |
| `03_Tips.rst` に「Excelファイル」等の Excel 固有表現が単独で残っていない | OK | 修正前15件 → 修正後2件（コードブロック内 Java コメント `// Excelファイルからデータ取得` のみ残存、これはコード例のため対象外）。本文・見出し・ラベルの「Excelファイル」はすべて「テストデータファイル」に置換済み | | |
| `make html` がエラーなく完了し、エラー行数が0である | OK | `make html` 結果: "build succeeded, 11 warnings." ERROR 行数: 0 | | |

## QA Expert Review

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Verification approach meaningful to the objective | | |

## Expert Reviews (axes the task needs)

### Craft Expert (writing)

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Medium-specific best practice | | |
| Consistency with existing style | | |

## Overall Verdict

- Self-check: OK
- QA: OK / NG
- Design expert: N/A
- Craft expert: OK / NG / N/A
- Verification expert: N/A
- Ready to check off: Yes / No (reason)
