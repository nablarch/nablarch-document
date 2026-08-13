# task-12 Completion Check

`#12` `:ref:` ラベル命名規則の確定（`style.md` S-08 改訂）。作業指示は `ntf-doc-12-ref-labels.md`。
基準コミット `25de65b`（`#11` 承認記録の直後）。**ページを作らないタスクであり、`ja/` 配下は1行も変更していない。**

## ゲート1 — S-08 のラベルと `ja/` 既存ラベルの全件突き合わせ（実行順の先頭）

母集合は**ホワイトリストで切り出さず**、`ja/` 配下の全 `.rst` から機械抽出した。

実行コマンド（`ja/` 配下の実ファイルから抽出。`.rn/` 配下は参照していない）:

```
python3 -c "
import re, pathlib, collections
pat = re.compile(r'^\.\.\s+_\`?([^:\`]+)\`?:\s*$')
labels = collections.defaultdict(list)
files = sorted(pathlib.Path('ja').rglob('*.rst'))
for p in files:
    for i, line in enumerate(p.read_text(encoding='utf-8').splitlines(), 1):
        m = pat.match(line)
        if m:
            labels[m.group(1).strip()].append(f'{p}:{i}')
"
```

出力:

```
走査 .rst ファイル数: 299
抽出ラベル総数(ユニーク): 959
抽出ラベル総数(定義箇所): 959
既存の重複ラベル: 0
```

959という抽出数は、作業指示が引用するレビュー役の実測値（`ja/` 全体の959ラベル）と一致する。
定義箇所の総数（959）とユニーク数（959）が等しいことから、**改訂前の `ja/` には既存の重複ラベルが
1件も無い**ことも同時に確認できる。したがって以降のビルドで重複ラベル警告が出た場合、その原因は
本タスク以降に追加したラベルに限られる。

### 全件表（37件）

作成済み11件（第1部1・第2部3・第3部2・第4部2・表題3）は「自ページ以外に定義箇所が無いこと」、
新規26件は「`ja/` 全体に同名が存在しないこと」を判定条件とした。

| # | 区分 | 部 | ファイル（`ja/development_tools/testing_framework/` 配下） | ラベル | `ja/` 959ラベル中の定義箇所 | 判定 |
|---|---|---|---|---|---|---|
| 1 | 作成済 | 第1部 | `about/index.rst` | `testing_framework_about` | `ja/development_tools/testing_framework/about/index.rst:1` | OK 自ページのみ |
| 2 | 作成済 | 第2部 | `setup/common.rst` | `testing_framework_common` | `ja/development_tools/testing_framework/setup/common.rst:1` | OK 自ページのみ |
| 3 | 作成済 | 第2部 | `setup/junit5_extension.rst` | `junit5_extension` | `ja/development_tools/testing_framework/setup/junit5_extension.rst:1` | OK 自ページのみ |
| 4 | 作成済 | 第2部 | `setup/master_data_restore.rst` | `master_data_restore` | `ja/development_tools/testing_framework/setup/master_data_restore.rst:1` | OK 自ページのみ |
| 5 | 作成済 | 第3部 | `implementation/testdata_notation.rst` | `testdata_notation` | `ja/development_tools/testing_framework/implementation/testdata_notation.rst:1` | OK 自ページのみ |
| 6 | 作成済 | 第3部 | `implementation/testdata_examples.rst` | `testdata_examples` | `ja/development_tools/testing_framework/implementation/testdata_examples.rst:1` | OK 自ページのみ |
| 7 | 作成済 | 第4部 | `tools/testdata_converter.rst` | `testdata_converter` | `ja/development_tools/testing_framework/tools/testdata_converter.rst:1` | OK 自ページのみ |
| 8 | 作成済 | 第4部 | `tools/master_data_tool.rst` | `master_data_tool` | `ja/development_tools/testing_framework/tools/master_data_tool.rst:1` | OK 自ページのみ |
| 9 | 作成済 | 表題 | `setup/index.rst` | `testing_framework_setup` | `ja/development_tools/testing_framework/setup/index.rst:1` | OK 自ページのみ |
| 10 | 作成済 | 表題 | `implementation/index.rst` | `testing_framework_implementation` | `ja/development_tools/testing_framework/implementation/index.rst:1` | OK 自ページのみ |
| 11 | 作成済 | 表題 | `tools/index.rst` | `testing_framework_tools` | `ja/development_tools/testing_framework/tools/index.rst:1` | OK 自ページのみ |
| 12 | 新規 | 第2部 | `setup/class_unit_test.rst` | `class_unit_test_setting` | （無し） | OK 衝突なし |
| 13 | 新規 | 第2部 | `setup/request_unit_test/web.rst` | `request_unit_test_setting_web` | （無し） | OK 衝突なし |
| 14 | 新規 | 第2部 | `setup/request_unit_test/rest.rst` | `request_unit_test_setting_rest` | （無し） | OK 衝突なし |
| 15 | 新規 | 第2部 | `setup/request_unit_test/http_messaging.rst` | `request_unit_test_setting_http_messaging` | （無し） | OK 衝突なし |
| 16 | 新規 | 第2部 | `setup/request_unit_test/batch.rst` | `request_unit_test_setting_batch` | （無し） | OK 衝突なし |
| 17 | 新規 | 第2部 | `setup/request_unit_test/mom.rst` | `request_unit_test_setting_mom` | （無し） | OK 衝突なし |
| 18 | 新規 | 第2部 | `setup/request_unit_test/db_queue.rst` | `request_unit_test_setting_db_queue` | （無し） | OK 衝突なし |
| 19 | 新規 | 第2部 | `setup/deal_unit_test/rest.rst` | `deal_unit_test_setting_rest` | （無し） | OK 衝突なし |
| 20 | 新規 | 第2部 | `setup/deal_unit_test/http_messaging.rst` | `deal_unit_test_setting_http_messaging` | （無し） | OK 衝突なし |
| 21 | 新規 | 第2部 | `setup/deal_unit_test/mom.rst` | `deal_unit_test_setting_mom` | （無し） | OK 衝突なし |
| 22 | 新規 | 第3部 | `implementation/class_unit_test/entity.rst` | `entity_unit_test` | （無し） | OK 衝突なし |
| 23 | 新規 | 第3部 | `implementation/class_unit_test/component.rst` | `component_unit_test` | （無し） | OK 衝突なし |
| 24 | 新規 | 第3部 | `implementation/request_unit_test/web.rst` | `request_unit_test_web` | （無し） | OK 衝突なし |
| 25 | 新規 | 第3部 | `implementation/request_unit_test/rest.rst` | `request_unit_test_rest` | （無し） | OK 衝突なし |
| 26 | 新規 | 第3部 | `implementation/request_unit_test/http_messaging.rst` | `request_unit_test_http_messaging` | （無し） | OK 衝突なし |
| 27 | 新規 | 第3部 | `implementation/request_unit_test/batch.rst` | `request_unit_test_batch` | （無し） | OK 衝突なし |
| 28 | 新規 | 第3部 | `implementation/request_unit_test/mom.rst` | `request_unit_test_mom` | （無し） | OK 衝突なし |
| 29 | 新規 | 第3部 | `implementation/request_unit_test/db_queue.rst` | `request_unit_test_db_queue` | （無し） | OK 衝突なし |
| 30 | 新規 | 第3部 | `implementation/deal_unit_test/web.rst` | `deal_unit_test_web` | （無し） | OK 衝突なし |
| 31 | 新規 | 第3部 | `implementation/deal_unit_test/rest.rst` | `deal_unit_test_rest` | （無し） | OK 衝突なし |
| 32 | 新規 | 第3部 | `implementation/deal_unit_test/http_messaging.rst` | `deal_unit_test_http_messaging` | （無し） | OK 衝突なし |
| 33 | 新規 | 第3部 | `implementation/deal_unit_test/batch.rst` | `deal_unit_test_batch` | （無し） | OK 衝突なし |
| 34 | 新規 | 第3部 | `implementation/deal_unit_test/mom.rst` | `deal_unit_test_mom` | （無し） | OK 衝突なし |
| 35 | 新規 | 第3部 | `implementation/deal_unit_test/db_queue.rst` | `deal_unit_test_db_queue` | （無し） | OK 衝突なし |
| 36 | 新規 | 第4部 | `tools/request_data_tool.rst` | `request_data_tool` | （無し） | OK 衝突なし |
| 37 | 新規 | 第4部 | `tools/html_check_tool.rst` | `html_check_tool` | （無し） | OK 衝突なし |

**37件中 NG 0件。衝突0件。**

**判定: PASS。** 37件中 NG 0件。新規26件は `ja/` の959ラベルのいずれとも衝突せず、作成済み11件は
いずれも自ページ1箇所のみで定義されている（改名の必要なし）。

### 語幹をそのまま使った場合の衝突（規約改訂の根拠）

同じ抽出結果に対し、ファイル名の語幹を直接引いた場合を実測した。

| 語幹 | `ja/` 全体での定義箇所 | 語幹を使った場合の結果 |
|---|---|---|
| `http_messaging` | `ja/application_framework/application_framework/web_service/http_messaging/index.rst:1` | **既存ラベルと衝突** |
| `web` | （無し） | NTF内部で3ページが同名になり衝突 |
| `rest` | （無し） | NTF内部で4ページが同名になり衝突 |
| `mom` | （無し） | NTF内部で4ページが同名になり衝突 |
| `batch` | （無し） | NTF内部で3ページが同名になり衝突 |
| `db_queue` | （無し） | NTF内部で3ページが同名になり衝突 |

`http_messaging` は FW解説書側に実在するラベルであり、**衝突は仮定ではなく実在する**。
残り5語幹は `ja/` 全体では未定義だが、NTF解説書の内部で第2部の設定ページと第3部の実装ページが
同じ語幹を共有するため、語幹をそのまま使えば NTF 内部で衝突する。

## ゲート2 — S-08 の一覧と `design.md` §13「1対1対応表」の突き合わせ

実行コマンド（両ファイルからファイルパスを機械抽出して集合比較）:

```
python3 -c "
import re
d=open('design.md',encoding='utf-8').read()
sec=d[d.index('### 1対1対応表'):]
paths_design=re.findall(r'\|\s*\`([a-z0-9_/]+\.rst)\`\s*\|', sec)
s=open('mapping/style.md',encoding='utf-8').read()
s08=s[s.index('#### NTF解説書のページ先頭ラベル一覧'):s.index('### S-09')]
rows=re.findall(r'\|\s*[^|]+\|\s*\`([a-z0-9_/]+\.rst)\`\s*\|\s*\`([a-z0-9_]+)\`\s*\|', s08)
"
```

出力:

```
design.md §13 のページ数: 34 (重複 0 )
S-08 の行数: 37 うち表題ページ 3
S-08 - 表題 = 34
design にあって S-08 に無い: []
S-08 にあって design に無い（表題除く）: []
ラベルのユニーク性: 37 / 37
```

**判定: PASS。** `design.md` §13 の34ページ（第1部1・第2部13・第3部16・第4部4）と S-08 の一覧が
**過不足なく1対1で対応**する。差集合はどちらの向きも空である。S-08 が34を超える3件は表題ページ
（`setup/index.rst` / `implementation/index.rst` / `tools/index.rst`）で、`design.md:752` が
「マッピングに対応する内容ページではないため、上記『1対1対応表』には含めない」と明記している
導線専用ページである。表題ページ3件はすでに作成済みでラベルも定義済みのため、S-08 の一覧には
「作成済み（改名しない）」として載せた。37件のラベルはすべてユニークである。

## ゲート3 — `ja/` 配下に差分が無い

```
$ git diff 25de65b -- ja/ | wc -l
0
```

**判定: PASS。** `ja/` 配下の `.rst` を1行も変更していない。`ja/conf.py` も差分0行。

## ゲート4 — `verify_mapping.py` と行数不変条件

```
$ python3 mapping/tools/verify_mapping.py ; echo exit=$?
Loaded 594 rows from mapping.csv
lines total (all rows): 12986
lines total (excluding DROP): 11983
（中略）
OK: no errors
exit=0
```

`csv.DictReader` による独立カウント:

```
rows 594 lines合計 12986 DROP除く 11983
```

**判定: PASS。** exit 0、594行 / 12,986 / 11,983 が不変。ツールの出力と `csv.DictReader` による
独立集計が一致している。

## ゲート5 — 変更禁止ファイルに差分が無い

```
$ git diff 25de65b -- .rn/20260724-ntf-yaml-support/mapping/mapping.csv \
    .rn/20260724-ntf-yaml-support/mapping/_batch/ \
    .rn/20260724-ntf-yaml-support/mapping/vocabulary.md \
    .rn/20260724-ntf-yaml-support/mapping/glossary.md \
    .rn/20260724-ntf-yaml-support/design.md | wc -l
0
```

**判定: PASS。**

## ゲート6 — `style.md` の差分が S-08 の節の中に収まっている

改訂前の `style.md` における S-08 の範囲は261〜281行目（S-09 の見出しは282行目）。

```
$ git diff -U0 25de65b -- .rn/20260724-ntf-yaml-support/mapping/style.md | grep -E "^@@"
@@ -263,3 +263,6 @@
@@ -268,0 +272,8 @@
@@ -281,0 +293,69 @@

$ git diff 25de65b -- .rn/20260724-ntf-yaml-support/mapping/style.md | grep -E "^[+-]### S-"
（出力なし）
```

**判定: PASS。** 3つの hunk はいずれも旧263〜281行目、すなわち S-08 の節の内側に位置する
（規約文の書き換え／確認手順と例外の追記／ラベル一覧の追記）。`### S-` で始まる行に追加・削除が
1件も無いことから、S-01〜S-07・S-09〜S-11 の見出しと節の境界がいずれも変わっていない。

## ゲート7 — S-08 の既存の根拠が削除されていない

```
$ sed -n '/### S-08/,/### S-09/p' mapping/style.md | grep -nE "FW:libraries/(exclusive_control|date|session_store)"
22:- `FW:libraries/exclusive_control.rst:1` ページ先頭ラベル `.. _exclusive_control:`
23:- `FW:libraries/exclusive_control.rst:15,93,152,237,379` セクションラベル
27:- `FW:libraries/date.rst:41,57,141,150` セクションラベル `date-system_time_settings`、
29:- `FW:libraries/session_store.rst:1,61,87,101` ページ先頭ラベルは `` .. _`session_store`: ``
```

**判定: PASS。** FW解説書の file:line 4件がすべて S-08 の節の中に残っている。改訂は規約文の
書き換えと一覧・例外の追記にとどめ、根拠は1件も削っていない。

## ゲート8 — Docker フルビルド

README「環境構築」＞「Docker」の手順に従い、コンテナ内で `-a`（全ファイル強制再生成）付きで実行した。

```
$ docker run --rm -v "$(pwd)":/root/document nablarch-document-build /bin/bash -c \
    "cd /root/document; sphinx-build -a -d _build/.doctrees/ja -b html ja _build/html"
（中略）
build succeeded, 1 warning.
exit=0
```

警告の全件（`grep -nE "WARNING|ERROR"` の出力）:

```
310:/root/document/ja/application_framework/application_framework/libraries/db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test (if the link has no caption the label must precede a section header)
```

未解決参照系のキーワード（`undefined label` / `nonexisting document` / `unknown document` /
`duplicate label`）の該当行数は **1件**であり、それが上記の既知警告そのものである。すなわち
**`duplicate label` は0件**であり、S-08 に載せたラベルによる重複は発生していない
（本タスクでは `ja/` を変更していないため当然だが、ゲート1の「改訂前の `ja/` に既存の重複ラベルが
0件」という実測と併せて、以降のページ作成でラベルを追加した時点の差分検出が可能な状態にある）。

**判定: PASS。** `build succeeded`、警告は既知の `db_double_submit.rst` 1件のみ、新規0件。

なお警告が報告する行番号 `:108` は、参照が置かれた `.. important::` ブロックの解決位置であり、
ソース上の `:ref:` の記述行は `db_double_submit.rst:106` である（`grep -rn` で実測）。
`checks/task-07.md`「リンク切れになる参照」の記載（`:106`）と食い違いはない。
この警告は `implementation/request_unit_test/web.rst` の作成タスクで
`how_to_set_token_in_request_unit_test` を定義することで解消する。

## STEP 3 — 引き継ぐ外部ラベルの例外

`how_to_set_token_in_request_unit_test` を S-08 の例外として明記した。名前は変えていない
（本タスクでは `ja/` を変更していないため、そもそも定義も行っていない）。参照元
`ja/application_framework/application_framework/libraries/db_double_submit.rst:106` は
`implementation/request_unit_test/web.rst` の作成タスクで解消される。

## 禁止事項の遵守

| 禁止事項 | 確認方法 | 結果 |
|---|---|---|
| `ja/` 配下の `.rst` を1行も変更しない | ゲート3 | OK（差分0行） |
| `mapping.csv` / `_batch/` / `vocabulary.md` / `glossary.md` / `design.md` / `ja/conf.py` を変更しない | ゲート5、`git diff -- ja/conf.py` | OK（いずれも差分0行） |
| `style.md` の S-08 以外の観点を変更しない | ゲート6 | OK |
| S-08 の既存の根拠を削除しない | ゲート7 | OK（4件とも保持） |
| ラベルを新たに考案しない | 作業指示 STEP 2 の表と S-08 の一覧を照合。`decide` に回す未掲載ページは0件（ゲート2で34ページ過不足なし） | OK |
| `how_to_set_token_in_request_unit_test` の名前を変えない | S-08 に例外として明記。定義自体を行っていない | OK |
| 4観点のレビューは回さない | 回していない。`reviews/` に本タスクの記録は作らない | OK |
