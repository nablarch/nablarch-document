.. _bean_util:

BeanUtil
==================================================
.. contents:: 目次
  :depth: 3
  :local:

Java Beansに関する以下機能を提供する。また、Java16より標準化されたレコードをJava Beansと同様に取り扱うことができる。
詳細は :ref:`bean_util-use_record` を参照。

* プロパティに対する値の設定と取得
* 他のJava Beansへの値の移送
* Java Beansとjava.util.Mapとの間での値の移送

モジュール一覧
---------------------------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-beans</artifactId>
  </dependency>

.. _bean_util-use_java_beans:

使用方法
--------------------------------------------------
:java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` が提供するAPIを使用して、任意のJava Beansに対する操作が実現できる。

BeanUtilの使用例を以下に示す。

Bean定義
  .. code-block:: java

    public class User {
        private Long id;
        private String name;
        private Date birthDay;
        private Address address;
        // getter & setterは省略
    }

    public class Address {
        private String postNo;
        // getter & setterは省略
    }

    public class UserDto {
        private String name;
        private String birthDay;
        // getter & setterは省略
    }

BeanUtilの使用例
  幾つかのAPIの使用例を以下に示す。
  詳細は、BeanUtilの :java:extdoc:`Javadoc <nablarch.core.beans.BeanUtil>` を参照。

  .. code-block:: java

    final User user = new User();
    user.setId(1L);
    user.setName("名前");
    user.setBirthDay(new Date());

    final Address address = new Address();
    address.setPostNo("1234");
    user.setAddress(address);
    

    // プロパティ名を指定して値を取得する(1が取得できる)。
    // 値はgetter経由で取得される。
    final Long id = (Long) BeanUtil.getProperty(user, "id");

    // プロパティ名を指定して値を設定する(nameプロパティの値が「新しい名前」に変更される)
    // 値はsetter経由で設定される。
    BeanUtil.setProperty(user, "name", "新しい名前");

    // 他のBeanを作成しつつ値の移送する。
    // Userのプロパティ名と一致するUserDtoのプロパティに対して値が移送される。
    // 値の移送はgetter及びsetterを使用して行われる。
    // 移送先に存在しないプロパティは無視される。
    // 移送先のプロパティの型が異なる場合は、ConversionUtilにより型変換が行われる。
    final UserDto dto = BeanUtil.createAndCopy(UserDto.class, user);

    // プロパティの値をMapに移送する。
    // Mapのキーは、プロパティ名で値がgetterで取得した値となる。
    // ネストしたBeanの値はキー名が「.」で区切られて移送される(Map -> Mapとネストはしない)
    // 例えば、address.postNoとなる。
    final Map<String, Object> map = BeanUtil.createMapAndCopy(user);
    final String postNo = (String) map.get("address.postNo");     // 1234が取得できる。

    // Mapの値をBeanに移送する。
    // Mapのキーと一致するプロパティのsetterを使用してMapの値を移送する。
    // ネストしたBeanに値を移送する場合は、Mapのキー名が「.」で区切られている必要がある。(Map -> Mapとネストしたものは扱えない)
    // 例えば、address.postNoとキー名を定義することで、User.addressのpostNoプロパティに値が設定される。
    final Map<String, Object> userMap = new HashMap<String, Object>();
    userMap.put("id", 1L);
    userMap.put("address.postNo", 54321);
    final User user = BeanUtil.createAndCopy(User.class, userMap);
    final String postNo2 = user.getAddress()
                          .getPostNo();             // 54321が取得できる。

.. important::

  BeanUtilはList型の型パラメータに対応していない。List型の型パラメータを使いたい場合は具象クラスでgetterをオーバーライドして対応すること。

  .. code-block:: java

    public class ItemsForm<D extends Serializable> {
        private List<D> items;
        public List<D> getItems() {
            return items;
        }
        public void setItems(List<D> items) {
            this.items = items;
        }
    }

    public class Item implements Serializable {
        // プロパティは省略
    }

    // 具象クラスでオーバーライドしない場合。
    // BeanUtil.createAndCopy(BadSampleForm.class, map)を呼び出すと、
    // List型の型パラメータに対応していないため実行時例外が発生する。
    public class BadSampleForm extends ItemsForm<Item> {
    }

    // 具象クラスでオーバーライドした場合。
    // BeanUtil.createAndCopy(GoodSampleForm.class, map)が正常に動作する。
    public static class GoodSampleForm extends ItemsForm<Item> {
        @Override
        public List<Item> getItems() {
            return super.getItems();
        }
    }

.. _utility-conversion:

BeanUtilの型変換ルール
--------------------------------------------------
:java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` では、Java BeansオブジェクトやMapオブジェクトから
別のJava Beansオブジェクトにデータ移行する際にプロパティを型変換している。

なお、MapオブジェクトからJava Beansオブジェクトにデータ移行する場合、
Mapオブジェクトのキーに ``.`` が含まれていればそのプロパティをネストオブジェクトとして扱う。

型変換ルールについては、 :java:extdoc:`nablarch.core.beans.converter` パッケージ配下に配置されている
:java:extdoc:`Converter <nablarch.core.beans.Converter>` 実装クラスをそれぞれ参照すること。

.. important::

  デフォルトで提供する型変換ルールでは、精度の小さい型へ変換した場合(例えばLongからIntegerへの変換)で、変換先の精度を超えるような値を指定しても正常に処理を終了する。
  このため、BeanUtilを使用してコピーする際には、コピーする値がシステムで許容されているかどうかを :ref:`validation` によって事前に検証しておく必要がある。
  検証しなかった場合、不正な値がシステムに取り込まれ障害の原因となる可能性がある。

.. important::

  型変換ルールはアプリケーション共通の設定となる。
  特定の処理のみ異なる型変換ルールを適用したい場合は、 :ref:`bean_util-format_logical` を参照し、
  特定のプロパティや型に対して :java:extdoc:`Converter <nablarch.core.beans.Converter>` 実装を適用し対応すること。

.. _utility-conversion-add-rule:

型変換ルールを追加する
--------------------------------------------------

型変換ルールを追加するには、以下の手順が必要となる。

1. 必要に応じて以下のインタフェースを実装し型変換処理を実現する。

  * :java:extdoc:`Converter <nablarch.core.beans.Converter>`
  * :java:extdoc:`ExtensionConverter <nablarch.core.beans.ExtensionConverter>`
  
2. :java:extdoc:`ConversionManager <nablarch.core.beans.ConversionManager>` の実装クラスを作成する。
   今回は標準の型変換ルールに追加でルールを設定するため、 :java:extdoc:`ConversionManager <nablarch.core.beans.ConversionManager>` をプロパティとして持つ、
   :java:extdoc:`ConversionManager <nablarch.core.beans.ConversionManager>` の実装クラスを作成する。

  .. code-block:: java

    public class SampleConversionManager implements ConversionManager {

        private ConversionManager delegateManager;

        @Override
        public Map<Class<?>, Converter<?>> getConverters() {
            Map<Class<?>, Converter<?>> converters = new HashMap<Class<?>, Converter<?>>();

            // 標準のコンバータ
            converters.putAll(delegateManager.getConverters());

            // 今回作成したコンバータ
            converters.put(BigInteger.class, new CustomConverter());

            return Collections.unmodifiableMap(converters);
        }

        @Override
        public List<ExtensionConverter<?>> getExtensionConvertor() {
            final List<ExtensionConverter<?>> extensionConverters =
                new ArrayList<ExtensionConverter<?>>(delegateManager.getExtensionConvertor());
            extensionConverters.add(new CustomExtensionConverter());
            return extensionConverters;
        }

        public void setDelegateManager(ConversionManager delegateManager) {
            this.delegateManager = delegateManager;
        }
    }

3. コンポーネント設定ファイルに、 :java:extdoc:`ConversionManager <nablarch.core.beans.ConversionManager>` の実装クラスを設定する。

   ポイント
    * コンポーネント名は **conversionManager** とすること。

   .. code-block:: xml

    <component name="conversionManager" class="sample.SampleConversionManager">
      <property name="delegateManager">
        <component class="nablarch.core.beans.BasicConversionManager" />
      </property>
    </component>

型変換時に許容するフォーマットを指定する
--------------------------------------------------
型変換時には、許容するフォーマットを指定することで日付や数値のフォーマットを解除できる。
例えば、カンマ編集されたString型の値(1,000,000)を数値型(1000000)に変換できる。

許容するフォーマットは、以下の3種類の指定方法がある。優先順位は上に記載したものが高くなる。

* :ref:`BeanUtil呼び出し時に設定 <bean_util-format_logical>`
* :ref:`プロパティ単位にアノテーションで設定 <bean_util-format_property_setting>`
* :ref:`デフォルト設定(システム共通設定) <bean_util-format_default_setting>`

.. _bean_util-format_default_setting:

デフォルト(システム共通)の許容するフォーマットを設定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
フォーマットのデフォルト設定は、コンポーネント設定ファイルに設定する。

例えば、画面上で入力される数値についてはカンマ編集されているものも許容する場合には、デフォルト設定しておくことで個別指定が不要となる。

以下に設定方法を示す。

ポイント
  * コンポーネント名を **conversionManager** で :java:extdoc:`BasicConversionManager <nablarch.core.beans.BasicConversionManager>` を定義する。
  * ``datePatterns`` プロパティに許容する日付及び日時形式のフォーマットを設定する。
  * ``numberPatterns`` プロパティに許容する数値形式のフォーマット定義を設定する。
  * 複数のフォーマットを許容する場合は複数設定する。

設定例
  .. code-block:: xml

    <component name="conversionManager" class="nablarch.core.beans.BasicConversionManager">
      <!-- 日付及び日時の許容するフォーマットを指定する -->
      <property name="datePatterns">
        <list>
          <value>yyyy/MM/dd</value>
          <value>yyyy-MM-dd</value>
        </list>
      </property>
      <!-- 数値の許容するフォーマットを指定する -->
      <property name="numberPatterns">
        <list>
          <value>#,###</value>
        </list>
      </property>
    </component>

.. important::

  ``yyyy/MM/dd`` と ``yyyy/MM/dd HH:mm:ss`` の用に日付と日時のフォーマットを指定した場合、
  日時形式の値も `yyyy/MM/dd` パース出来てしまうため時間情報が欠落してしまうケースがある。

  このため、デフォルト指定では日付のフォーマットのみを指定し、日時形式の項目については :ref:`プロパティ単位にアノテーションで設定 <bean_util-format_property_setting>`
  を使用してデフォルト設定をオーバライドするなどの対応が必要となる。

.. _bean_util-format_property_setting:

コピー対象のプロパティに対して許容するフォーマットを設定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
特定機能だけ :ref:`デフォルト設定 <bean_util-format_default_setting>` を適用せずに異なるフォーマットを指定したい場合がある。
この場合は、コピー対象のBean(コピー元またはコピー先)の該当プロパティに対応したフィールドに対してアノテーションを指定し許容するフォーマットを上書きする。

アノテーションは、コピー元とコピー先のどちらに指定しても動作するが、基本的に許容するフォーマットはString型のプロパティに対応するフィールドに指定するのが好ましい。
なぜなら、フォーマットした値を持つのはString型のプロパティであり、そのプロパティに対して許容するフォーマットが指定されていることが自然であるためである。
もし、コピー元とコピー先の両方に指定されている場合は、コピー元の設定を使用する。

例えば、デフォルト設定では日付のフォーマットを指定している場合で、特定機能のみ日時フォーマットを許容する場合に使用するとよい。

以下に実装例を示す。

ポイント
  * コピー元(コピー先)のプロパティに対応したフィールドに対して :java:extdoc:`CopyOption <nablarch.core.beans.CopyOption>` アノテーションを設定する。
  * CopyOptionの ``datePattern`` に許容する日付及び日時のフォーマットを指定する。
  * CopyOptionの ``numberPattern`` に許容する数値のフォーマットを指定する。

実装例
  .. code-block:: java

    public class Bean {
        // 許容する日時フォーマットを指定する
        @CopyOption(datePattern = "yyyy/MM/dd HH:mm:ss")
        private String timestamp;

        // 許容する数値フォーマットを指定する
        @CopyOption(numberPattern = "#,###")
        private String number;

        // setter及びgetterは省略
    }

.. _bean_util-format_logical:

BeanUtil呼び出し時に許容するフォーマットを設定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
特定機能だけ :ref:`デフォルト設定 <bean_util-format_default_setting>` を適用せずに異なるフォーマットを指定したいが、
OSSなどを用いてBeanを自動生成している場合に :ref:`プロパティ単位にアノテーションで設定 <bean_util-format_property_setting>` が使用できない場合がある。
また、特定プロパティのみ異なる型変換ルールを適用したい場合がある。

このような場合は、 :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` 呼び出し時に、許容するフォーマットや型変換ルールを設定し対応する。

以下に実装例を示す。

ポイント
  * :java:extdoc:`CopyOptions <nablarch.core.beans.CopyOptions>` を使用してプロパティに対して設定する。
    ``CopyOptions`` の構築方法は、 :java:extdoc:`CopyOptions.Builder <nablarch.core.beans.CopyOptions.Builder>` を参照。
  * 生成した :java:extdoc:`CopyOptions <nablarch.core.beans.CopyOptions>` を使用して :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` を呼び出す。

実装例
  .. code-block:: java

   final CopyOptions copyOptions = CopyOptions.options()
           // timestampプロパティに対して許容するフォーマットを指定
           .datePatternByName("timestamp", "yyyy年MM月dd日 HH時mm分ss秒")
           // customプロパティに対してCustomDateConverterを適用
           .converterByName("custom", Date.class, new CustomDateConverter())
           .build();

    // CopyOptionsを指定してBeanUtilを呼び出す。
    final DestBean copy = BeanUtil.createAndCopy(DestBean.class, bean, copyOptions);


.. _bean_util-use_record:

BeanUtilでレコードを使用する
--------------------------------------------------

BeanUtilでは、Java16より標準化されたレコードをJava Beansと同様に取り扱うことができる。

注意点として、一度生成したレコードは後から変更することができない。
そのため、 :java:extdoc:`BeanUtil.setProperty <nablarch.core.beans.BeanUtil.setProperty(java.lang.Object-java.lang.String-java.lang.Object)>` や
:java:extdoc:`BeanUtil.copy <nablarch.core.beans.BeanUtil.copy(SRC-DEST)>` といったメソッドの引数に、変更対象のオブジェクトとしてレコードを渡した場合は実行時例外が発生する。

使用方法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:ref:`Java Beansに対する操作 <bean_util-use_java_beans>` に準ずる。

.. important::

  BeanUtilはList型の型パラメータを含むレコードに対応していない。レコードは継承することができないため、
  List型の型パラメータは最初から具象型を設定して、レコードを定義すること。

  .. code-block:: java

    public class Item implements Serializable {
        // プロパティは省略
    }

    // List型の型パラメータに具象型を設定していない場合。
    // BeanUtil.createAndCopy(BadSampleRecord.class, map)を呼び出すと、
    // List型の型パラメータに対応していないため実行時例外が発生する。
    public class BadSampleRecord<T>(List<T> items) {}

    // List型の型パラメータに具象型を設定した場合。
    // BeanUtil.createAndCopy(GoodSampleRecord.class, map)が正常に動作する。
    public record GoodSampleRecord(List<Item> items) {}
