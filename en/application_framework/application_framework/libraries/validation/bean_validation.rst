.. _bean_validation:

Bean Validation
==================================================
.. contents:: Table of contents
  :depth: 3
  :local:

This chapter describes the validation function compliant with Jakarta Bean Validation of Jakarta EE.

.. important::

  The Jakarta Bean Validation engine is not implemented by this function.

  Jakarta EE environments (such as WebLogic and WildFly) use the Jakarta Bean Validation implementation that is bundled in the server.
  For use outside Jakarta EE environments, the Jakarta Bean Validation implementation must be added to the reference library separately.
  (It is recommended that the compatible implementation `Hibernate Validator(external site) <http://hibernate.org/validator/>`_ be used.)

Function overview
---------------------

Can validate domains
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Provides a function that can define validation rules for each domain.

When using domain validation, it is only necessary to specify the domain name in the Bean property, which makes changing the validation rules easy.

For details, see `Use domain validation`_.

.. _bean_validation-validator:

Commonly Used Validators are Provided
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Since Nablarch provides commonly used validators, basic validations can be used without having to create anything.

For the validators provided by Nablarch, see the annotations (annotation type) in the following packages.

* :java:extdoc:`nablarch.core.validation.ee`
* :java:extdoc:`nablarch.common.code.validator.ee`

Module list
--------------------------------------------------
.. code-block:: xml

  <Dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-validation-ee</artifactId>
  </dependency>

  <!--
   Only to build messages using message management
   Message management is used by default
   -->
  <Dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-message</artifactId>
  </dependency>

  <!-- Only when using a code value validator -->
  <Dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-code</artifactId>
  </dependency>

  <!-- For use in web applications-->
  <Dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>


How to use
--------------------------------------------------

.. _bean_validation-configuration:

Configure settings to use Bean Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The configuration required to use Bean Validation are shown below.

MessageInterpolator configuration
  Configure the class that constructs the message when validation errors occur in Jakarta Bean Validation (a class that implements :java:extdoc:`MessageInterpolator <jakarta.validation.MessageInterpolator>`).

  If this is not configured, then :java:extdoc:`NablarchMessageInterpolator <nablarch.core.validation.ee.NablarchMessageInterpolator>` which uses :ref:`message` is used.

  For example, when using the implementation that builds a message from the property file of Hibernate Validator, configure as shown below.

  .. important::

    Be sure to use component name **messageInterpolator**.

  .. code-block:: xml

    <!-- Specify messageInterpolator for the component name and configure the MessageInterpolator implementation class -->
    <compnent name="messageInterpolator"
        class="org.hibernate.validator.messageinterpolation.ResourceBundleMessageInterpolator"/>

Configuration for domain validation
  See :ref:`bean_validation-domain_validation`

Configuration for using Bean Validation in web application
  See :ref:`bean_validation-web_application`

Configuration for using Bean Validation in RESTful web service
  See :ref:`bean_validation-restful_web_service`

Define the error message for validation error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
As explained in :ref:`bean_validation-configuration`, message during an error is built using :ref:`message` by default.
Therefore, refer to :ref:`message` for more information, such as where the message is defined.

The message definition rule when using the default :java:extdoc:`NablarchMessageInterpolator <nablarch.core.validation.ee.NablarchMessageInterpolator>` is as given below.

* Build a message using :ref:`message` only when the value specified in the ``message`` attribute of the annotation is enclosed within ``{`` and ``}``.
* A placeholder for embedding the attribute information of the validation annotation can be used in the message text.
  A placeholder is defined by enclosing the attribute name of the annotation within ``{`` and ``}``.
* Expressions that dynamically build messages (ex: EL expressions) cannot be used.

An example is shown below.

Java implementation example
  .. code-block:: java

      public class SampleForm {

        @Length(max = 10)
        @SystemChar(charsetDef = "Full-width character")
        @Required
        private String userName;

        @Length(min = 8, max = 8)
        @SystemChar(charsetDef = "Half-width character")
        private String birthday;

        // Getter and setter are omitted
      }

Message definition example
  Define a message using the message ID specified in the annotation as the key.
  When the message attribute of the annotation is not specified, the default value will be the message ID.

  .. code-block:: properties

    # Message corresponding to Length annotation
    # Value specified in min or max attribute of Length annotation can be embedded in the message
    nablarch.core.validation.ee.Length.min.message= Enter at least {min} characters.
    nablarch.core.validation.ee.Length.max.message= Enter no more than{max} characters
    nablarch.core.validation.ee.Length.min.max.message={min} Enter a value between {min} and {max} characters.

    # Message corresponding to SystemChar
    nablarch.core.validation.ee.SystemChar.message= Please enter with {charsetDef}.

.. tip::
  When the default behavior is changed in :ref:`bean_validation-configuration`,
  the message is defined according to the :java:extdoc:`MessageInterpolator <jakarta.validation.MessageInterpolator>` implementation.


How to configure validation rules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Validation rules can be specified by configuring annotations in a Field or Property (getter).
Also, note that annotations cannot be specified for a setter. (It is meaningless even if specified (will be ignored))

.. _bean_validation-form_property:

.. tip::

  All the property types of Bean class should be defined as a String.

  Bean Validation is performed after converting the input values to Bean.
  Therefore, whatever values are sent as external input values must be converted to Bean.

  When a property other than String exists and an invalid value is sent (for example, if an alphabetic character is sent for a numeric type),
  the conversion process to Bean, which is performed before validation, fails and an unexpected exception is thrown, resulting in a failure.

  Normally, a failure should not occur no matter what value is input, and the validation result should be notified externally (for example, the screen).

  To convert an external value to a type other than String, convert it after validation is performed.

  Even if validation is performed on the client side using JavaScript,
  there is no guarantee that the validated value will be sent to the server side, hence, the property must be a `String`.
  This is because the user can easily disable JavaScript and tamper with it using the browser developer tools on the client side.
  When such an operation is performed, there is a possibility that an invalid value will be sent to the server side, bypassing the client side validation.

Implementation examples
  Configure annotations by referring to :ref:`the validators provided by Nablarch <bean_validation-validator>`.

  .. tip::

    If annotations are configured individually, errors during implementation and maintenance costs will increase.
    Hence, it is recommended to use :ref:`the domain validation <bean_validation-domain_validation>` described below.

  .. code-block:: java

    public class SampleForm {

      @Length(max = 10)
      @SystemChar(charsetDef = "Full-width character")
      @Required
      private String userName;

      @Length(min = 8, max = 8)
      @SystemChar(charsetDef = "Half-width character")
      private String birthday;

      // Getter and setter are omitted
    }

.. _bean_validation-domain_validation:

Use domain validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Show the configuration and implementation examples to use domain validation.

Creating Bean that defines the validation rules for each domain
  To use domain validation, first create an Bean (domain Bean) with validation rules for each domain.

  This Bean class defines fields for each domain and configures annotations for the fields.
  The field name becomes the domain name. In the following example, two domains, ``name`` and ``date``, have been defined.

  .. tip::

   Configure the :java:extdoc:`@Required <nablarch.core.validation.ee.Required>` annotation which indicates required items on the individual Bean side instead of in the domain Bean.
   Whether an item is required or not cannot be enforced on the domain side, since it depends on the function design.

  .. code-block:: java

    package sample;

    import nablarch.core.validation.ee.Length;
    import nablarch.core.validation.ee.SystemChar;

    public class SampleDomainBean {

        @Length(max = 10)
        @SystemChar(charsetDef = "Full-width character")
        String name;

        @Length(min = 8, max = 8)
        @SystemChar(charsetDef = "Half-width character")
        String date;

    }

Domain Bean Enabled
  To enable the domain bean, create the implementation class :java:extdoc:`DomainManager <nablarch.core.validation.ee.DomainManager>`.
  :java:extdoc:`getDomainBean <nablarch.core.validation.ee.DomainManager.getDomainBean()>` returns the domain Bean class object.

  .. code-block:: java

    package sample;

    public class SampleDomainManager implements DomainManager<SampleDomainBean> {
      @Override
      public Class<SampleDomainBean> getDomainBean() {
          // Returns the Class object for the domain bean
          return SampleDomainBean.class;
      }
    }


  By defining `SampleDomainBean` of the :java:extdoc:`DomainManager <nablarch.core.validation.ee.DomainManager>` implementation class in the component configuration file,
  domain validation using `SampleDomainBean` will be enabled.

  .. code-block:: xml

    <!-- DomainManager implementation class should be configured with the name domainManager -->
    <component name="domainManager" class="sample.SampleDomainManager"/>

Use domain validation for each Bean
  Domain validation is performed by configuring the :java:extdoc:`@Domain <nablarch.core.validation.ee.Domain>` annotation to the bean properties to be validated.

  In this example, validation configured in the `name` field of `SampleDomainBean` is performed for `userName`.
  Similarly, validation configured in the `date` field is performed for `birthday`.

  * UserName is a required item.

  .. code-block:: java

    public class SampleForm {

      @Domain("name")
      @Required
      private String userName;

      @Domain("date")
      private String birthday;

      // Getter and setter are omitted
    }

.. _bean_validation-system_char_validator:

Performing Character Type Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Validation by character type can be performed using the validation function of system allowed characters.

To perform validation by character type, define the character set for each character type.
For example, it is necessary to define that half-width numbers from ``0`` to ``9`` are allowed in the character type of half-width numbers.

The method of defining allowed character sets for each character type is shown below.

Define the allowed character set in the component definition
  The set of allowed characters is registered using any one of the following classes.
  During registration, configure the component name to an arbitrary name that indicates the character type.

  * :java:extdoc:`RangedCharsetDef <nablarch.core.validation.validator.unicode.RangedCharsetDef>` (Used when registering the allowed character sets in the range)
  * :java:extdoc:`LiteralCharsetDef <nablarch.core.validation.validator.unicode.LiteralCharsetDef>` (Used when registering all allowed character sets in the literal)
  * :java:extdoc:`CompositeCharsetDef <nablarch.core.validation.validator.unicode.CompositeCharsetDef>` (Used when registering allowed characters consisting of multiple RangedCharsetDef and LiteralCharsetDef)

  A configuration example is shown below.

  .. code-block:: xml

    <!-- Half-width number -->
    <component name="Half-width number" class="nablarch.core.validation.validator.unicode.LiteralCharsetDef">
      <property name="allowedCharacters" value="01234567890" />
      <property name="messageId" value="numberString.message" />
    </component>

    <!-- ASCII (excluding control code) -->
    <component name="ascii" class="nablarch.core.validation.validator.unicode.RangedCharsetDef">
      <property name="startCodePoint" value="U+0020" />
      <property name="endCodePoint" value="U+007F" />
      <property name="messageId" value="ascii.message" />
    </component>

    <!-- Alphanumeric -->
    <component name="Alphanumeric" class="nablarch.core.validation.validator.unicode.CompositeCharsetDef">
      <property name="charsetDefList">
        <list>
          <!-- Definition of half-width number -->
          <component-ref name="Half-width number" />

          <!-- Definition of half-width characters -->
          <component class="nablarch.core.validation.validator.unicode.LiteralCharsetDef">
            <property name="allowedCharacters"
                value="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" />
          </component>
        </list>
      </property>
      <property name="messageId" value="asciiAndNumberString.message" />
    </component>

Specify the character type with annotation
  Configure the :java:extdoc:`@SystemChar <nablarch.core.validation.ee.SystemChar>` annotation in the property that performs character type validation.
  Configure the name indicating the allowed character type in the :java:extdoc:`charsetDef <nablarch.core.validation.ee.SystemChar.charsetDef()>` attribute of this annotation.
  This name will be the component name when the character type set is registered in the component configuration file mentioned above.

  Since ``half-width numbers`` have been specified in this example, "0123456789" are allowed as per the component definition mentioned above.

  .. code-block:: java

    public class SampleForm {

        @SystemChar(charsetDef = "Half-width character")
        public void setAccountNumber(String accountNumber) {
            this.accountNumber = accountNumber;
        }
    }

.. tip::

  When there are a large number of characters in the set of allowed characters, it takes time to check the characters that are defined after. (To simply check whether the characters are included in the character set in order from the beginning)
  To solve this problem, provide a mechanism to cache the results of a character once it has been checked.

  * In principle, it is advisable to proceed with development without using the cache function, and consider using the cache function if character type validation becomes a bottleneck.

  Usage is simple. Configure the definition of the original character type set to :java:extdoc:`CachingCharsetDef <nablarch.core.validation.validator.unicode.CachingCharsetDef>`
  for caching, as in the component definition shown below.

  .. code-block:: xml

    <component name="Half-width character" class="nablarch.core.validation.validator.unicode.CachingCharsetDef">
      <property name="charsetDef">
        <component class="nablarch.core.validation.validator.unicode.LiteralCharsetDef">
          <property name="allowedCharacters" value="01234567890" />
        </component>
      </property>
      <property name="messageId" value="numberString.message" />
    </component>

Allowing Surrogate Pairs
  This validation does not allow surrogate pairs by default.
  (They are not allowed even if the characters for surrogate pairs are explicitly defined in `LiteralCharsetDef`.)

  To allow surrogate pairs, :java:extdoc:`SystemCharConfig <nablarch.core.validation.ee.SystemCharConfig>` must be configured in the component configuration file as follows.

  Point
   * The component name should be ``ee.SystemCharConfig``

  .. code-block:: xml

    <component name="ee.SystemCharConfig" class="nablarch.core.validation.ee.SystemCharConfig">
      <!-- Allows surrogate pairs -->
      <property name="allowSurrogatePair" value="true"/>
    </component>

.. _bean_validation-correlation_validation:

Performing Correlation Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To perform correlation validation using multiple items, use the :java:extdoc:`@AssertTrue <jakarta.validation.constraints.AssertTrue>` annotation of Jakarta Bean Validation.

Implementation examples
  In this example, it has been verified that the email address and the confirmation email address match.
  When a verification error occurs, the message specified in the `message` property becomes the error message.

  .. code-block:: java

    public class SampleForm {
      private String mailAddress;

      private String confirmMailAddress;

      @AssertTrue(message = "{compareMailAddress}")
      public boolean isEqualsMailAddress() {
        return Objects.equals(mailAddress, confirmMailAddress);
      }
    }

.. important::

  Since the execution order of the validation is not guaranteed in Jakarta Bean Validation,
  correlation validation may be called even before the validation of individual items.

  Therefore, it is necessary to implement validation logic so that unexpected exceptions do not occur,
  even if the validation of individual items is not executed in correlation validation.

  If `mailAddress` and `confirmMailAddress` are optional items in the example above,
  a result must be returned without executing validation if they have not been input.

  .. code-block:: java

    @AssertTrue(message = "{compareMailAddress}")
    public boolean isEqualsMailAddress() {
      if (StringUtil.isNullOrEmpty(mailAddress) || StringUtil.isNullOrEmpty(confirmMailAddress)) {
        // If either of them is not input, correlation validation is not performed.(Validation is OK)
        return true;
      }
      return Objects.equals(mailAddress, confirmMailAddress);
    }


.. _bean_validation-database_validation:

Performing Correlation Validation with the Database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Correlation validation with the database is implemented on the business action side for the following reasons.

Reason
  When correlation validation is performed for the database using Bean Validation,
  the database is accessed using the unsafe value before validation is performed.
  (There is no guarantee that the value of the object during Bean Validation is safe.)
  This is an implementation that should be avoided as it causes vulnerabilities such as SQL injection.

  By validating with a business action after validation is performed,
  the database can be accessed using the validated safe value.

.. _bean_validation-create_message_for_property:

To create a validation error message linked to a specific item
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When an error occurs in the validation performed with action handlers such as :ref:`Correlation validation with the database <bean_validation-database_validation>`,
sometimes it may be required to highlight the target item as an error on the screen.

In this case, as shown in the implementation example below, an error message is built using :java:extdoc:`ValidationUtil#createMessageForProperty <nablarch.core.validation.ValidationUtil.createMessageForProperty(java.lang.String-java.lang.String-java.lang.Object...)>`
and the :java:extdoc:`ApplicationException <nablarch.core.message.ApplicationException>` is thrown.

.. code-block:: java

  throw new ApplicationException(
          ValidationUtil.createMessageForProperty("form.mailAddress", "duplicate.mailAddress"));


Performing validation using a function that performs Bean multiple input, such as batch registration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
There are cases where the same information is input multiple times, such as in batch registration.
In such cases, a nested Bean is defined for the Bean for validation.

.. tip::
  Since this is the specifications for Jakarta Bean Validation, see Jakarta Bean Validation specifications for details.

An example is shown below.

.. code-block:: java

  // Form that stores all the information that has been batch input
  public class SampleBulkForm {

    // Configure the Valid annotation that indicates
    // validation is also executed for nested Bean.
    @Valid
    private List<SampleForm> sampleForm;

    public SampleBulkForm() {
      sampleForm = new ArrayList<>();
    }

    // Getter and setter are omitted
  }


  // Form that retains the information of one input of the information that is input in batch
  public class SampleForm {
    @Domain("name")
    private String name;

    // Getter and setter are omitted
  }

Important points when validating nested Bean
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Nested bean information may not be sent, for example, when the html is tampered with a browser developer tool and the web service receives an invalid Json or XML, etc.
In this case, the nested Bean becomes uninitialized (null) and will not be a target for validation.
Hence, implementation is required so that the status of the nested Bean can be reliably validated.

Some implementation examples are shown below.

When parent Bean and nested Bean are 1:N
  The nested Bean will be a target for validation, and the fields of the nested Bean are also initialized when the parent Bean is initialized.
  If the information of nested Bean is required (select or input at least one),
  configure the :java:extdoc:`Size <nablarch.core.validation.ee.Size>` annotation.

  .. code-block:: java

    // Validates that at least one is selected by configuring the Size annotation.
    @Valid
    @Size(min = 1, max = 5)
    private List<SampleNestForm> sampleNestForms;

    public SampleForm() {
      // Initialize the fields of the nested Bean when creating an instance
      sampleNestForms = new ArrayList<>();
    }

When parent Bean and nested Bean are 1:1
  Consider whether a flat Bean can be made without nesting the Bean.
  When unable to respond to requests from the connection destination, perform implementation so that nested Bean validation can be executed reliably.

  .. code-block:: java

    // Target nested Beans for validation
    @Valid
    private SampleNestForm sampleNestForm;

    public SampleForm() {
      // Initialize the fields of the nested Bean when creating an instance
      sampleNestForm = new SampleNestForm();
    }


.. _bean_validation-web_application:

Checking User Input Values for Web Applications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The user input values for web applications are checked using :ref:`inject_form_interceptor`.
For details, see :ref:`inject_form_interceptor`.

To use Bean Validation with :ref:`inject_form_interceptor`, it must be defined in the component configuration file.
As shown in the example below, Define a component definition of :java:extdoc:`BeanValidationStrategy <nablarch.common.web.validator.BeanValidationStrategy>` with the name  ``validationStrategy``.

.. code-block:: xml

  <component name="validationStrategy" class="nablarch.common.web.validator.BeanValidationStrategy" />

.. tip::

  BeanValidationStrategy sorts the error messages for validation errors in the following order.

  * Order of item names returned by jakarta.servlet.ServletRequest#getParameterNames
    (If the item in which the error occurred does not exist in the request parameter, it is moved to the end)

  Note that the value returned by ``getParameterNames`` is implementation-dependent, and the alignment order may change depending on the application server used.
  To change the sort order in the project, BeanValidationStrategy is inherited.


.. _bean_validation-restful_web_service:

Checking User Input Values for RESTful Web Services
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Checking user input values for RESTful web services is done by setting the :java:extdoc:`Valid <jakarta.validation.Valid>` annotation on the method of the resource class that receives input values.
For details, see :ref:`jaxrs_bean_validation_handler_perform_validation` .


.. _bean_validation_onerror:


Request parameters are to be obtained from the request scope even when there is a validation error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When :ref:`inject_form_interceptor` is used, the validated Form is stored in the request scope after successful validation.
This can be used to reference the request parameters, but there may also be similar cases where you would like to get the parameters from the request scope when a validation error occurs.


For example, the following process must be added when using the JSTL tag (EL expression),
since it is not possible to implicitly refer to [#1]_ the request parameters unlike with the Nablarch custom tag.

* Use Nablarch tag ``<n:set>`` once to store the values of request parameters in a variable.
* Access request parameters using the implicit object ``param``

An example using the former ``<n:set>`` is shown below.

.. code-block:: jsp

   <%-- Substitutes the values of request parameters in a variable so that they can be referenced even with JSTL (EL expression) --%>
   <n:set var="quantity" name="form.quantity" />
   <c:if test="${quantity >= 100}">
     <%-- When the quantity is 100 or more... --%>


In such a case, the Bean that copied the request parameters can be stored in the request scope
even when a validation error occurs by configuring the property ``copyBeanToRequestScopeOnError`` of
:java:extdoc:`BeanValidationStrategy <nablarch.common.web.validator.BeanValidationStrategy>` to ``true``.
A configuration example is shown below.

.. code-block:: xml

  <component name="validationStrategy" class="nablarch.common.web.validator.BeanValidationStrategy">
    <!-- Copies values to the request scope when a validation error occurs -->
    <property name="copyBeanToRequestScopeOnError" value="true"/>
  </component>

The Bean is stored in the request scope using a key specified with the ``name`` ``@InjectForm``
(same as normal operation of :ref:`inject_form_interceptor`).


By enabling this function, the JSP mentioned above can be described as follows.


.. code-block:: jsp

   <%-- Request parameter values can also be referenced with JSTL (EL expression) via request scope --%>
   <c:if test="${form.quantity >= 100}">
     <%-- When the quantity is 100 or more... --%>

.. [#1] For a description of how the Nablarch custom tag works, see :ref:`tag-access_rule`.

.. _bean_validation-property_name:


Embed the item name in the message when a validation error occurs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Although the item name cannot be embedded in the message as per the Jakarta Bean Validation specifications,
you may want to embed the item name in the message according to the requirements etc.
Therefore, Nablarch provides a function that embeds the item name of the item in which an error has occurred, even if Jakarta Bean Validation is used.

The usage method is shown below.

Component configuration file
  Configure the factory class that generates the message converter which embeds the item name in a message.
  Configure ``constraintViolationConverterFactory`` in the component name
  and :java:extdoc:`ItemNamedConstraintViolationConverterFactory <nablarch.core.validation.ee.ItemNamedConstraintViolationConverterFactory>` in the class name.

  .. code-block:: xml

    <component name="constraintViolationConverterFactory"
        class="nablarch.core.validation.ee.ItemNamedConstraintViolationConverterFactory" />

Form to be validated
  .. code-block:: java

    package sample;

    public class User {

      @Required
      private String name;

      @Required
      private String address;
    }

Definition of item name
  Item names are defined as messages.
  The message ID of item name is the fully qualified class name for validation + "." + item property name.

  In the case of the above Form class, ``sample.User`` is a fully qualified name with 2 properties- ``name`` and ``address``.
  As shown below, ``sample.User.name`` and ``sample.User.address`` are required to define the item name.

  If the item name is not defined, it will not be added in the message.

  .. code-block:: properties

    # Required message
    nablarch.core.validation.ee.Required.message= Please enter

    # Definition of item name
    sample.User.name = User name
    sample.User.address = Mailing address

Generated Message
  In the generated message, the item name is added to the beginning of the error message.
  Item name is enclosed by ``[`` , ``]``.

  .. code-block:: text

    [User Name] Please enter.
    [Mailing Address] Please enter.

.. tip::
  To change the method of adding the item name to the message, see :java:extdoc:`ItemNamedConstraintViolationConverterFactory <nablarch.core.validation.ee.ItemNamedConstraintViolationConverterFactory>`
  and add the implementation on the project side.


.. _bean_validation-use_groups:

Use groups of Bean Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Jakarta Bean Validation specification allows you to limit the rules used for validation to a specific group by specifying a group at the time of validation execution.
Nablarch also provides APIs that allow group specification in Bean Validation.

The usage method is shown below.

Form to be validated
  .. code-block:: java

    public class SampleForm {

        @SystemChar(charsetDef = "Number", groups = {Default.class, Test1.class})
        String id;

        @SystemChar.List({
                @SystemChar(charsetDef = "Full-width character") // If no group is specified, the validation rule is assumed to belong to the Default group.
                @SystemChar(charsetDef = "Half-width character", groups = Test1.class),
        })
        String name;

        public interface Test1 {}
    }


Process to perform validation
  .. code-block:: java

    SampleForm form = new SampleForm();

    ...

    // If no group is specified, the rules belonging to the Default group are used for validation.
    ValidatorUtil.validate(form);

    // If groups are specified, validation is performed using the rules belonging to the specified groups.
    ValidatorUtil.validateWithGroup(form, SampleForm.Test1.class);


See :java:extdoc:`ValidatorUtil#validateWithGroup <nablarch.core.validation.ee.ValidatorUtil.validateWithGroup(java.lang.Object-java.lang.Class...)>`
and :java:extdoc:`ValidatorUtil#validateProperty <nablarch.core.validation.ee.ValidatorUtil.validateProperty(java.lang.Object-java.lang.String-java.lang.Class...)>` for details on the APIs.

.. tip::
   By using the group function to switch validation rules, a single form class can be shared by multiple screens and APIs.
   However, Nablarch does not recommend such usage (see :ref:`Form class is created for each HTML form <application_design-form_html>` and :ref:`Form class is created for each API <rest-application_design-form_html>` for details ).
   If you use the group function for the purpose of sharing form classes, please use it after careful consideration in your project.


Expansion example
-------------------------
To add project-specific annotations and validation logic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If the requirements cannot be satisfied with the validators described in :ref:`bean_validation-validator`,
annotations and validation logic are added on the project side.

For details on the implementation method, see the following links and Nablarch implementation.

* `Hibernate Validator(external site) <http://hibernate.org/validator/>`_
* `Jakarta Bean Validation(external site) <https://jakarta.ee/specifications/bean-validation/>`_
