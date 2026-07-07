# task9 Completion Check

## Completion Criteria

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| `05_UnitTestGuide/index.rst` の toctree に `03_Tips` が含まれており、HTML 出力で「テストの実装方法」配下にページが確認できる | OK | `../06_TestFWGuide/03_Tips` を toctree に追加済み（commit `69746ca`）。`make html` でビルド成功 | | |
| `03_Tips.rst` に「Excelファイル」「Excelシート」等の Excel 固有表現が単独で使われている箇所が残っていない | OK | `grep` 結果: Java コードブロック内コメント 2 箇所（57行・127行）のみ。本文・見出しは全て汎用表現に置換済み | | |
| `make html` がエラーなく完了し、エラー行数が0である | OK | `build succeeded.` ERROR 行数: 0 | | |

## Replaced expressions

| 元の表現 | 置換後 | 種別 |
|---|---|---|
| 「Excelファイルから、入力パラメータや戻り値に対する期待値などを取得したい」（見出し） | 「テストデータファイルから、入力パラメータや戻り値に対する期待値などを取得したい」 | セクション見出し |
| 「任意のディレクトリのExcelファイルを読み込みたい」（見出し） | 「任意のディレクトリのテストデータファイルを読み込みたい」 | セクション見出し |
| 「Excelファイル記述例」（小見出し）複数箇所 | 「テストデータ記述例」 | 小見出し |
| 「Excelファイルに記載しておくことができる。」 | 「テストデータファイルに記載しておくことができる。」 | 本文 |
| 「Excelファイルよりデータを取得できる。」 | 「テストデータファイルよりデータを取得できる。」 | 本文 |
| 「Excelデータを追加するだけで」 | 「テストデータを追加するだけで」 | 本文 |
| 「テストデータ用のExcelに記述されたデータ」 | 「テストデータファイルに記述されたデータ」 | 本文 |
| 「URLエンコーディングされたデータをExcelに記述する必要があるが」 | 「URLエンコーディングされたデータをテストデータファイルに記述する必要があるが」 | 本文 |

## QA Expert Review

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| 完了条件1: toctree に `03_Tips` が含まれる | OK | `05_UnitTestGuide/index.rst` 122行目に `../06_TestFWGuide/03_Tips` が追加済み。`make html` でビルド成功し、HTML 出力でページが「テストの実装方法」配下に生成される。 |
| 完了条件2: Excel 固有表現が残っていない | OK | `grep -n "Excel" 03_Tips.rst \| grep -v "// Excel"` の結果が空行。残存するのは Java コードブロック内コメント2箇所（57行・127行）のみで、仕様により対象外。本文・見出しの Excel 固有表現は全て汎用表現に置換済み。 |
| 完了条件3: `make html` エラー行数0 | OK | ビルド出力: `build succeeded.` / `The HTML pages are in _build/html.` / ERROR 行数: 0 |
| Findings | 0 件 | 全完了条件を満たしており修正不要。 |

## Expert Reviews (axes the task needs)

### Craft Expert (writing)

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| アンダーライン長がテキスト表示幅以上か | NG→Fixed | 「テストデータファイル記述例」（表示幅26）に対しアンダーラインが不足していた5箇所（19・19・19・24・20文字）を全て26文字（`==`×26）に修正。commit 77fbab0 |
| 置換後の文意・文脈が自然か | OK | 「テストデータファイルよりデータを取得」「テストデータファイルに記載しておくことができる」等、全置換箇所で文脈・文意が自然に通っている |
| 文体（だ・である調）の統一 | OK（既存踏襲） | 本文の既存文体はです・ます調が混在しているが、元来の状態であり今回の変更で新たにです・ます調を追加した箇所はない |
| ラベル変更なし | OK | `.. _how_to_get_data_from_excel:` / `.. _using_TestDataParser:` 等、既存ラベルは全て変更なし |
| ビルドエラー | OK | `make html` → `build succeeded.` / 03_Tips.rst 関連の WARNING・ERROR ゼロ |

**Verdict: OK（Finding 1件を修正済み）**

## Overall Verdict

- Self-check: OK
- QA: OK
- Craft expert: OK（Finding 1件修正済み — アンダーライン長不足5箇所）
- Ready to check off: Yes
