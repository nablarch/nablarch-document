# `#16` ページのリード文の確定と `design.md` の3点追記 — 検証記録

作業指示: `.rn/20260724-ntf-yaml-support/ntf-doc-16-lead-and-design.md`
基準コミット: `a2b27e4`（`#15` の user review 承認時点の HEAD）
実施日: 2026-08-12

新しいページは作っていない。`ja/` の変更は3ページのリード文の移動のみである。

---

## ゲート1 — 第2部・第3部の作成済み全ページのリード文の有無と位置（全件表）

母集合は `ja/development_tools/testing_framework/` 配下の全 `.rst`（`guide/` 配下の削除前資料を除く）を機械抽出したものであり、ホワイトリストで切り出していない。各ファイルについて `:local:` の次の非空行（ラベル行 `.. _...:` は読み飛ばす）を取り、それが最初のL2見出しであれば「リード文なし」と判定した。

抽出スクリプト（`python3`、`glob` で全件走査）の出力:

| ファイル | リード文 | リード文の行 | 最初のL2見出し | 本タスクでの変更 |
|---|---|---|---|---|
| `setup/common.rst` | あり | `:10` | `:12` 使用方法 | **移動した** |
| `setup/class_unit_test.rst` | あり | `:10` | `:12` 使用方法 | **移動した** |
| `setup/request_unit_test/web.rst` | あり | `:10` | `:12` 使用方法 | **移動した** |
| `about/index.rst` | なし（`:12` 全体像 のL2が直後） | — | `:12` 全体像 | 変更なし |
| `implementation/testdata_notation.rst` | なし（`:12` 機能概要 のL2が直後） | — | `:12` 機能概要 | 変更なし |
| `implementation/testdata_examples.rst` | なし（`:12` データブロックとデータタイプ のL2が直後） | — | `:12` データブロックとデータタイプ | 変更なし |
| `index.rst` / `setup/index.rst` / `implementation/index.rst` / `tools/index.rst` | 対象外（`.. contents::` を持たない表題ページ） | — | — | 変更なし |
| `setup/junit5_extension.rst` / `setup/master_data_restore.rst` / `implementation/request_unit_test/web.rst` / `tools/html_check_tool.rst` / `tools/master_data_tool.rst` / `tools/testdata_converter.rst` | 対象外（前方参照のスタブ。`.. contents::` を持たない） | — | — | 変更なし |

判定: **PASS**。3ページはリード文が目次の直後（`:local:` = `:8` の次の非空行 `:10`）にあり、最初のL2見出し `:12` より前にある。後者3ページは `git status` で未変更であることを確認済み（作業ツリーの変更は3ページと `design.md`・`style.md` のみ）。

後者3ページを対象外とする根拠は作業指示のとおりで、`機能概要`・`全体像`・最初のL2セクションの導入文がリード文の役を担う構成が `design.md` §4 と user review（`#8`・`#9`・`#10`）で確定済みであることによる。`design.md` §4 にもこの旨を追記した（STEP 2）。

### 参考: FW解説書ライブラリの全件調査（`style.md` S-02 の根拠）

`ja/application_framework/application_framework/libraries/*.rst` の全件について `:local:` の次の非空行を機械抽出した。`.. contents::` を持つのは20ページで、うち**19ページが見出しの無いリード文**を持ち、持たないのは `format.rst`（`:10` が `機能概要` のL2）の1ページのみである。

| ページ | リード文の行 | 冒頭 |
|---|---|---|
| `bean_util.rst` | `:9` | Java Beansに関する以下機能を提供する。… |
| `code.rst` | `:10` | アプリケーションで使用する値と名称とのマッピングを管理する機能を提供する。 |
| `date.rst` | `:8` | アプリケーションで使用するシステム日時(OS日時)と業務日付を一元的に管理する機能を提供する。 |
| `db_double_submit.rst` | `:10` | :ref:`二重サブミット防止 <tag-double_submission>` … |
| `exclusive_control.rst` | `:10` | この機能では、データベースのデータ更新に対する排他制御を行う。 |
| `file_path_management.rst` | `:9` | システムで使用するファイルの入出力先のディレクトリや拡張子を管理するための機能を… |
| `format.rst` | **なし** | （`:10` `機能概要` のL2） |
| `log.rst` | `:10` | ログ出力を行う機能を提供する。 |
| `mail.rst` | `:14` | メールを送信する機能を提供する。（`:10-12` に置換定義が挟まる） |
| `message.rst` | `:10` | メッセージとは、画面の固定文言(項目タイトルなど)やエラーメッセージのことを指す… |
| `repository.rst` | `:10` | アプリケーションを実装する際に様々な箇所で使用されるオブジェクトや、設定値などを… |
| `service_availability.rst` | `:10` | この機能では、アプリケーションが提供する機能に対して、サービス提供可否をチェック… |
| `session_store.rst` | `:10` | HTTPセッションを抽象化した機能を提供する。 |
| `static_data_cache.rst` | `:8` | データベースやファイルなどに格納した静的データへのアクセスを高速化するためのキャ… |
| `system_messaging.rst` | `:10` | 外部システムとメッセージの送受信を行う機能を提供する。 |
| `tag.rst` | `:25` | この機能では、ウェブアプリケーションの画面作成を支援するカスタムタグを提供する。 |
| `transaction.rst` | `:9` | トランザクション制御が必要となるリソース（データベースやメッセージキュー）に対す… |
| `utility.rst` | `:10` | 本フレームワークで提供している、汎用的に使用できるユーティリティクラスを以下に示… |
| `data_converter.rst` / `database_management.rst` / `index.rst` / `permission_check.rst` / `stateless_web_app.rst` / `validation.rst` | 対象外（`.. contents::` を持たない） | — |

**作業指示の実測表との差**（指示の値を実ファイルで検算した結果、2件を訂正した）:

- `mail.rst` のリード文は `:13` ではなく **`:14`**（`:13` は空行。`:10-12` に `.. |JavaMail| raw:: html` の置換定義が挟まる）。
- `session_store.rst` のリード文は `:9` ではなく **`:10`**（`:9` は空行）。
- 「例外なく」という指示の記述は正確ではない。`format.rst` の1件が例外である。`style.md` に書いた根拠はこの実測に合わせ「20ページ中19ページ」とした。

「ここでは、」で始まるリード文は**0件**である。`ここでは、` 自体は `mail.rst:423`・`log.rst:1366`・`tag.rst:486,1632` に現れるが、いずれもページ途中の節の導入文でありリード文ではない（`grep -n "^ここでは" libraries/*.rst` の全4件を目視確認）。

---

## ゲート2 — `使用方法` の直後がL3見出しであること

```
$ grep -n -A4 '^使用方法$' ja/development_tools/testing_framework/setup/common.rst
12:使用方法
13---------------------------------------------------
14-
15-テストデータの読み込み先を変更する
16-~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

$ grep -n -A4 '^使用方法$' ja/development_tools/testing_framework/setup/class_unit_test.rst
12:使用方法
13---------------------------------------------------
14-
15-エンティティ単体テストの設定項目を登録する
16-~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

$ grep -n -A4 '^使用方法$' ja/development_tools/testing_framework/setup/request_unit_test/web.rst
12:使用方法
13---------------------------------------------------
14-
15-コンポーネント設定ファイルに設定項目を登録する
16-~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```

判定: **PASS**。3ページとも `使用方法` の下線（`:13`）の次は空行（`:14`）で、その次はL3見出し（`:15-16`）である。地の文は残っていない。空行を1行残すのは `FW:libraries/date.rst:10-13`（`機能概要` の下線の次が空行、その次がL3見出し）と同じ形である。

---

## ゲート3 — `ja/` の差分がリード文の移動と文頭の書き直しに由来するものだけであること

```
$ git diff --numstat a2b27e4 -- ja/
2	1	ja/development_tools/testing_framework/setup/class_unit_test.rst
2	1	ja/development_tools/testing_framework/setup/common.rst
2	1	ja/development_tools/testing_framework/setup/request_unit_test/web.rst
```

差分は3ページとも同じ形（`+` 2行 = 目次の直後のリード文とその後の空行、`-` 1行 = `使用方法` 直下の導入文）である。移動元では導入文の行だけを取り除き、`使用方法` の下線の次にあった空行をそのまま残している。

| ファイル | 移動前（`使用方法` 直下） | 移動後（目次の直後） |
|---|---|---|
| `setup/common.rst` | ここでは、テストデータの読み込み先の変更、システム日時の固定、シーケンス採番のテーブル採番への置き換えについて説明する。いずれも設定ファイルへの記述で行う。 | **共通設定では、**テストデータの読み込み先の変更、システム日時の固定、シーケンス採番のテーブル採番への置き換え**ができる。**いずれも設定ファイルへの記述で行う。 |
| `setup/class_unit_test.rst` | ここでは、エンティティ単体テストで使用する設定項目と、データベースを使用するクラスのテストでカラムの記述を省略したときのデフォルト値について説明する。いずれもテスト用のコンポーネント設定ファイルに記述する。 | **クラス単体テストでは、**エンティティ単体テストで使用する設定項目と、データベースを使用するクラスのテストでカラムの記述を省略したときのデフォルト値**を設定できる。**いずれもテスト用のコンポーネント設定ファイルに記述する。 |
| `setup/request_unit_test/web.rst` | ここでは、ウェブアプリケーションのリクエスト単体テストで使用する設定項目と、テストの実行速度を上げる設定について説明する。 | **ウェブアプリケーションのリクエスト単体テストでは、**テストで使用する設定項目と、テストの実行速度を上げる設定**を指定できる。** |

書き直しは文頭の主語の追加と文末の言い切りへの変更のみで、列挙している対象（何を説明するか）は3件とも変えていない。2文目（`いずれも〜`）は2ページとも無変更である。

見出しの文言・並び順が不変であること。罫線（下線）の行が差分に1行も現れないこと、および `a2b27e4` から見出しを機械抽出して現在と `diff` を取ることの2通りで確認した。

```
$ git diff a2b27e4 -- ja/ | grep -E '^[-+]' | grep -vE '^(---|\+\+\+)' | grep -cE '^[-+][-~=]{3,}$'
0

$ for f in <3ページ>; do
    diff <(git show a2b27e4:$f | grep -B1 -E '^([-~=]{5,})$' | grep -vE '^([-~=]{5,}|--)$') \
         <(grep -B1 -E '^([-~=]{5,})$' $f      | grep -vE '^([-~=]{5,}|--)$') \
    && echo "見出し 差分なし"; done
=== setup/common.rst ===
見出し 差分なし
=== setup/class_unit_test.rst ===
見出し 差分なし
=== setup/request_unit_test/web.rst ===
見出し 差分なし
```

抽出された見出し（H1を含む。上から出現順）:

- `setup/common.rst`: 共通設定 / 使用方法 / テストデータの読み込み先を変更する / システム日時を固定する / シーケンス採番をテーブル採番に置き換える
- `setup/class_unit_test.rst`: クラス単体テストの設定 / 使用方法 / エンティティ単体テストの設定項目を登録する / 省略したテーブルのカラムのデフォルト値を変更する
- `setup/request_unit_test/web.rst`: リクエスト単体テストの設定（ウェブアプリケーション） / 使用方法 / コンポーネント設定ファイルに設定項目を登録する / テストの実行速度を上げる / 拡張例 / テストデータの書き方を拡張する

判定: **PASS**。L3以下の本文・表・コードブロックに差分は無い（`git diff --numstat` の `1 1` が3件のみ）。

---

## ゲート4 — `verify_mapping.py`

```
$ cd .rn/20260724-ntf-yaml-support && python3 mapping/tools/verify_mapping.py
Loaded 594 rows from mapping.csv
...
lines total (all rows): 12986
lines total (excluding DROP): 11983
...
OK: no errors
exit=0
```

判定: **PASS**。594行 / 12,986 / 11,983 は `#15` から不変。

---

## ゲート5 — `mapping/` と `ja/conf.py` に差分が無いこと

```
$ git diff --stat a2b27e4 -- .rn/20260724-ntf-yaml-support/mapping/ ja/conf.py
 .rn/20260724-ntf-yaml-support/mapping/style.md | 29 ++++++++++++++++++++++++++
 1 file changed, 29 insertions(+)

$ git diff --stat a2b27e4 -- .rn/20260724-ntf-yaml-support/mapping/ ja/conf.py \
    ':(exclude).rn/20260724-ntf-yaml-support/mapping/style.md'
（出力なし）
```

判定: **PASS（ただし読み替えあり）**。`style.md` は `mapping/` 配下にあるため、ゲート5をそのまま適用すると本タスクの STEP 1（`style.md` S-02 への追記）と両立しない。ゲート7が `style.md` の差分を S-02 の中に限定して検証しているため、**ゲート5は `style.md` を除いた `mapping/` と `ja/conf.py` に対して適用した。** 禁止事項が名指ししている `mapping.csv` / `_batch/` / `vocabulary.md` / `glossary.md` / `ja/conf.py` はいずれも差分0である（上記2つ目のコマンドで確認）。

---

## ゲート6 — `design.md` の差分が §3・§4・§8・§13 の中に収まり、削除0行であること

```
$ git diff --numstat a2b27e4 -- .rn/20260724-ntf-yaml-support/design.md
51	0	.rn/20260724-ntf-yaml-support/design.md

$ git diff -U0 a2b27e4 -- .rn/20260724-ntf-yaml-support/design.md | grep '^@@'
@@ -178,0 +179 @@
@@ -190,0 +192,2 @@
@@ -244,0 +248 @@
@@ -253,0 +258,2 @@
@@ -398,0 +405,14 @@
@@ -404,0 +425,15 @@
@@ -708,0 +744,2 @@
@@ -753,0 +791,14 @@
```

`a2b27e4` 時点の節の範囲（`grep -n '^## '`）: §3 = `:147-209`、§4 = `:210-284`、§8 = `:366-406`、§13 = `:691-`。

| ハンクの旧行 | 属する節 | 内容 |
|---|---|---|
| 178 | §3 ページのアウトライン | 擬似ツリーにリード文の行を追加（STEP 2） |
| 190 | §3 | リード文の位置の1段落を追加（`style.md` S-08 ではなく S-02 を指す） |
| 244 | §4 ページのアウトライン | 擬似ツリーにリード文の行を追加（STEP 2） |
| 253 | §4 | リード文の位置と、作成済み2ページ＋第1部を遡って変更しない旨を追加 |
| 398 | §8 出典と確定設計が食い違う場合 | 陳腐化した例示の扱い（STEP 4-2） |
| 404 | §8 出典と実装が食い違う場合 | 外部の挙動の変化の追記（STEP 4-3） |
| 708 | §13 ツリー全体 | `setup/request_unit_test/images/web/` の2行を追加（STEP 4-1） |
| 753 | §13 | 「画像の配置」の小節を追加（STEP 4-1） |

判定: **PASS**。全8ハンクが §3・§4・§8・§13 の中にあり、削除は0行（`numstat` の第2列が `0`）。

`ハンク 190` は `**「使用方法」のみ必須とし…**` の直前に入るため、既存の段落を分断していない。`ハンク 708` は `setup/request_unit_test/` の直下に `images/` と `web/` の2行を足すもので、既存のファイル行を書き換えていない。

---

## ゲート7 — `style.md` の差分が S-02 の中に収まり、削除0行であること

```
$ git diff --numstat a2b27e4 -- .rn/20260724-ntf-yaml-support/mapping/style.md
29	0	.rn/20260724-ntf-yaml-support/mapping/style.md

$ git diff -U0 a2b27e4 -- .rn/20260724-ntf-yaml-support/mapping/style.md | grep '^@@'
@@ -36,0 +37,8 @@
@@ -88,0 +97,21 @@
```

`a2b27e4` 時点で S-02 = `:33-88`（S-03 は `:89`）。ハンクの旧行 36・88 はいずれも S-02 の中である。

- `+37..44`（8行）: **規約** の箇条書きの先頭にリード文の項を追加。既存の第1項（第2部の並び順）より前に挿入しており、既存の行は動かしていない。
- `+97..117`（21行）: S-02 の末尾（S-03 の直前）に **根拠**（リード文の位置と書き出し）を追加。既存の3つの **根拠** ブロックは無変更。

判定: **PASS**。削除0行。

---

## ゲート8 — `:ref:` の未定義参照が0件、段落内改行が0件

未定義参照はゲート9のフルビルドで確認した。`undefined label` は既知の1件（`FW:libraries/db_double_submit.rst:108` の `how_to_set_token_in_request_unit_test`。第2部の未作成ページを指す既知の警告）のみで、NTF解説書の3ページに由来するものは0件である。`toctree contains reference to nonexisting document` / `unknown document` はいずれも0件。

段落内改行:

```
$ python3（3ページについて、空行を挟まず日本語の行が連続する箇所を検出）
段落内改行: 0 件
```

判定: **PASS**。追加したリード文は3ページとも1行の段落であり、直後に空行を置いている。

---

## ゲート9 — Docker フルビルド

```
$ docker run --rm -v /home/tie303177/work/lovaizu/nablarch-document:/root/document \
    nablarch-document-build /bin/bash -c \
    "cd /root/document; sphinx-build -a -d _build/.doctrees/ja -b html ja _build/html"
...
build succeeded, 1 warning.
exit=0

$ grep -i 'WARNING' build16.log
/root/document/ja/application_framework/application_framework/libraries/db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test (if the link has no caption the label must precede a section header)
```

判定: **PASS**。`build succeeded`、警告は既知の `db_double_submit.rst` 1件のみで新規0件。

---

## STEP 別の実施結果

| STEP | 実施内容 | 成果物 |
|---|---|---|
| 1 | `style.md` S-02 にリード文の規約と根拠を追加（規約8行・根拠21行、削除0行） | `mapping/style.md` |
| 2 | `design.md` §3・§4 の擬似ツリーにリード文の行を追加し、位置の規約を1段落ずつ添えた | `design.md` |
| 3 | 3ページの導入文を目次の直後へ移し、文頭を主語のある形に書き直した | `setup/common.rst`・`setup/class_unit_test.rst`・`setup/request_unit_test/web.rst` |
| 4-1 | §13 のツリーに `images/web/` を追加し、「画像の配置」の小節を新設（FW解説書の3例を実ディレクトリで確認） | `design.md` §13 |
| 4-2 | §8「出典と確定設計が食い違う場合」に陳腐化した例示の扱いを追加 | `design.md` §8 |
| 4-3 | §8「出典と実装が食い違う場合」に外部の挙動の変化の追記を追加 | `design.md` §8 |
| 5 | 本ファイル・`reviews/` 3件への追記・`steering.md` の `#16` エントリ | — |

### STEP 4-1 の根拠の検算

作業指示が挙げる FW解説書の3例を実ディレクトリで確認した。

```
$ ls ja/application_framework/application_framework/libraries/images
code  data_format  images.xlsx  log  mail  message  session_store  system_messaging  tag
```
うち `code`・`log`・`mail`・`message`・`session_store`・`system_messaging`・`tag` の7件は `libraries/<名前>.rst` が実在する（ページ名と一致）。`data_format` に対応する `.rst` は `libraries/` 直下に無い。

```
$ ls ja/application_framework/application_framework/handlers/images | head
BodyConvertHandler  CorsPreflightRequestHandler  CsrfTokenVerificationHandler  ...
$ ls ja/application_framework/application_framework/web/getting_started/images
client_create  images.xlsx  popup  project_bulk_update  project_delete  ...
$ ls ja/application_framework/application_framework/web/images
application_design.png  application_structure.png  images.xlsx  web-design.png
```

`web/images/` が平置きであることも確認した（作業指示の記述どおり）。`design.md` §13 にはこの実測に沿って書いた。

`#15` の画像移動が `guide/` 配下からであることも確認した。

```
$ git log --oneline -M --name-status ae89097 -1 | grep png
R100	.../testing_framework/guide/development_guide/06_TestFWGuide/_images/edit_jre.png	.../setup/request_unit_test/images/web/edit_jre.png
R100	.../installed_jre.png	.../setup/request_unit_test/images/web/installed_jre.png
R100	.../skip_resource_copy.png	.../setup/request_unit_test/images/web/skip_resource_copy.png
R100	.../vmoptions.png	.../setup/request_unit_test/images/web/vmoptions.png
```

---

## 作業指示から外れた点

1. **ゲート5の適用範囲**（上記ゲート5に記載）。`style.md` が `mapping/` 配下にあるため、`style.md` を除いて適用した。
2. **`style.md` の根拠の記述を実測に合わせた**（上記ゲート1の参考節）。作業指示の「例外なく」「`mail.rst:13`」「`session_store.rst:9`」は実ファイルと合わないため、`20ページ中19ページ`・`mail.rst:14`・`session_store.rst:10` と書いた。指示が示す事実（FW解説書のリード文は目次の直後にある）自体は変わらない。
3. **`design.md` §4 に、作成済み3ページを遡って変更しない旨を1文加えた。** STEP 2 は「擬似ツリーにリード文を1行加える」だけを求めているが、リード文を規約にすると `about/index.rst`・`testdata_notation.rst`・`testdata_examples.rst` が規約違反に見えるため、ゲート1の判定根拠を `design.md` 側にも残した。
