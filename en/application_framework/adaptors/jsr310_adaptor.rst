.. _jsr310_adaptor:

JSR310(Date and Time API)Adapter
==================================================

.. contents:: Table of contents
  :depth: 3
  :local:
  
Provides an adapter to enable date and time details in JSR310 (Date and Time API). 
By using this adapter, JSR310 (Date and Time API) can be used with  :ref:`bean_util` .

.. important::

  The functions provided by this adapter have been incorporated into framework body since Nablarch 6u2,
  so you can use the JSR310 (Date and Time API) with  :ref:`bean_util`  without using this adapter.
  This adapter is maintained for backward compatibility.

.. important::

  The types supported by this adapter are as follows. 
  Add the converter to the project for handling other types.
  
  * :java:extdoc:`LocalDate <java.time.LocalDate>`
  * :java:extdoc:`LocalDateTime <java.time.LocalDateTime>`

Module list
--------------------------------------------------
.. code-block:: xml

  <!-- JSR310 adapter -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-jsr310-adaptor</artifactId>
  </dependency>
  
How to use
---------------------------------------------------------------------

For details such as conversion possible types and conversion rules, see :java:extdoc:`converter list <nablarch.core.beans.converter>`.

Configuration
  This function is enabled by adding the following to the component configuration file of :ref:`repository` .

  .. code-block:: xml

      <import file="JSR310.xml" />

.. tip::
 
  The following work is required to change the format when converting from a string.
  
  Create a class with a definition such as format
    Add implementation class of :java:extdoc:`DateTimeConfiguration <nablarch.integration.jsr310.util.DateTimeConfiguration>`  and define the format of date and time. 
    Referring to :java:extdoc:`BasicDateTimeConfiguration <nablarch.integration.jsr310.util.BasicDateTimeConfiguration>` is good.
    
  Define the class that is added in the component configuration file
    Define the component with the component name as ``dateTimeConfiguration``.
    
    An example is shown below.
    
    .. code-block:: xml
    
      <component name="dateTimeConfiguration" class="sample.SampleDateTimeConfiguration" />
      