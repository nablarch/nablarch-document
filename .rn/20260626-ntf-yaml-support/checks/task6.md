# task6 Completion Check

## Completion Criteria

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| 対象ページの「テストデータの書き方」節が B-1 への :ref: 参照に変わっており、参照先ラベルが Evidence に列挙されている | OK | ntf_testdata, ntf_testdata_testshots, ntf_testdata_messaging, ntf_testdata_values（全10ファイル修正済み） | OK | 4ラベルの定義が testdata/ 配下に実在することを確認。how_to_write_excel の定義が 01_Abstract.rst:192 に維持されていることを確認。 |
| make html がエラーなく完了し、既存の :ref: ラベルが壊れていない | OK | `make html` の ERROR カウント: 0 | OK | `grep -c "^ERROR"` が 0、`build succeeded.` を確認。 |

## QA Expert Review

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Verification approach meaningful to the objective (checks the right thing, not just "passed") | OK | ビルドで参照解決エラーなし、かつ B-1 ラベルが testdata/ 配下の 8 ファイルに存在することを grep で確認済み |

## Expert Reviews (axes the task needs)

### Craft Expert (writing)

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Medium-specific best practice | OK | だ・である調で統一、既存文との一貫性を維持 |
| Consistency with existing style | OK | rest.rst「ただし」断絶・グループA文頭重複・03_DealUnitTest/send_sync.rst Excel/YAML区別未明示の3件を修正済み。 |

### Verification Expert (fact-check)

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Artifact actually checked (tests run / claims verified / flow traced) | OK | make html 0 errors 確認済み |
| Coverage (edge cases / claims / steps) | OK | 全10ファイル（グループA 3件・B 4件・C 2件・D 1件）を修正・確認 |

## Overall Verdict

- Self-check: OK
- QA: OK
- Design expert: N/A
- Craft expert: OK
- Verification expert: OK
- Ready to check off: Yes
