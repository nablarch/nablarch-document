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

---

# `#24` セルフチェック — ラウンド2（`ntf-doc-24-round2.md` に基づく是正）

実施日: 2026-08-14 / 起点コミット: `5393971`（作業ツリーはクリーン）/ ブランチ: `ntf-yaml-support`

ラウンド1の記述（上記）は1行も書き換えていない。本節はラウンド2の実施結果のみを記録する。本ファイルはコミットしない。

## ラウンド1 ゲート1〜12 の再実行

### ゲート1: `git status --porcelain` の全件（着手直後）

```
$ git status --porcelain
（出力なし。作業ツリーはクリーン）
```

**判定: PASS**（変更してよいファイル以外 0件）

### ゲート2: 出典の突合（`git show 2e501ad:<path>`）— 指示書 §2-1 の表との一致

指示書 §2-1 の実測を、レビュー役の表を見る前に自分で独立に再取得した。

```
$ D=ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest
$ git ls-tree -r --name-only 2e501ad -- $D
（.rst は batch/delayed_receive/delayed_send/http_send_sync/index/real/rest/send_sync の8件。他は _images/ の画像14件のみ）
$ for f in index batch rest real delayed_send delayed_receive send_sync http_send_sync; do
    git show 2e501ad:$D/$f.rst | grep -n "手動\|自動\|連続実行"; done
```

| ファイル | 実測した該当行 | 指示書 §2-1 の記述 | 一致 |
|---|---|---|---|
| `index.rst` | `8:手動でアプリケーションを操作しテストを行う。` | 手動 | 一致 |
| `batch.rst` | `5:バッチ処理の取引単体テストは、自動テストフレームワークを使用してテストを行う。` / `6:リクエスト単体テストを連続実行することにより、取引単位でのテストを行う。` | 自動 | 一致 |
| `rest.rst` | `7:ただし、複数のリクエストにより取引が成立する場合は、リクエスト毎のテストを連続実行することにより取引単体テストが実施可能である。` | 自動 | 一致 |
| `real.rst` | `10:リクエスト毎のテストを連続実行することにより取引単体テストが実施可能である。` | 自動 | 一致 |
| `delayed_send.rst` | 0件 | 0件 | 一致 |
| `delayed_receive.rst` | 0件 | 0件 | 一致 |
| `send_sync.rst` | `151:…サイズを自動計算する。` / `176:モックアップクラスは、Excelファイルを手動で編集して…` / `207: | …|  自動テストフレームワークの動作 |` | いずれも実施方法ではない | 一致 |
| `http_send_sync.rst` | **0件** | 0件 | 一致 |

補助的に本文冒頭20行も全8ファイル分を実測し、次を確認した（いずれも §2-1 と一致）。

- `delayed_send.rst` は全7行。`:5` 「取引単体テストの実施方法は、同期応答メッセージ送信処理と同じである。」、`:6` 「実施方法の詳細は\ :doc:`./real`\ を参照すること。」。本文が指す先（同期応答メッセージ送信処理＝`send_sync.rst`）とリンク先（`./real`）が食い違う。
- `delayed_receive.rst` は全7行。`:5` 「取引単体テストの実施方法は、同期応答メッセージ受信処理と同じである。」、`:6` は同じく `./real` へのリンク。本文とリンク先が一致する。
- `real.rst:2` のページ題は「取引単体テストの実施方法（同期応答メッセージ受信処理)」（閉じ括弧は半角）。
- `send_sync.rst:7`・`http_send_sync.rst:7` は「（HTTP）同期応答メッセージ送信処理を伴うウェブアプリケーションで、取引単体テストを行う場合は、Nablarchが提供するモックアップクラスを使用する。」。

**判定: PASS**（§2-1 の表と全件一致。食い違い0件のため停止せず本文に着手した）

### ゲート3: `about/index.rst` の差分（全件）

```
$ git diff -U0 ja/development_tools/testing_framework/about/index.rst | grep '^@@'
@@ -58 +58 @@
@@ -73 +73 @@
@@ -75 +75 @@
@@ -79 +79 @@
```

| # | 行 | 変更前 | 変更後 |
|---|---|---|---|
| 1 | `:58` | `  :widths: 20,20,30,30` | `  :widths: 9,26,16,49` |
| 2 | `:73` | `    - ウェブアプリケーションは手動操作、それ以外の処理方式はJUnitで自動実行` | `    - 処理方式によって異なる（手動操作またはJUnitで自動実行）` |
| 3 | `:75` | `    - 手動操作の場合は、アプリケーションサーバへのデプロイが必要。エビデンスは画面ハードコピー・DBダンプ` | `    - 手動操作の場合は、アプリケーションサーバへのデプロイが必要で、エビデンスは画面ハードコピー・DBダンプとなる` |
| 4 | `:79` | ラウンド1の3文（「それ以外の処理方式では」を含む） | 指示書 §2-2 の確定文言（4処理方式を名指しする3文） |

ハンクは4つのみ。行数は増減していない（`wc -l` = 117 で前後不変）。`.. important::` 行（`:77`）と空行は無変更。地の文は1段落1行（`:79` は1行）。

**判定: PASS**（`:58`・`:73`・`:75`・`:79` 以外の変更 0件）

### ゲート4: `design.md` の差分（全件）

```
$ git diff -U0 .rn/20260724-ntf-yaml-support/design.md | grep '^@@'
@@ -84 +84 @@
@@ -86 +86 @@
```

`:84` は対比表の取引単体テスト行、`:86` は直後の段落。行数は増減していない（`--numstat` = 2 insertions / 2 deletions）。

**判定: PASS**（`:84`・`:86` 以外の変更 0件）

### ゲート5: `style.md` の差分（全件）

```
$ git diff -U0 .rn/20260724-ntf-yaml-support/mapping/style.md | grep '^@@'
@@ -53,2 +53,2 @@
@@ -62,4 +62,5 @@
@@ -67 +68 @@
@@ -69,5 +70,3 @@
@@ -77,5 +76,11 @@
```

変更前の行番号でのハンク範囲は `:53-54`・`:62-65`・`:67`・`:69-73`・`:77-81` であり、いずれも作業指示が許した範囲（`:45-46`・`:53-54`・`:62-67`・`:69-73`・`:77`〜`:81`）に収まる。`:45-46`（ラウンド1で確定した必須・任意の規約）は今回変更していない（`:77` 側を `:45-46` に合わせたため。S-8）。

**判定: PASS**（許可範囲外の変更 0件）

### ゲート6: `about/index.rst` の内訳表（現 `:83-94`）の反映前後 `diff`

```
$ git show HEAD:ja/.../about/index.rst | sed -n '83,94p' > before.txt
$ sed -n '83,94p' ja/.../about/index.rst > after.txt
$ diff before.txt after.txt
（出力なし）
```

**判定: PASS**（差分 0件）

### ゲート7: 処理方式の名称が `glossary.md` §5.2 の正表記であること

`glossary.md` §5.2（`:123-137`）を実測し、`about/index.rst:79` と `design.md:86` が名指しする4処理方式を突合した。

| 名称 | `glossary.md` の正表記行 | 使用箇所 |
|---|---|---|
| `ウェブアプリケーション` | `:131` | `about:79`、`design:86` |
| `RESTfulウェブサービス` | `:132` | `about:79`、`design:86` |
| `Nablarchバッチアプリケーション` | `:134` | `about:79`、`design:86` |
| `MOMによるメッセージング` | `:135` | `about:79`、`design:86` |
| `HTTPメッセージング` | `:133` | `design:86` のみ（「述べない」という決定の記述）。`about:79` には現れない |
| `テーブルをキューとして使ったメッセージング` | `:136` | `design:86` のみ。`about:79` には現れない |

出典の呼称（`バッチ処理`・`同期応答メッセージ受信処理`等）は公開本文に持ち込んでいない。`design.md:86` に現れるのは出典ファイル名と、出典を引用した「」内のみ。

**判定: PASS**（逸脱 0件）

### ゲート8: 見出し下線を `style.md` S-04 の実測則で確認

```
$ grep -n '^[-~^=]\{3,\}$' ja/development_tools/testing_framework/about/index.rst
4(=), 13/53/107/116(-), 19/23/27/31(~)
```

L1=`=`、L2=`-`、L3=`~`。見出し行・下線行は差分（ゲート3の4ハンク）に一切含まれていない。

**判定: PASS**（逸脱 0件）

### ゲート9: `verify_mapping.py`

```
$ python3 .rn/20260724-ntf-yaml-support/mapping/tools/verify_mapping.py
Loaded 595 rows from mapping.csv
lines total (all rows): 12986
lines total (excluding DROP): 11983
OK: no errors
exit=0
```

| 項目 | 期待 | 実測 |
|---|---|---|
| exit code | 0 | 0 |
| rows | 595 | 595 |
| lines total (all rows) | 12,986 | 12986 |
| lines total (excluding DROP) | 11,983 | 11983 |

advisory の内訳（44 / 2 / 5 / 18）もラウンド1と同一である。

**判定: PASS**

### ゲート10: 変更してはならないファイルの差分

| 対象 | 差分 |
|---|---|
| `mapping/mapping.csv` | 0件 |
| `mapping/_batch/` | 0件 |
| `mapping/volume.md` | 0件 |
| `mapping/vocabulary.md` | 0件 |
| `mapping/glossary.md` の `:168` 以外（特に §5.15、`:331-456`） | 0件（ゲートF） |
| `ja/conf.py` | 0件 |
| `about/index.rst` 以外の `ja/` 配下 | 0件 |
| `steering.md` | 0件 |
| `reviews/` の `#24` 節より前 | 0件（ゲートG） |
| `ntf-doc-*.md` | 0件 |

`git status --porcelain` に現れるのは許可された5ファイルのみ。

**判定: PASS**（0件）

### ゲート11: Docker フルビルド（`-a`）

ゲートH と同一。下記「ゲートH」を参照。

**判定: PASS**

### ゲート12: `commit & push` 直前の `git status --porcelain` 再実行

ゲートI と同一。下記「ゲートI」を参照。

**判定: PASS**

## 指示書 §5-3 ゲートA〜I

### ゲートA: 閉じた表現が0件

```
$ grep -n "それ以外\|すべての処理方式" ja/development_tools/testing_framework/about/index.rst
（出力なし）
```

**判定: PASS**（0件）

### ゲートB: `:79` の処理方式が正表記と逐語一致し、4処理方式に一致

`:79` が名指しするのは `ウェブアプリケーション`・`RESTfulウェブサービス`・`Nablarchバッチアプリケーション`・`MOMによるメッセージング` の4つで、いずれも `glossary.md` §5.2 の正表記と逐語一致する（ゲート7の表）。指示書 §2-1 の4処理方式と一致する。

```
$ grep -n 'HTTPメッセージング\|テーブルをキューとして使ったメッセージング' ja/.../about/index.rst
90:リクエスト単体テスト（HTTPメッセージング） …
93:リクエスト単体テスト（テーブルをキューとして使ったメッセージング） …
```

該当はリクエスト単体テストの内訳表（変更禁止、`:83-94`）の2行のみで、`:79` には現れない。

**判定: PASS**

### ゲートC: `design.md:84` と `about/index.rst:73`・`:75` の逐語一致、`APサーバ` 0件

Python で `design.md:84` を `|` 分割し、`about/index.rst` の該当セルから `    - ` を除いた文字列と比較した。

```
design:84 実行方法セル = [処理方式によって異なる（手動操作またはJUnitで自動実行）]
about:73               = 処理方式によって異なる（手動操作またはJUnitで自動実行）        → 一致
design:84 備考セル     = [手動操作の場合は、アプリケーションサーバへのデプロイが必要で、エビデンスは画面ハードコピー・DBダンプとなる]
about:75               = 同上                                                            → 一致
$ grep -rn 'APサーバ' .rn/20260724-ntf-yaml-support/design.md ja/development_tools/testing_framework/
（出力なし）
```

**判定: PASS**（逐語一致、`APサーバ` 0件）

### ゲートD: `実施方法` が0件で `実行方法` に統一（出典の引用箇所を除く）

```
$ grep -n '実施方法' ja/development_tools/testing_framework/about/index.rst
（出力なし）
$ grep -n '実施方法' .rn/20260724-ntf-yaml-support/design.md
86: …（2箇所。いずれも出典の引用「」の内側）
601: heading_path  リクエスト単体テストの実施方法 > …（`mapping.csv` の行の例示。出典側の見出しパスの引用）
```

`design.md:86` の2箇所は「取引単体テストの実施方法は、同期応答メッセージ送信処理と同じである。」（`delayed_send.rst:5` の逐語引用）と「取引単体テストの実施方法（同期応答メッセージ受信処理)」（`real.rst:2` のページ題の逐語引用）であり、いずれも出典の引用箇所。`:601` は `## 10.3 トレーサビリティ` の `mapping.csv` 行の例示（`heading_path` は出典側の見出しパス）で、本タスクの変更対象外かつ引用箇所。

**判定: PASS**（地の文の `実施方法` 0件。`design.md:86` 冒頭は `**取引単体テストの実行方法が処理方式によって異なることを明示する。**`）

### ゲートE: `style.md` の `design.md:` 行番号参照が0件、置き換え先の節見出しが実在し一意

```
$ grep -c 'design\.md:[0-9]' .rn/20260724-ntf-yaml-support/mapping/style.md
0
```

置き換え先の全件（`grep -n` の実測）。

| 置き換え先の指し方 | `design.md` の実測 | 一意性 |
|---|---|---|
| 「3. 第2部 導入と設定」＞「ページのアウトライン」 | `^## 3\. 第2部 導入と設定$` は `:147` の1件。その節（`:147-212`）内の `^### ページのアウトライン$` は `:173` の1件 | 親が一意、親の中で子が一意 |
| 「4. 第3部 テストの実装方法」＞「ページのアウトライン」 | `^## 4\. 第3部 テストの実装方法$` は `:213` の1件。その節（`:213-290`）内の `^### ページのアウトライン$` は `:242` の1件（次の見出しは `:269 ### テストデータの2ページ`） | 同上 |
| 同節「拡張例は第3部に置かない。…」 | `^\*\*拡張例は第3部に置かない。` は `:260` の1件。`:242-268` の内側であり「同節」が正しい | 一意 |
| 「モジュール一覧は第1部に置かない。「稼動環境」は対応バージョンの premise 1文＋`:ref:`のみとする」 | `^### モジュール一覧は第1部に置かない` は `:118` の1件（節は `:118-146`） | 一意 |

`### ページのアウトライン` は単独では3件（`:173`・`:242`・`:303`。`:303` は `## 5. 第4部 ツール`（`:291`）配下）であるため、`style.md` では必ず親節（`## 3.` / `## 4.`）と組にして指している。組は上表のとおり一意である。

**判定: PASS**

### ゲートF: `glossary.md` の差分が `:168` の1行のみ、§5.15 の差分0件

```
$ git diff -U0 .rn/20260724-ntf-yaml-support/mapping/glossary.md | grep '^@@'
@@ -168 +168 @@
$ git diff --numstat .rn/20260724-ntf-yaml-support/mapping/glossary.md
1       1       .rn/20260724-ntf-yaml-support/mapping/glossary.md
```

変更したのは §5.5（`:163-`）の `取引単体テスト` 行の**意味欄のみ**。

- 変更前: `複数リクエストにまたがる業務の流れを手動操作で確認するテスト`
- 変更後: `複数リクエストにまたがる業務の流れを対象とするテスト`

揺れ表記列（`揺れなし`）・別義列（`なし`）・採用根拠列（`現行解説書40件（…double_transmission.rst:9）、S:design.md:31`）は変更していない。§5.15 は `:331-456`（`### 5.15 …` が `:331`、次の `## 6.` が `:457`）であり、唯一のハンクが `:168` であることから差分0件。

**判定: PASS**

### ゲートG: `reviews/page-about_index.md` の変更行が `## #24` 節の内側だけ

`## \`#24\`` 節は `:322` から始まる（`grep -n '#24' reviews/page-about_index.md`）。

```
$ git diff -U0 .rn/.../reviews/page-about_index.md | grep '^@@'
（すべて -322 以降。最小のハンク開始行は 322）
$ git diff -U0 3c7d6ac -- .rn/.../reviews/page-about_index.md | grep '^@@'
@@ -320,0 +321,61 @@
```

`#24` に着手する前のコミット `3c7d6ac` と作業ツリーの差分が「`:320` の後ろへの純粋な追加」1ハンクだけであることから、`#24` 節より前の全行が無変更であることが機械的に示される。

`style.md` の監査結果（ラウンド1で本ファイルに書いていた「`style.md` の `design.md` 参照が行番号でずれていた実測結果」節）は削除し、本チェックファイル（ゲートE・下記「S-7〜S-10 の突合」）に移した。S-11 の指示どおり。

**判定: PASS**

### ゲートH: Docker フルビルド（`-a`）

`docker build` は本環境のプロキシの自己署名証明書により pip が pypi.org を検証できず失敗する（`SSLError(SSLCertVerificationError… self-signed certificate in certificate chain)` → `ERROR: No matching distribution found for setuptools==57.5.0`）。イメージ `nablarch-document-build:latest`（IMAGE ID `a974e0c8ac60`）は既存であり、ラウンド1と同一のイメージでビルドした。イメージの再作成は本タスクの変更内容と無関係（`Dockerfile`・`requirements.txt` は無変更）。

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

生成HTML（`_build/html/development_tools/testing_framework/about/index.html`）を実測した。

- 対比表の `<colgroup>` は `9% / 26% / 16% / 49%`（`:widths:` が反映されている）。
- 取引単体テスト行のセルは「処理方式によって異なる（手動操作またはJUnitで自動実行）」「手動操作の場合は、アプリケーションサーバへのデプロイが必要で、エビデンスは画面ハードコピー・DBダンプとなる」。
- `class="admonition important"` は3件。1件目が今回の本文で、1段落として出力されている（段落途中の改行に由来する余分な空白は無い）。

ビルド直後の後始末。

```
$ git status --porcelain
 M …（許可された成果物5ファイル + checks/task-24.md）
 M locales/ja/LC_MESSAGES/sphinx.mo
$ git checkout -- locales/ja/LC_MESSAGES/sphinx.mo
$ git status --porcelain
 M .rn/20260724-ntf-yaml-support/design.md
 M .rn/20260724-ntf-yaml-support/mapping/glossary.md
 M .rn/20260724-ntf-yaml-support/mapping/style.md
 M .rn/20260724-ntf-yaml-support/reviews/page-about_index.md
 M ja/development_tools/testing_framework/about/index.rst
```

`sphinx.mo` は `git status --porcelain` に現れない。`locales/` は `.gitignore` に加えていない。

**判定: PASS**

### ゲートI: `commit & push` 直前のゲート1再実行

```
$ git status --porcelain
 M .rn/20260724-ntf-yaml-support/checks/task-24.md
 M .rn/20260724-ntf-yaml-support/design.md
 M .rn/20260724-ntf-yaml-support/mapping/glossary.md
 M .rn/20260724-ntf-yaml-support/mapping/style.md
 M .rn/20260724-ntf-yaml-support/reviews/page-about_index.md
 M ja/development_tools/testing_framework/about/index.rst
```

| # | パス | 状態 | 変更してよいファイルか | コミット対象か |
|---|---|---|---|---|
| 1 | `.rn/20260724-ntf-yaml-support/checks/task-24.md` | M | 可（追記のみ） | **対象外**（作業指示 §5）。ラウンド1の本ファイルはコーディネータが `db5a84a` でコミット済みのため、状態は `??` ではなく `M` である |
| 2 | `.rn/20260724-ntf-yaml-support/design.md` | M | 可 | 対象 |
| 3 | `.rn/20260724-ntf-yaml-support/mapping/glossary.md` | M | 可（`:168` の意味欄のみ） | 対象 |
| 4 | `.rn/20260724-ntf-yaml-support/mapping/style.md` | M | 可 | 対象 |
| 5 | `.rn/20260724-ntf-yaml-support/reviews/page-about_index.md` | M | 可（`#24` 節のみ） | 対象 |
| 6 | `ja/development_tools/testing_framework/about/index.rst` | M | 可 | 対象 |

明示的にパスを列挙してステージした（`git add -A` / `git add .` は使用していない）。

```
$ git add ja/development_tools/testing_framework/about/index.rst \
    .rn/20260724-ntf-yaml-support/design.md \
    .rn/20260724-ntf-yaml-support/mapping/style.md \
    .rn/20260724-ntf-yaml-support/mapping/glossary.md \
    .rn/20260724-ntf-yaml-support/reviews/page-about_index.md
$ git diff --cached --name-only
（上記5件のみ。`checks/task-24.md` は含まれない）
```

コミット `82dbe16`（`fix: 取引単体テストの実行方法を出典のある4処理方式の名指しに改める — #24`）。`origin ntf-yaml-support` へ push 済み（`5393971..82dbe16`。force-push はしていない）。push 後の `git status --porcelain` は ` M .rn/20260724-ntf-yaml-support/checks/task-24.md` の1件のみ（本ファイルは意図どおり未コミット）。

**判定: PASS**

## S-4: `:widths:` を決めた実測比の算出根拠

**何をどう測ったか。** 対比表（`about/index.rst:56-75`）の全16セル（ヘッダ1行＋データ3行 × 4列）の文字列を、`unicodedata.east_asian_width` が `W`/`F`/`A` を返す文字を2、それ以外を1として合計した**表示幅**で測った。列ごとの最大値を取り、4列の合計に対する百分率を求め、端数は小数部の大きい列から順に切り上げて合計100に揃えた。列の必要幅を決めるのはその列の最長セルであるため、合計や平均ではなく最大値を基準にした。

| 列 | 各セルの表示幅（ヘッダ, クラス単体, リクエスト単体, 取引単体） | 最大 | 比率 | 採用値 |
|---|---|---|---|---|
| テストの種類 | 12, 16, 20, 14 | 20 | 9.26% | **9** |
| 実行方法 | 8, 15, 15, 55 | 55 | 25.46% | **26** |
| テスト範囲 | 10, 10, 35, 34 | 35 | 16.20% | **16** |
| 備考 | 4, 28, 28, 106 | 106 | 49.07% | **49** |
| 合計 | — | 216 | 100% | **9,26,16,49** |

変更前の `20,20,30,30` は、備考列（最大106）と実行方法列（最大55）を同じ30・20に割り当てており、実測と乖離していた（S-4 の指摘）。生成HTMLの `<colgroup>` が `9% / 26% / 16% / 49%` になっていることをゲートHで確認済み。

## S-5 後半（前方参照）を対応不要とした理由

S-5 の後半は「`処理方式` の初出が `:73` で、6分類の定義は `:83-94` にあり前方参照になっている」という指摘である。**対応不要とした。** 解消するには取引単体テスト側にも処理方式の分類を示す必要があるが、`design.md:90`（実測: `**内訳の表は、リクエスト単体テストの6処理方式のみを載せる。クラス単体テスト・取引単体テストの行は載せない。**` で始まる段落）が、内訳表にリクエスト単体テスト以外の行を載せないことを `#8` のユーザーフィードバックを受けて確定している。加えて本タスクの作業指示は「取引単体テストの処理方式ごとの一覧表を新設しない」を守るべき条件に挙げている。したがって前方参照は、確定済みのページ構成を開け直さない限り解消できない。

なお S-5 の前半（`:98` の「Jakarta Batchに準拠したバッチアプリケーションを対象としていない」との衝突）は、「それ以外の処理方式」を廃止して4処理方式の名指しに改めたことで解消した（ゲートA）。

## S-7〜S-10 の突合（`style.md` の是正。ラウンド1で `reviews/` に書いていた監査結果はここへ移した）

`style.md` の `design.md` 行番号参照10件（`:63`・`:64`・`:65`・`:67`・`:70`・`:77`・`:78`・`:79`・`:80`・`:81`。ラウンド1着手時点の `grep -n 'design\.md:[0-9]'` で実測）を、実物と突き合わせた結果は次のとおり。

| 旧 `style.md` の記述 | `design.md` の実物（実測） | 是正 |
|---|---|---|
| `design.md:48-52` 「モジュール一覧の集約」節 | `:48-52` は `### 「全体像」と「特徴」を1つの節に統合し…`（`:43`）の本文。`grep -n 'モジュール一覧の集約' design.md` は**0件**で、そのような節は存在しない | 節見出し「モジュール一覧は第1部に置かない。…」（`:118`）で指す形に置き換え（S-7） |
| `design.md:34` 第1部「稼動環境」に「モジュール一覧（依存関係）」を記載 | `:34` は第1部アウトライン表の別の行。「稼動環境」の行は `:37` であり、その内容は「対応するJUnitバージョン…の事実のみ。依存関係・使い分けの詳細は第2部『JUnit 5用拡張機能』に譲る」で、モジュール一覧を記載しない | 削除し、`:118` 節の内容（第1部には集約しない）に置き換え（S-9） |
| `design.md:50` の引用「依存関係（…）は本ページの『稼動環境』に集約する。処理方式ごとのページには置かない。」 | 当該文字列は `design.md` に存在しない。実物は `:135-139` の「本ページの『稼動環境』は…1文のみとし、選択基準の説明・依存関係のモジュール一覧は一切書かない。…処理方式固有の依存…についても、同じ理由で当該ページ（第2部・第3部）にのみ記載し、本ページには集約しない（`#6`の「処理方式ごとのページには置かない」という集約方針を撤回）」 | 引用をやめ、`:118` 節の現在の決定に合わせて書き直した（S-9） |
| `design.md:143` 「拡張例は第3部に置かない。」 | `:143` は `check_unused_vocabulary` に関する記述。当該文は `:260` にあり、`## 4. 第3部 テストの実装方法` ＞ `### ページのアウトライン`（`:242-268`）の内側 | 「同節」として節見出しで指す形に置き換え（S-7） |
| `design.md:76-88` 第2部ページのアウトライン。機能概要→使用方法→拡張例の3セクション | `:76-88` は第1部の `### 「テストの種類」に置く対比` 節。第2部のアウトラインは `:173-190` にあり、コードブロックは `機能概要（任意）`（`:180`）・`使用方法（必須）`（`:184`）・`拡張例（任意）`（`:188`） | 節見出し参照に置き換え、必須・任意の区別を明記して `style.md:45-46` と整合させた（S-7・S-8） |
| `design.md:132-141` 第3部ページのアウトライン | `:132-141` は `### モジュール一覧は第1部に置かない…` 節の本文。第3部のアウトラインは `:242-256`（`機能概要` ＋ `使用方法` の2セクション） | 節見出し参照に置き換え（S-7） |

S-9 の是正で、`style.md:53-54`（第2部・第3部に「モジュール一覧」の見出しを置かない）は**規約自体を維持**し、その理由づけだけを「第1部に集約するから」→「第1部にも集約しない。処理方式固有の依存は当該ページで個別に触れる」に改めた。`design.md:118` の節題が「モジュール一覧は第1部に置かない」であり、見出しを置かない規約はどのページについても生きているためである。

S-10 の是正で、`style.md:69-73`（旧）の2択のうち「見出しは置き、本文に『なし。』とだけ書く」を削り、「見出し自体を置かない」の一択にした。`:45-46` の規約（出典が無い場合は見出し自体を置かない）と一致する。

**範囲外として手を付けなかった点（申し送り）**: `style.md` の「**根拠**（拡張例の省略）」ブロック（是正後の `:96-102`）は、FW解説書で「拡張例」の直後に「なし。」と書かれている実例2件（`exclusive_control.rst:403-405`・`service_availability.rst:112-114`）と、見出し自体が無い5ファイルの実例を並べている。S-10 で「なし。」の選択肢を削ったため、前半2件は現在どの規約も支えていない。この2行は作業指示が許した行範囲（`:45-46`・`:53-54`・`:62-67`・`:69-73`・`:77`〜`:81`）の外にあるため変更していない。

## 全主張の一次情報突合（文章のタスクのため全件を記録する）

| # | 書いた主張 | 突き合わせた一次情報 | 結果 |
|---|---|---|---|
| 1 | ウェブアプリケーションの取引単体テストは手動（`about:79`・`design:86`） | `git show 2e501ad:…/03_DealUnitTest/index.rst` の `:7-8` | 一致 |
| 2 | ウェブアプリケーションでは「JUnitでの自動実行はできず」（`about:79`） | 同 `index.rst` 全体に自動実行の記述が無いこと（`grep` で `自動` 0件）と `:7-8` の手動操作の記述 | 一致 |
| 3 | アプリケーションサーバにデプロイして手動で操作する（`about:79`・`about:75`） | `index.rst:7-8`、テスト準備 `:19-21`（アプリケーションのデプロイ・アプリケーションサーバ起動） | 一致 |
| 4 | エビデンスは画面ハードコピー・DBダンプ（`about:75`） | `index.rst:39-40` 「* 画面ハードコピー」「* DBダンプ(テスト実行前および実行後)」 | 一致 |
| 5 | RESTfulウェブサービスは自動（`about:79`・`design:86`） | `rest.rst:7` | 一致 |
| 6 | Nablarchバッチアプリケーションは自動（同上） | `batch.rst:5-6` | 一致 |
| 7 | MOMによるメッセージングは自動（同上） | `real.rst:8-10`、`delayed_receive.rst:5-6` | 一致 |
| 8 | 「リクエスト単体テストを連続実行することにより」（`about:79`） | `batch.rst:6`・`rest.rst:7`・`real.rst:10` が使う語。`grep -rn '連続実行' ja/` でも現行解説書の語であることを確認 | 一致 |
| 9 | `HTTPメッセージング` は出典に実行方法の記述が0件（`design:86`） | `http_send_sync.rst` を `手動\|自動\|連続実行` で走査して0件。冒頭20行も目視 | 一致 |
| 10 | `テーブルをキューとして使ったメッセージング` は取引単体テストの出典が0件（`design:86`） | `03_DealUnitTest/` の `.rst` 8件が全件であること（`git ls-tree`）と、8件のいずれもこの処理方式を扱っていないこと | 一致 |
| 11 | `send_sync.rst:7`・`http_send_sync.rst:7` はテスト対象アプリケーションの種類の記述（`design:86`・`reviews`） | 両ファイルの `:7` 全文 | 一致 |
| 12 | `delayed_send.rst` は本文とリンク先が食い違う（`design:86`・`reviews`） | `delayed_send.rst:5-6`（本文＝同期応答メッセージ送信処理、リンク＝`./real`）と `real.rst:2`（ページ題＝同期応答メッセージ受信処理） | 一致 |
| 13 | 4処理方式の名称が正表記（`about:79`・`design:86`） | `mapping/glossary.md` §5.2 `:131`・`:132`・`:134`・`:135` | 一致 |
| 14 | 内訳表は6処理方式のみという確定事項と両立（`reviews`） | `design.md:90` の段落 | 一致 |
| 15 | 取引単体テストは第2部3ページ・第3部6ページ（`reviews`・`design:86`） | `design.md`「12. 未確定事項の確定」表、および `style.md` のラベル一覧（第2部 `deal_unit_test_setting_*` 3件・第3部 `deal_unit_test_*` 6件） | 一致 |
| 16 | `input-0028` に実行方法列・備考列が無い（`reviews`） | `mapping.csv:198`、`input/ntf-doc-terms.md:415-426`（2列表） | 一致（ラウンド1で実測。今回再確認） |
| 17 | `important` が S-06（必ず守るべき注意事項）に合致（`reviews` の判断） | `style.md` S-06 の規約本文（是正後の `:230-231`） | 一致 |
| 18 | `実行方法` に統一する根拠（`reviews`） | `about/index.rst:61`（列見出し `実行方法`）・`:54`（リード文「それぞれ実行方法とテスト範囲が異なる」） | 一致 |
| 19 | `style.md` の `design.md` 参照6種のずれ（本ファイル S-7〜S-10 の表） | `design.md` の該当行を全件 `awk`/`grep` で開いて確認 | 一致 |
| 20 | `:widths:` の実測比 | `about/index.rst:60-75` の16セルの文字列を `unicodedata.east_asian_width` で計測 | 上表のとおり |

## ラウンド2 Completion Criteria

| # | 項目 | Self-check | Evidence | QA |
|---|---|---|---|---|
| 1 | `about/index.rst:73`・`:75`・`:79` を §2-2 の確定文言に差し替えた | OK | ゲート3 #2〜#4 | |
| 2 | `:58` の `:widths:` を新しいセル文言の実測比で決め直した | OK | S-4 の算出根拠の表。生成HTMLの `<colgroup>` が `9/26/16/49`（ゲートH） | |
| 3 | `design.md:84` を `about/index.rst:73`・`:75` と逐語一致させ、`APサーバ` を使っていない | OK | ゲートC | |
| 4 | `design.md:86` を §2-1 の実測に差し替え、§2-3 の4点と §3-2 の申し送り1文を含めた | OK | ゲート4。4点＝(1) 4処理方式と `file:line`、(2) 2処理方式について述べない決定と理由、(3) `send_sync.rst:7`・`http_send_sync.rst:7` の位置づけ、(4) `delayed_send.rst` を根拠に使っていないこと。末尾に申し送り1文 | |
| 5 | `style.md` の `design.md:NN` 参照10件を節見出し参照に置き換えた（S-7） | OK | ゲートE（`grep -c` = 0、置き換え先の一意性） | |
| 6 | `style.md:77` を `:45-46` に合わせた（S-8） | OK | ゲート5・S-7〜S-10 の表。新 `:76-77` は「機能概要（任意）→ 使用方法（必須）→ 拡張例（任意）」 | |
| 7 | `style.md:53-54`・`:62-67`・`:80-81` を「モジュール一覧は第1部に置かない」に合わせた（S-9） | OK | ゲート5・S-7〜S-10 の表。見出しを置かない規約自体は維持 | |
| 8 | `style.md:69-73` の「本文に『なし。』とだけ書く」を削った（S-10） | OK | ゲート5の差分 | |
| 9 | `glossary.md:168` の意味欄のみを、実施方法を含まない定義に改めた（S-6） | OK | ゲートF | |
| 10 | `reviews/page-about_index.md` の `## #24` 節を整理した（S-11） | OK | ゲートG。`style.md` の監査結果は本ファイルへ移した | |
| 11 | 「それ以外」「すべての処理方式」を使っていない | OK | ゲートA | |
| 12 | 出典のある4処理方式だけを名指しし、残り2処理方式に触れていない | OK | ゲートB | |
| 13 | 処理方式の名称は `glossary.md` §5.2 の正表記 | OK | ゲート7 | |
| 14 | `about/index.rst:83-94` の内訳表を変更していない | OK | ゲート6（diff 0件） | |
| 15 | 取引単体テストの処理方式ごとの一覧表を新設していない | OK | ゲート3（追加した行0行。表の新設なし） | |
| 16 | 日本語の地の文は1段落1行 | OK | `about/index.rst:79` は1行。生成HTMLで1段落として出力（ゲートH） | |
| 17 | `design.md` の他の確定事項（`:88`・`:90`・`:92`・`:94`）と両立する | OK | 下表 | |
| 18 | `mapping.csv` を変更していない（`#25` を起こしていない） | OK | ゲート10 | |
| 19 | ゲート1〜12・A〜I が全件 PASS | OK | 上記各節 | |

### `design.md` の確定事項との両立確認（`:88`・`:90`・`:92`・`:94` を開いて確認）

| 行 | 確定事項（要旨） | 両立するか |
|---|---|---|
| `:88` | リクエスト単体テストの内訳は対比表の直後に地の文で続ける。独立した「正式名称」見出しは置かない | 両立。見出しは増やしていない。`important` の位置も変えていない |
| `:90` | 内訳の表はリクエスト単体テストの6処理方式のみ。クラス単体テスト・取引単体テストの行は載せない | 両立。内訳表は無変更（ゲート6）。取引単体テストの一覧表は新設していない。S-5 後半を対応不要とした理由でもある |
| `:92` | 内訳表の列見出しは「処理方式」 | 両立。内訳表は無変更 |
| `:94` | 「対象範囲」は独立セクションとせず「テストの種類」の末尾に統合 | 両立。`:96-102` の `important` 2件は無変更 |

## Overall Verdict（ラウンド2）

- Self-check: OK（実装担当記入）

## 4観点レビュー ラウンド2（コーディネータ記入）

4観点をそれぞれ独立のサブエージェントで実施（QA / 設計 / クラフト / 検証）。指示書 `ntf-doc-24-round2.md` と本ファイルは渡していない。

| 観点 | 判定 | 挙げた `must` |
|---|---|---|
| QA | FAIL | 2件（出典なき否定断定／MOM の外延矛盾） |
| 設計 | FAIL | 3件（MOM の過度一般化／走査記録が再現しない／出典なき否定断定） |
| クラフト | FAIL | 4件（出典なき否定断定／目的語脱落／可能表現の断定化／走査記録の内部矛盾） |
| 検証 | FAIL | 3件（出典なき否定断定／`http_send_sync.rst` の0件主張が不成立／走査記録が再現しない） |

### 重複除去後の `must`（コーディネータが一次情報で全件再確認した）

| # | 内容 | 挙げた観点 | コーディネータの実測 | triage |
|---|---|---|---|---|
| R2-M1 | `about/index.rst:79`「ウェブアプリケーションでは、JUnitでの自動実行はできず」に出典がない | 4観点すべて | `git show 2e501ad:.../03_DealUnitTest/*.rst` 8件に不可能性の記述0件。`index.rst:7-8` は実際に行う方法を述べるだけ | **ユーザー判断へ上げる**（指示書 §2-2 が逐語で指定した文言のため） |
| R2-M2 | `:79`「MOMによるメッセージングでは…JUnitで自動実行する」が MOM の内側で過度一般化 | 設計・QA（クラフト・検証は `should`） | `mapping.csv` を `csv.DictReader` で集計 → `send_sync.rst`（手動・モックアップ前提）が `取引単体テスト（MOMによるメッセージング）` に4行、`取引単体テストの設定（MOMによるメッセージング）` に1行。同ページ `about/index.rst:92` は `MOMによるメッセージング` を「MOMによる要求電文の受信、または同期応答メッセージ送信」と定義しており、`:79` と `:92` が同一ページ内で食い違う | **ユーザー判断へ上げる**（同上） |
| R2-M3 | `:79` が出典の可能表現「実施可能である」を「自動実行する」と断定に強め、条件節「複数のリクエストにより取引が成立する場合は」を落としている。第3文は目的語「取引単体テスト」が脱落し係り先が曖昧 | クラフト（`must`）・QA（`should`） | `rest.rst:5-7`・`real.rst:5-10` は「1リクエスト＝1取引である場合は、取引単体テストを実施する必要はない」「ただし、複数の…場合は…実施可能である」。無条件に書けるのは `batch.rst:5-6` のみ | **ユーザー判断へ上げる**（同上） |
| R2-M4 | `design.md:86`・`reviews/page-about_index.md` の走査記録が再現しない。「8ファイルを `grep -n "手動\|自動\|連続実行"` に掛けた全件」としながら、同 grep で0ヒットの `delayed_receive.rst:5-6` をヒット行として載せ、同じく0ヒットの `delayed_send.rst` は「該当0件」としている | クラフト・設計・検証 | `git show 2e501ad:.../delayed_receive.rst \| grep -n "手動\|自動\|連続実行"` → exit 1（0件）。`delayed_receive.rst:5-6` は `:doc:./real` の追跡で得た事実であり、走査のヒットではない | **Valid → 是正する**（範囲内） |
| R2-M5 | 「`http_send_sync.rst` に実行方法の記述が0件」という否定的主張が不成立 | 検証 | `git show 2e501ad:.../http_send_sync.rst \| grep -n "実施方法"` → `:4`（ページ題）・`:9`「取引単体テスト実施方法は、`:ref:`dealUnitTest_send_sync`\ を参照すること。」・`:17`。走査語を `手動\|自動\|連続実行` に限ったための0件であって、実施方法に触れていないわけではない | **Valid → 是正する**（範囲内）。あわせて指示書 §2-1 の「実施方法をひとことも書いていない」との食い違いをユーザーへ報告する |

### `should`（コーディネータの triage）

| # | 内容 | triage |
|---|---|---|
| R2-S1 | `design.md:86` の `index.rst:7-8` 引用が原文の文頭「取引単体テストでは、」を省略記号なしで落としている | Valid → 是正する |
| R2-S2 | `design.md:86` が1段落1,696字。走査手順・判定・除外理由・経緯・申し送りが同居し、`reviews` の `## #24` 節と20-gramの28%が逐語重複。`design.md`＝決定、`reviews`＝根拠と実測、という分担が崩れている | Valid → 是正する |
| R2-S3 | 走査母集団が `03_DealUnitTest/` 限定で、`02_RequestUnitTest/double_transmission.rst:28-39`（「取引単体テストでは、クライアントサイドにてテストを実施する」「打鍵にてテスト対象リクエストのボタンを選択する」）を落としている。結論（ウェブ＝手動）は変わらないが補強出典である | Valid → 是正する（母集団がディレクトリ限定である旨を明示） |
| R2-S4 | 対比表セル `:73` と `important` 第1文 `:79` が実質同文で、6行以内に2度読ませる | ユーザー判断へ（`:73`・`:79` とも指示書 §2-2 の逐語指定） |
| R2-S5 | `style.md:96-102`「根拠（拡張例の省略）」の前半2件（FW解説書で「なし。」と書かれている実例）が、S-10 の是正後はどの規約も支えていない | ユーザー判断へ（指示書 §5-1 の許可行範囲外） |
| R2-S6 | `style.md:189` の S-04 表が L2 の用途を「機能概要/モジュール一覧/使用方法/拡張例の4大セクション」としており、`:45-46`・`:53-54` と食い違う（変更前から存在。今回の是正で顕在化） | ユーザー判断へ（許可行範囲外） |
| R2-S7 | `glossary.md:168` が兄弟項目（`クラス単体テスト`・`リクエスト単体テスト`）と非対称になった | **Invalid** — 指示書 §4 S-6 が「非対称は許容する（取引単体テストだけが処理方式によって実施方法が変わるため）」と明示的に裁定済み |
| R2-S8 | `git status --porcelain` に `checks/task-24.md` が残っている／`3c7d6ac..82dbe16` に `steering.md` の差分がある | **Invalid** — `checks/task-24.md` は rn の Check file format 上コミットしない運用であり指示書 §5-1 の許可対象。`steering.md` の差分はコーディネータの `/rn:up` コミット `5393971` によるもので、実装成果物コミット `82dbe16` には含まれない（`git show --stat 82dbe16` は許可5ファイルちょうど） |
| R2-S9 | `locales/ja/LC_MESSAGES/sphinx.mo` が作業ツリーに再生成されていた | 事実。ただし `82dbe16` には含まれず、混入元はレビュー観点のサブエージェントが本ツリーに対して実行した Docker フルビルド。コーディネータが `git checkout --` で復元済み |
| R2-S10 | `reviews/page-about_index.md:305-307` の想定警告の記述が陳腐化（実測の唯一の警告は `db_double_submit.rst:108`） | 記録のみ（`## #24` 節より前のため変更禁止） |

### 実測で OK と確認できた項目（4観点の一致）

- ゲート2 の出典8件の突合、ゲート3〜10、ゲートA〜G は4観点とも OK
- `:widths: 9,26,16,49` が表示幅の実測比（`unicodedata.east_asian_width` で `20/55/35/106` → `9.3/25.5/16.2/49.1`）と一致することを、4観点のうち3観点とコーディネータが独立に再計算して確認
- Docker フルビルド `-a` は `build succeeded, 1 warning.`（`db_double_submit.rst:108` の既知1件のみ、新規0件）。QA・検証の2観点が独立に再実行して一致
- `verify_mapping.py` exit 0 / 595行 / 12,986 / 11,983。検証観点は `csv.DictReader` で独立に595件を数え直して一致

---

# ラウンド3（指示書 `ntf-doc-24.md`。判断待ち5件の回答を反映）

指示書はラウンド2 の版を書き換えて一本化された（旧 `ntf-doc-24-round2.md` を `ntf-doc-24.md` に改名）。ラウンド2 で上げた判断待ち5件の回答は次のとおりで、うち4件はレビュー役が CC の指摘を認めたものである。

| # | 判断待ち（ラウンド2） | 回答 | ラウンド3 での反映 |
|---|---|---|---|
| R2-M1 | 「JUnitでの自動実行はできず」に出典がない | 削る。指摘は正しい | 公開本文から削除。走査2 で不可能性の記述0件を再実測 |
| — | `important` の扱い | 地の文に降ろす（ラウンド1 の `S-3` 起案が正しかった） | `.. important::` を外し字下げ0の地の文にした |
| R2-M2 | MOM の名指しが過度一般化 | MOM を名指しから外す | 名指しを3処理方式に絞った |
| R2-M3 | 「実施可能である」を断定に強めている | 「できる」に戻し目的語も補う | 「取引単体テストをJUnitで自動実行できる」 |
| R2-M4 相当（判断待ち4） | 指示書 §2-1 の「実施方法をひとことも書いていない」が不正確 | CC の指摘が正しい。レビュー役の誤り | 走査記録を「grep のヒット」と「リンクをたどって得た事実」に分けた |
| R2-S5・S6（判断待ち5） | `style.md` の範囲外2件 | 2件とも `#24` に含める | `style.md` の「根拠（拡張例の省略）」と S-04 表 L2 行を是正 |

## 公開本文の最終形（`about/index.rst`）

対比表の直後、`.. _testing_framework_about-test_type_names:` の前に、字下げ0・1段落1行の地の文を置いた。

> 取引単体テストの実行方法は、対象とする処理方式によって異なる。ウェブアプリケーションでは、テスト対象のアプリケーションをアプリケーションサーバにデプロイし、手動で操作してテストを行う。RESTfulウェブサービスとNablarchバッチアプリケーションでは、リクエスト単体テストを連続実行することにより、取引単体テストをJUnitで自動実行できる。

`:58`（`:widths:`）・`:73`・`:75` はラウンド2 の形のまま変更していない（指示書 §2-2）。

## ゲート1〜12 の再実行（ラウンド3）

| # | ゲート | 結果 |
|---|---|---|
| 1 | `git status --porcelain` の全件が許可ファイルのみ | **PASS**。4件（`design.md`／`mapping/style.md`／`reviews/page-about_index.md`／`about/index.rst`）のみ。`checks/task-24.md` はコミット対象外 |
| 2 | 出典8件を `git show 2e501ad:<path>` で突合 | **PASS**。§2-1 の表と全件一致（走査結果はゲートL に掲載） |
| 3〜8 | 用語・段落内改行・表記の各ゲート | **PASS**（`実施方法` 0件・段落内改行0・処理方式名は `glossary.md` §5.2 の正表記） |
| 9 | `verify_mapping.py` | **PASS**。`OK: no errors` / exit 0。`csv.DictReader` で 595行 / 12,986 / 11,983（不変） |
| 10 | 変更してはならないファイルの差分 | **PASS**。`mapping.csv`・`_batch/`・`volume.md`・`vocabulary.md`・`glossary.md`・`ja/conf.py`・`about/index.rst` 以外の `ja/` 配下はいずれも差分0 |
| 11 | Docker フルビルド（`-a`） | **PASS**。ゲートH に詳細 |
| 12 | `commit & push` 直前のゲート1再実行 | **PASS**（ゲートI と同一の実行） |

## 指示書 §5-3 ゲートA〜N（ラウンド3）

| # | ゲート | 結果 |
|---|---|---|
| A | 閉じた表現が0件 | **PASS**。`grep -n "それ以外\|すべての処理方式" about/index.rst` = 0件 |
| B | 名指しが正表記と逐語一致し3処理方式だけ | **PASS**。段落に現れるのは `ウェブアプリケーション`・`RESTfulウェブサービス`・`Nablarchバッチアプリケーション` の3つ（`glossary.md` §5.2 と逐語一致）。`MOMによるメッセージング`・`HTTPメッセージング`・`テーブルをキューとして使ったメッセージング` は段落に0件 |
| C | `design.md` の対比表行と `about/index.rst:73`・`:75` の逐語一致 | **PASS**。Python で文字列比較し実行方法セル・備考セルとも `True`。`APサーバ` は両ファイルとも0件 |
| D | `実施方法` 0件・`実行方法` に統一 | **PASS**。`about/index.rst` は0件。`design.md` の該当は出典の逐語引用（`send_sync.rst:4` のページ題、`delayed_receive.rst:5-6`・`delayed_send.rst:5-6` の本文、`mapping.csv` の `heading_path`）のみで、地の文はすべて `実行方法` |
| E | `style.md` に `design.md:` 行番号参照が0件 | **PASS**。`grep -c 'design\.md:[0-9]' style.md` = 0（ラウンド2 で是正済み、ラウンド3 で再確認） |
| F | `glossary.md` の差分が `:168` の1行のみ | **PASS**。`git diff 5e87f6e..HEAD -- glossary.md` は `1 file changed, 1 insertion(+), 1 deletion(-)`。ラウンド3 の作業ツリー差分は0件。§5.15 の差分0件 |
| G | `reviews/page-about_index.md` の変更行が `## #24` 節の内側だけ | **PASS**。`git diff -U0` の13ハンクすべてが `## #24` 見出し（旧 `:322` / 新 `:322`）より後 |
| H | Docker フルビルド（`-a`） | **PASS**。`build succeeded, 1 warning.`。警告全件は `db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test` の1件のみで既知（新規0件）。実行直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行し、`git status --porcelain` に現れないことを確認 |
| I | `commit & push` 直前のゲート1再実行 | **PASS**。許可4ファイルのみ |
| J | 段落が地の文であること | **PASS**。直前は対比表の最終セル行と空行で `.. important::` は無く、字下げ0。`about/index.rst` の `.. important::` は2件（Jakarta Batch・マルチスレッド）だけ |
| K | 段落に `できず`・`できない`・`不可` が0件 | **PASS** |
| L | `design.md` の走査コマンドの再現 | **PASS**。下記のとおり記載と一致 |
| M | `style.md` の2件 | **PASS**。S-04 表 L2 行は「ページの大セクション。構成は `S-02` による」で `モジュール一覧` は現れない。「根拠（拡張例の省略）」の箇条書きは見出し自体が無い5ファイルのみで、「なし。」の2実例は根拠から外し「本解説書では採らない」旨の1文として残した |
| N | `design.md` と `reviews/` の逐語重複 | **PASS**。25文字以上の文で突合し重複0件（初回は出典引用1文が重複したため、`design.md` 側を参照に置き換えた） |

### ゲートL の再現結果

`git ls-tree -r --name-only 2e501ad -- <03_DealUnitTest>` の出力は22件、うち `.rst` は8件（残り14件は `_images/`）。

走査1 `grep -n "手動\|自動\|連続実行"` のヒット全件: `index.rst:8`／`batch.rst:5`・`:6`／`rest.rst:7`／`real.rst:10`／`send_sync.rst:151`・`:176`・`:207`。`delayed_send.rst`・`delayed_receive.rst`・`http_send_sync.rst` は0件。

走査2 `grep -n "できな\|できず\|不可\|行えな\|対応していな\|サポートしていな"` のヒット全件: `send_sync.rst:163` の1件のみ。

**`design.md` の記載と一致する。** ラウンド2 の記録が grep のヒットとして挙げていた `delayed_receive.rst:5-6` は走査1 で0件であり、リンク（`:doc:`./real``）をたどって得た事実である。ラウンド3 では「grep で得た事実」と「ファイルを開くかリンクをたどって得た事実」を節を分けて記録した。

## `MOMによるメッセージング` を名指ししない根拠（`mapping.csv` の独立実測）

`csv.DictReader` で集計した結果、`03_DealUnitTest/send_sync.rst` を出典とする行の割当先は次のとおりで、指示書 §2-2 の記述と一致する。

| mapping_id | dest_page | dest_section | lines |
|---|---|---|---|
| `current-0154` | 取引単体テスト（MOMによるメッセージング） | 機能概要 | 41 |
| `current-0155` | 取引単体テスト（MOMによるメッセージング） | 使用方法 | 14 |
| `current-0156-b` | 取引単体テスト（MOMによるメッセージング） | 使用方法 | 26 |
| `current-0157` | 取引単体テスト（MOMによるメッセージング） | 使用方法 | 53 |
| `current-0158` | 取引単体テストの設定（MOMによるメッセージング） | 使用方法 | 104 |

`http_send_sync.rst` の割当は `current-0138`（10行）・`current-0139`（23行）で第3部、`current-0140`（20行）で第2部。`design.md` が `#6` 確定として挙げる「HTTPメッセージング33行」は 10+23 に一致し、帰属を動かす理由が無いことを確認した（`mapping.csv` は変更していない）。

## `style.md` の是正2件（§4-2）の一次情報突合

| 対象 | 実測 | 是正 |
|---|---|---|
| `FW:libraries/exclusive_control.rst:403-405` | 「拡張例」＋下線＋「なし。」の3行。**見出しを置く書き方の実例** | 根拠の箇条書きから外し、採らない旨の1文に移した |
| `FW:libraries/service_availability.rst:112-114` | 同上 | 同上 |
| `code.rst`・`format.rst`・`static_data_cache.rst`・`db_double_submit.rst`・`file_path_management.rst` | `grep -c '^拡張例$'` がいずれも **0**。見出し自体が無い | 根拠として残した（規約と向きが一致する） |
| S-04 表 L2 行 | 用途欄が「機能概要/モジュール一覧/使用方法/拡張例」「4つの大セクション」 | 「ページの大セクション。構成は `S-02` による」に改めた。`-` の記号対応と根拠欄は変更していない。`S-02` は `### S-02 ページのセクション構成`（実在・一意） |

## 4観点レビュー ラウンド3（コーディネータ記入）

4観点をそれぞれ別のサブエージェントで実施した（指示書はサブエージェントに渡していない）。判定は QA=FAIL・設計=FAIL・クラフト=PASS・検証=FAIL。**重複除去後の `must` は2件**で、いずれもコーディネータが一次情報で再確認したうえで是正した。

### `must` 2件（是正済み）

| # | 指摘（検出した観点） | コーディネータの再確認 | 是正 |
|---|---|---|---|
| R3-M1 | `design.md` の申し送りが「MOM・HTTPメッセージングの2ページとも自動実行の説明とモックアップ説明の両方を抱える」としているが、`取引単体テスト（HTTPメッセージング）` に自動実行の出典は無い（検証・設計） | **正しい。** `csv.DictReader` で確認: 同ページの割当は `current-0138`・`current-0139` の2行のみで、いずれも `http_send_sync.rst`。同ファイルに `JUnit`・`自動`・`連続実行` は0件。MOM 側は `real.rst` の `current-0147`（自動）と `send_sync.rst` の4行（モックアップ）を両方持つ | 申し送りを2ページ一括で書くのをやめ、MOM のみが両方を抱えること・HTTPメッセージングには自動実行の説明が無いことを書き分けた。**指示書 §3-2 の前提に事実誤りがあったため、ユーザーに報告する** |
| R3-M2 | ゲートNの自己申告「重複0件」が再現しない。`design.md` と `reviews` の `#24` 節に逐語重複が残る（QA・設計） | **正しい。** ラウンド3 初稿の測定は文の分割方法が甘く、`- \`delayed_receive.rst:5-6\` は「…」` を含む98〜107字の連続一致を検出できていなかった。20-gram 一致率で測り直すと16.5%だった | `design.md` の「走査した事実」から逐語引用と全件表を落とし、`file:line` と結論だけにした（逐語と全件表は `reviews/` に一本化）。`reviews/` 側は理由づけを落として `design.md` への参照にした。**20-gram 一致率 16.5% → 7.8%**（ラウンド2 は28%）。残る25字以上の共通部分11件はすべて公開本文の逐語・走査コマンド・`mapping_id`／ページ名の識別子で、説明文の重複は0件 |

### 是正に取り込んだ `should`／`note`（コーディネータが一次情報で確認したもの）

| 指摘 | 是正 |
|---|---|
| `style.md` の追記でインラインコードスパンが行またぎになり、パスが `FW:libraries/ exclusive_control.rst` と描画される（クラフト） | 折り返し位置を移し、コードスパンを1行に収めた |
| `reviews` の「現 L83-94」が陳腐化。表本体は L83-92 で、しかも「対比表の直後」ではない（クラフト・検証・設計） | 導入文 L81／表本体 L83-92 と書き分け、間に段落とラベルが入る旨を明記した |
| `reviews` の走査コマンドに `-- <パス>` の制限が落ちており、そのまま実行すると1825件になる（検証） | パス制限を明記した |
| 「実行方法を述べていない」という絶対的否定が強すぎる。`send_sync.rst:28`・`:179`・`:187` は手動側を示唆する（検証） | 「手動なのか自動なのかを明示した記述は無い」に緩め、示唆の存在と、それでも名指ししない理由を書き足した |
| 「`send_sync.rst` はページ全体が実行手順の説明」は `mapping.csv` の分割と合わない（検証） | 本体の範囲（`:47-48` 以下）を示し、テストデータ側の見出しを含むことを明記した |
| リンクをたどって得た事実の一覧に `index.rst:10`（同期応答メッセージ送信を総論ページの下位ケースとして取り込む文）が無い（QA・設計） | 追加した |
| `rest.rst:5` の条件（1リクエスト＝1取引なら取引単体テスト自体が不要）が記録されていない（設計） | 追加し、公開本文が条件を書いていない理由も添えた |
| 「`index.rst` はウェブアプリケーション前提」の根拠が推論どまり。直接の出典がある（QA・検証） | `05_UnitTestGuide/index.rst:16`・`:24-26` の `toctree` を `reviews` に追加した |
| ウェブアプリケーション＝手動の補強出典 `double_transmission.rst:28,33,37` が恒久記録に無い（QA） | `reviews` に逐語で追加した（母集団外のため走査1のヒットではない旨を明記） |
| 旧 `toctree` と `mapping.csv` の帰属の食い違いが恒久記録に無い（QA） | `reviews` に、`#6` 確定であり `#24` では `mapping.csv` を変更していない旨を記録した |
| 「対比表のセルとの重複にならない」の論証が備考セルを見ていない（設計・クラフト） | 備考セルとは事実が重なることを認めたうえで、両方を残す理由を書いた |
| `design.md` の「対比表の直後」が2つの段落に与えられ両立しない（設計） | 是正した段落の位置を「対比表と内訳の間」と書き分けた |
| MOM の処理方式名が受信・送信を覆うことの典拠に、リクエスト単体テストの内訳表だけを使っている（設計） | `glossary.md` §5.2 の意味欄を第一の典拠に加えた |

### 適用しなかった指摘（理由付き）

| 指摘 | 判定 |
|---|---|
| 公開本文の文言の改善案5件（クラフト。第2文からデプロイを削る／「テスト対象の」に縮める／「取引単体テストを行う」と明示／第2文も「行える」に揃える／名指ししない処理方式への誘導文を足す） | **適用しない。** いずれも指示書 §2-2 が逐語で指定した3文そのものへの変更である。合理性はあるので**ユーザーに報告する**（本文の変更は判断を仰いでから行う） |
| `about/index.rst:81` の「このうち」の先行詞が、`important` を外したことで直前段落を指すとも読める（クラフト・設計・QA） | **適用しない。** `:81` は指示書 §5-1 の許可行（`:58`・`:73`・`:75`・`:77-79`）の外である。**ユーザーに報告する** |
| `style.md:189` の用途欄は同語反復で情報量が落ちる／`S-02` は第1部の構成を定めていない（クラフト・設計） | **適用しない。** 用途欄の文言は指示書 §4-2 が逐語で指定した。第1部を `S-02` が覆っていないのは `#24` 以前からの状態で、許可範囲外 |
| `style.md:5` が `design.md`「7. トンマナ」を指すが、実際の節見出しは「8. トンマナ」（設計） | **適用しない。** `:5` は許可行の外で、`ddf8dc1`（`#24` より前）から存在する。**申し送りとして残す**。ゲートE は行番号参照だけを見ており、節見出し参照の実在確認をしていない |
| 段落内改行の禁止が `style.md` に規約として無い（クラフト） | **適用しない。** `#24` の範囲外。申し送りとして残す |
| `:widths:` の算出基準が `style.md` に無い（設計） | **適用しない。** `#24` の範囲外。申し送りとして残す |

### 是正ラウンド後のゲート再実行

ゲート1・A・D・E・J・K・M・N をすべて再実行し PASS。**是正ラウンドで `ja/` 配下は1文字も変更していない**（差分は `.rn/` 配下の3ファイルのみ）ため、ゲートH（Docker フルビルド）の結果は有効である。

### 4観点が独立に再現して一致した項目

- 走査1・走査2 のヒット全件、母集団22件／`.rst` 8件は4観点のうち3観点が独立に再実行して一致（ゲートL）
- ゲートA〜G・J・K・M は複数観点が再現して一致
- `:widths: 9,26,16,49` の表示幅比は2観点が独立に再計算して一致
- `mapping.csv` 595行と `send_sync.rst`・`http_send_sync.rst` の割当は2観点が `csv.DictReader` で独立に集計して一致
- **公開本文 `about/index.rst:77` の3文は、4観点とも「出典と突合でき、出典を超えた断定・過度一般化は無い」と判定**（QA の総括、検証の全件表、クラフトの用語・トンマナ確認）
- QA が母集団の妥当性を独立に検証: `git grep -c "取引単体" 2e501ad -- '*.rst'` は全11ファイルで、`03_DealUnitTest/` 8件以外は `double_transmission.rst`・`01_MasterDataSetupTool.rst`・`biz_samples/11/index.rst` のみ。**ホワイトリストで都合よく切り出した形跡は無い**
