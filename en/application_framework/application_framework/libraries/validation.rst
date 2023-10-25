.. _validation:

Input Value Check
==================================================
Provides a function to verify whether the user input value sent from the client or the value sent by an external system through an inter-system link is appropriate.

Input value check performs the following.

* Checks if the input value is a valid format (for example, checks the number of digits and character type)
* Checks if the input value matches the system status (for example, check of duplicate account registration)

For the method of defining the message displayed when an error occurs during input value check, see :doc:`message`.

Nablarch offers two types of validation functions:

.. toctree::
  :maxdepth: 1

  Validation function compliant with Jakarta Bean Validation of Jakarta EE (Bean Validation) <validation/bean_validation>
  Nablarch independent validation function (Nablarch Validation) <validation/nablarch_validation>

Input value can be checked by using any one of the functions, but it is recommended to use the Jakarta EE-compliant function for the following reasons.

* Jakarta Bean Validation is specified in Jakarta EE and extensive information is available.
* Developers do not have to learn how to use the independent validation of Nablarch.

.. tip::
 Refer to :ref:`validation-functional_comparison` for the difference between the functions provided by :ref:`bean_validation` and :ref:`nablarch_validation`.

.. toctree::
  :hidden:

  validation/functional_comparison
