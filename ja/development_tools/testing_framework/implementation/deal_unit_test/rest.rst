.. _deal_unit_test_rest:

取引単体テスト（RESTfulウェブサービス）
==================================================

.. contents:: 目次
  :depth: 3
  :local:

RESTfulウェブサービスの取引単体テストは、1つの取引を構成する複数のリクエストを1つのテストメソッドの中で順に送信し、取引全体が想定どおりに処理されることを検証する。

機能概要
--------------------------------------------------

RESTfulウェブサービスでは、取引が1つのリクエストで完結することがほとんどである。このように1リクエストが1取引に対応する場合は、取引単体テストを実施する必要はない。

複数のリクエストによって1つの取引が成立する場合は、1つのテストメソッドの中でリクエストを順に送ることで取引単体テストを実施できる。

使用方法
--------------------------------------------------

テストクラスの作成方法とテストの実行方法は\ :ref:`リクエスト単体テスト（RESTfulウェブサービス） <request_unit_test_rest>`\ と同じである。テストデータの記述方法は\ :ref:`テストデータの書き方 <testdata_notation>`\ に従う。

テストメソッドを作成する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1つの取引を構成するリクエストは、1つのテストメソッドの中で順に送信する。

次の例では、更新対象のプロジェクトを取得し、取得した情報から更新用のフォームを作成して更新を実行し、更新後のプロジェクトを再度取得して想定どおりに更新されたことを検証している。

.. code-block:: java

  @Test
  public void プロジェクト更新取引() {
      String message1 = "変更対象取得";
      RestMockHttpRequest request001 = get("/projects?projectName=プロジェクト００１");
      HttpResponse response001 = sendRequest(request001);
      assertStatusCode(message1, HttpResponse.Status.OK, response001);
      // 取得した変更対象を使って更新用フォームを作成
      Project project = parseProject(response001).setProjectName("プロジェクト８８８");
      ProjectUpdateForm updateForm = new ProjectUpdateForm(project);

      String message2 = "プロジェクト更新";
      RestMockHttpRequest updateRequest = put("/projects").setBody(updateForm);
      HttpResponse updateResponse = sendRequest(updateRequest);
      assertStatusCode(message2, HttpResponse.Status.OK, updateResponse);

      String message3 = "取得したプロジェクトが変更した内容と一致すること";
      RestMockHttpRequest request888 = get("/projects?projectName=プロジェクト８８８");
      HttpResponse response888 = sendRequest(request888);
      assertStatusCode(message3, HttpResponse.Status.OK, response888);
      assertProjectEquals(project, parseProject(response888));
  }

``parseProject``\ と\ ``assertProjectEquals``\ は、テストクラスに用意した補助メソッドである。

この例では、1回目の\ ``get``\ で受け取ったレスポンスからプロジェクトを組み立て、\ ``put``\ の本文に設定している。このように、先行するレスポンスの値はテストメソッドの中で次のリクエストへ渡す。

.. tip::

  セッションIDやCSRFトークンのように、サーバがレスポンスで返す値を毎回同じ手順で引き継ぐ場合は、引き継ぐ処理をコンポーネント設定ファイルに登録できる。設定方法は\ :ref:`取引単体テストの設定（RESTfulウェブサービス） <deal_unit_test_setting_rest>`\ を参照。
