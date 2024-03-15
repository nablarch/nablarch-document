Create a Search Function
================================================================
This section describes the search function based on an example application.

Description of the function to be created
  This function adds search conditions to the query parameter during a GET request, 
  and returns the project information that matches the conditions in JSON format.

  ``Customer ID (exact match)`` and  ``project name (partial match)`` can be specified as the search conditions. 
  If a search condition is not specified, all project information is returned.

Communication confirmation procedure
  1. Search for project information

    The following searches the project information for customer ID `1`.

    Use any REST client to send the following request.

    URL
      http://localhost:9080/projects?clientId=1
    HTTP method
      GET

  2. Confirm the search results

    Confirm that the following JSON format response is returned by executing 1.

    .. code-block:: javascript

      [{
          "projectId":1,
          "projectName":"Project 001",
          "projectType":"development",

          // Omitted

      }]

Search the project information
---------------------------------

Create a form
  Create a form to accept the value submitted by the client.

  ProjectSearchForm.java
    .. code-block:: java

      public class ProjectSearchForm implements Serializable {

          /** Customer ID */
          @Domain("id")
          private String clientId;

          /** Project name */
          @Domain("projectName")
          private String projectName;

          // Getter and setter are omitted
      }

  Key points of this implementation
    * All properties are declared as String type. For more information, see  :ref:`how to set validation rules <bean_validation-form_property>` .

Create a bean that holds the search condition
  Create a bean to hold the search condition.

  ProjectSearchDto.java
    .. code-block:: java

      public class ProjectSearchDto implements Serializable {

          /** Customer ID */
          private Integer clientId;

          /** Project name */
          private String projectName;

          // Getter and setter are omitted

  Key points of this implementation
   * Bean property should be of the :ref:`type that is compatible with the definition (type) of the corresponding condition column <universal_dao-search_with_condition>`.

Create a SQL for search
  Create a SQL for searching.

    Project.sql
      .. code-block:: none

        FIND_PROJECT =
        SELECT
            *
        FROM
            PROJECT
        WHERE
            $if(clientId) {CLIENT_ID = :clientId}
            AND $if(projectName) {PROJECT_NAME LIKE :%projectName%}

    Key points of this implementation
      * To prevent SQL injection, SQL is written in an external file. For more information, see  :ref:`database-use_sql_file` .
      * Bind the value to SQL using the bean property name. For more information, see :ref:`database-input_bean`.
      * To include only the items specified as search condition in the conditions, build a SQL statement using the :ref:`$if syntax <database-use_variable_condition>` .

Implementation of a business action method
  Implement the process to search a database based on search conditions.

  ProjectAction.java
    .. code-block:: java

      @Produces(MediaType.APPLICATION_JSON)
      public List<Project> find(JaxRsHttpRequest req) {

          // Convert request parameters to bean
          ProjectSearchForm form =
                  BeanUtil.createAndCopy(ProjectSearchForm.class, req.getParamMap());

          // Run BeanValidation
          ValidatorUtil.validate(form);

          ProjectSearchDto searchCondition = BeanUtil.createAndCopy(ProjectSearchDto.class, form);
          return UniversalDao.findAllBySqlFile(Project.class, "FIND_PROJECT", searchCondition);
      }

  Key points of this implementation
   * Specifies ``MediaType.APPLICATION_JSON``  in  :java:extdoc:`Produces<javax.ws.rs.Produces>` annotation to return the search results in JSON format to the client.
   * Acquires the query parameter from :java:extdoc:`JaxRsHttpRequest<nablarch.fw.jaxrs.JaxRsHttpRequest>` .
   * Creates a form from the request parameters using :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` .
   * Validates form using :java:extdoc:`ValidatorUtil#validate <nablarch.core.validation.ee.ValidatorUtil.validate(java.lang.Object)>`.
   * Copies the form value to the search condition bean using :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` .
   * Returns a list of project information obtained using :ref:`universal_dao`, as a return value.
   * As the returned object is converted to JSON format by :ref:`body_convert_handler` , 
     conversion process implementation in the business action method is not required.

Define the mapping to the URL
  Use :ref:`router_adaptor` to map business actions and URLs.
  Use :ref:`Path annotation for JAX-RS <router_adaptor_path_annotation>` for mapping.

  ProjectAction.java
    .. code-block:: java

      @Path("/projects")
      public class ProjectAction {
        @GET
        @Produces(MediaType.APPLICATION_JSON)
        public List<Project> find(JaxRsHttpRequest  req) {

            // Convert request parameters to beans
            ProjectSearchForm form =
                    BeanUtil.createAndCopy(ProjectSearchForm.class, req.getParamMap());

            // Validate
            ValidatorUtil.validate(form);

            ProjectSearchDto searchCondition = BeanUtil.createAndCopy(ProjectSearchDto.class, form);
            return UniversalDao.findAllBySqlFile(Project.class, "FIND_PROJECT", searchCondition);
        }

  Key points of this implementation
    * The ``@Path`` and ``@GET`` annotations are used to define the business action methods to be mapped on GET requests.

