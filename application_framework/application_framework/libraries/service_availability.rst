.. _`service_availability`:

サービス提供可否チェック
=====================================================================

.. contents:: 目次
  :depth: 3
  :local:

この機能では、アプリケーションが提供する機能に対して、サービス提供可否をチェックする。

この機能を使うことで、以下のようなことが実現できる。

* ウェブにおいて一部機能へのアクセスを遮断し、503エラーを返す。
* 常駐バッチにおいて、空回り(処理せずに待機する状態)を行う。

.. important::
 本機能は、アプリケーションの要件が合致する場合に限り、使用すること。
 本機能は、データベースを使用してサービス提供可否の状態を管理し、
 リクエスト単位でサービス提供可否を設定する( :ref:`service_availability-settings` を参照)。
 例えば、ウェブの登録機能といった場合、初期表示/確認/戻る/登録といった複数リクエストで構成されるのが一般的である。
 そのため、本機能は、細かくサービス提供可否を設定できる反面、非常に細かいデータ設計が必要となり、
 開発時の生産性低下やリリース後の運用負荷が高まる可能性がある。

機能概要
---------------------------------------------------------------------

リクエスト単位でサービス提供可否をチェックすることができる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`ServiceAvailabilityCheckHandler` をハンドラキューに設定することで、
ウェブでも常駐バッチでも、リクエスト単位でサービス提供可否をチェックすることができるようになる。
この機能は、ウェブや常駐バッチといった処理方式に依存しない。

詳細は以下を参照。

* :ref:`service_availability-settings`
* :ref:`service_availability-check`
* :ref:`service_availability-view_control`

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-auth</artifactId>
  </dependency>
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-auth-jdbc</artifactId>
  </dependency>

使用方法
---------------------------------------------------------------------

.. _`service_availability-settings`:

サービス提供可否チェックを使うための設定を行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
この機能では、データベースを使用してサービス提供可否の状態を管理する。
テーブルのレイアウトは以下となる。

====================== ===================================================
リクエストID(PK)       リクエストを識別するための値。文字列型
サービス提供可否状態   可の場合は"1"。文字列型。設定で値を変更できる。
====================== ===================================================

サービス提供可否チェックを使うためには、
:java:extdoc:`BasicServiceAvailability <nablarch.common.availability.BasicServiceAvailability>` の設定をコンポーネント定義に追加する。
コンポーネント名には **serviceAvailability** と指定する。

.. code-block:: xml

 <component name="serviceAvailability" class="nablarch.common.availability.BasicServiceAvailability">
   <!-- テーブル名 -->
   <property name="tableName" value="REQUEST"/>
   <!-- リクエストIDのカラム名 -->
   <property name="requestTableRequestIdColumnName" value="REQUEST_ID"/>
   <!-- サービス提供可否状態のカラム名 -->
   <property name="requestTableServiceAvailableColumnName" value="SERVICE_AVAILABLE"/>
   <!-- サービス提供可を示す値 -->
   <property name="requestTableServiceAvailableOkStatus" value="1"/>
   <!-- データベースアクセスに使用するトランザクションマネージャ -->
   <property name="dbManager" ref="serviceAvailabilityDbManager"/>
 </component>

.. _`service_availability-check`:

サービス提供可否をチェックする
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
サービス提供可否チェックは、 :java:extdoc:`ServiceAvailabilityUtil <nablarch.common.availability.ServiceAvailabilityUtil>` を使用する。

.. _`service_availability-view_control`:

サービス提供可否に応じて画面表示を制御する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
サービス提供可否に応じてボタンやリンクの非表示(非活性)を制御したい場合は、カスタムタグを使用する。
:ref:`tag-submit_display_control` を参照。

拡張例
---------------------------------------------------------------------
なし。
