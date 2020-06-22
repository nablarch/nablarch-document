==================================
取引単体テストの実施方法
==================================

ウェブサービスにおいては、取引は1リクエストで完結することがほとんどである。このように、１リクエスト＝１取引である場合は、取引単体テストを実施する必要はない。

ただし、複数のリクエストにより取引が成立する場合は、リクエスト毎のテストを連続実行することにより取引単体テストが実施可能である。

以下の例では更新対象を取得し、取得した情報から更新用のフォームを作成して更新実行、想定通りに更新されていることを検証している。

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
