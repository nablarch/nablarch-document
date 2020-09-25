=====================================================================
How to Execute a Subfunction Unit (Receiving Synchronous Message)
=====================================================================

In the receiving synchronous message process, the scope of the request and the subfunction is almost always the same.
Thus, if 1 request = 1 subfunction, there is no need to perform a subfunction unit test.

However, if a subfunction is executed by multiple messages, \
the subfunction unit test can be executed by continuously executing the test for each request in the same way as the subfunction unit test in the batch process.

However, the superclasses inherited by the test class are different (using \ ``MessagingRequestTestSupport``\ ).
The test class should be created to satisfy the following conditions.

* The package of the test class is the package of the subfunction to be tested.
* Create a test class with the class name <subfunction ID> Test.

For example, if the subfunction ID of the target subfunction is M21AA03, the test class will be as follows.

.. code-block:: java

 package nablarch.sample.ss21AA03

 import nablarch.test.core.messaging.MessagingRequestTestSupport;

 // Middle is omitted
 
 public class M21AA03Test extends MessagingRequestTestSupport {


For more information on how to execute, see batch execution method.

:doc:`./batch`


