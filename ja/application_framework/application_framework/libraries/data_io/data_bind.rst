.. _data_bind:

データバインド
==================================================

.. contents:: 目次
  :depth: 3
  :local:

CSVやTSV、固定長といったデータをJava Beansオブジェクト及びMapオブジェクトとして扱う機能を提供する。

機能概要
---------------------------------------------------------------------

データをJava Beansオブジェクトとして扱うことができる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
データファイルのデータをJava Beansオブジェクトとして扱うことができる。

Java Beansオブジェクトへの変換時、Java Beansクラスに定義されたプロパティの型に
:java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` を使用して自動的に型変換する。
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

データファイルのフォーマットをアノテーションで指定できる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
データファイルのフォーマットは設定ファイルに記述するのではなく、
アノテーションや :java:extdoc:`DataBindConfig <nablarch.common.databind.DataBindConfig>` を使用して定義できる。

詳細なフォーマットの指定方法は以下を参照。

  * :ref:`data_bind-csv_format`
  * :ref:`data_bind-fixed_length_format`

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
データファイルを先頭から1データずつ読み込み、Java Beansオブジェクトとして取得できる。

データの読み込みは、 :java:extdoc:`ObjectMapperFactory#create <nablarch.common.databind.ObjectMapperFactory.create(java.lang.Class,java.io.InputStream)>`
で生成した :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` [#thread-unsafe]_ を使用して行い、
:java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` の生成時に指定した、
Java Beansクラスに定義されたアノテーションをもとにデータを読み込む。

Java Beansクラスへのアノテーション定義方法の詳細は以下を参照。

  * :ref:`CSVファイルをJava Beansクラスにバインドする場合のフォーマット指定方法 <data_bind-csv_format-beans>`
  * :ref:`固定長ファイルをJava Beansクラスにバインドする場合のフォーマット指定方法 <data_bind-fixed_length_format-beans>`

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

  ``try-with-resources`` を使用することでクローズ処理を省略可能。

.. _data_bind-bean_to_file:

Java Beansオブジェクトの内容をデータファイルに書き込む
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Java Beansオブジェクトの内容をデータファイルに1データずつ書き込むことができる。

データファイルへの書き込みは、 :java:extdoc:`ObjectMapperFactory#create <nablarch.common.databind.ObjectMapperFactory.create(java.lang.Class,java.io.OutputStream)>`
で生成した :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>`  [#thread-unsafe]_ を使用して行い、
:java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` の生成時に指定した、
Java Beansクラスに定義されたアノテーションをもとにデータを書き込む。

Java Beansクラスへのアノテーション定義方法の詳細は以下を参照。

  * :ref:`CSVファイルをJava Beansクラスにバインドする場合のフォーマット指定方法 <data_bind-csv_format-beans>`
  * :ref:`固定長ファイルをJava Beansクラスにバインドする場合のフォーマット指定方法 <data_bind-fixed_length_format-beans>`

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
データファイルを先頭から1データずつ読み込み、Mapオブジェクトとして取得できる。

データの読み込みは、
:java:extdoc:`ObjectMapperFactory#create <nablarch.common.databind.ObjectMapperFactory.create(java.lang.Class,java.io.InputStream,nablarch.common.databind.DataBindConfig)>`
で生成した :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` [#thread-unsafe]_ を使用して行い、
:java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` の生成時に指定した、
:java:extdoc:`DataBindConfig <nablarch.common.databind.DataBindConfig>` の設定値をもとにデータを読み込む。

:java:extdoc:`DataBindConfig <nablarch.common.databind.DataBindConfig>` への設定方法の詳細は以下を参照。

  * :ref:`CSVファイルをMapクラスにバインドする場合のフォーマット指定方法 <data_bind-csv_format-map>`
  * :ref:`固定長ファイルをMapクラスにバインドする場合のフォーマット指定方法 <data_bind-fixed_length_format-map>`

CSVファイルの全データを読み込む場合の実装例を以下に示す。

.. code-block:: java

  // DataBindConfigオブジェクトを生成
  DataBindConfig config = CsvDataBindConfig.DEFAULT.withHeaderTitles("年齢", "名前")
                                                   .withProperties("age", "name");
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
:java:extdoc:`ObjectMapperFactory#create <nablarch.common.databind.ObjectMapperFactory.create(java.lang.Class,java.io.OutputStream,nablarch.common.databind.DataBindConfig)>`
で生成した :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` [#thread-unsafe]_ を使用して行い、
:java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` の生成時に指定した、
:java:extdoc:`DataBindConfig <nablarch.common.databind.DataBindConfig>` の設定値をもとにデータを書き込む。

:java:extdoc:`DataBindConfig <nablarch.common.databind.DataBindConfig>` への設定方法の詳細は以下を参照。

  * :ref:`CSVファイルをMapクラスにバインドする場合のフォーマット指定方法 <data_bind-csv_format-map>`
  * :ref:`固定長ファイルをMapクラスにバインドする場合のフォーマット指定方法 <data_bind-fixed_length_format-map>`

リスト内の全てのMapオブジェクトをCSVファイルに書き込む場合の実装例を以下に示す。

.. code-block:: java

  // DataBindConfigオブジェクトを生成
  DataBindConfig config = CsvDataBindConfig.DEFAULT.withHeaderTitles("年齢", "名前")
                                                   .withProperties("age", "name");
  try (ObjectMapper<Map> mapper = ObjectMapperFactory.create(Map.class, outputStream, config)) {
      for (Map<String, Object> person : personList) {
          mapper.write(person);
      }
  }

.. tip::

  Mapオブジェクトのvalue値が ``null`` の場合は、未入力を表す値が出力される。
  例えば、CSVファイルに書き込む場合は空文字が出力される。
  
.. _data_bind-line_number:

ファイルのデータの論理行番号を取得する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ファイルのデータをJava Beansオブジェクトとして取得する際、Java Beansクラスにプロパティを定義して
:java:extdoc:`LineNumber <nablarch.common.databind.LineNumber>` を使用することで、データの論理行番号も一緒に取得できる。

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

  CSVファイルのフォーマットは予め用意したフォーマットセットの中から選択できる。
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
  :java:extdoc:`CsvFormat <nablarch.common.databind.csv.CsvFormat>` を使用して個別にフォーマットを指定できる。

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
            quoteMode = CsvDataBindConfig.QuoteMode.ALL,
            emptyToNull = true)
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

  また、フォーマットを指定する際は、
  :java:extdoc:`CsvDataBindConfig#withProperties <nablarch.common.databind.csv.CsvDataBindConfig.withProperties(java.lang.String...)>`
  で設定したプロパティ名がMapオブジェクトのキーとして使用される。
  なお、CSVにヘッダ行が存在する場合は、プロパティ名の設定を省略することでヘッダタイトルをキーとして使用できる。

  以下に実装例を示す。

  ポイント
    * ヘッダタイトル、プロパティ名はCSVの項目順と一致するように定義すること

  .. code-block:: java

    // ヘッダタイトル、プロパティ名はCSVの項目順と一致するように定義する
    DataBindConfig config = CsvDataBindConfig.DEFAULT.withHeaderTitles("年齢", "名前")
                                                     .withProperties("age", "name");
    ObjectMapper<Map> mapper = ObjectMapperFactory.create(Map.class, outputStream, config);

.. _data_bind-fixed_length_format:

固定長ファイルのフォーマットを指定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
固定長ファイルのフォーマット指定は、Java Beansクラスにバインドする場合とMapクラスにバインドする場合で2種類の指定方法がある。

.. _data_bind-fixed_length_format-beans:

Java Beansクラスにバインドする場合
  以下のアノテーションを使用してフォーマットを指定する。

  * :java:extdoc:`FixedLength <nablarch.common.databind.fixedlength.FixedLength>`
  * :java:extdoc:`Field <nablarch.common.databind.fixedlength.Field>`

  また、固定長ファイルの各フィールドに対し、パディングやトリム等を変換するコンバータを指定できる。
  標準で指定できるコンバータについては、 :java:extdoc:`nablarch.common.databind.fixedlength.converter` パッケージ配下を参照。

  以下に実装例を示す。

  .. code-block:: java

    @FixedLength(length = 19, charset = "MS932", lineSeparator = "\r\n")
    public class Person {

        @Field(offset = 1, length = 3)
        @Lpad
        private Integer age;

        @Field(offset = 4, length = 16)
        @Rpad
        private String name;

        // getter、setterは省略
    }

  もし、以下の様に未使用領域が存在するフォーマットの場合、
  固定長ファイルへの書き込み時に ``FixedLength#fillChar`` に設定した文字で自動的にパディングされる。(デフォルトは半角スペース)

  .. code-block:: java

    @FixedLength(length = 24, charset = "MS932", lineSeparator = "\r\n", fillChar = '0')
    public class Person {

        @Field(offset = 1, length = 3)
        @Lpad
        private Integer age;

        @Field(offset = 9, length = 16)
        @Rpad
        private String name;

        // getter、setterは省略
    }

.. _data_bind-fixed_length_format-map:

Mapクラスにバインドする場合
  :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` の生成時に
  :java:extdoc:`FixedLengthDataBindConfig <nablarch.common.databind.fixedlength.FixedLengthDataBindConfig>` を使用して個別にフォーマットを指定する。

  :java:extdoc:`FixedLengthDataBindConfig <nablarch.common.databind.fixedlength.FixedLengthDataBindConfig>` は、
  :java:extdoc:`FixedLengthDataBindConfigBuilder <nablarch.common.databind.fixedlength.FixedLengthDataBindConfigBuilder>` を使用して生成できる。

  以下に実装例を示す。

  .. code-block:: java

    final DataBindConfig config = FixedLengthDataBindConfigBuilder
            .newBuilder()
            .length(19)
            .charset(Charset.forName("MS932"))
            .lineSeparator("\r\n")
            .singleLayout()
            .field("age", 1, 3, new Lpad.Converter('0'))
            .field("name", 4, 16, new Rpad.RpadConverter(' '))
            .build();

    final ObjectMapper<Map> mapper = ObjectMapperFactory.create(Map.class, outputStream, config);

.. _data_bind-fixed_length_format-multi_layout:

固定長ファイルに複数のフォーマットを指定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
複数のフォーマットを持つ固定長ファイルのフォーマット指定についても、
Java Beansクラスにバインドする場合とMapクラスにバインドする場合で2種類の指定方法がある。

Java Beansクラスにバインドする場合
  フォーマットごとにJavaBeansクラスを定義して、それらのJava Beansクラスをプロパティとして持つ
  :java:extdoc:`MultiLayout <nablarch.common.databind.fixedlength.MultiLayout>` の継承クラスを作成することで、
  複数フォーマットの固定長ファイルに対応できる。

  以下にフォーマット指定の実装例を示す。

  ポイント
    * フォーマットごとにJava Beansクラスを定義する。
    * 上記のフォーマットを定義したJava Beansクラスをプロパティとして持つ、
      :java:extdoc:`MultiLayout <nablarch.common.databind.fixedlength.MultiLayout>` の継承クラスを定義する。
    * :java:extdoc:`MultiLayout <nablarch.common.databind.fixedlength.MultiLayout>` の継承クラスに
      :java:extdoc:`FixedLength <nablarch.common.databind.fixedlength.FixedLength>` アノテーションを設定し、 ``multiLayout`` 属性に ``true`` を設定する。
    * :java:extdoc:`MultiLayout#getRecordIdentifier <nablarch.common.databind.fixedlength.MultiLayout.getRecordIdentifier()>` メソッドをオーバーライドして、
      対象のデータがどのフォーマットに紐づくかを識別する :java:extdoc:`RecordIdentifier <nablarch.common.databind.fixedlength.MultiLayoutConfig.RecordIdentifier>` の実装クラスを返却する。

  .. code-block:: java

    @FixedLength(length = 20, charset = "MS932", lineSeparator = "\r\n", multiLayout = true)
    public class Person extends MultiLayout {

        @Record
        private Header header;

        @Record
        private Data data;

        @Override
        public RecordIdentifier getRecordIdentifier() {
            return new RecordIdentifier() {
                @Override
                public RecordName identifyRecordName(byte[] record) {
                    return record[0] == 0x31 ? RecordType.HEADER : RecordType.DATA;
                }
            };
        }

        // getter、setterは省略
    }

    public class Header {

        @Field(offset = 1, length = 1)
        private Long id;

        @Rpad
        @Field(offset = 2, length = 19)
        private String field;

        // getter、setterは省略
    }

    public class Data {

        @Field(offset = 1, length = 1)
        private Long id;

        @Lpad
        @Field(offset = 2, length = 3)
        private Long age;

        @Rpad
        @Field(offset = 5, length = 16)
        private String name;

        // getter、setterは省略
    }

    enum RecordType implements MultiLayoutConfig.RecordName {
        HEADER {
            @Override
            public String getRecordName() {
                return "header";
            }
        },
        DATA {
            @Override
            public String getRecordName() {
                return "data";
            }
        }
    }

  次に、指定されたフォーマットをもとに固定長データの読み込み・書き込みを行う実装例を示す。

  .. code-block:: java

    // 読み込む場合の実装例
    try (ObjectMapper<Person> mapper = ObjectMapperFactory.create(Person.class, inputStream)) {
        final Person person = mapper.read();
        if (RecordType.HEADER == person.getRecordName()) {
            final Header header = person.getHeader();

            // 後続の処理は省略
        }
    }

    // 書き込む場合の実装例
    try (ObjectMapper<Person> mapper = ObjectMapperFactory.create(Person.class, outputStream)) {
        final Person person = new Person();
        person.setHeader(new Header("1", "test"));
        mapper.write(person);
    }


Mapクラスにバインドする場合
  :ref:`固定長ファイルをMapクラスにバインドする場合のフォーマット指定方法 <data_bind-fixed_length_format-map>`
  と同様の手順でフォーマットを指定できる。

  以下にフォーマット指定の実装例を示す。

  ポイント
    * ``multiLayout`` メソッドを呼び出し、マルチレイアウト用のDataBindConfigを生成する。
    * ``recordIdentifier`` メソッドには、対象のデータがどのフォーマットに紐づくかを識別する
      :java:extdoc:`RecordIdentifier <nablarch.common.databind.fixedlength.MultiLayoutConfig.RecordIdentifier>` の実装クラスを指定する。

  .. code-block:: java

    final DataBindConfig config = FixedLengthDataBindConfigBuilder
            .newBuilder()
            .length(20)
            .charset(Charset.forName("MS932"))
            .lineSeparator("\r\n")
            .multiLayout()
            .record("header")
            .field("id", 1, 1, new DefaultConverter())
            .field("field", 2, 19, new Rpad.RpadConverter(' '))
            .record("data")
            .field("id", 1, 1, new DefaultConverter())
            .field("age", 2, 3, new Lpad.LpadConverter('0'))
            .field("name", 5, 16, new Rpad.RpadConverter(' '))
            .recordIdentifier(new RecordIdentifier() {
                @Override
                public RecordName identifyRecordName(byte[] record) {
                    return record[0] == 0x31 ? RecordType.HEADER : RecordType.DATA;
                }
            })
            .build();

  次に、指定されたフォーマットをもとに固定長データの読み込み・書き込みを行う実装例を示す。

  .. code-block:: java

    // 読み込む場合の実装例
    try (ObjectMapper<Map> mapper = ObjectMapperFactory.create(Map.class, inputStream, config)) {
        final Map<String, ?> map = mapper.read();
        if (RecordType.HEADER == map.get("recordName")) {
            final Map<String, ?> header = map.get("header");

            // 後続の処理は省略
        }
    }

    // 書き込む場合の実装例
    try (ObjectMapper<Map> mapper = ObjectMapperFactory.create(Map.class, outputStream, config)) {
        final Map<String, ?> header = new HashMap<>();
        header.put("id", "1");
        header.put("field", "test");

        final Map<String, ?> map = new HashMap<>();
        map.put("recordName", RecordType.HEADER);
        map.put("header", header);

        mapper.write(map);
    }

.. _data_bind-formatter:

出力するデータの表示形式をフォーマットする
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
データを出力する際に、 :ref:`format` を使用することで日付や数値などのデータの表示形式をフォーマットできる。

詳細は :ref:`format` を参照すること。

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
  クォートモードは以下のモードから選択できる。

  ================ ================================================================
  クォートモード名 フィールド囲み文字で囲む対象のフィールド
  ================ ================================================================
  NORMAL           フィールド囲み文字、列区切り文字、改行のいずれかを含むフィールド
  ALL              全てのフィールド
  ================ ================================================================

  .. tip::

    CSVファイルの読み込み時は、クォートモードは使用せずに自動的にフィールド囲み文字の有無を判定して読み込みを行う。
    
    
.. [#thread-unsafe]

  :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` の読み込み及び書き込みは、スレッドアンセーフであるため複数スレッドから同時に呼び出された場合の動作は保証しない。
  このため、 :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` のインスタンスを複数スレッドで共有するような場合には、呼び出し元にて同期処理を行うこと。
  

