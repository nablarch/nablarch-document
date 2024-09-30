=========================================================================
Regarding the specification name of Jakarta EE
=========================================================================

.. contents:: Table of contents
  :depth: 3
  :local:

Regarding the notation of acronyms
=========================================================================

Nablarch6 basically replaces all acronyms of specification in Java EE with Jakarta EE specification names.

**Example**

* JPA (Java Persistence API) -> Jakarta Persistence
* JAX-RS (Java API for RESTful Web Services) -> Jakarta RESTful Web Services

However, some acronyms are retained where readability is compromised.
Unless otherwise specified, the acronyms used in this document refer to the Jakarta EE specifications as follows:


.. list-table:: Mapping acronyms to Jakarta EE specifications
   :widths: 1,3
   :header-rows: 1

   * - Acronyms
     - Jakarta EE specifications
   * - JSF
     - `Jakarta Faces (external site) <https://jakarta.ee/specifications/faces/>`_
   * - JASPIC
     - `Jakarta Authentication (external site) <https://jakarta.ee/specifications/authentication/>`_
   * - JACC
     - `Jakarta Authorization (external site) <https://jakarta.ee/specifications/authorization/>`_
   * - JMS
     - `Jakarta Messaging (external site) <https://jakarta.ee/specifications/messaging/>`_
   * - JPA
     - `Jakarta Persistence (external site) <https://jakarta.ee/specifications/persistence/>`_
   * - JTA
     - `Jakarta Transactions (external site) <https://jakarta.ee/specifications/transactions/>`_
   * - jBatch
     - `Jakarta Batch (external site) <https://jakarta.ee/specifications/batch/>`_
   * - JCA
     - `Jakarta Connectors (external site) <https://jakarta.ee/specifications/connectors/>`_
   * - JAF
     - `Jakarta Activation (external site) <https://jakarta.ee/specifications/activation/>`_
   * - EL
     - `Jakarta Expression Language (external site) <https://jakarta.ee/specifications/expression-language/>`_
   * - EJB
     - `Jakarta Enterprise Beans (external site) <https://jakarta.ee/specifications/enterprise-beans/>`_
   * - JAXB
     - `Jakarta XML Binding (external site) <https://jakarta.ee/specifications/xml-binding/>`_
   * - JSON-B
     - `Jakarta JSON Binding (external site) <https://jakarta.ee/specifications/jsonb/>`_
   * - JSON-P
     - `Jakarta JSON Processing (external site) <https://jakarta.ee/specifications/jsonp/>`_
   * - JSP
     - `Jakarta Server Pages (external site) <https://jakarta.ee/specifications/pages/>`_
   * - JAX-WS
     - `Jakarta XML Web Services (external site) <https://jakarta.ee/specifications/xml-web-services/>`_
   * - JAX-RS
     - `Jakarta RESTful Web Services (external site) <https://jakarta.ee/specifications/restful-ws/>`_
   * - JSTL
     - `Jakarta Standard Tag Library (external site) <https://jakarta.ee/specifications/tags/>`_
   * - CDI
     - `Jakarta Contexts and Dependency Injection (external site) <https://jakarta.ee/specifications/cdi/>`_

.. _renamed_features_in_nablarch_6:

Regarding features that have been renamed in Nablarch 5 and 6
=========================================================================

As Java EE was transferred to the Eclipse Foundation and the names of each specification were changed, the names of features provided by Nablarch that included Java EE specification names were changed.
Below is a mapping table of names before and after the change.


.. list-table:: Mapping table of features whose names have been changed in Nablarch 5 and 6
   :widths: 1,1
   :header-rows: 1

   * - Name up to Nablarch5
     - Name from Nablarch6
   * - JAX-RS BeanValidation Handler
     - :doc:`../application_framework/application_framework/handlers/rest/jaxrs_bean_validation_handler` [#jaxr_rs_bean_validation_handler_footnote]_
   * - JAX-RS Adapter
     - :doc:`../application_framework/adaptors/jaxrs_adaptor`
   * - JAX-RS support
     - :doc:`Jakarta RESTful Web Services support <../application_framework/application_framework/web_service/rest/architecture>`
   * - JAX-RS Response Handler
     - :doc:`../application_framework/application_framework/handlers/rest/jaxrs_response_handler`
   * - JSP Custom Tags
     - :doc:`../application_framework/application_framework/libraries/tag`
   * - JSP Static Analysis Tool
     - :doc:`../development_tools/toolbox/JspStaticAnalysis/index`
   * - JSR352-compliant Batch Application
     - :doc:`../application_framework/application_framework/batch/jsr352/index`

.. [#jaxr_rs_bean_validation_handler_footnote]
  "BeanValidation" refers to :doc:`../application_framework/application_framework/libraries/validation/bean_validation`, a validation feature provided by Nablarch, so it has not been changed to Jakarta Bean Validation.

It should be noted that only the name has changed, there is no feature change.
Also, classes and package names have not been changed to maintain backward compatibility.
