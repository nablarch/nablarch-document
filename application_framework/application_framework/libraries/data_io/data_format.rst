.. _data_format:

汎用データフォーマット
==================================================

.. contents:: 目次
  :depth: 3
  :local:

システムで扱う多様なデータ形式に対応した汎用の入出力ライブラリ機能を提供する。

本機能の大まかな構成は以下のとおり。

.. image:: ../images/data_format/structure.png


機能概要
--------------------------------------------------

.. _data_format-support_type:

標準でサポートするフォーマットが豊富
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
標準では、以下の形式のフォーマットに対応している。

固定長と可変長のデータ形式では、レコード毎にレイアウトの異なるマルチレイアウトデータにも対応している。
(XMLとJSONには、レコードという概念が存在しない。)

* 固定長
* 可変長(csvやtsvなど)
* JSON
* XML

.. important::

  本機能には、以下のデメリットがある。

  * 複雑な :ref:`フォーマット定義ファイル <data_format-format_definition_file>` を作成する必要がある。
  * 入出力が :java:extdoc:`Map <java.util.Map>` に限定されており、実装誤りを起こしやすい。

    * フィールド名を文字列で指定する必要があり、IDEの補完も使えないなど、実装時にミスを起こしやすい。
    * アプリケーション側で、Mapから取り出した値をダウンキャストする必要がある。(誤ると、実行時に例外が送出される。)

  * データとJavaオブジェクトのマッピングに :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` を使用していないため、他の機能とはマッピング方法が異なる。
  * 出力対象の :java:extdoc:`Map <java.util.Map>` の扱い方がフォーマットによって異なる。このため、同じデータを複数のフォーマットに対応させる機能を使用した場合に、フォーマットによっては例外が発生するなど正常に動作しない場合がある。
    
    例えば、下のケースで問題がある。
    
    XMLとJSONで必須項目にnullを指定した場合：
      * XML：値を空文字として出力
      * JSON：必須の例外を送出
  
  * 出力対象のデータによってはJSONの仕様を満たせない場合がある。
  
    例えば、 :java:extdoc:`数値型 <nablarch.core.dataformat.convertor.datatype.JsonNumber>` や :java:extdoc:`真偽値型 <nablarch.core.dataformat.convertor.datatype.JsonBoolean>` を使用し、出力対象のデータ型がこれらの型に対応していない場合に不正なJSONが出力される。
    
    例：数値型を指定し、出力対象が「data」などの文字列の場合、{"number":data}のような不正なJSONが出力される。
  
  * データ形式によって使用できる :java:extdoc:`データタイプ <nablarch.core.dataformat.convertor.datatype.DataType>` の実装クラスが異なるため拡張しづらい。また、この設定の誤りは実行時まで検知できない。
  
  このため原則本機能はやむを得ない場合を除き非推奨とする。
  なお、 :ref:`messaging` は、内部で本機能を利用しているため、代替機能を使用することはできない。

  本機能の代替機能
    :固定長: 固定長の代替機能は存在しない。本機能を使用すること。
    :可変長: :ref:`data_bind` を使用すること。
    :XML: :java:extdoc:`JAXB <javax.xml.bind>` を推奨する。
    :JSON: OSSの使用を推奨する。例えば、 `Jackson(外部サイト、英語) <https://github.com/FasterXML/jackson>`_ が広く使われている。


様々な文字セットや文字種、データ形式に対応
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
文字列や10進数数値だけでなく、ホストでよく扱われるパック数値やゾーン10進数形式などに対応している。
また、UTF-8やShift_JISだけではなくEBCDICなどの文字セットにも対応している。

.. tip::
  
  文字セットについては、実行環境のJVMでサポートされているものが使用できる。

.. _data_format-value_convertor:

パディングやトリミングなどの変換処理に対応
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
固定長ファイルで多く利用されるスペースやゼロ(0)パディング及びトリミングに対応している。
このため、アプリケーション側でパディング処理やトリミング処理を行わなくて良い。

パディングやトリミングの詳細は、 :ref:`data_format-field_convertor_list` を参照。

モジュール一覧
---------------------------------------------------------------------
* :ref:`アップロードヘルパー <data_format-upload_helper>` を使用する場合は、 ``nablarch-fw-web-extension`` を追加する。
* :ref:`ファイルダウンロード <data_format-file_download>` を使用する場合は、 ``nablarch-fw-web-extension`` を追加する。

.. code-block:: xml

  <!-- 汎用データフォーマット -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-dataformat</artifactId>
  </dependency>

  <!--
  アップロードヘルパーを使用する場合、ダウンロードを使用する場合は以下を追加する
   -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web-extension</artifactId>
  </dependency>



使用方法
--------------------------------------------------

.. _data_format-format_definition_file:

入出力データのフォーマットを定義する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
入出力対象データのフォーマット定義は、フォーマット定義ファイルに行う。

フォーマット定義ファイルは、以下のようなテキストファイル形式で作成する。
詳細な仕様は、 :doc:`data_format/format_definition` を参照。

.. code-block:: bash

  file-type:        "Variable" # 可変長
  text-encoding:    "MS932"    # 文字列型フィールドの文字エンコーディング
  record-separator: "\r\n"     # 改行コード(crlf)
  field-separator:  ","        # csv

  # レコード識別フィールドの定義
  [Classifier]
  1 dataKbn X     # 1つめのフィールド
  3 type    X     # 3つめのフィールド

  [parentData]
  dataKbn = "1"
  type    = "01"
  1 dataKbn X
  2 ?filler X
  3 type    X
  4 data    X

  [childData]
  dataKbn = "1"
  type    = "02"
  1 dataKbn X
  2 ?filler X
  3 type    X
  4 data    X
  

.. toctree::
  :hidden:

  data_format/format_definition


ファイルにデータを出力する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
データレコードの内容をファイルに出力する方法について説明する。

ファイルへのデータ出力は、 :java:extdoc:`FileRecordWriterHolder <nablarch.common.io.FileRecordWriterHolder>` を使用することで実現できる。

以下に実装例を示す。

ポイント
  * ファイルに書き込むデータは :java:extdoc:`Map <java.util.Map>` として準備する。
  * :java:extdoc:`Map <java.util.Map>` のキー値は、 :ref:`data_format-format_definition_file` で定義したフィールド名を設定する。(大文字、小文字は区別しない)
  * :java:extdoc:`FileRecordWriterHolder <nablarch.common.io.FileRecordWriterHolder>` の `open` メソッドを呼び出して、ファイルリソースを書き込み可能状態にする。
  * :java:extdoc:`FileRecordWriterHolder <nablarch.common.io.FileRecordWriterHolder>` の `write` メソッドを呼び出して、データをファイルに書き込む。

.. code-block:: java

  // 書き込み対象のデータ
  Map<String, Object> user = new HashMap<>();
  user.put("name", "名前");
  user.put("age", 20);

  // 書き込み対象のファイルを開く
  FileRecordWriterHolder.open("users.csv", "user_csv_format");

  // データを書き込む
  FileRecordWriterHolder.write(user, "user.csv");

.. tip::

  :java:extdoc:`FileRecordWriterHolder <nablarch.common.io.FileRecordWriterHolder>` を使用するためには、
  :ref:`フォーマット定義ファイル <data_format-format_definition_file>` の配置ディレクトリや出力先ディレクトリを
  :ref:`file_path_management` に設定する必要がある。

  必要となるディレクトリの設定値については、 :java:extdoc:`FileRecordWriterHolder <nablarch.common.io.FileRecordWriterHolder>` を参照。

.. important::

  :java:extdoc:`FileRecordWriterHolder <nablarch.common.io.FileRecordWriterHolder>` で開いたファイルリソースは、
  :ref:`file_record_writer_dispose_handler` にて自動的に開放される。
  このため、 :java:extdoc:`FileRecordWriterHolder <nablarch.common.io.FileRecordWriterHolder>` を使用する場合には、
  必ず :ref:`file_record_writer_dispose_handler` をハンドラキュー上に設定すること。

.. _data_format-file_download:
  
ファイルダウンロードで使用する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
データレコードの内容をファイルダウンロード形式でクライアントに応答する方法について解説する。

ファイルダウンロード形式のレスポンスは、 :java:extdoc:`DataRecordResponse <nablarch.common.web.download.DataRecordResponse>` を使用することで実現できる。

以下に実装例を示す。

ポイント
  * :java:extdoc:`DataRecordResponse <nablarch.common.web.download.DataRecordResponse>` 生成時に、
    フォーマット定義ファイルが格納された論理パス名と、フォーマット定義ファイル名を指定する。
  * :java:extdoc:`DataRecordResponse#write <nablarch.common.web.download.DataRecordResponse.write(java.util.Map)>` を使って、
    データを出力する。(複数のレコードをダウンロードする場合には、繰り返し出力する)
  * `Content-Type` 及び `Content-Disposition` を設定する。
  * 業務アクションから :java:extdoc:`DataRecordResponse <nablarch.common.web.download.DataRecordResponse>` を返却する。

.. code-block:: java

  public HttpResponse download(HttpRequest request, ExecutionContext context) {

    // 業務処理

    // ダウンロードデータを格納したMapの作成する。
    Map<String, Object> user = new hashMap<>()
    user.put("name", "なまえ");
    user.put("age", 30);

    // フォーマット定義ファイルが格納された論理パス名と
    // フォーマット定義ファイル名を指定してDataRecordResponseを生成する。
    DataRecordResponse response = new DataRecordResponse("format", "users_csv");

    // ダウンロードデータを出力する。
    response.write(user);

    // Content-Typeヘッダ、Content-Dispositionヘッダを設定する
    response.setContentType("text/csv; charset=Shift_JIS");
    response.setContentDisposition("メッセージ一覧.csv");

    return response;
  }
  

.. tip::
  フォーマット定義ファイルの格納パスは、 :ref:`file_path_management` に設定する必要がある。

.. _data_format-load_upload_file:

アップロードしたファイルを読み込む
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
アップロードしたファイルを読み込む方法について解説する。

この機能では、以下の2種類の方法でアップロードしたファイルを読み込むことが出来る。
:ref:`アップロードヘルパーを使った読み込み <data_format-upload_helper>` に記載のある通り、
:ref:`汎用データフォーマット(本機能)のみを使った読み込み <data_format-native_upload_file_load>` の使用を推奨する。

* :ref:`汎用データフォーマット(本機能)のみを使った読み込み <data_format-native_upload_file_load>`
* :ref:`アップロードヘルパーを使った読み込み <data_format-upload_helper>`

.. _data_format-native_upload_file_load:

汎用データフォーマット(本機能)のみを使ったアップロードファイルの読み込み
  後述のアップロードヘルパーを使わずに本機能のAPIを使用したアップロードファイルのロード処理について解説する。

  以下に実装例を示す。

  ポイント
    * :java:extdoc:`HttpRequest#getPart <nablarch.fw.web.HttpRequest.getPart(java.lang.String)>` を呼び出してアップロードされたファイルを取得する。
    * :java:extdoc:`HttpRequest#getPart <nablarch.fw.web.HttpRequest.getPart(java.lang.String)>` の引数には、パラメータ名を指定する。
    * :java:extdoc:`FilePathSetting <nablarch.core.util.FilePathSetting>` からフォーマット定義ファイルの :java:extdoc:`File <java.io.File>` オブジェクトを取得する。
    * フォーマット定義ファイルを指定し、 :java:extdoc:`FormatterFactory <nablarch.core.dataformat.FormatterFactory>`
      から :java:extdoc:`DataRecordFormatter <nablarch.core.dataformat.DataRecordFormatter>` を生成する。
    * :java:extdoc:`DataRecordFormatter <nablarch.core.dataformat.DataRecordFormatter>` にアップロードファイルを読み込むための :java:extdoc:`InputStream <java.io.InputStream>` を設定する。
      設定する :java:extdoc:`InputStream <java.io.InputStream>` の実装クラスは、 :java:extdoc:`mark <java.io.InputStream.mark(int)>`/:java:extdoc:`reset <java.io.InputStream.reset()>` がサポートされている必要がある。
    * :java:extdoc:`DataRecordFormatter <nablarch.core.dataformat.DataRecordFormatter>` のAPIを呼び出し、アップロードファイルのレコードを読み込む。

  .. code-block:: java

    public HttpResponse upload(HttpRequest req, ExecutionContext ctx) {

      // アップロードしたファイルの情報を取得
      final List<PartInfo> partInfoList = request.getPart("users");

      // フォーマット定義ファイルのFileオブジェクトを取得する
      final File format = FilePathSetting.getInstance()
                                         .getFile("format", "users-layout");

      // フォーマット定義ファイルを取得し、アップロードファイルを読み込むためのフォーマッターを生成する。
      try (final DataRecordFormatter formatter = FormatterFactory.getInstance()
                                                                 .createFormatter(format)) {

        // アップロードファイルを読み込むためのInputStreamをフォーマッターに設定し初期化する。
        // mark/resetがサポートされている必要が有るため、BufferedInputStreamでラップする。
        formatter.setInputStream(new BufferedInputStream(partInfoList.get(0).getInputStream()))
                 .initialize();

        // レコードが終わるまで繰り返し処理を行う。
        while (formatter.hasNext()) {
          // レコードを読み込む。
          final DataRecord record = formatter.readRecord();

          // レコードに対する処理を行う
          final Users users = BeanUtil.createAndCopy(Users.class, record);

          // 以下省略
        }
      } catch (IOException e) {
        throw new RuntimeException(e);
      }
    }

.. _data_format-upload_helper:

アップロードヘルパーを使用したアップロードファイルの読み込み
  アップロードヘルパー( :java:extdoc:`UploadHelper <nablarch.fw.web.upload.util.UploadHelper>` )を使用すると、
  ファイルの読み込み、バリデーション、データベースへの保存を簡易的に実行出来る。

  しかし、この機能では以下の制限(デメリット)があるため、 :ref:`汎用データフォーマット(本機能)のみを使ったアップロードファイルの読み込み <data_format-native_upload_file_load>`
  を使用することを推奨する。

  * 入力値のチェックは :ref:`nablarch_validation` に限定される。(推奨される :ref:`bean_validation` が使用できない。)
  * 拡張可能ではあるが、難易度が高く容易に要件を満たす実装ができない。

  以下にシングルレイアウトのアップロードファイルに対して、入力チェックを行いデータベースに登録する例を示す。

  ポイント
    * :java:extdoc:`HttpRequest#getPart <nablarch.fw.web.HttpRequest.getPart(java.lang.String)>` を呼び出してアップロードされたファイルを取得する。
    * :java:extdoc:`HttpRequest#getPart <nablarch.fw.web.HttpRequest.getPart(java.lang.String)>` の引数には、パラメータ名を指定する。
    * 取得したアップロードファイルを元に :java:extdoc:`UploadHelper <nablarch.fw.web.upload.util.UploadHelper>` を生成する。
    * :java:extdoc:`UploadHelper#applyFormat <nablarch.fw.web.upload.util.UploadHelper.applyFormat(java.lang.String)>` を使って、フォーマット定義ファイルを設定する。

    * :java:extdoc:`setUpMessageIdOnError <nablarch.fw.web.upload.util.BulkValidator.setUpMessageIdOnError(java.lang.String, java.lang.String, java.lang.String)>` を使って、バリデーションエラー用のメッセージIDを設定する。
    * :java:extdoc:`validateWith <nablarch.fw.web.upload.util.BulkValidator.ErrorHandlingBulkValidator.validateWith(java.lang.Class,%20java.lang.String)>` を使って、バリデーションを実行するJava Beansクラスとバリデーションメソッドを設定する。
    * :java:extdoc:`importWith <nablarch.fw.web.upload.util.BulkValidationResult.importWith(nablarch.core.db.support.DbAccessSupport, java.lang.String)>` を使って、バリデーション実行後のJava Beansオブジェクトの内容をデータベースに登録する。

  .. code-block:: java

    public HttpResponse upload(HttpRequest req, ExecutionContext ctx) {

      PartInfo partInfo = req.getPart("fileToSave").get(0);

      // 全件一括登録
      UploadHelper helper = new UploadHelper(partInfo);
      int cnt = helper
          .applyFormat("N11AC002")                     // フォーマットを適用する
          .setUpMessageIdOnError("format.error",       // 形式エラー時のメッセージIDを指定する
                                 "validation.error",   // バリデーションエラー時のメッセージIDを指定する
                                 "file.empty.error")   // ファイルが空の場合のメッセージIDを指定する
          .validateWith(UserInfoTempEntity.class,      // バリデーションメソッドを指定する
                        "validateRegister")
          .importWith(this, "INSERT_SQL");             // INSERT文のSQLIDを指定する

    }

  .. tip::

    :java:extdoc:`nablarch.fw.web.upload.util` パッケージ内のクラスのドキュメントを合わせて参照すること。

.. _data_format-structured_data:

JSONやXMLの階層構造のデータを読み書きする
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
JSONやXMLの階層構造データを読み書きする際のMapの構造について解説する。

JSONやXMLのような階層構造のデータを読み込んだ場合、Mapのキー値は各階層の要素名をドット( ``.`` )で囲んだ値となる。

以下に例を示す。

フォーマット定義ファイル
  JSONの場合には、 `file-type` を ``JSON`` に読み替えること。
  階層構造を表すフォーマット定義ファイルの定義方法は、 :ref:`階層構造の定義 <data_format-nest_object>` を参照。

  .. code-block:: bash

    file-type:        "XML"
    text-encoding:    "UTF-8"

    [users]              # ルート要素
    1 user    [0..*] OB

    [user]               # ネストした要素
    1 name    [0..1] N   # 最下層の要素
    2 age     [0..1] X9
    3 address [0..1] N

  .. important::

    親要素が任意であり、親要素が存在する場合のみ子要素を必須、といった設定には対応していない。
    そのため、階層構造のデータをフォーマット定義ファイルに定義する際は、全て任意項目として定義することを推奨する。

Mapの構造
  上記フォーマット定義ファイルを使って、XML及びJSONにデータを出力するMapの構造は以下のようになる。

  ポイント
    * 階層構造の場合、「親要素名 + "." + 子要素名」形式でMapに値を設定する。
    * 階層構造が深い場合は、更に ``.`` で要素名が連結される。
    * 最上位の要素名は、キーに含める必要はない
    * 配列要素の場合添字(0から開始)を設定する。

  .. code-block:: java

    Map<String, Object> data = new HashMap<String, Object>();

    // user配列要素の1要素目
    data.put("user[0].name", "なまえ1");
    data.put("user[0].address", "住所1");
    data.put("user[0].age", 30);

    // user配列要素の2要素目
    data.put("user[1].name", "なまえ2");
    data.put("user[1].address", "住所2");
    data.put("user[1].age", 31);

XMLおよびJSONの構造
  上記フォーマット定義ファイルに対応したXML及びJSONの構造は以下のとおり。

  XML
    .. code-block:: xml

      <?xml version="1.0" encoding="UTF-8"?>
      <users>
        <user>
          <name>なまえ1</name>
          <address>住所1</address>
          <age>30</age>
        </user>
        <user>
          <name>なまえ2</name>
          <address>住所2</address>
          <age>31</age>
        </user>
      </users>    

  JSON
    .. code-block:: json

      {
        "user": [
          {
            "name": "なまえ1",
            "address": "住所1",
            "age": 30
          },
          {
            "name": "ななえ2",
            "address": "住所2",
            "age": 31
          }
        ]
      }

XMLで名前空間を使う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
接続先システムとの接続要件で、名前空間を使用しなければならない場合がある。
この場合は、フォーマット定義ファイルにて名前空間を定義することで対応できる。


以下に例を示す。

ポイント
  * 名前空間は、名前空間を使用する要素に「"?\@xmlns:" + 名前空間」として定義する。
    タイプは、 ``X`` とし、フィールドコンバータ部にURIを指定する。
  * 名前空間は、「名前空間 + ":" + 要素名」形式で表す。
  * 入出力対象データのMapのキー値は、「名前空間＋要素名(先頭大文字)」となる。


フォーマット定義ファイル
  .. code-block:: bash

    file-type:        "XML"
    text-encoding:    "UTF-8"

    [testns:data]
    # 名前空間の定義
    1 ?@xmlns:testns X "http://testns.hoge.jp/apply"
    2 testns:key1 X

XMLデータ
  上記フォーマット定義ファイルに対応したXMLは以下のとおり。

  .. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <testns:data xmlns:testns="http://testns.hoge.jp/apply">
      <testns:key1>value1</testns:key1>
    </testns:data>

Mapデータ
  入出力対象のMapの構造は以下のとおり。

  .. code-block:: java

    Map<String, Object> data = new HashMap<String, Object>();
    data.put("testnsKey1", "value1");

XMLで属性を持つ要素にコンテンツを定義する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
XMLで属性を持つ要素にコンテンツを定義したい場合は、
フォーマット定義ファイルにコンテンツを表すフィールドを定義する。

設定例を以下に示す。

ポイント
  * コンテンツを表すフィールド名には ``body`` を指定する。
    コンテンツを表すフィールド名をデフォルトから変更したい場合は、 :ref:`data_format-xml_content_name_change` を参照。

フォーマット定義ファイル
  .. code-block:: bash

    file-type:        "XML"
    text-encoding:    "UTF-8"

    [parent]
    1 child   OB

    [child]
    1 @attr   X
    2 body    X

XMLデータ
  上記フォーマット定義ファイルに対応したXMLは以下のとおり。

  .. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <parent>
      <child attr="value1">value2</child>
    </parent>

Mapデータ
  入出力対象のMapの構造は以下のとおり。

  .. code-block:: java

    Map<String, Object> data = new HashMap<String, Object>();
    data.put("child.attr", "value1");
    data.put("child.body", "value2");

.. _data_format-replacement:

文字の置き換え(寄せ字)を行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
寄せ字機能を使うことで、外部からデータを読み込む際に、システムで利用可能な文字に置き換えることが出来る。

以下に使用方法を示す。

置き換えルールを定義したプロパティを作成する
  プロパティファイルには、「置き換え前の文字=置き換え後の文字」形式で、置き換えルールを定義する。

  置き換え前、置き換え後の文字に定義できる値は、ともに1文字のみである。
  また、サロゲートペアには対応していない。

  コメントなどの記述ルールは、 :java:extdoc:`java.util.Properties` を参照。

  .. code-block:: properties

    髙=高
    﨑=崎
    唖=■

  .. tip::
    接続先ごとに置き換えルールを定義する場合には、複数のコンフィグファイルを作成する。

置き換えルールの設定をコンポーネント設定ファイルに追加する
  ポイント
    * :java:extdoc:`CharacterReplacementManager <nablarch.core.dataformat.CharacterReplacementManager>` をコンポーネント名 ``characterReplacementManager`` で設定する。
    * :java:extdoc:`configList <nablarch.core.dataformat.CharacterReplacementManager.setConfigList(java.util.List)>` プロパティにリスト形式で :java:extdoc:`CharacterReplacementConfig <nablarch.core.dataformat.CharacterReplacementConfig>` を設定する。
    * 複数のプロパティファイルを定義する場合は、 :java:extdoc:`typeName <nablarch.core.dataformat.CharacterReplacementConfig.setTypeName(java.lang.String)>` プロパティに異なる名前を設定する。

  .. code-block:: xml

    <component name="characterReplacementManager"
        class="nablarch.core.dataformat.CharacterReplacementManager">
      <property name="configList">
        <list>
          <!-- Aシステムとの寄せ字ルール -->
          <component class="nablarch.core.dataformat.CharacterReplacementConfig">
            <property name="typeName" value="a_system"/>
            <property name="filePath" value="classpath:a-system.properties"/>
            <property name="encoding" value="UTF-8"/>
          </component>
          <!-- Bシステムとの寄せ字ルール -->
          <component class="nablarch.core.dataformat.CharacterReplacementConfig">
            <property name="typeName" value="b_system"/>
            <property name="filePath" value="classpath:b-system.properties"/>
            <property name="encoding" value="UTF-8"/>
          </component>
        </list>
      </property>
    </component>

フォーマット定義ファイルにどの置き換えルールを使用するかを定義する
  入出力時に文字の置き換えを行う場合は、 :ref:`replacement <data_format-replacement_convertor>` を使用する。

  `replacement` の引数には、上記で設定した置き換えルールの `typeName` を設定する。

  .. code-block:: bash
    
    # Aシステムとの置き換えルールを適用
    1 name N(100) replacement("a_system")

    # Bシステムとの置き換えルールを適用
    1 name N(100) replacement("b_system")


拡張例
--------------------------------------------------

.. _data_format-field_type_add:

フィールドタイプを追加する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`Nablarchが提供する標準データタイプ <data_format-field_type_list>` では要件を満たせない場合がある。
例えば、文字列タイプのパディング文字がバイナリの場合などが該当する。

このような場合は、プロジェクト固有のフィールドタイプを定義することで対応する。

以下に手順を示す。

#. フィールドタイプを処理するための :java:extdoc:`DataType<nablarch.core.dataformat.convertor.datatype.DataType>` 実装クラスを作成する。
#. 設定ファイルにフィールドタイプ定義を行う。

詳細な手順は以下のとおり。

フィールドタイプに対応したデータタイプ実装の追加
  :java:extdoc:`DataType<nablarch.core.dataformat.convertor.datatype.DataType>` を実装したクラスを作成する。

  .. tip::
    
    標準のフィールドタイプ実装は、 :java:extdoc:`nablarch.core.dataformat.convertor.datatype` パッケージ配下に配置されている。
    実装を追加する際には、これらのクラスを参考にすると良い。

設定ファイルへの追加
  追加したフィールドタイプを有効にするために、設定ファイルにフィールドタイプの設定を追加する。

  フィールドタイプは、各フォーマットタイプに応じた設定クラスの `convertorTable` プロパティに対して行う。
  以下にフォーマットタイプ毎の設定クララスを示す。

  .. list-table::
    :class: white-space-normal
    :header-rows: 1
    :widths: 33 33 34
    
    * - データタイプ
      - クラス名(コンポーネント名)
      - デフォルトタイプ定義クラス

    * - Fixed(固定長)
      - :java:extdoc:`FixedLengthConvertorSetting <nablarch.core.dataformat.convertor.FixedLengthConvertorSetting>`
        (fixedLengthConvertorSetting)
      - :java:extdoc:`FixedLengthConvertorFactory <nablarch.core.dataformat.convertor.FixedLengthConvertorFactory>`
    * - Variable(可変長)
      - :java:extdoc:`VariableLengthConvertorSetting <nablarch.core.dataformat.convertor.VariableLengthConvertorSetting>`
        (variableLengthConvertorSetting)
      - :java:extdoc:`VariableLengthConvertorFactory <nablarch.core.dataformat.convertor.VariableLengthConvertorFactory>`
    * - JSON
      - :java:extdoc:`JsonDataConvertorSetting <nablarch.core.dataformat.convertor.JsonDataConvertorSetting>`
        (jsonDataConvertorSetting)
      - :java:extdoc:`JsonDataConvertorFactory <nablarch.core.dataformat.convertor.JsonDataConvertorFactory>`
    * - XML
      - :java:extdoc:`XmlDataConvertorSetting <nablarch.core.dataformat.convertor.XmlDataConvertorSetting>`
        (xmlDataConvertorSetting)
      - :java:extdoc:`XmlDataConvertorFactory <nablarch.core.dataformat.convertor.XmlDataConvertorFactory>`

  以下にFixed(固定長)の場合の例を示す。

  コンポーネント名は、上記表のコンポーネント名を設定する。固定長の場合は、 `fixedLengthConvertorSetting` となる。

  追加したフィールドタイプを設定する際には、デフォルトのフィールドタイプ及びフィールドコンバータの設定を合わせて設定する。
  デフォルトのフィールドタイプ及びフィールドコンバータの設定は、上記表のデフォルトタイプ定義クラスの実装から転記すること。

  .. code-block:: xml

    <component name="fixedLengthConvertorSetting"
        class="nablarch.core.dataformat.convertor.FixedLengthConvertorSetting">

      <property name="convertorTable">
        <map>
          <!-- デフォルトの設定ここから -->
          <entry key="X" value="nablarch.core.dataformat.convertor.datatype.SingleByteCharacterString" />
          <entry key="N" value="nablarch.core.dataformat.convertor.datatype.DoubleByteCharacterString" />
          <entry key="XN" value="nablarch.core.dataformat.convertor.datatype.ByteStreamDataString" />
          <entry key="Z" value="nablarch.core.dataformat.convertor.datatype.ZonedDecimal" />
          <entry key="SZ" value="nablarch.core.dataformat.convertor.datatype.SignedZonedDecimal" />
          <entry key="P" value="nablarch.core.dataformat.convertor.datatype.PackedDecimal" />
          <entry key="SP" value="nablarch.core.dataformat.convertor.datatype.SignedPackedDecimal" />
          <entry key="X9" value="nablarch.core.dataformat.convertor.datatype.NumberStringDecimal" />
          <entry key="SX9" value="nablarch.core.dataformat.convertor.datatype.SignedNumberStringDecimal" />
          <entry key="B" value="nablarch.core.dataformat.convertor.datatype.Bytes" />

          <entry key="pad" value="nablarch.core.dataformat.convertor.value.Padding" />
          <entry key="encoding" value="nablarch.core.dataformat.convertor.value.UseEncoding" />
          <entry key="_LITERAL_" value="nablarch.core.dataformat.convertor.value.DefaultValue" />
          <entry key="number" value="nablarch.core.dataformat.convertor.value.NumberString" />
          <entry key="signed_number" value="nablarch.core.dataformat.convertor.value.SignedNumberString" />
          <entry key="replacement" value="nablarch.core.dataformat.convertor.value.CharacterReplacer" />

          <!-- 追加したフィールドタイプの定義 -->
          <entry key="SAMPLE_TYPE" value="sample.SampleType" />
        </map>
      </property>
    </component>

.. _data_format-xml_content_name_change:

XMLで属性を持つ要素のコンテンツ名を変更する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
属性を持つ要素のコンテンツ名を変更するには、
以下のクラスをコンポーネント設定ファイルに設定し、``contentName`` プロパティに変更後のコンテンツ名をそれぞれ設定する。

* :java:extdoc:`XmlDataParser<nablarch.core.dataformat.XmlDataParser>`
* :java:extdoc:`XmlDataBuilder<nablarch.core.dataformat.XmlDataBuilder>`

コンポーネント設定ファイルの設定例を以下に示す。

ポイント
 * :java:extdoc:`XmlDataParser<nablarch.core.dataformat.XmlDataParser>` のコンポーネント名は ``XmlDataParser`` とすること
 * :java:extdoc:`XmlDataBuilder<nablarch.core.dataformat.XmlDataBuilder>` のコンポーネント名は ``XmlDataBuilder`` とすること

.. code-block:: xml

  <component name="XmlDataParser" class="nablarch.core.dataformat.XmlDataParser">
    <property name="contentName" value="change" />
  </component>

  <component name="XmlDataBuilder" class="nablarch.core.dataformat.XmlDataBuilder">
    <property name="contentName" value="change" />
  </component>