.. _testing_framework_setup:

テスティングフレームワークの導入と設定
==================================================
ここでは、アーキテクトが行う導入と設定を説明する。\ :ref:`テスティングフレームワークの導入 <testing_framework_introduction>`\ ・\ :ref:`JUnit 5での使用 <standard_usage>`\ ・\ :ref:`テストデータの設定（形式・配置・記述の省略） <testdata_setting>`\ の3ページは全員が読む。\ JUnit 4\ で書き続けるプロジェクトは、\ :ref:`JUnit 4での使用 <junit4_support>`\ も読む。\ :ref:`システム日時と採番の固定 <fixed_time_and_id>`\ ・\ :ref:`エンティティ単体テストの設定 <entity_unit_test_setting>`\ ・\ :ref:`コンポーネント単体テストの設定（デフォルト以外のトランザクション） <component_unit_test_setting>`\ ・\ :ref:`マスタデータ復旧機能 <master_data_restore>`\ は該当するテストがあるときだけ読み、残りは自分が担当する処理方式のページを読む。

.. toctree::
   :maxdepth: 1

   introduction
   standard_usage
   junit4
   testdata
   fixed_time_and_id
   entity_unit_test
   component_unit_test
   request_unit_test/web
   request_unit_test/rest
   request_unit_test/http_messaging
   request_unit_test/batch
   request_unit_test/mom
   request_unit_test/db_queue
   deal_unit_test/rest
   deal_unit_test/http_messaging
   deal_unit_test/mom
   master_data_restore
