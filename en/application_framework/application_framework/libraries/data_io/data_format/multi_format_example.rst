Sample Collection of Fixed (Fixed-Length) Multi Format Definition
---------------------------------------------------------------------

Example of identifying format with a single field
  When a single field is a condition, if the field value matches the condition defined in each format, then it is processed with the record definition.

  In this example, records are identified by the following rules:

  * Header record type if dataKbn is 1.
  * Data record type if dataKbn is 2.

  .. code-block:: bash

    file-type:        "Fixed" # Fixed-length
    text-encoding:    "MS932" # Character encoding of the string type field
    record-length:    40      # Length of each record
    record-separator: "\r\n"  # Carriage return and Line feed (crlf)

    # Define record identification field
    [Classifier]
    1 dataKbn X(1)

    # Define the header record
    [header]
    dataKbn = "1"
    1 dataKbn X(1)
    2 data    X(39)

    # Define data record
    [data]
    dataKbn = "2"
    1 dataKbn X(1)
    2 data    X(39)

Example of identifying format with multiple fields
  When a record is identified by multiple of fields, the processing is performed by the record definition if all conditions are satisfied.

  In this example, records are identified by the following rules:

  * ParentData record type if dataKbn is 1 and type is 01.
  * ChildData record type if dataKbn is 2 and type is 02.

  .. code-block:: bash

    file-type:        "Fixed" # Fixed-length
    text-encoding:    "MS932" # Character encoding of the string type field
    record-length:    40      # Length of each record
    record-separator: "\r\n"  # Carriage return and Line feed (crlf)

    # Define record identification field
    [Classifier]
    1   dataKbn X(1)      # First 1 byte
    10  type    X(2)      # 2 bytes from the 10th byte

    [parentData]
    dataKbn = "1"
    type    = "01"
    1  dataKbn X(1)
    2  ?filler X(9)
    10 type    X(2)
    13 data    X(28)

    [childData]
    dataKbn = "1"
    type    = "02"
    1  dataKbn X(1)
    2  ?filler X(9)
    10 type    X(2)
    13 data    X(28)

Example when the identification item is different for each record
  When items used for identification differ for each record, all fields used for identification are defined in the record identification field. 
  In the condition definition section of each record, a condition for identifying the record is defined.

  In this example, records are identified by the following rules:

  * Header record type if dataKbn is 1.
  * Data1 record type if dataKbn is 2 and type is 01.
  * Data2 record type if dataKbn is 2 and type is 02.

  .. code-block:: bash

    file-type:        "Fixed" # Fixed-length
    text-encoding:    "MS932" # Character encoding of the string type field
    record-length:    40      # Length of each record
    record-separator: "\r\n"  # Carriage return and Line feed (crlf)

    # Define record identification field
    [Classifier]
    1   dataKbn X(1)      # First 1 byte
    10  type    X(2)      # 2 bytes from the 10th byte

    # Header
    [header]
    dataKbn = "1"
    1  dataKbn X(1)
    2  ?filler X(39)

    [data1]
    dataKbn = "2"
    type    = "01"
    1  dataKbn X(1)
    2  ?filler X(9)
    10 type    X(2)
    13 data    X(28)

    [data2]
    dataKbn = "2"
    type    = "02"
    1  dataKbn X(1)
    2  ?filler X(9)
    10 type    X(2)
    13 data    X(28)

Sample Collection of Variable (Variable Length) Multi Format Definition
--------------------------------------------------------------------------------
This section describes the definition method for multi-format for variable (variable length) data.

Example of identifying format with a single field
  When a single field is a condition, if the field value matches the condition defined in each format, then it is processed with the record definition.

  In this example, records are identified by the following rules:

  * Header record type if dataKbn is 1.
  * Data record type if dataKbn is 2.

  .. code-block:: bash

    file-type:        "Variable" # Variable length
    text-encoding:    "MS932"    # Character encoding of the string type field
    record-separator: "\r\n"     # Carriage return and Line feed (crlf)
    field-separator:  ","        # csv


    # Define record identification field
    [Classifier]
    1 dataKbn X

    # Define the header record
    [header]
    dataKbn = "1"
    1 dataKbn X
    2 data    X

    # Define data record
    [data]
    dataKbn = "2"
    1 dataKbn X
    2 data    X

Example of identifying format with multiple fields
  When a record is identified by multiple of fields, the processing is performed by the record definition if all conditions are satisfied.

  In this example, records are identified by the following rules:

  * ParentData record type if dataKbn is 1 and type is 01.
  * ChildData record type if dataKbn is 2 and type is 02.

  .. code-block:: bash

    file-type:        "Variable" # Variable length
    text-encoding:    "MS932"    # Character encoding of the string type field
    record-separator: "\r\n"     # Carriage return and Line feed (crlf)
    field-separator:  ","        # csv

    # Define record identification field
    [Classifier]
    1 dataKbn X
    3 type    X

    [parentData]
    dataKbn = "1"
    type    = "01"
    1 dataKbn X
    2 ?filler X
    3 type    X
    4 data    X

    [childData]
    dataKbn = "1"
    type    = "02"
    1 dataKbn X
    2 ?filler X
    3 type    X
    4 data    X
 
Example when the identification item is different for each record
  When items used for identification differ for each record, all fields used for identification are defined in the record identification field. 
  In the condition definition section of each record, a condition for identifying the record is defined.

  In this example, records are identified by the following rules:

  * Header record type if dataKbn is 1.
  * Data1 record type if dataKbn is 2 and type is 01.
  * Data2 record type if dataKbn is 2 and type is 02.

  .. code-block:: bash

    file-type:        "Variable" # Variable length
    text-encoding:    "MS932"    # Character encoding of the string type field
    record-separator: "\r\n"     # Carriage return and Line feed (crlf)
    field-separator:  ","        # csv

    # Define record identification field
    [Classifier]
    1   dataKbn X
    3   type    X

    # Header
    [header]
    dataKbn = "1"
    1 dataKbn X
    2 ?filler X

    [data1]
    dataKbn = "2"
    type    = "01"
    1 dataKbn X
    2 ?filler X
    3 type    X
    4 data    X

    [data2]
    dataKbn = "2"
    type    = "02"
    1 dataKbn X
    2 ?filler X
    3 type    X
    4 data    X

.. _data_format-variable_title_sample:

Example of using title record
  For variable length file With :ref:`title record <data_format-requires-title>` , defining record identification conditions for title records is not required.

  When the format other than title record is a single format, definition of record identifier ( ``Classifier`` ) is not required as shown in the example below. 
  The layout definition of the title record is defined with ``Title``  as the record type name.

  .. code-block:: bash

    # If requires-title is true, the first line is read and written as the title.
    requires-title: true  

    # Title-specific record type The first line is read and written with this record type.
    [Title]               
    1   Kubun      N
    2   Name       N
    3   Publisher  N
    4   Authors    N
    5   Price      N

    # Data record type. The lines after the first line are read and written with this record type.
    [DataRecord]          
    1   Kubun      X
    2   Name       N
    3   Publisher  N
    4   Authors    N
    5   Price      N

  When the format other than title record is multi-format, definition of record identifier ( ``Classifier`` ) is required as shown in the example below. 
  For the record definition whose record type indicating the title record is  ``Title`` , the condition definition required for multi-format is not required.

  .. code-block:: bash

    file-type:    "Variable"     # Variable length
    text-encoding:     "ms932"   # File encoding
    record-separator:  "\r\n"    # Carriage return and Line feed line break
    field-separator:   ","       # Field separator character
    quoting-delimiter: "\""      # Enclosing character
    requires-title: true         # Read/write first line as title


    [Classifier]
    1  Kubun X                   # Record type identification field (data classification)
                                 # 1: Data, 2: Trailer

    # Title-specific record type Multi-format does not require format application conditions.
    [Title]                      
    1   Kubun      N  "Data partition"
    2   Name       N  "Book title"
    3   Publisher  N  "Publisher"
    4   Authors    N  "Authors"
    5   Price      N  "Price"

    [DataRecord]                 # Data record type
      Kubun = "1"                # Data format application conditions
    1   Kubun      X             # Data partition
    2   Name       N             # Book title
    3   Publisher  N             # Publisher
    4   Authors    N             # Authors
    5   Price      N             # Price

    [TrailerRecord]              # Trailer record type
      Kubun = "2"                # Trailer format application conditions
    1   Kubun      X             # Data partition
    2   RecordNum  X             # The total number of cases

  .. tip::
    
    To change the record type name of the title record from  ``Title`` , use :ref:`data_format-title_type_name directive <data_format-title_type_name>` . 
    In that case, change the record type name that indicates the title record from  ``Title``  to the value configured in :ref:`data_format-title_type_name directive <data_format-title_type_name>` .


