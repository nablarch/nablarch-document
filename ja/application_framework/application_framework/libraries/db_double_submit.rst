.. _`db_double_submit`:

データベースを使用した二重サブミット防止
=====================================================================

.. contents:: 目次
  :depth: 3
  :local:

:ref:`二重サブミット防止 <tag-double_submission>` では、サーバ側のトークンはHTTPセッションに保存される。
このため、アプリケーションサーバをスケールアウトする際には、スティッキーセッションやセッションレプリケーション等を
使用する必要がある。

サーバ側のトークンをデータベースに保管する実装を使用することで、特にアプリケーションサーバの設定をしなくても、
複数のアプリケーションサーバ間でトークンを共有できる。

.. tip::

  ブラウザが閉じられた場合などにテーブル上にトークンが残ってしまうことがある。
  そのため、期限切れのトークンは定期的に削除する必要がある。

.. important::

  HTTPセッションを使用した :ref:`二重サブミット防止 <tag-double_submission>` はCSRF対策に使用できたが、
  本機能はユーザを識別せずにトークンをDBに格納しているためCSRF対策に使用できない。
  本機能を使用する場合は、CSRF対策に :ref:`csrf_token_verification_handler` を使用すること。

機能概要
---------------------------------------------------------------------

サーバ側のトークンをデータベースに保管できる

モジュール一覧
---------------------------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web-doublesubmit-jdbc</artifactId>
  </dependency>


使用方法
---------------------------------------------------------------------

データベース上にトークンを保存するためのテーブルが必要となる。

作成するテーブルの定義を以下に示す。

`DOUBLE_SUBMISSION` テーブル
  ==================== ====================
  カラム名             データ型
  ==================== ====================
  TOKEN(PK)            `java.lang.String`
  CREATED_AT           `java.sql.Timestamp`
  ==================== ====================

テーブル名およびカラム名は変更可能である。
変更する場合は、 :java:extdoc:`DbTokenManager.dbTokenSchema <nablarch.common.web.token.DbTokenManager.setDbTokenSchema(nablarch.common.web.token.DbTokenSchema)>` に
:java:extdoc:`DbTokenSchema <nablarch.common.web.token.DbTokenSchema>` のコンポーネントを定義する。

2種類のコンポーネント定義を追加する。

``tokenManager`` という名前でコンポーネント定義を追加する。
これにより、トークンがデータベースで管理されるようになる。
``tokenManager`` は :ref:`初期化<repository-initialize_object>` が必要。

.. code-block:: xml
                
  <component name="tokenManager" class="nablarch.common.web.token.DbTokenManager">
    <property name="dbManager">
      <component class="nablarch.core.db.transaction.SimpleDbTransactionManager">
        <property name="dbTransactionName" value="tokenTransaction"/>
      </component>
    </property>
    <!-- 上記のテーブル定義からテーブル名、カラム名を変更する場合のみ以下設定が必要 -->
    <property name="dbTokenSchema">
      <component class="nablarch.common.web.token.DbTokenSchema">
        <property name="tableName" value="DB_TOKEN"/>
        <property name="tokenName" value="VALUE_COL"/>
        <property name="createdAtName" value="CREATED_AT_COL"/>
      </component>
    </property>
  </component>

  <!-- 初期化が必要なため、以下を設定 -->
  <component name="initializer" class="nablarch.core.repository.initialization.BasicApplicationInitializer">
    <property name="initializeList">
      <list>
        <component-ref name="tokenManager"/>
      </list>
    </property>
  </component>


``tokenGenerator`` という名前でコンポーネント定義を追加する。
これによりトークンにUUIDが使用され、推測および衝突の可能性を考慮しなくてよくなる。

.. code-block:: xml

    <component name="tokenGenerator"
               class="nablarch.common.web.token.UUIDV4TokenGenerator" />

.. important::

  :ref:`テスティングフレームワークのトークン発行<how_to_set_token_in_request_unit_test>` はトークンのDB保存に対応していない。
  そのため、自動テスト実行時には :java:extdoc:`HttpSessionTokenManager <nablarch.common.web.token.HttpSessionTokenManager>` に差し替えてテストする必要がある。

  .. code-block:: xml

    <!-- トークンをHTTPセッションに保存する -->
    <component name="tokenManager" class="nablarch.common.web.token.HttpSessionTokenManager"/>
