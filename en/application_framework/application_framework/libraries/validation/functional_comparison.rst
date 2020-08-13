.. _`validation-functional_comparison`:

Comparison of Function between Bean Validation and Nablarch Validation
----------------------------------------------------------------------------------------------------
This section describes the functional comparison with the validation function provided by Nablarch.

.. list-table:: Function comparison (✓: Provided; △: Partially provided; ×: Not provided; -: Not applicable)
  :header-rows: 1
  :class: something-special-class

  * - Function
    - Bean |br| Validation
    - Nablarch |br| Validation
    - JSR 349
  * - Items to be validated can be specified
    - ✓ [#property_validation]_
    - ✓ |br| :ref:`To the manual <nablarch_validation-execute>`
    - ✓
  * - Validation can be performed  |br| for Java Beans objects |br| that have a hierarchical structure
    - ✓ [#jsr]_
    - ✓ |br| :ref:`To the manual <nablarch_validation-nest_bean>`
    - ✓
  * - Validation can be performed  |br| for method arguments and return values
    - × [#method]_
    - × [#method]_
    - ✓
  * - Can perform correlation validation
    - ✓ |br| :ref:`To the manual <bean_validation-correlation_validation>`
    - ✓ |br| :ref:`To the manual <nablarch_validation-correlation_validation>`
    - ✓
  * - Execution order of validation can be specified
    - × [#order]_
    - ✓ |br| :ref:`To the manual <nablarch_validation-execute>`
    - ✓
  * - Validation items can be switched based |br| on the value of a specific item
    - ✓ [#conditional]_
    - ✓ |br| :ref:`To the manual <nablarch_validation-conditional>`
    - ✓
  * - Embedded parameters can be used |br| in error messages
    - ✓ [#parameter]_ |br| :ref:`To the manual <message>`
    - ✓ |br| :ref:`To the manual <message>`
    - ✓
  * - Can validate domains
    - ✓ |br| :ref:`To the manual <bean_validation-domain_validation>`
    - ✓ |br| :ref:`To the manual <nablarch_validation-domain_validation>`
    - ×
  * - Can convert value types
    - × [#type_converter]_
    - ✓ |br| :ref:`To the manual <nablarch_validation-definition_validator_convertor>`
    - ×
  * - Can normalize values
    - × [#normalized]_
    - ✓ |br| :ref:`To the manual <nablarch_validation-definition_validator_convertor>`
    - ×
  * - Can embed item names in error messages
    - ✓ |br| :ref:`To the manual <bean_validation-property_name>`
    - ✓ |br| :ref:`To the manual <nablarch_validation-property_name>`
    - ×


.. [#property_validation] By validating all the items of the form, receipt of invalid input values can be prevented. Therefore, using Bean Validation for executing the validation of item specification is not recommended. If validation of only specified items is required, use :java:extdoc:`ValidatorUtil#validate <nablarch.core.validation.ee.ValidatorUtil.validate(java.lang.Object-java.lang.String...)>` .

.. [#jsr] The response method conforms to the specifications of |jsr349| .
.. [#method] Since Nablarch always performs validation at the timing when data is received from the outside, validation for method arguments and return values is not supported.
.. [#order] Since the execution order of validation cannot be controlled, implementation requiring expected execution order of validation should not be performed. For example, correlation validation should not be expected to be performed after item-by-item validation.
.. [#conditional]  Use the class-level validation function of |jsr349| to switch validation items by logic.
.. [#parameter] EL expression can be used to embed parameters in Bean Validation.
.. [#type_converter] Since all property types are defined as string (:ref:`Reason to define as a string <bean_validation-form_property>`)in Bean Validation, type conversion is not performed. If type conversion is required after validation, change the type using :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>`.
.. [#normalized] Normalization is provided as a handler instead of a Bean Validation function. If normalization is needed, use :ref:`normalize_handler` .

.. |jsr349| raw:: html

   <a href="https://jcp.org/en/jsr/detail?id=349" target="_blank">JSR349(external site, English)</a>

.. |br| raw:: html

   <br />
