====================================================
Nablarchフレームワークが使用するテーブル名の変更手順
====================================================

-----------
概要
-----------

Nablarchフレームワークが認可チェックなどで使用するテーブル名が命名規約にそぐわなかったり、
スキーマ修飾したい場合に変更する手順を記述する。

-----------
変更方法
-----------

以下、Nablarchが提供する各アーキタイプから生成したブランクプロジェクトで、Nablarchフレームワークが使用するテーブル名を一律「T_テーブル名」に変更する場合の例である。

src/main/resources/common.configに、プロジェクトが使用する機能に必要なテーブルの設定を追加する。各機能に対して必要な設定と設定例を以下に記載する。

 .. code-block:: properties
    
    # 日付管理
    nablarch.businessDateTable.tableName=T_BUSINESS_DATE
    
    # コード管理
    nablarch.codeNameTable.name=T_CODE_NAME
    nablarch.codePatternTable.name=T_CODE_PATTERN
    
    # 自動採番
    nablarch.idGeneratorTable.tableName=T_ID_GENERATE
    
    # メール送信
    nablarch.mailAttachedFileTable.tableName=T_MAIL_ATTACHED_FILE
    nablarch.mailRecipientTable.tableName=T_MAIL_RECIPIENT
    nablarch.mailRequestTable.tableName=T_MAIL_REQUEST
    nablarch.mailTemplateTable.tableName=T_MAIL_TEMPLATE
    
    # メッセージ管理（データベースで管理時）
    nablarch.messageTable.tableName=T_MESSAGE
    
    # サービス提供可否チェック
    # (nablarch.batchRequestTable.nameはプロセス多重起動防止、プロセス停止制御でも使用する。)
    nablarch.requestTable.name=T_REQUEST
    nablarch.batchRequestTable.name=T_BATCH_REQUEST
    
    # 認可チェック
    nablarch.permissionUnitTable.name=T_PERMISSION_UNIT
    nablarch.permissionUnitRequestTable.name=T_PERMISSION_UNIT_REQUEST
    nablarch.systemAccountTable.name=T_SYSTEM_ACCOUNT
    nablarch.systemAccountAuthorityTable.name=T_SYSTEM_ACCOUNT_AUTHORITY
    nablarch.ugroupTable.name=T_UGROUP
    nablarch.ugroupAuthorityTable.name=T_UGROUP_AUTHORITY
    nablarch.ugroupSystemAccountTable.name=T_UGROUP_SYSTEM_ACCOUNT


ウェブアプリケーションの場合、セッションストアに使用するテーブル名も変更する。（アプリケーションでコンポーネント定義していない場合は定義する。）

 .. code-block:: xml

  <component class="nablarch.common.web.session.store.DbStore">
    <property name="userSessionSchema">
      <component class="nablarch.common.web.session.store.UserSessionSchema">
        <property name="tableName" value="T_USER_SESSION" />
        <property name="sessionIdName" value="SESSION_ID" />
        <property name="sessionObjectName" value="SESSION_OBJECT" />
        <property name="expirationDatetimeName" value="EXPIRATION_DATETIME" />
      </component>
    </property>
  </component>
