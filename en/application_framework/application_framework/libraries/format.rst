.. _`format`:

Formatter
==================================================

.. contents:: Table of contents
  :depth: 3
  :local:

Function overview
---------------------------------------------------------------------

Provides a function to format data such as date and number, and convert it to string type. 
By consolidating the format configuration in this function, configuration is not necessary for each format such as screen, file and email.


Module list
---------------------------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core</artifactId>
  </dependency>

How to use
---------------------------------------------------------------------

Configure the formatter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This function can use the formatter that the framework supports by default even without any configuration.

To change the default format pattern or add a formatter, refer to :ref:`format_custom`  and add the configuration to the system repository.

Use the formatter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use :java:extdoc:`FormatterUtil <nablarch.core.text.FormatterUtil>` for formatting.

The formatter has a separate name from the class name to specify the formatter to be used.

When calling FormatterUtil.format, formatter name, format target, and format pattern are specified, 
and an appropriate formatter is selected based on the format name and data type to be formatted.

Formatted using the selected formatter and specified format pattern. 
If the format pattern is not specified explicitly, the default pattern configured for each formatter is used.

Implementation examples

.. code-block:: java

  // Format using the default pattern
  // Specify the name of the formatter to use for the first argument
  // Specify the value to format in the second argument
  FormatterUtil.format("dateTime", input);

  // When specifying a pattern for formatting
  // Specify the first and second arguments in the same way as the default pattern
  // Specify the format pattern to use for the third argument.
  FormatterUtil.format("dateTime", input, "yyyy/MM/dd");

The formatter provided by default with this function are shown below:

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 20,40,40,40

  * - Formatter name
    - Type of data to format
    - Default format pattern
    - Remarks

  * - :ref:`dateTime <format_datetime>`
    - :java:extdoc:`Date <java.util.Date>`
    - yyyy/MM/dd
    -

  * - :ref:`dateTime <format_datetime>`
    - :java:extdoc:`String <java.lang.String>`
    - yyyy/MM/dd
    - Requires a pattern to format the date string (default ``yyyyMMdd`` )
    
  * - :ref:`number <format_number>`
    - :java:extdoc:`Number <java.lang.Number>`
    - #,###.###
    -

  * - :ref:`number <format_number>`
    - :java:extdoc:`String <java.lang.String>`
    - #,###.###
    -

.. _`format_dateTime`:

dateTime
  Formatter for formatting dates.

  The types to be formatted are  :java:extdoc:`Date <java.util.Date>` , its derived classes and  :java:extdoc:`String <java.lang.String>` . 
  For the pattern, specify the syntax specified by :java:extdoc:`SimpleDateFormat <java.text.SimpleDateFormat>`. 
  The default pattern is  ``yyyy/MM/dd`` .

  To format :java:extdoc:`String <java.lang.String>` , the pattern of the date string to be formatted should also be configured. 
  The date string pattern to be formatted is  ``yyyyMMdd``  by default. To change the configuration, refer to  :ref:`format_custom` .

.. _`format_number`:

number
  Formatter for formatting numerics.

  The types to be formatted are  :java:extdoc:`Number <java.lang.Number>` , its derived classes and  :java:extdoc:`String <java.lang.String>` . 
  For the pattern, specify the syntax specified by :java:extdoc:`DecimalFormat <java.text.DecimalFormat>`. 
  The default pattern is  ``#,###.###`` .

Usage examples
  For example, to output to a file using data binding with this function, 
  use it with getter of Bean.


  .. code-block:: java

    import java.util.Date;

    public class SampleDto {
        private Date startDate;
        private Integer sales;

        // Create a getter to acquire the formatted string
        public String getFormattedStartDate() {
            return FormatterUtil.format("dateTime", startDate);
        }

        public String getFormattedSales() {
            return FormatterUtil.format("number", sales, "#,### Yen");
        }

        // Other setters and getters are omitted.
    }


.. _`format_custom`:

Change the formatter configuration
---------------------------------------------------------------------

The following procedures are required to change the formatter configuration.

Configure  ``nablarch.core.text.FormatterConfig`` in the component configuration file.

  Point
   * The component name should be  ``formatterConfig`` .

  Configure the formatter list used for ``nablarch.core.text.FormatterConfig`` . 
  The property name of the list should be  ``formatters`` .


  The default format configuration supported by the framework is shown below.

  .. code-block:: xml

    <component name="formatterConfig" class="nablarch.core.text.FormatterConfig">
      <!-- List holding formatters -->
      <property name="formatters">
        <list>
          <component class="nablarch.core.text.DateTimeFormatter">
            <!-- Name to use when calling the formatter -->
            <property name="formatterName" value="dateTime" />
            <!-- Configure the default format pattern -->
            <property name="defaultPattern" value="yyyy/MM/dd" />
          </component>
          <component class="nablarch.core.text.DateTimeStrFormatter">
            <property name="formatterName" value="dateTime" />
            <property name="defaultPattern" value="yyyy/MM/dd" />
            <!-- Configuration of the properties that represent the date string pattern
                 is also required for the formatter of date string -->
            <property name="dateStrPattern" value="yyyyMMdd" />
          </component>
          <component class="nablarch.core.text.NumberFormatter">
            <property name="formatterName" value="number" />
            <property name="defaultPattern" value="#,###.###" />
          </component>
          <component class="nablarch.core.text.NumberStrFormatter">
            <property name="formatterName" value="number" />
            <property name="defaultPattern" value="#,###.###" />
          </component>
        </list>
      </property>
    </component>

  .. important::
    When changing the default formatter configuration in component definition, 
    configuration for formatters and properties that do not change should be described. 
    Formatters not described in the component definition cannot be used.


Adding formatter
---------------------------------------------------------------------

The following steps are required to add a formatter.

1. Create the implementation class :java:extdoc:`Formatter <nablarch.core.text.Formatter>` .

  Format process is performed by the class that implements  :java:extdoc:`Formatter <nablarch.core.text.Formatter>` .


2. Add the formatter configuration created in the component configuration file

  Configure  ``nablarch.core.text.FormatterConfig``  and format list to the component configuration file by refering to :ref:`format_custom` .

  .. code-block:: xml

    <component name="formatterConfig" class="nablarch.core.text.FormatterConfig">
      <property name="formatters">
        <list>
          <!-- Default formatter -->
          <component class="nablarch.core.text.DateTimeFormatter">
            <property name="formatterName" value="dateTime" />
            <property name="defaultPattern" value="yyyy/MM/dd" />
          </component>
          <component class="nablarch.core.text.DateTimeStrFormatter">
            <property name="formatterName" value="dateTime" />
            <property name="defaultPattern" value="yyyy/MM/dd" />
            <property name="dateStrPattern" value="yyyyMMdd" />
          </component>
          <component class="nablarch.core.text.NumberFormatter">
            <property name="formatterName" value="number" />
            <property name="defaultPattern" value="#,###.###" />
          </component>
          <component class="nablarch.core.text.NumberStrFormatter">
            <property name="formatterName" value="number" />
            <property name="defaultPattern" value="#,###.###" />
          </component>
          <!-- Added formatter -->
          <component class="sample.SampleFormatter">
            <property name="formatterName" value="sample" />
            <property name="defaultPattern" value="#,### Yen" />
          </component>
        </list>
      </property>
    </component>
