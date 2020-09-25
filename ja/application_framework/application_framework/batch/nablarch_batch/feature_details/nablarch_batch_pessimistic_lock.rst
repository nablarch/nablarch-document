.. _nablarch_batch_pessimistic_lock:

Nablarchバッチアプリケーションの悲観的ロック
============================================================
本項では、Nablarchバッチアプリケーションで悲観的ロックを行うための実装例を示す。
以下に示す例を参考に実装することで、ロック時間が短縮され他プロセスへの影響を抑えることができる。

ポイント
 * データリーダでは処理対象レコードの主キーのみ取得する。
 * `handle` メソッド内で悲観的ロックを行う。
   :ref:`universal_dao` を使用した悲観的ロックについては :ref:`universal_dao_jpa_pessimistic_lock` を参照。

.. code-block:: java

  public class SampleAction extends BatchAction<SqlRow> {

      @Override
      public DataReader<SqlRow> createReader(final ExecutionContext ctx) {
          final DatabaseRecordReader reader = new DatabaseRecordReader();
          final SqlPStatement statement = DbConnectionContext.getConnection()
                  .prepareParameterizedSqlStatementBySqlId(
                          Project.class.getName() + "#GET_ID");

          // 検索条件の取得処理は省略

          reader.setStatement(statement, condition);
          return reader;
      }

      @Override
      public Result handle(final SqlRow inputData, final ExecutionContext ctx) {
          final Project project =
                  UniversalDao.findBySqlFile(Project.class, "FIND_BY_ID_WITH_LOCK", inputData);

          // 業務処理のため省略

          UniversalDao.update(project);
          return new Success();
      }
  }

