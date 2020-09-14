
=====================================================
 Item Name Rule for Environment Configuration Values
=====================================================

In the default configuration provided by Nablarch, items are identified in advance so that they can be easily customized in individual PJs.
We will describe the naming rules for the item names. Note: PJ is the abbreviation for project.

General Rules
==============

* Item names are described in lowerCamelCase.
* \ ``.``\ (dot) is used as a delimiter.

Common prefix
==================

The prefix \ ``nablarch.``\ is added to the item names of the configuration items that Nablarch provides by default.
As a result, this prefix becomes a namespace, and it is possible to prevent duplication of item names with those in the applied PJ.
Also, it is possible to determine whether a certain configuration item is a default Nablarch item or one created individually in PJ.

**Example**

.. code-block:: bash
                
  # Whether the code is loaded at startup
  nablarch.codeCache.loadOnStartUp=true


.. tip::
   It is recommended to add a predetermined prefix to the items created individually by PJ.
   This is to make it easier to search for items created individually by PJ.


Configuration items that are used only within a single component
=================================================================

In this case, it is named with the following rules.

``Nablarch.<Component name>.<Property name>``


We will explain using the above example.

.. code-block:: bash
                
  # Whether the code is loaded at startup
  nablarch.codeCache.loadOnStartUp=true

In practice, this configuration item is used in the following component definition.
  
.. code-block:: xml
                
  <!-- Component name is 'codeCache' -->
  <component name="codeCache"
             class="nablarch.core.cache.BasicStaticDataCache">
             
    <!-- Property name is 'loadOnStartUp'  -->             
    <property name="loadOnStartup" value="${nablarch.codeCache.loadOnStartUp}"/>
              
    <!-- Middle is omitted -->
  </component>
  

In this case, ``codeCache``\ is the component name, while \ ``loadOnStartUp``\ is the property of that component.
As the above-mentioned \ `common prefix`_\  is added to this, the name becomes \ ``nablarch.codeCache.loadOnStartUp``\.


With this rule, it becomes easy to find out within which component a certain item is used.


Configuration items that are used across multiple component definitions
=========================================================================

In this case, it is named with the following rules.


``nablarch.commonProperty.<item name>.``


   
Schema information for the DB table
=====================================

The naming rule for the schema information of the tables
used by the Nablarch Application Framework is as follows:

``nablarch.<Nablarch Default table name>Table.<Various setting values>``

For example, since the default table name used in the message function is \ ``MESSAGE``\,
the item names are as follows:

**Example**

.. code-block:: bash
                
  # Default physical name of the message table
  nablarch.messageTable.tableName=MESSAGE
  # ID column physical name of the message table
  nablarch.messageTable.idColumnName=MESSAGE_ID
  # Language column physical name of the message table
  nablarch.messageTable.langColumnName=LANG
  # Message column physical name of the message table
  nablarch.messageTable.valueColumnName=MESSAGE


.. tip::
   When Nablarch Application Framework uses the table keeping the default values as it is,
   there is no need to worry about these setting values.
