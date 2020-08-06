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

Cookieなど前のレスポンスの情報を引き継ぐ方法
----------------------------------------------------
取引単体テストの場合、セッションIDやCSRFトークンなど、先行するリクエストのレスポンスとしてサーバから受け取った値を
次のリクエストに含めたい場合がある。
そのような場合は以下の方法で実現することができる。

``RequestResponseProcessor`` の実装クラスを作成する
****************************************************************
RESTfulウェブサービス実行基盤向けテスティングフレームワークでは :java:extdoc:`RequestResponseProcessor<nablarch.test.core.http.RequestResponseProcessor>` という
リクエスト・レスポンスを操作するためのインターフェースを用意している。

各アプリケーションの要件に合わせてこのインタフェースの実装クラスを作成し、
:java:extdoc:`SimpleRestTestSupport#setDefaultProcessor<nablarch.test.core.http.SimpleRestTestSupport.setDefaultProcessor(nablarch.test.core.http.RequestResponseProcessor)>`
に設定する。

フレームワークではよく使われる実装として :java:extdoc:`NablarchSIDManager<nablarch.test.core.http.NablarchSIDManager>` を提供している。
この実装ではレスポンスの ``Set-Cookie`` ヘッダーからセッションIDを抽出し、リクエストの ``Cookie`` ヘッダーに値を引き継ぐことができる。

``SimpleRestTestSupport`` の ``DefaultProcessor`` に実装クラスを設定する
**************************************************************************
.. code-block:: java

    public abstract class ExampleRestTest extends SimpleRestTestSupport {
        // テストクラス実行前にsetDefaultProcessorする。
        @BeforeClass
        public void setUp(){
            NablarchSIDManager processor = new NablarchSIDManager();
            setDefaultProcessor(processor);
        }
    }

アプリケーション全体で共通の ``RequestResponseProcessor`` を設定したい場合は基底クラスを作成しコンストラクタで設定することも可能である。

.. code-block:: java

    public abstract class ExampleRestTestBase extends SimpleRestTestSupport {
        public ExampleRestBase() {
            NablarchSIDManager processor = new NablarchSIDManager();
            setDefaultProcessor(processor);
        }
    }

また、複数の ``RequestResponseProcessor`` を設定したい場合は、 :java:extdoc:`ComplexRequestResponseProcessor<nablarch.test.core.http.ComplexRequestResponseProcessor>` を
利用することで実現できる。

.. code-block:: java

    ComplexRequestResponseProcessor processor = new ComplexRequestResponseProcessor();
    processor.setProcessors(Arrays.asList(
            new NablarchSIDManager(),
            new CsrfTokenManager()));
    setDefaultProcessor(processor);

``SimpleRestTestSupport#setDefaultProcessor`` で設定された ``RequestResponseProcessor`` は、内蔵サーバへのリクエスト送信前に
:java:extdoc:`RequestResponseProcessor#processRequest<nablarch.test.core.http.RequestResponseProcessor.processRequest(nablarch.fw.web.HttpRequest)>` が
レスポンス受信後に :java:extdoc:`RequestResponseProcessor#processResponse<nablarch.test.core.http.RequestResponseProcessor.processResponse(nablarch.fw.web.HttpRequest,nablarch.fw.web.HttpResponse)>` が
それぞれ実行される。 