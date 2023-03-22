=========================================================================
Nablarch 5から6への移行ガイド
=========================================================================

.. contents:: 目次
  :depth: 3
  :local:

ここでは、Nablarch 5で作られたプロジェクトをNablarch 6にバージョンアップする方法について説明する。

Nablarch 5と6で異なる点
=========================================================================

Nablarch 6がNablarch 5と比べて大きく異なっている点に、Jakarta EE 10に対応していることが挙げられる。

Jakarta EEとは、Java EEがEclipse Foundationに移管された後の名前で、Java EEの後継となる。
基本的にはJava EEの仕様がそのまま移管されているが、Jakarta EE 9でパッケージが ``javax.*`` から ``jakarta.*`` になるという大きな変更が入っている。

したがって、Nablarch 5で作られたプロジェクトをNablarch 6にバージョンアップするためには、プロジェクトにもこれと同様の対応を行う必要がある。

前提条件
=========================================================================

ここで説明する手順は、Nablarch 5の最新版へのバージョンアップが済んでいることを前提としている。

古いバージョンで作られたプロジェクトは、まずはNablarch 5の最新版へのバージョンアップを済ませてからNablarch 6へのバージョンアップを行うこと。
Nablarch 5の最新版へのバージョンアップに必要となる修正内容については、 :doc:`../releases/index` を参照のこと。

また、Nablarch 6のモジュールはJava 17でコンパイルされているため、実行にはJava 17以上が必要となる。


移行手順の概要
=========================================================================

Nablarch 5のプロジェクトをNablarch 6に上げるためには、大まかに次の2つの修正が必要となる。

* Nablarchのバージョンアップ
* Jakarta EE対応

1つ目の「Nablarchのバージョンアップ」は、プロジェクトで使用しているNablarchのバージョンを5から6に変更することを指す。

2つ目の「Jakarta EE対応」は、プロジェクトをJakarta EE 10に対応させることを指す。
これには、Jakarta EE 9で入ったパッケージの変更対応や、Java EEに依存しているライブラリをJakarta EE対応版に変更する対応が含まれる。

以下で、それぞれの具体的な手順について説明する。


移行手順の詳細
=========================================================================

ここでは、Nablarch 5のプロジェクトをNablarch 6にバージョンアップする際に必要になる移行手順について、それぞれ詳細な内容を説明する。

なお、具体的な修正内容をイメージしやすくするため、ここではNablarch 5の `nablarch-example-web (外部サイト) <https://github.com/nablarch/nablarch-example-web>`_ をNablarch 6にバージョンアップする場合を例にして説明している。
プロジェクトによっては不要な手順が含まれる可能性があるが、その場合は適宜取捨選択して読み進めること（例えば、 :ref:`waitt-to-jetty` や :ref:`update-ntf-jetty` はウェブプロジェクト固有の手順なので、バッチプロジェクトでは読み飛ばして問題ない）。

.. tip::
    nablarch-example-webの5系のコードは、 ``5uXX`` のタグに切り替えることで取得できる。
    タグの一覧は `こちら (外部サイト) <https://github.com/nablarch/nablarch-example-web/tags>`_ から確認できる。

--------------------------------------------------------------------
Nablarchのバージョンアップ
--------------------------------------------------------------------

Nablarchを構成する各モジュールのバージョンはbomで管理しているので、bomのバージョンを変えることでNablarchのバージョンアップができる。
以下のように、 ``pom.xml`` でNablarchのbomを読み込んでいる部分の ``<version>`` を6に変更する。

.. code-block:: xml

  <dependencyManagement>
    <dependencies>
      <dependency>
        <groupId>com.nablarch.profile</groupId>
        <artifactId>nablarch-bom</artifactId>
        <version>6</version> <!-- bom のバージョンを 6 にする-->
        <type>pom</type>
        <scope>import</scope>
      </dependency>
      ...
    </dependencies>
  </dependencyManagement>

--------------------------------------------------------------------
Jakarta EE対応
--------------------------------------------------------------------


Java EEの依存関係をJakarta EEに変更する
-----------------------------------------------------------------

Java EEのAPIの依存関係(``dependency``)を、Jakarta EEのものに変更する必要がある。
例えば代表的なものとしては、Java Servletなどが挙げられる。

nablarch-example-webの ``pom.xml`` では、以下がJava EEのAPIの依存関係になる。

.. code-block:: xml

  <!-- Java API for RESTful Web Services (JAX-RS) -->
  <dependency>
    <groupId>javax.ws.rs</groupId>
    <artifactId>javax.ws.rs-api</artifactId>
    <version>2.0</version>
  </dependency>

  <!-- Java Servlet -->
  <dependency>
    <groupId>javax.servlet</groupId>
    <artifactId>javax.servlet-api</artifactId>
    <version>3.1.0</version>
    <scope>provided</scope>
  </dependency>

  <!-- JavaServer Pages (JSP) -->
  <dependency>
    <groupId>javax.servlet.jsp</groupId>
    <artifactId>javax.servlet.jsp-api</artifactId>
    <version>2.3.1</version>
    <scope>provided</scope>
  </dependency>

  <!-- JavaServer Pages Standard Tag Library (JSTL) -->
  <dependency>
    <groupId>javax.servlet.jsp.jstl</groupId>
    <artifactId>javax.servlet.jsp.jstl-api</artifactId>
    <version>1.2.1</version>
  </dependency>

  <!-- Java Persistence API (JPA) -->
  <dependency>
    <groupId>org.apache.geronimo.specs</groupId>
    <artifactId>geronimo-jpa_2.0_spec</artifactId>
  </dependency>

これをJakarta EEが提供するものに置き換えると、以下のようになる。

.. code-block:: xml

  <dependencyManagement>
    <dependencies>
      ...
      <dependency>
        <groupId>jakarta.platform</groupId>
        <artifactId>jakarta.jakartaee-bom</artifactId>
        <version>10.0.0</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
    </dependencies>
  </dependencyManagement>

  <!-- Jakarta RESTful Web Services -->
  <dependency>
    <groupId>jakarta.ws.rs</groupId>
    <artifactId>jakarta.ws.rs-api</artifactId>
  </dependency>

  <!-- Jakarta Servlet -->
  <dependency>
    <groupId>jakarta.servlet</groupId>
    <artifactId>jakarta.servlet-api</artifactId>
    <scope>provided</scope>
  </dependency>

  <!-- Jakarta Server Pages -->
  <dependency>
    <groupId>jakarta.servlet.jsp</groupId>
    <artifactId>jakarta.servlet.jsp-api</artifactId>
    <scope>provided</scope>
  </dependency>

  <!-- Jakarta Standard Tag Library -->
  <dependency>
    <groupId>jakarta.servlet.jsp.jstl</groupId>
    <artifactId>jakarta.servlet.jsp.jstl-api</artifactId>
  </dependency>

  <!-- Jakarta Persistence -->
  <dependency>
    <groupId>jakarta.persistence</groupId>
    <artifactId>jakarta.persistence-api</artifactId>
  </dependency>

Jakarta EEのAPIにはbomが用意されているので、これを読み込むことでAPIごとにバージョンを指定する必要がなくなる。
バージョンを調べる手間や指定のミスが減り管理も楽になるため、bomを読み込むことを推奨する。

Java EEのAPIの ``dependency`` は、jarの提供元やバージョンによってバラバラになっており統一されていない。
このため、Java EEとJakarta EEの ``dependency`` の完全な対応表を提供することはできない。
どの ``dependency`` がJava EEのAPIなのかは、 ``groupId`` や ``artifactId`` 、jarの中に含まれるクラスなどから判断しなければならない。

参考までに、本ページ末尾の付録に :ref:`java_ee_jakarta_ee_comparation` を記載する。
Jakarta EEでの ``dependency`` が何になるかは各仕様のページに記載されているので、そちらを確認すること（例えば `Jakarta Servlet 6.0 の仕様のページ (外部サイト、英語) <https://jakarta.ee/specifications/servlet/6.0/#details>`_ には、「Maven coordinates」のところに ``jakarta.servlet:jakarta.servlet-api:jar:6.0.0`` と記載されている）。


Java EE関係のランタイムを更新する
-----------------------------------------------------------------

Java EEの仕様のランタイムをアプリケーションに組み込んでいる場合は、これらをJakarta EEのものに置き換える。
例えば、nablarch-example-webにはBean ValidationのランタイムであるHibernate Validatorが含まれている。

.. code-block:: xml

  <dependency>
    <groupId>org.hibernate</groupId>
    <artifactId>hibernate-validator</artifactId>
    <version>5.3.6.Final</version>
  </dependency>

これを、Jakarta EE版の ``dependency`` に変更すると以下のようになる。

.. code-block:: xml

  <dependency>
    <groupId>org.hibernate.validator</groupId>
    <artifactId>hibernate-validator</artifactId>
    <version>8.0.0.Final</version>
  </dependency>

どの ``dependency`` がJava EEのランタイムなのかは、それぞれの ``dependency`` ごとに個別に調査するしかない。
また、Java EEのランタイムであることが分かった場合、そのランタイムのJakarta EE対応版の ``dependency`` が何になるかはランタイムごとに異なる。
したがって、プロジェクトで使用しているランタイムごとに公式サイトなどを確認する必要がある。

参考までに、代表的なランタイムのJava EEとJakarta EEでの ``dependency`` を本ページの付録の :ref:`jakarta_ee_runtime_dependency` に記載している。
その他の仕様のランタイムについてはJakarta EEの各仕様のページで互換実装が紹介されているので、そちらも参考にすること。
(例えば、 `Jakarta RESTful Web Services 3.1 の仕様のページ (外部サイト、英語) <https://jakarta.ee/specifications/restful-ws/3.1/#compatible-implementations>`_ では、互換実装として Eclipse Jersey 3.1.0 が紹介されている)

gsp-dba-maven-pluginを更新する
-----------------------------------------------------------------

nablarch-example-webをはじめ、アーキタイプから作ったNablarchプロジェクトなどには `gsp-dba-maven-plugin (外部サイト) <https://github.com/coastland/gsp-dba-maven-plugin>`_ があらかじめ組み込まれている。
このプラグインは、データベーステーブルのメタデータからJavaのエンティティクラスを生成する機能(``generate-entity``)を提供している。
このエンティティクラスにはJPAなどのJava EEのアノテーションが設定されるため、そのままではJakarta EE環境で使用できない。

gsp-dba-maven-pluginは5.0.0でJakarta EE対応が入ったので、 ``pom.xml`` を以下のように修正する。

.. code-block:: xml

    <plugin>
      <groupId>jp.co.tis.gsp</groupId>
      <artifactId>gsp-dba-maven-plugin</artifactId>
      <version>5.0.0</version> <!-- gsp-dba-maven-plugin の version を Jakarta EE 対応版に変更する -->
      <configuration>
      ...

さらに、Jakarta EE対応されたgsp-dba-maven-pluginの ``generate-entity`` を使うためには、 ``dependency`` やJVM引数の追加が必要となる。
詳細については `gsp-dba-maven-pluginのガイド (外部サイト) <https://github.com/coastland/gsp-dba-maven-plugin#generate-entity>`_ を参照のこと。

以上で、Jakarta EEのアノテーションが設定されたエンティティが生成されるようになる。

.. _waitt-to-jetty:

waitt-maven-pluginをjetty-ee10-maven-pluginに変更する
-----------------------------------------------------------------

nablarch-example-webをはじめ、アーキタイプから作ったNablarchプロジェクトなどには `waitt-maven-plugin (外部サイト、英語) <https://github.com/kawasima/waitt>`_ があらかじめ組み込まれている。
このプラグインは、プロジェクトのコードを組み込みサーバ(Tomcatなど)にデプロイして簡単に実行できる機能を提供している。
しかし、このプラグインはJakarta EE対応がされていないので、同様の機能を提供していてJakarta EEにも対応しているjetty-ee10-maven-pluginに変更する。

修正前、nablarch-example-webでは以下のようにwaitt-maven-pluginが ``pom.xml`` に設定されている。

**修正前**

.. code-block:: xml

  <plugin>
    <groupId>net.unit8.waitt</groupId>
    <artifactId>waitt-maven-plugin</artifactId>
    <version>1.2.3</version>
    <configuration>
      <servers>
        <server>
          <groupId>net.unit8.waitt.server</groupId>
          <artifactId>waitt-tomcat8</artifactId>
          <version>1.2.3</version>
        </server>
      </servers>
    </configuration>
  </plugin>

これを、以下のようにしてjetty-ee10-maven-pluginに変更する。

**修正後**

.. code-block:: xml

  <plugin>
    <groupId>org.eclipse.jetty.ee10</groupId>
    <artifactId>jetty-ee10-maven-plugin</artifactId>
    <version>12.0.0</version>
  </plugin>

これで、アプリケーションのコードをJettyにデプロイして実行できるようになる。

実際に動かしたい場合は、以下のコマンドでJettyを起動できる。

.. code-block:: batch

  mvn jetty-ee10:run

.. _update-ntf-jetty:

nablarch-testing-jetty6をnablarch-testing-jetty12に変更する
-----------------------------------------------------------------

ウェブアプリケーションのプロジェクトでNTF (Nablarch Testing Framework)を使用している場合、JUnitのテストで組み込みサーバを実行するために ``nablarch-testing-jetty6`` というモジュールを使用する。
このモジュールで起動するJetty 6はJakarta EEに対応していない。
JettyがJakarta EE 10に対応したのはJetty 12なので、Jetty 12を起動できる ``nablarch-testing-jetty12`` を使うように変更する必要がある。

.. tip::
  Java 11以上のプロジェクトではJetty 9を起動する ``nablarch-testing-jetty9`` を使用するが、これもJakarta EEには対応していないため ``nablarch-testing-jetty12`` に変更する必要がある。

まずは、 ``pom.xml`` を以下のように修正する。

.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-testing-jetty12</artifactId> <!-- artifactId を nablarch-testing-jetty12 に変更する -->
    <scope>test</scope>
  </dependency>

次に、 ``HttpServerFactory`` のコンポーネントを定義している部分を以下のように修正する。

**修正前**

.. code-block:: xml

  <component name="httpServerFactory" class="nablarch.fw.web.httpserver.HttpServerFactoryJetty6"/>

**修正後**

.. code-block:: xml

  <component name="httpServerFactory" class="nablarch.fw.web.httpserver.HttpServerFactoryJetty12"/>

nablarch-example-webの場合は、 ``src/test/resources/unit-test.xml`` に上記設定が存在する。

以上で、NTF実行時に起動される組み込みサーバがJakarta EE対応版に切り替わる。

javaxパッケージをjakartaパッケージに変更する
-----------------------------------------------------------------

Jakarta EE 9で入ったパッケージ変更の対応を、アプリケーションのコードにも実施する。
パッケージ変更対応の大まかな流れを以下に記載する。

1. プロジェクト全体を ``javax`` でGrep検索する
2. 検索で見つかった箇所に関して、Java EEのパッケージかどうか判定する
3. Java EEのパッケージである場合は、 ``javax`` を ``jakarta`` に置換する

以下で、詳細について説明する。

``javax`` の記述は、多くの場合はJavaソースコード上の ``import`` 文に現れる。
ここまでの修正でJava EEの依存関係がなくなりJakarta EEの依存関係に置き換わっているため、 ``javax`` パッケージで ``import`` している部分はコンパイルエラーが発生するようになっている。

しかし、 ``javax`` が現れるのは ``import`` 文だけとは限らず、コンパイルエラーにならない場所にも存在する可能性がある。
たとえば、Java Servletでフォワード元のリクエストURIを取得するためのキー ``javax.servlet.forward.request_uri`` は文字列で指定するため、コンパイルエラーにはならない（このキーは、Jakarta Servletでは ``jakarta.servlet.forward.request_uri`` に変える必要がある）。
他にも、JSPや設定ファイルの中に記述されている場合も、コンパイルエラーにはならないが修正対象となる。

したがって ``javax`` パッケージの有無を調査するには、プロジェクト全体に対してGrep検索を行わなければならない。

次に、 ``javax`` で検索にヒットした箇所について、それが本当にJava EEのパッケージであるかどうかを判定する。
例えば、nablarch-example-webを ``javax`` で検索すると、以下のような記述がヒットする。

.. code-block:: java

  import javax.validation.ConstraintValidator;

これは、Bean Validationのクラスを ``import`` している箇所なので、Java EEのパッケージと判断できる。

一方で、以下のような記述もヒットする。

.. code-block:: java

  import javax.crypto.SecretKeyFactory;

これは標準ライブラリに含まれる暗号処理に関するクラスを ``import`` している箇所になるので、Java EEのパッケージではない。

このように、 ``javax`` でヒットしたからといって、それらが全てJava EEのパッケージとは一概には判断できない。
本ページ付録の :ref:`java_ee_jakarta_ee_comparation` に各仕様のパッケージを記載しているので、これを参考にヒットした ``javax`` がJava EEのものか判断すること。

Java EEのパッケージであると判断できた場合は、 ``javax`` の部分を ``jakarta`` に置換する。
以下は、前述の ``import`` を ``jakarta`` に置換した場合の例になる。

.. code-block:: java

  import jakarta.validation.ConstraintValidator;


以上の修正で、nablarch-example-webに関してはJakarta EE 10対応されたアプリケーションサーバ上で動作できるようになる。


JSR352に準拠したバッチアプリケーションの移行手順
=========================================================================

Nablarchが提供する実行制御基盤は、いずれも前節で説明した移行手順でバージョンアップができる。

ただし :doc:`../application_framework/application_framework/batch/jsr352/index` のみ、JBatchのランタイムとして使用しているJBeretと関連するライブラリの更新が複雑であるため、ここで追加で説明する。

JSR352に準拠したバッチアプリケーションをアーキタイプから生成した場合、Nablarch 5までは以下のように ``dependency`` が ``pom.xml`` に設定されている。

**修正前**

.. code-block:: xml

    <dependency>
      <groupId>org.glassfish</groupId>
      <artifactId>javax.el</artifactId>
      <version>...</version>
    </dependency>

    ...

    <!-- JBeretに最低限必要な依存関係 -->
    <dependency>
      <groupId>org.jboss.spec.javax.batch</groupId>
      <artifactId>jboss-batch-api_1.0_spec</artifactId>
      <version>...</version>
    </dependency>
    <dependency>
      <groupId>javax.inject</groupId>
      <artifactId>javax.inject</artifactId>
      <version>...</version>
    </dependency>
    <dependency>
      <groupId>javax.enterprise</groupId>
      <artifactId>cdi-api</artifactId>
      <version>...</version>
    </dependency>
    <dependency>
      <groupId>org.jboss.spec.javax.transaction</groupId>
      <artifactId>jboss-transaction-api_1.2_spec</artifactId>
      <version>...</version>
    </dependency>
    <dependency>
      <groupId>org.jberet</groupId>
      <artifactId>jberet-core</artifactId>
      <version>...</version>
    </dependency>
    <dependency>
      <groupId>org.jboss.marshalling</groupId>
      <artifactId>jboss-marshalling</artifactId>
      <version>...</version>
    </dependency>
    <dependency>
      <groupId>org.jboss.logging</groupId>
      <artifactId>jboss-logging</artifactId>
      <version>...</version>
    </dependency>
    <dependency>
      <groupId>org.jboss.weld</groupId>
      <artifactId>weld-core</artifactId>
      <version>...</version>
    </dependency>
    <dependency>
      <groupId>org.wildfly.security</groupId>
      <artifactId>wildfly-security-manager</artifactId>
      <version>...</version>
    </dependency>
    <dependency>
      <groupId>com.google.guava</groupId>
      <artifactId>guava</artifactId>
      <version>...</version>
    </dependency>

    <!-- JBereteをJavaSEで動作させるための依存関係 -->
    <dependency>
      <groupId>org.jberet</groupId>
      <artifactId>jberet-se</artifactId>
      <version>...</version>
    </dependency>
    <dependency>
      <groupId>org.jboss.weld.se</groupId>
      <artifactId>weld-se</artifactId>
      <version>...</version>
    </dependency>

Nablarch 6に上げる場合は、これを以下のように修正する。

**修正後**

.. code-block:: xml

    <dependency>
      <groupId>org.glassfish.expressly</groupId>
      <artifactId>expressly</artifactId>
      <version>5.0.0</version>
    </dependency>

    ...

    <!-- JBeretに最低限必要な依存関係 -->
    <dependency>
      <groupId>jakarta.batch</groupId>
      <artifactId>jakarta.batch-api</artifactId>
    </dependency>
    <dependency>
      <groupId>jakarta.inject</groupId>
      <artifactId>jakarta.inject-api</artifactId>
    </dependency>
    <dependency>
      <groupId>jakarta.enterprise</groupId>
      <artifactId>jakarta.enterprise.cdi-api</artifactId>
    </dependency>
    <dependency>
      <groupId>jakarta.transaction</groupId>
      <artifactId>jakarta.transaction-api</artifactId>
    </dependency>
    <dependency>
      <groupId>org.jberet</groupId>
      <artifactId>jberet-core</artifactId>
      <version>2.1.1.Final</version>
    </dependency>
    <dependency>
      <groupId>org.jboss.marshalling</groupId>
      <artifactId>jboss-marshalling</artifactId>
      <version>2.0.12.Final</version>
    </dependency>
    <dependency>
      <groupId>org.jboss.logging</groupId>
      <artifactId>jboss-logging</artifactId>
      <version>3.4.3.Final</version>
    </dependency>
    <dependency>
      <groupId>org.jboss.weld</groupId>
      <artifactId>weld-core-impl</artifactId>
      <version>5.0.0.SP1</version>
    </dependency>
    <dependency>
      <groupId>org.wildfly.security</groupId>
      <artifactId>wildfly-elytron-security-manager</artifactId>
      <version>1.19.0.Final</version>
    </dependency>
    <dependency>
      <groupId>com.google.guava</groupId>
      <artifactId>guava</artifactId>
      <version>31.1-jre</version>
    </dependency>

    <!-- JBereteをJavaSEで動作させるための依存関係 -->
    <dependency>
      <groupId>org.jberet</groupId>
      <artifactId>jberet-se</artifactId>
      <version>2.1.1.Final</version>
    </dependency>
    <dependency>
      <groupId>org.jboss.weld.se</groupId>
      <artifactId>weld-se-core</artifactId>
      <version>5.0.0.SP1</version>
    </dependency>

--------------------------------------------------------------------
実行時にエラーになる場合の対処方法
--------------------------------------------------------------------

NoClassDefFoundErrorになる場合
-----------------------------------------------------------------

.. code-block:: text
  
  org.jboss.weld.exceptions.WeldException
      at org.jboss.weld.executor.AbstractExecutorServices.checkForExceptions (AbstractExecutorServices.java:82)
      ...
  Caused by: java.lang.NoClassDefFoundError
      at jdk.internal.reflect.NativeConstructorAccessorImpl.newInstance0 (Native Method)
      ...
  Caused by: java.lang.NoClassDefFoundError: Could not initialize class org.jboss.weld.logging.BeanLogger
      at org.jboss.weld.util.Beans.getBeanConstructor (Beans.java:279)

実行時に上記のようなスタックトレースが出力されてエラーになる場合、 ``pom.xml`` 上の ``slf4j-nablarch-adaptor`` の位置をLogbackより下に配置することでエラーを解消できる。

.. code-block:: xml

  <dependency>
    <groupId>ch.qos.logback</groupId>
    <artifactId>logback-classic</artifactId>
    <version>1.2.4</version>
  </dependency>

  <!-- Logbackより下にslf4j-nablarch-adaptorを配置する -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>slf4j-nablarch-adaptor</artifactId>
    <scope>runtime</scope>
  </dependency>


付録
=========================================================================

.. _java_ee_jakarta_ee_comparation:

--------------------------------------------------------------------
Java EEとJakarta EEの仕様の対応表
--------------------------------------------------------------------

.. list-table:: Java EEとJakarta EEの仕様の対応表
    :widths: 3, 1, 1, 3
    :header-rows: 1

    * - Java EE
      - 省略名
      - パッケージプレフィックス
      - Jakarta EE
    * - Java Servlet
      - 
      - ``javax.servlet``
      - `Jakarta Servlet (外部サイト、英語) <https://jakarta.ee/specifications/servlet/>`_
    * - JavaServer Faces
      - JSF
      - ``javax.faces``
      - `Jakarta Faces (外部サイト、英語) <https://jakarta.ee/specifications/faces/>`_
    * - Java API for WebSocket
      - 
      - ``javax.websocket``
      - `Jakarta WebSocket (外部サイト、英語) <https://jakarta.ee/specifications/websocket/>`_
    * - Concurrency Utilities for Java EE
      - 
      - ``javax.enterprise.concurrent``
      - `Jakarta Concurrency (外部サイト、英語) <https://jakarta.ee/specifications/concurrency/>`_
    * - Interceptors
      - 
      - ``javax.interceptor``
      - `Jakarta Interceptors (外部サイト、英語) <https://jakarta.ee/specifications/interceptors/>`_
    * - Java Authentication SPI for Containers
      - JASPIC
      - ``javax.security.auth.message``
      - `Jakarta Authentication (外部サイト、英語) <https://jakarta.ee/specifications/authentication/>`_
    * - Java Authorization Contract for Containers
      - JACC
      - ``javax.security.jacc``
      - `Jakarta Authorization (外部サイト、英語) <https://jakarta.ee/specifications/authorization/>`_
    * - Java EE Security API
      - 
      - ``javax.security.enterprise``
      - `Jakarta Security (外部サイト、英語) <https://jakarta.ee/specifications/security/>`_
    * - Java Message Service
      - JMS
      - ``javax.jms``
      - `Jakarta Messaging (外部サイト、英語) <https://jakarta.ee/specifications/messaging/>`_
    * - Java Persistence API
      - JPA
      - ``javax.persistence``
      - `Jakarta Persistence (外部サイト、英語) <https://jakarta.ee/specifications/persistence/>`_
    * - Java Transaction API
      - JTA
      - ``javax.transaction``
      - `Jakarta Transactions (外部サイト、英語) <https://jakarta.ee/specifications/transactions/>`_
    * - Batch Application for the Java Platform
      - JBatch
      - ``javax.batch``
      - `Jakarta Batch (外部サイト、英語) <https://jakarta.ee/specifications/batch/>`_
    * - JavaMail
      - 
      - ``javax.mail``
      - `Jakarta Mail (外部サイト、英語) <https://jakarta.ee/specifications/mail/>`_
    * - Java EE Connector Architecture
      - JCA
      - ``javax.resource``
      - `Jakarta Connectors (外部サイト、英語) <https://jakarta.ee/specifications/connectors/>`_
    * - Common Annotations for the Java Platform
      - 
      - ``javax.annotation``
      - `Jakarta Annotations (外部サイト、英語) <https://jakarta.ee/specifications/annotations/>`_
    * - JavaBeans Activation Framework
      - JAF
      - ``javax.activation``
      - `Jakarta Activation (外部サイト、英語) <https://jakarta.ee/specifications/activation/>`_
    * - Bean Validation
      - 
      - ``javax.validation``
      - `Jakarta Bean Validation (外部サイト、英語) <https://jakarta.ee/specifications/bean-validation/>`_
    * - Expression Language
      - EL
      - ``javax.el``
      - `Jakarta Expression Language (外部サイト、英語) <https://jakarta.ee/specifications/expression-language/>`_
    * - Enterprise JavaBeans
      - EJB
      - ``javax.ejb``
      - `Jakarta Enterprise Beans (外部サイト、英語) <https://jakarta.ee/specifications/enterprise-beans/>`_
    * - Java Architecture for XML Binding
      - JAXB
      - ``javax.xml.bind``
      - `Jakarta XML Binding (外部サイト、英語) <https://jakarta.ee/specifications/xml-binding/>`_
    * - Java API for JSON Binding
      - JSON-B
      - ``javax.json.bind``
      - `Jakarta JSON Binding (外部サイト、英語) <https://jakarta.ee/specifications/jsonb/>`_
    * - Java API for JSON Processing
      - JSON-P
      - * ``javax.json``
        * ``javax.json.spi``
        * ``javax.json.stream``
      - `Jakarta JSON Processing (外部サイト、英語) <https://jakarta.ee/specifications/jsonp/>`_
    * - JavaServer Pages
      - JSP
      - ``javax.servlet.jsp``
      - `Jakarta Server Pages (外部サイト、英語) <https://jakarta.ee/specifications/pages/>`_
    * - Java API for XML-Based Web Services
      - JAX-WS
      - ``javax.xml.ws``
      - `Jakarta XML Web Services (外部サイト、英語) <https://jakarta.ee/specifications/xml-web-services/>`_
    * - Java API for RESTful Web Services
      - JAX-RS
      - ``javax.ws.rs``
      - `Jakarta RESTful Web Services (外部サイト、英語) <https://jakarta.ee/specifications/restful-ws/>`_
    * - JavaServer Pages Standard Tag Library
      - JSTL
      - ``javax.servlet.jsp.jstl``
      - `Jakarta Standard Tag Library (外部サイト、英語) <https://jakarta.ee/specifications/tags/>`_
    * - Contexts and Dependency Injection for Java
      - CDI
      - * ``javax.decorator``
        * ``javax.enterprise.context``
        * ``javax.enterprise.event``
        * ``javax.enterprise.inject``
        * ``javax.enterprise.util``
      - `Jakarta Contexts and Dependency Injection (外部サイト、英語) <https://jakarta.ee/specifications/cdi/>`_
    * - Dependency Injection for Java
      - 
      - ``javax.inject``
      - `Jakarta Dependency Injection (外部サイト、英語) <https://jakarta.ee/specifications/dependency-injection/>`_

.. _jakarta_ee_runtime_dependency:

--------------------------------------------------------------------
代表的な仕様のランタイムのdependency
--------------------------------------------------------------------


JAX-RS, Jakarta RESTful Web Services
-----------------------------------------------------------------

※記載しているアーティファクトはあくまで例であり、全てのプロジェクトでこれらが必要になるというわけではない。

**Java EE**

.. code-block:: xml
    
  <dependencyManagement>
    <dependencies>
      ...
      <dependency>
        <groupId>org.glassfish.jersey</groupId>
        <artifactId>jersey-bom</artifactId>
        <version>...</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
    </dependencies>
  </dependencyManagement>

  <dependency>
    <groupId>org.glassfish.jersey.media</groupId>
    <artifactId>jersey-media-json-jackson</artifactId>
  </dependency>

  <dependency>
    <groupId>org.glassfish.jersey.core</groupId>
    <artifactId>jersey-client</artifactId>
  </dependency>

  <dependency>
    <groupId>org.glassfish.jersey.inject</groupId>
    <artifactId>jersey-hk2</artifactId>
  </dependency>


**Jakarta EE 10**

.. code-block:: xml
    
  <dependencyManagement>
    <dependencies>
      ...
      <dependency>
        <groupId>org.glassfish.jersey</groupId>
        <artifactId>jersey-bom</artifactId>
        <version>3.1.1</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
    </dependencies>
  </dependencyManagement>

  <dependency>
    <groupId>org.glassfish.jersey.media</groupId>
    <artifactId>jersey-media-json-jackson</artifactId>
  </dependency>

  <dependency>
    <groupId>org.glassfish.jersey.core</groupId>
    <artifactId>jersey-client</artifactId>
  </dependency>

  <dependency>
    <groupId>org.glassfish.jersey.inject</groupId>
    <artifactId>jersey-hk2</artifactId>
  </dependency>


EL, Jakarta Expression Language
-----------------------------------------------------------------

**Java EE**

.. code-block:: xml

  <dependency>
    <groupId>org.glassfish</groupId>
    <artifactId>javax.el</artifactId>
    <version>...</version>
  </dependency>

**Jakarta EE 10**

.. code-block:: xml

  <dependency>
    <groupId>org.glassfish.expressly</groupId>
    <artifactId>expressly</artifactId>
    <version>5.0.0</version>
  </dependency>


JSTL, Jakarta Standard Tag Library
-----------------------------------------------------------------

**Java EE**

.. code-block:: xml

  <dependency>
    <groupId>taglibs</groupId>
    <artifactId>standard</artifactId>
    <version>...</version>
  </dependency>

**Jakarta EE 10**

.. code-block:: xml

  <dependency>
    <groupId>org.glassfish.web</groupId>
    <artifactId>jakarta.servlet.jsp.jstl</artifactId>
    <version>3.0.0</version>
  </dependency>
