Jakarta Batchに準拠したバッチアプリケーションの悲観的ロック
============================================================
本項では、Jakarta Batchに準拠したバッチアプリケーションで悲観的ロックを行うための実装例を示す。
以下に示す例を参考に実装することで、ロック時間が短縮され他プロセスへの影響を抑えることができる。

ポイント
 * `ItemReader` では処理対象レコードの主キーのみ取得する。
 * `ItemProcessor` で主キーをもとに処理対象レコードを取得して悲観的ロックを行う。
   :ref:`universal_dao` を使用した悲観的ロックについては :ref:`universal_dao_jpa_pessimistic_lock` を参照。

.. code-block:: java

  @Dependent
  @Named
  public class SampleReader extends AbstractItemReader {

      private DeferredEntityList<ProjectId> list;

      private Iterator<ProjectId> iterator;

      @Override
      public void open(Serializable checkpoint) throws Exception {

          // 検索条件の取得処理は省略

          list = (DeferredEntityList<ProjectId>) UniversalDao.defer()
                  .findAllBySqlFile(ProjectId.class, "GET_ID", condition);
          iterator = list.iterator();
      }

      @Override
      public Object readItem() {
          if (iterator.hasNext()) {
              return iterator.next();
          }
          return null;
      }

      @Override
      public void close() throws Exception {
          list.close();
      }
  }

  @Dependent
  @Named
  public class SampleProcessor implements ItemProcessor {

      @Override
      public Object processItem(Object item) {
          final Project project =
                  UniversalDao.findBySqlFile(Project.class, "FIND_BY_ID_WITH_LOCK", item);

          // 業務処理のため省略

          return project;
      }
  }

  @Dependent
  @Named
  public class SampleWriter extends AbstractItemWriter {

      @Override
      public void writeItems(List<Object> items) {
          UniversalDao.batchUpdate(items);
      }
  }

