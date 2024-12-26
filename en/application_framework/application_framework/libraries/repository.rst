.. _repository:

System Repository
==================================================

.. contents:: Table of contents
  :depth: 3
  :local:

Provides a function to manage objects used in various places and configuration values when implementing an application.

The function can be used for the following.

* Logic that may differ for each environment (generated class and property values) can be defined in an external file.
* Relationships can be built between objects based on the definition of external files. (with DI container function)

Function overview
--------------------------------------------------
Objects can be constructed using DI containers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The DI container feature allows objects to be constructed based on the definition of components defined in :ref:`xml <repository-root_node>`
or the :ref:`annotated class <repository-inject-annotation-component>`.
The constructed object is a **singleton**.

The DI container function can do the following:

* :ref:`Can inject setter. <repository-definition_bean>`
* :ref:`Strings, numbers and booleans can be used. <repository-property_type>`
* :ref:`Can inject list and map. <repository-map_list>`
* :ref:`Allows automatic injection into setters with matching types and names. <repository-autowired>`
* :ref:`Can inject factory.  <repository-factory_injection>`
* :ref:`Can construct objects of the annotated classes. <repository-inject-annotation-component>`
* :ref:`Allows management of environment-dependent values. <repository-environment_configuration>`

DI container is accessed from the system repository instead of direct access from the application.
For details, see :ref:`repository-use_system_repository`.

Objects can be initialized
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Any initialization processing can be executed after object construction.

Since restrictions may occur in the initialization order based on the dependency of the objects,
this function allows the initialization order of the objects to be specified.

For details, see :ref:`repository-initialize_object`.

Module list
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core</artifactId>
  </dependency>
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-repository</artifactId>
  </dependency>

How to use
--------------------------------------------------

.. _repository-root_node:

Define root node in xml
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The root node of the component configuration file (xml) is `component-configuration`.
If `schemaLocation` is configured correctly, the document of each element and attribute in the IDE can be referred, and the completion functions can be utilized effectively.

.. code-block:: xml

  <component-configuration xmlns="http://tis.co.jp/nablarch/component-configuration"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://tis.co.jp/nablarch/component-configuration /component-configuration.xsd">

  </component-configuration>

Refer below for details on how to define components in xml.

* :ref:`repository-definition_bean`
* :ref:`repository-override_bean`
* :ref:`repository-property_type`
* :ref:`repository-map_list`
* :ref:`repository-autowired`
* :ref:`repository-environment_configuration`
* :ref:`repository-user_environment_configuration`
* :ref:`repository-factory_injection`
* :ref:`repository-initialize_object`
* :ref:`repository-split_xml`

.. _repository-definition_bean:

Configure Java Beans object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Java Beans object is defined using the component element.

* Configure FQCN of the class managed by DI container in class attribute.
* An any name can be configured using the name attribute.
* Setter can be injected using the property child element.
* Component can be defined in the property child element.
* Component defined elsewhere can be injected with the setter using ref attribute of property.


An example is shown below.

.. code-block:: xml

  <!-- Configure Java Beans object using component element -->
  <component name="sample" class="sample.SampleBean" />

  <component name="component" class="sample.SampleComponent">
    <!--
     Setter injection with property element
     In this example, the object defined as component with the name sample is injected
     -->
    <property name="sample" ref="sample" />

    <!-- Component can also be defined in the child element of property
    without using the ref attribute -->
    <property name="obj">
      <component class="sample.SampleObject" />
    </property>

    <!-- Setter injection of literal value -->
    <property name="limit" value="100" />
  </component>


.. important::

  The created instance is a singleton. Therefore, note the following points.

  - Since the instance is a singleton, it is not created each time it is acquired (not a prototype).
  - The instance is not destroyed until the application is terminated.
  
  Special caution is required as a serious bug will be embedded if this is not understood.
  For example, there is a possibility of causing serious bugs such as the generated instance mistaken for a prototype,
  and a certain request will cause the input value of user A to be set in the component and request from another user B will use that value.
  
  If the state of a component is intentionally changed or shared across the application, that component must be thread-safe.


.. tip::

  Instance of an object is created for each component element. For example, if a component is defined in 2 places as follows, separate instances will be created.

  .. code-block:: xml

    <!-- Two instances of SampleBean are registered in the repository -->
    <component name="sample1" class="sample.SampleBean" />
    <component name="sample2" class="sample.SampleBean" />

.. tip::

  Since the component defined by nesting is also stored in the global area of the repository, the name can be specified to acquire the object.
  For information on how to get the object, see :ref:`repository-get_object`.

  

.. tip::
   Injection is not performed for static properties (static setter methods).
   If the property to be injected is static, an exception will be thrown when building the DI container.
   
.. _repository-override_bean:

Overwrite the configuration of Java Beans object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The configuration of previously read objects can be overwritten by registering objects with the same name attribute of component tag.
This function can be used to replace the object for production environment with the object (mock) for testing when testing is conducted.

When an object is overwritten, simply registering an object with the same name will automatically give priority to the object that is read later.

An example is shown below.

.. code-block:: xml

  <component name="sample" class="sample.SampleBean">
    <property name="prop" value="message" />
  </component>

  <!-- Define and overwrite a component with the same name -->
  <component name="sample" class="sample.MockSampleBean" />

.. important::

  If different classes are configured as in the above example, all the property configurations before overwriting will be discarded.
  This is because even if the class implements the same interface, they do not always have the same property.

  However, when the same class is configured, the configuration of property before overwriting are all inherited to the class after overwriting.
  Therefore, the configuration to a specific property cannot be removed with the configuration after overwriting.
  For example, when the following overwrite configuration is configured, the property element does not exist in the configuration after overwriting,
  but message is configured in prop as the value of prop before overwriting is inherited.

  .. code-block:: xml

    <component name="sample" class="sample.SampleBean">
      <property name="prop" value="message" />
    </component>

    <!--
    Property is not set, but the value of prop before overwriting is inherited
     -->
    <component name="sample" class="sample.SampleBean" />

.. _repository-property_type:

Use a string, numeric, or boolean value as the configuration value
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If property type is of the following type, the value can be easily configured using literal notation.

* java.lang.String
* java.lang.String[]
* java.lang.Integer(int)
* java.lang.Integer[](int[])
* java.lang.Long(long)
* java.lang.Boolean(boolean)

A configuration example is shown below.

java.lang.String
  When configuring a value in java.lang.String type, describe the value to be configured with literal in the value attribute.

  In this example, "abcde" is set for the str property.

  .. code-block:: xml

    <property name="str" value="abcde" />

java.lang.String[]
  When configuring a value in java.lang.String [] type, configure the value in value attribute using the comma (,) delimiter.
  Values separated by commas will be one element of the array.

  In this example, "a, b, c, d, e" is set for the array property.
  The delimiter, cannot be set as an element.

  .. code-block:: xml

    <property name="array" value="a, b, c, d, e" />

java.lang.Integer(int)
  When configuring a value in java.lang.Integer type and int type, describe the value to be configured in the value attribute.
  The value that can be configured is the value that can be converted by `Integer#valueOf`.

  In this example, "12345" is configured to the num property of Integer (int) type.

  .. code-block:: xml

    <property name="num" value="12345" />

java.lang.Integer[](int[])
  Similar to java.lang.String [] type, configure the value in the value attribute using the comma (,) delimiter.
  The value that can be configured in each element is the value that can be converted by `Integer#valueOf`.

java.lang.Long(long)
  Similar to java.lang.Integer(int), describe the value to be configured in value attribute.
  The value that can be configured is the value that can be converted by `Long#valueOf`.

java.lang.Boolean(boolean)
  When configuring a value in java.lang.Boolean type, describe the value to be configured with literal in the value attribute.
  The value that can be configured is the value that can be converted by `Boolean#valueOf`.

  In this example, "true" is configured to the bool property of Boolean(boolean) type.

  .. code-block:: xml

    <property name="bool" value="true" />

.. _repository-map_list:

Use list or map as the configuration value
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
By configuring the component using list element and map element, setter can be injected for the property receiving list or map.

Configuration of the list using the list element
  List element can be set to a string or any Java Beans object.

  In this example, list of strings with [string1, string2, string3] is configured for the stringList property of SampleBean.

  .. code-block:: xml

    <component class="sample.SampleBean">
      <property name="stringList">
        <list>
          <value>string1</value>
          <value>string2</value>
          <value>string3</value>
        </list>
      </property>
    </component>

  An any name can be configured for the list element and the name can be referenced in the property element.
  The configuration of this example is the same as the above example.

  .. code-block:: xml

    <list name="strList">
      <value>string1</value>
      <value>string2</value>
      <value>string3</value>
    </list>

    <component class="sample.ListSample">
      <!-- Configure a List named strList -->
      <property name="stringList" ref="strList" />
    </component>

  In this example, list of Java Beans objects with `SampleHandler1`, `SampleHandler2` and `SampleHandler3` is configured for the handlers property.

  The name can be referenced by using the component-ref element, which is also shown in the following example.

  .. code-block:: xml

    <component name="sampleHandler3" class="sample.SampleHandler3" />

    <component class="sample.ListSample">
      <property name="handlers">
        <list>
          <component class="sample.SampleHandler1" />
          <component class="sample.SampleHandler2" />
          <component-ref name="sampleHandler3" />
        </list>
      </property>
    </component>

Map configuration using the map element
  In this example, map with "{key1=1, key2=2, key3=3}" in the entry is configured for the map property.

  .. code-block:: xml

    <property name="map">
      <map>
        <entry key="key1" value="1" />
        <entry key="key2" value="2" />
        <entry key="key3" value="3" />
      </map>
    </property>

  An any name can be configured for the map and the name can be referenced in the property element.
  The configuration of this example is the same as the above example.

  .. code-block:: xml

      <map name="map">
        <entry key="key1" value="1" />
        <entry key="key2" value="2" />
        <entry key="key3" value="3" />
      </map>

    <component class="sample.ListSample">
      <!-- Configure a Map named map -->
    <property name="map" ref="map">
    </component>

  An any Bean can be configured as Map value by using value-component element.

  .. code-block:: xml

    <property name="settings">
      <map>
        <entry key="sample1">
          <value-component class="sample.SampleBean1" />
        </entry>
        <entry key="sample2">
          <value-component class="sample.SampleBean2" />
        </entry>
      </map>
    </property>

.. important::
  When multiple name attributes of map or list are defined, the one defined first is valid.
  Note that this is a different behavior from :ref:`bean overwrite <repository-override_bean>`.

  To change the map or list information for each environment, change the file to be read for each environment.
  

.. _repository-autowired:

Inject components automatically
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Provide a function to automatically inject a component even if the property tag definition of the component is omitted.
Automatic injection type can be specified for this function by using autowireType attribute of the component element.

.. important::

  The following are the problems when using the automatic injection function, explicitly specifying `None` in autowireType attribute is recommended.

  * The state of the final generated object cannot be read from the component configuration file (xml).
  * If the property definition of an optional item is omitted, an object that is not expected may be automatically injected.
  * When automatic injection by type is used and object configuration of the same type are increased during derivation development,
    maintainability is poor as it requires property to be defined.

The types that can be specified for the autowireType attribute are as follows.

ByType
  Automatically injects the component if there is only one type of that property in the DI container.Inject components automatically.
  This type is is used by default.

ByName
  A component with the same name as the property name is automatically injected.
  An error occurs if the property and component type does not match.

None
  Automatic injection is not performed.

An example of automatic injection with the default (ByType) configuration is shown below.

Create an injection target class
  Create an injection target interface and implementation class.
  Although the interface is created in this example, it is not required.

  .. code-block:: java

    public interface SampleComponent {
    }

    public class BasicSampleComponent implements SampleComponent {
    }

Create a class that uses the object to be injected
  Create a class that processes using the class created above.
  This class receives the above class by setter injection.

  .. code-block:: java

    public class SampleClient {
      private SampleComponent component;

      public void setSampleComponent(SampleComponent component) {
        this.component = component;
      }
    }

Define component in component configuration file
  In this example, `sampleComponent` property is not defined in `SampleClient`, but since there is only one configuration in the class implementing \`SampleComponent`\,
  `BasicSampleComponent` is automatically configured in the `sampleComponent` property.

  .. code-block:: xml

    <component name="sampleComponent" class="sample.BasicSampleComponent" />

    <component name="sampleClient" class="sample.SampleClient" />


  The above configuration is the same as when the property is explicitly defined as given below.

  .. code-block:: xml

    <component name="sampleComponent" class="sample.BasicSampleComponent" />

    <component name="sampleClient" class="sample.SampleClient">
      <property name="sampleComponent" ref="sampleComponent" />
    </component>

.. _repository-split_xml:

Split the component configuration file (xml)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The xml file size increases significantly if all the definitions are defined in one component configuration file, which causes the problem of poor maintainability.
Therefore, a function to split the xml file into multiple files is provided.

When splitting the xml file, it is better to split the file based on functional units, etc.
The split xml file can be read using the import element.

An example is shown below.

In the following example, 3 xml files are loaded.

.. code-block:: xml

  <import file="library/database.xml" />
  <import file="library/validation.xml" />
  <import file="handler/multipart.xml" />

.. _repository-environment_configuration:

Set the dependent value
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Values (database connection information, directory path, etc.) that differ between the test and production environments can be managed in the environment configuration file.

Describe the environment configuration file in the simple key-value format as given below.
For detailed description rules, see :ref:`repository-environment_configuration_file_rule`.

.. code-block:: bash

  database.url = jdbc:h2:mem:sample
  database.user = sa
  database.password = sa

.. important::

  Note that if the key value of the environment configuration value is duplicated, the one defined later will be valid.

An example is shown below.

Environment dependent value
  .. code-block:: bash

    database.url = jdbc:h2:mem:sample
    database.user = sa
    database.password = sa

.. _repository-user_environment_configuration:

Reference environment dependent value from the component configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The environment configuration file can be read from the component configuration file (xml) and used as the configuration value of Java Beans object.

When configuring (injection) the environment dependent value for the object managed by the DI container,
describe the key value of the environment dependent value in the component configuration file by enclosing with ``${`` and ``}``.

Note that this notation cannot be used in the configuration files. (other environment dependent values cannot be referenced in the environment configuration file.)

An example is shown below.

Environment configuration file
  .. code-block:: bash

    database.url = jdbc:h2:mem:sample
    database.user = sa
    database.password = sa

Component configuration file
  Config-file element is used to read the environment configuration file.
  The file can be read by specifying the file name as in this example, or all the files under a specific directory can be read at once.

  When the name of the environment configuration file is "database.properties", "\jdbc:h2:mem:sample" is configured in the `url` of `JdbcDataSource`.

  .. code-block:: xml

    <!-- Reading the database.properties file -->
    <config-file file="database.properties" />

    <component class="org.h2.jdbcx.JdbcDataSource">
      <property name="url" value="${database.url}" />
    </component>

  There are two types of environment configuration files, config file and properties file.
  The config file is parsed by independent specifications of Nablarch, and the properties file is parsed by java.util.Properties.
  Since the config file is an independent specification of Nablarch, the properties file is recommended as the environment configuration file.

  For specifications of the environment configuration file, refer to :ref:`repository-environment_configuration_file_rule`.

.. important::

  Throws ConfigurationLoadException if a key with an environment dependent value that is not defined in the configuration file is referenced from the component configuration file.

.. _repository-overwrite_environment_configuration:

Overwrite environment dependent values using system properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Environment dependent value can be overwritten with the system property (value that can be acquired by `java.lang.System#getProperties()`).
Since the system property has priority over the value set in the environment configuration file, the configuration value can be easily overwritten with the vm option.

For example, to change the configuration value only for a specific batch application, the system property can be used to overwrite the environment dependent value.

An example is shown below.

Environment configuration file

  .. code-block:: bash

    Message= Message to be overwritten

Overwrite values with system properties
  By configuring the system property with the ``-D`` option of Java command, the value of the environment configuration file can be overwritten.
  In this example, the value of `message` is "message which will be overwritten".

  java -Dmessage= Message which will be overwritten

.. _repository-overwrite_environment_configuration_by_os_env_var:

Overwrite environment dependent values using OS environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
With the settings described below, you can override environment dependent values with OS environment variables.

How to enable overwriting by OS environment variables
  The mechanism for overriding environment dependent values is implemented by a class that implements the Externalsized :java:extdoc:`ExternalizedComponentDefinitionLoader <nablarch.core.repository.di.config.externalize.ExternalizedComponentDefinitionLoader>` interface.

  This implementation class is loaded using ``java.util.ServiceLoader``.
  If no service provider has been set, :java:extdoc:`SystemPropertyExternalizedLoader <nablarch.core.repository.di.config.externalize.SystemPropertyExternalizedLoader>` is used by default.
  This class is a class for overwriting by system properties, and the overwriting by system properties described in the previous section is implemented by this class.

  To override environment-dependent values with OS environment variables, use the :java:extdoc:`OsEnvironmentVariableExternalizedLoader <nablarch.core.repository.di.config.externalize.OsEnvironmentVariableExternalizedLoader>` as an implementation class.

  The concrete configuration is as follows:

  #. Create a directory named ``META-INF/services`` directly under the classpath
  #. In the directory created above, create a text file named ``nablarch.core.repository.di.config.externalize.ExternalizedComponentDefinitionLoader``
  #. In the file, list the fully qualified name of the implementation class to be used, separated by a new line

  For example, to use an :java:extdoc:`OsEnvironmentVariableExternalizedLoader <nablarch.core.repository.di.config.externalize.OsEnvironmentVariableExternalizedLoader>`,
  the content of the ``nablarch.core.repository.di.config.externalize.ExternalizedComponentDefinitionLoader`` is described as follows:

  .. code-block:: text

    nablarch.core.repository.di.config.externalize.OsEnvironmentVariableExternalizedLoader


  When you combine multiple implementation classes, you can also enumerate them with a line separator as shown below.

  .. code-block:: text

    nablarch.core.repository.di.config.externalize.OsEnvironmentVariableExternalizedLoader
    nablarch.core.repository.di.config.externalize.SystemPropertyExternalizedLoader

  If multiple implementation classes are specified, they are overwritten in order from the top.
  Therefore, when an environment dependent value with the same name is overwritten by each method, the class described at the bottom is finally adopted.
  In the case of the above example, a value set in a system property takes precedence over a value set in an OS environment variable.

.. _repository-overwrite_environment_configuration_by_os_env_var_naming_rule:

About the names of OS environment variables
  On Linux, you cannot use ``.`` or ``-`` in the name of the OS environment variable.
  Therefore, it is not possible to define OS environment variables to override an environment dependent value with a name like ``example.error-message``.

  In order to avoid this problem, Nablarch searches for OS environment variables after performing the following transformations to the names of environment dependent values.

  #. Replace ``.`` and ``-`` with ``_``
  #. Convert alphabet to uppercase

  That is, the environment dependent value named ``example.error-message`` can be overridden by defining an OS environment variable named ``EXAMPLE_ERROR_MESSAGE``.

  On Windows, you can use ``.`` and ``-`` as OS environment variables, but the above conversion process is performed regardless of the OS at the time of execution.
  Therefore, the OS environment variable to override ``example.error-message`` must be named ``EXAMPLE_ERROR_MESSAGE`` on Windows as well.


.. _repository-factory_injection:

Inject the object created by the factory class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If the class is implemented as Java Beans, a value can be configured using setter injection and an object can be generated.
However, there are cases where objects, which are not implemented as Java Beans such as those provided by the vendor or OSS, have to be managed in the system repository.

In this case, these classes can be managed in the system repository by creating a factory class and then creating an object through the factory class.

The procedure is shown below.

Create a factory class
  The factory class is created by implementing :java:extdoc:`ComponentFactory <nablarch.core.repository.di.ComponentFactory>`.

  Implementation examples
    .. code-block:: java

      public class SampleComponentFactory implements ComponentFactory<SampleComponent> {
        // Configuration value for the generated object
        private String configValue;

        public void setConfigValue(String configValue) {
          this.configValue = configValue;
        }

        public SampleComponent createObject() {
          // Create an object.
          // In this example, an object is created using the value that is injected
          // by the setter into this class.
          return new SampleComponent(configValue);
        }
      }

Configure the factory class in the component configuration file
  The object created by the factory class is automatically configured
  by configuring the factory class like a normal component.

  .. code-block:: xml

    <!-- Factory class definition -->
    <component name="sampleComponent" class="sample.SampleComponentFactory">
      <property name="configValue" value="Configuration value" />
    </component>

    <!-- Class that configures the object generated by the factory class -->
    <component class="sample.SampleBean">
      <!-- Object generated with factory class is configured in the sampleObject property -->
      <property name="sampleObject" ref="sampleComponent" />
    </component>

.. important::

  Nablarch does not support nesting of factory classes.
  That is, the properties of a factory class can not specify other factory classes.

  .. code-block:: xml

      <component name="sampleComponent" class="sample.SampleComponentFactory">
        <!-- Nesting of the factory class -->
        <property name="property">
          <component class="sample.OtherSampleComponentFactory">
        </property>
      </component>

  In this case, building objects within one factory class, including objects to be built in nested factory classes,
  or Create a class such as Creator/Builder/Provider to generate objects to be built in the nested factory class,
  and Corresponding to the injection as a component.

.. _repository-inject-annotation-component:

Constructing objects of annotated classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Adding :java:extdoc:`SystemRepositoryComponent <nablarch.core.repository.di.config.externalize.annotation.SystemRepositoryComponent>`
to the class allows it to be managed in DI container without having to write :ref:`the settings in XML <repository-definition_bean>`.

.. important::

  This feature is not available on some web application servers that manage the resources under the classpath in their own file system.

  For example, Jboss and Wildfly cannot search for classes annotated with the ``SystemRepositoryComponent`` annotation
  because the resources under the classpath are managed by a virtual file system called vfs.

  If such a web application server is used, the component definitions should be :ref:`defined in XML <repository-definition_bean>` as usual.

How to use
********************

Create a class to identify the packages to be collected.
  The collection of the class to which :java:extdoc:`SystemRepositoryComponent <nablarch.core.repository.di.config.externalize.annotation.SystemRepositoryComponent>`
  is assigned is handled by a class that implements the :java:extdoc:`ExternalizedComponentDefinitionLoader <nablarch.core.repository.di.config.externalize.ExternalizedComponentDefinitionLoader>`
  interface. This class is an abstract class named :java:extdoc:`AnnotationComponentDefinitionLoader <nablarch.core.repository.di.config.externalize.AnnotationComponentDefinitionLoader>`
  and has an abstract method named :java:extdoc:`getBasePackage <nablarch.core.repository.di.config.externalize.AnnotationComponentDefinitionLoader.getBasePackage()>`
  that returns the base package for the collection target.

  Override the above abstract methods so that collection is carried out in accordance with each project's package name.

  .. code-block:: java

    public class ExampleComponentDefinitionLoader extends AnnotationComponentDefinitionLoader {
        @Override
        protected String getBasePackage() {
            return "com.example";
        }
    }

Set the created class as a service provider.
  Create a file named ``nablarch.core.repository.di.config.externalize.ExternalizedComponentDefinitionLoader``
  as well as :ref:`How to enable overwriting by OS environment variables <repository-overwrite_environment_configuration_by_os_env_var>`
  to be loaded with ``java.util.ServiceLoader`` and write the fully qualified names of the above classes.

Annotate the classes to be managed in the DI container.
  By assigning :java:extdoc:`SystemRepositoryComponent <nablarch.core.repository.di.config.externalize.annotation.SystemRepositoryComponent>` to be managed in a DI container.

  .. code-block:: java

    @SystemRepositoryComponent
    public class ExampleAction {

Using the constructor injection
****************************************

:java:extdoc:`SystemRepositoryComponent <nablarch.core.repository.di.config.externalize.annotation.SystemRepositoryComponent>`
assigned classes are performed with constructor injection if they fulfill the following conditions at the time of construction.

* Only one constructor is defined
* Constructor with arguments

If the conditions are fulfilled, it is injected with the following specifications.

* Arguments assigned with :java:extdoc:`ConfigValue <nablarch.core.repository.di.config.externalize.annotation.ConfigValue>` are injected with a set value
* The argument given by :java:extdoc:`ComponentRef <nablarch.core.repository.di.config.externalize.annotation.ComponentRef>` is the component registered in the DI container is injected
* If none of the above annotations are assigned

  * If there is only one component on the DI container that matches the argument type, automatically inject that component
  * If no or multiple components matching the argument type exist on the DI container, do not inject anything

Injection of configuration values
  The value of the annotation ``value`` is injected into the constructor by assigning :java:extdoc:`ConfigValue <nablarch.core.repository.di.config.externalize.annotation.ConfigValue>`
  to the constructor argument. The available types of values are the same as :ref:`Use a string, numeric, or boolean value as the configuration value <repository-property_type>`.

  As in case :ref:`Reference environment dependent value from the component configuration file <repository-user_environment_configuration>`,
  key values of environment-dependent values can be described by enclosing them in ``${``` and ``}``.

  .. code-block:: java

    @SystemRepositoryComponent
    public class ExampleService {

        private final String errorMessageId;

        public ExampleService(@ConfigValue("${example.service.errorMessageId}") String errorMessageId) {
            this.errorMessageId = errorMessageId;
        }

Injecting components
  The component with the name of the annotation ``value`` is injected by assigning
  :java:extdoc:`ComponentRef <nablarch.core.repository.di.config.externalize.annotation.ComponentRef>` to the constructor argument.

  The following example injects a component named ``lettuceRedisClientProvider``.

  .. code-block:: java

    @SystemRepositoryComponent
    public class ExampleService {

      private LettuceRedisClient client;

      public ExampleService(@ComponentRef("lettuceRedisClientProvider") LettuceRedisClient client) {
          this.client = client;
      }

.. tip::

  The constructor injection is handled by class :java:extdoc:`ConstructorInjectionComponentCreator <nablarch.core.repository.di.config.ConstructorInjectionComponentCreator>`.
  By overriding :java:extdoc:`newComponentCreator <nablarch.core.repository.di.config.externalize.AnnotationComponentDefinitionLoader.newComponentCreator()>` in ``AnnotationComponentDefinitionLoader``,
  it can be replaced with a :java:extdoc:`ComponentCreator <nablarch.core.repository.di.ComponentCreator>`
  implementation that handles any processing at object construction time in the annotated class.

  .. code-block:: java

    public class ExampleComponentDefinitionLoader extends AnnotationComponentDefinitionLoader {
      @Override
      protected String getBasePackage() {
          return "com.example";
      }

      @Override
      protected ComponentCreator newComponentCreator() {
        // Change to any ComponentCreator implementation class.
        return new ExampleComponentCreator();
      }
    }

Managing the Action class in a DI container
************************************************************

Annotations can be assigned to the Action class to be managed in a DI container.
In the dispatch handlers (:ref:`Routing Adapter <router_adaptor>`, :ref:`Request Dispatch Handler <request_path_java_package_mapping>`, :ref:`HTTP Request Dispatch Handler <http_request_java_package_mapping>`)
provided by Nablarch, the class to be dispatched is instantiated in the dispatcher.
Therefore, when registering an Action class to the DI container, it is necessary to replace :java:extdoc:`DelegateFactory <nablarch.fw.handler.DelegateFactory>`
to obtain the dispatch target class from the system repository.
The replacement is set up using :java:extdoc:`DispatchHandler#setDelegateFactory <nablarch.fw.handler.DispatchHandler.setDelegateFactory(nablarch.fw.handler.DelegateFactory)>` as follows:

  .. code-block:: xml

    <component name="packageMapping" class="nablarch.integration.router.RoutesMapping">
      <!-- DelegateFactory to get the dispatch destination from the system repository -->
      <property name="delegateFactory">
          <component class="nablarch.fw.handler.SystemRepositoryDelegateFactory"/>
      </property>
      <!-- Other properties omitted -->
    </component>

.. _repository-initialize_object:

Initialize the object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following steps are required for the initialization process of the object.

#. Implement the :java:extdoc:`Initializable <nablarch.core.repository.initialization.Initializable>` interface.
#. Configure a list targets for initialization in the component configuration file.

The detailed procedure is shown below.

Implement Initializable interface
  Initialize with :java:extdoc:`initialize <nablarch.core.repository.initialization.Initializable.initialize()>`.

  .. code-block:: java

    public class SampleComponent implements Initializable {
      public void initialize() {
        // Initialize based on the value injected into the property
      }
    }

Configure a list targets for initialization in the component configuration file
  Configure the object to be initialized to :java:extdoc:`BasicApplicationInitializer <nablarch.core.repository.initialization.BasicApplicationInitializer>`.

  If information of the initialization order of the object to be initialized is required, configure the object that is to be initialized first to a higher order.
  For the configuration example given below, initialization is performed in the following order.
  
  #. `sampleObject1`
  #. `sampleObject3`
  #. `sampleObject2`

  .. important::
    
    Set the component name of :java:extdoc:`BasicApplicationInitializer <nablarch.core.repository.initialization.BasicApplicationInitializer>` to **initializer**.

  .. code-block:: xml

    <!-- Configure the object to be initialized -->
    <component name="sampleObject1" class="sample.SampleComponent" />
    <component name="sampleObject2" class="sample.SampleComponent2" />
    <component name="sampleObject3" class="sample.SampleComponent3" />

    <component name="initializer"
        class="nablarch.core.repository.initialization.BasicApplicationInitializer">

      <!-- List the objects to be initialized with the list element in the initializeList property-->
      <property name="initializeList">
        <list>
          <component-ref name="sampleObject1"/>
          <component-ref name="sampleObject3" />
          <component-ref name="sampleObject2" />
        </list>
      </property>

    </component>

.. _repository-dispose_object:

Handling the disposal of objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In order to perform the disposal process of an object, the following steps are required.

#. Implement the :java:extdoc:`Disposable <nablarch.core.repository.disposal.Disposable>` interface.
#. Set the list of discarded targets in the component configuration file.

Detailed steps are shown below.

Implementing the Disposable Interface
  Disposal process in :java:extdoc:`dispose <nablarch.core.repository.disposal.Disposable.dispose()>`.

  .. code-block:: java

    public class SampleComponent implements Disposable {
      public void dispose() throws Exception{
        // Release of resources, etc., for the disposal process
      }
    }

Set the list of discarded targets in the component configuration file
  Set the object to be discarded to :java:extdoc:`BasicApplicationDisposer <nablarch.core.repository.disposal.BasicApplicationDisposer>`.

  If the discard order of the objects to be discarded needs to be considered, set the objects which want to be discarded first to **down**.
  In the case of the example configuration below, the disposal process is done in the following order.

  #. `sampleObject1`
  #. `sampleObject2`
  #. `sampleObject3`

  .. important::

    The component name of :java:extdoc:`BasicApplicationDisposer <nablarch.core.repository.disposal.BasicApplicationDisposer>` must be **disposer**.


  .. code-block:: xml

    <!-- Setting up the objects to be discarded -->
    <component name="sampleObject1" class="sample.SampleComponent1" />
    <component name="sampleObject2" class="sample.SampleComponent2" />
    <component name="sampleObject3" class="sample.SampleComponent3" />

    <component name="disposer"
        class="nablarch.core.repository.disposal.BasicApplicationDisposer">

      <!-- Enumerate the objects to be discarded by the list element in the disposableList property -->
      <property name="disposableList">
        <list>
          <component-ref name="sampleObject3" />
          <component-ref name="sampleObject2" />
          <component-ref name="sampleObject1" />
        </list>
      </property>

    </component>

  The ``BasicApplicationDisposer`` has a method, :java:extdoc:`addDisposable <nablarch.core.repository.disposal.BasicApplicationDisposer.addDisposable(nablarch.core.repository.disposal.Disposable)>`,
  to which any :java:extdoc:`Disposable <nablarch.core.repository.disposal.Disposable>` can be added after the component is created.

  | The :java:extdoc:`Disposable <nablarch.core.repository.disposal.Disposable>` added in this :java:extdoc:`addDisposable <nablarch.core.repository.disposal.BasicApplicationDisposer.addDisposable(nablarch.core.repository.disposal.Disposable)>` is expected to be added in the order in which its instance was created.
  | In that case, the discard process should be done in the opposite order of instance creation (e.g., JDBC ``Connection``, ``Statement``, and ``ResultSet``).

  For this reason, :java:extdoc:`BasicApplicationDisposer <nablarch.core.repository.disposal.BasicApplicationDisposer>` calls the disposal process in the opposite order to that set in the ``disposableList``.

Set the Closeable object in the list of objects to be discarded
  If a component implements ``java.io.Closeable``, it can easily be set up in the list of discarded items by using
  :java:extdoc:`DisposableAdaptor <nablarch.core.repository.disposal.DisposableAdaptor>`

  .. code-block:: xml

    <!-- Components that implement java.io.Closeable -->
    <component name="closeableComponent" class="sample.CloseableComponent" />

    <component name="disposer"
        class="nablarch.core.repository.disposal.BasicApplicationDisposer">

      <property name="disposableList">
        <list>
          <component class="nablarch.core.repository.disposal.DisposableAdaptor">
            <!-- Set the target property of DisposableAdaptor to a component that implements Closeable -->
            <property name="target" ref="closeableComponent" />
          </component>
        </list>
      </property>

    </component>

.. _repository-use_system_repository:

Configure the DI container information to the system repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
By loading the information of the DI container into the system repository, the objects in the DI container from all points in the application can be accessed.

An example of loading and configuring the component configuration file in the system repository is shown below.

In this example, information of the DI container constructed based on ``web-boot.xml`` is configured in the system repository.

.. code-block:: java

  XmlComponentDefinitionLoader loader
      = new XmlComponentDefinitionLoader("web-boot.xml");
  SystemRepository.load(new DiContainer(loader));

.. important::

  The process of registering DI container information in the system repository is implemented by the following classes provided by Nablarch.
  Therefore, there is basically no individual implementation.

  * Implementation class of ServletContextListener
  * Launch class of independent application

.. _repository-get_object:

Get object from system repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To acquire the object from the system repository, use the class :java:extdoc:`SystemRepository <nablarch.core.repository.SystemRepository>`.

The DI container information must be configured in the system repository in advance.
For details, see :ref:`repository-use_system_repository`.

Object can be acquired by specifying the value of name attribute configured in the component element (including list and map elements) as shown below.

Component definition
  .. code-block:: xml

    <component name="sampleComponent" class="sample.SampleComponent" />

    <component name="component" class="sample.Component" >
      <property name="component2">
        <component name="component2" class="sample.Component2" />
      </property>
    </component>

Acquisition example
  .. code-block:: java

    // Get using SystemRepository#get.
    SampleComponent sample = SystemRepository.get("sampleComponent");

    // Obtain nested component by concatenating the parent name and its own name with ".".
    Component2 component2 = SystemRepository.get("component.component2");

.. _repository-environment_configuration_file_rule:

Rules for describing environment configuration file
------------------------------------------------------
There are two types of environment configuration files, config file and properties file. The description rules of each environment configuration file are explained.

Specifications of properties file
  Analyzed based on the Java Properties specifications.

config file specifications
  The specifications of the config file are described below.

  Description format of setting value
    The configuration value is described by separating the key and value with ``=``.

    .. code-block:: bash
    
      key1=value1
      key2=value2

  Comment description
    Only line comments using ``#`` is supported.
    If ``#`` is present in a line, the rest of the line is considered as a comment.

    .. code-block:: bash

      # This is a comment
      key = value   # This is a comment

  Description of configuration values that spans multiple lines
    By using ``\`` at the end of the line, the configuration value can be described over multiple lines.

    In the case of the example below, the combinations of configuration values are as follows.

    * key -> value
    * key2 -> value,value2
    * key3 -> abcdefg

    .. code-block:: bash

      key = value
      key2 = value,\
      value2
      key3 = abcd\    # Comments can be defined here
      efg

  Reserved word escape
    ``\`` is used to escape when handling the following reserved words as general characters.

    * ``#``
    * ``=``
    * ``\``

    In the case of the example below, the combinations of configuration values are as follows.

    * key -> a=a
    * key2 -> #This is not a comment
    * key3 -> a\\b

    .. code-block:: bash

      key = a\=a
      key2 = \# This is not a comment
      key3 = a\\b

.. tip::

  Only the value of half-width space is not supported in the config file, but it can be handled by configuring the numeric reference character in the properties file.

  .. code-block:: bash

    key = \u0020

.. tip::

  Empty value is not supported in the config file, but it is treated as an empty character in the properties file.
   Therefore, care must be taken when referring to environment-dependent values from the component configuration file because the behavior is different.

  In the case of the following component definition, describe the behavior of the config and properties files.
  
  * If the configuration file is a config file, ``config.value`` does not exist and an exception will be thrown.(※)  
  * If the configuration file is a properties file, the ``property`` of the component is set to an empty string.

  .. code-block:: xml

    <property name="property" value="${config.value}" />

  .. code-block:: bash

    # empty value
    config.value=

  ※Prior to Nablarch5u18, if the configuration value does not exist, no exception will be thrown, and a WARNING level log will be output and ``property`` will be set to the string "${config.value}".
