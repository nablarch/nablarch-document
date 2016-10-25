.. _bean_validation:

Bean Validation
==================================================
.. contents:: 目次
  :depth: 3
  :local:

この章では、Java EE7のBean Validation(JSR349)に準拠したバリデーション機能の解説を行う。

.. important::

  この機能は、Bean Validationのエンジンを実装しているわけではない。

  Java EE環境(WebLogicやWildFlyなど)では、そのサーバ内にバンドルされているBean Validationの実装が利用される。
  Java EE環境外で利用するには、別途Bean Validationの実装を参照ライブラリに追加する必要がある。
  (参照実装である `Hibernate Validator(外部サイト、英語) <http://hibernate.org/validator/>`_ を利用することを推奨する。)

機能概要
---------------------

ドメインバリデーションができる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ドメインごとにバリデーションルールを定義できる機能を提供する。

ドメインバリデーションを使うと、Beanのプロパティにはドメイン名の指定だけを行えばよく、バリデーションルールの変更が容易になる。

詳細は、 `ドメインバリデーションを使う`_ を参照。

.. _bean_validation-validator:

よく使われるバリデータが提供されている
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Nablarchでは、よく使われるバリデータが提供されているため、基本的なバリデーションは何かを作りこむことなく利用できる。

Nablarchで提供しているバリデータは以下のパッケージ内のアノテーション(注釈型)を参照。

* :java:extdoc:`nablarch.core.validation.ee`
* :java:extdoc:`nablarch.common.code.validator.ee`

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-validation-ee</artifactId>
  </dependency>
  
  <!--
   メッセージ管理を使用してメッセージを構築する場合のみ
   デフォルトでは、メッセージ管理が使用される
   -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-message</artifactId>
  </dependency>

  <!-- コード値のバリデータを使用する場合のみ -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-code</artifactId>
  </dependency>
  
  <!-- ウェブアプリケーションで使用する場合 -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>
  

使用方法
--------------------------------------------------

.. _bean_validation-configuration:

Bean Validationを使うための設定を行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Bean Validationを使うために必要となる設定を以下に示す。

MessageInterpolatorの設定
  Bean Validationでバリデーションエラーが発生した際のメッセージを構築するクラス( :java:extdoc:`MessageInterpolator <javax.validation.MessageInterpolator>` を実装したクラス)を設定する。

  設定を省略した場合(デフォルト)は、 :ref:`message` を使用する :java:extdoc:`NablarchMessageInterpolator <nablarch.core.validation.ee.NablarchMessageInterpolator>` が使用される。

  例えば、Hibernate Validatorのプロパティファイルからメッセージを構築する実装を使用する場合には、以下のように設定する。

  .. important::

    componentの名前は、必ず **messageInterpolator** とすること。

  .. code-block:: xml

    <!-- コンポーネント名にmessageInterpolatorを指定し、MessageInterpolatorの実装クラスを設定する -->
    <compnent name="messageInterpolator"
        class="org.hibernate.validator.messageinterpolation.ResourceBundleMessageInterpolator"/>

ドメインバリデーション用の設定
  :ref:`bean_validation-domain_validation` を参照

ウェブアプリケーションでBean Validationを使うための設定
  :ref:`bean_validation-web_application` を参照

バリデーションエラー時のエラーメッセージを定義する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`bean_validation-configuration` で説明したように、デフォルトでは :ref:`message` を使用してバリデーションエラー時のメッセージを構築する。
このため、メッセージの定義場所などの詳細は、 :ref:`message` を参照すること。

デフォルトの :java:extdoc:`NablarchMessageInterpolator <nablarch.core.validation.ee.NablarchMessageInterpolator>` を使用した場合のメッセージ定義ルールは以下のとおり。

* アノテーションの ``message`` 属性に指定された値が ``{`` 、``}`` で囲まれていた場合のみ :ref:`message` を使用してメッセージを構築する。
* メッセージテキスト内には、バリデーションのアノテーションの属性情報を埋め込むためのプレースホルダを使用できる。
  プレースホルダは、アノテーションの属性名を ``{`` 、 ``}`` で囲んで定義する。
* メッセージを動的に組み立てる式(例えばEL式)は使用できない。

以下に例を示す。

Java実装例
  .. code-block:: java

      public class SampleForm {

        @Length(max = 10)
        @SystemChar(charsetDef = "全角文字")
        @Required
        private String userName;

        @Length(min = 8, max = 8)
        @SystemChar(charsetDef = "半角数字")
        private String birthday;

        // getter、setterは省略
      }

メッセージ定義例
  アノテーションで指定されているメッセージIDをキーにメッセージを定義する。
  アノテーションのmessage属性を指定していない場合は、デフォルト値がメッセージIDとなる。

  .. code-block:: properties

    # Lengthアノテーションに対応したメッセージ
    # Lengthアノテーションのminやmax属性に指定した値をメッセージに埋め込むことが出来る
    nablarch.core.validation.ee.Length.min.message={min}文字以上で入力してください。
    nablarch.core.validation.ee.Length.max.message={max}文字以内で入力してください。
    nablarch.core.validation.ee.Length.min.max.message={min}文字以上{max}文字以内で入力してください。

    # SystemCharに対応したメッセージ
    nablarch.core.validation.ee.SystemChar.message={charsetDef}を入力してください。

.. tip:: 
  :ref:`bean_validation-configuration` で、デフォルト動作を変更している場合には、
  :java:extdoc:`MessageInterpolator <javax.validation.MessageInterpolator>` の実装に従いメッセージを定義すること。


バリデーションルールの設定方法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
バリデーションルールは、アノテーションをFieldかProperty(getter)に設定することで指定できる。
なお、setterにはアノテーションを指定できないので注意すること。(指定しても意味が無い(無視する))

.. _bean_validation-form_property:

.. tip::

  Beanクラスのプロパティの型は全てStringとして定義すること。

  Bean Validationでは、入力値をBeanに変換した後でバリデーションが実施される。
  このため、外部からどのような値が入力値として送られてきても、必ずBeanに変換する必要がある。

  もし、String以外のプロパティが存在していて、不正な値が送信された場合（例えば、数値型に対して英字が送信された場合)に、
  バリデーション実施前に行うBeanへの変換処理が失敗し、予期せぬ例外が送出され障害となってしまう。

  本来であれば、どのような値が入力されたとしても障害とするのではなく、バリデーションの結果を外部（例えば画面）に対して通知すべきである。

  外部からの値をString以外の型に変換したい場合には、バリデーション実施後に変換すること。

  クライアントサイドでJavaScriptを用いてバリデーションを行っている場合でも、
  サーバサイドにはバリデーション済みの値が送信される保証はないため、プロパティは必ず `String` とすること。
  なぜなら、クライアントサイドではユーザによりJavaScriptの無効化やブラウザの開発者ツールを用いた改竄が容易に行えるためである。
  このような操作が行われた場合、クライアントサイドバリデーションをすり抜け、サーバサイドに不正な値が送られる可能性がある。

実装例
  :ref:`Nablarchで提供しているバリデータ <bean_validation-validator>` を参照し、アノテーションを設定する。

  .. tip::

    個別にアノテーションを設定した場合、実装時のミスが増えたりメンテナンスコストが大きくなるため、
    後述する :ref:`ドメインバリデーション <bean_validation-domain_validation>` を使うことを推奨する。

  .. code-block:: java

    public class SampleForm {

      @Length(max = 10)
      @SystemChar(charsetDef = "全角文字")
      @Required
      private String userName;

      @Length(min = 8, max = 8)
      @SystemChar(charsetDef = "半角数字")
      private String birthday;

      // getter、setterは省略
    }

.. _bean_validation-domain_validation:

ドメインバリデーションを使う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ドメインバリデーションを使うための設定や実装例を示す。

ドメインごとのバリデーションルールを定義したBeanの作成
  ドメインバリデーションを利用するには、まずドメインごとのバリデーションルールを持つBean(ドメインBean)を作成する。

  このBeanクラスには、ドメインごとのフィールドを定義し、フィールドに対してアノテーションを設定する。
  フィールド名がドメイン名となる。以下の例では ``name`` と ``date`` の２つのドメインが定義されている。

  .. tip::

   必須項目を表す :java:extdoc:`@Required <nablarch.core.validation.ee.Required>` アノテーションは、ドメインBeanに設定するのではなく個別のBean側に設定すること。
   必須かどうかはドメイン側で強制できるものではなく、機能の設計によるため。

  .. code-block:: java

    package sample;

    import nablarch.core.validation.ee.Length;
    import nablarch.core.validation.ee.SystemChar;

    public class SampleDomainBean {

        @Length(max = 10)
        @SystemChar(charsetDef = "全角文字")
        String name;

        @Length(min = 8, max = 8)
        @SystemChar(charsetDef = "半角数字")
        String date;

    }

ドメインBeanを有効化
  ドメインBeanを有効化するには、 :java:extdoc:`DomainManager <nablarch.core.validation.ee.DomainManager>` 実装クラスを作成する。
  :java:extdoc:`getDomainBean <nablarch.core.validation.ee.DomainManager.getDomainBean()>` では、ドメインBeanのクラスオブジェクトを返す。

  .. code-block:: java

    package sample;

    public class SampleDomainManager implements DomainManager<SampleDomainBean> {
      @Override
      public Class<SampleDomainBean> getDomainBean() {
          // ドメインBeanのClassオブジェクトを返す
          return SampleDomainBean.class;
      }
    }


  :java:extdoc:`DomainManager <nablarch.core.validation.ee.DomainManager>` 実装クラスの `SampleDomainBean` をコンポーネント定義ファイルに設定することで、
  `SampleDomainBean` を使用したドメインバリデーションが有効となる。

  .. code-block:: xml

    <!-- DomainManager実装クラスは、domainManagerという名前で設定すること -->
    <component name="domainManager" class="sample.SampleDomainManager"/>

各Beanでドメインバリデーションを使う
  Beanのバリデーション対象プロパティに :java:extdoc:`@Domain <nablarch.core.validation.ee.Domain>` アノテーションを設定することで、ドメインバリデーションが行われる。

  この例では、 `userName` に対して `SampleDomainBean` の `name` フィールドに設定したバリデーションが行われる。
  同じように `birthday` に対しては、 `date` フィールドに設定したバリデーションが行われる。

  ※userNameは必須項目となる。

  .. code-block:: java

    public class SampleForm {

      @Domain("name")
      @Required
      private String userName;

      @Domain("date")
      private String birthday;

      // getter、setterは省略
    }

.. _bean_validation-system_char_validator:

文字種バリデーションを行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
システム許容文字のバリデーション機能を使用することで、文字種によるバリデーションを行うことが出来る。

文字種によるバリデーションを行うには、文字種毎に許容する文字のセットを定義する。
例えば、半角数字という文字種には、半角の ``0`` から ``9`` を許容するといった定義が必要となる。

以下に文字種毎の許容文字セットの定義方法を示す。

コンポーネント定義に許容文字のセットを定義する
  許容文字のセットは、以下のクラスの何れかを使って登録する。
  登録する際には、コンポーネント名には文字種を表す任意の名前を設定すること。

  * :java:extdoc:`RangedCharsetDef <nablarch.core.validation.validator.unicode.RangedCharsetDef>` (範囲で許容文字セットを登録する場合に使用する)
  * :java:extdoc:`LiteralCharsetDef <nablarch.core.validation.validator.unicode.LiteralCharsetDef>` (リテラルで許容文字を全て登録する場合に使用する)
  * :java:extdoc:`CompositeCharsetDef <nablarch.core.validation.validator.unicode.CompositeCharsetDef>` (複数のRangedCharsetDefやLiteralCharsetDefからなる許容文字を登録する場合に使用する)

  設定例は以下のとおり。

  .. code-block:: xml

    <!-- 半角数字 -->
    <component name="半角数字" class="nablarch.core.validation.validator.unicode.LiteralCharsetDef">
      <property name="allowedCharacters" value="01234567890" />
      <property name="messageId" value="numberString.message" />
    </component>

    <!-- ASCII(制御コードを除く) -->
    <component name="ascii" class="nablarch.core.validation.validator.unicode.RangedCharsetDef">
      <property name="startCodePoint" value="U+0020" />
      <property name="endCodePoint" value="U+007F" />
      <property name="messageId" value="ascii.message" />
    </component>

    <!-- 英数字 -->
    <component name="英数字" class="nablarch.core.validation.validator.unicode.CompositeCharsetDef">
      <property name="charsetDefList">
        <list>
          <!-- 半角数字の定義 -->
          <component-ref name="半角数字" />

          <!-- 半角英字の定義 -->
          <component class="nablarch.core.validation.validator.unicode.LiteralCharsetDef">
            <property name="allowedCharacters"
                value="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" />
          </component>
        </list>
      </property>
      <property name="messageId" value="asciiAndNumberString.message" />
    </component>

アノテーションで文字種を指定する
  文字種バリデーションを行うプロパティには、 :java:extdoc:`@SystemChar <nablarch.core.validation.ee.SystemChar>` アノテーションを設定する。
  このアノテーションの :java:extdoc:`charsetDef <nablarch.core.validation.ee.SystemChar.charsetDef()>` 属性には、許容する文字種を表す名前を設定する。
  この名前は、上記のコンポーネント定義ファイルに文字種セットを登録した際のコンポーネント名となる。

  この例では、 ``半角数字`` を指定しているので、上記のコンポーネント定義に従い「0123456789」が許容される。

  .. code-block:: java

    public class SampleForm {

        @SystemChar(charsetDef = "半角数字")
        public void setAccountNumber(String accountNumber) {
            this.accountNumber = accountNumber;
        }
    }

.. tip::

  許容する文字セットの文字数が大きくなった場合、後方に定義されている文字のチェックには時間を要する。(単純に前方から順に文字セットに含まれるかをチェックするため)
  この問題を解決するために、一度チェックした文字の結果をキャッシュする仕組みを提供している。

  ※原則キャッシュ機能は使わずに開発を進め、どうしても文字種バリデーションがボトルネックとなる場合に、キャッシュ機能を使うか否か検討すると良い。

  使い方は単純で、以下のコンポーネント定義のように、オリジナルの文字種セットの定義を、
  キャッシュ用の :java:extdoc:`CachingCharsetDef <nablarch.core.validation.validator.unicode.CachingCharsetDef>` に設定するだけである。

  .. code-block:: xml

    <component name="半角数字" class="nablarch.core.validation.validator.unicode.CachingCharsetDef">
      <property name="charsetDef">
        <component class="nablarch.core.validation.validator.unicode.LiteralCharsetDef">
          <property name="allowedCharacters" value="01234567890" />
        </component>
      </property>
      <property name="messageId" value="numberString.message" />
    </component>

.. _bean_validation-correlation_validation:

相関バリデーションを行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
複数の項目を使用した相関バリデーションを行うには、Bean Validationの :java:extdoc:`@AssertTrue <javax.validation.constraints.AssertTrue>` アノテーションを使用する。

実装例
  この例では、メールアドレスと確認用メールアドレスが一致していることを検証している。
  検証エラーとなった場合は、 `message` プロパティに指定したメッセージがエラーメッセージとなる。

  .. code-block:: java

    public class SampleForm {
      private String mailAddress;

      private String confirmMailAddress;

      @AssertTrue(message = "{compareMailAddress}")
      public boolean isEqualsMailAddress() {
        return Objects.equals(mailAddress, confirmMailAddress);
      }
    }

.. important::

  Bean Validationでは、バリデーションの実行順序は保証されないため、
  項目単体のバリデーションよりも前に相関バリデーションが呼び出される場合がある。

  このため、相関バリデーションでは項目単体のバリデーションが実行されていない場合でも、
  予期せぬ例外が発生しないようにバリデーションのロジックを実装する必要がある。

  例えば、上記の例で `mailAddress` 及び `confirmMailAddress` が任意項目の場合は、
  未入力の場合にはバリデーションを実行せずに、結果を戻す必要がある。

  .. code-block:: java
    
    @AssertTrue(message = "{compareMailAddress}")
    public boolean isEqualsMailAddress() {
      if (StringUtil.isNullOrEmpty(mailAddress) || StringUtil.isNullOrEmpty(confirmMailAddress)) {
        // どちらかが未入力の場合は、相関バリデーションは実施しない。(バリデーションOKとする)
        return true;
      }
      return Objects.equals(mailAddress, confirmMailAddress);
    }


.. _bean_validation-database_validation:

データベースとの相関バリデーションを行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
データベースとの相関バリデーションは、以下理由により業務アクション側で実装すること。

理由
  Bean Validationを使ってデータベースに対する相関バリデーションを実施した場合、
  バリデーション実施前の安全ではない値を使ってデータベースアクセスを行うことになる。
  (Bean Validation実行中のオブジェクトの値は、安全である保証がない。)
  これは、SQLインジェクションなどの脆弱性の原因となるため、さけるべき実装であるため。

  バリデーション実行後に業務アクションでバリデーションを行うことで、
  バリデーション済みの安全な値を使用してデータベースへアクセスできる。

.. _bean_validation-create_message_for_property:

特定の項目に紐づくバリデーションエラーのメッセージを作りたい
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`データベースとの相関バリデーション <bean_validation-database_validation>` のようにアクションハンドラで行うバリデーションでエラーが発生した場合に、
画面上で対象項目をエラーとしてハイライト表示したい場合がある。

この場合には、下記の実装例のように :java:extdoc:`ValidationUtil#createMessageForProperty <nablarch.core.validation.ValidationUtil.createMessageForProperty(java.lang.String, java.lang.String, java.lang.Object...)>`
を使用してエラーメッセージを構築し、 :java:extdoc:`ApplicationException <nablarch.core.message.ApplicationException>` を送出する。

.. code-block:: java

  throw new ApplicationException(
          ValidationUtil.createMessageForProperty("form.mailAddress", "duplicate.mailAddress"));


一括登録のようなBeanの複数入力を行う機能でバリデーションを行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
一括登録のように同一の情報を複数入力するケースがある。
このような場合には、バリデーション対象のBeanに対してネストしたBeanを定義することで対応する。

.. tip::
  これはBean Validationの仕様のため、詳細はBean Validationの仕様を参照すること。

以下に例を示す。

.. code-block:: java

  // 一括入力された全ての情報を保持するForm
  public class SampleBulkForm {

    // ネストしたBeanに対してもバリデーションを実行することを
    // しめすValidアノテーションを設定する。
    @Valid
    private List<SampleForm> sampleForm;

    public SampleBulkForm() {
      sampleForm = new ArrayList<>();
    }

    // setter、getterは省略
  }


  // 一括入力された情報の1入力分の情報を保持するForm
  public class SampleForm {
    @Domain("name")
    private String name;

    // setter、getterは省略
  }

ネストしたBeanをバリデーションする際の注意点
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ブラウザの開発者ツールでhtmlを改竄されたり、Webサービスで不正なJsonやXMLを受信した際にネストしたBeanの情報が送信されない場合がある。
この場合、ネストしたBeanが未初期化状態(null)となり、バリデーション対象とならない問題がある。
このため、確実にネストしたBeanの状態がバリデーションされるよう実装を行う必要がある。

以下に幾つかの実装例を示す。

親BeanとネストしたBeanが1対Nの場合
  ネストしたBeanをバリデーション対象にし、親のBean初期化時にネストしたBeanのフィールドも初期化する。
  ネストしたBeanの情報が必須(最低1つは選択 or 入力されていること)の場合は、
  :java:extdoc:`Size <nablarch.core.validation.ee.Size>` アノテーションを設定する。
  
  .. code-block:: java

    // Sizeアノテーションを設定することで、必ず1つは選択されていることをバリデーションする。
    @Valid
    @Size(min = 1, max = 5)
    private List<SampleNestForm> sampleNestForms;

    public SampleForm() {
      // インスタンス作成時にネストしたBeanのフィールドを初期化する
      sampleNestForms = new ArrayList<>();
    }

親BeanとネストしたBeanが1対1の場合
  BeanをネストさせずにフラットなBeanにできないか検討すること。
  接続先からの要求で対応できない場合には、ネストしたBeanに対するバリデーションが確実に実行されるよう実装を行うこと。

  .. code-block:: java
  
    // ネストしたBeanをバリデーション対象にする
    @Valid
    private SampleNestForm sampleNestForm;

    public SampleForm() {
      // インスタンス作成時にネストしたBeanのフィールドを初期化する
      sampleNestForm = new SampleNestForm();
    }


.. _bean_validation-web_application:

ウェブアプリケーションのユーザ入力値のチェックを行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ウェブアプリケーションのユーザ入力値のチェックは :ref:`inject_form_interceptor` を使用して行う。
詳細は、 :ref:`inject_form_interceptor` を参照。

:ref:`inject_form_interceptor` でBean Validationを使用するためには、コンポーネント定義ファイルへの設定が必要となる。
以下例のように、 :java:extdoc:`BeanValidationStrategy <nablarch.common.web.validator.BeanValidationStrategy>` を ``validationStrategy`` という名前でコンポーネント定義すること。

.. code-block:: xml

  <component name="validationStrategy" class="nablarch.common.web.validator.BeanValidationStrategy" />

.. tip::

  BeanValidationStrategyでは、バリデーションエラーのエラーメッセージを、以下の順でソートする。

  * javax.servlet.ServletRequest#getParameterNamesが返す項目名順
    (エラーが発生した項目がリクエストパラメータに存在しない場合は、末尾に移動する)

  ``getParameterNames`` が返す値は実装依存であり、使用するアプリケーションサーバによっては並び順が変わる可能性がある点に注意すること。
  プロジェクトでソート順を変更したい場合は、BeanValidationStrategyを継承し対応すること。

.. _bean_validation-property_name:

バリデーションエラー時のメッセージに項目名を含めたい
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Bean Validation(JSR349)の仕様では、項目名をメッセージに含めることができないが、
要件などによってはメッセージに項目名を含めたい場合がある。
このため、NablarchではBean Validationを使用した場合でもメッセージにエラーが発生した項目の項目名を含める機能を提供している。

以下に使用方法を示す。

コンポーネント設定ファイル
  メッセージに項目名を含めるメッセージコンバータを生成するファクトリクラスを設定する。
  コンポーネント名には、 ``constraintViolationConverterFactory`` を設定し、
  クラス名には :java:extdoc:`ItemNamedConstraintViolationConverterFactory <nablarch.core.validation.ee.ItemNamedConstraintViolationConverterFactory>` を設定する。

  .. code-block:: xml

    <component name="constraintViolationConverterFactory"
        class="nablarch.core.validation.ee.ItemNamedConstraintViolationConverterFactory" />

バリデーション対象のForm
  .. code-block:: java
  
    package sample;

    public class User {

      @Required
      private String name;

      @Required
      private String address;
    }

項目名の定義
  項目名は、メッセージとして定義する。
  項目名のメッセージIDは、バリデーション対象のクラスの完全修飾名 + "." + 項目のプロパティ名とする。

  上記のFormクラスの場合、 ``sample.User`` が完全修飾名で ``name`` と ``address`` の２つのプロパティがある。
  項目名の定義には、以下のように ``sample.User.name`` と ``sample.User.address`` が必要となる。

  なお、項目名の定義を行わなかった場合、メッセージに項目名は付加されない。

  .. code-block:: properties

    # Requiredのメッセージ
    nablarch.core.validation.ee.Required.message=入力してください。

    # 項目名の定義
    sample.User.name = ユーザ名
    sample.User.address = 住所

生成されるメッセージ
  生成されるメッセージは、エラーメッセージの先頭に項目名が付加される。
  項目名は ``[`` 、 ``]`` で囲まれる。

  .. code-block:: text

    [ユーザ名]入力してください。
    [住所]入力してください。
  
.. tip::
  メッセージへの項目名の追加方法を変更したい場合には、 :java:extdoc:`ItemNamedConstraintViolationConverterFactory <nablarch.core.validation.ee.ItemNamedConstraintViolationConverterFactory>` 
  を参考にし、プロジェクト側で実装を追加し対応すること。

拡張例
---------------
プロジェクト固有のアノテーションとバリデーションロジックを追加したい
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`bean_validation-validator` に記載のバリデータで要件を満たすことができない場合は、
プロジェクト側でアノテーション及びバリデーションのロジックを追加すること。

実装方法などの詳細については、以下のリンク先及びNablarchの実装を参照。

* `Hibernate Validator(外部サイト、英語) <http://hibernate.org/validator/>`_
* `JSR349(外部サイト、英語) <https://jcp.org/en/jsr/detail?id=349>`_

