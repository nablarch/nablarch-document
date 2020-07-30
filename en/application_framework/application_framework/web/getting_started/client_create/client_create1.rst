.. _`client_create_1`:

Create Initial Display of Registration Screen
===============================================
This chapter describes the initial display of the registration screen.

Create a JSP for the registration screen
  Place the template JSP under `/src/main/webapp/WEB-INF/view/client`.

     :download:`create.jsp <../downloads/client_create/create.jsp>`

Implement the part that is initially displayed on the screen.
  Add the content of the registration screen to create.jsp.

  /src/main/webapp/WEB-INF/view/client/create.jsp
    .. code-block:: jsp

      <n:form>
          <div class="form-group label-static is-empty">
              <label class="control-label"> Client name</label>
              <!-- Client name text box -->
              <!-- Since the form has not been created, specify a temporary value for the name attribute -->
              <n:text name="tmp" cssClass="form-control input-text"/>
          </div>
          <div class="form-group label-static is-empty">
              <label class="control-label">Industry type</label>
              <!-- Pull down of industry type -->
              <!-- Since the form has not been created, specify a temporary value for the name attribute -->
              <n:select
                      listName="industries"
                      elementValueProperty="industryCode"
                      elementLabelProperty="industryName"
                      name="tmp"
                      withNoneOption="true"
                      cssClass="btn dropdown-toggle"/>
          </div>
          <div class="button-nav">
              <!-- Registration button -->
              <!-- Since the registration confirmation screen is not yet created, specify a temporary value for the uri attribute -->
              <n:button
                      uri="tmp"
                      cssClass="btn btn-raised btn-success">Registration</n:button>
          </div>
      </n:form>

  Key points of this implementation
    * Use :ref:`tag` to create a text input form and pull-down.
      See :ref:`tag-input_form`.
    * The industry type list to be registered in the request scope with the initial display method described below is specified
      in the `listName` attribute of :ref:`tag-select_tag` and displays it in the pull-down.
      See  :ref:`tag-selection`.

Create an initial display method for a business action
  Add a business action method to `ClientAction` that performs the following process.

    * Acquire the data to be displayed in the pull-down and register it in the request scope.
    * Forward to the JSP of the initial display screen.

    ClientAction.java
      .. code-block:: java

        public HttpResponse input(HttpRequest request, ExecutionContext context) {
            EntityList<Industry> industries = UniversalDao.findAll(Industry.class);
            context.setRequestScopedVar("industries", industries);
            return new HttpResponse("/WEB-INF/view/client/create.jsp");
        }

    The signature of the business action method should be as follows.
    A 404 error occurs if the business action method does not meet the following signature.

    .. java:method:: public HttpResponse methodName(HttpRequest request, ExecutionContext context)

      :param request: request object passed from the framework

      :param context: execution context passed from the framework

      :param return: response object with transition destination


    Key points of this implementation
      * To display the pull down of industry type on the registration screen, use :ref:`universal_dao` to acquire all the industry type information from the database.
      * To pass a value to a JSP, register the acquired industry type list in the request scope.

Map URLs and business actions
  The mapping process is performed using the OSS library `http_request_router(external site) <https://github.com/kawasima/http-request-router>`_ .
  Add configuration for mapping the specified URL and initial display process.

    routes.xml
      .. code-block:: xml

        <routes>
          <!-- Set it before other mappings because it will be evaluated from above -->
          <get path="/action/client" to="Client#input"/>
          <!-- Other settings are omitted -->
        </routes>

    .. tip::
      For instructions on how to specify routes.xml, see `Library README document (external site) <https://github.com/kawasima/http-request-router/blob/master/README.ja.md>`_ .

Create a link to the registration screen
  Create a link to the client registration screen in the header menu.

  /src/main/webapp/WEB-INF/view/common/menu.jsp
    .. code-block:: jsp

      <ul class="nav navbar-nav">
        <!-- Other links are omitted -->
        <li>
          <n:a href="/action/client"> Client registration</n:a>
        </li>
      </ul>

  Key points of this implementation
    * Create a link using :ref:`tag-a_tag` of :ref:`tag`.

Communication confirmation
  Confirm communications with the following procedure.

  1. Log in to the application and confirm that the "Client Registration"(顧客登録) link has been created in the header menu.

    .. image:: ../images/client_create/header_menu.png

  2. Confirm that it transitions to the client registration screen on clicking the Client Registration link, and the "Client Name"(顧客名) form, the "Industry type"(業種) pull-down, and the registration button are displayed.

    .. image:: ../images/client_create/initial_display.png

  3. Confirm if the "Industry type"(業種) pull-down can be selected.

    .. image:: ../images/client_create/initial_display_select.png

:ref:`Next <client_create_2>`
