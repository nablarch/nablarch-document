.. _`permission_check`:

認可チェック
=====================================================================

.. contents:: 目次
  :depth: 3
  :local:

この機能では、アプリケーションが提供する機能に対して、認可チェックを行う。
この機能を使うことで、ウェブにおいてユーザごとに使用できる機能を制限する、
といったアクセス制御ができるようになる。

.. important::
 本機能は、アプリケーションの要件が合致する場合に限り、使用すること。

 本機能は、データベースを使用して認可チェックに使用する権限データを管理し、
 リクエスト単位で権限を設定する( :ref:`permission_check-authority_model` に示した概念モデルを参照)。
 例えば、ウェブの登録機能といった場合、初期表示/確認/戻る/登録といった複数リクエストで構成されるのが一般的である。

 そのため、本機能は、細かく権限を設定できる反面、非常に細かいデータ設計が必要となり、
 開発時の生産性低下やリリース後の運用負荷が高まる可能性がある。

機能概要
---------------------------------------------------------------------

リクエスト単位で認可チェックを行うことができる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`permission_check_handler` をハンドラキューに設定することで、
リクエスト単位で認可チェックを行うことができる。

詳細は以下を参照。

* :ref:`permission_check-settings`
* :ref:`permission_check-server_side_check`
* :ref:`permission_check-view_control`

.. _`permission_check-authority_model`:

グループ単位とユーザ単位を併用した権限設定ができる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
認可チェックに使う権限設定の概念モデルは以下となる。

.. image:: images/permission_check/conceptual_model.png

グループは、部署など、組織単位での権限割り当てに使用する。

認可チェック単位は、複数のリクエストをまとめ、認可チェックの最小単位を表す。
認可チェック単位には、認可チェックを実現するために必要なリクエスト、つまり、ウェブであれば画面のイベントが複数紐付く。
例えば、ユーザ登録機能であれば、以下のようなデータとなる。

認可チェック単位
 | ユーザ登録

認可チェック単位「ユーザ登録」に紐付くリクエスト
 | 入力画面の初期表示
 | 入力画面の確認ボタン
 | 確認画面の登録ボタン
 | 確認画面の戻るボタン

グループとユーザ、グループと認可チェック単位の関連を設定することで、グループ単位の権限を設定することができる。
さらに、ユーザに直接認可チェック単位を設定することもできるため、特定ユーザに対するイレギュラーな権限付与に対応することができる。

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

.. _`permission_check-settings`:

認可チェックを使うための設定を行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
この機能では、データベースを使用して認可チェックに使う権限データを管理する。
テーブルのレイアウトは以下となる。

グループ
 ====================== ===================================================
 グループID(PK)         グループを識別するための値。文字列型
 ====================== ===================================================

システムアカウント
 ====================== ===================================================
 ユーザID(PK)           ユーザを識別するための値。文字列型
 ユーザIDロック状態     ユーザIDのロック状態。文字列型。
 有効日(From)           ユーザの有効日(From)。文字列型。
 有効日(To)             ユーザの有効日(To)。文字列型。
 ====================== ===================================================

 :ユーザIDロック状態: ロックされていない場合は"0"、ロックされた場合は"0"以外
 :有効日(From): yyyyMMdd形式で、指定しない場合は”19000101”
 :有効日(To): yyyyMMdd形式で、指定しない場合は”99991231”

グループシステムアカウント
 ====================== ===================================================
 グループID(PK)         グループを識別するための値。文字列型
 ユーザID(PK)           ユーザを識別するための値。文字列型
 有効日(From)(PK)       ユーザの有効日(From)。文字列型
 有効日(To)             ユーザの有効日(To)。文字列型
 ====================== ===================================================

 :有効日(From): yyyyMMdd形式で、指定しない場合は”19000101”
 :有効日(To): yyyyMMdd形式で、指定しない場合は”99991231”

認可チェック単位
 ====================== ===================================================
 認可チェック単位ID(PK)         認可チェック単位を識別するための値。文字列型
 ====================== ===================================================

認可チェック単位リクエスト
 ====================== ===================================================
 認可チェック単位ID(PK)         認可チェック単位を識別するための値。文字列型
 リクエストID(PK)       リクエストを識別するための値。文字列型
 ====================== ===================================================

グループ権限
 ====================== ===================================================
 グループID(PK)         グループを識別するための値。文字列型
 認可チェック単位ID(PK)         認可チェック単位を識別するための値。文字列型
 ====================== ===================================================

システムアカウント権限
 ====================== ===================================================
 ユーザID(PK)           ユーザを識別するための値。文字列型
 認可チェック単位ID(PK)         認可チェック単位を識別するための値。文字列型
 ====================== ===================================================

認可チェックを使うためには、以下の設定を行う。

* :java:extdoc:`BasicPermissionFactory <nablarch.common.permission.BasicPermissionFactory>`
  の設定をコンポーネント定義に追加する。
* :java:extdoc:`BasicPermissionFactory <nablarch.common.permission.BasicPermissionFactory>` は、
  :ref:`permission_check_handler` に設定して使うので、コンポーネント名は任意の名前を指定する。

.. code-block:: xml

 <component name="permissionFactory" class="nablarch.common.permission.BasicPermissionFactory">

   <!-- グループスキーマ -->
   <property name="groupTableSchema">
     <component class="nablarch.common.permission.schema.GroupTableSchema">
       <!-- プロパティへの設定は省略 -->
     </component>
   </property>

   <!-- システムアカウントスキーマ -->
   <property name="systemAccountTableSchema">
     <component class="nablarch.common.permission.schema.SystemAccountTableSchema">
       <!-- プロパティへの設定は省略 -->
     </component>
   </property>

   <!-- グループシステムアカウントスキーマ -->
   <property name="groupSystemAccountTableSchema">
     <component class="nablarch.common.permission.schema.GroupSystemAccountTableSchema">
       <!-- プロパティへの設定は省略 -->
     </component>
   </property>

   <!-- 認可チェック単位スキーマ -->
   <property name="permissionUnitTableSchema">
     <component class="nablarch.common.permission.schema.PermissionUnitTableSchema">
       <!-- プロパティへの設定は省略 -->
     </component>
   </property>

   <!-- 認可チェック単位リクエストスキーマ -->
   <property name="permissionUnitRequestTableSchema">
     <component class="nablarch.common.permission.schema.PermissionUnitRequestTableSchema">
       <!-- プロパティへの設定は省略 -->
     </component>
   </property>

   <!-- グループ権限スキーマ -->
   <property name="groupAuthorityTableSchema">
     <component class="nablarch.common.permission.schema.GroupAuthorityTableSchema">
       <!-- プロパティへの設定は省略 -->
     </component>
   </property>

   <!-- システムアカウント権限スキーマ -->
   <property name="systemAccountAuthorityTableSchema">
     <component class="nablarch.common.permission.schema.SystemAccountAuthorityTableSchema">
       <!-- プロパティへの設定は省略 -->
     </component>
   </property>

   <!-- データベースアクセスに使用するトランザクションマネージャ -->
   <property name="dbManager" ref="permissionCheckDbManager"/>

   <!-- 有効日(FROM/TO)の判定に使用する業務日付を提供するプロバイダ -->
   <property name="businessDateProvider" ref="businessDateProvider" />
 </component>

:java:extdoc:`BasicPermissionFactory <nablarch.common.permission.BasicPermissionFactory>` は、
初期化が必要なので、以下のコンポーネント定義も追加する。

.. code-block:: xml

 <component name="initializer"
            class="nablarch.core.repository.initialization.BasicApplicationInitializer">
   <property name="initializeList">
     <list>
       <!-- BasicPermissionFactoryを初期化する -->
       <component-ref name="permissionFactory" />
     </list>
   </property>
 </component>

.. _`permission_check-server_side_check`:

サーバサイドで認可チェックを行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
認可チェックは、 :java:extdoc:`Permission <nablarch.common.permission.Permission>` を使用する。
:ref:`permission_check_handler` により、スレッドコンテキストに
:java:extdoc:`Permission <nablarch.common.permission.Permission>` が設定されているので、
:java:extdoc:`PermissionUtil.getPermission <nablarch.common.permission.PermissionUtil.getPermission()>`
を使って取得する。

.. code-block:: java

 Permission permission = PermissionUtil.getPermission();
 if (permission.permit("/action/user/unlock")) {
     // 認可チェックがOKの場合の処理がここにくる
 }

.. _`permission_check-view_control`:

権限に応じて画面表示を制御する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
権限の有無でボタンやリンクの非表示(非活性)を制御したい場合は、カスタムタグを使用する。
:ref:`tag-submit_display_control` を参照。

権限データにアクセスする
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
アプリケーションの要件によっては、特定グループに属するユーザ一覧を取得するといった、
権限データにアクセスしたい場合がある。
しかし、本機能では、認可チェックを行う機能しか提供していない。

そのため、権限データにアクセスしたい場合は、 :ref:`universal_dao` を使用し、
SQLを作成することで対応する。

拡張例
---------------------------------------------------------------------
なし。
