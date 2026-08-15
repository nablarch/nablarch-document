# #27 独立検証の結果

宛先: rn / CC

## 結論

**要是正 0 件。`#27` は承認可能。** 21ページすべてについて、構成・スタイル・ビルド・ラベル・出典の消化を検証し、修正を要する指摘は出なかった。

申し送りが2件ある（いずれも `guide/` 残骸の扱い。`#27` の是正ではなく `#pre-last` 以降の作業）。

## 検証環境

| 項目 | 値 |
| --- | --- |
| 検証対象 | `7e19f68`（`docs: エンティティ単体テストのページを作成する — #27-21`） |
| 検証方法 | CC のツリーから `git clone --no-hardlinks` した独立クローンで、すべてのコマンドを自分で実行 |
| `#27` の範囲 | `6fceb6f`〜`7e19f68` の22コミット |
| 削除前の現行解説書 | `2e501ad` |
| `nablarch-testing` | `e21bf67`（`main` の先端） |

`982a3ba`（`chore: rn:dn`）は `.rn/20260724-ntf-yaml-support/steering.md` の4行のみの変更で、`ja/` 配下に変更がないため、本検証の結論はそのまま有効。

## 検証した項目と結果

| 項目 | 結果 |
| --- | --- |
| ファイル構成 | `guide/` を除く `.rst` が38件。`design.md:830-890` のツリーと完全一致 |
| toctree 4ページ | `index.rst`・`setup/index.rst`・`implementation/index.rst`・`tools/index.rst` の並びが `design.md:837-886` と完全一致 |
| ページ先頭ラベル | `style.md:299-400` の S-08 一覧37件と実物が0件不一致 |
| ラベルの重複 | `ja/` 全体の参照ラベル定義1003件に重複0件 |
| フルビルド | `sphinx-build -a` で **build succeeded、WARNING・ERROR ともに0件** |
| `checks/task-07.md` のリンク切れ3件 | すべて解消済み |
| `verify_mapping.py` | `OK: no errors`（exit 0） |
| `verify_glossary.py` | 不一致25件。`#pre-last` が処理予定の既知件数どおりで、新規の劣化なし |
| S-01・S-02・S-04・S-05・S-09・S-11 | 38ファイルを機械検査して指摘0件（見出し384件・code-block 201件・list-table 136件・目次31件を走査したことをカウンタで確認済み） |
| 出典行の消化 | 未出現の識別子を全件、解説書全体に対して追跡。取りこぼしなし（下記） |

`ja/conf.py:103` が `keep_warnings = True` のため未解決参照はビルドを失敗させないが、今回は WARNING 自体が0件のため、この設定に依存せず参照の健全性を確認できている。

## db_queue 3ページのゲート（DQ1〜DQ5）

`ntf-doc-27-db-queue.md` の5ゲートをすべて確認し、合格。

| ゲート | 結果 |
| --- | --- |
| DQ1 `code-block` 0件 | 3ページとも6行で code-block なし |
| DQ2 `機能概要`・`使用方法` の見出しなし | 3ページともラベル・タイトル・本文1行のみ |
| DQ3 `:ref:` 飛び先ラベルが実在 | `request_unit_test_setting_batch`（`setup/request_unit_test/batch.rst:1`）・`request_unit_test_batch`（`implementation/request_unit_test/batch.rst:1`）・`deal_unit_test_batch`（`implementation/deal_unit_test/batch.rst:1`）の3件とも実在 |
| DQ4 `setup/deal_unit_test/db_queue.rst` 未作成 | `setup/deal_unit_test/` は `http_messaging.rst`・`mom.rst`・`rest.rst` の3件のみ。`design.md:386`・`:891` のとおり |
| DQ5 `undefined label` 増加なし | フルビルドで WARNING 0件 |

## 出典から変えた点のうち、実装で正しさを確認したもの

出典に出現する識別子で解説書全体に現れないものを全件追跡した結果、内容の取りこぼしはなかった。差分の大半は S-08 によるラベル改名とサンプルコードの書き直しだが、次の5件は**出典の記述が実装と食い違っており、新ページが実装どおりに直している**。実装（`nablarch-testing` `e21bf67`）で確認した。

| # | 出典の記述 | 新ページの記述 | 実装での確認箇所 |
| --- | --- | --- | --- |
| 1 | `beforeExecuteRequest` / `afterExecuteRequest` | `beforeExecute` / `afterExecute`（`implementation/request_unit_test/web.rst:106`・`:109`） | `src/main/java/nablarch/test/core/http/Advice.java:23`・`:31` |
| 2 | `isTokenValid` カラム | `isValidToken`（`implementation/request_unit_test/web.rst:105`、`implementation/testdata_notation.rst:411`） | `src/main/java/nablarch/test/core/http/TestCaseInfo.java:48` |
| 3 | ロガー名 `MESSAGING_SEND_MAP` / `MESSAGING_SEND_CSV` | `MESSAGING_MAP` / `MESSAGING_CSV`（`implementation/deal_unit_test/mom.rst:111`） | `src/main/java/nablarch/test/core/messaging/SendSyncSupport.java:40`・`:43` |
| 4 | testShots の `outFile` カラム | `expectedFile`（`implementation/deal_unit_test/batch.rst:93`） | `src/main/java/nablarch/test/core/batch/BatchRequestTestSupport.java:128` |
| 5 | 「Linuxの場合はシェルスクリプト(httpDump.sh)を選択する」 | 起動用スクリプトを `httpDump.bat` のみとする（`tools/request_data_tool.rst:62`・`:82`） | 現行解説書の配布物（`2e501ad`）にも `download/httpDump.bat` しかなく、`httpDump.sh` は存在しない |

5件とも `reviews/` に記録済みであることを確認した（1・2は `page-request_unit_test_web.md`、3は `page-deal_unit_test_mom.md`、4は `page-deal_unit_test_batch.md`、5は `page-request_data_tool.md`）。

## 申し送り（`#27` の是正ではない）

### 申し送り1: `about/index.rst:108` が `guide/` 配下の画像を参照している

`about/index.rst:108` が `.. image:: ../guide/development_guide/06_TestFWGuide/_images/abstract_structure.png` を参照している。`design.md:907` は画像を該当ページへ `git mv` すると規定し、`guide/` は全ページ移設完了後にディレクトリごと無くなる残骸としているため、この参照が残っていると `guide/` を削除できない。

### 申し送り2: `guide/` 配下に追跡ファイルが88件残っている

`guide/` 配下に git 追跡下のファイルが88件（png 71・xlsx 8・java 6・jpg 2・JPG 1、`.rst` は0件）残存している。新ページから参照されているのは申し送り1の1件のみで、**87件が未参照**。

いずれも `#pre-last` または `#last` で扱う対象と考える（判断は user）。

## `#last` に引き継ぐ確認済み事項

`#last` の Completion criteria のうち、次は `7e19f68` の時点で既に充足している。`#last` では再確認のみでよい。

- `undefined label` / `toctree contains reference to nonexisting document` / `unknown document` が各0件（`steering.md:644-650`）
- `checks/task-07.md` のリンク切れ3件の解消（`steering.md:651`）
