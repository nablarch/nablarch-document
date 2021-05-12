.. _`project_download`:

Create a File Download Function
==========================================
This section describes the function to download a CSV file, based on an example application.

Description of the function to be created
  1. Click the download button at the right side of the search results on the project list screen.

    .. image:: ../images/project_download/project_download-list.png
      :scale: 80

  2. The CSV file with the latest search results is downloaded.

    .. image:: ../images/project_download/project_download-download.png
      :scale: 80

Download the CSV file
---------------------------------
How to implement the download function of the CSV file is explained.

For how to create project search function, refer to :ref:`Create search function<project_search>`.

  #. :ref:`Create a download button<project_download-download_button>`
  #. :ref:`Create a Bean to bind a file<project_download-create_bean>`
  #. :ref:`Create a business action method<project_upload-file_download_action>`

.. _`project_download-download_button`:

Create a download button
  Configure a link that sends a GET request to the file download method.

  /src/main/webapp/WEB-INF/view/project/index.jsp
    .. code-block:: jsp

      <!-- Only the surrounding of the download button is described -->
      <div style="float:left;">
          <span class="font-group">
          Search results
          </span>
          <span class="search-result-count">
              <c:if test="${not empty searchResult}">
                  <n:write name="searchResult.pagination.resultCount" />
              </c:if>
              <c:if test="${empty searchResult}">
                  0
              </c:if>
          </span>
          <!-- Configure the current search condition as a parameter -->
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
              <n:write name="label" />
              <n:img src="/images/download.png" alt="Download" />
          </n:a>
      </div>

.. _`project_download-create_bean`:

Create a Bean to bind a file
  A bean to bind the contents of the file is created.

  ProjectDownloadDto.java
    .. code-block:: java

      @Csv(headers = { /** Describe the header **/},
              properties = { /** Properties to bind **/},
              type = Csv.CsvType.CUSTOM)
      @CsvFormat(charset = "Shift_JIS", fieldSeparator = ',',ignoreEmptyLine = true,
              lineSeparator = "\r\n", quote = '"',
              quoteMode = CsvDataBindConfig.QuoteMode.NORMAL, requiredHeader = true, emptyToNull = true)
      public class ProjectDownloadDto implements Serializable {

          // Excerpt of some items only. Getter and setter are omitted

          /** Project name */
          private String projectName;

          /** Project type */
          private String projectType;
      }

  Key points of this implementation
    * Use :java:extdoc:`@Csv<nablarch.common.databind.csv.Csv>` to configure the association between the contents of the downloaded CSV fie and Bean properties.
      Use :java:extdoc:`@CsvFormat<nablarch.common.databind.csv.CsvFormat>` to specify the acceptable CSV format.
      （:java:extdoc:`@CsvFormat<nablarch.common.databind.csv.CsvFormat>` is not required when using the :ref:`default format specification<data_bind-csv_format_set>`）
      For information on how to configure the annotation, refer to :ref:`format specification method when binding the CSV file to the Java Beans <data_bind-csv_format-beans>`.

.. _`project_upload-file_download_action`:

Create a business action method
  Create a business action method to write the search results to a CSV file.

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
          response.setContentDisposition("Project List.csv");

          return response;
      }

  Key points of this implementation
    * For implementation method of the search process, refer to :ref:`create search function: Business action implementation<project_search-create_action>`.
    * To bind the bean to a file and generate an output, use :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>`
      provided by :ref:`Data bind <data_bind>`.
    * To download the data output to a file, use :java:extdoc:`FileResponse <nablarch.common.web.download.FileResponse>`.
      For more information, see :ref:`Use data binding for download<data_bind-file_download>`.
    * When reading a large amount of data, to prevent straining of the memory, use :java:extdoc:`UniversalDao#defer <nablarch.common.dao.UniversalDao.defer()>`
      for :ref:`deferred loading<universal_dao-lazy_load>` of the search results.
    * Configure the response content type using
      :java:extdoc:`HttpResponse#setContentType<nablarch.fw.web.HttpResponse.setContentType(java.lang.String)>`.
      For more information, see :ref:`Use general data format for downloads <data_format-file_download>`.
    * Configure the file name of the downloaded file using
      :java:extdoc:`HttpResponse#setContentDisposition<nablarch.fw.web.HttpResponse.setContentDisposition(java.lang.String)>`.
      For more information, see :ref:`Use general data format for downloads <data_format-file_download>`.

This completes the description of the file download function.

:ref:`Getting Started To TOP page <getting_started>`