.. _data_bind:

データバインド
==================================================

.. contents:: 目次
  :depth: 3
  :local:

CSVやTSVといったデータファイルのデータをJava Beansオブジェクト及びMapオブジェクトとして扱う機能を提供する。

機能概要
---------------------------------------------------------------------

データをJava Beansオブジェクトとして扱うことができる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
データファイルのデータをJava Beansオブジェクトとして扱うことができる。

Java Beansオブジェクトへの変換時、Java Beansクラスに定義されたプロパティの型に
:java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` を使用して自動的に型変換を行う。
型変換に失敗した場合は例外が発生し、Java Beansオブジェクトは生成されない。

.. important::

  アップロードファイルなどの外部から受け付けたデータを読み込む場合は、
  不正なデータの場合でも異常終了とせずに不正な値を業務エラーとして通知する必要があるため、
  Java Beansクラスのプロパティは全てString型で定義しなければならない。

データをJava Beansオブジェクトとして扱う方法の詳細は以下を参照。

* :ref:`data_bind-file_to_bean`
* :ref:`data_bind-bean_to_file`

データをMapオブジェクトとして扱うことができる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
データファイルのデータをMapオブジェクトとして扱うことができる。

Mapオブジェクトへの変換時、値は全てString型で格納される。

詳細は以下を参照。

* :ref:`data_bind-file_to_map`
* :ref:`data_bind-map_to_file`

データファイルのフォーマットをアノテーションで指定することができる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
データファイルのフォーマットは設定ファイルに記述するのではなく、
アノテーションや :java:extdoc:`DataBindConfig <nablarch.common.databind.DataBindConfig>` を使用して定義することができる。

詳細なフォーマットの指定方法は、 :ref:`data_bind-csv_format` を参照。

モジュール一覧
---------------------------------------------------------------------

.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-databind</artifactId>
  </dependency>

  <!-- ファイルダウンロードを使用する場合のみ -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web-extension</artifactId>
  </dependency>

使用方法
---------------------------------------------------------------------

.. _data_bind-file_to_bean:

データをJava Beansオブジェクトとして読み込む
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
データファイルを先頭から1データずつ読み込み、Java Beansオブジェクトとして取得することができる。

データの読み込みは、 :java:extdoc:`ObjectMapperFactory#create <nablarch.common.databind.ObjectMapperFactory.create(java.lang.Class,%20java.io.InputStream)>`
で生成した :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` を使用して行い、
:java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` の生成時に指定した、
Java Beansクラスに定義されたアノテーションをもとにデータを読み込む。

Java Beansクラスへのアノテーション定義方法の詳細は、
:ref:`CSVファイルをJava Beansクラスにバインドする場合のフォーマット指定方法 <data_bind-csv_format-beans>` を参照。

全データを読み込む場合の実装例を以下に示す。

.. code-block:: java

  try (ObjectMapper<Person> mapper = ObjectMapperFactory.create(Person.class, inputStream)) {
      Person person;
      while ((person = mapper.read()) != null) {
          // Java Beansオブジェクトごとの処理を記述(Java Beansオブジェクトへの変換処理など)
      }
  } catch (InvalidDataFormatException e) {
      // 読み込んだデータのフォーマットが不正な場合の処理を記述
  }

.. important::

  全データの読み込みが完了したら、 :java:extdoc:`ObjectMapper#close <nablarch.common.databind.ObjectMapper.close()>` でリソースを解放すること。

  ただし、Java7以降の環境であれば ``try-with-resources`` を使用することでクローズ処理を省略可能。

.. _data_bind-bean_to_file:

Java Beansオブジェクトの内容をデータファイルに書き込む
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Java Beansオブジェクトの内容をデータファイルに1データずつ書き込むことができる。

データファイルへの書き込みは、 :java:extdoc:`ObjectMapperFactory#create <nablarch.common.databind.ObjectMapperFactory.create(java.lang.Class,%20java.io.OutputStream)>`
で生成した :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` を使用して行い、
:java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` の生成時に指定した、
Java Beansクラスに定義されたアノテーションをもとにデータを書き込む。

Java Beansクラスへのアノテーション定義方法の詳細は、
:ref:`CSVファイルをJava Beansクラスにバインドする場合のフォーマット指定方法 <data_bind-csv_format-beans>` を参照。

リスト内の全てのJava Beansオブジェクトをデータファイルに書き込む場合の実装例を以下に示す。

.. code-block:: java

  try (ObjectMapper<Person> mapper = ObjectMapperFactory.create(Person.class, outputStream)) {
      for (Person person : personList) {
          mapper.write(person);
      }
  }

.. tip::

  プロパティの値が ``null`` の場合は、未入力を表す値が出力される。
  例えば、CSVファイルに書き込む場合は空文字が出力される。

.. _data_bind-file_to_map:

データをMapオブジェクトとして読み込む
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
データファイルを先頭から1データずつ読み込み、Mapオブジェクトとして取得することができる。

データの読み込みは、
:java:extdoc:`ObjectMapperFactory#create <nablarch.common.databind.ObjectMapperFactory.create(java.lang.Class,%20java.io.InputStream,%20nablarch.common.databind.DataBindConfig)>`
で生成した :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` を使用して行い、
:java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` の生成時に指定した、
:java:extdoc:`DataBindConfig <nablarch.common.databind.DataBindConfig>` の設定値をもとにデータを読み込む。

:java:extdoc:`DataBindConfig <nablarch.common.databind.DataBindConfig>` への設定方法の詳細は、
:ref:`CSVファイルをMapクラスにバインドする場合のフォーマット指定方法 <data_bind-csv_format-map>` を参照。

データファイルの全データを読み込む場合の実装例を以下に示す。

.. code-block:: java

  // DataBindConfigオブジェクトを生成
  DataBindConfig config = CsvDataBindConfig.DEFAULT.withHeaderTitles("年齢", "名前");
  try (ObjectMapper<Map> mapper = ObjectMapperFactory.create(Map.class, inputStream, config)) {
      Person person;
      while ((person = mapper.read()) != null) {
          // Java Beansオブジェクトごとの処理を記述(Java Beansオブジェクトへの変換処理など)
      }
  } catch (InvalidDataFormatException e) {
      // 読み込んだデータのフォーマットが不正な場合の処理を記述
  }

.. _data_bind-map_to_file:

Mapオブジェクトの内容をデータファイルに書き込む
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Mapオブジェクトの内容をデータファイルに1データずつ書き込むことができる。

データファイルへの書き込みは、
:java:extdoc:`ObjectMapperFactory#create <nablarch.common.databind.ObjectMapperFactory.create(java.lang.Class,%20java.io.OutputStream,%20nablarch.common.databind.DataBindConfig)>`
で生成した :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` を使用して行い、
:java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` の生成時に指定した、
:java:extdoc:`DataBindConfig <nablarch.common.databind.DataBindConfig>` の設定値をもとにデータを書き込む。

:java:extdoc:`DataBindConfig <nablarch.common.databind.DataBindConfig>` への設定方法の詳細は、
:ref:`CSVファイルをMapクラスにバインドする場合のフォーマット指定方法 <data_bind-csv_format-map>` を参照。

リスト内の全てのMapオブジェクトをデータファイルに書き込む場合の実装例を以下に示す。

.. code-block:: java

  // DataBindConfigオブジェクトを生成
  DataBindConfig config = CsvDataBindConfig.DEFAULT.withHeaderTitles("年齢", "名前");
  try (ObjectMapper<Map> mapper = ObjectMapperFactory.create(Map.class, outputStream, config)) {
      for (Map<String, Object> person : personList) {
          mapper.write(person);
      }
  }

.. tip::

  Mapオブジェクトのvalue値が ``null`` の場合は、未入力を表す値が出力される。
  例えば、CSVファイルに書き込む場合は空文字が出力される。

データの論理行番号を取得する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
データファイルのデータをJava Beansオブジェクトとして取得する際、Java Beansクラスにプロパティを定義して
:java:extdoc:`LineNumber <nablarch.common.databind.LineNumber>` を使用することで、データの論理行番号も一緒に取得することができる。

例えば、入力値チェック時にバリデーションエラーが発生したデータの行番号をログに出力したい場合などに使用する。

実装例を以下に示す。

.. code-block:: java

  private Long lineNumber;

  @LineNumber
  public Long getLineNumber() {
      return lineNumber;
  }

.. tip::

  Mapオブジェクトとして取得する場合は、データの行番号を取得できない点に注意すること。


.. _data_bind-validation:

データの入力値をチェックする
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
データをJava Beansオブジェクトとして読み込むことができるため、
:ref:`bean_validation` による入力値チェックを行うことができる。

実装例を以下に示す。

.. code-block:: java

  try (ObjectMapper<Person> mapper = ObjectMapperFactory.create(Person.class, inputStream)) {
      Person person;
      while ((person = mapper.read()) != null) {
          // 入力値チェックを実行
          ValidatorUtil.validate(person);

          // 後続の処理は省略
      }
  } catch (InvalidDataFormatException e) {
      // データファイルのフォーマット不正時の処理を記述
  }

.. _data_bind-file_download:

ファイルダウンロードで使用する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ウェブアプリケーションで、Java Beansオブジェクトの内容をデータファイルとしてダウンロードするための実装例を以下に示す。

ポイント
  * データをメモリ上に展開すると大量データのダウンロード時などにメモリを圧迫する恐れがあるため、一時ファイルに出力する。
  * データファイルへの書き込みについては、 :ref:`data_bind-bean_to_file` を参照。
  * :java:extdoc:`FileResponse <nablarch.common.web.download.FileResponse>` オブジェクト生成時にデータファイルを指定する。
  * リクエスト処理の終了時に自動的にファイルを削除する場合は、 `FileResponse` のコンストラクタの第二引数に ``true`` を指定する。
  * レスポンスに `Content-Type` 及び `Content-Disposition` を設定する。

.. code-block:: java

  public HttpResponse download(HttpRequest request, ExecutionContext context) {

      // 業務処理

      final Path path = Files.createTempFile(null, null);
      try (ObjectMapper<Person> mapper =
              ObjectMapperFactory.create(Person.class, Files.newOutputStream(path))) {
          for (Person person : persons) {
              mapper.write(BeanUtil.createAndCopy(PersonDto.class, person));
          }
      }

      // ファイルをボディに設定する。
      FileResponse response = new FileResponse(path.toFile(), true);

      // Content-Typeヘッダ、Content-Dispositionヘッダを設定する
      response.setContentType("text/csv; charset=Shift_JIS");
      response.setContentDisposition("person.csv");

      return response;
  }

.. _data_bind-upload_file:

アップロードファイルのデータを読み込む
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ウェブアプリケーションで、画面からアップロードされたデータファイルをJava Beansオブジェクトとして読み込むための実装例を以下に示す。

ポイント
 * :java:extdoc:`PartInfo#getInputStream <nablarch.fw.web.upload.PartInfo.getInputStream()>` を使用して、アップロードファイルのストリームを取得する。
 * 不正なデータが入力されている可能性があるため、:ref:`bean_validation` を使用して入力チェックを行う。

.. code-block:: java

  List<PartInfo> partInfoList = request.getPart("uploadFile");
  if (partInfoList.isEmpty()) {
      // アップロードファイルが見つからない場合の処理を記述
  }

  PartInfo partInfo = partInfoList.get(0);
  try (ObjectMapper<Person> mapper = ObjectMapperFactory.create(Person.class, partInfo.getInputStream())) {
      Person person;
      while ((person = mapper.read()) != null) {
          // 入力値チェックを実行
          ValidatorUtil.validate(person);

          // 後続の処理は省略
      }
  } catch (InvalidDataFormatException e) {
      // データファイルのフォーマット不正時の処理を記述
  }

.. _data_bind-csv_format:

CSVファイルのフォーマットを指定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CSVファイルのフォーマット指定は、Java Beansクラスにバインドする場合とMapクラスにバインドする場合で2種類の指定方法がある。

.. _data_bind-csv_format-beans:

Java Beansクラスにバインドする場合
  以下のアノテーションを使用してフォーマットを指定する。

  * :java:extdoc:`Csv <nablarch.common.databind.csv.Csv>`
  * :java:extdoc:`CsvFormat <nablarch.common.databind.csv.CsvFormat>`

  CSVファイルのフォーマットは予め用意したフォーマットセットの中から選択することができる。
  フォーマットセットについては  :ref:`data_bind-csv_format_set` を参照。

  以下に実装例を示す。

  .. code-block:: java

    @Csv(type = Csv.CsvType.DEFAULT, properties = {"age", "name"}, headers = {"年齢", "氏名"})
    public class Person {
        private Integer age;
        private String name;

        // getter、setterは省略。
    }

  また、CSVファイルのフォーマットが、予め用意したフォーマットセットのいずれにも当てはまらない場合は、
  :java:extdoc:`CsvFormat <nablarch.common.databind.csv.CsvFormat>` を使用して個別にフォーマットを指定することができる。

  以下に実装例を示す。

  .. code-block:: java

    // type属性にCUSTOMを指定する。
    @Csv(type = Csv.CsvType.CUSTOM, properties = {"age", "name"})
    @CsvFormat(
            fieldSeparator = '\t',
            lineSeparator = "\r\n",
            quote = '\'',
            ignoreEmptyLine = false,
            requiredHeader = false,
            charset = "UTF-8",
            quoteMode = CsvDataBindConfig.QuoteMode.ALL)
    public class Person {
        private Integer age;
        private String name;

        // getter、setterは省略。
    }

  .. tip::

    Java Beansクラスにバインドする場合、フォーマット指定はアノテーションで行うため、
    :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` の生成時に
    :java:extdoc:`DataBindConfig <nablarch.common.databind.DataBindConfig>` を使用したフォーマットの指定はできない。

.. _data_bind-csv_format-map:

Mapクラスにバインドする場合
  :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` の生成時に
  :java:extdoc:`CsvDataBindConfig <nablarch.common.databind.csv.CsvDataBindConfig>` を使用して個別にフォーマットを指定する。

  また、フォーマットを指定する際は、Mapオブジェクトのキーとして使用するため、
  :java:extdoc:`CsvDataBindConfig#withHeaderTitles <nablarch.common.databind.csv.CsvDataBindConfig.withHeaderTitles(java.lang.String...)>`
  でCSVファイルのヘッダフィールド名を設定する必要がある。

  以下に実装例を示す。

  .. code-block:: java

    DataBindConfig config = CsvDataBindConfig.DEFAULT.withHeaderTitles("年齢", "名前");
    ObjectMapper<Map> mapper = ObjectMapperFactory.create(Map.class, outputStream, config);


拡張例
---------------------------------------------------------------------

Java Beansクラスにバインドできるファイル形式を追加する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Java Beansクラスにバインドできるファイル形式を追加するには、以下の手順が必要となる。

1. 指定した形式のファイルとJava Beansクラスをバインドさせるため、 :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` の実装クラスを作成する。
2. :java:extdoc:`ObjectMapperFactory <nablarch.common.databind.ObjectMapperFactory>` を継承したクラスを作成し、
   先ほど作成した :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` の実装クラスを生成する処理を追加する。
3. :java:extdoc:`ObjectMapperFactory <nablarch.common.databind.ObjectMapperFactory>` の継承クラスをコンポーネント設定ファイルに設定する。
   以下にコンポーネント設定ファイルへの設定例を示す。


  ポイント
   * コンポーネント名は、 **objectMapperFactory** とすること。

  .. code-block:: xml

    <component name="objectMapperFactory" class="sample.SampleObjectMapperFactory" />

.. _data_bind-csv_format_set:

CSVファイルのフォーマットとして指定できるフォーマットセット
---------------------------------------------------------------------
デフォルトで提供しているCSVファイルのフォーマットセット及び設定値は以下のとおり。

================== ================= ================= ================= =================
\                  DEFAULT           RFC4180           EXCEL             TSV
================== ================= ================= ================= =================
列区切り           カンマ(,)         カンマ(,)         カンマ(,)         タブ(\\t)
行区切り           改行(\\r\\n)      改行(\\r\\n)      改行(\\r\\n)      改行(\\r\\n)
フィールド囲み文字 ダブルクォート(") ダブルクォート(") ダブルクォート(") ダブルクォート(")
空行を無視         true              false             false             false
ヘッダ行あり       true              false             false             false
文字コード         UTF-8             UTF-8             UTF-8             UTF-8
クォートモード     NORMAL            NORMAL            NORMAL            NORMAL
================== ================= ================= ================= =================

クォートモード
  クォートモードとは、CSVファイルへの書き込み時にどのフィールドをフィールド囲み文字で囲むかを示すモードである。
  クォートモードは以下のモードから選択することができる。

  ================ ================================================================
  クォートモード名 フィールド囲み文字で囲む対象のフィールド
  ================ ================================================================
  NORMAL           フィールド囲み文字、列区切り文字、改行のいずれかを含むフィールド
  ALL              全てのフィールド
  ================ ================================================================

  .. tip::

    CSVファイルの読み込み時は、クォートモードは使用せずに自動的にフィールド囲み文字の有無を判定して読み込みを行う。