Log Output of Progress Status
==================================================
.. contents:: Table of contents
  :depth: 3
  :local:
  
.. _jsr352-progress_log:

Contents output in the progress log
--------------------------------------------------
Outputs the following content to the log:

* Job start and end logs
* Step start and end logs
* Number of logs for processing (The number of logs for processing must be determined by the application)
* Logs for progress status of steps

  * TPS (calculated from the number of logs for processing and number of processed logs) from the start
  * Latest TPS (TPS calculated from the elapsed time during previous TPS calculation and number of processed logs)
  * Unprocessed number
  * Estimated end time (estimated end time of step determined from unprocessed number and TPS).
  
An output example is shown below.

.. code-block:: bash

  INFO progress start job. job name: [test-job]
  INFO progress start step. job name: [test-job] step name: [test-step]
  INFO progress job name: [test-job] step name: [test-step] input count: [25]
  INFO progress job name: [test-job] step name: [test-step] total tps: [250.00] current tps: [250.00] estimated end time: [2017/02/13 04:02:25.656] remaining count: [15]
  INFO progress job name: [test-job] step name: [test-step] total tps: [384.62] current tps: [519.32] estimated end time: [2017/02/13 04:02:25.668] remaining count: [5]
  INFO progress job name: [test-job] step name: [test-step] total tps: [409.84] current tps: [450.00] estimated end time: [2017/02/13 04:02:25.677] remaining count: [0]
  INFO progress finish step. job name: [test-job] step name: [test-step] step status: [null]
  INFO progress finish job. job name: [test-job]

Add the configuration to output the progress log to a dedicated log file
---------------------------------------------------------------------------------
Output the log indicating progress with the log category name as  ``progress`` . 
By using this category name, the log can be output to the progress log file.

Shown below is an configuration example of ``log.properties`` when the :ref:`log` is used. 
When using :ref:`log_adaptor` , refer to the manual of the log library corresponding to the adapter to perform the configuration.

.. code-block:: properties

  # progress log file
  writer.progressLog.className=nablarch.core.log.basic.FileLogWriter
  writer.progressLog.filePath=./log/progress.log
  writer.progressLog.encoding=UTF-8
  writer.progressLog.formatter.className=nablarch.core.log.basic.BasicLogFormatter
  writer.progressLog.formatter.format=$date$ -$logLevel$- $message$
  
  # logger list
  availableLoggersNamesOrder=SQL,MON,PROGRESS,ROO
  
  # progress logger setting
  loggers.PROGRESS.nameRegex=progress
  loggers.PROGRESS.level=INFO
  loggers.PROGRESS.writerNames=progressLog

Output the progress log in batchlet step
--------------------------------------------------
An implementation example to output the progress status to the log with batchlet step is shown below.

There are few cases where the batchlet requires a progress log to execute task-oriented processes. 
If loop processing is required in the batchlet, it would be better to output the progress log based on the implementation example given below.

Point
  * At the beginning of the process method, acquire the number for processing (count result to the database, number of records in file, etc.) and configure in :java:extdoc:`inputCount <nablarch.fw.batch.ee.progress.ProgressManager.setInputCount(long)>` .
  
    .. important::
    
      The starting time for calculating TPS is the timing when  :java:extdoc:`inputCount <nablarch.fw.batch.ee.progress.ProgressManager.setInputCount(long)>` is called. 
      If intensive processing such as extracting the target data from the database after calling :java:extdoc:`inputCount <nablarch.fw.batch.ee.progress.ProgressManager.setInputCount(long)>` is performed, the TPS will be different (a value that is smaller than the actual value) from the actual result.
      
  * Calls :java:extdoc:`outputProgressInfo <nablarch.fw.batch.ee.progress.ProgressManager.outputProgressInfo(long)>` to output the progress log at regular intervals in the loop process that performs the process.

Implementation examples
  .. code-block:: java

    @Named
    @Dependent
    public class ProgressBatchlet extends AbstractBatchlet {

        /** Function to output the progress log */
        private final ProgressManager progressManager;
        
        /** Progress log output interval */
        private static final int PROGRESS_LOG_INTERVAL = 1000;

        /**
         * Use constructor injection to inject the function to output the progress log.
         */
        @Inject
        public ProgressBatchlet(ProgressManager progressManager) {
          this.progressManager = progressManager;
        }

        @Override
        public String process() throws Exception {
         
          // Configures the number for processing.
          // The number for processing is the number of records in the database or file.
          progressManager.setInputCount(10000);
          
          // Number of processed logs
          long processedCount = 0;
          
          while (while the processing targets exists) {
              processedCount++;
              
              //  Actual process omitted
              
              if (processedCount % PROGRESS_LOG_INTERVAL == 0) {
                // The progress log is output by transferring the number of processed logs to the progress log output function
                progressManager.outputProgressInfo(processedCount);
              }
          }
          return "SUCCESS";
        }
    }
  
Output the progress log in chunk step
--------------------------------------------------
An implementation example to output the progress status to the log with chunk step is shown below.

.. _jsr352-progress_reader:

ItemReader
  Point
    * Use constructor injection to inject the interface ( :java:extdoc:`ProgressManager <nablarch.fw.batch.ee.progress.ProgressManager>` ) that outputs the progress log.
    * With the open method, acquire the number for processing (count result to the database, number of records in file, etc.) and set in :java:extdoc:`inputCount <nablarch.fw.batch.ee.progress.ProgressManager.setInputCount(long)>` .
    
      .. important::
      
        The starting time for calculating TPS is the timing when :java:extdoc:`inputCount <nablarch.fw.batch.ee.progress.ProgressManager.setInputCount(long)>` is called. 
        If intensive processing such as extracting the target data from the database after calling :java:extdoc:`inputCount <nablarch.fw.batch.ee.progress.ProgressManager.setInputCount(long)>` is performed, the TPS will be different (a value that is smaller than the actual value) from the actual result.
    
  Implementation examples
    .. code-block:: java

      @Named
      @Dependent
      public class ProgressReader extends AbstractItemReader {

        /** Function to output the progress log */
        private final ProgressManager progressManager;

        /**
         * Use constructor injection to inject the function to output the progress log.
         */
        @Inject
        public ProgressReader(ProgressManager progressManager) {
            this.progressManager = progressManager;
        }

        @Override
        public void open(Serializable checkpoint) throws Exception {
          // Configure the number for processing in the function that outputs the progress log with the open method.
          // Configures the result of the count statement for the database and number of records in the file
          progressManager.setInputCount(10000);
        }

        @Override
        public Object readItem() throws Exception {
          // Omitted
        }
      }

.. _jsr352-progress_listener:

Job definition file
  Point
    * Configure the listener that outputs the progress log to the list of listeners (name is fixed as ``progressLogListener`` ) under step.
    
  Implementation examples
    .. code-block:: xml
    
      <job id="batchlet-progress-test" xmlns="https://jakarta.ee/xml/ns/jakartaee" version="2.0">
        <listeners>
          <listener ref="nablarchJobListenerExecutor" />
        </listeners>
      
        <step id="step">
          <listeners>
            <listener ref="nablarchStepListenerExecutor" />
            <listener ref="nablarchItemWriteListenerExecutor" />
            <!-- Configure the listener that outputs the progress log under step. -->
            <listener ref="progressLogListener" />
          </listeners>
          <chunk item-count="1000">
            <reader ref="progressReader" />
            <writer ref="progressWriter" />
          </chunk>
        </step>
      </job>

.. important::
  If :ref:`the progress log output listener <jsr352-progress_listener>` is configured without setting the number of logs for processing in :ref:`ItemReader <jsr352-progress_reader>` , an exception is thrown as a setting fault and the operation ends abnormally. 
  Therefore, if the progress log is not required, make sure to delete the configuration of :ref:`the progress log output listener <jsr352-progress_listener>` .
  
.. important::
  If the setting of retrying exceptions was performed in the chunk step, the progress log output by the listener will not function properly. 
  This is because the number of read logs :java:extdoc:`metrics <jakarta.batch.runtime.context.StepContext.getMetrics()>` being used by the listener as the number of processed logs, deviates from the actual number.
  
  To perform the retry process using retrying exceptions when an exception occurs, calculate the number of processed logs with the implementation class :java:extdoc:`ItemWriter <jakarta.batch.api.chunk.ItemWriter>` and output the progress log using :java:extdoc:`outputProgressInfo <nablarch.fw.batch.ee.progress.ProgressManager.outputProgressInfo(long)>` .
  

