.. _`database-functional_comparison_jdbc_wrapper`:

ユニバーサルDAOとJDBCラッパーとの機能比較
----------------------------------------------------------------------------------------------------
この章では、以下の機能の比較を示す。

* :ref:`ユニバーサルDAO <universal_dao>`
* :ref:`JDBCラッパー <database>`

ユニバーサルDAOは、内部で :ref:`JDBCラッパー <database>` を使用してデータベースアクセスを行う簡易的なO/Rマッパーである。
このため、 :ref:`database_management` で説明したように、SQLの実行は原則としてユニバーサルDAOで行い、
ユニバーサルDAOで実現できない場合に :ref:`JDBCラッパー <database>` を使用する。

JDBCラッパーを使用する場面
  ユニバーサルDAOでは実現できず、JDBCラッパーを使用する必要がある代表的な場面は以下のとおり。

  * 任意の更新系SQL(UPDATE、INSERT、DELETE、MERGE)を実行する場合(例えば、主キー以外の条件を指定した更新や削除)
  * ストアードプロシージャを実行する場合
  * サイズの大きいバイナリデータやテキストデータ(BLOBやCLOB)を、メモリに展開せずストリームで登録、更新、取得する場合
  * 登録日時や更新日時といった共通項目の値を、SQL実行時に自動的に設定する場合
  * 検索結果をキャッシュする場合
  * Entityから自動生成されるSQLで、SQL文中のスキーマを環境毎に切り替える場合
  * バッチ処理やメッセージング処理のデータリーダに、検索用のステートメントを渡す場合
  * どうしてもSQLファイルに定義できないSQLを、SQL文を直接指定して実行する場合

.. list-table:: 機能比較（○：提供あり　△：一部提供あり　×：提供なし　－:対象外）
  :header-rows: 1
  :class: something-special-class

  * - 機能
    - ユニバーサルDAO
    - JDBCラッパー

  * - Entityを元にCRUDが実行できる |br|
      SQLを作成することなくCRUDのSQLを実行できる
    - ○ |br| :ref:`解説書へ <universal_dao-execute_crud_sql>`
    - × [#crud]_

  * - SQLファイルに記述した任意のSQLで検索できる
    - ○ |br| :ref:`解説書へ <universal_dao-sql_file>`
    - ○ |br| :ref:`解説書へ <database-execute_sqlid>`

  * - 任意の更新系SQL(UPDATE、INSERT、DELETE、MERGE)を実行できる |br|
      (主キー以外の条件を指定した更新や削除など)
    - × [#update]_
    - ○ |br| :ref:`解説書へ <database-input_bean>`

  * - SQL文を直接指定して実行できる
    - ×
    - ○ [#direct_sql]_ |br| :ref:`解説書へ <database-sql_file>`

  * - ストアードプロシージャを実行できる
    - ×
    - ○ |br| :ref:`解説書へ <database-stored_procedure>`

  * - Beanのプロパティ値をSQLのバインド変数に設定できる
    - ○ |br| :ref:`解説書へ <universal_dao-search_with_condition>`
    - ○ |br| :ref:`解説書へ <database-input_bean>`

  * - SQLの動的組み立てができる
    - ○ [#criteria]_ |br| :ref:`解説書へ <universal_dao-sql_file>`
    - ○ |br| :ref:`解説書へ <database-variable_condition>`

  * - 検索結果をJava Beansオブジェクトとして取得できる
    - ○ |br| :ref:`解説書へ <universal_dao-bean_mapping>`
    - × [#sqlrow]_

  * - 大量データを取得する際に遅延ロードができる |br|
      (ヒープを圧迫せずに大量データを処理できる)
    - ○ |br| :ref:`解説書へ <universal_dao-lazy_load>`
    - ○ [#iterator]_

  * - ページング用の範囲指定の検索ができる
    - ○ |br| :ref:`解説書へ <universal_dao-paging>`
    - ○ |br| :ref:`解説書へ <database-paging>`

  * - 検索結果をキャッシュできる
    - × [#cache]_
    - ○ |br| :ref:`解説書へ <database-use_cache>`

  * - バッチ実行(一括登録、更新、削除)ができる
    - ○ |br| :ref:`解説書へ <universal_dao-batch_execute>`
    - ○ [#batch]_

  * - 楽観的ロックができる
    - ○ |br| :ref:`解説書へ <universal_dao_jpa_optimistic_lock>`
    - × [#optimistic_lock]_

  * - 悲観的ロックができる
    - － [#pessimistic_lock]_ |br| :ref:`解説書へ <universal_dao_jpa_pessimistic_lock>`
    - － [#pessimistic_lock]_

  * - 共通項目(登録日時や更新日時など)の値を自動的に設定できる
    - × [#common_property]_
    - ○ |br| :ref:`解説書へ <database-common_bean>`

  * - サイズの大きいバイナリデータやテキストデータ(BLOBやCLOB)を |br|
      ストリームで登録、更新、取得できる
    - × [#lob]_
    - ○ |br| :ref:`解説書へ(バイナリ型) <database-binary_column>` |br| :ref:`解説書へ(CLOB型) <database-clob_column>`

  * - サロゲートキーの値を採番できる
    - ○ |br| :ref:`解説書へ <universal_dao-generate_surrogate_key>`
    - × [#generator]_

  * - 現在のトランザクションとは異なるトランザクションで実行できる
    - ○ |br| :ref:`解説書へ <universal_dao-transaction>`
    - ○ |br| :ref:`解説書へ <database-new_transaction>`

  * - SQL文中のスキーマを環境毎に切り替えられる
    - △ [#schema]_ |br| :ref:`解説書へ <universal_dao-execute_crud_sql>`
    - ○ |br| :ref:`解説書へ <database-replace_schema>`

  * - バッチ処理やメッセージング処理のデータリーダに |br| 検索用のステートメントを渡せる
    - ×
    - ○ |br| :ref:`解説書へ(バッチ) <nablarch_batch-data_reader>` |br| :ref:`解説書へ(メッセージング) <db_messaging_architecture-reader>`

.. [#crud] JDBCラッパーでは、CRUDのSQLもSQLファイルに記述して実行する。
.. [#update] ユニバーサルDAOでは、SQLファイルに記述したSQLは検索にのみ使用できる。更新や削除は、Entityから自動生成されるSQL(主キーを条件とした更新、削除)に限られる。
.. [#direct_sql] SQLは原則SQLファイルに記述し、SQL文を直接指定するAPIは、どうしてもSQLファイルに定義できない場合のみ使用すること。詳細は、 :ref:`database-sql_file` を参照。
.. [#criteria] ユニバーサルDAOでは、SQLファイルに記述した条件及びソート項目に限り動的な組み立てができる。詳細は、 :ref:`SQLの動的組み立て <database-variable_condition>` を参照。
.. [#sqlrow] JDBCラッパーでは、検索結果は :java:extdoc:`SqlResultSet <nablarch.core.db.statement.SqlResultSet>` ( :java:extdoc:`SqlRow <nablarch.core.db.statement.SqlRow>` のリスト)として取得する。
.. [#iterator] JDBCラッパーでは、 :java:extdoc:`SqlPStatement#executeQuery <nablarch.core.db.statement.SqlPStatement.executeQuery()>` で取得した :java:extdoc:`ResultSetIterator <nablarch.core.db.statement.ResultSetIterator>` を使用して、検索結果を1件ずつ処理する。
.. [#cache] ユニバーサルDAOで実行する検索には、 :ref:`database-use_cache` の設定は適用されない。
.. [#batch] JDBCラッパーでは、 :java:extdoc:`SqlPStatement#addBatch <nablarch.core.db.statement.SqlPStatement.addBatch()>` や :java:extdoc:`ParameterizedSqlPStatement#addBatchObject <nablarch.core.db.statement.ParameterizedSqlPStatement.addBatchObject(java.lang.Object)>` でバッチにSQLを追加し、 :java:extdoc:`SqlPStatement#executeBatch <nablarch.core.db.statement.SqlPStatement.executeBatch()>` で一括実行する。
.. [#optimistic_lock] JDBCラッパーでは、バージョン番号の比較と更新をSQLに記述することで楽観的ロックを実現する。
.. [#pessimistic_lock] 悲観的ロックは、どちらの機能でもデータベースの行ロック( ``select for update`` )をSQLに記述することで実現する。
.. [#common_property] 共通項目の値を自動設定する場合は、 :ref:`doma_adaptor` を適用するか、ユニバーサルDAOを呼び出す前にアプリケーションで明示的に値を設定する。
.. [#lob] ユニバーサルDAOでは、データをすべてメモリに展開しないと登録(更新)できない。
.. [#generator] JDBCラッパーで採番した値を使用する場合は、 :ref:`generator` の記載に従いアプリケーション側で採番する。
.. [#schema] ユニバーサルDAOでは、Entityから自動生成されるSQLに対して :ref:`database-replace_schema` は使用できない。この場合は ``@Table`` アノテーションでスキーマを指定する。

.. |br| raw:: html

  <br />
