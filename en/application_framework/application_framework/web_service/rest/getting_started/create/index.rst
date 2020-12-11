Creation of a Registration Function
================================================================
This section describes the registration function based on an example application.

Description of the function to be created
  This function registers the project information in the database by setting the JSON format project information in the request body during POST requests.

Communication confirmation procedure
  1. Check the DB status in advance

     Execute the following SQL from the console of H2 and confirm that the record does not exist.

     .. code-block:: sql

       SELECT * FROM PROJECT WHERE PROJECT_NAME = 'Project 999';

  2. Registration of project information

    Use any REST client to send the following request.

    URL
      http://localhost:9080/projects
    HTTP method
      POST
    Content-Type
      application/json
    Request body
      .. code-block:: json

        {
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
            "allocationOfCorpExpenses": 40000
        }

  3. Communication confirmation

    Execute the following SQL from the console of H2 and confirm that one record can be retrieved.

    .. code-block:: sql

      SELECT * FROM PROJECT WHERE PROJECT_NAME = 'Project 999';

Register project information
---------------------------------

Create a form
  Create a form to accept the value submitted by the client.

  ProjectForm.java
    .. code-block:: java

      public class ProjectForm implements Serializable {

          // Partial excerpt

          /** Project name */
          @Required
          @Domain("projectName")
          private String projectName;

          // Getter and setter are omitted
      }

    Key points of this implementation
     * All properties are declared as String type. For more information, see :ref:`how to set validation rules <bean_validation-form_property>` .

Implementation of a business action method
  Implement the process of registering the project information to the database.

  ProjectAction.java
    .. code-block:: java

      @Consumes(MediaType.APPLICATION_JSON)
      @Valid
      public HttpResponse save(ProjectForm project) {
          UniversalDao.insert(BeanUtil.createAndCopy(Project.class, project));
          return new HttpResponse(HttpResponse.Status.CREATED.getStatusCode());
      }

   Key points of this implementation
    * To accept the request in JSON format, specify :java:extdoc:`Consumes<javax.ws.rs.Consumes>` in the ``MediaType.APPLICATION_JSON`` annotation.
    * Validates the request using the :java:extdoc:`Valid <javax.validation.Valid>` . 
      For details, see :ref:`jaxrs_bean_validation_handler` .
    * Convert the form to an entity with :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` and register the project information in the database using :ref:`universal_dao`. 
    * :java:extdoc:`HttpResponse<nablarch.fw.web.HttpResponse>` is returned as the return value, indicating that the creation of the resource is complete (status code: ``201``).

Define the mapping to the URL
  Use :ref:`router_adaptor` to map business actions and URLs.
  Use :ref:`Path annotation for JAX-RS <router_adaptor_path_annotation>` for mapping.

  ProjectAction.java
    .. code-block:: java

      @Path("/projects")
      public class ProjectAction {
        @POST
        @Consumes(MediaType.APPLICATION_JSON)
        @Valid
        public HttpResponse save(ProjectForm project) {
          UniversalDao.insert(BeanUtil.createAndCopy(Project.class, project));
          return new HttpResponse(HttpResponse.Status.CREATED.getStatusCode());
      }

  Key points of this implementation
    * The ``@Path`` and ``@POST`` annotations are used to define the business action methods to be mapped on POST requests.

