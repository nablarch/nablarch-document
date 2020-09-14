.. _db_messaging-multiple_process:

Multi-process
==========================================================

Support should be provided in the application for multiple launches to perform multi-process [#multi_process]_ messaging using databases as queues.
If multi-process of messaging is performed using the same database as queue without providing proper support, note that the same data will be processed and may cause a double capture failure.

Below is an implementation example of the messaging process using database as a queue with multi- process.

1.Add a column with pessimistic lock to the table that contains the processing targets.
  When extracting data to process messaging using a database as a queue, only unprocessed data is extracted using a normal status column, etc.
  When using multi-process, add a column for the pessimistic locking of target records processed
  by each process since only this information causes multiple processes to acquire the same data.

  Example (only required columns are described)
    ============ ===============================================================
    Column name  Description
    ============ ===============================================================
    ID           Primary key
    STATUS       Status column to identify if data is unprocessed
    PROCESS_ID   Column used for pessimistic locking of records by each process
    ============ ===============================================================

2.Create SQL for the pessimistic locking of process target records
  Create SQL for pessimistic locking of other unprocessed data that is not locked by other processes.

  When the above table definition is as given above, records for which value is not set in
  ``PROCESS_ID`` (if null) and ``STATUS`` is unprocessed will not be locked.

  .. code-block:: sql

    UPDATE SAMPLE_TABLE
    SET PROCESS_ID = :processId
    WHERE STATUS = '0'
     AND PROCESS_ID IS NULL

3.Create SQL to extract unprocessed records with pessimistic lock.
  For extracting pessimistic locked records, the conditions are unprocessed and having a ``PROCESS_ID``.

  .. code-block:: sql

    SELECT
      *
    FROM
      SAMPLE_TABLE
    WHERE
      STATUS = '0'
      AND PROCESS_ID = :processId

4. Implement action for pessimistic record process and to extract records with pessimistic lock.

  .. code-block:: java

    /**
     * Process ID.
     *
     * In this example, the process ID is generated based on the UUID.
     */
    private static final String PROCESS_ID = UUID.randomUUID().toString();

    @Override
    public DataReader<SqlRow> createReader(ExecutionContext context) {
        final Map<String, String> param = new HashMap<>();
        param.put("processId", PROCESS_ID);

        // Create a DatabaseRecordReader to extract unprocessed data that was pessimistically locked
        final DatabaseRecordReader reader = new DatabaseRecordReader();
        reader.setStatement(getParameterizedSqlStatement("FIND_RECEIVED_PROJECTS"), param);

        // Register the process that executes the pessimistic lock SQL in the call back process
        // performed by the DatabaseRecordReader, before data extraction.
        // This process needs to be executed in another transaction.
        databaseRecordReader.setListener(new DatabaseRecordListener() {
            @Override
            public void beforeReadRecords() {
                final SimpleDbTransactionManager transactionManager = SystemRepository.get("redundancyTransaction");
                new SimpleDbTransactionExecutor<Void>(transactionManager) {
                    @Override
                    public Void execute(final AppDbConnection appDbConnection) {
                        appDbConnection
                                .prepareParameterizedSqlStatementBySqlId(SQL_ID_PREFIX + "UPDATE_PROCESS_ID")
                                .executeUpdateByMap(PROCESS_MAP);
                        return null;
                    }
                }.doTransaction();

            }
        });

        return new DatabaseTableQueueReader(reader, 1000, "RECEIVED_MESSAGE_SEQUENCE");;
    }

.. [#multi_process]
  This applies to the case of starting messaging with the same database queued on multiple servers in a redundant configuration.