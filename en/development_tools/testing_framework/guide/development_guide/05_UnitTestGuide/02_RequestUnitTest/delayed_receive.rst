==============================================================================
How to Conduct a Request Unit Test (Receiving Asynchronous Message Process)
==============================================================================

--------------------
Summary
--------------------
Action classes for processing receiving asynchronous messages are provided as part of Nablarch.
For this reason, the request unit test uses this action class to check the \ `Deliverables to be tested`_  given below.

*** Unlike other tests, it is not necessary to cover the conditions for action classes or perform limit value tests.**

Deliverables to be tested
==========================
* Format definition file that defines the message layout
* Form class used to register a message to the database
* Insert statement to register a message in the database

--------------------------
How to write a test class
--------------------------

The test class should be created in such a way that the following conditions are met.

* The package of the test class is the package of the function to be tested.
* Create a test class with the class name <request ID of the message> RequestTest.
* Inherits ``nablarch.test.core.messaging.MessagingReceiveTestSupport``.

For example, if the package of the function to be tested is nablarch.sample.ss21AA and request ID of the message is RM21AA100, the test class will be as follows.

.. code-block:: java

  package nablarch.sample.ss21AA;
  
  // ~ Middle is omitted ~

  public class RM21AA100RequestTest extends MessagingReceiveTestSupport {

-------------------------
How to write test data
-------------------------
This section explains how to describe the test data required to test the `Deliverables to be tested`_.

Refer to :ref:`real_request_test` for details on how to write test data.
In this section, the differences in the description method with :ref:`real_request_test` are explained.


Various expected values
==========================

Response message
----------------

In the process of receiving asynchronous message, there is no need to confirm that the response message meets the expected value as there is no response message. Only the status of the expected database is to be verified.

For this reason, "MESSAGE=expectedMessages" is not required to be defined.