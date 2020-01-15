=========================================
 データベースを使用した2重サブミット防止
=========================================

.. contents:: 目次
  :depth: 3
  :local:


     
機能概要
========

デフォルト実装では、サーバ側のトークンはHTTPセッションに保存される。
このため、アプリケーションサーバをスケールアウトする際には、スティッキーセッションやセッションレプリケーション等を
使用する必要がある。

サーバ側のトークンをデータベースに保管する実装を使用することで、特にアプリケーションサーバの設定をしなくても、
複数のアプリケーションサーバ間でトークンを共有できる。


モジュール一覧
==============

<dependency>
  <groupId>com.nablarch.framework</groupId>
  <artifactId>nablarch-fw-doublesubmit-jdbc</artifactId>
</dependency>

使用方法
========

 ``tokenManager`` という名前でコンポーネント定義を追加する。

.. code-block:: xml
                
    <component name="tokenManager"
               class="nablarch.common.web.token.JdbcTokenManager" />

               
