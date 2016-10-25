.. _repository:

システムリポジトリ
==================================================

.. contents:: 目次
  :depth: 3
  :local:

アプリケーションを実装する際に様々な箇所で使用されるオブジェクトや、設定値などを管理する機能を提供する。

この機能では、以下の事ができる。

* 環境毎に異なる可能性のあるロジック(生成されるクラスやプロパティの値)を、 外部ファイルに定義できる。
* 外部ファイルの定義を元に、オブジェクト間の関連を構築できる。(DIコンテナ機能を持つ)

機能概要
--------------------------------------------------
DIコンテナによるオブジェクトの構築ができる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DIコンテナ機能を使うことで、 :ref:`xml <repository-root_node>` に定義されたコンポーネントの定義を元にオブジェクトを構築できる。

DIコンテナ機能では、以下のことができる。

* :ref:`setterインジェクションができる。 <repository-definition_bean>`
* :ref:`文字列や数値、真偽値を使用できる。 <repository-property_type>`
* :ref:`ListやMapをインジェクションできる。 <repository-map_list>`
* :ref:`型が一致するsetterへの自動インジェクションができる。 <repository-autowired>`
* :ref:`ファクトリインジェクションができる。 <repository-factory_injection>`
* :ref:`環境依存値を管理できる。 <repository-environment_configuration>`

アプリケーションからはDIコンテナに直接アクセスするのではなく、システムリポジトリ経由でアクセスする。
詳細は、 :ref:`repository-use_system_repository` を参照。

オブジェクトの初期化ができる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
オブジェクト構築後に任意の初期化処理を実行できる。

オブジェクトの依存関係によっては、初期化順に制約が発生することが考えられるため、
この機能ではオブジェクトの初期化順が指定できる。

詳細は、 :ref:`repository-initialize_object` を参照。

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core</artifactId>
  </dependency>
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-repository</artifactId>
  </dependency>

使用方法
--------------------------------------------------

.. _repository-root_node:

xmlにルートノードを定義する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
コンポーネント設定ファイル(xml)のルートノードは、 `component-configuration` とする。
`schemaLocation` を正しく設定すると、IDEで各要素や属性のドキュメントが参照できたり、補完機能が有効活用できる。

.. code-block:: xml

  <component-configuration xmlns="http://tis.co.jp/nablarch/component-configuration"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://tis.co.jp/nablarch/component-configuration /component-configuration.xsd">

  </component-configuration>

xmlへのコンポーネント定義方法の詳細は、以下を参照。

* :ref:`repository-definition_bean`
* :ref:`repository-override_bean`
* :ref:`repository-property_type`
* :ref:`repository-map_list`
* :ref:`repository-autowired`
* :ref:`repository-environment_configuration`
* :ref:`repository-user_environment_configuration`
* :ref:`repository-factory_injection`
* :ref:`repository-initialize_object`
* :ref:`repository-split_xml`

.. _repository-definition_bean:

Java Beansオブジェクトを設定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Java Beansオブジェクトは、component要素を用いて定義する。

* class属性にDIコンテナで管理するクラスのFQCNを設定する。
* name属性を使って任意の名前を設定することができる。
* property子要素を使って、setterインジェクションができる。
* propertyの子要素にcomponentを定義できる。
* propertyのref属性を使って、他で定義したcomponentをsetterインジェクションできる。


以下に例を示す。

.. code-block:: xml

  <!-- component要素を使ってJava Beansオブジェクトを設定する -->
  <component name="sample" class="sample.SampleBean" />

  <component name="service" class="sample.SampleService">
    <!--
     property要素を使ってsetterインジェクションを行う
     この例では、sampleという名前でcomponent定義されたオブジェクトがインジェクションされる
     -->
    <property name="sample" ref="sample" />

    <!-- ref属性を使わずに、propertyの子要素にcomponentを定義することもできる -->
    <property name="obj">
      <component class="sample.SampleObject" />
    </property>

    <!-- リテラル値をsetterインジェクションする -->
    <property name="limit" value="100" />
  <component/>

.. _repository-override_bean:

Java Beansオブジェクトの設定を上書きする
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
同じ名前のオブジェクトが登録された場合、後に読み込まれたオブジェクトで設定を上書きする。
この機能は、テスト時にプロダクション環境用のオブジェクトをテスト用のオブジェクト(モック)に置き換える際に利用できる。

オブジェクトを上書きする場合は、同じ名前のオブジェクトを登録するだけで自動的に後で読み込まれたオブジェクトが優先される。

以下に例を示す。

.. code-block:: xml

  <component name="sample" class="sample.SampleBean">
    <property name="prop" value="message" />
  </component>

  <!-- 同じ名前でコンポーネントを定義して上書きする -->
  <component name="sample" class="sample.MockSampleBean" />

.. important::

  上の例のように異なるクラスを設定すると、上書き前のpropertyへの設定は全て破棄される。
  これは、同じインタフェースを実装していても、同じpropertyを持っているとは限らないためである。

  ただし、同じクラスを設定した場合、上書き前のpropertyへの設定が上書き後のクラスに全て引き継がれる。
  このため、上書き後の設定で特定propertyへの設定を削除することはできない。
  例えば、以下の様な上書き設定をした場合、上書き後の設定にはproperty要素は存在していないが、
  上書き前のpropの値が引き継がれるため、propにはmessageが設定された状態となる。

  .. code-block:: xml

    <component name="sample" class="sample.SampleBean">
      <property name="prop" value="message" />
    </component>

    <!--
    propertyを設定していないが、上書き前のpropの値が引き継がれる
     -->
    <component name="sample" class="sample.SampleBean" />

.. _repository-property_type:

文字列や数値、真偽値を設定値として使う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
プロパティの型が以下の型の場合、リテラル表記で値を簡易的に設定することができる。

* java.lang.String
* java.lang.String[]
* java.lang.Integer(int)
* java.lang.Integer[](int[])
* java.lang.Long(long)
* java.lang.Boolean(boolean)

以下に設定例を示す。

java.lang.String
  java.lang.String型に値を設定する場合、value属性にリテラルで設定する値を記述する。

  この例では、strプロパティに対して「あいうえお」が設定される。

  .. code-block:: xml

    <property name="str" value="あいうえお" />

java.lang.String[]
  java.lang.String[]型に値を設定する場合、value属性に値をカンマ(,)区切りで設定する。
  カンマで区切られた値が、配列の1つの要素となる。

  この例では、arrayプロパティに対して「[あ, い, う, え, お]」が設定される。
  なお、区切り文字である ``,`` を要素として設定することはできない。

  .. code-block:: xml

    <property name="array" value="あ,い,う,え,お" />

java.lang.Integer(int)
  java.lang.Integer型及びint型に値を設定する場合、value属性に設定する値を記述する。
  設定できる値は、 `Integer#valueOf` により変換できる値。

  この例では、Integer(int)型のnumプロパティに対して「12345」が設定される。

  .. code-block:: xml

    <property name="num" value="12345" />

java.lang.Integer[](int[])
  java.lang.String[]と同じように、value属性に値をカンマ(,)区切りで設定する。
  各要素に設定できる値は、 `Integer#valueOf` により変換できる値。

java.lang.Long(long)
  java.lang.Integer(int)と同じように、value属性に設定する値を記述する。
  設定できる値は、 `Long#valueOf` により変換できる値。

java.lang.Boolean(boolean)
  java.lang.Boolean型に値を設定する場合、value属性にリテラルで設定する値を記述する。
  設定できる値は、 `Boolean#valueOf` により変換できる値。

  この例では、Boolean(boolean)型のboolプロパティに対して「true」が設定される。

  .. code-block:: xml

    <property name="bool" value="true" />

.. _repository-map_list:

ListやMapを設定値として使う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
list要素やmap要素を使ってコンポーネント設定をすることで、ListやMapを受け取るpropertyに対するsetterインジェクションが行える。

list要素を使ったListの設定
  この例では、integerListプロパティに対して、要素に[1, 2, 3]を持つListが設定される。

  .. code-block:: xml

      <property name="integerList">
        <list>
          <value>1</value>
          <value>2</value>
          <value>3</value>
        </list>
      </property>

  list要素にも任意の名前を設定でき、property要素で名前参照することができる。
  この例は、上の例と同じ設定となる。

  .. code-block:: xml

    <list name="numList">
      <value>1</value>
      <value>2</value>
      <value>3</value>
    </list>

    <component class="sample.ListSample">
      <!-- numListという名前のListを設定する -->
      <property name="integerList" ref="numList" />
    </component>

  Listに対しては、任意のJava Beansオブジェクトを設定することができる。
  この例では、handlersプロパティに対して `SampleHandler1` 、 `SampleHandler2` 、 `SampleHandler3` を持つListが設定される。
  なお、下の例にもあるがcomponent-ref要素を使用することで、名前参照することができる。

  .. code-block:: xml

    <component name="sampleHandler3" class="sample.SampleHandler3" />

    <component class="sample.ListSample">
      <property name="handlers">
        <list>
          <component class="sample.SampleHandler1" />
          <component class="sample.SampleHandler2" />
          <component-ref name="sampleHandler3" />
        </list>
      </property>
    </component>

map要素を使ったMapの設定
  この例では、mapプロパティに対してentryに「{key1=1, key2=2, key3=3}」を持つMapが設定される。

  .. code-block:: xml

    <property name="map">
      <map>
        <entry key="key1" value="1" />
        <entry key="key2" value="2" />
        <entry key="key3" value="3" />
      </map>
    </property>

  mapにも任意の名前を設定でき、property要素で名前参照することができる。
  この例は、上の例と同じ設定となる。

  .. code-block:: xml

      <map name="map">
        <entry key="key1" value="1" />
        <entry key="key2" value="2" />
        <entry key="key3" value="3" />
      </map>

    <component class="sample.ListSample">
      <!-- mapという名前のMapを設定する -->
    <property name="map" ref="map">
    </component>

  value-component要素を使用することで、任意のBeanをMapの値として設定することもできる。

  .. code-block:: xml

    <property name="settings">
      <map>
        <entry key="sample1">
          <value-component class="sample.SampleBean1" />
        </entry>
        <entry key="sample2">
          <value-component class="sample.SampleBean2" />
        </entry>
      </map>
    </property>

.. _repository-autowired:

型が一致するオブジェクトを自動インジェクションする
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
propertyの型に対応するオブジェクトがDIコンテナ内に1つしか存在しない場合、propertyの定義を省略しても自動的にインジェクションする機能を提供する。

.. important::

  自動インジェクション機能を使用するのではなく、propertyを定義し明示的にインジェクションする方法を推奨する。

  なぜなら、この機能を使用すると最終的に生成されるオブジェクトの状態が、コンポーネント設定ファイル(xml)から読み取れない問題がある。
  また、派生開発で同一の型のオブジェクトの設定が増えた場合、propertyの定義が必要になるなどメンテナンス性が悪い問題がある。

以下に自動インジェクションとなる例を示す。

インジェクション対象のクラスを作成する
  インジェクション対象のインタフェース及び実装クラスを作成する。
  この例では、インタフェースを作成しているが、インタフェースの作成は必須ではない。

  .. code-block:: java

    public interface SampleService {
    }

    public class BasicSampleService implements SampleService {
    }

インジェクション対象のオブジェクトを使用するクラスを作成する
  上記で作成したクラスを使って処理を行うクラスを作成する。
  このクラスは、setterインジェクションで上記のクラスを受け取る。

  .. code-block:: java

    public class SampleController {
      private SampleService service;

      public void setService(SampleService service) {
        this.service = service;
      }
    }

コンポーネント設定ファイルにコンポーネントを定義する
  この例では、 `SampleController` に `service` propertyを定義していないが、`SampleService` を実装したクラスの設定が1つだけなので
  `service` propertyに自動的に `BasicSampleService` が設定される。

  .. code-block:: xml

    <component name="service" class="sample.BasicSampleService" />

    <component name="controller" class="sample.SampleController" />


  上記の設定は、以下のように明示的にpropertyを定義した場合と同じ動作となる。

  .. code-block:: xml

    <component name="service" class="sample.BasicSampleService" />

    <component name="controller" class="sample.SampleController">
      <property name="service" ref="service" />
    </component>

.. _repository-split_xml:

コンポーネント設定ファイル(xml)を分割する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
全ての定義を1つのコンポーネント設定ファイルに定義するとxmlが巨大となり、メンテナンス性が悪くなる問題がある。
このため、xmlファイルを複数ファイルに分割できる機能を提供している。

xmlファイルを分割する際には、機能単位などある程度の粒度でファイルを分割すると良い。
分割したxmlファイルは、import要素で読み込む事ができる。

以下に例を示す。

この例では、3つのxmlファイルがロードされる。

.. code-block:: xml

  <import file="library/database.xml" />
  <import file="library/validation.xml" />
  <import file="handler/multipart.xml" />

.. _repository-environment_configuration:

環境依存値を設定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
テスト環境や本番環境で異なる値(データベースの接続情報やディレクトリのパスなど)は、環境設定ファイルで管理することができる。

環境設定ファイルは、以下のようにシンプルなkey-value形式で記述する。
詳細な記述ルールは、 :ref:`repository-environment_configuration_file_rule` を参照。

.. code-block:: bash

  database.url = jdbc:h2:mem:sample
  database.user = sa
  database.password = sa

.. important::

  環境設定値のキー値が重複していた場合、後に定義されたものが有効となるため注意すること。

以下に例を示す。

環境依存値
  .. code-block:: bash

    database.url = jdbc:h2:mem:sample
    database.user = sa
    database.password = sa

.. _repository-user_environment_configuration:

コンポーネント設定ファイルから環境依存値を参照する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
コンポーネント設定ファイル(xml)から環境設定ファイルを読み込み、Java Beansオブジェクトの設定値として利用できる。

DIコンテナで管理するオブジェクトに対して環境依存値を設定(インジェクション)する場合は、
コンポーネント設定ファイルに環境依存値のキー値を ``${`` と ``}`` で囲んで記述する。

なお、この記法を環境設定ファイルで使用することはできない。(環境設定ファイル内では、他の環境依存値は参照できない。)

以下に例を示す。

環境設定ファイル
  .. code-block:: bash

    database.url = jdbc:h2:mem:sample
    database.user = sa
    database.password = sa

コンポーネント設定ファイル
  環境設定ファイルを読み込む場合には、config-file要素を使用する。
  この例のようにファイル名指定で読み込んだり、特定ディレクトリ配下のファイルを一括で読み込むことができる。

  上記の環境設定ファイルの名前が「database.config」の場合、 `JdbcDataSource` の `url` には、「\jdbc:h2:mem:sample」が設定される。

  .. code-block:: xml

    <!-- database.configファイルの読み込み -->
    <config-file file="database.config" />

    <component class="org.h2.jdbcx.JdbcDataSource">
      <property name="url" value="${database.url}" />
    </component>

.. _repository-overwrite_environment_configuration:

システムプロパティを使って環境依存値を上書きする
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
環境依存値は、システムプロパティ( `java.lang.System#getProperties()` で取得できる値)で上書きできる。
システムプロパティは、環境設定ファイルに設定した値より優先されるため、vmオプションで容易に設定値を上書きすることができる。

例えば、特定のバッチアプリケーションだけ設定値を変えたいといった場合に、システムプロパティを使用して環境依存値を上書きするといったことができる。

以下に例を示す。

環境設定ファイル

  .. code-block:: bash

    message=上書きされるメッセージ

システムプロパティで値を上書きする
  javaコマンドの ``-D`` オプションでシステムプロパティを設定することで、環境設定ファイルの値を上書きすることができる。
  この例の場合、 `message` の値は「上書きするメッセージ」となる。

  java -Dmessage=上書きするメッセージ

.. _repository-factory_injection:

ファクトリクラスで生成したオブジェクトをインジェクションする
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Java Beansとして実装されているクラスであれば、setterインジェクションを使用して値を設定しオブジェクトを生成することができる。
しかし、ベンダー提供やOSSなどのJava Beansとして実装されていないオブジェクトをシステムリポジトリで管理したい場合がある。

この場合は、ファクトリクラスを作成しファクトリクラス経由でオブジェクトを生成することで、これらのクラスをシステムリポジトリで管理できるようになる。

以下に手順を示す。

ファクトリクラスを作成する
  ファクトリクラスは、 :java:extdoc:`ComponentFactory <nablarch.core.repository.di.ComponentFactory>` インタフェースを実装し作成する。

  実装例
    .. code-block:: java

      public class SampleComponentFactory implements ComponentFactory<SampleComponent> {
        // 生成するオブジェクトへの設定値
        private String configValue;

        public void setConfigValue(String configValue) {
          this.configValue = configValue;
        }

        public SampleComponent createObject() {
          // オブジェクトを生成する。
          // この例では、このクラスにsetterインジェクションした値を使ってオブジェクトを生成する。
          return new SampleComponent(configValue);
        }
      }

コンポーネント設定ファイルにファクトリクラスを設定する
  ファクトリクラスを通常のコンポーネントと同じように設定することで、
  自動的にファクトリクラスが生成したオブジェクトが設定される。

  .. code-block:: xml

    <!-- ファクトリクラスの定義 -->
    <component name="sampleComponent" class="sample.SampleComponentFactory">
      <property name="configValue" value="設定値" />
    </component>

    <!-- ファクトリクラスで生成したオブジェクトを設定するクラス -->
    <component class="sample.SampleBean">
      <!-- sampleObjectプロパティにファクトリクラスで生成したオブジェクトが設定される -->
      <property name="sampleObject" ref="sampleComponent" />
    </component>

.. _repository-initialize_object:

オブジェクトの初期化処理を行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
オブジェクトの初期化処理を行うためには、以下の手順が必要となる。

#. :java:extdoc:`Initializable <nablarch.core.repository.initialization.Initializable>` インタフェースを実装する。
#. コンポーネント設定ファイルに初期化対象のリストを設定する。

以下に詳細な手順を示す。

Initializableインタフェースを実装する
  :java:extdoc:`initialzie <nablarch.core.repository.initialization.Initializable.initialize()>` で初期化処理を行う。

  .. code-block:: java

    public class SampleComponent implements Initializable {
      public void initialize() {
        // プロパティにインジェクションされた値などを元に初期化処理を行う
      }
    }

コンポーネント設定ファイルに初期化対象のリストを設定する
  初期化対象のオブジェクトを :java:extdoc:`BasicApplicationInitializer <nablarch.core.repository.initialization.BasicApplicationInitializer>` に設定する。

  初期化対象のオブジェクトの初期化順を意識する必要がある場合は、先に初期化を行いたいオブジェクトをより上に設定する。
  下の設定例の場合、以下の順で初期化が行われる。
  
  #. `sampleObject`
  #. `sampleObject3`
  #. `sampleObject2`

  .. important::
    
    :java:extdoc:`BasicApplicationInitializer <nablarch.core.repository.initialization.BasicApplicationInitializer>` のコンポーネント名は、 必ず **initializer** とすること。

  .. code-block:: xml

    <!-- 初期化対象のオブジェクトの設定 -->
    <component name="sampleObject" class="sample.SampleComponent" />
    <component name="sampleObject2" class="sample.SampleComponent2" />
    <component name="sampleObject3" class="sample.SampleComponent3" />

    <component name="initializer"
        class="nablarch.core.repository.initialization.BasicApplicationInitializer">

      <!-- initializeListプロパティにlist要素で初期化対象のオブジェクトを列挙する -->
      <property name="initializeList">
        <list>
          <component-ref name="sampleObject"/>
          <component-ref name="sampleObject3" />
          <component-ref name="sampleObject2" />
        </list>
      </property>

    </component>

.. _repository-use_system_repository:

DIコンテナの情報をシステムリポジトリに設定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DIコンテナの情報をシステムリポジトリにロードすることで、アプリケーション内の全ての箇所からDIコンテナ上のオブジェクトにアクセスすることができる。

コンポーネント設定ファイルをロードし、システムリポジトリに設定する例を以下に示す。

この例では、 ``web-boot.xml`` を元に構築されたDIコンテナの情報がシステムリポジトリに設定される。

.. code-block:: java

  XmlComponentDefinitionLoader loader
      = new XmlComponentDefinitionLoader("web-boot.xml");
  SystemRepository.load(new DiContainer(loader));

.. important::

  DIコンテナの情報をシステムリポジトリへ登録する処理は、Nablarchが提供する以下のクラスで実施される。
  このため、個別にこのような実装を行うことは基本的にない。

  * ServletContextListenerの実装クラス
  * 独立型アプリケーションの起動クラス

システムリポジトリからオブジェクトを取得する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
システムリポジトリ上からオブジェクトを取得する場合には、 :java:extdoc:`SystemRepository <nablarch.core.repository.SystemRepository>` クラスを使用する。

なお、システムリポジトリには事前にDIコンテナの情報を設定しておく必要がある。
詳細は、 :ref:`repository-use_system_repository` を参照。

以下のように、component要素(listやmap要素を含む)に設定したname属性の値を指定して、オブジェクトを取得できる。

.. code-block:: java

  SampleComponent sample = SystemRepository.get("sampleComponent");


.. _repository-environment_configuration_file_rule:

環境設定ファイルの記述ルール
--------------------------------------------------
環境設定ファイルの記述ルールについて説明する。

記述ルールは、プロパティファイルと似ているが細かな点に違いがあるため注意すること。

設定値の記述形式
  設定値は、 キーと値を ``=`` で区切って記述する。

  .. code-block:: bash
    
    key1=value1
    key2=value2

コメントの記述
  コメントは、 ``#`` を用いた行コメントのみサポートする。
  行中に ``#`` が存在した場合は、それ以降をコメントとして扱う。

  .. code-block:: bash

    # コメントです
    key = value   # コメントです

複数行にまたがった設定値の記述
  行末に ``\`` を記述することで、複数行にまたがって設定値を記述することができる。

  下の例の場合、設定値の組み合わせは以下のようになる。

  * key -> value
  * key2 -> value,value2
  * key3 -> abcdefg

  .. code-block:: bash

    key = value
    key2 = value,\
    value2
    key3 = abcd\    # ここにコメントを定義できる
    efg

予約語のエスケープ
  以下の予約語を一般文字として扱う場合は、 ``\`` を用いてエスケープを行う。

  * ``#``
  * ``=``
  * ``\``

  下の例の場合、設定値の組み合わせは以下のようになる。

  * key -> a=a
  * key2 -> #コメントではない
  * key3 -> あ\\い

  .. code-block:: bash

    key = a\=a
    key2 = \#コメントではない
    key3 = あ\\い
