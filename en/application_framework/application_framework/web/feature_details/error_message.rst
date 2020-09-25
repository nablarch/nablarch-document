Display Validation Error Messages on the Screen
==================================================
Error messages of the validation in the server are stored in the request scope by the :ref:`http_error_handler`.
The template engine can display the error messages by accessing :java:extdoc:`ErrorMessages <nablarch.fw.web.message.ErrorMessages>` stored in the request scope.
For variable name of request scope, see :ref:`setting error message in request scope <http_error_handler-error_messages>`.

.. tip::

  When using JSP, although error messages can be displayed by using :ref:`error display using custom tags <tag-write_error>`,
  compatibility with the CSS framework is poor because of the limitations of the DOM structure output by the custom tags.

  When an object is used in the request scope, the object in the request scope can be accessed directly even with JSP and the error message can be displayed as there is no limitation on the DOM structure.
  

The following is an implementation example of :ref:`Thymeleaf <web_thymeleaf_adaptor>`.

To display a message corresponding to a specific property
  :java:extdoc:`ErrorMessages#hasError <nablarch.fw.web.message.ErrorMessages.hasError(java.lang.String)>` and
  :java:extdoc:`ErrorMessages#getMessage <nablarch.fw.web.message.ErrorMessages.getMessage(java.lang.String)>`
  can be used to display the error or message corresponding to the property (value of the name attribute of the input item).

  In this example, the message is displayed if the request scope has an error message corresponding to the ``form.userName`` property.

  .. code-block:: html

    <input type='text' name='form.txt' />
    <span class="error" th:if="${errors.hasError('form.userName')}"
        th:text="${errors.getMessage('form.userName')}"> is to be entered. </span>

To display global messages (messages that are not associated with a property)
  :java:extdoc:`ErrorMessages#getGlobalMessages() <nablarch.fw.web.message.ErrorMessages.getGlobalMessages()>`
  can be used to display the global messages.

  .. code-block:: html

    <ul>
      <li th:each="message : ${errors.globalMessages}" th:text="${message}"></li>
    </ul>

To display all the messages
  :java:extdoc:`ErrorMessages#getAllMessages() <nablarch.fw.web.message.ErrorMessages.getAllMessages()>`
  can be used to display all messages.
  
  .. code-block:: html

    <ul>
      <li th:each="message : ${errors.allMessages}" th:text="${message}"> Error message </li>
    </ul>

