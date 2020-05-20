.. _`project_download`:

ファイルダウンロード機能の作成
==========================================
Exampleアプリケーションを元に、CSVファイルをダウンロードする機能の解説を行う。

作成する機能の説明
  1. プロジェクト一覧画面の、検索結果右横のダウンロードボタンを押下する。

    .. image:: ../images/project_download/project_download-list.png
      :scale: 80

  2. 現在の検索結果を出力したCSVファイルがダウンロードされる。

    .. image:: ../images/project_download/project_download-download.png
      :scale: 80

CSVファイルのダウンロードを行う
---------------------------------
CSVファイルをダウンロードする機能の実装方法を解説する。

プロジェクト検索機能の作成方法については、 :ref:`検索機能の作成<project_search>` を参照すること。

  #. :ref:`ダウンロードボタンの作成<project_download-download_button>`
  #. :ref:`ファイルをバインドするBeanの作成<project_download-create_bean>`
  #. :ref:`業務アクションメソッドの作成<project_upload-file_download_action>`

.. _`project_download-download_button`:

ダウンロードボタンの作成
  ファイルダウンロードメソッドへのGETリクエストを送信するリンクを配置する。

  /src/main/webapp/WEB-INF/view/project/index.jsp
    .. code-block:: jsp

      <!-- ダウンロードボタン周辺のみ記載 -->
      <div style="float:left;">
          <span class="font-group">
          検索結果
          </span>
          <span class="search-result-count">
              <c:if test="${not empty searchResult}">
                  <n:write name="searchResult.pagination.resultCount" />
              </c:if>
              <c:if test="${empty searchResult}">
                  0
              </c:if>
          </span>
          <!-- 現在の検索条件をパラメータとして設定 -->
          <c:url value="/action/project/download" var="download_uri">
              <c:param name="searchForm.clientId" value="${searchForm.clientId}"/>
              <c:param name="searchForm.clientName" value="${searchForm.clientName}"/>
              <c:param name="searchForm.projectName" value="${searchForm.projectName}"/>
              <c:param name="searchForm.projectType" value="${searchForm.projectType}"/>
              <c:forEach items="${searchForm.projectClass}" var="projectClass">
                  <c:param name="searchForm.projectClass" value="${projectClass}" />
              </c:forEach>
              <c:param name="searchForm.projectStartDateBegin" value="${searchForm.projectStartDateBegin}"/>
              <c:param name="searchForm.projectStartDateEnd" value="${searchForm.projectStartDateEnd}"/>
              <c:param name="searchForm.projectEndDateBegin" value="${searchForm.projectEndDateBegin}"/>
              <c:param name="searchForm.projectEndDateEnd" value="${searchForm.projectEndDateEnd}"/>
              <c:param name="searchForm.sortKey" value="${searchForm.sortKey}"/>
              <c:param name="searchForm.sortDir" value="${searchForm.sortDir}"/>
              <c:param name="searchForm.pageNumber" value="${searchForm.pageNumber}"/>
          </c:url>
          <n:a href="${download_uri}">
          <n:a href="download">
              <n:write name="label" />
              <n:img src="/images/download.png" alt="ダウンロード" />
          </n:a>
      </div>

.. _`project_download-create_bean`:

ファイルをバインドするBeanの作成
  ファイルの内容をバインドするBeanを作成する。

  ProjectDownloadDto.java
    .. code-block:: java

      @Csv(headers = { /** ヘッダーを記述 **/},
              properties = { /** バインド対象のプロパティ **/},
              type = Csv.CsvType.CUSTOM)
      @CsvFormat(charset = "Shift_JIS", fieldSeparator = ',',ignoreEmptyLine = true,
              lineSeparator = "\r\n", quote = '"',
              quoteMode = CsvDataBindConfig.QuoteMode.NORMAL, requiredHeader = true)
      public class ProjectDownloadDto implements Serializable {

          // 一部項目のみ抜粋。ゲッタ及びセッタは省略

          /** プロジェクト名 */
          private String projectName;

          /** プロジェクト種別 */
          private String projectType;
      }

  この実装のポイント
    * ダウンロードするCSVファイルの内容と、Beanのプロパティとの紐付けの設定は、 :java:extdoc:`@Csv<nablarch.common.databind.csv.Csv>` を使用する。
      受け付けるCSVのフォーマットの指定は、 :java:extdoc:`@CsvFormat<nablarch.common.databind.csv.CsvFormat>` を使用する。
      （ :ref:`デフォルトのフォーマットの指定<data_bind-csv_format_set>` を利用する場合は、 :java:extdoc:`@CsvFormat<nablarch.common.databind.csv.CsvFormat>` は不要）
      アノテーションの設定方法の詳細は、 :ref:`CSVファイルをJava Beansクラスにバインドする場合のフォーマット指定方法 <data_bind-csv_format-beans>` を参照。

.. _`project_upload-file_download_action`:

業務アクションメソッドの作成
  検索結果をCSVファイルに書きこむ業務アクションメソッドを作成する。

  ProjectAction.java
    .. code-block:: java

      @InjectForm(form = ProjectSearchForm.class, prefix = "searchForm", name = "searchForm")
      @OnError(type = ApplicationException.class, path = "/WEB-INF/view/project/index.jsp")
      public HttpResponse download(HttpRequest request, ExecutionContext context) {

          ProjectSearchForm searchForm = context.getRequestScopedVar("searchForm");
          ProjectSearchDto searchCondition = BeanUtil.createAndCopy(ProjectSearchDto.class, searchForm);
          LoginUserPrincipal userContext = SessionUtil.get(context, "userContext");
          searchCondition.setUserId(userContext.getUserId());

          final Path path = TempFileUtil.createTempFile();
          try (DeferredEntityList<ProjectDownloadDto> searchList = (DeferredEntityList<ProjectDownloadDto>) UniversalDao
                  .defer()
                  .findAllBySqlFile(ProjectDownloadDto.class, "SEARCH_PROJECT", searchCondition);
               ObjectMapper<ProjectDownloadDto> mapper = ObjectMapperFactory.create(ProjectDownloadDto.class,
                       TempFileUtil.newOutputStream(path))) {

              for (ProjectDownloadDto dto : searchList) {
                  mapper.write(dto);
              }
          }
          
          FileResponse response = new FileResponse(path.toFile(), true);
          response.setContentType("text/csv; charset=Shift_JIS");
          response.setContentDisposition("プロジェクト一覧.csv");

          return response;
      }

  この実装のポイント
    * 検索処理の実装方法については  :ref:`検索機能の作成：業務アクションの実装<project_search-create_action>` を参照。
    * Beanをファイルにバインドして出力するには、 :ref:`データバインド<data_bind>` が提供する、
      :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` を使用する。
    * ファイルに出力されたデータをダウンロードさせるには、 :java:extdoc:`FileResponse <nablarch.common.web.download.FileResponse>` を使用する。
      詳細は、 :ref:`データバインドをダウンロードで使用する<data_bind-file_download>` を参照。
    * 大量のデータを読み込む場合は、メモリの逼迫を防ぐために :java:extdoc:`UniversalDao#defer <nablarch.common.dao.UniversalDao.defer()>` を使用して、
      検索結果を :ref:`遅延ロード<universal_dao-lazy_load>` する。
    * レスポンスのコンテンツタイプは
      :java:extdoc:`HttpResponse#setContentType<nablarch.fw.web.HttpResponse.setContentType(java.lang.String)>` を使用して設定する。
      詳細は :ref:`汎用データフォーマットをダウンロードで使用する <data_format-file_download>` を参照。
    * ダウンロードファイルのファイル名は
      :java:extdoc:`HttpResponse#setContentDisposition<nablarch.fw.web.HttpResponse.setContentDisposition(java.lang.String)>` を使用して設定する。
      詳細は :ref:`汎用データフォーマットをダウンロードで使用する <data_format-file_download>` を参照。

ファイルダウンロード機能の解説は以上。

:ref:`Getting Started TOPページへ <getting_started>`