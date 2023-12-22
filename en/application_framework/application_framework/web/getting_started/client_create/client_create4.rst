.. _`client_create_4`:

Register to the Database
==========================================
This chapter describes the process of registering client information to a database.

:ref:`Previous <client_create_3>`

Implementation of the registration process
  Add a method to `ClientAction` to process the registration of client information.

  ClientAction.java
    .. code-block:: java

      public HttpResponse create(HttpRequest request, ExecutionContext context) {

          Client client = SessionUtil.get(context, "client");

          UniversalDao.insert(client);

          SessionUtil.delete(context, "client");

          return new HttpResponse(303, "redirect://complete");
      }

  Key points of this implementation
    * Retrieve the client entity from the :ref:`session store <session_store>` and register the entity in the database using :ref:`universal_dao`.
    * Remove client information from :ref:`session store <session_store>`.
    * Specify a redirect to the registration completion screen display as the transition destination for the response object (to prevent multiple registration of client information when the update button of the browser is clicked on the completion screen).
      For the status code specified in redirect, see :ref:`web_feature_details-status_code`.

Prevent duplicate form submission
  Add control to both business action and JSP so that requests are not sent twice when a button is double clicked.

  ClientAction.java
    .. code-block:: java

      @OnDoubleSubmission
      public HttpResponse create(HttpRequest request, ExecutionContext context) {

      // No change in implementation

      }

  Key points of this implementation
    * Assign :java:extdoc:`OnDoubleSubmission <nablarch.common.web.token.OnDoubleSubmission>` for transitioning to the error page
      when the business action method is executed twice. For more information, see :ref:`tag-double_submission`.

  .. tip::

    Configure the default transition destination screen for double submission in the example application.
    For information on how to specify the default transition destination, see :ref:`tag-double_submission`.

  /src/main/webapp/WEB-INF/view/client/create.jsp
    .. code-block:: jsp

      <!-- Parts that are not modified are omitted -->
      <!-- Return to input, confirm button is only shown on the confirmation screen -->
        <n:forConfirmationPage>
            <n:button uri="/action/client/back"
                      cssClass="btn btn-raised btn-default">Return to input</n:button>
            <!-- Specify false for allowDoubleSubmission attribute -->
            <n:button uri="/action/client/create"
                      allowDoubleSubmission="false"
                      cssClass="btn btn-raised btn-success">Confirm</n:button>
        </n:forConfirmationPage>

  Key points of this implementation
    * JavaScript that controls duplicate form submission is added by specifying false in `allowDoubleSubmission` attribute of :ref:`tag-button_tag`.
    * Double submission control is also performed on the server in consideration of the case where JavaScript in the browser is disabled.

Implementation of the display process of the registration completion screen
  Implements the display process of the registration completion screen.

  Implementation of a business action method
    Implements the display process of the registration completion screen.

    ClientAction.java
      .. code-block:: java

        public HttpResponse complete(HttpRequest request, ExecutionContext context) {
            return new HttpResponse("/WEB-INF/view/client/complete.jsp");
        }

  Create a JSP for the registration completion screen
    Create a new JSP for the registration completion screen

    /src/main/webapp/WEB-INF/view/client/complete.jsp
      .. code-block:: jsp

        <%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
        <%@ taglib prefix="c" uri="jakarta.tags.core" %>
        <%@ taglib prefix="n" uri="http://tis.co.jp/nablarch" %>
        <%@ page session="false" %>
        <!DOCTYPE html>
        <html>
            <head>
                <title>Client registration completion screen</title>
            </head>
            <body>
                <n:include path="/WEB-INF/view/common/menu.jsp" />
                <n:include path="/WEB-INF/view/common/header.jsp" />
                <div class="container-fluid mainContents">
                    <section class="row">
                        <div class="title-nav">
                            <span class="page-title">Client registration completion screen</span>
                        </div>
                        <div class="message-area message-info">
                            Customer registration completed
                        </div>
                    </section>
                </div>
                <n:include path="/WEB-INF/view/common/footer.jsp" />
            </body>
        </html>

Communication confirmation
  Confirm that the registration process is implemented correctly by following the below steps.

  1. Displays the client registration screen(顧客登録画面).

    .. image:: ../images/client_create/input_display.png

  2. Select a full-width string for the client name(顧客名) and an arbitrary value for the industry type(業種) and click the "registration"(登録) button.

    .. image:: ../images/client_create/input_valid_value.png

  3. Confirm that the registration confirmation screen is displayed, and the client name and industry type entered in `2` are displayed as labels.

    .. image:: ../images/client_create/confirm_display.png

  4. Click the "Confirm"(確定) button to confirm that the registration completion screen is displayed.

    .. image:: ../images/client_create/complete_display.png

  5. Click the search button in the client column of the side menu for transitioning to the client search screen.

    .. image:: ../images/client_create/client_confirm_sidemenu.png

  6. Confirm that the registered client information can be searched.

    .. image:: ../images/client_create/client_search_result.png


This completes the description of the registration function.

:ref:`Getting Started To TOP page <getting_started>`
