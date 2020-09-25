.. _`project_delete`:

Create a Delete Function
==========================================
This section describes the delete function based on an example application.

Description of the function to be created
  1. Click the project ID in the project list.

    .. image:: ../images/project_delete/project_delete_list.png
      :scale: 80

  2. Click the change(変更) button on the details screen.

    .. image:: ../images/project_delete/project_delete_detail.png
      :scale: 80

  3. Click the delete (削除) button on the update screen.

    .. image:: ../images/project_delete/project_delete_update.png
      :scale: 60

  4. The completion screen is displayed.

    .. image:: ../images/project_delete/project_delete_complete.png
      :scale: 80

Delete
-----------
The basic implementation method of the delete function is described in the following order:

  #. :ref:`Create a delete button on the update screen<project_delete-update>`
  #. :ref:`Create a business action method for deletion<project_delete-delete_action>`
  #. :ref:`Create a deletion completion screen<project_delete-complete>`

.. _`project_delete-update`:

Create a delete button on the update screen
  Create a delete button on the update screen.
  For description on creating the update screen, see :ref:`create business action method to display the update screen<project_update-create_edit_action>` and
  :ref:`create update screen JSP<project_update-create_update_jsp>`.

.. _`project_delete-delete_action`:

Create a business action method for deletion
  Create a business action method to delete the target project from the database.

  ProjectAction.java
    .. code-block:: java

      @OnDoubleSubmission
      public HttpResponse delete(HttpRequest request, ExecutionContext context) {

          // The project information is stored in the session when the update screen is displayed
          Project project = SessionUtil.delete(context, "project");
          UniversalDao.delete(project);

          return new HttpResponse(303, "redirect://completeOfDelete");
      }

  Key points of this implementation
    * Deletion with the primary key can be performed without creating SQL by executing :java:extdoc:`UniversalDao#delete <nablarch.common.dao.UniversalDao.delete(T)>`
      with the entity set in the primary key as an argument.

  .. tip::

    :ref:`universal_dao` provides only the function to delete with the primary key as a condition. When deleting with a condition other than the primary key, a separate SQL is required to be created and executed.
    For information on how to execute SQL, see :ref:`execute SQL by specifying SQL ID<database-execute_sqlid>`.

.. _`project_delete-complete`:

Create a deletion completion screen
  Displays the deletion completion screen.
  For description on creating the completion screen, see  :ref:`create business action method to display the completion screen<project_update-create_complete_action>` and
  :ref:`create update completion screen<project_update-create_success_jsp>`.

This completes the description of the deletion function.

:ref:`Getting Started To TOP page <getting_started>`