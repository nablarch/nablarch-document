====================================================
JSP Static Analysis Tool Configuration Change Guide
====================================================

.. contents:: Table of Contents
  :depth: 2
  :local:

This section describes how to change the settings of :doc:`index`\ .

Prerequisites
----------------

* Generation of a blank project from the archetype must be complete.


Structure of configuration file
--------------------------------

The structure of the configuration file is shown in the table below.

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 10,13


  * - File name
    - Description

  * - pom.xml
    - Perform the configuration required for startup and jspanalysis.excludePatterns.

  * - tools/nablarch-tools.xml
    - Check the Ant task definition file [1]_ . Usually it need not be edited

  * - tools/static-analysis/jspanalysis/config.txt
    - JSP static analysis tool configuration file. Refer to :ref:`01_customJspAnalysis` for the description method


  * - tools/static-analysis/jspanalysis/transform-to-html.xsl
    - Definition file for converting JSP static analysis result XML to HTML. |br|
      Refer to "JSP Analysis (XML Report Output)" in :ref:`01_outputJspAnalysis` for the description method.

  * - Pom.xml of nablarch-archetype-parent
    - Perform the configuration other than jspanalysis.excludePatterns




.. [1] It exists because Ant is used internally. The user usually doesn’t become aware of it because it is executed via Maven.

.. _01_customJspAnalysisProp:

Rewriting pom.xml
-----------------------------------------------
When modifying properties for the JSP static analysis tool according to the execution environment, if there are modifications to jspanalysis.excludePatterns, modify the pom.xml of the project that executes the tool. When other items are to be modified, modify pom.xml of nablarch-archetype-parent.

================================  ============================================================================================================
Configuration property                    Description
================================  ============================================================================================================
jspanalysis.checkjspdir           Configure the target JSP directory path or file path.

                                  Configure the directory when batch check is to be done |br|
                                  like the CI environment.

                                  Example::

                                     ./main/web

                                  If a directory is specified, the check is performed recursively.

jspanalysis.xmloutput             Configure the output path of XML report file of check results.

                                  Example::

                                     ./build/reports/jsp/report.xml

jspanalysis.htmloutput            Configure the output path of HTML report file of check results.

                                  Example::

                                     ./build/reports/jsp/report.html

jspanalysis.checkconfig           Configure the file path of the JSP static analysis tool configuration file.

                                  Example::

                                    ./tool/jspanalysis/config.txt

jspanalysis.charset               Configure the character code of the JSP file to be checked.

                                  Example::

                                     utf-8

jspanalysis.lineseparator         Configure the line feed code used  |br|
                                  in the check target JSP file.

                                  Example::

                                     \n

jspanalysis.xsl                   Configure the XSLT file path for converting the XML |br|
                                  of the check results to HTML file.

                                  Example::

                                    ./tool/jspanalysis/transform-to-html.xsl

jspanalysis.additionalext         Configure the filename extension of the JSP file to be checked.

                                  Configure the filename extension of the JSP file to be checked.
                                  When multiple filename extensions are to be specified, they must be separated with commas (,). 
                                  Regardless of the configuration value that is configured, files with the extension jsp are always checked.

                                  Example::

                                    tag

jspanalysis.excludePatterns [2]_  Configure the directory (file) name to be excluded from the check  |br|
                                  with a regular expression.

                                  When multiple patterns are to be configured, specify them with comma(,) separator.

                                  Example::

                                    ui_local,ui_test,ui_test/.*/set.tag
================================  ============================================================================================================

.. [2] This setting is commented out by default. While using this configuration, uncomment pom.xml and nablarch-tools.xml in the tools directory.


.. tip::

  The file path (directory path) can also be specified as an absolute path.

.. _how_to_setup_ant_view_in_eclipse_jsp_analysis:


.. |br| raw:: html

  <br />