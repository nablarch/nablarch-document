.. _`project_bulk_update`:

一括更新機能の作成
==========================================
Exampleアプリケーションを元に一括更新機能の解説を行う。

作成する機能の説明
  1. メニューの一括更新リンクを押下し、一括更新画面へ遷移する。

    .. image:: ../images/project_bulk_update/project_bulk_update-menu.png
      :scale: 80

  2. プロジェクト全件検索の結果が表示される。

    .. image:: ../images/project_bulk_update/project_bulk_update-list.png
      :scale: 80

  3. 当該ページで更新する項目を書き換えて、更新ボタンを押下する(ページをまたいだ更新はできない)。

    .. image:: ../images/project_bulk_update/project_bulk_update-list_changed.png
      :scale: 80

  4. 更新確認画面が表示されるので、確定ボタンを押下する。

    .. image:: ../images/project_bulk_update/project_bulk_update-confirm.png
      :scale: 80

  5. データベースが更新され、更新完了画面が表示される。

    .. image:: ../images/project_bulk_update/project_bulk_update-complete.png
      :scale: 80

一括更新機能の作成
---------------------
一括更新機能の作成方法を解説する。

  #. :ref:`フォームの作成<project_bulk_update-create_form>`
  #. :ref:`画面に更新対象を受け渡すBeanの作成<project_bulk_update-create_bean>`
  #. :ref:`一括更新画面を表示する業務アクションメソッドの作成<project_bulk_update-action_list>`
  #. :ref:`一括更新画面JSPの作成<project_bulk_update-update_jsp>`
  #. :ref:`更新内容を確認する業務アクションメソッドの作成<project_bulk_update-confirm_action>`
  #. :ref:`確認画面JSPの作成<project_bulk_update-confirm_jsp>`
  #. :ref:`データベースを一括更新する業務アクションメソッドの作成<project_bulk_update-bulk_update>`
  #. :ref:`完了画面の作成<project_bulk_update-complete_jsp>`

.. _`project_bulk_update-create_form`:

フォームの作成
  検索条件を受け付けるフォームと、更新内容を受け付けるフォームをそれぞれ作成する。

  検索フォームの作成
    検索フォームの実装は、 :ref:`検索機能の作成：フォームの作成<project_search-create_form>` と同様であるためそちらを参照。

  更新フォームの作成
    複数のプロジェクトの更新情報を一括で送信するため、フォームを2種類作成する。

      #. :ref:`プロジェクト一つ分の更新情報を受け付けるフォーム<project_bulk_update-create_single_pj_form>`
      #. :ref:`プロジェクト一つ分のフォームのリストをプロパティとして持つ親フォーム<project_bulk_update-create_multi_pj_form>`

        .. image:: ../images/project_bulk_update/project_bulk_update-form.png

    .. _`project_bulk_update-create_single_pj_form`:

    プロジェクト一つ分の更新情報を受け付けるフォーム
      プロジェクト一つ分の更新値を受け付けるフォームを作成する。

        InnerProjectForm.java
          .. code-block:: java

            public class InnerProjectForm implements Serializable {

                // 一部項目のみ抜粋

                /** プロジェクト名 */
                @Required
                @Domain("projectName")
                private String projectName;

                // ゲッタ及びセッタは省略
            }

      この実装のポイント
        * 入れ子となったフォームに対しても  :ref:`Bean Validation<bean_validation>` を実行するため、
          :java:extdoc:`@Required<nablarch.core.validation.ee.Required>` や :java:extdoc:`@Domain<nablarch.core.validation.ee.Domain>`
          などのバリデーション用のアノテーションを付与する。

    .. _`project_bulk_update-create_multi_pj_form`:

    プロジェクト一つ分のフォームのリストをプロパティとして持つ親フォーム
      複数プロジェクトの更新情報を一括で受け付けるために、プロジェクト一つ分の更新情報を受け付けるフォームのリストを定義した親フォームを作成する。

      ProjectBulkForm.java
        .. code-block:: java

          public class ProjectBulkForm implements Serializable {

              /** プロジェクト情報のリスト */
              @Valid
              private List<InnerProjectForm> projectList = new ArrayList<>();

              // ゲッタ及びセッタは省略
          }

      この実装のポイント
        * :java:extdoc:`@Valid<javax.validation.Valid>` を付与することで、入れ子としたフォームも :ref:`Bean Validation<bean_validation>` の対象に含めることができる。

.. _`project_bulk_update-create_bean`:

業務アクションで取得した更新対象リストを画面へ受け渡すBeanの作成
  業務アクションで取得した更新対象リストを画面へ受け渡すBeanを作成する。このBeanは一括更新画面と確認画面で持ちまわすため、 :ref:`セッションストア <session_store>` に登録する。

    ProjectListDto.java
      .. code-block:: java

        public class ProjectListDto implements Serializable {

            /** プロジェクトリスト */
            private List<Project> projectList = new ArrayList<>();

            // ゲッタ及びセッタは省略
        }

    この実装のポイント
      * 配列やコレクション型を :ref:`セッションストア <session_store>` に登録する場合は、シリアライズ可能なBeanのプロパティとして定義し、
        そのBeanを :ref:`セッションストア <session_store>` に登録すること。詳細は :ref:`セッションストア使用上の制約<session_store-constraint>` を参照。

.. _`project_bulk_update-action_list`:

一括更新画面を表示する業務アクションメソッドの作成
  データベースから対象プロジェクトを取得し、一括更新画面に表示する業務アクションメソッドを作成する。

  ProjectBulkAction.java
    .. code-block:: java

      @InjectForm(form = ProjectSearchForm.class, prefix = "searchForm",  name = "searchForm")
      @OnError(type = ApplicationException.class, path = "forward://initialize")
      public HttpResponse list(HttpRequest request, ExecutionContext context) {

          ProjectSearchForm searchForm = context.getRequestScopedVar("searchForm");

          // 検索実行
          ProjectSearchDto projectSearchDto
              = BeanUtil.createAndCopy(ProjectSearchDto.class, searchForm);
          EntityList<Project> projectList = searchProject(projectSearchDto, context);
          ProjectListDto projectListDto = new ProjectListDto();
          projectListDto.setProjectList(projectList);
          SessionUtil.put(context, "projectListDto", projectListDto);

          // 更新対象を画面に引き渡す
          context.setRequestScopedVar("bulkForm", projectListDto);

          // 検索条件を保存
          SessionUtil.put(context, "projectSearchDto", projectSearchDto);

          return new HttpResponse("/WEB-INF/view/projectBulk/update.jsp");
      }

  この実装のポイント
    * 検索メソッドの実装方法に関しては :ref:`検索機能の作成：業務アクションの実装<project_search-create_action>` と同様であるためそちらを参照。
    * 確認画面から一括更新画面へ戻った際に、同条件でページングや再検索ができるように
      検索条件を :ref:`セッションストア <session_store>` に登録して持ちまわす。

.. _`project_bulk_update-update_jsp`:

一括更新画面JSPの作成
  検索結果の表示と複数のプロジェクトの情報の編集を行う、一括更新画面のJSPを作成する。

  /src/main/webapp/WEB-INF/projectBulk/update.jsp
    .. code-block:: jsp

      <!-- 顧客検索結果の表示部分 -->
      <n:form>
          <!-- 現在の検索結果の表示に使用した検索条件をパラメータとして持つURIを、
               変数としてpageスコープに登録する。
               この変数は、<app:listSearchResult>タグのページング用のURIとして使用される。-->
          <c:url value="list" var="uri">
              <!-- セッションストア上のprojectSearchDtoから検索条件を取得する -->
              <c:param name="searchForm.clientId" value="${projectSearchDto.clientId}"/>
              <c:param name="searchForm.clientName" value="${projectSearchDto.clientName}"/>
              <c:param name="searchForm.projectName" value="${projectSearchDto.projectName}"/>
              <!-- 以降も同様に検索条件パラメータであるため省略 -->

          </c:url>
          <app:listSearchResult>
          <!-- listSearchResultの属性値は省略 -->
              <jsp:attribute name="headerRowFragment">
                  <tr>
                      <th>プロジェクトID</th>
                      <th>プロジェクト名</th>
                      <th>プロジェクト種別</th>
                      <th>開始日</th>
                      <th>終了日</th>
                  </tr>
              </jsp:attribute>
              <jsp:attribute name="bodyRowFragment">
                  <tr class="info">
                      <td>
                          <!-- プロジェクトIDをパラメータとするリンクを表示する -->
                          <n:a href="show/${row.projectId}">
                              <n:write name="bulkForm.projectList[${status.index}].projectId"/>
                          </n:a>
                          <n:plainHidden name="bulkForm.projectList[${status.index}].projectId"/>
                      </td>
                      <td>
                          <div class="form-group">
                              <n:text name="bulkForm.projectList[${status.index}].projectName"
                                      maxlength="64" cssClass="form-control"
                                      errorCss="input-error input-text"/>
                              <n:error errorCss="message-error"
                                      name="bulkForm.projectList[${status.index}].projectName" />
                          </div>
                      </td>
                      <!-- その他の編集項目は省略 -->

                  </tr>
              </jsp:attribute>
          </app:listSearchResult>
          <div class="title-nav page-footer">
              <div class="button-nav">
                  <n:button id="bottomUpdateButton" uri="/action/projectBulk/confirmOfUpdate"
                      disabled="${isUpdatable}" cssClass="btn btn-raised btn-success">
                          更新</n:button>
                  <n:a id="bottomCreateButton" type="button" uri="/action/project"
                      cssClass="btn btn-raised btn-default" value="新規登録"></n:a>
              </div>
          </div>
      </n:form>

  この実装のポイント
    * 検索結果を表示するJSPの作成方法は :ref:`検索機能の作成：検索結果表示部分の作成<project_search-create_result_jsp>` と同様であるため、そちらを参照。
    * 確認画面から一括更新画面に戻った際に、同条件での再検索やページングが行えるように、 :ref:`セッションストア <session_store>` から取得した検索条件を元に検索条件パラメータを構成する。
      JSPでは、 :ref:`セッションストア <session_store>` に登録したオブジェクトは、リクエストスコープに登録したオブジェクトと同様に扱うことができる。
    * 配列型、もしくは :java:extdoc:`List<java.util.List>` 型プロパティの要素は、 `プロパティ名[index]` 形式でアクセスできる。
      詳細は :ref:`tag-access_rule` 参照。

.. _`project_bulk_update-confirm_action`:

更新内容の確認を行う業務アクションメソッドの作成
  更新内容の確認を行う業務アクションメソッドを作成する。

  ProjectBulkAction.java
    .. code-block:: java

      @InjectForm(form = ProjectBulkForm.class, prefix = "bulkForm", name = "bulkForm")
      @OnError(type = ApplicationException.class, path = "/WEB-INF/view/projectBulk/update.jsp")
      public HttpResponse confirmOfUpdate(HttpRequest request, ExecutionContext context) {

          ProjectBulkForm form = context.getRequestScopedVar("bulkForm");
          ProjectListDto dto = SessionUtil.get(context, "projectListDto");

          // 更新内容をセッションに上書き
          final List<InnerProjectForm> innerForms = form.getProjectList();
          dto.getProjectList()
             .forEach(project ->
                     innerForms.stream()
                               .filter(innerForm ->
                                       Objects.equals(innerForm.getProjectId(), project.getProjectId()
                                                                                       .toString()))
                               .findFirst()
                               .ifPresent(innerForm -> BeanUtil.copy(innerForm, project)));

          return new HttpResponse("/WEB-INF/view/projectBulk/confirmOfUpdate.jsp");
      }

  この実装のポイント
    * 更新する情報は :ref:`セッションストア <session_store>` に保持する。

.. _`project_bulk_update-confirm_jsp`:

確認画面JSPの作成
  変更後のプロジェクト情報を表示する画面のJSPを作成する。

  /src/main/webapp/WEB-INF/projectBulk/confirmOfUpdate.jsp
    .. code-block:: jsp

          <section>
              <div class="title-nav">
                  <span>プロジェクト検索一覧更新画面</span>
                  <div class="button-nav">
                      <n:form useToken="true">
                        <!-- ボタン部分は省略 -->
                      </n:form>
                  </div>
              </div>
              <h4 class="font-group">プロジェクト変更一覧</h4>
              <div>
                  <table class="table table-striped table-hover">
                      <tr>
                          <th>プロジェクトID</th>
                          <th>プロジェクト名</th>
                          <th>プロジェクト種別</th>
                          <th>開始日</th>
                          <th>終了日</th>
                      </tr>
                      <c:forEach var="row" items="${projectListDto.projectList}">
                          <tr class="<n:write name='oddEvenCss' />">
                              <td>
                                  <n:write name="row.projectId" />
                              </td>
                              <!-- 他項目は省略 -->
                          </tr>
                      </c:forEach>
                  </table>
              </div>
          </section>

.. _`project_bulk_update-bulk_update`:

データベースを一括更新する業務アクションメソッドの作成
  対象プロジェクトを一括で更新する。

  ProjectBulkAction.java
    .. code-block:: java

      @OnDoubleSubmission
      public HttpResponse update(HttpRequest request, ExecutionContext context) {

        ProjectListDto projectListDto = SessionUtil.get(context, "projectListDto");
        projectListDto.getProjectList().forEach(UniversalDao::update);

        return new HttpResponse("redirect://completeOfUpdate");
      }

  この実装のポイント
    * 基本的な実装方法は  :ref:`更新機能の作成：データベースを更新する業務アクションメソッドの作成<project_update-create_decide_action>` と同様である。
    * :java:extdoc:`UniversalDao#update <nablarch.common.dao.UniversalDao.update(java.lang.Object)>` を更新件数分実行する。
      排他制御エラーが発生した場合は全件の更新がロールバックされる。

      .. tip::
        Exampleアプリケーションでは独自のエラー制御ハンドラを追加しているため、排他制御エラーにより :java:extdoc:`OptimisticLockException<javax.persistence.OptimisticLockException>` が発生した場合、
        排他制御エラー画面へ遷移する。ハンドラによるエラー制御の作成方法は、 :ref:`ハンドラで例外クラスに対応したエラーページに遷移させる <forward_error_page-handler>` を参照。

    * :java:extdoc:`UniversalDao<nablarch.common.dao.UniversalDao>` には、エンティティのリストを引数に取る
      :java:extdoc:`UniversalDao#batchUpdate <nablarch.common.dao.UniversalDao.batchUpdate(java.util.List)>` メソッドも用意されているが、
      このメソッドは :ref:`バッチ実行<universal_dao-batch_execute>` での使用を想定したものであり、排他制御を行わない。
      排他制御が必要である場合は、 :java:extdoc:`UniversalDao#update <nablarch.common.dao.UniversalDao.update(java.lang.Object)>`
      を使用すること。

.. _`project_bulk_update-complete_jsp`:

完了画面の表示
  完了画面の実装方法は :ref:`更新機能の作成：更新完了画面の作成<project_update-create_success_jsp>` と同様であるためそちらを参照。

一括更新機能の解説は以上。

:ref:`Getting Started TOPページへ <getting_started>`