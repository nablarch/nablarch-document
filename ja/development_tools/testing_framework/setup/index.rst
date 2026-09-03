.. _testing_framework_setup:

テスティングフレームワークの導入と設定
==================================================
この部では、アーキテクトが行う導入と設定を説明する。次の順に読む。

まず、テストの種類によらず全員が行う設定を3ページで説明する。\ :ref:`テスティングフレームワークの導入 <testing_framework_introduction>`\ で依存関係の追加とテスト用のコンポーネント設定ファイルの用意を行い、\ :ref:`JUnit 5での使用 <standard_usage>`\ でテストクラスからテスティングフレームワークの機能を使う方法を確認し、\ :ref:`テストデータの設定 <testdata_setting>`\ でテストデータの形式・配置・記述の省略を設定する。既にJUnit 4で書いたテスト資産があるプロジェクトは、\ :ref:`JUnit 5での使用 <standard_usage>`\ に加えて\ :ref:`JUnit 4での使用 <junit4_support>`\ を読む（読み替えに使う合成アノテーションの対応表は\ :ref:`JUnit 5での使用 <standard_usage>`\ にある）。

次の2ページは、必要な場合だけ読む。\ :ref:`システム日時と採番の固定 <fixed_time_and_id>`\ は、登録日時・更新日時や採番したIDをテーブルの期待値に書くテストがあるときに読む。\ :ref:`クラス単体テストの設定 <class_unit_test_setting>`\ は、エンティティ単体テスト・コンポーネント単体テストを行うときに読む。

続いて、自分が担当する処理方式のページを読む。リクエスト単体テストの設定は6つの処理方式それぞれに1ページある。取引単体テストの設定は、RESTfulウェブサービス・HTTPメッセージング・MOMによるメッセージングの3つにある。

最後の\ :ref:`マスタデータ復旧機能 <master_data_restore>`\ は、テストの実行中にマスタデータを変更するテストがあるときに読む。

.. toctree::
   :maxdepth: 1

   introduction
   standard_usage
   junit4
   testdata
   fixed_time_and_id
   class_unit_test
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
