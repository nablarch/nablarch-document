# `#pre-last` self-check — `verify_glossary.py` の不一致の一括是正と、横断の是正

対象タスク: `#pre-last`。ページを作らないタスク。成果物は `mapping/glossary.md`・`mapping/scan-terms.tsv`・`mapping/tools/`（3ファイル）と、横断の是正に由来する `ja/` 配下の4ファイル。

## 1. 着手時点の不一致

`#27` 完了時点（`7e19f68`）の `verify_glossary.py` は不一致25件だった。内訳は `[term]` 9件・`[ref]` 13件・`[count]` 2件・`[section]` 1件である。

## 2. 再発防止の判断 — 2つの選択肢は排他ではなく、両方を実施した

作業指示は「`design.md` を `scan` のコーパスから外す」か「`glossary.md` から `S:design.md:NN` の行番号指定を無くす」かの二者択一として提示していた。実測の結果、**両方が別々の検査を壊している**ことを確認したため、両方を実施した。

| 壊れる検査 | 原因 | 対処 |
|---|---|---|
| `refs`（13件） | `glossary.md` が `S:design.md:27`〜`:151` を行番号で指しており、`design.md` の改訂で行がずれた | 行番号を書かない `PREFIX:path` の形を認め、39箇所の `S:design.md:NN` を `S:design.md` に変えた |
| `counts`（再生成すると3件） | `scan` の `design` コーパスが `#10a`（`6ce81b5`）以降再生成されておらず、`glossary.md` の `designN件` の主張が実物とずれた（`セクション` 10→59、`稼動環境` 2→6、`使用方法` 4→22） | `SCAN_DEFAULT_CORPORA` から `design` を外し、`designN件` の主張5件を件数を使わない形に書き換えた |

行番号を書かない参照は「引用または表記がそのファイルのどこかに実在すること」を**生きた `design.md` に対して**検査し続けるので、行番号をピン留めするより強い。`verify_glossary.py` は `designN件` の形を見つけたら、数が合っていても不一致として落とす（`check_counts`）。ルールは `glossary.md` §1 に明文化した。

## 3. 実施した是正

| 分類 | 件数 | 実施内容 |
|---|---:|---|
| `[term]` | 9 | 未登録9表記を `mapping/tools/term_candidates.tsv` に登録した（`テストコード`/`テストソースコード`、`型名称`、`型記号`、`環境設定ファイル`/`propertiesファイル`/`プロパティファイル`、`デフォルト`/`既定`） |
| `[ref]` | 13 | 39箇所の行番号を撤廃した。あわせて内容が実際にずれていた3件を是正した（下表） |
| `[count]` | 2 | `scan-terms.tsv` を再生成した |
| `[section]` | 1 | `テストソースコード` → `テストコード` の行を §8 対応表に追加した |

### 行番号の撤廃では直らなかった3件（引用・参照の中身が誤っていた）

| 箇所 | 誤り | 一次情報での確認 |
|---|---|---|
| `glossary.md:119` | 引用「特化したテスト補助機能を提供すること」が `design.md` に存在しない | `git log --all -S` で `4e07294`（`#8` 2ラウンド目）に削除されたことを確認し、現行の「Nablarch特化APIを提供すること」（`design.md:54`）に差し替えた |
| `glossary.md:199` | 参照が、意図した後続の引用ではなく直前の引用（`glossary.md` 自身の §2 の文言）に係っていた | 語順を入れ替え、`#8` の確定文が参照の直前に来るようにした |
| `glossary.md:229` | `型記号` の登録により、参照が `型記号` に係って `input/ntf-testdata-doc.md:633`（`型名称` を含む行）と食い違った | 語順を入れ替え、`型名称` が参照の直前に来るようにした |

## 4. 横断の是正1 — 例示のコンポーネント名の衝突

**判断: 取引単体テスト側の例示名を `defaultRealTimeMessagingClient` に変えた。** リクエスト単体テスト側は出典どおり `defaultMessageSenderClient` のままとする。

根拠は実装である。コンポーネント名は環境設定ファイルの `messageSender.<リクエストID>.messageSenderClient` が指す任意の名前であり（`MessageSenderSettings` の `KEY_PREFIX`＝`messageSender`・`KEY_SEPARATOR`＝`.`・`KEY_DEFAULT_TARGET`＝`DEFAULT`。`nablarch-fw-messaging-6-NEXT-SNAPSHOT.jar` の `nablarch/fw/messaging/MessageSenderSettings.class` を `javap -p -c` で確認）、フレームワークが固定しているルックアップ名ではない。**NTF 自身のテストリソースは、この2クラスに別の名前を与えて同一ファイル内で共存させている。**

| 実装側の対応 | クラス | コンポーネント名 |
|---|---|---|
| `web-component-configuration.xml:31`、`messageSender.config:30` | `MockMessagingClient` | `defaultRealTimeMessagingClient` |
| `web-component-configuration-request-testing.xml:37`、`messageSender.config:121` | `RequestTestingMessagingClient` | `defaultMessageSenderClient` |

いずれも `nablarch-testing` の `src/test/resources/nablarch/test/core/messaging/web/` 配下。コミットは `fdf55d4b3149f0bd6181819b88c1008cfc4970cb`（2026-08-05）。

出典（`NTF:05_UnitTestGuide/03_DealUnitTest/http_send_sync.rst:62`）は取引単体テスト側にも `defaultMessageSenderClient` を使っており、逐語ではこれから離れる。離す理由は、両方のテストを行うプロジェクトが2ページを写経すると同名で異なるクラスを登録することになり、書かれたとおりでは動かないためである。散文で注意書きを足す案は `#25` で不採用となっている。名前を分ければ注意書きは不要になる。

## 5. 横断の是正2 — 語の統一3件

### (a) `メッセージの送信` → `電文の送信`

`glossary.md:275` が `電文` を「メッセージングで送受信するメッセージ」と定めており、送受信の対象を指す本文は `電文` を使う。実測（`guide/` を除く `.rst`）では名詞句が `電文の送信` 3件・`メッセージの送信` 2件で、外れ値は後者だった。2件を `電文の送信` に統一した（`setup/request_unit_test/http_messaging.rst:21`・`setup/deal_unit_test/http_messaging.rst:21`）。

処理方式名（`応答不要メッセージ送信` ほか §5.4）と、FW解説書の見出しに由来する動詞句「メッセージを送信する」は対象外とした。方式そのものの名前であり、`電文` に置き換えると出典の見出しと一致しなくなる。

### (b) `アプリケーション開発者` → `アプリケーションプログラマ`

**作業指示の申し送りとは逆の結論になった。** 申し送り（`#25`）は「`アプリケーション開発者` 3件に対し `アプリケーションプログラマ` は `setup/request_unit_test/web.rst:229` の1件のみで、外れ値は承認済みの `web.rst` 側」としていたが、`#27` で21ページが増えた後の実測は次のとおりで、前提が成り立たない。

| コーパス | `アプリケーションプログラマ` | `アプリケーション開発者` |
|---|---:|---:|
| FW解説書 | 4（`FW:libraries/tag.rst:566` ほか） | 1（`FW:nablarch/policy.rst:18`） |
| 現行解説書（基準コミット） | 13 | 0 |
| input資料 | 0 | 0 |
| 新解説書（`guide/` を除く `.rst`、是正前） | 4 | 5 |

`glossary.md` §2 の優先順位1（FW解説書に同じ概念の用語があればその表記を採用する）に従い、`アプリケーションプログラマ` を正表記とした。現行解説書13対0も同じ側を支持する。新ページ5件（`index.rst` 2件・`setup/deal_unit_test/mom.rst`・`setup/request_unit_test/http_messaging.rst`・`setup/deal_unit_test/http_messaging.rst`）を置き換え、§5.14 と §8 に登録した。

これに伴い `checks/task-26.md` の「語は `glossary.md` に従い『テストを実装するアプリケーション開発者』」という記述は現在の `glossary.md` と食い違う。同ファイルに追記で是正した。

### (c) `メッセージングログ` への `:ref:`

`setup/request_unit_test/http_messaging.rst:33` と `setup/deal_unit_test/http_messaging.rst:33` の `メッセージングログ` に `:ref:`メッセージングログ <messaging_log>`` を張った。参照先のラベルは `ja/application_framework/application_framework/libraries/log/messaging_log.rst:1` に実在する。

## 6. 範囲外だが直した1件 — `extract_terms.py` のテストが赤だった

`tools/test_extract_terms.py::TestRealFiles::test_extract_all_runs_against_the_real_session_files` が着手時点で失敗していた。原因は `extract_terms.py` が見出しを `## 5. 処理方式の名称` とハードコードしていたのに対し、`design.md` の章が1つ増えて `## 6. 処理方式の名称` になっていたこと。同じ抽出を行う `extract_vocabulary.py:161` は既に `6.` に追随していた。章番号に依存しない正規表現（`^##\s+[0-9]+\.\s*処理方式の名称\s*$`）に変えた。本タスクの変更に由来する失敗ではない。

## 7. 検証結果

| ゲート | コマンド | 結果 |
|---|---|---|
| 用語集 | `python3 mapping/tools/verify_glossary.py` | **RESULT: OK**（9検査すべて不一致0件。refs 283・counts 118・sections 86・terms 201・applies 96・population 331・design_sections 21・scheme_names 7・reasons 0） |
| マッピング | `python3 mapping/tools/verify_mapping.py` | `OK: no errors`（exit 0） |
| 単体テスト | `python3 -m pytest mapping/tools/ -q` | `183 passed, 96 subtests passed`（着手時は1 failed） |
| フルビルド | `docker run --rm -v "$PWD":/root/document nablarch-document-build-sandboxed /bin/bash -c "cd /root/document; sphinx-build -a -d _build/.doctrees/ja -b html ja _build/html"` | `build succeeded.`（WARNING・ERROR ともに0件） |
| `ja/` の差分 | `git diff --stat ja/` | 4ファイル・9行。すべて横断の是正1・2に由来する（`index.rst` 1行、`setup/deal_unit_test/mom.rst` 1行、`setup/deal_unit_test/http_messaging.rst` 4行、`setup/request_unit_test/http_messaging.rst` 3行） |

ビルド後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行済み。

## 8. 追加した検証ルール（`#pre-last` 確定）

- 参照は `PREFIX:path:line` を原則とするが、`S:design.md` は行番号を書かない。`verify_glossary.py` は行番号のない参照を「引用または表記がファイルのどこかに実在すること」で検査する。
- `design.md` は `scan` のコーパスに含めない。`designN件` と書くと `verify_glossary.py` が不一致として落とす。
- いずれも `glossary.md` §1 に明文化し、`test_verify_glossary.py` に4件のテストを追加した（行番号なし参照の解決・実在検査・不在検出・`design` 件数の拒否）。
