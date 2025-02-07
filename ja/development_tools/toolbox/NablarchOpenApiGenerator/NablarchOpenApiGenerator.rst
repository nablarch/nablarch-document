.. _nablarch_openapi_generator:

====================================================
Nablarch OpenAPI Generator
====================================================

.. contents:: 目次
  :depth: 3
  :local:

ツールの概要
-------------

Nablarch OpenAPI Generatorは、 `OpenAPI(外部サイト、英語) <https://www.openapis.org/>`_ ドキュメントからソースコードを生成する  `OpenAPI Generator(外部サイト、英語) <https://openapi-generator.tech/>`_ のGenerator実装である。

本ツールはNablarch RESTfulウェブサービス用のGeneratorを提供しており、 `OpenAPI GeneratorのMavenプラグイン(外部サイト、英語) <https://openapi-generator.tech/docs/plugins>`_ に組み込み実行することでソースコードを生成する。

生成されたソースコードを使用することで、OpenAPIドキュメントで定義したREST APIのインターフェースに従ったアクションクラスの実装が容易となる。

前提条件
---------

* Nablarch RESTfulウェブサービスのソースコード生成元となるOpenAPIドキュメントが作成されていること
* OpenAPIドキュメントは `OpenAPI 3.0.3(外部サイト、英語) <https://spec.openapis.org/oas/v3.0.3.html>`_ 仕様で記述されていること

動作概要
--------

本ツールではソースコード生成元となるOpenAPIドキュメントを入力として指定することで、OpenAPIドキュメントから以下のソースコードを生成する。

* パスおよびオペレーション定義を元にした、リソース(アクション)インターフェース
* スキーマ定義を元にした、リクエスト、レスポンスに対応するモデル

.. tip::

  OpenAPI Generatorの仕様上 ``.openapi-generator-ignore`` 、 ``.openapi-generator/FILES`` 、 ``.openapi-generator/VERSION`` が :ref:`NablarchOpenApiGeneratorConfiguration` の ``output`` で指定したディレクトリ配下に生成されるが、これらは使用しない。

運用方法
--------

本ツールは以下の運用方法を想定している。

#. ウェブサービスの設計情報を元にOpenAPIドキュメントを作成する
#. Nablarch RESTfulウェブサービスのプロジェクトを作成し、MavenプラグインとしてOpenAPI Generatorおよび本ツールの設定を行う
#. プロジェクトをビルドし、リソース(アクション)インターフェースとモデルを生成する
#. 生成したリソース(アクション)インターフェースとモデルを使用して、Nablarch RESTfulウェブサービスの実装を行う

.. tip::

  本ツールはOpenAPIドキュメントの修正に合わせて繰り返し実行されることを想定している。Nablarch RESTfulウェブサービスのアクションクラスは生成されたリソース(アクション)インターフェースを実装して作成するため、本ツールによる自動生成を再度行ってもアクションクラスに実装した内容が失われることはない。

.. tip::

  OpenAPI Generatorおよび本ツールはMavenプラグインとしての実行形態を想定しているが、CLIでも使用可能である。詳しくは :ref:`NablarchOpenApiGeneratorAsCli` を参照すること。

使用方法
---------

Mavenプラグインの設定
===========================

本ツールを使用するために最低限必要な、OpenAPI GeneratorのMavenプラグインの設定例を以下に示す。

.. code-block:: xml

      <plugin>
        <groupId>org.openapitools</groupId>
        <artifactId>openapi-generator-maven-plugin</artifactId>
        <version>7.10.0</version>
        <dependencies>
          <!-- 本ツールのモジュールを依存関係に追加 -->
          <dependency>
            <groupId>com.nablarch.tool</groupId>
            <artifactId>nablarch-openapi-generator</artifactId>
            <version>1.0.0</version>
          </dependency>
        </dependencies>
        <executions>
          <execution>
            <goals>
              <goal>generate</goal>
            </goals>
            <configuration>
              <!-- OpenAPIドキュメントのファイルパスを指定する -->
              <inputSpec>${project.basedir}/src/main/resources/openapi.yaml</inputSpec>
              <generatorName>nablarch-jaxrs</generatorName>
              <configOptions>
                <sourceFolder>src/gen/java</sourceFolder>
                <apiPackage>com.example.api</apiPackage>
                <modelPackage>com.example.model</modelPackage>

                <!-- その他、本ツールのオプションを指定する -->
              </configOptions>
            </configuration>
          </execution>
        </executions>
      </plugin>

本ツールは以下の依存関係により提供される。

.. code-block:: xml

          <dependency>
            <groupId>com.nablarch.tool</groupId>
            <artifactId>nablarch-openapi-generator</artifactId>
            <version>1.0.0</version>
          </dependency>

OpenAPI GeneratorのMavenプラグインを使用するにあたり、最低限必要な設定はソースコードの生成対象となるOpenAPIドキュメントを指定する ``inputSpec`` と、どのGeneratorを使用するかを指定する ``generatorName`` の2つである。

``generatorName`` には ``nablarch-jaxrs`` を指定することで、本ツールを利用できる。

その他の設定項目については :ref:`NablarchOpenApiGeneratorConfiguration` を参照すること。

.. tip::

  本ツールはOpenAPI Generator 7.10.0を使用して開発、テストをしている。
  OpenAPI Generatorのバージョンを変更する場合は、プロジェクト側でテストを行い問題ないことを確認すること。

実行方法
========

本ツールはMavenのcompileゴールで実行できる。

.. code-block:: text

  mvn compile

なお :ref:`NablarchOpenApiGeneratorConfiguration` の ``sourceFolder`` を明示的に設定した場合、 ``mvn compile`` 時に生成されたソースコードをMavenプラグインを設定したプロジェクトのコンパイル対象に含めるようになる。

この動作はOpenAPI GeneratorのMavenプラグインによって行われる。

出力先
========

OpenAPI GeneratorのMavenプラグインのデフォルト設定では、生成されたソースコードは ``target/generated-sources/openapi/src/gen/java`` に出力される。  

出力先を変更したい場合は :ref:`NablarchOpenApiGeneratorConfiguration` の ``output`` と ``sourceFolder`` を参照すること。

.. _NablarchOpenApiGeneratorConfiguration:

Generatorの設定項目
===========================

OpenAPI GeneratorのMavenプラグインの主要な設定項目を以下に示す。これらは ``configuration`` タグ内直下のタグとして指定する。

==================  =========================================================  ==========  ===============================
項目名              設定内容                                                   必須/任意   デフォルト値
==================  =========================================================  ==========  ===============================
``inputSpec``       入力となるOpenAPIドキュメントのファイルパスを指定する。    必須        なし
``generatorName``   ソースコードを生成するGeneratorの名前を指定する。 |br|     必須        なし
                    本ツールでは ``nablarch-jarxrs`` と指定すること。
``output``          ソースコードの生成先ディレクトリを指定する。               任意        ``generated-sources/openapi``
==================  =========================================================  ==========  ===============================

本ツールの設定項目を以下に示す。すべて任意項目であり、これらは ``configOptions`` タグ内に指定する。

==================================== ======================================================================================================= =====================================================================
項目名                               設定内容                                                                                                デフォルト値
==================================== ======================================================================================================= =====================================================================
``apiPackage``                       生成するリソース(アクション)インターフェースのパッケージを |br|                                         ``org.openapitools.api``
                                     指定する。                 
``modelPackage``                     生成するモデルのパッケージを指定する。                                                                  ``org.openapitools.model``
``hideGenerationTimestamp``          ``Generated`` アノテーションを注釈する時に ``date`` 属性を |br|                                         ``false``
                                     付与するか否か。デフォルトではソースコードを生成した日時が |br|
                                     出力される。
``sourceFolder``                     ソースコードの生成先ディレクトリを指定する。  |br|                                                      ``src/gen/java``
                                     OpenAPI GeneratorのMavenプラグイン設定の ``output`` からの |br|
                                     相対パスとして解釈される。 |br|
                                     この項目を指定すると、本ツールにより生成したソースコードが |br|
                                     ``mvn compile`` 時のコンパイル対象に含まれるようになる。
``useTags``                          生成するリソース(アクション)インターフェースの単位を |br|                                               ``false``
                                     パスではなくエンドポイントに付与されているタグの単位とする。 |br|
                                     なお、エンドポイントに複数のタグが付与されている場合は最初の |br|
                                     タグが有効となる。
``serializableModel``                生成するモデルに ``java.io.Serializable`` |br|                                                          ``false``
                                     インターフェースを実装する。
``generateBuilders``                 モデルに対するビルダークラスを生成する。                                                                ``false``
``useBeanValidation``                OpenAPIドキュメントのバリデーション定義から、|br|                                                       ``false``
                                     :ref:`bean_validation` の機能を使った |br|
                                     バリデーションを行うようにソースコードを生成する。
``additionalModelTypeAnnotations``   生成するモデルのクラス宣言に追加のアノテーションを注釈する。 |br|                                       なし
                                     複数のアノテーションを追加する場合は ``;`` 区切りで指定する。
``additionalEnumTypeAnnotations``    生成するenum型に追加のアノテーションを注釈する。 |br|
                                     複数のアノテーションを追加する場合は ``;`` 区切りで指定する。                                           なし
``primitivePropertiesAsString``      モデルのプリミティブなデータ型のプロパティをすべて |br|                                                 ``false``
                                     ``String`` として出力する。
``supportConsumesMediaTypes``        生成するリソース(アクション)インターフェースがリクエストを |br|                                         ``application/json,multipart/form-data``
                                     受け付けるメディアタイプを ``,`` 区切りで指定する。
``supportProducesMediaTypes``        生成するリソース(アクション)インターフェースがレスポンス |br|                                           ``application/json``
                                     とするメディアタイプを ``,`` 区切りで指定する。
==================================== ======================================================================================================= =====================================================================

Bean Validationを使用するソースコードを生成する
==================================================

:ref:`bean_validation` を使用するようにソースコードを生成する場合は、 ``useBeanValidation`` の値を ``true`` に設定する。

以下に設定例を示す。

.. code-block:: xml

            <configuration>
              <!-- OpenAPIドキュメントのファイルパスを指定する -->
              <inputSpec>${project.basedir}/src/main/resources/openapi.yaml</inputSpec>
              <generatorName>nablarch-jaxrs</generatorName>
              <configOptions>
                <sourceFolder>src/gen/java</sourceFolder>
                <apiPackage>com.example.api</apiPackage>
                <modelPackage>com.example.model</modelPackage>

                <!-- Bean Validationを使用するソースコードを生成する -->
                <useBeanValidation>true</useBeanValidation>
              </configOptions>
            </configuration>

``useBeanValidation`` のデフォルト値は ``false`` のため、デフォルトでは :ref:`bean_validation` の機能を使用するアノテーションは注釈されない。

これは、OpenAPI仕様にて規定されてるバリデーション定義では業務要件を満たせないことが多いと考えられ、また相関バリデーションの定義も行えないためである。

このような観点も含め、バリデーション機能を使用するようにソースコード生成する場合の仕様や運用上の注意点は :ref:`openapi_property_to_bean_validation` に詳細に記載しているので参照すること。

.. _NablarchOpenApiGeneratorAsCli:

CLIとして実行する
===========================

本ツールは主にMavenプラグインとして使用することを想定しているが、CLIとしても使用可能である。ここでは補足としてCLIでの実行方法を紹介する。

CLIとして実行するには、 `OpenAPI Generator 7.10.0のJARファイル(外部サイト) <https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/7.10.0/openapi-generator-cli-7.10.0.jar>`_ および `本ツールのJARファイル(外部サイト) <https://repo1.maven.org/maven2/com/nablarch/tool/nablarch-openapi-generator/1.0.0/nablarch-openapi-generator-1.0.0.jar>`_ をダウンロードしてjavaコマンドで実行する。実行例を以下に示す。

.. code-block:: text

  java -cp openapi-generator-cli-7.10.0.jar:nablarch-openapi-generator-1.0.0.jar org.openapitools.codegen.OpenAPIGenerator generate --generator-name nablarch-jaxrs --input-spec openapi.yaml --output out --additional-properties=apiPackage=com.example.api,modelPackage=com.example.model,useBeanValidation=true,hideGenerationTimestamp=true

``--generator-name`` には ``nablarch-jaxrs`` を指定する。 :ref:`NablarchOpenApiGeneratorConfiguration` のうちOpenAPI Generatorの設定項目はOpenAPI GeneratorのCLIでも指定できる。詳しくは以下のコマンドの結果を参照。

.. code-block:: text

  java -jar openapi-generator-cli-7.10.0.jar help generate

.. tip::

  OpenAPI Generatorの設定項目は、 ``--generator-name`` のようにハイフン区切りの形式になる。

:ref:`NablarchOpenApiGeneratorConfiguration` のうち本ツール固有の設定項目については、 ``--additional-properties`` に ``key=value`` の形式で指定する。複数指定する場合は ``,`` 区切りでの指定となる。

.. tip::

  本ツール固有の設定項目は、 ``--additional-properties=hideGenerationTimestamp=true`` のように ``--additional-properties=`` に続けて項目名をそのまま指定する。


ソースコード生成仕様
------------------------

以降では、本ツールがOpenAPIドキュメントを元にソースコードを生成する仕様について記載する。

.. important::

  Nablarch RESTfulウェブサービスはJakarta RESTful Web Servicesが提供するすべてのアノテーションをサポートしているわけではないため、ここで記載する内容以外のOpenAPIドキュメントの内容は生成されるソースコードに反映されないことに注意すること。

  Nablarch RESTfulウェブサービスがサポートしているアノテーションについては :ref:`restful_web_service_architecture` および、ルーティングアダプタの :ref:`router_adaptor_path_annotation` を参照すること。

リソース(アクション)インターフェース生成仕様
===============================================

ここではリソース(アクション)インターフェースの生成仕様を記載する。 :ref:`rest_feature_details-method_signature` に則った形で生成するのでこちらも参照すること。

リソース(アクション)インターフェースの生成単位や型定義に関する仕様を以下に示す。

* OpenAPIドキュメントに定義されたパスおよびオペレーションの情報を元に生成する。
* Javaのインターフェースとして生成する。
* リソース(アクション)インターフェースの生成単位は、以下から選択する。

  * デフォルトではOpenAPIドキュメントのパスの第一階層でまとめられたものとなる。
  * ``useTags`` を ``true`` にした場合はオペレーションに付与されているタグの単位となる。

* リソース(アクション)インターフェースの宣言には ``Path`` アノテーションを注釈する。
* ``Generated`` アノテーションを注釈する。

リソース(アクション)インターフェースのメソッド生成に関する仕様を以下に示す。

**メソッド宣言に注釈するアノテーション**

================== ====================================================================================================
アノテーション     説明
================== ====================================================================================================
``GET``            オペレーションのHTTPメソッドがGETの場合に注釈する。
``POST``           オペレーションのHTTPメソッドがPOSTの場合に注釈する。
``PUT``            オペレーションのHTTPメソッドがPUTの場合に注釈する。
``DELETE``         オペレーションのHTTPメソッドがDELETEの場合に注釈する。
``PATCH``          オペレーションのHTTPメソッドがPATCHの場合に注釈する。
``HEAD``           オペレーションのHTTPメソッドがHEADの場合に注釈する。
``OPTIONS``        オペレーションのHTTPメソッドがOPTIONSの場合に注釈する。
``Consumes``       リクエストのコンテンツタイプがある場合に注釈する。
``Produces``       レスポンスのコンテンツタイプがあり、 ``type: string`` かつ ``format: binary`` 以外の場合に注釈する。
``Valid``          リクエストボディがあり、 ``useBeanValidation``  が ``true`` の場合に注釈する。
================== ====================================================================================================

.. tip::

  ``type: string`` かつ ``format: binary`` はファイルダウンロードを意味しており、この場合のコンテンツタイプは :java:extdoc:`HttpResponse#setContentType<nablarch.fw.web.HttpResponse.setContentType(java.lang.String)>` を使用して設定する。

**メソッド名の生成仕様**

* OpenAPIドキュメントの ``operationId`` 要素の値をメソッド名として使用する。
* ``operationId`` 要素が指定されていない場合は、 パスの値とHTTPメソッド名を組み合わせてメソッド名を生成する。

**メソッド引数の生成仕様**

====================================================================== =============================================================================================================================
メソッド引数の型                                                       説明
====================================================================== =============================================================================================================================
リクエストモデルの型                                                   リクエストボディを受け取り、かつリクエストのコンテンツタイプがマルチパート以外の場合、対応するモデルの型の引数を設定する。
:java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>`   常に生成し、引数に設定する。
:java:extdoc:`ExecutionContext <nablarch.fw.ExecutionContext>`         常に生成し、引数に設定する。
====================================================================== =============================================================================================================================

.. tip::

  * RESTfulウェブサービスはJakarta RESTful Web Servicesで規定されている ``PathParam`` や ``QueryParam`` 等には対応していないため、 ``parameters`` の定義はメソッド引数には反映されない。これらの情報は :java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>` より取得すること。
  * リクエストのコンテンツタイプが ``multipart/form-data`` の場合は、リクエストモデルの型の引数は生成されない。アップロードされたファイルは :java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>` より取得すること。

**メソッド戻り値の生成仕様**

====================================================================== ==========================================================================================
メソッド戻り値の型                                                     説明
====================================================================== ==========================================================================================
:java:extdoc:`EntityResponse <nablarch.fw.jaxrs.EntityResponse>`       レスポンスがモデルの場合に生成する。型パラメータにはモデルの型を反映する。
:java:extdoc:`HttpResponse <nablarch.fw.web.HttpResponse>`             レスポンスがモデルでない場合やHTTPステータスコードが ``200`` 以外の場合に生成する。
====================================================================== ==========================================================================================

モデル生成仕様
===============

モデルの生成単位や型定義に関する仕様を以下に示す。

* スキーマとして定義しているモデルに対して生成する。
* Javaのクラスとして生成する。
* ``JsonTypeName`` アノテーションを注釈する。
* ``Generated`` アノテーションを注釈する。

モデルのプロパティに関する生成仕様を以下に示す。

* OpenAPIドキュメントのスキーマに定義されたフィールドに対応するプロパティを生成する。
* プロパティに対するgetterおよびsetterを生成し、 ``JsonProperty`` アノテーションを注釈する。
* プロパティの値を設定してモデル自身の型を返す、メソッドチェインが可能なメソッドを生成する。
* ``useBeanValidation`` が ``true`` かつOpenAPIドキュメントにバリデーション定義がある場合、 :ref:`bean_validation` を使用したバリデーションを有効にする。
* バリデーションで使用するアノテーションは、Nablarchの提供する :ref:`bean_validation` 固有のものとJakarta EE標準の :java:extdoc:`jakarta.validation.constraints` パッケージのものを使用する。

OpenAPIドキュメントでのデータ型やフォーマットとJavaのデータ型との対応仕様は :ref:`openapi_datatypes_format_to_java_datatypes` 、バリデーション定義とバリデーションで使用するアノテーションの対応仕様は :ref:`openapi_property_to_bean_validation` に記載する。

モデルのその他の生成仕様を以下に示す。

* ``hashCode`` 、 ``equals`` 、 ``toString`` メソッドを生成する。

生成されるソースコードが依存するモジュール
==================================================

本ツールで生成されるソースコードをビルドするには、依存関係に以下のモジュールが必要になる。

.. code-block:: xml

    <dependency>
      <groupId>com.nablarch.framework</groupId>
      <artifactId>nablarch-fw-jaxrs</artifactId>
    </dependency>
    <dependency>
       <groupId>com.nablarch.framework</groupId>
       <artifactId>nablarch-core-validation-ee</artifactId>
    </dependency>
    <dependency>
      <groupId>jakarta.ws.rs</groupId>
      <artifactId>jakarta.ws.rs-api</artifactId>
    </dependency>
    <dependency>
      <groupId>jakarta.annotation</groupId>
      <artifactId>jakarta.annotation-api</artifactId>
    </dependency>
    <dependency>
      <groupId>com.fasterxml.jackson.core</groupId>
      <artifactId>jackson-annotations</artifactId>
      <version>2.17.1</version>
    </dependency>

RESTfulウェブサービスのブランクプロジェクトに設定されている依存関係にはこれらはすべて含まれている。

.. _openapi_datatypes_format_to_java_datatypes:

OpenAPIドキュメントのデータ型およびフォーマットとJavaのデータ型の対応仕様
===========================================================================

OpenAPIドキュメント上で定義されたデータ型とフォーマットに対して、本ツールによるJavaのデータ型の対応表を以下に示す。

=================================== ======================================== =======================================================
OpenAPIでのデータ型( ``type`` )     OpenAPIでのフォーマット( ``format`` )    モデルのプロパティのデータ型
=================================== ======================================== =======================================================
``integer``                                                                  ``java.lang.Integer``
``integer``                         ``int32``                                ``java.lang.Integer``
``integer``                         ``int64``                                ``java.lang.Long``
``number``                                                                   ``java.math.BigDecimal``
``number``                          ``float``                                ``java.lang.Float``
``number``                          ``double``                               ``java.lang.Double``
``boolean``                                                                  ``java.lang.Boolean``
``string``                                                                   ``java.lang.String``
``string``                          ``byte``                                 ``byte[]``
``string``                          ``date``                                 ``java.time.LocalDate``
``string``                          ``date-time``                            ``java.time.OffsetDateTime``
``string``                          ``number``                               ``java.math.BigDecimal``
``string``                          ``uuid``                                 ``java.util.UUID``
``string``                          ``uri``                                  ``java.net.URI``
``string``                                                                   enum ( ``enum`` を指定すると対応するEnum型を生成する )
``array``                                                                    ``java.util.List``
``array``                                                                    ``java.util.Set`` ( ``uniqueItems: true`` の場合)
``object``                                                                   対応するモデルの型
``object``                                                                   対応する型がない場合は ``java.lang.Object``
=================================== ======================================== =======================================================

.. tip::

  * ``type: string`` かつ ``format: binary`` はリクエストのコンテンツタイプが ``multipart/form-data`` の場合のみ利用可能で、それ以外コンテンツタイプやレスポンスのモデル定義内で使用した場合はモデルの生成を中止する。
  * ``type: string`` の場合は上記表以外にも多数のフォーマットがあるが、すべて ``java.lang.String`` として生成する。

.. _openapi_property_to_bean_validation:

OpenAPIドキュメントのバリデーション定義とBean Validationの対応仕様
=======================================================================

本ツールでは ``useBeanValidation`` のデフォルト値が ``false`` のためOpenAPIドキュメントの定義に関わらずデフォルトでは :ref:`bean_validation` で使用するアノテーションは注釈しないが、 ``true`` とした場合はOpenAPIドキュメントの記述内容によって以下の2つの方針でプロパティにアノテーションを注釈する。

* OpenAPI仕様にて規定されているプロパティに対応するバリデーション
* ドメインバリデーション

OpenAPI仕様にて規定されているプロパティに対応するバリデーション
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

`OpenAPI仕様にて規定されているプロパティ(外部サイト、英語) <https://spec.openapis.org/oas/v3.0.3.html#properties>`_ を使用してバリデーション定義を行った場合、以下の対応表に沿ってアノテーションを注釈する。

=================================== ======================================== ========================================== ============================================================================================================
OpenAPIでのデータ型( ``type`` )     OpenAPIでのフォーマット( ``format`` )    OpenAPIで使用しているプロパティ            注釈するバリデーション用のアノテーション
=================================== ======================================== ========================================== ============================================================================================================
``integer``                         (フォーマットは問わない)                 ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``integer``                                                                  ``minimum`` および ``maximum``             :java:extdoc:`NumberRange(min = {minimum}, max = {maximum}) <nablarch.core.validation.ee.NumberRange>`
``integer``                         ``int32``                                ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``integer``                         ``int32``                                ``minimum`` および ``maximum``             :java:extdoc:`NumberRange(min = {minimum}, max = {maximum}) <nablarch.core.validation.ee.NumberRange>`
``integer``                         ``int64``                                ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``integer``                         ``int64``                                ``minimum`` および ``maximum``             :java:extdoc:`NumberRange(min = {minimum}, max = {maximum}) <nablarch.core.validation.ee.NumberRange>`
``number``                          (フォーマットは問わない)                 ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``number``                                                                   ``minimum`` および ``maximum``             :java:extdoc:`DecimalRange(min = "{minimum}", max = "{maximum}") <nablarch.core.validation.ee.DecimalRange>`
``number``                          ``float``                                ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``number``                          ``float``                                ``minimum`` および ``maximum``             :java:extdoc:`DecimalRange(min = "{minimum}", max = "{maximum}") <nablarch.core.validation.ee.DecimalRange>`
``number``                          ``double``                               ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``number``                          ``double``                               ``minimum`` および ``maximum``             :java:extdoc:`DecimalRange(min = "{minimum}", max = "{maximum}") <nablarch.core.validation.ee.DecimalRange>`
``boolean``                                                                  ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``string``                          (フォーマットは問わない)                 ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``string``                                                                   ``minLength`` および ``maxLength``         :java:extdoc:`Length(min = {minLength}, max = {maxLength}) <nablarch.core.validation.ee.Length>`
``string``                                                                   ``pattern``                                :java:extdoc:`Pattern(regexp = "{pattern}")<jakarta.validation.constraints.Pattern>`
``array``                                                                    ``required``                               :java:extdoc:`Required <nablarch.core.validation.ee.Required>`
``array``                                                                    ``minItems`` および ``maxItems``           :java:extdoc:`Size(min = {minItems}, max = {maxItems}) <nablarch.core.validation.ee.Size>`
=================================== ======================================== ========================================== ============================================================================================================

.. tip::

  * ``multipleOf`` 、 ``exclusiveMinimum`` 、 ``exclusiveMaximum`` 、 ``minProperties`` 、 ``maxProperties`` には対応していない。
  * ``minimum`` および ``maximum`` 、 ``minLength`` および ``maxLength`` 、 ``minItems`` および ``maxItems`` はどちらか片方だけでも指定可能。
  * Javaのデータ型が ``java.math.BigDecimal`` 、 ``java.util.List`` 、 ``java.util.Set`` またはモデルの場合は ``Valid`` アノテーションを注釈する。
  * :java:extdoc:`Pattern<jakarta.validation.constraints.Pattern>` のみJakarta Bean Validation標準のアノテーションを注釈し、それ以外はNablarchの提供する :ref:`bean_validation` 固有のアノテーションを注釈する。

ドメインバリデーション
+++++++++++++++++++++++++

本ツールでは、 `OpenAPI仕様の拡張プロパティ(外部サイト、英語) <https://spec.openapis.org/oas/v3.0.3.html#specification-extensions>`_ を使用してOpenAPI仕様では表現できない :ref:`bean_validation-domain_validation` ことをサポートする。

拡張プロパティには ``x-nablarch-domain`` を使用し、値にはドメイン名を指定する。

.. code-block:: yaml

        propertyName:
          type: string
          x-nablarch-domain: "domainName"

``useBeanValidation`` を ``true`` に指定してソースコードを生成すると、対象のプロパティに :java:extdoc:`Domain("{domainName}") <nablarch.core.validation.ee.Domain>` が注釈される。

なお、ドメインバリデーションには様々なバリデーション定義を含めることができるため、 競合する可能性があるバリデーション定義を検出した場合はソースコードの生成を中止する。これは、ドメインに含まれているバリデーションルールと同じものが指定された場合、重複してバリデーションが行われることになるためである。
  
具体的には、 ``x-nablarch-domain`` を指定したプロパティに対して、 ``minimum`` 、 ``maximum`` 、 ``minLength`` 、 ``maxLength`` 、 ``minItems`` 、 ``maxItems`` 、 ``pattern`` のいずれかが指定されている場合はソースコードの生成を中止する。

``required`` は必須項目を表しドメイン側で強制するものではないため、併用を可能とする。

バリデーションに関する運用上の注意点
========================================

本ツールを使用して、バリデーション定義を含めたソースコードを生成する場合の運用上の注意点を記載する。

OpenAPI仕様の規定範囲では項目単位や相関バリデーションの要求を満たせない場合の注意点
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

OpenAPI仕様で規定されているバリデーションは必須定義と長さチェック、正規表現によるチェックのみのため、業務アプリケーションが求めるものとしては不足することも想定される。

また自動生成されたソースコードを直接修正することは望ましくないため、ドメインバリデーションを使用しても生成されたモデルに相関バリデーションを実装できない。

このため、OpenAPI仕様や本ツールのカバー範囲ではバリデーションの要件を満たすことができず別途実装が必要となり、結果として自動生成したモデルと手動で実装したフォーム等でバリデーション定義が分散されやすい状況になることに注意すること。

**自動生成したモデルにはバリデーション定義を含めない場合の実装方法**

ここでは、バリデーション定義として自動生成したモデルと同じ定義のフォーム等を作成し、 :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` を使用してプロパティ値をコピー後、バリデーションを実施する方法を紹介する。

本ツールがデフォルトでバリデーション用のアノテーションを注釈しないのは、前述のとおりバリデーション定義が分散される状況が生まれやすいことを想定しており、それは望ましくないと考えているからである。

考え方としては :ref:`bean_validation-execute_explicitly` と同様で、実装イメージを以下に記載する。

.. code-block:: java

  public class ProjectAction implements ProjectsApi {  // ProjectsApiは本ツールで生成したインターフェース

      // インターフェースに定義されたメソッドを実装
      @Override
      public EntityResponse<ProjectResponse> createProject(ProjectCreateRequest projectCreateRequest, JaxRsHttpRequest jaxRsHttpRequest, ExecutionContext context) {
          // モデルと同じプロパティ定義に、単項目バリデーションや相関バリデーションを加えたフォーム
          ProjectCreateForm form;

          try {
              // ユーティリティクラス内でモデルからフォームに値をコピーした後、バリデーションを明示的に実行する
              form = ProjectValidatorUtil.validate(ProjectCreateForm.class, projectCreateRequest);
          } catch (ApplicationException e) {
              // バリデーションエラー時に任意の処理を行う
              // ...

              throw e;
          }

          // 省略

          return response;
      }
  }

  // ユーティリティクラスのイメージ
  public final class ProjectValidatorUtil {
      // その他の処理は省略

      /**
       * HTTPリクエストからBeanを生成し、バリデーションを行う。
       *
       * @param beanClass 生成したいBeanクラス
       * @param src プロパティのコピー元オブジェクト
       * @return  プロパティに値が登録されたBeanオブジェクト
       */
      public static <T> T validate(Class<T> beanClass, Object src) {
          T bean = BeanUtil.createAndCopy(beanClass, src));
          ValidatorUtil.validate(bean);
          return bean;
      }
  }

ドメインバリデーションを使用する場合の注意点
++++++++++++++++++++++++++++++++++++++++++++++++++

ドメインバリデーションを使用すると、モデルのプロパティに対するドメインを定義することでバリデーション定義をまとめたりOpenAPI仕様でサポートしていないバリデーションを使用できる。

ただしOpenAPI仕様でサポートしているバリデーション範囲も含めてバリデーション仕様がドメイン側に隠蔽されやすくなり、OpenAPIドキュメントからバリデーション仕様が見えなくなる可能性がある点に注意すること。

OpenAPIドキュメントと生成されるソースコードの例
---------------------------------------------------

以下に、OpenAPIドキュメントと生成されるソースコードの例を記載する。

ソースコード生成時の本ツールの設定例は以下とする。この設定と異なる設定項目が必要になる例では、本ツールの設定例も併記する。

.. code-block:: xml

            <configuration>
              <inputSpec>${project.basedir}/src/main/resources/openapi.yaml</inputSpec>
              <generatorName>nablarch-jaxrs</generatorName>
              <configOptions>
                <sourceFolder>src/gen/java</sourceFolder>
                <apiPackage>com.example.api</apiPackage>
                <modelPackage>com.example.model</modelPackage>
              </configOptions>
            </configuration>

なお、記載している各種例はイメージを掴むことを目的とするため抜粋での記載としている。

OpenAPIドキュメントのパスおよびオペレーションの定義とソースコードの生成例
===========================================================================

OpenAPIドキュメント例

.. code-block:: yaml

  /projects:
    post:
      tags:
      - project
      summary: プロジェクトを登録する
      description: プロジェクトを登録する
      operationId: createProject
      requestBody:
        description: プロジェクト登録情報
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ProjectCreateRequest'
      responses:
        "200":
          description: 登録したプロジェクト情報
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProjectResponse'
  /projects/{id}:
    get:
      tags:
      - project
      summary: プロジェクトを取得する
      description: プロジェクトIDを指定してプロジェクトを取得する
      operationId: findProjectById
      parameters:
      - name: id
        in: path
        description: ID
        required: true
        schema:
          type: string
      responses:
        "200":
          description: 取得したプロジェクト情報
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProjectResponse'
        "404":
          description: プロジェクトが見つからなかった場合

本ツールにより生成されるリソース(アクション)インターフェース例

.. code-block:: java

  @Path("/projects")
  @jakarta.annotation.Generated(value = "nablarch.tool.openapi.codegen.JavaNablarchJaxrsServerCodegen", date = "2024-12-10T13:54:26.470544738+09:00[Asia/Tokyo]", comments = "Generator version: 7.10.0")
  public interface ProjectsApi {
      /**
       * POST  : プロジェクトを登録する
       *
       * プロジェクトを登録する
       *
       * @param projectCreateRequest プロジェクト登録情報
       * @param jaxRsHttpRequest HTTPリクエスト
       * @param context ハンドラ実行コンテキスト
       * @return 登録したプロジェクト情報
       */
      @POST
      @Consumes({ "application/json" })
      @Produces({ "application/json" })
      EntityResponse<ProjectResponse> createProject(ProjectCreateRequest projectCreateRequest, JaxRsHttpRequest jaxRsHttpRequest, ExecutionContext context);

      /**
       * GET /{id} : プロジェクトを取得する
       *
       * プロジェクトIDを指定してプロジェクトを取得する
       *
       * @param jaxRsHttpRequest HTTPリクエスト
       * @param context ハンドラ実行コンテキスト
       * @return 取得したプロジェクト情報
       * @return プロジェクトが見つからなかった場合
       */
      @GET
      @Path("/{id}")
      @Produces({ "application/json" })
      EntityResponse<ProjectResponse> findProjectById(JaxRsHttpRequest jaxRsHttpRequest, ExecutionContext context);

  }

OpenAPIドキュメントのスキーマの定義とソースコードの生成例
============================================================

OpenAPIドキュメント例

.. code-block:: yaml

    ProjectResponse:
      description: プロジェクト情報
      type: object
      properties:
        id:
          format: uuid
          description: プロジェクトID
          type: string
        name:
          description: プロジェクト名
          type: string
        sales:
          format: int64
          description: 売上
          type: integer
        startDate:
          format: date
          description: 開始日
          type: string
        endDate:
          format: date
          description: 終了日
          type: string

本ツールにより生成されるモデル例

.. code-block:: java

  @JsonTypeName("ProjectResponse")
  @jakarta.annotation.Generated(value = "nablarch.tool.openapi.codegen.JavaNablarchJaxrsServerCodegen", date = "2024-12-10T13:54:26.470544738+09:00[Asia/Tokyo]", comments = "Generator version: 7.10.0")
  public class ProjectResponse   {
    private UUID id;
    private String name;
    private Long sales;
    private LocalDate startDate;
    private LocalDate endDate;
   
      /**
       * プロジェクトID
       */
      public ProjectResponse id(UUID id) {
          this.id = id;
          return this;
      }
   
      
      @JsonProperty("id")
      public UUID getId() {
          return id;
      }
   
      @JsonProperty("id")
      public void setId(UUID id) {
          this.id = id;
      }
   
      /**
       * プロジェクト名
       */
      public ProjectResponse name(String name) {
          this.name = name;
          return this;
      }
   
      
      @JsonProperty("name")
      public String getName() {
          return name;
      }
   
      @JsonProperty("name")
      public void setName(String name) {
          this.name = name;
      }
   
      /**
       * 売上
       */
      public ProjectResponse sales(Long sales) {
          this.sales = sales;
          return this;
      }
   
      
      @JsonProperty("sales")
      public Long getSales() {
          return sales;
      }
   
      @JsonProperty("sales")
      public void setSales(Long sales) {
          this.sales = sales;
      }
   
      /**
       * 開始日
       */
      public ProjectResponse startDate(LocalDate startDate) {
          this.startDate = startDate;
          return this;
      }
   
      
      @JsonProperty("startDate")
      public LocalDate getStartDate() {
          return startDate;
      }
   
      @JsonProperty("startDate")
      public void setStartDate(LocalDate startDate) {
          this.startDate = startDate;
      }
   
      /**
       * 終了日
       */
      public ProjectResponse endDate(LocalDate endDate) {
          this.endDate = endDate;
          return this;
      }
   
      
      @JsonProperty("endDate")
      public LocalDate getEndDate() {
          return endDate;
      }
   
      @JsonProperty("endDate")
      public void setEndDate(LocalDate endDate) {
          this.endDate = endDate;
      }

      // hashCode、equals、toString等は省略
  }

Bean Validationを使用するソースコードの生成例
====================================================================================================

OpenAPIドキュメント例

.. code-block:: yaml

  ## パスおよびオペレーション
  /projects:
    post:
      tags:
      - project
      summary: プロジェクトを作成する
      description: プロジェクトを作成する
      operationId: createProject
      requestBody:
        description: プロジェクト登録情報
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ProjectCreateRequest'
      responses:
        "200":
          description: project created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProjectResponse'

    ## スキーマ
    ProjectCreateRequest:
      description: プロジェクト作成リクエスト
      required:
      - projectName
      - projectType
      - startDate
      type: object
      properties:
        projectName:
          description: プロジェクト名
          maxLength: 100
          minLength: 1
          type: string
        projectType:
          description: プロジェクト種別
          maxLength: 100
          minLength: 1
          type: string
        startDate:
          format: date
          description: 開始日
          type: string
        endDate:
          format: date
          description: 終了日
          type: string

本ツールの設定例

.. code-block:: xml

            <configuration>
              <inputSpec>${project.basedir}/src/main/resources/openapi.yaml</inputSpec>
              <generatorName>nablarch-jaxrs</generatorName>
              <configOptions>
                <sourceFolder>src/gen/java</sourceFolder>
                <apiPackage>com.example.api</apiPackage>
                <modelPackage>com.example.model</modelPackage>
                <!-- Bean Validationを使用する場合はuseBeanValidationにtrueを指定する -->
                <useBeanValidation>true</useBeanValidation>
              </configOptions>
            </configuration>

本ツールにより生成されるリソース(アクション)インターフェース例

.. code-block:: java

  @Path("/projects")
  @jakarta.annotation.Generated(value = "nablarch.tool.openapi.codegen.JavaNablarchJaxrsServerCodegen", date = "2024-12-10T13:54:26.470544738+09:00[Asia/Tokyo]", comments = "Generator version: 7.10.0")
  public interface ProjectsApi {
      /**
       * POST  : プロジェクトを作成する
       *
       * プロジェクトを作成する
       *
       * @param projectCreateRequest プロジェクト登録情報
       * @param jaxRsHttpRequest HTTPリクエスト
       * @param context ハンドラ実行コンテキスト
       * @return project created
       */
      @POST
      @Consumes({ "application/json" })
      @Produces({ "application/json" })
      // HTTPボディでリクエストを受け取る場合に@Validアノテーションが付与される
      @Valid
      EntityResponse<ProjectResponse> createProject(ProjectCreateRequest projectCreateRequest, JaxRsHttpRequest jaxRsHttpRequest, ExecutionContext context);

  }

本ツールにより生成されるモデル例

.. code-block:: java

  @JsonTypeName("ProjectCreateRequest")
  @jakarta.annotation.Generated(value = "nablarch.tool.openapi.codegen.JavaNablarchJaxrsServerCodegen", date = "2024-12-10T13:54:26.470544738+09:00[Asia/Tokyo]", comments = "Generator version: 7.10.0")
  public class ProjectCreateRequest   {
    private String projectName;
    private String projectType;
    private LocalDate startDate;
    private LocalDate endDate;
  
      /**
       * プロジェクト名
       */
      public ProjectCreateRequest projectName(String projectName) {
          this.projectName = projectName;
          return this;
      }
  
  
      @JsonProperty("projectName")
      @Required @Length(min = 1, max = 100)
      public String getProjectName() {
          return projectName;
      }
  
      @JsonProperty("projectName")
      public void setProjectName(String projectName) {
          this.projectName = projectName;
      }
  
      /**
       * プロジェクト種別
       */
      public ProjectCreateRequest projectType(String projectType) {
          this.projectType = projectType;
          return this;
      }
  
  
      @JsonProperty("projectType")
      @Required @Length(min = 1, max = 100)
      public String getProjectType() {
          return projectType;
      }
  
      @JsonProperty("projectType")
      public void setProjectType(String projectType) {
          this.projectType = projectType;
      }
  
      /**
       * 開始日
       */
      public ProjectCreateRequest startDate(LocalDate startDate) {
          this.startDate = startDate;
          return this;
      }
  
  
      @JsonProperty("startDate")
      @Required
      public LocalDate getStartDate() {
          return startDate;
      }
  
      @JsonProperty("startDate")
      public void setStartDate(LocalDate startDate) {
          this.startDate = startDate;
      }
  
      /**
       * 終了日
       */
      public ProjectCreateRequest endDate(LocalDate endDate) {
          this.endDate = endDate;
          return this;
      }
  
  
      @JsonProperty("endDate")
  
      public LocalDate getEndDate() {
          return endDate;
      }
  
      @JsonProperty("endDate")
      public void setEndDate(LocalDate endDate) {
          this.endDate = endDate;
      }

      // hashCode、equals、toString等は省略
  }

ドメインバリデーションを使用するソースコードの生成例
=======================================================

OpenAPIドキュメント例

.. code-block:: yaml

  ## パスおよびオペレーション
  /projects:
    post:
      tags:
      - project
      summary: プロジェクトを作成する
      description: プロジェクトを作成する
      operationId: createProject
      requestBody:
        description: プロジェクト登録情報
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ProjectCreateRequest'
      responses:
        "200":
          description: project created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProjectResponse'

    ## スキーマ
    ProjectCreateRequest:
      description: プロジェクト作成リクエスト
      required:
      - projectName
      type: object
      properties:
        projectName:
          description: プロジェクト名
          type: string
          ## ドメインバリデーションの使用
          x-nablarch-domain: "projectName"

本ツールの設定例

.. code-block:: xml

            <configuration>
              <inputSpec>${project.basedir}/src/main/resources/openapi.yaml</inputSpec>
              <generatorName>nablarch-jaxrs</generatorName>
              <configOptions>
                <sourceFolder>src/gen/java</sourceFolder>
                <apiPackage>com.example.api</apiPackage>
                <modelPackage>com.example.model</modelPackage>
                <!-- Bean Validationを使用する場合はuseBeanValidationにtrueを指定する -->
                <useBeanValidation>true</useBeanValidation>
              </configOptions>
            </configuration>

本ツールにより生成されるモデル例

.. code-block:: java

  @JsonTypeName("ProjectCreateRequest")
  @jakarta.annotation.Generated(value = "nablarch.tool.openapi.codegen.JavaNablarchJaxrsServerCodegen", date = "2024-12-10T13:54:26.470544738+09:00[Asia/Tokyo]", comments = "Generator version: 7.10.0")
  public class ProjectCreateRequest   {
    private String projectName;
  
      /**
       * プロジェクト名
       */
      public ProjectCreateRequest projectName(String projectName) {
          this.projectName = projectName;
          return this;
      }
  
      
      @JsonProperty("projectName")
      @Required @Domain("projectName")
      public String getProjectName() {
          return projectName;
      }
  
      @JsonProperty("projectName")
      public void setProjectName(String projectName) {
          this.projectName = projectName;
      }

      // hashCode、equals、toString等は省略
  }

ファイルアップロードの定義例
==============================

OpenAPIドキュメント例

.. code-block:: yaml

  ## パスおよびオペレーション
  /customers/upload:
    post:
      tags:
      - customer
      summary: 顧客CSVファイルをアップロードする
      description: 顧客CSVファイルをアップロードして顧客情報を取り込む
      operationId: uploadCustomersCsvFile
      requestBody:
        description: 顧客CSVファイル情報
        content:
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CustomersCsvFileUploadRequest'
      responses:
        "200":
          description: 顧客CSVファイルアップロード取り込み結果
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CustomersCsvFileUploadResultResponse'


    ## スキーマ
    CustomersCsvFileUploadRequest:
      description: 顧客CSVファイル情報
      required:
      - fileName
      - file
      type: object
      properties:
        fileName:
          description: ファイル名
          type: string
        file:
          description: 顧客CSVファイル
          type: string
          format: binary

本ツールにより生成されるリソース(アクション)インターフェース例

.. code-block:: java

  @Path("/customers/upload")
  @jakarta.annotation.Generated(value = "nablarch.tool.openapi.codegen.JavaNablarchJaxrsServerCodegen", date = "2024-12-10T14:36:36.602623815+09:00[Asia/Tokyo]", comments = "Generator version: 7.10.0")
  public interface CustomersApi {
      /**
       * POST  : 顧客CSVファイルをアップロードする
       *
       * 顧客CSVファイルをアップロードして顧客情報を取り込む
       *
       * @param jaxRsHttpRequest HTTPリクエスト
       * @param context ハンドラ実行コンテキスト
       * @return 顧客CSVファイルアップロード取り込み結果
       */
      @POST
      @Consumes({ "multipart/form-data" })
      @Produces({ "application/json" })
      EntityResponse<CustomersCsvFileUploadResultResponse> uploadCustomersCsvFile(JaxRsHttpRequest jaxRsHttpRequest, ExecutionContext context);

  }

.. tip::

  ファイルアップロードの場合、リクエストのコンテンツタイプには ``multipart/form-data`` を指定する。またアップロードファイルには ``type: string`` かつ ``format: binary`` を指定する。この時、スキーマに対応するモデルのソースコードは生成されない。アップロードされたファイルは :java:extdoc:`JaxRsHttpRequest <nablarch.fw.jaxrs.JaxRsHttpRequest>` より取得する。

ファイルダウンロードの定義例
==============================

OpenAPIドキュメント例

.. code-block:: yaml

  /customers/upload:
    get:
      tags:
      - customer
      summary: 顧客情報をCSVファイルとしてダウンロードする
      description: 顧客情報をCSVファイルとしてダウンロードする
      operationId: downloadCustomersCsvFile
      responses:
        "200":
          description: 顧客CSVファイル
          content:
            text/csv:
              schema:
                type: string
                format: binary

本ツールにより生成されるリソース(アクション)インターフェース例

.. code-block:: java

  @Path("/customers/upload")
  @jakarta.annotation.Generated(value = "nablarch.tool.openapi.codegen.JavaNablarchJaxrsServerCodegen", date = "2024-12-10T14:48:03.670170037+09:00[Asia/Tokyo]", comments = "Generator version: 7.10.0")
  public interface CustomersApi {
      /**
       * GET  : 顧客情報をCSVファイルとしてダウンロードする
       *
       * 顧客情報をCSVファイルとしてダウンロードする
       *
       * @param jaxRsHttpRequest HTTPリクエスト
       * @param context ハンドラ実行コンテキスト
       * @return 顧客CSVファイル
       */
      @GET
      HttpResponse downloadCustomersCsvFile(JaxRsHttpRequest jaxRsHttpRequest, ExecutionContext context);

  }

.. tip::

  ファイルダウンロードではレスポンスのコンテンツタイプは任意となる。レスポンスのスキーマ定義は ``type: string`` かつ ``format: binary`` とし、ダウンロードするファイルの内容やレスポンスヘッダは :java:extdoc:`HttpResponse <nablarch.fw.web.HttpResponse>` を使って設定する。


.. |br| raw:: html

  <br />
