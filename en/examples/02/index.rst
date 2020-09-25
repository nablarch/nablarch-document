=====================================
Extended Validation Functions
=====================================

.. important::

  This sample uses a Nablarch 1.4 compliant API.

  When combining with versions later than Nablarch 1.4 series, customize as necessary.


This section describes the specifications of the validation functions provided in this sample.

For an overview of the validation function and details about the basic validation, refer to the validation description in the Nablarch Application Framework documentation.

`Source code <https://github.com/nablarch/nablarch-biz-sample-all>`_

----------------------------
Delivery package
----------------------------

The functions are provided in the below package.

  *please.change.me.* **core.validation.validator**


.. _ExtendedValidation_mailAddressValidator:

----------------------------
Email address validation
----------------------------
This section describes the validation function for email addresses.

  .. list-table::
   :widths: 100 200
   :header-rows: 1

   * - Validator class name
     - Corresponding annotation
   * - MailAddressValidator
     - @MailAddress

The configuration values that can be set in the validator are as follows.

  .. list-table::
   :widths: 100 200
   :header-rows: 1

   * - property name
     - Settings
   * - messageId (required)
     - Message ID when there is a validation error in the email address

       Example: "{0} is not a valid email address."

.. tip::

  When validation using annotations are not available such as email address input field is divided into local and domain parts, 
  the following utility can be used to perform the email address validation.

      .. class:: VariousValidationUtil
      .. function:: boolean isValidMailAddress

        :param value: Email address to be validated
        :return: True if it is a valid email address

E-mail address validation specification
================================================

Structure of the email address is given below. ::

  "Local Part" @ "Domain Part"

Characters that can be used in email addresses are specified by RFC 5321 and RFC 5322.

However, regarding the local part, email addresses that violate the RFC are also used.

Therefore, if a strict check is performed on the local part, there is a risk that the user cannot register the email address.

Therefore, validation for the local part is only for the number of digits and character type.

The validation specifications for email address are as follows.

* Validation specifications for the entire email address.

  * Required validations are not performed.
  * It must consist of only valid character types for email addresses. Valid character types for email addresses are as follows.

    * UPPER CASE Alphabets:   A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
    * Lowercase alphabets:   a b c d e f g h i j k l m n o p q r s t u v w x y z
    * Numerals:   0 1 2 3 4 5 6 7 8 9
    * Other symbols:   ! # $ % & \ * + - . / = ? @ ^ _ ` { | } ~

  * Only one '@' (an at symbol) must be present.
  * When sending an email with JavaMail, the format check should not result in an error.

  .. tip::
    The invalid ASCII characters for email addresses are as follows.Spaces must also be invalid.  ::

        " ( ) , : ; < > [ \ ]

    These invalid characters can be used by using the notation "quoted-string" defined in RFC 5322. 
    Since these notations are rarely used for email addresses, they are disabled in this function.

* Validation specifications for local part.

  * Email address must not start with '@' (at symbol). (Local part must be present.)
  * The local part must be 64 characters or less.

* Validation specifications for domain part.

  * Email addresses should not end with the '@' (at symbol). (Domain part must be present.)
  * The domain part must be 255 characters or less.
  * The domain part must not end with a '.' (dot).
  * A '.' (dot) must be present in the domain part.
  * Domain part must not begin with a '.' (dot).
  * There must be no consecutive '.' (dots) in the domain part.

  .. tip:: This function only checks the number of digits in the local and domain parts specified in RFC.
    The total number of email addressees that can be registered is usually decided for each project, and is not validated by the function.

.. _ExtendedValidation_japaneseTelNumberValidator:

-------------------------------------------
Validation of Japan telephone numbers
-------------------------------------------
This section describes the validation of Japan telephone numbers There are two ways for allowing the user to enter a Japan telephone number.

* When the phone number is not separated into fields such as area code and is entered as a single string.
* When entering the area code, city code, and subscriber number as separate input items.

Below, the detailed validated methods for both the methods is explained below.


Validation of a single item phone number
================================================

This section describes the validation function when the phone number is not divided into fields such as the area code and is entered as a single string. 
In this case, it is realized by the single item validation function.

  .. list-table::
   :widths: 100 200
   :header-rows: 1

   * - Validator class name
     - Corresponding annotation
   * - JapaneseTelNumberValidator
     - @JapaneseTelNumber

The configuration values that can be set in the validator are as follows.

  .. list-table::
   :widths: 100 200
   :header-rows: 1

   * - property name
     - Settings
   * - messageId (required)
     - Message ID when there is a validation error in the telephone number

       Example: "{0} is not a valid phone number."

Validation specifications
------------------------------------

The validation specifications are as follows.

* Required validations are not performed.
* The beginning must start with a "0".
* It must consist of only hyphens and numbers.
* The digit pattern must be one of the following:

    .. list-table::
     :widths: 100 200
     :header-rows: 1

     * - "Area code digits" - "city code digits" - "subscriber number digits"
       - Example:
     * - "3 digits" - "3 digits" - "4 digits"
       - 012-345-6789
     * - "3 digits" - "4 digits" - "4 digits"
       - 012-3456-7890
     * - "4 digits" - "2 digits" - "4 digits"
       - 0123-45-6789
     * - "5 digits" - "1 digits" - "4 digits"
       - 01234-5-6789
     * - "2 digits" - "4 digits" - "4 digits"
       - 01-2345-6789
     * - "11 digits"
       - 01234567890
     * - "10 digits"
       - 0123456789


Validation of a multiple item telephone number
=================================================

Explain the validation function when entering the area code, city code, and subscriber number as separate input items. 
In this case, Nablarch offers the following validation utilities:

  .. class:: VariousValidationUtil
  .. function:: boolean isValidJapaneseTelNum

   :param areaCode: Area code
   :param cityCode: City code
   :param subscriberNumber: Subscriber number
   :return: True if it is a valid Japanese telephone number


Validation specifications
---------------------------------

The validation specifications are as follows.

* Do not check if all items have been filled in.
* The beginning must start with a "0".
* It must consist of only hyphens and numbers.
* The digit pattern must be one of the following:

    .. list-table::
     :widths: 100 200
     :header-rows: 1

     * - "Area code digits" - "city code digits" - "subscriber number digits"
       - Example:
     * - "3 digits" - "3 digits" - "4 digits"
       - 012-345-6789
     * - "3 digits" - "4 digits" - "4 digits"
       - 012-3456-7890
     * - "4 digits" - "2 digits" - "4 digits"
       - 0123-45-6789
     * - "5 digits" - "1 digits" - "4 digits"
       - 01234-5-6789
     * - "2 digits" - "4 digits" - "4 digits"
       - 01-2345-6789

  .. important::

    If all the arguments are null or empty strings, true is returned. 
    If a case where all three items (area code, city code, and subscriber number) have not been entered is not permitted, then validation is required to be performed at the caller of this validation process. (refer to :ref:`telNum_fields_code` given below.)

.. _telNum_fields_code:

Implementation examples
--------------------------

  .. code-block:: java

    @ValidateFor("registerCompany")
    public static void validateForRegisterCompany(
                          ValidationContext<CompanyEntity> context) {
        // Single item validation
        ValidationUtil.validateWithout(context, REGISTER_COMPANY_SKIP_PROPS);
        if (!context.isValid()) {
            return;
        }

        // Validation between items
        CompanyEntity companyEntity = context.createObject();
        // Check if all items are input
        // This check should be done when necessary.
        if (StringUtil.isNullOrEmpty(companyEntity.getAreaCode,
                                     companyEntity.getCityCode,
                                     companyEntity.getSubscriberNumber)) {
            // Add message to context
            // Omitted
        }
        // Telephone number validation
        if (!VariousValidationUtil.isValidJapaneseTelNum(
                                     companyEntity.getAreaCode,
                                     companyEntity.getCityCode,
                                     companyEntity.getSubscriberNumber)) {
            // Add message to context
            // Omitted
        }

----------------------------
Code value validation
----------------------------
Code value validation is expected to specify different patterns from multiple functions for validation. 
For this reason, this sample provides a utility to perform code value validation by specifying a pattern.

.. tip::

  For more information on code value validation, refer to the Code Management chapter of the Nablarch Application Framework Description.

Methods provided by the utility
========================================
Provides the following 2 methods:

  .. function:: void validate()

   :param context: Validation context
   :param codeId: Code ID
   :param pattern: Pattern
   :param propertyName: Property to be validated

  .. function:: void validate()

   :param context: Validation context
   :param codeId: Code ID
   :param pattern: Pattern
   :param propertyName: Property to be validated
   :param messageId: Message ID (overrides the default message ID with the specified message ID)



Usage example of utility
===========================
An usage example of utility is shown below.

.. code-block:: java

    
    // [Description] Perform code value validation using CodeValidationUtil#validate method.
    CodeValidationUtil.validate(context, "0001", "PATTERN1", "gender");

    // [Description] To overwrite the message ID, specify the message ID in argument 5.
    CodeValidationUtil.validate(context, "0001", "PATTERN1", "gender", "message_id");
  
