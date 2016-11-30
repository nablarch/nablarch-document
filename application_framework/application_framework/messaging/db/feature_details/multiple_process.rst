.. _db_messaging-multiple_process:

マルチプロセス化
==========================================================

:ref:`データベースをキューとしたメッセージング<db_messaging>` を複数プロセス化 [#multi_process]_ したい場合、アプリケーション側で複数起動できるように対応を行う必要がある。
もし、何も対応を行わずに同一のデータベースをキューとしたメッセージングを複数起動した場合、同一のデータを処理し2重取り込みの障害などが発生するため注意すること。

マルチプロセスでデータベースをキューとしたメッセージングを起動するための手順は、
基本的には :ref:`nablarch_batch_multiple_process` と同様となるため、そちらを参照すること。

本項では、マルチプロセス化するための悲観ロック処理と悲観ロックしたレコードを抽出するActionの実装例を示す。

  .. code-block:: java

    /**
     * プロセスID。
     *
     * この例では、UUIDを元にプロセスIDを生成している。
     */
    private static final String PROCESS_ID = UUID.randomUUID().toString();

    @Override
    public DataReader<SqlRow> createReader(ExecutionContext context) {
        final Map<String, String> param = new HashMap<>();
        param.put("processId", PROCESS_ID);

        // 自身が悲観ロックした未処理データを抽出するDatabaseRecordReaderを作成する
        final DatabaseRecordReader reader = new DatabaseRecordReader();
        reader.setStatement(getParameterizedSqlStatement("FIND_RECEIVED_PROJECTS"), param);

        // DatabaseRecordReaderがデータ抽出前に行うコールバック処理に、
        // 悲観ロックSQLを実行する処理を登録する。
        // なお、この処理は別トランザクションで実行する必要がある。
        reader.setListener(() -> {
            new SimpleDbTransactionExecutor<Void>(SystemRepository.get("myTran")) {
                @Override
                public Void execute(final AppDbConnection appDbConnection) {
                    appDbConnection
                            .prepareParameterizedSqlStatementBySqlId(
                                    SQL_ID_PREFIX + "UPDATE_PROCESS_ID")
                            .executeUpdateByMap(param);
                    return null;
                }
            }.doTransaction();
        });

        return new DatabaseTableQueueReader(reader, 1000, "RECEIVED_MESSAGE_SEQUENCE");;
    }

.. [#multi_process]
  冗長化構成の複数のサーバ上で同一のデータベースをキューとしたメッセージングを起動するケースなどが該当する。