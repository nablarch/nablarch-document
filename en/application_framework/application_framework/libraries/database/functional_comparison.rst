.. _`database-functional_comparison`:

ユニバーサルDAOとJSR317(JPA2.0)との機能比較
----------------------------------------------------------------------------------------------------
この章では、以下の機能の比較を示す。

* :ref:`ユニバーサルDAO <universal_dao>`
* |JSR317|

.. important::

  ユニバーサルDAOでは、JPAで定義されているアノテーションのうち、 :ref:`universal_dao_jpa_annotations` に記載のあるものだけをサポートしている。
  ここに記載のないアノテーションに関連する機能については、使用することはできない。

.. list-table:: 機能比較（○：提供あり　△：一部提供あり　×：提供なし　－:対象外）
  :header-rows: 1
  :class: something-special-class

  * - 機能
    - ユニバーサルDAO
    - JSR317

  * - リレーションシップに対応できる |br|
    - × [#relation]_
    - ○

  * - Entityを元にCRUDが実行できる |br|
      SQLを作成することなくCRUDのSQLを実行できる
    - ○ |br| :ref:`解説書へ <universal_dao-execute_crud_sql>`
    - ○

  * - 検索結果をJava Beansオブジェクトとして取得できる
    - ○ |br| :ref:`解説書へ <universal_dao-bean_mapping>`
    - ○

  * - 任意のSQL文を実行できる
    - ○ |br| :ref:`解説書へ <universal_dao-sql_file>`
    - ○

  * - SQLの動的組み立てができる
    - △ [#criteria]_ |br| :ref:`解説書へ <universal_dao-sql_file>`
    - ○

  * - バッチ実行ができる
    - ○ |br| :ref:`解説書へ <universal_dao-batch_execute>`
    - ×

  * - 大量データを取得する際に遅延ロードができる |br|
      (ヒープを圧迫せずに大量データを処理できる)
    - ○ |br| :ref:`解説書へ <universal_dao-lazy_load>`
    - ×

  * - ページング用の範囲指定の検索ができる
    - ○ |br| :ref:`解説書へ <universal_dao-paging>`
    - ○

  * - サロゲートキーの値を採番できる
    - ○ |br| :ref:`解説書へ <universal_dao-generate_surrogate_key>`
    - ○

  * - Entityの状態をデータベースに反映時に |br| Bean Validationが実行できる
    - × [#validaiton]_
    - ○

  * - データベースアクセス前後に |br| 任意の処理(コールバック呼び出し)を実行できる
    - × [#callback]_
    - ○

  * - 排他制御ができる
    - △ [#lock]_ |br| :ref:`解説書へ(楽観ロック) <universal_dao_jpa_optimistic_lock>` |br| :ref:`解説書へ(悲観ロック) <universal_dao_jpa_pessimistic_lock>`
    - ○

.. [#relation] リレーションシップがあるテーブルの検索はSQLを作成することで対応できる。登録、更新、削除については、テーブル毎に必要な処理を呼び出すことで対応する。
.. [#criteria] ユニバーサルDAOでは、条件及びソート項目に限り動的な組み立てができる。詳細は、 :ref:`SQLの動的組み立て <database-variable_condition>` を参照
.. [#validaiton] Nablarchでは、外部からのデータを受け付けたタイミングでバリデーションを実施し、バリデーションエラーがない場合のみEntityへの変換及びデータベースへの保存を行う。
.. [#callback] 任意の処理が必要となる場合は、ユニバーサルDAOを呼び出す側で処理を行うことで対応する。
.. [#lock] ユニバーサルDAOでは、楽観的ロックのみサポートする。悲観的ロックやJSRで定義されている検索時のロックモードの指定などはサポートしない。(悲観的ロックは、 ``select for update`` などを使用することで実現できる。)

.. |jsr317| raw:: html

   <a href="https://jcp.org/en/jsr/detail?id=317" target="_blank">JSR317(外部サイト、英語)</a>

.. |br| raw:: html

  <br />
