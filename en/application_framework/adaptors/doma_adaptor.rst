.. _doma_adaptor:

Doma Adapter
==================================================

.. contents:: Table of contents
  :depth: 3
  :local:

Provides an adapter to access the database using `Doma2(external site) <https://doma.readthedocs.io/en/stable/>`_

Using Doma for database access offers the following benefits:

* Like Nablarch, you can build SQL statements dynamically during execution.  
* Since it is 2waySQL, SQL statements are not required to be rewritten as in Nablarch and can be executed directly using an SQL tool.

Since only the actions specified in  :java:extdoc:`Transactional<nablarch.integration.doma.Transactional>` .
interceptor can be subject to transaction management by using this adapter, unnecessary transaction control processing is reduced, and performance is improved.

Module list
--------------------------------------------------
.. code-block:: xml

  <!-- Doma adaptor -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-doma-adaptor</artifactId>
  </dependency>
    
.. tip::

  Tests are conducted using Doma version 2.16.0. 
  When changing the version, test in the project to confirm that there are no problems.

Configuration for using the Doma adapter
--------------------------------------------------
To use this adapter, it is necessary to define the dialect and data source of Doma in the component configuration file according to the RDBMS used in the project.

A configuration example when H2 is used is shown below.

Point
 * The defined dialect should be an implementation class of  ``org.seasar.doma.jdbc.dialect.Dialect`` .
 * The component name of the dialect should be ``domaDialect`` .
 * The component name of the data source should be ``dataSource`` .

.. code-block:: xml

  <component name="domaDialect" class="org.seasar.doma.jdbc.dialect.H2Dialect"  />
  <component name="dataSource" class="org.h2.jdbcx.JdbcDataSource">
    <!--  Property omitted  -->
  </component>

Access the database using Doma
--------------------------------------------------
The procedure to access the database using Doma is shown below.

Create Dao interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Create Dao (Data Access Object) interface for database access.

Point
 * Specify :java:extdoc:`DomaConfig<nablarch.integration.doma.DomaConfig>` in config attribute of Dao annotation.

.. code-block:: java

  @Dao(config = DomaConfig.class)
  public interface ProjectDao {
          // Omitted
  }

Implement database access processing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Implement database access processing in business action method.

Point
 * Configure :java:extdoc:`Transactional<nablarch.integration.doma.Transactional>` interceptor to make business action method be subject to transaction management
 * Configure :java:extdoc:`DomaDaoRepository#get<nablarch.integration.doma.DomaDaoRepository.get(java.lang.Class)>` to look up Dao implementation class

  .. tip::

    In Doma, since the implementation class of Dao is automatically generated during compilation by annotation processing, the implementation class does not exist as yet at the time of coding.
    Therefore,  :java:extdoc:`DomaDaoRepository<nablarch.integration.doma.DomaDaoRepository>` is provided as a function to look up the implementation class of Dao in this adapter.  

.. code-block:: java

    @Transactional
    public HttpResponse create(final HttpRequest request, final ExecutionContext context) {
        final Project project = SessionUtil.delete(context, "project");

        DomaDaoRepository.get(ProjectDao.class).insert(project);

        return new HttpResponse("redirect://complete");
    }

Execute in another transaction
--------------------------------------------------
Accessing the database using a different transaction than the one started by the :java:extdoc:`Transactional<nablarch.integration.doma.Transactional>` interceptor may be required in some cases

n that case, control in another transaction using TransactionManager fetched by  :java:extdoc:`DomaConfig#getTransactionManager <nablarch.integration.doma.DomaConfig.getTransactionManager()>`.

An implementation example is shown below.

.. code-block:: java

  DomaConfig.singleton()
          .getTransactionManager()
          .requiresNew(() ->
                  DomaDaoRepository.get(ProjectDao.class).insert(project);


Using in a JSR352-compliant batch application
----------------------------------------------------------------
The following listeners are provided in this adapter to use Doma in JSR352-compliant batch applications.

* :java:extdoc:`DomaTransactionStepListener<nablarch.integration.doma.batch.ee.listener.DomaTransactionStepListener>`
* :java:extdoc:`DomaTransactionItemWriteListener<nablarch.integration.doma.batch.ee.listener.DomaTransactionItemWriteListener>`

By defining these listeners in the listener list, it is possible to access the database using Doma even in JSR352-compliant batch applications.

The configuration example shown below.

.. code-block:: xml

  <list name="stepListeners">
    <!--  Other listeners are omitted  -->
    <component class="nablarch.integration.doma.batch.ee.listener.DomaTransactionStepListener" />
  </list>

  <list name="itemWriteListeners">
    <!--  Other listeners are omitted  -->
    <component class="nablarch.integration.doma.batch.ee.listener.DomaTransactionItemWriteListener" />
  </list>

.. important::

  When performing batch update (batch insert, batch update, etc.) for the database with ItemWriter of :ref:`Chunk step <jsr352-batch_type_chunk>` , the batch size has to be specified explicitly.
  ※Note that the size of the item-count of the Chunk step is not the batch size

  If the batch size is not specified explicitly, the default value of Doma will be applied, and performance may not improve by using batch updates.

  Implementation examples
    For example, when batch insert is performed for every 1000 records, implement the Dao method as follows.

    .. code-block:: java

      @BatchInsert(batchSize = 1000)
      int[] batchInsert(List<Bonus> bonuses);


Deferred loading in jsr352-compliant batch applications
---------------------------------------------------------
When loading a large amount of data with JSR352-compliant batch applications, you may want to use deferred loading.

In that case, specify :java:extdoc:`DomaTransactionNotSupportedConfig<nablarch.integration.doma.DomaTransactionNotSupportedConfig>` in the config attribute of Dao annotation.

.. important::

  If :java:extdoc:`DomaConfig<nablarch.integration.doma.DomaConfig>` is used for the config attribute, then the stream is closed when the transaction is committed by :java:extdoc:`DomaTransactionItemWriteListener<nablarch.integration.doma.batch.ee.listener.DomaTransactionItemWriteListener>` and subsequent records cannot be read.

An implementation example is shown below.

Dao interface
  Point
    * Specify :java:extdoc:`DomaTransactionNotSupportedConfig<nablarch.integration.doma.DomaTransactionNotSupportedConfig>`  in the config attribute of Dao annotation.
    * The search result is fetched by :java:extdoc:`Stream<java.util.stream.Stream>`.

  .. code-block:: java

    @Dao(config = DomaTransactionNotSupportedConfig.class)
    public interface ProjectDao {

            @Select(strategy = SelectType.RETURN)
            Stream<Project> search();
    }

ItemReader class
  Point
     * Fetch the search result stream with open method.
     * Always close the stream with the close method to prevent the release of resources.

  .. code-block:: java

    @Dependent
    @Named
    public class ProjectReader extends AbstractItemReader {

        private Iterator<Project> iterator;

        private Stream<Project> stream;

        @Override
        public void open(Serializable checkpoint) throws Exception {
            final ProjectDao dao = DomaDaoRepository.get(ProjectDao.class);
            stream = dao.search();
            iterator = stream.iterator();
        }

        @Override
        public Object readItem() {
            if (iterator.hasNext()) {
                return iterator.next();
            } else {
                return null;
            }
        }

        @Override
        public void close() throws Exception {
            stream.close();
        }
    }

Use in ETL
--------------------------------------------------
When using ETL, using Doma in steps added to the project may be required.
In such a case, a listener list in which a job name and step name are specified is defined.

The configuration example shown below.

Job definition file
  .. code-block:: xml

    <job id="sampleJob" xmlns="http://xmlns.jcp.org/xml/ns/javaee" version="1.0">
      <step id="sampleStep">
        <listeners>
          <listener ref="nablarchStepListenerExecutor" />
          <listener ref="nablarchItemWriteListenerExecutor" />
        </listeners>
        <chunk>
          <reader ref="sampleItemReader" />
          <writer ref="sampleItemWriter" />
        </chunk>
      </step>
    </job>

Component configuration file
  .. code-block:: xml

    <list name="sampleJob.sampleStep.stepListeners">
      <!--  Other listeners are omitted  -->
      <component
          class="nablarch.integration.doma.batch.ee.listener.DomaTransactionStepListener" />
    </list>

    <list name="sampleJob.sampleStep.itemWriteListeners">
      <!--  Other listeners are omitted  -->
      <component
          class="nablarch.integration.doma.batch.ee.listener.DomaTransactionItemWriteListener" />
    </list>

Accessing multiple databases
--------------------------------------------------
If more than one database is to be accessed, create a new config class and implement access to the other database using that config class.

An implementation example is shown below.

Component configuration file
  .. code-block:: xml

    <component name="customDomaDialect" class="org.seasar.doma.jdbc.dialect.OracleDialect"  />
    <component name="customDataSource" class="oracle.jdbc.pool.OracleDataSource">
      <!--  Property omitted  -->
    </component>

Config class
  .. code-block:: java

    @SingletonConfig
    public final class CustomConfig implements Config {

        private CustomConfig() {
            dialect = SystemRepository.get("customDomaDialect");
            localTransactionDataSource =
                    new LocalTransactionDataSource(SystemRepository.get("customDataSource"));
            localTransaction = localTransactionDataSource.getLocalTransaction(getJdbcLogger());
            localTransactionManager = new LocalTransactionManager(localTransaction);
        }

            // Implement other fields and methods in reference to DomaConfig
    }

Dao interface
  .. code-block:: java

    @Dao(config = CustomConfig.class)
    public interface ProjectDao {
            // Omitted
    }


Business action class
  .. code-block:: java

    public HttpResponse create(final HttpRequest request, final ExecutionContext context) {
        final Project project = SessionUtil.delete(context, "project");

        CustomConfig.singleton()
                .getTransactionManager()
                .requiresNew(() ->
                        DomaDaoRepository.get(ProjectDao.class).insert(project);

        return new HttpResponse("redirect://complete");
    }
    
Use Doma and Nablarch database access together
--------------------------------------------------
Even if Doma is used for database access, you may want to use database access :ref:`provided by Nablarch<database_management>`. 
For example, when using :ref:`the mail sending library <mail>`. (:ref:`Database is used in mail send request <mail-request>`.)

To solve this problem, a function is provided by the database access processing of Nablarch that can use the same transaction (database connection) as Doma.

Usage procedure
  Add the following definition to the component configuration file. 
  As a result, database access of Nablarch is automatically executed under the transaction of Doma.
  
  * Define :java:extdoc:`ConnectionFactoryFromDomaConnection <nablarch.integration.doma.ConnectionFactoryFromDomaConnection>` in the component configuration file.
    The component name should be ``connectionFactoryFromDoma``.
  * Configure ConnectionFactoryFromDomaConnection in the listener that controls the transaction of JSR352 Doma.

  .. code-block:: xml

    <!--  Component name is connectionFactoryFromDoma  -->
    <component name="connectionFactoryFromDoma"
        class="nablarch.integration.doma.ConnectionFactoryFromDomaConnection">
        
        <!--  Configuration of properties are omitted  -->
      
    </component>
    
    <!--  
    When using in JSR352-compliant batch application configure connectionFactoryFromDoma defined 
    above in the listener that controls the transaction of Doma.
    -->
    <component class="nablarch.integration.doma.batch.ee.listener.DomaTransactionItemWriteListener">
      <property name="connectionFactory" ref="connectionFactoryFromDoma" />
    </component>

    <component class="nablarch.integration.doma.batch.ee.listener.DomaTransactionStepListener">
      <property name="connectionFactory" ref="connectionFactoryFromDoma" />
    </component>

Switch logger
--------------------------------------------------
This adapter provides  :java:extdoc:`NablarchJdbcLogger<nablarch.integration.doma.NablarchJdbcLogger>`, which uses Nablarch logger as an implementation of the logger used by Doma.
Although  :java:extdoc:`NablarchJdbcLogger<nablarch.integration.doma.NablarchJdbcLogger>` is used by default, if the logger is to be replaced with another one, it must be configured in the component definition file.

The configuration example when ``org.seasar.doma.jdbc.UtilLoggingJdbcLogger`` is used is shown below.

Point
 * The defined logger must be an implementation class of ``org.seasar.doma.jdbc.JdbcLogger``
 * The component name of the logger should be ``domaJdbcLogger``

.. code-block:: xml

  <component name="domaJdbcLogger" class="org.seasar.doma.jdbc.UtilLoggingJdbcLogger"  />

Perform configuration for java.sql.Statement
--------------------------------------------------
You may want to configure items related to ``java.sql.Statement`` such as fetch size and query timeout for the whole project.

In such a case, configure :java:extdoc:`DomaStatementProperties<nablarch.integration.doma.DomaStatementProperties>` in the component configuration file.

Items that can be configured include the following.

* Maximum number of rows
* Fetch size
* Query timeout (seconds)
* Batch size

The configuration example shown below.

Point
 * The component name should be ``domaStatementProperties``

.. code-block:: xml

  <component class="nablarch.integration.doma.DomaStatementProperties" name="domaStatementProperties">
    <!-- Configure the limit for maximum number of rows to 1000 -->
    <property name="maxRows" value="1000" />
    <!-- Configure the fetch size to 200 rows -->
    <property name="fetchSize" value="200" />
    <!-- Configure query timeout to 30 seconds -->
    <property name="queryTimeout" value="30" />
    <!-- Configure batch size to 400 -->
    <property name="batchSize" value="400" />
  </component>
