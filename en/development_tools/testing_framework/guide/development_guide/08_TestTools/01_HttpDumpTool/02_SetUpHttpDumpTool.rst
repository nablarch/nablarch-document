========================================================
Request Unit Data Creation Tool Installation Guide
========================================================

This section describes how to install the :doc:`index`\.

.. _http_dump_tool_prerequisite:

Prerequisites
================

The following prerequisites must be met to use this tool.

* The following commands must be included in the path.

  * java
  * mvn

* HTML file must be associated with the browser.
* Browser proxy setting must exclude localhost.


Method of provision
=========================

This tool is provided in the following jar.

* nablarch-testing-XXX.jar
* nablarch-testing-jetty6-XXX.jar (for Java 8 and earlier versions)
* nablarch-testing-jetty9-XXX.jar (for Java 11 and later versions) 

Get(save from right click menu) the bat file for launching this tool from the following, and place it in the same directory as project's pom.xml.

* :download:`httpDump.bat <download/httpDump.bat>`

Integration with Eclipse
==============================

This tool can be launched from Eclipse with the following settings.


Configuration Screen Startup
---------------------------------

From the toolbar, select Window → Preference. 
Select General → Editors → File Associations from the left pane, 
select * .html from the right pane and click the Add button.

.. image:: ./_image/01_Eclipse_Preference.png
   :scale: 100

 
External program selection
--------------------------------

Select External Program from the radio button and click the Browse button.

.. image:: ./_image/02_Eclipse_EditorSelection.png
   :scale: 100


Select batch file (shell script) for startup
-----------------------------------------------

Select the batch file (httpDump.bat) for Windows, 
and the shell script (httpDump.sh) for Linux.

.. image:: ./_image/03_Eclipse_OpenFile.png
   :scale: 100


.. _howToExecuteFromEclipse:

How from launch from HTML file
----------------------------------

You can start the tool by right-clicking the HTML file from Package Explorer of Eclipse and opening the file with httpDump.

.. image:: ./_image/04_Eclipse_OpenWith.png
   :scale: 100
