=====================================================================
 Request Unit Test (HTTP Sending Synchronous Message Process)
=====================================================================

Refer to \ :doc:`RequestUnitTest_send_sync`\  for details on how to perform a request unit test.

In this section, the differences with \ :doc:`RequestUnitTest_send_sync`\ are explained.

However, the following content in "Sending synchronous message" should be read as given below "HTTP sending synchronous message":

+----------------------------------------------+------------------------------------------------------+
|Sending synchronous message                   |HTTP sending synchronous message                      |
+==============================================+======================================================+
|MockMessagingContext                          |MockMessagingClient                                   |
+----------------------------------------------+------------------------------------------------------+
|RequestTestingMessagingProvider               |RequestTestingMessagingClient                         |
+----------------------------------------------+------------------------------------------------------+

.. tip:: 
 For an overview of the request unit test, refer to :ref:`message_httpSendSyncMessage_test`.

