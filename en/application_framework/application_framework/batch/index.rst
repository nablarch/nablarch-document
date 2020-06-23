.. _batch_application:

Batch Application Edition
==================================================
This chapter provides information necessary for developing batch applications using the Nablarch application framework.

Nablarch batch application provides the following two types of batch application frameworks.

.. toctree::
  :maxdepth: 1

  jsr352/index
  nablarch_batch/index

Although a batch application can be built using either framework,
creating a batch application using :doc:`jsr352/index` is recommended for the following reasons.

Reason
  :doc:`nablarch_batch/index` is similar to `JSR352(external site) <https://jcp.org/en/jsr/detail?id=352>`_
  and `Spring Batch(external site) <http://projects.spring.io/spring-batch/>`_ [#spring_batch]_,
  but there are many parts that are different.
  For this reason, the disadvantage of using :doc:`nablarch_batch/index`
  is that it requires extensive learning and the learning cost increases.
  Parts that appear to be similar are a source of confusion for developers
  and has the disadvantage of reducing development productivity.

.. tip::

  Refer to :ref:`batch-functional_comparison` for the difference between the functions provided by
  :ref:`jsr352_batch` and :ref:`nablarch_batch`.

.. toctree::
  :maxdepth: 1
  :hidden:

  functional_comparison


.. [#spring_batch] JSR352 has been standardized with many features inherited from Spring Batch.
                   For this reason, experienced users of Spring Batch can develop batch applications
                   using JSR352 without having to learn much.
