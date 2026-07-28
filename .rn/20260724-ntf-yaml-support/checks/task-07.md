# #7 self-check: 現行NTF解説書の削除

## 削除前の全ファイル一覧（`.rst`、パスと行数）

対象: `ja/development_tools/testing_framework/` 配下の `.rst`。件数は47件で、`#2a` 完了時点の実測値
（RST 47）と一致する。行数は `wc -l` の値（改行数）。

```
ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst: 770
ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/02_entityUnitTestWithNablarchValidation.rst: 763
ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/index.rst: 12
ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/01_ClassUnitTest/02_componentUnitTest.rst: 355
ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/01_ClassUnitTest/index.rst: 13
ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/batch.rst: 619
ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/delayed_receive.rst: 56
ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/delayed_send.rst: 118
ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/double_transmission.rst: 39
ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/fileupload.rst: 112
ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/http_real.rst: 177
ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/http_send_sync.rst: 164
ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/index.rst: 755
ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/mail.rst: 28
ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/real.rst: 320
ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/rest.rst: 118
ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/send_sync.rst: 296
ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/batch.rst: 183
ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/delayed_receive.rst: 7
ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/delayed_send.rst: 7
ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/http_send_sync.rst: 69
ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/index.rst: 58
ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/real.rst: 36
ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/rest.rst: 95
ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/send_sync.rst: 383
ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/index.rst: 106
ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/01_Abstract.rst: 739
ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/02_DbAccessTest.rst: 554
ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/02_RequestUnitTest.rst: 552
ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/03_Tips.rst: 832
ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/04_MasterDataRestore.rst: 215
ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/JUnit5_Extension.rst: 455
ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_batch.rst: 262
ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_http_send_sync.rst: 23
ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_real.rst: 197
ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_rest.rst: 361
ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_send_sync.rst: 156
ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/index.rst: 22
ja/development_tools/testing_framework/guide/development_guide/08_TestTools/01_HttpDumpTool/01_HttpDumpTool.rst: 93
ja/development_tools/testing_framework/guide/development_guide/08_TestTools/01_HttpDumpTool/02_SetUpHttpDumpTool.rst: 110
ja/development_tools/testing_framework/guide/development_guide/08_TestTools/01_HttpDumpTool/index.rst: 10
ja/development_tools/testing_framework/guide/development_guide/08_TestTools/02_MasterDataSetup/01_MasterDataSetupTool.rst: 71
ja/development_tools/testing_framework/guide/development_guide/08_TestTools/02_MasterDataSetup/02_ConfigMasterDataSetupTool.rst: 122
ja/development_tools/testing_framework/guide/development_guide/08_TestTools/02_MasterDataSetup/index.rst: 21
ja/development_tools/testing_framework/guide/development_guide/08_TestTools/03_HtmlCheckTool/index.rst: 238
ja/development_tools/testing_framework/guide/development_guide/08_TestTools/index.rst: 12
ja/development_tools/testing_framework/index.rst: 27
```

（取得コマンド: `find ja/development_tools/testing_framework -type f -name "*.rst" | sort` に対し各ファイルへ `wc -l` を実行）

## リンク切れになる参照（3件、`#7`フォローアップで確定。`ntf-doc-07-followup.md` 参照）

削除前の `ja/development_tools/index.rst`:

```rst
============================================
Nablarch開発ツール
============================================

.. toctree::
   :maxdepth: 1

   java_static_analysis/index
   testing_framework/index
   toolbox/index
```

`.rst` 削除に伴い、以下の3件がリンク切れになる。

| # | 参照元 | 参照の形 | 対応 |
|---|---|---|---|
| 1 | `ja/development_tools/index.rst:10` | toctree `testing_framework/index` | `#8〜` の新構成確定後に更新 |
| 2 | `ja/index.rst:54` | `:doc:` `` `テスティングフレームワーク <development_tools/testing_framework/index>` `` | `#8〜` の新構成確定後に更新 |
| 3 | `ja/application_framework/application_framework/libraries/db_double_submit.rst:106` | `:ref:` `` `テスティングフレームワークのトークン発行<how_to_set_token_in_request_unit_test>` `` | **`#8〜` で `implementation/request_unit_test/web.rst` に同名ラベル（`how_to_set_token_in_request_unit_test`）を定義する** |

3件目（FW解説書からNTF解説書への被参照）の詳細:

- 文脈: `db_double_submit.rst` の `.. important::` ブロック内。「テスティングフレームワークのトークン発行はトークンのDB保存に対応していない」という注意喚起の導線
- ラベル定義元（削除済み）: `06_TestFWGuide/02_RequestUnitTest.rst:169`（`.. _how_to_set_token_in_request_unit_test:` / 見出し「トークン発行」）
- 内容を引き継ぐマッピング行: `current-0206`（`02_RequestUnitTest.rst` 106-207、`MOVE`）
- 新しい行き先: 第3部 リクエスト単体テスト（ウェブアプリケーション）> 使用方法 → `implementation/request_unit_test/web.rst`
- NTF解説書の再構築スコープ外（FW解説書側）から入ってくるリンクであり、新ページで同名ラベルを定義しない限り FW解説書の `.. important::` が黙って壊れる

1・2件目は `ja/development_tools/index.rst` 以外の箇所（`ja/index.rst:54`）も含めて当初の `#7` self-check で記録済み。3件目は `:ref:` によるラベル参照でパス文字列（`testing_framework`）を含まないため、`grep -rn "testing_framework"` では検出できず、`#7`フォローアップ（`ntf-doc-07-followup.md`）で追加した独立調査（下記「ラベルの全数調査」）で発見した。

### `en/` 側は影響なし（確認済み）

`en/index.rst:52` と `en/development_tools/index.rst:10` も `testing_framework` を参照しているが、これらは影響しない。

- `ja/conf.py` と `en/conf.py` が別に存在し、Sphinx プロジェクトが分かれている
- `en/development_tools/testing_framework/` が独立したツリーとして存在し、削除されていない
- `en/` から（`ja/` 削除ツリーと同名の）ラベルへの `:ref:` 参照は123件あるが、すべて `en/` 内のラベルを解決する

`#7` が `ja/` 側のみを記録したのは正しい判断である。

### 未解決参照がビルド失敗にならない理由

リポジトリに CI 設定（workflow）は存在しない。また `ja/conf.py:103` は `keep_warnings = True` のため、
`make html` を実行しても未解決の `:ref:`/`:doc:` 参照はビルド失敗にならず、出力に警告として
埋め込まれるだけである。したがって上記3件は `make html` のエラー0件では検出できず、
本ドキュメントでの手動記録が唯一の追跡手段になる。

### ラベルの全数調査（`#7`フォローアップ、独立検証）

削除した47ファイルが定義していた `:ref:` ラベルを全件洗い出し、`ja/` の削除ツリー外から
参照されているものを特定した。

実行コマンド（削除前コミット `2e501ad` から取得。削除コミットは `6bf8cfb`）:

```bash
for f in $(git diff --name-only --diff-filter=D 2e501ad 6bf8cfb); do
  git show 2e501ad:"$f" | grep -oE '^\.\. _[A-Za-z0-9_-]+:'
done | sed 's/^\.\. _//;s/:$//' | sort -u > /tmp/labels.txt
wc -l < /tmp/labels.txt
```

→ **定義ラベル76件**

次に `ja/` 配下（削除ツリーを除く）の全 `.rst` から `:ref:` 参照を機械的に抽出（``:ref:`表示文字<label>` `` と ``:ref:`label` `` の両形式に対応）し、定義ラベル集合との交差を取った:

```bash
grep -rnoE ':ref:`[^`]+`' --include="*.rst" ja/ \
  | grep -v '^ja/development_tools/testing_framework/' \
  > ja_ref_refs_raw.txt
wc -l < ja_ref_refs_raw.txt   # 2708件（ja/ 全体の :ref: 総数、削除ツリー除く）

# `<label>` 形式は < 以降を、それ以外は本体をラベルとして抽出し、
# 定義ラベル集合(labels.txt)との交差を取る
awk -F'\t' 'NR==FNR{labels[$1]=1; next} { if ($2 in labels) print }' labels.txt ja_ref_labels.txt
```

→ **`ja` 外部参照1件**: `ja/application_framework/application_framework/libraries/db_double_submit.rst:106: how_to_set_token_in_request_unit_test`

定義ラベル76件・`ja` 外部参照1件は、`ntf-doc-07-followup.md` が事前に提示した独立検証の実測値（76件／1件）と一致する。

## 画像・ダウンロード素材の保持

`_image/` / `_images/` 配下および `download/` / `_download/` 配下のファイル（125件）は削除対象外。
削除は `.rst` の47件のみに限定する。

## 削除後の確認

- `find ja/development_tools/testing_framework -type f -name "*.rst"` の結果が0件
- `find ja/development_tools/testing_framework -type f ! -name "*.rst" | wc -l` が125件のまま変化なし
