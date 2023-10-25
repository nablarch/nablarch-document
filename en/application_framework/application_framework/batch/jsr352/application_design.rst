Responsibility Assignment of Application
=========================================
This section describes the classes to be implemented and their responsibilities when creating a Jakarta Batch-compliant batch application.

.. _jsr352-batchlet_design:

For Batchlet step
--------------------------------------------------
This section describes the classes to be implemented and their responsibilities in the case of Batchlet step.

.. image:: images/batchlet-design.png
  :scale: 80
  

Batchlet (Batchlet class)
  Executes the business logic with the batchlet and returns the character string [#batchlet_status]_ representing the processing result of the step.

  For example, the batchlet downloads files on the Internet or performs processing [#insert_select]_ that can be completed with just 1 SQL statement.

.. _jsr352-chunk_design:

For Chunk step
--------------------------------------------------
This section describes the classes to be implemented and their responsibilities in the case of Chunk step.

.. image:: images/chunk-design.png
  :scale: 80

Item reader (ItemReader class)
  Implements the process to read the data to be processed from the data source (file, database, etc.).
  Converts the read data into a form and returns the form.

  Item reader is an interface specified by Jakarta Batch.
  For this reason, see `Jakarta Batch Specification(external site) <https://jakarta.ee/specifications/batch/>`_  for details of the implementation method.

Item processor (ItemProcessor class)
  Executes the business logic based on the data read by the item reader to generate the data to be output.

  If the output target is a database, converts the data after the execution of business logic into an entity.
  If the output target is not a database, converts the data after the execution of business logic to a form for output.

  Item processor is an interface specified by Jakarta Batch.
  For this reason, see `Jakarta Batch Specification(external site) <https://jakarta.ee/specifications/batch/>`_  for details of the implementation method.

  .. tip::
    If the data read by the item reader is externally acquired data, checks the input values before executing the business logic.
    For information about checking input values, see :ref:`checking input values<validation>`.

Item writer (ItemWriter class)
  Item writer implements the process to output the entity or form, converted by the item processor, to a database or file.

  Item writer is an interface specified by Jakarta Batch.
  For this reason, see `Jakarta Batch Specification(external site) <https://jakarta.ee/specifications/batch/>`_  for details of the implementation method.

Form (form class)
  This class holds the data read by the item reader. A class that holds the data to be output if the output target is not a database.

  In the case of a form that holds unreliable values such as externally received files, all property types should be string.
  For the reason, see :ref:`Bean Validation <bean_validation-form_property>`.
  In the case of a binary item, the type is defined by a byte array.

Entity (entity class)
  A class with a one-to-one correspondence with a table. The entity class has property corresponding to columns.

.. [#batchlet_status] For details on the character string returned by the batchlet (end status of batchlet), see `Jakarta Batch Specification (external site) <https://jakarta.ee/specifications/batch/>`_ .
.. [#insert_select] For example, it refers to the execution of SQL that completes the process only by ``insert ~ select``.
