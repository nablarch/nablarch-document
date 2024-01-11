.. _webspheremq_adaptor:

IBM MQ Adapter
==================================================

.. contents:: Table of contents
  :depth: 3
  :local:

Provides an adapter to use `IBM MQ (external site) <https://www.ibm.com/docs/en/ibm-mq/9.3?topic=mq-about>`_ with :ref:`the MOM messaging function of Nablarch <mom_messaging>` .

Refer to the official Website and manuals of IBM Corporation for the specifications and construction procedures of IBM MQ.

Module list
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-wmq-adaptor</artifactId>
  </dependency>

.. important::

  The library included with IBM MQ v9.3 is used for testing.
  When changing the version, test in the project to confirm that there are no problems.

Configuration for using this adapter
--------------------------------------------------
The adapter is enabled by defining components with the following procedure.

1. Add the definition of ``nablarch.integration.messaging.wmq.provider.WmqMessagingProvider`` to the component configuration file.
2. Configure ``WmqMessagingProvider`` configured in ``1`` to :ref:`messaging_context_handler` .

A configuration example is shown below.

.. code-block:: xml

  <!-- Provider implementation for IBM MQ Adapter- -->
  <component name="wmqMessagingProvider"
      class="nablarch.integration.messaging.wmq.provider.WmqMessagingProvider">
    <!-- See Javadoc for configuration value-->
  </component>

  <!--
  Message context management handler

  Configure WmqMessagingProvider defined above in messagingProvider property.
  -->
  <component class="nablarch.fw.messaging.handler.MessagingContextHandler">
    <property name="messagingProvider" ref="wmqMessagingProvider" />
  </component>

Use distributed transaction
--------------------------------------------------
This adapter includes a function to realize distributed transactions using IBM MQ as the transaction manager.

This function is used to prevent omission and duplicate capture when sending and receiving messages to and from external systems.

The procedure for using distributed transaction is shown below.

1. Define a data source (class that implements :java:extdoc:`javax.sql.XADataSource` ) that supports distributed transactions.

2. Define a factory class to generate a database connection to support the distributed transaction. |br|
   (Define ``nablarch.integration.messaging.wmq.xa.WmqXADbConnectionFactoryForXADataSource`` .)

3. Configure the factory class defined in ``2`` to :ref:`database_connection_management_handler` .

4. Define a factory class to generate transaction objects for distributed transactions.  |br|
   (Define ``nablarch.integration.messaging.wmq.xa.WmqXATransactionFactory`` .)

5. Configure the factory class defined in ``4`` to  :ref:`transaction_management_handler` .

A configuration example is shown below.

.. code-block:: xml

  <!--
  Configuration of data source for XA
  Configure the XA data source in the JDBC implementation of the database product to be used.

  In this example, the configuration is for an Oracle database.
  -->
  <component name="xaDataSource" class="oracle.jdbc.xa.client.OracleXADataSource">
    <!-- Configuration of property is omitted -->
  </component>

  <!-- Configuration of class to generate XA database connection -->
  <component name="xaConnectionFactory"
      class="nablarch.integration.messaging.wmq.xa.WmqXADbConnectionFactoryForXADataSource">

    <!-- Configure XA data source in xaDataSource property.-->
    <property name="xaDataSource" ref="xaDataSource" />

    <!-- Properties other than the above are omitted -->
  </component>

  <!-- Configure DB connection handler for distributed transaction -->
  <component class="nablarch.common.handler.DbConnectionManagementHandler">
    <!-- Configure the class that generates the database connection for XA configured above in the DB connection factory. -->
    <property name="connectionFactory" ref="xaConnectionFactory" />

    <!-- Properties other than the above are omitted -->
  </component>

  <!-- Configuration of class that generates XA transaction control object -->
  <component name="xaTransactionFactory"
      class="nablarch.integration.messaging.wmq.xa.WmqXATransactionFactory" />

  <!-- Configure transaction handler for distributed transaction -->
  <component class="nablarch.common.handler.TransactionManagementHandler">
    <!-- Configure a class that generates the XA transaction control object
    configured above in the transaction factory.
    -->
    <property name="transactionFactory" ref="xaTransactionFactory" />

    <!-- Properties other than the above are omitted -->
  </component>

.. important::

  For using distributed transactions, an XA resource manager has to be configured for IBM MQ and authority to the database has to be granted. 
  Refer to the manual of the product to be used for the detailed configuration method and necessary authority.

.. |br| raw:: html

  <br />
