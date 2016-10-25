検索機能の作成
================================================================
Exampleアプリケーションを元に、検索機能の解説を行う。

作成する機能の説明
  本機能は、GETリクエスト時にクエリパラメータに検索条件を付与することで、
  条件に合致するプロジェクト情報をJSON形式で返却する。

  検索条件として、 ``顧客ID(完全一致)``  、 ``プロジェクト名(部分一致)`` を指定することができる。
  検索条件を指定しない場合は、全てのプロジェクト情報を返却する。

動作確認手順
  1. プロジェクト情報の検索

    ここでは、顧客IDが `1` のプロジェクト情報の検索を行う。

    任意のRESTクライアントを使用して、以下のリクエストを送信する。

    URL
      http://localhost:9080/projects?clientId=1
    HTTPメソッド
      GET

  2. 検索結果の確認

    1.を実行した結果、以下のようなJSON形式のレスポンスが返却されることを確認する。

    .. code-block:: json

      [{
          "projectId":1,
          "projectName":"プロジェクト００１",
          "projectType":"development",

          // 省略

      }]

プロジェクト情報を検索する
---------------------------------

URLとのマッピングを定義
  :ref:`router_adaptor` を使用して、業務アクションとURLのマッピングを行う。

    routes.xml
      .. code-block:: xml

        <routes>
          <get path="projects" to="Project#find"/>
        </routes>

    この実装のポイント
     * ``get`` タグを使用して、GETリクエスト時にマッピングする業務アクションメソッドを定義する。

フォームの作成
  クライアントから送信された値を受け付けるフォームを作成する。

  ProjectSearchForm.java
    .. code-block:: java

      public class ProjectSearchForm implements Serializable {

          /** 顧客ID */
          @Domain("id")
          private String clientId;

          /** プロジェクト名 */
          @Domain("projectName")
          private String projectName;

          // ゲッタ及びセッタは省略
      }

  この実装のポイント
    * プロパティは全てString型で宣言する。詳細は :ref:`バリデーションルールの設定方法 <bean_validation-form_property>` を参照。

検索条件を保持するBeanの作成
  検索条件を保持するBeanを作成する。

  ProjectSearchDto.java
    .. code-block:: java

      public class ProjectSearchDto implements Serializable {

          /** 顧客ID */
          private Integer clientId;

          /** プロジェクト名 */
          private String projectName;

          // ゲッタ及びセッタは省略

  この実装のポイント
   * Beanのプロパティは、:ref:`対応する条件カラムの定義(型)と互換性のある型とする<universal_dao-search_with_condition>` こと。

検索に利用するSQLの作成
  検索に利用するSQLを作成する。

    Project.sql
      .. code-block:: sql

        FIND_PROJECT =
        SELECT
            *
        FROM
            PROJECT
        WHERE
            $if(clientId) {CLIENT_ID = :clientId}
            AND $if(projectName) {PROJECT_NAME LIKE :%projectName%}

    この実装のポイント
      * SQLインジェクションを防ぐため、SQLは外部ファイルに記述する。詳細は :ref:`database-use_sql_file` を参照。
      * Beanのプロパティ名を使って、SQLに値をバインドする。詳細は :ref:`database-input_bean` を参照。
      * 検索条件として指定された項目のみを条件に含める場合には、 :ref:`$if 構文を使用してSQL文を構築<database-use_variable_condition>` する。

業務アクションメソッドの実装
  検索条件をもとにデータベースから検索する処理を実装する。

  ProjectAction.java
    .. code-block:: java

      @Produces(MediaType.APPLICATION_JSON)
      public List<Project> find(HttpRequest req) {

          // リクエストパラメータをBeanに変換
          ProjectSearchForm form =
                  BeanUtil.createAndCopy(ProjectSearchForm.class, req.getParamMap());

          // BeanValidation実行
          ValidatorUtil.validate(form);

          ProjectSearchDto searchCondition = BeanUtil.createAndCopy(ProjectSearchDto.class, form);
          return UniversalDao.findAllBySqlFile(Project.class, "FIND_PROJECT", searchCondition);
      }

  この実装のポイント
   * 検索結果をJSON形式でクライアントに返却するため、 :java:extdoc:`Produces<javax.ws.rs.Produces>` アノテーションに
     ``MediaType.APPLICATION_JSON`` を指定する。
   * クエリパラメータは :java:extdoc:`HttpRequest<nablarch.fw.web.HttpRequest>` から取得する。
   * :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` を利用してリクエストパラメータからフォームを作成する。
   * :java:extdoc:`ValidatorUtil#validate <nablarch.core.validation.ee.ValidatorUtil.validate(java.lang.Object)>`
     を使用してフォームのバリデーションを行う。
   * フォームの値を :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` を利用して検索条件Beanにコピーする。
   * :ref:`universal_dao` を使用して取得したプロジェクト情報のリストを戻り値として返却する。
   * 戻り値のオブジェクトは :ref:`body_convert_handler` によってJSON形式に変換されるため、
     業務アクションメソッド内で変換処理を実装する必要はない。
