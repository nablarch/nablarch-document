======================================================
Field Type Expansion in the Data Formatter Function
======================================================

The specifications of the formatter functions provided in this sample are described.

For an overview of the formatter functions and more information on basic general data formatting functions, see :ref:`data_format`.

----------------------------
Summary
----------------------------

When data linking double-byte characters of EBCDIC (CP930), a shift code may be added before and after the item. 
However, when data linking with a host computer, 
the shift code may not be added since it is assumed that the item starts in the shift out state even if it is a double-byte character.

Thus, depending on the interface with the connection destination system, the shift code may or may not be added and each case must be handled.

This sample provides a data type class for double-byte characters of EBCDIC (CP930) with a shift code, 
and a data type class for double-byte characters of EBCDIC (CP930) without a shift code.

Since it is assumed that the double-byte string data type (DoubleByteCharacterString) provided in Nablarch by default is used for input/output of the full-width characters (double-byte characters) field when the character code of the file is Shift_JIS or MS932, each project must expand when handling EBCDIC (CP930).

(Whether a shift code is added or not depends on the JDK, 
and CP930 used in the JDK must have a shift code added to double-byte characters.)

Since the shift code is added and removed transparently when this data type is used, it is possible to absorb the difference mentioned above and convert it into a string or encode it into a byte sequence.



Delivery package
--------------------------------------------------------------------

The functions are provided in the below package.

  *please.change.me.* **core.dataformat.convertor.datatype**


Structure of field type
--------------------------------------------------------------------

The sample is an assumption that corresponds to both the case where a 2-byte string item in a fixed length file in EBCDIC (CP930) is assigned a shift code and the case where it is not assigned.
Hence, the following field type classes are added.

The following is a list of classes used in this function.

  .. list-table::
   :widths: 130 150 200
   :header-rows: 1

   * - Package name
     - Class name
     - Summary
   * - *please.change.me.* **core.dataformat.** **convertor.datatype**
     - EbcdicDoubleByteCharacterString
     - | Data type class for double-byte strings of EBCDIC (CP930).
       | It is used for input/output of full-width character (double-byte character) field of fixed-length data format.
       | It is implemented as a data type that **assumes the shift code** is used for the input/output byte data.
   * - *please.change.me.* **core.dataformat.** **convertor.datatype**
     - EbcdicNoShiftCodeDoubleByteCharacterString
     - | Data type class for double-byte strings of EBCDIC (CP930).
       | It is used for input/output of full-width character (double-byte character) field of fixed-length data format.
       | It is implemented as a data type that **assumes the shift code** is not used for the input/output byte data.



How to use the field type
--------------------------------------------------------------------
  For details on how to use the added field types, see :ref:`data_format-field_type_add`.
  An implementation example of a fixed-length format factory class is shown below.

  .. code-block:: java

    public class EbcdicFixedLengthConvertorFactory extends FixedLengthConvertorFactory {
        @Override
        protected Map<String, Class<?>> getDefaultConvertorTable() {
            final Map<String, Class<?>> defaultConvertorTable = new CaseInsensitiveMap<Class<?>>(
                    new ConcurrentHashMap<String, Class<?>>(super.getDefaultConvertorTable()));
            // Add data types ESN and EN for EBCDIC (CP930)
            // Add data types ESN and EN for EBCDIC (CP930)
            defaultConvertorTable.put("ESN", EbcdicDoubleByteCharacterString.class);
            defaultConvertorTable.put("EN", EbcdicNoShiftCodeDoubleByteCharacterString.class);
            return Collections.unmodifiableMap(defaultConvertorTable);
        }
    }



Field type and field converter definition list
--------------------------------------------------------------------
  This section describes the field types that have been added.

  **Field type**

  .. list-table::
   :widths: 130 150 200
   :header-rows: 1

   * - Type identifier
     - Java type
     - Details
   * - ESN
     - String
     - | Double-byte string (byte length = number of characters x 2 + 2 (shift code part))
       | This sample performs right trim and padding with full-width empty space by default.
       | During input, the shift-out/shift-in codes are assumed to be added and converted to a string without anything being done,
       | while during output, the shift-out/shift-in codes are added automatically.
       | Sample implementation class: please.change.me.core.dataformat.converter.datatype.EbcdicDoubleByteCharacterString
       | argument: Byte length (numerical value, specification required)
   * - EN
     - String
     - | Double-byte string (byte length = number of characters x 2)
       | This sample performs right trim and padding with full-width empty space by default.
       | During input, the shift-out/shift-in codes are complemented internally and converted into a string,
       | while during output, the shift-out/shift-in codes are not added.
       | Sample implementation class: please.change.me.core.dataformat.converter.datatype.EbcdicNoShiftCodeDoubleByteCharacterString
       | argument: Byte length (numerical value, specification required)
