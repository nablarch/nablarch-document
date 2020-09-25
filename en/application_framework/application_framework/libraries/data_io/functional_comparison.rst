.. _`data_io-functional_comparison`:

Comparison Table of Data Bind and General Data Format
----------------------------------------------------------------------------------------------------
This section compares the following functions:

* :ref:`data_bind`
* :ref:`data_format`


.. list-table:: Function comparison (A: Provided B: Partially provided C: Not provided D: Not applicable)
  :header-rows: 1
  :class: something-special-class

  * - Function
    - Data bind
    - General data format

  * - CSV can be input/output
    - A |br|
      :ref:`To the manual <data_bind-csv_format>`
    - A |br|
      :ref:`To the manual <data_format-support_type>`

  * - CSV with different formats |br| input/output for each record
    - C [#csv_multi_format]_
    - A |br|
      :ref:`To the manual <data_format-multi_layout_data>`

  * - CSV definition can be configured |br|
      (comma, quote characters, etc. can be changed)
    - A |br|
      :ref:`To the manual <data_bind-csv_format>`
    - A |br|
      :ref:`To the manual <data_format-variable_data_directive>`

  * - Fixed-length data can be input/output
    - A |br|
      :ref:`To the manual <data_bind-fixed_length_format>`
    - A |br|
      :ref:`To the manual <data_format-support_type>`

  * - Fixed-length data with different formats |br| for each record can be input/output
    - A |br|
      :ref:`To the manual <data_bind-fixed_length_format-multi_layout>`
    - A |br|
      :ref:`To the manual <data_format-multi_layout_data>`

  * - JSON data can be input/output
    - C [#json_layout]_
    - A |br|
      :ref:`To the manual <data_format-support_type>`

  * - XML data can be input/output
    - C [#xml_layout]_
    - A |br|
      :ref:`To the manual <data_format-support_type>`

  * - Value can be converted during data input/output |br|
      (trim, packed decimal, conversion of zone decimal, etc.)
    - B [#converter]_
    - A |br|
      :ref:`To the manual <data_format-value_convertor>`

  * - Refers to the conversion into characters that are allowed |br|
      in a system that can use collated characters for data
    - C [#char_replace]_
    - A |br|
      :ref:`To the manual <data_format-replacement>`

.. [#csv_multi_format] When handling CSV of different format for each record, use :ref:`data_format`.
.. [#json_layout] Input/output of JSON data is not implemented. When handling JSON data, use :ref:`data_format` or OSS.
.. [#xml_layout] Input/output of XML data is not implemented. When handling XML data, use :ref:`data_format` or JAXB.
.. [#converter] Converters such as trim only for fixed-length data are provided. To convert the value with CSV, data format conversion has to be performed before output and after input.
.. [#char_replace] Create a handler for character conversion to handle the collated characters (character conversion) of input data.

.. |br| raw:: html

  <br />
