.. _nablarch_policy:

Basic Policy
============================

This chapter describes the basic policy of the Nablarch application framework.

.. contents:: Table of contents
  :depth: 3
  :local:

.. _nablarch_architecture-no_input:

Handling of values received from outside that are not entered
-------------------------------------------------------------------
The application accepts various data including values not entered received from outside.
There are generally 2 ways of expressing non-input values: ``null`` and empty string.
If application developers need to be aware of the 2 ways of expression, implementation errors are likely to occur, which may cause unexpected failures.
To avoid this problem, the handling of null values must be unified.

To unify the expression of non-input values, Nablarch converts the non-input values to  ``null`` . 
For example, the non-input values of external data, such as HTTP request parameters or XML, are converted to ``null`` . 
Also, when null is output to the outside as a custom tag or formatted output, the value is converted to a value that indicates ``null`` according to the output data format. 
Since the conversion is performed by Nablarch handler or library, there is no need for the application to convert the non-input values.
However, :ref:`normalize_handler` must be added to the handler queue to convert non-input values to ``null`` .

The application develops non-input values as ``null`` in accordance with this policy.

APIs that return a collection or array do not return null in principle
-----------------------------------------------------------------------------------
When the target data does not exist, an API that returns a collection or array provided by Nablarch basically returns an empty collection or array instead of ``null`` . 
As a result, this can prevent bugs caused by ``null`` reference in the caller and improve readability by reducing branches.

For example, when the database search results are displayed in the list format in view (JSP), looping without determining ``null`` improves the code readability. 
If ``null`` must be considered, there will be a lot of useless code, such as branches in JSP or filling the request scope in the server with a ``null`` collection. 
This also makes implementation errors more likely to occur.

APIs that specify and get identifiers such as HTTP request parameters return ``null`` instead of an empty array.

Nablarch does not throw checked exceptions
--------------------------------------------------
All APIs in Nablarch throw only unchecked exceptions.In addition, all exception classes defined in Nablarch are unchecked exceptions.
By making all exceptions unchecked, the application is not required to be aware of exceptions, and handlers can perform common exception process.

Incidentally, checked exceptions have the following disadvantages.

* If exceptions are not caught or listed in ``throws`` , compile errors will occur. 
  If an exception is caught, similar exception process must be implemented throughout.
  
* The application code is affected whenever more exceptions are thrown. 
  The effects are wide-ranging, such as ``throws`` have to be added in all methods up to the method that catches the exceptions.

Logs and exception messages should be unified in English
------------------------------------------------------------------
Since Nablarch is intended for use outside of Japan as well, all logs and exception messages are in English. 
Nablarch does not provide a function to change the output log and exception messages to a language other than English.
  
The SQL issued by Nablarch can be changed by replacing the components
----------------------------------------------------------------------------
Nablarch has an interface defined for the components accessing the database, allowing the implementation to be replaced. 
This is because an implementation class is created in the project to replace the components in the configuration file so that the SQL issued can be changed.

Thus, for example, adding or deleting the columns of a table used by Nablarch can be supported by replacing the components.

To change the default table or column name, a new class need not be created. Simply modify the configuration file.

OSS is not used
--------------------------------------------------
As we want to respond and release quickly when a critical bug or vulnerability is found, the production code of Nablarch does not use OSS.

For code having advantage by using OSS, components that can use OSS as an :ref:`adaptor` are provided, and they should be adopted according to the project requirements.

Throws a cause exception when multiple exceptions occur
--------------------------------------------------------------
Multiple exceptions occur when an exception is thrown during the process, and another exception is thrown during the subsequent processes.
In that case, Nablarch throws a cause exception since a cause exception is important to solve the problem.
Any information other than the cause exception will be output to the WARNING log so that the information of other exceptions can also be used to investigate the problem.

Thread-safe
--------------------------------------------------
The functionality provided by Nablarch is basically thread-safe.
This is because Nablarch uses an architecture in which each thread executes a handler on the handler queue to process a request. For more information about architecture, see :ref:`the architecture chapter <nablarch_architecture>` .
This ensures that a request can be safely processed and the result returned to the client even on a platform where each thread processes a request from the client, such as a web application.

Since the object on the :ref:`repository` is a singleton, it must be thread-safe.

.. tip::

  Thread-unsafe functions (for example, database connection, etc.) have been specified on Javadoc as thread-unsafe.

Compliant with Java17
--------------------------------------------------
Nablarch production code is compliant with Java17 and does not use the APIs provided in Java18 or later.

This is to maintain backward compatibility for existing Nablarch 6 implementation projects.

When developing an application that uses Nablarch, Java17 or a later version can be used, 
and APIs provided in Java18 or later can also be used without any problem.

.. _nablarch_architecture-backward_compatible:

APIs that may be used in the application
--------------------------------------------------

Nablarch defines APIs that are supposed to be essential for application development as public APIs. 
A public API is assigned the :java:extdoc:`Published<nablarch.core.util.annotation.Published>`  annotation, which shows the classes and methods that are public APIs.

Public APIs are APIs used by the application to maintain backward compatibility during version upgrades and ensure that modifications are not made to the application. 
However, in some cases it is not possible to maintain backward compatibility when dealing with critical bug and vulnerabilities.

Heap shortage when converting from a string to BigDecimal
------------------------------------------------------------------
The following problems may occur if an exponential expression (for example, a value such as ``9e100000`` ) is specified when converting from a string to BigDecimal:

* An exceptionally large string is generated and the heap is compressed when calling :java:extdoc:`BigDecimal#toPlainString() <java.math.BigDecimal.toPlainString()>`
* An exceptionally large string is generated and the heap is compressed when formatting with :java:extdoc:`DecimalFormat <java.text.DecimalFormat>`

For this reason, Nablarch uses  :java:extdoc:`BigDecimal#scale <java.math.BigDecimal.scale()>` to check the number of digits when converting from a string to a BigDecimal, and a large value from being imported that can burden the heap. 
This function allows the range of the allowable scale to be from ``-9999`` to ``9999``, and an exception is thrown to prevent the heap from being burdened when attempting to convert an exponential value that exceeds this range.

The range of the allowable scale can be changed in the configuration.
The configuration is specified in the environment configuration file of the system repository function.
For information on the configuration method, see :ref:`repository-environment_configuration`.

For example, to set the allowable range from ``-10`` to ``10``, add the following configuration.

.. code-block:: properties

  nablarch.max_scale=10

Deprecated API
------------------------------------------------------------------
Nablarch deprecates the following APIs by adding the :java:extdoc:`@Deprecated <java.lang.Deprecated>` annotation.

* Class moved to another package

  If a class is moved to another package for the convenience of the Nablarch team, the class before the move is deprecated. 
  It is described in Javadoc that the destination class should be used.

  Since the class before the move delegates all processes to the class after the move, operation is guaranteed even if the class before the move is used. 
  However, since methods are not added, using the destination class is preferred.

* Classes and methods that have bugs or security issues

  Classes with bugs or security issues are deprecated. 
  The reasons and alternative APIs to use, as well as the method to implement them are described in Javadoc.

  It is essential to refer to Javadoc and use the APIs to resolve bugs or security issues.

  .. important::

   Basically, bugs and vulnerabilities must be fixed to resolve problems.
   However, an API with a problem may be left deprecated for the purpose of maintaining class structure restrictions or backward compatibility.
   If left as a deprecated API, support will not be provided even if a new bug is identified.
   Therefore, measures to use the new API that has resolved the problem must be taken in the application.

.. tip::

  APIs for which the use of alternative functions have been recommended in this document are not deprecated APIs (assigned  :java:extdoc:`@Deprecated <java.lang.Deprecated>` ). 
  This is because these APIs (functions) can be used without any issues, and even if any bugs are identified, support will be provided during a version upgrade.

  
