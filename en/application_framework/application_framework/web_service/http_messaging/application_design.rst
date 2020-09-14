.. _`http_messaging-design`:

Responsibility Assignment of the Application
====================================================
This section describes the classes to be implemented and their responsibilities when creating HTTP messaging.

**Classes and their responsibilities**

.. image:: images/http_messaging_design.png

Action class
  The action class executes the business logic based on the request message (:java:extdoc:`RequestMessage<nablarch.fw.messaging.RequestMessage>`), 
  and creates and returns the response message (:java:extdoc:`ResponseMessage<nablarch.fw.messaging.ResponseMessage>`).

  For example, the following process is performed as business logic in the case of a request message capture process.

  - Creates a form class from the request message and performs validation.
  - Creates an entity class from the form class and adds data to the database.
  - Creates and returns a response message.

Form class
  Class to map request messages (:java:extdoc:`RequestMessage<nablarch.fw.messaging.RequestMessage>`).

  Has the annotation configuration for validation and logic for correlation validation.

  All the form class properties must be defined by a `String` .
    See :ref:`Bean Validation <bean_validation-form_property>` for the reason why the property must be a `String` . 
    However, in the case of a binary item, it is defined by a byte array.

Entity class
  A class with a one-to-one correspondence with a table. Has the property corresponding to columns.

