.. _`data_format-definition`:

Description Rules for Format Definition File
==================================================

.. contents:: Table of contents
  :depth: 3
  :local:

.. |br| raw:: html

    <br/>

Common notation for format definition files
--------------------------------------------------
This section describes the common description rules for format definition.

Character code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The character code of the format definition file is ``UTF-8``.


Literal notation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When a literal is configured in the configuration value, follow the rules below.


.. list-table::
  :class: white-space-normal
  :header-rows: 1
  :widths: 30 70

  * - Literal type
    - Description
  * - String
    - Enclose the value with ``"`` just like the Java character literal.

      Note that Unicode escapes or octal escapes are not supported.
      
      Example of the description
       | "Nablarch"
       | "\\r\\n"

  * - Decimal integer
    - Described in the same way as a Java numeric literal.

      Note that decimals are not supported.

      Example of the description
        | 123
        | -123

  * - Boolean
    - Configure as ``true`` or ``false``. (Uppercase letters are allowed)

Comment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Content following ``#`` in a line is treated as a comment.

An example is shown below.

.. code-block:: bash

  #
  # Sample file
  # 
  file-type:     "Fixed"  # Fixed-length
  text-encoding: "ms932"  # Character code is ms932
  record-length:  120     # The length of each line is 120 bytes




Structure of the format definition file
--------------------------------------------------

The format definition file is mainly composed of the following two sections.

:Directive declaration section:
  This section defines common configuration such as the data format (fixed-length or JSON etc.) used and encoding.

  For details, see :ref:`data_format-definition_directive`.

:Record format definition section:
  Defines contents of the record.

  Specifically, the field definition in record, data type and data conversion rule for each field are defined.

  For details, see :ref:`data_format-definition_record`.

.. _data_format-definition_directive:

Definition of the directive declaration section
--------------------------------------------------

Directive list that can be used in common
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Directive definitions used in all data formats are as follows.

.. list-table::
  :class: white-space-normal
  :widths: 30 70
  :header-rows: 1

  * - Directive
    - Description
  * - file-type ``required``
    - Specify the data format 

      The following data formats can be specified as standard.

      * Fixed (fixed-length)
      * Variable(variable length such as CSV and TSV)
      * JSON
      * XML

  * - text-encoding ``required``
    - .. _data_format-directive_text_encoding:

      Specify the encoding to use when reading and writing string fields.

      Only character encodings that are available to JVM used can be specified. For example, specify ``UTF-8`` and ``SJIS``.

      If JSON is specified for `file-type`, only the following encodings can be specified

      * UTF-8
      * UTF-16(BE or LE)
      * UTF-32(BE or LE)

      If XML is specified for `file-type`, the encoding specified in the XML declaration section
      takes precedence over this configured value.

  * - record-separator ``optional``
    - Specify the record end character (Carriage return and Line feed).

      This is ``required`` if Variable (variable length) is specified for `file-type`.

      This configuration value is not used when the `file-type` is JSON or XML.

List of directives that can be specified in fixed (fixed-length) format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The directives used for data in the fixed (fixed-length) format are as follows.

.. list-table::
  :class: white-space-normal
  :widths: 30 70
  :header-rows: 1

  * - Directive
    - Description
  * -  record-length ``required``
    - Specify the byte length of one record.

  * - positive-zone-sign-nibble ``optional``
    - .. _data_format-positive_zone_sign_nibble:

      Specify the plus sign to be configured in the zone section of the signed zoned decimal as a string in hexadecimal notation.

      By default, the following values are used depending on the value of :ref:`text-encoding <data_format-directive_text_encoding>`.

      :For ASCII-compatible: 0x3      
      :For EBCDIC-compatible: 0xC

  * - negative-zone-sign-nibble ``optional``
    - .. _data_format-negative_zone_sign_nibble:

      Specify the minus sign to be configured in the zone section of the signed zone numeric as a string in hexadecimal notation.

      By default, the following values are used depending on the value of :ref:`text-encoding <data_format-directive_text_encoding>`.

      :For ASCII-compatible: 0x7      
      :For EBCDIC-compatible: 0xD

  * - positive-pack-sign-nibble ``optional``
    - .. _data_format-positive_pack_sign_nibble:
      
      Specify the plus sign to be configured in the sign bit of the signed pack numeric as a string in hexadecimal notation.

      By default, the following values are used depending on the value of :ref:`text-encoding <data_format-directive_text_encoding>`.

      :For ASCII-compatible: 0x3      
      :For EBCDIC-compatible: 0xC
  
  * - negative-pack-sign-nibble ``optional``
    - .. _data_format-negative_pack_sign_nibble:
      
      Specify the minus sign to be configured in the sign bit of the signed packed decimal as a string in hexadecimal notation.

      By default, the following values are used depending on the value of :ref:`text-encoding <data_format-directive_text_encoding>`.

      :For ASCII-compatible: 0x7      
      :For EBCDIC-compatible: 0xD

  * - required-decimal-point ``optional``
    - Specifies if a decimal point is required for unsigned and signed numeric.

      If ``true`` is specified, a decimal point will be added to the data to be written.

      If ``false`` is specified, a decimal point will not be added to the data to be written. (The decimal place will be fixed)

      The default option is to add a decimal point ( ``true`` ).

  * - fixed-sign-position ``optional``
    - Specifies if the sign position of a signed numeric is to be fixed.

      If the sign position is fixed ( ``true`` ), the sign position is fixed to the beginning of the item.
      If the sign position is not fixed ( ``false`` ), the sign position is added to the beginning of the numeric before padding.

      The default option is fixed ( ``true`` ).

      Example
        :Sign position fixed: -000123456
        :Sign position not fixed: 000-123456

  
  * - required-plus-sign ``optional``
    - Specifies if a plus sign is required for the signed numeric.

      When ``true`` is specified, the data to be read must have a plus sign ( ``+`` ),
      and a plus sign ( ``+`` ) is added to the written data.

      The default option is not added ( ``false`` ).



An example is shown below.

.. code-block:: bash

  #
  # Directive definition section
  #
  file-type:                      "Fixed"  # Fixed-length file
  text-encoding:                  "ms932"  # Character encoding of the string type field
  record-length:                  120      # Byte length of each record 
  positive-zone-sign-nibble:      "C"      # Plus sign of zone numeric
  negative-zone-sign-nibble:      "D"      # Minus sign of zone numeric
  positive-pack-sign-nibble:      "C"      # Plus sign of pack numeric
  negative-pack-sign-nibbleL      "D"      # Minus sign of pack numeric
  required-decimal-point:         true     # With decimal point
  fixed-sign-position:            true     # Sign at the beginning
  required-plus-sign:             false    # Plus sign is not added

.. _data_format-variable_data_directive:

List of directives that can be specified in variable (variable length) format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The directives used for data in variable (variable length) format are as follows.

.. list-table::
  :class: white-space-normal
  :widths: 30 70
  :header-rows: 1

  * - Directive
    - Description
  * - field-separator ``required``
    - Specifies a separator character for the field (item).

      For example, specify ``,`` for CSV and specify ``\t`` for TSV.

  * - quoting-delimiter ``optional``
    - Specifies the character used to quote field (item) values.

      For example, use ``"`` to configure double quotes,
      and use ``'`` for single quotes.

      When the value is configured, all fields (items) are quoted during output.
      By default, quotes are not used.
      
      If the value is configured, the quote characters before and after the field is removed during input.
      For handling Carriage return and Line feed and quote characters in the fields, see RFC4180.

  * - ignore-blank-lines ``optional``
    - Configures if blank lines should be ignored when reading the data.

      When configured to ``true``, records on blank lines (only Carriage return and Line feed) are ignored.

      By default, blank lines are ignored.

  * - requires-title ``optional``
    - .. _data_format-requires-title:
      
      Configures if the first record should be read or written as a title.

      When configured to ``true``, the first record is treated as the title.

      By default, the first record is not treated as a title.

      For the layout definition of the title record, see :ref:`title-record-type-name directive <data_format-title_type_name>`.

  * - title-record-type-name ``optional``
    - .. _data_format-title_type_name:
      
      Configures the record type name of the title.

      If not specified, the record type name of the title will be ``Title``.

      The title record is edited according to the record format definition associated with the record type name specified in this directive.

      For the sample format definition file using the title record type,
      see :ref:`title record format definition example <data_format-variable_title_sample>`.

      For details of record types and record definitions, see :ref:`data_format-definition_record`.

  * - max-record-length ``optional``
    - Specifies the number of characters in a record that can be read.

      When data that does not have a record separator character (corrupted data) is read,
      if all records are expanded on the heap, the process may terminate abnormally due to insufficient heap.

      Therefore, if the record separator character does not exist even after reading the number of characters configured in this directive,
      the reading process is aborted, and an exception is thrown as invalid data.

      By default, configured to 1,000,000 characters.

An example is shown below.

.. code-block:: bash

  #
  # Directive definition section
  #
  file-type:                  "Variable"  # Variable length file
  text-encoding:              "utf-8"     # Character encoding of the string type field
  record-separator:           "\\r\\n"    # Carriage return and Line feed

  field-separator:            ","         # CSV
  quoting-delimiter:          "\""        # Enclose items in double quotes
  ignore-blank-lines:         true        # Ignore blank lines
  requires-title:             false       # No title record
  max-record-length:          1000        # Maximum 1000 characters for this csv record

Directive list that can be specified in JSON format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
There are no directives specific to the JSON data format.

An example is shown below.

.. code-block:: bash

  file-type:      "JSON"      # json format
  text-encoding:  "utf-8"     # Character encoding of the string type field


Directive list that can be specified in XML format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
There are no directives specific to the XML data format.

An example is shown below.

.. code-block:: bash

  file-type:      "XML"       # xml format
  text-encoding:  "utf-8"     # Character encoding of the string type field

.. _data_format-definition_record:

Record format definition section
--------------------------------------------------
The record format definition section configures the definition information of the fields (items) that make up the record (such as position and data type in the record).

An example of record format definition is shown below.

Points
  * A record type name, to identify the record, is defined by enclosing with ``[``, ``]`` brackets.
  * Record type name must be unique in the format definition file.
  * The record type name defines an optional value.
  * The fields (items) in the record are defined from the next line of the record type.
  * The field (item) definition are repeated for the number of fields.
  * For field definition format, see :ref:`field definition format <data_format-field_definition>`.

.. code-block:: bash

  [data]              # Record type name:data
  1 name  N(100)      # Name
  2 age   X9(3)       # Age

.. important::

  When defining fields in JSON and XML data formats, in multiple fields with the same field name, fields with the field type ``OB`` should not be mixed with fields with other field types.

  When mixed, the field type of the field that specifies other than OB is ignored because the definition of OB has priority.

  As a result, even though the field is not actually an OB, it is treated as an OB type when reading and writing.
  This can cause problems where data and format item definitions do not match and data cannot be read and written correctly.

  Inappropriate examples
    .. code-block:: bash

      [order]
      1 id     N
      2 data   OB  # field type:OB
      3 detail OB

      [data]
      1 value  N

      [detail]
      1 data   N   # field type:N  <- Inappropriate notation: The field type is considered to be OB.

.. _data_format-field_definition:

Field definition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Field definition is defined with the following format.

.. code-block:: text
  
  <Field start position> <Field name> <Multiplicity> <Field type> <Field converter>

Details of each element of the field definition are as given below.

.. list-table::
  :class: white-space-normal
  :widths: 30 70

  * - Field start position ``required``
    - Define the field start position according to the following rules for each data format.

      :Fixed (fixed-length): Configure the number of starting bytes (count from 1) of the field.
      :Variable (variable length): Configure the item serial number of the field.
      :JSON: Element serial number of the field
      :XML: Element serial number of the field

  * - Field name ``required``
    - Configure the name to identify the field.

      The field name is the key of :java:extdoc:`java.util.Map` used for input/output by this function.

      If ``?`` is added to the beginning of the field name, that item will not be read into :java:extdoc:`java.util.Map` during input.
      For example, any extra items can be excluded by using ``?`` for filler items of a fixed-length file that is often handled by the host.

      .. important::

        Note that a field name cannot be defined with only numbers.

      In the case of XML data format, items are treated as an attribute value by adding ``@`` the beginning of the field name.

      An example is shown below.
      
      .. code-block:: bash

        [tagName]
        @attr

      The XML corresponding to the above is as follows.

      .. code-block:: xml

        <tagName attr="val">
        ・・・
        </tagName>

  * - Multiplicity ``optional``
    - Specifies the number of fields that can be defined.

      This value can be specified only for JSON and XML data formats.

      The description rules are as follows.
        * The number that can be defined is described by enclosing with ``[``, ``]``.
        * When there is a lower limit and an upper limit, write ``..`` between the lower limit and the upper limit.
        * If there is no upper limit, write ``*``.
        * If omitted, it becomes ``[1]``.

      A specification example is shown below.

      .. code-block:: bash

        address [1..3]    # 1 to 3 can be defined
        address           # Only one is possible as it is omitted
        address [0..*]    # No condition (0 to unlimited)
        address [*]       # No condition (0 to unlimited)
        address [1..*]    # 1 or more

      In the case of the following xml, the number of definitions in the ``address`` field is ``2``.

      .. code-block:: xml

        <person>
          <address>Home address</address>
          <address>Work address</address>
        </person>

      In the case of the following JSON, the number of elements in the ``address`` field is ``3``.

      .. code-block:: json

        {
          "address" : ["Home address", "Work address", "Delivery address"]
        }
      

  * - Field Type ``required``
    - Defines the data type of the field.

      For field types that can be specified by default, see :ref:`data_format-field_type_list`.

  * - Field convertor ``optional``
    - Defines the contents of input/output pre-processing, such as specifying options for field types or data conversion.

      For field types that can be specified by default, see :ref:`data_format-field_convertor_list`.

      Multiple field converters can be configured.


.. _data_format-multi_layout_data:

Define a multiformat record
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
For multi-format data, define multiple record formats in the format definition file.

The record format of the input /output data is automatically determined by the value of a specific field.
If the input /output target data does not match any record type, it is treated as invalid data and the process is terminated abnormally.

Example of format definition for multi-format is shown below.

Points
  * Defines the record identification field. The record type name is ``Classifier``.
  * The condition to determine a record is defined directly below the record type name of each record definition.
  * The field defined in record identification (Classifier) must exist in the record definition.

.. code-block:: bash

  file-type:        "Fixed" # Fixed-length
  text-encoding:    "MS932" # Character encoding of the string type field
  record-length:    40      # Length of each record
  record-separator: "\r\n"  # Carriage return and Line feed (crlf)

  # Define the record identification condition
  [Classifier]
  1 dataKbn X(1)      # Determine the record type by using the field of the first byte

  # Define the header record
  [header]
  dataKbn = "1"         # Header record if dataKbn is "1"
  1 dataKbn X(1)
  2 data    X(39)

  # Define the data record
  [data]
  dataKbn = "2"        # Data record if dataKbn is "2"
  1 dataKbn X(1)
  2 data    X(39)

For a sample of the multi-format definition, refer to the following link.

.. toctree::
  :maxdepth: 1

  multi_format_example

.. tip::

  Since JSON and XML data formats do not have the concept of a record,
  format definition for multiformat is not supported.

.. _data_format-field_type_list:

Field type list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The data type definition list provided as standard is shown below.

List of available field types for Fixed (fixed-length) data format
  .. list-table::
    :class: white-space-normal
    :header-rows: 1
    :widths: 13 15 72

    * - Type
      - Java data types
      - Description

    * - .. _data_format-field_type-single_byte_character_string:

        X
      - String
      - Single byte character string (byte length = character string length)

        By default, right trim/padding is performed using half-width space.

        :Argument: Byte length (numeric) ``required``

        If the output target value is ``null``, the value is converted to an empty character before processing.

        If the read value is an empty string, it is converted to ``null``.
        Configure :java:extdoc:`convertEmptyToNull <nablarch.core.dataformat.convertor.FixedLengthConvertorSetting.setConvertEmptyToNull(boolean)>` to ``false``
        if conversion of empty string to ``null`` is not required.

    * - N
      - String
      - Double-byte character string (byte length = number of characters/2)

        By default, right trim/padding is performed with full-width space.

        :Argument: Byte length (numeric) ``required``

        * If the byte length is not a multiple of 2, a syntax error will occur.

        If the output target value is ``null`` or the read value is an empty string,
        the handling is the same as :ref:`single byte string field type <data_format-field_type-single_byte_character_string>`.

    * - XN
      - String
      - Multibyte string

        Specify this field type when handling a field where characters of different byte lengths are mixed, such as UTF-8.

        This field type is also used when the padding for the full-width string (double-byte string) uses a half-width space.

        By default, right trim/padding is performed with half-width space.

        :Argument: Byte length (numeric) ``required``

        If the output target value is ``null`` or the read value is an empty string,
        the handling is the same as :ref:`single byte string field type <data_format-field_type-single_byte_character_string>`.

    * - .. _data_format-field_type-zoned_decimal:

        Z
      - BigDecimal
      - Zone numeric (byte length = number of digits)

        By default, left trim/padding is performed with ``0``.

        :Argument 1: Byte length (numeric) ``required``
        :Argument 2: Number of digits after decimal point (numeric) ``optional`` Default: ``0``

        If the output target value is ``null``, the value is converted to ``0`` before processing.

        If the number of bytes in the read value is ``0``, it is converted to ``null``.
        Configure :java:extdoc:`convertEmptyToNull <nablarch.core.dataformat.convertor.FixedLengthConvertorSetting.setConvertEmptyToNull(boolean)>` to ``false``,
        when the number of bytes is ``0`` and conversion to ``null`` is not required.

    * - SZ
      - BigDecimal
      - Signed zone numeric (byte length = number of digits)

        By default, left trim/padding is performed with ``0``.

        :Argument 1: Byte length (numeric) ``required``
        :Argument 2: Number of digits after the decimal point (numeric) ``optional`` Default: ``0``
        :Argument 3: Plus sign to be configured in the zone section (hexadecimal string) ``optional``
        :Argument 4: Minus sign to be configured in the zone section (hexadecimal string) ``optional``

        Argument 3 and argument 4 are configured when overwriting the :ref:`plus sign of the signed zone numeric <data_format-positive_zone_sign_nibble>`
        and minus sign of the :ref:`signed zone numeric <data_format-negative_zone_sign_nibble>`.

        When the output target value is ``null`` or the number of bytes of the read value is ``0``,
        then the handling is the same as :ref:`zone numeric field type <data_format-field_type-zoned_decimal>`.

    * - P
      - BigDecimal
      - Pack numeric (byte length = number of digits/2 [rounded up])

        By default, left trim/padding is performed with ``0``.

        :Argument 1: Byte length (numeric) ``required``
        :Argument 2: Number of digits after the decimal point (numeric) ``optional`` Default: ``0``

        When the output target value is ``null`` or the number of bytes of the read value is ``0``,
        then the handling is the same as :ref:`zone numeric field type <data_format-field_type-zoned_decimal>`.

    * - SP
      - BigDecimal
      - Signed pack numeric (byte length = (number of digits + 1)/2 [rounded up])

        By default, left trim/padding is performed with ``0``.

        :Argument 1: Byte length (numeric) ``required``
        :Argument 2: Number of digits after the decimal point (numeric) ``optional`` Default: ``0``
        :Argument 3: Plus sign to be configured in the zone section (hexadecimal string) ``optional``
        :Argument 4: Minus sign to be configured in the zone section (hexadecimal string) ``optional``

        Argument 3 and argument 4 are configured when overwriting the :ref:`plus sign of the signed pack numeric <data_format-positive_pack_sign_nibble>`
        and minus sign of the :ref:`signed pack numeric <data_format-negative_pack_sign_nibble>`.

        When the output target value is ``null`` or the number of bytes of the read value is ``0``,
        then the handling is the same as :ref:`zone numeric field type <data_format-field_type-zoned_decimal>`.

    * - B
      - byte[]
      - Binary string

        Padding and trimming are not performed.

        :Argument: Byte length (numeric) ``required``

        The conversion specifications for each application are different when the output value is ``null``.
        Therefore, the value is not converted for this field type even in such a case and
        :java:extdoc:`InvalidDataFormatException <nablarch.core.dataformat.InvalidDataFormatException>`
        is thrown.

        When using this field type, configure the value explicitly in the application according to the requirements.

    * - X9
      - BigDecimal
      - Unsigned numeric string (byte length = number of characters)

        Treat single-byte strings (X) in the field as numeric.

        By default, left trim/padding is performed with ``0``.
        Decimal point sign ( ``.`` ) can be included in the string.

        :Argument 1: Byte length (numeric) ``required``
        :Argument 2: Number of digits after the decimal point (numeric) for fixed decimal point ``optional`` Default: ``0``

        When the output value is ``null``,
        then the handling is the same as :ref:`zone numeric field type <data_format-field_type-zoned_decimal>`.

        If the read value is an empty string,
        the handling is the same as :ref:`single byte string field type <data_format-field_type-single_byte_character_string>`.


    * - SX9
      - BigDecimal
      - Signed numeric string (byte length = number of characters)

        Single byte string (X) in the field is treated as a signed numeric.
        By default, left trim/padding is performed with ``0``.

        :Argument 1: Byte length (numeric) ``required``
        :Argument 2: Number of digits after the decimal point (numeric) for fixed decimal point ``optional`` Default: ``0``

        When the output value is ``null``,
        then the handling is the same as :ref:`zone numeric field type <data_format-field_type-zoned_decimal>`.

        If the read value is an empty string,
        the handling is the same as :ref:`single byte string field type <data_format-field_type-single_byte_character_string>`.

        To change the sign character (``+`` 、``-``), a project-specific field type can be created to support the implementation of the following classes.

        * :java:extdoc:`SignedNumberStringDecimal <nablarch.core.dataformat.convertor.datatype.SignedNumberStringDecimal>`

        For additional field types, see :ref:`data_format-field_type_add`.

List of available field types for Variable (Variable length) data format
  .. list-table::
    :class: white-space-normal
    :header-rows: 1
    :widths: 13 15 72

    * - Type
      - Java data types
      - Description

    * - X |br|
        N |br|
        XN |br|
        X9 |br|
        SX9
      - String
      - All fields are read and written as strings for variable-length data formats.

        The operation does not change no matter what type of identifier is specified.
        Since there is no concept of field length, arguments are not required.

        To read and write as numeric format of character string (BigDecimal),
        use :ref:`number converter <data_format-number_convertor>`
        or :ref:`signed_number converter <data_format-signed_number_convertor>`.

        If the output target value is ``null``, the value is converted to a empty character before processing.
        
        If the read value is an empty string, it is converted to ``null``.
        Configure :java:extdoc:`convertEmptyToNull <nablarch.core.dataformat.convertor.VariableLengthConvertorSetting.setConvertEmptyToNull(boolean)>` to ``false`` if conversion of empty string to null is not required.


List of available field types for JSON and XML data formats
  .. list-table::
    :class: white-space-normal
    :header-rows: 1
    :widths: 13 15 72

    * - Type
      - Java data types
      - Description

    * - .. _data_format-field_type-nullable_string:

        X |br|
        N |br|
        XN
      - String
      - String data type

        Editing such as padding is not performed.

        The value is enclosed in double quotes ``"`` during output for JSON.

        If the output value is ``null``, the value is not converted in JSON,
        and is converted to an empty string in XML.

    * - X9 |br|
        SX9 |br|
      - String
      - Numeric string type

        Data editing such as padding is not performed. During output, the value is output without change.

        To read and write as numeric format of character string (BigDecimal),
        use :ref:`number converter <data_format-number_convertor>`
        or :ref:`signed_number converter <data_format-signed_number_convertor>`.

        When the output value is ``null``,
        the handling is the same as :ref:`field type for string data type <data_format-field_type-nullable_string>`.

    * - BL
      - String	
      - String（ ``true`` or ``false`` expressed as a string）

        Data editing such as padding is not performed. During output, the value is output without change.

        When the output value is ``null``,
        the handling is the same as :ref:`field type for string data type <data_format-field_type-nullable_string>`.

    * - .. _data_format-nest_object:

        OB
      - \-
      - Used to specify nested record types.

        The record type corresponding to the field name is input/output as a nested element.

        When the output value is ``null``,
        the handling is the same as :ref:`field type for string data type <data_format-field_type-nullable_string>`.

        An usage example is shown below.

        json
          .. code-block:: json

            {
              "users": [
                {
                  "name"    : "Name",
                  "age"     : 30,
                  "address" : "Address"
                },
                {
                  "name"    : "Name 1",
                  "age"     : 31,
                  "address" : "Address 1"
                }
              ]
            }

        xml
          .. code-block:: xml
            
            <users>
              <user>
                <name> Name </name>
                <age>30</age>
                <address> Address </address>
              </user>
              <user>
                <name> Name 1</name>
                <age>31</age>
                <address> Address 1</address>
              </user>
            </users>

        The format definition file for JSON and xml above are as follows:

        .. code-block:: bash

          [users]       # Root element
          1 user [1..*] OB

          [user]        # Nested element
          1 name    N   # Bottom layer element
          2 age     X9
          3 address N


.. _data_format-field_convertor_list:

Field converter list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The data converter list provided as standard is shown below.

.. list-table::
  :class: white-space-normal
  :header-rows: 1
  :widths: 20 30 50

  * - Converter name
    - Type conversion specification
    - Description

  * - pad
    - No type conversion
    - Configure the characters to pad and trim.

      Padding and trim positions operate as follows for each field type.

      :X: Right trim, right padding
      :N: Right trim, right padding
      :XN: Right trim, right padding
      :Z: Left trim, left padding
      :SZ: Left trim, left padding
      :P: Left trim, left padding
      :SP: Left trim, left padding
      :X9: Left trim, left padding
      :SX9: Left trim, left padding

      For more information on field types, see :ref:`data_format-field_type_list`.

      :Argument: Value for padding/trim ``required``

  * - encoding
    - No type conversion
    - Configure the character encoding for string type field

      Configure when overwriting the common configuration (:ref:`text-encoding <data_format-directive_text_encoding>`) for only specific fields.

      Can be used only for ``X``, ``N`` and ``XN`` fields.
      Ignored if it is configured to any other field type.

      :Argument: Encoding name (string) ``required``


  * - Literal value
    - No type conversion
    - Configure the default value for output.

      Outputs the specified literal value if the value was not configured during output.

      This configuration value is not used during input.

  * - .. _data_format-number_convertor:
    
      number
    - String <-> BigDecimal
    - Configure when conversion of numeric string to numeric (BigDecimal) is required.

      :During input: Checks that the input numeric string is in the unsigned numeric format \
               and converts it to BigDecimal type.

      :During output: Converts the output value to a string, and then outputs after checking that it is in the unsigned numeric value format.

  * - .. _data_format-signed_number_convertor:
      
      signed_number

    - String <-> BigDecimal

    - Configure when conversion of signed numeric string to numeric (BigDecimal) is required.

      Expect that signs are allowed, the specification is the same as :ref:`number converter <data_format-number_convertor>`.

  * - .. _data_format-replacement_convertor:
      
      replacement
    - No type conversion
    - The character is converted to the conversion destination character and returned for both input and output.

      :Argument: Replacement type name ``optional``

      For details, see :ref:`data_format-replacement`.


Omitting item definitions
--------------------------------------------------
Describes the behavior when the item definition of the format definition file does not match the item definition of the data.

For fixed-length and variable length data
  For fixed-length and variable length data, the field definition of the data and the format definition must match exactly.
  For this reason, an item must be defined in the format definition file even if there are items that are not required by the application.

For JSON and XML data
  In the case of JSON and XML, items that are not defined in the format definition file will not be read.
  Therefore, item definition is not required for items that are present in the data but are not required by the application.
  

