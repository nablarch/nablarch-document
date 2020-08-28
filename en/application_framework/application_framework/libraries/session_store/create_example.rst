.. _`create_example`:

Implementation Example with Registration Function
=====================================================================

Initial display of input screen
---------------------------------------------------------------------
.. code-block:: java

  // Delete because the session may remain when the browser is closed directly
  SessionUtil.delete(ctx, "project");

Transition from the input screen to the confirmation screen
---------------------------------------------------------------------
.. code-block:: java

  // Acquire input information from the request scope
  ProjectForm form = context.getRequestScopedVar("form");

  // Convert Form to Entity
  Project project = BeanUtil.createAndCopy(Project.class, form);

  // Save input information in session store
  SessionUtil.put(ctx, "project", project);

Return from the confirmation screen to the input screen
---------------------------------------------------------------------
.. code-block:: java

  // Fetch input information from the session store
  Project project = SessionUtil.get(ctx, "project");

  // Convert Entity to Form
  ProjectForm form = BeanUtil.createAndCopy(ProjectForm.class, project);

  // Configure input information to the request scope
  context.setRequestScopedVar("form", form);

  // Delete the input information from the session store
  SessionUtil.delete(ctx, "project");

Execute the registration process
---------------------------------------------------------------------
.. code-block:: java

  // Fetch input information from the session store
  Project project = SessionUtil.get(ctx, "project");

  // Registration process is omitted

  // Delete the input information from the session store
  SessionUtil.delete(ctx, "project");
