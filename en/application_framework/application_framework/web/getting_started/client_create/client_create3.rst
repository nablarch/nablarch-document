.. _`client_create_3`:

Return to the Registration Screen From the Registration Confirmation Screen
=============================================================================
This chapter describes the process of returning to the registration screen from the registration confirmation screen.

:ref:`Previous <client_create_2>`

Implementation of return process to the registration screen
  Add a method to `ClientAction` for returning to the registration screen.

  ClientAction.java
    .. code-block:: java
      :emphasize-lines: 1,2,3,4,5,6,7,8,9,13

      public HttpResponse back(HttpRequest request, ExecutionContext context) {

          Client client = SessionUtil.get(context, "client");

          ClientForm form = BeanUtil.createAndCopy(ClientForm.class, client);
          context.setRequestScopedVar("form", form);

          return new HttpResponse("forward://input");
      }

      public HttpResponse input(HttpRequest request, ExecutionContext context) {

          SessionUtil.delete(context, "client");

          EntityList<Industry> industries = UniversalDao.findAll(Industry.class);
          context.setRequestScopedVar("industries", industries);

          return new HttpResponse("/WEB-INF/view/client/create.jsp");
      }

  Key points of this implementation
    * Retrieve client information from :ref:`session store <session_store>`.
    * A client entity is converted into a form by using :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` to display the acquired client information on a registration screen.
    * The transition destination of the response object is the internal forward to the initial display process
      (to acquire the industry type information to be displayed again in the pull-down when the registration screen is displayed).
    * Delete the objects registered in the  :ref:`session store <session_store>` with the initial display process (considering the case where the registration screen transitions directly from the header menu without clicking the back button).

Communication confirmation
  1. Displays the registration screen(登録画面).

    .. image:: ../images/client_create/input_display.png

  2. Select a full-width string for the client name(顧客名) and an arbitrary value for the industry type(業種) and click the "registration"(登録) button.

    .. image:: ../images/client_create/input_valid_value.png

  3. On the confirmation screen, click the "Return to input"(入力へ戻る) button.

    .. image:: ../images/client_create/confirm_display.png

  4. Confirm that the registration screen(登録画面) is displayed, and the client name and industry type entered in `2` is displayed on the screen.

    .. image:: ../images/client_create/input_back.png

:ref:`Next <client_create_4>`
