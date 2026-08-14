# `#24` セルフチェック — 取引単体テストの実施方法の是正・`style.md` の必須任意の書き足し

実施日: 2026-08-14 / 起点コミット: `3c7d6ac`（作業ツリーはクリーン）/ ブランチ: `ntf-yaml-support`

本ファイルはコミットしない（作業指示 §5・§6）。レビュー判定（QA/専門家レビュー）の欄はコーディネータが埋めるため、本ファイルには書かない。

---

## ゲート1: `git status --porcelain` の全件

```
$ git status --porcelain
 M .rn/20260724-ntf-yaml-support/design.md
 M .rn/20260724-ntf-yaml-support/mapping/style.md
 M ja/development_tools/testing_framework/about/index.rst
```

| # | パス | 状態 | 変更してよいファイルか |
|---|---|---|---|
| 1 | `.rn/20260724-ntf-yaml-support/design.md` | M | 可 |
| 2 | `.rn/20260724-ntf-yaml-support/mapping/style.md` | M | 可 |
| 3 | `ja/development_tools/testing_framework/about/index.rst` | M | 可 |

`reviews/page-about_index.md` と `checks/task-24.md` は上記実行時点では未更新のため出ていない（ゲート12で再確認）。

**判定: PASS**（変更してよいファイル以外 0件）

---

## ゲート2: 出典5件の突合（`git show 2e501ad:<path>`）

```
$ for f in index.rst batch.rst rest.rst real.rst delayed_send.rst delayed_receive.rst send_sync.rst http_send_sync.rst; do \
    git show 2e501ad:ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/$f | cat -n; done
```

| # | 出典 | 指示書の記述 | 実測した本文 | 一致 |
|---|---|---|---|---|
| 1 | `index.rst:7-8` | アプリケーションサーバにデプロイし、手動でアプリケーションを操作しテストを行う | `7 取引単体テストでは、テスト対象のアプリケーションをアプリケーションサーバにデプロイし、\` / `8 手動でアプリケーションを操作しテストを行う。` | 一致 |
| 2 | `batch.rst:5-6` | バッチ処理の取引単体テストは、自動テストフレームワークを使用してテストを行う。リクエスト単体テストを連続実行することにより、取引単位でのテストを行う | `5 バッチ処理の取引単体テストは、自動テストフレームワークを使用してテストを行う。` / `6 リクエスト単体テストを連続実行することにより、取引単位でのテストを行う。` | 一致 |
| 3 | `rest.rst:7` | 複数のリクエストにより取引が成立する場合は、リクエスト毎のテストを連続実行することにより取引単体テストが実施可能である | `7 ただし、複数のリクエストにより取引が成立する場合は、リクエスト毎のテストを連続実行することにより取引単体テストが実施可能である。` | 一致 |
| 4 | `real.rst:8-10` | 複数のメッセージにより取引が成立する場合は、バッチ処理における取引単体テストと同様に、リクエスト毎のテストを連続実行することにより取引単体テストが実施可能である | `8 ただし、複数のメッセージにより取引が成立する場合は、\` / `9 バッチ処理における取引単体テストと同様に、\` / `10 リクエスト毎のテストを連続実行することにより取引単体テストが実施可能である。` | 一致 |
| 5 | `delayed_send.rst:5-6`／`delayed_receive.rst:5-6` | 実施方法は同期応答メッセージ送信／受信処理と同じ（`./real` を参照） | `delayed_send.rst:5 取引単体テストの実施方法は、同期応答メッセージ送信処理と同じである。` / `:6 実施方法の詳細は\ :doc:`./real`\ を参照すること。`／`delayed_receive.rst:5 取引単体テストの実施方法は、同期応答メッセージ受信処理と同じである。` / `:6 実施方法の詳細は\ :doc:`./real`\ を参照すること。` | 一致 |

補助的に確認した事実（いずれも一致）。

| 出典 | 実測した本文 |
|---|---|
| `index.rst:19-21` | `* データベース準備（データ投入）` / `* アプリケーションのデプロイ` / `* アプリケーションサーバ起動` |
| `index.rst:39-40` | `* 画面ハードコピー` / `* DBダンプ(テスト実行前および実行後)` |
| `send_sync.rst:7` | `同期応答メッセージ送信処理を伴うウェブアプリケーションで、取引単体テストを行う場合は、Nablarchが提供するモックアップクラスを使用する。` |
| `http_send_sync.rst:7` | `HTTP同期応答メッセージ送信処理を伴うウェブアプリケーションで、取引単体テストを行う場合は、Nablarchが提供するモックアップクラスを使用する。` |

ディレクトリ内の `.rst` は上記8ファイルで全件（`git ls-tree -r --name-only 2e501ad <dir>` で確認。他は `_images/` のみ）。

`input-0028` の出典についても実測した。

```
$ awk 'NR==198' .rn/20260724-ntf-yaml-support/mapping/mapping.csv
$ grep -n 'テストの種類' .rn/20260724-ntf-yaml-support/mapping/mapping.csv
```

- `dest_section=テストの種類` の行は `mapping.csv:198`（`input-0028`）の1件のみ。
- 出典 `input/ntf-doc-terms.md:415-426` は `| 正式名称 | 内容 |`（`:416`）＋区切り行（`:417`）＋データ8行の2列表。実行方法列・備考列は無い。
- よって `about/index.rst:73`・`:75` の出所は `design.md`「「テストの種類」に置く対比」節の対比表であり、`mapping.csv` は変更しない。

**判定: PASS**（5件すべて一致。本文着手前に確認済み）

---

## ゲート3: `about/index.rst` の差分（全件）

```
$ git diff -U0 ja/development_tools/testing_framework/about/index.rst
```

| # | 行 | 変更前 | 変更後 |
|---|---|---|---|
| 1 | `:73` | `    - 手動操作` | `    - ウェブアプリケーションは手動操作、それ以外の処理方式はJUnitで自動実行` |
| 2 | `:75` | `    - APサーバへのデプロイが必要。エビデンスは画面ハードコピー・DBダンプ` | `    - 手動操作の場合は、アプリケーションサーバへのデプロイが必要。エビデンスは画面ハードコピー・DBダンプ` |
| 3 | `:79` | `  取引単体テストは、自動実行ではなく手動操作によって行う。自動実行の対象となるのは、クラス単体テストとリクエスト単体テストである。` | `  取引単体テストの実施方法は、対象とする処理方式によって異なる。ウェブアプリケーションでは、テスト対象のアプリケーションをアプリケーションサーバにデプロイし、手動で操作してテストを行う。それ以外の処理方式では、リクエスト単体テストを連続実行することにより、取引単体テストをJUnitで自動実行できる。` |

ハンクは `@@ -73 +73 @@`・`@@ -75 +75 @@`・`@@ -79 +79 @@` の3つのみ。`:77-79` の `important` は削除せず本文のみ差し替えた（`.. important::` 行と空行は無変更）。行数は増減していない（118行のまま）。地の文は1段落1行（`:79` は1行）。

**判定: PASS**（`:73`・`:75`・`:77-79` 以外の変更 0件）

---

## ゲート4: `design.md` の差分（全件）

```
$ git diff -U0 .rn/20260724-ntf-yaml-support/design.md
```

| # | 行 | 変更前 | 変更後 |
|---|---|---|---|
| 1 | `:84` | `| 取引単体テスト | 手動操作 | 複数リクエストにまたがる業務の流れ | APサーバへのデプロイが必要。エビデンスは画面ハードコピー・DBダンプ |` | `| 取引単体テスト | ウェブアプリケーションは手動操作、それ以外の処理方式はJUnitで自動実行 | 複数リクエストにまたがる業務の流れ | 手動操作の場合はAPサーバへのデプロイが必要。エビデンスは画面ハードコピー・DBダンプ |` |
| 2 | `:86` | `取引単体テストが自動テストではないことを明示する。` | `**取引単体テストの実施方法が処理方式によって異なることを明示する。** …（出典5件を添えた1段落。全文は `git diff` 参照）` |

ハンクは `@@ -84 +84 @@`・`@@ -86 +86 @@` の2つのみ。行数は増減していない。

**判定: PASS**（`:84`・`:86` 以外の変更 0件）

---

## ゲート5: `style.md` の差分（全件）

```
$ git diff -U0 .rn/20260724-ntf-yaml-support/mapping/style.md
```

| # | 行 | 変更前 | 変更後 |
|---|---|---|---|
| 1 | `:45`（→ `:45-46`） | `- 第2部のページは「機能概要 → 使用方法 → 拡張例」の順に並べる。` | `- 第2部のページは「使用方法」のみ必須とし、「機能概要」「拡張例」は出典が無い場合は見出し自体を` / `  置かない。置く場合は「機能概要 → 使用方法 → 拡張例」の順に並べる。` |
| 2 | `:55-56`（→ `:56-58`） | `この構成は `design.md` の第2部ページアウトライン（`design.md:76-88`）、第3部ページアウトライン` / `（`design.md:132-141`）の決定に基づく。` | `この構成は `design.md` の「3. 第2部 導入と設定」＞「ページのアウトライン」節、および` / `「4. 第3部 テストの実装方法」＞「ページのアウトライン」節の決定に基づく。`design.md` は` / `更新が続く文書のため、行番号ではなく節見出しで指す。` |

ハンクは `@@ -45 +45,2 @@`・`@@ -55,2 +56,3 @@` の2つのみ。`:46-51` の第3部の規約は無変更。

指示書は2件目を `:56-57` と記していたが、実測した現物は `:55-56` であった（`この構成は…` が `:55`、`（design.md:132-141）の決定に基づく。` が `:56`）。指す対象は同一の文であるため、その文を改めた。

`design.md` の節見出しは実物で確認した（`grep -n '^#\{1,4\} ' design.md`）。

- `## 3. 第2部 導入と設定`（`:147`）＞ `### ページのアウトライン`（`:173`。本文は `:173-190`）
- `## 4. 第3部 テストの実装方法`（`:213`）＞ `### ページのアウトライン`（`:242`）

旧記述がずれていたことも実測した。`design.md:76` は `### 「テストの種類」に置く対比`（第1部）、`design.md:132-141` は `### モジュール一覧は第1部に置かない。…` 節の本文である。

**判定: PASS**（`:45` と `:55-56` の参照先表記以外の変更 0件）

---

## ゲート6: `about/index.rst` の内訳表（現 `:83-94`）の反映前後 `diff`

```
$ git show HEAD:ja/development_tools/testing_framework/about/index.rst | sed -n '83,94p' > before.txt
$ sed -n '83,94p' ja/development_tools/testing_framework/about/index.rst > after.txt
$ diff before.txt after.txt
（出力なし）
G6: diff 0件
```

**判定: PASS**（差分 0件）

---

## ゲート7: 処理方式の名称が `glossary.md` §5.2 の正表記であること

`glossary.md` §5.2（`:123-137`）を開き、7正表記を実測した。

`ウェブアプリケーション`／`RESTfulウェブサービス`／`HTTPメッセージング`／`Nablarchバッチアプリケーション`／`MOMによるメッセージング`／`テーブルをキューとして使ったメッセージング`／`Jakarta Batchに準拠したバッチアプリケーション`

```
$ grep -n "ウェブアプリケーション\|RESTfulウェブサービス\|HTTPメッセージング\|Nablarchバッチアプリケーション\|MOMによるメッセージング\|テーブルをキューとして使ったメッセージング\|Jakarta Batch" ja/development_tools/testing_framework/about/index.rst
```

| # | 箇所 | 使用した名称 | 正表記か | 本タスクでの変更 |
|---|---|---|---|---|
| 1 | `about/index.rst:73` | `ウェブアプリケーション` | 正表記（`glossary.md:131`） | 追加 |
| 2 | `about/index.rst:79` | `ウェブアプリケーション` | 正表記（`glossary.md:131`） | 追加 |
| 3 | `about/index.rst:88-93` | 6処理方式（内訳表） | 正表記 | 変更なし |
| 4 | `about/index.rst:98` | `Jakarta Batchに準拠したバッチアプリケーション` | 正表記（`glossary.md:137`） | 変更なし |
| 5 | `design.md:84` | `ウェブアプリケーション` | 正表記 | 追加 |
| 6 | `design.md:86` | `ウェブアプリケーション` | 正表記 | 追加 |

出典の呼称（`バッチ処理`・`メッセージ受信処理`・`同期応答メッセージ送信処理`）は本文に持ち込んでいない（`design.md:86` に現れるのは出典ファイル名のみ）。

**判定: PASS**（逸脱 0件）

---

## ゲート8: 見出し下線を `style.md` S-04 の実測則で確認

```
$ grep -n '^[-~^=]\{3,\}$' ja/development_tools/testing_framework/about/index.rst
4:==...（L1）  13,53,107,116:--...（L2）  19,23,27,31:~~...（L3）
```

見出しは増減していない（`git diff --stat` は `ja/…/about/index.rst | 6 +++---` で、変更3行・行数増減なし）。見出し行・下線行のいずれも差分に含まれていない（ゲート3の3ハンクは `:73`・`:75`・`:79` のみ）。L1=`=`、L2=`-`、L3=`~` の対応はS-04どおり。

**判定: PASS**（逸脱 0件）

---

## ゲート9: `verify_mapping.py`

```
$ python3 .rn/20260724-ntf-yaml-support/mapping/tools/verify_mapping.py
Loaded 595 rows from mapping.csv

pending zero assignments: 0 (awaiting #6 decision)
lines total (all rows): 12986
lines total (excluding DROP): 11983

candidate duplicate destinations: 44 (advisory only, not auto-fixed)
reference-only sections: 2 (advisory only, not auto-fixed)
intro section split advisories: 5 (not auto-fixed)
part2 optional sections (機能概要/拡張例) zero count: 18 (advisory only, not an error)

OK: no errors
exit=0
```

| 項目 | 期待 | 実測 |
|---|---|---|
| exit code | 0 | 0 |
| rows | 595 | 595 |
| lines total (all rows) | 12,986 | 12986 |
| lines total (excluding DROP) | 11,983 | 11983 |

**判定: PASS**

---

## ゲート10: 変更してはならないファイルの差分

```
$ git status --porcelain
 M .rn/20260724-ntf-yaml-support/design.md
 M .rn/20260724-ntf-yaml-support/mapping/style.md
 M ja/development_tools/testing_framework/about/index.rst
```

| 対象 | 差分 |
|---|---|
| `mapping/mapping.csv` | 0件 |
| `mapping/_batch/` | 0件 |
| `mapping/volume.md` | 0件 |
| `mapping/vocabulary.md` | 0件 |
| `mapping/glossary.md` | 0件 |
| `ja/conf.py` | 0件 |
| `about/index.rst` 以外の `ja/` 配下 | 0件 |
| `steering.md` | 0件 |

**判定: PASS**（0件）

---

## ゲート11: Docker フルビルド（`-a`）

```
$ docker run --rm -v /home/tie303177/work/nablarch/nablarch-document:/root/document nablarch-document-build \
    /bin/bash -c "cd /root/document; sphinx-build -a -d _build/.doctrees/ja -b html ja _build/html"
…
build succeeded, 1 warning.

$ （警告の全件）
/root/document/ja/application_framework/application_framework/libraries/db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test (if the link has no caption the label must precede a section header)
```

| 項目 | 期待 | 実測 |
|---|---|---|
| ビルド結果 | `build succeeded` | `build succeeded, 1 warning.` |
| 警告 | 既知の `db_double_submit.rst:108` のみ | 同左1件 |
| 新規警告 | 0件 | 0件 |

生成HTMLで表・`important` の描画も確認した（`_build/html/development_tools/testing_framework/about/index.html`）。対比表の取引単体テスト行と `important` の本文が意図どおり出力されている。

ビルド直後の後始末。

```
$ git status --porcelain
 M .rn/20260724-ntf-yaml-support/design.md
 M .rn/20260724-ntf-yaml-support/mapping/style.md
 M ja/development_tools/testing_framework/about/index.rst
 M locales/ja/LC_MESSAGES/sphinx.mo

$ git checkout -- locales/ja/LC_MESSAGES/sphinx.mo
$ git status --porcelain
 M .rn/20260724-ntf-yaml-support/design.md
 M .rn/20260724-ntf-yaml-support/mapping/style.md
 M ja/development_tools/testing_framework/about/index.rst
```

**判定: PASS**（`sphinx.mo` は戻し済み）

---

## ゲート12: `commit & push` 直前の `git status --porcelain` 再実行

```
$ git status --porcelain
 M .rn/20260724-ntf-yaml-support/design.md
 M .rn/20260724-ntf-yaml-support/mapping/style.md
 M .rn/20260724-ntf-yaml-support/reviews/page-about_index.md
 M ja/development_tools/testing_framework/about/index.rst
?? .rn/20260724-ntf-yaml-support/checks/task-24.md
```

| # | パス | 状態 | 変更してよいファイルか | コミット対象か |
|---|---|---|---|---|
| 1 | `.rn/20260724-ntf-yaml-support/design.md` | M | 可 | 対象 |
| 2 | `.rn/20260724-ntf-yaml-support/mapping/style.md` | M | 可 | 対象 |
| 3 | `.rn/20260724-ntf-yaml-support/reviews/page-about_index.md` | M | 可 | 対象 |
| 4 | `ja/development_tools/testing_framework/about/index.rst` | M | 可 | 対象 |
| 5 | `.rn/20260724-ntf-yaml-support/checks/task-24.md` | ?? | 可（新規作成） | **対象外**（作業指示 §6） |

明示的にパスを列挙してステージした（`git add -A`・`git add .` は使用していない）。

```
$ git add .rn/20260724-ntf-yaml-support/design.md .rn/20260724-ntf-yaml-support/mapping/style.md \
    ja/development_tools/testing_framework/about/index.rst .rn/20260724-ntf-yaml-support/reviews/page-about_index.md
$ git diff --cached --name-only
.rn/20260724-ntf-yaml-support/design.md
.rn/20260724-ntf-yaml-support/mapping/style.md
.rn/20260724-ntf-yaml-support/reviews/page-about_index.md
ja/development_tools/testing_framework/about/index.rst
```

**判定: PASS**（変更してよいファイル以外 0件。`checks/task-24.md` は未ステージ）

---

## Completion criteria の自己判定

| # | 項目 | 判定 | 根拠 |
|---|---|---|---|
| 1 | `design.md:84` の「実行方法」セルを、処理方式によって異なると分かる内容に改めた | OK | ゲート4 #1。`ウェブアプリケーションは手動操作、それ以外の処理方式はJUnitで自動実行` |
| 2 | `design.md:84` の「備考」セルを、ウェブアプリケーションの場合に限る旨が分かる内容に改めた | OK | ゲート4 #1。`手動操作の場合はAPサーバへのデプロイが必要。…` |
| 3 | `design.md:86` を「実施方法が処理方式によって異なることを明示する」に相当する内容へ差し替えた | OK | ゲート4 #2。出典5件を添えた1段落に差し替え |
| 4 | `about/index.rst:73`・`:75` に1・2を反映し、`:77-79` の `important` を差し替えた（削除していない） | OK | ゲート3。`.. important::` 行は無変更で本文のみ差し替え |
| 5 | `style.md:45` を、順序の規約と必須・任意の区別の両方を含む記述に改めた | OK | ゲート5 #1 |
| 6 | `style.md` の `design.md` 参照を節見出しで指す形に改めた | OK | ゲート5 #2 |
| 7 | 処理方式の名称は `glossary.md` §5.2 の正表記 | OK | ゲート7 |
| 8 | `about/index.rst:83-94` の内訳表を変更していない | OK | ゲート6（diff 0件） |
| 9 | 取引単体テストの処理方式ごとの一覧表を新設していない | OK | ゲート3（追加した行は0行。表の新設なし） |
| 10 | 日本語の地の文は1段落1行 | OK | `about/index.rst:79` は1行。`design.md:86` も1行 |
| 11 | 対比表が `list-table` 形式であることを確認したうえで編集した | OK | `about/index.rst:56-58` が `.. list-table::` ＋ `:header-rows: 1` ＋ `:widths: 20,20,30,30`。編集は `* -` 行の継続行（`    - `）のみで、simple table の幅合わせは不要 |
| 12 | 内部設計文書の言い回しをそのまま使っていない | OK | `連続実行` は現行解説書の `batch.rst:6`・`rest.rst:7`・`real.rst:10` が使う語（`grep -rn 連続実行 ja/` で実測）。`対象とする処理方式によって` は同ページ `:83` の既存表現に揃えた |
| 13 | `design.md` の他の確定事項と両立する | OK | 下記「design.md の確定事項との両立確認」 |
| 14 | `reviews/page-about_index.md` に `#24` の節を追記した（既存は書き換えない） | OK | 末尾に `## `#24`（取引単体テストの実施方法の是正、2026-08-14）` を追加。既存行は無変更 |
| 15 | `mapping.csv` を変更していない | OK | ゲート2・ゲート10 |

### `design.md` の確定事項との両立確認（`:88`・`:90`・`:92`・`:94` を実際に開いて確認）

| 行 | 確定事項（要旨） | 両立するか |
|---|---|---|
| `:88` | リクエスト単体テストの処理方式ごとの内訳は対比表の直後に地の文で続ける。独立した「正式名称」見出しは置かない | 両立。見出しは増やしていない。`important` は対比表と内訳の地の文（`:83`）の間に元からあり、位置も変えていない |
| `:90` | 内訳の表は、リクエスト単体テストの6処理方式のみを載せる。クラス単体テスト・取引単体テストの行は載せない | 両立。内訳表は無変更（ゲート6）。取引単体テストの処理方式ごとの一覧表は新設していない |
| `:92` | 内訳表の列見出しは「テスト種別」ではなく「処理方式」とする | 両立。内訳表は無変更 |
| `:94` | 「対象範囲」は独立セクションとせず「テストの種類」の末尾に統合する | 両立。`:96-102` の `important` 2件は無変更 |

---

## 判断を要する事項（コーディネータ・ユーザーへ）

いずれも本タスクの「変更してはならないファイル」または「変更してよいファイル」の範囲外の行にあたるため、**手を付けていない**。

### 1. `glossary.md` §5.5 の `取引単体テスト` の意味欄が旧認識のまま

`mapping/glossary.md:168` は `| `取引単体テスト` | 複数リクエストにまたがる業務の流れを**手動操作で確認する**テスト | …` と書いている（実測）。本タスクの是正と矛盾する。`glossary.md` は変更してはならないファイルのため未修正。

### 2. `style.md` の「根拠」ブロックの `design.md` 参照も同じくずれている

ゲート5で改めたのは `:55-56` の1文のみである。同じ `style.md` の「**根拠**（design.mdの決定）」ブロック（現 `:76-80`）は、同一のずれた行番号をそのまま持つ。実測結果は次のとおり。

| 現 style.md の記述 | `design.md` の実際の内容（実測） |
|---|---|
| `design.md:76-88` 第2部ページのアウトライン | `### 「テストの種類」に置く対比`（第1部）の節と本文 |
| `design.md:132-141` 第3部ページのアウトライン | `### モジュール一覧は第1部に置かない。…` 節の本文 |
| `design.md:143` 「拡張例は第3部に置かない。…」 | `check_unused_vocabulary` に関する記述。当該文は実際には `design.md:260` |
| `design.md:48-52` 「モジュール一覧の集約」節 | `### 「全体像」と「特徴」を1つの節に統合し…` 節の本文。「モジュール一覧の集約」という節は `design.md` に存在しない（`grep -n 'モジュール一覧の集約' design.md` が0件）。同節の方針は `design.md:139` で「`#6`の「処理方式ごとのページには置かない」という集約方針を撤回」と明記されており、現行の該当節は `### モジュール一覧は第1部に置かない。…`（`:118`） |
| `design.md:34` 第1部「稼動環境」への記載 | `| 1 | 全体像 | …`。「稼動環境」の行は `design.md:37` |

指示書のゲート5は「`:45`（と `:56-57` の参照先表記）以外の変更が0件」を判定基準にしているため、範囲を自分で広げず未修正のままとした。**別タスクとして是正するか、本タスクに含めるかの判断を求める。**

### 3. 「ウェブアプリケーション以外はすべて自動」の出典カバレッジ

出典が直接カバーするのは、ウェブアプリケーション（手動）・Nablarchバッチアプリケーション（自動）・RESTfulウェブサービス（自動）・MOMによるメッセージング（自動）の4処理方式である。`HTTPメッセージング` と `テーブルをキューとして使ったメッセージング` については、`03_DealUnitTest/` に実施方法を述べた出典が無い（実測: 同ディレクトリの `.rst` は8ファイルで全件）。

このうち `取引単体テスト（HTTPメッセージング）` に割り当てられている出典（`mapping.csv` の `current-0138`・`current-0139`、いずれも `http_send_sync.rst`）と、`取引単体テスト（MOMによるメッセージング）` に割り当てられている `current-0154`・`current-0155`・`current-0156-b`・`current-0157`（いずれも `send_sync.rst`）は、本文が「（HTTP）同期応答メッセージ送信処理を伴う**ウェブアプリケーション**で、取引単体テストを行う場合は…」であり、内容としては手動側（ウェブアプリケーション）に属する。

したがって、第3部の `取引単体テスト（HTTPメッセージング）`・`取引単体テスト（MOMによるメッセージング）` の2ページは、**自動実行の説明とモックアップクラスによる手動テストの説明の両方を抱えることになる**。ページ作成時に扱いを決める必要がある。本タスクでは `mapping.csv` を変更していない。

---

## 4観点レビュー ラウンド1（コーディネータ記入）

各観点を別々のサブエージェントで実施した。self-check ファイル・実装担当の要約・他観点の判定はいずれも渡していない（中立の枠組み）。

| 観点 | 判定 | `must` | `should` | `note` |
|---|---|---|---|---|
| QA（検証のやり方が目的に照らして意味を持つか） | **FAIL** | 4 | 2 | 3 |
| 設計（構造の適合・文書間整合） | **FAIL** | 1 | 7 | 4 |
| クラフト（文章） | **FAIL** | 2 | 5 | 3 |
| 検証（ファクトチェック） | **FAIL** | 3 | 4 | 4 |

**4観点とも独立に同一の核心へ到達した。** 重複を除いた `must` は次の1件に集約される。

**M-1（公開本文の事実誤り）**: `about/index.rst:73`・`:79` の「それ以外の処理方式はJUnitで自動実行」が、出典を持たない処理方式まで断定で覆っている。`design.md:86` の「全件確認した結果」も同じ穴を持つ（挙げている出典は3処理方式ぶんのみ）。

コーディネータが独立に作成した全件表（母集合は `glossary.md` §5.2 の正表記7件から NTF 対象外の `Jakarta Batchに準拠したバッチアプリケーション` を除いた6件。出典は `mapping.csv` の `dest_page` から機械的に引いた）。

| # | 処理方式 | 取引単体テストの出典 | 出典が述べる実施方法 |
|---|---|---|---|
| 1 | ウェブアプリケーション | `index.rst`（current-0142〜0145）・`double_transmission.rst`（current-0059） | 手動 |
| 2 | RESTfulウェブサービス | `rest.rst`（current-0148/0149） | 自動 |
| 3 | Nablarchバッチアプリケーション | `batch.rst`（current-0128-a〜0134） | 自動 |
| 4 | MOMによるメッセージング | `real.rst`（current-0147）・`delayed_*`（current-0135/0136）＝自動 ＋ `send_sync.rst`（current-0154〜0157）＝手動 | **混在** |
| 5 | HTTPメッセージング | `http_send_sync.rst`（current-0138/0139）のみ | **手動のみ。自動の出典0件** |
| 6 | テーブルをキューとして使ったメッセージング | **0件**（`design.md:240` が導線のみと明記） | **出典なし** |

**自動と言い切れるのは6分の2〜3。** 旧版が `index.rst` 1ページの記述を全体へ広げたのと構造的に同型の過度一般化であり、向きが反転しただけである。

### M-1 の根にある未決着（本タスクの範囲では解けない）

`send_sync.rst`・`http_send_sync.rst` の帰属が、出典自身の構成と `mapping.csv` とで食い違う。

- **出典自身の構成**: 旧 `05_UnitTestGuide/index.rst:16-27` の `toctree` は、`03_DealUnitTest/send_sync`・`03_DealUnitTest/http_send_sync` を `03_DealUnitTest/index`・`double_transmission` と同じ **\*ウェブアプリケーション\*** 節に置いている（RESTful は `:30-37`、バッチは `:40-47`、メッセージングは `:49-` と別節）。本文も `send_sync.rst:7`・`http_send_sync.rst:7` がともに「〜を伴う**ウェブアプリケーション**で」と書く
- **`mapping.csv`**: `current-0154`〜`0157` を `取引単体テスト（MOMによるメッセージング）`、`current-0138`/`0139` を `取引単体テスト（HTTPメッセージング）` に割り当てている

どちらを正とするかで結論が変わる。`mapping.csv` が正なら「手動なのはウェブアプリケーションだけ」は偽。出典の構成が正なら `mapping.csv` の6行が誤りで、`取引単体テスト（HTTPメッセージング）` は出典0件となり第3部のページ構成（`design.md:240` の6ページ）の見直しに波及する。**`mapping.csv` は本タスクの変更禁止ファイルであり、ユーザー判断に上げる。**

なお**どちらに決まっても**、`テーブルをキューとして使ったメッセージング`（出典0件）は「それ以外の処理方式」に含まれてしまう。包括表現をやめて処理方式を名指しすれば、帰属の決着を待たずに公開本文を正しくできる。

### 4観点が挙げた `should`（重複除去後。M-1 の結論が出てから一括で処理する）

| # | 観点 | 内容 |
|---|---|---|
| S-1 | QA・クラフト | `about/index.rst:75` の備考セル第2文「エビデンスは画面ハードコピー・DBダンプ」が無スコープ。第1文だけに「手動操作の場合は」を付けたため係りが割れ、取引単体テスト全体のエビデンスと読める。出典 `index.rst:39-40` はウェブアプリケーション限定 |
| S-2 | クラフト | `実行方法`（表の列見出し `:61`・リード文 `:54`）と `実施方法`（`important` `:79`）の揺れ。本コミットが持ち込んだ |
| S-3 | クラフト | `important` 3文のうち2文が直前の表セルの言い換え。`style.md` S-06 の important の定義（守るべき注意事項）にも合致しない。表直後の地の文にするのが妥当 |
| S-4 | クラフト | `:widths: 20,20,30,30`（`:58`）が実測比（約 9:32:16:44）と乖離。実行方法列だけ同列他行の4.6倍に伸びた |
| S-5 | クラフト・設計 | 「それ以外の処理方式」が同ページ `:98`「Jakarta Batchに準拠したバッチアプリケーションを対象としていない」と衝突する。`処理方式` の初出が `:73` で、6分類の定義は `:83-94`（前方参照） |
| S-6 | 全観点 | `glossary.md:168` の `取引単体テスト` の意味欄が「複数リクエストにまたがる業務の流れを**手動操作で確認する**テスト」のまま。同じ表の `クラス単体テスト`・`リクエスト単体テスト` は「JUnitで自動実行する」と定義されており、対比構造の中で取引単体テストだけが手動と定義されている。**変更禁止ファイルのため未着手** |
| S-7 | 設計・検証 | `style.md` に `design.md` の行番号参照が**10件残存**し、全件が誤った位置を指す。うち `:77`（`design.md:76-88`）・`:78`（`design.md:132-141`）は**今回 `:56` で直したのと同一の参照**。`:65` の `design.md:50` に至っては引用文字列が `design.md` に存在しない |
| S-8 | 設計・検証 | `style.md:45-46`（今回の是正）と `:77`（「第2部ページのアウトライン。機能概要→使用方法→拡張例の3セクション」）が自己矛盾 |
| S-9 | 設計・検証 | `style.md:53-54`・`:62-67`・`:80-81` が根拠にする「依存関係は第1部『稼動環境』に集約し、処理方式ごとのページには置かない」は、`design.md:139` で**撤回済み**（「`#6`の「処理方式ごとのページには置かない」という集約方針を撤回」）。行番号のずれではなく規約の内容が追随できていない |
| S-10 | 設計 | `style.md:69-73` が「拡張例」を「見出しは置き、本文に『なし。』とだけ書く」選択肢を残しており、今回 `:45-46` で規約化した一択と二枚舌。実ページに「なし。」は0件 |
| S-11 | 設計 | `reviews/page-about_index.md` §#24 に `style.md` の監査結果が入っている。`about/index.rst` のページレビュー記録としては宛先が違う |
| S-12 | クラフト | `design.md:84`（`APサーバ`）と `about/index.rst:75`（`アプリケーションサーバ`）が逐語一致でなくなった。是正前は完全一致していた。公開本文側が正（新NTFページに `APサーバ` は0件） |
| S-13 | QA | `delayed_send.rst:5-6` は本文（「同期応答メッセージ**送信**処理と同じ」＝`send_sync.rst`＝手動）とリンク（`./real`＝受信処理＝自動）が食い違う自己矛盾した出典。自動に分類した判断根拠が `design.md:86` に書かれていない |

### 実測で OK と確認できた項目（4観点の一致）

- 完了条件（ゲート1〜12 相当）は**全項目 OK**。差分は許可された4ファイルのみ、ハンクも `about/index.rst` 3件・`design.md` 2件・`style.md` 2件に収まる
- 出典5件の `file:line` と記述は**全件逐語一致**（3観点が独立に突合）
- 内訳表（`:83-94`）の反映前後 `diff` は0件。取引単体テストの一覧表の新設なし
- `style.md:45-46` の新しい規約は `design.md:180`・`:185`・`:189`・`:194`・`:783` と一致し、実ページ8件の実態（全ページ「使用方法」のみ・「拡張例」3ページ・「機能概要」0ページ）とも一致
- `style.md:56-58` の新しい節見出し参照は実在し一意（`design.md:147` ＞ `:173`、`:213` ＞ `:242`）
- `reviews/page-about_index.md` の「`input-0028` に実行方法列・備考列が無い」は逐語的に正確（`dest_section=テストの種類` は595行中 `input-0028` 1件のみ、`ntf-doc-terms.md:416-417` は2列表）
- Docker フルビルド（`-a`）は `build succeeded, 1 warning.`／警告は既知の `db_double_submit.rst:108` のみ・**新規0件**（検証観点が独立に再実行）。`sphinx.mo` は復元済み

## Overall Verdict

- Self-check: OK（実装担当記入）
- QA: **NG**
- Design expert: **NG**
- Craft expert: **NG**
- Verification expert: **NG**
- Ready to check off: **No** — `must` 1件（M-1）が未解決。M-1 は `mapping.csv`（本タスクの変更禁止ファイル）の帰属の決着と、レビュー役が示した「手動なのはウェブアプリケーションだけであり、他はすべて自動である」という前提そのものの見直しを要するため、**是正を回さずユーザー判断に上げた**（`#22` 回答 §7「範囲を自分で広げない」に従う）
