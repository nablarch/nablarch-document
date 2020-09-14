Implementation Example with Update Function
=====================================================================

Initial display of input screen
---------------------------------------------------------------------
.. code-block:: java

  // Delete because the session may remain when the browser is closed directly
  SessionUtil.delete(ctx, "project");

  // Acquisition process of the update target data is omitted

  // Save the data to be updated in the session store
  SessionUtil.put(ctx, "project", project);

  // Convert Entity to Form
  ProjectForm form = BeanUtil.createAndCopy(ProjectForm.class, project);

  // Configure the update target data to the request scope
  context.setRequestScopedVar("form", form);

Transition from the input screen to the confirmation screen
---------------------------------------------------------------------
.. code-block:: java

  // Acquire input information from the request scope
  ProjectForm form = context.getRequestScopedVar("form");

  // Acquire update target data from the session store
  Project project = SessionUtil.get(context, "project");

  // Overwrite the input information with the update target data
  BeanUtil.copy(form, project);

Return from the confirmation screen to the input screen
---------------------------------------------------------------------
.. code-block:: java

  // Acquire the update target data from the session store
  Project project = SessionUtil.get(ctx, "project");

  // Convert Entity to Form
  ProjectForm form = BeanUtil.createAndCopy(ProjectForm.class, project);

  // Configure the update target data to the request scope
  context.setRequestScopedVar("form", form);

Execute the update process
---------------------------------------------------------------------
.. code-block:: java

  // Acquire the update target data from the session store
  Project project = SessionUtil.get(ctx, "project");

  // Update process is omitted

  // Delete the update target data from the session store
  SessionUtil.delete(ctx, "project");
