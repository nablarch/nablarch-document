=================================================
How to Perform a Subfunction Unit Test (Batch)
=================================================

Subfunction unit tests for batch processing are tested using an automated test framework. 
Tests are performed in subfunction units by continuously executing the request unit tests.

The test class should be created in such a way that the following conditions are met.

* The package of the test class is the package of the subfunction to be tested.
* Create a test class with the class name <subfunction ID> Test.

For example, if the subfunction ID of the target subfunction is B21AC01, the test class will be as follows.

.. code-block:: java

 package nablarch.sample.ss21AC01

 import nablarch.test.core.batch.BatchRequestTestSupport;

 // Middle is omitted
 
 public class B21AC01Test extends BatchRequestTestSupport {
 

Test case division policy
================================

Basically, \ **one test case per sheet**\ . 
Exceptions are shown below.


For complex test cases
------------------------

When there is a large amount of test data, \
or when there are many processes included in one sheet, \
including all the test data into one sheet may result in too much data in the sheet decreasing the readability. \
Dividing one case into multiple sheets is better.

For very simple test cases
------------------------------

If the test case is very simple and the amount of test data is small, 
all test cases may be included in one sheet.


Basic description method
================================

Basically, one test case is written in a single sheet. \
When multiple batch executions are written in a single sheet, it is a subfunction unit test.

In the following example, a subfunction consisting of three batches (file input batch, user deletion batch and file output batch) is executed.

.. code-block:: java

 /** Case that ends normally */
 @Test
 public void testSuccess() {
     execute();
 }


**[TestSuccess sheet]**

LIST_MAP=testShots

=== ============= ==================  ========== ========= ================ ============ ===============
no  description   expectedStatusCode  setUpTable setUpFile expectedTable    expectedFile   requestPath    
=== ============= ==================  ========== ========= ================ ============ ===============
 1  File input    100                 default    default   default                       fileInputBatch 
 2  Delete user   100                 default              default                       userDeleteBatch
 3  File Output   100                 default              fileInputBatch   default      fileOutputBatch
=== ============= ==================  ========== ========= ================ ============ ===============


When dividing a single test case into multiple sheets
============================================================

For example, the test case illustrated in the previous section (\ `Basic description method`_\) can be divided and described as follows.

.. code-block:: java

 package nablarch.sample.ss21AA01

 import org.junit.Test;
 import nablarch.test.core.messaging.BatchRequestTestSupport;

 // Middle is omitted

 public class B21AA01Test extends BatchRequestTestSupport {

     @Test
     public void testSuccess() {
      
         // Register the input file to the temporary table
         execute("testSuccess_fileInput");
      
         // Delete the user-related table for temporary table information
         execute("testSuccess_userDelete");
      
         // Output the results to a file
         execute("testSuccess_fileOutput");
     }

\

**[TestSuccess_fileInput sheet]**

LIST_MAP=testShots

==== ============= ==================  ========== =========== ===============
 no  case          expectedStatusCode  setUpTable setUpFile   requestPath    
==== ============= ==================  ========== =========== ===============
  1  File input    100                 default    default     fileInputBatch 
==== ============= ==================  ========== =========== ===============

\

**[testSuccess_userDelete sheet]**

LIST_MAP=testShots

==== ============= ==================  ========== ============= ===============
 no  case          expectedStatusCode  setUpTable expectedTable requestPath    
==== ============= ==================  ========== ============= ===============
  1  Delete user   100                 default    default       userDeleteBatch
==== ============= ==================  ========== ============= ===============


**[TestSuccess_fileOutput sheet]**

LIST_MAP=testShots

==== ============= ==================  ========== ========= ===============
 no  case          expectedStatusCode  setUpTable outFile    requestPath    
==== ============= ==================  ========== ========= ===============
  1  File Output   100                 default    default   fileOutputBatch 
==== ============= ==================  ========== ========= ===============


When multiple cases are included in one sheet
====================================================

In the case of very simple test cases, they may be grouped together.

In the following example, two test cases (a normal case and a case with 0 records as input data) are described in a single sheet

.. code-block:: java

 /** Case that ends normally */
 @Test
 public void testSuccess() {
     execute();
 }


**[TestSuccess sheet]**

LIST_MAP=testShots

=== ======================== ==================  ========== ========= ============== ============ ===============
 no  description             expectedStatusCode  setUpTable setUpFile expectedTable  expectedFile   requestPath    
=== ======================== ==================  ========== ========= ============== ============ ===============
1-1  File input              100                 shot1      shot1                                 fileInputBatch 
1-2  Delete user             100                                      shot1                       userDeleteBatch
2-1  File input（0 record）  100                 shot2      shot2                                 fileInputBatch 
2-2  Delete user（0 record） 100                                      shot2                       userDeleteBatch
=== ======================== ==================  ========== ========= ============== ============ ===============

\

.. tip::
 Group IDs can be used to describe multiple cases of test data on one sheet. 
 For more information, see the "\ :ref:`tips_groupId`\" section.
