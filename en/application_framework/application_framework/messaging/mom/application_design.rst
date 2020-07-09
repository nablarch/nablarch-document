Responsibility Assignment of the Application
=====================================================
This section describes the classes to be implemented and their responsibilities when creating MOM messaging.

**Classes and their responsibilities**

.. image:: images/mom_messaging_design.png

Action class
  The action class executes the business logic based on the request message (:java:extdoc:`RequestMessage<nablarch.fw.messaging.RequestMessage>`) read by the data reader (:java:extdoc:`FwHeaderReader<nablarch.fw.messaging.reader.FwHeaderReader>` /
  :java:extdoc:`MessageReader<nablarch.fw.messaging.reader.MessageReader>`) and returns the response message (:java:extdoc:`ResponseMessage<nablarch.fw.messaging.ResponseMessage>`).

  For example, the following processing is performed as business logic when capturing a request message.

  - Creates a form class from the request message and performs validation.
  - Creates an entity class from the form class and adds data to database.
  - Creates and returns a response message.

  .. tip::
   Asynchronous response messaging differs in the following points.

   * Asynchronous response messaging is not validated because the purpose is to capture data and the business logic is performed by the subsequent batch.
   * Since asynchronous response messaging does not return a message, :java:extdoc:`Success<nablarch.fw.Result.Success>`  is returned as the processing result.
     
Form class
  Class which maps the request message (:java:extdoc:`RequestMessage<nablarch.fw.messaging.RequestMessage>`) read by the data reader (:java:extdoc:`FwHeaderReader<nablarch.fw.messaging.reader.FwHeaderReader>` /
  :java:extdoc:`MessageReader<nablarch.fw.messaging.reader.MessageReader>`).

  Has the configuration of annotation for validation of the request message and logic for correlation validation.

  All the form class properties are defined by a `String`.
    See :ref:`Bean Validation <bean_validation-form_property>`  for the reason why the property must be a `String` . 
    However, in the case of a binary item, it is defined by a byte array.
    
Entity class
  A class with a one-to-one correspondence with a table. Has the property corresponding to columns.

.. important::
 Since the assumption is that a common reader will be used by the system, 
 the action is not responsible for creating a data reader unlike :ref:`responsibility assignment of the Nablarch batch application <nablarch_batch-application_design>` .

 The data reader used in messaging is added to the component definition with the name ``dataReader``.