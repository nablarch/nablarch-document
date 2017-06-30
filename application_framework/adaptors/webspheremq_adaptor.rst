.. _webspheremq_adaptor:

IBM WebSphere MQアダプタ
==================================================

.. contents:: 目次
  :depth: 3
  :local:

:ref:`NablarchのMOMメッセージング機能 <mom_messaging>` で `IBM WebSphere MQ(外部サイト、英語) <http://www-03.ibm.com/software/products/ja/websphere-mq>`_ を使用するためのアダプタを提供する。

WebSphere MQの仕様及び構築手順などは、IBM社のオフィシャルサイト及びマニュアルを参照すること。

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-wmq-adaptor</artifactId>
  </dependency>

.. important::

  WebSphere MQのjarに関しては、製品マニュアルを参照し必要なものをクラスパスに追加すること。

本アダプタを使用するための設定
--------------------------------------------------
本アダプタは、以下の手順にてコンポーネント定義を行うことで有効になる。

1.  ``nablarch.integration.messaging.wmq.provider.WmqMessagingProvider`` をコンポーネント定義に追加する。
2. ``1`` で設定した、 ``WmqMessagingProvider`` を :ref:`messaging_context_handler` に設定する。


以下に設定例を示す。

.. code-block:: xml

  <!-- IBM WebSphere MQアダプタ用のプロバイダ実装 -->
  <component name="wmqMessagingProvider"
      class="nablarch.integration.messaging.wmq.provider.WmqMessagingProvider">
    <!-- 設定値はJavadocを参照 -->
  </component>

  <!--
  メッセージコンテキスト管理ハンドラ

  上で定義したWmqMessagingProviderを、messagingProviderプロパティに設定する。
  -->
  <component class="nablarch.fw.messaging.handler.MessagingContextHandler">
    <property name="messagingProvider" ref="wmqMessagingProvider" />
  </component>

分散トランザクションを利用する
--------------------------------------------------
本アダプタには、IBM WebSphere MQをトランザクションマネージャとして、分散トランザクションを実現する機能が含まれている。

この機能は、外部システムとメッセージの送受信を行う際に、取り込み漏れや2重取り込みを防止する目的で利用する。

分散トランザクションを利用するための手順を以下に示す。

1. 分散トランザクションに対応したデータソース( :java:extdoc:`javax.sql.XADataSource` を実装したクラス)を定義する。

2. 分散トランザクションに対応したデータベース接続を生成するファクトリクラスを定義する。 |br|
   (``nablarch.integration.messaging.wmq.xa.WmqXADbConnectionFactoryForXADataSource`` を定義する。)

3. ``2`` で定義したファクトリクラスを、 :ref:`database_connection_management_handler` に設定する。

4. 分散トランザクション用のトランザクションのオブジェクトを生成するファクトリクラスを定義する。 |br|
   (``nablarch.integration.messaging.wmq.xa.WmqXATransactionFactory`` を定義する。)

5. ``4`` で定義したファクトリクラスを :ref:`transaction_management_handler` に設定する。

以下に設定例を示す。

.. code-block:: xml

  <!--
  XA用のデータソースの設定
  使用するデータベース製品のJDBC実装内のXA用のデータソースを設定する。

  この例では、Oracleデータベース用の設定となる。
  -->
  <component name="xaDataSource" class="oracle.jdbc.xa.client.OracleXADataSource">
    <!-- プロパティへの設定は省略 -->
  </component>

  <!-- XA用のデータベース接続を生成するクラスの設定-->
  <component name="xaConnectionFactory"
      class="nablarch.integration.messaging.wmq.xa.WmqXADbConnectionFactoryForXADataSource">

    <!-- xaDataSourceプロパティにXA用のデータソースを設定する。-->
    <property name="xaDataSource" ref="xaDataSource" />

    <!-- 上記以外のプロパティは省略 -->
  </component>

  <!-- 分散トランザクション用のDB接続ハンドラの設定 -->
  <component class="nablarch.common.handler.DbConnectionManagementHandler">
    <!-- DB接続ファクトリには、上記で設定したXA用のデータベース接続を生成するクラスを設定する。 -->
    <property name="connectionFactory" ref="xaConnectionFactory" />

    <!-- 上記以外のプロパティは省略 -->
  </component>

  <!-- XA用のトランザクション制御オブジェクトを生成するクラスの設定 -->
  <component name="xaTransactionFactory"
      class="nablarch.integration.messaging.wmq.xa.WmqXATransactionFactory" />

  <!-- 分散トランザクション用のトランザクションハンドラの設定 -->
  <component class="nablarch.common.handler.TransactionManagementHandler">
    <!-- トランザクションファクトリには、上記で設定した
    XA用のトランザクション制御オブジェクトを生成するクラスを設定する。
    -->
    <property name="transactionFactory" ref="xaTransactionFactory" />

    <!-- 上記以外のプロパティは省略 -->
  </component>

.. important::

  分散トランザクションを使用するためには、WebSphere MQに対するXA リソース・マネージャーの設定や、データベースに対する権限付与が必要となる。
  詳細な設定方法や必要な権限などは、使用する製品のマニュアルを参照すること。

.. |br| raw:: html

  <br />
