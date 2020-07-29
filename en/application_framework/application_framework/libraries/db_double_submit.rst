.. _`db_double_submit`:

Double submission prevention using the database
=====================================================================

.. contents:: Table of contents
  :depth: 3
  :local:

In :ref:`Double submission prevention <tag-double_submission>`, server tokens are stored in an HTTP session.
Therefore, when you scale out an application server, you should use sticky sessions or session replication.

By using an implementation that stores server-side tokens in a database,
tokens can be shared among multiple application servers without the need for any particular application server configuration.

.. tip::

  A token may remain on the table when the browser is closed, for example.
  Therefore, expired tokens need to be deleted periodically.

.. important::

  Although :ref:`Double submission prevention <tag-double_submission>` using HTTP session could be used for CSRF measure,
  this feature cannot be used for CSRF measure because the token is stored in DB without identifying the user.
  If you use this feature, use :ref:`csrf_token_verification_handler` for the CSRF measure.

Function overview
---------------------------------------------------------------------

Server-side tokens can be stored in a database

Module list
---------------------------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web-doublesubmit-jdbc</artifactId>
  </dependency>


How to use
---------------------------------------------------------------------

A table for storing tokens in the database is required.

The following is the definition of the table to be created.

`DOUBLE_SUBMISSION` table
  ==================== ====================
  Colum name           Data type
  ==================== ====================
  TOKEN(PK)            `java.lang.String`
  CREATED_AT           `java.sql.Timestamp`
  ==================== ====================

Table names and column names can be changed.
If changing them, define a component of :java:extdoc:`DbTokenSchema <nablarch.common.web.token.DbTokenSchema>` in
:java:extdoc:`DbTokenManager.dbTokenSchema <nablarch.common.web.token.DbTokenManager.setDbTokenSchema(nablarch.common.web.token.DbTokenSchema)>`.

Add two component definitions.

Add a component definition named ``tokenManager``.
This will allow the tokens to be managed in the database.
``tokenManager`` needs :ref:`initialize <repository-initialize_object>`.

.. code-block:: xml
                
  <component name="tokenManager" class="nablarch.common.web.token.DbTokenManager">
    <property name="dbManager">
      <component class="nablarch.core.db.transaction.SimpleDbTransactionManager">
        <property name="dbTransactionName" value="tokenTransaction"/>
      </component>
    </property>
    <!-- The following settings are required only when changing table names
         and column names from the above table definition -->
    <property name="dbTokenSchema">
      <component class="nablarch.common.web.token.DbTokenSchema">
        <property name="tableName" value="DB_TOKEN"/>
        <property name="tokenName" value="VALUE_COL"/>
        <property name="createdAtName" value="CREATED_AT_COL"/>
      </component>
    </property>
  </component>

  <!-- Since initialization is required, set the following -->
  <component name="initializer" class="nablarch.core.repository.initialization.BasicApplicationInitializer">
    <property name="initializeList">
      <list>
        <component-ref name="tokenManager"/>
      </list>
    </property>
  </component>


Add a component definition named ``tokenGenerator``.
This will use UUIDs for the tokens, and eliminate the guessing and potential collisions.

.. code-block:: xml

    <component name="tokenGenerator"
               class="nablarch.common.web.token.UUIDV4TokenGenerator" />

.. important::

  The :ref:`Testing framework token issuance <how_to_set_token_in_request_unit_test>` does not support DB storage of tokens.
  Therefore, you need to replace :java:extdoc:`HttpSessionTokenManager <nablarch.common.web.token.HttpSessionTokenManager>`
  when you run the automated test.

  .. code-block:: xml

    <!-- Storing a token in an HTTP session -->
    <component name="tokenManager" class="nablarch.common.web.token.HttpSessionTokenManager"/>
