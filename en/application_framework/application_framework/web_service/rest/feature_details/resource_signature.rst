Implementation of the Resource (Action) Class
==================================================


.. _rest_feature_details-method_signature:

Signature of resource class methods
--------------------------------------------------
This section describes the types available for method arguments and return values of the resource classes.

Method argument
  .. list-table::
    :header-rows: 1
    :class: white-space-normal
    :widths: 30 70

    * - Argument definition
      - Description

    * - No argument
      - If no parameters or request bodies are required, the method can be defined with no arguments.

        Example:
          .. code-block:: java

            public HttpResponse sample() {
              // Omitted
            }

    * - Form (Java Beans)
      - When processed based on the form converted from the request body, the form is defined as an argument.
      
        Example:
          .. code-block:: java

            public HttpResponse sample(SampleForm form) {
              // Omitted
            }

    * - :java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>`\ [#]_\
      - When :ref:`path parameter <rest_feature_details-path_param>` and :ref:`query parameter <rest_feature_details-query_param>` are used or when the value of HTTP header is acquired,
        :java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>` is defined as an argument.

        Example:
          .. code-block:: java

            public HttpResponse sample(JaxRsHttpRequest request) {
              // Omitted
            }

    * - :java:extdoc:`ExecutionContext <nablarch.fw.ExecutionContext>`
      - To access the scope variables provided by  :java:extdoc:`ExecutionContext <nablarch.fw.ExecutionContext>`, 
        :java:extdoc:`ExecutionContext <nablarch.fw.ExecutionContext>` is defined as an argument.
        
        Example:
          .. code-block:: java

            public HttpResponse sample(ExecutionContext context) {
              // Omitted
            }

    * - Combination
      - The above types can be combined according to the application.
        
        For example, a method that requires HTTP header information and a Form converted from the request body is defined as follows.

        .. code-block:: java

          public HttpResponse sample(SampleForm form, JaxRsHttpRequest request) {
            // Omitted
          }

.. [#] 
  HttpRequest can also be used to maintain backward compatibility, but in principle JaxRsHttpRequest should be used.

Method return value
  .. list-table::
    :header-rows: 1
    :class: white-space-normal
    :widths: 30 70

    * - Form of return values
      - Description

    * - void
      - Returns ``204: NoContent`` to the client, indicating that the response body is empty.

    * - Form (Java Beans)
      - The form returned from the method is converted to the content to be output to the response body by using :ref:`body_convert_handler` and returned to the client.

    * - :java:extdoc:`HttpResponse <nablarch.fw.web.HttpResponse>`
      - The information of  :java:extdoc:`HttpResponse <nablarch.fw.web.HttpResponse>` returned from the method is returned to the client.


.. _rest_feature_details-path_param:

Handle path parameters
--------------------------------------------------
This section shows how to implement when a value indicating a resource to be searched, updated, or deleted is specified as the path parameter.

URL example
  ``123`` in ``GET /users/123`` is the path parameter.

Routing Configuration
  Configure an arbitrary name as the path parameter when mapping between URL and action. 
  In this example, the name ``id`` is configured to allow only numbers.
  
  For more information, see :ref:`router_adaptor`.

  .. code-block:: xml

    <routes>
      <get path="users/:id" to="UsersResource#find">
        <requirements>
          <requirement name="id" value="\d+$" />
        </requirements>
      </get>
    </routes>

Implementation of resource class methods
  Acquires the path parameter from  :java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>` . 
  For this reason,  :java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>` is defined as a temporary argument for the method of the resource.

  For the parameter name specified in :java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>` , 
  use the path parameter name specified in the routing configuration.

  .. code-block:: java

    @Produces(MediaType.APPLICATION_JSON)
    public User delete(JaxRsHttpRequest req) {
      // Acquire the path parameter value from JaxRsHttpRequest
      Long id = Long.valueOf(req.getPathParam("id"));
      return UniversalDao.findById(User.class, id);
    }

.. important::
  Note that :java:extdoc:`PathParam <jakarta.ws.rs.PathParam>` specified in Jakarta RESTful Web Services cannot be used.

.. _rest_feature_details-query_param:

Handling query parameters
--------------------------------------------------
Specifying the search condition as a query parameter in the resource search process may be required. 
The implementation method for such a case is shown below.

URL example
  ``GET /users/search?name=Duke``

Routing Configuration
  In the routing configuration, mapping to the resource class is performed based on the path excluding the query parameter.

  .. code-block:: xml

    <routes>
      <get path="users/search" to="Users#search"/>
    </routes>

Implementation of resource class methods
  Acquires the query parameter from  :java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>` . 
  For this reason,  :java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>` is defined as a temporary argument for the method of the resource.

  Parameters acquired from :java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>`  is mapped to form class using :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>`.

  .. code-block:: java

    public HttpResponse search(JaxRsHttpRequest req) {

      // Convert request parameters to Bean
      UserSearchForm form = BeanUtil.createAndCopy(UserSearchForm.class, req.getParamMap());

      // Perform validation
      ValidatorUtil.validate(form)

      // Execute the business logic (omitted)
    }

    // Form for mapping query parameters
    public UserSearchForm {
      private String name;
      // Omitted
    }

.. important::
  Note that  :java:extdoc:`QueryParam <jakarta.ws.rs.QueryParam>` specified in Jakarta RESTful Web Services cannot be used.

.. _rest_feature_details-response_header:

Set the response header
--------------------------------------------------
In some cases, it may be necessary to specify individual response headers for methods of the resource class.

.. important::
  If it is necessary to specify a response header that is common to the entire application, it should be set in the handler.
  If security-related response headers are to be specified, use :ref:`secure_handler`.

To create an :java:extdoc:`HttpResponse <nablarch.fw.web.HttpResponse>` with a method of the resource class, just set the response header to HttpResponse.

  .. code-block:: java

    public HttpResponse something(JaxRsHttpRequest request) {

        // Processing omitted.

        HttpResponse response = new HttpResponse();
        response.setHeader("Cache-Control", "no-store"); // Specify the response header
        return response;
    }

If the Produces annotation is used and the method of the resource class returns an entity (bean),
the response header cannot be specified.

  .. code-block:: java

    @Produces(MediaType.APPLICATION_JSON)
    public List<Client> something(JaxRsHttpRequest request, ExecutionContext context) {

        // Processing omitted.
        List<Client> clients = service.findClients(condition);

        return clients;
    }

The framework provides :java:extdoc:`EntityResponse <nablarch.fw.jaxrs.EntityResponse>`
to set the response header and status code when Produces annotation is used.
It should be implemented to return an EntityResponse instead of an entity.

  .. code-block:: java

    @Produces(MediaType.APPLICATION_JSON)
    public EntityResponse something(JaxRsHttpRequest request, ExecutionContext context) {

        // Processing omitted.
        List<Client> clients = service.findClients(condition);

        EntityResponse response = new EntityResponse();
        response.setEntity(clients); // Specify an entity
        response.setStatusCode(HttpResponse.Status.OK.getStatusCode()); // Specify the status code
        response.setHeader("Cache-Control", "no-store"); // Specify the response header
        return response;
    }
