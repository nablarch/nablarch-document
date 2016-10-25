.. _`project_delete`:

削除機能の作成
==========================================
Exampleアプリケーションを元に削除機能の解説を行う。

作成する機能の説明
  1. プロジェクト一覧のプロジェクトIDを押下する。

    .. image:: ../images/project_delete/project_delete_list.png
      :scale: 80

  2. 詳細画面の変更ボタンを押下する。

    .. image:: ../images/project_delete/project_delete_detail.png
      :scale: 80

  3. 更新画面上の削除ボタンを押下する。

    .. image:: ../images/project_delete/project_delete_update.png
      :scale: 60

  4. 完了画面が表示される。

    .. image:: ../images/project_delete/project_delete_complete.png
      :scale: 80

削除を行う
-----------
削除機能の基本的な実装方法を、以下の順に説明する。

  #. :ref:`更新画面上に削除ボタンを作成<project_delete-update>`
  #. :ref:`削除を行う業務アクションメソッドの作成<project_delete-delete_action>`
  #. :ref:`削除完了画面の作成<project_delete-complete>`

.. _`project_delete-update`:

更新画面上に削除ボタンを作成
  更新画面上に、削除ボタンを作成する。
  更新画面の作成に関する説明は、 :ref:`更新画面を表示する業務アクションメソッドの作成<project_update-create_edit_action>` 及び
  :ref:`更新画面のJSPの作成<project_update-create_update_jsp>` を参照。

.. _`project_delete-delete_action`:

削除を行う業務アクションメソッドの作成
  データベースから対象プロジェクトを削除する業務アクションメソッドを作成する。

  ProjectAction.java
    .. code-block:: java

      @OnDoubleSubmission
      public HttpResponse delete(HttpRequest request, ExecutionContext context) {

          // 更新画面を表示する際にセッションにプロジェクト情報を格納している
          Project project = SessionUtil.delete(context, "project");
          UniversalDao.delete(project);

          return new HttpResponse("redirect://completeOfDelete");
      }

  この実装のポイント
    * 主キーを条件とした削除は、主キーが設定されたエンティティを引数に :java:extdoc:`UniversalDao#delete <nablarch.common.dao.UniversalDao.delete(T)>`
      を実行することで、SQLを作成しなくとも実行できる。

  .. tip::

    :ref:`universal_dao` は、主キーを条件とする削除機能のみを提供する。主キー以外を条件とする削除を行う場合は、別途SQLを作成して実行する必要がある。
    SQLの実行方法については、 :ref:`SQLIDを指定してSQLを実行する<database-execute_sqlid>` を参照。

.. _`project_delete-complete`:

削除完了画面の作成
  削除完了を通知するメッセージを設定して、完了画面を表示する。
  完了画面の作成に関する説明は、 :ref:`完了画面を表示する業務アクションメソッドの作成<project_update-create_complete_action>` 及び
  :ref:`更新完了画面の作成<project_update-create_success_jsp>` を参照。

削除機能の解説は以上。

:ref:`Getting Started TOPページへ <getting_started>`