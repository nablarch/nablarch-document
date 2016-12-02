.. _mail:

メール送信
==================================================

.. contents:: 目次
  :depth: 3
  :local:

.. |JavaMail| raw:: html

  <a href="https://javamail.java.net/nonav/docs/api/" target="_blank">JavaMail API(外部サイト、英語)</a>

メールを送信する機能を提供する。

この機能では、ディレードオンライン処理と呼ばれる方式を採用しており、
メール送信を即時に行うのではなく、一旦、メール送信要求をデータベースに格納しておき、
:ref:`常駐バッチ<nablarch_batch-resident_batch>` を使い非同期にメール送信を行う。

.. image:: images/mail/mail_system.png
  :scale: 60

この方式を採用した理由は以下の通り。

* メール送信要求を出すアプリケーションで、メール送信を業務トランザクションに含めることができる。
* メールサーバやネットワークの障害により、メール送信が失敗しても、アプリケーションの処理に影響を与えない。

この機能では、上記方式を実現するため、2つの機能を提供する。

* :ref:`メール送信要求をデータベースに登録する機能<mail-request>`
* :ref:`メール送信要求に基づいてメールを送信するバッチ機能<mail-send>`

アプリケーションがメール送信要求を出す毎に1つのメール送信要求を作成し、
メール送信要求1つにつきメールを1通送信する。

.. tip::
  本機能は、即時にメール送信を行うAPIは提供していない。
  この場合は、 |JavaMail| を直接使用すること。

機能概要
--------------------------------------------------

テンプレートを使った定型メールを送信できる。
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
システムのメール送信では、登録完了通知メールのように、同じ文言で、一部の項目のみ異なるメールを送信することが多い。
そこで、本機能では、テンプレートを用意しておき、プレースホルダを変換して、件名と本文を作成する機能を提供している。
機能の詳細は、 :ref:`mail-request` を参照。

キャンペーン通知のような大量メールの一斉送信には対応していない
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
本機能では、キャンペーン通知のような一斉送信には対応していない。
下記に当てはまる場合は、プロダクトの利用を推奨する。

* キャンペーン通知やメールマガジンなど、一括で大量のメールを送信する。
* 配信したメールの開封率、クリックカウントの効果を測定する。
* メールアドレスからクライアント(例えば、フィーチャーフォンか否か)を判別し、送信するメールを切り替える。

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-mail-sender</artifactId>
  </dependency>

  <!-- メール送信要求IDの採番に使用する -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-idgenerator</artifactId>
  </dependency>
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-idgenerator-jdbc</artifactId>
  </dependency>

使用方法
--------------------------------------------------

.. _`mail-settings`:

メール送信を使うための設定を行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
この機能では、データベースを使用してメール送信に使うデータを管理する。
テーブルのレイアウトは以下となる。

.. |br| raw:: html

   <br />

.. list-table:: メール送信要求
  :header-rows: 0
  :class: white-space-normal
  :widths: 24,18,58

  * - メール送信要求ID ``PK``
    - 文字列型
    - メール送信要求を一意に識別するID
  * - メール送信パターンID（任意項目）
    - 文字列型
    - メールの送信方法のパターンを識別するためのID。 |br| パターンを使用した未送信データの抽出をする場合に定義する。（ :ref:`未送信のデータを抽出する際の条件<mail-mail_send_pattern>` を参照）
  * - メール送信バッチのプロセスID（任意項目）
    - 文字列型
    - マルチプロセス実行時に各プロセスがレコードを悲観ロックするために使用するカラム。 |br| マルチプロセス実行する場合に定義する。（ :ref:`mail-mail_multi_process` を参照）
  * - 件名
    - 文字列型
    -
  * - 送信者メールアドレス
    - 文字列型
    - メールのFromヘッダに指定するメールアドレス
  * - 返信先メールアドレス
    - 文字列型
    - メールのReply-Toヘッダに指定するメールアドレス
  * - 差戻し先メールアドレス
    - 文字列型
    - メールのReturn-Pathヘッダに指定するメールアドレス
  * - 文字セット
    - 文字列型
    - メールのContent-Typeヘッダに指定する文字セット
  * - ステータス
    - 文字列型
    - メールの送信状態(未送信／送信済／送信失敗)を表すコード値
  * - 要求日時
    - タイムスタンプ型
    -
  * - 送信日時
    - タイムスタンプ型
    -
  * - 本文
    - 文字列型
    -

.. list-table:: メール送信先
  :header-rows: 0
  :class: white-space-normal
  :widths: 24,18,58

  * - メール送信要求ID ``PK``
    - 文字列型
    -
  * - 連番 ``PK``
    - 数値型
    - 一つのメール送信要求内の連番
  * - 送信先区分
    - 文字列型
    - メールの送信先区分(TO／CC／BCC)を表すコード値
  * - メールアドレス
    - 文字列型
    -

.. list-table:: メール添付ファイル
  :header-rows: 0
  :class: white-space-normal
  :widths: 24,18,58

  * - メール送信要求ID ``PK``
    - 文字列型
    -
  * - 連番 ``PK``
    - 数値型
    - 一つのメール送信要求内の連番
  * - 添付ファイル名
    - 文字列型
    -
  * - Content-Type
    - 文字列型
    -
  * - 添付ファイル
    - バイト配列型
    -

.. list-table:: メールテンプレート
  :header-rows: 0
  :class: white-space-normal
  :widths: 24,18,58

  * - メールテンプレートID ``PK``
    - 文字列型
    -
  * - 言語 ``PK``
    - 文字列型
    -
  * - 件名
    - 文字列型
    -
  * - 本文
    - 文字列型
    -
  * - 文字セット
    - 文字列型
    - メール送信時に指定する文字セット

メール送信を使うには、以下の設定を行う。

* :ref:`メール送信要求とメール送信バッチの共通設定<mail-common_settings>`
* :ref:`メール送信要求の設定<mail-mail_requester_settings>`
* :ref:`メール送信バッチの設定<mail-mail_sender_settings>`

.. _mail-common_settings:

メール送信要求とメール送信バッチの共通設定
 共通設定では、以下の設定を行う。

 * :ref:`テーブルスキーマ<mail-common_settings_table_schema>`
 * :ref:`コード値とメッセージ<mail-common_settings_mail_config>`

 .. _mail-common_settings_table_schema:

 テーブルスキーマ
  次のクラスの設定をコンポーネント定義に追加する。
  設定項目の詳細はリンク先のJavadocを参照。

  * :java:extdoc:`MailRequestTable<nablarch.common.mail.MailRequestTable>` (メール送信要求テーブル)
  * :java:extdoc:`MailRecipientTable<nablarch.common.mail.MailRecipientTable>` (メール送信先テーブル)
  * :java:extdoc:`MailAttachedFileTable<nablarch.common.mail.MailAttachedFileTable>` (添付ファイルテーブル)
  * :java:extdoc:`MailTemplateTable<nablarch.common.mail.MailTemplateTable>` (メールテンプレートテーブル)

  設定例を以下に示す。

  .. code-block:: xml

   <!-- メール送信要求テーブルのスキーマ -->
   <component name="mailRequestTable" class="nablarch.common.mail.MailRequestTable">
     <!-- テーブル名とカラム名を指定する。ここでは省略する。 -->
   </component>

   <!-- メール送信先テーブルのスキーマ -->
   <component name="mailRecipientTable" class="nablarch.common.mail.MailRecipientTable">
     <!-- テーブル名とカラム名を指定する。ここでは省略する。 -->
   </component>

   <!-- 添付ファイルテーブルのスキーマ -->
   <component name="mailAttachedFileTable" class="nablarch.common.mail.MailAttachedFileTable">
     <!-- テーブル名とカラム名を指定する。ここでは省略する。 -->
   </component>

   <!-- メールテンプレートテーブルのスキーマ -->
   <component name="mailTemplateTable" class="nablarch.common.mail.MailTemplateTable">
     <!-- テーブル名とカラム名を指定する。ここでは省略する。 -->
   </component>

   <!-- 初期化設定 -->
   <component name="initializer"
              class="nablarch.core.repository.initialization.BasicApplicationInitializer">
     <property name="initializeList">
       <list>
         <!-- 他のコンポーネントは省略 -->
         <component-ref name="mailRequestTable" />
         <component-ref name="mailRecipientTable" />
         <component-ref name="mailAttachedFileTable" />
         <component-ref name="mailTemplateTable" />
       </list>
     </property>
   </component>

 .. tip::

   MailRequestTableのmailSendPatternIdColumnNameプロパティ, sendProcessIdColumnNameプロパティは任意項目であり、機能を使用したい場合に設定する。
   mailSendPatternIdColumnNameプロパティについては :ref:`未送信のデータを抽出する際の条件<mail-mail_send_pattern>` を、
   sendProcessIdColumnNameプロパティについては :ref:`mail-mail_multi_process` を参照すること。

 .. _mail-common_settings_mail_config:

 コード値とメッセージ
  メール送信に使用するコード値、メッセージID、障害コードを設定する。
  :java:extdoc:`MailConfig<nablarch.common.mail.MailConfig>` の設定をコンポーネント定義に追加する。
  設定項目の詳細は、 :java:extdoc:`MailConfigのJavadoc<nablarch.common.mail.MailConfig>` を参照。

  設定例を以下に示す。

  .. code-block:: xml

   <component name="mailConfig" class="nablarch.common.mail.MailConfig">

     <!-- メール送信要求IDの採番対象識別ID -->
     <property name="mailRequestSbnId" value="MAIL_REQUEST_ID" />

     <!-- メールの送信先区分(TO／CC／BCC)を表すコード値 -->
     <property name="recipientTypeTO" value="0" />
     <property name="recipientTypeCC" value="1" />
     <property name="recipientTypeBCC" value="2" />

     <!-- メールの送信状態(未送信／送信済／送信失敗)を表すコード値 -->
     <property name="statusUnsent" value="0" />
     <property name="statusSent" value="1" />
     <property name="statusFailure" value="2" />

     <!-- メール送信要求件数出力時のメッセージID -->
     <property name="mailRequestCountMessageId" value="mail.request.count" />

     <!-- メール送信成功時のメッセージID -->
     <property name="sendSuccessMessageId" value="mail.send.success" />

     <!-- 送信失敗時の障害コード -->
     <property name="sendFailureCode" value="mail.send.failure" />

     <!-- 送信失敗時の終了コード -->
     <property name="abnormalEndExitCode" value="199" />

   </component>

.. _mail-mail_requester_settings:

メール送信要求の設定
 以下のクラスをコンポーネント定義に追加する。
 設定項目の詳細はリンク先のJavadocを参照。

 * :java:extdoc:`MailRequester<nablarch.common.mail.MailRequester>` (メール送信要求をデータベースに登録するコンポーネント)
 * :java:extdoc:`MailRequestConfig<nablarch.common.mail.MailRequestConfig>` (メール送信要求時の設定値を保持するクラス)

 :java:extdoc:`MailRequester<nablarch.common.mail.MailRequester>` は、
 メール送信要求をデータベースに登録する際、
 :ref:`採番<generator>` を使ってメール送信要求IDを生成する。
 そのため、 :ref:`採番<generator>` の設定も別途必要となる。

 設定例を以下に示す。

 ポイント
  * :java:extdoc:`MailRequester<nablarch.common.mail.MailRequester>` は名前でルックアップされるため、
    コンポーネント名に ``mailRequester`` と指定する。

 .. code-block:: xml

  <!-- メール送信要求コンポーネント。 -->
  <component name="mailRequester" class="nablarch.common.mail.MailRequester">

    <!-- メール送信要求時の設定値(以下のコンポーネント定義を参照) -->
    <property name="mailRequestConfig" ref="mailRequestConfig" />

    <!-- メール送信要求IDの採番に使用するIdGenerator -->
    <property name="mailRequestIdGenerator" ref="idGenerator" />

    <!-- テーブルのスキーマ -->
    <property name="mailRequestTable" ref="mailRequestTable" />
    <property name="mailRecipientTable" ref="mailRecipientTable" />
    <property name="mailAttachedFileTable" ref="mailAttachedFileTable" />
    <property name="mailTemplateTable" ref="mailTemplateTable" />

  </component>

  <!-- メール送信要求時の設定値 -->
  <component name="mailRequestConfig" class="nablarch.common.mail.MailRequestConfig">

    <!-- デフォルトの返信先メールアドレス -->
    <property name="defaultReplyTo" value="default.reply.to@nablarch.sample" />

    <!-- デフォルトの差戻し先メールアドレス -->
    <property name="defaultReturnPath" value="default.return.path@nablarch.sample" />

    <!-- デフォルトの文字セット -->
    <property name="defaultCharset" value="ISO-2022-JP" />

    <!-- 最大宛先数 -->
    <property name="maxRecipientCount" value="100" />

    <!-- 最大添付ファイルサイズ(byte数で記述) -->
    <property name="maxAttachedFileSize" value="2097152" />

  </component>

.. _mail-mail_sender_settings:

メール送信バッチの設定
 メール送信バッチが使用するSMTPサーバーへの接続情報を設定する。
 :java:extdoc:`MailSessionConfig<nablarch.common.mail.MailSessionConfig>` をコンポーネント定義に追加する。
 設定項目の詳細は、リンク先のJavadocを参照。

 設定例を以下に示す。

 .. code-block:: xml

  <component name="mailSessionConfig" class="nablarch.common.mail.MailSessionConfig">
    <property name="mailSmtpHost" value="localhost" />
    <property name="mailHost" value="localhost" />
    <property name="mailSmtpPort" value="25" />
    <property name="mailSmtpConnectionTimeout" value="100000" />
    <property name="mailSmtpTimeout" value="100000" />
  </component>

.. _`mail-request`:

メール送信要求を登録する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
メール送信要求の登録には、以下のクラスを使用する。

* :java:extdoc:`MailRequester<nablarch.common.mail.MailRequester>` (メール送信要求をデータベースに登録する)
* :java:extdoc:`MailUtil<nablarch.common.mail.MailUtil>` ( :java:extdoc:`MailRequester<nablarch.common.mail.MailRequester>` を取得する)
* :java:extdoc:`FreeTextMailContext<nablarch.common.mail.FreeTextMailContext>` (非定型メールの送信要求)
* :java:extdoc:`TemplateMailContext<nablarch.common.mail.TemplateMailContext>` (定型メールの送信要求)
* :java:extdoc:`AttachedFile<nablarch.common.mail.AttachedFile>` (添付ファイル)

この機能では、フリーフォーマットの非定型メールと、
予め登録しておいたテンプレートを使用する定型メールに対応しており、
それぞれに対応したクラスを使用して、メール送信要求を作成する。

ここでは、定型メールの実装例を以下に示す。

.. code-block:: java

 // メール送信要求を作成する。
 TemplateMailContext mailRequest = new TemplateMailContext();
 mailRequest.setFrom("from@tis.co.jp");
 mailRequest.addTo("to@tis.co.jp");
 mailRequest.addCc("cc@tis.co.jp");
 mailRequest.addBcc("bcc@tis.co.jp");
 mailRequest.setSubject("件名");
 mailRequest.setTemplateId("テンプレートID");
 mailRequest.setLang("ja");

 // テンプレートのプレースホルダに対する値を設定する。
 mailRequest.setReplaceKeyValue("name", "名前");
 mailRequest.setReplaceKeyValue("address", "住所");
 mailRequest.setReplaceKeyValue("tel", "電話番号");
 // 以下のように値にnullを設定した場合、空文字列で置き換えが行われる。
 mailRequest.setReplaceKeyValue("opeion", null);

 // 添付ファイルを設定する。
 AttachedFile attachedFile = new AttachedFile("text/plain", new File("path/to/file"));
 mailRequest.addAttachedFile(attachedFile);

 // メール送信要求を登録する。
 MailRequester requester = MailUtil.getMailRequester();
 String mailRequestId = requester.requestToSend(mailRequest);

.. important::
 定型メールで、テンプレートのプレースホルダに対する値を設定する場合は、以下の点に注意する。

 - キーに ``null`` を指定した場合は、例外を送出する。
 - 値に ``null`` を指定した場合、空文字列で置き換えを行う。
 - テンプレートのプレースホルダと、プレースホルダに対して設定されたキー/値の整合性をチェックしない。
   そのため、テンプレート中にプレースホルダがあるにも関わらず、値が設定されなかった場合、プレースホルダが変換されずにメールが送信される。
   反対に、対応するプレースホルダがない値は、単に無視され、メールが送信される。

.. _`mail-send`:

メールを送信する(メール送信バッチを実行する)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
メール送信バッチには、 :java:extdoc:`MailSender<nablarch.common.mail.MailSender>` を使用する。
:java:extdoc:`MailSender<nablarch.common.mail.MailSender>` は、 :ref:`常駐バッチ<nablarch_batch-resident_batch>`
を使用して動作させるバッチアクションとして作成している。

以下に実行例を示す。
実行方法の詳細については、 :ref:`main-run_application` を参照。

ポイント
 * requestPathオプションで :java:extdoc:`MailSender<nablarch.common.mail.MailSender>` を指定する。

.. code-block:: bash

 java nablarch.fw.launcher.Main \
   -diConfig file:./mail-batch-config.xml \
   -requestPath nablarch.common.mail.MailSender/SENDMAIL00 \
   -userId mailBatchUser

.. _`mail-mail_send_pattern`:

未送信のデータを抽出する際の条件
 :java:extdoc:`MailSender<nablarch.common.mail.MailSender>` は、
 メール送信要求テーブルから未送信のデータを抽出し、メール送信を行う。
 未送信のデータを抽出する際の条件は、次の2つから選択可能となっている。

  * テーブル全体から未送信のデータを抽出する
  * メール送信パターンID毎に未送信のデータを抽出する

 メール送信パターンIDを使うケースとしては、
 例えば、送信までの時間をできるだけ短くしたい優先度が高いメールと、
 1時間に1回程度の間隔で送信すればよい優先度の低いメールを扱うようなシステムが考えられる。

 メール送信パターンID毎に未送信のデータを抽出する場合には、
 監視対象のメール送信パターンID毎にメール送信バッチのプロセスを起動する。
 そのため、プロセス起動時には、処理対象のメール送信パターンID(mailSendPatternId)を起動引数に指定する。

 以下に実行例を示す。

 ポイント
  * ``mailSendPatternId`` という名前のオプションでメール送信パターンIDを指定する。

 .. code-block:: bash

  java nablarch.fw.launcher.Main \
    -diConfig file:./mail-batch-config.xml \
    -requestPath nablarch.common.mail.MailSender/SENDMAIL00 \
    -userId mailBatchUser
    -mailSendPatternId 02

.. _`mail-mail_multi_process`:

メール送信をマルチプロセス化する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 メール送信をマルチプロセス化する場合（例えば冗長構成のサーバで実行する場合）、
 メール送信要求テーブルのプロセスIDカラムを使用して悲観ロックを行い、複数のプロセスが同一の送信要求を処理しないようにする。
 この機能を利用するには、 次の設定が必要となる。
 
 1. メール送信要求テーブルにメール送信バッチのプロセスIDのカラムを定義する
 2. :java:extdoc:`MailRequestTable<nablarch.common.mail.MailRequestTable>` のsendProcessIdColumnNameのプロパティの値にメール送信バッチのプロセスIDのカラム名を設定し、コンポーネント定義に追加する
 3. メール送信バッチのプロセスID更新用のトランザクションを ``mailMultiProcessTransaction`` の名前でコンポーネント定義に追加する(トランザクションの設定方法は :ref:`database-new_transaction` を参照)

 .. important::
 
   2. の設定がされていない場合、排他制御がされないため１件のメール送信要求を複数プロセスが処理する可能性がある。
   しかし、見かけ上メール送信バッチが動作するため、設定漏れを検知しづらい。
   メール送信をマルチプロセス化する場合は上記の設定を漏れなく行うこと。
 
.. _`mail-mail_header_injection`:

メールヘッダインジェクション攻撃への対策
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
メールヘッダインジェクション攻撃への根本的対策として、以下の対策を実施する必要がある。

* メールヘッダは固定値を使用する。外部からの入力値を使用しない。
* プログラミング言語の標準APIを使用してメール送信を行う。Javaの場合は |JavaMail| を使用する。

メールヘッダは固定値を使用する。外部からの入力値を使用しない。
 これについては、プロジェクトで対応する。
 固定値にできない場合は、改行コードを変換するか、取り除く対応をプロジェクトで行う。

プログラミング言語の標準APIを使用してメール送信を行う。Javaの場合は |JavaMail| を使用する。
 本機能では |JavaMail| を利用している。
 しかし、 |JavaMail| を利用しても、一部のメールヘッダの項目に改行コードが含まれていてもメール送信可能な項目がある。
 そのため、保険的対策として、これらの項目に対して改行コードが含まれている場合にはメール送信を実施しないチェック機能を設けている。
 改行コードが含まれていた場合には、
 :java:extdoc:`InvalidCharacterException<nablarch.common.mail.InvalidCharacterException>`
 の送出およびログ出力(ログレベル: FATAL)を行い、該当のメールは送信処理を失敗として扱うこととする。

 この保険的対策は、脆弱性となる可能性のある以下の項目を対象としている。

 * 件名
 * 差し戻し先メールアドレス

拡張例
---------------------------------------------------------------------

電子署名を付加したりメール本文を暗号化するなどメール送信処理を変更する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:java:extdoc:`MailSender<nablarch.common.mail.MailSender>` は、
メール送信要求やテンプレートで指定された内容をそのまま送信する。
アプリケーション要件によっては、電子署名を付加したりメール本文を暗号化する必要が出てくる。

そのような場合は、 :java:extdoc:`MailSender<nablarch.common.mail.MailSender>`
を継承したクラスをプロジェクトで作成して対応する。
詳細は、 :java:extdoc:`MailSenderのJavadoc<nablarch.common.mail.MailSender>` を参照。
