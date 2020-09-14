.. _nablarch_validation:

Nablarch Validation
==================================================

.. contents:: Table of contents
  :depth: 3
  :local:

This chapter explains the validation function originally implemented by Nablarch.

.. tip::

  As described in :ref:`validation`, it is recommended to use :doc:`bean_validation`.

Function overview
--------------------------------------------------

Can Perform Validation and Type Conversion and Normalization of Values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Nablarch validation can perform validation, and type conversion and normalization of input values.

Since it can perform type conversion, the input values can be directly mapped to the numeric type (Integer or Long) of the Bean class.
In addition, editing cancellation (normalization) of edited values can also be performed during type conversion.

For details, see :ref:`nablarch_validation-definition_validator_convertor`.

Can validate domains
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Validation rules can be defined for each domain.

When using domain validation, it is only necessary to specify the domain name in the Bean class setter, which makes changing the validation rules easy.

For details, see `Use domain validation`_.


.. _nablarch_validation-validator_convertor:

Commonly Used Validators and Convertors are Provided
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Nablarch provides commonly used validators and convertors as standard.
For this reason, validation can be executed in the project only using :ref:`nablarch_validation-definition_validator_convertor`.

See the following links for validators and convertors provided by Nablarch.

* :java:extdoc:`nablarch.core.validation.validator`
* :java:extdoc:`nablarch.core.validation.convertor`
* :java:extdoc:`nablarch.common.date`
* :java:extdoc:`nablarch.common.code.validator`


.. _nablarch_validation-module_list:

Module list
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-validation</artifactId>
  </dependency>

  <!-- Only when date validator and converter are used -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-date</artifactId>
  </dependency>

  <!-- Only when code value validator and converter are used -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-code</artifactId>
  </dependency>

How to use
--------------------------------------------------

.. _nablarch_validation-definition_validator_convertor:

Configuring Validators and Convertors for Use
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To enable validation, it is essential to register the validators and convertors being used in the component configuration file.

For the validators and convertors provided by Nablarch, see :ref:`nablarch_validation-validator_convertor`.

.. important::

  If the validators and convertors are not configured, the validation function cannot be used.

Configuration example
  * Define :java:extdoc:`ValidationManager <nablarch.core.validation.ValidationManager>` as a component named **validationManager**.
  * List the converters used for :java:extdoc:`ValidationManager#convertors <nablarch.core.validation.ValidationManager.setConvertors(java.util.List)>`.
  * List the validators used for :java:extdoc:`ValidationManager#validators <nablarch.core.validation.ValidationManager.setValidators(java.util.List)>`.

  .. code-block:: xml

    <component name="validationManager" class="nablarch.core.validation.ValidationManager">
      <property name="convertors">
        <list>
          <!-- List the convertors used here -->
        </list>
      </property>
      <property name="validators">
        <list>
          <!-- List the validators used here-->
        </list>
      </property>

      <!--
      Other attributes omitted
      For details, see Javadoc of ValidationManager
       -->
    </component>

Configure validation rules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Configure the annotations of validation rules in the properties (setter) of Bean class for validation.
Also, note that annotations cannot be specified for a getter.(It is meaningless even if specified.)

.. tip::

  If annotations are configured individually, errors during implementation and maintenance costs will increase.
  Hence, it is recommended to use the :ref:`domain validation <nablarch_validation-domain_validation>` described below.

Implementation examples
  Configure annotations by referring to the :ref:`validators and convertors provided by Nablarch<nablarch_validation-validator_convertor>`.

  In this example, inputting the `userName` is required, and a maximum of 10 full-width characters are permitted.
  For `birthday`, 8 half-width digits are permitted.
  For `age`, up to 3 integer digits are permitted.

  .. code-block:: java

    public class SampleForm {

      @Length(max = 10)
      @SystemChar(charsetDef = "Full-width character")
      @Required
      public void setUserName(String userName) {
          this.userName = userName;
      }

      @Length(min = 8, max = 8)
      @SystemChar(charsetDef = "Half-width character")
      public void setBirthday(String birthday) {
          this.birthday = birthday;
      }

      @Digits(integer = 3)
      public void setAge(Integer age) {
          this.age = age;
      }
    }

.. _nablarch_validation-domain_validation:

Use domain validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Show the configuration and implementation examples to use domain validation.

Creating Enum that defines the validation rules for each domain
  To use domain validation, first create an Enum (domain Enum) with validation rules for each domain.
  This Enum must implement the `DomainDefinition` interface.

  Each enumerator of the Enum will become a domain name. In the following example, two domains, ``NAME`` and ``DATE`` have been defined.

  .. code-block:: java

    public enum SampleDomain implements DomainDefinition {

        @Length(max = 10)
        @SystemChar(charsetDef = "Full-width character")
        NAME,

        @Length(min = 8, max = 8)
        @SystemChar(charsetDef = "Half-width character")
        DATE;

        // Implementation of the method defined in the interface
        // Implementation contents should be exactly the same as this example
        @Override
        public Annotation getConvertorAnnotation() {
            return DomainValidationHelper.getConvertorAnnotation(this);
        }

        @Override
        public List<Annotation> getValidatorAnnotations() {
            return DomainValidationHelper.getValidatorAnnotations(this);
        }
    }

Creating an annotation that represents a domain
  Create an annotation that represents the domain.
  The domain Enum created above can be specified in the `value` attribute.

  .. code-block:: java

    @ConversionFormat
    @Validation
    @Target(ElementType.METHOD)
    @Retention(RetentionPolicy.RUNTIME)
    public @interface Domain {
        SampleDomain value();
    }

Configure Domain in the Bean for Validation
  Domain validation is performed by setting the annotations representing the domain created above.

  In this example, the validation configured in `SampleDomain.NAME` is executed for `userName`.
  ※When a convertor is configured, the value is also converted by the convertor.

  .. code-block:: java

    @Domain(SampleDomain.NAME)
    public void setUserName(String userName) {
        this.userName = userName;
    }

Configuration to enable domain validation
  The following configurations are required to enable domain validation.

  * Configuration of :java:extdoc:`DomainValidationHelper <nablarch.core.validation.domain.DomainValidationHelper>`
  * Configuration of :java:extdoc:`DomainValidator <nablarch.core.validation.domain.DomainValidator>`
  * Configuration of :java:extdoc:`ValidationManager <nablarch.core.validation.ValidationManager>`
  * Configuration of initialization component

  An example is shown below.

  Configuration of :java:extdoc:`DomainValidationHelper <nablarch.core.validation.domain.DomainValidationHelper>`
    * Configure the fully qualified class name (FQCN) of the annotations representing the domain to
      :java:extdoc:`domainAnnotation property <nablarch.core.validation.domain.DomainValidationHelper.setDomainAnnotation(java.lang.String)>`.

    .. code-block:: xml

      <component name="domainValidationHelper"
          class="nablarch.core.validation.domain.DomainValidationHelper">

        <property name="domainAnnotation" value="sample.Domain" />

      </component>

  Configuration of :java:extdoc:`DomainValidator <nablarch.core.validation.domain.DomainValidator>`
    * Configure :java:extdoc:`DomainValidationHelper <nablarch.core.validation.domain.DomainValidationHelper>` that has been configured above
      to :java:extdoc:`domainValidationHelper property <nablarch.core.validation.domain.DomainValidator.setDomainValidationHelper(nablarch.core.validation.domain.DomainValidationHelper)>`.
    * Configure the validators list to
      :java:extdoc:`validators property <nablarch.core.validation.domain.DomainValidator.setValidators(java.util.List)>`.

    .. code-block:: xml

      <component name="domainValidator"
          class="nablarch.core.validation.domain.DomainValidator">

        <!--
          DomainValidator should not be configured here. If configured, it will become a circular reference,
          and an error occurs during system repository initialization.
        -->
        <property name="validators">
          <list>
            <component-ref name="requiredValidator" />
          </list>
        </property>
        <property name="domainValidationHelper" ref="domainValidationHelper" />
      </component>


  Configuration of :java:extdoc:`ValidationManager <nablarch.core.validation.ValidationManager>`
    * Configure :java:extdoc:`DomainValidationHelper <nablarch.core.validation.domain.DomainValidationHelper>` that has been configured above
      to :java:extdoc:`domainValidationHelper property <nablarch.core.validation.ValidationManager.setDomainValidationHelper(nablarch.core.validation.domain.DomainValidationHelper)>`.
    * Configure the validators list (without missing out :java:extdoc:`DomainValidator <nablarch.core.validation.domain.DomainValidator>` that has been configured above)
      to :java:extdoc:`validators property <nablarch.core.validation.ValidationManager.setValidators(java.util.List)>`.


    .. code-block:: xml

      <component name="validationManager" class="nablarch.core.validation.ValidationManager">
        <property name="validators">
          <list>
            <component-ref name="domainValidator" />
            <!-- Description of other validators is omitted -->
          </list>
        </property>
        <property name="domainValidationHelper" ref="domainValidationHelper" />
      </component>

  Configuration of initialization component
    Configure :java:extdoc:`DomainValidator <nablarch.core.validation.domain.DomainValidator>`
    and :java:extdoc:`ValidationManager <nablarch.core.validation.ValidationManager>` that have been configured above to the initialization list.

    .. code-block:: xml

      <component name="initializer"
          class="nablarch.core.repository.initialization.BasicApplicationInitializer">

        <property name="initializeList">
          <list>
            <component-ref name="validationManager" />
            <component-ref name="domainValidator" />
          </list>
        </property>
      </component>

Behavior when Multiple Validation Rules are Configured for Domain Validation
  If multiple errors are found in one input item in the domain validation, terminate scrutiny at the first error.

  .. code-block:: java

        public enum SampleDomain implements DomainDefinition {
          @Length(max = 10)
          @SystemChar(charsetDef = "Full-width character")
          NAME;
       }

  The `NAME` mentioned above does not perform `SystemChar` validation when a `Length` validation error occurs.

Inheriting the Bean for Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The Bean for validation can be inherited, but inheritance is not recommended for the following reasons.

When inheritance is performed easily, unexpected validation will be executed due to a change in the parent class,
and annotation configuration must be performed while being aware of complex validation overwrite rules, which causes errors (bugs).

The following actions take place when Bean is inherited:

* When only :java:extdoc:`@PropertyName <nablarch.core.validation.PropertyName>` is added in the subclass, the validators and convertors of the parent class are used.
* If even one validator annotation is added in the subclass,
  the validator annotation of the parent class is ignored and validators of the subclass will be used. The convertors of the parent class will be used.
* If even one convertor annotation is added in the subclass,
  the convertor annotation of the parent class is ignored and convertors of the subclass will be used. The validators of the parent class will be used.
* If both the validators and the convertors are configured in the subclass, all configurations of the subclass will be used.
* The configurations of convertors in the parent class cannot be deleted in the subclass.


In the case of the following parent-child Bean, the validation of :java:extdoc:`@Digits <nablarch.core.validation.convertor.Digits>`
and :java:extdoc:`@NumberRange <nablarch.core.validation.validator.NumberRange>` is executed for the value property of ChildForm.

.. code-block:: java

  // Parent Form
  public class ParentForm {
    @Digits(integer=5, fraction=3)
    public void setValue(BigDecimal value) {
        this.value = value;
    }
  }

  // Child Form
  public class ChildForm extends ParentForm {
    @Override
    @NumberRange(min=100.0, max=20000.0)
    public void setValue(BigDecimal value) {
        super.setBdValue(value);
    }
  }

.. _nablarch_validation-execute:

Executing Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Validation can be executed by calling the method provided by :java:extdoc:`ValidationUtil <nablarch.core.validation.ValidationUtil>`.

Implementation examples
  First, implement a constructor that takes Map as an argument in the Bean for validation to generate a Bean object from the input value.

  Next, implement a static method for performing validation in the Bean for validation.
  In this method, configure the :java:extdoc:`@ValidateFor <nablarch.core.validation.ValidateFor>` annotation, and specify an arbitrary value for identifying validation in the argument.

  The validation is executed using :java:extdoc:`ValidationUtil <nablarch.core.validation.ValidationUtil>` for the processing required for this method.

  .. code-block:: java

    public class SampleForm {

      public SampleForm(Map<String, Object> params) {
          userName = (String) params.get("userName");
          birthDay = (String) params.get("birthDay");
          age = (Integer) params.get("age");
      }

      @Domain(SampleDomain.NAME)
      @Required
      public void setUserName(String userName) {
          this.userName = userName;
      }

      @Domain(SampleDomain.DATE)
      public void setBirthday(String birthday) {
          this.birthday = birthday;
      }

      @Domain(SampleDomain.AGE)
      public void setAge(Integer age) {
          this.age = age;
      }

      @ValidateFor("validate")
      public static void validate(ValidationContext<SampleForm> context) {
        // Validate userName, birthday and age
        ValidationUtil.validate(context, new String[] {"userName", "birthday", "age"});
      }
    }

  To validate an input value request using the Bean described above, use :java:extdoc:`ValidationUtil <nablarch.core.validation.ValidationUtil>` as follows:
  In the case of a web application, validation can be performed more easily by `Checking User Input Values for Web Applications`_.

  .. code-block:: java

    // Execution of validation
    // Checks the input parameter request using SampleForm.
    //
    // Specifies which validation method of SampleForm is used for validation in the last argument.
    // Since validate is specified in this example,
    // validation is executed using the validate method specified in the @ValidateFor annotation of SampleForm.
    ValidationContext<SampleForm> validationContext =
            ValidationUtil.validateAndConvertRequest(SampleForm.class, request, "validate");

    // If a validation error has occurred, an Exception is thrown with abortIfInvalid
    validationContext.abortIfInvalid();

    // Generates Form using a constructor that takes Map as an argument.
    // (Form in which the input value request is converted can be acquired)
    SampleForm form = validationContext.createObject();

.. _nablarch_validation-execute_explicitly:

Performing Explicit Execution of Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The `Executing Validation`_ was performed based on the annotations configured in Bean property (setter), but here,
we will describe a method of executing the validation directly instead of configuring the annotations.

In principle, validation is performed using the `Executing Validation`_ method, use this method
if it is necessary to perform validation individually.
For example, if :ref:`code management pattern<code-use_pattern>` is being used
and validate is required to be performed by changing the pattern only for a specific screen, then execute validation individually.


Implementation examples
  Explicit validation is executed from the method in which the :java:extdoc:`@ValidateFor <nablarch.core.validation.ValidateFor>` annotation for the Bean class is configured.
  Annotations that can be specified when executing explicit validation are limited to those that implement :java:extdoc:`DirectCallableValidator <nablarch.core.validation.DirectCallableValidator>`.
  (Convertors cannot be specified.)

  .. code-block:: java

    public class SampleForm {
      // Attributes omitted

      @ValidateFor("validate")
      public static void validate(ValidationContext<SampleForm> context) {

          ValidationUtil.validate(context, new String[]{"userName", "prefectureCode"});

          // Perform required check on the userName
          ValidationUtil.validate(context, "userName", Required.class);

          //  Specify annotation parameters in Map
          Map<String, Object> params = new HashMap<String, Object>();
          params.put("codeId", "1052");     // Code ID
          params.put("pattern", "A");       // Code pattern name that is used
          params.put("messageId", "M4865"); // Error message ID
          ValidationUtil.validate(context, "prefectureCode", CodeValue.class, params);
      }
    }

  .. important::

    To perform explicit validation, it is essential to implement validation on the target items in advance.
    For details, see :ref:`nablarch_validation-execute`.

.. _nablarch_validation-system_char_validator:

Performing Character Type Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The definition method for character type validation is the same as :ref:`bean_validation`.
For the detailed configuration method, see :ref:`performing character type validation for Bean Validation <bean_validation-system_char_validator>`.
However, see the following since the configuration that allows surrogate pairs is different from :ref:`bean_validation`.

Note that the annotation being used is :java:extdoc:`@SystemChar <nablarch.core.validation.validator.unicode.SystemChar>`,
and the fully qualified name is different from :ref:`bean_validation` (annotation name is the same).

Allowing Surrogate Pairs
  This validation does not allow surrogate pairs by default.
  (They are not allowed even if the characters for surrogate pairs are explicitly defined in `LiteralCharsetDef`.)

  To allow surrogate pairs, :java:extdoc:`SystemCharValidator#allowSurrogatePair <nablarch.core.validation.validator.unicode.SystemCharValidator.setAllowSurrogatePair(boolean)>` must be configured in the component configuration file as follows.

  .. code-block:: xml

    <component name="systemCharValidator" class="nablarch.core.validation.validator.unicode.SystemCharValidator">
      <!--  Allows surrogate pairs -->
      <property name="allowSurrogatePair" value="true"/>

      <!-- Other properties are omitted -->
    </component>

.. _nablarch_validation-correlation_validation:

Performing Correlation Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Correlation validation using multiple items is implemented using the method in which the Bean class annotation :java:extdoc:`@ValidateFor <nablarch.core.validation.ValidateFor>` is configured.
This method first performs validation for each item, then executes validation using multiple items if no error occurs.

Implementation examples
  In this example, correlation validation is performed using mailAddress and confirmMailAddress.

  If an error has occurred during correlation validation, explicitly add the message ID indicating the message that must be notified to the user to :java:extdoc:`ValidationContext <nablarch.core.validation.ValidationContext>`.

  .. code-block:: java

    public class SampleForm {

      @Domain(SampleDomain.MAIL)
      @Required
      public void setMailAddress(String mailAddress) {
          this.mailAddress = mailAddress;
      }

      @Domain(SampleDomain.MAIL)
      @Required
      public void setConfirmMailAddress(String confirmMailAddress) {
          this.confirmMailAddress = confirmMailAddress;
      }

      @ValidateFor("validate")
      public static void validate(ValidationContext<SampleForm> context) {
          // Implement validation of mailAddress and confirmMailAddress
          ValidationUtil.validate(context, new String[] {"mailAddress", "confirmMailAddress"});

          // Correlation not performed validation if an error has occurred
          if (!context.isValid()) {
              return;
          }

          // Generate form object and implement correlation validation
          SampleForm form = context.createObject();
          if (!Objects.equals(form.mailAddress, form.confirmMailAddress)) {
              // An error occurs when mailAddress and confirmMailAddress do not match
              context.addMessage("compareMailAddress");
          }
      }
    }

.. _nablarch_validation-nest_bean:

Performing validation using a function that takes Bean array as the input, such as batch registration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
There are cases where the same information is input multiple times, such as in batch registration.
In such cases, a nested Bean is defined for the Bean for validation.

Configure the :java:extdoc:`@ValidationTarget <nablarch.core.validation.ValidationTarget>` annotation in the nested Bean setter, and specify the size of the nested Bean.
If the number of elements is fixed (determined during compile), specify it in the :java:extdoc:`size <nablarch.core.validation.ValidationTarget.size()>` attribute.
If the number of elements is variable, configure the property name having a size in the :java:extdoc:`sizeKey <nablarch.core.validation.ValidationTarget.sizeKey()>` attribute.

In this example, `SampleForm` stores `AddressForm` as an array since the `AddressForm` information can be inputted in a batch.
Also, :java:extdoc:`sizeKey <nablarch.core.validation.ValidationTarget.sizeKey()>` is used since the size is not determined during compile.

.. code-block:: java

  public class SampleForm {
      private AddressForm[] addressForms;
      // Size of addressForms
      // Send confidential items from the screen, etc.
      private Integer addressSize;

      @ValidationTarget(sizeKey = "addressSize")
      public void setAddressForms(AddressForm[] addressForms) {
          this.addressForms = addressForms;
      }

      @Domain(SampleDomain.SIZE)
      @Required
      public void setAddressSize(Integer addressSize) {
          this.addressSize = addressSize;
      }

      @ValidateFor("validate")
      public static void validate(ValidationContext<SampleForm> context) {
          ValidationUtil.validate(context, new String[] {"addressSize", "addressForms"});
      }
  }

  public class AddressForm {
      // Omitted
  }

.. _nablarch_validation-conditional:

Changing validation items based on the selected value of the radio button and list box
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
By using the :java:extdoc:`WebUtil <nablarch.common.web.WebUtil>` class, validation items can be replaced based on the selected value of the radio button and list box.

In this example, when the value of **form.radio** sent from the screen is **ptn1**, only `item1` is validated.
For values other than **ptn1**, `item1` and `item2` are validated.

.. code-block:: java

  public class SampleForm {

      // Property is omitted

      @ValidateFor("validate")
      public static void validate(ValidationContext<SampleForm> context) {
          if (WebUtil.containsPropertyKeyValue(context, "form.radio", "ptn1")) {
              ValidationUtil.validate(context, new String[] {"item1"});
          } else {
              ValidationUtil.validate(context, new String[] {"item1", "item2"});
          }
      }
  }

.. tip::

  In this example, :java:extdoc:`WebUtil.containsPropertyKeyValue <nablarch.common.web.WebUtil.containsPropertyKeyValue(nablarch.core.validation.ValidationContext-java.lang.String-java.lang.String)>` is used to check even the sent value,
  but to just examine whether the radio button is checked, use :java:extdoc:`WebUtil.containsPropertyKey <nablarch.common.web.WebUtil.containsPropertyKey(nablarch.core.validation.ValidationContext-java.lang.String)>`.

To create a validation error message linked to a specific item
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
See :ref:`to create a validation error message linked to a specific item of Bean Validation <bean_validation-create_message_for_property>`.

.. _nablarch_validation-property_name:

To embed the item name in the message when a validation error occurs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To embed the item name in the message, specify the item name of the item for validation using the :java:extdoc:`@PropertyName <nablarch.core.validation.PropertyName>` annotation.

Implementation examples
  Use a pattern character to embed the item name in the message.
  Since the item name is always specified first, specify **{0}** where the item name is to be embedded.

  .. code-block:: properties

    required.message = Please enter a {0}.

  Configure the annotation `@PropertyName` that sets the item name along with the validation annotation in the item for validation.

  .. code-block:: java

    public class SampleForm {

        @Domain(SampleDomain.NAME)
        @Required
        @PropertyName("name")
        public void setUserName(String userName) {
            this.userName = userName;
        }

        @Domain(SampleDomain.DATE)
        @PropertyName("birthday")
        public void setBirthday(String birthday) {
            this.birthday = birthday;
        }
    }

Generated Message
  In the above implementation, if a required error occurs in the `username` property, the message generated will be **"Please enter name"**.

Performing Type Conversion to Numeric Type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To convert the input value to a numeric type of the Bean class after validation, that item shall always require the :java:extdoc:`@Digits <nablarch.core.validation.convertor.Digits>` annotation.
※In the case of domain validation, the configuration for domain Enum is required.

Let us assume that the convertors for converting to a numeric type are configured according to the procedure in :ref:`nablarch_validation-definition_validator_convertor`.

Implementation examples
  In this example, it has been specified in setter, but we recommend specifying it in the domain Enum using domain validation.

  .. code-block:: java

    public class SampleForm {

        @PropertyName("age")
        @Digits(integer = 3)
        public void setAge(Integer age) {
            this.age = age;
        }
    }

.. _nablarch_validation-database:

Performing Correlation Validation with the Database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Correlation validation with the database is performed by business action.

See :ref:`validation correlation with the Bean validation database <bean_validation-database_validation>` for the reason why it is performed with business action.

Checking User Input Values for Web Applications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The user input values for web applications are checked using :ref:`inject_form_interceptor`.
For details, see :ref:`inject_form_interceptor`.

Expansion example
--------------------------------------------------
To add a project-specific validator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following steps are required to add a validator.

#. Creating an annotation
#. Creating a validator
#. Registering the validator in a configuration file

The procedure is shown below.

Creating an annotation
  Annotations must satisfy the following conditions.

  * Configure the :java:extdoc:`@Validation <nablarch.core.validation.Validation>` annotation.
  * Configure `ElementType.METHOD` with the :java:extdoc:`@Target <java.lang.annotation.Target>` annotation.
  * Configure `RetentionPolicy.RUNTIME` with the :java:extdoc:`@Retention <java.lang.annotation.Retention>` annotation.

  .. code-block:: java

    @Validation
    @Target(ElementType.METHOD)
    @Retention(RetentionPolicy.RUNTIME)
    public @interface Sample {
    }

Creating a validator
  The validator implements the :java:extdoc:`Validator <nablarch.core.validation.Validator>` interface and implements the validation logic.

  .. code-block:: java

    public class SampleValidator implements Validator {

      public Class<? extends Annotation> getAnnotationClass() {
          return Sample.class;
      }

      public <T> boolean validate(ValidationContext<T> context,
          // Omitted
      }
    }

Registering the validator in a configuration file
   See :ref:`nablarch_validation-definition_validator_convertor`.

To add a project-specific convertor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following steps are required to add a convertor.

#. Creating a convertor
#. Registering the converter in a configuration file

The procedure is shown below.

Creating a convertor
  The converter implements the :java:extdoc:`Convertor <nablarch.core.validation.Convertor>` interface and implements the type conversion logic, etc.

  .. code-block:: java

    public class SampleConvertor implements Convertor {

        @Override
        public Class<?> getTargetClass() {
            return Short.class;
        }

        @Override
        public <T> boolean isConvertible(ValidationContext<T> context, String propertyName, Object propertyDisplayName,
                Object value, Annotation format) {

            boolean convertible = true;

            if (value instanceof String) {
                try {
                    Short.valueOf((String) value);
                } catch (NumberFormatException e) {
                    convertible = false;
                }
            } else {
                convertible = false;
            }

            if (!convertible) {
                context.addResultMessage(propertyName, "sampleconvertor.message", propertyDisplayName);
            }
            return convertible;
        }

        @Override
        public <T> Object convert(ValidationContext<T> context, String propertyName, Object value, Annotation format) {
            return Short.valueOf((String) value);
        }
    }

Registering the converter in a configuration file
  See :ref:`nablarch_validation-definition_validator_convertor`.

To change the method of generating a Bean object for validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following steps are required to change the method of generating a Bean object for validation.

#. Create the implementation class :java:extdoc:`FormCreator <nablarch.core.validation.FormCreator>`
#. Add the component definition of the created class to :java:extdoc:`ValidationManager.formCreator <nablarch.core.validation.ValidationManager.setFormCreator(nablarch.core.validation.FormCreator)>`
