.. _`batch_request_test`:

===============================================
How to Execute a Request Unit Test (Batch)
===============================================

--------------------------------
How to write a test class
--------------------------------

The test class should be created in such a way that the following conditions are met.

* The test class package should be the same as the Action class to be tested.
* Create a test class with a class name of <Action class name>RequestTest.
* Inherits \ ``nablarch.test.core.batch.BatchRequestTestSupport``\ .

For example, if the Action class to be tested is \ ``nablarch.sample.ss21AA.RM21AA001Action``\ , 
the test class would be as follows.

.. code-block:: java

  package nablarch.sample.ss21AA;
  
  // ~ Middle is omitted ~

  public class RM21AA001ActionRequestTest extends BatchRequestTestSupport {



----------------------
Test method division
----------------------

In principle, there is one test method per test case. 
The test method to be created is determined by the following procedure:

* In principle, one test method is created for one test case.
* As an exception, if it is more efficient to describe multiple cases collectively, consider using multiple test cases in one test method.

In batch processing, multiple records are handled at once, so the test data is relatively large.\
If multiple test cases are described in one test method, a large amount of test data will be described in one sheet,\
and readability and maintainability will be reduced. Therefore, in principle, we use one test case and one test method.

However, it may be more efficient to describe multiple test cases together. \
In this case, we consider describing multiple cases together.

* When the test cases have a strong relationship and the readability is degraded by dividing the sheet. (e.g., a test case for checking the format of an input file)

* Since the test data is small, description on one sheet does not affect readability and maintainability.

--------------------------
How to write test data
--------------------------

The Excel file containing the test data should be stored in the same directory with the same name as the test source code, \
same as in the class unit test (only the extension differs).

For information on how to write test data, refer to "\ :ref:`how_to_write_excel`\".

Common database initial values for test classes
========================================================

The same applies for web applications. See "\ :ref:`request_test_setup_db`\ ".
 

.. _`batch_test_testcases`:

List of test cases
==========================

Case table for a single test method is described in the data type of LIST_MAP. The ID is \ **testShots**\ .

..    .. image:: ./_image/testShots.png
..    :scale: 80


Each case should have the following elements:

======================= =================================================================================================================================== ==============
Column name             Description                                                                                                                         Required 
======================= =================================================================================================================================== ==============
no                      Write the test case numbers sequentially from 1.                                                                                    Required     
description             Write an explanation of the test case.                                                                                              Required
expectedStatusCode      Expected status code                                                                                                                Required 
setUpTable              When registering in the database before each test case execution, 
                        the :ref:`Group ID<tips_groupId>`\ of the data described in the same sheet should be described\ [1]_\ .
                        Data is input by an automated test framework.                                                                          
setUpFile               When creating the input file before executing each test case, 
                        enter the :ref:`Group ID<tips_groupId>` of the data that is described in the same sheet\ [1]_\ . 
                        The creation of the file is done by an automated test framework.                                                                       
expectedFile            When comparing the contents of output files, 
                        describe the :ref:`Group ID<tips_groupId>` of the expected file\ [1]_\ .                                                                          
expectedTable           When comparing the contents of the database, 
                        the :ref:`Group ID<tips_groupId>` of the table that is be expected should be mentioned\ [1]_\.                                                                          
expectedLog             Describe the LIST_MAP data ID that describes the expected log message.
                        The log message is verified by the automated test framework to see if it has actually been output.
                        (See "\ `Log result verification`_\ ")
diConfig                Describe the path to the component configuration file when executing a batch.                                                       Required 
                        (See \ :ref:`Command line arguments <main-run_application>`\ )
requestPath             The request path to execute the batch is described.                                                                                 Required 
                        (See \ :ref:`Command line arguments <main-run_application>`\ )
userId                  Enter the batch execution user ID.                                                                                                  Required 
                        (See \ :ref:`Command line arguments <main-run_application>`\ )
expectedMessage         When sending synchronous message, the :ref:`Group ID<tips_groupId>` of the expected request message is described. \
                        Messages are created by an automated test framework.
responseMessage         If sending synchronous message, the :ref:`Group ID<tips_groupId>` of the response message to be returned is described.\
                        Messages are created by an automated test framework.
expectedMessageByClient When sending synchronous HTTP message, the :ref:`Group ID<tips_groupId>` of the expected request message is described.\
                        Messages are created by an automated test framework.
responseMessageByClient If sending synchronous HTTP message, the :ref:`Group ID<tips_groupId>` of the response message to be returned is described.\
                        Messages are created by an automated test framework.
======================= =================================================================================================================================== ==============

\


.. [1]
 To use the default group ID (but not the group ID), write \ `default`\ .
 Default group ID and individual groups can be used together.
 When both data are mixed, both data of the default group ID and data of the specified group ID are valid.

Command line arguments
--------------------------
The method to specify the \ :ref:`Command line arguments <main-run_application>`\  in the test data is described.

To specify the batch start-up arguments, \
add a column in the form of ``args[n]``\  (\ **where the index n is an integer greater than or equal to 0**\ ).


 == =========== === ================ =================== ================
 no case        ... args[0]          args[1]             args[2]
 == =========== === ================ =================== ================
 1  xxx case    ... First argument   Second argument     Third argument
 == =========== === ================ =================== ================

 .. important::
  The index n must be a continuous integer.

If the column other than the above is added to the Test Case list, \
the column is considered to be a command line option.

For example, suppose you have the following column in the list of Test Cases


 == =========== === ======== =======
 no case        ...  paramA  paramB
 == =========== === ======== =======
 1  xxx case    ...  valueA  valueB
 == =========== === ======== =======

\

.. code-block:: bash

 -paramA=valueA -paramB=valueB

Command line option is specified.



Various preparation data
==============================
This section explains how to describe the various preparation data required for testing. 
In batches, the database and input files are prepared.


Database preparation
--------------------------
Map with groupID in the same way as :ref:`online <request_test_testcases>`.


.. _`how_to_setup_fixed_length_file`:

Preparing a fixed-length file
--------------------------------------

If the information of the fixed length file is described in the test data, the automated test framework will create the file before the test execution. 
Describe in the following format.


SETUP_FIXED[Group ID]=filepath.
               
Directive line

+--------------+------------------+------------------+--------------+
|Record type   |Field name(1)     |Field name(2)     |...  [#]_\    |
|              +------------------+------------------+--------------+
|              |Data type(1)      |Data type(2)      |...           |
|              +------------------+------------------+--------------+
|              |Field length(1)   |Field length(2)   |...           |
|              +------------------+------------------+--------------+
|              |Data(1-1)         |Data(2-1)         |...           |
|              +------------------+------------------+--------------+
|              |Data(1-2)         |Data(2-2)         |...           |
|              +------------------+------------------+--------------+
|              |... \ [#]_\       |...               |...           |
+--------------+------------------+------------------+--------------+

\ 

.. [#] 
 On the right side, the number of fields continues in the same way.

.. [#]
 Below this, the number of data continues in the same way. 

\


========================== ============================================================================================================================================================================================================================================================================================================
Name                       Description
========================== ============================================================================================================================================================================================================================================================================================================
Group ID                   Specify the group ID. It is connected with the group ID described in the \ ``setUpFile``\ of the test case list.
File path                  Enter the file path from the current directory (including the file name).
Directive line \ [#]_\     Describes the directive. The cell to the right of the directive name cell contains the configuration value (multiple lines are allowed).
Record type                Describe the record type. In the case of multiple layouts, this description should be written in succession.
Field name                 Describes the field name. Describes only the number of fields.
Data type                  Describes the data type of the field. Describes only the number of fields.

                           The data type is described with a Japanese name such as "half-width alphabets (半角英字)".\
                           Refer to the member variable DEFAULT_TABLE of `BasicDataTypeMapping <https://github.com/nablarch/nablarch-testing/blob/master/src/main/java/nablarch/test/core/file/BasicDataTypeMapping.java>`_  for the mapping between data types in the format definition file and data types with Japanese names.
Field length               Describes the field type of the field. Describes only the number of fields.
Data                       Describe the data stored in that field. If multiple records exist, the entry of data should be continued in the next line.
========================== ============================================================================================================================================================================================================================================================================================================

.. [#]
 When writing a directive, the contents corresponding to the following in the format definition file need not be described.

 ============== ==================================================================================
 Item           Reason
 ============== ==================================================================================
 file-type      To indicate that the data type is a fixed length with SETUP_FIXED specification.
 record-length  To pad with the size specified in the field length.
 ============== ==================================================================================


.. important::
 Duplicate field names are \ **not allowed in one record type**\. For example, there should be not more than 1 field named as "Name".
 (Typically, unique field names are given in such cases, such as "Name of this member" and "Name of family member.") 
 It does not matter if the same name exists between different record types. 
 (For example, the header record and trailer record may each have the field name "number of cases")
 

.. tip::
 Field names, data types and field lengths can be efficiently created by copying and pasting them from the external interface design document. 
 (Check the "\ **transpose matrix**\ " option when pasting.)


.. tip::
 When "unsigned numeric" or "signed numeric" data types are used, the data shall contain the value input from the fixed length file (value output to the fixed length file) as it is.
 In other words, if there are padding characters or signs in a fixed-length file, it is necessary to describe them.\
  
 The following are examples of values to be represented and their representation method when the data type is a signed numeric value.（Format definition: Field length 10 digits, padding character '0', decimal point required, code position fixed, positive sign not required）
 
  ================================= ===========================  
  numeric value to be expressed     Description on test data 
  ================================= ===========================  
  12345                             0000012345 
  -12.34                            -000012.34 
  ================================= =========================== 

 When "signed numeric" and "signed numeric" are used as test data, it is necessary to set the data type for the test.

 See the example configuration below and add the settings for testing.

 .. code-block:: xml

  <component name="fixedLengthConvertorSetting"
      class="nablarch.core.dataformat.convertor.FixedLengthConvertorSetting">
    <property name="convertorTable">
      <map>
        <!--
        Default configuration
        If the default configuration is not configured, the default configuration will be overridden with the values configured here.
        -->
        <entry key="X" value="nablarch.core.dataformat.convertor.datatype.SingleByteCharacterString"/>
        <entry key="N" value="nablarch.core.dataformat.convertor.datatype.DoubleByteCharacterString"/>
        <entry key="XN" value="nablarch.core.dataformat.convertor.datatype.ByteStreamDataString"/>
        <entry key="Z" value="nablarch.core.dataformat.convertor.datatype.ZonedDecimal"/>
        <entry key="SZ" value="nablarch.core.dataformat.convertor.datatype.SignedZonedDecimal"/>
        <entry key="P" value="nablarch.core.dataformat.convertor.datatype.PackedDecimal"/>
        <entry key="SP" value="nablarch.core.dataformat.convertor.datatype.SignedPackedDecimal"/>
        <entry key="B" value="nablarch.core.dataformat.convertor.datatype.Bytes"/>
        <entry key="X9" value="nablarch.core.dataformat.convertor.datatype.NumberStringDecimal"/>
        <entry key="SX9" value="nablarch.core.dataformat.convertor.datatype.SignedNumberStringDecimal"/>

        <entry key="pad" value="nablarch.core.dataformat.convertor.value.Padding"/>
        <entry key="encoding" value="nablarch.core.dataformat.convertor.value.UseEncoding"/>
        <entry key="_LITERAL_" value="nablarch.core.dataformat.convertor.value.DefaultValue"/>
        <entry key="number" value="nablarch.core.dataformat.convertor.value.NumberString"/>
        <entry key="signed_number" value="nablarch.core.dataformat.convertor.value.SignedNumberString"/>

        <!--
        Configuring the data type for testing
        Unsigned number (X9)->TEST_X9:nablarch.test.core.file.StringDataType
        Signed number (X9)->TEST_SX9:nablarch.test.core.file.StringDataType
        -->
        <entry key="TEST_X9" value="nablarch.test.core.file.StringDataType"/>
        <entry key="TEST_SX9" value="nablarch.test.core.file.StringDataType"/>
      </map>
    </property>
  </component>





----

Specific examples are given. This file consists of the following records:
 * 1 Header record
 * 2 Data records
 * 1 Trailer record
 * One end record

Character code is \ ``Windows-31J``\ , record delimiting character is \ ``CRLF``\ .


----

``SETUP_FIXED=work/members.txt``

+-----------------+----------------------+-------------------+----------------+
|text-encoding    |Windows-31J                                                |
+-----------------+----------------------+-------------------+----------------+
|record-separator |CRLF                                                       |
+-----------------+----------------------+-------------------+----------------+
|Header           |Record classification |FILLER             |                |
|                 +----------------------+-------------------+----------------+
|                 |半角数字              |半角               |                |
|                 +----------------------+-------------------+----------------+
|                 |1                     |10                 |                |
|                 +----------------------+-------------------+----------------+
|                 |0                     |                   |                |
+-----------------+----------------------+-------------------+----------------+
|Data             |Record classification |Membership number  |Enrollment date |
|                 +----------------------+-------------------+----------------+
|                 |半角数字              |半角数字           |半角数字        |
|                 +----------------------+-------------------+----------------+
|                 |1                     |10                 |8               |
|                 +----------------------+-------------------+----------------+
|                 |1                     |0000000001         |20100101        |
|                 +----------------------+-------------------+----------------+
|                 |1                     |0000000002         |20100102        |
+-----------------+----------------------+-------------------+----------------+
|Trailer          |Record classification |Record count       |FILLER          |
|                 +----------------------+-------------------+----------------+
|                 |半角数字              |数値               |半角            |
|                 +----------------------+-------------------+----------------+
|                 |1                     |5                  |4               |
|                 +----------------------+-------------------+----------------+
|                 |8                     |2                  |                |
+-----------------+----------------------+-------------------+----------------+
|End              |Record classification |FILLER             |                |
|                 +----------------------+-------------------+----------------+
|                 |半角数字              |半角               |                |
|                 +----------------------+-------------------+----------------+
|                 |1                     |10                 |                |
|                 +----------------------+-------------------+----------------+
|                 |9                     |                   |                |
+-----------------+----------------------+-------------------+----------------+

----

.. _`how_to_setup_csv_file`:

Prepare variable-length file (CSV file)
-------------------------------------------

Preparation of variable length file (CSV file) is almost the same as fixed length file. 
The difference from fixed length is that the field length is not described for variable length files.

``SETUP_VARIABLE=work/members.csv``
               
+-----------------+----------------------+-----------------+---------------+
|text-encoding    |Windows-31J                                             |
+-----------------+----------------------+-----------------+---------------+
|record-separator |CRLF                                                    |
+-----------------+----------------------+-----------------+---------------+
|Header           |Record classification |                 |               |
|                 +----------------------+-----------------+---------------+
|                 |半角数字              |                 |               |
|                 +----------------------+-----------------+---------------+
|                 |0                     |                 |               |
+-----------------+----------------------+-----------------+---------------+
|Data             |Record classification |Membership number|Enrollment date|
|                 +----------------------+-----------------+---------------+
|                 |半角数字              |半角数字         |半角数字       |
|                 +----------------------+-----------------+---------------+
|                 |1                     |0000000001       |20100101       |
|                 +----------------------+-----------------+---------------+
|                 |1                     |0000000002       |20100102       |
+-----------------+----------------------+-----------------+---------------+
|Trailer          |Record classification |Record count     |               |
|                 +----------------------+-----------------+---------------+
|                 |半角数字              |数値             |               |
|                 +----------------------+-----------------+---------------+
|                 |8                     |2                |               |
+-----------------+----------------------+-----------------+---------------+
|End              |Record classification |                 |               |
|                 +----------------------+-----------------+---------------+
|                 |半角数字              |                 |               |
|                 +----------------------+-----------------+---------------+
|                 |9                     |                 |               |
+-----------------+----------------------+-----------------+---------------+

.. tip::
 If you want to change the field delimiter, specify the field delimiter explicitly in the directive. 
 For example, if you want to use tabs as delimiters (TSV file), specify the directive as follows.
 
 ``field-separator=\t``

How to define an empty file
----------------------------------------
You may want to define an empty file (0-byte file) as the preparation data or expected value.

The definition of the empty file on the test sheet can be realized by defining the directive line and omitting the record definition as in the example below.

**Definition example of empty file**

``SETUP_VARIABLE=work/members.csv``
               
+-----------------+-------------+-------------+-----------+
|text-encoding    |Windows-31J                            |
+-----------------+-------------+-------------+-----------+
|record-separator |CRLF                                   |
+-----------------+-------------+-------------+-----------+
|// Empty file                                            |
+-----------------+-------------+-------------+-----------+

Various expected values
=========================

When comparing the search results and database with expected values, 
link each data with the list of test cases using ID.


Expected database status
--------------------------

Link the expected database state with the test case list in the same way as :ref:`online <request_test_expected_tables>` .


Expected fixed-length file
------------------------------

Assert the fixed length file output by the tested batch. \

In the case of the preparation data, the data type is \ `SETUP_FIXED`\ , 
but when the expected value is described, it becomes \ `EXPECTED_FIXED`\ .

Other test data are described in the same way as the preparation data.\
See `Preparing a fixed-length file`_\ .

Expected variable length file
------------------------------------

Assert the variable length file output by the batch to be tested.\

In the case of preparation data, the data type is \ `SETUP_VARIABLE`\ , 
but \ `EXPECTED_VARIABLE`\ is used to describe the expected value.

Other test data are described in the same way as the preparation data. \
See `Prepare variable-length file (CSV file)`_\ .


--------------------------
How to write a test method
--------------------------

Super class
====================

Inherits the ``BatchRequestTestSupport``\  class. 
In this class, the request unit test is executed by the following procedure based on the prepared test data.


Create a test method
======================

Create a method corresponding to the prepared test sheet.


.. code-block:: java
    
    @Test
    public void testRegisterUser() {
    }


Call a superclass method
==============================

In the test method, call one of the following methods of the superclass.

* void execute()
* void execute(String sheetName)

Normally, execute() is used.\
Normally, the test sheet name and the test method name are the same though the execute method with argument can specify the sheet name of the test data. 
If the execute method with no argument is used, it is the same behavior as specifying the test method name to the sheet name of the test data.

.. code-block:: java
    
    @Test
    public void testResigster() {
        execute();   // [Description] Equivalent to execute ("testRegisterUser")
    }


-----------------------
How to launch the test
-----------------------

Same as the class unit test. Execute the test in the same way as a normal JUnit test.


--------------------------
Test result verification
--------------------------



Result verification of database
===============================

By entering the group ID in the expectedTable column of the test case list, 
the file output result can be checked with the test data of the group ID.



Result verification of file
==============================

By entering the group ID in the expectedFile column of the test case list, 
the file output result can be checked with the test data of the group ID.

The method of describing file expectation values is almost the same as the method of describing prepared data.
Only the ID description method is different.
The description method for each file type is shown below.

===================== ========================================================  ========================================================================
Type of file           Group ID not specified                                   When group ID is specified
===================== ========================================================  ========================================================================
Fixed-length file      ``EXPECTED_FIXED = Path of the file to be compared``      ``EXPECTED_FIXED [Group ID] = Path of the file to be compared``
Variable length file   ``EXPECTED_VARIABLE = Path of the file to be compared``   ``EXPECTED_VARIABLE [Group ID] = Path of the file to be compared``
===================== ========================================================  ========================================================================


Log result verification
=============================

By entering the group ID in the expectedLog column of the test case list, 
the log output result can be checked with the test data of the group ID.


The following should be included.

+------------------------+-------------------------------------+
|Column name             |Details                              |
+========================+=====================================+
|logLevel                |Log level of expected log            |
+------------------------+-------------------------------------+
|message\ **N**\ [#]_\   |Wording included in the expected log |
+------------------------+-------------------------------------+

\

.. [#]
 Where \ **N**\ is an integer greater than or equal to 1, multiple values (consecutive values) 
 Example: messsage1, message2...

.. tip::
 All of these conditions are \ **AND**\  conditions. 
 In the following cases, the expected log is not considered to have been output.
 
 * If the expected text is logged, but the \ **log level is not as expected**\ 
 * If the log level matches, but there is at \ **least one**\  expected text that is not logged


A specific example is shown below.

In the following example, we expect two types of log output.

``LIST_MAP=expectedLogMessages``

======== ============= ======================== =================
logLevel   message1     message2                message3
======== ============= ======================== =================
 INFO      NB11AA0101  Starts the process.      Member ID=[0001]
 FATAL     NB11AA0109  An error has occurred.	
======== ============= ======================== =================

.. important::

  If a group ID is entered in the expectedLog field, be sure to set at least one line of the expected message. 
  When the expected message is not set (when the expected message is 0 lines) or when the LIST_MAP element attached to the group ID described in the expectedLog column does not exist, 
  this framework judges that the preparation of the expected value is insufficient and throws out an exception.


