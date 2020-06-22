.. _nablarch_batch_pessimistic_lock:

Pessimistic Lock of Nablarch Batch Application
============================================================
This section shows an implementation example to perform pessimistic lock
in the Nablarch batch application. By implementing with reference to the examples shown below,
the lock duration can be reduced and the effect on other processes can be reduced.

Points
 * The data reader fetches only the primary key of the record to be processed.
 * Perform pessimistic lock with `handle` method.
   For information on pessimistic lock using :ref:`universal_dao`, see :ref:`universal_dao_jpa_pessimistic_lock`.

.. code-block:: java

  public class SampleAction extends BatchAction<SqlRow> {

      @Override
      public DataReader<SqlRow> createReader(final ExecutionContext ctx) {
          final DatabaseRecordReader reader = new DatabaseRecordReader();
          final SqlPStatement statement = DbConnectionContext.getConnection()
                  .prepareParameterizedSqlStatementBySqlId(
                          Project.class.getName() + "#GET_ID");

          // Omit search condition acquisition process

          reader.setStatement(statement, condition);
          return reader;
      }

      @Override
      public Result handle(final SqlRow inputData, final ExecutionContext ctx) {
          final Project project =
                  UniversalDao.findBySqlFile(Project.class, "FIND_BY_ID_WITH_LOCK", inputData);

          // Omitted for business process

          UniversalDao.update(project);
          return new Success();
      }
  }

