.. _data_converter:

Access to Data in Various Formats
==================================================
Provides a function to handle data in various formats.

Nablarch provides the following two types of data input/output functions.

.. toctree::
  :maxdepth: 1

  Data binding (function to map data and Java Beans object) <data_io/data_bind>
  General data format (function to perform data input/output based on the format definition file) <data_io/data_format>

.. _data_converter-data_bind_recommend:

Although data can be accessed by using either of the above functions, use of :ref:`data_bind` is recommended for the following reasons.

* Since :ref:`data_bind` can handle data as Java Beans object, the complementation of IDE can be effectively used, and the development efficiency is better. (Has the advantage that typos in item names cannot occur)
* Format definition of :ref:`data_format` is complicated and difficult to understand. Due to this, learning cost and maintenance cost increases.

.. important::

  For formats that cannot be handled by :ref:`data_bind` , :ref:`data_format` is required to beused.

.. tip::

  Refer to :ref:`data_io-functional_comparison` for the difference between the functions provided by :ref:`data_bind` and :ref:`data_format`.

.. toctree::
  :hidden:

  data_io/functional_comparison


