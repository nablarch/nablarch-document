.. _ntf_junit5_extension:

========================================
 Extensions for JUnit 5
========================================

.. contents:: Table of Contents
  :depth: 3
  :local:

---------
Overview
---------

This section describes the extensions for using the automated testing framework in tests written in JUnit 5.
By using this extension, you can combine the useful features provided by JUnit 5 such as parameterized tests with the automated testing framework.

.. tip::
  There is no need to modify the tests of the existing the automated testing framework written in JUnit 4 when this extension is introduced.
  Tests written in JUnit 4 can continue to run on JUnit 5 by using JUnit Vintage (see :ref:`run_ntf_on_junit5_with_vintage_engine` for information on how to use JUnit Vintage to run an automated testing framework).
  Therefore, you can leave tests written in JUnit 4, and write new tests in JUnit 5, 

-------------
Prerequisite
-------------

In order to use JUnit 5, the following conditions must be met.

* maven-surefire-plugin must be 2.22.0 or higher

This page assumes that you have basic knowledge of how to introduce JUnit 5 and how to create test cases, so it does not describe these procedures.
For more information about JUnit 5 itself, see `the official user guide (external site) <https://junit.org/junit5/docs/5.8.2/user-guide/>`_.

---------------
Module list
---------------

.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-testing-junit5</artifactId>
    <scope>test</scope>
  </dependency>

.. _ntf_junit5_extension_standard_usages:

---------------
Basic usage
---------------

The automated testing framework provides classes that implement the functionality required for testing, such as :java:extdoc:`TestSupport <nablarch.test.TestSupport>`.
In JUnit 4, in order to use the functionality of the classes provided by the automated testing framework in your test classes, your test classes had to inherit from these classes.

This extension provides a mechanism to generate instances of the classes provided by the automated testing framework on the extension side and inject them into the test classes.
This mechanism makes use of the JUnit 5 `Extension (external site) <https://junit.org/junit5/docs/5.8.2/user-guide/#extensions>`_.

In this extension, **Extension classes** and **Composed annotations** are provided for each class provided by the automated testing framework.
For example, :java:extdoc:`TestSupportExtension <nablarch.test.junit5.extension.TestSupportExtension>` and :java:extdoc:`NablarchTest <nablarch.test.junit5.extension.NablarchTest>` are provided for :java:extdoc:`TestSupport <nablarch.test.TestSupport>`.

.. tip::
  Composed annotation is a feature provided by JUnit 5 that allows you to combine the settings of multiple annotations into one annotation.
  For more information, see `"2.1.1. Meta-Annotations and Composed Annotations" in the official guide (external site) <https://junit.org/junit5/docs/5.8.2/user-guide/#writing-tests-meta-annotations>`_.


By using these classes and implementing them as follows, :java:extdoc:`TestSupport <nablarch.test.TestSupport>` can be used in tests.

.. code-block:: java

  // 1. Set the corresponding composed annotation to the test class
  @NablarchTest
  class YourTest {
      // 2. Declare the field of class to be used in the test class.
      TestSupport support;

      @Test
      void test() {
          ...
          // 3. Use in tests
          Map<String, String> map = support.getMap(sheetName, id);
          ...
      }
  }

When using :java:extdoc:`TestSupport <nablarch.test.TestSupport>` in a test class, first set the corresponding composed annotation (:java:extdoc:`NablarchTest <nablarch.test.junit5.extension.NablarchTest>`) in the test class.
This will cause :java:extdoc:`TestSupportExtension <nablarch.test.junit5.extension.TestSupportExtension>` to be applied to the test class.

Next, declare an instance field of type :java:extdoc:`TestSupport <nablarch.test.TestSupport>` in the test class.
The visibility of the instance field can be anything.

The extension creates an instance of the corresponding class (in this case :java:extdoc:`TestSupport <nablarch.test.TestSupport>`) before executing the test.
Then, when it finds a field that can be assigned to the test class, it automatically injects an instance.

.. warning::

  Don't set any value to the field, because the extension will terminate in error if the field it be injected is not null.

----------------------------------------------------
List of Extension classes and composed annotations
----------------------------------------------------

This extension provides the following Extension classes and composed annotations.

.. list-table:: List of Extension classes and composed annotations
   :header-rows: 1

   * - Classes provided by the automated testing framework
     - Extension classes
     - Composed annotations
   * - :java:extdoc:`TestSupport <nablarch.test.TestSupport>`
     - :java:extdoc:`TestSupportExtension <nablarch.test.junit5.extension.TestSupportExtension>`
     - :java:extdoc:`NablarchTest <nablarch.test.junit5.extension.NablarchTest>`
   * - :java:extdoc:`BatchRequestTestSupport <nablarch.test.core.batch.BatchRequestTestSupport>`
     - :java:extdoc:`BatchRequestTestExtension <nablarch.test.junit5.extension.batch.BatchRequestTestExtension>`
     - :java:extdoc:`BatchRequestTest <nablarch.test.junit5.extension.batch.BatchRequestTest>`
   * - :java:extdoc:`DbAccessTestSupport <nablarch.test.core.db.DbAccessTestSupport>`
     - :java:extdoc:`DbAccessTestExtension <nablarch.test.junit5.extension.db.DbAccessTestExtension>`
     - :java:extdoc:`DbAccessTest <nablarch.test.junit5.extension.db.DbAccessTest>`
   * - :java:extdoc:`EntityTestSupport <nablarch.test.core.db.EntityTestSupport>`
     - :java:extdoc:`EntityTestExtension <nablarch.test.junit5.extension.db.EntityTestExtension>`
     - :java:extdoc:`EntityTest <nablarch.test.junit5.extension.db.EntityTest>`
   * - :java:extdoc:`BasicHttpRequestTestTemplate <nablarch.test.core.http.BasicHttpRequestTestTemplate>`
     - :java:extdoc:`BasicHttpRequestTestExtension <nablarch.test.junit5.extension.http.BasicHttpRequestTestExtension>`
     - :java:extdoc:`BasicHttpRequestTest <nablarch.test.junit5.extension.http.BasicHttpRequestTest>`
   * - :java:extdoc:`HttpRequestTestSupport <nablarch.test.core.http.HttpRequestTestSupport>`
     - :java:extdoc:`HttpRequestTestExtension <nablarch.test.junit5.extension.http.HttpRequestTestExtension>`
     - :java:extdoc:`HttpRequestTest <nablarch.test.junit5.extension.http.HttpRequestTest>`
   * - :java:extdoc:`RestTestSupport <nablarch.test.core.http.RestTestSupport>`
     - :java:extdoc:`RestTestExtension <nablarch.test.junit5.extension.http.RestTestExtension>`
     - :java:extdoc:`RestTest <nablarch.test.junit5.extension.http.RestTest>`
   * - :java:extdoc:`SimpleRestTestSupport <nablarch.test.core.http.SimpleRestTestSupport>`
     - :java:extdoc:`SimpleRestTestExtension <nablarch.test.junit5.extension.http.SimpleRestTestExtension>`
     - :java:extdoc:`SimpleRestTest <nablarch.test.junit5.extension.http.SimpleRestTest>`
   * - :java:extdoc:`IntegrationTestSupport <nablarch.test.core.integration.IntegrationTestSupport>`
     - :java:extdoc:`IntegrationTestExtension <nablarch.test.junit5.extension.integration.IntegrationTestExtension>`
     - :java:extdoc:`IntegrationTest <nablarch.test.junit5.extension.integration.IntegrationTest>`
   * - :java:extdoc:`MessagingReceiveTestSupport <nablarch.test.core.messaging.MessagingReceiveTestSupport>`
     - :java:extdoc:`MessagingReceiveTestExtension <nablarch.test.junit5.extension.messaging.MessagingReceiveTestExtension>`
     - :java:extdoc:`MessagingReceiveTest <nablarch.test.junit5.extension.messaging.MessagingReceiveTest>`
   * - :java:extdoc:`MessagingRequestTestSupport <nablarch.test.core.messaging.MessagingRequestTestSupport>`
     - :java:extdoc:`MessagingRequestTestExtension <nablarch.test.junit5.extension.messaging.MessagingRequestTestExtension>`
     - :java:extdoc:`MessagingRequestTest <nablarch.test.junit5.extension.messaging.MessagingRequestTest>`

Supplemental information on using BasicHttpRequestTest
=========================================================

Except for :java:extdoc:`BasicHttpRequestTestTemplate <nablarch.test.core.http.BasicHttpRequestTestTemplate>`, you can use it in the way described in :ref:`ntf_junit5_extension_standard_usages`. It can be used in the way described in :ref:`ntf_junit5_extension_standard_usages`.

Only :java:extdoc:`BasicHttpRequestTestTemplate <nablarch.test.core.http.BasicHttpRequestTestTemplate>` needs to specify parameters when using :java:extdoc:`BasicHttpRequestTest <nablarch.test.junit5.extension.http.BasicHttpRequestTest>`, which is a composed annotation, so we will supplement it.

.. code-block:: java

  // 1. Specify the baseUri of BasicHttpRequestTest
  @BasicHttpRequestTest(baseUri = "/test/")
  class YourTestClass {
      // 2. The method of injecting BasicHttpRequestTestTemplate is the same as the others.
      BasicHttpRequestTestTemplate support;

      @Test
      void test() {
          support.execute();
      }
  }

The :java:extdoc:`BasicHttpRequestTest <nablarch.test.junit5.extension.http.BasicHttpRequestTest>` annotation needs to set the ``baseUri``.
This value corresponds to the value returned by the ``getBaseUri()`` method of :java:extdoc:`AbstractHttpRequestTestTemplate <nablarch.test.core.http.AbstractHttpRequestTestTemplate>`.

-------------------------
Add your own extensions
-------------------------

Describe how to extend the classes provided by the automated testing framework.

.. tip::
  The procedure described here can also be applied to existing your own extension classes written in JUnit 4.

When creating your own extension classes, the following are the major steps to take.

#. Inherit the classes provided by the automated testing framework and create your own extended classes
#. Create the Extension for your own extension that inherits from the Extension corresponding to the class from which it inherits, and implement it to create an instance of your own extension class.
#. Apply the Extension for your own extension to the test class using the ``ExtendWith`` annotation.

Create your own extension class
==================================

In this section, we will use the case of creating a class that extends :java:extdoc:`TestSupport <nablarch.test.TestSupport>` as an example.

First, create your own extension class that inherits from :java:extdoc:`TestSupport <nablarch.test.TestSupport>`.

.. code-block:: java

  public class CustomTestSupport extends TestSupport {
      // Implement the constructor to pass the Class instance of the test class to TestSupport.
      public CustomTestSupport(Class<?> testClass) {
          super(testClass);
      }

      // Implement your own extension methods
  }

Basically, the classes provided by the automated testing framework need to be passed the ``Class`` object of the test class when instantiating.
Therefore, you need to define a constructor of your own extension class that can accept ``Class`` objects of the test class.

.. tip::
  :java:extdoc:`SimpleRestTestSupport <nablarch.test.core.http.SimpleRestTestSupport>` can be used without passing a ``Class`` object of the test class to the constructor.

Create the Extension for your own extension
============================================

Next, create the Extension for your own extension by inheriting from the Extension class corresponding to the extension source class.

In the example, since it inherits from :java:extdoc:`TestSupport <nablarch.test.TestSupport>`, the corresponding Extension class will be :java:extdoc:`TestSupportExtension <nablarch.test.junit5.extension.TestSupportExtension>`.

.. tip::
  If you use your own extension class that directly inherits from :java:extdoc:`AbstractHttpRequestTestTemplate <nablarch.test.core.http.AbstractHttpRequestTestTemplate>`, you can use :java:extdoc:`BasicHttpRequestTestExtension <nablarch.test.junit5.extension.http.BasicHttpRequestTestExtension>` as the corresponding Extension.


.. code-block:: java

  public class CustomTestSupportExtension extends TestSupportExtension {
  
      // Override createSupport() and implement it to return an instance of your own extension class
      @Override
      protected TestEventDispatcher createSupport(Object testInstance, ExtensionContext context) {
          return new CustomTestSupport(testInstance.getClass());
      }
  }

Override ``createSupport()`` method in the Extension for your own extension.
Then, implement it so that it returns an instance of the your own extension class you just created.

Note that instances of your own extension class created by the ``createSupport()`` method are stored in the ``support`` instance field of :java:extdoc:`TestEventDispatcher <nablarch.test.event.TestEventDispatcher>` type defined in the parent class :java:extdoc:`TestEventDispatcherExtension <nablarch.test.junit5.extension.event.TestEventDispatcherExtension>`.
This field is ``protected``, so it can be referenced by subclasses.

Applying to the test class with ExtendWith
===========================================

The Extension for your own extension can be applied to the test class using the ``ExtendWith`` annotation.
An example implementation is shown below.

.. code-block:: java

  ..
  import org.junit.jupiter.api.extension.ExtendWith;
  
  // 1. ExtendWith to apply the Extension for your own extension to the test class
  @ExtendWith(CustomTestSupportExtension.class)
  class YourTest {
      // 2. Declare an instance field of your own extension class.
      CustomTestSupport support;

      @Test
      void test() {
          // 3. Use your own extension classes in your tests
          support.customMethod();
      }
  }

When extending BasicHttpRequestTestTemplate, also create annotations
======================================================================

When extending :java:extdoc:`BasicHttpRequestTestTemplate <nablarch.test.core.http.BasicHttpRequestTestTemplate>` or :java:extdoc:`AbstractHttpRequestTestTemplate <nablarch.test.core.http.AbstractHttpRequestTestTemplate>`, it is necessary to pass ``baseUri`` to an instance of your own extension class.
Since ``ExtendWith`` has no parameters other than the Extension class, you need to create your own annotations as well.

The following is an example of implementation in :java:extdoc:`BasicHttpRequestTestTemplate <nablarch.test.core.http.BasicHttpRequestTestTemplate>`.

.. code-block:: java

  public class CustomHttpRequestTestSupport extends BasicHttpRequestTestTemplate {
      private final String baseUri;
     
      // Implement baseUri so that it can be passed from outside.
      public CustomHttpRequestTestSupport(Class<?> testClass, String baseUri) {
          super(testClass);
          this.baseUri = baseUri;
      }
  
      @Override
      protected String getBaseUri() {
          return baseUri;
      }
  }

First, create your own extension class by inheriting from :java:extdoc:`BasicHttpRequestTestTemplate <nablarch.test.core.http.BasicHttpRequestTestTemplate>`.
The constructor needs to have the parameters the Class instance of the test class and ``baseUri``.

Next, create a composed annotation for your own extension class.

.. code-block:: java

  import org.junit.jupiter.api.extension.ExtendWith;
  
  import java.lang.annotation.ElementType;
  import java.lang.annotation.Retention;
  import java.lang.annotation.RetentionPolicy;
  import java.lang.annotation.Target;
  
  @Retention(RetentionPolicy.RUNTIME)
  @Target(ElementType.TYPE)
  // Specify the Extension for your own extension to be created later.
  @ExtendWith(CustomHttpRequestTestExtension.class)
  public @interface CustomHttpRequestTest {
      // Declare the baseUri
      String baseUri();
  }

In the composed annotation, declare ``baseUri`` so that it can be passed.
The Extension for your own extension specified by ``ExtendWith`` are implemented as follows.

.. code-block:: java

  public class CustomHttpRequestTestExtension extends BasicHttpRequestTestExtension {
  
      @Override
      protected TestEventDispatcher createSupport(Object testInstance, ExtensionContext context) {
          // Obtaining annotation information from the test class
          CustomHttpRequestTest annotation = findAnnotation(testInstance, CustomHttpRequestTest.class);
          // Pass the baseUri information to the constructor of your own extension class
          return new CustomHttpRequestTestSupport(testInstance.getClass(), annotation.baseUri());
      }
  }

The ``findAnnotation(Object, Class)`` can be used to obtain information about annotations set in the test class.
This allows you to pass the value of ``baseUri`` to your own extension class.

Finally, you can use your own extension class that inherits from :java:extdoc:`BasicHttpRequestTestTemplate <nablarch.test.core.http.BasicHttpRequestTestTemplate>` by implementing it as follows using your own composed annotation.

.. code-block:: java

  // Set your own composed annotation to the test class (also set baseUri)
  @CustomHttpRequestTest(baseUri = "/custom/")
  class YourTest {
      // Declare the fields of your own extension class
      CustomHttpRequestTestSupport support;
  
      @Test
      void test() {
          // Use your own extension class in Tests
          support.customMethod();
      }
  }

Implementing pre-processing and post-processing
================================================

In the Extension for your own extension, you can implement pre-processing and post-processing of tests by overriding the following methods.

* beforeAll
* beforeEach
* afterAll
* afterEach

In ``beforeAll`` and ``afterAll``, you can implement pre-processing and post-processing for the entire test class.
And with ``beforeEach`` and ``afterEach``, you can implement pre-processing and post-processing for each test method.

When overriding each method, it is always necessary to execute the same method of the parent class as follows.
If not, the pre-processing and post-processing defined in the parent class will not be called.

.. code-block:: java

  @Override
  public void beforeAll(ExtensionContext context) {
      // Always execute the parent's method first.
      super.beforeAll(context);

      // Implement your own pre-processing
      ...
  }

Reproducing the TestRule of JUnit 4
====================================

If you have your own extension class created in an existing project, and it uses the ``TestRule`` of JUnit 4, this section explains how to port it to this extension.

For example, suppose that the following your own extension class exists.

.. code-block:: java

  import org.junit.Rule;
  import org.junit.rules.Timeout;
  import java.util.concurrent.TimeUnit;
  
  public class CustomTestSupport extends TestSupport {
      // Using the TestRule of JUnit 4
      @Rule
      public Timeout timeout = new Timeout(1000, TimeUnit.MILLISECONDS);
  
      public CustomTestSupport(Class<?> testClass) {
          super(testClass);
      }
  }

When porting this to this extension, the Extension for your own extension is implemented as follows.

.. code-block:: java

  public class CustomTestSupportExtension extends TestSupportExtension {
  
      @Override
      protected TestEventDispatcher createSupport(Object testInstance, ExtensionContext context) {
          return new CustomTestSupport(testInstance.getClass());
      }
  
      // 1. Override the resolveTestRules method
      @Override
      protected List<TestRule> resolveTestRules() {
          // 2. Generate a list based on the result of resolveTestRules() of the parent class
          List<TestRule> rules = new ArrayList<>(super.resolveTestRules());
          // 3. Add the TestRule defined in your own extension class to the list
          rules.add(((CustomTestSupport) support).timeout);
          // 4. Return the generated list
          return rules;
      }
  }

In the Extension for your own extension, you can override the method ``resolveTestRules()``.
Implement this method to return a list of the ``TestRules`` of JUnit 4 that you want to reproduce.
This allows you to reproduce  ``TestRule`` of JUnit 4 on JUnit 5 tests.

Note that overriding ``resolveTestRules()`` should always be based on the list returned by the parent class ``resolveTestRules()``.
If not, the ``TestRule`` registered in the parent class will not be reproduced.


-------------------------------
Using with RegisterExtension
-------------------------------

JUnit 5 provides a mechanism called RegisterExtension to programmatically create an instance of Extension and apply it to a test class.

.. tip::
  For an explanation of RegisterExtension, see `"5.2.2. Programmatic Extension Registration" in the Official Guide (external site) <https://junit.org/junit5/docs/5.8.2/user-guide/#extensions-registration-programmatic>`_.

The Extensions provided by this extension can also be used with RegisterExtension.
However, in such a case, it must be used in a static field.
If used in an instance field, ``beforeAll`` and ``afterAll`` will not be executed, and the Extension will not work properly.

An example of implementation is shown below.

.. code-block:: java

  class YourTest {
      // 1. Use RegisterExtension in static fields
      @RegisterExtension
      static TestSupportExtension extension = new TestSupportExtension();
  
      // 2. Declare the instance field of the class provided by the automated testing framework
      TestSupport support;
  
      @Test
      void test() {
          // 3. Using support in tests
          ...
      }
  }

