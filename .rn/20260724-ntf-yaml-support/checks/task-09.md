# self-check: `#9` テストデータの書き方（`implementation/testdata_notation.rst`）

## 対象行の反映

`mapping.csv` の `dest_page=テストデータの書き方` 全140行（使用方法139・機能概要1、`DROP`なし）を、
観点Aレビューで140件全件を出典と突合して確認した（内訳: `05_UnitTestGuide`系29件・`06_TestFWGuide`系34件・
`ntf-doc-terms.md`/`ntf-testdata-loading.md`系19件・`ntf-testdata-doc.md`系49件・
`ntf-testdata-doc-examples-testshots.md`系9件）。`REFERENCE`区分（`current-0290`）が本文化されていないことも
`grep -n "batch_request_test"`で確認済み（該当なし）。詳細は`reviews/page-testdata_notation.md`参照。

```
$ python3 -c "
import csv
with open('mapping/mapping.csv') as f:
    rows = [r for r in csv.DictReader(f) if r['dest_page']=='テストデータの書き方']
print(len(rows), sum(1 for r in rows if r['disposition']=='DROP'))
"
140 0
```

## 4観点レビュー

A（網羅性）・B（トンマナ）・C（用語）・D（整合性）を、それぞれ別のサブエージェントで実施した。
プロンプトには「実測コマンドで裏付けよ」「検証スクリプトを正解として使わず独立に組め」「敵対的にレビューせよ」の
3点を含めた。指摘・対応内容は`reviews/page-testdata_notation.md`に全件記録済み。

## 未対応の指摘

- `must`区分は全件（A-1・A-2・B-F02〜F10・T-01・T-02・D-1）解消済み
- `decide`区分3件（A-3・B-F01・D-4）はユーザーレビューで判断を仰ぐ。理由は`reviews/page-testdata_notation.md`参照
- `note`区分2件（D-3・D-5）は実害が小さいため未対応のまま記録のみ

## `make html`（Docker、README「環境構築」＞「Docker」手順）

```
$ docker run --rm -v <repo>:/root/document nablarch-document-build-sandboxed \
    /bin/bash -c "cd /root/document; sphinx-build -a -d _build/.doctrees/ja -b html ja _build/html"
(...)
/root/document/ja/application_framework/application_framework/libraries/db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test (if the link has no caption the label must precede a section header)
build succeeded, 1 warning.
```

警告1件は`#7`から追跡済みの既知警告（`checks/task-07.md`参照）で、本タスクによる新規警告は0件。

## toctree導線

`implementation/index.rst`の`toctree`に`testdata_notation`・`testdata_examples`（次ページ`#10`用スタブ）を追記済み。

## `verify_mapping.py`

```
$ python3 mapping/tools/verify_mapping.py
(...)
lines total (all rows): 12986
lines total (excluding DROP): 11983
OK: no errors
$ python3 -c "import csv; print(sum(1 for _ in csv.DictReader(open('mapping/mapping.csv'))))"
594
```

594行 / 12,986 / 11,983 いずれも不変（`mapping.csv`は本タスクで変更していない）。
