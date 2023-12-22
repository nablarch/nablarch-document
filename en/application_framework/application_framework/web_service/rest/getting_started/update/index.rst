Create Update Function
================================================================
This section describes the update function based on an example application.
 
Description of the function to be created
  This function updates the project information that matches the project ID in the database by setting the JSON format project information in the request body during PUT requests.

Communication confirmation procedure
  1. Check the DB status in advance
 
     Execute the following SQL from the console of H2 and check the update target record.
 
     .. code-block:: sql
 
       SELECT * FROM PROJECT WHERE PROJECT_ID = 1;
 
  2. Update the project information
 
    Use any REST client to send the following request.
 
    URL
      http://localhost:9080/projects
    HTTP method
      PUT
    Content-Type
      application/json
    Request body
      .. code-block:: json
 
        {
            "projectId": 1,
            "projectName": "Project 999",
            "projectType": "development",
            "projectClass": "ss",
            "projectManager": "Yamada",
            "projectLeader": "Tanaka",
            "clientId": 10,
            "projectStartDate": "20160101",
            "projectEndDate": "20161231",
            "note": "Remarks 999",
            "sales": 10000,
            "costOfGoodsSold": 20000,
            "sga": 30000,
            "allocationOfCorpExpenses": 40000,
            "version": 1
        }
 
  3. Communication confirmation
 
    Execute the following SQL from the console of H2 and confirm that the record has been updated.
 
    .. code-block:: sql
 
      SELECT * FROM PROJECT WHERE PROJECT_ID = 1;
 
Update the project information
---------------------------------------

Create a form
  Create a form to accept the value submitted by the client.
 
  ProjectUpdateForm.java
    .. code-block:: java
 
      public class ProjectUpdateForm implements Serializable {
 
          // Partial excerpt

          /** Project name */
          @Required
          @Domain("id")
          private String projectId;
 
          /** Project name */
          @Required
          @Domain("projectName")
          private String projectName;

          /** Project type */
          @Required
          @Domain("projectType")
          private String projectType;
 
          // Getter and setter are omitted
      }
 
    Key points of this implementation
     * All properties are declared as String type. For more information, see how to set :ref:`validation rules <bean_validation-form_property>` .
 
Implementation of a business action method
  Implement the process to update the project information in the database.
 
  ProjectAction.java
    .. code-block:: java

      @Consumes(MediaType.APPLICATION_JSON)
      @Valid
      public HttpResponse update(ProjectUpdateForm form) {
          Project project = BeanUtil.createAndCopy(Project.class, form);

          UniversalDao.update(project);

          return new HttpResponse(HttpResponse.Status.OK.getStatusCode());
      }
 
   Point of this implementation
    * To accept the request body in JSON format, specify :java:extdoc:`Consumes<jakarta.ws.rs.Consumes>` in the ``MediaType.APPLICATION_JSON`` annotation. 
    * Validates the request using the :java:extdoc:`Valid <jakarta.validation.Valid>` annotation.
      For details, see :ref:`jaxrs_bean_validation_handler`.
    * Create an entity from a form with :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` and update the project information using :ref:`universal_dao`.
    * If the update is successful, :java:extdoc:`HttpResponse<nablarch.fw.web.HttpResponse>` , which indicates a successful completion (status code:``200``) is returned.
    
    .. tip::
      In the example application, :java:extdoc:`ErrorResponseBuilder<nablarch.fw.jaxrs.ErrorResponseBuilder>`  is uniquely extended, 
      response ``404`` if :java:extdoc:`NoDataException<nablarch.common.dao.NoDataException>` occurs and ``409`` if :java:extdoc:`OptimisticLockException<jakarta.persistence.OptimisticLockException>` occurs is generated and returned to the client.

Define the mapping to the URL
  Use :ref:`router_adaptor` to map business actions and URLs.
  Use :ref:`Path annotation for Jakarta RESTful Web Services <router_adaptor_path_annotation>` for mapping.

  ProjectAction.java
    .. code-block:: java

      @Path("/projects")
      public class ProjectAction {
        @PUT
        @Consumes(MediaType.APPLICATION_JSON)
        @Valid
        public HttpResponse update(ProjectUpdateForm form) {
            Project project = BeanUtil.createAndCopy(Project.class, form);

            UniversalDao.update(project);

            return new HttpResponse(HttpResponse.Status.OK.getStatusCode());
        }

  Key points of this implementation
    * The ``@Path`` and ``@PUT`` annotations are used to define the business action methods to be mapped on PUT requests.
