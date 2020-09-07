=========================================
Job Screen JSP Validation Tool
=========================================

.. contents::
   :local:
   :depth: 2
   :backlinks: none


-----------------------------------------
Summary
-----------------------------------------

This tool performs the following verifications on JSP files.

Also, it has the capability to change the verification contents in the settings file, and the verification content itself can be added.

**Implemented**

  * It can verify to ensure that only the tags that are permitted to be used, are used in the JSP of the business screen.
  * It can verify that the required structure is satisfied in the JSP.
  * It can verify that the prohibited structure is not being used in the JSP.
  * It can verify that the attributes specified for each tag are indeed the attributes defined for each tag.

**Not implemented**

  * It can verify that attribute value of each tag corresponds to the type of attribute.


-----------------------------------------
Initial Environment Construction
-----------------------------------------


Node.js installation
=========================================

Since this tool depends on `Node.js <http://nodejs.org/>`_ , the installer from the below site based on the environment being used is to be downloaded and installed.

  http://nodejs.org/


Check environment variables
=========================================

When performing the below procedure under a proxy environment, the below values of the environment variables are to be checked.

=========================================== ======================================================
Explanatory variable name                                  Value
=========================================== ======================================================
HTTP_PROXY                                  URL of the proxy server for HTTP
HTTPS_PROXY                                 URL of the proxy server for HTTPS
=========================================== ======================================================


Install dependent packages
=========================================

This tool is dependent on multiple open source libraries. (To know more about the libraries that the tool depends on, refer to `package.json`.)

To install the libraries, execute the below command in the root directory (directory where `package.json` is saved) of this tool.

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 10,5,18


  * - Execution directory
    - Command
    - Details to be checked

  * - Root directory of this tool (directory where `package.json` is saved.)
    - `npm install`
    - * The command must have been completed successfully.
      * The `node_modules`\ directory must be created in the root directory.


.. important::

   To install the dependent package according to the above procedure, the environment needs to be connected to the Internet.

   Also, if a proxy environment is used, it is necessary for the proxy server address to be configured to the below environment variables.

   * http_proxy ：example: http_proxy=http://proxy.example.com:8080
   * https_proxy ：example: https_proxy=http://proxy.example.com:8080

   Also, if installed in an environment that is not connected to the Internet, 
   it can be used by initially performing the above procedures in an environment connected to the Internet, 
   and placing the `node_modules` directory created in the root directory, 
   in the root directory of this tool that has been extracted in the target environment.


Confirm if it can be used normally.
=========================================

Ensure that all tests are successful by executing the below commands in the root directory of this tool.

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 14,5,13


  * - Execution directory
    - Command
    - Details to be checked

  * - Root directory of this tool (directory where `package.json` is saved.)
    - `npm test`
    - * Success of all tests.

Modification of environment dependency setting value.
=================================================================

Modify the below setting value of verification_config.json at the directory where the actual tag file is saved.

.. code-block:: json

    {
      "TagAttributeVerifier" : {
        "directory" : "C:\\nablarch\\workspace\\tutorial\\main\\web\\WEB-INF\\tags\\widget",
        "encoding" : "utf-8"
      }
    }



-----------------------------------------
How to Use the tool
-----------------------------------------


Execute with a bat file
=========================================

Drag and drop the file to `jsp_verifier.bat` that is in the root directory of this tool.

If a command line window is displayed and there are 0 verification errors,

Verification Succeeded.

Is displayed, and if there are one or more verification error,

Verification Failed!! |br|
12 violations are found. |br|
Detected violations are dumped to violations-1390366626297.log.

The file name where the error content is output is displayed like this.



Execution from command line.
=========================================

The below commands are executed in the root directory of this tool.

.. code-block:: sh

   node bin/jsp_verifier <Verification target JSP file path(s)>

The output contents of the standard output are as above.


-----------------------------------------
Configuration method
-----------------------------------------

`verification_config.json` of the root directory is the configuration file of this tool. 
Verification is performed by detailing the verification contents to be executed in this file and settings of each verification content.

.. important::

  In the below example configuration file, for the purpose of explanation, though comments are written in JavaScript format, comments cannot be written in the actual JSON file.

.. code-block:: javascript

  {
    // Verification contents to be implemented are described in verifiers.
    "verifiers": {
      // Verification of tags that can be used
      "TagUsageVerifier": {
      }
      // Regular expression verification
      "RegexpBasedVerifier": {
      }
      // DOM tree verification
      "SelectorBasedVerifier": {
      }
      // Parent tag verification
      "WrappingTagVerifier": {
      }
      // Tag attribute verification
      "TagAttributeVerifier": {
      }
      // Verification not defined here will not be performed
    }
  }

Default setting contents
=========================================

Verification of tags that can be used
-----------------------------------------

Only the below tags that have usage permission are to be used.

* n:form
* n:set
* n:write
* n:ConfirmationPage
* n:forConfirmationPage
* n:forInputPage
* n:param
* n:hidden
* t:page_template
* t:errorpage_template
* box:.*
* button:.*
* field:.*
* link:.*
* tab:.*
* table:.*
* column:.*
* spec:.*
* c:if
* jsp:attribute
* %--
* %\@page
* %\@taglib

Regular expression verification
-----------------------------------------

Strings matching the below regular expression are not recognized (uppercase/lowercase not sensitive).

* /> (Self terminating element. If a self-terminating element is used, as the description content cannot be drawn after that element, it is prohibited)

DOM tree validation
-----------------------------------------

The below prohibited structures are not to be used.

* table:not([id]) （As IDs is required when displaying multiple tables, ID is forced on the table.）
* table:not([listSearchInfoName]) （listSearchInfoName is forced as the number of results cannot be displayed if the table does not have listSearchInfoName.）

Parent tag verification
-----------------------------------------

The below required structure is to be satisfied.

* The table widget must be enclosed with n:form.
* The button widget needs to be enclosed with n:form.
* The widget displayed in the screen item definition in the design view must be enclosed by spec:layout.

Tag attribute verification
-----------------------------------------

The attribute of the tag (the one with the tag file stored under C:\\nablarch\\workspace\\tutorial\\main\\web\\WEB-INF\\tags\\widget) being used in JSP should be the actual attribute that defines the tag.



.. |br| raw:: html

  <br />