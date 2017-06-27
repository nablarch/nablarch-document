データベースを入力とするChunkステップ
======================================================
.. contents:: 目次
  :depth: 3
  :local:
  
データベースから処理対象データを抽出する場合は、JSR352で提供されているリーダではなく
本機能で提供する :java:extdoc:`BaseDatabaseItemReader <nablarch.fw.batch.ee.chunk.BaseDatabaseItemReader>` を実装すること。

:java:extdoc:`BaseDatabaseItemReader <nablarch.fw.batch.ee.chunk.BaseDatabaseItemReader>` を実装することで、
リーダ専用のデータベース接続を使用してデータを抽出できる。
これにより、トランザクション制御時にカーソルを自動的にクローズするデータベースの場合でも、
データベースを入力とするChunkステップを実現できる。

以下に実装例を示す。

.. code-block:: java

  @Dependent
  @Named
  public class EmployeeSearchReader extends BaseDatabaseItemReader {
  
    /** データベースからの取得結果(リソース解放用) */
    private DeferredEntityList<EmployeeForm> list;

    /** データベースからの取得結果を保持するイテレータ */
    private Iterator<EmployeeForm> iterator;

    /** 進捗管理Bean */
    private final ProgressManager progressManager;

    /**
     * コンストラクタ。
     * @param progressManager 進捗管理Bean
     */
    @Inject
    public EmployeeSearchReader(ProgressManager progressManager) {
      this.progressManager = progressManager;
    }
  
    /**
     * BaseDatabaseItemReaderが提供するdoOpenを実装して、データベースから処理対象データを抽出する。
     * 大量データを取得する場合には、ヒープを圧迫しないよう遅延ロードを行うこと
     */
    @Override
    public void doOpen(Serializable checkpoint) throws Exception {
      progressManager.setInputCount(
          UniversalDao.countBySqlFile(EmployeeForm.class, "SELECT_EMPLOYEE"));

      list = (DeferredEntityList<EmployeeForm>) UniversalDao.defer()
              .findAllBySqlFile(EmployeeForm.class, "SELECT_EMPLOYEE");
      iterator = list.iterator();
    }

    /**
     * readItemでは、次の1レコードを返す。
     * なお、データが存在しない場合や最後まで処理した場合はnullを返す。
     */
    @Override
    public Object readItem() {
        if (iterator.hasNext()) {
            return iterator.next();
        }
        return null;
    }

    /**
     * リソースの解放が必要な場合は、doCloseを実装する。
     */
    @Override
    public void doClose() throws Exception {
        list.close();
    }
  }
