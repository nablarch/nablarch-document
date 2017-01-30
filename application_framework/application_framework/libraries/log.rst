.. _log:

ログ出力
==================================================

.. contents:: 目次
  :depth: 3
  :local:

ログ出力を行う機能を提供する。

機能概要
--------------------------------------------------

ログ出力機能の実装を差し替えることができる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ログ出力は、３つの処理から構成されており、それぞれの実装を差し替えることができる。

  .. image:: images/log/log-structure.png

アプリケーションの要件に応じて、
:java:extdoc:`LogWriter <nablarch.core.log.basic.LogWriter>` や
:java:extdoc:`LogFormatter <nablarch.core.log.basic.LogFormatter>`
の単位で差し替えることもできるし、
これらだけでは要件を満たせなければ
:java:extdoc:`Logger <nablarch.core.log.Logger>` /
:java:extdoc:`LoggerFactory <nablarch.core.log.LoggerFactory>`
を実装してほぼ全ての処理を差し替えることもできる。

例えば、オープンソースのログ出力ライブラリを使用したい場合などは
:java:extdoc:`Logger <nablarch.core.log.Logger>` /
:java:extdoc:`LoggerFactory <nablarch.core.log.LoggerFactory>` を差し替えればよい。

なお、オープンソースで使用実績の多いロギングフレームワークは、専用のLogger/LoggerFactoryを既に用意している。

詳細は、:ref:`log_adaptor` を参照。

本機能と利用実績の多いlog4jとの機能比較は、 :ref:`log-functional_comparison` を参照。

ログ出力機能がデフォルトで提供しているクラスを示す。

Logger/LoggerFactory
 * :java:extdoc:`BasicLogger <nablarch.core.log.basic.BasicLogger>`
 * :java:extdoc:`BasicLoggerFactory <nablarch.core.log.basic.BasicLoggerFactory>`

.. _log-log_writers:

LogWriter
 * :java:extdoc:`FileLogWriter (ファイルへ出力。ファイルサイズによるローテーション) <nablarch.core.log.basic.FileLogWriter>`
 * :java:extdoc:`SynchronousFileLogWriter (複数プロセスから1ファイルへの出力) <nablarch.core.log.basic.SynchronousFileLogWriter>`
 * :java:extdoc:`StandardOutputLogWriter (標準出力へ出力) <nablarch.core.log.basic.StandardOutputLogWriter>`

.. _log-log_formatters:

LogFormatter
 * :java:extdoc:`BasicLogFormatter (パターン文字列によるフォーマット) <nablarch.core.log.basic.BasicLogFormatter>`

.. important::
 :java:extdoc:`SynchronousFileLogWriter <nablarch.core.log.basic.SynchronousFileLogWriter>`
 を使う場合は、 :ref:`log-synchronous_file_log_writer_attention` を参照すること。

.. tip::
 ログ出力機能で使用するログレベルについては、 :ref:`log-log_level` を参照。

各種ログの出力機能を予め提供している
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
本フレームワークでは、アプリケーションに共通で必要とされる各種ログの出力機能を予め提供している。
アプリケーションの要件に応じて、ログのフォーマットを設定で変更して使用できる。

.. toctree::
  :hidden:
  :glob:

  log/failure_log
  log/sql_log
  log/performance_log
  log/http_access_log
  log/messaging_log

.. list-table:: ログの種類
   :header-rows: 1
   :class: white-space-normal
   :widths: 20,80

   * - ログの種類
     - 説明

   * - :ref:`障害通知ログ <failure_log>`
     - 障害発生時に1次切り分け担当者を特定するのに必要な情報を出力する。

   * - :ref:`障害解析ログ <failure_log>`
     - 障害原因の特定に必要な情報を出力する。

   * - :ref:`SQLログ <sql_log>`
     - 深刻なパフォーマンス劣化の要因となりやすいSQL文の実行について、
       パフォーマンスチューニングに使用するために、SQL文の実行時間とSQL文を出力する。

   * - :ref:`パフォーマンスログ <performance_log>`
     - 任意の処理について、パフォーマンスチューニングに使用するために実行時間とメモリ使用量を出力する。

   * - :ref:`HTTPアクセスログ <http_access_log>`
     - ウェブアプリケーションで、アプリケーションの実行状況を把握するための情報を出力する。
       アプリケーションの性能測定に必要な情報、アプリケーションの負荷測定に必要な情報の出力も含む。
       さらに、アプリケーションの不正使用を検知するために、
       全てのリクエスト及びレスポンス情報を出力する証跡ログとしても使用する。

   * - :ref:`メッセージングログ <messaging_log>`
     - メッセージング処理において、メッセージ送受信の状況を把握するための情報を出力する。

.. tip::
 本フレームワークでは、 :ref:`障害通知ログ <failure_log>` と :ref:`障害解析ログ <failure_log>` を合わせて障害ログと呼ぶ。

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core</artifactId>
  </dependency>
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-applog</artifactId>
  </dependency>

  <!-- SQLログを使用する場合のみ -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-jdbc</artifactId>
  </dependency>

  <!-- HTTPアクセスログを使用する場合のみ -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>

  <!-- メッセージングログを使用する場合のみ -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-messaging</artifactId>
  </dependency>

使用方法
--------------------------------------------------

ログを出力する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ログの出力には :java:extdoc:`Logger <nablarch.core.log.Logger>` を使用する。
:java:extdoc:`Logger <nablarch.core.log.Logger>` は
:java:extdoc:`LoggerManager <nablarch.core.log.LoggerManager>` から取得する。

.. code-block:: java

 // クラスを指定してLoggerを取得する。
 // Loggerはクラス変数に保持する。
 private static final Logger LOGGER = LoggerManager.get(UserManager.class);

.. code-block:: java

 // ログの出力有無を事前にチェックし、ログ出力を行う。
 if (LOGGER.isDebugEnabled()) {
     String message = "userId[" + user.getId() + "],name[" + user.getName() + "]";
     LOGGER.logDebug(message);
 }

:java:extdoc:`Logger <nablarch.core.log.Logger>` の取得ではロガー名を指定する。
ロガー名には文字列またはクラスが指定できる。
クラスが指定された場合は、指定されたクラスのFQCNがロガー名となる。

.. important::
 アプリケーションにおいて、常にログを出力することになっているレベルは、
 ソースコードの可読性が落ちるため、事前チェックをしなくてよい。
 例えば、本番運用時に出力するログレベルをINFOレベルにするのであれば、
 FATALレベルからINFOレベルまでは事前チェックしなくてよい。

.. tip::
 ロガー名には、SQLログや監視ログなど、特定の用途向けのログ出力を行う場合は、
 その用途を表す名前(SQLやMONITOR等)を指定し、それ以外はクラスのFQCNを指定する。

.. _log-basic_setting:

ログ出力の設定を行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ログ出力の設定は、プロパティファイルに行う。

プロパティファイルの場所
 クラスパス直下の **log.properties** を使用する。
 場所を変更したい場合は、システムプロパティで **nablarch.log.filePath** をキーにファイルパスを指定する。
 ファイルパスの指定方法は
 :java:extdoc:`FileUtil#getResource <nablarch.core.util.FileUtil.getResource(java.lang.String)>` を参照。

 .. code-block:: bash

  >java -Dnablarch.log.filePath=classpath:nablarch/example/log.properties ...

プロパティファイルの記述ルール
 プロパティファイルの記述ルールを以下に示す。

 LoggerFactory
  \

  記述ルール
   \

   loggerFactory.className
    LoggerFactoryを実装したクラスのFQCNを指定する。
    本機能を使う場合は、 :java:extdoc:`BasicLoggerFactory <nablarch.core.log.basic.BasicLoggerFactory>` を指定する。

  記述例
   .. code-block:: properties

    # LoggerFactoryにより、ログ出力に使用する実装(本機能やLog4Jなど)が決まる。
    loggerFactory.className=nablarch.core.log.basic.BasicLoggerFactory

 LogWriter
  \

  記述ルール
   \

   writerNames
    使用する全てのLogWriterの名前を指定する。複数指定する場合はカンマ区切り。

   writer.<名前>.className
    LogWriterを実装したクラスのFQCNを指定する。

   writer.<名前>.<プロパティ名>
    LogWriter毎のプロパティに設定する値を指定する。
    指定できるプロパティについては使用するLogWriterのJavadocを参照。

  記述例
   .. code-block:: properties

    # 2つの名前を定義する。
    writerNames=appLog,stdout

    # appLogの設定を行う。
    writer.appLog.className=nablarch.core.log.basic.FileLogWriter
    writer.appLog.filePath=/var/log/app/app.log

    # stdoutの設定を行う。
    writer.stdout.className=nablarch.core.log.basic.StandardOutputLogWriter

 ロガー設定
  \

  記述ルール
   \

   availableLoggersNamesOrder
    使用する全てのロガー設定の名前を指定する。複数指定する場合はカンマ区切り。

    .. important::
     availableLoggersNamesOrderプロパティは、記述順に意味があるので注意すること。

     :java:extdoc:`Logger <nablarch.core.log.Logger>` の取得では、ログ出力を行うクラスが指定したロガー名に対して、
     ここに記述した順番で :java:extdoc:`Logger <nablarch.core.log.Logger>` のマッチングを行い、
     最初にマッチした :java:extdoc:`Logger <nablarch.core.log.Logger>` を返す。

     例えば、以下の記述例にあるavailableLoggersNamesOrderの記述順をavailableLoggersNamesOrder=root,sqlと記述した場合、
     全てのロガー取得がロガー設定 ``root`` にマッチしてしまう。
     その結果、ロガー名 ``SQL`` でログ出力しても ``sqlLog`` に出力されず、ロガー設定 ``root`` に指定された ``appLog`` に出力される。

     したがって、availableLoggersNamesOrderプロパティは、より限定的な正規表現を指定したロガー設定から順に記述すること。

    .. important::
     availableLoggersNamesOrderとloggers.*で指定するロガー設定の名称は、必ず一致させる必要がある。
     :java:extdoc:`BasicLoggerFactory <nablarch.core.log.basic.BasicLoggerFactory>` の初期処理で一致しているかチェックを行い、
     一致しない場合は例外をスローする。
     例えば、上記の設定にあるavailableLoggersNamesOrderから ``access`` を取り除くと、例外がスローされる。

     このチェックは、設定漏れの発生を防ぐために行っている。
     上記の設定にあるavailableLoggersNamesOrderから ``access`` を取り除いた場合は、明示的にloggers.access.*の設定も取り除く必要がある。

   loggers.<名前>.nameRegex
    ロガー名とのマッチングに使用する正規表現を指定する。
    正規表現は、ロガー設定の対象となるロガーを絞り込むために使用する。
    ロガーの取得時に指定されたロガー名(つまり :java:extdoc:`LoggerManager#get <nablarch.core.log.LoggerManager.get(java.lang.String)>`
    の引数に指定されたロガー名)に対してマッチングを行う。

   loggers.<名前>.level
    :java:extdoc:`LogLevel <nablarch.core.log.basic.LogLevel>` の名前を指定する。
    ここで指定したレベル以上のログを全て出力する。

   loggers.<名前>.writerNames
    出力先とするLogWriterの名前を指定する。
    複数指定する場合はカンマ区切り。
    ここで指定した全てのLogWriterに対してログの書き込みを行う。

  記述例
   .. code-block:: properties

    # 2つのロガー設定の名前を定義する。
    availableLoggersNamesOrder=sql,root

    # rootの設定を行う。
    loggers.root.nameRegex=.*
    loggers.root.level=WARN
    loggers.root.writerNames=appLog

    # sqlの設定を行う。
    loggers.sql.nameRegex=SQL
    loggers.sql.level=DEBUG
    loggers.sql.writerNames=sqlLog

プロパティファイルの記述例
 プロパティファイル全体の記述例を以下に示す。

 .. code-block:: properties

  loggerFactory.className=nablarch.core.log.basic.BasicLoggerFactory

  writerNames=appLog,sqlLog,monitorLog,stdout

  # アプリケーション用のログファイルの設定例
  writer.appLog.className=nablarch.core.log.basic.FileLogWriter
  writer.appLog.filePath=/var/log/app/app.log

  # SQL出力用のログファイルの設定例
  writer.sqlLog.className=nablarch.core.log.basic.FileLogWriter
  writer.sqlLog.filePath=/var/log/app/sql.log

  # 監視用のログファイルの設定例
  writer.monitorLog.className=nablarch.core.log.basic.FileLogWriter
  writer.monitorLog.filePath=/var/log/app/monitoring.log

  # 標準出力の設定例
  writer.stdout.className=nablarch.core.log.basic.StandardOutputLogWriter

  availableLoggersNamesOrder=sql,monitoring,access,validation,root

  # 全てのロガー名をログ出力の対象にする設定例
  # 全てのロガー取得を対象に、WARNレベル以上をappLogに出力する。
  loggers.root.nameRegex=.*
  loggers.root.level=WARN
  loggers.root.writerNames=appLog

  # 特定のロガー名をログ出力の対象にする設定例。
  # ロガー名に"MONITOR"を指定したロガー取得を対象に、
  # ERRORレベル以上をappLog,monitorLogに出力する。
  loggers.monitoring.nameRegex=MONITOR
  loggers.monitoring.level=ERROR
  loggers.monitoring.writerNames=appLog,monitorLog

  # 特定のロガー名をログ出力の対象にする設定例。
  # ロガー名に"SQL"を指定したロガー取得を対象に、
  # DEBUGレベル以上をsqlLogに出力する。
  loggers.sql.nameRegex=SQL
  loggers.sql.level=DEBUG
  loggers.sql.writerNames=sqlLog

  # 特定のクラスをログ出力の対象にする設定例。
  # ロガー名に"app.user.UserManager"を指定したロガー取得を対象に、
  # INFOレベル以上をappLogとstdoutに出力する。
  loggers.access.nameRegex=app\\.user\\.UserManager
  loggers.access.level=INFO
  loggers.access.writerNames=appLog,stdout

  # 特定のパッケージ以下をログ出力の対象にする設定例。
  # ロガー名に"nablarch.core.validation"から始まる名前を指定したロガー取得を対象に、
  # DEBUGレベル以上をstdoutに出力する。
  loggers.validation.nameRegex=nablarch\\.core\\.validation\\..*
  loggers.validation.level=DEBUG
  loggers.validation.writerNames=stdout

 .. tip::
  ロガー設定では、全てのログ出力にマッチするロガー設定を1つ用意し、availableLoggersNamesOrderの最後に指定することを推奨する。
  万が一設定が漏れた場合でも、重要なログの出力を逃してしまう事態を防ぐことができる。
  設定例としては、上記の記述例にあるロガー設定 ``root`` を参照。

ログ出力の設定を上書く
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ログ出力の設定は、システムプロパティを使用して、
プロパティファイルと同じキー名で値を指定することにより上書きすることができる。
これにより、共通のプロパティファイルを用意しておき、プロセス毎にログ出力設定を変更するといったことができる。

ロガー設定 ``root`` のログレベルをINFOに変更したい場合の例を以下に示す。

.. code-block:: bash

 >java -Dloggers.root.level=INFO ...

.. _log-log_format:

ログのフォーマットを指定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
本機能では、汎用的に使用できる :java:extdoc:`LogFormatter <nablarch.core.log.basic.LogFormatter>` として、
:java:extdoc:`BasicLogFormatter <nablarch.core.log.basic.BasicLogFormatter>` を提供している。

:java:extdoc:`BasicLogFormatter <nablarch.core.log.basic.BasicLogFormatter>` では、
プレースホルダを使用してフォーマットを指定する。
使用できるプレースホルダについては、
:java:extdoc:`BasicLogFormatter <nablarch.core.log.basic.BasicLogFormatter>`
のJavadocを参照。

フォーマットの設定例を以下に示す。
フォーマットはLogWriterのプロパティに指定する。

.. code-block:: properties

 # フォーマットを指定する場合はBasicLogFormatterを明示的に指定する。
 writer.appLog.formatter.className=nablarch.core.log.basic.BasicLogFormatter

 # プレースホルダを使ってフォーマットを指定する。
 writer.appLog.formatter.format=$date$ -$logLevel$- $loggerName$ $message$

 # 日時のフォーマットに使用するパターンを指定する。
 # 指定しなければ"yyyy-MM-dd HH:mm:ss.SSS"となる。
 writer.appLog.formatter.datePattern=yyyy/MM/dd HH:mm:ss[SSS]

 # ログレベルの文言を指定する。
 # 指定しなければLogLevel列挙型の名前(FATAL、INFOなど)となる。
 writer.appLog.formatter.label.fatal=F
 writer.appLog.formatter.label.error=E
 writer.appLog.formatter.label.warn=W
 writer.appLog.formatter.label.info=I
 writer.appLog.formatter.label.debug=D
 writer.appLog.formatter.label.trace=T

:java:extdoc:`BasicLogFormatter <nablarch.core.log.basic.BasicLogFormatter>`
では、出力されたログの状況を特定するために、以下の項目を出力できる。
これらの出力項目について説明しておく。

* :ref:`起動プロセス <log-boot_process>`
* :ref:`処理方式 <log-processing_system>`
* :ref:`実行時ID <log-execution_id>`

.. _log-boot_process:

起動プロセス
 起動プロセスとは、アプリケーションを起動した実行環境を特定するために使用する名前である。
 起動プロセスにサーバ名とJOBIDなどの識別文字列を組み合わせた名前を使用することで、
 同一サーバの複数プロセスから出力されたログの実行環境を特定することができる。
 起動プロセスは、プロジェクト毎にID体系などで体系を規定することを想定している。

 起動プロセスは、システムプロパティに ``nablarch.bootProcess`` というキーで指定する。
 システムプロパティの指定がない場合、起動プロセスはブランクとなる。

.. _log-processing_system:

処理方式
 処理方式とは、ウェブ、バッチなどを意味する。
 アプリケーションの処理方式を識別したい場合に、プロジェクト毎に規定して使用する。

 処理方式は、 :ref:`log-basic_setting` で説明したプロパティファイルに
 ``nablarch.processingSystem`` というキーで指定する。
 プロパティの指定がない場合はブランクとなる。

.. _log-execution_id:

実行時ID
 実行時IDとは、リクエストIDに対するアプリケーションの個々の実行を識別するためにつけるIDである。
 1つのリクエストIDに対して実行された数だけ実行時IDが発行されるため、
 リクエストIDと実行時IDの関係は1対多となる。

 実行時IDは、複数のログを出力している場合に、出力された複数のログを紐付けるために使用する。

 実行時IDは、各処理方式の :java:extdoc:`ThreadContext <nablarch.core.ThreadContext>`
 を初期化するタイミングで発行し、 :java:extdoc:`ThreadContext <nablarch.core.ThreadContext>` に設定される。

 実行時IDのID体系
  .. code-block:: properties

   # 起動プロセスは指定された場合のみ付加する。
   起動プロセス＋システム日時(yyyyMMddHHmmssSSS)＋連番(4桁)

.. important::
 リクエストID、実行時ID、ユーザIDを出力する場合は、
 これらの取得元が :java:extdoc:`ThreadContext <nablarch.core.ThreadContext>` なので、
 ハンドラ構成に :ref:`thread_context_handler` が含まれている必要がある。

改行コードとタブ文字を含めたい場合
 フォーマットに改行コードとタブ文字を含めたい場合は、以下に示すように、Javaと同様の記述を使用する。

 .. code-block:: properties

  改行コード \n
  タブ文字   \t

 改行コードは、Java標準のシステムプロパティに含まれる ``line.separator`` から取得する。
 このため、システムプロパティの ``line.separator`` を変更しなければOSの改行コードが使用される。

 .. tip::
  :java:extdoc:`BasicLogFormatter <nablarch.core.log.basic.BasicLogFormatter>` では
  ``\n`` と ``\t`` という文字列を出力することはできない。

.. _log-app_log_setting:

各種ログの設定を行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
各種ログの出力機能は、各種ログの用途に合わせたフォーマット処理のみを行っており、
ログの出力処理自体は本機能を使用している。
つまり、各種ログの出力機能では、 :java:extdoc:`Logger <nablarch.core.log.Logger>`
に指定するメッセージ作成を行う。

このため、各種ログの出力機能を使うには、 :ref:`log-basic_setting` に加えて、各種ログの設定が必要となる。
各種ログの設定は、プロパティファイルに行う。

プロパティファイルの場所
 クラスパス直下の **app-log.properties** を使用する。
 場所を変更したい場合は、システムプロパティで **nablarch.appLog.filePath** をキーにファイルパスを指定する。
 ファイルパスの指定方法は
 :java:extdoc:`FileUtil#getResource <nablarch.core.util.FileUtil.getResource(java.lang.String)>` を参照。

 .. code-block:: bash

  >java -Dnablarch.appLog.filePath=file:/var/log/app/app-log.properties ...

プロパティファイルの記述ルール
 各種ログごとに異なるので、以下を参照。

 * :ref:`failure_log-setting`
 * :ref:`sql_log-setting`
 * :ref:`performance_log-setting`
 * :ref:`http_access_log-setting`
 * :ref:`messaging_log-setting`


拡張例
---------------------------------------------------------------------

.. _log-add_log_writer:

LogWriterを追加する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
新しいLogWriterを追加する場合は、 :java:extdoc:`LogWriter <nablarch.core.log.basic.LogWriter>`
インタフェースを実装したクラスを作成する。
また、 :java:extdoc:`LogFormatter <nablarch.core.log.basic.LogFormatter>` を使用するLogWriterを作成する場合は、
共通処理を提供する :java:extdoc:`LogWriterSupport <nablarch.core.log.basic.LogWriterSupport>` を継承して作成する。

LogFormatterを追加する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
新しいLogFormatterを追加する場合は、 :java:extdoc:`LogFormatter <nablarch.core.log.basic.LogFormatter>`
インタフェースを実装したクラスを作成する。
また、ログレベルを表す文言を設定で変更可能にしたい場合は、
:java:extdoc:`LogLevelLabelProvider <nablarch.core.log.basic.LogLevelLabelProvider>` を使用する。

新しいLogFormatterの追加に伴い、ログ出力時に指定するパラメータを増やし、
LogFormatterで増やしたパラメータを受け取りたいことがある。
本機能では、ログ出力時に指定するパラメータを増やす目的で、
:java:extdoc:`Logger <nablarch.core.log.Logger>` インタフェースのログ出力メソッドに
Object型の可変長引数optionsを設けている。

.. code-block:: java

 // Logger#logInfoメソッドのシグネチャ
 public void logInfo(String message, Object... options)
 public void logInfo(String message, Throwable cause, Object... options)

ログ出力時のパラメータを増やしたい場合は、options引数を規定して使用すること。

ログの出力項目(プレースホルダ)を追加する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:java:extdoc:`BasicLogFormatter <nablarch.core.log.basic.BasicLogFormatter>` は、
:java:extdoc:`LogItem <nablarch.core.log.LogItem>` インタフェースを使用して、
各プレースホルダに対応する出力項目を取得する。
そのため、新規にプレースホルダを追加したい場合は、以下の作業を行う。

* :java:extdoc:`LogItem <nablarch.core.log.LogItem>` を実装したクラスを作る
* :java:extdoc:`BasicLogFormatter <nablarch.core.log.basic.BasicLogFormatter>` を継承したクラスを作り、プレースホルダを追加する

LogFormatterの設定から起動プロセスを取得するように変更する場合の例を示す。
LogFormatterの設定は、下記を想定する。

.. code-block:: properties

 # カスタムのLogFormatterを指定する。
 writer.appLog.formatter.className=nablarch.core.log.basic.CustomLogFormatter

 # フォーマットを指定する。
 writer.appLog.formatter.format=$date$ -$logLevel$- $loggerName$ [$bootProcess$] $message$

 # LogFormatterの設定で起動プロセスを指定する。
 # ここで指定した起動プロセスを$bootProcess$に出力する。
 writer.appLog.formatter.bootProcess=CUSTOM_PROCESS

:java:extdoc:`LogItem <nablarch.core.log.LogItem>` を実装したクラスを作る
 .. code-block:: java

  // カスタムの起動プロセスを取得するクラス。
  public class CustomBootProcessItem implements LogItem<LogContext> {

      private String bootProcess;

      public CustomBootProcessItem(ObjectSettings settings) {
          // LogFormatterの設定から起動プロセスを取得する。
          bootProcess = settings.getProp("bootProcess");
      }

      @Override
      public String get(LogContext context) {
          // 設定から取得した起動プロセスを返す。
          return bootProcess;
      }
  }

:java:extdoc:`BasicLogFormatter <nablarch.core.log.basic.BasicLogFormatter>` を継承したクラスを作り、プレースホルダを追加する
 .. code-block:: java

  public class CustomLogFormatter extends BasicLogFormatter {

      // フォーマット対象のログ出力項目を取得するメソッドをオーバーライドする。
      @Override
      protected Map<String, LogItem<LogContext>> getLogItems(ObjectSettings settings) {

          // 起動プロセスのプレースホルダを上書きで設定する。
          Map<String, LogItem<LogContext>> logItems = super.getLogItems(settings);
          logItems.put("$bootProcess$", new CustomBootProcessItem(settings));
          return logItems;
      }
  }

.. _log-synchronous_file_log_writer_attention:

SynchronousFileLogWriterを使用するにあたっての注意事項
--------------------------------------------------------------------------

.. important::
 :java:extdoc:`SynchronousFileLogWriter <nablarch.core.log.basic.SynchronousFileLogWriter>`
 には以下の制約があるため、利用にあたっては十分検討すること。

 * ログのローテーションができない。
 * 出力されるログの内容が正常でない場合がある。

:java:extdoc:`SynchronousFileLogWriter <nablarch.core.log.basic.SynchronousFileLogWriter>` は、
ロックファイルを用いて排他制御を行いながらファイルにログを書き込む。
そして、ロック取得の待機時間を超えてもロックを取得できない場合、強制的にロックファイルを削除し、
自身のスレッド用のロックファイルを生成してからログの出力を行う。

もし強制的にロックファイルを削除できない場合は、ロックを取得していない状態で強制的にログの出力を行う。
また、ロックファイルの生成に失敗した場合および、ロック取得待ちの際に割り込みが発生した場合も、
ロックを取得していない状態で強制的にログの出力を行う。

**ロックを取得しない状態で強制的にログを出力する場合に、複数プロセスからのログ出力が競合するとログが正常に出力されない場合がある点に注意すること。**

このような障害が発生した場合には、強制出力したログに加えて、同一のログファイルに障害のログを出力する。
デフォルトでは本フレームワークが用意したログが出力されるが、
:java:extdoc:`SynchronousFileLogWriter <nablarch.core.log.basic.SynchronousFileLogWriter>`
のプロパティに障害コードを設定することで、障害通知ログのフォーマット(障害コードを含む)でログを出力することができる。
障害通知ログのフォーマットで出力することで通常の障害通知ログと同様の方法でログの監視が可能となるので、
障害コードの設定を行うことを推奨する。

障害コードを設定するプロパティ名を以下に示す。

failureCodeCreateLockFile
 :障害の内容: ロックファイルが生成できない
 :ログレベル: FATAL
 :メッセージの設定例({0}にはロックファイルのパスが設定される): ロックファイルの生成に失敗しました。おそらくロックファイルのパスが間違っています。ロックファイルパス=[{0}]。
 :デフォルトで出力するログ(障害コードなどは出力されない): failed to create lock file. perhaps lock file path was invalid. lock file path=[{0}].

failureCodeReleaseLockFile
 :障害の内容: 生成したロックファイルを解放(削除)できない
 :ログレベル: FATAL
 :メッセージの設定例({0}にはロックファイルのパスが設定される): ロックファイルの削除に失敗しました。ロックファイルパス=[{0}]。
 :デフォルトで出力するログ(障害コードなどは出力されない): failed to delete lock file. lock file path=[{0}].

failureCodeForceDeleteLockFile
 :障害の内容: 解放されないロックファイルを強制削除できない
 :ログレベル: FATAL
 :メッセージの設定例({0}にはロックファイルのパスが設定される): ロックファイルの強制削除に失敗しました。ロックファイルが不正に開かれています。ロックファイルパス=[{0}]。
 :デフォルトで出力するログ(障害コードなどは出力されない): failed to delete lock file forcedly. lock file was opened illegally. lock file path=[{0}].

failureCodeInterruptLockWait
 :障害の内容: ロック取得待ちでスレッドをスリープしている際に、割り込みが発生
 :ログレベル: FATAL
 :メッセージの設定例: ロック取得中に割り込みが発生しました。
 :デフォルトで出力するログ(障害コードなどは出力されない): interrupted while waiting for lock retry.

.. important::
 障害コードを設定した場合、障害通知ログのフォーマットで同一のログファイルにログが出力されるが、
 障害解析ログは出力されない点に注意すること。

:java:extdoc:`SynchronousFileLogWriter <nablarch.core.log.basic.SynchronousFileLogWriter>`
の設定例を以下に示す。

.. code-block:: properties

 writerNames=monitorLog

 # SynchronousFileLogWriterクラスを指定する。
 writer.monitorLog.className=nablarch.core.log.basic.SynchronousFileLogWriter
 # 書き込み先のファイルパスを指定する。
 writer.monitorLog.filePath=/var/log/app/monitor.log
 # 書き込み時に使用する文字エンコーディングを指定する。
 writer.monitorLog.encoding=UTF-8
 # 出力バッファのサイズを指定する。(単位はキロバイト。1000バイトを1キロバイトと換算する。指定しなければ8KB)
 writer.monitorLog.outputBufferSize=8
 # ログフォーマッタのクラス名を指定する。
 writer.monitorLog.formatter.className=nablarch.core.log.basic.BasicLogFormatter
 # LogLevel列挙型の名称を指定する。ここで指定したレベル以上のログを全て出力する。
 writer.monitorLog.level=ERROR
 # ロックファイルのファイル名を指定する。
 writer.monitorLog.lockFilePath=/var/log/lock/monitor.lock
 # ロック取得の再試行間隔(ミリ秒)を指定する。
 writer.monitorLog.lockRetryInterval=10
 # ロック取得の待機時間(ミリ秒)を指定する。
 writer.monitorLog.lockWaitTime=3000
 # ロックファイルが生成できない場合の障害通知コードを指定する。
 writer.monitorLog.failureCodeCreateLockFile=MSG00101
 # 生成したロックファイルを解放(削除)できない場合の障害通知コードを指定する。
 writer.monitorLog.failureCodeReleaseLockFile=MSG00102
 # 解放されないロックファイルを強制削除できない場合の障害通知コードを指定する。
 writer.monitorLog.failureCodeForceDeleteLockFile=MSG00103
 # ロック待ちでスレッドをスリープしている際に、割り込みが発生した場合の障害通知コードを指定する。
 writer.monitorLog.failureCodeInterruptLockWait=MSG00104

.. important::

 maxFileSizeプロパティを指定するとログのローテーションが発生し、
 ログの出力が出来なくなることがあるので指定しないこと。


.. _log-log_level:

ログレベルの定義
--------------------------------------------------
本機能では、以下のログレベルを使用する。

.. list-table:: ログレベルの定義
   :header-rows: 1
   :class: white-space-normal
   :widths: 15,85

   * - ログレベル
     - 説明

   * - FATAL
     - アプリケーションの継続が不可能になる深刻な問題が発生したことを示す。
       監視が必須で即通報および即対応が必要となる。

   * - ERROR
     - アプリケーションの継続に支障をきたす問題が発生したことを示す。
       監視が必須であるが、通報および対応にFATALレベルほどの緊急性がない。

   * - WARN
     - すぐには影響を与えないが、放置しておくとアプリケーションの継続に支障をきたす問題になる恐れがある事象が発生したことを示す。
       できれば監視した方がよいが、ERRORレベルほどの緊急性がない。

   * - INFO
     - 本番運用時にアプリケーションの情報を出力するログレベル。アクセスログや統計ログが該当する。

   * - DEBUG
     - 開発時にデバッグ情報を出力するログレベル。SQLログや性能ログが該当する。

   * - TRACE
     - 開発時にデバッグ情報より、さらに細かい情報を出力したい場合に使用するログレベル。

ログレベルは、6段階とし、FATALからTRACEに向かって順にレベルが低くなる。
そして、ログ出力機能では、設定で指定されたレベル以上のログを全て出力する。
例えば、WARNレベルが設定で指定された場合は、FATALレベル,ERRORレベル,WARNレベルが指定されたログのみ出力する。

.. tip::
 本番運用時は、INFOレベルでログを出力することを想定している。
 ログファイルのサイズが肥大化しないように、プロジェクト毎にログの出力内容を規定すること。

.. tip::
 本フレームワークでも、ログ出力機能を使ってログを出力している。
 フレームワークが出力するログについては、 :ref:`log-fw_log_policy` を参照すること。

.. _log-fw_log_policy:

フレームワークのログ出力方針
--------------------------------------------------
本フレームワークでは、下記の出力方針に基づきログ出力を行う。

.. list-table:: フレームワークのログ出力方針
    :header-rows: 1
    :class: white-space-normal
    :widths: 15,85

    * - ログレベル
      - 出力方針

    * - FATAL/ERROR
      - 障害ログの出力時にFATAL/ERRORレベルで出力する。

        障害ログは、障害監視の対象であり、障害発生時の一時切り分けの起点ともなる為、
        原則として1件の障害に対して、1件の障害ログを出力する方針としている。

        このため、実行制御基盤では単一のハンドラ(例外を処理するハンドラ)により、
        障害通知ログを出力する方針としている。

    * - WARN
      - 障害発生時に連鎖して例外が発生した場合など、
        障害ログとして出力できない例外をWARNレベルで出力する。

        例えば、業務処理とトランザクションの終了処理の2つで例外が発生した場合は、
        業務処理の例外を障害ログに出力し、トランザクションの終了処理の例外をWARNレベルで出力する。

    * - INFO
      - アプリケーションの実行状況に関連するエラーを検知した場合にINFOレベルで出力する。

        例えば、URLパラメータの改竄エラーや認可チェックエラーが発生した場合にINFOレベルで出力する。

    * - DEBUG
      - アプリケーション開発時に使用するデバッグ情報を出力する。

        アプリケーション開発時は、DEBUGレベルを設定することで開発に必要な情報が出力されるよう考慮している。

    * - TRACE
      - フレームワーク開発時に使用するデバッグ情報を出力する。アプリケーション開発での使用は想定していない。

.. _log-functional_comparison:

log4jとの機能比較
--------------------------------------------------
ここでは、本機能と `log4j(外部サイト、英語) <http://logging.apache.org/log4j/1.2/>`_ との機能比較を示す。

.. list-table:: 機能比較（○：提供あり　△：一部提供あり　×：提供なし　－:対象外）
  :header-rows: 1
  :class: white-space-normal
  :widths: 50, 25, 25

  * - 機能
    - Nablarch
    - log4j

  * - ログの出力有無をログレベルで制御できる
    - ○
      |br|
      :ref:`解説書へ <log-basic_setting>`
    - ○

  * - ログの出力有無をカテゴリ(パッケージ単位や名前など)で制御できる
    - ○
      |br|
      :ref:`解説書へ <log-basic_setting>`
    - ○

  * - 1つのログを複数の出力先に出力できる
    - ○
      |br|
      :ref:`解説書へ <log-basic_setting>`
    - ○

  * - ログを標準出力に出力できる
    - ○
      |br|
      :ref:`解説書へ <log-log_writers>`
    - ○

  * - ログをファイルに出力できる
    - ○
      |br|
      :ref:`解説書へ <log-log_writers>`
    - ○

  * - ファイルサイズによるログファイルのローテーションができる
    - △ [#logrolate]_
      |br|
      :ref:`解説書へ <log-log_writers>`
    - ○

  * - 日時によるログファイルのローテーションができる
    - × [#extends_or_log4j]_
    - ○

  * - ログをメールで送信できる
    - × [#extends_or_log4j]_
    - ○

  * - ログをTelnetで送信できる
    - × [#extends_or_log4j]_
    - ○

  * - ログをSyslogで送信できる
    - × [#extends_or_log4j]_
    - ○

  * - ログをWindows NTのイベントログに追加できる
    - × [#extends_or_log4j]_
    - ○

  * - データベースにログを出力できる
    - × [#extends_or_log4j]_
    - ○

  * - ログを非同期で出力できる
    - × [#extends_or_log4j]_
    - ○

  * - ログのフォーマットをパターン文字列で指定できる
    - ○
      |br|
      :ref:`解説書へ <log-log_format>`
    - ○

  * - 障害ログを出力できる
    - ○
      |br|
      :ref:`解説書へ <failure_log>`
    - －

  * - HTTPアクセスログを出力できる
    - ○
      |br|
      :ref:`解説書へ <http_access_log>`
    - －

  * - SQLログを出力できる
    - ○
      |br|
      :ref:`解説書へ <sql_log>`
    - －

  * - パフォーマンスログを出力できる
    - ○
      |br|
      :ref:`解説書へ <performance_log>`
    - －

  * - メッセージングログを出力できる
    - ○
      |br|
      :ref:`解説書へ <messaging_log>`
    - －

.. [#logrolate] Nablarchのログ出力は、ファイルの世代管理を提供していないので、一部提供ありとしている。

.. [#extends_or_log4j] :ref:`log_adaptor` を使用する。
                       または、プロジェクトで作成する。作成方法は、 :ref:`log-add_log_writer` を参照。

.. |br| raw:: html

  <br />

