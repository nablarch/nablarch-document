.. _`example_application`:

=======
Example
=======

The Example is an implementation example that demonstrates how to use the features of the Nablarch Application Framework, and is created for each :ref:`runtime platform <runtime_platform>`.
This chapter describes the procedures for building the environment and executing the application, which are necessary for an Example.


  .. tip::
    Examples are not intended to be used to create a full-fledged application by modifying Examples.
    If you want to create a full-fledged application, create it from :ref:`blank_project`.
 
 
How to Run Example
==================

Procedure to build the environment
----------------------------------
The Example uses Apache Maven to build and run the application. Refer to the following page to install Apache Maven on the PC and configure the necessary settings.

:ref:`maven`


Procedure to execute
--------------------

For instructions on how to run the Examples, refer to the README at the top of the GitHub repository for each Example.

Running on Java 21
------------------
Examples are assumed to run in Java 17.
If you want to run it on Java 21 , you will need to modify the dependent libraries.
For more information, see the description of the blank project below.

:ref:`setup_blank_project_for_Java21`

List of Examples
================

Web application
---------------

See also :ref:`Web Application <web_application>` and :ref:`Thymeleaf Adapter <web_thymeleaf_adaptor>` as appropriate.

- `Example of Web Application (JSP) <https://github.com/nablarch/nablarch-example-web>`_
- `Example of Web Application (Thymeleaf) <https://github.com/nablarch/nablarch-example-thymeleaf-web>`_

Web Service
-----------

RESTful Web Service
~~~~~~~~~~~~~~~~~~~

See also :ref:`RESTful Web Service <restful_web_service>` as appropriate.

- `Example of RESTful Web Service <https://github.com/nablarch/nablarch-example-rest>`_

HTTP Messaging
~~~~~~~~~~~~~~

See also :ref:`HTTP Messaging <http_messaging>` as appropriate.

- `Example of HTTP Messaging (sending) <https://github.com/nablarch/nablarch-example-http-messaging-send>`_
- `Example of HTTP Messaging (receiving) <https://github.com/nablarch/nablarch-example-http-messaging>`_

Batch Application
-----------------

Jakarta Batch-compliant Batch Application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See also :ref:`Jakarta Batch-compliant Batch Application <jsr352_batch>` as appropriate.

- `Example of Jakarta Batch-compliant Batch Application <https://github.com/nablarch/nablarch-example-batch-ee>`_

Nablarch Batch Application
~~~~~~~~~~~~~~~~~~~~~~~~~~

See also :ref:`Nablarch Batch Application <nablarch_batch>` as appropriate.

- `Example of Nablarch Batch Application <https://github.com/nablarch/nablarch-example-batch>`_

Messaging
---------

Messaging with MOM
~~~~~~~~~~~~~~~~~~

See also :ref:`Messaging with MOM <mom_messaging>` as appropriate.

  .. _`example_application-mom_system_messaging-async_message_send`:

- `Example of Messaging with MOM (sending asynchronous messages) <https://github.com/nablarch/nablarch-example-mom-delayed-send>`_

  .. _`example_application-mom_system_messaging-sync_message_send`:

- `Example of Messaging with MOM (sending synchronous messages) <https://github.com/nablarch/nablarch-example-mom-sync-send-batch>`_

  .. _`example_application-mom_system_messaging-async_message_receive`:

- `Example of Messaging with MOM (receiving asynchronous messages) <https://github.com/nablarch/nablarch-example-mom-delayed-receive>`_

    .. _`example_application-mom_system_messaging-sync_message_receive`:

- `Example of Messaging with MOM (receiving synchronous messages) <https://github.com/nablarch/nablarch-example-mom-sync-receive>`_

Messaging Using Tables as Queues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See also :ref:`Messaging Using Tables as Queues <db_messaging>` as appropriate.

- `Example of Messaging Using Tables as Queues <https://github.com/nablarch/nablarch-example-db-queue>`_
