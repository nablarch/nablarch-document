.. _request_unit_test_http_messaging:

リクエスト単体テスト（HTTPメッセージング）
==================================================

.. contents:: 目次
  :depth: 3
  :local:

機能概要
--------------------------------------------------

HTTPメッセージングのリクエスト単体テストは、\ MOM\ によるメッセージングのリクエスト単体テストと同じ枠組みで実施する。このページでは、\ MOM\ によるメッセージングとの差分だけを説明する。

HTTPメッセージ受信のリクエスト単体テストは、\ :ref:`リクエスト単体テスト（MOMによるメッセージング） <request_unit_test_mom>`\ の同期応答メッセージ受信と同じ方法で行う。HTTPメッセージ送信のリクエスト単体テストは、同ページの同期応答メッセージ送信と同じ方法で行う。

MOM\ によるメッセージングと記述方法が異なるのは、テストデータとコンポーネント設定である。テストデータの書き方は\ :ref:`テストショット一覧（testShots）を記述する <testdata_notation-test_shots>`\ と\ :ref:`メッセージングのデータを記述する <testdata_notation-messaging_data>`\ を、コンポーネント設定は\ :ref:`リクエスト単体テストの設定（HTTPメッセージング） <request_unit_test_setting_http_messaging>`\ を参照。

使用方法
--------------------------------------------------

:ref:`リクエスト単体テスト（MOMによるメッセージング） <request_unit_test_mom>`\ の手順をそのまま使う。HTTPメッセージングに固有の手順はない。

用語を読み替える
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`リクエスト単体テスト（MOMによるメッセージング） <request_unit_test_mom>`\ が同期応答メッセージ送信の説明で使う用語は、HTTPメッセージングでは次のとおり読み替える。

.. list-table::
  :class: white-space-normal
  :header-rows: 1
  :widths: 50,50

  * - MOM\ によるメッセージングでの用語
    - HTTPメッセージングでの用語
  * - 同期応答メッセージ送信
    - HTTPメッセージ送信
  * - 送信キュー・受信キュー
    - 通信先
  * - ``RequestTestingMessagingProvider``
    - ``RequestTestingMessagingClient``

ただし\ ``RequestTestingMessagingClient``\ は、\ ``RequestTestingMessagingProvider``\ と異なり内部クラスを持たない。要求電文のアサートと応答電文の返却は、同クラス自身が行う。
