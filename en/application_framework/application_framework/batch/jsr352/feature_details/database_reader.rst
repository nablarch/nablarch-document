Chunk Step with Database as Input
======================================================
.. contents:: Table of contents
  :depth: 3
  :local:
  
When extracting data for processing from the database, implement :java:extdoc:`BaseDatabaseItemReader <nablarch.fw.batch.ee.chunk.BaseDatabaseItemReader>` that is provided by this function instead of the reader provided by JSR352.

By implementing :java:extdoc:`BaseDatabaseItemReader <nablarch.fw.batch.ee.chunk.BaseDatabaseItemReader>` , data can be extracted using a database connection that is exclusive for the reader. 
As a result, Chunk step can be implemented with database as input even in the case of databases that automatically close the cursor during transaction control.

An implementation example is shown below.

.. code-block:: java

  @Dependent
  @Named
  public class EmployeeSearchReader extends BaseDatabaseItemReader {
  
    /** Results fetched from the database ((for releasing resources)) */
    private DeferredEntityList<EmployeeForm> list;

    /** Iterator that stores the result acquired from the database */
    private Iterator<EmployeeForm> iterator;

    /** Progress manager Bean */
    private final ProgressManager progressManager;

    /**
     * Constructor.
     * @param progressManager Progress manager Bean
     */
    @Inject
    public EmployeeSearchReader(ProgressManager progressManager) {
      this.progressManager = progressManager;
    }
  
    /**
     *  Implementation of doOpen provided by BaseDatabaseItemReader and extracts the data for processing from the database.
     * When fetching a large amount of data, perform deferred loading to avoid heap compression
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
     * readItem returns the next record.
     *Returns null if the data is not found or has been processed to the end.
     */
    @Override
    public Object readItem() {
        if (iterator.hasNext()) {
            return iterator.next();
        }
        return null;
    }

    /**
     * If resources needs to be released, implement doClose.
     */
    @Override
    public void doClose() throws Exception {
        list.close();
    }
  }
