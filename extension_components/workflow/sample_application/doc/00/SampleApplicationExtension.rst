====================================================
ゲートウェイの進行先ノード判定ロジックを変更する方法
====================================================

.. _customize_flow_proceed_condition:

-------------------------------------
進行先ノードの判定制御ロジックの実装
-------------------------------------

``FlowProceedCondition`` インタフェースを実装することで、進行先ノードの判定制御としてPJ固有のロジックを用いることが出来る。

**実装例(CM111004Component.java)**

以下は、``FlowProceedCondition`` を実装したコンポーネントの一部であり、ローン申請の内部自動審査後の条件分岐
（:ref:`ワークフロー定義 <loan_appliance_definition>` の④に対応）のための
業務ロジックを実装している。

このコンポーネントは、内部自動審査後のXORゲートウェイから流出するすべてのシーケンスフローのフロー進行条件として
設定されているため、評価対象のシーケンスフローがどのタスクに進行するシーケンスフローかに応じて返却する値を変える必要がある。

.. admonition:: 仕様

   パラメータから ``LoanApplicationEntity`` を取得(キー:``loanApplication``)し、
   年収及びローン申請額を元に進行先を決定する。

   ローン申請額が年収の半分以下の場合は「調査」タスクに進行し、半分より大きい場合は「却下」タスクに進行する。


.. admonition:: 実装方法

   ローン申請額が年収の半分以下で、評価対象の ``SequenceFlow`` （引数として渡されている ``sequenceFlow`` ）の
   進行先が「調査」タスクの場合に ``true`` を返却する。

   それ以外の場合には ``false`` を返却する。


.. code-block:: java

    @Override
    public boolean isMatch(String instanceId, Map<String, ?> param, SequenceFlow sequenceFlow) {
        LoanApplicationEntity loanApplication = (LoanApplicationEntity) param.get("loanApplication");

        int annualSalary = loanApplication.getAnnualSalary().intValue();
        int loanAmount = loanApplication.getLoanAmount().intValue();

        if ((loanAmount * 2) <= annualSalary) {
            // 審査OKの場合、調査タスクが遷移先の場合に進行先とする。
            return sequenceFlow.getTargetFlowNodeId().equals(SURVEY_TASK_ID);
        } else {
            // 審査NGの場合、調査タスク以外(ワークフロー定義上、却下のみ)が遷移先の場合に進行先とする。
            return !sequenceFlow.getTargetFlowNodeId().equals(SURVEY_TASK_ID);
        }
    }

