更新機能の作成
================================================================
Exampleアプリケーションを元に、更新機能の解説を行う。
 
作成する機能の説明
  本機能は、PUTリクエスト時にリクエストボディにJSON形式のプロジェクト情報を設定することで、
  データベース上のプロジェクトIDが一致するプロジェクト情報を更新する。

動作確認手順
  1. 事前にDBの状態を確認
 
     H2のコンソールから下記SQLを実行し、更新対象レコードを確認する。
 
     .. code-block:: sql
 
       SELECT * FROM PROJECT WHERE PROJECT_ID = 1;
 
  2. プロジェクト情報の更新
 
    任意のRESTクライアントを使用して、以下のリクエストを送信する。
 
    URL
      http://localhost:9080/projects
    HTTPメソッド
      PUT
    Content-Type
      application/json
    リクエストボディ
      .. code-block:: json
 
        {
            "projectId": 1,
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
            "allocationOfCorpExpenses": 40000,
            "version": 1
        }
 
  3. 動作確認
 
    H2のコンソールから下記SQLを実行し、レコードが更新されていることを確認する。
 
    .. code-block:: sql
 
      SELECT * FROM PROJECT WHERE PROJECT_ID = 1;
 
プロジェクト情報を更新する
---------------------------------

URLとのマッピングを定義
  :ref:`router_adaptor` を使用して、業務アクションとURLのマッピングを行う。

    routes.xml
      .. code-block:: xml

        <routes>
          <put path="projects" to="Project#update" />
        </routes>

    この実装のポイント
     * ``put`` タグを使用して、PUTリクエスト時にマッピングする業務アクションメソッドを定義する。

フォームの作成
  クライアントから送信された値を受け付けるフォームを作成する。
 
  ProjectUpdateForm.java
    .. code-block:: java
 
      public class ProjectUpdateForm implements Serializable {
 
          // 一部のみ抜粋

          /** プロジェクト名 */
          @Required
          @Domain("id")
          private String projectId;
 
          /** プロジェクト名 */
          @Required
          @Domain("projectName")
          private String projectName;

          /** プロジェクト種別 */
          @Required
          @Domain("projectType")
          private String projectType;
 
          // ゲッタ及びセッタは省略
      }
 
    この実装のポイント
     * プロパティは全てString型で宣言する。詳細は :ref:`バリデーションルールの設定方法 <bean_validation-form_property>` を参照。
 
業務アクションメソッドの実装
  データベース上のプロジェクト情報を更新する処理を実装する。
 
  ProjectAction.java
    .. code-block:: java

      @Consumes(MediaType.APPLICATION_JSON)
      @Valid
      public HttpResponse update(ProjectUpdateForm form) {
          Project project = BeanUtil.createAndCopy(Project.class, form);

          UniversalDao.update(project);

          return new HttpResponse(HttpResponse.Status.OK.getStatusCode());
      }
 
   この実装のポイント
    * リクエストボディをJSON形式で受け付けるため、 :java:extdoc:`Consumes<javax.ws.rs.Consumes>` アノテーションに
      ``MediaType.APPLICATION_JSON`` を指定する。
    * :java:extdoc:`Valid <javax.validation.Valid>` アノテーションを使用して、リクエストのバリデーションを行う。
      詳細は :ref:`jaxrs_bean_validation_handler` を参照。
    * :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` でフォームからエンティティを作成し、
      :ref:`universal_dao` を使用してプロジェクト情報を更新する。
    * 更新に成功した場合は、正常終了(ステータスコード： ``200`` )を表す :java:extdoc:`HttpResponse<nablarch.fw.web.HttpResponse>` を返却する。

    .. tip::

      Exampleアプリケーションでは :java:extdoc:`ErrorResponseBuilder<nablarch.fw.jaxrs.ErrorResponseBuilder>` を独自に拡張しており、
      :java:extdoc:`NoDataException<nablarch.common.dao.NoDataException>` が発生した場合は ``404`` 、
      :java:extdoc:`OptimisticLockException<javax.persistence.OptimisticLockException>` が発生した場合は ``409``
      のレスポンスを生成してクライアントに返却している。

