.. _doma_adaptor:

Domaアダプタ
==================================================

.. contents:: 目次
  :depth: 3
  :local:

`Doma2(外部サイト) <https://doma.readthedocs.io/ja/latest/>`_ を使用したデータベースアクセスを行うためのアダプタを提供する。

データベースアクセスにDomaを使用することで以下のメリットが得られる。

* Nablarchと同じように、実行時に動的にSQL文を構築できる。
* 2waySQLなので、NablarchのようにSQL文を書き換える必要がなく、SQLツール等でそのまま実行できる。

また、本アダプタを使用することで、 :java:extdoc:`Transactional<nablarch.integration.doma.Transactional>` インターセプタで
指定したアクションのみトランザクション管理対象にできるため、
不要なトランザクション制御処理を削減でき、パフォーマンスの向上が期待できる。

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <!-- Domaアダプタ -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-doma-adaptor</artifactId>
  </dependency>
  
.. tip::

  Domaのバージョン2.62.0を使用してテストを行っている。
  バージョンを変更する場合は、プロジェクト側でテストを行い問題ないことを確認すること。

Domaアダプタを使用するための設定を行う
--------------------------------------------------
本アダプタを使用するための手順を以下に示す。

依存関係の設定
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
以下を参考にプロジェクトの依存関係を設定する必要がある。

詳細は `Doma2でのMavenビルド設定(外部サイト) <https://doma.readthedocs.io/ja/latest/build/#build-with-maven>`_ を参照。

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
                    <!-- Eclipseを使用する場合は、 以下の引数を設定すること
                    <compilerArgs>
                        <arg>-Adoma.resources.dir=${project.basedir}/src/main/resources</arg>
                    </compilerArgs>
                    -->
                </configuration>
            </plugin>
        </plugins>
    </build>

使用するRDBMSに合わせてDomaのダイアレクトやデータソースを設定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
プロジェクトで使用するRDBMSに合わせてDomaのダイアレクトやデータソースをコンポーネント設定ファイルに定義する必要がある。

H2を使用する場合の設定例を以下に示す。

ポイント
 * 定義するダイアレクトは ``org.seasar.doma.jdbc.dialect.Dialect`` の実装クラスとすること
 * ダイアレクトのコンポーネント名は ``domaDialect`` とすること
 * データソースのコンポーネント名は ``dataSource`` とすること

.. code-block:: xml

  <component name="domaDialect" class="org.seasar.doma.jdbc.dialect.H2Dialect"  />
  <component name="dataSource" class="org.h2.jdbcx.JdbcDataSource">
    <!-- プロパティは省略 -->
  </component>

Domaを使用してデータベースにアクセスする
--------------------------------------------------
Domaを使用したデータベースアクセスを行うための手順を以下に示す。

Daoインタフェースを作成する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
データベースアクセスを行うためのDao(Data Access Object)インタフェースを作成する。

.. code-block:: java

  @Dao
  public interface ProjectDao {
      // 省略
  }

データベースアクセス処理を実装する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
業務アクションのメソッドにデータベースアクセス処理を実装する。

ポイント
 * 業務アクションメソッドをトランザクション管理対象とするため、
   :java:extdoc:`Transactional<nablarch.integration.doma.Transactional>` インターセプタを設定する
 * :java:extdoc:`DomaDaoRepository#get<nablarch.integration.doma.DomaDaoRepository.get(java.lang.Class)>` を使用してDaoの実装クラスをルックアップする

  .. tip::

    Domaでは注釈処理によってコンパイル時に自動的にDaoの実装クラスが生成されるため、コーディング時にはまだ実装クラスが存在しない。
    そのため、本アダプタではDaoの実装クラスをルックアップする機能として :java:extdoc:`DomaDaoRepository<nablarch.integration.doma.DomaDaoRepository>` を提供している。

.. code-block:: java

    @Transactional
    public HttpResponse create(final HttpRequest request, final ExecutionContext context) {
        final Project project = SessionUtil.delete(context, "project");

        DomaDaoRepository.get(ProjectDao.class).insert(project);

        return new HttpResponse("redirect://complete");
    }

.. tip::

    Doma 2.44.0よりDaoアノテーションのconfig属性が非推奨になったため、Doma 2.44.0以前に案内していた内容から実装方法を変更している。  
    詳しくは、 :ref:`migration_doma2.44.0` を参照すること。

別トランザクションで実行する
--------------------------------------------------
:java:extdoc:`Transactional<nablarch.integration.doma.Transactional>` インターセプタによって開始されたトランザクションではなく、
別のトランザクションを使用してデータベースアクセスを行いたい場合がある。

その場合は、 :java:extdoc:`DomaConfig#getTransactionManager <nablarch.integration.doma.DomaConfig.getTransactionManager()>` で取得した
`TransactionManager` を使用して別トランザクションで制御する。

実装例を以下に示す。

.. code-block:: java

  DomaConfig.singleton()
          .getTransactionManager()
          .requiresNew(() ->
                  DomaDaoRepository.get(ProjectDao.class).insert(project);


Jakarta Batchに準拠したバッチアプリケーションで使用する
----------------------------------------------------------------
Jakarta Batchに準拠したバッチアプリケーションでDomaを使用するために、
本アダプタでは以下のリスナーを提供している。

* :java:extdoc:`DomaTransactionStepListener<nablarch.integration.doma.batch.ee.listener.DomaTransactionStepListener>`
* :java:extdoc:`DomaTransactionItemWriteListener<nablarch.integration.doma.batch.ee.listener.DomaTransactionItemWriteListener>`

これらのリスナーをリスナーリストに定義することで、
Jakarta Batchに準拠したバッチアプリケーションでもDomaを使用したデータベースアクセスを行うことができる。

設定例を以下に示す。

.. code-block:: xml

  <list name="stepListeners">
    <!-- その他のリスナーは省略 -->
    <component class="nablarch.integration.doma.batch.ee.listener.DomaTransactionStepListener" />
  </list>

  <list name="itemWriteListeners">
    <!-- その他のリスナーは省略 -->
    <component class="nablarch.integration.doma.batch.ee.listener.DomaTransactionItemWriteListener" />
  </list>

.. important::

  :ref:`Chunkステップ <jsr352-batch_type_chunk>` のItemWriterでデータベースに対してバッチ更新(バッチinsertやバッチupdateなど)する場合、バッチサイズの指定を明示的に行う必要がある。
  ※Chunkステップのitem-countのサイズがバッチサイズとなるわけではないので注意すること

  これを行わなかった場合、Domaのデフォルト値が適用されるため、バッチ更新を使用してもパフォーマンスが向上しない可能性がある。

  実装例
    例えば、1000件ごとにバッチinsertを行う場合には、Daoのメソッドを以下のように実装する。

    .. code-block:: java

      @BatchInsert(batchSize = 1000)
      int[] batchInsert(List<Bonus> bonuses);


Jakarta Batchに準拠したバッチアプリケーションで遅延ロードを行う
----------------------------------------------------------------
Jakarta Batchに準拠したバッチアプリケーションで大量データの読み込みを行う際に、遅延ロードを使用したい場合がある。

その場合は、Daoの実装クラスをルックアップする際に :java:extdoc:`DomaDaoRepository#get(java.lang.Class,java.lang.Class)<nablarch.integration.doma.DomaDaoRepository.get(java.lang.Class,java.lang.Class)>` を使用し、第2引数に :java:extdoc:`DomaTransactionNotSupportedConfig<nablarch.integration.doma.DomaTransactionNotSupportedConfig>` のClassクラスを指定する。

.. important::

  引数が1つの :java:extdoc:`DomaDaoRepository#get(java.lang.Class)<nablarch.integration.doma.DomaDaoRepository.get(java.lang.Class)>` を使用した場合は :java:extdoc:`DomaConfig<nablarch.integration.doma.DomaConfig>` が使用されるため、 :java:extdoc:`DomaTransactionItemWriteListener<nablarch.integration.doma.batch.ee.listener.DomaTransactionItemWriteListener>` によるトランザクションのコミットでストリームがクローズされるため、後続のレコードが読み込めなくなってしまう。

実装例を以下に示す。

Daoインタフェース
  ポイント
    * 検索結果は :java:extdoc:`Stream<java.util.stream.Stream>` で取得する。

  .. code-block:: java

    @Dao
    public interface ProjectDao {

        @Select(strategy = SelectType.RETURN)
        Stream<Project> search();
    }

ItemReaderクラス
  ポイント
     * Daoの実装クラスを取得する際に :java:extdoc:`DomaDaoRepository#get(java.lang.Class,java.lang.Class)<nablarch.integration.doma.DomaDaoRepository.get(java.lang.Class,java.lang.Class)>` を使用し、第2引数に :java:extdoc:`DomaTransactionNotSupportedConfig<nablarch.integration.doma.DomaTransactionNotSupportedConfig>` を指定する。
     * openメソッドで検索結果のストリームを取得する。
     * リソースの解放漏れを防ぐため、closeメソッドで必ずストリームを閉じる。

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

    Doma 2.44.0よりDaoアノテーションのconfig属性が非推奨になったため、Doma 2.44.0以前に案内していた内容から実装方法を変更している。  
    詳しくは、 :ref:`migration_doma2.44.0` を参照すること。

複数のデータベースにアクセスする
--------------------------------------------------
複数のデータベースにアクセスする必要がある場合は、新しくConfigクラスを作成し、
別のデータベースへのアクセスはそのConfigクラスを使用して行うように実装する。

実装例を以下に示す。

コンポーネント設定ファイル
  .. code-block:: xml

    <component name="customDomaDialect" class="org.seasar.doma.jdbc.dialect.OracleDialect"  />
    <component name="customDataSource" class="oracle.jdbc.pool.OracleDataSource">
      <!-- プロパティは省略 -->
    </component>

Configクラス
  ポイント
     * Domaの提供するConfigインターフェースを実装すること。
     * 可視性がpublicで引数なしのコンストラクタを持つこと。

  .. code-block:: java

    public final class CustomConfig implements Config {

        public CustomConfig() {
            dialect = SystemRepository.get("customDomaDialect");
            localTransactionDataSource =
                    new LocalTransactionDataSource(SystemRepository.get("customDataSource"));
            localTransaction = localTransactionDataSource.getLocalTransaction(getJdbcLogger());
            localTransactionManager = new LocalTransactionManager(localTransaction);
        }

        // その他のフィールド、メソッドはDomaConfigを参考に実装すること
    }

Daoインタフェース
  .. code-block:: java

    @Dao
    public interface ProjectDao {
        // 省略
    }


業務アクションクラス
  ポイント
     * Daoの実装クラスを取得する際に、 :java:extdoc:`DomaDaoRepository#get(java.lang.Class,java.lang.Class)<nablarch.integration.doma.DomaDaoRepository.get(java.lang.Class,java.lang.Class)>` を使用し、第2引数に作成したConfigクラスを指定する。

  .. code-block:: java

    public HttpResponse create(final HttpRequest request, final ExecutionContext context) {
        final Project project = SessionUtil.delete(context, "project");

        CustomConfig.singleton()
                .getTransactionManager()
                .requiresNew(() ->
                        DomaDaoRepository.get(ProjectDao.class, CustomConfig.class).insert(project);

        return new HttpResponse("redirect://complete");
    }

  .. tip::

    Doma 2.44.0より作成するConfigへのSingletonConfigアノテーションの付与およびDaoアノテーションのconfig属性が非推奨になったため、Doma 2.44.0以前に案内していた内容から実装方法を変更している。  
    詳しくは、 :ref:`migration_doma2.44.0` を参照すること。

DomaとNablarchのデータベースアクセスを併用する
--------------------------------------------------
データベースアクセスにDomaを採用した場合でも、 :ref:`Nablarch提供のデータベースアクセス <database_management>` を使用したい場合がある。
例えば、 :ref:`メール送信ライブラリ <mail>` を使用する場合が該当する。(:ref:`メール送信要求 <mail-request>` で :ref:`database` を使用している。)

この問題を解決するため、Nablarchのデータベースアクセス処理が、Domaと同じトランザクション(データベース接続)を使用できる機能を提供している。

利用手順
  コンポーネント設定ファイルに以下の定義を追加する。
  これにより、Nablarchのデータベースアクセスが、自動的にDomaのトランザクション配下で実行されるようにある。
  
  * コンポーネント設定ファイルに :java:extdoc:`ConnectionFactoryFromDomaConnection <nablarch.integration.doma.ConnectionFactoryFromDomaConnection>` を定義する。
    コンポーネント名は、 ``connectionFactoryFromDoma`` とする。
  * Jakarta Batch用のDomaのトランザクションを制御するリスナーに、ConnectionFactoryFromDomaConnectionを設定する。

  .. code-block:: xml

    <!-- コンポーネント名は、connectionFactoryFromDomaとする -->
    <component name="connectionFactoryFromDoma"
        class="nablarch.integration.doma.ConnectionFactoryFromDomaConnection">
        
      <!-- プロパティに対する設定は省略 -->
      
    </component>
    
    <!-- 
    Jakarta Batchに準拠したバッチアプリケーションで使用する場合は、Domaのトランザクションを制御するリスナーに
    上記で定義したconnectionFactoryFromDomaを設定する。
     -->
    <component class="nablarch.integration.doma.batch.ee.listener.DomaTransactionItemWriteListener">
      <property name="connectionFactory" ref="connectionFactoryFromDoma" />
    </component>

    <component class="nablarch.integration.doma.batch.ee.listener.DomaTransactionStepListener">
      <property name="connectionFactory" ref="connectionFactoryFromDoma" />
    </component>

ロガーを切り替える
--------------------------------------------------
本アダプタではDomaが使うロガーの実装として、Nablarchのロガーを使用する :java:extdoc:`NablarchJdbcLogger<nablarch.integration.doma.NablarchJdbcLogger>` を提供している。
デフォルトでは :java:extdoc:`NablarchJdbcLogger<nablarch.integration.doma.NablarchJdbcLogger>` が使用されるが、他のものに差し替える場合はコンポーネント定義ファイルに設定する必要がある。

``org.seasar.doma.jdbc.UtilLoggingJdbcLogger`` を使用する場合の設定例を以下に示す。

ポイント
 * 定義するロガーは ``org.seasar.doma.jdbc.JdbcLogger`` の実装クラスとすること
 * ロガーのコンポーネント名は ``domaJdbcLogger`` とすること

.. code-block:: xml

  <component name="domaJdbcLogger" class="org.seasar.doma.jdbc.UtilLoggingJdbcLogger"  />

java.sql.Statementに関する設定を行う
--------------------------------------------------
フェッチサイズやクエリタイムアウトなど、 ``java.sql.Statement`` に関する項目をプロジェクト全体に設定したい場合がある。

その場合はコンポーネント設定ファイルに :java:extdoc:`DomaStatementProperties<nablarch.integration.doma.DomaStatementProperties>` を設定する。

設定できる項目には下記のものがある。

* 最大行数の制限値
* フェッチサイズ
* クエリタイムアウト（秒）
* バッチサイズ

設定例を以下に示す。

ポイント
 * コンポーネント名は ``domaStatementProperties`` とすること

.. code-block:: xml

  <component class="nablarch.integration.doma.DomaStatementProperties" name="domaStatementProperties">
    <!-- 最大行数の制限値を1000行に設定する -->
    <property name="maxRows" value="1000" />
    <!-- フェッチサイズを200行に設定する -->
    <property name="fetchSize" value="200" />
    <!-- クエリタイムアウトを30秒に設定する -->
    <property name="queryTimeout" value="30" />
    <!-- バッチサイズを400に設定する -->
    <property name="batchSize" value="400" />
  </component>

.. _`migration_doma2.44.0`:

Doma 2.44.0までの実装方法から移行する
--------------------------------------------------

`Doma 2.44.0より(外部サイト、英語) <https://github.com/domaframework/doma/releases/tag/2.44.0>`_ Daoアノテーションのconfig属性およびSingletonConfigアノテーションが非推奨となったことにより、NablarchでもAPIを追加し、案内していた内容から実装方法を変更している。

引き続きDaoアノテーションのconfig属性およびSingletonConfigアノテーションを使用した実装も動作するが、Domaの変更に合わせて実装方法を移行することを推奨する。

ここではDoma 2.44.0以前にNablarchで案内していた実装方法との対比を説明する。

なお、Doma 2.44.0以前に案内していた実装方法でも引き続き同じ動作を行う。

DomaConfigを使った基本的な実装をしている場合
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Daoアノテーションのconfig属性に :java:extdoc:`DomaConfig<nablarch.integration.doma.DomaConfig>` を使用した実装例を以下に示す。

.. code-block:: java

  // Daoの定義
  @Dao(config = DomaConfig.class)  /* config属性を指定 */
  public interface ProjectDao {
      // 省略
  }

  // Daoを使用する実装例
  @Transactional
  public HttpResponse create(final HttpRequest request, final ExecutionContext context) {
      final Project project = SessionUtil.delete(context, "project");

      DomaDaoRepository.get(ProjectDao.class).insert(project);

      return new HttpResponse("redirect://complete");
  }

これは以下の実装と等価となる。

.. code-block:: java

  // Daoの定義
  @Dao  /* config属性の指定を削除 */
  public interface ProjectDao {
      // 省略
  }

  // Daoを使用する実装例
  @Transactional
  public HttpResponse create(final HttpRequest request, final ExecutionContext context) {
      final Project project = SessionUtil.delete(context, "project");

      DomaDaoRepository.get(ProjectDao.class).insert(project);  /* 変更なし */

      return new HttpResponse("redirect://complete");
  }

Daoアノテーションのconfig属性を指定しないDaoを使用して :java:extdoc:`DomaDaoRepository#get<nablarch.integration.doma.DomaDaoRepository.get(java.lang.Class)>` を使ってDaoの実装クラスを取得した場合、 :java:extdoc:`DomaConfig<nablarch.integration.doma.DomaConfig>` を使用してDaoの実装クラスが構築される。

DomaTransactionNotSupportedConfigを使用して遅延ロードに対応している場合
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Jakarta Batchに準拠したバッチアプリケーションで遅延ロードに対応するため、 :java:extdoc:`DomaTransactionNotSupportedConfig<nablarch.integration.doma.DomaTransactionNotSupportedConfig>` を使用した実装例を以下に示す。

.. code-block:: java

    // Daoの定義
    @Dao(config = DomaTransactionNotSupportedConfig.class)  /* config属性を指定 */
    public interface ProjectDao {

        @Select(strategy = SelectType.RETURN)
        Stream<Project> search();
    }

    // Daoを使用する実装例
    @Dependent
    @Named
    public class ProjectReader extends AbstractItemReader {

        private Iterator<Project> iterator;

        private Stream<Project> stream;

        @Override
        public void open(Serializable checkpoint) throws Exception {
            /* DomaDaoRepository#getにはDaoのインターフェースのみを指定 */
            final ProjectDao dao = DomaDaoRepository.get(ProjectDao.class);
            stream = dao.search();
            iterator = stream.iterator();
        }

        // 省略
    }

これは以下の実装と等価となる。

.. code-block:: java

    // Daoの定義
    @Dao  /* config属性の指定を削除 */
    public interface ProjectDao {

        @Select(strategy = SelectType.RETURN)
        Stream<Project> search();
    }

    // Daoを使用する実装例
    @Dependent
    @Named
    public class ProjectReader extends AbstractItemReader {

        private Iterator<Project> iterator;

        private Stream<Project> stream;

        @Override
        public void open(Serializable checkpoint) throws Exception {
            /* DomaDaoRepository#getの第2引数にDomaTransactionNotSupportedConfig.classを指定 */
            final ProjectDao dao = DomaDaoRepository.get(ProjectDao.class, DomaTransactionNotSupportedConfig.class);
            stream = dao.search();
            iterator = stream.iterator();
        }

        // 省略
    }

Daoアノテーションにconfig属性を指定しないDaoを使用して :java:extdoc:`DomaDaoRepository#get(java.lang.Class,java.lang.Class)<nablarch.integration.doma.DomaDaoRepository.get(java.lang.Class,java.lang.Class)>` を呼び出した場合、第2引数に指定したConfigを使用してDaoの実装クラスが構築される。

独自にConfigクラスを作成している場合
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

複数のデータベースにアクセスする等の理由で、独自にConfigクラスを作成して実装する例を以下に示す。

.. code-block:: java

    // Configクラスの定義
    @SingletonConfig  /* SingletonConfigアノテーションを付与 */
    public final class CustomConfig implements Config {

        private CustomConfig() {  /* コンストラクタはprivate */
            // 省略
        }

        // 省略
    }

    // Daoの定義
    @Dao(config = CustomConfig.class)  /* config属性に作成したConfigクラスを指定 */
    public interface ProjectDao {
        // 省略
    }

    // Daoを使用する実装例
    public HttpResponse create(final HttpRequest request, final ExecutionContext context) {
        final Project project = SessionUtil.delete(context, "project");

        CustomConfig.singleton()
                .getTransactionManager()
                .requiresNew(() ->
                        /* DomaDaoRepository#getにはDaoのインターフェースのみを指定 */
                        DomaDaoRepository.get(ProjectDao.class);

        return new HttpResponse("redirect://complete");
    }

これは以下の実装と等価となる。

.. code-block:: java

    // Configクラスの定義
    /* SingletonConfigアノテーションを削除 */
    public final class CustomConfig implements Config {

        public CustomConfig() {  /* publicな引数なしのコンストラクタに変更 */
            // 省略
        }

        // 省略
    }

    // Daoの定義
    @Dao  /* config属性の指定を削除 */
    public interface ProjectDao {
        // 省略
    }

    // Daoを使用する実装例
    public HttpResponse create(final HttpRequest request, final ExecutionContext context) {
        final Project project = SessionUtil.delete(context, "project");

        CustomConfig.singleton()
                .getTransactionManager()
                .requiresNew(() ->
                        /* DomaDaoRepository#getの第2引数に作成したConfigのClassクラスを指定 */
                        DomaDaoRepository.get(ProjectDao.class, CustomConfig.class);

        return new HttpResponse("redirect://complete");
    }

Daoアノテーションにconfig属性を指定しないDaoを使用して :java:extdoc:`DomaDaoRepository#get(java.lang.Class,java.lang.Class)<nablarch.integration.doma.DomaDaoRepository.get(java.lang.Class,java.lang.Class)>` を呼び出した場合、第2引数に指定したConfigを使用してDaoの実装クラスが構築される。
