更新機能での実装例
=====================================================================

入力画面の初期表示
---------------------------------------------------------------------
.. code-block:: java

  // ブラウザを直接閉じた場合などにセッションが残っている場合があるので削除
  SessionUtil.delete(ctx, "project");

  // 更新対象データの取得処理は省略

  // 更新対象データをセッションストアに保存
  SessionUtil.put(ctx, "project", project);

  // EntityからFormへ変換
  ProjectForm form = BeanUtil.createAndCopy(ProjectForm.class, project);

  // 更新対象データをリクエストスコープに設定
  context.setRequestScopedVar("form", form);

入力画面から確認画面へ遷移
---------------------------------------------------------------------
.. code-block:: java

  // リクエストスコープから入力情報を取得
  ProjectForm form = context.getRequestScopedVar("form");

  // 更新対象データをセッションストアから取得
  Project project = SessionUtil.get(context, "project");

  // 入力情報を更新対象データに上書き
  BeanUtil.copy(form, project);

確認画面から入力画面へ戻る
---------------------------------------------------------------------
.. code-block:: java

  // セッションストアから更新対象データを取得
  Project project = SessionUtil.get(ctx, "project");

  // EntityからFormへ変換
  ProjectForm form = BeanUtil.createAndCopy(ProjectForm.class, project);

  // 更新対象データをリクエストスコープに設定
  context.setRequestScopedVar("form", form);

更新処理を実行
---------------------------------------------------------------------
.. code-block:: java

  // セッションストアから更新対象データを取得
  Project project = SessionUtil.get(ctx, "project");

  // 更新処理は省略

  // セッションストアから更新対象データを削除
  SessionUtil.delete(ctx, "project");
