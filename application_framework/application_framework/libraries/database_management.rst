.. _database_management:

データベースアクセス
==================================================
データベースへの接続やSQLの実行を行う機能を提供する。

Nablarchでは、以下の2種類のデータベースアクセス機能を提供している。

.. toctree::
  :maxdepth: 1

  database/database
  database/universal_dao

上記のどちらの機能を使用した場合でも、SQLの実行を行うことができるが、
以下の理由により :ref:`ユニバーサルDAO <universal_dao>` を使用することを推奨する。

* CRUDのSQL文をEntityから自動的に生成しSQLが実行できる
* 検索結果がBeanオブジェクトとして取得できるため、IDEの補完機能が有効活用でき開発効率が良い

.. important::

  :ref:`ユニバーサルDAO <universal_dao>` を使用した場合でも、
  データベースへの接続やSQL実行は :ref:`JDBCのラッパー機能 <database>` を使用している。
  このため、 :ref:`JDBCのラッパー機能 <database>` を使うための設定などは必要になる。

.. tip::
 :ref:`universal_dao` とJSR317(JPA2.0)との機能比較は、 :ref:`database-functional_comparison` を参照。

.. toctree::
  :hidden:

  database/functional_comparison