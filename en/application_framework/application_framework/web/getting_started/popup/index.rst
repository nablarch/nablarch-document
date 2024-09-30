.. _`client_popup`:

Create a Pop-up Screen
==========================================
This section describes how to create a pop-up screen based on an example application.

The pop-up screen is not created in a separate window as described :ref:`tag-submit_popup`, but in a dialog format.

Description of the function to be created
  1. Click the Change(変更) button on the Project Details screen.

    .. image:: ../images/popup/popup-project_update_btn.png
      :scale: 80

  2. Click the search button in the client field.

    .. image:: ../images/popup/popup-project_update.png
      :scale: 75

  3. The client search screen is displayed in a dialog. Click the search(検索) button.

    .. image:: ../images/popup/popup-popup_init.png
      :scale: 60

  4. Click the client ID link in the search results.

    .. image:: ../images/popup/popup-popup_search.png
      :scale: 80

  5. The client search screen is closed, and the selected values are set to the client ID and client name on the project change screen.

    .. image:: ../images/popup/popup-complete.png
      :scale: 80

Display a pop-up (dialog) screen
------------------------------------------------
The pop-up (dialog) display is realized using OSS (Bootstrap).
For more information, see  `Bootstrap documentation (external site) <https://fezvrasta.github.io/bootstrap-material-design/>`_ .

.. _`popup-action`:

Create a business action method
  Search for a client and pass the results of the selection to the parent screen.
  
  This function realizes the search process by calling Ajax from a dialog.
  For information on how to implement action classes, see :ref:`restful_web_service`.

.. _`popup-popup_jsp`:

Create a JSP for the pop-up screen
  Use jQuery to build a DOM based on the result of the Ajax call and display the result.
  Since jQuery is used, the detailed explanation is omitted.
  
  For more information, see `Documentation (external site) <https://jquery.com/>`_ .

.. _`popup-parent_hand_over`:

Create a JavaScript function to pass a value from the pop-up screen to the parent window
  Use jQuery to set the information in the dialog to the client name and client ID part.
  Since jQuery is used, the detailed explanation is omitted.
  
 For more information, see `Documentation (external site) <https://jquery.com/>`_ .
  
This completes the explanation of the pop-up screen.

:ref:`Getting Started To TOP page <getting_started>`