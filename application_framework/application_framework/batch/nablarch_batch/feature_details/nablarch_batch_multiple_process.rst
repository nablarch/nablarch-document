.. _nablarch_batch_multiple_process:

常駐バッチアプリケーションのマルチプロセス化
======================================================================
:ref:`常駐バッチ<nablarch_batch-resident_batch>` を複数プロセス化 [#multi_process]_ したい場合、アプリケーション側で複数起動できるように対応を行う必要がある。
もし、何も対応を行わずに同一の常駐バッチアプリケーションを複数起動した場合、同一のデータを処理し2重取り込みの障害などが発生するため注意すること。

以下にマルチプロセスで常駐バッチを起動する為の実装例を示す。

1.処理対象を保持するテーブルに悲観ロック用のカラムを追加する。
  常駐バッチで処理対象データを抽出する際は、通常ステータスカラムなどを用いてい未処理データのみを抽出する。
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
  悲観ロックしたレコード抽出するため、条件は未処理かつ ``PROCESS_ID`` が自身のプロセスIDであることとする。

  .. code-block:: sql
  
    SELECT
      *
    FROM
      SAMPLE_TABLE
    WHERE
      STATUS = '0'
      AND PROCESS_ID = :processId
      
4.悲観ロック処理と悲観ロックしたレコードを抽出するようActionを実装する。
  DatabaseRecordReaderを使用した場合の実装例を示す。
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
        reader.setListener(() -> {
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
        });
        return reader;
    }

.. [#multi_process]
  冗長化構成の複数のサーバ上で同一の常駐バッチアプリケーションを起動するケースなどが該当する。
  



