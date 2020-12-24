.. _`getting_started_batchlet`:

Creating a Batch to Delete the data in the target table(Batchlet Step)
==========================================================================
This section explains a batch that Delete the data in the target table in the :ref:`batchlet step<jsr352-batch_type_Batchlet>` based on the example application.

Description of the function to be created
  1. Check the current DB status

     Execute the following SQL from the console of H2.

     .. code-block:: sql

       SELECT * FROM ZIP_CODE_DATA;
       SELECT * FROM ZIP_CODE_DATA_WORK;

     If data is not registered, perform step 2.

  2. (If data is not registered) Execute the mailing address registration batch

    Execute the following command from the command prompt

    .. code-block:: bash

      $cd {nablarch-example-batch-ee System repository}
      $mvn exec:java -Dexec.mainClass=nablarch.fw.batch.ee.Main ^
          -Dexec.args=etl-zip-code-csv-to-db-chunk

    Execute the following SQL from the console of H2 and confirm that the data is registered.

    .. code-block:: sql

      SELECT * FROM ZIP_CODE_DATA;
      SELECT * FROM ZIP_CODE_DATA_WORK;

  3. Execute the mailing address table delete batch

    Execute the following command from the command prompt

    .. code-block:: bash

      $cd {nablarch-example-batch-ee System repository}
      $mvn exec:java -Dexec.mainClass=nablarch.fw.batch.ee.Main ^
          -Dexec.args=zip-code-truncate-table

  4. Confirm that the data in the target table has been deleted

     Execute the following SQL from the console of H2 and confirm that the data has been deleted.

     .. code-block:: sql

       SELECT * FROM ZIP_CODE_DATA;
       SELECT * FROM ZIP_CODE_DATA_WORK;

Delete the data in the target table
---------------------------------------
This section explains how to implement a batch to delete the mailing address information.

For the process flow, refer to the process flow of the :ref:`batch of the batchlet step<jsr352-batch_flow_batchlet>`.
For the responsibility assignment, refer to the :ref:`responsibility assignment of the batchlet step<jsr352-batchlet_design>`.

  #. :ref:`Create batchlet<getting_started_batchlet_create>`
  #. :ref:`Creating a JOB configuration file<getting_started_batchlet_job>`

.. _`getting_started_batchlet_create`:

Create batchlet
  Create batchlet class of batch to delete the mailing address information.

  Interfaces to be implemented and their responsibilities
    Implement the following interface in the batchlet class to create the batch process. The overridden method is called at an appropriate timing by Batch Runtime.

   ==================================================================   =============================================================================================
   Interface                                                            Implementation
   ==================================================================   =============================================================================================
   :java:extdoc:`Batchlet<javax.batch.api.Batchlet>`                    Implement batch processing.

                                                                        Inherits :java:extdoc:`AbstractBatchlet<javax.batch.api.AbstractBatchlet>`, which provides the default implementation.

                                                                          * `Batchlet#process`
                                                                          * `Batchlet#stop`
   ==================================================================   =============================================================================================

  .. tip::

    Batch process is configured by a listener that provides common processes such as transaction control in addition to the implementation of the above interface.
    For details of the listener, see :ref:`listener used in the batch application<jsr352-listener>` and :ref:`how to specify the listener<jsr352-listener_definition>`.

  TruncateTableBatchlet.java
    .. code-block:: java

      @Dependent
      @Named
      public class TruncateTableBatchlet extends AbstractBatchlet {

          @Inject
          @BatchProperty
          private String tableName;

          @Override
          public String process() {

              final AppDbConnection conn = DbConnectionContext.getConnection();
              final SqlPStatement statement
                  = conn.prepareStatement("TRUNCATE TABLE " + tableName);
              statement.executeUpdate();

              return "SUCCESS";
          }
      }

    Key points of this implementation
      * Inherits :java:extdoc:`AbstractBatchlet<javax.batch.api.AbstractBatchlet>`, and performs the business process by `process` method.

      .. _getting_started_batchlet-cdi:

      * :java:extdoc:`Named<javax.inject.Named>` and :java:extdoc:`Dependent<javax.enterprise.context.Dependent>` are assigned to the class. |br|
        By configuring named and dependent annotations, batchlet implementation class can be used as CDI management bean.
        As a result, the batchlet class name specified in the job definition can be described with the CDI management name. |br|
        (If CDI management bean is not used, describe with fully qualified name (FQCN))

      * Execute TRUNCATE statement using :ref:`database access<database>`.

.. _`getting_started_batchlet_job`:

Create a job definition file
  Create a file that defines the job execution settings.

  zip-code-truncate-table.xml
    .. code-block:: xml

     <job id="zip-code-truncate-table" xmlns="http://xmlns.jcp.org/xml/ns/javaee" version="1.0">
       <listeners>
         <listener ref="nablarchJobListenerExecutor" />
       </listeners>

       <step id="step1" next="step2">
         <listeners>
           <listener ref="nablarchStepListenerExecutor" />
         </listeners>
         <batchlet ref="truncateTableBatchlet">
           <properties>
             <property name="tableName" value="ZIP_CODE_DATA" />
           </properties>
         </batchlet>
       </step>
       <step id="step2">
         <listeners>
           <listener ref="nablarchStepListenerExecutor" />
         </listeners>
         <batchlet ref="truncateTableBatchlet">
           <properties>
             <property name="tableName" value="ZIP_CODE_DATA_WORK" />
           </properties>
         </batchlet>
       </step>
     </job>

  Key points of this implementation
    * Job definition file is located under `/src/main/resources/META-INF/batch-jobs/`.
    * Specify the job name in the `id` attribute of the `job` element.
    * For a batch job consisting of multiple steps, define multiple `step` elements and execute the process sequentially.
    * Specify a name with the first letter of the batchlet class name in lowercase for the `ref` attribute of `batchlet` element.
    * Specify the value to be injected into the property of batchlet class in the `property` element.
    * Refer to `JSR352 Specification(external site) <https://jcp.org/en/jsr/detail?id=352>`_ for detailed description method of the configuration file.

.. |jsr352| raw:: html

  <a href="https://jcp.org/en/jsr/detail?id=352" target="_blank">JSR352(external site)</a>

.. |br| raw:: html

  <br />
