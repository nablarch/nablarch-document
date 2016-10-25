============================================
ワークフロー定義例
============================================

.. 参考情報：
     `Wikipedia <http://ja.wikipedia.org/wiki/%E3%83%AF%E3%83%BC%E3%82%AF%E3%83%95%E3%83%AD%E3%83%BC%E3%82%B7%E3%82%B9%E3%83%86%E3%83%A0>`_
     `intra-mart ワークフロー <http://www.intra-mart.jp/products/iap/im-workflow/feature1.html>`_
     `楽々 Workflow II<http://www.sei-info.co.jp/workflow/functions/control.html>`_

一般的な「申請」「確認」「承認」のステップからなるワークフローを、 :doc:`../index` ではどのような
ワークフロー定義として実現するかの例を記載する。

.. _workflow_normal_process:

通常経路（申請・確認・承認）
-----------------------------------------------------
  **ワークフロー概要**
    ワークフローインスタンスを生成し、ワークフローを開始・進行・終了させる。

    確認や承認の :ref:`workflow_element_task` の :ref:`workflow_task_assignee` を指定してワークフローを進行させる。

  **実現方法**
    各フローノードについて、それに続くフローノードを定義する。

  **ワークフロー定義の例**
    .. image:: _images/normal_process.png
       :align: left
       :scale: 80


.. _workflow_conditional_branch:

条件分岐
-----------------------------------------------------
  **ワークフロー概要**
    ある :ref:`workflow_element_task` での処理結果などに応じて進行先の :ref:`workflow_element_task` を変更する。

  **実現方法**
    :ref:`workflow_element_gateway_xor` を利用し、進行先となる可能性のあるフローノードとそれらに進行する条件を定義する。
    3つ以上に条件分岐することも可能。

  **ワークフロー定義の例**
    .. image:: _images/conditional_branch.png
       :align: left
       :scale: 80


.. _workflow_remand:

差戻
-----------------------------------------------------
  **ワークフロー概要**
    確認などを行う :ref:`workflow_element_task` で、確認結果がNGだった場合に申請者に差戻しを行う。

    このとき、差戻し後の :ref:`workflow_element_task` の :ref:`workflow_task_assignee` は、
    その :ref:`workflow_element_task` を直前に実行したユーザとなる。

  **実現方法**
    確認結果がOKかどうかで進行先となるフローノードを切り替える :ref:`workflow_element_gateway_xor` を利用し、
    OKの場合には承認タスクへ、NGの場合は前の申請タスクにワークフローを進行させる。

    一般に、既に一度実行されている :ref:`workflow_element_task` へワークフローを進行させる必要がある場合には、
    :ref:`workflow_element_gateway_xor` を利用することで要件を実現できる。
    その場合の :ref:`workflow_task_assignee` には、その :ref:`workflow_element_task` に最後に割り当てられていたユーザが設定される。

  **ワークフロー定義の例**
    .. image:: _images/remand.png
       :align: left
       :scale: 80


.. _workflow_reapply:

再申請
-----------------------------------------------------
  **ワークフロー概要**
    差し戻された申請を修正し、再申請を行う。

    上記の単純な差戻しフローとは異なり、初回の申請と再申請を明確に区別する。

  **実現方法**
    差戻しと同様に、確認結果がOKかどうかで進行先となるフローノードを切り替える :ref:`workflow_element_gateway_xor` を利用する。
    ただし、NGの場合には、申請タスクではなく、再申請タスクにワークフローを進行させる。

    なお、申請者は申請タスクを実施後に必ずしも再申請を行うわけではないため、
    申請タスクと再申請タスクを結ぶシーケンスフローは作成しないこと。

  **ワークフロー定義の例**
    .. image:: _images/reapply.png
       :align: left
       :scale: 80


.. _workflow_cancel:

取消
-----------------------------------------------------
  **ワークフロー概要**
    申請者が、申請の取り消しを行う。

    申請が取り消された場合には、ワークフローを完了させる。

  **実現方法**
    申請の取り消しを行うことができる作業種別に対応する :ref:`workflow_element_task` に、
    :ref:`workflow_element_boundary_event` を関連付ける。

    それらの :ref:`workflow_element_boundary_event` からは、 :ref:`workflow_element_event_terminate` に
    ワークフローを進行させるようにしておく。

    申請の取り消しが行われた時には、上記の :ref:`workflow_element_boundary_event` をトリガーし、ワークフローを完了する。

  **ワークフロー定義の例**
    .. image:: _images/cancel.png
       :align: left
       :scale: 80


.. _workflow_reject:

却下
-----------------------------------------------------
  **ワークフロー概要**
    確認者や承認者が、申請を却下する。

    申請が却下された場合には、ワークフローを完了させる。

  **実現方法**
    :ref:`workflow_remand` と同様に、確認結果がOKかどうかで進行先となるフローノードを切り替える
    :ref:`workflow_element_gateway_xor` を利用し、却下の場合には、 :ref:`workflow_element_event_terminate` にワークフローを進行させる。

  **ワークフロー定義の例**
    .. image:: _images/reject.png
       :align: left
       :scale: 80


.. _workflow_pullback:

引戻
-----------------------------------------------------
  **ワークフロー概要**
    確認依頼などが行われ、既に別実行ユーザの担当する :ref:`workflow_element_task` にワークフローが進行している場合に、
    以前の実行ユーザが自分の担当する :ref:`workflow_element_task` までワークフローを巻き戻す。

  **実現方法**
    :ref:`workflow_cancel` と同様に、申請の引戻しを行うことができる作業種別に対応する :ref:`workflow_element_task` に、
    :ref:`workflow_element_boundary_event` を関連付ける。

    それらの :ref:`workflow_element_boundary_event` からは、引戻し後の :ref:`workflow_element_task` に
    ワークフローを進行させるようにしておく。

    申請の引戻しが行われた時には、上記の :ref:`workflow_element_boundary_event` を発生させし、
    ワークフローを引戻し後の :ref:`workflow_element_task` に進行させる。

  **ワークフロー定義の例**
    .. image:: _images/pullback.png
       :align: left
       :scale: 80


.. _workflow_confirm:

後閲
-----------------------------------------------------
  **ワークフロー概要**
    :ref:`workflow_element_task` が代理ユーザによって処理された場合には、代理元ユーザ本人が対象を確認して、ワークフローが完了する。

  **実現方法**
    後閲の可能性があるフローに入る際には、必ずユーザを選択してからワークフローを進行させるものとし、
    選択されたユーザが代理ユーザであるかどうかで、ワークフローを分岐する。

    なお、要件上、確認後にユーザ選択を強制することができない場合には、フロー進行条件をアプリケーションで実装し、
    直前の :ref:`workflow_element_task` の実行ユーザが代理ユーザであったかどうかをゲートウェイで判定することで、
    下記例の確認後の「承認者選択タスク」は不要となり、確認後にユーザ選択を強制する必要はなくなる。

  **ワークフロー定義の例**
    .. image:: _images/confirm.png
       :align: left
       :scale: 80


.. _workflow_council:

合議（回覧）
-----------------------------------------------------
  **ワークフロー概要**
    複数人で承認を行い、全員の承認が完了した時点でワークフローを進行させる。

    一人でも差戻しなどを行った場合には、合議を中断して差戻し先にワークフローを進行させる。

  **実現方法**
    合議に対応する :ref:`workflow_element_task` には、担当ユーザを複数人割り当てることのできる
    :ref:`workflow_element_multi_instance_task` を利用する。

    なお、合議に参加する人数は動的に決定できる。

  **ワークフロー定義の例**
    .. image:: _images/council.png
       :align: left
       :scale: 80


.. _workflow_escalation:

審議（エスカレーション）／スキップ
-----------------------------------------------------
  **ワークフロー概要**
    審議：確認や承認などを行った後、内容に応じて別の担当者による審査を実施する。

    スキップ：確認や承認などを行った後、内容に応じて別の担当者による審査はスキップする。

  **実現方法**
    審議とスキップは、同一のワークフロー定義であらわされる。
    :ref:`workflow_conditional_branch` を利用して、内容に応じた分岐を行えばよい。

  **ワークフロー定義の例**
    .. image:: _images/escalation.png
       :align: left
       :scale: 80

