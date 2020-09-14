.. _file_path_management:

File path management
==================================================
.. contents:: Table of contents
  :depth: 3
  :local:

Provides a function to manage the input/output directories and extensions of files used in the system.


Function overview
--------------------------------------------------

Manage directories and extensions with logical names
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Directories and extensions can be managed with logical names.

The file input/output function enables realization of input/output for the files under the directory simply by specifying the logical name.

For details, see  :ref:`file_path_management-definition` .

Module list
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core</artifactId>
  </dependency>

How to use
--------------------------------------------------

.. _file_path_management-definition:

Configure the directory and extension
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Configure the directory and extension in :java:extdoc:`FilePathSetting <nablarch.core.util.FilePathSetting>`  and define in the component configuration file.

An example is shown below.

Point
  * Set the component name of :java:extdoc:`FilePathSetting <nablarch.core.util.FilePathSetting>`  to  ``filePathSetting`` .
  * Configure the directory in :java:extdoc:`basePathSettings <nablarch.core.util.FilePathSetting.setBasePathSettings(java.util.Map)>` 
  * Configure the extension in :java:extdoc:`fileExtensions <nablarch.core.util.FilePathSetting.setFileExtensions(java.util.Map)>` . 
  * When configuring multiple extensions for one directory, set multiple logical names.
  * If the file has no extension, omit the extension configuration for that logical name.
  * The scheme can be  ``file``  and ``classpath`` . If omitted,  ``classpath``  is used.
  * For the ``classpath``  scheme, the path must exist as a directory. (The path in archived files such as jar cannot be specified)
  * Spaces cannot be included in the path. (Path with spaces cannot be specified)

  .. important::

    When the classpath scheme is used, this function cannot be used with some web application servers. 
    This is because the web application server uses its own file system to manage the resources under the classpath.

    For example, a virtual file system called vfs manages the resources under the classpath in Jboss and Wildfly and the classpath scheme cannot be used.

    Therefore, using file scheme instead of classpth scheme is recommended.



.. code-block:: xml

  <component name="filePathSetting" class="nablarch.core.util.FilePathSetting">
    <!-- Configuration of directory-->
    <property name="basePathSettings">
      <map>
        <entry key="csv-input" value="file:/var/nablarch/input" />
        <entry key="csv-output" value="file:/var/nablarch/output" />

        <entry key="dat-input" value="file:/var/nablarch/input" />
        <entry key="fixed-file-input" value="file:/var/nablarch/input" />
      </map>
    </property>

    <!-- Configuration of extension-->
    <property name="fileExtensions">
      <map>
        <entry key="csv-input" value="csv" />
        <entry key="csv-output" value="csv" />

        <entry key="dat-input" value="dat" />

        <!-- Extension is not configured as fixed-file-input does not have an extension -> -->
      </map>
    </property>

  </component>

Acquire the file path indicated by the logical name
----------------------------------------------------------
Use :java:extdoc:`FilePathSetting <nablarch.core.util.FilePathSetting>`  to acquire the file path corresponding to the logical name.

Several usage examples are shown below.

.. code-block:: java

  // /var/nablarch/input/users.csv
  File users = filePathSetting.getFileWithoutCreate("csv-input", "users")

  //  /var/nablarch/output
  File csvOutputDir = filePathSetting.getBaseDirectory("csv-output");

  // /var/nablarch/input/users
  File users = filePathSetting.getFileWithoutCreate("fixed-file-input", "users")

