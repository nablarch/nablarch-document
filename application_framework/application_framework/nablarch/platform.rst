.. _`platform`:

稼動環境
====================================

.. contents:: 目次
   :depth: 3
   :local:

Nablarchフレームワークの稼動環境について説明する。

.. tip::
 Nablarchフレームワーク以外のコンテンツ(例えばUI開発基盤など)に関する稼動環境は、
 各コンテンツのドキュメントを参照。

Nablarchフレームワークの環境要件
-----------------------------------------------------
Nablarchフレームワークは、Java標準仕様のみを使って作成しており、動かすには最低以下が必要となる。

* Java SE 6
* JDBC 3.0

さらに、使用するNablarchの機能に応じて、以下のJava標準仕様が必要となる。

* JavaServer Pages Standard Tag Library 1.1
* JavaBeans Activation Framework 1.1
* JavaServer Pages 2.1
* Java Servlet 2.5
* Java API for XML-Based Web Services (JAX-WS) 2.0
* JavaMail API 1.4
* Java Message Service API 1.1-rev-1
* Java Persistence 2.0
* Batch Applications for the Java Platform 1.0
* Bean Validation 1.1
* Java API for RESTful Web Services (JAX-RS) 2.0

.. important::
 ここで示したバージョン番号は、特定バージョンを表記しているが、
 基本的に表記しているバージョン番号以上と読み替えて問題ない。
 Java標準仕様のバージョンアップで、基本的に後方互換が維持されるため。

Nablarchフレームワークのテスト環境
-----------------------------------------------------
Nablarchフレームワークは、以下の環境においてテストを実施し、正常に動作することを確認している。

Java
 * Java SE 6/7/8

データベース
 * Oracle Database 12c
 * DB2 10
 * SQLServer 2008
 * PostgreSQL 9

アプリケーションサーバ
 * Oracle Weblogic Server 12c
 * WebSphere Application Server 7
 * JBoss Application Server 7
 * Apache Tomcat 6/7

Java EE
 * Hibernate Validator 5.1.3.Final
 * JBeret 1.2

MOM（メッセージ指向ミドルウェア）
 * WebSphere MQ 7

ブラウザ
 PC
  * Internet Explorer 6/7/8/9/10/11
  * Microsoft Edge 12
  * Mozilla Firefox
  * Google Chrome
  * Safari
 スマートフォン
  * iOS Safari
  * Android Browser 4.3

Nablarchフレームワークの稼動実績
-----------------------------------------------------
2016年2月時点の稼働実績を以下に示す。

OS
 * RedHat Enterprise Linux 5/6
 * WindowsServer 2008
 * AIX 7

Java
 * Java SE 6/7/8

データベース
 * Oracle Database 11g/12c
 * DB2 10
 * SQLServer 2008
 * PostgreSQL 9

アプリケーションサーバ
 * Oracle Weblogic Server 11g/12c
 * WebSphere Application Server 7/8
 * JBoss Application Server 7
 * Apache Tomcat 6/7/8

MOM（メッセージ指向ミドルウェア）
 * WebSphere MQ 7
