.. _nablarch_batch_multiple_process:

常駐バッチアプリケーションのマルチプロセス化
======================================================================
基本的には :ref:`データベースをキューとしたメッセージングのマルチプロセス化<db_messaging-multiple_process>`
と同様となるため、そちらを参照すること。

ただし、Actionの実装についてはデータベースをキューとしたメッセージングとは異なるため、
以下にDatabaseRecordReaderを使用した場合のActionの実装例を示す。

なお、Readerを自作している場合には、下の例を参考に悲観ロック後に処理対象データを抽出するようにするとよい。
  
  .. code-block:: java
  
    /**
     * プロセスID。
     *
     * この例では、UUIDを元にプロセスIDを生成している。
     */
    private final String processId = UUID.randomUUID()
                                         .toString();

    @Override
    public DatabaseRecordReader createReader(ExecutionContext context) {
        final Map<String, String> param = new HashMap<>();
        param.put("processId", processId);
        
        // 自身が悲観ロックした未処理データを抽出するDatabaseRecordReaderを作成する
        final DatabaseRecordReader reader = new DatabaseRecordReader();
        final ParameterizedSqlPStatement statement =
            DbConnectionContext.getConnection()
                               .prepareParameterizedSqlStatementBySqlId(
                                   FileCreateRequest.class.getName() + "#GET_MISHORI_FILE_INFO");
        reader.setStatement(statement, param);
        
        // DatabaseRecordReaderがデータ抽出前に行うコールバック処理に、
        // 悲観ロックSQLを実行する処理を登録する。
        // なお、この処理は別トランザクションで実行する必要がある。
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
  



