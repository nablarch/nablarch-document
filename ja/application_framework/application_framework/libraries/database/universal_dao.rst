.. _universal_dao:

ユニバーサルDAO
=====================================================================

.. contents:: 目次
   :depth: 3
   :local:

ユニバーサルDAOでは、 `Jakarta Persistence (外部サイト、英語) <https://jakarta.ee/specifications/persistence/>`_
のアノテーションを使った簡易的なO/Rマッパーを提供する。

ユニバーサルDAOの内部では、 :ref:`database` を使用しているので、
ユニバーサルDAOを使用するには :ref:`database` の設定が必要となる。

.. tip::
 ユニバーサルDAOは、簡易的なO/Rマッパーと位置付けていて、
 すべてのデータベースアクセスをユニバーサルDAOで実現しようとは考えていない。
 ユニバーサルDAOで実現できない場合は、素直に :ref:`database` を使うこと。

 例えば、ユニバーサルDAOでは、主キー以外の条件を指定した更新/削除は行えないので、
 :ref:`database` を使用する必要がある。

.. tip::

  ユニバーサルDAOは、共通項目(全てのテーブルに定義する登録ユーザや更新ユーザ等)に対する値の自動設定機能は提供しない。
  共通項目に対する値を自動設定したい場合は、 :ref:`doma_adaptor` を適用し、Domaのエンティティリスナー機能を使用すれば良い。

  どうしてもユニバーサルDAOを使用したい場合は、ユニバーサルDAOの機能を使用する前にアプリケーションで明示的に共通項目を設定すること。

.. _universal_dao-spec:

機能概要
---------------------------------------------------------------------

.. _universal_dao-execute_crud_sql:

SQLを書かなくても単純なCRUDができる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Jakarta PersistenceアノテーションをEntityに付けるだけで、SQLを書かなくても、以下の単純なCRUDができる。
SQL文は、Jakarta Persistenceアノテーションを元に実行時に構築する。

* 登録/一括登録
* 主キーを指定した更新/一括更新
* 主キーを指定した削除/一括削除
* 主キーを指定した検索

Entityに使用できるJakarta Persistenceアノテーションについては、 :ref:`universal_dao_jpa_annotations` を参照。


.. tip::
   ユニバーサルDAOの上記CRUD機能では、\ ``@Table``\ アノテーションを使ってスキーマを指定できる\
   （ :ref:`universal_dao_jpa_annotations` を参照）。
   ただし、 :ref:`database` の :ref:`database-replace_schema` 機能は、ユニバーサルDAOの上記CRUD機能では使用できない。\
   環境毎にスキーマを切り替える用途には、ユニバーサルDAOではなく :ref:`database` を使用すること。
   
.. _universal_dao-bean_mapping:

検索結果をBeanにマッピングできる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
検索では、 :ref:`database` と同様に、SQLファイルを作成し、SQL IDを指定した検索ができる。
さらに、ユニバーサルDAOでは、検索結果をBean（Entity、Form、DTO）にマッピングして取得できる。
Beanのプロパティ名とSELECT句の名前が一致する項目をマッピングする。

Beanに使用できるデータタイプについては、 :ref:`universal_dao_bean_data_types` を参照。

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-dao</artifactId>
  </dependency>

使用方法
---------------------------------------------------------------------

.. important::
 ユニバーサルDAOの基本的な使い方は、 :java:extdoc:`nablarch.common.dao.UniversalDao` を参照。

ユニバーサルDAOを使うための設定を行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ユニバーサルDAOを使うためには、 :ref:`database` の設定に加えて、
:java:extdoc:`BasicDaoContextFactory <nablarch.common.dao.BasicDaoContextFactory>` の設定をコンポーネント定義に追加する。

.. code-block:: xml

 <!-- コンポーネント名は"daoContextFactory"で設定する。 -->
 <component name="daoContextFactory" class="nablarch.common.dao.BasicDaoContextFactory" />

.. _universal_dao-sql_file:

任意のSQL(SQLファイル)で検索する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
任意のSQLで検索したい場合は、データベースアクセスの :ref:`database-use_sql_file` と同様に、
SQLファイルを作成し、SQL IDを指定して検索する。

.. code-block:: java

 UniversalDao.findAllBySqlFile(User.class, "FIND_BY_NAME");

SQLファイルは、検索結果をマッピングするBeanから導出する。
上の例のUser.classがsample.entity.Userの場合、
SQLファイルのパスは、クラスパス配下のsample/entity/User.sqlとなる。

SQL IDに「#」が含まれると、「SQLファイルのパス#SQL ID」と解釈する。
下の例では、SQLファイルのパスがクラスパス配下のsample/entity/Member.sql、
SQL IDがFIND_BY_NAMEとなる。

.. code-block:: java

 UniversalDao.findAllBySqlFile(GoldUser.class, "sample.entity.Member#FIND_BY_NAME");

.. tip::
 「#」を含めた指定は、機能単位（Actionハンドラ単位）にSQLを集約したい場合などに使用できる。
 ただし、指定が煩雑になるデメリットがあるため、基本は「#」を付けない指定を使用すること。

.. _universal_dao-join:

テーブルをJOINした検索結果を取得する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
一覧検索などで、複数のテーブルをJOINした結果を取得したい場合がある。
このような場合は、非効率なため、JOIN対象のデータを個別に検索せずに、
**1回で検索できるSQL** と **JOINした結果をマッピングするBean** を作成すること。

.. _universal_dao-lazy_load:

検索結果を遅延ロードする
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
大量の検索結果を扱う処理では、メモリが足らなくなるため、検索結果をすべてメモリに展開できない。
以下のようなケースがある。

* ウェブで大量データをダウンロードする
* バッチで大量データを処理する

そのような場合は、ユニバーサルDAOの遅延ロードを使用する。
遅延ロードを使用すると、ユニバーサルDAOとしては1件ずつロードするが、
JDBCのフェッチサイズによってメモリの使用量が変わる。
フェッチサイズの詳細は、データベースベンダー提供のマニュアルを参照。

遅延ロードは、検索時に、 :java:extdoc:`UniversalDao#defer <nablarch.common.dao.UniversalDao.defer()>` メソッドを先に呼び出すだけで使用できる。
遅延ロードでは、内部でサーバサイドカーソルを使用しているので、
:java:extdoc:`DeferredEntityList#close <nablarch.common.dao.DeferredEntityList.close()>` メソッドを呼び出す必要がある。

.. code-block:: java

 // try-with-resourcesを使ったclose呼び出し。
 // DeferredEntityListはダウンキャストして取得する。
 try (DeferredEntityList<User> users
         = (DeferredEntityList<User>) UniversalDao.defer()
                                         .findAllBySqlFile(User.class, "FIND_BY_NAME")) {
     for (User user : users) {
         // userを使った処理
     }
 }

.. important::
   使用するRDBMSによっては、カーソルオープン中にトランザクション制御が行われるとカーソルがクローズされる。
   これにより、遅延ロードを使用した大量データの処理中にトランザクション制御を行った場合、クローズ済みのカーソルを参照し、エラーとなる可能性があるため注意すること。
   データベースベンダ提供のマニュアルに沿ってカーソルの挙動を調整するか、大量データを扱わないよう :ref:`ページング<universal_dao-paging>` などで回避すること。

.. _universal_dao-search_with_condition:

条件を指定して検索する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
検索画面のように、条件を指定した検索をユニバーサルDAOでも提供している。

.. code-block:: java

 // 検索条件を取得する
 ProjectSearchForm condition = context.getRequestScopedVar("form");

 // 条件を指定して検索する
 List<Project> projects = UniversalDao.findAllBySqlFile(
     Project.class, "SEARCH_PROJECT", condition);

.. important::
  検索条件は、Entityではなく検索条件を持つ専用のBeanを指定する。
  ただし、1つのテーブルのみへのアクセスの場合は、Entityを指定しても良い。


型を変換する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ユニバーサルDAOでは、 :ref:`@Temporal <universal_dao_jpa_temporal>` を使用して、 ``java.util.Date`` 及び ``java.util.Calendar`` 型の値をデータベースにマッピングする方法を指定できる。
他の型については、任意のマッピングは不可能であるため、Entityのプロパティは、データベースの型及び使用するJDBCドライバの仕様に応じて定義すること。

また、ユニバーサルDAOは、自動生成したSQLをDBに送信する場合はJakarta Persistenceアノテーションの情報を使用するが、任意のSQLをDBに送信する場合はJakarta Persistenceアノテーションの情報は使用しない。
そのため、型変換については、以下のようになる。

:ref:`Entityから自動的に生成したSQLを実行する場合 <universal_dao-execute_crud_sql>`
  データベースへの出力時
    * :ref:`@Temporal <universal_dao_jpa_temporal>` が設定されているプロパティについては、@Temporalに指定された型へ変換する。
    * 上記以外については、:ref:`database` に処理を委譲して変換する。

  データベースから取得時
    * :ref:`@Temporal <universal_dao_jpa_temporal>` が設定されているプロパティについては、@Temporalに指定された型から変換する。
    * 上記以外はEntityの情報を元に、値が変換される。

:ref:`任意のSQLで検索する場合 <universal_dao-sql_file>`
  データベースへの出力時
    * :ref:`database` に処理を委譲して変換する。

  データベースから取得時
    * Entityから自動的に生成したSQLを実行する場合と同様の処理を行う。


.. important::
  データベースの型とプロパティの型が不一致の場合、実行時に型変換エラーが発生する場合がある。
  また、SQL実行時に暗黙的型変換が行われ、性能劣化(indexが使用されないことに起因する)となる可能性がある。

  データベースとJavaのデータタイプのマッピングについては、使用するプロダクトに依存するため、
  JDBCドライバのマニュアルを参照すること。

  例えば、DBがdate型の場合には、多くのデータベースではプロパティの型は :java:extdoc:`java.sql.Date` となる。
  また、DBが数値型(integerやbigint、number)などの場合は、プロパティの型は
  `int` (:java:extdoc:`java.lang.Integer`) や `long` (:java:extdoc:`java.lang.Long`) となる。


.. _universal_dao-paging:

ページングを行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ユニバーサルDAOの検索は、ページングをサポートしている。
ページングは、検索時に、 :java:extdoc:`UniversalDao#per <nablarch.common.dao.UniversalDao.per(long)>` メソッド、 :java:extdoc:`UniversalDao#page <nablarch.common.dao.UniversalDao.page(long)>` メソッドを先に呼び出すだけで使用できる。

.. code-block:: java

 EntityList<User> users = UniversalDao.per(3).page(1)
                             .findAllBySqlFile(User.class, "FIND_ALL_USERS");

ページングの画面表示に必要な検索結果件数といった情報は、 :java:extdoc:`Pagination <nablarch.common.dao.Pagination>` が保持している。
:java:extdoc:`Pagination <nablarch.common.dao.Pagination>` は、 :java:extdoc:`EntityList <nablarch.common.dao.EntityList>` から取得できる。

.. code-block:: java

 Pagination pagination = users.getPagination();

.. tip::
  ページング用の検索処理は、 :ref:`データベースアクセス(JDBCラッパー)の範囲指定検索機能 <database-paging>` を使用して行う。

.. tip::
  ページングでは、実際の範囲指定レコードの取得処理の前に、件数取得SQLが発行される。
  件数取得SQLに起因して性能劣化が発生した場合等、必要に応じて :ref:`universal_dao-customize_sql_for_counting` を参考にして件数取得SQLを変更する。

.. _universal_dao-generate_surrogate_key:

サロゲートキーを採番する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. toctree::
  :maxdepth: 1
  :hidden:

  generator

サロゲートキーを採番する場合は、以下のアノテーションを使用する。

* :ref:`@GeneratedValue <universal_dao_jpa_generated_value>`
* :ref:`@SequenceGenerator <universal_dao_jpa_sequence_generator>`
* :ref:`@TableGenerator <universal_dao_jpa_table_generator>`

ユニバーサルDAOでは、 :java:extdoc:`jakarta.persistence.GenerationType` のすべてのストラテジをサポートしている。

GenerationType.AUTO
 \

 .. code-block:: java

  @Id
  @Column(name = "USER_ID", length = 15)
  @GeneratedValue(strategy = GenerationType.AUTO)
  public Long getId() {
      return id;
  }

 - データベース機能に設定された :java:extdoc:`Dialect <nablarch.core.db.dialect.Dialect>` を元に採番方法を選択する。
   優先順位は、IDENTITY→SEQUENCE→TABLEの順となる。
 - SEQUENCEが選択された場合、シーケンスオブジェクト名は"<テーブル名>_<採番するカラム名>"となる。
 - シーケンスオブジェクト名を指定したい場合は、 :ref:`@SequenceGenerator <universal_dao_jpa_sequence_generator>` で指定する。

GenerationType.IDENTITY
 \

 .. code-block:: java

  @Id
  @Column(name = "USER_ID", length = 15)
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  public Long getId() {
      return id;
  }

GenerationType.SEQUENCE
 \

 .. code-block:: java

  @Id
  @Column(name = "USER_ID", length = 15)
  @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "seq")
  @SequenceGenerator(name = "seq", sequenceName = "USER_ID_SEQ")
  public Long getId() {
      return id;
  }

 - シーケンスオブジェクトの名前は :ref:`@SequenceGenerator <universal_dao_jpa_sequence_generator>` で指定する。
 - sequenceName属性を省略した場合、"<テーブル名>_<採番するカラム名>"となる。

GenerationType.TABLE
 \

 .. code-block:: java

  @Id
  @Column(name = "USER_ID", length = 15)
  @GeneratedValue(strategy = GenerationType.TABLE, generator = "table")
  @TableGenerator(name = "table", pkColumnValue = "USER_ID")
  public Long getId() {
      return id;
  }

 - レコードを識別する値は :ref:`@TableGenerator <universal_dao_jpa_table_generator>` で指定する。
 - pkColumnValue属性を省略した場合、"<テーブル名>_<採番するカラム名>"となる。

.. tip::

  シーケンス及びテーブルを使用したサロゲートキーの採番処理は、 :ref:`generator` を使用して行う。
  設定値(テーブルを使用した場合のテーブル名やカラム名の設定など)は、リンク先を参照すること。

.. _universal_dao-batch_execute:

バッチ実行(一括登録、更新、削除)を行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ユニバーサルDAOでは、大量データの一括登録や更新、削除時にバッチ実行ができる。
バッチ実行することで、アプリケーション稼働サーバとデータベースサーバとのラウンドトリップ回数を削減でき、パフォーマンスの向上が期待できる。

バッチ実行は以下のメソッドを使用する。

* :java:extdoc:`batchInsert <nablarch.common.dao.UniversalDao.batchInsert(java.util.List)>`
* :java:extdoc:`batchUpdate <nablarch.common.dao.UniversalDao.batchUpdate(java.util.List)>`
* :java:extdoc:`batchDelete <nablarch.common.dao.UniversalDao.batchDelete(java.util.List)>`

.. important::

  `batchUpdate` を使用した、一括更新処理では排他制御処理を行わない。
  もし、更新対象のEntityとデータベースのバージョンが不一致だった場合、そのレコードの更新は行われずに処理が正常終了する。

  排他制御が必要となる更新処理では、一括更新ではなく1レコード毎の更新処理を呼び出すこと。

.. _`universal_dao_jpa_optimistic_lock`:

楽観的ロックを行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ユニバーサルDAOでは、 :ref:`@Version <universal_dao_jpa_version>`
が付いているEntityを更新した場合、自動で楽観的ロックを行う。
楽観的ロックで排他エラーが発生した場合は、 :java:extdoc:`jakarta.persistence.OptimisticLockException` を送出する。

.. important::
 :ref:`@Version <universal_dao_jpa_version>` は数値型のプロパティのみに指定できる。
 文字列型のプロパティだと正しく動作しない。

排他エラー時の画面遷移は、 :java:extdoc:`OnError <nablarch.fw.web.interceptor.OnError>` を使用して行う。

.. code-block:: java

 // type属性に対象とする例外、path属性に遷移先のパスを指定する。
 @OnError(type = OptimisticLockException.class,
          path = "/WEB-INF/view/common/errorPages/userError.jsp")
 public HttpResponse update(HttpRequest request, ExecutionContext context) {

     UniversalDao.update(user); // 前後の処理は省略。

 }

.. important::
  :ref:`universal_dao-batch_execute` に記載があるように、
  一括更新処理(`batchUpdate`)では楽観的ロックは使用できないので注意すること。

.. _`universal_dao_jpa_pessimistic_lock`:

悲観的ロックを行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ユニバーサルDAOでは、悲観的ロックの機能を特に提供していない。

悲観的ロックは、データベースの行ロック（select for update）を使用することで行う。
行ロック（select for update）を記載したSQLは、
:java:extdoc:`UniversalDao#findBySqlFile <nablarch.common.dao.UniversalDao.findBySqlFile(java.lang.Class,java.lang.String,java.lang.Object)>` メソッドを使って実行する。

排他制御の考え方
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
排他制御に使用するバージョンカラムをどのテーブルに定義するかは業務的な観点により決める必要がある。

バージョン番号を持つテーブルは、排他制御を行う単位ごとに定義し、競合が許容される最大の単位で定義する。
たとえば、「ユーザ」という大きな単位でロックすることが業務的に許容されるならば、ユーザテーブルにバージョン番号を定義する。
ただし、単位を大きくすると、競合する可能性が高くなり、更新失敗(楽観的ロックの場合)や処理遅延(悲観的ロックの場合)を招く点に注意すること。


データサイズの大きいバイナリデータを登録（更新）する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
OracleのBLOBのように、データサイズの大きいバイナリデータを登録（更新）したい場合がある。
ユニバーサルDAOだと、データをすべてメモリに展開しないと登録（更新）できないため、
データベースが提供する機能を使ってファイルなどから直接登録（更新）すること。

詳細は、 :ref:`database-binary_column` を参照。

データサイズの大きいテキストデータを登録（更新）する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
OracleのCLOBのように、データサイズの大きいテキストデータを登録（更新）したい場合がある。
ユニバーサルDAOだと、データをすべてメモリに展開しないと登録（更新）できないため、
データベースが提供する機能を使ってファイルなどから直接登録（更新）すること。

詳細は、 :ref:`database-clob_column` を参照。

.. _universal_dao-transaction:

現在のトランザクションとは異なるトランザクションで実行する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`database` の :ref:`database-new_transaction` と同じことを、ユニバーサルDAOで行う方法を説明する。

個別トランザクションを使用するには、以下の手順が必要となる。

#. コンポーネント設定ファイルに :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` を定義する。
#. :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` を使用して、新たなトランザクションでユニバーサルDAOを実行する。

以下に使用例を示す。

コンポーネント設定ファイル
  コンポーネント設定ファイルに :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` を定義する。

  * :java:extdoc:`connectionFactory <nablarch.core.db.transaction.SimpleDbTransactionManager.setConnectionFactory(nablarch.core.db.connection.ConnectionFactory)>`
    プロパティに :java:extdoc:`ConnectionFactory <nablarch.core.db.connection.ConnectionFactory>` 実装クラスを設定する。
    :java:extdoc:`ConnectionFactory <nablarch.core.db.connection.ConnectionFactory>` 実装クラスの詳細は、 :ref:`database-connect` を参照。

  * :java:extdoc:`transactionFactory <nablarch.core.db.transaction.SimpleDbTransactionManager.setTransactionFactory(nablarch.core.transaction.TransactionFactory)>`
    プロパティに :java:extdoc:`TransactionFactory <nablarch.core.transaction.TransactionFactory>` 実装クラスを設定する。
    :java:extdoc:`TransactionFactory <nablarch.core.transaction.TransactionFactory>` 実装クラスの詳細は、 :ref:`transaction-database` を参照。

  .. code-block:: xml

    <component name="find-persons-transaction"
        class="nablarch.core.db.transaction.SimpleDbTransactionManager">

      <!-- connectionFactoryプロパティにConnectionFactory実装クラスを設定する -->
      <property name="connectionFactory" ref="connectionFactory" />

      <!-- transactionFactoryプロパティにTransactionFactory実装クラスを設定する -->
      <property name="transactionFactory" ref="transactionFactory" />

      <!-- トランザクションを識別するための名前を設定する -->
      <property name="dbTransactionName" value="update-login-failed-count-transaction" />

    </component>

実装例
  コンポーネント設定ファイルに設定した  :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` を使って、ユニバーサルDAOを実行する。
  なお、 :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` を直接使うのではなくトランザクションを制御する、
  :java:extdoc:`UniversalDao.Transaction <nablarch.common.dao.UniversalDao.Transaction>` を使用すること。

  まず、 :java:extdoc:`UniversalDao.Transaction <nablarch.common.dao.UniversalDao.Transaction>` を継承したクラスを作成する。

  .. code-block:: java

    private static final class FindPersonsTransaction extends UniversalDao.Transaction {

        // 結果を受け取る入れ物を用意する。
        private EntityList<Person> persons;

        FindPersonsTransaction() {
            // SimpleDbTransactionManagerをsuper()に指定する。
            // コンポーネント定義で指定した名前、またはSimpleDbTransactionManagerオブジェクトを指定できる。
            // この例では、コンポーネント定義で指定した名前を指定している。
            super("find-persons-transaction");
        }

        // このメソッドが自動的に別のトランザクションで実行される。
        // 正常に処理が終了した場合はトランザクションがコミットされ、
        // 例外やエラーが送出された場合には、トランザクションがロールバックされる。
        @Override
        protected void execute() {
            // executeメソッドにUniversalDaoを使った処理を実装する。
            persons = UniversalDao.findAllBySqlFile(Person.class, "FIND_PERSONS");
        }

        // 結果を返すgetterを用意する。
        public EntityList<Person> getPersons() {
            return persons;
        }
    }

  そして、 :java:extdoc:`UniversalDao.Transaction <nablarch.common.dao.UniversalDao.Transaction>` を継承したクラスを呼び出す。

  .. code-block:: java

    // 生成すると別のトランザクションで実行される。
    FindPersonsTransaction findPersonsTransaction = new FindPersonsTransaction();

    // 結果を取得する。
    EntityList<Person> persons = findPersonsTransaction.getPersons();


拡張例
---------------------------------------------------------------------

DatabaseMetaDataから情報を取得できない場合に対応する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
データベースによっては、シノニムを使用している場合や権限の問題で、
:java:extdoc:`java.sql.DatabaseMetaData` から主キー情報を取得できない場合がある。
主キー情報を取得できなくなると、主キーを指定した検索が正しく動作しない。
そのような場合は、 :java:extdoc:`DatabaseMetaDataExtractor <nablarch.common.dao.DatabaseMetaDataExtractor>` を継承したクラスを作成して対応する。
主キー情報をどのように取得するかはデータベース依存のため、製品のマニュアルを参照すること。

作成したクラスを使用するには、設定が必要となる。

.. code-block:: xml

 <!--
 sample.dao.CustomDatabaseMetaDataExtractorを作成した場合の設定例
 コンポーネント名は"databaseMetaDataExtractor"で設定する。
 -->
 <component name="databaseMetaDataExtractor" class="sample.dao.CustomDatabaseMetaDataExtractor" />

.. _universal_dao-customize_sql_for_counting:

ページング処理の件数取得用SQLを変更する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`ページング <universal_dao-paging>` 処理では、実際の範囲指定レコードの取得処理の前に、件数取得SQLが発行される。
件数取得SQLは、デフォルトでは元のSQLを ``SELECT COUNT(*) FROM`` で包んだSQLとなる。
元のSQLが ``ORDER BY`` 句を含むなど処理負荷が大きいSQLで、負荷軽減のため ``ORDER BY`` 句を外したいといった場合には、
使用しているダイアレクトをカスタマイズし、件数取得SQLを変更することで対応する。

.. important::
   件数取得SQLは、元のSQLと同一の検索条件を持つ必要がある。件数取得SQLを用意する場合は、両者の検索条件に差分が発生しないよう注意すること。

件数取得SQLを変更する場合は、プロジェクトで使用しているダイアレクトを継承した上で、 :java:extdoc:`Dialect#convertCountSql(String, Object, StatementFactory) <nablarch.core.db.dialect.Dialect.convertCountSql(java.lang.String,java.lang.Object,nablarch.core.db.statement.StatementFactory)>` の実装を変更する。

実装例
   以下に :java:extdoc:`nablarch.core.db.dialect.H2Dialect` をカスタマイズする例を示す。
   この例では、元のSQLと件数取得SQLのマッピングをコンポーネントに設定し、件数取得SQLを変更している。

   .. tip::
      プロジェクトごとに適切なマッピングルールを検討すること。
   
   .. code-block:: java
   
      public class CustomH2Dialect extends H2Dialect {
      
          /**
           * 件数取得SQLのマッピング
           */
          private Map<String, String> sqlMap;
      
          /**
           * {@inheritDoc}
           *
           * 件数取得SQLのマッピング内に{@code sqlId}に対応するSQLIDが存在すれば、
           * それを件数取得SQLとして返却する。
           */
          @Override
          public String convertCountSql(String sqlId, Object params, StatementFactory statementFactory) {
      
              if (sqlMap.containsKey(sqlId)) {
                  return statementFactory.getVariableConditionSqlBySqlId(sqlMap.get(sqlId), params);
              }
      
              return convertCountSql(statementFactory.getVariableConditionSqlBySqlId(sqlId, params));
          }
      
          /**
           * 件数取得SQLのマッピングを設定する。
           *
           * @param sqlMap 件数取得SQLのマッピング
           */
          public void setSqlMap(Map<String, String> sqlMap){
              this.sqlMap = sqlMap;
          }
      }

   カスタマイズしたダイアレクトは、コンポーネント設定ファイルで設定する必要がある。
   以下に、カスタマイズしたダイアレクトをコンポーネント設定ファイルに設定する例を示す。
   この例では、件数取得SQLのマッピングを ``<property>`` 要素で設定している。
   
   .. code-block:: xml
                   
      <component name="dialect" class="com.nablarch.example.app.db.dialect.CustomH2Dialect">
        <property name="sqlMap">
          <map>
            <entry key="com.nablarch.example.app.entity.Project#SEARCH_PROJECT"
                   value="com.nablarch.example.app.entity.Project#SEARCH_PROJECT_FORCOUNT"/>
          </map>
        </property>
      </component>

.. _`universal_dao_jpa_annotations`:

Entityに使用できるJakarta Persistenceアノテーション
---------------------------------------------------------------------
Entityに使用できるJakarta Persistenceアノテーションは以下のとおり。

* クラスに設定するアノテーション

  * :ref:`@Entity <universal_dao_jpa_entity>`
  * :ref:`@Table <universal_dao_jpa_table>`
  * :ref:`@Access <universal_dao_jpa_access>`
* getterまたはフィールドに設定するアノテーション

  * :ref:`@Column <universal_dao_jpa_column>`
  * :ref:`@Id <universal_dao_jpa_id>`
  * :ref:`@Version <universal_dao_jpa_version>`
  * :ref:`@Temporal <universal_dao_jpa_temporal>`
  * :ref:`@GeneratedValue <universal_dao_jpa_generated_value>`
  * :ref:`@SequenceGenerator <universal_dao_jpa_sequence_generator>`
  * :ref:`@TableGenerator <universal_dao_jpa_table_generator>`

.. important::
 ここに記載のないアノテーション及び属性を使用しても機能しない。

フィールドに設定する場合には@Accessで明示的に指定すること。@Accessで明示的に指定した場合のみ、フィールドのアノテーションを参照する。

フィールドにアノテーションを設定する場合でも、UniversalDaoでは値の取得と設定はプロパティを通して行われるため、getterとsetterは必ず作成すること。

フィールドとプロパティは名前で紐づいているため、名前が異なるとフィールドのアノテーションをプロパティで参照できなくなる。
そのためフィールド名と、プロパティ名(get〇〇,set〇〇の〇〇の部分)を必ず同じものにすること。

.. tip::
 例えば、Lombokのようなボイラープレートコードを生成するライブラリを使用する場合、
 アノテーションをフィールドに設定することでgetterを自分で作成する必要がなくなり、
 ライブラリの利点をより活かすことができる。

.. _`universal_dao_jpa_entity`:

*jakarta.persistence.Entity*
 データベースのテーブルに対応したEntityクラスに設定するアノテーション。

 本アノテーションを設定した場合、クラス名からテーブル名が導出される。
 クラス名(パスカルケース)をスネークケース(全て大文字)へ変換した値がテーブル名となる。

 .. code-block:: bash

  Bookクラス        -> BOOK
  BookAuthorクラス  -> BOOK_AUTHOR

 .. tip::
  クラス名からテーブル名を導出できない場合は、
  後述の :ref:`@Table <universal_dao_jpa_table>` を用いて明示的にテーブル名を指定すること。

.. _`universal_dao_jpa_table`:

*jakarta.persistence.Table*
 テーブル名を指定するために使用するアノテーション。

 name属性に値が指定されている場合、その値がテーブル名として使用される。
 schema属性に値が指定されている場合、指定されたスキーマ名を修飾子として指定してテーブルにアクセスを行う。
 例えば、schema属性にworkと指定した場合で、テーブル名がusers_workの場合、work.users_workにアクセスを行う。

.. _`universal_dao_jpa_access`:

*jakarta.persistence.Access*
 アノテーションを設定する場所を指定するために使用するアノテーション。

 明示的にフィールドに指定した場合のみ、フィールドのアノテーションを参照する。

.. _`universal_dao_jpa_column`:

*jakarta.persistence.Column*
 カラム名を指定するために使用するアノテーション。

 name属性に値が指定されている場合、その値がカラム名として使用される。

 .. tip::
  本アノテーションが設定されていない場合は、プロパティ名からカラム名が導出される。
  導出方法は、テーブル名の導出方法と同じである。
  詳細は、 :ref:`@Entity <universal_dao_jpa_entity>` を参照。

.. _`universal_dao_jpa_id`:

*jakarta.persistence.Id*
 主キーに設定するアノテーション。

 複合主キーの場合には、複数のgettterもしくはフィールドに本アノテーションを設定する。

.. _`universal_dao_jpa_version`:

*jakarta.persistence.Version*
 排他制御で使用するバージョンカラムに設定するアノテーション。

 本アノテーションは数値型のプロパティのみに指定できる。
 文字列型のプロパティだと正しく動作しない。

 本アノテーションが設定されている場合、
 更新処理時にバージョンカラムが条件に自動的に追加され楽観ロックが行われる。

 .. tip::
  本アノテーションは、Entity内に1つだけ指定可能。

.. _`universal_dao_jpa_temporal`:

*jakarta.persistence.Temporal*
 *java.util.Date* 及び *java.util.Calendar* 型の値を
 データベースにマッピングする方法を指定するアノテーション。

 value属性に指定されたデータベース型に、Javaオブジェクトの値を変換してデータベースに登録する。

.. _`universal_dao_jpa_generated_value`:

*jakarta.persistence.GeneratedValue*
 自動採番された値を登録することを示すアノテーション。

 strategy属性に採番方法を設定する。
 AUTOを設定した場合、以下のルールにて採番方法が選択される。

 * generator属性に対応するGenerator設定がある場合、そのGeneratorを使用して採番処理を行う。
 * generatorが未設定な場合や、対応するGenerator設定がない場合は、
   データベース機能に設定された :java:extdoc:`Dialect <nablarch.core.db.dialect.Dialect>` を元に採番方法を選択する。
   優先順位は、IDENTITY→SEQUENCE→TABLEの順となる。

 generator属性に任意の名前を設定する。

 .. tip::
  :ref:`@GeneratedValue <universal_dao_jpa_generated_value>` を使用して、
  シーケンス採番のシーケンスオブジェクト名や
  テーブル採番のレコードを識別する値を取得できない場合は、
  それぞれの値をテーブル名と自動採番するカラム名から導出する。

  .. code-block:: bash

   テーブル名「USER」、採番するカラム名「ID」  -> USER_ID

.. _`universal_dao_jpa_sequence_generator`:

*jakarta.persistence.SequenceGenerator*
 シーケンス採番を使用する場合に設定するアノテーション。

 name属性には、:ref:`@GeneratedValue <universal_dao_jpa_generated_value>`
 のgenerator属性と同じ値を設定する。

 sequenceName属性には、データベース上に作成されているシーケンスオブジェクト名を設定する。

 .. tip::
  シーケンス採番は、採番機能を使用して行う。
  このため、 :ref:`採番用の設定 <generator_dao_setting>` を別途行う必要がある。

.. _`universal_dao_jpa_table_generator`:

*jakarta.persistence.TableGenerator*
 テーブル採番を使用する場合に設定するアノテーション。

 name属性には、 :ref:`@GeneratedValue <universal_dao_jpa_generated_value>`
 のgenerator属性と同じ値を設定する。

 pkColumnValue属性には、採番テーブルのレコードを識別するための値を設定する。

 .. tip::
  テーブル採番は、採番機能を使用して行う。
  このため、 :ref:`採番用の設定 <generator_dao_setting>` を別途行う必要がある。

.. _`universal_dao_bean_data_types`:

Beanに使用できるデータタイプ
---------------------------------------------------------------------
検索結果をマッピングするBeanに使用できるデータタイプは以下のとおり。

.. important::
 ここに記載のないデータタイプに対して、検索結果をマッピングできない(実行時例外となる)。

*java.lang.String*
 \

*java.lang.Short*
 プリミティブ型も指定可能。プリミティブ型の場合、 ``null`` は ``0`` として扱う。

*java.lang.Integer*
 プリミティブ型も指定可能。プリミティブ型の場合、 ``null`` は ``0`` として扱う。

*java.lang.Long*
 プリミティブ型も指定可能。プリミティブ型の場合、 ``null`` は ``0`` として扱う。

*java.math.BigDecimal*
 \

*java.lang.Boolean*
 プリミティブ型も指定可能。プリミティブ型の場合、 ``null`` は ``false`` として扱う。
 ラッパー型(Boolean)の場合は、リードメソッド名はgetから開始される必要がある。
 プリミティブ型の場合は、リードメソッド名がisで開始されていても良い。

*java.util.Date*
 Jakarta Persistenceの :ref:`@Temporal <universal_dao_jpa_temporal>`
 でデータベース上のデータ型を指定する必要がある。


*java.sql.Date*
 \

*java.sql.Timestamp*
 \

*java.time.LocalDate*
 \

*java.time.LocalDateTime*
 \

*byte[]*
  BLOBなどのように非常に大きいサイズのデータ型の値は、
  本機能を用いてデータをヒープ上に展開しないように注意すること。
  非常に大きいサイズのバイナリデータを扱う場合には、
  データベースアクセスを直接使用し、Stream経由でデータを参照すること。

  詳細は :ref:`database-binary_column` を参照。
