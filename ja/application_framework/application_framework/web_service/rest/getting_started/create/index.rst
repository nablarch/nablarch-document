登録機能の作成
================================================================
Exampleアプリケーションを元に、登録機能の解説を行う。

作成する機能の説明
  本機能は、POSTリクエスト時にリクエストボディにJSON形式のプロジェクト情報を設定することで、
  データベースにプロジェクト情報を登録する。

動作確認手順
  1. 事前にDBの状態を確認

     H2のコンソールから下記SQLを実行し、レコードが存在しないことを確認する。

     .. code-block:: sql

       SELECT * FROM PROJECT WHERE PROJECT_NAME = 'プロジェクト９９９';

  2. プロジェクト情報の登録

    任意のRESTクライアントを使用して、以下のリクエストを送信する。

    URL
      http://localhost:9080/projects
    HTTPメソッド
      POST
    Content-Type
      application/json
    リクエストボディ
      .. code-block:: json

        {
            "projectName": "プロジェクト９９９",
            "projectType": "development",
            "projectClass": "ss",
            "projectManager": "山田",
            "projectLeader": "田中",
            "clientId": 10,
            "projectStartDate": "20160101",
            "projectEndDate": "20161231",
            "note": "備考９９９",
            "sales": 10000,
            "costOfGoodsSold": 20000,
            "sga": 30000,
            "allocationOfCorpExpenses": 40000
        }

  3. 動作確認

    H2のコンソールから下記SQLを実行し、レコードが1件取得できることを確認する。

    .. code-block:: sql

      SELECT * FROM PROJECT WHERE PROJECT_NAME = 'プロジェクト９９９';

プロジェクト情報を登録する
---------------------------------

URLとのマッピングを定義
  :ref:`router_adaptor` を使用して、業務アクションとURLのマッピングを行う。

    routes.xml
      .. code-block:: xml

        <routes>
          <post path="projects" to="Project#save"/>
        </routes>

    この実装のポイント
     * ``post`` タグを使用して、POSTリクエスト時にマッピングする業務アクションメソッドを定義する。

フォームの作成
  クライアントから送信された値を受け付けるフォームを作成する。

  ProjectForm.java
    .. code-block:: java

      public class ProjectForm implements Serializable {

          // 一部のみ抜粋

          /** プロジェクト名 */
          @Required
          @Domain("projectName")
          private String projectName;

          // ゲッタ及びセッタは省略
      }

    この実装のポイント
     * プロパティは全てString型で宣言する。詳細は :ref:`バリデーションルールの設定方法 <bean_validation-form_property>` を参照。

業務アクションメソッドの実装
  プロジェクト情報をデータベースに登録する処理を実装する。

  ProjectAction.java
    .. code-block:: java

      @Consumes(MediaType.APPLICATION_JSON)
      @Valid
      public HttpResponse save(ProjectForm project) {
          UniversalDao.insert(BeanUtil.createAndCopy(Project.class, project));
          return new HttpResponse(HttpResponse.Status.CREATED.getStatusCode());
      }

   この実装のポイント
    * リクエストをJSON形式で受け付けるため、 :java:extdoc:`Consumes<javax.ws.rs.Consumes>` アノテーションに
      ``MediaType.APPLICATION_JSON`` を指定する。
    * :java:extdoc:`Valid <javax.validation.Valid>` アノテーションを使用して、リクエストのバリデーションを行う。
      詳細は :ref:`jaxrs_bean_validation_handler` を参照。
    * :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` でフォームをエンティティに変換し、
      :ref:`universal_dao` を使用してプロジェクト情報をデータベースに登録する。
    * 戻り値として、リソースの作成完了(ステータスコード： ``201`` )を表す :java:extdoc:`HttpResponse<nablarch.fw.web.HttpResponse>` を返却する。

