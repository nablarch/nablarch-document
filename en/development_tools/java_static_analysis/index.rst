Efficient Java Static Checks
=============================

.. contents:: Table of Contents
  :depth: 2
  :local:

Practice the following three to improve the quality and maintainability of code.

* :ref:`code-analysis`
* :ref:`code-format`
* :ref:`api-analysis`

To execute the above, it is recommended to use `IntelliJ IDEA(external site) <https://www.jetbrains.com/idea/>`_ , an IDE manufactured by JetBrains in Nablarch.
An efficient Java static check method using IntelliJ IDEA is explained in this page.

.. _code-analysis:

Conduct syntax check
---------------------

To check the syntax, static inspection function (inspection) of IntelliJ IDEA is used.
Inspection is a function that provides real time alerts by checking if the code follows the Java coding conventions and if there are any potential bugs.

The configuration file of inspection used in the development of Nablarch is provided for the project.
Inspection configuration is applied by downloading the below file and storing them under ``PROJECT_ROOT/.idea/inspectionProfiles``.

:download:`Configuration file <download/Project_Default.xml>`

.. important::
  To ensure that the same syntax check is performed by all developers, the inspection configuration file must be managed by VCS.
  
.. important::
  The Inspection configuration contents can be referred from the point where the warning was issued and can be checked efficiently on IDE. For this reason, separate documents, such as a list of checks should not be created.

.. tip::
  Inspection can be customized by project based on the requirements.
  The customized configuration is reflected in the configuration file under ``PROJECT_ROOT/.idea/inspectionProfiles``.

~~~~~~~~~~~~~~~~~
Check with IDE
~~~~~~~~~~~~~~~~~

The inspection configuration of IntelliJ IDEA is enabled by default and executed real time when the code is written.
For more information, see `Manual <https://www.jetbrains.com/idea/documentation/>`_ of IntelliJ.


~~~~~~~~~~~~~~~~
Check with CI
~~~~~~~~~~~~~~~~

Inspection of IntelliJ IDEA can also be executed on a CI (Jenkins) server.
For information on the configuration method, see `(external site) <http://siosio.hatenablog.com/entry/2016/12/23/212140>`_ .

.. _code-format:

Unify the format
----------------------

To unify the format, formatted using the default code style of IntelliJ IDEA.
For more information, see `Manual <https://www.jetbrains.com/idea/documentation/>`_ of IntelliJ.

.. important::
  The Code Style configuration contents can be efficiently checked with IDE. For this reason, separate documents, such as coding conventions should not be created.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Automatically unify the formats before commit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
IntelliJ IDEA has a function that manages the formatting of target commit files when committing to VCS.
By making effective use of this, it is possible to commit the code will in accordance with the Code Style.

.. _api-analysis:

Check if unauthorized APIs are being used
-------------------------------------------------

We provide two tools for this check: the IntelliJ IDEA plugin and the SpotBugs plugin which does not depend on IntelliJ IDEA.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use nablarch-intellij-plugin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
`nablarch-intellij-plugin <https://github.com/nablarch/nablarch-intellij-plugin/tree/master/en>`_  is a plugin to use IntelliJ IDEA for supporting Nablarch development and has the following functions.

* Throws a warning if Nablarch private API is used.
* Throws warning if Java API registered in the black list is used.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use Unauthorized API Check Tool
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unauthorized API Check Tool is provided as a SpotBugs plugin. 
See `Nablarch style guide <https://github.com/nablarch-development-standards/nablarch-style-guide/blob/master/en/java/staticanalysis/unpublished-api/README.md>`_ for detailed specifications and instructions.
Note that the blank project has been preconfigured to `run in Maven <https://github.com/nablarch-development-standards/nablarch-style-guide/blob/master/en/java/staticanalysis/spotbugs/docs/Maven-settings.md>`_ , so it can be checked immediately.
