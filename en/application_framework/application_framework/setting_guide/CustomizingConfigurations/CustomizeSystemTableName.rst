=======================================================
Procedure to rename a table used by Nablarch framework
=======================================================

-----------
Summary
-----------

We will describe how to change the names of tables used by the Nablarch framework for permission checks, etc.,
if the names do not conform to the naming conventions or if you want to qualify the schema.

--------------
How to Change
--------------

The following are the examples of blank projects generated from each archetype provided by Nablarch, where the table name used by the Nablarch framework is uniformly changed to "T_Table name".

Add table configuration required for the function used by a project in src/main/resources/common.properties. The necessary configuration and the configuration examples for each function are described below:

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


In the case of web applications, also change the table name used for the session store. (Define the components if they are not defined in the application.)

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
