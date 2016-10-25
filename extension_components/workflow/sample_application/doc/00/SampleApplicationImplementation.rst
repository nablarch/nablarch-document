==============================================
ワークフローライブラリの基本的な使用方法
==============================================

本章では、ワークフローライブラリの使用時に、あわせて業務データについても処理を行う必要がある場合について、
基本的な使用方法を記載する。

下記以外のAPIについては、「ワークフローライブラリ解説書」を参照すること。

.. _start_workflow:

-----------------------
ワークフローの開始
-----------------------
ワークフローは、 ``WorkflowManager#startInstance`` を呼び出すことで開始される。

ワークフローを開始するとワークフローインスタンスが返却されるので、
そのワークフローインスタンスを使用して担当者やグループの割り当てを行う。

このとき、ワークフローインスタンスを一意に識別するID(インスタンスID)が採番されるので、
以降のリクエストでもワークフローインスタンスを取得できるように業務データのテーブルにインスタンスIDを格納する。

**実装例(CM111001Component.java)**

以下は、ワークフローサンプルアプリケーションのワークフロー開始処理
（:ref:`ワークフロー定義 <trans_expence_appliance_definition>` の①に対応）のコードである。


.. code-block:: java

    /**
     * 交通費を申請する。<br/>
     * 申請IDは自動採番される。
     * 
     * @param entity 登録する交通費申請情報を設定したEntity
     * @param confirmUserId 確認者ユーザID
     * @param authorizeUserId 承認者ユーザID
     * @return 採番した交通費申請ID
     */
    public String applyTransExpense(TransExpeApplicationEntity entity, String confirmUserId, String authorizeUserId) {

        // ワークフローを開始する。
        WorkflowInstance workflow = WorkflowManager.startInstance(TRANS_EXPENSE_APPLICATION_WORKFLOW_ID);

        // ワークフローの各タスクに、担当ユーザを割り当てる。
        workflow.assignUser(CONFIRMATION_TASK, confirmUserId);
        workflow.assignUser(AUTHORIZATION_TASK, authorizeUserId);
        workflow.assignUser(REAPPLICATION_TASK, ThreadContext.getUserId());

        // 申請登録
        String applicationId = IdGeneratorUtil.generateTransExpeAppliId();
        entity.setTransExpeAppliId(applicationId);
        entity.setWfInstanceId(workflow.getInstanceId());
        entity.setTransExpeAppliStatusCd(REGISTER_COMPLETE);
        ParameterizedSqlPStatement statement = getParameterizedSqlStatement("REGISTER_TRANS_EXPENCE_APPLICATION");
        statement.executeUpdateByObject(entity);

        // 履歴登録
        TransExpeAppliHistoryEntity historyEntity = new TransExpeAppliHistoryEntity();
        historyEntity.setTransExpeAppliId(applicationId);
        historyEntity.setTransExpeAppliActionCd(REGISTER);
        historyEntity.setTransExpeAppliResultCd(FORWARD_RESULT);
        registerHistory(historyEntity);

        return applicationId;
    }

.. _complete_task:

-----------------------
ワークフローの進行
-----------------------
ワークフローインスタンスに対して ``WorkflowInstance#completeUserTask`` 、
または ``WorkflowInstance#completeGroupTask`` を呼び出すことでワークフローを進行させることができる。

アプリケーションではワークフローの進行後に、処理履歴の追加や、業務データのステータスの更新を行う。

.. tip::

   ワークフローの進行後にそのワークフローが完了する場合にも、特に追加の処理は必要ない。

**実装例(CM111001Component.java)**

以下は、交通費申請の確認タスクを承認タスクへ進行させる処理
（:ref:`ワークフロー定義 <trans_expence_appliance_definition>` の②に対応）のコードである。

確認タスク後のXORゲートウェイから承認タスクに進行させる必要があるので、 ``completeUserTask`` にパラメータを
渡す必要がある。XORゲートウェイから承認タスクに進行するシーケンスフローのフロー進行条件には、
``eq(condition,0)`` が設定されているので、 ``completeUserTask`` のパラメータに ``condition`` として ``FORWARD_CONDITION``
（ ``"0"`` ）を設定している。

.. tip::

   ワークフロー定義ファイルのフロー進行条件に設定されている値と、具体的なパラメータとの関連は
   「ワークフロー設計ガイド」を参照。

確認タスクから承認タスクにワークフローが進行する際に、業務データについても合わせて以下の処理を行っている。

* 業務データのステータスを「確認完了」に更新。
* 処理履歴の追加

.. code-block:: java

    /**
     * 確認タスクを承認タスクへ進める。
     *
     * @param applicationEntity 交通費申請情報を保持するEntity
     * @param historyEntity 交通費申請履歴情報を保持するEntity
     */
    public void executeConfirmation(TransExpeApplicationEntity applicationEntity, TransExpeAppliHistoryEntity historyEntity) {

        // アプリケーションデータを取得
        SqlRow application = getApplication(applicationEntity.getTransExpeAppliId());

        // ワークフローインスタンスを取得し、承認タスクに進行するようにパラメータを渡してタスクを完了する。
        Map<String, Object> parameter = new HashMap<String, Object>();
        parameter.put("condition", FORWARD_CONDITION);
        WorkflowManager.findInstance(application.getString("WF_INSTANCE_ID")).completeUserTask(parameter);

        // 業務データのステータスを更新
        applicationEntity.setTransExpeAppliStatusCd(CONFIRM_COMPLETE);
        updateApplicationStatus(applicationEntity);

        // 処理履歴の追加
        historyEntity.setTransExpeAppliActionCd(CONFIRM);
        historyEntity.setTransExpeAppliResultCd(FORWARD_RESULT);
        registerHistory(historyEntity);
    }

.. _trigger_event:

-----------------------
境界イベントの実行
-----------------------
境界イベントは、ワークフローインスタンスに対して ``WorkflowInstance#triggerEvent`` を呼び出すことで実行される。
呼び出すAPI以外は、前述のワークフローの進行と同様である。

**実装例(CM111001Component.java)**

以下は、ワークフローサンプルアプリケーションの境界イベント
（:ref:`ワークフロー定義 <trans_expence_appliance_definition>` の③に対応）を実行するコードである。

.. code-block:: java

    /**
     * 確認タスクを引戻す。
     * 
     * @param applicationEntity 交通費申請情報を保持するEntity
     * @param historyEntity 交通費申請履歴情報を保持するEntity
     */
    public void cancelConfirmation(TransExpeApplicationEntity applicationEntity, TransExpeAppliHistoryEntity historyEntity) {

        SqlRow application = getApplication(applicationEntity.getTransExpeAppliId());

        // 境界イベントを実行する。
        WorkflowManager.findInstance(application.getString("WF_INSTANCE_ID")).triggerEvent(CANCEL_TRIGGER);

        // ワークアイテムの更新
        applicationEntity.setTransExpeAppliStatusCd(CONFIRM_CANCEL);
        updateApplicationStatus(applicationEntity);

        // 履歴情報の登録
        historyEntity.setTransExpeAppliActionCd(CANCEL);
        historyEntity.setTransExpeAppliResultCd(FORWARD_RESULT);
        registerHistory(historyEntity);
    }

-----------------------
ワークフローの検索
-----------------------
ワークフローの検索処理では、通常の業務アプリケーションと同様に、
アクティブユーザタスクテーブルなどのワークフローライブラリが利用するテーブルに対して検索処理を実装する。

**実装例(CM211AB1Component.sql)**

以下は、承認情報の一覧検索を行うコードである。

.. code-block:: sql

    -- 進行可能申請一覧検索用SQL
    -- 各ワークアイテムを、ユーザまたはグループが割り当てられているアクティブタスクで絞りこんでから結合する。
    SELECT_ACTIVE_APPLICATION_BY_CONDITION=
    WITH
        ACTIVE_TASK AS
        (
        SELECT    -- アクティブユーザタスク
            WF_ACTIVE_USER_TASK.INSTANCE_ID,
            WF_ACTIVE_USER_TASK.FLOW_NODE_ID
        FROM
            WF_ACTIVE_USER_TASK
        WHERE
            WF_ACTIVE_USER_TASK.ASSIGNED_USER_ID = :loginUserId
        UNION ALL
        SELECT    -- アクティブグループタスク
            WF_ACTIVE_GROUP_TASK.INSTANCE_ID,
            WF_ACTIVE_GROUP_TASK.FLOW_NODE_ID
        FROM
            WF_ACTIVE_GROUP_TASK
        WHERE
            WF_ACTIVE_GROUP_TASK.ASSIGNED_GROUP_ID = :ugroupId
        )
    SELECT
        WORK_ITEM.BUSINESS_TYPE,
        WORK_ITEM.APPLICATION_ID,
        WORK_ITEM.APPLICATION_DATE,
        USERS.KANJI_NAME APPLICATION_USER_NAME,
        WORK_ITEM.STATUS_CD
    FROM
        (
        SELECT  -- 交通費申請
            TRANS_EXPE_APPLICATION.WF_INSTANCE_ID,
            '2' BUSINESS_TYPE,
            TRANS_EXPE_APPLICATION.TRANS_EXPE_APPLI_ID APPLICATION_ID,
            TRANS_EXPE_APPLICATION.INSERT_DATE_TIME APPLICATION_DATE,
            TRANS_EXPE_APPLICATION.INSERT_USER_ID APPLICATION_USER_ID,
            TRANS_EXPE_APPLICATION.TRANS_EXPE_APPLI_STATUS_CD STATUS_CD
        FROM
            TRANS_EXPE_APPLICATION
        INNER JOIN
            ACTIVE_TASK
        ON
            TRANS_EXPE_APPLICATION.WF_INSTANCE_ID = ACTIVE_TASK.INSTANCE_ID
        UNION ALL
        SELECT  -- ローン申請
            LOAN_APPLICATION.WF_INSTANCE_ID,
            '1',
            LOAN_APPLICATION.LOAN_APPLI_ID,
            LOAN_APPLICATION.INSERT_DATE_TIME,
            LOAN_APPLICATION.INSERT_USER_ID,
            LOAN_APPLICATION.LOAN_APPLI_STATUS_CD
        FROM
            LOAN_APPLICATION
        INNER JOIN
            ACTIVE_TASK
        ON
            LOAN_APPLICATION.WF_INSTANCE_ID = ACTIVE_TASK.INSTANCE_ID
        ) WORK_ITEM
    INNER JOIN
        USERS
    ON
        WORK_ITEM.APPLICATION_USER_ID = USERS.USER_ID
    WHERE
        $if(businessType) {WORK_ITEM.BUSINESS_TYPE = :businessType}
        AND $if(applicationUserId) {WORK_ITEM.APPLICATION_USER_ID = :applicationUserId}
    ORDER BY
        WORK_ITEM.APPLICATION_DATE


-----------------------------
排他制御についての注意事項
-----------------------------

ワークフローを進行する場合など、ワークフローインスタンスの状態を変更する場合には、 **必ず**
業務データで排他制御を行う必要がある。

例えば、以下のようなAPIを使用する場合には、業務データで排他制御を行わなくてはならない。

* ワークフローの進行(``WorkflowInstance#completeUserTask``,\ ``WorkflowInstance#completeGroupTask``)
* 境界イベントによるワークフローの進行(``WorkflowInstance#triggerEvent``)
* ユーザ/グループの割り当て(``WorkflowInstance#assignUser``,\ ``WorkflowInstance#assignGroup``, ...)
* 割り当て済みユーザ/グループの変更(``WorkflowInstance#changeAssignedUser``,\ ``WorkflowInstance#changeAssignedGroup``)

**実装例**

排他制御処理の実装方法は、通常のウェブアプリケーションと同じである。

以下は、ワークフローサンプルアプリケーションの交通費申請承認画面の表示処理を行うコードと、
交通費申請の承認タスクを完了する処理を行うコードである。

交通費申請承認画面の表示（W11AD02Action.java）

.. code-block:: java

    /**
     * 交通費申請承認画面を表示する。<br/>
     * （交通費承認一覧画面からの遷移）
     *
     * @param request リクエストコンテキスト
     * @param context HTTPリクエストの処理に関連するサーバ側の情報
     * @return HTTPレスポンス
     */
    @OnError(type = ApplicationException.class, path = "forward:///action/ss11AB/W11AB01Action/RW11AB0102")
    public HttpResponse doRW11AD0201(HttpRequest request, ExecutionContext context) {
       
        // ワークアイテムのキーを取得
        W11AD02Form form = W11AD02Form.validate("W11AD02", request, "initial");
        String applicationId = form.getApplicationId();
        
        // 排他制御開始
        HttpExclusiveControlUtil.prepareVersion(context,
                new ExclusiveCtrlTransExpeApplicationContext(applicationId));
        
        // 後略
    }
    
承認タスクの完了処理（W11AD02Action.java）

.. code-block:: java

    /**
     * 交通費申請の承認タスクを完了する。
     * 
     * @param request リクエストコンテキスト
     * @param context HTTPリクエストの処理に関連するサーバ側の情報
     * @return HTTPレスポンス
     */
    @OnErrors({
        @OnError(type = OptimisticLockException.class,
                 path = "forward:///action/ss11AB/W11AB01Action/RW11AB0102"),
        @OnError(type = ApplicationException.class,
                 path = "forward:///action/ss11AD/W11AD02Action/RW11AD0210")
    })
    public HttpResponse doRW11AD0205(HttpRequest request, ExecutionContext context) {
        
        // 排他制御
        HttpExclusiveControlUtil.updateVersionsWithCheck(request);
        
        W11AD02Form form = W11AD02Form.validate("W11AD02", request, "authorize");
        
        // ワークフローの進行、業務処理の実施
        CM111001Component component = new CM111001Component();
        component.executeAuthorization(form.getApplicationEntity(), form.getHistoryEntity());
        
        // 後略
    }