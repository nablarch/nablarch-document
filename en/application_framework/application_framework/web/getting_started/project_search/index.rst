.. _`project_search`:

Create a Search Function
==========================================
This section describes the search function based on an example application.

Description of the function to be created
  1. Enter the search condition in the "Project Name(プロジェクト名)" field of the side menu and click the "Search(検索)" button.

    .. image:: ../images/project_search/project_search_sidemenu.png
      :scale: 60

  2. The search results by project name are displayed.

    .. image:: ../images/project_search/project_search_search_with_condition.png
      :scale: 80

  3. Clear the project name and click on the "Start this year(今年開始)" link in the "Search by period(期間からさがす)" column.

    .. image:: ../images/project_search/project_search_start_date.png
          :scale: 60

  4. Projects with a project start date of this year are displayed.

    .. image:: ../images/project_search/project_search_start_date_result.png
      :scale: 80

Perform a search
-----------------

The basic implementation method of the search function is described in the following order:

  #. :ref:`Create a form<project_search-create_form>`
  #. :ref:`Create a JSP for the search condition input<project_search-create_jsp>`
  #. :ref:`Create a search condition bean<project_search-create_bean>`
  #. :ref:`Create a SQL for search<project_search-create_sql>`
  #. :ref:`Implementation of a business action<project_search-create_action>`
  #. :ref:`Create a search result display part<project_search-create_result_jsp>`

.. _`project_search-create_form`:

Create a form
  Create a form that accepts the search condition.

  ProjectSearchForm.java
    .. code-block:: java

      public class ProjectSearchForm extends SearchFormBase implements Serializable {

          // Partial excerpt

          /** Project name */
          @Domain("projectName")
          private String projectName;

          /** Project start date (FROM) */
          @Domain("date")
          private String projectStartDateBegin;

          // Getter and setter are omitted

  Key points of this implementation
    * All properties that accept input values should be declared as string type. For more information, see :ref:`how to set validation rules <bean_validation-form_property>`.

.. _`project_search-create_jsp`:

Create a JSP for the search condition input
  Creates a JSP for the search condition input.

  /src/main/webapp/WEB-INF/view/common/sidemenu.jsp
    .. code-block:: jsp

      <n:form method="GET" action="list">
          <!-- Omitted -->
          <label for="projectName" class="control-label">Project name</label>
          <div>
              <n:text
                      id="projectName"
                      name="searchForm.projectName"
                      size="25"
                      maxlength="64"
                      cssClass="form-control"
                      errorCss="input-error form-control"
                      placeholder="Project name"/>
              <n:error errorCss="message-error" name="searchForm.projectName" />
          </div>
          <!-- Omitted -->
          <div align="center">
              <input type="submit" id="search" class="btn btn-primary" value="Search" />
          </div>
      </n:form>

    Key points of this implementation
      * When sending a request by GET, specify GET in the `method` attribute of :ref:`tag-form_tag`.
        In the case of GET, custom tags cannot be used for buttons and links, so the buttons and links must be created in HTML. For more information, see :ref:`tag-using_get`.

.. _`project_search-create_bean`:

Create a search condition bean
  Creates a bean that sets the search conditions and hands over to :ref:`universal_dao`.
  Bean property should be of the :ref:`type that is compatible with the definition (type) of the corresponding condition column<universal_dao-search_with_condition>`.

  ProjectSearchDto.java
    .. code-block:: java

      public class ProjectSearchDto implements Serializable {

          // Partial excerpt

          /** Project name */
          private String projectName;

          /** Project start date (FROM) */
          private java.sql.Date projectStartDateBegin;

          // Getter and setter are omitted

    Key points of this implementation
      * Use :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` to transfer values from the form to search condition Bean.
        Since :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` transfers items with the same property name,
        it is necessary to match the property names of the items used as search conditions in the form and search condition Bean.
      * When values are transferred using :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` the property can be transferred with a type conversion for properties that are compatible.
        For more information, see :ref:`type conversion rules<utility-conversion>`.
      * Bean property is defined by Java type that matches the corresponding column type.

.. _`project_search-create_sql`:

Create a SQL for search
  Create a SQL for searching.

    Project.sql
      .. code-block:: none

        SEARCH_PROJECT =
        SELECT
            PROJECT_ID,
            PROJECT_NAME,
            PROJECT_TYPE,
            PROJECT_CLASS,
            PROJECT_START_DATE,
            PROJECT_END_DATE,
            VERSION
        FROM
            PROJECT
        WHERE
            USER_ID = :userId
            AND $if(clientId)     {CLIENT_ID = :clientId}
            AND $if(projectName) {PROJECT_NAME LIKE  :%projectName%}
            AND $if(projectType) {PROJECT_TYPE = :projectType}
            AND $if(projectClass) {PROJECT_CLASS IN (:projectClass[])}
            AND $if(projectStartDateBegin) {PROJECT_START_DATE >= :projectStartDateBegin}
            AND $if(projectStartDateEnd) {PROJECT_START_DATE <= :projectStartDateEnd}
            AND $if(projectEndDateBegin) {PROJECT_END_DATE >= :projectEndDateBegin}
            AND $if(projectEndDateEnd) {PROJECT_END_DATE <= :projectEndDateEnd}
        $sort(sortId){
            (idAsc PROJECT_ID)
            (idDesc PROJECT_ID DESC)
            (nameAsc PROJECT_NAME, PROJECT_ID)
            (nameDesc PROJECT_NAME DESC, PROJECT_ID DESC)
            (startDateAsc PROJECT_START_DATE, PROJECT_ID)
            (startDateDesc PROJECT_START_DATE DESC, PROJECT_ID DESC)
            (endDateAsc PROJECT_END_DATE, PROJECT_ID)
            (endDateDesc PROJECT_END_DATE DESC, PROJECT_ID DESC)
        }

    Key points of this implementation
      * To prevent SQL injection, SQL is written in an external file. For more information, see :ref:`database-use_sql_file`.
      * Bind the value to SQL using the bean property name. For more information, see :ref:`database-input_bean`.
      * To include only the items specified on the search screen in the conditions, :ref:`build a SQL statement using the $if syntax<database-use_variable_condition>`.
      * To make the sort key selectable from the screen, use the :ref:`$sort syntax to construct an SQL statement<database-make_order_by>`.

.. _`project_search-create_action`:

Implementation of a business action
  Implement a search process for a business action.

  Create a business action method
    Create a method to search based on the search conditions given on the screen.

    ProjectAction.java
      .. code-block:: java

          @InjectForm(form = ProjectSearchForm.class, prefix = "searchForm", name = "searchForm")
          @OnError(type = ApplicationException.class, path = "/WEB-INF/view/project/index.jsp")
          public HttpResponse list(HttpRequest request, ExecutionContext context) {

              ProjectSearchForm searchForm = context.getRequestScopedVar("searchForm");
              ProjectSearchDto searchCondition =
                      BeanUtil.createAndCopy(ProjectSearchDto.class, searchForm);

              List<Project> searchList = searchProject(searchCondition, context);
              context.setRequestScopedVar("searchResult", searchList);

              return new HttpResponse("/WEB-INF/view/project/index.jsp");
          }

    Key points of this implementation
      * The search condition is validated by adding
        :java:extdoc:`InjectForm <nablarch.common.web.interceptor.InjectForm>` as the search condition is not guaranteed to be safe with input values from outside.
      * Form validated by :java:extdoc:`InjectForm <nablarch.common.web.interceptor.InjectForm>`
        can be acquired from the request scope.
      * Copies the form value to the search condition bean using :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>`.

  Create a private method to perform a search
    This method searches the database by specifying the SQL mentioned above.

      ProjectAction.java
        .. code-block:: java

          private List<Project> searchProject(ProjectSearchDto searchCondition,
                                              ExecutionContext context) {

              LoginUserPrincipal userContext = SessionUtil.get(context, "userContext");
              searchCondition.setUserId(userContext.getUserId());

              return UniversalDao
                      .page(searchCondition.getPageNumber())
                      .per(20L)
                      .findAllBySqlFile(Project.class, "SEARCH_PROJECT", searchCondition);
          }

      Key points of this implementation
        * To execute the preceding SQL statement, specify :ref:`SQLID <database-execute_sqlid>` (or "SEARCH_PROJECT" in the case of the preceding SQL) as the second argument of
          :java:extdoc:`UniversalDao#findAllBySqlFile <nablarch.common.dao.UniversalDao.findAllBySqlFile(java.lang.Class-java.lang.String-java.lang.Object)>`.
        * Search for paging can be performed using the :java:extdoc:`UniversalDao#per <nablarch.common.dao.UniversalDao.per(long)>` method and
          :java:extdoc:`UniversalDao#page <nablarch.common.dao.UniversalDao.page(long)>`.
          For more information, see :ref:`narrow the search for paging<universal_dao-paging>`.

.. _`project_search-create_result_jsp`:

Create a search result display part
  Implements the process to display the search results registered in the request scope on the screen in JSP.

  /src/main/webapp/WEB-INF/view/project/index.jsp
    .. code-block:: jsp

      <!-- Search result -->
      <app:listSearchResult>
      <!-- Attribute value specification of app:listSearchResult is omitted -->
      <!-- Omitted -->
          <jsp:attribute name="headerRowFragment">
              <tr>
                  <th>Project ID</th>
                  <th>Project name</th>
                  <th>Project type</th>
                  <th>Project start date</th>
                  <th>Project end date</th>
              </tr>
          </jsp:attribute>
          <jsp:attribute name="bodyRowFragment">
              <tr class="info">
                  <td>
                      <!-- Create the URL to which the project ID was added -->
                      <!-- Transition to the project detail screen -->
                      <n:a href="show/${row.projectId}">
                          <n:write name="row.projectId"/>
                      </n:a>
                  </td>
                  <!-- Omitted -->
                  <td>
                      <n:write name="row.projectName" />
                  </td>
                  <!-- Omitted -->
                  <td>
                      <n:write name="row.projectStartDate" valueFormat="dateTime{yyyy/MM/dd}"/>
                  </td>
                  <!-- Omitted -->
              </tr>
          </jsp:attribute>
      </app:listSearchResult>

  Key points of this implementation
    * To include a parameter in the URL of the GET request, such as a link to the detail screen, create using `<c:url>` tag of JSTL or EL expression.
    * Since the routing is configured as follows in the Example application, a URL with a project ID at the end is associated with "`ProjectAction#show`".
      For more information, see `library README documentation (external site) <https://github.com/kawasima/http-request-router/blob/master/README.ja.md>`_ .

      routes.xml
        .. code-block:: xml

          <routes>
                <match path="/action/:controller/:action/:projectId">
                    <requirements>
                        <requirement name="projectId" value="\d+$" />
                    </requirements>
                </match>
            <!-- Other settings are omitted -->
          </routes>

    * The :ref:`tag-write_tag` is used to output the value.
      To output the value in a format such as "date" or "amount", specify the format with the `valueFormat` attribute. For more information, see :ref:`tag-format_value`.
    * For information on how to use `<app:listSearchResult>`, see :ref:`list_search_result`.

This completes the description of the search function.

:ref:`Getting Started To TOP page <getting_started>`
