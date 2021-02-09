Create an Application That Monitors Table Queues and Imports Unprocessed Data
======================================================================================
The application that monitors table queues and imports unprocessed data will be explained using an example application.

Overview of the function to be created
  Regularly monitor the table queues and import the data of the unprocessed data (status:``0``).
  Information of the table queues and table to be imported are as given below.

  :Monitored table queue: Receive the project registration message (INS_PROJECT_RECEIVE_MESSAGE)
  :Table to be imported: Project (PROJECT)

Execution procedure of the example application
  SQL should be executed within the procedure after connecting any arbitrary database client to H2.
  For information on the connection destination, see ``config/database.properties``.

  1. Delete data in the project table.

  .. code-block:: sql

    truncate table project

  2. Execute the application.

  .. code-block:: bash

    $cd nablarch-example-db-queue
    $mvn clean package
    $mvn exec:java -Dexec.mainClass=nablarch.fw.launcher.Main ^
        -Dexec.args="'-diConfig' 'com/nablarch/example/app/batch/project-creation-service.xml' '-requestPath' 'ProjectCreationService' '-userId' 'samp'"

  3. Add the unprocessed data to the table queue.

  Execute the following SQL and add the unprocessed data to the monitored table queue.

  .. code-block:: sql

    insert into ins_project_receive_message (
      received_message_sequence,
      project_name,
      project_type,
      project_class,
      project_start_date,
      project_end_date,
      client_id,
      project_manager,
      project_leader,
      user_id,
      note,
      sales,
      cost_of_goods_sold,
      sga,
      allocation_of_corp_expenses,
      status
    ) values (
      1,
      'Project name',
      'development',
      'Classification',
      '2011-01-01',
      '2020-12-31',
      1,
      'admin',
      'user1',
      1,
      ' ',
      100,
      200,
      300,
      400,
      '0'
    )

  4. Confirm that the data has been registered in the project table.

  Execute the following SQL and check whether unprocessed data is imported into the project table.
  
  .. code-block:: sql

    select * from project

  5. Stop the application.

  Force terminate the process with (Ctrl + C etc.) from the command prompt, etc. from where the application was executed.

.. _db_queue_example-create_action:

Create a action class
--------------------------------------------------
Creates an action class by inheriting :java:extdoc:`BatchAction <nablarch.fw.action.BatchAction>`.

Implementation examples
  .. code-block:: java

    public class ProjectCreationServiceAction extends BatchAction<SqlRow> {
      // How to create the contents will be described later
    }

Point
  * Since the table is handled as a queue, the input data becomes the search result of the table.
    For this reason, :java:extdoc:`SqlRow <nablarch.core.db.statement.SqlRow>` is specified in the type parameter of :java:extdoc:`BatchAction <nablarch.fw.action.BatchAction>`.


Create a reader to monitor the table
--------------------------------------------------
Create a method to generate a reader that monitors the table in the action class created with :ref:`db_queue_example-create_action`.

As described in :ref:`Reader used for database queue <db_messaging_architecture-reader>`, create
:java:extdoc:`DatabaseTableQueueReader <nablarch.fw.reader.DatabaseTableQueueReader>` as reader.

Implementation examples
  Action class
    .. code-block:: java

      @Override
      public DataReader<SqlRow> createReader(final ExecutionContext context) {
          final DatabaseRecordReader databaseRecordReader = new DatabaseRecordReader();

          databaseRecordReader.setStatement(
                  getParameterizedSqlStatement("FIND_RECEIVED_PROJECTS"), PROCESS_MAP);

          databaseRecordReader.setListener(() -> {
              final SimpleDbTransactionManager transactionManager =
                      SystemRepository.get("redundancyTransaction");
              new SimpleDbTransactionExecutor<Void>(transactionManager) {
                  @Override
                  public Void execute(final AppDbConnection appDbConnection) {
                      appDbConnection
                              .prepareParameterizedSqlStatementBySqlId(
                                      SQL_ID_PREFIX + "UPDATE_PROCESS_ID")
                              .executeUpdateByMap(PROCESS_MAP);
                      return null;
                  }
              }.doTransaction();
          });

          return new DatabaseTableQueueReader(
                  databaseRecordReader, 1000, "RECEIVED_MESSAGE_SEQUENCE");
      }

  SQL file (ProjectCreationServiceAction.sql)
    .. code-block:: sql

      -- SQL for pessimistically locking the unprocessed data that is received
      UPDATE_PROCESS_ID=
      update
        ins_project_receive_message
      set
        process_id = :processId
      where
        status = '0' and process_id is null

      -- SQL to acquire the unprocessed data that is received
      FIND_RECEIVED_PROJECTS=
      select
        received_message_sequence
      from
        ins_project_receive_message
      where
        status = '0' and process_id = :processId

Point
  * Implement :java:extdoc:`createReader <nablarch.fw.action.BatchAction.createReader(nablarch.fw.ExecutionContext)>`
    and create :java:extdoc:`DatabaseTableQueueReader <nablarch.fw.reader.DatabaseTableQueueReader>`.

  * Specify the following in :java:extdoc:`DatabaseTableQueueReader <nablarch.fw.reader.DatabaseTableQueueReader>`.

    * Reader for searching from the database (:java:extdoc:`DatabaseRecordReader <nablarch.fw.reader.DatabaseRecordReader>`)
    * Wait time when there is no unprocessed data (1 second in this example)
    * List of primary key column names

  * Specify the following in :java:extdoc:`DatabaseRecordReader <nablarch.fw.reader.DatabaseRecordReader>`.

    * :java:extdoc:`SqlPStatement <nablarch.core.db.statement.SqlPStatement>` to search the unprocessed data
    * Implementation class :java:extdoc:`DatabaseRecordListener <nablarch.fw.reader.DatabaseRecordListener>`
      for pessimistic lock of unprocessed data.
      For details, see :ref:`db_messaging-multiple_process`.

  * Define the following SQL in the SQL file.

    * SQL for the pessimistic locking of unprocessed data to avoid the data from being used as processing object of other processes
    * SQL that acquires records with the ``STATUS`` column value ``0`` and ``PROCESS_ID`` column value
      same as the process ID for acquiring unprocessed data to be processed by the process

  * For SQL description rules to prepare the SQL file, see :ref:`database-use_sql_file`.

Execute business process based on unprocessed data
----------------------------------------------------
Create a method to implement the business process in the action class created with :ref:`db_queue_example-create_action`.

Implementation examples
  .. code-block:: java

    @Override
    public Result handle(final SqlRow inputData, final ExecutionContext context) {

      // Retrieve attribute data based on the primary key of unprocessed data
      final Project project = UniversalDao.findBySqlFile(
          Project.class,
          SQL_ID + "GET_RECEIVED_PROJECT",
          inputData);

      if (!isValidProjectPeriod(project)) {
        throw new ApplicationException(
            MessageUtil.createMessage(MessageLevel.ERROR, "abnormal.project.period"));
      }

      // Register to project table
      UniversalDao.insert(project);

      return new Result.Success();
    }

Point
  * Implement the business process in the method :java:extdoc:`handle <nablarch.fw.action.BatchAction.handle(D-nablarch.fw.ExecutionContext)>`.
    (Detailed explanation of the process details is omitted as depends on the example dependent.)

  * Returns :java:extdoc:`Result.Success <nablarch.fw.Result.Success>`, which indicates that the processing was normal.
    Since an exception is thrown even if the processing fails, :java:extdoc:`Result.Success <nablarch.fw.Result.Success>` can be always returned.

Update the status of processed data
--------------------------------------------------
Create a method to update the status in the action class created with :ref:`db_queue_example-create_action`.

Implementation examples
  Action class
    .. code-block:: java

      @Override
      protected void transactionSuccess(final SqlRow inputData, final ExecutionContext context) {
        // Update status to success
        updateStatus(inputData, StatusUpdateDto::createNormalEnd);
      }

      @Override
      protected void transactionFailure(final SqlRow inputData, final ExecutionContext context) {
        // Update status to abnormal (failed)
        updateStatus(inputData, StatusUpdateDto::createAbnormalEnd);
      }

      private void updateStatus(
          final SqlRow inputData, final Function<String, StatusUpdateDto> function) {
        getParameterizedSqlStatement("UPDATE_STATUS")
            .executeUpdateByObject(
                function.apply(inputData.getString("RECEIVED_MESSAGE_SEQUENCE")));
      }

      public static final class StatusUpdateDto {
        // Property and accessors, Javadoc omitted

        private static StatusUpdateDto createNormalEnd(String id) {
            return new StatusUpdateDto(id, "1");
        }

        private static StatusUpdateDto createAbnormalEnd(String id) {
            return new StatusUpdateDto(id, "2");
        }
      }

  SQL file (ProjectCreationServiceAction.sql)
    .. code-block:: sql

      -- SQL to update status
      UPDATE_STATUS =
      update
        ins_project_receive_message
      set
        status = :newStatus
      where
        received_message_sequence = :id

Point
  * Implement the update process of the normally processed record in :java:extdoc:`transactionSuccess <nablarch.fw.action.BatchActionBase.transactionSuccess(D-nablarch.fw.ExecutionContext)>`.
    (if the processing is normal (exception is not thrown), the method is called back by Nablarch.)

  * The update process of records that were not processed normally is implemented in :java:extdoc:`transactionFailure <nablarch.fw.action.BatchActionBase.transactionSuccess(D-nablarch.fw.ExecutionContext)>`.
    (The method where an exception or error is thrown during processing is called back by Nablarch.)

  * The status of the specific record is updated in SQL.

  * For SQL description rules to prepare the SQL file, see :ref:`database-use_sql_file`.
