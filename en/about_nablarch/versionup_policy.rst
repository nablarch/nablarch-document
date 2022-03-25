.. _`versionup_policy`:

Nablarch upgrade policy
==================================================

.. |br| raw:: html

  <br />

.. contents:: Table of Contents
  :depth: 3
  :local:

This section describes the upgrade policy for the content provided by Nablarch.

.. _`versionup_policy-release_type`:

Release unit
----------------------------------------------
Nablarch releases in units called versions.
A version consists of a combination of multiple modules.

.. list-table:: Nablarch release units
  :header-rows: 1
  :class: white-space-normal
  :widths: 40 20 20 20

  * - Module Example
    - Nablarch5
    - Nablarch5u1
    - Nablarch5u2

  * - nablarch-fw
    - 1.0.0
    - 1.0.1
    - 1.0.2

  * - nablarch-common-dao
    - 1.0.0
    - 1.1.0
    - 1.1.0

  * - nablarch-fw-jaxrs
    - －
    - －
    - 1.0.0

In the above table, 5/5u1/5u2 are the release versions of Nablarch.

.. _`versionup_policy-versionup_type`:

Types of upgrades
----------------------------------------------
There are three types of Nablarch version upgrades.

.. list-table:: Types of upgrades
  :header-rows: 1
  :class: white-space-normal
  :widths: 20 40 28 18

  * - Type
    - Description
    - Content to be updated
    - release cycle

  * - Minor upgrade
    - Make changes to the application framework that involve large-scale feature additions or functional changes. |br|
      |br|
      e.g., Renewal of the execution control platform
    - Application framework |br|
      Extension component |br|
      Development tools |br|
      Development standard |br|
      Implementation Examples
    - 1 year ~

  * - Revision up
    - Fix bugs, add/change functions. |br|
      |br|
      e.g., Follow the latest version of Java, Addition/change of development standard |br|
    - Same as above
    - Half year [#release_schedule_for_bugs_revision_up]_
  * - Bug fix
    - Fix bugs in highly urgent application frameworks that have a fatal impact on security and operational levels.
    - Application framework
    - As needed  [#release_schedule_for_bugs_bug_fix]_


.. [#release_schedule_for_bugs_revision_up] For bugs, we will determine the scope of impact, determine the release schedule, and release it.
.. [#release_schedule_for_bugs_bug_fix] We will fix bugs immediately after detecting.

.. _`versionup_policy-product_version_number`:

Version numbering system
----------------------------------------------
The version numbering system is as follows.

 .. code-block:: html

  (product version number)u(update number)

 e.g., 5(initial release of product version 5), 5u1(Update release 1 of product version 5)

 Product Version Number
  Incremented at minor upgrade. |br|
  e.g., Nablarch 5u6 → Nablarch 6 |br|
  The starting number is 5.

 Update Number
  Incremented at revision up or bug fix. |br|
  e.g., Nablarch 5u6 → Nablarch 5u7 |br|
  The starting number is 0. However, if the number is 0, no update number will be given.

.. _`versionup_policy-backward_compatibility_policy`:

Backward compatibility policy
----------------------------------------------
Describes the backward compatibility policy of Nablarch.

Extent to which backward compatibility is maintained
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Version upgrades of the Application Framework and Testing Framework (hereinafter referred to as the "Frameworks") shall maintain backward compatibility
as described in the section on :ref:`versionup_policy-backward_compatibility_contents` ,
except in cases where :ref:`versionup_policy-backward_compatibility_is_not_maintained`.

.. important::
 This backward compatibility policy covers the public APIs defined by Nablarch among the framework's APIs.
 The public APIs defined by Nablarch are those with the :java:extdoc:`Published <nablarch.core.util.annotation.Published>` annotation.
 When all APIs of a class are published, the :java:extdoc:`Published <nablarch.core.util.annotation.Published>`
 annotation is added to the class declaration, and when individual methods are published,
 the :java:extdoc:`Published <nablarch.core.util.annotation.Published>` annotation is added to the method declaration.
 An API without the Published annotation is a unauthorized  API.

 **Do not use the unauthorized  API in your project as the unauthorized API may be upgraded without maintaining backward compatibility.**
 **If you use unauthorized  APIs in your project, backward compatibility will not be maintained when upgrading, and unexpected problems may occur.**

 Nablarch provides a tool to detect the use of unauthorized APIs.
 Please use this tool in your project to prevent the use of unauthorized APIs.
 For more information on the tool, see :ref:`api-analysis`.

.. tip::
  When giving Published annotations, we categorize them into those for architects and those for application programmers.

  * Public API for architects → @Published(tag = "architect")
  * Public API for application programmers → @Published

  Since both are public APIs and backward compatibility is maintained, there is no problem in exposing the public API for architects to application programmers at the project's discretion.

.. tip::

 Content other than frameworks is not subject to backward compatibility.

 What does it mean to maintain backward compatibility of documents?
 Do you want to keep the description of the old version of the framework?
 But even if you don't do that, you can solve it by looking at the old version of the documentation.
 The same is true for development standards.
 The Nablarch tool can also be solved by using the development tool for that version if you are using an older version of the design document.
 It may also have its own customizations.
 In this case, even if the API is backward compatible, it needs to be dealt with individually.

 As you can see, content other than frameworks does not need to be, so it is excluded from maintaining backward compatibility.

.. _`versionup_policy-backward_compatibility_contents`:

Contents of backward compatibility maintenance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
We will upgrade Nablarch with backward compatibility in mind so that the work that occurs when upgrading Nablarch is as small as possible.

This backward compatibility policy is as follows When the framework is upgraded, consideration will be given to avoid the following as much as possible.

* Modification of existing application code.
* Modification of existing automated test code.
* Modification of existing automated test data.

Considering this backward compatibility policy, the framework can basically be upgraded by simply :ref:`beforefirstStepSpecityNablarchVer` and changing the configuration file.

.. _`versionup_policy-backward_compatibility_is_not_maintained`:

Backward compatibility exception
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If any of the following applies, we may upgrade the version so that backward compatibility is not maintained.

* When changing the level or wording of the log output by the framework.
* When a framework bug is detected and cannot be fixed while maintaining backward compatibility.
* When a problem occurs due to a version upgrade of JDK, which is the environment in which the framework operates, and it cannot be fixed while maintaining backward compatibility.

If we make changes that don't maintain backward compatibility, we'll explain what they're doing and how to deal with them in the "Impact on the system and how to deal with it(システムへの影響の可能性の内容と対処)" section of the `Release Notes(Japanese Page) <https://nablarch.github.io/docs/LATEST/doc/releases/index.html>`_.

