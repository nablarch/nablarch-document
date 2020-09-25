.. _`create_example`:

登録機能での実装例
=====================================================================

入力画面の初期表示
---------------------------------------------------------------------
.. code-block:: java

  // ブラウザを直接閉じた場合などにセッションが残っている場合があるので削除
  SessionUtil.delete(ctx, "project");

入力画面から確認画面へ遷移
---------------------------------------------------------------------
.. code-block:: java

  // リクエストスコープから入力情報を取得
  ProjectForm form = context.getRequestScopedVar("form");

  // FormからEntityへ変換
  Project project = BeanUtil.createAndCopy(Project.class, form);

  // 入力情報をセッションストアに保存
  SessionUtil.put(ctx, "project", project);

確認画面から入力画面へ戻る
---------------------------------------------------------------------
.. code-block:: java

  // セッションストアから入力情報を取得
  Project project = SessionUtil.get(ctx, "project");

  // EntityからFormへ変換
  ProjectForm form = BeanUtil.createAndCopy(ProjectForm.class, project);

  // 入力情報をリクエストスコープに設定
  context.setRequestScopedVar("form", form);

  // セッションストアから入力情報を削除
  SessionUtil.delete(ctx, "project");

登録処理を実行
---------------------------------------------------------------------
.. code-block:: java

  // セッションストアから入力情報を取得
  Project project = SessionUtil.get(ctx, "project");

  // 登録処理は省略

  // セッションストアから入力情報を削除
  SessionUtil.delete(ctx, "project");
