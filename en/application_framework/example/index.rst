.. _`example_application`:

Example
==========================================

This chapter describes the procedures for building the environment and executing the application, which are necessary for an Example application created using the Nablarch application framework.


  .. tip::
    Example is an implementation for showing how to use the features of Nablarch and is not intended to be used to create a full-fledged application by modifying Example.
    If you want to create a full-fledged application, create it from :ref:`blank_project`.
 
 
Procedure to build the environment
------------------------------------------
The example application uses Apache Maven to build and run the application. Refer to the following page to install Apache Maven on the PC and configure the necessary settings.

:ref:`maven`


Application execution procedure
--------------------------------------------------

For instructions on how to run the Example application, refer to the README on the github of each Example application.

  Web applications
   \

    Sample using JSP and custom tags
     https://github.com/nablarch/nablarch-example-web
    Sample using Thymeleaf
     https://github.com/nablarch/nablarch-example-thymeleaf-web


  Web service
   \

   RESTfulWeb service
    https://github.com/nablarch/nablarch-example-rest

   HTTP messaging
    Send
     https://github.com/nablarch/nablarch-example-http-messaging-send
    Receiving
     https://github.com/nablarch/nablarch-example-http-messaging

  Batch application
   \

   JSR352-compliant batch applications
    https://github.com/nablarch/nablarch-example-batch-ee

   Nablarch Batch Application
    https://github.com/nablarch/nablarch-example-batch

  Messaging
   \

   Messaging with MOM
    \

    .. _`example_application-mom_system_messaging-async_message_send`:

    Sending asynchronous message
     https://github.com/nablarch/nablarch-example-mom-delayed-send

    .. _`example_application-mom_system_messaging-sync_message_send`:

    Sending synchronous message
     https://github.com/nablarch/nablarch-example-mom-sync-send-batch

    .. _`example_application-mom_system_messaging-async_message_receive`:

    Receiving asynchronous message
     https://github.com/nablarch/nablarch-example-mom-delayed-receive

    .. _`example_application-mom_system_messaging-sync_message_receive`:

    Receiving synchronous message
     https://github.com/nablarch/nablarch-example-mom-sync-receive

    Messaging Using Tables as Queues
     https://github.com/nablarch/nablarch-example-db-queue

Running on Java 11 or higher
--------------------------------------------------

Example is assumed to run in Java 8.
If you want to run it on Java 11 or higher, you will need to modify the dependent libraries.
For more information, see the description of the blank project below.

* :ref:`setup_blank_project_for_Java11`
* :ref:`setup_blank_project_for_Java17`
* :ref:`setup_blank_project_for_Java21`
