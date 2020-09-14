.. _db_messaging-multiple_process:

マルチプロセス化
==========================================================

データベースをキューとしたメッセージングを複数プロセス化 [#multi_process]_ したい場合、アプリケーション側で複数起動できるように対応を行う必要がある。
もし、何も対応を行わずに同一のデータベースをキューとしたメッセージングを複数起動した場合、同一のデータを処理し2重取り込みの障害などが発生するため注意すること。

以下にマルチプロセスでデータベースをキューとしたメッセージングを起動する為の実装例を示す。

1.処理対象を保持するテーブルに悲観ロック用のカラムを追加する。
  データベースをキューとしたメッセージングで処理対象データを抽出する際は、通常ステータスカラムなどを用いて未処理データのみを抽出する。
  マルチプロセス化する際には、この情報だけでは複数のプロセスが同一データを取得してしまうため、
  各プロセスが処理する対象レコードを悲観ロックする為のカラムを追加する。

  例(必要なカラムのみ記載)
    ========== ===============================================================
    カラム名   説明
    ========== ===============================================================
    ID         主キー
    STATUS     未処理データかどうかを判断するためのステータスカラム
    PROCESS_ID 各プロセスがレコードを悲観ロックするために使用するカラム
    ========== ===============================================================

2.処理対象レコードを悲観ロックするSQLを作成する。
  他のプロセスからロックされていない未処理データを悲観ロックするSQLを作成する。

  上記のテーブル定義とした場合、 ``PROCESS_ID`` に値が設定されていない(nullの場合)レコードで、
  ``STATUS`` が未処理のレコードがロックされていないレコードとなる。

  .. code-block:: sql

    UPDATE SAMPLE_TABLE
    SET PROCESS_ID = :processId
    WHERE STATUS = '0'
     AND PROCESS_ID IS NULL

3.悲観ロックした未処理レコードを抽出するSQLを作成する。
  悲観ロックしたレコードを抽出するため、条件は未処理かつ ``PROCESS_ID`` が自身のプロセスIDであることとする。

  .. code-block:: sql

    SELECT
      *
    FROM
      SAMPLE_TABLE
    WHERE
      STATUS = '0'
      AND PROCESS_ID = :processId

4.悲観ロック処理と悲観ロックしたレコードを抽出するようActionを実装する。

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
  冗長化構成の複数のサーバ上で同一のデータベースをキューとしたメッセージングを起動するケースなどが該当する。