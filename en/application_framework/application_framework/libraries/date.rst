Date Management
=====================================================================

.. contents:: Table of contents
  :depth: 3
  :local:

Provides a function to centrally manage the system date and time (OS date and time) and business date used in applications.

Function overview
--------------------------

System date and time (OS date and time) and business date can be switched
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
With this function, the system date and time (OS date and time) and business date are acquired using the class specified in the component definition.
Therefore, the acquisition method of system date and time (OS date and time) and business date used by the application can be switched simply by replacing the class specified in the component definition. 
This switching can be used to temporarily switch the system date/time (OS date/time) or business date in a test, etc.

* :ref:`date-system_time_change`
* :ref:`date-business_date_change`

Module list
---------------------------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core</artifactId>
  </dependency>

  <!-- Only when using business date management function-->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-jdbc</artifactId>
  </dependency>

How to use
--------------------------------------------------

.. _date-system_time_settings:

Configure settings to use the system date and time management function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To use the system date and time management function, 
add :java:extdoc:`BasicSystemTimeProvider <nablarch.core.date.BasicSystemTimeProvider>` configuration to the component definition. 
Specify the component name as  **systemTimeProvider** .

.. code-block:: xml

 <component name="systemTimeProvider" class="nablarch.core.date.BasicSystemTimeProvider" />

Acquire system date and time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use  :java:extdoc:`SystemTimeUtil <nablarch.core.date.SystemTimeUtil>`  to acquire the system date and time.

.. _date-business_date_settings:

Configure settings to use the business date management function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The business date management function uses a database to manage multiple business dates. 
The table layout is as follows.

================ ===================================================
Category (PK)         A value for identifying the business date. String type
Date             Business date. String type and value in yyyyMMdd format
================ ===================================================

To use the business date management function, 
add :java:extdoc:`BasicBusinessDateProvider <nablarch.core.date.BasicBusinessDateProvider>` configuration to the component definition. 
Specify the component name as  **businessDateProvider**.

Also, since initialization is required, set it in the list to be initialized.

.. code-block:: xml

 <component name="businessDateProvider" class="nablarch.core.date.BasicBusinessDateProvider">
   <!-- Table name -->
   <property name="tableName" value="BUSINESS_DATE" />
   <!-- Column name of category -->
   <property name="segmentColumnName" value="SEGMENT"/>
   <!-- Column name of date -->
   <property name="dateColumnName" value="BIZ_DATE"/>
   <!-- Category used when business date is obtained by omitting the category -->
   <property name="defaultSegment" value="00"/>
   <!-- Transaction manager used for database access -->
   <property name="transactionManager" ref="transactionManager" />
 </component>

 <component name="initializer"
     class="nablarch.core.repository.initialization.BasicApplicationInitializer">
   <property name="initializeList">
     <list>
       <!-- Other components are omitted -->
       <component-ref name="businessDateProvider" />
     </list>
   </property>
 </component>

Acquire business date
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use  :java:extdoc:`BusinessDateUtil <nablarch.core.date.BusinessDateUtil>`  to acquire the business date.

Overwrite business date to an arbitrary date
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When re-executed during failure in batch process, using the past date as the business date during batch execution may be preferred in some cases. 
In such a case, only the re-execution process can execute with an arbitrary date as the business date.

.. tip::
 If all functions are executed in one process like a web application, 
 simply change the date managed in the database.

Business date is overwritten by using  :ref:`repository-overwrite_environment_configuration` . 
Specify as a system property in the following format.

Format of system property
 BasicBusinessDateProvider. <Category> = date

 \*\ Date is in yyyyMMdd format

Example of system property file
 When overwriting the date of category "batch" to "2016/03/17"

 -DBasicBusinessDateProvider.batch=20160317

Update business date
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Business date is updated by using  :java:extdoc:`BasicBusinessDateProvider <nablarch.core.date.BasicBusinessDateProvider>` .

.. code-block:: java

 // Acquire BasicBusinessDateProvider from the system repository
 BusinessDateProvider provider = SystemRepository.get("businessDateProvider");

 // Call setDate method and update
 provider.setDate(segment, date);

Expansion example
--------------------------------------------------

.. _date-system_time_change:

Switch system date and time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To switch the system date and time when executing a unit test, perform the following procedure.

1. Create a class that implements  :java:extdoc:`SystemTimeProvider <nablarch.core.date.SystemTimeProvider>` .
2. Configure in accordance with :ref:`date-system_time_settings` .

.. _date-business_date_change:

Switch business date
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To switch the business date when executing a unit test, perform the following procedure.

1. Create a class that implements :java:extdoc:`BusinessDateProvider <nablarch.core.date.BusinessDateProvider>` .
2. Configure in accordance with :ref:`date-business_date_settings` .
