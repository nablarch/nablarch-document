.. _testing_framework_implementation:

テスティングフレームワークによるテスト実装
==================================================
この部では、アプリケーションプログラマが行うテストデータの記述とテストコードの実装を説明する。次の順に読む。

まず\ :ref:`テストデータの書き方 <testdata_notation>`\ を読む。テストデータの構成と値の解釈規則は、テストの種類・処理方式・テストデータの形式によらず共通である。\ :ref:`テストデータの記載例 <testdata_examples>`\ には、その記法の実例を用途別に載せている。通しで読む必要はなく、テストデータを書くときに必要な例を引く。

次に、自分が実装するテストのページを読む。クラス単体テストは、テスト対象のクラスによって\ :ref:`エンティティ単体テスト <entity_unit_test>`\ と\ :ref:`コンポーネント単体テスト <component_unit_test>`\ に分かれる。リクエスト単体テストと取引単体テストは、処理方式ごとに1ページある。3種類のテストの違いは、\ :ref:`テスティングフレームワークとは <testing_framework_about>`\ で説明している。

各ページのテストは、\ :ref:`テスティングフレームワークの導入と設定 <testing_framework_setup>`\ が済んでいることを前提とする。

動くテストコードとテストデータの実物は、Exampleアプリケーション（\ `nablarch-example-web <https://github.com/nablarch/nablarch-example-web>`_\ ・\ `nablarch-example-rest <https://github.com/nablarch/nablarch-example-rest>`_\ ・\ `nablarch-example-batch <https://github.com/nablarch/nablarch-example-batch>`_\ ）の\ ``src/test``\ にある（テストデータはExcel形式）。テストクラスの形やテストデータの書き方に迷ったときの参考にする。

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
