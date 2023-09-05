==========================================================
Testing framework
==========================================================


.. toctree::
   :maxdepth: 1
   :titlesonly:

   guide/development_guide/05_UnitTestGuide/index
   guide/development_guide/06_TestFWGuide/index
   guide/development_guide/08_TestTools/index

Test implementers who use testing frameworks to implement functional tests should refer to :ref:`unitTestGuide`.
For architects who will be adopting testing frameworks, refer to :ref:`testFWGuide`.

.. important::

  The testing framework does not support the following platforms and libraries: 
  For this reason, testing framework such as `JUnit (external site) <http://junit.org>`_  should be used for testing applications that use these platforms and libraries.

  * :ref:`JSR352-compliant batch application <jsr352_batch>`

.. important::

  The testing framework does not support multi-thread functions. 
  Testing of multi-threaded functions should be performed with tests that do not use the testing framework (such as integration tests).
