.. _batch_application:

Batch Application
==================================================
This chapter provides information necessary for developing batch applications using the Nablarch application framework.

Nablarch batch application provides the following two types of batch application frameworks.

.. toctree::
  :maxdepth: 1

  jsr352/index
  nablarch_batch/index

Although a batch application can be built using either framework,
creating a batch application using :doc:`nablarch_batch/index` is recommended for the following reasons.

Reason
  Since Jakarta Batch has little information as of 2020 and it is difficult for experts to assign it, we recommend creating a batch application using :doc:`nablarch_batch/index`.

.. tip::

  Although the manuals up to Nablarch 5u15 recommended Jakarta Batch-compliant batch applications, the policy has changed to recommend Nablarch batch applications due to their current prevalence and high learning costs in 2020.



.. tip::

  Refer to :ref:`batch-functional_comparison` for the difference between the functions provided by
  :ref:`jsr352_batch` and :ref:`nablarch_batch`.

.. toctree::
  :maxdepth: 1
  :hidden:

  functional_comparison


