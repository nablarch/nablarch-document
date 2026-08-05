# self-check: `#9`着手前検査の全面撤回

`ntf-doc-09-pre.md`（背景の前提誤認）→`ntf-doc-09-pre-rev1.md`（STEP 2撤回・検査1修正）と2段階で
修正を試みたが、`steering.md`・`design.md`の全量読了により、3検査すべてが既存の仕組み
（観点Aレビュー・`verify_mapping.py`のadvisory・`#last`のundefined label確認・grep）と重複する
ことが判明したため、`ntf-doc-09-pre-withdrawn.md`により全面撤回した。理由の詳細は同ファイル参照。

着手済みだった`mapping/tools/verify_pages.py`・`mapping/tools/test_verify_pages.py`・
`checks/task-09-pre.md`はいずれも未コミットだったため、`git reset`＋削除で作業ツリーから
除去した（コミット履歴に残っていない）。`ntf-doc-09-pre.md`・`ntf-doc-09-pre-rev1.md`も削除した。

`about/index.rst`・`mapping.csv`・`_batch/`・`vocabulary.md`・`glossary.md`・`steering.md`・
`design.md`はいずれも今回の一連の作業で無変更（`git diff --stat`で確認、差分0件）。

```
$ python3 mapping/tools/verify_mapping.py
(...)
lines total (all rows): 12986
lines total (excluding DROP): 11983
OK: no errors
$ python3 -c "import csv; print(sum(1 for _ in csv.DictReader(open('mapping/mapping.csv'))))"
594
```

594行 / 12,986 / 11,983 いずれも不変。
