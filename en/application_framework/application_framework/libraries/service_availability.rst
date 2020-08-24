.. _`service_availability`:

Service Availability Check
=====================================================================

.. contents:: Table of contents
  :depth: 3
  :local:

This function checks the service availability for the functions provided by the application.

The following can be realized by using this function.

* Blocks access to some functions on the web and returns a 503 error.
* Idles (standby without processing) in the resident batch.

.. important::
 This function should be used only when the application requirements are met.
 This function manages the service availability status using the database and configures the service availability
 on a request basis (see :ref:`service_availability-settings`).
 For example, a web registration function is generally composed of multiple requests such as initial display/confirmation/return/registration.
 Therefore, while service availability can be configured in detail for this function, data design is also required in detail,
 which may reduce productivity during development and increase operational load after release.

Function overview
---------------------------------------------------------------------

Service availability check on a request basis is possible
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Service availability check on a request basis is possible for both web and resident batch
by configuring :ref:`ServiceAvailabilityCheckHandler` in the handler queue.
This function does not depend on the processing architecture such as web or resident batch.

See below for details.

* :ref:`service_availability-settings`
* :ref:`service_availability-check`
* :ref:`service_availability-view_control`

Module list
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-auth</artifactId>
  </dependency>
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-auth-jdbc</artifactId>
  </dependency>

How to use
---------------------------------------------------------------------

.. _`service_availability-settings`:

Configure settings to use service availability check
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This function uses a database to manage the service availability status.
The table layout is as follows.

============================= ===================================================================
Request ID (PK)               Values for identifying the request. String type
Service availability status   If yes, "1". String type.Value can be changed in the configuration.
============================= ===================================================================

To use the service availability check,
add the definition of :java:extdoc:`BasicServiceAvailability <nablarch.common.availability.BasicServiceAvailability>` to the component configuration file.
Specify the component name as **serviceAvailability**.

.. code-block:: xml

 <component name="serviceAvailability" class="nablarch.common.availability.BasicServiceAvailability">
   <!-- Table name -->
   <property name="tableName" value="REQUEST"/>
   <!-- Request ID column name-->
   <property name="requestTableRequestIdColumnName" value="REQUEST_ID"/>
   <!-- Column name of service availability-->
   <property name="requestTableServiceAvailableColumnName" value="SERVICE_AVAILABLE"/>
   <!-- Value indicating service availability -->
   <property name="requestTableServiceAvailableOkStatus" value="1"/>
   <!-- Transaction manager used for database access -->
   <property name="dbManager" ref="serviceAvailabilityDbManager"/>
 </component>

.. _`service_availability-check`:

Check service availability check
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
For service availability check, use :java:extdoc:`ServiceAvailabilityUtil <nablarch.common.availability.ServiceAvailabilityUtil>`.

.. _`service_availability-view_control`:

Control screen display according to service availability
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use a custom tag to control the non-display (inactivity) of buttons and links according to service availability.
See :ref:`tag-submit_display_control`.

Expansion example
---------------------------------------------------------------------
None.
