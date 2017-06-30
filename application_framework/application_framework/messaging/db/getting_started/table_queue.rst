テーブルキューを監視し未処理データを取り込むアプリケーションの作成
======================================================================================
Exampleアプリケーションを元にテーブルキューを監視し、未処理データを取り込むアプリケーションの解説を行う。

作成する機能の概要
  テーブルキューを定期的に監視し、未処理データ(ステータス:``0``)のデータを取り込む。
  テーブルキュー及び取り込み先テーブルの情報は以下の通り。

  :監視対象のテーブルキュー: プロジェクト登録メッセージ受信(INS_PROJECT_RECEIVE_MESSAGE)
  :取り込み先テーブル: プロジェクト(PROJECT)

Exampleアプリケーションの実行手順
  手順内で行っているSQLの実行については、任意のデータベースクライアントでH2に接続し、行うこと。
  接続先情報は、 ``config/database.config`` を参照。

  1. プロジェクトテーブルのデータを削除する。

  .. code-block:: sql

    truncate table project

  2. アプリケーションを実行する。

  .. code-block:: bash

    $cd nablarch-example-db-queue
    $mvn install
    $mvn dependency:copy-dependencies -DoutputDirectory=target/dependency
    $java -classpath target/classes;target/dependency/*\
         nablarch.fw.launcher.Main\
         -diConfig com/nablarch/example/app/batch/project-creation-service.xml\
         -requestPath ProjectCreationService -userId sample


  3. テーブルキューに未処理のデータを追加する。

  以下のSQLを実行し、監視対象のテーブルキューに未処理データを追加する。

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
      'プロジェクト名',
      'development',
      '分類',
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

  4. プロジェクトテーブルにデータが登録されていることを確認する。

  以下のSQLを実行し、未処理のデータがプロジェクトテーブルに取り込まれたことを確認する。
  
  .. code-block:: sql

    select * from project

  5. アプリケーションを停止する。

  アプリケーションを実行したコマンドプロンプトなどでプロセスを強制終了(Ctrl + Cなどで)する。

.. _db_queue_example-create_action:

アクションクラスを作成する
--------------------------------------------------
:java:extdoc:`BatchAction <nablarch.fw.action.BatchAction>` を継承したアクションクラスを作成する。

実装例
  .. code-block:: java

    public class ProjectCreationServiceAction extends BatchAction<SqlRow> {
      // 中身の作成方法は後述
    }

ポイント
  * テーブルをキューとして扱うため、入力データはテーブルの検索結果となる。
    このため、 :java:extdoc:`BatchAction <nablarch.fw.action.BatchAction>` の型パラメータには :java:extdoc:`SqlRow <nablarch.core.db.statement.SqlRow>` を指定する。


テーブルを監視するためのリーダを生成する
--------------------------------------------------
:ref:`db_queue_example-create_action` で作成したアクションクラスに、テーブルを監視するリーダを生成するメソッドを作成する。

:ref:`データベースキューで使用するリーダ <db_messaging_architecture-reader>` に記載がある通り、
:java:extdoc:`DatabaseTableQueueReader <nablarch.fw.reader.DatabaseTableQueueReader>` をリーダとして生成する。

実装例
  アクションクラス
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

  SQLファイル(ProjectCreationServiceAction.sql)
    .. code-block:: sql

      -- 未処理の受信データを悲観ロックするSQL
      UPDATE_PROCESS_ID=
      update
        ins_project_receive_message
      set
        process_id = :processId
      where
        status = '0' and process_id is null

      -- 未処理の受信データを取得するSQL
      FIND_RECEIVED_PROJECTS=
      select
        received_message_sequence
      from
        ins_project_receive_message
      where
        status = '0' and process_id = :processId

ポイント
  * :java:extdoc:`createReader <nablarch.fw.action.BatchAction.createReader(nablarch.fw.ExecutionContext)>` を実装し、
    :java:extdoc:`DatabaseTableQueueReader <nablarch.fw.reader.DatabaseTableQueueReader>` を生成する。

  * :java:extdoc:`DatabaseTableQueueReader <nablarch.fw.reader.DatabaseTableQueueReader>` には以下を指定する。

    * データベースから検索を行うためのリーダ(:java:extdoc:`DatabaseRecordReader <nablarch.fw.reader.DatabaseRecordReader>`)
    * 未処理データが存在しない場合の待機時間(この例では1秒)
    * 主キーのカラム名のリスト

  * :java:extdoc:`DatabaseRecordReader <nablarch.fw.reader.DatabaseRecordReader>` には以下を指定する。

    * 未処理データを検索するための :java:extdoc:`SqlPStatement <nablarch.core.db.statement.SqlPStatement>`
    * 未処理データの悲観ロックを行う
      :java:extdoc:`DatabaseRecordListener <nablarch.fw.reader.DatabaseRecordListener>` の実装クラス。
      詳細は、:ref:`db_messaging-multiple_process` を参照。

  * SQLファイルでは、以下のSQLを定義する。

    * 他のプロセスの処理対象となることを防ぐため、未処理データを悲観ロックするSQL
    * 自身のプロセスの処理対象となる未処理データを取得するため、
      ``STATUS`` カラムの値が ``0`` 、かつ ``PROCESS_ID`` カラムの値が自身のプロセスIDであるレコードを取得するSQL

  * SQLファイルへのSQLの記述ルールは、 :ref:`database-use_sql_file` を参照。

未処理データを元に業務処理を実行する
--------------------------------------------------
:ref:`db_queue_example-create_action` で作成したアクションクラスに、業務処理を実装するメソッドを作成する。

実装例
  .. code-block:: java

    @Override
    public Result handle(final SqlRow inputData, final ExecutionContext context) {

      // 未処理データの主キーを元に属性データを取得する
      final Project project = UniversalDao.findBySqlFile(
          Project.class,
          SQL_ID + "GET_RECEIVED_PROJECT",
          inputData);

      if (!isValidProjectPeriod(project)) {
        throw new ApplicationException(
            MessageUtil.createMessage(MessageLevel.ERROR, "abnormal.project.period"));
      }

      // プロジェクトテーブルへ登録する
      UniversalDao.insert(project);

      return new Result.Success();
    }

ポイント
  * :java:extdoc:`handle <nablarch.fw.action.BatchAction.handle(D, nablarch.fw.ExecutionContext)>` メソッドに業務処理を実装する。
    (処理内容の詳細な説明は、Example依存のため省略する。)

  * 正常に処理したことを示す :java:extdoc:`Result.Success <nablarch.fw.Result.Success>` を返却する。
    処理が失敗した場合、例外を送出するため、常に :java:extdoc:`Result.Success <nablarch.fw.Result.Success>` を返却すれば良い。

処理済みデータのステータスを更新する
--------------------------------------------------
:ref:`db_queue_example-create_action` で作成したアクションクラスに、ステータスを更新するメソッドを作成する。

実装例
  アクションクラス
    .. code-block:: java

      @Override
      protected void transactionSuccess(final SqlRow inputData, final ExecutionContext context) {
        // ステータスを正常に更新する
        updateStatus(inputData, StatusUpdateDto::createNormalEnd);
      }

      @Override
      protected void transactionFailure(final SqlRow inputData, final ExecutionContext context) {
        // ステータスを異常(失敗)に更新する
        updateStatus(inputData, StatusUpdateDto::createAbnormalEnd);
      }

      private void updateStatus(
          final SqlRow inputData, final Function<String, StatusUpdateDto> function) {
        getParameterizedSqlStatement("UPDATE_STATUS")
            .executeUpdateByObject(
                function.apply(inputData.getString("RECEIVED_MESSAGE_SEQUENCE")));
      }

      public static final class StatusUpdateDto {
        // プロパティ及びアクセッサ、Javadocは省略

        private static StatusUpdateDto createNormalEnd(String id) {
            return new StatusUpdateDto(id, "1");
        }

        private static StatusUpdateDto createAbnormalEnd(String id) {
            return new StatusUpdateDto(id, "2");
        }
      }

  SQLファイル(ProjectCreationServiceAction.sql)
    .. code-block:: sql

      -- ステータスを更新するSQL
      UPDATE_STATUS =
      update
        ins_project_receive_message
      set
        status = :newStatus
      where
        received_message_sequence = :id

ポイント
  * 正常に処理できたレコードの更新処理は、 :java:extdoc:`transactionSuccess <nablarch.fw.action.BatchActionBase.transactionSuccess(D, nablarch.fw.ExecutionContext)>` に実装する。
    (正常に処理できた場合(例外が送出されなかった場合)、このメソッドがNablarchによりコールバックされる。)

  * 正常に処理できなかったレコードの更新処理は、 :java:extdoc:`transactionFailure <nablarch.fw.action.BatchActionBase.transactionSuccess(D, nablarch.fw.ExecutionContext)>` に実装する。
    (処理中に例外やエラーが送出されたレコードの場合、このメソッドがNablarchによりコールバックされる)

  * SQLでは、指定のレコードのステータスを更新する。

  * SQLファイルへのSQLの記述ルールは、 :ref:`database-use_sql_file` を参照。
