.. _`db_double_submit`:

データベースを使用した2重サブミット防止
=====================================================================

.. contents:: 目次
  :depth: 3
  :local:

デフォルト実装では、サーバ側のトークンはHTTPセッションに保存される。
このため、アプリケーションサーバをスケールアウトする際には、スティッキーセッションやセッションレプリケーション等を
使用する必要がある。

サーバ側のトークンをデータベースに保管する実装を使用することで、特にアプリケーションサーバの設定をしなくても、
複数のアプリケーションサーバ間でトークンを共有できる。
     
機能概要
---------------------------------------------------------------------

サーバ側のトークンをデータベースに保管することができる

モジュール一覧
---------------------------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web-doublesubmit-jdbc</artifactId>
  </dependency>


使用方法
---------------------------------------------------------------------

2種類のコンポーネント定義を追加する。

``tokenManager`` という名前でコンポーネント定義を追加する。
これにより、トークンがデータベースで管理されるようになる。

.. code-block:: xml
                
  <component name="tokenManager" class="nablarch.common.web.token.DbTokenManager">
    <!-- 設定値の詳細はJavadocを参照 -->
  </component>

``tokenGenerator`` という名前でコンポーネント定義を追加する。
これによりトークンにUUIDが使用され、推測および衝突の可能性を考慮しなくてよくなる。

.. code-block:: xml

    <component name="tokenGenerator"
               class="nablarch.common.web.token.UUIDV4TokenGenerator" />

また、データベース上にトークンを保存するためのテーブルが必要となる。

作成するテーブルの定義を以下に示す。

`TOKEN` テーブル
  ==================== ====================
  カラム名             データ型
  ==================== ====================
  VALUE(PK)            `java.lang.String`
  CREATED_AT           `java.sql.Timestamp`
  ==================== ====================

テーブル名およびカラム名は変更可能である。
変更する場合は、 :java:extdoc:`DbTokenManager.dbTokenSchema <nablarch.common.web.token.DbTokenManager.setDbTokenSchema(nablarch.common.web.token.DbTokenSchema)>` に
:java:extdoc:`DbTokenSchema <nablarch.common.web.token.DbTokenSchema>` のコンポーネントを定義する。

.. code-block:: xml

  <property name="dbTokenSchema">
    <component class="nablarch.common.web.token.DbTokenSchema">
      <!-- 設定値の詳細はJavadocを参照 -->
    </component>
  </property>
