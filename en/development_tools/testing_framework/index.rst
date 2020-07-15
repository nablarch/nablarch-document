========================================================
Robust Testing Framework for Large Scale Development
========================================================


.. toctree::
   :maxdepth: 1
   :numbered:
   :titlesonly:

   guide/development_guide/05_UnitTestGuide/index
   guide/development_guide/06_TestFWGuide/index
   guide/development_guide/08_TestTools/index

.. important::

  The testing framework does not support the following platforms and libraries: 
  For this reason, testing framework such as `JUnit (external site, in English) <http://junit.org>`_  should be used for testing applications that use these platforms and libraries.

  * :ref:`RESTful web service <restful_web_service>`
  * :ref:`JSR352-compliant batch application <jsr352_batch>`
  * :ref:`Bean Validation <bean_validation>`

.. important::

  The testing framework does not support multi-thread functions. 
  Testing of multi-threaded functions should be performed with tests that do not use the testing framework (such as integration tests).
