.. _redundant_resident_batch:

バッチごとに処理対象のレコードを指定する
========================================

常駐バッチの冗長化を行う上で、バッチ処理ごとに処理対象のレコードを指定したい場合、
テーブルに処理識別IDを持たせるためのカラムを追加し、データ読み込み時に別トランザクションでIDの更新を行う。

以下にその実装例と設定例を示す。

* アクションクラスに処理識別IDの更新を行うための実装を追加

.. code-block:: java

    /** 処理識別IDのDTO */
    private final ProcessIdentificationIdDto processIdentificationIdDto =
            new ProcessIdentificationIdDto(UUID.randomUUID().toString());

    @Override
    public DataReader<SqlRow> createReader(final ExecutionContext context) {
        updateProcessIdentificationId();

        final DatabaseRecordReader databaseRecordReader = new DatabaseRecordReader();
        databaseRecordReader.setStatement(
                getParameterizedSqlStatement("FIND_RECEIVED_PROJECTS"), processIdentificationIdDto);
        return new DatabaseTableQueueReader(databaseRecordReader, 1000, "RECEIVED_MESSAGE_SEQUENCE");
    }
    
    /**
     * 処理識別IDを更新する。
     */
    private void updateProcessIdentificationId() {
        SimpleDbTransactionManager dbTransactionManager = SystemRepository.get("process-identification-transaction");
        new SimpleDbTransactionExecutor<Void>(dbTransactionManager) {
            @Override
            public Void execute(AppDbConnection connection) {
                final ParameterizedSqlPStatement statement
                        = connection.prepareParameterizedSqlStatementBySqlId(SQL_ID + "UPDATE_PROCESS_IDENTIFICATION_ID");
                statement.executeUpdateByObject(processIdentificationIdDto);
                return null;
            }
        }.doTransaction();
    }
    
    /**
     * 処理識別IDを保持するDTO
     */
    public static final class ProcessIdentificationIdDto {

        /** 処理識別ID */
        private final String processIdentificationId;

        public ProcessIdentificationIdDto(String processIdentificationId) {
            this.processIdentificationId = processIdentificationId;
        }

        public String getProcessIdentificationId() {
            return processIdentificationId;
        }
    }

* SQLファイルに処理識別IDの更新を行うSQLを追加

.. code-block:: sql

  UPDATE_PROCESS_IDENTIFICATION_ID =
  update
    ins_project_receive_message
  set
    process_identification_id = :processIdentificationId
  where
    status = '0'
  and process_identification_id is null
  
* コンポーネント設定ファイルに処理識別ID更新のためのトランザクション設定を追加

.. code-block:: xml

  <component name="process-identification-transaction" class="nablarch.core.db.transaction.SimpleDbTransactionManager">
    <property name="connectionFactory" ref="connectionFactory" />
    <property name="transactionFactory" ref="transactionFactory" />
    <property name="dbTransactionName" value="process-identification-transaction" />
  </component>
  
