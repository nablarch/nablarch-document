.. _doma_adaptor:

Doma Adapter
==================================================

.. contents:: Table of contents
  :depth: 3
  :local:

Provides an adapter to access the database using `Doma2(external site) <https://doma.readthedocs.io/en/latest/>`_

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

  Tests are conducted using Doma version 2.62.0. 
  When changing the version, test in the project to confirm that there are no problems.

Configuration for using the Doma adapter
--------------------------------------------------
The steps for using this adapter are shown below.

.. _`doma_dependency`:

Configure dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You need to set the project dependencies by referring to the following.

For details, see `Maven build configuration in Doma2(external site) <https://doma.readthedocs.io/en/latest/build/#build-with-maven>`_ .

.. code-block:: xml

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                    <annotationProcessorPaths>
                        <path>
                            <groupId>org.seasar.doma</groupId>
                            <artifactId>doma-processor</artifactId>
                            <version>2.62.0</version>
                        </path>
                    </annotationProcessorPaths>
                    <!-- If you are using Eclipse, set the following arguments.
                    <compilerArgs>
                        <arg>-Adoma.resources.dir=${project.basedir}/src/main/resources</arg>
                    </compilerArgs>
                    -->
                </configuration>
            </plugin>
        </plugins>
    </build>

Configure the Doma dialect and data source to match the RDBMS you are using
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You need to define the Doma dialect and data source in the component configuration file to match the RDBMS used in your project.

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

.. code-block:: java

  @Dao
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

.. tip::

    As the config attribute of the Dao annotation has been deprecated from Doma 2.44.0, the implementation method has changed from the information provided prior to Doma 2.44.0.
    For more information, see :ref:`migration_doma2.44.0` .

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


Using in a Jakarta Batch-compliant batch application
----------------------------------------------------------------
The following listeners are provided in this adapter to use Doma in Jakarta Batch-compliant batch applications.

* :java:extdoc:`DomaTransactionStepListener<nablarch.integration.doma.batch.ee.listener.DomaTransactionStepListener>`
* :java:extdoc:`DomaTransactionItemWriteListener<nablarch.integration.doma.batch.ee.listener.DomaTransactionItemWriteListener>`

By defining these listeners in the listener list, it is possible to access the database using Doma even in Jakarta Batch-compliant batch applications.

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


Deferred loading in Jakarta Batch-compliant batch applications
---------------------------------------------------------------
When loading a large amount of data with Jakarta Batch-compliant batch applications, you may want to use deferred loading.

In that case, when looking up the Dao implementation class, use :java:extdoc:`DomaDaoRepository#get(java.lang.Class,java.lang.Class)<nablarch.integration.doma.DomaDaoRepository.get(java.lang.Class,java.lang.Class)>` and specify the Class class of :java:extdoc:`DomaTransactionNotSupportedConfig<nablarch.integration.doma.DomaTransactionNotSupportedConfig>` as the second argument.

.. important::

  When :java:extdoc:`DomaDaoRepository#get(java.lang.Class)<nablarch.integration.doma.DomaDaoRepository.get(java.lang.Class)>` is used, :java:extdoc:`DomaConfig<nablarch.integration.doma.DomaConfig>` is used, therefore the stream is closed when the transaction is committed by :java:extdoc:`DomaTransactionItemWriteListener<nablarch.integration.doma.batch.ee.listener.DomaTransactionItemWriteListener>` , and subsequent records cannot be read.

An implementation example is shown below.

Dao interface
  Point
    * The search result is fetched by :java:extdoc:`Stream<java.util.stream.Stream>`.

  .. code-block:: java

    @Dao
    public interface ProjectDao {

            @Select(strategy = SelectType.RETURN)
            Stream<Project> search();
    }

ItemReader class
  Point
     * To get the Dao implementation class, use :java:extdoc:`DomaDaoRepository#get(java.lang.Class,java.lang.Class)<nablarch.integration.doma.DomaDaoRepository.get(java.lang.Class,java.lang.Class)>` and specify :java:extdoc:`DomaTransactionNotSupportedConfig<nablarch.integration.doma.DomaTransactionNotSupportedConfig>` as the second argument.
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
            final ProjectDao dao = DomaDaoRepository.get(ProjectDao.class, DomaTransactionNotSupportedConfig.class);
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

.. tip::

    As the config attribute of the Dao annotation has been deprecated from Doma 2.44.0, the implementation method has changed from the information provided prior to Doma 2.44.0.
    For more information, see :ref:`migration_doma2.44.0` .

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
  Point
     * Implement the Config interface provided by Doma.
     * It has public visibility and a no-arg constructor.

  .. code-block:: java

    public final class CustomConfig implements Config {

        public CustomConfig() {
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

    @Dao
    public interface ProjectDao {
        // Omitted
    }


Business action class
  Point
     * To get the Dao implementation class, use :java:extdoc:`DomaDaoRepository#get(java.lang.Class,java.lang.Class)<nablarch.integration.doma.DomaDaoRepository.get(java.lang.Class,java.lang.Class)>` and specify the created Config class as the second argument.

  .. code-block:: java

    public HttpResponse create(final HttpRequest request, final ExecutionContext context) {
        final Project project = SessionUtil.delete(context, "project");

        CustomConfig.singleton()
                .getTransactionManager()
                .requiresNew(() ->
                        DomaDaoRepository.get(ProjectDao.class).insert(project);

        return new HttpResponse("redirect://complete");
    }

.. tip::

    As SingletonConfig annotation and config attribute of Dao annotation has been deprecated from Doma 2.44.0, the implementation method has changed from the information provided prior to Doma 2.44.0.
    For more information, see :ref:`migration_doma2.44.0` .

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
  * Configure ConnectionFactoryFromDomaConnection in the listener that controls the transaction of Doma for Jakarta Batch.

  .. code-block:: xml

    <!--  Component name is connectionFactoryFromDoma  -->
    <component name="connectionFactoryFromDoma"
        class="nablarch.integration.doma.ConnectionFactoryFromDomaConnection">
        
        <!--  Configuration of properties are omitted  -->
      
    </component>
    
    <!--  
    When using in Jakarta Batch-compliant batch application configure connectionFactoryFromDoma defined 
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

.. _`migration_doma2.44.0`:

Migrating from Doma 2.44.0
--------------------------------------------------

As the config attribute of the Dao annotation and the SingletonConfig annotation have been deprecated from `Doma 2.44.0(external site) <https://github.com/domaframework/doma/releases/tag/2.44.0>`_ , Nablarch has also added an API and changed the implementation method from what was previously provided.

Implementations using the config attribute of the Dao annotation and the SingletonConfig annotation will continue to work, but it is recommended to migrate the implementation method to match the changes in Doma.

Here we explain the comparison with the implementation method that was provided on Nablarch before Doma 2.44.0.

Note that the implementation method provided before Doma 2.44.0 will continue to operate in the same way.

If you are using the basic implementation using DomaConfig
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
An implementation example in which DomaConfig is specified in the config attribute of Dao annotation is shown below.

.. code-block:: java

  // Definition of Dao
  @Dao(config = DomaConfig.class)  /* Specify the config attribute */
  public interface ProjectDao {
      // Omitted
  }

  // Example of implementation using Dao
  @Transactional
  public HttpResponse create(final HttpRequest request, final ExecutionContext context) {
      final Project project = SessionUtil.delete(context, "project");

      DomaDaoRepository.get(ProjectDao.class).insert(project);

      return new HttpResponse("redirect://complete");
  }

This is equivalent to the following implementation.

.. code-block:: java

  // Definition of Dao
  @Dao  /* Remove the config attribute specification */
  public interface ProjectDao {
      // Omitted
  }

  // Example of implementation using Dao
  @Transactional
  public HttpResponse create(final HttpRequest request, final ExecutionContext context) {
      final Project project = SessionUtil.delete(context, "project");

      DomaDaoRepository.get(ProjectDao.class).insert(project);  /* No changes */

      return new HttpResponse("redirect://complete");
  }

When you use a Dao that does not specify the config attribute of the Dao annotation and obtain the Dao implementation class using :java:extdoc:`DomaDaoRepository#get<nablarch.integration.doma.DomaDaoRepository.get(java.lang.Class)>` , the Dao implementation class is constructed using :java:extdoc:`DomaConfig<nablarch.integration.doma.DomaConfig>` .

If you are using DomaTransactionNotSupportedConfig for lazy loading
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
An implementation example using :java:extdoc:`DomaTransactionNotSupportedConfig<nablarch.integration.doma.DomaTransactionNotSupportedConfig>` is shown below to support lazy loading in a batch application compliant with Jakarta Batch.

.. code-block:: java

    // Definition of Dao
    @Dao(config = DomaTransactionNotSupportedConfig.class)  /* Specify the config attribute */
    public interface ProjectDao {

        @Select(strategy = SelectType.RETURN)
        Stream<Project> search();
    }

    // Example of implementation using Dao
    @Dependent
    @Named
    public class ProjectReader extends AbstractItemReader {

        private Iterator<Project> iterator;

        private Stream<Project> stream;

        @Override
        public void open(Serializable checkpoint) throws Exception {
            /* Specify only the Dao interface to DomaDaoRepository#get */
            final ProjectDao dao = DomaDaoRepository.get(ProjectDao.class);
            stream = dao.search();
            iterator = stream.iterator();
        }

        // Omitted
    }

This is equivalent to the following implementation.

.. code-block:: java

    // Definition of Dao
    @Dao  /* Remove the config attribute specification */
    public interface ProjectDao {

        @Select(strategy = SelectType.RETURN)
        Stream<Project> search();
    }

    // Example of implementation using Dao
    @Dependent
    @Named
    public class ProjectReader extends AbstractItemReader {

        private Iterator<Project> iterator;

        private Stream<Project> stream;

        @Override
        public void open(Serializable checkpoint) throws Exception {
            /* Specify DomaTransactionNotSupportedConfig.class as the second argument of DomaDaoRepository#get */
            final ProjectDao dao = DomaDaoRepository.get(ProjectDao.class, DomaTransactionNotSupportedConfig.class);
            stream = dao.search();
            iterator = stream.iterator();
        }

        // Omitted
    }

When :java:extdoc:`DomaDaoRepository#get(java.lang.Class,java.lang.Class)<nablarch.integration.doma.DomaDaoRepository.get(java.lang.Class,java.lang.Class)>` is called using a Dao that does not specify the config attribute in the Dao annotation, the implementation class of the Dao is constructed using the Config specified in the second argument.

If you have created your own Config class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
An example of creating and implementing a unique Config class for reasons such as accessing multiple databases is shown below.

.. code-block:: java

    // Defining the Config class
    @SingletonConfig  /* Set the SingletonConfig annotation */
    public final class CustomConfig implements Config {

        private CustomConfig() {  /* Make it a private constructor */
            // Omitted
        }

        // Omitted
    }

    // Definition of Dao
    @Dao(config = CustomConfig.class)  /* Specify the Config class you created in the config attribute */
    public interface ProjectDao {
        // Omitted
    }

    // Example of implementation using Dao
    public HttpResponse create(final HttpRequest request, final ExecutionContext context) {
        final Project project = SessionUtil.delete(context, "project");

        CustomConfig.singleton()
                .getTransactionManager()
                .requiresNew(() ->
                        /* Specify only the Dao interface to DomaDaoRepository#get */
                        DomaDaoRepository.get(ProjectDao.class);

        return new HttpResponse("redirect://complete");
    }

This is equivalent to the following implementation.

.. code-block:: java

    // Defining the Config class
    /* Remove SingletonConfig annotation */
    public final class CustomConfig implements Config {

        public CustomConfig() {  /* Change to public constructor with no arguments */
            // Omitted
        }

        // Omitted
    }

    // Definition of Dao
    @Dao  /* Remove the config attribute specification */
    public interface ProjectDao {
        // Omitted
    }

    // Example of implementation using Dao
    public HttpResponse create(final HttpRequest request, final ExecutionContext context) {
        final Project project = SessionUtil.delete(context, "project");

        CustomConfig.singleton()
                .getTransactionManager()
                .requiresNew(() ->
                        /* Specify the Class of the Config you created as the second argument of DomaDaoRepository#get */
                        DomaDaoRepository.get(ProjectDao.class, CustomConfig.class);

        return new HttpResponse("redirect://complete");
    }

When :java:extdoc:`DomaDaoRepository#get(java.lang.Class,java.lang.Class)<nablarch.integration.doma.DomaDaoRepository.get(java.lang.Class,java.lang.Class)>` is called using a Dao that does not specify the config attribute in the Dao annotation, the implementation class of the Dao is constructed using the Config specified in the second argument.
