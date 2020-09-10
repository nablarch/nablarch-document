.. _nablarch_batch_multiple_process:

Multi-processing of Resident Batch Applications
======================================================================
Refer to :ref:`multiple process of messaging that uses the database as a queue <db_messaging-multiple_process>`,
as it is basically the same as multi-processing of resident batch applications.

Since the implementation of action is different from messaging that uses the database as a queue,
the following is an implementation example of action when DatabaseRecordReader is used.

If the application implements its own reader, it is preferable to extract the processed data
after the pessimistic lock referring to the example below.

  .. code-block:: java

    /**
     * Process ID.
     *
     * In this example, the process ID is generated based on the UUID.
     */
    private final String processId = UUID.randomUUID()
                                         .toString();

    @Override
    public DatabaseRecordReader createReader(ExecutionContext context) {
        final Map<String, String> param = new HashMap<>();
        param.put("processId", processId);

        // Create the DatabaseRecordReader to extract unprocessed data that have pessimistically locked by self.
        final DatabaseRecordReader reader = new DatabaseRecordReader();
        final ParameterizedSqlPStatement statement =
            DbConnectionContext.getConnection()
                               .prepareParameterizedSqlStatementBySqlId(
                                   FileCreateRequest.class.getName() + "#GET_MISHORI_FILE_INFO");
        reader.setStatement(statement, param);

        // Register the process that executes the pessimistic lock SQL in the call back process
        // performed by the DatabaseRecordReader, before data extraction.
        // This process needs to be executed in another transaction.
        databaseRecordReader.setListener(new DatabaseRecordListener() {
          @Override
          public void beforeReadRecords() {
            new SimpleDbTransactionExecutor<Void>(SystemRepository.get("myTran")) {
              @Override
              public Void execute(final AppDbConnection connection) {
                final ParameterizedSqlPStatement statement = connection.
                    prepareParameterizedSqlStatementBySqlId(
                        FileCreateRequest.class.getName() + "#MARK_UNPROCESSED_DATA");
                statement.executeUpdateByMap(param);
                return null;
              }
            }.doTransaction();
          }
        });
        
        return reader;
    }
  



