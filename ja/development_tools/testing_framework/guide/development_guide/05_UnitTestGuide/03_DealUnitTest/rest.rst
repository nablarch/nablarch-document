==================================
取引単体テストの実施方法
==================================

ウェブサービスにおいては、取引は1リクエストで完結することがほとんどである。このように、１リクエスト＝１取引である場合は、取引単体テストを実施する必要はない。

ただし、複数のリクエストにより取引が成立する場合は、リクエスト毎のテストを連続実行することにより取引単体テストが実施可能である。

取引単体テストのテストクラス例
---------------------------------

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

Cookieなど前のレスポンスの情報を引き継ぐ方法
----------------------------------------------------
取引単体テストの場合、セッションIDやCSRFトークンなど、先行するリクエストのレスポンスとしてサーバから受け取った値を
次のリクエストに含めたい場合がある。
そのような場合は以下の方法で実現できる。

``RequestResponseProcessor`` の実装クラスを作成する
****************************************************************
RESTfulウェブサービス実行基盤向けテスティングフレームワークでは :java:extdoc:`RequestResponseProcessor<nablarch.test.core.http.RequestResponseProcessor>` という
リクエスト・レスポンスを操作するためのインターフェースを用意している。

各アプリケーションの要件に合わせてこのインタフェースの実装クラスを作成する。

フレームワークではよく使われる実装として :java:extdoc:`RequestResponseCookieManager<nablarch.test.core.http.RequestResponseCookieManager>` を提供している。
この実装ではレスポンスの ``Set-Cookie`` ヘッダからプロパティで指定した名前のクッキーを抽出し、リクエストの ``Cookie`` ヘッダに値を引き継ぐことができる。

クッキーのうち、 :ref:`session_store` のセッションIDに特化した実装として :java:extdoc:`NablarchSIDManager<nablarch.test.core.http.NablarchSIDManager>` も提供している。
この実装では、 :ref:`session_store_handler` がセッションIDを保持する際のデフォルトのクッキー名 ``NABLARCH_SID`` で、 ``Set-Cookie`` ヘッダからクッキーを抽出する。
セッションIDのクッキー名をデフォルトから変更した場合は、 :java:extdoc:`RequestResponseCookieManager<nablarch.test.core.http.RequestResponseCookieManager>` を使用し、クッキー名を明示する。

``RequestResponseProcessor`` は1つの取引単体テストケース内で先に受信したレスポンスの値を次のリクエストに受け渡すために使用する。
この時、レスポンスから抽出した値をリクエストに受け渡すために内部に状態として持つことになる。
以下の方法でコンポーネント設定した場合、NablarchのDIコンテナではインスタンスはシングルトンとなってしまうため
明示的に状態を初期化しないと、複数のテストケース間で状態が引き継がれてしまう。
これを防ぐためにフレームワークではテストケースごとに :java:extdoc:`RequestResponseProcessor#reset<nablarch.test.core.http.RequestResponseProcessor.reset()>` を呼び出している。
複数テストケース間で状態を引き継ぎたくない場合は、 ``reset()`` に初期化する処理を実装する必要がある。
内部状態を持たない場合や、複数のテストケース間で状態を共有したい場合は、 ``reset()`` メソッドを何もしないメソッドとしてもよい。

コンポーネント設定ファイルに ``defaultProcessor`` という名前で実装クラスを設定する
***********************************************************************************
.. code-block:: xml

  <component name="defaultProcessor" class="nablarch.test.core.http.RequestResponseCookieManager"/>
    <property name="cookieName" value="JSESSIONID"/>
  </component>


また、複数の ``RequestResponseProcessor`` を設定したい場合は、 :java:extdoc:`ComplexRequestResponseProcessor<nablarch.test.core.http.ComplexRequestResponseProcessor>` を
使用することで実現できる。

.. code-block:: xml

  <component name="defaultProcessor" class="nablarch.test.core.http.ComplexRequestResponseProcessor">
    <property name="processors">
      <list>
        <component class="nablarch.test.core.http.RequestResponseCookieManager"/>
          <property name="cookieName" value="JSESSIONID"/>
        </component>
        <component class="nablarch.test.core.http.NablarchSIDManager"/>
        <component class="com.example.test.CSRFTokenManager"/>
      </list>
    </property>
  </component>

``defaultProcessor`` という名前で設定された ``RequestResponseProcessor`` は、内蔵サーバへのリクエスト送信前に
:java:extdoc:`RequestResponseProcessor#processRequest<nablarch.test.core.http.RequestResponseProcessor.processRequest(nablarch.fw.web.HttpRequest)>` が、
レスポンス受信後に :java:extdoc:`RequestResponseProcessor#processResponse<nablarch.test.core.http.RequestResponseProcessor.processResponse(nablarch.fw.web.HttpRequest-nablarch.fw.web.HttpResponse)>` が
それぞれ実行される。 
