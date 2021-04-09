.. _`getting_started_nablarch_batch`:

Creating a Batch to Register Files to the DB
==========================================================
How to register files in DB will be explained with an example application.

Overview of the function to be created
  .. image:: ../images/overview.png

Execution procedure of the mailing address file registration batch
  1. Delete data in the table to be registered

     Execute the following SQL from the console of H2 and delete the data in the table to be registered.

     .. code-block:: sql

       TRUNCATE TABLE ZIP_CODE_DATA;

  2. Execute the mailing address file registration batch

    Execute the following command from the command prompt

    .. code-block:: bash

      $cd {nablarch-example-batch repository}
      $mvn exec:java -Dexec.mainClass=nablarch.fw.launcher.Main ^
          -Dexec.args="'-requestPath' 'ImportZipCodeFileAction/ImportZipCodeFile' '-diConfig' 'classpath:import-zip-code-file.xml' '-userId' '105'"

  3. Confirm that the contents of the file are registered in the DB

     Execute the following SQL from the console of H2 and confirm that the mailing address information is registered.

     .. code-block:: sql

       SELECT * FROM ZIP_CODE_DATA;

Register file to DB
----------------------
For the method of creating the batch to register the files to database,
it is explained by dividing into
:ref:`reads data from the input data source <getting_started_nablarch_batch-read>` and
:ref:`execution of business logic <getting_started_nablarch_batch-business-action>`.

For the process flow, see :ref:`process flow of the Nablarch batch <nablarch_batch-process_flow>`.
For responsibility assignment, refer to :ref:`the responsibility assignment of the Nablarch batch<nablarch_batch-application_design>`.

Refer to `import-zip-code-file.xml` for the handler configuration of the mailing address file registration batch.


.. _`getting_started_nablarch_batch-read`:

Reads data from the input data source
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
The process of reading data from the input data source is described.

#. :ref:`Create a form that accepts input files<getting_started_nablarch_batch-form>`
#. :ref:`Create a data reader<getting_started_nablarch_batch-data_reader>`

.. _`getting_started_nablarch_batch-form`:

Create a form that accepts input files
  Create a form that binds CSV(mailing address file) using :ref:`data_bind`.

  ZipCodeForm.java
    .. code-block:: java

      @Csv(properties = {/** Property definition is omitted **/}, type = CsvType.CUSTOM)
      @CsvFormat(charset = "UTF-8", fieldSeparator = ',',
              ignoreEmptyLine = true, lineSeparator = "\r\n", quote = '"',
              quoteMode = QuoteMode.NORMAL, requiredHeader = false, emptyToNull = true)
      public class ZipCodeForm {

          // Excerpt of only some items

          /** National local government code */
          @Domain("localGovernmentCode")
          @Required
          private String localGovernmentCode;

          /**
           * Returns the zip code (5 digits).
           *
           * @return Zip code (5 digits)
           */
          public String getZipCode5digit() {
              return zipCode5digit;
          }

          /**
           * Column holding the line count
           */
          private Long lineNumber;

          /**
           * Get line count.
           *
           * @return line count
           */
          @LineNumber
          public Long getLineNumber() {
              return lineNumber;
          }

          // Other setters and getters are omitted

      }

  Key points of this implementation
    * To bind the CSV to the form using :ref:`data_bind`, :java:extdoc:`Csv<nablarch.common.databind.csv.Csv>`
      and :java:extdoc:`CsvFormat<nablarch.common.databind.csv.CsvFormat>` are granted.
    * To execute :ref:`bean_validation`, annotation is granted for validation.
    * By defining the line count property and granting :java:extdoc:`LineNumber<nablarch.common.databind.LineNumber>` to the getter,
      the line of the target data can be configured automatically.

.. _`getting_started_nablarch_batch-data_reader`:

Create a data reader
  Create an implementation class of :java:extdoc:`DataReader<nablarch.fw.DataReader>` 
  that reads the file and passing one line at a time to the business action method.

  ZipCodeFileReader.java
    .. code-block:: java

      public class ZipCodeFileReader implements DataReader<ZipCodeForm> {

          /**
           * Name of the file to read
           */
          private static final String FILE_NAME = "importZipCode";

          /**
           * Iterator that returns the data to be processed
           */
          private ObjectMapperIterator<ZipCodeForm> iterator;

          /**
           * Return one line of data processed by the business handler.
           *
           * @param ctx Execution context
           * @return One line of data
           */
          @Override
          public ZipCodeForm read(ExecutionContext ctx) {
              if (iterator == null) {
                  initialize();
              }
              return iterator.next();
          }

          /**
           * Returns whether there is a next line.
           *
           * @param ctx Execution context
           * @return If there is a next line {@code true} , if there is no next line {@code false}
           */
          @Override
          public boolean hasNext(ExecutionContext ctx) {
              if (iterator == null) {
                  initialize();
              }
              return iterator.hasNext();
          }

          /**
           * End process.
           * <p/>
           * {@link ObjectMapperIterator#close()} is called.
           * @param ctx Execution context
           */
          @Override
          public void close(ExecutionContext ctx) {
              iterator.close();
          }

          /**
           * Initialization process.
           * <p/>
           * Create an iterator.
           * @throws RuntimeException When reading the file fails
           */
          private void initialize() {
              FilePathSetting filePathSetting = FilePathSetting.getInstance();
              File zipCodeFile = filePathSetting.getFileWithoutCreate("csv-input", FILE_NAME);

              // Create an iterator used for reading files
              try {
                  iterator
                      = new ObjectMapperIterator<>(ObjectMapperFactory.create(ZipCodeForm.class,
                          new FileInputStream(zipCodeFile)));
              } catch (FileNotFoundException e) {
                  throw new IllegalStateException(e);
              }
          }
      }

  Key points of this implementation
    * Implements the process to return data of one line in `read` method. The data that has been read by using the `read` method is delivered to the business action handler.
    * Implements the process to determine if the next line exists in `hasNext` method. The file reading process is terminated if this method returns `false`.
    * The `close` method implements the close process after reading of the file is complete.

  .. tip::
    When data is read from a class that does not have the `hasNext` method like :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>`,
    it is not only possible to simplify the implementation of data reader by creating an iterator,
    but also the effort of implementing the data reading process for each batch can be minimized.
    For iterator implementation, see the implementation of `ObjectMapperIterator.java` in the example application.

.. _`getting_started_nablarch_batch-business-action`:

Execute the business logic
++++++++++++++++++++++++++++++++++++
This section describes the part that executes the business logic

#. :ref:`Create a business action<getting_started_nablarch_batch-action>`

.. _`getting_started_nablarch_batch-action`:

Create a business action
  Inherits :java:extdoc:`BatchAction<nablarch.fw.action.BatchAction>` and creates the business action class.

  ImportZipCodeFileAction.java
    .. code-block:: java

      public class ImportZipCodeFileAction extends BatchAction<ZipCodeForm> {

          /**
           * {@link com.nablarch.example.app.batch.reader.ZipCodeFileReader}
           * registers information of one line passed by the above to the DB.
           * <p/>
           * Since {@link com.nablarch.example.app.batch.interceptor.ValidateData}
           * is intercepted when the method is executed, validated
           * {@param inputData} is always passed to this method.
           *
           * @param inputData Mailing address information for one line
           * @param ctx       Execution context
           * @return Result object
           */
          @Override
          @ValidateData
          public Result handle(ZipCodeForm inputData, ExecutionContext ctx) {

              ZipCodeData data = BeanUtil.createAndCopy(ZipCodeData.class, inputData);
              UniversalDao.insert(data);

              return new Result.Success();
          }

          /**
           * Create a reader.
           *
           * @param ctx Execution context
           * @return Reader object
           */
          @Override
          public DataReader<ZipCodeForm> createReader(ExecutionContext ctx) {
              return new ZipCodeFileReader();
          }
      }

  Key points of this implementation
    * Process for one line of data that is passed over from the data reader is implemented in the `handle` method.
    * Use :java:extdoc:`UniversalDao#insert <nablarch.common.dao.UniversalDao.insert(java.lang.Object)>` to register a mailing address entity in the database.
    * The `createReader` method returns the instance of data reader class to be used.

  .. tip::
    As there is no difference in the execution logic of :ref:`bean_validation` between the batches,
    the validation process is shared by creating an interceptor in the example application.
    For interceptor implementation, see the implementation of `ValidateData.java` in the example application.
