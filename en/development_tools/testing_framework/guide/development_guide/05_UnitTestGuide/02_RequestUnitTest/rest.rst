==================================
How to execute a request unit test
==================================

Prerequisites
-------------

Testing for the RESTful web service runtime platform requires the addition of dependent modules
in addition to other runtime testing frameworks.
See :ref:`How to Use the Automated Testing Framework<rest_testing_fw>` for more information.


How to implement the test class
--------------------------------

* :ref:`Inherit the superclasses of test classes provided by the framework. <rest_test_extends_superclass>`
* Use JUnit4 annotations (annotate your test methods with the @Test annotation)
* Generating a request with :ref:`Pre-preparation assistance features <rest_test_helper>`
* :ref:`Send request <rest_test_execute>`
* :ref:`Result validation <rest_test_assert>`

.. code-block:: java

    import nablarch.fw.web.HttpResponse;
    import nablarch.fw.web.RestMockHttpRequest;
    import nablarch.test.core.http.RestTestSupport;
    import org.json.JSONException;
    import org.junit.Test;
    import org.skyscreamer.jsonassert.JSONAssert;
    import org.skyscreamer.jsonassert.JSONCompareMode;

    import static com.jayway.jsonpath.matchers.JsonPathMatchers.hasJsonPath;
    import static org.hamcrest.Matchers.hasSize;
    import static org.junit.Assert.assertThat;

    public class SampleTest extends RestTestSupport { //Inherit RestTestSupport
        @Test  //Annotate
        public void testsThatTheProjectListCanBeObtained() throws JSONException {
            String message = "Get the project list";

            RestMockHttpRequest request = get("/projects");               //Generate Request
            HttpResponse response = sendRequest(request);                 //Send Request
            assertStatusCode(message, HttpResponse.Status.OK, response);  //Assert result

            assertThat(response.getBodyString(), hasJsonPath("$", hasSize(10)));    //Validation of the response body using json path-assert

            JSONAssert.assertEquals(message, readTextResource("testsThatTheProjectListCanBeObtained.json")
                    , response.getBodyString(), JSONCompareMode.LENIENT);                  //Verification of the response body using JSONAssert
        }
    }

.. _rest_test_extends_superclass:

Inherit the superclasses of test classes provided by the framework
==================================================================

Inherit class ``nablarch.test.core.http.RestTestSupport`` as a superclass of the test class.
``SimpleRestTestSupport`` class if you do not need to put in test data and assert the database.
In that case you can skip reading :ref:`How to write test data <rest_test_data>` below.

See :ref:`How to Use the Automated Test Framework <rest_test_superclasses>` for details on each superclass.

Use JUnit4 annotations
=================================
Since the Testing Framework is based on JUnit4, the method under test is annotated with ``@Test``.

Generating a request with Pre-preparation assistance features
=============================================================
Generate the request using the :ref:`pre-preparation assistance features <rest_test_helper>` provided in the superclass.

Send request
=======================
Send the request by calling the :ref:`send request method <rest_test_execute>` provided in the superclass.

Result validation
=================
Status codes are verified by calling the :ref:`methods <rest_test_assert>` provided in the superclass.
For the response body, use an arbitrary library to perform application-specific verification.


.. _rest_test_data:

How to write test data
-----------------------

You can write test data as described in :ref:`how_to_write_excel`. 
However, the only data that is automatically loaded in the tests for the RESTful web services execution infrastructure is the following.

* Common database initial values across test classes
* Database initial values per test method

.. important::
    For other tests than the RESTful web service runtime platform, an Excel file was required for each test class.
    For the RESTful web service runtime platform, the absence of an Excel file does not result in an error,
    it simply skips the data load into the database.

.. important::
    It is possible to include test data other than the above in an Excel file.
    In that case, you will need to write the process of getting the values into the test class in the way described in :ref:`how_to_get_data_from_excel`.
    In order to reduce the amount of test class implementation,
    the superclass RestTestSupport provides the following methods.

    .. code-block:: java

        List<Map<String, String>> getListMap(String sheetName, String id)
        List<Map<String, String[]>> getListParamMap(String sheetName, String id)
        Map<String, String[]> getParamMap(String sheetName, String id)

Common database initial values across test classes
==================================================

See :ref:`request_test_setup_db`.

Database initial values per test method
=======================================

Prepare a sheet with \ **name of the test method**\  in an Excel file containing the test data,
and write the database initial values with the data type accoring to \ **SETUP_TABLES**\.
The data written here will be put in when the test method is executed by the framework.

