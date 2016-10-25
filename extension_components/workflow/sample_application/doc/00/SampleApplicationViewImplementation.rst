======================================================
アクティブタスクの判定と処理の分岐
======================================================

------------------------------------------------------
タスクがアクティブかどうかの判定
------------------------------------------------------

現在処理可能なタスク（アクティブタスク）は、 ``WorkflowInstance#isActive`` を利用して判定することができる。

ワークフローの進行後のアクティブタスクに応じて処理を分岐する必要がある場合や、現在のアクティブタスクに応じて処理を
分岐する必要がある場合には、以下のように ``isActive`` の結果に応じて分岐すれば良い。

**実装例(W11AD02Action.java)**

.. code-block:: java

    /**
     * 交通費申請処理で精査エラーが発生した際の処理を行う。
     *
     * @param request リクエストコンテキスト
     * @param context HTTPリクエストの処理に関連するサーバ側の情報
     * @return HTTPレスポンス
     */
    public HttpResponse doRW11AD0210(HttpRequest request, ExecutionContext context) {

        // ～ 中略 ～

        WorkflowInstance workflow = WorkflowManager.findInstance(application.getString("WF_INSTANCE_ID"));

        if (workflow.isActive(REAPPLICATION_TASK)) {
            // 再申請タスクがアクティブタスクとなっている場合には、再申請用画面に遷移する。
            setupAssignUserList(context);
            return new HttpResponse("/ss11AD/W11AD0203.jsp");
        } else {
            // それ以外（確認/承認タスクがアクティブタスク）の場合には、確認/承認用画面に遷移する。
            application.put("historyComment", form.getHistoryComment());
            context.setRequestScopedVar("W11AD02", application);
            context.setRequestScopedVar("confirmTask", workflow.isActive(CONFIRMATION_TASK));
            context.setRequestScopedVar("authorizeTask", workflow.isActive(AUTHORIZATION_TASK));
            return new HttpResponse("/ss11AD/W11AD0201.jsp");
        }
    }

------------------------------------------------------------
担当ユーザ/グループへのアクティブタスクの割り当て状況の確認
------------------------------------------------------------

あるユーザ/グループに割り当てられたアクティブタスクが存在するかどうかは、
``WorkflowInstance#hasActiveUserTask``, ``WorkflowInstance#hasActiveGroupTask`` を使用して判定することができる。

たとえば交通費申請の場合、一覧画面から承認画面に遷移する際には、一覧画面からは排他制御を行わないため、
承認画面に遷移する際に、ユーザに該当のワークフローインスタンスのアクティブタスクが実際に割り当てられているかどうかを
確認する必要がある。

このような場合には、以下のように ``hasActiveUserTask``, ``hasActiveGroupTask`` を利用して、
ワークフローインスタンスのアクティブタスクを実際にユーザが処理可能であるかどうかを確認する。

**実装例(W11AD02Action.java)**

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

        // ワークアイテム取得
        SqlRow applicationInfo = getApplication(applicationId);
        WorkflowInstance workflow = WorkflowManager.findInstance(applicationInfo.getString("WF_INSTANCE_ID"));

        // アクティブタスク割当精査
        if (!workflow.hasActiveUserTask(ThreadContext.getUserId())) {
            throw new ApplicationException(MessageUtil.createMessage(MessageLevel.ERROR, "MSG00034"));
        }

        // ～ 後略 ～
    }


------------------------------------------------------
画面表示項目の切り替え
------------------------------------------------------

タスクがアクティブかどうかの判定結果や、アクティブタスクの割り当て状況によって画面表示項目を切り替える場合、
以下の実装例のように、判定結果をリクエストスコープに格納し、その判定結果をJSPで参照して分岐を行うことで実現できる。

**実装例**

業務アクション(W11AD02Action.java)

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

        // ～ 中略 ～

        if (workflow.isActive(REAPPLICATION_TASK)) {
            // ～ 中略 ～
        } else {
            context.setRequestScopedVar("detail", applicationInfo);
        // 確認タスクがアクティブかどうかの判定結果をリクエストスコープに格納
            context.setRequestScopedVar("confirmTask", workflow.isActive(CONFIRMATION_TASK));
        // 承認タスクがアクティブかどうかの判定結果をリクエストスコープに格納
            context.setRequestScopedVar("authorizeTask", workflow.isActive(AUTHORIZATION_TASK));
            return new HttpResponse("/ss11AD/W11AD0201.jsp");
        }
    }

JSP(W11AD0201.jsp)

.. code-block:: jsp

   <%-- アクティブタスクごとの値を設定 --%>
   <c:if test="${confirmTask}"><%-- 確認待ち --%>
     <n:set var="pageTitleName" value="交通費申請確認"/>
     <n:set var="forwardButtonName" value="確認"/>
     <n:set var="forwardUri" value="/action/ss11AD/W11AD02Action/RW11AD0202"/>
     <n:set var="rejectUri" value="/action/ss11AD/W11AD02Action/RW11AD0203"/>
     <n:set var="turnDownUri" value="/action/ss11AD/W11AD02Action/RW11AD0204"/>
   </c:if>
   <c:if test="${authorizeTask}"><%-- 承認待ち --%>
     <n:set var="pageTitleName" value="交通費申請承認"/>
     <n:set var="forwardButtonName" value="承認"/>
     <n:set var="forwardUri" value="/action/ss11AD/W11AD02Action/RW11AD0205"/>
     <n:set var="rejectUri" value="/action/ss11AD/W11AD02Action/RW11AD0206"/>
     <n:set var="turnDownUri" value="/action/ss11AD/W11AD02Action/RW11AD0207"/>
   </c:if>

