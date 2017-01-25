.. _`project_update`:

更新機能の作成
==========================================
Exampleアプリケーションを元に更新機能の解説を行う。

作成する機能の説明
  1. プロジェクト一覧のプロジェクトIDを押下する。

    .. image:: ../images/project_update/project_update_detail_link.png
      :scale: 80

  2. 対象プロジェクトの詳細画面が表示されるので、変更ボタンを押下する。

    .. image:: ../images/project_update/project_update_detail.png
      :scale: 80

  3. 更新する項目を書き換えて、更新ボタンを押下する。

    .. image:: ../images/project_update/project_update_update.png
      :scale: 80

  4. 更新確認画面が表示されるので、確定ボタンを押下する。

    .. image:: ../images/project_update/project_update_confirm.png
      :scale: 80

  5. データベースが更新され、更新完了画面が表示される。

    .. image:: ../images/project_update/project_update_complete.png
      :scale: 80

更新内容の入力と確認
---------------------
更新機能の実装方法のうち、更新内容の入力及び確認について以下の順に解説する。

  #. :ref:`フォームの作成<project_update-create_form>`
  #. :ref:`更新画面を表示する業務アクションメソッドの作成<project_update-create_edit_action>`
  #. :ref:`更新画面のJSPの作成<project_update-create_update_jsp>`
  #. :ref:`更新内容の確認を行う業務アクションメソッドの作成<project_update-create_confirm_action>`
  #. :ref:`更新確認画面のJSPの作成<project_update-create_confirm_jsp>`

.. _`project_update-create_form`:

フォームの作成
  詳細画面から更新画面へ遷移する際のパラメータを受け付けるフォームと、更新画面編集欄への入力値を受け付けるフォームを作成する。

  詳細画面から更新画面へ遷移する際にパラメータを受け付けるフォーム
    詳細画面から更新画面へ遷移する際にパスパラメータ(「show/:projectId」の「:projectId」部分)として渡される、
    対象のプロジェクトIDを受け付けるフォームを作成する。

    ProjectTargetForm.java
      .. code-block:: java

        public class ProjectTargetForm implements Serializable {

            /** プロジェクトID */
            @Required
            @Domain("id")
            private String projectId;

            // ゲッタ及びセッタは省略

  更新画面から入力された値を受け付けるフォーム
    更新画面から入力された、編集後の値を受け付けるフォームを作成する。

    ProjectUpdateForm.java
      .. code-block:: java

        public class ProjectUpdateForm implements Serializable {

            // 一部のみ抜粋

            /** プロジェクト名 */
            @Required
            @Domain("projectName")
            private String projectName;

            /**
             * プロジェクト名を取得する。
             *
             * @return プロジェクト名
             */
            public String getProjectName() {
                return this.projectName;
            }

            /**
             * プロジェクト名を設定する。
             *
             * @param projectName 設定するプロジェクト名
             */
            public void setProjectName(String projectName) {
                this.projectName = projectName;
            }
        }

    この実装のポイント
      * 入力項目がプロジェクト登録画面と重複しているが、
        責務配置上 :ref:`フォームはHTMLのフォーム単位で作成すべきである<application_design-form_html>` ため、プロジェクト更新画面専用のフォームを作成する。

.. _`project_update-create_edit_action`:

更新画面を表示する業務アクションメソッドの作成
  データベースから現在の情報を取得し、更新画面を表示する業務アクションメソッドを作成する。

  ProjectAction.java
    .. code-block:: java

        @InjectForm(form = ProjectTargetForm.class)
        public HttpResponse edit(HttpRequest request, ExecutionContext context) {

            // 更新処理で使用するセッション情報を削除しておく。
            SessionUtil.delete(context, "project");

            ProjectTargetForm targetForm = context.getRequestScopedVar("form");
            LoginUserPrincipal userContext = SessionUtil.get(context, "userContext");

            // 他のユーザによって対象プロジェクトが削除されている場合NoDataExceptionを送出
            ProjectDto dto = UniversalDao.findBySqlFile(ProjectDto.class, "FIND_BY_PROJECT",
                    new Object[]{targetForm.getProjectId(), userContext.getUserId()});

            // 出力情報をリクエストスコープにセット
            context.setRequestScopedVar("form", dto);

            SessionUtil.put(context, "project", BeanUtil.createAndCopy(Project.class, dto));

            return new HttpResponse("/WEB-INF/view/project/update.jsp");
        }

  この実装のポイント
    * 編集フォームに初期表示する値を取得するために、
      :java:extdoc:`UniversalDao#findBySqlFile <nablarch.common.dao.UniversalDao.findBySqlFile(java.lang.Class, java.lang.String, java.lang.Object)>`
      を使用して一意キー検索を行う。
      :ref:`テーブルをJOINした結果を取得する<universal_dao-join>` ために、検索結果はBeanで受け付ける。
      一意キー検索では、対象データが存在しない場合 :java:extdoc:`NoDataException<nablarch.common.dao.NoDataException>` を送出する。

        .. tip::
          Exampleアプリケーションでは、独自のエラー制御ハンドラを追加しているため、 :java:extdoc:`NoDataException<nablarch.common.dao.NoDataException>` が発生した場合は404エラー画面へ遷移する。
          ハンドラによるエラー制御の作成方法は、 :ref:`ハンドラで例外クラスに対応したエラーページに遷移させる <forward_error_page-handler>` を参照。

    * 編集中に他ユーザによる更新が行われる可能性を考慮し、編集開始時点のバージョン番号を用いて :ref:`楽観的ロック<universal_dao_jpa_version>` (後述)を行うため、
      編集開始時点のエンティティを :ref:`session_store` に登録する。

.. _`project_update-create_update_jsp`:

更新画面のJSPの作成
  画面の作成については、登録編の :ref:`client_create_1` にて説明済みであるため省略する。

.. _`project_update-create_confirm_action`:

更新内容の確認を行う業務アクションメソッドの作成
  更新内容をバリデーションし、確認画面を表示する業務アクションメソッドを作成する。
  :ref:`bean_validation` に加えて、業務アクションメソッド内に、データベース検索を伴うバリデーションを実装する。

  ProjectAction.java
    .. code-block:: java

      @InjectForm(form = ProjectUpdateForm.class, prefix = "form")
      @OnError(type = ApplicationException.class,
              path = "/WEB-INF/view/project/update.jsp")
      public HttpResponse confirmOfUpdate(HttpRequest request, ExecutionContext context) {
          ProjectUpdateForm form = context.getRequestScopedVar("form");

          // データベースを検索して入力されたIDを持つ顧客が存在するか確認する
          if (form.hasClientId()) {
              if (!UniversalDao.exists(Client.class, "FIND_BY_CLIENT_ID",
                      new Object[] {Integer.parseInt(form.getClientId()) })) {
                          throw new ApplicationException(
                              MessageUtil.createMessage(MessageLevel.ERROR,
                                  "errors.nothing.client", form.getClientId()));

              }
          }

          Project project = SessionUtil.get(context, "project");

          // フォームの値をセッションへ上書きする
          BeanUtil.copy(form, project);

          // 出力情報をリクエストスコープにセット
          context.setRequestScopedVar("form", BeanUtil.createAndCopy(ProjectDto.class, form));
          context.setRequestScopedVar("profit", new ProjectProfit(
                  project.getSales(),
                  project.getCostOfGoodsSold(),
                  project.getSga(),
                  project.getAllocationOfCorpExpenses()
          ));

          return new HttpResponse("/WEB-INF/view/project/confirmOfUpdate.jsp");
      }

  この実装のポイント
    * データベース検索が必要なバリデーションは業務アクションメソッドに記述する。
      データの存在確認をする場合、 :java:extdoc:`UniversalDao#exists <nablarch.common.dao.UniversalDao.exists(java.lang.Class, java.lang.String, java.lang.Object)>`
      を使用する。詳細は、 :ref:`データベース検索が必要なバリデーション<bean_validation-database_validation>` を参照。
    * 責務配置上 :ref:`フォームを直接セッションストアに格納すべきではない<session_store-form>` ため、Beanへ詰め替える。

  SQLの作成
    顧客の存在確認に使用するために、顧客IDから顧客情報を取得するSQLを作成する。

    client.sql
      .. code-block:: sql

        FIND_BY_CLIENT_ID =
        SELECT
            CLIENT_ID,
            CLIENT_NAME,
            INDUSTRY_CODE
        FROM
            CLIENT
        WHERE
            CLIENT_ID = :clientId

      この実装のポイント
        * 存在確認用のSQLはSELECT文として作成する。

.. _`project_update-create_confirm_jsp`:

更新確認画面のJSPの作成
  更新画面を使い回して、更新確認画面を作成する。

  /src/main/webapp/WEB-INF/view/project/update.jsp
    .. code-block:: jsp

      <n:form useToken="true">
        <!-- 登録内容の確認部分 -->
          <div class="title-nav page-footer">
              <!-- ページ下部のボタン部分 -->
              <div class="button-nav">
                  <n:forInputPage>
                      <!-- 入力画面向けボタン部分 -->
                  </n:forInputPage>
                  <n:forConfirmationPage>
                      <!-- 確認画面向けボタン部分 -->
                      <n:submit value = "確定" uri="/action/project/update" id="bottomSubmitButton"
                              cssClass="btn btn-raised btn-success"
                              allowDoubleSubmission="false" type="button" />
                  </n:forConfirmationPage>
              </div>
          </div>
      </n:form>

  この実装のポイント
    * 更新画面を確認画面として使い回す方法は、 :ref:`登録機能の確認画面作成<client_create_forConfirmationPage>` にて説明済みであるため省略する。
    * 二重サブミットを防ぐJavaScriptを追加するために、 :ref:`tag-submit_tag` の `allowDoubleSubmission` 属性にfalseを指定する。
      詳細は :ref:`tag-double_submission` を参照。

データベースの更新
---------------------
更新機能の実装方法のうち、更新内容の確認について以下の順に解説する。

  #. :ref:`業務アクションメソッドの作成<project_update-create_decide_action>`
  #. :ref:`更新完了画面の作成<project_update-create_success_jsp>`

.. _`project_update-create_decide_action`:

業務アクションメソッドの作成
  データベースを更新し、変更を確定する業務アクションメソッドを作成する。
  :ref:`楽観的ロック<universal_dao_jpa_version>` を行うためのエンティティ定義も合わせて解説する。

  データベース更新を行う業務アクションメソッドの作成
    データベースを更新し、完了画面表示メソッドへリダイレクトする業務アクションメソッドを作成する。

      ProjectAction.java
        .. code-block:: java

          @OnDoubleSubmission
          public HttpResponse update(HttpRequest request, ExecutionContext context) {
              Project targetProject = SessionUtil.delete(context, "project");
              UniversalDao.update(targetProject);

              return new HttpResponse("redirect://completeOfUpdate");
          }

    この実装のポイント
      * エンティティに更新したい値を設定し、 :java:extdoc:`UniversalDao#update <nablarch.common.dao.UniversalDao.update(java.lang.Object)>` を使用してデータベースを更新する。
        更新処理では楽観的ロックが実行される。
      * 二重サブミットを防止するために、 :java:extdoc:`@OnDoubleSubmission <nablarch.common.web.token.OnDoubleSubmission>` を付与する。
      * ブラウザ更新での再実行を防ぐために、レスポンスをリダイレクトする。
        リソースパスの書式については :java:extdoc:`ResourceLocator <nablarch.fw.web.ResourceLocator>` を参照。

  楽観的ロックの対象となるエンティティの作成
    :ref:`楽観的ロック<universal_dao_jpa_version>` を有効化したエンティティを作成する。

    Project.java
      .. code-block:: java

        // その他のプロパティは省略

        /** バージョン番号 */
        private Long version;

        /**
         * バージョン番号を返します。
         *
         * @return バージョン番号
         */
        @Version
        @Column(name = "VERSION", precision = 19, nullable = false, unique = false)
        public Long getVersion() {
            return version;
        }

        /**
         * バージョン番号を設定します。
         *
         * @param version バージョン番号
         */
        public void setVersion(Long version) {
            this.version = version;
        }

    この実装のポイント
      * :ref:`楽観的ロック<universal_dao_jpa_version>` を行うために、エンティティに `version` プロパティを作成し
        ゲッタに :ref:`@Version <universal_dao_jpa_version>` を付与する。

  .. _`project_update-create_complete_action`:

  完了画面を表示する業務アクションメソッドの作成
    更新メソッドのリダイレクト先となる、完了メッセージの追加と完了画面の表示を行う業務アクションメソッドを作成する。

    ProjectAction.java
      .. code-block:: java

        public HttpResponse completeOfUpdate(HttpRequest request, ExecutionContext context) {
            WebUtil.notifyMessages(context,
                    MessageUtil.createMessage(MessageLevel.INFO, "success.update.project"));
            return new HttpResponse("/WEB-INF/view/project/completeOfChange.jsp");
        }

    メッセージファイルに完了メッセージを追加
      messages.properties
        .. code-block:: jproperties

          success.update.project=プロジェクトの更新が完了しました。

  この実装のポイント
    * メッセージは :ref:`メッセージ管理<message>` を用いてプロパティファイルから読み込む。
    * 削除完了時と更新完了時に表示する画面は同一なので、出力するメッセージを出し分ける
      :java:extdoc:`WebUtil#notifyMessages <nablarch.common.web.WebUtil.notifyMessages(nablarch.fw.ExecutionContext, nablarch.core.message.Message...)>` を用いる。
    * 画面表示時のスタイルを切り替えるために、
      :java:extdoc:`MessageUtil#createMessage <nablarch.core.message.MessageUtil.createMessage(nablarch.core.message.MessageLevel, java.lang.String, java.lang.Object...)>` を用いて
      :ref:`メッセージのレベルを使い分ける<message-level>` 。

.. _`project_update-create_success_jsp`:

更新完了画面の作成
  更新完了メッセージが挿入された完了画面作成する。

  /src/main/webapp/WEB-INF/view/project/completeOfChange.jsp
    .. code-block:: jsp

      <n:form>
          <div class="title-nav">
              <h1 class="page-title">プロジェクト変更完了画面</h1>
              <div class="button-nav">
                <!-- 省略 -->
              </div>
          </div>
          <div class="message-area">
              <n:errors errorCss="message-error" infoCss="message-info"/>
          </div>
          <!-- 省略 -->
      </n:form>

  この実装のポイント
    * メッセージを表示するには :ref:`tag-errors_tag` を使用する。

更新機能の解説は以上。

:ref:`Getting Started TOPページへ <getting_started>`
