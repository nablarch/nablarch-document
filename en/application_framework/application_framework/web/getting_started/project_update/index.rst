.. _`project_update`:

Create Update Function
==========================================
This section describes the update function based on an example application.

Description of the function to be created
  1. Click the project ID in the project list.

    .. image:: ../images/project_update/project_update_detail_link.png
      :scale: 80

  2. Click the "Change(変更)" button on the target project's detail screen.

    .. image:: ../images/project_update/project_update_detail.png
      :scale: 80

  3. Rewrite the item to be updated and click the Update (更新) button.

    .. image:: ../images/project_update/project_update_update.png
      :scale: 80

  4. When the update confirmation screen is displayed, click on the confirm (確定) button.

    .. image:: ../images/project_update/project_update_confirm.png
      :scale: 80

  5. The database is updated and the update completion screen is displayed.

    .. image:: ../images/project_update/project_update_complete.png
      :scale: 80

Enter and confirm update contents
-----------------------------------
Of the implementation methods of the update function, the input and confirmation of the update contents are described in the following order.

  #. :ref:`Create a form<project_update-create_form>`
  #. :ref:`Create a business action method to display the update screen<project_update-create_edit_action>`
  #. :ref:`Create a JSP for the update screen<project_update-create_update_jsp>`
  #. :ref:`Create a business action method to check the updated contents<project_update-create_confirm_action>`
  #. :ref:`Create a JSP for the update confirmation screen<project_update-create_confirm_jsp>`

.. _`project_update-create_form`:

Create a form
  Create a form to accept parameters for transitioning from detail screen to update screen and a form to accept input values for edit field of update screen.

  A form to accept parameters when transitioning from the detail screen to the update screen
    Create a form to accept the target project ID which is passed as a path parameter ( ":projectId" part of "show/:projectId")
    when transitioning from the detail screen to the update screen.

    ProjectTargetForm.java
      .. code-block:: java

        public class ProjectTargetForm implements Serializable {

            /** Project ID */
            @Required
            @Domain("id")
            private String projectId;

            // Getter and setter are omitted

  A form that accepts values entered from the update screen
    Create a form to accept the value entered from the update screen after editing.

    ProjectUpdateForm.java
      .. code-block:: java

        public class ProjectUpdateForm implements Serializable {

            // Partial excerpt

            /** Project name */
            @Required
            @Domain("projectName")
            private String projectName;

            /**
             * Acquire the project name.
             *
             * @return Project name
             */
            public String getProjectName() {
                return this.projectName;
            }

            /**
             * Set the project name.
             *
             * @param projectName Project name to be set
             */
            public void setProjectName(String projectName) {
                this.projectName = projectName;
            }
        }

    Key points of this implementation
      * Although the input items are duplicated with the project registration screen,
        the form for the project update screen should be created since :ref:`form should be created for each HTML form <application_design-form_html>` for responsibility assignment.

.. _`project_update-create_edit_action`:

Create a business action method to display the update screen
  Create a business action method that retrieves the current information from the database and displays the update screen.

  ProjectAction.java
    .. code-block:: java

        @InjectForm(form = ProjectTargetForm.class)
        public HttpResponse edit(HttpRequest request, ExecutionContext context) {

            // Delete the session information used in the update process.
            SessionUtil.delete(context, "project");

            ProjectTargetForm targetForm = context.getRequestScopedVar("form");
            LoginUserPrincipal userContext = SessionUtil.get(context, "userContext");

            // Throws a NoDataException if the target project has been deleted by another user
            ProjectDto dto = UniversalDao.findBySqlFile(ProjectDto.class, "FIND_BY_PROJECT",
                    new Object[]{targetForm.getProjectId(), userContext.getUserId()});

            // Set the output information to the request scope
            context.setRequestScopedVar("form", dto);

            SessionUtil.put(context, "project", BeanUtil.createAndCopy(Project.class, dto));

            return new HttpResponse("/WEB-INF/view/project/update.jsp");
        }

  Key points of this implementation
    * A unique key lookup using
      :java:extdoc:`UniversalDao#findBySqlFile <nablarch.common.dao.UniversalDao.findBySqlFile(java.lang.Class-java.lang.String-java.lang.Object)>`
      to get the initial value to display in the edit form.
      For :ref:`acquire the result of table JOIN<universal_dao-join>`, the search result is accepted as a bean.
      If there is no target data in the unique key search, :java:extdoc:`NoDataException<nablarch.common.dao.NoDataException>` is thrown.

        .. tip::
          Since an error control handler is added to the example application, :java:extdoc:`NoDataException<nablarch.common.dao.NoDataException>` occurs, the screen transitions to the 404 error screen.
          For how to create an error control handler, refer to :ref:`transition to the error page for the exception class with the handler <forward_error_page-handler>`.

    * Considering the possibility of updates by other users during editing, the entity at the time of the start of editing is registered in :ref:`session_store`
      to perform an :ref:`optimistic lock<universal_dao_jpa_version>` (described below) using the version number at the time of the start of editing.

.. _`project_update-create_update_jsp`:

Create a JSP for the update screen
  Screen creation has been described in :ref:`client_create_1` in the registration section and is omitted.

.. _`project_update-create_confirm_action`:

Create a business action method to check the updated contents
  Create a business action method that validates the update content and displays the confirmation screen.
  In addition to :ref:`bean_validation`, the validation with database search is implemented in the business action method.

  ProjectAction.java
    .. code-block:: java

      @InjectForm(form = ProjectUpdateForm.class, prefix = "form")
      @OnError(type = ApplicationException.class,
              path = "/WEB-INF/view/project/update.jsp")
      public HttpResponse confirmOfUpdate(HttpRequest request, ExecutionContext context) {
          ProjectUpdateForm form = context.getRequestScopedVar("form");

          // Search the database to check if there are any customers with the entered ID
          if (form.hasClientId()) {
              if (!UniversalDao.exists(Client.class, "FIND_BY_CLIENT_ID",
                      new Object[] {Integer.parseInt(form.getClientId()) })) {
                          throw new ApplicationException(
                              MessageUtil.createMessage(MessageLevel.ERROR,
                                  "errors.nothing.client", form.getClientId()));

              }
          }

          Project project = SessionUtil.get(context, "project");

          // Overwrite a form value to a session
          BeanUtil.copy(form, project);

          // Set the output information to the request scope
          context.setRequestScopedVar("form", BeanUtil.createAndCopy(ProjectDto.class, form));
          context.setRequestScopedVar("profit", new ProjectProfit(
                  project.getSales(),
                  project.getCostOfGoodsSold(),
                  project.getSga(),
                  project.getAllocationOfCorpExpenses()
          ));

          return new HttpResponse("/WEB-INF/view/project/confirmOfUpdate.jsp");
      }

  Key points of this implementation
    * Validation that requires a database search is described in the business action method.
      To confirm the existence of data, use :java:extdoc:`UniversalDao#exists <nablarch.common.dao.UniversalDao.exists(java.lang.Class-java.lang.String-java.lang.Object)>`.
      For more information, see :ref:`Validation that requires a database lookup<bean_validation-database_validation>`.
    * Since the :ref:`form should not be stored directly in the session store<session_store-form>` due to responsibility assignment, it should be reworded to a bean.

  Create SQL
    Create SQL to acquire customer information from customer IDs to confirm the existence of a customer.

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

      Key points of this implementation
        * The SQL for existence confirmation is made as a SELECT statement.

.. _`project_update-create_confirm_jsp`:

Create a JSP for the update confirmation screen
  Create an update confirmation screen by reusing the update screen.

  /src/main/webapp/WEB-INF/view/project/update.jsp
    .. code-block:: jsp

      <n:form useToken="true">
        <!-- Confirmation of registration -->
          <div class="title-nav page-footer">
              <!-- Button at the bottom of the page -->
              <div class="button-nav">
                  <n:forInputPage>
                      <!-- Button for input screen -->
                  </n:forInputPage>
                  <n:forConfirmationPage>
                      <!-- Button for confirmation screen -->
                      <n:submit value = "Confirm" uri="/action/project/update" id="bottomSubmitButton"
                              cssClass="btn btn-raised btn-success"
                              allowDoubleSubmission="false" type="button" />
                  </n:forConfirmationPage>
              </div>
          </div>
      </n:form>

  Key points of this implementation
    * How to use the update screen as a confirmation screen has been omitted as it is explained in :ref:`create a confirmation screen for the registration function<client_create_forConfirmationPage>`.
    * To add JavaScript to prevent duplicate form submission, set the `allowDoubleSubmission` attribute of :ref:`tag-submit_tag` to false.
      For more information, see :ref:`tag-double_submission`.

Database update
---------------------
Among the implementation methods of update function, confirmation of update content is explained in the following order.

  #. :ref:`Create a business action method<project_update-create_decide_action>`
  #. :ref:`Create an update completion screen<project_update-create_success_jsp>`

.. _`project_update-create_decide_action`:

Create a business action method
  Create a business action method to update the database and finalize the changes.
  The entity definition for performing :ref:`optimistic lock<universal_dao_jpa_version>` is also explained.

  Create a business action method for database update
    Create a business action method to update the database and redirect to the completion screen display method.

      ProjectAction.java
        .. code-block:: java

          @OnDoubleSubmission
          public HttpResponse update(HttpRequest request, ExecutionContext context) {
              Project targetProject = SessionUtil.delete(context, "project");
              UniversalDao.update(targetProject);

              return new HttpResponse(303, "redirect://completeOfUpdate");
          }

    Key points of this implementation
      * Sets the values you want to update to an entity and updates the database using :java:extdoc:`UniversalDao#update <nablarch.common.dao.UniversalDao.update(java.lang.Object)>`.
        In the update process, optimistic locking is performed.
      * Assign :java:extdoc:`@OnDoubleSubmission <nablarch.common.web.token.OnDoubleSubmission>` to prevent duplicate form submission.
      * Redirect the response to prevent a rerun in the browser update.
      
        * For the format of the resource path, see :java:extdoc:`ResourceLocator <nablarch.fw.web.ResourceLocator>`.
        * For the status code specified in redirect, see :ref:`web_feature_details-status_code`.

  Create an entity for optimistic locking
    Create an entity with :ref:`optimistic lock<universal_dao_jpa_version>` enabled.

    Project.java
      .. code-block:: java

        // Other properties are omitted

        /** Version number */
        private Long version;

        /**
         * Returns the version number.
         *
         * @return Version number
         */
        @Version
        @Column(name = "VERSION", precision = 19, nullable = false, unique = false)
        public Long getVersion() {
            return version;
        }

        /**
         * Set the version number.
         *
         * @param version Version number
         */
        public void setVersion(Long version) {
            this.version = version;
        }

    Key points of this implementation
      * To perform :ref:`optimistic locking<universal_dao_jpa_version>`, create a `version` property in the entity and assign
        :ref:`@Version <universal_dao_jpa_version>` to the getter.

  .. _`project_update-create_complete_action`:

  Create a business action method to display the completion screen
    Create a business action method that displays the completion screen, which is the redirect destination of the update method.

    ProjectAction.java
      .. code-block:: java

        public HttpResponse completeOfUpdate(HttpRequest request, ExecutionContext context) {
            return new HttpResponse("/WEB-INF/view/project/completeOfUpdate.jsp");
        }

.. _`project_update-create_success_jsp`:

Create an update completion screen
  Creates an update completion screen.

  /src/main/webapp/WEB-INF/view/project/completeOfUpdate.jsp
    .. code-block:: jsp

      <n:form>
          <div class="title-nav">
              <h1 class="page-title">Project change completion screen</h1>
              <div class="button-nav">
                <!-- Omitted -->
              </div>
          </div>
          <div class="message-area message-info">
              Project update is now complete.
          </div>
          <!-- Omitted -->
      </n:form>

This completes the description of the update function.

:ref:`Getting Started To TOP page <getting_started>`
