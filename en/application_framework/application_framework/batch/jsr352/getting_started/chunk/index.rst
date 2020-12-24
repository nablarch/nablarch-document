.. _`getting_started_chunk`:

Create Batch to Derive Data (Chunk Step)
===============================================================
This section explains the :ref:`Chunk step<jsr352-batch_type_chunk>` batch architecture, which calculates from existing data and derives new data based on the Example application.

Overview of the function to be created
  .. image:: ../images/chunk/overview.png

Communication confirmation procedure
  1. Delete data in the table (bonus table) to be registered

     Execute the following SQL from the console of H2 and delete the data in the bonus table.

     .. code-block:: sql

       TRUNCATE TABLE BONUS;

  2. Execute bonus calculation batch

     Execute the bonus calculation batch from the command prompt.

    .. code-block:: bash

      $cd {nablarch-example-batch-ee system repository}
      $mvn exec:java -Dexec.mainClass=nablarch.fw.batch.ee.Main ^
          -Dexec.args=bonus-calculate

  5. Check the status after batch execution

    Execute the following SQL from the console of H2 and confirm that the bonus information is registered.

    .. code-block:: sql

        SELECT * FROM BONUS;

Deriving data
-------------------
A method to implement a batch that calculates from existing data and derives new data will be described in the following order.

#. :ref:`getting_started_chunk-read`
#. :ref:`getting_started_chunk-business_logic`
#. :ref:`getting_started_chunk-persistence`
#. :ref:`getting_started_chunk-job`

For the process flow, see :ref:`process flow of Chunk step batch<jsr352-batch_flow_chunk>`.
For responsibility assignment, see :ref:`responsibility assignment of the Chunk step<jsr352-chunk_design>`.

Batch process is configured by a listener that provides common processes such as transaction control in addition to the implementation of the interface specified in `JSR352 (external site) <https://jcp.org/en/jsr/detail?id=352>`_.
For details of the listener, see :ref:`listener used in the batch application<jsr352-listener>`, and :ref:`how to specify the listener<jsr352-listener>`.

.. _`getting_started_chunk-read`:

Reads data from the input data source
++++++++++++++++++++++++++++++++++++++
Implements the process to fetch the data required for calculation.

#. :ref:`Create a form<getting_started_chunk-form>`
#. :ref:`Create an ItemReader<getting_started_chunk-reader>`

.. _`getting_started_chunk-form`:

Create a form
  In the Chunk step, use form to link data with :java:extdoc:`ItemReader<javax.batch.api.chunk.ItemReader>`
  and :java:extdoc:`ItemProcessor<javax.batch.api.chunk.ItemProcessor>`.

  EmployeeForm.java
    .. code-block:: java

      public class EmployeeForm {

          //Partial excerpt

          /** Employee ID */
          private Long employeeId;

          /**
           *Returns employee ID.
           *
           * @return Employee ID
           */
          public Long getEmployeeId() {
              return employeeId;
          }

          /**
           * Sets the employee ID.
           *
           * @param employeeId Employee ID
           */
          public void setEmployeeId(Long employeeId) {
              this.employeeId = employeeId;
          }
      }

.. _`getting_started_chunk-reader`:

Create an ItemReader
  Inherits :java:extdoc:`AbstractItemReader<javax.batch.api.chunk.AbstractItemReader>` and reads data.

    ==================================================================   =============================================================================================
    Interface Name                                                       Obligation
    ==================================================================   =============================================================================================
    :java:extdoc:`ItemReader<javax.batch.api.chunk.ItemReader>`          Reads data.

                                                                         Inherits :java:extdoc:`AbstractItemReader<javax.batch.api.chunk.AbstractItemReader>`, which provides a empty implementation.

                                                                           * `ItemReader#open`
                                                                           * `ItemReader#readItem`
                                                                           * `ItemReader#close`
    ==================================================================   =============================================================================================

  EmployeeSearchReader.java
    .. code-block:: java

      @Dependent
      @Named
      public class EmployeeSearchReader extends AbstractItemReader {

          /** List of employee information */
          private DeferredEntityList<EmployeeForm> list;

          /** Iterator holding employee information */
          private Iterator<EmployeeForm> iterator;

          @Override
          public void open(Serializable checkpoint) throws Exception {
              list = (DeferredEntityList<EmployeeForm>) UniversalDao.defer()
                      .findAllBySqlFile(EmployeeForm.class, "SELECT_EMPLOYEE");
              iterator = list.iterator();
          }

          @Override
          public Object readItem() {
              if (iterator.hasNext()) {
                  return iterator.next();
              }
              return null;
          }

          @Override
          public void close() throws Exception {
              list.close();
          }
      }

  EmployeeForm.sql
    .. code-block:: java

      SELECT_EMPLOYEE=
      SELECT
          EMPLOYEE.EMPLOYEE_ID,
          EMPLOYEE.FULL_NAME,
          EMPLOYEE.BASIC_SALARY,
          EMPLOYEE.GRADE_CODE,
          GRADE.BONUS_MAGNIFICATION,
          GRADE.FIXED_BONUS
      FROM
          EMPLOYEE
      INNER JOIN GRADE ON EMPLOYEE.GRADE_CODE = GRADE.GRADE_CODE

  Key points of this implementation
    * :java:extdoc:`Named<javax.inject.Named>` and :java:extdoc:`Dependent<javax.enterprise.context.Dependent>` are assigned to the class.
      For details, see :ref:`Explanation of named and dependent of batchlet<getting_started_batchlet-cdi>`.
    * Read the data to be processed with `open` method.
    * For the location and how to create the SQL file, see :ref:`universal_dao-sql_file`.
    * When reading a large amount of data, to prevent straining of the memory, use :java:extdoc:`UniversalDao#defer <nablarch.common.dao.UniversalDao.defer()>`
      to :ref:`defer the loading<universal_dao-lazy_load>` of the search results.
    * Returns one line of data from the data read by `readItem` method.
      The object returned by this method is given as an argument of `processItem` method of :java:extdoc:`ItemProcessor<javax.batch.api.chunk.ItemProcessor>` that follows.

.. _`getting_started_chunk-business_logic`:

Execute business logic
++++++++++++++++++++++
Implements the business logic of bonus calculation.

Create ItemProcessor
  Implements :java:extdoc:`ItemProcessor<javax.batch.api.chunk.ItemProcessor>`
  and carries out the business logic (since the persistence process is a duty of :java:extdoc:`ItemWriter<javax.batch.api.chunk.ItemWriter>`, it is not executed).

    ==================================================================   =============================================================================================
    Interface Name                                                       Obligation
    ==================================================================   =============================================================================================
    :java:extdoc:`ItemProcessor<javax.batch.api.chunk.ItemProcessor>`    Performs the business process on one line of data.

                                                                           * `ItemProcessor#processItem`
    ==================================================================   =============================================================================================

  BonusCalculateProcessor.java
    .. code-block:: java

      @Dependent
      @Named
      public class BonusCalculateProcessor implements ItemProcessor {

          @Override
          public Object processItem(Object item) {

              EmployeeForm form = (EmployeeForm) item;
              Bonus bonus = new Bonus();
              bonus.setEmployeeId(form.getEmployeeId());
              bonus.setPayments(calculateBonus(form));

              return bonus;
          }

          /**
           * Calculate bonus based on employee information.
           *
           * @param form Employee Information Form
           * @return Bonus
           */
          private static Long calculateBonus(EmployeeForm form) {
              if (form.getFixedBonus() == null) {
                  return form.getBasicSalary() * form.getBonusMagnification() / 100;
              } else {
                  return form.getFixedBonus();
              }
          }
      }

  Key points of this implementation
    * At the timing when a certain number of entities (how to configure is described in :ref:`getting_started_chunk-job`) are returned by the `processItem` method,
      the `writeItems` method of :java:extdoc:`ItemWriter<javax.batch.api.chunk.ItemWriter>` that follows is executed.

.. _`getting_started_chunk-persistence`:

Persistence process
++++++++++++++++++++
Implements the persistence process for DB update, etc.

Create ItemWriter
  Implements :java:extdoc:`ItemWriter<javax.batch.api.chunk.ItemWriter>` and makes data persistence.

    ==================================================================   =============================================================================================
    Interface Name                                                        Obligation
    ==================================================================   =============================================================================================
    :java:extdoc:`ItemWriter<javax.batch.api.chunk.ItemWriter>`          Persistence of data

                                                                           * `ItemWriter#writeItems`
    ==================================================================   =============================================================================================

  BonusWriter.java
    .. code-block:: java

      @Dependent
      @Named
      public class BonusWriter extends AbstractItemWriter {

          @Override
          public void writeItems(List<Object> items) {
              UniversalDao.batchInsert(items);
          }
      }

  Key points of this implementation
    * Uses :java:extdoc:`UniversalDao#batchInsert <nablarch.common.dao.UniversalDao.batchInsert(java.util.List)>` to batch register entity list.
    * The transaction is committed after execution of the `writeItems` method and a new transaction is started.
    * After execution of the `writeItems` method, the batch process is repeated from the execution of `readItem` method.

.. _`getting_started_chunk-job`:

Create a configuration file for JOB
+++++++++++++++++++++++++++++++++++
Create a file with the job execution configuration.

  bonus-calculate.xml
    .. code-block:: xml

     <job id="bonus-calculate" xmlns="http://xmlns.jcp.org/xml/ns/javaee" version="1.0">
       <listeners>
         <listener ref="nablarchJobListenerExecutor" />
       </listeners>

       <step id="step1">
         <listeners>
           <listener ref="nablarchStepListenerExecutor" />
           <listener ref="nablarchItemWriteListenerExecutor" />
         </listeners>

         <chunk item-count="1000">
           <reader ref="employeeSearchReader" />
           <processor ref="bonusCalculateProcessor" />
           <writer ref="bonusWriter" />
         </chunk>
       </step>
     </job>

  Key points of this implementation
    * The job definition file is located under `/src/main/resources/META-INF/batch-jobs/`.
    * Specify the `job` name in the `id` attribute of the job element.
    * Configure the number of `writeItems` processed each time by the `item-count` attribute of the `chunk` element.
    * Refer to `JSR352 specification (external site) <https://jcp.org/en/jsr/detail?id=352>`_ for detailed description method of the configuration file.

.. |jsr352| raw:: html

  <a href="https://jcp.org/en/jsr/detail?id=352" target="_blank">JSR352(external site)</a>
