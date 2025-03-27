.. _`platform`:

稼動環境
====================================

.. contents:: 目次
   :depth: 3
   :local:

Nablarchフレームワークの稼動環境について説明する。

.. tip::
 Nablarchフレームワーク以外のコンテンツ(例えばNablarch SQL Executorなど)に関する稼動環境は、
 各コンテンツのドキュメントを参照。

Nablarchフレームワークの環境要件
-----------------------------------------------------
Nablarchフレームワークは、Java標準仕様のみを使って作成しており、動かすには最低以下が必要となる。

* Java SE 17
* JDBC 3.0

さらに、使用するNablarchの機能に応じて、以下のJakarta EE仕様が必要となる。

* Jakarta Standard Tag Library 3.0
* Jakarta Activation 2.1
* Jakarta Server Pages 3.1
* Jakarta Servlet 6.0
* Jakarta Mail 2.1
* Jakarta Messaging 3.1
* Jakarta Persistence 3.1
* Jakarta Batch 2.1
* Jakarta Bean Validation 3.0
* Jakarta RESTful Web Services 3.1

.. important::
 ここで示したバージョン番号は、特定バージョンを表記しているが、
 基本的に表記しているバージョン番号以上と読み替えて問題ない。
 Java標準仕様とJakarta EE仕様のバージョンアップで、基本的に後方互換が維持されるため。

Nablarchフレームワークのテスト環境
-----------------------------------------------------
Nablarchフレームワークは、以下の環境においてテストを実施し、正常に動作することを確認している。

Java
 * Java SE 17/21 [#java21]_

データベース
 * Oracle Database 19c/21c/23ai
 * IBM Db2 11.5/12.1
 * SQL Server 2017/2019/2022
 * PostgreSQL 12.2/13.2/14.0/15.2/16.2/17.4

アプリケーションサーバ
 * WebSphere Application Server Liberty 25.0.0.2
 * Open Liberty 25.0.0.2
 * Red Hat JBoss Enterprise Application Platform 8.0.0
 * WildFly 35.0.1.Final
 * Apache Tomcat 10.1.17

Jakarta EE
 * Hibernate Validator 8.0.0.Final
 * JBeret 2.1.1.Final

MOM（メッセージ指向ミドルウェア）
 * IBM MQ 9.3

ブラウザ
 PC
  * Microsoft Edge
  * Mozilla Firefox
  * Google Chrome
  * Safari

.. [#java21] Java21で使用する場合、別途設定変更が必要となる。設定方法は :doc:`../blank_project/setup_blankProject/setup_Java21` を参照。
