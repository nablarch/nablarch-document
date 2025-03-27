.. _`project_bulk_update`:

Create a batch update function
==========================================
This section describes the batch update function based on an example application.

Description of the function to be created
  1. Click on the batch update (プロジェクト一括更新)link on the menu for transition to the batch update screen.

    .. image:: ../images/project_bulk_update/project_bulk_update-menu.png
      :scale: 80

  2. Results of all project searches are displayed.

    .. image:: ../images/project_bulk_update/project_bulk_update-list.png
      :scale: 80

  3. Rewrite the item to be updated on the relevant page and click the update(更新) button (update across pages is not possible).

    .. image:: ../images/project_bulk_update/project_bulk_update-list_changed.png
      :scale: 80

  4. When the update confirmation screen is displayed, click on the confirm(確定) button.

    .. image:: ../images/project_bulk_update/project_bulk_update-confirm.png
      :scale: 80

  5. The database is updated and the update completion screen is displayed.

    .. image:: ../images/project_bulk_update/project_bulk_update-complete.png
      :scale: 80

Create a batch update function
-------------------------------
Describes how to create a bulk update feature.

  #. :ref:`Create a form<project_bulk_update-create_form>`
  #. :ref:`Create a bean to pass the update target to the screen<project_bulk_update-create_bean>`
  #. :ref:`Create a business action method to display the batch update screen<project_bulk_update-action_list>`
  #. :ref:`Create a batch update screen JSP<project_bulk_update-update_jsp>`
  #. :ref:`Create a business action method to check the update content<project_bulk_update-confirm_action>`
  #. :ref:`Create a confirmation screen JSP<project_bulk_update-confirm_jsp>`
  #. :ref:`Create a business action method that updates the database in a batch<project_bulk_update-bulk_update>`
  #. :ref:`Create the completion screen<project_bulk_update-complete_jsp>`

.. _`project_bulk_update-create_form`:

Create a form
  Create a form to accept search condition and to accept update contents respectively.

  Create a search form
    Refer to :ref:`create search function：Form creation<project_search-create_form>` as the same implementation can be used for the search form.

  Create an update form
    Create two types of forms as the update information of multiple projects is sent in a batch.

      #. :ref:`A form to accept updates for one project<project_bulk_update-create_single_pj_form>`
      #. :ref:`Parent form with a list of forms as properties for a single project<project_bulk_update-create_multi_pj_form>`

        .. image:: ../images/project_bulk_update/project_bulk_update-form.png

    .. _`project_bulk_update-create_single_pj_form`:

    A form to accept updates for one project
      Create a form that accepts the update value for one project.

        InnerProjectForm.java
          .. code-block:: java

            public class InnerProjectForm implements Serializable {

                // Excerpt of some items only

                /** Project name */
                @Required
                @Domain("projectName")
                private String projectName;

                // Getter and setter are omitted
            }

      Key points of this implementation
        * Since :ref:`Bean Validation<bean_validation>` is executed even for nested forms, assign annotations for validations such as
          :java:extdoc:`@Required<nablarch.core.validation.ee.Required>` and :java:extdoc:`@Domain<nablarch.core.validation.ee.Domain>`.


    .. _`project_bulk_update-create_multi_pj_form`:

    Parent form with a list of forms as properties for a single project
      To receive updated information of multiple projects in a batch, create a parent form that defines a list of forms to receive update information for one project.

      ProjectBulkForm.java
        .. code-block:: java

          public class ProjectBulkForm implements Serializable {

              /** List of project information */
              @Valid
              private List<InnerProjectForm> projectList = new ArrayList<>();

              // Getter and setter are omitted
          }

      Key points of this implementation
        * By assigning :java:extdoc:`@Valid<jakarta.validation.Valid>`, nested forms can also be included as targets of :ref:`Bean Validation<bean_validation>`.

.. _`project_bulk_update-create_bean`:

Create a bean that delivers the update target list acquired with business action to the screen.
  Creates a bean that delivers the update target list acquired with business action to the screen. This bean is registered in the :ref:`session store <session_store>` to be carried through the batch update and confirmation screen.

    ProjectListDto.java
      .. code-block:: java

        public class ProjectListDto implements Serializable {

            /** Project list */
            private List<Project> projectList = new ArrayList<>();

            // Getter and setter are omitted
        }

    Key points of this implementation
      * When registering array or collection type in the :ref:`session store <session_store>`, it is defined as a serializable Bean property and that Bean is registered
        in the :ref:`session store <session_store>`. For more information, see :ref:`restrictions on the use of the session store<session_store-constraint>`.

.. _`project_bulk_update-action_list`:

Create a business action method to display the batch update screen
  Acquire the target project from the database and create a business action method to be displayed on the batch update screen.

  ProjectBulkAction.java
    .. code-block:: java

      @InjectForm(form = ProjectSearchForm.class, prefix = "searchForm",  name = "searchForm")
      @OnError(type = ApplicationException.class, path = "forward://initialize")
      public HttpResponse list(HttpRequest request, ExecutionContext context) {

          ProjectSearchForm searchForm = context.getRequestScopedVar("searchForm");

          // Search execution
          ProjectSearchDto projectSearchDto
              = BeanUtil.createAndCopy(ProjectSearchDto.class, searchForm);
          EntityList<Project> projectList = searchProject(projectSearchDto, context);
          ProjectListDto projectListDto = new ProjectListDto();
          projectListDto.setProjectList(projectList);
          SessionUtil.put(context, "projectListDto", projectListDto);

          // Pass the update target to the screen
          context.setRequestScopedVar("bulkForm", projectListDto);

          // Save the search criteria
          SessionUtil.put(context, "projectSearchDto", projectSearchDto);

          return new HttpResponse("/WEB-INF/view/projectBulk/update.jsp");
      }

  Key points of this implementation
    * Refer to :ref:`create search function：Business action implementation<project_search-create_action>` as the same implementation method can be used for the search method.
    * When returning to the batch update screen from the confirmation screen, register and carry out the search conditions
      in the :ref:`session store <session_store>` so that paging and re-search is enabled under the same conditions.

.. _`project_bulk_update-update_jsp`:

Create a batch update screen JSP
  Create a JSP for batch update screen that displays the search results and compiles information of multiple projects.

  /src/main/webapp/WEB-INF/projectBulk/update.jsp
    .. code-block:: jsp

      <!-- Display section of customer search result -->
      <n:form>
          <!-- Register the URI containing the search conditions used to display the current search results as a
               variable in the page scope as a variable.
               This variable is used as URI for the paging of <app:listSearchResult> tag. -->
          <c:url value="list" var="uri">
              <!-- Acquire search criteria from projectSearchDto of the session store -->
              <c:param name="searchForm.clientId" value="${projectSearchDto.clientId}"/>
              <c:param name="searchForm.clientName" value="${projectSearchDto.clientName}"/>
              <c:param name="searchForm.projectName" value="${projectSearchDto.projectName}"/>
              <!--  Omitted as it is a search condition parameter as well -->

          </c:url>
          <app:listSearchResult>
          <!-- Attribute values of listSearchResult are omitted  -->
              <jsp:attribute name="headerRowFragment">
                  <tr>
                      <th>Project ID</th>
                      <th>Project name</th>
                      <th>Project type</th>
                      <th>Start date</th>
                      <th>End date</th>
                  </tr>
              </jsp:attribute>
              <jsp:attribute name="bodyRowFragment">
                  <tr class="info">
                      <td>
                          <!-- Displays the link with project ID as a parameter -->
                          <n:a href="show/${row.projectId}">
                              <n:write name="bulkForm.projectList[${status.index}].projectId"/>
                          </n:a>
                          <n:plainHidden name="bulkForm.projectList[${status.index}].projectId"/>
                      </td>
                      <td>
                          <div class="form-group">
                              <n:text name="bulkForm.projectList[${status.index}].projectName"
                                      maxlength="64" cssClass="form-control form-control-lg"
                                      errorCss="input-error"/>
                              <n:error errorCss="message-error"
                                      name="bulkForm.projectList[${status.index}].projectName" />
                          </div>
                      </td>
                      <!-- Other editing items are omitted -->

                  </tr>
              </jsp:attribute>
          </app:listSearchResult>
          <div class="title-nav page-footer">
              <div class="button-nav">
                  <n:button id="bottomUpdateButton" uri="/action/projectBulk/confirmOfUpdate"
                      disabled="${isUpdatable}" cssClass="btn btn-lg btn-success">
                          Update</n:button>
                  <n:a id="bottomCreateButton" type="button" uri="/action/project"
                      cssClass="btn btn-lg btn-light" value="New registration"></n:a>
              </div>
          </div>
      </n:form>

  Key points of this implementation
    * Refer to :ref:`create search function: Create a search result display part<project_search-create_result_jsp>` as the method to create a JSP that displays search results.
    * When returning to the batch update screen from the confirmation screen, configure search condition parameters based on the search conditions acquired from :ref:`session store <session_store>`,
      so that re-search and paging is enabled under the same conditions. In JSP, objects registered in :ref:`session store <session_store>` can be handled in the same way as objects registered in the request scope.
    * Array type or :java:extdoc:`List<java.util.List>` type property element can be accessed by the `property name[index]` format.
      For more information, see :ref:`tag-access_rule`.

.. _`project_bulk_update-confirm_action`:

Create a business action method to check the updated contents
  Create a business action method to check the updated contents.

  ProjectBulkAction.java
    .. code-block:: java

      @InjectForm(form = ProjectBulkForm.class, prefix = "bulkForm", name = "bulkForm")
      @OnError(type = ApplicationException.class, path = "/WEB-INF/view/projectBulk/update.jsp")
      public HttpResponse confirmOfUpdate(HttpRequest request, ExecutionContext context) {

          ProjectBulkForm form = context.getRequestScopedVar("bulkForm");
          ProjectListDto dto = SessionUtil.get(context, "projectListDto");

          // Overwrite updates to session
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

  Key points of this implementation
    * The information to be updated is held in the :ref:`session store <session_store>`.

.. _`project_bulk_update-confirm_jsp`:

Create a confirmation screen JSP
  Create a JSP that displays the changed project information on the screen.

  /src/main/webapp/WEB-INF/projectBulk/confirmOfUpdate.jsp
    .. code-block:: jsp

          <section>
              <div class="title-nav">
                  <span>Project search list update screen</span>
                  <div class="button-nav">
                      <n:form useToken="true">
                        <!-- Button part is omitted -->
                      </n:form>
                  </div>
              </div>
              <h2 class="font-group my-3">Project update list</h2>
              <div>
                  <table class="table table-striped table-hover">
                      <tr>
                          <th>Project ID</th>
                          <th>Project name</th>
                          <th>Project type</th>
                          <th>Start date</th>
                          <th>End date</th>
                      </tr>
                      <c:forEach var="row" items="${projectListDto.projectList}">
                          <tr class="<n:write name='oddEvenCss' />">
                              <td>
                                  <n:write name="row.projectId" />
                              </td>
                              <!-- Other items are omitted -->
                          </tr>
                      </c:forEach>
                  </table>
              </div>
          </section>

.. _`project_bulk_update-bulk_update`:

Create a business action method that updates the database in a batch
  The target project is updated in a batch.

  ProjectBulkAction.java
    .. code-block:: java

      @OnDoubleSubmission
      public HttpResponse update(HttpRequest request, ExecutionContext context) {

        ProjectListDto projectListDto = SessionUtil.get(context, "projectListDto");
        projectListDto.getProjectList().forEach(UniversalDao::update);

        return new HttpResponse(303, "redirect://completeOfUpdate");
      }

  Key points of this implementation
    * The basic implementation method is the same as :ref:`create an update function: Create business action method to update the database<project_update-create_decide_action>`.
    * Execute :java:extdoc:`UniversalDao#update <nablarch.common.dao.UniversalDao.update(java.lang.Object)>` for the number of updates.
      When an exclusive control error occurs, all updates are rolled back.

      .. tip::
        Since an error control handler is added to the example application, if :java:extdoc:`OptimisticLockException<jakarta.persistence.OptimisticLockException>` occurs due to an exclusive control error,
        the screen transitions to the exclusive control error screen. For how to create error control handler, refer to :ref:`transition to the error page for the exception class with the handler <forward_error_page-handler>`.

    * Although :java:extdoc:`UniversalDao<nablarch.common.dao.UniversalDao>` also provides a
      :java:extdoc:`UniversalDao#batchUpdate <nablarch.common.dao.UniversalDao.batchUpdate(java.util.List)>` method that takes a list of entities as arguments,
      method that takes a list of entities as arguments, :ref:`batch execution<universal_dao-batch_execute>` and does not perform exclusive control.
      If exclusive control is required, use :java:extdoc:`UniversalDao#update <nablarch.common.dao.UniversalDao.update(java.lang.Object)>`.


.. _`project_bulk_update-complete_jsp`:

Display completion screen
  Refer to :ref:`create an update function: Create update completion screen<project_update-create_success_jsp>` as the same implementation method can be used for the completion screen.

This completes the description of the batch update function.

:ref:`Getting Started To TOP page <getting_started>`