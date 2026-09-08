.. _component_unit_test_setting:

コンポーネント単体テストの設定（デフォルト以外のトランザクション）
==================================================================

.. contents:: 目次
  :depth: 3
  :local:

機能概要
--------------------------------------------------
コンポーネント単体テストでは、テストメソッドの実行前後にデフォルトのデータベーストランザクションが開始・終了される。デフォルト以外のトランザクションも使うコンポーネントをテストする場合は、そのトランザクションを環境設定ファイルに指定する。

使用方法
--------------------------------------------------

.. _component_unit_test_setting-db_transaction:

デフォルト以外のトランザクションを使用する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
コンポーネント単体テストでは、テストメソッドの実行前後に、\ :java:extdoc:`DbAccessTestSupport <nablarch.test.core.db.DbAccessTestSupport>`\ がデフォルトのデータベーストランザクションを開始・終了する。これ以外のトランザクションも使用する場合は、テスト用のコンポーネント設定ファイルに\ :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>`\ を登録し、環境設定ファイルの\ ``dbAccessTest.dbTransactionName``\ にそのコンポーネント名を記述する。複数指定する場合はカンマで区切る。指定した名前のコンポーネントが登録されていない場合は、テストメソッドの実行前に例外が発生する。デフォルトのトランザクションは、この記述の有無にかかわらず開始される。この設定を読むのは\ :java:extdoc:`DbAccessTestSupport <nablarch.test.core.db.DbAccessTestSupport>`\ だけであり、リクエスト単体テストには影響しない。

.. code-block:: properties

  dbAccessTest.dbTransactionName=employeeTransaction,departmentTransaction
