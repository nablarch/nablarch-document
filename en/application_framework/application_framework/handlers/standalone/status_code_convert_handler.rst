.. _status_code_convert_handler:

Status Code → Process End Code Conversion Handler
====================================================

.. contents:: Table of contents
  :depth: 3
  :local:

This handler converts the status code of the process result by the subsequent handler to the exit code of the process.

The process flow is as follows.

.. image:: ../images/StatusCodeConvertHandler/StatusCodeConvertHandler_flow.png

Handler class name
--------------------------------------------------
* :java:extdoc:`nablarch.fw.handler.StatusCodeConvertHandler`

Module list
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-standalone</artifactId>
  </dependency>

Constraints
--------------------------------------------------
Configure immediately after :ref:`main` 
  This handler converts the status code of the process result to the exit code of the process.

.. _status_code_convert_handler-rules:

Status code → Process exit code conversion
--------------------------------------------------------------
Conversion of status code to process exit code is performed according to the following rules.

.. important::
 Use 100 to 199 when specifying the status code in the error process of the application.

============================== ============================
Status code                    Process exit code
============================== ============================
-1 or less                     1
0 ~ 199                        0 ~ 199 (not converted)
200 ~ 399                      0
400                            10
401                            11
403                            12
404                            13
409                            14
400 ~ 499 excluding the above  15
Above 500                      20
============================== ============================

.. tip::
 The conversion rule cannot be changed by configuration for this handler. For this reason, a project-specific conversion handler has to be created if the requirements cannot be satisfied by this conversion rule.
