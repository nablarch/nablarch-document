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

## `ja/development_tools/index.rst` の NTF への toctree 参照の現状

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

`testing_framework/index` の toctree エントリが存在する。`.rst` 削除に伴いこのエントリは
リンク切れになるが、本タスク（#7）では白紙化のみを行い、`index.rst` の更新はスコープ外
（`#8〜` のページ作成でNTFの新構成が確定してから toctree を張り直す）。

参考: 同様に `ja/index.rst:54` にも `:doc:` 参照
（`` :doc:`テスティングフレームワーク <development_tools/testing_framework/index>` ``）があり、
これも `.rst` 削除後はリンク切れになる。`ja/development_tools/index.rst` 以外の参照だが、
影響範囲の記録として合わせて残す。この2箇所以外に `testing_framework` を参照する `.rst` は
存在しない（`grep -rn "testing_framework" --include="*.rst" ja/` で確認）。

## 画像・ダウンロード素材の保持

`_image/` / `_images/` 配下および `download/` / `_download/` 配下のファイル（125件）は削除対象外。
削除は `.rst` の47件のみに限定する。

## 削除後の確認

- `find ja/development_tools/testing_framework -type f -name "*.rst"` の結果が0件
- `find ja/development_tools/testing_framework -type f ! -name "*.rst" | wc -l` が125件のまま変化なし
