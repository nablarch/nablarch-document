.. _`example_application`:

=======
Example
=======

Exampleアプリケーションは、Nablarchアプリケーションフレームワークの機能の使用方法を示した実装例であり、 :ref:`実行制御基盤 <runtime_platform>` 毎に作成している。
本章では、Exampleアプリケーションに必要な環境構築手順と、アプリケーションの実行手順を解説する。

.. tip::
 Exampleを改修して本格的なアプリケーションを作成することは想定していない。
 
 本格的なアプリケーションを作成する場合は :ref:`blank_project` から作成すること。


環境構築手順について
==========================================
Exampleアプリケーションは、Apache Mavenを使用してアプリケーションをビルド、実行する。以下のページを参考に、ApacheMavenのPCへのインストール及び必要な設定を行うこと。

:ref:`maven`


アプリケーションの実行手順について
==================================================

Exampleアプリケーションの実行手順は、各ExampleアプリケーションのgithubのREADMEを参照すること。
開発イメージを掴むためには、処理方式毎のGetting Startedを参照すると良い。

  ウェブアプリケーション
   \

    JSPとカスタムタグを使用したサンプル（ :ref:`Getting Started <getting_started>` ）
     https://github.com/nablarch/nablarch-example-web
    Thymeleafを使用したサンプル
     ※本サンプルについては、対応するGetting Startedを用意していない
     https://github.com/nablarch/nablarch-example-thymeleaf-web


  ウェブサービス
   \

   RESTfulウェブサービス（ :ref:`Getting Started <rest_getting_started>` ）
    https://github.com/nablarch/nablarch-example-rest

   HTTPメッセージング（ :ref:`Getting Started <http-messaging_getting_started>` ）
    送信
     https://github.com/nablarch/nablarch-example-http-messaging-send
    受信
     https://github.com/nablarch/nablarch-example-http-messaging

  バッチアプリケーション
   \

   Jakarta Batchに準拠したバッチアプリケーション（ :ref:`Getting Started <jBatch_getting_started>` ）
    https://github.com/nablarch/nablarch-example-batch-ee

   Nablarchバッチアプリケーション（ :ref:`Getting Started <nablarch_Batch_getting_started>` ）
    https://github.com/nablarch/nablarch-example-batch

  メッセージング
   \

   MOMによるメッセージング（ :ref:`Getting Started <mom_messaging_getting_started>` ）
    \

    .. _`example_application-mom_system_messaging-async_message_send`:

    応答不要メッセージ送信
     https://github.com/nablarch/nablarch-example-mom-delayed-send

    .. _`example_application-mom_system_messaging-sync_message_send`:

    同期応答メッセージ送信
     https://github.com/nablarch/nablarch-example-mom-sync-send-batch

    .. _`example_application-mom_system_messaging-async_message_receive`:

    応答不要メッセージ受信
     https://github.com/nablarch/nablarch-example-mom-delayed-receive

    .. _`example_application-mom_system_messaging-sync_message_receive`:

    同期応答メッセージ受信
     https://github.com/nablarch/nablarch-example-mom-sync-receive

   テーブルをキューとして使ったメッセージング（ :ref:`Getting Started <db_messaging_getting_started>` ）
    https://github.com/nablarch/nablarch-example-db-queue


Java 21 で動かす場合について
==================================================

ExampleはJava 17での実行を前提としている。
Java 21で動かす場合は、個別にセットアップが必要となる。
詳細は、以下のブランクプロジェクトの説明を参照のこと。

* :ref:`setup_blank_project_for_Java21`
