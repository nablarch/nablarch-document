.. _nablarch_openapi_generator:

====================================================
Nablarch OpenAPI Generator
====================================================

.. contents:: Table of Contents
  :depth: 3
  :local:

Summary
-------------

Nablarch OpenAPI Generator is a Generator implementation of  `OpenAPI Generator(external site) <https://openapi-generator.tech/>`_ that generate source code using `OpenAPI(external site) <https://www.openapis.org/>`_ document as input.

This tool provides a generator for Nablarch RESTful web services, and generates source code by running it as `OpenAPI Generator Maven Plugin(external site) <https://openapi-generator.tech/docs/plugins>`_ .

Using the generated source code makes it easy to implement action classes that conform to the REST API interface defined in the OpenAPI document.

Prerequisites
-------------

* An OpenAPI document has been created from which the source code for the Nablarch RESTful Web Service will be generated.
* OpenAPI documents must be written in `OpenAPI 3.0.3(external site) <https://spec.openapis.org/oas/v3.0.3.html>`_ specification.

Overview
--------

This tool generates the following source code by specifying an OpenAPI document as input.

* Resource (Action) interfaces based on path and operation definitions.
* Model that corresponds to requests and responses based on a schema definition.

.. tip::

  Due to the OpenAPI Generator specifications, ``.openapi-generator-ignore``, ``.openapi-generator/FILES``, and ``.openapi-generator/VERSION`` are generated under the directory specified in ``output`` of :ref:`NablarchOpenApiGeneratorConfiguration` . However, these are not used.

Tool operation
----------------

The assumed operation method for this tool is described below.

#. Create an OpenAPI document based on the web service design information.
#. Create a Nablarch RESTful Web Service project and configure the OpenAPI Generator and this tool as a Maven plugin.
#. Build the project and generate the Resource (Action) interfaces and Model.
#. Implement the Nablarch RESTful Web Service using the generated Resource (Action) interfaces and Model.

.. tip::

  It is assumed that this tool will be executed repeatedly as OpenAPI document is modified. The action classes of the Nablarch RESTful Web Service are created by implementing the generated Resource (Action) interfaces, so the contents implemented in the Action classes will not be lost even if automatic generation is performed again using this tool.

.. tip::

  OpenAPI Generator and this tool are assumed to be executed as Maven plugins. However, they can also be used as a CLI. For more information, see :ref:`NablarchOpenApiGeneratorAsCli` .

How to Use
-------------

Configuring the Maven Plugin
==============================

An example of the minimum configuration of Maven plugin for OpenAPI Generator required to use this tool is shown below.

.. code-block:: xml

      <plugin>
        <groupId>org.openapitools</groupId>
        <artifactId>openapi-generator-maven-plugin</artifactId>
        <version>7.10.0</version>
        <dependencies>
          <!-- Add this tool's module to the dependencies -->
          <dependency>
            <groupId>com.nablarch.tool</groupId>
            <artifactId>nablarch-openapi-generator</artifactId>
            <version>1.0.0</version>
          </dependency>
        </dependencies>
        <executions>
          <execution>
            <goals>
              <goal>generate</goal>
            </goals>
            <configuration>
              <!-- Specify the file path of the OpenAPI document -->
              <inputSpec>${project.basedir}/src/main/resources/openapi.yaml</inputSpec>
              <generatorName>nablarch-jaxrs</generatorName>
              <configOptions>
                <sourceFolder>src/gen/java</sourceFolder>
                <apiPackage>com.example.api</apiPackage>
                <modelPackage>com.example.model</modelPackage>

                <!-- Specify the options for this tool -->
              </configOptions>
            </configuration>
          </execution>
        </executions>
      </plugin>

This tool is provided by the following dependencies.

.. code-block:: xml

          <dependency>
            <groupId>com.nablarch.tool</groupId>
            <artifactId>nablarch-openapi-generator</artifactId>
            <version>1.0.0</version>
          </dependency>

The minimum required settings to use the OpenAPI Generator Maven plugin are ``inputSpec`` , which specifies the OpenAPI document for which source code will be generated, and ``generatorName`` , which specifies which Generator to use.

You can use this tool by specifying ``nablarch-jaxrs`` for ``generatorName`` .

For other configurations, see :ref:`NablarchOpenApiGeneratorConfiguration` .

.. tip::

  This tool was developed and tested using OpenAPI Generator 7.10.0.
  When changing the OpenAPI Generator version, test it on the project side to ensure that there are no problems.

How to do it
============

This tool can be run using compile goal.

.. code-block:: text

  mvn compile

If you explicitly set the ``sourceFolder`` in :ref:`NablarchOpenApiGeneratorConfiguration` , the source code generated when you run ``mvn compile`` will be included in the compilation target of the project for which the Maven plugin is configured.

This behavior is due to the OpenAPI Generator Maven plugin.

Output Destination
====================

With the default settings of the OpenAPI Generator Maven plugin, the generated source code is output to ``target/generated-sources/openapi/src/gen/java`` .

If you want to change the output destination, see ``output`` and ``sourceFolder`` in :ref:`NablarchOpenApiGeneratorConfiguration` .

.. _NablarchOpenApiGeneratorConfiguration:

Configure the Generator
===========================

The main configuration of the OpenAPI Generator Maven plugin is shown below. These are specified as tags directly under the ``configuration`` tag.

==================  =========================================================  ====================  ===============================
Name                Explanation                                                Required/Optional     Defautl value
==================  =========================================================  ====================  ===============================
``inputSpec``       Specify the file path of the input OpenAPI document.       Required              None
``generatorName``   Specifies the name of the Generator that generates |br|
                    the source code. |br|
                    For this tool, specify ``nablarch-jarxrs``.                Required              None
``output``          Specifies the directory where the source code |br|
                    will be generated.                                         Optional              ``generated-sources/openapi``
==================  =========================================================  ====================  ===============================

The configuration for this tool is shown below. All are optional and should be specified within the ``configOptions`` tag.

==================================== ================================================================================================== =====================================================================
Name                                 Explanation                                                                                        Defautl value
==================================== ================================================================================================== =====================================================================
``apiPackage``                       Specifies the package for the generated Resource (Action) interface.                               ``org.openapitools.api``
``modelPackage``                     Specifies the package of the Model to be generated.                                                ``org.openapitools.model``
``hideGenerationTimestamp``          Whether to add the ``date`` attribute when annotating |br|                                         ``false``
                                     the ``Generated`` annotation. By default, the date and time |br|
                                     the source code was generated is output.                             
``sourceFolder``                     Specifies the directory where the source code will be generated. |br|                              ``src/gen/java``
                                     It is interpreted as a relative path from the ``output`` of |br|
                                     the Maven plugin setting of the OpenAPI Generator. By configuring |br|
                                     this, the source code generated by this tool will be included in |br|
                                     the compilation target when ``mvn compile`` is executed.
``useTags``                          The unit of the generated Resource (Action) interface is the tag |br|                              ``false``
                                     attached to the endpoint, not the path. If multiple tags are attached |br|
                                     to the endpoint, the first tag is used.
``serializableModel``                Implement the ``java.io.Serializable`` interface in the Model |br|                                 ``false``
                                     you are generating.
``generateBuilders``                 Generate a Builder class for the Model.                                                            ``false``
``useBeanValidation``                From the validation definition in the OpenAPI document, |br|                                       ``false``
                                     source code is generated to perform validation using |br|
                                     :ref:`bean_validation` .
``additionalModelTypeAnnotations``   Add additional annotations to the class declaration of the Model |br|                              None
                                     to be generated. To add multiple annotations, separate them with ``;``. 
``additionalEnumTypeAnnotations``    Annotate the generated enum type with additional annotations. |br|                                 None
                                     To add multiple annotations, separate them with ``;`` .
``primitivePropertiesAsString``      Prints all properties of the model that are primitive data types |br|                              ``false``
                                     as ``String``.
``supportConsumesMediaTypes``        Specifies the media types that the Resource (Action) interface to be |br|                          ``application/json,multipart/form-data``
                                     generated will accept requests for, separated by ``,`` .
``supportProducesMediaTypes``        Specifies the media types that the generated Resource (Action) |br|                                ``application/json``
                                     interface will respond to, separated by ``,`` .
==================================== ================================================================================================== =====================================================================

Generate source code that uses Bean Validation
==================================================

If you want to generate source code to use :ref:`bean_validation` , set the value of ``useBeanValidation`` to ``true`` .

An example setting is shown below.

.. code-block:: xml

            <configuration>
              <!-- Specify the file path of the OpenAPI document -->
              <inputSpec>${project.basedir}/src/main/resources/openapi.yaml</inputSpec>
              <generatorName>nablarch-jaxrs</generatorName>
              <configOptions>
                <sourceFolder>src/gen/java</sourceFolder>
                <apiPackage>com.example.api</apiPackage>
                <modelPackage>com.example.model</modelPackage>
                <!-- Generate source code using Bean Validation -->
                <useBeanValidation>true</useBeanValidation>
              </configOptions>
            </configuration>

Default value of ``useBeanValidation`` is ``false``, so annotations that use :ref:`bean_validation` function are not annotated by default.

This is because the validation definitions defined in the OpenAPI specification often do not satisfy business requirements, and it is also not possible to define correlated validation.

Please refer to :ref:`openapi_property_to_bean_validation` for details on the specifications and operational precautions when generating source code to use the validation function, including these points.

.. _NablarchOpenApiGeneratorAsCli:

Use as CLI
===========================

This tool is assumed to be used as a Maven plugin. However, it can also be used as a CLI. Here we will introduce how to use it as a CLI as a supplement.

To run it as a CLI, download the `OpenAPI Generator 7.10.0 JAR file(external site) <https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/7.10.0/openapi-generator-cli-7.10.0.jar>`_ and `this tool's JAR file(external site) <https://repo1.maven.org/maven2/com/nablarch/tool/nablarch-openapi-generator/1.0.0/nablarch-openapi-generator-1.0.0.jar>`_  , and run it with the java command. An example of execution is shown below.

.. code-block:: text

  java -cp openapi-generator-cli-7.10.0.jar:nablarch-openapi-generator-1.0.0.jar org.openapitools.codegen.OpenAPIGenerator generate --generator-name nablarch-jaxrs --input-spec openapi.yaml --output out --additional-properties=apiPackage=com.example.api,modelPackage=com.example.model,useBeanValidation=true,hideGenerationTimestamp=true

Specify ``nablarch-jaxrs`` for ``--generator-name`` . The OpenAPI Generator configuration items in :ref:`NablarchOpenApiGeneratorConfiguration` can also be specified in the OpenAPI Generator CLI. For details, see the result of the command below.

.. code-block:: text

  java -jar openapi-generator-cli-7.10.0.jar help generate

.. tip::

  The format for specifying OpenAPI Generator options is hyphen-separated, like this: ``--generator-name`` .

The tool-specific configuration of :ref:`NablarchOpenApiGeneratorConfiguration` is specified in ``--additional-properties`` with the format ``key=value``. Multiple settings are separated by ``,`` .

.. tip::

  The tool-specific configuration is specified by ``--additional-properties=`` followed by the name of the item and its value as is. For example, ``--additional-properties=hideGenerationTimestamp=true`` .

Source Code Generation Specifications
---------------------------------------

The following describes the specifications for how this tool generates source code based on an OpenAPI document.

.. important::

  Nablarch RESTful Web Service does not support all annotations provided by Jakarta RESTful Web Services. Therefore, please note that the contents of the OpenAPI document other than those described here will not be reflected in the generated source code.

  For information about annotations supported by Nablarch RESTful Web Service, see :ref:`restful_web_service_architecture` and :ref:`router_adaptor_path_annotation` for the routing adapter.

Resource (Action) interface generation specifications
=========================================================

The generation specifications for Resource (Action) interface are described here. It will be generated in accordance with :ref:`rest_feature_details-method_signature`, so please refer to this as well.

Specifications related to the generation unit and type definition of the Resource (Action) interface are shown below.

* Generated based on the path and operation information defined in the OpenAPI document.
* Generate it as a Java interface.
* The unit for generating Resource (Action) interface is selected from the following:

  * By default, it is compiled at the first level of the path defined in the OpenAPI document.
  * If ``useTags`` is set to ``true``, the unit of measurement will be the tags attached to the operation.

* The Resource (Action) interface declaration is annotated with the ``Path`` annotation.
* Annotate with the ``Generated`` annotation.

The specifications regarding method generation of Resource (Action) interface are shown below.

**Annotations that annotate method declarations**

================== ==============================================================================================================
Annotation         Explanation
================== ==============================================================================================================
``GET``            Annotate when the operation's HTTP method is GET.
``POST``           Annotate when the operation's HTTP method is POST.
``PUT``            Annotate when the operation's HTTP method is PUT.
``DELETE``         Annotate when the operation's HTTP method is DELETE.
``PATCH``          Annotate when the operation's HTTP method is PATCH.
``HEAD``           Annotate when the operation's HTTP method is HEAD.
``OPTIONS``        Annotate when the operation's HTTP method is OPTIONS.
``Consumes``       Annotate if the content type of the request is defined.
``Produces``       Annotate if the response content type is defined and is other than ``type: string`` and ``format: binary`` .
``Valid``          Annotate if a request body is defined and ``useBeanValidation`` is ``true`` .
================== ==============================================================================================================

.. tip::

  ``type: string`` and ``format: binary`` indicate that a file will be downloaded. In this case, the content type is set using :java:extdoc:`HttpResponse#setContentType<nablarch.fw.web.HttpResponse.setContentType(java.lang.String)>` .
  
**Method name generation specification**

* Use the value of the ``operationId`` element in the OpenAPI document as the method name.
* If the ``operationId`` element is not set, the method name is generated by combining the path value and the HTTP method name.

**Method argument generation specifications**

====================================================================== =============================================================================================================================
Method Argument Types                                                  Explanation
====================================================================== =============================================================================================================================
Request Model Type                                                     When a request body is received and the request content type is other than multipart, set the corresponding |br|
                                                                       Model type argument.
:java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>`   Always generate and set as argument.
:java:extdoc:`ExecutionContext <nablarch.fw.ExecutionContext>`         Always generate and set as argument.
====================================================================== =============================================================================================================================

.. tip::

  * RESTful Web Service do not support annotations such as ``PathParam`` and ``QueryParam`` defined in Jakarta RESTful Web Services, so the definition of ``parameters`` in the OpenAPI document is not reflected in the method arguments. This information can be obtained from :java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>` .
  * If the content type of the request is ``multipart/form-data``, the request Model type argument will not be generated. Uploaded files should be retrieved using :java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>` .

**Method return value generation specifications**

====================================================================== ==========================================================================================
Method Return Types                                                    Explanation
====================================================================== ==========================================================================================
:java:extdoc:`EntityResponse <nablarch.fw.jaxrs.EntityResponse>`       Generated if the response is a Model. The type parameter reflects the type of the Model.
:java:extdoc:`HttpResponse <nablarch.fw.web.HttpResponse>`             Generated if the response is not a Model or the HTTP status code is other than ``200`` .
====================================================================== ==========================================================================================

Model generation specifications
===================================

The specifications regarding the Model generation units and type definitions are shown below.

* Generate for a model defined as a schema.
* Generate as a Java class.
* Annotate the ``JsonTypeName`` annotation.
* Annotate the ``Generated`` annotation.

The generation specifications for the Model properties are shown below.

* Generates properties corresponding to the fields defined in the schema in the OpenAPI document.
* Generate getters and setters for properties and annotate them with ``JsonProperty`` annotations.
* Generate a chainable method that sets the property value and returns the Model's own type.
* If ``useBeanValidation`` is ``true`` and the OpenAPI document contains validation definitions, it enables :ref:`bean_validation` .
* The annotations used in validation are those provided by Nablarch in the :ref:`bean_validation` package and those in the Jakarta EE standard :java:extdoc:`jakarta.validation.constraints` package.

The correspondence specifications between data types and formats in the OpenAPI document and Java data types are described in :ref:`openapi_datatypes_format_to_java_datatypes` , and the correspondence specifications between validation definitions and annotations used in validation are described in :ref:`openapi_property_to_bean_validation` .

Other Model generation specifications are shown below.

* Generates the ``hashCode``, ``equals`` and ``toString`` methods.

Modules on which the generated source code depends
==================================================

To build the source code generated by this tool, the following modules are required as dependencies.

.. code-block:: xml

    <dependency>
      <groupId>com.nablarch.framework</groupId>
      <artifactId>nablarch-fw-jaxrs</artifactId>
    </dependency>
    <dependency>
       <groupId>com.nablarch.framework</groupId>
       <artifactId>nablarch-core-validation-ee</artifactId>
    </dependency>
    <dependency>
      <groupId>jakarta.ws.rs</groupId>
      <artifactId>jakarta.ws.rs-api</artifactId>
    </dependency>
    <dependency>
      <groupId>jakarta.annotation</groupId>
      <artifactId>jakarta.annotation-api</artifactId>
    </dependency>
    <dependency>
      <groupId>com.fasterxml.jackson.core</groupId>
      <artifactId>jackson-annotations</artifactId>
      <version>2.17.1</version>
    </dependency>

All of these are included in the dependencies set up in the blank RESTful Web Service project.

.. _openapi_datatypes_format_to_java_datatypes:

Correspondence specifications between OpenAPI document data types and formats and Java data types
====================================================================================================

The following table shows the correspondence between the data types and formats defined in the OpenAPI document and the Java data types defined by this tool.

=================================== ======================================== ===========================================================================
OpenAPI data types( ``type`` )      OpenAPI format( ``format`` )             Model property data types
=================================== ======================================== ===========================================================================
``integer``                                                                  ``java.lang.Integer``
``integer``                         ``int32``                                ``java.lang.Integer``
``integer``                         ``int64``                                ``java.lang.Long``
``number``                                                                   ``java.math.BigDecimal``
``number``                          ``float``                                ``java.lang.Float``
``number``                          ``double``                               ``java.lang.Double``
``boolean``                                                                  ``java.lang.Boolean``
``string``                                                                   ``java.lang.String``
``string``                          ``byte``                                 ``byte[]``
``string``                          ``date``                                 ``java.time.LocalDate``
``string``                          ``date-time``                            ``java.time.OffsetDateTime``
``string``                          ``number``                               ``java.math.BigDecimal``
``string``                          ``uuid``                                 ``java.util.UUID``
``string``                          ``uri``                                  ``java.net.URI``
``string``                                                                   enum ( Specifying ``enum`` will generate the corresponding Enum type. )
``array``                                                                    ``java.util.List``
``array``                                                                    ``java.util.Set`` ( When ``uniqueItems: true`` )
``object``                                                                   Corresponding Model type
``object``                                                                   If there is no corresponding type, ``java.lang.Object``
=================================== ======================================== ===========================================================================

.. tip::

  * ``type: string`` and ``format: binary`` are only available if the request content type is ``multipart/form-data`` . Using any other content type or encountering this data type/format combination in the response Model definition will abort Model creation.
  * In the case of ``type: string`` , there are many other formats available in addition to those listed in the table above, but all are generated as ``java.lang.String`` .

.. _openapi_property_to_bean_validation:

Mapping OpenAPI document validation definitions to Bean Validation
======================================================================

In this tool, the default value of ``useBeanValidation`` is ``false``, so by default, annotations used in :ref:`bean_validation` will not be added regardless of the definition in the OpenAPI document. However, if you set it to ``true``, annotations will be added to properties according to the following two policies depending on the contents of the OpenAPI document.

* Validation corresponding to properties defined in the OpenAPI specification
* domain validation

Validation corresponding to properties defined in the OpenAPI specification
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When validation is defined using `properties defined in the OpenAPI specification(external site) <https://spec.openapis.org/oas/v3.0.3.html#properties>`_ , annotations should be added according to the following table.

=================================== ======================================== ========================================== ============================================================================================================
OpenAPI data types( ``type`` )      OpenAPI format( ``format`` )             Properties used in OpenAPI                 Annotations for validation
=================================== ======================================== ========================================== ============================================================================================================
``integer``                         (any format)                             ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``integer``                                                                  ``minimum`` and ``maximum``                :java:extdoc:`NumberRange(min = {minimum}, max = {maximum}) <nablarch.core.validation.ee.NumberRange>`
``integer``                         ``int32``                                ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``integer``                         ``int32``                                ``minimum`` and ``maximum``                :java:extdoc:`NumberRange(min = {minimum}, max = {maximum}) <nablarch.core.validation.ee.NumberRange>`
``integer``                         ``int64``                                ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``integer``                         ``int64``                                ``minimum`` and ``maximum``                :java:extdoc:`NumberRange(min = {minimum}, max = {maximum}) <nablarch.core.validation.ee.NumberRange>`
``number``                          (any format)                             ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``number``                                                                   ``minimum`` and ``maximum``                :java:extdoc:`DecimalRange(min = "{minimum}", max = "{maximum}") <nablarch.core.validation.ee.DecimalRange>`
``number``                          ``float``                                ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``number``                          ``float``                                ``minimum`` and ``maximum``                :java:extdoc:`DecimalRange(min = "{minimum}", max = "{maximum}") <nablarch.core.validation.ee.DecimalRange>`
``number``                          ``double``                               ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``number``                          ``double``                               ``minimum`` and ``maximum``                :java:extdoc:`DecimalRange(min = "{minimum}", max = "{maximum}") <nablarch.core.validation.ee.DecimalRange>`
``boolean``                                                                  ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``string``                          (any format)                             ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``string``                                                                   ``minLength`` and ``maxLength``            :java:extdoc:`Length(min = {minLength}, max = {maxLength}) <nablarch.core.validation.ee.Length>`
``string``                                                                   ``pattern``                                :java:extdoc:`Pattern(regexp = "{pattern}")<jakarta.validation.constraints.Pattern>`
``array``                                                                    ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``array``                                                                    ``minItems`` and ``maxItems``              :java:extdoc:`Size(min = {minItems}, max = {maxItems}) <nablarch.core.validation.ee.Size>`
=================================== ======================================== ========================================== ============================================================================================================

.. tip::

  * ``multipleOf`` , ``exclusiveMinimum`` , ``exclusiveMaximum`` , ``minProperties`` and ``maxProperties`` are not supported.
  * Combinations of ``minimum`` and ``maximum`` , ``minLength`` and ``maxLength`` , and ``minItems`` and ``maxItems`` can be specified with just one of them.
  * If the Java data type is ``java.math.BigDecimal`` , ``java.util.List`` , ``java.util.Set`` , or a model, annotate with ``Valid`` annotation.
  * Only :java:extdoc:`Pattern<jakarta.validation.constraints.Pattern>` is annotated with Jakarta Bean Validation standard annotations, and the rest are annotated with annotations of :ref:`bean_validation` provided by Nablarch.

Domain validation
^^^^^^^^^^^^^^^^^^^^

This tool uses `extension of the OpenAPI specification(external site) <https://spec.openapis.org/oas/v3.0.3.html#specification-extensions>`_ to support :ref:`domain validation<bean_validation-domain_validation>` that cannot be expressed by the OpenAPI specification.

Use ``x-nablarch-domain`` as the extended property and specify the domain name as the value.

.. code-block:: yaml

        propertyName:
          type: string
          x-nablarch-domain: "domainName"

If you generate source code by specifying ``useBeanValidation`` as ``true``, the target property will be annotated with :java:extdoc:`Domain("{domainName}") <nablarch.core.validation.ee.Domain>` .

Further, since domain validation can contain various validation definitions, if validation definitions that may conflict are detected, source code generation is stopped. This is because if the same validation rules as those included in the domain are specified, duplicate validation will be performed.

Specifically, if any of ``minimum`` , ``maximum`` , ``minLength`` , ``maxLength`` , ``minItems`` , ``maxItems``, or ``pattern`` is specified for a property that specifies ``x-nablarch-domain``, source code generation will be stopped.

``required`` indicates a required item and is not enforced by the domain, so it can be used in combination.

Operational precautions regarding validation
==================================================

This section describes precautions to take when using this tool to generate source code including validation definitions.

Points to note when the requirements for item-level or correlation validation cannot be met within the scope of the OpenAPI specification
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Validation stipulated in the OpenAPI specification only includes required definitions, length checks, and regular expression checks, so it is assumed that this will not be sufficient for business applications.

Furthermore, since it is not desirable to directly modify the generated source code, correlation validation cannot be implemented in the generated model even if domain validation is used.

For this reason, the validation requirements cannot be satisfied within the scope of the OpenAPI specification and this tool, and a separate implementation is required. As a result, it should be noted that the validation definitions are likely to be distributed between the generated model and manually implemented forms, etc.

**How to implement when validation definitions are not included in the automatically generated Model**

This section introduces a method to create a form etc. with the same definition as the model automatically generated as the validation definition, copy the property values using :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` , and then perform validation.

The reason why this tool does not add validation annotations by default is that, as mentioned above, it is anticipated that validation definitions may end up being distributed, which is considered undesirable.

The concept is similar to :ref:`bean_validation-execute_explicitly` and the implementation diagram is shown below.

.. code-block:: java

  public class ProjectAction implements ProjectsApi {  // ProjectsApi is the interface generated by this tool.

      // Implement the methods defined in the interface
      @Override
      public EntityResponse<ProjectResponse> createProject(ProjectCreateRequest projectCreateRequest, JaxRsHttpRequest jaxRsHttpRequest, ExecutionContext context) {
          // A form with the same property definition as the Model, with single-item validation and correlation validation added
          ProjectCreateForm form;

          try {
              // Explicitly run validation after copying values f​From the Model to the Form in a utility class
              form = ProjectValidatorUtil.validate(ProjectCreateForm.class, projectCreateRequest);
          } catch (ApplicationException e) {
              // Perform any processing when a validation error occurs
              // ...

              throw e;
          }

          // Omitted

          return response;
      }
  }

  // Image of utility class
  public final class ProjectValidatorUtil {
      // Other implementations are omitted.

      /**
       * Generate a Bean from the HTTP request and perform validation.
       *
       * @param beanClass Bean class you want to generate
       * @param src The object from which the properties are copied
       * @return  Bean object with registered values for properties
       */
      public static <T> T validate(Class<T> beanClass, Object src) {
          T bean = BeanUtil.createAndCopy(beanClass, src));
          ValidatorUtil.validate(bean);
          return bean;
      }
  }

Points to note when using domain validation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Domain validation allows you to organize your validation definitions by defining a domain for your Model properties, or to use validations that are not supported by the OpenAPI specification.

However, the validation specifications, including those supported by the OpenAPI specification, will be hidden from the domain side. As a result, please note that the validation specifications may not be visible from the OpenAPI document.

Example of OpenAPI document and generated source code
----------------------------------------------------------

Below is an example of an OpenAPI document and the generated source code.

The following is an example of the settings for this tool when generating source code. If settings different from these settings are required, the example settings for this tool are also provided.

.. code-block:: xml

            <configuration>
              <inputSpec>${project.basedir}/src/main/resources/openapi.yaml</inputSpec>
              <generatorName>nablarch-jaxrs</generatorName>
              <configOptions>
                <sourceFolder>src/gen/java</sourceFolder>
                <apiPackage>com.example.api</apiPackage>
                <modelPackage>com.example.model</modelPackage>
              </configOptions>
            </configuration>

The various examples described are excerpts for the purpose of getting an overview of the generated source code.

Example of defining paths and operations in an OpenAPI document and generating source code
===============================================================================================

Example OpenAPI document

.. code-block:: yaml

  /projects:
    post:
      tags:
      - project
      summary: Create a project
      description: Create a project
      operationId: createProject
      requestBody:
        description: Project Creation Request
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ProjectCreateRequest'
      responses:
        "200":
          description: Information about the created project
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProjectResponse'
  /projects/{id}:
    get:
      tags:
      - project
      summary: Get the project
      description: Get a project by specifying the project ID
      operationId: findProjectById
      parameters:
      - name: id
        in: path
        description: ID
        required: true
        schema:
          type: string
      responses:
        "200":
          description: Project information obtained
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProjectResponse'
        "404":
          description: If the project is not found

Example of Resource (Action) interface generated by this tool

.. code-block:: java

  @Path("/projects")
  @jakarta.annotation.Generated(value = "nablarch.tool.openapi.codegen.JavaNablarchJaxrsServerCodegen", date = "2024-12-10T13:54:26.470544738+09:00[Asia/Tokyo]", comments = "Generator version: 7.10.0")
  public interface ProjectsApi {
      /**
       * POST  : Create a project
       *
       * Create a project
       *
       * @param projectCreateRequest Project Creation Request
       * @param jaxRsHttpRequest HTTP Request
       * @param context Handler Execution Context
       * @return Information about the created project
       */
      @POST
      @Consumes({ "application/json" })
      @Produces({ "application/json" })
      EntityResponse<ProjectResponse> createProject(ProjectCreateRequest projectCreateRequest, JaxRsHttpRequest jaxRsHttpRequest, ExecutionContext context);

      /**
       * GET /{id} : Get the project
       *
       * Get a project by specifying the project ID
       *
       * @param jaxRsHttpRequest HTTP Request
       * @param context Handler Execution Context
       * @return Project information obtained
       * @return If the project is not found
       */
      @GET
      @Path("/{id}")
      @Produces({ "application/json" })
      EntityResponse<ProjectResponse> findProjectById(JaxRsHttpRequest jaxRsHttpRequest, ExecutionContext context);

  }

Example of OpenAPI document schema definition and source code generation
===========================================================================

Example OpenAPI document

.. code-block:: yaml

    ProjectResponse:
      description: Project Information
      type: object
      properties:
        id:
          format: uuid
          description: Project ID
          type: string
        name:
          description: Project name
          type: string
        sales:
          format: int64
          description: Sales
          type: integer
        startDate:
          format: date
          description: Start date
          type: string
        endDate:
          format: date
          description: End date
          type: string

Example of a model generated by this tool

.. code-block:: java

  @JsonTypeName("ProjectResponse")
  @jakarta.annotation.Generated(value = "nablarch.tool.openapi.codegen.JavaNablarchJaxrsServerCodegen", date = "2024-12-10T13:54:26.470544738+09:00[Asia/Tokyo]", comments = "Generator version: 7.10.0")
  public class ProjectResponse   {
    private UUID id;
    private String name;
    private Long sales;
    private LocalDate startDate;
    private LocalDate endDate;
   
      /**
       * Project ID
       */
      public ProjectResponse id(UUID id) {
          this.id = id;
          return this;
      }
   
      
      @JsonProperty("id")
      public UUID getId() {
          return id;
      }
   
      @JsonProperty("id")
      public void setId(UUID id) {
          this.id = id;
      }
   
      /**
       * Project name
       */
      public ProjectResponse name(String name) {
          this.name = name;
          return this;
      }
   
      
      @JsonProperty("name")
      public String getName() {
          return name;
      }
   
      @JsonProperty("name")
      public void setName(String name) {
          this.name = name;
      }
   
      /**
       * Sales
       */
      public ProjectResponse sales(Long sales) {
          this.sales = sales;
          return this;
      }
   
      
      @JsonProperty("sales")
      public Long getSales() {
          return sales;
      }
   
      @JsonProperty("sales")
      public void setSales(Long sales) {
          this.sales = sales;
      }
   
      /**
       * Start date
       */
      public ProjectResponse startDate(LocalDate startDate) {
          this.startDate = startDate;
          return this;
      }
   
      
      @JsonProperty("startDate")
      public LocalDate getStartDate() {
          return startDate;
      }
   
      @JsonProperty("startDate")
      public void setStartDate(LocalDate startDate) {
          this.startDate = startDate;
      }
   
      /**
       * End date
       */
      public ProjectResponse endDate(LocalDate endDate) {
          this.endDate = endDate;
          return this;
      }
   
      
      @JsonProperty("endDate")
      public LocalDate getEndDate() {
          return endDate;
      }
   
      @JsonProperty("endDate")
      public void setEndDate(LocalDate endDate) {
          this.endDate = endDate;
      }

      // hashCode, equals, toString, etc. are omitted.
  }

Example of generating source code that uses Bean Validation
============================================================

Example OpenAPI document

.. code-block:: yaml

  ## Paths and Operations
  /projects:
    post:
      tags:
      - project
      summary: Create a project
      description: Create a project
      operationId: createProject
      requestBody:
        description: Project Creation Request
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ProjectCreateRequest'
      responses:
        "200":
          description: Information about the created project
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProjectResponse'

    ## Scheme
    ProjectCreateRequest:
      description: Project Create Request
      required:
      - projectName
      - projectType
      - startDate
      type: object
      properties:
        projectName:
          description: Project name
          maxLength: 100
          minLength: 1
          type: string
        projectType:
          description: Project type
          maxLength: 100
          minLength: 1
          type: string
        startDate:
          format: date
          description: Start date
          type: string
        endDate:
          format: date
          description: End date
          type: string

Example of settings for this tool

.. code-block:: xml

            <configuration>
              <inputSpec>${project.basedir}/src/main/resources/openapi.yaml</inputSpec>
              <generatorName>nablarch-jaxrs</generatorName>
              <configOptions>
                <sourceFolder>src/gen/java</sourceFolder>
                <apiPackage>com.example.api</apiPackage>
                <modelPackage>com.example.model</modelPackage>
                <!-- If you want to use Bean Validation, specify true for useBeanValidation. -->
                <useBeanValidation>true</useBeanValidation>
              </configOptions>
            </configuration>

Example of Resource (Action) interface generated by this tool

.. code-block:: java

  @Path("/projects")
  @jakarta.annotation.Generated(value = "nablarch.tool.openapi.codegen.JavaNablarchJaxrsServerCodegen", date = "2024-12-10T13:54:26.470544738+09:00[Asia/Tokyo]", comments = "Generator version: 7.10.0")
  public interface ProjectsApi {
      /**
       * POST  : Create a project
       *
       * Create a project
       *
       * @param projectCreateRequest Project Creation Request
       * @param jaxRsHttpRequest HTTP Request
       * @param context Handler Execution Context
       * @return Information about the created project
       */
      @POST
      @Consumes({ "application/json" })
      @Produces({ "application/json" })
      // The @Valid annotation is added when a request is received in the HTTP body.
      @Valid
      EntityResponse<ProjectResponse> createProject(ProjectCreateRequest projectCreateRequest, JaxRsHttpRequest jaxRsHttpRequest, ExecutionContext context);
  }

Example of a model generated by this tool

.. code-block:: java

  @JsonTypeName("ProjectCreateRequest")
  @jakarta.annotation.Generated(value = "nablarch.tool.openapi.codegen.JavaNablarchJaxrsServerCodegen", date = "2024-12-10T13:54:26.470544738+09:00[Asia/Tokyo]", comments = "Generator version: 7.10.0")
  public class ProjectCreateRequest   {
    private String projectName;
    private String projectType;
    private LocalDate startDate;
    private LocalDate endDate;
  
      /**
       * Project name
       */
      public ProjectCreateRequest projectName(String projectName) {
          this.projectName = projectName;
          return this;
      }
  
  
      @JsonProperty("projectName")
      @Required @Length(min = 1, max = 100)
      public String getProjectName() {
          return projectName;
      }
  
      @JsonProperty("projectName")
      public void setProjectName(String projectName) {
          this.projectName = projectName;
      }
  
      /**
       * Project type
       */
      public ProjectCreateRequest projectType(String projectType) {
          this.projectType = projectType;
          return this;
      }
  
  
      @JsonProperty("projectType")
      @Required @Length(min = 1, max = 100)
      public String getProjectType() {
          return projectType;
      }
  
      @JsonProperty("projectType")
      public void setProjectType(String projectType) {
          this.projectType = projectType;
      }
  
      /**
       * Start date
       */
      public ProjectCreateRequest startDate(LocalDate startDate) {
          this.startDate = startDate;
          return this;
      }
  
  
      @JsonProperty("startDate")
      @Required
      public LocalDate getStartDate() {
          return startDate;
      }
  
      @JsonProperty("startDate")
      public void setStartDate(LocalDate startDate) {
          this.startDate = startDate;
      }
  
      /**
       * End date
       */
      public ProjectCreateRequest endDate(LocalDate endDate) {
          this.endDate = endDate;
          return this;
      }
  
  
      @JsonProperty("endDate")
  
      public LocalDate getEndDate() {
          return endDate;
      }
  
      @JsonProperty("endDate")
      public void setEndDate(LocalDate endDate) {
          this.endDate = endDate;
      }

      // hashCode, equals, toString, etc. are omitted.
  }

Example of source code generation using domain validation
=================================================================

Example OpenAPI document

.. code-block:: yaml

  ## Paths and Operations
  /projects:
    post:
      tags:
      - project
      summary: Create a project
      description: Create a project
      operationId: createProject
      requestBody:
        description: Project Creation Request
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ProjectCreateRequest'
      responses:
        "200":
          description: Information about the created project
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProjectResponse'

    ## Scheme
    ProjectCreateRequest:
      description: Project Create Request
      required:
      - projectName
      - projectType
      - startDate
      type: object
      properties:
        projectName:
          description: Project name
          type: string
          ## Using domain validation
          x-nablarch-domain: "projectName"

Example of settings for this tool

.. code-block:: xml

            <configuration>
              <inputSpec>${project.basedir}/src/main/resources/openapi.yaml</inputSpec>
              <generatorName>nablarch-jaxrs</generatorName>
              <configOptions>
                <sourceFolder>src/gen/java</sourceFolder>
                <apiPackage>com.example.api</apiPackage>
                <modelPackage>com.example.model</modelPackage>
                <!-- If you want to use Bean Validation, specify true for useBeanValidation. -->
                <useBeanValidation>true</useBeanValidation>
              </configOptions>
            </configuration>

Example of a model generated by this tool

.. code-block:: java

  @JsonTypeName("ProjectCreateRequest")
  @jakarta.annotation.Generated(value = "nablarch.tool.openapi.codegen.JavaNablarchJaxrsServerCodegen", date = "2024-12-10T13:54:26.470544738+09:00[Asia/Tokyo]", comments = "Generator version: 7.10.0")
  public class ProjectCreateRequest   {
    private String projectName;
  
      /**
       * Project name
       */
      public ProjectCreateRequest projectName(String projectName) {
          this.projectName = projectName;
          return this;
      }
  
      
      @JsonProperty("projectName")
      @Required @Domain("projectName")
      public String getProjectName() {
          return projectName;
      }
  
      @JsonProperty("projectName")
      public void setProjectName(String projectName) {
          this.projectName = projectName;
      }

      // hashCode, equals, toString, etc. are omitted.
  }

Example of a file upload definition
========================================

Example OpenAPI document

.. code-block:: yaml

  ## Paths and Operations
  /customers/upload:
    post:
      tags:
      - customer
      summary: Upload a customer CSV file
      description: Import customer information by uploading a customer CSV file
      operationId: uploadCustomersCsvFile
      requestBody:
        description: Customer CSV file information
        content:
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CustomersCsvFileUploadRequest'
      responses:
        "200":
          description: Result of importing customer CSV upload file
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CustomersCsvFileUploadResultResponse'


    ## Schema
    CustomersCsvFileUploadRequest:
      description: Customer CSV file information
      required:
      - fileName
      - file
      type: object
      properties:
        fileName:
          description: File name
          type: string
        file:
          description: Customer CSV file
          type: string
          format: binary

Example of Resource (Action) interface generated by this tool

.. code-block:: java

  @Path("/customers/upload")
  @jakarta.annotation.Generated(value = "nablarch.tool.openapi.codegen.JavaNablarchJaxrsServerCodegen", date = "2024-12-10T14:36:36.602623815+09:00[Asia/Tokyo]", comments = "Generator version: 7.10.0")
  public interface CustomersApi {
      /**
       * POST  : Upload a customer CSV file
       *
       * Import customer information by uploading a customer CSV file
       *
       * @param jaxRsHttpRequest HTTP Request
       * @param context Handler Execution Context
       * @return Result of importing customer CSV upload file
       */
      @POST
      @Consumes({ "multipart/form-data" })
      @Produces({ "application/json" })
      EntityResponse<CustomersCsvFileUploadResultResponse> uploadCustomersCsvFile(JaxRsHttpRequest jaxRsHttpRequest, ExecutionContext context);

  }

.. tip::

  When uploading a file, specify ``multipart/form-data`` as the request content type. Also, specify ``type: string`` and ``format: binary`` for the uploaded file. In this case, the source code for the Model corresponding to the schema is not generated. The uploaded file is retrieved from :java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>` .

Example of a file download definition
========================================

Example OpenAPI document

.. code-block:: yaml

  /customers/upload:
    get:
      tags:
      - customer
      summary: Download customer information as a CSV file
      description: Download customer information as a CSV file
      operationId: downloadCustomersCsvFile
      responses:
        "200":
          description: Customer CSV file
          content:
            text/csv:
              schema:
                type: string
                format: binary

Example of Resource (Action) interface generated by this tool

.. code-block:: java

  @Path("/customers/upload")
  @jakarta.annotation.Generated(value = "nablarch.tool.openapi.codegen.JavaNablarchJaxrsServerCodegen", date = "2024-12-10T14:48:03.670170037+09:00[Asia/Tokyo]", comments = "Generator version: 7.10.0")
  public interface CustomersApi {
      /**
       * GET  : Download customer information as a CSV file
       *
       * Download customer information as a CSV file
       *
       * @param jaxRsHttpRequest HTTP Request
       * @param context Handler Execution Context
       * @return Customer CSV file
       */
      @GET
      HttpResponse downloadCustomersCsvFile(JaxRsHttpRequest jaxRsHttpRequest, ExecutionContext context);

  }

.. tip::

  When downloading a file, you can specify any type as the response content type. The response schema definition should be ``type: string`` and ``format: binary``, and the content of the file to be downloaded and the response headers should be set using :java:extdoc:`HttpResponse <nablarch.fw.web.HttpResponse>` .


.. |br| raw:: html

  <br />
