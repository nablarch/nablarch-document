.. _message:

メッセージ管理
======================

.. contents:: 目次
  :depth: 3
  :local:

メッセージとは、画面の固定文言(項目タイトルなど)やエラーメッセージのことを指す。

画面の固定文言は、国際化の要件がなければJSPに直接埋め込んでも問題ない。

.. tip::

  メッセージは、安易に共通化せずに出来るだけ個別に定義すること。

  安易に共通化を行った場合、以下の問題が発生する可能性がある。

  例えば、他業務のメッセージに使えそうなメッセージがあるからとそのメッセージを使用したとする。
  他業務の仕様変更でそのメッセージが変更されると、そのメッセージを使っていた箇所に関係のないメッセージが表示される。

機能概要
--------------------------

メッセージの定義場所を指定できる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
メッセージは、データベースやプロパティファイルで管理できる。デフォルトでは、プロパティファイルでの管理となる。

プロパティファイルをデフォルトとしている理由は以下のとおり。

プロパティファイルで管理した場合、メッセージの追加・変更や確認を簡単に行える。
例えば、メッセージを追加する際にデータベースへinsertするよりも、プロパティファイルに行追加するほうがはるかに楽である。

プロパティファイルでの管理の詳細は以下を参照。

* :ref:`message-property_unit`
* :ref:`message-property_definition`

.. tip::
 メッセージの定義場所に関わらず、本機能では、アプリケーションの実行中に、メッセージを更新する機能は提供していない。
 メッセージを更新する場合は、アプリケーションの再起動が必要となる。

メッセージをフォーマットすることが出来る
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
メッセージは :java:extdoc:`java.text.MessageFormat` の拡張機能を使用してフォーマットする。
実行時に保持している値をメッセージに埋め込みたい場合は、 :ref:`message-format-spec` に従いパターン文字列を定義する。

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core</artifactId>
  </dependency>
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-message</artifactId>
  </dependency>

  <!-- メッセージをデータベースで管理する場合のみ -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-jdbc</artifactId>
  </dependency>

使用方法
---------------------------

.. _message-property_unit:

プロパティファイルの作成単位
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
アプリケーション単位に作成する。
1つのシステムであっても、社内向けとコンシューマ向けのアプリケーションがある場合は、それぞれにプロパティファイルを作成する。

アプリケーション単位に作成することで、メッセージの影響範囲をアプリケーション内に限定できるメリットがある。
（よくある、「そのアプリケーションで使っているとは思ってませんでした」による、障害を未然に防ぐことができる）

例
  コンシューマ向けアプリケーション
    consumer/main/resources/messages.properties

  社員向けアプリケーション
    intra/main/resources/messages.properties

.. _message-property_definition:

プロパティファイルにメッセージを定義する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
デフォルトの設定では、プロパティファイルのパスは ``classpath:messages.properties`` となる。

メッセージは、 :java:extdoc:`java.util.Properties` を使用してロードする。
なお、NablarchはJava6以上を想定しているため、 **UTF-8** で作成すればよくユニコード変換(native2ascii)は必要ない。

プロパティファイルの例
  .. code-block:: properties

    label.user.register.title=ユーザ登録画面
    errors.login.alreadyExist=入力されたログインIDは既に登録されています。別のログインIDを入力してください。
    errors.login=ログインに失敗しました。ログインIDまたはパスワードが誤っています。
    errors.compare.date={0}は{1}より後の日付を入力してください。
    success.delete.project=プロジェクトの削除が完了しました。
    success.update.project=プロジェクトの更新が完了しました。

.. _message-multi_lang:

多言語化対応を行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
メッセージの多言語化を行う場合には、言語ごとのプロパティファイルを用意し、サポートする言語を :java:extdoc:`PropertiesStringResourceLoader.locales <nablarch.core.message.PropertiesStringResourceLoader.setLocales(java.util.List)>` に設定する。
なお、デフォルトのロケールに対応する言語( `Locale.getDefault().getLanguage()` )については、サポートする言語に追加しなくても良い。

メッセージ取得時にどの言語が使用されるかは、 :java:extdoc:`ThreadContext#getLanguage <nablarch.core.ThreadContext.getLanguage()>` が返すロケールによって決定される。
もし、 :java:extdoc:`ThreadContext#getLanguage <nablarch.core.ThreadContext.getLanguage()>` からロケールが取得できない場合は :java:extdoc:`Locale.getDefault() <java.util.Locale.getDefault()>` が使用される。

  
PropertiesStringResourceLoaderへの言語設定
  サポートする言語として、 ``en`` 、 ``zh`` 、 ``de`` を設定する場合の例を示す。

  .. code-block:: xml

    <component class="nablarch.core.cache.BasicStaticDataCache" name="messageCache">
      <property name="loader">
        <!-- 多言語化したPropertiesStringResourceLoaderの定義 -->
        <component class="nablarch.core.message.PropertiesStringResourceLoader">
          <!-- サポートする言語 -->
          <property name="locales">
            <list>
              <value>en</value>
              <value>zh</value>
              <value>de</value>
            </list>
          </property>

          <!-- デフォルトの言語 -->
          <property name="defaultLocale" value="ja" />
        </component>
      </property>
    </component>

    <component name="stringResourceHolder" class="nablarch.core.message.StringResourceHolder">
      <!-- 多言語化したPropertiesStringResourceLoaderを持つBasicStaticDataCacheを設定する -->
      <property name="stringResourceCache" ref="messageCache" />
    </component>

    <component name="initializer" 
               class="nablarch.core.repository.initialization.BasicApplicationInitializer">
      <property name="initializeList">
        <list>
          <!-- BasicStaticDataCacheを初期化対象に追加する -->
          <component-ref name="messageCache" />
        </list>
      </property>
    </component>


言語ごとのプロパティファイルの作成
  上記の :java:extdoc:`PropertiesStringResourceLoader <nablarch.core.message.PropertiesStringResourceLoader>` に設定したサポート言語に対応するプロパティファイルの作成例を示す。

  :java:extdoc:`PropertiesStringResourceLoader <nablarch.core.message.PropertiesStringResourceLoader>` に設定した言語に対応するプロパティファイルを作成する。
  ファイル名は、 **messages_言語.properties** とする。

  デフォルトのロケールに対応するプロパティファイルは、言語を入れずに **messages.properties** として作成する。
  **messages.properties** が存在していない場合は、エラーとして処理を終了するので注意すること。

  .. code-block:: none

    main/resources/messages.properties       # デフォルトの言語に対応したファイル
                   messages_en.properties    # enに対応したファイル
                   messages_zh.properties    # zhに対応したファイル
                   messages_de.properties    # deに対応したファイル

メッセージを持つ業務例外を送出する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
プロパティファイルに設定されたメッセージを持つ業務例外( :java:extdoc:`ApplicationException <nablarch.core.message.ApplicationException>` ) を送出する例を示す。

プロパティファイルに設定されたメッセージを取得するには、 :java:extdoc:`MessageUtil <nablarch.core.message.MessageUtil>` クラスを使用する。
:java:extdoc:`MessageUtil <nablarch.core.message.MessageUtil>` から取得した :java:extdoc:`Message <nablarch.core.message.Message>` を元に業務例外( :java:extdoc:`ApplicationException <nablarch.core.message.ApplicationException>` )を生成し送出する。


プロパティファイル
  .. code-block:: properties

    errors.login.alreadyExist=入力されたログインIDは既に登録されています。別のログインIDを入力してください。

実装例
  .. code-block:: java

    Message message = MessageUtil.createMessage(MessageLevel.ERROR, "errors.login.alreadyExist");

    throw new ApplicationException(message);

.. _message-format-spec:

埋め込み文字を使用する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:java:extdoc:`java.text.MessageFormat` 形式での埋め込み文字に対応している。
メッセージに埋め込む値に :java:extdoc:`Map <java.util.Map>` のみを指定した場合は、
:java:extdoc:`java.text.MessageFormat` を使用せずに :java:extdoc:`Map <java.util.Map>` のキー値を元に値を埋め込む拡張機能を使用する。

埋め込み文字を使用する場合には、メッセージにパターン文字を使用し、メッセージ取得時に埋め込み文字を指定する。

埋め込み文字に :java:extdoc:`Map <java.util.Map>` 以外を使用した場合
  プロパティファイル
    :java:extdoc:`java.text.MessageFormat` の仕様に従い、メッセージを定義する。

    .. code-block:: properties

      success.upload.project={0}件のプロジェクトを登録しました。


  実装例
    `projects.size()` が **5** を返した場合、取得されるメッセージは「5件のプロジェクトを登録しました。」となる。

    .. code-block:: java

      MessageUtil.createMessage(MessageLevel.INFO, "success.upload.project", projects.size());

埋め込み文字に :java:extdoc:`Map <java.util.Map>` のみを使用した場合
  プロパティファイル
    埋め込み文字部分には、 :java:extdoc:`Map <java.util.Map>` のキー名を ``{`` 、 ``}`` で囲んで定義する。

    .. code-block:: properties

      success.upload.project={projectCount}件のプロジェクトを登録しました。

  実装例
    メッセージ取得時に指定する埋め込み文字に :java:extdoc:`Map <java.util.Map>` を指定する。

    `projects.size()` が **5** を返した場合、取得されるメッセージは「5件のプロジェクトを登録しました。」となる。

    .. code-block:: java

      Map<String, Object> options = new HashMap<>();
      options.put("projectCount", projects.size());

      MessageUtil.createMessage(MessageLevel.INFO, "success.upload.project", options);

    .. important:: 

      埋め込み文字に指定できる値は、 :java:extdoc:`Map <java.util.Map>` のみとなる。
      複数の :java:extdoc:`Map <java.util.Map>` や、 :java:extdoc:`Map <java.util.Map>` 以外の値とセットで指定された場合は、
      :java:extdoc:`java.text.MessageFormat` を使用した値の埋め込み処理をおこなう。



画面の固定文言をメッセージから取得する    
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
画面の固定文言にメッセージの値を出力したい場合は、カスタムタグライブラリの `message` タグを使用する。

`message` タグの詳細な使用方法は、 :ref:`tag-write_message` を参照。

プロパティファイル
  .. code-block:: properties

    login.title=ログイン

JSP
  .. code-block:: jsp

    <div class="title-nav">
      <span><n:message messageId="login.title" /></span>
    </div>

画面表示結果
  プロパティファイルに定義したメッセージが固定文言として表示される。

  .. image:: images/message/jsp_title.png

.. _message-level:

メッセージレベルを使い分ける
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
メッセージレベルを使い分けることで、画面表示時のスタイルを切り替えることができる。
スタイルの切り替えは、カスタムタグライブラリの `errors` タグを使用することで実現できる。

メッセージレベルは、 `INFO` 、 `WARN` 、 `ERROR` の3種類があり、
:java:extdoc:`MessageLevel <nablarch.core.message.MessageLevel>` に定義されている。

errorsタグを使用すると、メッセージレベルに応じて以下のcssクラスが適用される。
`errors` タグの詳細な使用方法は、 :ref:`tag-write_error` を参照。

:INFO: nablarch_info
:WARN: nablarch_warn
:ERROR: nablarch_error

.. tip::

  :doc:`バリデーション機能 <validation>` から送出される業務例外( :java:extdoc:`ApplicationException <nablarch.core.message.ApplicationException>` )が持つメッセージは、
  全て `ERROR` レベルとなる。


プロパティファイル
  .. code-block:: properties

    info=インフォメーション
    warn=ワーニング
    error=エラー

スタイルシート
  メッセージレベルに対応したスタイル定義を行う。

  .. code-block:: css

    .nablarch_info {
      color: #3333BB;
    }

    .nablarch_warn {
      color: #EA8128;
    }

    .nablarch_error {
      color: #ff0000;
    }

action class
  `errors` タグで出力するメッセージは、 :java:extdoc:`WebUtil.notifyMessages <nablarch.common.web.WebUtil.notifyMessages(nablarch.fw.ExecutionContext,%20nablarch.core.message.Message...)>` を使ってリクエストスコープに格納する。

  .. code-block:: java

    WebUtil.notifyMessages(context, MessageUtil.createMessage(MessageLevel.INFO, "info"));
    WebUtil.notifyMessages(context, MessageUtil.createMessage(MessageLevel.WARN, "warn"));
    WebUtil.notifyMessages(context, MessageUtil.createMessage(MessageLevel.ERROR, "error"));

JSP
  `errors` タグを使用して、 :java:extdoc:`WebUtil <nablarch.common.web.WebUtil>` に格納したメッセージを画面表示する。

  .. code-block:: jsp

    <n:errors />

画面表示結果
  メッセージレベルに応じてスタイルが切り替わっていることがわかる。

  .. image:: images/message/message_level.png


拡張例
--------------------------------------------------
プロパティファイル名や格納場所を変更する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:java:extdoc:`PropertiesStringResourceLoader <nablarch.core.message.PropertiesStringResourceLoader>` には、ファイル名やディレクトリのパスを変更するためのプロパティが用意されている。
デフォルト構成を変更したい場合は、これらのプロパティを用いて変更すること。



メッセージをデータベースで管理する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
メッセージをデータベースで管理するには :java:extdoc:`BasicStringResourceLoader <nablarch.core.message.BasicStringResourceLoader>` を使用してメッセージをロードする必要がある。

以下にデータベースで管理するメッセージを利用するための設定例を示す。

.. code-block:: xml

  <!-- データベースからメッセージをロードするコンポーネント -->
  <component name="stringResourceLoader" class="nablarch.core.message.BasicStringResourceLoader">
    <property name="dbManager" ref="defaultDbManager"/>
    <property name="tableName" value="MESSAGE"/>
    <property name="idColumnName" value="ID"/>
    <property name="langColumnName" value="LANG"/>
    <property name="valueColumnName" value="MESSAGE"/>
  </component>

  <!-- ロードしたメッセージをキャッシュするコンポーネント -->
  <component name="stringResourceCache" class="nablarch.core.cache.BasicStaticDataCache">
    <!-- ローダーには、データベースからメッセージをロードするクラスを指定する -->
    <property name="loader" ref="stringResourceLoader"/>
    <!-- 起動時に一括でロードする -->
    <property name="loadOnStartup" value="true"/>
  </component>

  <!--
  メッセージの元となる文字リソースを保持するコンポーネント
  コンポーネント名はstringResourceHolderとすること
  -->
  <component name="stringResourceHolder" class="nablarch.core.message.StringResourceHolder">
    <!-- メッセージをキャッシュするコンポーネントを指定する -->
    <property name="stringResourceCache" ref="stringResourceCache"/>
  </component>


