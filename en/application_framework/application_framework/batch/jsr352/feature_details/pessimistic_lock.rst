Pessimistic Lock for JSR352-compliant Batch Applications
============================================================
This section shows an implementation example for pessimistic lock in a JSR352-compliant batch application. 
By implementing with reference to the examples shown below, the lock time can be reduced and the effect on other processes can be reduced.

Point
 * The `ItemReader` fetches only the primary key of the record to be processed.
 * Fetch the record for processing based on the master key in `ItemProcessor` and perform a pessimistic lock. 
   For information on pessimistic lock using :ref:`universal_dao` , see :ref:`universal_dao_jpa_pessimistic_lock` .

.. code-block:: java

  @Dependent
  @Named
  public class SampleReader extends AbstractItemReader {

      private DeferredEntityList<ProjectId> list;

      private Iterator<ProjectId> iterator;

      @Override
      public void open(Serializable checkpoint) throws Exception {

          // The acquisition process for search criteria is omitted

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

          // Omitted for business operations

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

