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

    JSPとカスタムタグを使用したサンプル
     https://github.com/nablarch/nablarch-example-web

     このExampleを使用したGetting Startedは :ref:`こちら <getting_started>`

    Thymeleafを使用したサンプル
     https://github.com/nablarch/nablarch-example-thymeleaf-web

     ※本サンプルについては、対応するGetting Startedを用意していない

  ウェブサービス
   \

   RESTfulウェブサービス
    https://github.com/nablarch/nablarch-example-rest

    このExampleを使用したGetting Startedは :ref:`こちら <rest_getting_started>`

   HTTPメッセージング

    送信
     https://github.com/nablarch/nablarch-example-http-messaging-send

     ※本サンプルについては、対応するGetting Startedを用意していない

    受信
     https://github.com/nablarch/nablarch-example-http-messaging

     このExampleを使用したGetting Startedは :ref:`こちら <http-messaging_getting_started>`

  バッチアプリケーション
   \

   Jakarta Batchに準拠したバッチアプリケーション
    https://github.com/nablarch/nablarch-example-batch-ee

    このExampleを使用したGetting Startedは :ref:`こちら <jBatch_getting_started>`

   Nablarchバッチアプリケーション
    https://github.com/nablarch/nablarch-example-batch

    このExampleを使用したGetting Startedは :ref:`こちら <nablarch_Batch_getting_started>`

  メッセージング
   \

   MOMによるメッセージング
    \

    ※MOMによるメッセージングでは、個別のGetting Startedを用意していない。
    :ref:`mom_system_messaging` ライブラリの機能説明でExampleアプリケーションを使用しているため、そちらを参照すると良い。
   
    .. _`example_application-mom_system_messaging-async_message_send`:

    応答不要メッセージ送信
     https://github.com/nablarch/nablarch-example-mom-delayed-send

     このExampleで実装されている機能の説明は :ref:`こちら <mom_system_messaging-async_message_send>`

    .. _`example_application-mom_system_messaging-sync_message_send`:

    同期応答メッセージ送信
     https://github.com/nablarch/nablarch-example-mom-sync-send-batch

     このExampleで実装されている機能の説明は :ref:`こちら <mom_system_messaging-sync_message_send>`

    .. _`example_application-mom_system_messaging-async_message_receive`:

    応答不要メッセージ受信
     https://github.com/nablarch/nablarch-example-mom-delayed-receive

     このExampleで実装されている機能の説明は :ref:`こちら <mom_system_messaging-async_message_receive>`

    .. _`example_application-mom_system_messaging-sync_message_receive`:

    同期応答メッセージ受信
     https://github.com/nablarch/nablarch-example-mom-sync-receive

     このExampleで実装されている機能の説明は :ref:`こちら <mom_system_messaging-sync_message_receive>`

   テーブルをキューとして使ったメッセージング
    https://github.com/nablarch/nablarch-example-db-queue

    このExampleを使用したGetting Startedは :ref:`こちら <db_messaging_getting_started>`


Java 21 で動かす場合について
==================================================

ExampleはJava 17での実行を前提としている。
Java 21で動かす場合は、個別にセットアップが必要となる。
詳細は、以下のブランクプロジェクトの説明を参照のこと。

* :ref:`setup_blank_project_for_Java21`
