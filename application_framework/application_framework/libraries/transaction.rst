.. _transaction:

トランザクション管理
============================
.. contents:: 目次
  :depth: 3
  :local:

トランザクション制御が必要となるリソース（データベースやメッセージキュー）に対するトランザクション管理機能を提供する。

機能概要
--------------------------
各種リソースに対するトランザクション制御が出来る
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
データベースやメッセージキューといったトランザクション制御が必要となるリソースに対するトランザクション管理が出来る。

データベースに対するトランザクション制御の詳細は以下を参照。

* :ref:`transaction-database`
* :ref:`transaction-timeout`

新たなリソースに対して、トランザクション制御を行う要件が出た場合には、本機能で定められたインタフェースを実装することで容易に実現できる。
詳細は、 :ref:`transaction_addResource` を参照。

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-transaction</artifactId>
  </dependency>

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-jdbc</artifactId>
  </dependency>

使用方法
--------------------------------------------------

.. _transaction-database:

データベースに対するトランザクション制御を行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
コンポーネント定義ファイルにJDBCを使用したトランザクション制御を追加することで、データベースに対するトランザクション制御が実現出来る。
なお、データベースに対する接続設定が行われていることが前提となる。

データベース接続方法の詳細は、 :ref:`database-connect` を参照。

なお、1SQL単位などの粒度の小さいトランザクションを使用する場合は、 :ref:`database-new_transaction` を参照に設定及び実装を行うこと。

コンポーネント定義例
  JDBC用のトランザクションクラスを生成するファクトリクラス( :java:extdoc:`JdbcTransactionFactory <nablarch.core.db.transaction.JdbcTransactionFactory>` )をコンポーネント定義ファイルに設定する。

  .. code-block:: xml

    <!-- コンポーネントとしてJdbcTransactionFactoryを設定する -->
    <component class="nablarch.core.db.transaction.JdbcTransactionFactory">

      <!-- アイソレーションレベル -->
      <property name="isolationLevel" value="READ_COMMITTED" />

      <!-- トランザクションタイムアウト秒数 -->
      <property name="transactionTimeoutSec" value="15" />

    </component>

.. tip::

  上記に設定したクラスを直接使用することは基本的にない。
  トランザクション制御を必要とする場合には、 :ref:`transaction_management_handler` を使用すること。

.. _transaction-timeout:

データベースに対するトランザクションタイムアウトを適用する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:java:extdoc:`JdbcTransactionFactory <nablarch.core.db.transaction.JdbcTransactionFactory>` に対してトランザクションタイムアウト秒数を設定することで、トランザクションタイムアウト機能が有効となる。
もし、設定されたトランザクションタイムアウト秒数が0以下の場合には、トランザクションタイムアウト機能は無効化される。

.. tip::

  バッチアプリケーションなどの大量データを一括で処理するような機能では、トランザクションタイムアウト機能を使用するのではなく、
  ジョブスケジューラの終了遅延監視などで処理遅延のハンドリングを行うこと。

  なぜなら、バッチアプリケーションでは、全体の処理時間が想定内であればよく、個々のトランザクションで遅延が起きても問題ないからである。
  例えば、特定トランザクションがデータベースのリソース不足で1分かかったとしても、処理全体が想定時間内に終わっていれば問題ないと判断される。


トランザクションタイムアウトのチェックを開始するタイミング
  トランザクションの開始時( :java:extdoc:`Transaction#begin() <nablarch.core.transaction.Transaction.begin()>` )にチェックが開始される。

  複数のトランザクションを使用した場合（例えば、トランザクション内で別トランザクションを実行した場合）は、
  トランザクションごとにタイムアウトのチェックを行う。

トランザクションタイムアウトのチェックタイミング
  トランザクションタイムアウト秒数を超過したか否かは以下のタイミングでチェックする。

  SQL実行前
    SQL実行前にトランザクションタイムアウト秒数を超過していた場合は、 :java:extdoc:`TransactionTimeoutException <nablarch.core.transaction.TransactionTimeoutException>` を送出する。

    SQL実行前にチェックを行うのは、既にトランザクションタイムアウト秒数を経過していた場合に、
    データベースにアクセスすることはリソースを不必要に消費することになるため。

  SQL実行後
    SQL実行後にトランザクションタイムアウト秒数を超過していた場合は、 :java:extdoc:`TransactionTimeoutException <nablarch.core.transaction.TransactionTimeoutException>` を送出する。

    SQL実行中や結果セットの変換中にトランザクションタイムアウト秒数を超過する可能性があるため、
    SQLの実行が正常に終わった場合でもチェックを行っている。

  クエリータイムアウト例外発生時
    クエリータイムアウトを示す例外が発生した場合で、トランザクションタイムアウト秒数を超過していた場合は、 :java:extdoc:`TransactionTimeoutException <nablarch.core.transaction.TransactionTimeoutException>` を送出する。
    クエリータイムアウト例外か否かは、データベース機能の :ref:`ダイアレクト <database-dialect>` を用いて判定する。

    処理時間の長いSQL文(単純に重いSQLやロック開放待ちのSQL)が実行された場合、制御がデータベースから戻ってこない可能性がある。
    このため、トランザクションタイムアウトの残り秒数を `java.sql.Statement#setQueryTimeout` に設定し、
    トランザクションタイムアウト秒数超過時には強制的に実行をキャンセルしている。

    なお、SQL実行時にクエリータイムアウト時間が設定されていた場合は、
    設定済みのクエリータイムアウト時間よりトランザクションタイムアウトの残り秒数が小さい場合に、
    設定済みクエリータイムアウト時間をトランザクションタイムアウトの残り秒数で上書きする。

    クエリータイムアウトのハンドリング例を以下に示す。

    パターン1
      | 設定済みクエリータイムアウト時間: 10秒
      | トランザクションタイムアウトの残り秒数: 15秒
      | SQL実行時に設定するクエリータイムアウト時間: 10秒
      | クエリータイムアウト発生時にはトランザクションタイムアウトとはならずSQL実行時例外が送出される

    パターン2
      | 設定済みクエリータイムアウト時間: 10秒
      | トランザクションタイムアウトの残り秒数: 5秒
      | SQL実行時に設定するクエリータイムアウト時間: 5秒
      | クエリータイムアウト発生時にはトランザクションタイムアウトとなり、 :java:extdoc:`TransactionTimeoutException <nablarch.core.transaction.TransactionTimeoutException>` が送出される。

  .. tip::

    この機能は、データベースアクセス時にトランザクションタイムアウトチェックを行うため、
    データベースにアクセスしないロジックで処理遅延が発生した場合は、トランザクションタイムアウトとはならない。

    例えば、データベースアクセスを行わないロジックで無限ループが発生した場合は、本機能ではトランザクションタイムアウトを検出することはできない。
    このような場合には、アプリケーションサーバのタイムアウト機能などを用いて、遅延しているアプリケーションスレッドのハンドリングを行うこと。

トランザクションタイムアウト時間のリセットタイミング
  トランザクションを明示的に開始した場合( :java:extdoc:`Transaction#begin <nablarch.core.transaction.Transaction.begin()>` を呼び出した場合)に、トランザクションタイムアウト時間がリセットされる。
  トランザクションの終了時( :java:extdoc:`Transaction#commit <nablarch.core.transaction.Transaction.commit()>` や :java:extdoc:`Transaction#rollback <nablarch.core.transaction.Transaction.rollback()>` )では、
  トランザクションタイムアウトの残り時間はリセットされないので注意すること。

拡張例
--------------------------------------------------

.. _transaction_addResource:

トランザクション対象のリソースを追加する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
トランザクション対象のリソースを追加する場合は、以下の手順が必要となる。

例えば、IBMのWebSphere MQを分散トランザクションのトランザクションマネージャとしてトランザクション制御を行う場合などが該当する。

#. トランザクション実装の追加
#. トランザクションを生成するためのファクトリ実装の追加
#. :ref:`transaction_management_handler` を使ってトランザクション制御を実現

以下に詳細な手順を示す。

トランザクション実装の追加
  トランザクションは、 :java:extdoc:`Transaction <nablarch.core.transaction.Transaction>` インタフェースを実装し、
  トランザクション対象のリソースに対するトランザクションの開始、終了処理を実装する。

  .. code-block:: java

    public class SampleTransaction implements Transaction {

      private final String resourceName;

      // トランザクション制御対象のリソースを識別するための
      // リソース名を受け取る。
      // トランザクション制御時に、このリソース名からトランザクション制御対象のリソースを取得する必要がある。
      public SampleTransaction(String resourceName) {
        this.resourceName = resourceName;
      }

      @Override
      public void begin() {
        // トランザクション対象リソースに対するトランザクションの開始処理を実装する
      }

      @Override
      public void commit() {
        // トランザクション対象リソースに対するトランザクションの確定処理を実装する
      }

      @Override
      public void rollback() {
        // トランザクション対象リソースに対するトランザクションの破棄処理を実装する
      }
    }

トランザクションを生成するためのファクトリ実装の追加
  トランザクションを生成するためのファクトリクラスを作成する。
  ファクトリクラスは、 :java:extdoc:`TransactionFactory <nablarch.core.transaction.TransactionFactory>` を実装する。

  この例は、上記で作成した `SampleTransaction` を生成するファクトリクラスとなっている。

  .. code-block:: java

    public class SampleTransactionFactory implements TransactionFactory {

      @Override
      public Transaction getTransaction(String resourceName) {
        // トランザクション対象を識別するためのリソース名を持つ
        // トランザクションオブジェクトを生成し返却する。
        SampleTransaction transaction = new SampleTransaction(resourceName);
        return transaction;
      }
    }

:ref:`transaction_management_handler` を使ってトランザクション制御を実現
  Nablarchの標準ハンドラに含まれるトランザクション制御ハンドラを使うことでトランザクション制御が実現出来る。

  以下の例のように、追加したファクトリクラスを、トランザクション制御ハンドラに設定する。

  .. code-block:: xml

    <!-- トランザクション制御ハンドラ -->
    <component class="nablarch.common.handler.TransactionManagementHandler">

      <!-- トランザクションファクトリ -->
      <property name="transactionFactory">
        <component class="sample.SampleTransactionFactory" />
      </property>

   </component>

