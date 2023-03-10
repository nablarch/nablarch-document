========================================
Online Access Log Aggregation Function
========================================
The Online Access Log Aggregation Function aggregates the following information into one request ID [#r1]_ , based on the access log output from the screen function.

* Number of requests
* Number of requests with processing time exceeding the threshold
* Processing time (average)
* Processing time (median)
* processing time（maximum value）

.. [#r1]
  By specifying the request ID in the configuration file, the function to be aggregated can be narrowed down.

  See \ `Online access log analysis and configuration of aggregation`_\  sample for configuration examples.

------------------------------
Sample structure
------------------------------
This sample consists of the following three types.

============================================================    ========================================================================================================================================
Sample name                                                      Summary
============================================================    ========================================================================================================================================
`Online access log analysis batch`_                             Batch processing that analyzes the online access log and outputs only the information needed for aggregation to a CSV file.
`Online access log analysis result aggregation batch`_          Batch processing to perform aggregate processing based on the CSV file output by `Online access log analysis batch`_\ .

                                                                The aggregation period will be for the number of days specified in the configuration file.

`Online access log aggregation result reporting sample`_        Excel marco that outputs a report (table of aggregate results) to Excel based on the aggregate results output 
                                                                by the `Online access log analysis result aggregation batch`_\ .
============================================================    ========================================================================================================================================

Process flow
===============
The following is a flow of processing until the online access log using the above sample and outputting the report information to Excel

 .. image:: ../_images/OnlineLogStatistics.png
    :width: 100%

\

.. tip::

 In the above diagram, the online log deployment server and the terminal in charge of operations are explicitly described separately.
 This is because the online access log may contain personal information and it is recommended to do it in a secure environment.

 Since the request information aggregation result does not include items such as personal information, although it may be run in a non-secure environment,
 there is no particular problem in running the log analysis and aggregation process in the environment in which it was executed.


----------------------------------------------------------
Specifications and execution procedures for each sample
----------------------------------------------------------

Online access log analysis batch
==================================
Batch processing that analyzes the online access log and outputs only the information needed for aggregate processing to a CSV file.

This sample is assumed to be executed on a daily basis.
In addition, CSV files of analysis results should be stored as analysis results without deleting them.By collecting the analysis results CSV for the past, 
it is possible to perform accurate aggregation processing in the subsequent \ `Online access log analysis result aggregation batch`_\ processing.

The CSV file name is "REQUEST_INFO\_ + "system date (8 digits)" + .csv".

The following information is output to the CSV file after executing this batch.

**Output contents to a CSV file**

=================== =====================================================================
Item name           Remarks
=================== =====================================================================
Years               End of request (END) Year of log output
Month               End of request (END) Month of log output
Day                 End of request (END) date and time of log output
Process name        Process name

                    ?Blank if no process name is output to the log
Request ID          Request ID
processing time     Request processing time
Status code         Process status code
=================== =====================================================================

Configuration information for executing this sample
------------------------------------------------------
See `Online access log analysis and configuration of aggregation`_\  sample.

Execution
----------
This batch is implemented using the :ref:`nablarch_batch` .

The following parameters are required when running this sample.

* diConfig

  You can specify "main/resources/statistics-batch.xml" in the log aggregation function project. 
  When the classpath is configured to the resources directory, the specified value is "statistics-batch.xml".

* requestPath

  Specify the class name (OnlineAccessLogParseAction) of this batch action class.

* userId

  Configure the batch user ID.



Online access log analysis result aggregation batch
=======================================================
Batch processing to perform aggregate processing based on the CSV file output by `Online access log analysis batch`_\ . The aggregation period will be for the number of days specified in the configuration file.

.. tip::

  The number of target days is determined by using the date included in the file name of the analysis result.

  An example is shown below.

  * When analysis processing is executed daily.

    When the analysis results of the following four files are used as inputs for tabulation, and the batch execution date is October 10, 2012 and the tabulation period is set to two days in the past, 
    the CSV files from October 8 to October 10, 2012 are the tabulation targets.

    The content of each CSV file contains only one day's analysis results, so the range of calculation is basically the same as the past two days specified.

    | REQUEST_INFO_20121007.csv     (Analysis of the online logs for seventh)
    | REQUEST_INFO_20121008.csv     (Analysis of the online logs for eighth)
    | REQUEST_INFO_20121009.csv     (Analysis of the online logs for ninth)
    | REQUEST_INFO_20121010.csv     (Analysis of the online logs for tenth)

  * When the analysis process is not executed daily (for example, when it is executed once every two days)

    When the analysis results of the following two files are used as inputs for tabulation, and the batch execution date is October 10, 2012 and the tabulation period is set to two days in the past,
    the CSV files from October 8 to October 10, 2012 are the tabulation targets.

    In this case, because the CSV file of 20121008 contains analysis results for two days (7 and 8), 
    Logs output on October 7 beyond the past two days, which is the aggregation range, are also output as aggregate results.

    | REQUEST_INFO_20121008.csv     (Analysis of the online logs for the seventh and eighth)
    | REQUEST_INFO_20121010.csv     (Analysis of the online logs for the ninth and tenth)

The following three CSV files are output as the aggregation result.

======================================= ======================================================================================================================
File name                               Output contents
======================================= ======================================================================================================================
Aggregate results by time               Outputs hourly aggregate processing.

Aggregate results by day                Outputs aggregate results on a daily basis.

Aggregate results by year and month     Outputs aggregate results for each year and month.

                                        Note that the year-month-by-year tabulation results only include data for the system monthly date. For this reason,
                                        the aggregate results of the past years should be accumulated without deleting them.

                                        .. tip::

                                          If the range is less than one month, such as 10 days, \
                                          the value output in the month/year summary results will be 10 days only.
                                          If the aggregation process is executed on 30th and the range of aggregation is 10 days, \
                                          the range from 20th to 30th is the target of aggregation.
======================================= ======================================================================================================================

**Output contents to a CSV file**

============================================================================== ==============================================================================================================
Item name                                                                      Remarks
============================================================================== ==============================================================================================================
Request ID                                                                     Request ID
Period for aggregation                                                         The following values are output for each file.
                                                                               ::

                                                                                By time: 0 - 23
                                                                                By day1 - 31
                                                                                By month and year: Month and year of system date
Process name                                                                   Process name
Number of requests                                                             Number of requests in the period under review
Number of requests for which the processing time exceeds the threshold.        The number of requests whose processing time exceeds the threshold time specified in the configuration file.
Processing time (average)                                                      Average value within the aggregation period
Processing time (median)                                                       Median value within the aggregation period
Processing time (maximum processing time within the aggregation target period) Maximum processing time within the aggregation target period
============================================================================== ==============================================================================================================

Configuration information for executing this sample
----------------------------------------------------------
See `Online access log analysis and configuration of aggregation`_\  sample.


Execution
------------
This batch is implemented using the :ref:`nablarch_batch` .

The following parameters are required when running this sample.

* diConfig

  You can specify "main/resources/statistics-batch.xml" in the log aggregation function project. 
  When the classpath is configured to the resources directory, the specified value is "statistics-batch.xml".

* requestPath

  Specify the class name (RequestInfoAggregateAction) of this batch action class.

* userId

  Configure the batch user ID.


Online access log aggregation result reporting sample
===========================================================
This sample outputs a report (table of aggregate results) to Excel based on the aggregate results output by the online access log analysis result aggregation batch.

This sample is a sample to create a table of aggregate results. When creating a graph based on a table, use the Excel function to create a graph.


Execution
------------
For details on how to use, refer to the following files under the log aggregation project.

* /tool/WebApplicationRequestReportingTool.xls


Online access log analysis and configuration of aggregation
===================================================================
Describes the configuration values for executing `Online access log analysis batch`_\ and \ `Online access log analysis result aggregation batch`_\ .

The configuration value must be set in the \ **please.change.me.statistics.action.settings.OnlineStatisticsDefinition**\  property and all are required items.

However, since the configuration values of the standard configuration are prepared in the following files of the operational information statistical function project, 
only the items that need to be changed depending on the environment of the project that uses this sample need to be modified.

* main/resources/statistics/onlineStatisticsDefinition.xml
* main/resources/statistics/statistics.config

==============================    ============================================================================================================================================
Configuration property name                  Settings
==============================    ============================================================================================================================================
accessLogDir                      The path of the directory where the online access log to be analyzed is stored.

                                  Specify with absolute path or relative path.

accessLogFileNamePattern          File name pattern of online access log to be analyzed

                                  Use "*" to specify any value. (Note that this is different from regular expressions.)

                                  Example:
                                    If the file name always starts with "access", specify "access*".
                                  
accessLogParseDir                 Path to the temporary directory used to analyze the access log

                                  The access log to be analyzed is copied to this directory and analyzed.

                                  Specify with absolute path or relative path.


endLogPattern                     Regular expression pattern to identify the access log termination log

includeRequestIdList              Set the request ID list to be analyzed.

                                  .. tip::

                                   If the request ID has increased or decreased, add (delete) the request ID to be analyzed.

==============================    ============================================================================================================================================


==============================    ============================================================================================================================================
Configuration property name                  Settings
==============================    ============================================================================================================================================
findRequestIdPattern              Regular expression for extracting request ID from end log

                                  Set a regular expression so that the part where the request ID is output is grouped.

findProcessNamePattern            Regular expression for extracting the process name from the end log

                                  Set a regular expression so that the part where the process name is output is grouped.

findStatusCodePattern             Regular expression for extracting status code from end log

                                  Set the regular expression so that the part where the status code is output is grouped.

logOutputDateTimeStartPosition    Start position of the area where the log output date and time is output

                                  Set the number of characters starting from 0. (Same specification as String#substring)

logOutputDateTimeEndPosition      End position of the area where the log output date and time is output

                                  Set the number of characters starting from 0. (Same specification as String#substring)

logOutputDateTimeFormat           Format of log output date and time

                                  It is set by the type which can be specified in SimpleDateFormat.

findExecutionTimePattern          Regular expression for extracting the processing time of a request

                                  Set the regular expression so that the part where the processing time is output is grouped.

thresholdExecutionTime            Threshold of the processing time for one request (milliseconds)

                                  This is used to obtain the number of requests whose processing time exceeds the threshold.
                                  For example, if it is set to 3000, the number of requests exceeding 3 seconds can be calculated.

aggregatePeriod                   Configure the aggregation period.

                                  It is recommended to set a minimum of 30 to ensure that the year and month are aggregated without fail.
==============================    ============================================================================================================================================


==============================    ============================================================================================================================================
Configuration property name                  Settings
==============================    ============================================================================================================================================
requestInfoFormatName             File name of the format definition file of the analysis result CSV

                                  The definition file uses the following files under the log aggregation project.

                                  This format file is also used when reading the analysis results in \ `Online access log analysis result aggregation batch`_.

                                  * main/format/requestInfo.fmt

                                  .. tip::

                                    Basically, it is not necessary to specify any other format definition file than the one mentioned above.
                                    However, when the analysis and aggregation batches are extended and the items output to the format definition file are added (deleted), 
                                    it is necessary to create the format definition file corresponding to the extended batch.
                                    In such a case, it is necessary to set the name of the newly created format definition file.


requestInfo.dir                   Logical name of the output destination directory of the analysis result CSV

                                  Refer to the following files under the log aggregation project for mapping with the actual directory.

                                  * main/resources/statistics/file.xml

requestInfoSummaryBaseName        Logical name of the output destination directory for the aggregation result CSV

                                  Refer to the following files under the log aggregation project for mapping with the actual directory.

                                  * main/resources/statistics/file.xml

requestInfoSummaryFormatName      Format definition file name of the aggregation result CSV file

                                  The definition file uses the following files under the log aggregation project.

                                  * main/format/requestInfoAggregate.fmt

                                  .. tip::

                                    Basically, it is not necessary to specify any other format definition file than the one mentioned above.
                                    However, when the item output to the format definition file is added (deleted) by extending the aggregation batch, 
                                    it is necessary to create the format definition file corresponding to the extended batch.
                                    In such a case, it is necessary to set the name of the newly created format definition file.

==============================    ============================================================================================================================================
