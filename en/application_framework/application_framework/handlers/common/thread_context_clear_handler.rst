.. _thread_context_clear_handler:

Thread Context Variable Delete Handler
============================================

.. contents:: Table of contents
  :depth: 3
  :local:
  
This handler deletes variables in the thread local configured by the :ref:`thread_context_handler` .

This handler performs the following process.

* :ref:`thread_context_clear_handler-clear`

The process flow is as follows.

.. image:: ../images/ThreadContextClearHandler/flow.png

Handler class name
--------------------------------------------------
* :java:extdoc:`nablarch.common.handler.threadcontext.ThreadContextClearHandler`

Module list
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw</artifactId>
  </dependency>

Constraints
---------------------------------------
This handler should be placed at the beginning as far as possible. 
The reason is that the handlers before this handler cannot access the thread context in response processing.

.. _thread_context_clear_handler-clear:

Deletion process of thread context
-----------------------------------------------------------
Deletes all the values configured on the thread local with :ref:`thread_context_handler` .

