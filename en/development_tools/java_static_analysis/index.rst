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

Run inspection
---------------------

IntelliJ IDEA has an `inspection feature(external site) <https://www.jetbrains.com/help/idea/code-inspection.html>`_ that performs static analysis, checking for conformity to Java coding conventions and potential bugs, and alerting you in real time.

By default, Inspection is set to warn you about things you should generally be aware of.

If you have established rules for your project, you can use Inspection more effectively by changing the settings to suit your project.
Changed settings can be exported and imported to be shared among project developers.
See `Configure profiles(external site) <https://www.jetbrains.com/help/idea/customizing-profiles.html>`_ for how to export and import.

.. _code-format:

Unify the format
----------------------

By using code formatter feature of IntelliJ IDEA, you can unify the code style in your project.
See `Java Code Formatter Description in Java style guide <https://github.com/Fintan-contents/coding-standards/blob/main/java/code-formatter.md>`_  for how to use it.

.. _api-analysis:

Check if unauthorized APIs are being used
-------------------------------------------------

We provide two tools for this check: the IntelliJ IDEA plugin and the SpotBugs plugin which does not depend on IntelliJ IDEA.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use nablarch-intellij-plugin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
`nablarch-intellij-plugin <https://github.com/nablarch/nablarch-intellij-plugin/tree/main/en>`_  is a plugin to use IntelliJ IDEA for supporting Nablarch development and has the following functions.

* Throws a warning if Nablarch private API is used.
* Throws warning if Java API registered in the black list is used.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use Unauthorized API Check Tool
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unauthorized API Check Tool is provided as a SpotBugs plugin. 
See `Unauthorized API Check Tool Description in Java style guide <https://github.com/Fintan-contents/coding-standards/blob/main/en/java/staticanalysis/unpublished-api/README.md>`_ for detailed specifications and instructions.

Note that the blank project has been preconfigured to `run in Maven <https://github.com/Fintan-contents/coding-standards/blob/main/en/java/staticanalysis/spotbugs/docs/Maven-settings.md>`_ , so it can be checked immediately.
