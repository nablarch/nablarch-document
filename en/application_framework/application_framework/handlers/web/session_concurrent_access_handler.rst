.. _session_concurrent_access_handler:

Session Concurrent Access Handler
==================================================
.. contents:: Table of contents
  :depth: 3
  :local:


.. important::
  This handler is not recommended to be used in new projects. Use a session variable save handler.

This handler provides a function to prevent processing inconsistency between threads caused by simultaneous execution
for concurrent simultaneous access of request process for each session.


This handler performs the following processes.

* Creates a copy of the information held in the session
* Checks if the session is updated by other threads after processing, and issues an error if it has been updated
* After processing is completed, incorporate a copy of the session information to the session


.. image:: ../images/SessionConcurrentAccessHandler/flow.png

Handler class name
--------------------------------------------------
* :java:extdoc:`nablarch.fw.web.handler.SessionConcurrentAccessHandler`

Module list
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>

Constraints
------------------------------

None.

