.. _jaxrs_adaptor:

Jakarta RESTful Web Services Adapter
===========================================

.. contents:: Table of contents
  :depth: 3
  :local:

.. tip::
  This function was called "JAX-RS Adapter" until Nablarch5.
  However, as Java EE was transferred to the Eclipse Foundation and the specification name changed, the name was changed to "Jakarta RESTful Web Services Adapter".

  Only the name has changed, there is no functional difference.

  For other features renamed in Nablarch 6, see :ref:`renamed_features_in_nablarch_6`.

Provides the following adapter to use in :ref:`RESTful web service <restful_web_service>`.


*	Adapter to convert JSON using `Jackson (external site) <https://github.com/FasterXML/jackson>`_
*	Adapter for using :ref:`RESTful web service <restful_web_service>` with `Jersey (external site) <https://eclipse-ee4j.github.io/jersey/>`_
*	Adapter for using :ref:`RESTful web service <restful_web_service>` with `RESTEasy (external site) <https://resteasy.dev/>`_

Module list
--------------------------------------------------
.. code-block:: xml

  <!-- When using jackson adapter -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-jackson-adaptor</artifactId>
  </dependency>

  <!-- When using the Jersey adapter -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-jersey-adaptor</artifactId>
  </dependency>

  <!-- When using RESTEasy adapter -->  
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-resteasy-adaptor</artifactId>
  </dependency>
  
.. tip::

  Tests are conducted using jackson version 2.10.3. 
  When changing the version, test in the project to confirm that there are no problems.
  
.. tip::

  Due to the vulnerability of Jackson1-based libraries, support for Jackson1-based libraries is discontinued from Nablarch5u16.
  If you have been using Jackson1-based libraries, you should migrate to Jackson2-based libraries.

  [Reference information]

  * https://jvndb.jvn.jp/ja/contents/2019/JVNDB-2019-012258.html
  * https://github.com/advisories/GHSA-r6j9-8759-g62w

Using RESTful web services under Jersey environment
-------------------------------------------------------
If the implementation of `Jakarta RESTful Web Services(external site) <https://jakarta.ee/specifications/restful-ws/>`_ bundled with the web application server is `Jersey(external site) <https://eclipse-ee4j.github.io/jersey/>`_ , use the adapter for Jersey.

An application of Jersey adapter is shown below.

For :java:extdoc:`JaxRsMethodBinderFactory#setHandlerList <nablarch.fw.jaxrs.JaxRsMethodBinderFactory.setHandlerList(java.util.List)>`, a factory class that constructs a Jersey handler (:java:extdoc:`JerseyJaxRsHandlerListFactory <nablarch.integration.jaxrs.jersey.JerseyJaxRsHandlerListFactory>`) is factory injected. As a result, the following handler configurations for Jersey are automatically configured.

* Configuration of :ref:`body_convert_handler` (the following converters are set)

  * :java:extdoc:`Jackson2BodyConverter <nablarch.integration.jaxrs.jackson.Jackson2BodyConverter>` is configured for the JSON converter.
  * :java:extdoc:`JaxbBodyConverter <nablarch.fw.jaxrs.JaxbBodyConverter>` is configured for the XML converter.
  * :java:extdoc:`FormUrlEncodedConverter <nablarch.fw.jaxrs.FormUrlEncodedConverter>` is configured for the converter of application/x-www-form-urlencoded.

* :ref:`jaxrs_bean_validation_handler`

.. code-block:: xml

  <component name="packageMapping" class="nablarch.integration.router.RoutesMapping">
    <property name="methodBinderFactory">
      <component class="nablarch.fw.jaxrs.JaxRsMethodBinderFactory">
        <property name="handlerList">
          <!-- Factory injection of Jersey handler queue to the handlerList property -->
          <component class="nablarch.integration.jaxrs.jersey.JerseyJaxRsHandlerListFactory"/>
        </property>
      </component>
    </property>

    <!-- Properties other than the above are omitted  -->
  </component>

.. tip::
  If  `Jackson (external site) <https://github.com/FasterXML/jackson>`_ is not bundled with the web application server to be used, deploy the Jackson module with the application module as a set.
  
Using RESTful web services under RESTEasy environment
--------------------------------------------------------
If the implementation of `Jakarta RESTful Web Services (external site) <https://jakarta.ee/specifications/restful-ws/>`_ bundled with the web application server is `RESTEasy (external site) <https://resteasy.dev/>`_ , use the adapter for RESTEasy.

An application of RESTEasy adapter is shown below.

For :java:extdoc:`JaxRsMethodBinderFactory#setHandlerList <nablarch.fw.jaxrs.JaxRsMethodBinderFactory.setHandlerList(java.util.List)>`, a factory class that constructs a RESTEasy handler (:java:extdoc:`ResteasyJaxRsHandlerListFactory <nablarch.integration.jaxrs.resteasy.ResteasyJaxRsHandlerListFactory>`) is factory injected. 
As a result, the following handler configurations for RESTEasy are automatically configured.

*  Configuration of :ref:`body_convert_handler` (the following converters are set)

  * :java:extdoc:`Jackson2BodyConverter <nablarch.integration.jaxrs.jackson.Jackson2BodyConverter>` is configured for the JSON converter.
  * :java:extdoc:`JaxbBodyConverter <nablarch.fw.jaxrs.JaxbBodyConverter>` is configured for the XML converter.
  * :java:extdoc:`FormUrlEncodedConverter <nablarch.fw.jaxrs.FormUrlEncodedConverter>` is configured for the converter of application/x-www-form-urlencoded.

* :ref:`jaxrs_bean_validation_handler`

.. code-block:: xml

  <component name="packageMapping" class="nablarch.integration.router.RoutesMapping">
    <property name="methodBinderFactory">
      <component class="nablarch.fw.jaxrs.JaxRsMethodBinderFactory">
        <property name="handlerList">
          <!-- Factory injection of RESTEasy handler queue to the handlerList property -->
          <component class="nablarch.integration.jaxrs.resteasy.ResteasyJaxRsHandlerListFactory"/>
        </property>
      </component>
    </property>

    <!-- Properties other than the above are omitted -->
  </component>

.. tip::
  If `Jackson (external site) <https://github.com/FasterXML/jackson>`_  is not bundled with the web application server to be used, deploy the Jackson module with the application module as a set.

To change (add) the body converter used in each environment
----------------------------------------------------------------------
If the MIME to be supported in the project increases, support by implementing :java:extdoc:`JaxRsHandlerListFactory <nablarch.fw.jaxrs.JaxRsHandlerListFactory>`.

For the implementation method, refer to this adapter (:java:extdoc:`JerseyJaxRsHandlerListFactory <nablarch.integration.jaxrs.jersey.JerseyJaxRsHandlerListFactory>`, :java:extdoc:`ResteasyJaxRsHandlerListFactory <nablarch.integration.jaxrs.resteasy.ResteasyJaxRsHandlerListFactory>`).
