.. _`example_application`:

=======
Example
=======

The Example application is an implementation example that demonstrates how to use the features of the Nablarch Application Framework, and is created for each :ref:`runtime platform <runtime platform>`.
This chapter describes the procedures for building the environment and executing the application, which are necessary for an Example application.


  .. tip::
    Example and is not intended to be used to create a full-fledged application by modifying Example.
    If you want to create a full-fledged application, create it from :ref:`blank_project`.
 
 
Procedure to build the environment
==========================================
The example application uses Apache Maven to build and run the application. Refer to the following page to install Apache Maven on the PC and configure the necessary settings.

:ref:`maven`


Application execution procedure
==================================================

For instructions on how to run the Example application, refer to the README on the github of each Example application.
To get the basic knowledge of the development, refer to Getting Started for each processing architecture.

  Web applications
   \

    Sample using JSP and custom tags
     https://github.com/nablarch/nablarch-example-web

     :ref:`Click here <getting_started>` for Getting Started with this Example.

    Sample using Thymeleaf
     https://github.com/nablarch/nablarch-example-thymeleaf-web

     *For this example, the corresponding Getting Started is not available.


  Web service
   \

   RESTfulWeb service
    https://github.com/nablarch/nablarch-example-rest

    :ref:`Click here <rest_getting_started>` for Getting Started with this Example.

   HTTP messaging
    Send
     https://github.com/nablarch/nablarch-example-http-messaging-send

     *For this example, the corresponding Getting Started is not available.

    Receiving
     https://github.com/nablarch/nablarch-example-http-messaging

     :ref:`Click here <http-messaging_getting_started>` for Getting Started with this Example.

  Batch application
   \

   Jakarta Batch-compliant batch applications
    https://github.com/nablarch/nablarch-example-batch-ee

    :ref:`Click here <jBatch_getting_started>` for Getting Started with this Example.

   Nablarch Batch Application
    https://github.com/nablarch/nablarch-example-batch

    :ref:`Click here <nablarch_Batch_getting_started>` for Getting Started with this Example.

  Messaging
   \

   Messaging with MOM
    \

    *Only Example applications are provided for Messaging with MOM, and no Getting Started is provided.
    Example implementations using Example applications can be found in :ref:`mom_system_messaging`.

    .. _`example_application-mom_system_messaging-async_message_send`:

    Sending asynchronous message
     https://github.com/nablarch/nablarch-example-mom-delayed-send

     :ref:`Click here <mom_system_messaging-async_message_send>` for the example implementation using this Example application.

    .. _`example_application-mom_system_messaging-sync_message_send`:

    Sending synchronous message
     https://github.com/nablarch/nablarch-example-mom-sync-send-batch

     :ref:`Click here <mom_system_messaging-sync_message_send>` for the example implementation using this Example application.

    .. _`example_application-mom_system_messaging-async_message_receive`:

    Receiving asynchronous message
     https://github.com/nablarch/nablarch-example-mom-delayed-receive

     :ref:`Click here <mom_system_messaging-async_message_receive>` for the example implementation using this Example application.

    .. _`example_application-mom_system_messaging-sync_message_receive`:

    Receiving synchronous message
     https://github.com/nablarch/nablarch-example-mom-sync-receive

     :ref:`Click here <mom_system_messaging-sync_message_receive>` for the example implementation using this Example application.


   Messaging Using Tables as Queues
    https://github.com/nablarch/nablarch-example-db-queue

    :ref:`Click here <db_messaging_getting_started>` for Getting Started with this Example.

Running on Java 21
==================================================
Example is assumed to run in Java 17.
If you want to run it on Java 21 , you will need to modify the dependent libraries.
For more information, see the description of the blank project below.

* :ref:`setup_blank_project_for_Java21`
