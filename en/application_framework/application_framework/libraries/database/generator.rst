.. _generator:

Surrogate Key Numbering
=========================

.. contents:: Table of contents
  :depth: 3
  :local:

Provides a function for numbering the value of surrogate keys of the database.

This function is used when numbering surrogate keys with :ref:`universal_dao`  (numbering simple serial numbers).

In addition, it can be used with implementation other than :ref:`universal_dao` , 
but support from the application side is recommended for the following reasons.

Reason
  Since :ref:`universal_dao`  performs the numbering process for the surrogate key, it is not necessary to use the numbering function directly in the application.
  When assigning values for other applications, the numbering rules are expected to be complicated and the assigned values will be edited.
  Since this function assigns a simple serial number, it cannot be used, and design and implementation are required in the application for such cases.
  (Although this function can be used, there is no advantage in using this function as design and implementation (configuration) are required)

  For example, in the case where the serial number is assigned to the parent key, a value can be assigned with the following procedure.

  1. Create a dedicated table to assign a serial number for each parent key.
  2. The application registers a record in the dedicated table when the parent key is registered.
  3. By incrementing the numbered value corresponding to the parent key at the timing when numbering is required, serial numbers within the parent key can be numbered.

Function overview
--------------------
Values can be numbered using sequences
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unique value can be assigned using the sequence object created in the database.

The SQL statement for acquiring the next value using a sequence is constructed using the dialect of the database access function.

For the dialect function, see  :ref:`dialect <database-dialect>` .

Values can be numbered using table
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A unique value can be assigned by managing the current value for each record of the table.

The following table layout is assumed.

============================================ =====================================================================================================
Numbering identification |br| name (PK)      A value for identifying the numbering target

Current value                                Current value |br| (value obtained by adding 1 to the current value is obtained |br| after numbering)
============================================ =====================================================================================================

.. important::

  The necessary records must be configured up in advance. When numbering is executed, 
  if there is no record corresponding to the specified numbering identification name (PK), 
  terminates abnormally (throws an exception) instead of adding a new record.


.. important::

  Numbering using a table often becomes a bottleneck in batch processing that processes a large amount of data. 
  For this reason, the use of numbering column or sequence in the database instead of using the numbering table is highly recommended.

  Use the numbering tables only when the numbering columns and sequence objects cannot be used as a database function.

Module list
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-idgenerator</artifactId>
  </dependency>
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-idgenerator-jdbc</artifactId>
  </dependency>

How to use
--------------------------------------------

.. _generator_dao_setting:

Configure numbering for Universal DAO
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To use this function in :ref:`universal_dao` , :java:extdoc:`BasicDaoContextFactory <nablarch.common.dao.BasicDaoContextFactory>`  must be configured.

In this example, although both sequence numbering and table numbering have been configured, and numbering that will not be used need not be configured. 
Since table numbering is not recommended,  `sequenceIdGenerator`  should be configured when using sequence numbering for numbering surrogate keys.


If the numbering function (automatic numbering column) of the database is used without using sequence numbering, configuration of numbering is not required.

.. code-block:: xml

  <component name="daoContextFactory" class="nablarch.common.dao.BasicDaoContextFactory">
    <!-- Configuration of sequence numbering -->
    <property name="sequenceIdGenerator">
      <component class="nablarch.common.idgenerator.SequenceIdGenerator"/>
    </property>

    <!-- Configuration of table numbering -->
    <property name="tableIdGenerator">
      <component class="nablarch.common.idgenerator.TableIdGenerator">
          <property name="tableName" value="GENERATOR" />
          <property name="idColumnName" value="ID" />
          <property name="noColumnName" value="NO" />
      </component>
    </property>

    <!-- Skip configuration that are not required for numbering -->
  </component>

Expansion example
--------------------------------------------------
Replace table or sequence numbering
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When replacing the numbering implementation by a table or sequence, 
it can be supported by creating a class that implements :java:extdoc:`IdGenerator <nablarch.common.idgenerator.IdGenerator>` .

The created class can be used by defining it in the component configuration file according to the  `Configure numbering for Universal DAO`_ .

.. |br| raw:: html

  <br />
