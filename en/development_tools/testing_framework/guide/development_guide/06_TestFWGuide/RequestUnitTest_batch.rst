.. _request-util-test-batch:

========================================
 Request Unit Test (Batch Process)
========================================


Summary
========

Request unit tests (batch process) simulate and test the behavior of the batch when it is actually launched from the command line.




Overall picture
------------------

.. image:: ./_images/batch_request_test_class.png
   :scale: 70



Main Classes, resources
==============================

+----------------------+---------------------------------------------------------------------------+-------------------------------------------+
|Name                  |Role                                                                       | Creation unit                             |
+======================+===========================================================================+===========================================+
|Request unit\         |Implement the test logic.                                                  |Create one per class (Action) to be tested.|
|Test class            |                                                                           |                                           |
+----------------------+---------------------------------------------------------------------------+-------------------------------------------+
|Excel file \          |Describe test data, such as preparation data to be stored in the table, \  |Create one per test class                  |
|（Test data）         |expected results and input files.                                          |                                           |
+----------------------+---------------------------------------------------------------------------+-------------------------------------------+
|StandaloneTest\       |Provides a test execution environment for batch, messaging, \              | \-                                        |
|SupportTemplate       |and other processes that run outside the container.                        |                                           |
+----------------------+---------------------------------------------------------------------------+-------------------------------------------+
|BatchRequest\         |Provides test preparation function and \                                   | \-                                        |
|TestSupport           |various asserts required for batch request unit test.                      |                                           |
+----------------------+---------------------------------------------------------------------------+-------------------------------------------+
|TestShot              |A class that stores information for one test case defined in a datasheet.\ | \-                                        |
|                      |                                                                           |                                           |
+----------------------+---------------------------------------------------------------------------+-------------------------------------------+
|MainForRequestTesting |Main class for testing. Absorb the differences during test execution.      | \-                                        |
+----------------------+---------------------------------------------------------------------------+-------------------------------------------+
|DbAccessTestSupport   |Provides the necessary functions for testing using the database, \         | \-                                        |
|                      |such as DB preparation data input.                                         |                                           |
+----------------------+---------------------------------------------------------------------------+-------------------------------------------+
|FileSupport           |Provides the necessary functions for testing using the file, \             | \-                                        |
|                      |such as preparation of input file.                                         |                                           |
+----------------------+---------------------------------------------------------------------------+-------------------------------------------+


Structure
==========


StandaloneTestSupportTemplate
-----------------------------
Provides a test execution environment for batch, messaging, and other processes that run outside the container. 
Reads test data and executes all test shots (\ `TestShot`_ \ ).

TestShot
--------

Executes by holding information of 1 TestShot. \
The TestShot consists of the following elements:


* Preparation of input data
* Launch the main class
* Confirm the output results

Provides common preparation process and result checking functions for testing processes that operate outside of containers, 
such as batch and messaging processes.

 +----------------------------+----------------------------+
 | Preparation process        | Confirmation of results    |
 +============================+============================+
 | Database setup             | Check for database updates |
 |                            +----------------------------+
 |                            | Check log output results   |
 |                            +----------------------------+
 |                            | Confirm the status code    |
 +----------------------------+----------------------------+

Since the input data preparation and result confirmation logic is different for each batch and various messaging processes, \
it can be customized according to the architecture.


BatchRequestTestSupport
-----------------------

Superclass for batch process tests. \
The application programmer creates a test class by inheriting this class.

This class adds the following functions to the preparation process and result confirmation provided by \ `TestShot`_ \.

 +----------------------------+---------------------------------------+
 | Preparation process        | Confirmation of results               |
 +============================+=======================================+
 |Prepare input file          |Check the contents of the output file  |
 +----------------------------+---------------------------------------+

By using this class, the test source and test data of the request unit test can be standardized, \ 
and description of test source can be significantly reduced.

For the specific usage method, refer to \ :doc:`../05_UnitTestGuide/02_RequestUnitTest/batch`\ .


MainForRequestTesting
---------------------

Main class for request unit test. \
The primary differences from the main class for production are as follows.

* Initialize the system repository from the component configuration file of the test.
* Disable the resident function.


FileSupport
--------------

A class that provides operations related to files. 
Primarily, the following functions are provided.

* Creates an input file from the test data.
* Compares the expected value of the test data with the actual output file and its contents.

File operations are provided as an independent class because they are necessary for other than batch processing (for example, file download).


Test data
============

The test data specific to the batch process is described.


 .. _`about_fixed_length_file`:

Fixed-length file
---------------------

For the basic description, see :ref:`batch_request_test`.

Padding
~~~~~~~~~~

If the byte length of the data is shorter than the specified field length, 
padding is added to the data according to the data type of the field. 
The algorithm used for padding is the same algorithm used for the main body of the Nablarch Application Framework.


How to write binary data
~~~~~~~~~~~~~~~~~~~~~~~~

To represent binary data, write the test data in hexadecimal format. 
For example, when written as \ ``0x4AD``\ , it is interpreted as a byte array of 2-bytes expressed as \ ``0000 0100 1010 1101``\ (\ ``0x04AD``\ ).

.. tip::
 If the test data is not pre-fixed with 0x, the data is considered a string, 
 and the string is encoded with the character code of the directive and converted to a byte array.
 
 For example, if \ ``4AD``\  is written in the field of the binary type test data of a file with Windows-31J character code, 
 it is converted to a byte array of 3-bytes expressed as \ ``0011 0100 0100 0001 0100 0100``\  (\ ``0x344144``\ ).
  

Variable length file
--------------------------

For the basic description, see :ref:`batch_request_test`.

Various configuration values
===================================

Handler configuration of resident batch test
-----------------------------------------------------
When performing a resident batch test, the handler configuration for production has to be changed for the test. 
If the test is performed without making this change, the test will not be implemented successfully because the process of the resident batch application that is being tested will not finish.

**[Handlers that need to be modified]**

========================= ========================= ======================================================================================
Handler to be modified    Modified handler          Reason for revision
========================= ========================= ======================================================================================
RequestThreadLoopHandler  OneShotLoopHandler        If the test is executed with RequestThreadLoopHandler, 
                                                    the control will not return to the test code without completing the batch execution.

                                                    By replacing the handler with OneShotLoopHandler, 
                                                    the batch execution will be completed and control returns to the test code 
                                                    after all the request data setup before the test execution is processed.
========================= ========================= ======================================================================================

The configuration example of the component configuration file is shown below.

* Production configuration

  .. code-block:: xml

    <!-- Request thread loop -->
    <component name="requestThreadLoopHandler" class="nablarch.fw.handler.RequestThreadLoopHandler">
      <!-- Configuration of property is omitted -->
    </component>

* Test configuration

  Configure a component with the same name as the production configuration and overwrite it to use a handler for testing.

  .. code-block:: xml

    <!-- Configuration to replace the request thread loop handler with a handler for testing -->
    <component name="requestThreadLoopHandler" class="nablarch.test.OneShotLoopHandler" />


Default value of directive
----------------------------

If the file directives are unified to some extent in the system, 
it is redundant to describe the same directive in each test data.

In such a case, by describing the default directive in the component configuration file, 
the directive description can be omitted for each test data.

Use map format for the component configuration file. The naming rules are as follows.

======================= ==============================
 Target file type  name attribute
======================= ==============================
 Shared                 defaultDirectives            
 Fixed-length file      fixedLengthDirectives    
 Variable length file   variableLengthDirectives 
======================= ==============================


The configuration example is shown below.

.. code-block:: xml

  <!-- Directive (common) -->
  <map name="defaultDirectives">
    <entry key="text-encoding" value="Windows-31J" />
  </map>

  <!-- Directive (fixed-length) -->
  <map name="variableLengthDirectives">
    <entry key="record-separator" value="NONE"/>
  </map>

  <!-- Directive (variable length) -->
  <map name="variableLengthDirectives">
    <entry key="quoting-delimiter" value="" />
    <entry key="record-separator" value="CRLF"/>
  </map>
