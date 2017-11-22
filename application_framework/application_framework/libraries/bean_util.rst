.. _bean_util:

Bean Util
==================================================
.. contents:: 目次
  :depth: 3
  :local:

Java Beansに関する以下機能を提供する。

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

.. _utility-conversion:

BeanUtilの型変換ルール
--------------------------------------------------
:java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` では、Java BeansオブジェクトやMapオブジェクトから
別のJava Beansオブジェクトにデータ移行する際にプロパティの型変換を行っている。

なお、MapオブジェクトからJava Beansオブジェクトにデータ移行する場合、
Mapオブジェクトのキーに ``.`` が含まれていればそのプロパティをネストオブジェクトとして扱う。

型変換ルールについては、 :java:extdoc:`nablarch.core.beans.converter` パッケージ配下に配置されている
:java:extdoc:`Converter <nablarch.core.beans.Converter>` 実装クラスをそれぞれ参照すること。

.. important::

  デフォルトで提供する型変換ルールでは、精度の小さい型への変換を行った場合(例えばLongからIntegerへの変換)で、変換先の精度を超えるような値を指定しても正常に処理を終了する。
  このため、BeanUtilを使用してコピーを行う際には、コピーする値がシステムで許容されているかどうかを :ref:`validation` によって事前に検証しておく必要がある。
  検証を行わなかった場合、不正な値がシステムに取り込まれ障害の原因となる可能性がある。

.. important::

  型変換ルールはアプリケーション共通の設定となる。このため、1つのアプリケーションの中で異なる設定を利用することは出来ない。

  例えば、特定の処理のみ異なる変換ルールを適用することは出来ない。
  もし、特定の処理に固有の変換ルールを適用したい場合には、アプリケーション側で型変換と移送処理を行うこと。

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

