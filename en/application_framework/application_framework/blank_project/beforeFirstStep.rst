=============================
Before Initial Setup
=============================

.. contents:: Table of contents
  :depth: 2
  :local:


----------------------------------------------------------
Blank project (project template)
----------------------------------------------------------

Blank project types
----------------------------------------------------------

The initial setup shows how to create the following blank project.

* Web projects
* RESTful web service project
* JSR352-compliant batch project
* Nablarch batch project
* Web project for container
* RESTful web service project for container
* Nablarch batch project for container


Blank project design concept and points to note
----------------------------------------------------------

Blank projects created during initial setup emphasize the ease of initial build.Therefore, all source and resource files are placed in one project so that each application can be built in one project.
Component definitions and dependencies are defined to operate with the minimum handler configuration.

After the initial setup (not necessarily immediately), the architect needs to consider the project structure.
For example, it is better to consider the necessity of a project for common parts in the following cases.

* Multiple applications (such as web application and batch application) constitute the system.
* Common components (for example, entity class) exist between applications.


When examining the project configuration, refer to :ref:`mavenModuleStructuresModuleDivisionPolicy` before examining the project configuration.


.. _firstStepPreamble:

----------------------------------------------------------
Prerequisites for initial setup
----------------------------------------------------------

The following software are assumed to be installed in the execution environment.

All projects
  * Maven 3.0.5 or higher

Web, RESTful web service, JSR352-compliant batch, Nablarch batch
  * JDK1.8 or higher

Web for container, RESTful web service for container, Nablarch batch for container
  * JDK11 or higher
  * Docker Desktop 2.2.0.0 or higher

The following do not require advance preparation in the initial setup.

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 4,20

  * - Software
    - Description
  * - AP server
    - Use Tomcat8 to confirm the communication between the web project and RESTful web service project. Since the waitt-maven-plugin is executed from the mvn command, and the application is deployed and launched to Tomcat8 embedded in the waitt-maven-plugin during the procedure, advance preparation is not required.
  * - DB server
    - Since the H2 Database Engine (hereinafter H2) is incorporated in the archetype for communication confirmation, separate installation is not required.



----------------------------------------------------------
Configuration of Maven
----------------------------------------------------------

Before the initial setup, configure settings.xml of Maven so that Nablarch and related modules can connect to the available Maven repository.

If the xml file is not configured, refer to :ref:`mvnSetting` and configure.

.. important ::

  In the following steps, if you run into any problems that you think are Maven-related, please refer to :ref:`mvnFrequentlyTrouble`.


----------------------------------------------------------
Specifying the version of Nablarch to use
----------------------------------------------------------

Nablarch uses the bom mechanism of Maven to define the version of each module that constitutes the Nablarch framework.

When generating a blank project using the Maven command, it is necessary to specify the version of nablarch-bom as the version of Nablarch to be used.

Definition in nablarch-bom (excerpt)

.. code-block:: xml

  <dependencyManagement>
    <dependencies>

      <dependency>
        <groupId>com.nablarch.framework</groupId>
        <artifactId>nablarch-core</artifactId>
        <version>1.2.2</version> <!-- Defining the version of nablarch-core module -->
      </dependency>

      <dependency>
        <groupId>com.nablarch.framework</groupId>
        <artifactId>nablarch-core-applog</artifactId>
        <version>1.0.1</version> <!-- Defining the version of nablarch-core-applog module -->
      </dependency>


The specified version is reflected in pom.xml of the generated blank project as follows.

.. code-block:: xml

  <dependencyManagement>
    <dependencies>
      <dependency>
        <groupId>com.nablarch.profile</groupId>
        <artifactId>nablarch-bom</artifactId>
        <version>5u6</version> <!--  Specified version -->
        <type>pom</type>
        <scope>import</scope>
      </dependency>
    </dependencies>
  </dependencyManagement>


----------------------------------------------------------
Common precautions for initial setup
----------------------------------------------------------

When performing the initial setup, note the following points.

* Do not include multi-byte characters in the path of the directory where the blank project is created.
  An error may occur as some maven plugins do not work properly if multi-byte characters are included.
* Execute "mvn archetype:generate" from the command line. If it is executed from eclipse4.4.2, unintended files are output.
* Sometimes you get an error about Maven's life cycle when you open a blank project you created in eclipse.

    * Example error message: Plugin execution not covered by lifecycle configuration
    * If this error occurs, eclipse will suggest the installation of the plugin, and you can resolve it by following the suggestion and installing the plugin.
    * If the network environment is unstable, each developer may take time to install the plug-ins, so you should consider measures such as distributing eclipse with the plug-ins installed in advance.
