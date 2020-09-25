=========================
 Master Data Input Tool
=========================

.. tip::

  If you build a project using :ref:`blank_project`, :ref:`gsp-dba-maven-plugin <gsp-maven-plugin>` will be configured as a database-related tool.

  Therefore, the use of :ref:`gsp-dba-maven-plugin  <gsp-maven-plugin>` is recommended instead of this tool to submit the master data to the database.

.. important::

  This tool does not support the multi-thread function. 
  Testing of multi-thread functions should be performed with tests that do not use the testing framework (such as integration tests).

.. toctree::
   :maxdepth: 1
   
   ./01_MasterDataSetupTool
   ./02_ConfigMasterDataSetupTool

