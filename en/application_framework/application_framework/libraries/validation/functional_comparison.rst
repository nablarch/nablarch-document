.. _`validation-functional_comparison`:

Comparison of Function between Bean Validation and Nablarch Validation
----------------------------------------------------------------------------------------------------
This section compares the validation capabilities of Nablarch with those of |jsr349| (external site).

.. list-table:: Function comparison (A: Provided; B: Partially provided; C: Not provided; D: Not applicable)
  :header-rows: 1
  :class: something-special-class

  * - Function
    - Bean |br| Validation
    - Nablarch |br| Validation
    - Jakarta |br| Bean Validation
  * - Items to be validated can be specified
    - A [#property_validation]_
    - A |br| :ref:`To the manual <nablarch_validation-execute>`
    - A
  * - Validation can be performed  |br| for Java Beans objects |br| that have a hierarchical structure
    - A [#jsr]_
    - A |br| :ref:`To the manual <nablarch_validation-nest_bean>`
    - A
  * - Validation can be performed  |br| for method arguments and return values
    - C [#method]_
    - C [#method]_
    - A
  * - Can perform correlation validation
    - A |br| :ref:`To the manual <bean_validation-correlation_validation>`
    - A |br| :ref:`To the manual <nablarch_validation-correlation_validation>`
    - A
  * - Execution order of validation can be specified
    - C [#order]_
    - A |br| :ref:`To the manual <nablarch_validation-execute>`
    - A
  * - Validation items can be switched based |br| on the value of a specific item
    - A [#conditional]_
    - A |br| :ref:`To the manual <nablarch_validation-conditional>`
    - A
  * - Embedded parameters can be used |br| in error messages
    - A [#parameter]_ |br| :ref:`To the manual <message>`
    - A |br| :ref:`To the manual <message>`
    - A
  * - Can validate domains
    - A |br| :ref:`To the manual <bean_validation-domain_validation>`
    - A |br| :ref:`To the manual <nablarch_validation-domain_validation>`
    - C
  * - Can convert value types
    - C [#type_converter]_
    - A |br| :ref:`To the manual <nablarch_validation-definition_validator_convertor>`
    - C
  * - Can normalize values
    - C [#normalized]_
    - A |br| :ref:`To the manual <nablarch_validation-definition_validator_convertor>`
    - C
  * - Can embed item names in error messages
    - A |br| :ref:`To the manual <bean_validation-property_name>`
    - A |br| :ref:`To the manual <nablarch_validation-property_name>`
    - C


.. [#property_validation] By validating all the items of the form, receipt of invalid input values can be prevented. Therefore, using Bean Validation for executing the validation of item specification is not recommended. If validation of only specified items is required, use :java:extdoc:`ValidatorUtil#validate <nablarch.core.validation.ee.ValidatorUtil.validate(java.lang.Object-java.lang.String...)>` .

.. [#jsr] The response method conforms to the specifications of |jsr349| .
.. [#method] Since Nablarch always performs validation at the timing when data is received from the outside, validation for method arguments and return values is not supported.
.. [#order] Since the execution order of validation cannot be controlled, implementation requiring expected execution order of validation should not be performed. For example, correlation validation should not be expected to be performed after item-by-item validation.
.. [#conditional]  Use the class-level validation function of |jsr349| to switch validation items by logic.
.. [#parameter] EL expression can be used to embed parameters in Bean Validation.
.. [#type_converter] Since all property types are defined as string (:ref:`Reason to define as a string <bean_validation-form_property>`)in Bean Validation, type conversion is not performed. If type conversion is required after validation, change the type using :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>`.
.. [#normalized] Normalization is provided as a handler instead of a Bean Validation function. If normalization is needed, use :ref:`normalize_handler` .

.. |jsr349| raw:: html

   <a href="https://jakarta.ee/specifications/bean-validation/" target="_blank">Jakarta Bean Validation(external site)</a>

.. |br| raw:: html

   <br />
