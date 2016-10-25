.. _nablarch_validation:

Nablarch Validation
==================================================

.. contents:: 目次
  :depth: 3
  :local:

この章では、Nablarchで独自に実装したバリデーション機能の解説を行う。

.. tip::

  :ref:`validation` で説明したように、 :doc:`bean_validation` を使用することを推奨する。

機能概要
--------------------------------------------------

バリデーションと型変換及び値の正規化ができる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Nablarchのバリデーションでは、バリデーションと入力値の型変換、正規化を行うことが出来る。

型変換が行えるため、入力値をBeanクラスの数値型(IntegerやLong)などに直接マッピングすることが出来る。
また、編集された値の編集解除(正規化)なども型変換時に行うことが出来る。

詳細は、 :ref:`nablarch_validation-definition_validator_convertor` を参照。

ドメインバリデーションができる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ドメインごとにバリデーションルールを定義できる。

ドメインバリデーションを使うと、Beanクラスのsetterにはドメイン名の指定だけを行えばよく、バリデーションルールの変更が容易になる。

詳細は、 `ドメインバリデーションを使う`_ を参照。


.. _nablarch_validation-validator_convertor:

よく使われるバリデータ及びコンバータが提供されている
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Nablarchでは、よく使われるバリデータやコンバータを標準で提供している。
このため、プロジェクト側では :ref:`nablarch_validation-definition_validator_convertor` だけで、バリデーションが実行できる。

Nablarchで提供しているバリデータ及びコンバータについては以下のリンク先を参照。

* :java:extdoc:`nablarch.core.validation.validator`
* :java:extdoc:`nablarch.core.validation.convertor`
* :java:extdoc:`nablarch.common.date`
* :java:extdoc:`nablarch.common.code.validator`


.. _nablarch_validation-module_list:

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-validation</artifactId>
  </dependency>

  <!-- 日付のバリデータ、コンバータを使用する場合のみ -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-date</artifactId>
  </dependency>

  <!-- コード値のバリデータ、コンバータを使用する場合のみ -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-code</artifactId>
  </dependency>

使用方法
--------------------------------------------------

.. _nablarch_validation-definition_validator_convertor:

使用するバリデータとコンバータを設定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
バリデーションを有効にするには、コンポーネント定義ファイルに使用するバリデータとコンバータの登録が必要となる。

Nablarchが提供しているバリデータ及びコンバータについては、 :ref:`nablarch_validation-validator_convertor` を参照。

.. important::

  バリデータやコンバータの設定がない場合、バリデーション機能は利用できないので必ず設定を行うこと。

設定例
  * :java:extdoc:`ValidationManager <nablarch.core.validation.ValidationManager>` を **validationManager** という名前でコンポーネント定義する。
  * :java:extdoc:`ValidationManager#convertors <nablarch.core.validation.ValidationManager.setConvertors(java.util.List)>` に使用するコンバータを列挙する。
  * :java:extdoc:`ValidationManager#validators <nablarch.core.validation.ValidationManager.setValidators(java.util.List)>` に使用するバリデータを列挙する。

  .. code-block:: xml

    <component name="validationManager" class="nablarch.core.validation.ValidationManager">
      <property name="convertors">
        <list>
          <!-- ここに使用するコンバータを列挙する -->
        </list>
      </property>
      <property name="validators">
        <list>
          <!-- ここに使用するバリデータを列挙する -->
        </list>
      </property>

      <!--
      他の属性は省略
      詳細は、ValidationManagerのJavadocを参照
       -->
    </component>

バリデーションルールを設定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
バリデーションルールのアノテーションは、バリデーション対象のBeanクラスのプロパティ(setter)に設定する。
なお、getterにはアノテーションを指定できないので注意すること。(指定しても意味が無い)

.. tip::

  個別にアノテーションを設定した場合、実装時のミスが増えたりメンテナンスコストが大きくなるため、
  後述する :ref:`ドメインバリデーション <nablarch_validation-domain_validation>` を使うことを推奨する。

実装例
  :ref:`Nablarchで提供しているバリデータとコンバータ <nablarch_validation-validator_convertor>` を参照しアノテーションを設定する。

  この例では、 `userName` は入力が必須で、全角文字の最大10文字が許容される。
  `birthday` は、半角数字の8桁が許容される。
  `age` は、整数で3桁まで許容される。

  .. code-block:: java

    public class SampleForm {

      @Length(max = 10)
      @SystemChar(charsetDef = "全角文字")
      @Required
      public void setUserName(String userName) {
          this.userName = userName;
      }

      @Length(min = 8, max = 8)
      @SystemChar(charsetDef = "半角数字")
      public void setBirthday(String birthday) {
          this.birthday = birthday;
      }

      @Digits(integer = 3)
      public void setAge(Integer age) {
          this.age = age;
      }
    }

.. _nablarch_validation-domain_validation:

ドメインバリデーションを使う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ドメインバリデーションを使うための設定や実装例を示す。

ドメインごとのバリデーションルールを定義したEnumの作成
  ドメインバリデーションを利用するには、まずドメインごとのバリデーションルールを持つEnum(ドメインEnum)を作成する。
  このEnumは、必ず `DomainDefinition` インタフェースを実装すること。

  Enumの各列挙子がドメイン名となる。以下の例では ``NAME`` と ``DATE`` の２つのドメインが定義されている。

  .. code-block:: java

    public enum SampleDomain implements DomainDefinition {

        @Length(max = 10)
        @SystemChar(charsetDef = "全角文字")
        NAME,

        @Length(min = 8, max = 8)
        @SystemChar(charsetDef = "半角数字")
        DATE;

        // インタフェースで定義されているメソッドの実装
        // 実装する内容は、この例と全く同じとすること
        @Override
        public Annotation getConvertorAnnotation() {
            return DomainValidationHelper.getConvertorAnnotation(this);
        }

        @Override
        public List<Annotation> getValidatorAnnotations() {
            return DomainValidationHelper.getValidatorAnnotations(this);
        }
    }

ドメインを表すアノテーションの作成
  ドメインを表すアノテーションを作成する。
  `value` 属性には、上記で作成したドメインEnumを指定できるようにする。

  .. code-block:: java

    @ConversionFormat
    @Validation
    @Target(ElementType.METHOD)
    @Retention(RetentionPolicy.RUNTIME)
    public @interface Domain {
        SampleDomain value();
    }

バリデーション対象のBeanにドメインを設定
  上記で作成したドメインを表すアノテーションを設定することで、ドメインバリデーションが行われる。

  この例では、 `userName` に対して `SampleDomain.NAME` に設定したバリデーションが実行される。
  ※コンバータが設定されている場合は、コンバータによる値の変換も行われる。

  .. code-block:: java

    @Domain(SampleDomain.NAME)
    public void setUserName(String userName) {
        this.userName = userName;
    }

ドメインバリデーションを有効にするための設定
  ドメインバリデーションを有効にするためには、以下の設定が必要となる。

  * :java:extdoc:`DomainValidationHelper <nablarch.core.validation.domain.DomainValidationHelper>` の設定
  * :java:extdoc:`DomainValidator <nablarch.core.validation.domain.DomainValidator>` の設定
  * :java:extdoc:`ValidationManager <nablarch.core.validation.ValidationManager>` の設定
  * 初期化コンポーネントの設定

  以下に例を示す。

  :java:extdoc:`DomainValidationHelper <nablarch.core.validation.domain.DomainValidationHelper>` の設定
    * :java:extdoc:`domainAnnotationプロパティ <nablarch.core.validation.domain.DomainValidationHelper.setDomainAnnotation(java.lang.String)>`   
      にドメインを表すアノテーションの完全修飾名(FQCN)を設定する。

    .. code-block:: xml

      <component name="domainValidationHelper"
          class="nablarch.core.validation.domain.DomainValidationHelper">

        <property name="domainAnnotation" value="sample.Domain" />

      </component>

  :java:extdoc:`DomainValidator <nablarch.core.validation.domain.DomainValidator>` の設定
    * :java:extdoc:`domainValidationHelperプロパティ <nablarch.core.validation.domain.DomainValidator.setDomainValidationHelper(nablarch.core.validation.domain.DomainValidationHelper)>` 
      に、上記で設定した :java:extdoc:`DomainValidationHelper <nablarch.core.validation.domain.DomainValidationHelper>` を設定する。
    * :java:extdoc:`validatorsプロパティ <nablarch.core.validation.domain.DomainValidator.setValidators(java.util.List)>` 
      にバリデータのリストを設定する。

    .. code-block:: xml

      <component name="domainValidator"
          class="nablarch.core.validation.domain.DomainValidator">

        <!--
          DomainValidatorはここには設定しないこと。設定すると循環参照となり、
          システムリポジトリ初期化時にエラーとなる。
        -->
        <property name="validators">
          <list>
            <component-ref name="requiredValidator" />
          </list>
        </property>
        <property name="domainValidationHelper" ref="domainValidationHelper" />
      </component>


  :java:extdoc:`ValidationManager <nablarch.core.validation.ValidationManager>` の設定
    * :java:extdoc:`domainValidationHelperプロパティ <nablarch.core.validation.ValidationManager.setDomainValidationHelper(nablarch.core.validation.domain.DomainValidationHelper)>` 
      に、上記で設定した :java:extdoc:`DomainValidationHelper <nablarch.core.validation.domain.DomainValidationHelper>` を設定する。
    * :java:extdoc:`validatorsプロパティ <nablarch.core.validation.ValidationManager.setValidators(java.util.List)>` 
      にバリデータのリスト(上記で設定した :java:extdoc:`DomainValidator <nablarch.core.validation.domain.DomainValidator>` を忘れずに) を設定する。


    .. code-block:: xml

      <component name="validationManager" class="nablarch.core.validation.ValidationManager">
        <property name="validators">
          <list>
            <component-ref name="domainValidator" />
            <!-- 他のバリデータの記述は省略 -->
          </list>
        </property>
        <property name="domainValidationHelper" ref="domainValidationHelper" />
      </component>

  初期化コンポーネントの設定
    上記で設定した、 :java:extdoc:`DomainValidator <nablarch.core.validation.domain.DomainValidator>` と
    :java:extdoc:`ValidationManager <nablarch.core.validation.ValidationManager>` を初期化対象のリストに設定する。
    
    .. code-block:: xml

      <component name="initializer"
          class="nablarch.core.repository.initialization.BasicApplicationInitializer">

        <property name="initializeList">
          <list>
            <component-ref name="validationManager" />
            <component-ref name="domainValidator" />
          </list>
        </property>
      </component>

バリデーション対象のBeanを継承する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
バリデーション対象のBeanは継承することもできるが、以下の理由により継承は推奨しない。

安易に継承を行った場合、親クラスの変更により予期せぬバリデーションが実行されたり、
複雑なバリデーションの上書きルールを意識したアノテーション設定を行わなければならず、間違い(バグ)の原因となる。

なお、Beanを継承した場合は以下の動作となる。

* サブクラス側に :java:extdoc:`@PropertyName <nablarch.core.validation.PropertyName>` のみをつけた場合、親クラス側のバリデータとコンバータが使用される。
* サブクラス側にバリデータ用のアノテーションを1つでもつけた場合、親クラス側のバリデータアノテーションは無視され
  サブクラス側のバリデータが使用される。コンバータは親クラスのものが使用される。
* サブクラス側にコンバータ用のアノテーションを1つでもつけた場合は、親クラスのコンバータのアノテーションは無視され
  サブクラス側のコンバータが使用される。バリデータは親クラスのものが使用される。
* サブクラス側にバリデータもコンバータも設定されている場合は、全てサブクラス側の設定が使われる。
* 親クラス側のコンバータの設定をサブクラス側で削除することはできない。


以下の親子関係のBeanの場合、 `ChildForm` の `value` プロパティに対しては、
:java:extdoc:`@Digits <nablarch.core.validation.convertor.Digits>` と :java:extdoc:`@NumberRange <nablarch.core.validation.validator.NumberRange>` のバリデーションが実行される。

.. code-block:: java

  // 親Form
  public class ParentForm {
    @Digits(integer=5, fraction=3)
    public void setValue(BigDecimal value) {
        this.value = value;
    }
  }

  // 子Form
  public class ChildForm extends ParentForm {
    @Override
    @NumberRange(min=100.0, max=20000.0)
    public void setValue(BigDecimal value) {
        super.setBdValue(value);
    }
  }

.. _nablarch_validation-execute:

バリデーションを実行する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
バリデーションは、 :java:extdoc:`ValidationUtil <nablarch.core.validation.ValidationUtil>` で提供されるメソッドを呼び出すことで実行できる。

実装例
  まず、入力値からBeanオブジェクトを生成するため、バリデーション対象のBeanにMapを引数に取るコンストラクタを実装する。

  次にバリデーション対象のBeanにバリデーションを行うためのstaticメソッドを実装する。
  このメソッドには、 :java:extdoc:`@ValidateFor <nablarch.core.validation.ValidateFor>` アノテーションを設定し、バリデーションを識別するための任意の値を引数で指定する。

  このメソッドに必要となる処理は、  :java:extdoc:`ValidationUtil <nablarch.core.validation.ValidationUtil>` を使用してバリデーションを実行すること。

  .. code-block:: java

    public class SampleForm {

      public SampleForm(Map<String, Object> params) {
          userName = (String) params.get("userName");
          birthDay = (String) params.get("birthDay");
          age = (Integer) params.get("age");
      }

      @Domain(SampleDomain.NAME)
      @Required
      public void setUserName(String userName) {
          this.userName = userName;
      }

      @Domain(SampleDomain.DATE)
      public void setBirthday(String birthday) {
          this.birthday = birthday;
      }

      @Domain(SampleDomain.AGE)
      public void setAge(Integer age) {
          this.age = age;
      }

      @ValidateFor("validate")
      public static void validate(ValidationContext<SampleForm> context) {
        // userNameとbirthdayとageに対してバリデーションを実行
        ValidationUtil.validate(context, new String[] {"userName", "birthday", "age"});
      }
    }

  上記のBeanを使って入力値の `request` をバリデーションするには、以下のように  :java:extdoc:`ValidationUtil <nablarch.core.validation.ValidationUtil>` を使用する。
  なお、ウェブアプリケーションの場合には `ウェブアプリケーションのユーザ入力値のチェックを行う`_ でより簡易的にバリデーションが行える。

  .. code-block:: java

    // バリデーションの実行
    // SampleFormを使って入力パラメータのrequestをチェックする。
    //
    // 最後の引数にはSampleFormのどのバリデーションメソッドを使用してバリデーションを行うのかを指定する。
    // この例では、validateを指しているので、SampleFormの@ValidateForアノテーションに
    // validateと指定されているメソッドを使ってバリデーションが実行される。
    ValidationContext<SampleForm> validationContext =
            ValidationUtil.validateAndConvertRequest(SampleForm.class, request, "validate");

    // バリデーションエラーが発生している場合、abortIfInvalidで例外が送出される
    validationContext.abortIfInvalid();

    // Mapを引数に取るコンストラクタを使用してFormを生成する。
    // (入力値のrequestが変換されたFormが取得できる)
    SampleForm form = validationContext.createObject();

.. _nablarch_validation-execute_explicitly:

バリデーションの明示的な実行を行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
`バリデーションを実行する`_ では、Beanのプロパティ(setter)に設定したアノテーションベースでバリデーションが実行されたが、
ここではアノテーションを設定するのではなく直接バリデーションを実行する方法を説明する。

原則、 `バリデーションを実行する`_ の方法でバリデーションを行うが、個別にバリデーションを実行する必要がある場合には、
この方法でバリデーションを行うこと。
例えば、 :ref:`コード管理のパターン<code-use_pattern>` を使っていて、
特定の画面だけパターンを変えてバリデーションしたい場合に、個別にバリデーションを実行する。


実装例
  明示的なバリデーションの実行は、Beanクラスの  :java:extdoc:`@ValidateFor <nablarch.core.validation.ValidateFor>` アノテーションが設定されたメソッドから行う。
  なお、明示的バリデーションの実行時に指定できるアノテーションは、 :java:extdoc:`DirectCallableValidator <nablarch.core.validation.DirectCallableValidator>` を実装しているものに限定される。
  (コンバータは指定することはできない。)

  .. code-block:: java

    public class SampleForm {
      // 属性は省略

      @ValidateFor("validate")
      public static void validate(ValidationContext<SampleForm> context) {

          ValidationUtil.validate(context, new String[]{"userName", "prefectureCode"});

          // userNameに対して必須チェックを実施
          ValidationUtil.validate(context, "userName", Required.class);

          // アノテーションのパラメータはMapで指定する
          Map<String, Object> params = new HashMap<String, Object>();
          params.put("codeId", "1052");     // コードID
          params.put("pattern", "A");       // 使用するコードパターン名
          params.put("messageId", "M4865"); // エラーメッセージのID
          ValidationUtil.validate(context, "prefectureCode", CodeValue.class, params);
      }
    }

  .. important::

    明示的なバリデーションを行うには、対象の項目に対し予めバリデーションを実施しておく必要がある。
    詳細は :ref:`nablarch_validation-execute` を参照

.. _nablarch_validation-system_char_validator:

文字種バリデーションを行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
文字種バリデーションの定義方法は、 :ref:`bean_validation` と同じである。
詳細な設定方法は、 :ref:`Bean Validationの文字種バリデーションを行う <bean_validation-system_char_validator>` を参照。

なお、使用するアノテーションは、 :java:extdoc:`@SystemChar <nablarch.core.validation.validator.unicode.SystemChar>` で、
:ref:`bean_validation` とは完全修飾名が異なる(アノテーション名は同一)ので注意すること。

.. _nablarch_validation-correlation_validation:

相関バリデーションを行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
複数の項目を使用した相関バリデーションは、Beanクラスの :java:extdoc:`@ValidateFor <nablarch.core.validation.ValidateFor>` アノテーションを設定したメソッドで実装する。
このメソッドでまずは項目ごとのバリデーションを実施し、エラーが発生しなかった場合に複数項目を使用したバリデーションを実行する。

実装例
  この例では、mailAddressとconfirmMailAddressを使用した相関バリデーションを行っている。

  相関バリデーションでエラーとなった場合は、ユーザに通知すべきメッセージを示すメッセージIDを明示的に :java:extdoc:`ValidationContext <nablarch.core.validation.ValidationContext>` に追加する。

  .. code-block:: java

    public class SampleForm {

      @Domain(SampleDomain.MAIL)
      @Required
      public void setMailAddress(String mailAddress) {
          this.mailAddress = mailAddress;
      }

      @Domain(SampleDomain.MAIL)
      @Required
      public void setConfirmMailAddress(String confirmMailAddress) {
          this.confirmMailAddress = confirmMailAddress;
      }

      @ValidateFor("validate")
      public static void validate(ValidationContext<SampleForm> context) {
          // mailAddressとconfirmMailAddressのバリデーションを実施
          ValidationUtil.validate(context, new String[] {"mailAddress", "confirmMailAddress"});

          // エラーが発生した場合は、相関バリデーションを実施しない
          if (!context.isValid()) {
              return;
          }

          // formオブジェクトを生成し、相関バリデーションを実施
          SampleForm form = context.createObject();
          if (!Objects.equals(form.mailAddress, form.confirmMailAddress)) {
              // mailAddressとconfirmMailAddressが一致していない場合エラー
              context.addMessage("compareMailAddress");
          }
      }
    }

.. _nablarch_validation-nest_bean:

一括登録のようなBeanの配列を入力とする機能でバリデーションを行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
一括登録のように同一の情報を複数入力するケースがある。
このような場合には、バリデーション対象のBeanに対してネストしたBeanを定義することで対応する。

ネストしたBeanのsetterには  :java:extdoc:`@ValidationTarget <nablarch.core.validation.ValidationTarget>` アノテーションを設定し、ネストしたBeanのサイズを指定する。
要素数が固定(コンパイル時に決まっている)の場合には :java:extdoc:`size <nablarch.core.validation.ValidationTarget.size()>` 属性に指定する。可変の場合には、
:java:extdoc:`sizeKey <nablarch.core.validation.ValidationTarget.sizeKey()>` 属性にサイズを持つプロパティの名前を設定する。

この例では `AddressForm` の情報を一括で入力できるため、 `SampleForm` は `AddressForm` を配列として保持している。
また、サイズはコンパイル時には決まっていないため、 :java:extdoc:`sizeKey <nablarch.core.validation.ValidationTarget.sizeKey()>` を使用している。

.. code-block:: java

  public class SampleForm {
      private AddressForm[] addressForms;
      // addressFormsのサイズ
      // 画面のhiddenなどから送信すること
      private Integer addressSize;

      @ValidationTarget(sizeKey = "addressSize")
      public void setAddressForms(AddressForm[] addressForms) {
          this.addressForms = addressForms;
      }

      @Domain(SampleDomain.SIZE)
      @Required
      public void setAddressSize(Integer addressSize) {
          this.addressSize = addressSize;
      }

      @ValidateFor("validate")
      public static void validate(ValidationContext<SampleForm> context) {
          ValidationUtil.validate(context, new String[] {"addressSize", "addressForms"});
      }
  }

  public class AddressForm {
      // 省略
  }

.. _nablarch_validation-conditional:

ラジオボタンやリストボックスの選択値に応じてバリデーション項目を変更する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:java:extdoc:`WebUtil <nablarch.common.web.WebUtil>` クラスを使うことで、ラジオボタンやリストボックスなどの選択値に応じてバリデーション項目を切り替えることが出来る。

この例では、画面から送信された **form.radio** の値が **ptn1** の場合に、 `item1` のみバリデーションを行う。
**ptn1** 以外の場合には、 `item1` と `item2` のバリデーションを行う。

.. code-block:: java

  public class SampleForm {

      // プロパティは省略

      @ValidateFor("validate")
      public static void validate(ValidationContext<SampleForm> context) {
          if (WebUtil.containsPropertyKeyValue(context, "form.radio", "ptn1")) {
              ValidationUtil.validate(context, new String[] {"item1"});
          } else {
              ValidationUtil.validate(context, new String[] {"item1", "item2"});
          }
      }
  }

.. tip::

  この例では、 :java:extdoc:`WebUtil.containsPropertyKeyValue <nablarch.common.web.WebUtil.containsPropertyKeyValue(nablarch.core.validation.ValidationContext,%20java.lang.String,%20java.lang.String)>` を使って、送信された値までチェックを行っているが、
  単純にラジオボタンのチェック有無だけを調べたいのであれば :java:extdoc:`WebUtil.containsPropertyKey <nablarch.common.web.WebUtil.containsPropertyKey(nablarch.core.validation.ValidationContext,%20java.lang.String)>` を使う。


特定の項目に紐づくバリデーションエラーのメッセージを作りたい
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`Bean Validationの特定の項目に紐づくバリデーションエラーのメッセージを作りたい <bean_validation-create_message_for_property>` を参照。

.. _nablarch_validation-property_name:

バリデーションエラー時のメッセージに項目名を埋め込みたい
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
メッセージに項目名を埋め込むには、 :java:extdoc:`@PropertyName <nablarch.core.validation.PropertyName>` アノテーションを使用して、バリデーション対象の項目の項目名を指定する。

実装例
  メッセージには、項目名を埋め込むためのパターン文字を使用する。
  項目名は、必ず先頭に指定されるので項目名を埋め込む箇所には、 **{0}** と指定する。

  .. code-block:: properties

    required.message = {0}を入力してください。

  バリデーション対象の項目に、バリデーション用のアノテーションとともに項目名を設定する `@PropertyName` アノテーションを設定する。

  .. code-block:: java

    public class SampleForm {

        @Domain(SampleDomain.NAME)
        @Required
        @PropertyName("名前")
        public void setUserName(String userName) {
            this.userName = userName;
        }

        @Domain(SampleDomain.DATE)
        @PropertyName("誕生日")
        public void setBirthday(String birthday) {
            this.birthday = birthday;
        }
    }

生成されるメッセージ
  上記実装で、 `username` プロパティで必須エラーが発生すると、生成されるメッセージは **「名前を入力してください。」** となる。

数値型への型変換を行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
バリデーション後にBeanクラスの数値型に入力値を変換したい場合、その項目には必ず :java:extdoc:`@Digits <nablarch.core.validation.convertor.Digits>` アノテーションが必要となる。
※ドメインバリデーションの場合、ドメインEnumに対して設定が必要となる。

なお、数値型へ変換するためのコンバータが :ref:`nablarch_validation-definition_validator_convertor` の手順に従い設定されていることが前提となる。

実装例
  この例では、setterに指定しているが、ドメインバリデーションを使用したドメインEnumへの指定を推奨する。

  .. code-block:: java

    public class SampleForm {

        @PropertyName("年齢")
        @Digits(integer = 3)
        public void setAge(Integer age) {
            this.age = age;
        }
    }

.. _nablarch_validation-database:

データベースとの相関バリデーションを行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
データベースとの相関バリデーションは、業務アクションで行う。

業務アクションで行う理由は、:ref:`Bean Validationのデータベースとの相関バリデーション <bean_validation-database_validation>` を参照。

ウェブアプリケーションのユーザ入力値のチェックを行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ウェブアプリケーションのユーザ入力値のチェックは :ref:`inject_form_interceptor` を使用して行う。
詳細は、 :ref:`inject_form_interceptor` を参照

拡張例
--------------------------------------------------
プロジェクト固有のバリデータを追加したい
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
バリデータを追加するには、以下の手順が必要となる。

#. アノテーションの作成
#. バリデータの作成
#. 設定ファイルにバリデータの登録

以下に手順を示す。

アノテーションの作成
  アノテーションは以下の条件を満たすこと。

  * :java:extdoc:`@Validation <nablarch.core.validation.Validation>` アノテーションを設定すること。
  * :java:extdoc:`@Target <java.lang.annotation.Target>` アノテーションで `ElementType.METHOD` を設定すること。
  * :java:extdoc:`@Retention <java.lang.annotation.Retention>` アノテーションで `RetentionPolicy.RUNTIME` を設定すること。

  .. code-block:: java

    @Validation
    @Target(ElementType.METHOD)
    @Retention(RetentionPolicy.RUNTIME)
    public @interface Sample {
    }

バリデータの作成
  バリデータは、 :java:extdoc:`Validator <nablarch.core.validation.Validator>` インタフェースを実装し、バリデーションロジックを実装する。

  .. code-block:: java

    public class SampleValidator implements Validator {

      public Class<? extends Annotation> getAnnotationClass() {
          return Sample.class;
      }

      public <T> boolean validate(ValidationContext<T> context,
          // 省略
      }
    }

設定ファイルにバリデータの登録
   :ref:`nablarch_validation-definition_validator_convertor` を参照。

プロジェクト固有のコンバータを追加したい
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
コンバータを追加するには、以下の手順が必要となる。

#. コンバータの作成
#. 設定ファイルにコンバータの登録

以下に手順を示す。

コンバータの作成
  コンバータは、 :java:extdoc:`Convertor <nablarch.core.validation.Convertor>` インタフェースを実装し、型変換ロジックなどを実装する。

  .. code-block:: java

    public class SampleConvertor implements Convertor {

        @Override
        public Class<?> getTargetClass() {
            return Short.class;
        }

        @Override
        public <T> boolean isConvertible(ValidationContext<T> context, String propertyName, Object propertyDisplayName,
                Object value, Annotation format) {

            boolean convertible = true;

            if (value instanceof String) {
                try {
                    Short.valueOf((String) value);
                } catch (NumberFormatException e) {
                    convertible = false;
                }
            } else {
                convertible = false;
            }

            if (!convertible) {
                context.addResultMessage(propertyName, "sampleconvertor.message", propertyDisplayName);
            }
            return convertible;
        }

        @Override
        public <T> Object convert(ValidationContext<T> context, String propertyName, Object value, Annotation format) {
            return Short.valueOf((String) value);
        }
    }

設定ファイルにコンバータの登録
  :ref:`nablarch_validation-definition_validator_convertor` を参照。

バリデーション対象のBeanオブジェクトの生成方法を変更したい
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
バリデーション対象のBeanオブジェクトの生成方法を変更するには、以下の手順が必要となる。

#. :java:extdoc:`FormCreator <nablarch.core.validation.FormCreator>` の実装クラスの作成
#. :java:extdoc:`ValidationManager.formCreator <nablarch.core.validation.ValidationManager.setFormCreator(nablarch.core.validation.FormCreator)>` に、作成したクラスのコンポーネント定義を追加
