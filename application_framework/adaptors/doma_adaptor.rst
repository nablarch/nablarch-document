.. _doma_adaptor:

Domaアダプタ
==================================================

.. contents:: 目次
  :depth: 3
  :local:

`Doma(外部サイト) <http://doma.readthedocs.io/ja/stable/>`_ を使用したデータベースアクセスを行うためのアダプタを提供する。

データベースアクセスにDomaを使用することで以下のメリットが得られる。

* Nablarchと同じように、実行時に動的にSQL文を構築することができる。
* 2waySQLなので、NablarchのようにSQL文を書き換える必要がなく、SQLツール等でそのまま実行することができる。

また、本アダプタを使用することで、 :java:extdoc:`Transactional<nablarch.integration.doma.Transactional>` インターセプタで
指定したアクションのみトランザクション管理対象とすることができるため、
不要なトランザクション制御処理を削減でき、パフォーマンスの向上が期待できる。

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <!-- Domaアダプタ -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-doma-adaptor</artifactId>
  </dependency>

  <!-- Doma -->
  <dependency>
    <groupId>org.seasar.doma</groupId>
    <artifactId>doma</artifactId>
  </dependency>

Domaアダプタを使用するための設定を行う
--------------------------------------------------
本アダプタを使用するためには、プロジェクトで使用するRDBMSに合わせてDomaのダイアレクトやデータソースをコンポーネント定義ファイルに設定する必要がある。

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

ポイント
 * Daoアノテーションのconfig属性には :java:extdoc:`DomaConfig<nablarch.integration.doma.DomaConfig>` を指定する

.. code-block:: java

  @Dao(config = DomaConfig.class)
  public interface ProjectDao {
      // 省略
  }

データベースアクセス処理を実装する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
業務アクションのメソッドにデータベースアクセス処理を実装する。

ポイント
 * データベースアクセスを行うメソッドには :java:extdoc:`Transactional<nablarch.integration.doma.Transactional>` インターセプタを設定する
 * :java:extdoc:`DomaDaoRepository#get<nablarch.integration.doma.DomaDaoRepository.get(java.lang.Class)>` を使用してDaoの実装クラスをルックアップする

.. code-block:: java

    @Transactional
    public HttpResponse create(final HttpRequest request, final ExecutionContext context) {
        final Project project = SessionUtil.delete(context, "project");

        DomaDaoRepository.get(ProjectDao.class).insert(project);

        return new HttpResponse("redirect://complete");
    }

別トランザクションで実行する
--------------------------------------------------
:java:extdoc:`Transactional<nablarch.integration.doma.Transactional>` インターセプタによって開始されたトランザクションではなく、
別のトランザクションを使用してデータベースアクセスを行いたい場合がある。

その場合は、 :java:extdoc:`DomaConfig#getTransactionManager <nablarch.integration.doma.DomaConfig.getTransactionManager()>` で取得した
`TransactionManager` を使用して別トランザクションでの制御を行う。

実装例を以下に示す。

.. code-block:: java

  DomaConfig.singleton()
          .getTransactionManager()
          .requiresNew(() ->
                  DomaDaoRepository.get(ProjectDao.class).insert(project);


JSR352に準拠したバッチアプリケーションで使用する
----------------------------------------------------------------
JSR352に準拠したバッチアプリケーションでDomaを使用するために、
本アダプタでは以下のリスナーを提供している。

* :java:extdoc:`DomaTransactionStepListener<nablarch.integration.doma.batch.ee.listener.DomaTransactionStepListener>`
* :java:extdoc:`DomaTransactionItemWriteListener<nablarch.integration.doma.batch.ee.listener.DomaTransactionItemWriteListener>`

これらのリスナーをリスナーリストに定義することで、
JSR352に準拠したバッチアプリケーションでもDomaを使用したデータベースアクセスを行うことができる。

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

JSR352に準拠したバッチアプリケーションで遅延ロードを行う
---------------------------------------------------------
JSR352に準拠したバッチアプリケーションで大量データの読み込みを行う際に、遅延ロードを使用したい場合がある。

その場合は、Daoアノテーションのconfig属性に
:java:extdoc:`DomaTransactionNotSupportedConfig<nablarch.integration.doma.DomaTransactionNotSupportedConfig>` を指定する。

.. important::

  config属性に :java:extdoc:`DomaConfig<nablarch.integration.doma.DomaConfig>` を使用すると、
  :java:extdoc:`DomaTransactionItemWriteListener<nablarch.integration.doma.batch.ee.listener.DomaTransactionItemWriteListener>`
  によるトランザクションのコミットでストリームがクローズされるため、後続のレコードが読み込めなくなってしまう。

実装例を以下に示す。

Daoインタフェース
  ポイント
    * Daoアノテーションのconfig属性には、
      :java:extdoc:`DomaTransactionNotSupportedConfig<nablarch.integration.doma.DomaTransactionNotSupportedConfig>` を指定する。
    * 検索結果は :java:extdoc:`Stream<java.util.stream.Stream>` で取得する。

  .. code-block:: java

    @Dao(config = DomaTransactionNotSupportedConfig.class)
    public interface ProjectDao {

        @Select(strategy = SelectType.RETURN)
        Stream<Project> search();
    }

ItemReaderクラス
  ポイント
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

ETLで使用する
--------------------------------------------------
ETL使用時に、プロジェクトで追加したステップの中でDomaを使用したい場合がある。
その場合は、ジョブ名およびステップ名を指定したリスナーリストを定義して対応する。

設定例を以下に示す。

ジョブ定義ファイル
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

コンポーネント定義ファイル
  .. code-block:: xml

    <list name="sampleJob.sampleStep.stepListeners">
      <!-- その他のリスナーは省略 -->
      <component
          class="nablarch.integration.doma.batch.ee.listener.DomaTransactionStepListener" />
    </list>

    <list name="sampleJob.sampleStep.itemWriteListeners">
      <!-- その他のリスナーは省略 -->
      <component
          class="nablarch.integration.doma.batch.ee.listener.DomaTransactionItemWriteListener" />
    </list>
