.. _`double_transmission_test`:

=========================================================================
How to Test Execution of Duplicate Form Submission Prevention Function
=========================================================================

For applications on Nablarch, \
the duplicate form submission prevention function works both on the server and client. \
Therefore, the testing method is different for the request unit test and subfunction unit test.

The following is a description of the test execution method for each.

-----------------------------------------------------------------------------------------
How to test the duplicate form submission prevention function with the request unit test
-----------------------------------------------------------------------------------------

The request unit test is performed on the server.


For testing the duplicate form submission prevention function, an isValidToken column is specified in the LIST_MAP of the test shot.\This column can be set to "false" to confirm that the duplicate form submission prevention function is working when an error occurs.\

 Refer to ":ref:`request_test_testcases`" for details on how to describe the test data.

-------------------------------------------------------------------------------------------
How to test the duplicate form submission prevention function in the subfunction unit test
-------------------------------------------------------------------------------------------

The subfunction unit test is performed on the client.


The procedure is as follows.

* Launch the application in debug mode.

* The breakpoint is configured to the process of the action for the request under test.

* The button of the test target request is selected manually.

* With the processing stopped at the breakpoint, select the button of the request to be tested again and confirm that the request is not sent.
