Launching the Jakarta Batch Application
==================================================
.. contents:: Table of contents
  :depth: 3
  :local:

.. _jsr352_run_batch_application:

Launch the batch application
--------------------------------------------------
In the case of Jakarta Batch-compliant batch application, the batch is launched using an API specified by Jakarta Batch.

Nablarch provides :java:extdoc:`nablarch.fw.batch.ee.Main`  as the standard implementation class. 
This class specifies the XML file name (file name excluding .xml) of the target JOB as an execution argument.

To specify the parameters during job execution, specify the launch option for  :java:extdoc:`nablarch.fw.batch.ee.Main` . 
The value specified in the launch option is configured in jobParameters of  :java:extdoc:`JobOperator#start <jakarta.batch.operations.JobOperator.start(java.lang.String,java.util.Properties)>` .

For the launch option, add ``--`` to the name and configure a value for the argument following the name.

Examples of using launch option
  .. code-block:: bash

    # In this example, two jobParameters "option1 = value1" and "option2 = value2" have been configured.
    $ java nablarch.fw.batch.ee.Main jobName --option1 value1 --option2 value2
  
.. tip::

  Even when creating a launch class in the project, it can be implemented by referring to the main class.


.. _jsr352_exitcode_batch_application:

Exit code for batch application
--------------------------------------------------
The exit code for the main class program mentioned above is as follows.

* Normal completion: 0 - When the exit status is other than "WARNING" and the batch status is :java:extdoc:`BatchStatus.COMPLETED <jakarta.batch.runtime.BatchStatus>` 
* Abnormal completion: 1 - When the exit status is other than "WARNING" and the batch status is not :java:extdoc:`BatchStatus.COMPLETED <jakarta.batch.runtime.BatchStatus>`
* Warning completion: 2 - When the completion status is "WARNING"

If the JOB is interrupted while waiting for completion, it will return an abnormal completion code.

If errors such as a validation error have occurred, for which a warning has to be issued, then warning completion can be used.
The method for warning completion is to call  :java:extdoc:`JobContext#setExitStatus(String) <jakarta.batch.runtime.context.JobContext.setExitStatus(java.lang.String)>` in chunk or batchlet, and configure the completion status as "WARNING". 
Since the batch status permits an arbitrary value at the time of warning completion, even if an exception is thrown in chunk or batchlet and batch status is other than  :java:extdoc:`BatchStatus.COMPLETED <jakarta.batch.runtime.BatchStatus>` , the above mentioned class ends with a warning if the completion status is configured as "WARNING".

.. _jsr352_run_batch_init_repository:

Initializing the system repository
--------------------------------------------------
:ref:`repository` can be initialized by configuring  ``nablarchJobListenerExecutor`` .

Configure the file name of the root xml file of the system repository to ``batch-boot.xml`` and place it directly under the class path. 
The file name or location can be changed with the parameters of ``nablarchJobListenerExecutor`` .

An example is shown below.

Example of the default ``batch-boot.xml`` configuration file
  .. code-block:: xml

    <job id="sample-job" xmlns="https://jakarta.ee/xml/ns/jakartaee" version="2.0">
      <listeners>
        <!-- Configure nablarchJobListenerExecutor in job listener -->
        <listener ref="nablarchJobListenerExecutor" />
      </listeners>

      <!-- Step definition is omitted -->
    </job>

Example of a configuration file other than default
  .. code-block:: xml

    <job id="sample-job" xmlns="https://jakarta.ee/xml/ns/jakartaee" version="2.0">
      <listeners>
        <listener ref="nablarchJobListenerExecutor">
          <properties>
            <!--
            Configures xml to read in diConfigFilePath properties
            In this example, "sample_project/batch-boot.xml" under the class path
            is loaded into the system repository
            -->
            <property name="diConfigFilePath" value="sample_project/batch-boot.xml" />
          </properties>
        </listener>
      </listeners>

      <!-- Step definition is omitted -->
    </job>
