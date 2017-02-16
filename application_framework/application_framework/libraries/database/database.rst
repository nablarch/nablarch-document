.. _database:

データベースアクセス(JDBCラッパー)
=========================================

.. contents:: 目次
  :depth: 3
  :local:

JDBCを使用してデータベースに対してSQL文を実行する機能を提供する。

.. tip::

  :ref:`database_management` で説明したように、SQLの実行に関しては :ref:`universal_dao` を使用することを推奨する。

  なお、:ref:`universal_dao` 内部では、この機能のAPIを使用してデータベースアクセスを行っているため、
  この機能を使用するための設定は必ず必要になる。

.. important::

  この機能は、JDBC 3.0に依存しているため、使用するJDBCドライバがJDBC 3.0以上を実装している必要がある。


機能概要
----------------------

.. _database-dialect:

データベースの方言を意識することなく利用できる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
使用するデータベース製品に対応した :java:extdoc:`Dialect <nablarch.core.db.dialect.Dialect>` を設定することで、
製品ごとの方言を意識せずにアプリケーションを実装できる。

:java:extdoc:`Dialect <nablarch.core.db.dialect.Dialect>` は、以下の機能を提供する。

* identityカラムを使えるか否かを返すメソッド(:java:extdoc:`supportsIdentity <nablarch.core.db.dialect.Dialect.supportsIdentity()>` )
* シーケンスオブジェクトを使えるか否かを返すメソッド(:java:extdoc:`supportsSequence <nablarch.core.db.dialect.Dialect.supportsSequence()>` )
* 検索クエリーの範囲指定でoffset（またはoffsetと同等の機能）を使えるか否かを返すメソッド(:java:extdoc:`supportsOffset <nablarch.core.db.dialect.Dialect.supportsOffset()>` )
* 一意制約違反を表す :java:extdoc:`SQLException <java.sql.SQLException>` か否かを判定するメソッド(:java:extdoc:`isDuplicateException <nablarch.core.db.dialect.Dialect.isDuplicateException(java.sql.SQLException)>` )
* トランザクションタイムアウト対象の  :java:extdoc:`SQLException <java.sql.SQLException>` か否かを判定するメソッド(:java:extdoc:`isTransactionTimeoutError <nablarch.core.db.dialect.Dialect.isTransactionTimeoutError(java.sql.SQLException)>` )
* シーケンスオブジェクトから次の値を取得するSQL文生成するメソッド(:java:extdoc:`buildSequenceGeneratorSql <nablarch.core.db.dialect.Dialect.buildSequenceGeneratorSql(java.lang.String)>` )
* :java:extdoc:`ResultSet <java.sql.ResultSet>` から値を取得する :java:extdoc:`ResultSetConvertor <nablarch.core.db.statement.ResultSetConvertor>` を返すメソッド(:java:extdoc:`getResultSetConvertor <nablarch.core.db.dialect.Dialect.getResultSetConvertor()>` )
* 検索クエリーを範囲指定（ページング用）SQLに変換するメソッド(:java:extdoc:`convertPaginationSql <nablarch.core.db.dialect.Dialect.convertPaginationSql(java.lang.String,%20nablarch.core.db.statement.SelectOption)>` )
* 検索クエリーを件数取得SQLに変換するメソッド(:java:extdoc:`convertCountSql <nablarch.core.db.dialect.Dialect.convertCountSql(java.lang.String)>` )
* :java:extdoc:`Connection <java.sql.Connection>` がデータベースに接続されているかチェックを行うSQLを返すメソッド(:java:extdoc:`getPingSql <nablarch.core.db.dialect.Dialect.getPingSql()>` )
* Javaオブジェクトをデータベースに出力する値に変換するメソッド(:java:extdoc:`convertToDatabase <nablarch.core.db.dialect.Dialect.convertToDatabase(java.lang.Object, int)>`)
* データベースから取得した値をJavaオブジェクトに変換するメソッド(:java:extdoc:`convertFromDatabase <nablarch.core.db.dialect.Dialect.convertFromDatabase(java.lang.Object, java.lang.Class)>`)

:java:extdoc:`Dialect <nablarch.core.db.dialect.Dialect>` の設定方法は、 :ref:`database-use_dialect` を参照。

.. _database-sql_file:

SQLはロジックではなくSQLファイルに記述する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SQLはSQLファイルに定義し、原則ロジック内には記述しない。

SQLファイルに記述することで、ロジックでSQLの組み立てを行う必要がなく、
必ず `PreparedStatement` を使用するため、SQLインジェクションの脆弱性が排除できる。

.. tip::

  どうしてもSQLファイルに定義できない場合は、SQLを直接指定して実行するAPIも提供しているので、そちらを使用すること。
  ただし、安易に使用するとSQLインジェクションの脆弱性が埋め込まれる可能性があるため注意すること。
  また、SQLインジェクションの脆弱性がないことなど、テストやレビューで担保出来ることが前提となる。


詳細は、 :ref:`database-use_sql_file` を参照。

.. _database-bean:

Beanのプロパティ値をSQLのバインド変数に埋め込むことができる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Beanのプロパティに設定した値を :java:extdoc:`java.sql.PreparedStatement` のINパラメータに自動的にバインドする機能を提供する。

この機能を使用することで、  :java:extdoc:`java.sql.PreparedStatement` の値設定用メソッドを複数回呼び出す必要がなくなり、
INパラメータが増減した際のインデクス修正などが不要となる。

詳細は :ref:`database-input_bean` を参照。

like検索を容易に実装できる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
like検索に対するescape句の挿入とワイルドカード文字のエスケープ処理を自動で行う機能を提供する。

詳細は :ref:`database-like_condition` を参照。

.. _database-variable_condition:

実行時のBeanオブジェクトの状態を元にSQL文を動的に構築できる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Beanオブジェクトの状態を元に、実行するSQL文を動的に組み立てる機能を提供する。

例えば、条件やin句の動的な構築などが行える。

詳細は以下を参照。

* :ref:`database-use_variable_condition`
* :ref:`database-in_condition`
* :ref:`database-make_order_by`

SQLのクエリ結果をキャッシュできる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
実行したSQLと外部から取得した条件(バインド変数に設定した値)が等価である場合に、
データベースにアクセスせずにキャッシュから検索結果を返却する機能を提供する。

詳細は、 :ref:`database-use_cache` を参照。

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-jdbc</artifactId>
  </dependency>

使用方法
--------------------------------------------------

.. _database-connect:

データベースに対する接続設定を行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
データベースに対する接続設定は、以下の2通りから選択することができる。

* :java:extdoc:`javax.sql.DataSource` を使ったデータベース接続の生成
* アプリケーションサーバなどに登録されたデータソースを使ったデータベース接続の生成

上記以外の接続方法を使用したい場合(例えばOSSのコネクションプーリングライブラリを使う場合など)は、
:ref:`database-add_connection_factory` を参照し、データベース接続を行う実装を追加すること。

接続設定例
  :java:extdoc:`javax.sql.DataSource` からデータベース接続の生成
    .. code-block:: xml

      <component class="nablarch.core.db.connection.BasicDbConnectionFactoryForDataSource">
        <!-- 設定値の詳細はJavadocを参照すること -->
      </component>

  アプリケーションサーバのデータソースからデータベース接続の生成
    .. code-block:: xml

      <component class="nablarch.core.db.connection.BasicDbConnectionFactoryForJndi">
        <!-- 設定値の詳細はJavadocを参照すること -->
      </component>

  :java:extdoc:`BasicDbConnectionFactoryForDataSource<nablarch.core.db.connection.BasicDbConnectionFactoryForDataSource>` や
  :java:extdoc:`BasicDbConnectionFactoryForJndi <nablarch.core.db.connection.BasicDbConnectionFactoryForJndi>` への
  設定値については、それぞれのクラスのJavadocを参照すること。

.. tip::

  上記に設定したクラスを直接使用することは基本的にない。
  データベースアクセスを必要とする場合には、 :ref:`database_connection_management_handler` を使用すること。

  なお、データベースを利用する場合はトランザクション管理も必要となる。
  トランザクション管理については、 :ref:`transaction` を参照。

.. _database-use_dialect:

データベース製品に対応したダイアレクトを使用する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
データベース製品に対応したダイアレクトをコンポーネント設定ファイルに設定することで、ダイアレクト機能が有効になる。

.. tip::
  設定を行わなかった場合は :java:extdoc:`DefaultDialect <nablarch.core.db.dialect.DefaultDialect>` が利用される。
  :java:extdoc:`DefaultDialect <nablarch.core.db.dialect.DefaultDialect>` は原則全ての機能が無効化されるので、必ずデータベース製品に対応したダイアレクトを設定すること。

  なお、使用するデータベース製品に対応するダイアレクトが存在しない場合や、
  新しいバージョンの新機能を使いたい場合には、 :ref:`database-add_dialect` を参照し新しいダイアレクトを作成すること。

コンポーネント設定例
  この例では、 :java:extdoc:`javax.sql.DataSource` からデータベース接続を取得するコンポーネントへの設定例となる。
  :java:extdoc:`BasicDbConnectionFactoryForJndi <nablarch.core.db.connection.BasicDbConnectionFactoryForJndi>` の場合も以下の例と同じように
  :java:extdoc:`dialect <nablarch.core.db.connection.ConnectionFactorySupport.setDialect(nablarch.core.db.dialect.Dialect)>` プロパティにダイアレクトを設定すれば良い。

  .. code-block:: xml

    <component class="nablarch.core.db.connection.BasicDbConnectionFactoryForDataSource">
      <!-- ダイアレクトと関係のないプロパティについては省略 -->

      <!--
      ダイアレクトは、dialectプロパティに設定する。
      この例では、Oracleデータベース用のダイアレクトを設定している。
      -->
      <property name="dialect">
        <component class="nablarch.core.db.dialect.OracleDialect" />
      </property>
    </component>


.. _database-use_sql_file:

SQLをファイルで管理する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
この機能では、 :ref:`database-sql_file` で説明したように、SQLはSQLファイルで管理する。
SQLファイルを扱うためには、コンポーネント設定ファイルへの設定が必要となる。
詳細は、 :ref:`SQLファイルからSQLをロードするための設定 <database-load_sql>` を参照。

SQLファイルは以下のルールで作成する。

* クラスパス配下に作成する。
* 1つのSQLファイルに複数のSQLを記述できるが、SQLIDはファイル内で一意とする。
* SQLIDとSQLIDとの間には空行を挿入する。(スペースが存在する行は空行とはみなさない)
* SQLIDとSQLとの間には ``=`` を入れる。
* コメントは ``--`` で記述する。(ブロックコメントはサポートしない)
* SQLは改行やスペース(tab)などで整形してもよい。

.. important::

  SQLを複数機能で流用せずに、かならず機能毎に作成すること。

  複数機能で流用した場合、意図しない使われ方やSQLが変更されることにより思わぬ不具合が発生する原因となる。
  例えば、複数機能で使用していたSQL文に排他ロック用の ``for update`` が追加された場合、
  排他ロックが不要な機能でロックが取得され処理遅延の原因となる。

以下にSQLファイルの例を示す。

.. code-block:: sql

  -- ＸＸＸＸＸ取得SQL
  -- SQL_ID:GET_XXXX_INFO
  GET_XXXX_INFO =
  select
     col1,
     col2
  from
     test_table
  where
     col1 = :col1


  -- ＸＸＸＸＸ更新SQL
  -- SQL_ID:UPDATE_XXXX
  update_xxxx =
  update
      test_table
  set
      col2 = :col2
  where
      col1 = :col1

.. _database-load_sql:

SQLファイルからSQLをロードするための設定
  SQLファイルからSQLをロードするために必要な設定内容を説明する。

  SQLをロードするためには、以下の例のように :java:extdoc:`BasicStatementFactory#sqlLoader <nablarch.core.db.statement.BasicStatementFactory.setSqlLoader(nablarch.core.cache.StaticDataLoader)>`
  に :java:extdoc:`BasicSqlLoader <nablarch.core.db.statement.BasicSqlLoader>` を設定する。

  この例では、ファイルエンコーディングと拡張子を設定している。設定を省略した場合は以下の設定値となる。

  :ファイルエンコーディング: utf-8
  :拡張子: sql

  ここで定義した :java:extdoc:`BasicStatementFactory <nablarch.core.db.statement.BasicStatementFactory>` コンポーネントは、 :ref:`database-connect`
  で定義したデータベース接続を取得するコンポーネントに設定する必要がある。

  設定例
    .. code-block:: xml

      <component name="statementFactory" class="nablarch.core.db.statement.BasicStatementFactory">
        <property name="sqlLoader">
          <component class="nablarch.core.db.statement.BasicSqlLoader">
            <property name="fileEncoding" value="utf-8"/>
            <property name="extension" value="sql"/>
          </component>
        </property>
      </component>

.. _database-execute_sqlid:

SQLIDを指定してSQLを実行する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SQLIDを元にSQLを実行するには、 :java:extdoc:`DbConnectionContext <nablarch.core.db.connection.DbConnectionContext>` から取得したデータベース接続を使用する。
なお、  :java:extdoc:`DbConnectionContext <nablarch.core.db.connection.DbConnectionContext>` には、 :ref:`database_connection_management_handler` でデータベース接続を登録する必要がある。

SQLIDと実際に実行されるSQLとのマッピングルールは以下のとおり。

* SQLIDの ``#`` までがSQLファイル名となる。
* SQLIDの ``#`` 以降がSQLファイル内のSQLIDとなる。

実装例
  この例では、 SQLIDに、 ``jp.co.tis.sample.action.SampleAction#findUser`` と指定しているため、
  SQLファイルはクラスパス配下の ``jp.co.tis.sample.action.SampleAction.sql`` となる。
  SQLファイル内のSQLIDは、 ``findUser`` となる。

  * :java:extdoc:`AppDbConnection <nablarch.core.db.connection.AppDbConnection>` や
    :java:extdoc:`SqlPStatement <nablarch.core.db.statement.SqlPStatement>` の使用方法は、Javadocを参照。

  .. code-block:: java

    // DbConnectionContextからデータベース接続を取得する。
    AppDbConnection connection = DbConnectionContext.getConnection();

    // SQLIDを元にステートメントを生成する。
    SqlPStatement statement = connection.prepareStatementBySqlId(
        "jp.co.tis.sample.action.SampleAction#findUser");

    // 条件を設定する。
    statement.setLong(1, userId);

    // 検索処理を実行する。
    SqlResultSet result = statement.retrieve();

ストアードプロシージャを実行する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ストアードプロシージャを実行する場合も、基本的にはSQLを実行する場合と同じように実装する。

.. important::

  ストアードプロシージャの実行では、 :ref:`database-bean` はサポートしない。
  これは、ストアードプロシージャを使用した場合、ロジックがJavaとストアードプロシージャに分散してしまい、
  保守性を著しく低下させるため原則使用すべきではないとしているためである。

  ただし、既存の資産などでどうしてもストアードプロシージャを使用しなければならないケースが想定されるため、
  本機能では非常に簡易的ではあるがストアードプロシージャを実行するためのAPIを提供している。

以下に例を示す。

* :java:extdoc:`SqlCStatement <nablarch.core.db.statement.SqlCStatement>` の詳細な使用方法は、Javadocを参照すること。

.. code-block:: java

  // SQLIDを元にストアードプロシージャ実行用のステートメントを生成する。
  SqlCStatement statement = connection.prepareCallBySqlId(
      "jp.co.tis.sample.action.SampleAction#execute_sp");

  // IN及びOUTパラメータを設定する。
  statement.registerOutParameter(1, Types.CHAR);

  // 実行する。
  statement.execute();

  // OUTパラメータを取得する。
  String result = statement.getString(1);

.. _database-paging:

検索範囲を指定してSQLを実行する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ウェブシステムの一覧検索画面などでは、ページング機能を用いて特定の範囲の結果のみを表示することがある。
このような用途向けに本機能では、検索結果の範囲を指定できる機能を提供している。

実装例
  データベース接続( `connection` )からステートメントを生成する際に、検索対象の範囲を指定する。
  この例では、以下の値を指定しているので、11件目から最大10件のレコードが取得される。

  :開始位置: 11
  :取得件数: 10

  .. code-block:: java

    // DbConnectionContextからデータベース接続を取得する
    AppDbConnection connection = DbConnectionContext.getConnection();

    // SQLIDと検索範囲を指定してステートメントオブジェクトを生成する。
    SqlPStatement statement = connection.prepareStatementBySqlId(
        "jp.co.tis.sample.action.SampleAction#findUser", new SelectOption(11, 10));

    // 検索処理を実行する
    SqlResultSet result = statement.retrieve();

.. tip::
  検索範囲が指定された場合、検索用のSQLを取得範囲指定のSQLに書き換えてから実行を行う。
  なお、取得範囲指定のSQLは :ref:`ダイアレクト <database-dialect>` により行われる。

.. _database-input_bean:

Beanオブジェクトを入力としてSQLを実行する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`database-bean` で説明したように、Beanオブジェクトを入力としてSQLを実行することができる。

Beanオブジェクトを入力としてSQLを実行する場合は、SQLのINパラメータには名前付きバインド変数を用いる。
名前付きパラメータには、 ``:`` に続けて入力として受け取るBeanのプロパティ名を記述する。

.. important::

  INパラメータをJDBC標準の ``?`` で記述した場合、 Beanオブジェクトを入力としたSQLの実行は動作しないので注意すること。

以下に実装例を示す。

SQL例
  INパラメータには名前付きパラメータを使用する。

  .. code-block:: sql

    insert into user
      (
      id,
      name
      ) values (
      :id,
      :userName
      )

実装例
  Beanオブジェクトに必要な値を設定し、Beanオブジェクトを入力としてSQLを実行する機能を呼び出す。

  * :java:extdoc:`AppDbConnection <nablarch.core.db.connection.AppDbConnection>` や :java:extdoc:`ParameterizedSqlPStatement <nablarch.core.db.statement.ParameterizedSqlPStatement>` の使用方法は、Javadocを参照。
  * SQLIDと実行されるSQLの関係については、 :ref:`database-execute_sqlid` を参照

  .. code-block:: java

    // beanを生成しプロパティに値を設定
    UserEntity entity = new UserEntity();
    entity.setId(1);              // idプロパティへの値設定
    entity.setUserName("なまえ"); // userNameプロパティへの値設定

    // DbConnectionContextからデータベース接続を取得する
    AppDbConnection connection = DbConnectionContext.getConnection();

    // SQLIDを元にステートメントを生成する
    ParameterizedSqlPStatement statement = connection.prepareParameterizedSqlStatementBySqlId(
        "jp.co.tis.sample.action.SampleAction#insertUser");

    // beanのプロパティの値をバインド変数に設定しSQLが実行される
    // SQLの:idにbeanのidプロパティの値が設定される。
    // SQLの:userNameには、beanのuserNameプロパティの値が設定される。
    int result = statement.executeUpdateByObject(entity);

.. tip::

  Beanの代わりに :java:extdoc:`java.util.Map` の実装クラスも指定できる。
  Mapを指定した場合は、Mapのキー値と一致するINパラメータに対して、Mapの値が設定される。

  なお、Beanを指定した場合でも内部的にはBeanの値をMapに変換して扱う。
  Mapへの変換には、 :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` を使用するので、
  :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` でサポートしないデータ型は、この機能で使用することはできない。

  :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` で扱えるデータ型では要件を満たす事ができない場合は、
  :ref:`utility-conversion` を参照し、変換可能なデータ型を追加すること。

.. tip::

  Beanへのアクセス方法をプロパティからフィールドに変更することができる。
  フィールドアクセスに変更する場合には、configファイルに以下の設定を追加する。

  .. code-block:: properties

     nablarch.dbAccess.isFieldAccess=true

  なお、フィールドアクセスは以下の理由により推奨しない。

  本フレームワークのその他の機能(例えば :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>`)では、Beanから値を取得する方法はプロパティアクセスで統一されている。
  データベース機能のみフィールドアクセスに変更した場合、プログラマはフィールドアクセスとプロパティアクセスの両方を意識する必要があり、生産性の低下や不具合の原因ともなる。

.. _database-common_bean:

SQL実行時に共通的な値を自動的に設定したい
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
データ登録時や更新時に毎回設定する値をSQLの実行直前に自動的に設定する機能を提供する。
例えば、登録日時や更新日時といった項目に対して、この機能が使用できる。

この機能は、プロパティに設定されたアノテーションを元に、値の自動設定を行うため、
:ref:`database-input_bean` を使用した場合のみ有効となる。

以下に使用例を示す。

コンポーネント設定ファイル
  この機能を使用するには、コンポーネント設定ファイルに値の自動設定を行うクラスを設定する。

  以下の例のように、 :java:extdoc:`BasicStatementFactory#updatePreHookObjectHandlerList <nablarch.core.db.statement.BasicStatementFactory.setUpdatePreHookObjectHandlerList(java.util.List)>` に対して、
  :java:extdoc:`AutoPropertyHandler <nablarch.core.db.statement.AutoPropertyHandler>` 実装クラスをlistで設定する。
  なお、標準で提供される実装クラスは :java:extdoc:`nablarch.core.db.statement.autoproperty` パッケージ配下に配置されている。

  ここで定義した :java:extdoc:`BasicStatementFactory <nablarch.core.db.statement.BasicStatementFactory>` コンポーネントは、 :ref:`database-connect`
  で定義したデータベース接続を取得するコンポーネントに設定すること。

  .. code-block:: xml

    <component name="statementFactory"
        class="nablarch.core.db.statement.BasicStatementFactory">

      <property name="updatePreHookObjectHandlerList">
        <list>
          <!-- nablarch.core.db.statement.AutoPropertyHandler実装クラスをlistで設定する-->
        </list>
      </property>
    </component>

Beanオブジェクト(Entity)
  自動で値を設定したいプロパティにアノテーションを設定する。
  なお、標準で提供されるアノテーションは :java:extdoc:`nablarch.core.db.statement.autoproperty` パッケージ配下に配置されている。

  .. code-block:: java

    public class UserEntity {
      // ユーザID
      private String id;

      // 登録日時
      // 登録時に自動設定される
      @CurrentDateTime
      private Timestamp createdAt;

      // 更新日時
      // 登録・更新時に自動設定される
      @CurrentDateTime
      private String updatedAt;

      // アクセスメソッドなどは省略
    }

SQL
  SQLは、 :ref:`database-input_bean` と同じように作成する。

  .. code-block:: sql

    insert into user (
      id,
      createdAt,
      updatedAt
    ) values (
      :id,
      :createdAt,
      :updatedAt
    )

実装例
  基本的には、 :ref:`database-input_bean` と同じように実装する。
  値が自動設定される項目については、ロジックでBeanに対して値を設定する必要が無い。
  なお、値を明示的に設定したとしても、SQL実行直前に値の自動設定機能により上書きされる。

  .. code-block:: java

    // beanを生成しプロパティに値を設定
    // 自動設定項目であるcreatedAtとupdatedAtには値を設定する必要はない
    UserEntity entity = new UserEntity();
    entity.setId(1);

    // DbConnectionContextからデータベース接続を取得する
    AppDbConnection connection = DbConnectionContext.getConnection();

    // SQLIDを元にステートメントを生成する
    ParameterizedSqlPStatement statement = connection.prepareParameterizedSqlStatementBySqlId(
        "jp.co.tis.sample.action.SampleAction#insertUser");

    // 自動設定項目に値を設定せずに呼び出す。
    // データベース機能が自動的に値を設定する。
    int result = statement.executeUpdateByObject(entity);

.. _database-like_condition:

like検索を行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
like検索は、 :ref:`database-input_bean` を使用し、SQLにはlike検索用の条件を以下のルールで記述する。

前方一致の場合
  名前付きパラメータの末尾に ``%`` を記述する。

  例: ``name like :userName%``

後方一致の場合
  名前付きパラメータの先頭に ``%`` を記述する。

  例: ``name like :%userName``

途中一致の場合
  名前付きパラメータの前後に ``%`` を記述する。

  例: ``name like :%userName%``

like検索時のエスケープ文字及びエスケープ対象文字の定義は、 :ref:`database-def_escape_char` を参照。

以下に実装例を示す。

SQL
  上記のルールに従いSQLを定義する。

  .. code-block:: sql

    select *
      from user
     where name like :userName%

実装例
  :ref:`database-input_bean` と同じようにSQLを実行するだけで、like条件用に値の書き換えやエスケープ処理が行われる。
  この例の場合、実際の条件は ``name like 'な%' escape '\'`` となる。

  * :java:extdoc:`AppDbConnection <nablarch.core.db.connection.AppDbConnection>` や :java:extdoc:`ParameterizedSqlPStatement <nablarch.core.db.statement.ParameterizedSqlPStatement>` の使用方法は、Javadocを参照。
  * SQLIDと実行されるSQLの関係については、 :ref:`database-execute_sqlid` を参照

  .. code-block:: java

    // beanを生成しプロパティに値を設定
    UserEntity entity = new UserEntity();
    entity.setUserName("な"); // userNameプロパティへの値設定

    // DbConnectionContextからデータベース接続を取得する
    AppDbConnection connection = DbConnectionContext.getConnection();

    // SQLIDを元にステートメントを生成する
    ParameterizedSqlPStatement statement = connection.prepareParameterizedSqlStatementBySqlId(
        "jp.co.tis.sample.action.SampleAction#findUserByName");

    // beanのプロパティ値をバインド変数に設定しSQLが実行される
    // この例の場合、name like 'な%' が実行される
    int result = statement.retrieve(bean);


.. _database-def_escape_char:

like検索時のエスケープ文字及びエスケープ対象文字を定義する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
エスケープ文字及びエスケープ対象文字の定義は、コンポーネント設定ファイルに行う。
なお、エスケープ文字は自動的対象にエスケープとなるため、明示的にエスケープ対象文字に設定する必要はない。

設定を省略した場合は、以下の値を使用する。

:エスケープ文字: ``\``
:エスケープ対象文字: ``%`` 、 ``_``

コンポーネント設定例
  この例ではエスケープ文字に ``\`` を設定し、エスケープ文字には ``%`` 、 ``％`` 、 ``_`` 、 ``＿`` の4文字を設定している。

  ここで定義した :java:extdoc:`BasicStatementFactory <nablarch.core.db.statement.BasicStatementFactory>` コンポーネントは、 :ref:`database-connect`
  で定義したデータベース接続を取得するコンポーネントに設定すること。

  .. code-block:: xml

    <component name="statementFactory" class="nablarch.core.db.statement.BasicStatementFactory">
      <!-- エスケープ文字の定義 -->
      <property name="likeEscapeChar" value="\" />

      <!-- エスケープ対象文字の定義(カンマ区切りで設定する) -->
      <property name="likeEscapeTargetCharList" value="%,％,_,＿" />
    </component>

.. _database-use_variable_condition:

可変条件を持つSQLを実行する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
可変条件を持つSQLの実行は、 :ref:`database-input_bean` を使用し、以下の記法を用いて条件を記述する。

可変条件の記述ルール
  可変条件は、 ``$if(プロパティ名) {SQL文の条件}`` で記述する。
  ``$if`` の後のプロパティ名に対応したBeanオブジェクトの値により、その条件が除外される。
  除外される条件は以下のとおり。

  * 配列や :java:extdoc:`java.util.Collection` の場合は、プロパティ値がnullやサイズ0の場合
  * 上記以外の型の場合は、プロパティ値がnullや空文字列(Stringオブジェクトの場合)

  なお、 ``$if`` 特殊構文には以下の制約がある。

  * 利用できる箇所はwhere句のみ
  * ``$if`` 内に ``$if`` を使用することはできない

  .. important::

    この機能は、ウェブアプリケーションの検索画面のようにユーザの入力内容によって検索条件が変わるような場合に使うものである。
    条件だけが異なる複数のSQLを共通化するために使用するものではない。
    安易に共通化した場合、SQLを変更した場合に思わぬ不具合を埋め込む原因にもなるため、必ずSQLを複数定義すること。


以下に例を示す。

SQL
  このSQLの場合、 ``user_name`` と ``user_kbn`` の条件が可変となる。

  .. code-block:: sql

    select
      user_id,
      user_name,
      user_kbn
    from
      user
    where
      $if (userName) {user_name like :user_name%}
      and $if (userKbn) {user_kbn in ('1', '2')}
      and birthday = :birthday

実装例
  `userName` プロパティのみに値が設定されているので、
  可変条件で定義されている ``user_kbn`` は実行時の条件から除外される。

  .. code-block:: java

    // beanを生成しプロパティに値を設定
    UserEntity entity = new UserEntity();
    entity.setUserName("なまえ");

    // DbConnectionContextからデータベース接続を取得する
    AppDbConnection connection = DbConnectionContext.getConnection();

    // SQLIDを元にステートメントを生成する
    // 2番めの引数には、条件を持つBeanオブジェクトを指定する。
    // このBeanオブジェクトの状態を元にSQLの可変条件の組み立てが行われる。
    ParameterizedSqlPStatement statement = connection.prepareParameterizedSqlStatementBySqlId(
        "jp.co.tis.sample.action.SampleAction#insertUser", entity);

    // entityのプロパティの値をバインド変数に設定しSQLが実行される
    SqlResultSet result = statement.retrieve(entity);

.. _database-in_condition:

in句の条件数が可変となるSQLを実行する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
in句の条件数が可変となるSQLの実行は、 :ref:`database-input_bean` を使用し、以下の記法を用いて条件を記述する。

in句の記述ルール
  条件の名前付きパラメータの末尾に ``[]`` を付加する。
  また名前付きパラメータに対応するBeanオブジェクトのプロパティの型は、
  配列か :java:extdoc:`java.util.Collection` (サブタイプ含む) とする必要がある。

  .. tip::

    in句の条件となるプロパティ値がnullやサイズ0となる場合には、該当条件は必ず可変条件として定義すること。
    もし、可変条件としなかった場合でプロパティ値がnullの場合、条件が ``xxxx in (null)`` となるため、
    検索結果が正しく取得できない可能性がある。

    ※in句は、条件式(カッコの中)を空にすることはできないため、サイズ0の配列やnullが指定された場合には、条件式を ``in (null)`` とする仕様としている。

以下に例を示す。

SQL
  このSQLでは、 ``user_kbn`` のin条件が動的に構築される。
  なお、 ``$if`` と併用しているため、 `userKbn` プロパティがnullやサイズが0の場合には条件から除外される。

  .. code-block:: sql

    select
      user_id,
      user_name,
      user_kbn
    from
      user
    where
      $if (userKbn) {user_kbn in (:userKbn[])}

実行例
  この例では、 `userKbn` プロパティに2つの要素が設定されているので、
  実行されるSQLの条件は ``userKbn in (?, ?)`` となる。

  データベースから取得されるのは、 `userKbn` が ``1`` と ``3`` のレコードとなる。

  .. code-block:: java

    // beanを生成しプロパティに値を設定
    UserSearchCondition condition = new UserSearchCondition();
    condition.setUserKbn(Arrays.asList("1", "3"));

    // DbConnectionContextからデータベース接続を取得する
    AppDbConnection connection = DbConnectionContext.getConnection();

    // SQLIDを元にステートメントを生成する
    // 2番めの引数には、条件を持つBeanオブジェクトを指定する。
    // このBeanオブジェクトの状態を元にSQLのin句の組み立てが行われる。
    ParameterizedSqlPStatement statement = connection.prepareParameterizedSqlStatementBySqlId(
        "jp.co.tis.sample.action.SampleAction#searchUser", condition);

    // conditionのプロパティの値をバインド変数に設定しSQLが実行される
    SqlResultSet result = statement.retrieve(condition);


.. _database-make_order_by:

order byのソート項目を実行時に動的に切り替えてSQLを実行する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
order byのソート項目が可変となるSQLの実行は、 :ref:`database-input_bean` を使用し、以下の記法を用いて条件を記述する。

order by句の記述ルール
  ソート項目を可変にする場合は、order by句の代わりに ``$sort`` を使用し、以下のように記述する。

  .. code-block:: text

     $sort(プロパティ名) {(ケース1)(ケース2)・・・(ケースn)}

     プロパティ名: BeanオブジェクトのソートIDを保持するプロパティ名
     ケース: order by句の切り替え候補を表す。
             候補を一意に識別するソートIDとorder by句に指定する文字列(以降はケース本体と称す)を記述する。
             どの候補にも一致しない場合に使用するデフォルトのケースには、ソートIDに"default"を指定する。

  * 各ケースは、ソートIDとケース本体を半角丸括弧で囲んで表現する。
  * ソートIDとケース本体は、半角スペースで区切る。
  * ソートIDには半角スペースを使用不可とする。
  * ケース本体には半角スペースを使用できる。
  * 括弧開き以降で最初に登場する文字列をソートIDとする。
  * ソートID以降で括弧閉じまでの間をケース本体とする。
  * ソートIDおよびケース本体はトリミングする。

以下に使用例を示す。

SQL
  .. code-block:: sql

    select
      user_id,
      user_name
    from
      user
    where
      user_name = :user_name
    $sort(sortId) {
      (user_id_asc  user_id asc)
      (user_id_desc user_id desc)
      (name_asc     user_name asc)
      (name_desc    user_name desc)
      (default      user_id)

実装例
  この例では、ソートIDに ``name_asc`` を設定しているので、
  order by句は ``order by user_name asc`` となる。

  .. code-block:: java

    // beanを生成しプロパティに値を設定
    UserSearchCondition condition = new UserSearchCondition();
    condition.setUserName("なまえ");
    condition.setSortId("name_asc");      // ソートIDを設定する

    // DbConnectionContextからデータベース接続を取得する
    AppDbConnection connection = DbConnectionContext.getConnection();

    // SQLIDを元にステートメントを生成する
    // 2番めの引数には、条件を持つBeanオブジェクトを指定する。
    // このBeanオブジェクトの状態を元にSQLのorder by句の組み立てが行われる。
    ParameterizedSqlPStatement statement = connection.prepareParameterizedSqlStatementBySqlId(
        "jp.co.tis.sample.action.SampleAction#searchUser", condition);

    // conditionのプロパティの値をバインド変数に設定しSQLが実行される
    SqlResultSet result = statement.retrieve(condition);

.. _database-binary_column:

バイナリ型のカラムにアクセスする
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
blob(データベース製品によりバイナリ型の型は異なる)などのバイナリ型のカラムへのアクセス方法について説明する。

バイナリ型の値を取得する
  バイナリ型の値を取得する場合には、検索結果オブジェクトの :java:extdoc:`SqlRow <nablarch.core.db.statement.SqlRow>` から `byte[]` として値を取得する。

  以下に例を示す。

  .. code-block:: java

    SqlResultSet rows = statement.retrieve();

    SqlRow row = rows.get(0);

    // 暗号化されたカラムの値をgetBytesを使ってバイナリで取得する
    byte[] encryptedPassword = row.getBytes("password");

  .. important::

    上記実装例の場合、カラムの内容が全てJavaのヒープ上に展開される。
    このため、非常に大きいサイズのデータを読み込んだ場合、ヒープ領域を圧迫し、システムダウンなどの障害の原因となる。

    このため、大量データを読み込む場合には、以下のように :java:extdoc:`Blob <java.sql.Blob>` オブジェクトを使用して、ヒープを大量に消費しないようにすること。

    .. code-block:: java

      SqlResultSet rows = select.retrieve();

      // Blogとしてデータを取得する
      Blob pdf = (Blob) rows.get(0).get("PDF");

      try (InputStream input = pdf.getBinaryStream()) {
        // InputStreamからデータを順次読み込み処理を行う。
        // 一括で読み込んだ場合、全てヒープに展開されるので注意すること
      }

バイナリ型の値を登録・更新する
  サイズの小さいバイナリ値を登録・更新する場合は、 :java:extdoc:`SqlPStatement#setByte <nablarch.core.db.statement.SqlPStatement.setBytes(int, byte[])>` を使用する。

  .. code-block:: java

    SqlPStatement statement = getSqlPStatement("UPDATE_PASSWORD");

    statement.setBytes(1, new byte[] {0x30, 0x31, 0x32});
    int updateCount = statement.executeUpdate();

 サイズが大きいバイナリ値を登録更新する場合は、 :java:extdoc:`SqlPStatement#setBinaryStream <nablarch.core.db.statement.SqlPStatement.setBinaryStream(int, java.io.InputStream, int)>`
 を使用して、ファイルなどを表す :java:extdoc:`InputStream <java.io.InputStream>` から直接データベースに値を送信する。

 .. code-block:: java

    final Path pdf = Paths.get("input.pdf");
    try (InputStream input = Files.newInputStream(pdf)) {
        statement.setBinaryStream(1, input, (int) Files.size(pdf));
    }



データベースアクセス時に発生する例外の種類
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
データベースアクセス時の例外は、大きく分けて以下の4種類が送出される。

これらの例外は全て非チェック例外のため、 :java:extdoc:`SQLException <java.sql.SQLException>` のように ``try-catch`` で補足する必要はない。

データベースアクセスエラー時の例外
  データベースアクセス時に発生する例外で、 :java:extdoc:`DbAccessException <nablarch.core.db.DbAccessException>` が送出される。

データベース接続エラー時の例外
  データベースアクセスエラー時の例外がデータベース接続エラーを示す場合には、 :java:extdoc:`DbConnectionException <nablarch.core.db.connection.exception.DbConnectionException>` が送出される。
  この例外は、 :ref:`retry_handler` により処理される。(:ref:`retry_handler` 未適用の場合には、実行時例外として扱われる。)

  なお、データベース接続エラーの判定には、 :ref:`ダイアレクト <database-dialect>` が使用される。

SQL実行時の例外
  SQLの実行に失敗した時に発生する例外で、 :java:extdoc:`SqlStatementException <nablarch.core.db.statement.exception.SqlStatementException>` が送出される。

SQL実行時の例外が一意制約違反の場合の例外
  SQL実行時の例外が一意制約違反を示す例外の場合は、 :java:extdoc:`DuplicateStatementException <nablarch.core.db.statement.exception.DuplicateStatementException>` が送出される。

  一意制約違反をハンドリングしたい場合には、 :ref:`database-duplicated_error` を参照。

  なお、一意制約違反の判定には、 :ref:`ダイアレクト <database-dialect>` が使用される。

.. tip::

  データベースアクセスエラー発生時の例外を変更したい場合（より細かく分けたい場合）などは、
  :ref:`database-change_exception` を参照すること。

.. _database-duplicated_error:

一意制約違反をハンドリングして処理を行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
一意制約違反時に何か処理を行う必要がある場合には、 :java:extdoc:`DuplicateStatementException <nablarch.core.db.statement.exception.DuplicateStatementException>` を ``try-catch`` で補足し処理をする。

なお、一意制約違反の判定には、 :ref:`ダイアレクト <database-dialect>` が使用される。

.. important::

  データベース製品によってはSQL実行時に例外が発生した場合に、ロールバックを行うまで一切のSQLを受け付けないものがあるので注意すること。
  このような製品の場合には、他の手段で代用できないか検討すること。

  例えば、登録処理で一意制約違反が発生した場合に更新処理をしたい場合は、
  例外ハンドリングを行うのではなく `merge` 文を使用することでこの問題を回避できる。

処理が長いトランザクションはエラーとして処理を中断させる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
トランザクション管理にて実現する。
詳細は、 :ref:`transaction-timeout` を参照。

.. _database-new_transaction:

現在のトランザクションとは異なるトランザクションでSQLを実行する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
データベース接続管理ハンドラ及びトランザクション制御ハンドラで開始したトランザクションではなく、
個別のトランザクションを使用してデータベースアクセスを行いたい場合がある。

例えば、業務処理が失敗した場合でも必ずデータベースへの変更を確定したい場合には、
現在のトランザクションとは異なるトランザクションを定義してデータベースにアクセスする。

個別トランザクションを使用するには、以下の手順が必要となる。

#. コンポーネント設定ファイルに :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` を定義する。
#. :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` をシステムリポジトリから取得し、新たなトランザクションでSQLを実行する。
   （システムリポジトリから取得するのではなく、 :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` を設定して使用してもよい)

以下に使用例を示す。

コンポーネント設定ファイル
  コンポーネント設定ファイルに  :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` を設定する。

  * :java:extdoc:`connectionFactory <nablarch.core.db.transaction.SimpleDbTransactionManager.setConnectionFactory(nablarch.core.db.connection.ConnectionFactory)>` プロパティに :java:extdoc:`ConnectionFactory <nablarch.core.db.connection.ConnectionFactory>` 実装クラスを設定する。
    :java:extdoc:`ConnectionFactory <nablarch.core.db.connection.ConnectionFactory>` 実装クラスの詳細は、 :ref:`database-connect` を参照。

  * :java:extdoc:`transactionFactory <nablarch.core.db.transaction.SimpleDbTransactionManager.setTransactionFactory(nablarch.core.transaction.TransactionFactory)>` プロパティに :java:extdoc:`TransactionFactory <nablarch.core.transaction.TransactionFactory>` 実装クラスを設定する。
     :java:extdoc:`TransactionFactory <nablarch.core.transaction.TransactionFactory>` 実装クラスの詳細は、 :ref:`transaction-database` を参照。

  .. code-block:: xml

    <component name="update-login-failed-count-transaction" class="nablarch.core.db.transaction.SimpleDbTransactionManager">
      <!-- connectionFactoryプロパティにConnectionFactory実装クラスを設定する -->
      <property name="connectionFactory" ref="connectionFactory" />

      <!-- transactionFactoryプロパティにTransactionFactory実装クラスを設定する -->
      <property name="transactionFactory" ref="transactionFactory" />

      <!-- トランザクションを識別するための名前を設定する -->
      <property name="dbTransactionName" ref="update-login-failed-count-transaction" />

    </component>

実装例
  コンポーネント設定ファイルに設定した :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` を使って、SQLを実行する。
  なお、 :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>` を直接使うのではなくトランザクション制御を行う、
  :java:extdoc:`SimpleDbTransactionExecutor<nablarch.core.db.transaction.SimpleDbTransactionExecutor>` を使用すること。

  .. code-block:: java

    // システムリポジトリからSimpleDbTransactionManagerを取得する
    SimpleDbTransactionManager dbTransactionManager =
        SystemRepository.get("update-login-failed-count-transaction");

    // SimpleDbTransactionManagerをコンストラクタに指定して実行する
    SqlResultSet resultSet = new SimpleDbTransactionExecutor<SqlResultSet>(dbTransactionManager) {
      @Override
      public SqlResultSet execute(AppDbConnection connection) {
        SqlPStatement statement = connection.prepareStatementBySqlId(
            "jp.co.tis.sample.action.SampleAction#findUser");
        statement.setLong(1, userId);
        return statement.retrieve();
      }
    }.doTransaction();

.. _database-use_cache:

検索結果をキャッシュする（同じSQLで同じ条件の場合にキャッシュしたデータを扱いたい)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
更新時間が決まっているデータや、頻繁にアクセスされるが必ず最新のデータを返す必要がない場合には、
データベースの負荷を軽減させるために検索結果をキャッシュすることが出来る。

この機能は、以下のような機能で有効に利用できる。

* 売り上げランキングのように結果が厳密に最新である必要が無く大量に参照されるデータ
* データ更新タイミングが夜間のみで日中は更新されないデータ

制約
  LOB型について
    LOB(BLOB型やCLOB型)のカラムを取得した場合、実際にDBに格納されたデータが取得されるのではなく、LOBロケータが取得される。
    実際の値を取得する場合は、このLOBロケータ経由で値を取得する。

    このLOBロケータの有効期間は、RDBMS毎の実装に依存している。
    通常、 :java:extdoc:`java.sql.ResultSet` や :java:extdoc:`java.sql.Connection` がクローズされた時点でアクセスできなくなる。
    このため、 `ResultSet` や `Connection` よりも生存期間が長いキャッシュにはBLOB、CLOB型を含めることができない。

  アプリケーションの冗長化について
    デフォルトで提供するキャッシュを保持するコンポーネントはJVMのヒープ上にキャッシュを保持する。
    このため、アプリケーションを冗長化構成とした場合、アプリケーションごとに検索結果がキャッシュされることになる。

    このため、キャッシュタイミングが異なるため、それぞれのアプリケーションで異なるキャッシュを保持する可能性がある。

    アプリケーションサーバを冗長化している場合で、ラウンドロビンでロードバランサを行う場合は、
    毎回異なるサーバにアクセスする可能性がある。
    もし、サーバごとに異なるキャッシュを保持していた場合、リクエストの都度異なる結果が画面表示される可能性があるので注意すること。

.. important::

  この機能は、参照系のデータベースアクセスを省略可能な場合に省略し、システム負荷を軽減することを目的としており、
  データベースアクセス（SQL）の高速化を目的としているものではない。
  このため、SQLの高速化を目的として使用してはならない。そのような場合には、SQLのチューニングを実施すること。

.. important::

  この機能は、データベースの値の更新を監視してキャッシュの最新化を行うことはない。
  このため、常に最新のデータを表示する必要がある機能では使用しないこと。

以下に使用例を示す。

コンポーネント設定ファイル
  以下の手順に従い、検索結果のキャッシュを有効化する設定を行う。

  #. クエリ結果をキャッシュするコンポーネントの定義
  #. SQLID毎の検索結果のキャッシュ設定
  #. 検索結果をキャッシュするSQL実行コンポーネントの定義

  クエリ結果のキャッシュクラスのコンポーネントの定義
    デフォルトで提供されるクエリ結果をキャッシュするクラスの :java:extdoc:`InMemoryResultSetCache <nablarch.core.db.cache.InMemoryResultSetCache>` を設定する。

    .. code-block:: xml

      <component name="resultSetCache" class="nablarch.core.db.cache.InMemoryResultSetCache">
        <property name="cacheSize" value="100"/>
        <property name="systemTimeProvider" ref="systemTimeProvider"/>
      </component>

  SQLID毎のキャッシュ設定
    SQLID毎のキャッシュ設定を行う。
    デフォルトで提供される :java:extdoc:`BasicExpirationSetting <nablarch.core.cache.expirable.BasicExpirationSetting>` では、SQLID毎にキャッシュの有効期限が設定できる。

    有効期限には、以下の単位が使用できる。

    :ms: ミリ秒
    :sec: 秒
    :min: 分
    :h: 時

    .. code-block:: xml

      <!-- キャッシュ有効期限設定 -->
        <component name="expirationSetting"
            class="nablarch.core.cache.expirable.BasicExpirationSetting">

          <property name="expiration">
            <map>
              <!-- keyにSQLIDを設定し、valueに有効期限を設定する -->
              <entry key="please.change.me.tutorial.ss11AA.W11AA01Action#SELECT" value="100ms"/>
              <entry key="please.change.me.tutorial.ss11AA.W11AA02Action#SELECT" value="30sec"/>
            </map>
          </property>

        </component>

  検索結果をキャッシュするSQL実行コンポーネントの定義
    検索結果をキャッシュさせるためには、SQL実行コンポーネントの生成クラスに :java:extdoc:`CacheableStatementFactory <nablarch.core.db.cache.statement.CacheableStatementFactory>` を設定する。
    :java:extdoc:`CacheableStatementFactory <nablarch.core.db.cache.statement.CacheableStatementFactory>` は、 デフォルトで提供される
    :java:extdoc:`BasicStatementFactory <nablarch.core.db.statement.BasicStatementFactory>` を継承しているため、
    基本的な設定値は、 :java:extdoc:`BasicStatementFactory <nablarch.core.db.statement.BasicStatementFactory>` と同じである。

    :java:extdoc:`expirationSetting <nablarch.core.db.cache.statement.CacheableStatementFactory.setExpirationSetting(nablarch.core.cache.expirable.ExpirationSetting)>` 及び
    :java:extdoc:`resultSetCache <nablarch.core.db.cache.statement.CacheableStatementFactory.setResultSetCache(nablarch.core.db.cache.ResultSetCache)>` プロパティに対しては、上で設定したクエリー結果のキャッシュコンポーネントと
    SQLID毎のキャッシュ設定のコンポーネントを設定すること。

    ここで定義した :java:extdoc:`CacheableStatementFactory <nablarch.core.db.cache.statement.CacheableStatementFactory>` コンポーネントは、
    :ref:`database-connect` で定義したデータベース接続を取得するコンポーネントに設定すること。

    .. code-block:: xml

      <!-- キャッシュ可能なステートメントを生成するCacheableStatementFactoryを設定する -->
      <component name="cacheableStatementFactory"
                 class="nablarch.core.db.cache.CacheableStatementFactory">

        <!-- 有効期限設定 -->
        <property name="expirationSetting" ref="expirationSetting"/>
        <!-- キャッシュ実装 -->
        <property name="resultSetCache" ref="resultSetCache"/>

      </component>

  実装例
    SQLを使ったデータベースアクセスは、キャッシュ有無によって変わることはない。
    以下と同じように実装すれば良い。

    * :ref:`database-execute_sqlid`
    * :ref:`database-input_bean`

`java.sql.Connection` を使って処理を行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
JDBCのネイティブなデータベース接続( :java:extdoc:`java.sql.Connection` )を扱いたい場合がある。
例えば、 :java:extdoc:`java.sql.DatabaseMetaData` を使用したい場合がこれに該当する。

この場合は、 :java:extdoc:`DbConnectionContext <nablarch.core.db.connection.DbConnectionContext>` から取得した
:java:extdoc:`TransactionManagerConnection <nablarch.core.db.connection.TransactionManagerConnection>` から :java:extdoc:`java.sql.Connection` を取得することで対応できる。

.. important::

  :java:extdoc:`java.sql.Connection` を使用した場合、チェック例外である :java:extdoc:`java.sql.SQLException` をハンドリングして例外制御を行う必要がある。
  この例外制御は実装を誤ると、障害が検知されなかったり障害時の調査ができないなどの問題が発生することがある。
  このため、どうしても :java:extdoc:`java.sql.Connection` を使わないと満たせない要件がない限り、この機能は使用しないこと。

以下に例を示す。

.. code-block:: java

  TransactionManagerConnection managerConnection = DbConnectionContext.getTransactionManagerConnection();
  Connection connection = managerConnection.getConnection();
  return connection.getMetaData();

拡張例
--------------------------------------------------

.. _database-add_connection_factory:

データベースへの接続法を追加する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
データベースの接続方法を追加する手順を説明する。
例えば、OSSのコネクションプールライブラリを使用する場合などは、この手順に従い作業すると良い。

#. :java:extdoc:`ConnectionFactorySupport <nablarch.core.db.connection.ConnectionFactorySupport>` を継承し、データベース接続を生成するクラスを作成する。
#. 作成したクラスをコンポーネント設定ファイルに設定する。( :ref:`database-connect` を参照)

.. _database-add_dialect:

ダイアレクトを追加する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ダイアレクトを追加する手順を説明する。

例えば、使用するデータベース製品に対応したダイアレクトがない場合や、特定機能の使用可否を切り替えたい場合にはダイアレクトを追加する必要がある。

#. :java:extdoc:`DefaultDialect <nablarch.core.db.dialect.DefaultDialect>` を継承し、 データベース製品に対応したダイアレクトを作成する。
#. 作成したダイアレクトをコンポーネント設定ファイルに設定する ( :ref:`database-use_dialect` を参照)

.. _database-change_exception:

データベースアクセス時の例外クラスを切り替える
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
データベースアクセス時の例外クラスを切り替える手順を説明する。

例えば、デッドロックエラーの例外クラスを変更したい場合には、この手順に従い作業すると良い。

#. データベースアクセスエラーを生成する :java:extdoc:`DbAccessExceptionFactory <nablarch.core.db.connection.DbAccessExceptionFactory>` の実装クラスを作成する。
#. SQL実行時エラーを生成する :java:extdoc:`SqlStatementExceptionFactory <nablarch.core.db.statement.SqlStatementExceptionFactory>` の実装クラスを作成する。
#. 作成したクラスをコンポーネント設定ファイルに定義する。

以下に詳細な手順を示す。

:java:extdoc:`DbAccessExceptionFactory <nablarch.core.db.connection.DbAccessExceptionFactory>` の実装クラスを作成する
  データベース接続取得時及びトランザクション制御時(commitやrollback)に発生させる :java:extdoc:`DbAccessException <nablarch.core.db.DbAccessException>` を変更したい場合は、
  このインタフェースの実装クラスを作成する。

:java:extdoc:`SqlStatementExceptionFactory <nablarch.core.db.statement.SqlStatementExceptionFactory>` の実装クラスを作成する
  SQL実行時に発生させる :java:extdoc:`SqlStatementException <nablarch.core.db.statement.exception.SqlStatementException>` を変更したい場合は、 このインタフェースの実装クラスを作成する。

コンポーネント設定ファイルに定義する
  :java:extdoc:`DbAccessExceptionFactory <nablarch.core.db.connection.DbAccessExceptionFactory>` の実装クラスは、 :ref:`database-connect`
  で定義したデータベース接続を取得するコンポーネントに設定する必要がある。

  .. code-block:: xml

    <component class="sample.SampleDbAccessExceptionFactory" />

  :java:extdoc:`SqlStatementExceptionFactory <nablarch.core.db.statement.SqlStatementExceptionFactory>` の実装クラスは、 :java:extdoc:`BasicStatementFactory <nablarch.core.db.statement.BasicStatementFactory>` に対して設定する。
  なお、 :java:extdoc:`BasicStatementFactory <nablarch.core.db.statement.BasicStatementFactory>` は、 :ref:`database-connect` で定義したデータベース接続を取得するコンポーネントに設定する必要がある。

  .. code-block:: xml

    <component name="statementFactory" class="nablarch.core.db.statement.BasicStatementFactory">
      <property name="sqlStatementExceptionFactory">
        <component class="sample.SampleStatementExceptionFactory" />
      </property>
    </component>

