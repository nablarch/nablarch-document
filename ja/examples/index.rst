.. _`example_application`:

=======
Example
=======

Exampleアプリケーションは、Nablarchアプリケーションフレームワークの機能の使用方法を示した実装例であり、 :ref:`実行制御基盤 <runtime_platform>` 毎に作成している。
本章では、Exampleアプリケーションに必要な環境構築手順と、アプリケーションの実行手順を解説する。

.. tip::
 Exampleを改修して本格的なアプリケーションを作成することは想定していない。
 
 本格的なアプリケーションを作成する場合は :ref:`blank_project` から作成すること。


Exampleの実行方法
=================

環境構築手順
------------

Exampleアプリケーションは、Apache Mavenを使用してアプリケーションをビルド、実行する。以下のページを参考に、ApacheMavenのPCへのインストール及び必要な設定を行うこと。

:ref:`maven`

アプリケーションの実行手順
--------------------------

Exampleアプリケーションの実行手順は、各ExampleアプリケーションのgithubのREADMEを参照すること。

Java 21 で動かす場合
----------------------------

ExampleはJava 17での実行を前提としている。
Java 21で動かす場合は、個別にセットアップが必要となる。
詳細は、以下のブランクプロジェクトの説明を参照のこと。

:ref:`setup_blank_project_for_Java21`

Exampleの一覧
=============

ウェブアプリケーション
----------------------

:ref:`ウェブアプリケーション編の解説 <web_application>` 、 :ref:`Thymeleafアダプタの解説 <web_thymeleaf_adaptor>` も合わせて確認すること。

- `JSPとカスタムタグを使用したサンプル(外部サイト) <https://github.com/nablarch/nablarch-example-web>`_
- `Thymeleafを使用したサンプル(外部サイト) <https://github.com/nablarch/nablarch-example-thymeleaf-web>`_


ウェブサービス
--------------

RESTfulウェブサービス
~~~~~~~~~~~~~~~~~~~~~

:ref:`RESTfulウェブサービス編の解説 <restful_web_service>` も合わせて確認すること。

- `RESTfulウェブサービスのサンプル(外部サイト) <https://github.com/nablarch/nablarch-example-rest>`_

HTTPメッセージング
~~~~~~~~~~~~~~~~~~

:ref:`HTTPメッセージング編の解説 <http_messaging>` も合わせて確認すること。

- `HTTPメッセージングの送信側のサンプル(外部サイト) <https://github.com/nablarch/nablarch-example-http-messaging-send>`_
- `HTTPメッセージングの受信側のサンプル(外部サイト) <https://github.com/nablarch/nablarch-example-http-messaging>`_


バッチアプリケーション
----------------------
  
Jakarta Batchに準拠したバッチアプリケーション
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:ref:`Jakarta Batchに準拠したバッチアプリケーションの解説 <jsr352_batch>` も合わせて確認すること。

- `Jakarta Batchに準拠したバッチアプリケーションのサンプル(外部サイト) <https://github.com/nablarch/nablarch-example-batch-ee>`_

Nablarchバッチアプリケーション
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:ref:`Nablarchバッチアプリケーションの解説 <nablarch_batch>` も合わせて確認すること。

- `Nablarchバッチアプリケーションのサンプル(外部サイト) <https://github.com/nablarch/nablarch-example-batch>`_


メッセージング
--------------

MOMによるメッセージング
~~~~~~~~~~~~~~~~~~~~~~~

:ref:`MOMによるメッセージングの解説 <mom_messaging>` も合わせて確認すること。

.. _`example_application-mom_system_messaging-async_message_send`:

- `応答不要メッセージ送信のサンプル(外部サイト) <https://github.com/nablarch/nablarch-example-mom-delayed-send>`_

.. _`example_application-mom_system_messaging-sync_message_send`:

- `同期応答メッセージ送信のサンプル(外部サイト) <https://github.com/nablarch/nablarch-example-mom-sync-send-batch>`_

.. _`example_application-mom_system_messaging-async_message_receive`:

- `応答不要メッセージ受信のサンプル(外部サイト) <https://github.com/nablarch/nablarch-example-mom-delayed-receive>`_

.. _`example_application-mom_system_messaging-sync_message_receive`:

- `同期応答メッセージ受信のサンプル(外部サイト) <https://github.com/nablarch/nablarch-example-mom-sync-receive>`_

テーブルをキューとして使ったメッセージング
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:ref:`テーブルをキューとして使ったメッセージング <db_messaging>` も合わせて確認すること。

- `テーブルをキューとして使ったメッセージングのサンプル(外部サイト) <https://github.com/nablarch/nablarch-example-db-queue>`_
