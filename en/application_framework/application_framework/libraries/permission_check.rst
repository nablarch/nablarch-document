Permission Check
=====================================================================
Provide the permission check function to check whether a user is permitted to use system functions.

Nablarch provides the following two types of permission check functions.

.. toctree::
  :maxdepth: 1

  authorization/permission_check
  authorization/role_check

.. tip::
  **Differences in the use of each function**

  :doc:`authorization/role_check` reduces the complexity of data management by simplifying the model structure of authority management and partially hard-coding the linkage between processing and data.
  Therefore, it is suitable for systems where the conditions for authority management remain basically the same and where you want to quickly introduce authority management at a small cost.
  
  On the other hand, in a system where the conditions for authority management may change, :doc:`authorization/permission_check` is suitable for authority management with solid data management, although the cost of implementation will increase.
  
  For details, see the respective descriptions.