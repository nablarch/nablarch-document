.. _`example_application`:

=======
Example
=======

Exampleは、Nablarchアプリケーションフレームワークの機能の使用方法を示した実装例であり、 :ref:`実行制御基盤 <runtime_platform>` 毎に作成している。
本章では、Exampleに必要な環境構築手順と、アプリケーションの実行手順を解説する。

.. tip::
 Exampleを改修して本格的なアプリケーションを作成することは想定していない。
 
 本格的なアプリケーションを作成する場合は :ref:`blank_project` から作成すること。


Exampleの実行方法
=================

環境構築手順
------------

Exampleは、Apache Mavenを使用してアプリケーションをビルド、実行する。以下のページを参考に、ApacheMavenのPCへのインストール及び必要な設定を行うこと。

:ref:`maven`

実行手順
--------

Exampleの実行手順は、各ExampleのGitHubリポジトリトップにあるREADMEを参照すること。


Java 11 以上で動かす場合
----------------------------

ExampleはJava 8での実行を前提としている。
Java 11以上で動かす場合は、依存ライブラリの修正が必要となる。
詳細は、以下のブランクプロジェクトの説明を参照のこと。

* :ref:`setup_blank_project_for_Java11`
* :ref:`setup_blank_project_for_Java17`
* :ref:`setup_blank_project_for_Java21`


Exampleの一覧
=============

実行制御基盤毎のExampleを以下に示す。実装の解説も用意しているので、必要に応じて、以下一覧の「解説」リンクより参照すること。

ウェブアプリケーション
----------------------

- `ウェブアプリケーション (JSP) <https://github.com/nablarch/nablarch-example-web>`_ (:ref:`解説 <getting_started>`)
- `ウェブアプリケーション (Thymeleaf) <https://github.com/nablarch/nablarch-example-thymeleaf-web>`_ (:ref:`解説 <web_thymeleaf_adaptor>`)


ウェブサービス
--------------

- `RESTfulウェブサービス <https://github.com/nablarch/nablarch-example-rest>`_ (:ref:`解説 <rest_getting_started>`)
- `HTTPメッセージング (受信) <https://github.com/nablarch/nablarch-example-http-messaging>`_ (:ref:`解説 <http-messaging_getting_started>`)
- `HTTPメッセージング (送信) <https://github.com/nablarch/nablarch-example-http-messaging-send>`_ (:ref:`解説 <http_system_messaging-message_send>`)


バッチアプリケーション
----------------------
  
- `JSR352に準拠したバッチアプリケーション <https://github.com/nablarch/nablarch-example-batch-ee>`_ (:ref:`解説 <jBatch_getting_started>`)
- `Nablarchバッチアプリケーション <https://github.com/nablarch/nablarch-example-batch>`_ (:ref:`解説 <nablarch_Batch_getting_started>`)


メッセージング
--------------

.. _`example_application-mom_system_messaging`:

- MOMによるメッセージング (:ref:`解説 <mom_messaging_getting_started>`)

  - `応答不要メッセージ送信 <https://github.com/nablarch/nablarch-example-mom-delayed-send>`_
  - `同期応答メッセージ送信 <https://github.com/nablarch/nablarch-example-mom-sync-send-batch>`_
  - `応答不要メッセージ受信 <https://github.com/nablarch/nablarch-example-mom-delayed-receive>`_
  - `同期応答メッセージ受信 <https://github.com/nablarch/nablarch-example-mom-sync-receive>`_

- `テーブルをキューとして使ったメッセージング <https://github.com/nablarch/nablarch-example-db-queue>`_ (:ref:`解説 <db_messaging_getting_started>`)
