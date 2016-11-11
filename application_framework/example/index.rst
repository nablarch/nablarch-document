.. _`example_application`:

Example
==========================================

本章では、Nablarchアプリケーションフレームワークを利用して作成したExampleアプリケーションに必要な環境構築手順と、アプリケーションの実行手順を解説する。


環境構築手順について
------------------------------------------
Exampleアプリケーションは、Apache Mavenを利用してアプリケーションのビルド、実行を行う。以下のページを参考に、Apache MavenのPCへのインストール及び必要な設定を行うこと。

:ref:`maven`


アプリケーションの実行手順について
--------------------------------------------------

Exampleアプリケーションの実行手順は、各ExampleアプリケーションのgithubのREADMEを参照すること。

  ウェブアプリケーション
    https://github.com/nablarch/nablarch-example-web


  ウェブサービス
   \

   RESTfulウェブサービス
    https://github.com/nablarch/nablarch-example-rest

   HTTPメッセージング
    送信
     https://github.com/nablarch/nablarch-example-http-messaging-send
    受信
     https://github.com/nablarch/nablarch-example-http-messaging

  バッチアプリケーション
   \

   JSR352に準拠したバッチアプリケーション
    https://github.com/nablarch/nablarch-example-batch-ee

   Nablarchバッチアプリケーション
    https://github.com/nablarch/nablarch-example-batch

  メッセージング
   \

   MOMによるメッセージング
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



   テーブルをキューとして使ったメッセージング
    https://github.com/nablarch/nablarch-example-db-queue
