
==============================================
Maven Archetype Configuration
==============================================
This chapter describes the Maven archetype configuration provided by Nablarch and overview of each directory and file.

.. contents:: Table of contents
  :depth: 2
  :local:


--------------------------------------------------
Overview of overall configuration
--------------------------------------------------


Nablarch offers the following archetypes: All the archetype group IDs are ``com.nablarch.archetype``.

.. list-table::
  :header-rows: 1
  :class: white-space-normal

  * - Artifact ID
    - Description
  * - nablarch-web-archetype
    - Archetype for using the web application runtime platform
  * - nablarch-jaxrs-archetype
    - Archetype for using the RESTful web service runtime platform
  * - nablarch-batch-ee-archetype
    - Archetype for using the JSR352-compliant batch application framework
  * - nablarch-batch-archetype
    - Archetype for using the Nablarch batch application runtime platform
  * - nablarch-batch-dbless-archetype
    - Archetype for using the Nablarch batch application runtime platform without DB connection
  * - nablarch-container-web-archetype
    - Docker container edition of the ``nablarch-web-archetype`` archetype
  * - nablarch-container-jaxrs-archetype
    - Docker container edition of the ``nablarch-jaxrs-archetype`` archetype
  * - nablarch-container-batch-archetype
    - Docker container edition of the ``nablarch-batch-archetype`` archetype

When ``pj-web``, ``pj-batch`` are specified respectively in ``artifactId``,
which is input during the project creation using nablarch-web-archetype and nablarch-batch-archetype archetypes, the configuration is as follows.


.. image:: maven_archetype.png

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 7,6,16

  * - Maven project name
    - Packaging
    - Application
  * - pj-web
    - war
    - Develop an application that uses the web application runtime platform.

      Finally, create in the unit to be deployed on the application server as war file.
  * - pj-batch
    - jar
    - Develop an application that uses the Nablarch batch application runtime platform.


.. tip::

  Automatically generated entity is generated when `gsp-dba-maven-plugin(external site) <https://github.com/coastland/gsp-dba-maven-plugin>`_ is used.
  The configuration description in :doc:`../addin_gsp` is required to use the plugin.

----------------------------------
Details of each component
----------------------------------

As in the case of pj-web and pj-batch above, the details of each component will be described assuming that the project was created according to the following table.

.. list-table::
  :header-rows: 1
  :class: white-space-normal

  * - Maven project name
    - Maven archetype
  * - pj-jaxrs
    - nablarch-jaxrs-archetype
  * - pj-batch-dbless
    - nablarch-batch-dbless-archetype
  * - pj-batch-ee
    - nablarch-batch-ee-archetype
  * - pj-container-web
    - nablarch-container-web-archetype
  * - pj-container-jaxrs
    - nablarch-container-jaxrs-archetype
  * - pj-container-batch
    - nablarch-container-batch-archetype

.. _about_maven_parent_module:

nablarch-archetype-parent (parent project)
============================================================

Summary
-------------

nablarch-archetype-parent is the parent project for the project created from each archetype.

This project cannot be directly re-written by the user.

The following configuration is mainly described in the project.

* Versions of various Maven plugins
* File path used by various tools

Location of nablarch-archetype-parent
-------------------------------------------------

If a project created from an archetype is built at least once, then pom.xml of nablarch-archetype-parent will be cached below the following hierarchy.
To check the configuration described in nablarch-archetype-parent, check the cached pom.xml.

.. code-block:: text

  <Home directory>/.m2/repository/com/nablarch/archetype/


pj-web project
==================

Project being packaged as a war file of the web application.

Project structure
---------------------------

.. code-block:: text

    myapp-web
    |
    |   pom.xml                     … Maven configuration file
    |   README.md                   … Supplementary explanation of this project (can be deleted after reading)
    |
    +---db                          … DDL and Insert statements for communication applications. Stored for each RDBMS.
    |
    +---h2
    |   +---bin                     … Contains files used to start H2.
    |   |
    |   \---db
    |           SAMPLE.mv.db        … Data file of H2.
    |           SAMPLE.mv.db.org    … Backup of H2 data files. If H2 does not start, copy it to "SAMPLE.mv.db" and use it.
    |
    +---src
    |   +---env                     … configuration files are stored for each environment.
    |   |
    |   +---main
    |   |   +---java                … Class of the communication confirmation application is stored.
    |   |   |
    |   |   +---resources           … The configuration file used in both the development environment and production environment are stored directly below.
    |   |   |   |
    |   |   |   +---entity          … Sample of ER diagram. Prepared as sample data when using the gsp-dba-maven-plugin.
    |   |   |   |
    |   |   |   \---net             … Contains the configuration file for the routing adapter.
    |   |   |
    |   |   \---webapp
    |   |       +---errorPages      … Sample of error screen is stored.
    |   |       |
    |   |       +---test            … File for communication confirmation screen is stored.
    |   |       |
    |   |       \---WEB-INF         … web.xml is stored.
    |   |
    |   \---test
    |       +---java                … Unit test for communication confirmation test is stored.
    |       |
    |       \---resources           … Configuration file for unit test is stored directly below.
    |           |
    |           +---data            … Prepared as sample data when using gsp-dba-maven-plugin.
    |           |
    |           \---nablarch        … Data for HTML check tool is stored.
    |
    \---tools                       … Configuration files of the tool used in conjunction with Maven is stored.


Tool configuration
-----------------------------------

The tools folder contains the configuration files for the tools used in conjunction with Maven.
The main directories and files are shown below.

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 9,20

  * - Directory or file
    - Description
  * - nablarch-tools.xml
    - Configuration file used while executing the JSP static analysis tool
  * - static-analysis/jspanalysis
    - Configuration file for the JSP static analysis tool is stored.


pj-jaxrs project
====================

Project packaged as a war file of the RESTful web service application.


Project structure
-------------------------------

Omitted because it is the same as web.


pj-batch-ee project
=======================

Project packaged as a jar file for JSR352-compliant batch applications.

.. _firstStepBatchEEProjectStructure:

Project structure
-----------------------------

(Descriptions of directories and files only for the elements that do not exist in web and batch)

.. code-block:: text

    myapp-batch-ee
    |
    |   pom.xml
    |   README.md
    |   distribution.xml                        … Configuration file used in maven-assembly-plugin
    |
    +---db
    |
    +---h2
    |   +---bin
    |   |
    |   \---db
    |           SAMPLE.mv.db
    |           SAMPLE.mv.db.org
    |
    +---src
        +---env
        |
        +---main
        |   +---java
        |   |
        |   \---resources
        |       |   batch-boot.xml              … Configuration files to be used when the batch is started.
        |       |
        |       +---entity
        |       |
        |       \---META-INF
        |           |   beans.xml               … File required to enable CDI.
        |           |
        |           +---batch-jobs
        |           |       sample-batchlet.xml … Job file of the application for communication confirmation of the batchlet architecture.
        |           |       sample-chunk.xml    … Job file of the application for communication confirmation of the chunk architecture.
        |           |       sample-etl.xml      … ETL function job file.
        |           |
        |           \---etl-config
        |                   sample-etl.json     … ETL function job configuration file.
        |
        |
        \---test
            +---java
            |
            \---resources
                |
                +---data

Release to production environment
-------------------------------------

The executable jar and dependent libraries of the batch application are stored in the zip file
generated under ``target`` during build of the batch application.

Therefore, while releasing to the production environment, batch can be executed with the following procedure.

1. Unzip the zip file into any directory.
2. Execute the batch with the following command.

  .. code-block:: bash

    java -jar <Executable jar file name> <Job name>

pj-batch project
============================

Project packaged as a jar file for Nablarch batch applications.

.. _firstStepBatchProjectStructure:

Project structure
------------------------------

(Descriptions of directories and files only for the elements that do not exist in the Web)

.. code-block:: text

    myapp-batch
    |
    |   pom.xml
    |   README.md
    |   distribution.xml                        … Configuration file used in maven-assembly-plugin
    |
    +---db
    |
    +---h2
    |   +---bin
    |   |
    |   \---db
    |           SAMPLE.mv.db
    |           SAMPLE.mv.db.org
    |
    +---src
        +---env
        |
        +---main
        |   +---java
        |   |
        |   +---resources
        |   |   |   batch-boot.xml              … Configuration file to be specified in on-demand batch when it is launched.
        |   |   |   mail-sender-boot.xml        … Configuration file to be specified while starting email send batch.
        |   |   |   resident-batch-boot.xml     … Configuration file to be specified while starting messaging using tables as queues.
        |   |   |
        |   |   \---entity
        |   |
        |   \---scripts                         … Shell script file to be used for starting a batch, etc. (use is optional)
        |
        \---test
            +---java
            |
            \---resources
                |
                \---data

Release to production environment
-------------------------------------

The executable jar and dependent libraries of the batch application are stored in the zip file
generated under ``target`` during build of the batch application.

Therefore, while releasing to the production environment, batch can be executed with the following procedure.

1. Unzip the zip file into any directory.
2. Execute the batch with the following command.

  .. code-block:: bash

    java -jar <Executable jar file name> ^
        -diConfig <Component configuration file > ^
        -requestPath <Request path> ^
        -userId <User ID>

pj-batch-dbless project
============================

Project packaged as a jar file for Nablarch batch applications without DB connection.

.. _firstStepDbLessBatchProjectStructure:

Project structure
------------------------------

Omitted because the DB-related directory and files are excluded from :ref:`pj-batch project structure <firstStepBatchProjectStructure>` .

Release to production environment
-------------------------------------

The executable jar and dependent libraries of the batch application are stored in the zip file
generated under ``target`` during build of the batch application.

Therefore, while releasing to the production environment, batch can be executed with the following procedure.

1. Unzip the zip file into any directory.
2. Execute the batch with the following command.

  .. code-block:: bash

    java -jar <Executable jar file name> ^
        -diConfig <Component configuration file > ^
        -requestPath <Request path> ^
        -userId <User ID>

.. _container_web_project_summary:

pj-container-web project
===============================

Project to build a Tomcat-based Docker image where the web application is deployed.

Project structure
------------------

.. code-block:: text

    myapp-container-web
    |
    |   pom.xml                     … Maven configuration file
    |   README.md                   … Supplementary explanation of this project (can be deleted after reading)
    |
    +---db                          … DDL and Insert statements for communication applications. Stored for each RDBMS.
    |
    +---h2
    |   +---bin                     … Contains files used to start H2.
    |   |
    |   \---db
    |           SAMPLE.mv.db        … Data file of H2.
    |           SAMPLE.mv.db.org    … Backup of H2 data files. If H2 does not start, copy it to "SAMPLE.mv.db" and use it.
    |
    +---src
    |   +---main
    |   |   +---java                … Class of the communication confirmation application is stored.
    |   |   |
    |   |   +---resources           … The configuration file used in both the development environment and production environment are stored directly below.
    |   |   |   |
    |   |   |   +---entity          … Sample of ER diagram. Prepared as sample data when using the gsp-dba-maven-plugin.
    |   |   |   |
    |   |   |   \---net             … Contains the configuration file for the routing adapter.
    |   |   |
    |   |   +---jib                 … It contains files to be placed against the container image.
    |   |   |
    |   |   \---webapp
    |   |       +---errorPages      … Sample of error screen is stored.
    |   |       |
    |   |       +---test            … File for communication confirmation screen is stored.
    |   |       |
    |   |       \---WEB-INF         … web.xml is stored.
    |   |
    |   \---test
    |       +---java                … Unit test for communication confirmation test is stored.
    |       |
    |       \---resources           … Configuration file for unit test is stored directly below.
    |           |
    |           +---data            … Prepared as sample data when using gsp-dba-maven-plugin.
    |           |
    |           \---nablarch        … Data for HTML check tool is stored.
    |
    \---tools                       … Configuration files of the tool used in conjunction with Maven is stored.
    
    
About src/main/jib
  Directories and files placed in ``src/main/jib`` will be placed on the container.
  For example, if place the ``src/main/jib/var/foo.txt`` file before building the container image, it enters the ``/var/foo.txt`` in the container.
  See `Jib's documentation (external site) <https://github.com/GoogleContainerTools/jib/tree/master/jib-maven-plugin#adding-arbitrary-files-to-the-image>`_ for more information.

  In the blank project, a number of Tomcat configuration files have been placed in order to make all of Tomcat's log output standard output.



Tool configuration
-----------------------------------

Omitted as it is identical to the web.


pj-container-jaxrs project
===============================

Project to build a Tomcat-based Docker image where the RESTful web services application is deployed.

Project structure
------------------

Omitted as it is identical to the container edition Web.

pj-container-batch project
===============================

Project to build a Docker image of a Linux Server where the Nablarch batch applications is deployed.

Project structure
------------------

(Descriptions of directories and files only for the elements that do not exist in the container edition Web.)

.. code-block:: text

    myapp-container-batch
    |
    |   pom.xml
    |   README.md
    |
    +---db
    |
    |
    +---h2
    |   +---bin
    |   |
    |   \---db
    |           SAMPLE.mv.db
    |           SAMPLE.mv.db.org
    |
    +---src
        +---main
        |   +---java
        |   |
        |   +---jib
        |   |
        |   +---resources
        |   |   |   batch-boot.xml              … Configuration file to be specified in on-demand batch when it is launched.
        |   |   |   mail-sender-boot.xml        … Configuration file to be specified while starting email send batch.
        |   |   |   resident-batch-boot.xml     … Configuration file to be specified while starting messaging using tables as queues.
        |   |   |
        |   |   \---entity
        |   |
        |   \---scripts                         … Shell script file to be used for starting a batch, etc. (use is optional)
        |
        \---test
            +---java
            |
            \---resources
                |
                \---data
                
.. _about_maven_web_batch_module:

Common configurations for each project
=========================================================

The following is configured respectively in each Maven project.

* Defining profiles
* Adding goals to be executed during the build phase
* Configuration for compile. The following configurations are present.

  *	Java version used
  *	File encoding
  *	JDBC driver
* Configuration of the tools described in :ref:`firstStepBuiltInTools`. The following configurations are present.

  * Database connection configuration used in `gsp-dba-maven-plugin(external site) <https://github.com/coastland/gsp-dba-maven-plugin>`_  (JDBC connection URL and database schema, etc.)
  * Coverage configuration


Details of each are shown below.


.. _mavenModuleStructuresProfilesList:

Profile list
----------------

Refer to ``pom.xml`` of each project for details on the profile that are defined.

The defined profiles are shown below.

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 4,18

  * - Profile name
    - Summary
  * - dev
    - Profile for development environment and unit test execution. Use resources in src/env/dev/resources directory.
  * - prod
    - Profile for the production environment. Use resources in the src/env/prod/resources directory.


.. tip::
   The activeByDefault element is described in dev profile of ``pom.xml`` and the dev profile can be used as default.

.. note::
   In a project for containers, the differences between environments switch using OS environment variables instead of profiles.
   Therefore, the project for containers has no profile defined.
   See :ref:`container_production_config` for more information.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
How to use profiles
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These profiles are used to create deliverables according to the environment.

For example, to create a war file for the production environment, specify the production environment profile
under the ``pj-web`` module and then execute the mvn command by specifying the production environment profile.

An example of the command is shown below.

.. code-block:: bash

   mvn package -P prod -DskipTests=true

.. tip ::

  In the above command, the unit test is skipped.

  By default, the unit test is also performed when the "mvn package" is executed, but the unit test fails to run in the production profile.


List of goals added to the build phase
-------------------------------------------------------

In addition to the default build phase definition of Maven, it is configured to execute the following goals

For details on the configuration, see ``pom.xml`` of each project and ``pom.xml`` of :ref:`about_maven_parent_module`.

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 5,8,9

  * - Build phase
    - Goal
    - Summary
  * - initialize
    - jacoco:prepare-agent
    - Prepare a JaCoCo runtime agent.
  * - pre-integration-test
    - jacoco:prepare-agent-integration
    - Prepare a JaCoCo runtime agent for the integration test.


.. tip::
  Since the execution of gsp-dba-maven-plugin is not tied together with the Maven build phase, goals implemented under gsp-dba-maven-plugin, such as automatic generation of entities, should be executed manually.


Configuration for compile
-----------------------------------

For details on the configuration, see ``pom.xml`` of each project and ``pom.xml`` of :ref:`about_maven_parent_module`.


Tool configuration
-----------------------------------

Tool configuration is described in ``pom.xml`` (each project and :ref:`about_maven_parent_module`).
Refer to :ref:`firstStepBuiltInTools` for the tools described in the parent project.


Build configuration
==============================================

For the following cases, change pom.xml of each module.

* Add or change the dependent library used in each module. For example, modify the version of nablarch-bom to change the version of Nablarch being used.
* Add or change the Maven plugin used in each module.

Example of changing the version of Nablarch used
-------------------------------------------------------------------

A configuration example when Nablarch 5u6 is used is shown below.

.. code-block:: xml

  <dependencyManagement>
    <dependencies>
      <dependency>
        <groupId>com.nablarch.profile</groupId>
        <artifactId>nablarch-bom</artifactId>

        <!--
        Specify the version corresponding to the version of Nablarch to be used.
        In this example 5u6 is specified.
        -->
        <version>5u6</version>

        <type>pom</type>
        <scope>import</scope>
      </dependency>
      …
  </dependencyManagement>


Example of adding dependent library
-------------------------------------------

An example of adding dependency to the nablarch-common-encryption for using the encryption utility in the ``pj-web`` module is shown below.

While adding dependency, scope should be configured appropriately. If the scope is not configured, there is a possibility of the module that should be used only in the unit tests might get used in the production.

.. code-block:: xml

  <dependencies>
  …
    <dependency>
      <groupId>com.nablarch.framework</groupId>
      <artifactId>nablarch-common-encryption</artifactId>
    </dependency>
  …
  </dependencies>


For Nablarch libraries, usually the version number need not be specified in pom.xml (since the version specified for nablarch-bom determines the version of each library)



.. _mavenModuleStructuresModuleDivisionPolicy:

--------------------------------------------------------
[Reference] Policy for splitting the projects
--------------------------------------------------------

Policy for recommended project configuration
================================================

The following are the policy of the recommended project configuration.

* If only one application is to be created (web only, batch only, etc.), then configure a single project respectively.
* If two web applications are to be created for internal and external use, create separate Maven projects instead of consolidating them into a single Maven project.
* If there are multiple applications and a library is to be shared, create a Maven project to deploy the shared library.
* While adding a runtime platform, create a Maven project for each execution control platform. For example, to add an application that uses the messaging execution control platform, create a new Maven project.
* Do not split the project more than necessary. For details, see :ref:`mavenModuleStructuresProblemsOfExcessivelyDivided`.

.. tip ::

  Be careful not to duplicate resources when you split up a project.

  For example, if you mix the edm files used by `gsp-dba-maven-plugin(external site) <https://github.com/coastland/gsp-dba-maven-plugin>`_ in multiple Maven projects,
  you will end up with duplicate entity classes in multiple Maven projects.

.. _mavenModuleStructuresProblemsOfExcessivelyDivided:

Problems when a project is divided excessively
==========================================================

Problems caused when a project is divided excessively is shown below.

* Build and deployment procedure becomes complicated.
* After the integration test, the management of modules that were combined and tested becomes complicated.

In general, smaller the number of Maven projects, smoother is the development.

.. |br| raw:: html

  <br />
