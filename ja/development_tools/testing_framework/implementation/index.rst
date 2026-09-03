.. _testing_framework_implementation:

テスティングフレームワークによるテスト実装
==================================================
この部では、アプリケーションプログラマが行うテストデータの記述とテストコードの実装を説明する。\ :ref:`テストデータの書き方 <testdata_notation>`\ を読んでから、自分が実装するテストのページを読む。\ :ref:`テストデータの記載例 <testdata_examples>`\ は、テストデータを書くときに必要な例を引く。

動くテストコードとテストデータの実物は、Exampleアプリケーション（\ `nablarch-example-web <https://github.com/nablarch/nablarch-example-web>`_\ ・\ `nablarch-example-rest <https://github.com/nablarch/nablarch-example-rest>`_\ ・\ `nablarch-example-batch <https://github.com/nablarch/nablarch-example-batch>`_\ ）の\ ``src/test``\ にある（テストデータはExcel形式）。

.. toctree::
   :maxdepth: 1

   testdata_notation
   testdata_examples
   class_unit_test/entity
   class_unit_test/component
   request_unit_test/web
   request_unit_test/rest
   request_unit_test/http_messaging
   request_unit_test/batch
   request_unit_test/mom
   request_unit_test/db_queue
   deal_unit_test/web
   deal_unit_test/rest
   deal_unit_test/http_messaging
   deal_unit_test/batch
   deal_unit_test/mom
   deal_unit_test/db_queue
