.. _bean_util:

BeanUtil
==================================================
.. contents:: Table of contents
  :depth: 3
  :local:

BeanUtil provides the following functions related to Java Beans. It can also handle records standardised from Java 16 in the same way as Java Beans.
See :ref:`bean_util-use_record` for more information.

* Configuring and acquiring values for properties
* Transferring values to other Java Beans
* Transferring values between Java Beans and java.util.Map

Module list
---------------------------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-beans</artifactId>
  </dependency>

.. _bean_util-use_java_beans:

How to use
--------------------------------------------------
:java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` can be used to implement operations for arbitrary Java Beans.

An usage example of BeanUtil is shown below.

Bean definition
  .. code-block:: java

    public class User {
        private Long id;
        private String name;
        private Date birthDay;
        private Address address;
        // Getter and setter are omitted
    }

    public class Address {
        private String postNo;
        // Getter and setter are omitted
    }

    public class UserDto {
        private String name;
        private String birthDay;
        // Getter and setter are omitted
    }

Usage example of BeanUtil
  Examples of several APIs are shown below. For details, see :java:extdoc:`Javadoc <nablarch.core.beans.BeanUtil>` of BeanUtil.

  .. code-block:: java

    final User user = new User();
    user.setId(1L);
    user.setName("Name");
    user.setBirthDay(new Date());

    final Address address = new Address();
    address.setPostNo("1234");
    user.setAddress(address);
    

    // Specify the property name and get the value (1 can be acquired).
    // The value is obtained through getter.
    final Long id = (Long) BeanUtil.getProperty(user, "id");

    // Specify the property name and configure the value (value of the name property is changed to "new name")
    // Value is configured through setter.
    BeanUtil.setProperty(user, "name", "New name");

    // Transfer values while creating another Bean.
    // The value is transferred to the property of UserDto that matches the property name of User.
    // Value is transferred using getters and setters.
    // Properties that do not exist in the destination are ignored.
    // If the property type of the destination is different, type conversion will be performed by ConversionUtil.
    final UserDto dto = BeanUtil.createAndCopy(UserDto.class, user);

    // Transfer the property value to Map.
    // Map key is the property name and the value is the value acquired by getter.
    // The value of the nested Bean is transferred with the key name separated by "." (Map-> Map is not nested)
    // For example, address.postNo
    final Map<String, Object> map = BeanUtil.createMapAndCopy(user);
    final String postNo = (String) map.get("address.postNo");     // 1234 can be acquired.

    // Transfer the value of Map to Bean.
    // Transfer the Map value using the property setter that matches the Map key.
    // When transferring values to nested Bean, Map key names must be separated by ".". (Nested Map-> Map cannot be handled)
    // For example, by defining address.postNo and key name, the value is set in postNo property of User.address.
    final Map<String, Object> userMap = new HashMap<String, Object>();
    userMap.put("id", 1L);
    userMap.put("address.postNo", 54321);
    final User user = BeanUtil.createAndCopy(User.class, userMap);
    final String postNo2 = user.getAddress()
                          .getPostNo();             // 54321 can be acquired.

.. important::

  BeanUtil does not support type parameters of the List type.
  If a type parameter of the List type is needed, override getter in the concrete class.

  .. code-block:: java

    public class ItemsForm<D extends Serializable> {
        private List<D> items;
        public List<D> getItems() {
            return items;
        }
        public void setItems(List<D> items) {
            this.items = items;
        }
    }

    public class Item implements Serializable {
        // Properties omitted
    }

    // When not to override in the concrete class.
    // Calling BeanUtil.createAndCopy(BadSampleForm.class, map)
    // throws a runtime exception because it does not support
    // type parameters of List type.
    public class BadSampleForm extends ItemsForm<Item> {
    }

    // When overridden by a concrete class.
    // BeanUtil.createAndCopy(GoodSampleForm.class, map) works correctly.
    public static class GoodSampleForm extends ItemsForm<Item> {
        @Override
        public List<Item> getItems() {
            return super.getItems();
        }
    }

.. _utility-conversion:

Type conversion rules of BeanUtil
--------------------------------------------------
:java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` performs property type conversion when data is migrated from Java Beans object or Map object to another Java Beans object.

When data is transferred from Map object to Java Beans object, if ``.`` is included in the key of the Map object, its property is treated as a nested object.

For type conversion rules, refer to the :java:extdoc:`Converter <nablarch.core.beans.Converter>` implementation class that is placed below the :java:extdoc:`nablarch.core.beans.converter` package.

.. important::

  When conversion is performed to a type with a lower precision (for example, conversion from Long to Integer) with the type conversion rules provided by default, the process ends normally even if a value that exceeds the conversion destination precision is specified. Therefore, when copying using BeanUtil, it is necessary to validate in advance whether the value to be copied is allowed in the system by :ref:`validation` . If the values are not verified, incorrect values could be captured by the system and cause a failure.

.. important::

  Type conversion rules are common to all applications. For application of different type conversion rules only for specific processes, refer to the :ref:`bean_util-format_logical` and apply :java:extdoc:`Converter <nablarch.core.beans.Converter>` implementation for specific properties and types.

.. _utility-conversion-add-rule:

Add type conversion rules
--------------------------------------------------

The following steps are required to add type conversion rules.

1. Implement the following interfaces as necessary to implement the type conversion process.

  * :java:extdoc:`Converter <nablarch.core.beans.Converter>`
  * :java:extdoc:`ExtensionConverter <nablarch.core.beans.ExtensionConverter>`

2. Create implementation class :java:extdoc:`ConversionManager <nablarch.core.beans.ConversionManager>` . To set rules in addition to the standard type conversion rules, create an implementation class for :java:extdoc:`ConversionManager <nablarch.core.beans.ConversionManager>` that has :java:extdoc:`ConversionManager <nablarch.core.beans.ConversionManager>` as a property.

  .. code-block:: java

    public class SampleConversionManager implements ConversionManager {

        private ConversionManager delegateManager;

        @Override
        public Map<Class<?>, Converter<?>> getConverters() {
            Map<Class<?>, Converter<?>> converters = new HashMap<Class<?>, Converter<?>>();

            // Standard converter
            converters.putAll(delegateManager.getConverters());

            // Converter created this time
            converters.put(BigInteger.class, new CustomConverter());

            return Collections.unmodifiableMap(converters);
        }

        @Override
        public List<ExtensionConverter<?>> getExtensionConvertor() {
            final List<ExtensionConverter<?>> extensionConverters =
                new ArrayList<ExtensionConverter<?>>(delegateManager.getExtensionConvertor());
            extensionConverters.add(new CustomExtensionConverter());
            return extensionConverters;
        }

        public void setDelegateManager(ConversionManager delegateManager) {
            this.delegateManager = delegateManager;
        }
    }

3. Configure implementation class :java:extdoc:`ConversionManager <nablarch.core.beans.ConversionManager>` in the component configuration file.

   Point
    * The component name should be **conversionManager**.

   .. code-block:: xml

    <component name="conversionManager" class="sample.SampleConversionManager">
      <property name="delegateManager">
        <component class="nablarch.core.beans.BasicConversionManager" />
      </property>
    </component>

Specify the format allowed during type conversion
--------------------------------------------------
During type conversion, format of date and numerics can be canceled by specifying the allowable format. For example, a string type value (1,000,000) with commas can be converted to a numeric type (1000000).

The following three specification methods are available to specify the permitted formats. The priority is higher for the method based on the order of description.

* :ref:`Configure when calling BeanUtil <bean_util-format_logical>`
* :ref:`Configure annotation to property unit <bean_util-format_property_setting>`
* :ref:`Default configuration (system common configuration) <bean_util-format_default_setting>`

.. _bean_util-format_default_setting:

Configure the default (system-wide) allowable format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Format default configurations are set in the component configuration file.

For example, in the case of allowing numerics with commas to be entered on the screen, individual specification is not required if default configuration is not required.

A configuration method is shown below.

Point
  * Define :java:extdoc:`BasicConversionManager <nablarch.core.beans.BasicConversionManager>` with component name **conversionManager** .
  * Configure the allowed date and datetime format in ``datePatterns`` .
  * Configure the allowable number format in ``numberPatterns`` property.
  * If multiple formats are allowed, set multiple formats.

Configuration example
  .. code-block:: xml

    <component name="conversionManager" class="nablarch.core.beans.BasicConversionManager">
      <!-- Specify acceptable formats for date and date and time -->
      <property name="datePatterns">
        <list>
          <value>yyyy/MM/dd</value>
          <value>yyyy-MM-dd</value>
        </list>
      </property>
      <!-- Specify acceptable format for numbers -->
      <property name="numberPatterns">
        <list>
          <value>#,###</value>
        </list>
      </property>
    </component>

.. important::

  If date and time format are specified as ``yyyy/MM/dd`` and ``yyyy/MM/dd HH:mm:ss`` , date and time format values are also parsed as `yyyy/MM/dd` and time information is lost in some cases.

  Therefore, it is necessary to specify only the date format in the default specification and override the default configuration using :ref:`configure with annotation in property units <bean_util-format_property_setting>` for the date/time format item.


.. _bean_util-format_property_setting:

Configure the allowed format for the copied property
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Specifying a different format without applying the :ref:`default configuration <bean_util-format_default_setting>` for specific functions may be preferred in some cases. In this case, specify the annotation for the field corresponding to the relevant property of the copy target Bean (copy source or copy destination) and overwrite the allowable format.

Although annotations work regardless of whether they are specified in the copy source or the copy destination, specifying the basic allowed format in the field corresponding to the string type property is preferred.
This is because the property that holds the formatted value is string type, and the allowable format is naturally specified for that property.
If both the copy source and copy destination are specified, the copy source configuration is used.

For example, it may be used when the date format is specified in the default configuration and the date and time format is allowed only for a specific function.

An implementation example is shown below.

Point
  * Configure :java:extdoc:`CopyOption <nablarch.core.beans.CopyOption>` annotation for the field corresponding to the copy source (copy destination) property.
  * Specify the allowed date and date and time format in ``datePattern`` of CopyOption.
  * Specify the allowed number format in ``numberPattern`` of CopyOption.

Implementation examples
  .. code-block:: java

    public class Bean {
        // Specify acceptable format for date and time
        @CopyOption(datePattern = "yyyy/MM/dd HH:mm:ss")
        private String timestamp;

        // Specify acceptable format for numbers
        @CopyOption(numberPattern = "#,###")
        private String number;

        // Setter and getter are omitted
    }

.. _bean_util-format_logical:

Specify the format allowed when calling BeanUtil
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
We want to specify a different format without applying the :ref:`default configuration <bean_util-format_default_setting>` only for specific functions, but :ref:`configure with annotation in property units <bean_util-format_property_setting>` cannot be used in some cases when Bean is automatically generated using OSS, etc. There are cases when different type conversion rules is required to be applied only for specific properties.

For such cases, when calling :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>`, provide support by configuring the allowable format and type conversion rules.

An implementation example is shown below.

Point
  * Configure the properties using :java:extdoc:`CopyOptions <nablarch.core.beans.CopyOptions>` . See :java:extdoc:`CopyOptions.Builder <nablarch.core.beans.CopyOptions.Builder>` for the method to constuct ``CopyOptions`` .
  * Call :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` using the generated :java:extdoc:`CopyOptions <nablarch.core.beans.CopyOptions>` .

Implementation examples
  .. code-block:: java

   final CopyOptions copyOptions = CopyOptions.options()
           // Specify the allowed format for the timestamp property
           .datePatternByName("timestamp", "yyyy/MM/dd/ HH:mm:ss")
           // Apply CustomDateConverter for custom property
           .converterByName("custom", Date.class, new CustomDateConverter())
           .build();

    // Call BeanUtil by specifying the CopyOptions.
    final DestBean copy = BeanUtil.createAndCopy(DestBean.class, bean, copyOptions);

.. _bean_util-use_record:

Use records in BeanUtil
--------------------------------------------------

BeanUtil can handle records standardised from Java16 in the same way as Java Beans.

Note that record is an immutable class.
Therefore, if a record is passed as an object to be modified as the argument to methods such as
:java:extdoc:`BeanUtil.setProperty <nablarch.core.beans.BeanUtil.setProperty(java.lang.Object,java.lang.String,java.lang.Object)>`  or :java:extdoc:`BeanUtil.copy <nablarch.core.beans.BeanUtil.copy(SRC,DEST)>` ,
a run-time exception is thrown.

How to use
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Same as :ref:`operation on Java Beans <bean_util-use_java_beans>` .

.. important::

   BeanUtil does not support records containing type parameters of List type.
   Since records cannot inherit, type parameters of List type should be set to a concrete type from the outset and records should be defined.

  .. code-block:: java

    public class Item implements Serializable {
        // Property omitted.
    }


    // If the type parameter of List type is not set to a concrete type.
    // Calling BeanUtil.createAndCopy(BadSampleRecord.class, map)
    // throws a runtime exception because it does not support
    // type parameters of List type.
    public class BadSampleRecord<T>(List<T> items) {}

    // If the type parameter of the List type is set to a concrete type.
    // BeanUtil.createAndCopy(GoodSampleRecord.class, map) works correctly.
    public record GoodSampleRecord(List<Item> items) {}
