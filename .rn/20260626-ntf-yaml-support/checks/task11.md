# task11 Completion Check

## Completion Criteria

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| 05_UnitTestGuide/index.rst の toctree に B-1 として1つのページエントリが現れ、HTML 出力で「テストデータの記述方法」が1ページに収まっている | OK | 05_UnitTestGuide/index.rst の toctree に `../06_TestFWGuide/testdata/index` の1エントリが存在し、7ファイルは toctree から削除済み。ビルドで testdata/index.html として1ページが生成された | OK | toctree 参照1件のみ確認済み（grep -c 結果 = 1）。旧7ファイル未含有確認済み |
| make html がエラーなく完了し、エラー行数が0である | OK | `build succeeded, 21 warnings.` — ERROR 行なし。警告は重複ラベル（旧ファイルが toctree 外に残っているため）と既存の jsp ハイライト警告のみ | OK | QA エキスパートが独立ビルドを実行し ERROR=0 を確認 |

## QA Expert Review

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Verification approach meaningful to the objective (checks the right thing, not just "passed") | OK | toctree エントリ数・8ラベル存在・旧7ファイル toctree 除外・ビルドエラー0件を個別に grep/ビルドで確認。全件 PASS |

## Expert Reviews (axes the task needs)

### Craft Expert (writing)

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Medium-specific best practice | OK | 見出しレベル6段階・アンダーライン長・コードブロック4スペースインデント・toctree 末尾配置すべて仕様どおり |
| Consistency with existing style | OK | だ・である調徹底（コードブロック内テストデータの「正しく更新されます」はデータ値のため問題なし）。7セクション論理順序で配置 |

## Overall Verdict

- Self-check: OK
- QA: OK
- Design expert: N/A
- Craft expert: OK
- Verification expert: N/A
- Ready to check off: YES
