# task12 Completion Check

## Completion Criteria

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| B-1 の各節（testshots/テーブルデータ/ファイルデータ/メッセージング/特殊値）に B-2 の対応セクションへの :ref: リンクが存在する | OK | index.rst の ntf_testdata_testshots 節末尾に `記述例は :ref:\`ntf_examples_testshots\` を参照。`、ntf_testdata_table_data 節末尾に `記述例は :ref:\`ntf_examples_table_data\` を参照。`、ntf_testdata_file_data 節末尾に `記述例は :ref:\`ntf_examples_file_data\` を参照。`、ntf_testdata_messaging 節末尾に `記述例は :ref:\`ntf_examples_messaging\` を参照。`、ntf_testdata_values 節末尾に `記述例は :ref:\`ntf_examples_values\` を参照。` を追加済み | OK | 5ラベル全て examples.rst に存在（行番号確認済み）。index.rst の5参照も対応節内に正しく配置されていることを行番号で確認 |
| make html がエラーなく完了し、エラー行数が0である | OK | `build succeeded, 27 warnings.` — エラー0件。undefined label 関連の警告なし（grep で確認済み） | OK | QA が独立ビルドを実行し ERROR=0・undefined label 警告0件を確認 |

## QA Expert Review

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Verification approach meaningful to the objective (checks the right thing, not just "passed") | OK | ラベル存在・リンク存在・配置正確性・ビルドエラーを個別に確認。全件 PASS |

## Expert Reviews (axes the task needs)

### Craft Expert (writing)

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Medium-specific best practice | N/A | |
| Consistency with existing style | N/A | |

## Overall Verdict

- Self-check: OK
- QA: OK
- Design expert: N/A
- Craft expert: N/A
- Verification expert: N/A
- Ready to check off: YES
