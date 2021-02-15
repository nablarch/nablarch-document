---------------------------------------------------
Initial Setup Procedure Supplementary Information
---------------------------------------------------

How to check H2 data
------------------------------------

When the data stored in H2 is to be checked for troubleshooting, start the H2 console as follows.

1. Execute h2/bin/h2.bat.

.. tip::

  Start h2.bat included in the project whose data is to be checked.


2. After a while, the browser will start, now enter each item as follows and click the [Test Connection] button.

============= ========================= ============================================================================
Item          Value                     Supplementary notes
============= ========================= ============================================================================
JDBC URL      ``jdbc:h2:../db/SAMPLE``  Specify the data file location with a relative path from h2.bat.
User Name     ``SAMPLE``
Password      ``SAMPLE``
============= ========================= ============================================================================

.. important ::

  The URL must be entered as above.
  You need to specify a relative path from h2.bat, so copy it from env.properties And the path is shifting.


3. Check that "Test successful" is displayed at the bottom of the screen.

4. Re-enter the Password field and click the [Connect] button.

.. important ::

  When clicking the [Connect] button, if the H2 data file does not exist at the specified URL, a new H2 data file is created.

  In order to avoid trouble, please click [Test Connection] as described in step 2, and confirm the existence of the data file.

5. Since the upper part of the right pane is the space for entering SQL, enter any SQL in this part.

6. The SQL can be executed by clicking the [Run] button (green button) at the top of the screen.

7. Disconnect by clicking the upper left disconnect button (button with the icon written in red).


.. important ::

  Projects generated from the archetype use the built-in mode of H2. When using the built-in mode, it will only accept connections from a single process.

  Therefore, **if you forget to disconnect, your application will not be able to connect to H2**.

.. _firstStepBuiltInTools:

Tools included in projects generated from archetypes
------------------------------------------------------------

The following tools are included in projects generated from archetypes.

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 7,8,18

  * - Tool
    - Maven Phase where the tool is executed
    - Supplementary notes
  * - :doc:`/development_tools/toolbox/JspStaticAnalysis/index`
    - verify
    -
  * - Obtain the coverage
    - test
    - Configuration has been completed to the point where jacoco.exec is generated.
      jacoco.exec can be used with SonarQube and Jenkins plugins.
  * - `Gsp-dba-maven-plugin (external site) <https://github.com/coastland/gsp-dba-maven-plugin>`_
    - －
    - Launch with "mvn -P gsp gsp-dba:<Goal name>". For example, generate-ddl can be executed
      with "mvn-P gsp gsp-dba: generate-ddl".

      By executing "mvn -P gsp generate-resources", "generate-ddl", "execute-ddl", "generate-entity", "load-data" and "export-schema" can be executed in order.


.. important ::

  You must understand the pom.xml of :ref:`about_maven_parent_module` before you change the configuration of the Tool.

  Understanding pom.xml will enable you to **easily** change the settings for many configuration items.

.. |br| raw:: html

  <br />
