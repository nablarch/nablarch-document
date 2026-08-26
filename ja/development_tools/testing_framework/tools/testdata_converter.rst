.. _testdata_converter:

テストデータ変換ツール
==================================================

.. contents:: 目次
  :depth: 3
  :local:

機能概要
--------------------------------------------------
テストデータ変換ツールは、テスティングフレームワークのテストデータを\ Excel\ 形式と\ YAML\ 形式の間で相互に変換する。\ Excel\ 形式で記述してきた既存のテストデータを、AIエージェントが扱いやすい\ YAML\ 形式へ移せる。

本ツールは、\ Excel\ 形式と\ YAML\ 形式のどちらか一方を正とするのではなく、両者の間に、テスティングフレームワークの仕様上の意味だけを持つ中間モデルを置く。\ Excel\ 形式と\ YAML\ 形式は、その意味をそれぞれの記法で表したものとして扱う。変換は、変換元の形式を中間モデルへ読み込み、その中間モデルを変換先の形式へ書き出すことで行う。

変換元と変換先には、\ Excel\ 形式・\ YAML\ 形式のどちらでも指定できる。変換元と変換先に同じ形式を指定した場合は、中間モデルへ読み込んで同じ形式へ書き戻す動作になり、既存のテストデータが中間モデルで正しく表現できるかの確認に使える。

.. tip::

  YAML\ 形式へ書き出す値は、値なしを除いてすべてダブルクォートで囲む。\ YAML\ の仕様では、囲まない\ ``123``\ は数値と解釈され、また前後の空白が脱落する。数値や空白を文字列として保つには、囲む必要がある。値なしだけは、文字列の\ ``"null"``\ と区別するためクォートなしの\ ``null``\ で表す。読み込み時は\ YAML\ のライブラリがダブルクォートを取り除くため、テストデータの値としてダブルクォートが残ることはない。

意味を変えずに往復できる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ある形式から中間モデルを経て同じ形式へ往復したとき、テスティングフレームワークの仕様上の意味は変わらない。中間モデルは両形式に共通であるため、\ Excel\ 形式から\ YAML\ 形式へ変換して再び\ Excel\ 形式へ戻した場合も、仕様上の意味は変わらない。中間モデルが保持する情報と、保持しない情報は次のとおりである。

.. list-table::
  :widths: 25,75
  :header-rows: 1

  * - 区分
    - 中間モデルでの扱い
  * - 構造
    - 解析済みの状態で保持する。レコードレイアウトの区切り、各行の役割、フィールド名と値の対応を持つ
  * - 値
    - 未変換のまま保持する。\ ``${systemTime}``\ などの特殊記法は解決せず、文字列として持つ
  * - 意図のある情報
    - 無損失で保持する。空欄のレコード種別が該当する
  * - 意味を持たない情報
    - 保持しない。コメント、マーカーカラム、データブロックの外側にある空行は除去する

YAML形式のテストデータの記述ミスを検出できる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
本ツールは、\ YAML\ 形式のテストデータを検証するクラス\ ``YamlTestDataValidator``\ を提供している。手で書いた\ YAML\ 形式のテストデータの記述ミスを、テストを実行する前に見つけるために使う。検査する内容は次の7つである。

* YAML\ として解析できること
* ``nablarch-testing-yaml``\ が提供するJSON Schema（\ :ref:`テストデータの書き方 <testdata_notation>`\ 参照）に適合すること
* レコード定義のフィールド数と、各データ行の要素数が一致すること
* 同一のレコード定義内でフィールド名が重複しないこと
* ディレクティブ名が既知のものであること
* ディレクティブ名がフレームワーク制御ヘッダに混入していないこと
* ファイルを読み込めること

.. tip::

  検証は変換の処理経路には組み込まれておらず、変換の実行時に自動では呼び出されない。検査したい場合は明示的に呼び出す。

前提事項
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
形式に固有で、テスティングフレームワークの仕様上の意味を持たない情報は中間モデルに保持されないため、往復しても再現されない。\ Excel\ 形式のセルの色・書式・結合セル、\ YAML\ 形式のコメントがこれにあたる。\ Excel\ 形式へ書き出す際は、元の色や書式ではなく、\ :ref:`Excel形式の出力を整形する <testdata_converter-xls_format>`\ の設定に従った整形が新たに付与される（設定しない場合はデフォルト値が適用される）。

テスティングフレームワーク独自の特殊記法（\ ``${systemTime}``\ ・\ ``${binaryFile:...}``\ など）は、本ツールでは解釈しない。記法のまま中間モデルへ運び、変換先の形式へそのまま書き出す。これらの記法は、テストの実行時にテスティングフレームワークが解釈する。

ただし\ Excel\ 形式のクォート記法（\ ``"値"``\ ・\ ``""``\ ）だけは例外で、読み込み時にクォートを外して中間モデルへ運ぶ。\ Excel\ 形式へ書き戻すときにクォートは付け直さないため、\ Excel\ 形式で\ ``"abc"``\ と書いたセルは往復後に\ ``abc``\ になる。

マーカーカラムは往復すると消える。テスティングフレームワークが読み込み対象から除外するため、中間モデルに入らない。マーカーカラムだけで構成したデータブロックは、\ Excel\ 形式から読み込むとデータ行も残らない。

カラム名を1つも持たないテーブルデータを\ Excel\ 形式へ書き出すとき、カラム名の行に置くマーカーカラムの名前には\ ``[EMPTY]``\ を使う。マーカーカラムを置くこと自体はテストデータの記法が定めるところで（\ :ref:`テーブルのデータを記述する <testdata_notation-table_data>`\ 参照）、名前を\ ``[EMPTY]``\ とするのが本ツールの決めである。

テーブルと\ ``LIST_MAP``\ ではカラム名の行、ファイルとメッセージではデータ行を含むすべての行について、行末の空セルは\ Excel\ 形式から読み込む時点で取り除かれるため、往復すると消える。データ行の空セルの扱いは形式によって異なるため、詳細は\ :ref:`テストデータの書き方 <testdata_notation>`\ を参照。

電文のレコード種別も、両形式で扱いが異なる。レコード種別に意味のある値を記載した\ Excel\ 形式のテストデータを\ YAML\ 形式へ変換すると、レコード種別の扱いが変わる。詳細は\ :ref:`テストデータの書き方 <testdata_notation>`\ を参照。

.. _testdata_converter-setup:

導入
--------------------------------------------------
本ツールは、Mavenプラグインとして実行する方法と、\ Java\ のコードから呼び出す方法の2通りで使用できる。既存のテストデータをまとめて変換する場合はMavenプラグインを、テストの実行時に変換する場合は\ Java\ のコードを使う。どちらを使うかによって、pom.xmlへの追加内容が異なる。

Mavenプラグインとして実行する場合は、pom.xmlにプラグインを追加する。

.. code-block:: xml

  <build>
    <plugins>
      <!-- テストデータ変換ツール -->
      <plugin>
        <groupId>com.nablarch.framework</groupId>
        <artifactId>nablarch-testing-converter</artifactId>
      </plugin>
    </plugins>
  </build>

Java\ のコードから呼び出す場合は、pom.xmlに\ ``nablarch-testing-converter``\ を依存関係として追加する。

.. code-block:: xml

  <!-- テストデータ変換ツール -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-testing-converter</artifactId>
    <scope>test</scope>
  </dependency>

使用方法
--------------------------------------------------
あらかじめ\ :ref:`導入 <testdata_converter-setup>`\ の手順を済ませておく。

.. TODO(NTF-MOD-01-2): 同名で拡張子違いのExcelブックが同居したときの変換対象の扱い。nablarch-testing-converter で XLS-28（同居を検出してエラーで止める）として要対応と確定・実装済み（5ab13d8、main 未マージ）。
   依頼書 .rn/20260724-ntf-yaml-support/ntf-mod-01-nablarch-testing-converter.md §3。
   XLS-28 の対応がマージされたら本 TODO を外す。本文の書き直しは不要。

Mavenプラグインで一括変換する場合も、\ Java\ のコードから変換を呼び出す場合も、入力ディレクトリ配下を再帰的に探索し、入力ディレクトリからの相対パスを保ったまま出力ディレクトリへ書き出す。変換元が\ Excel\ 形式の場合は、拡張子が\ ``.xls``\ のファイルと\ ``.xlsx``\ のファイルをどちらも対象とする。\ Excel\ 形式と\ YAML\ 形式では読み込み単位のまとめ方が異なるため、出力の構造は次のように読み替わる。

.. list-table::
  :widths: 22,39,39
  :header-rows: 1

  * - 変換の方向
    - 入力
    - 出力
  * - Excel\ 形式から\ YAML\ 形式へ
    - ブック\ ``foo/bar.xlsx``
    - ディレクトリ\ ``foo/bar/``\ と、その配下の\ ``<シート名>.yaml``
  * - YAML\ 形式から\ Excel\ 形式へ
    - ディレクトリ\ ``foo/bar/``
    - ブック\ ``foo/bar.xlsx``\ と、その中の読み込み単位ごとのシート

Mavenプラグインで一括変換する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``convert``\ ゴールを実行する。次の例は、\ Excel\ 形式のテストデータと同じディレクトリに\ YAML\ 形式のテストデータを書き出す。

.. code-block:: bash

  mvn com.nablarch.framework:nablarch-testing-converter:convert \
    -Dnablarch-testing-converter.from=xls \
    -Dnablarch-testing-converter.to=yaml \
    -Dnablarch-testing-converter.input=src/test/java/com/example/batch \
    -Dnablarch-testing-converter.output=src/test/java/com/example/batch

指定できるパラメータは次のとおりである。いずれも、コマンドラインの\ ``-D``\ オプションでも、pom.xmlの\ ``<configuration>``\ でも指定できる。pom.xmlに書く場合の要素名は、パラメータ名から\ ``nablarch-testing-converter.``\ を除いたものである。

.. list-table::
  :widths: 42,10,12,36
  :header-rows: 1

  * - パラメータ
    - 必須
    - デフォルト
    - 説明
  * - ``nablarch-testing-converter.from``
    - ○
    -
    - 変換元の形式。\ ``xls``\ または\ ``yaml``\ を指定する
  * - ``nablarch-testing-converter.to``
    - ○
    -
    - 変換先の形式。\ ``xls``\ または\ ``yaml``\ を指定する
  * - ``nablarch-testing-converter.input``
    - ○
    -
    - 入力ディレクトリ
  * - ``nablarch-testing-converter.output``
    - ○
    -
    - 出力ディレクトリ
  * - ``nablarch-testing-converter.overwrite``
    -
    - ``false``
    - 出力先に同名のファイルがある場合に上書きするかどうか。\ ``false``\ の場合、同名のファイルがあると変換を中断する

変換の対象を絞り込む設定は、pom.xmlの\ ``<configuration>``\ に記述する。いずれも複数指定でき、子要素に1件ずつ記述する。

.. list-table::
  :widths: 24,76
  :header-rows: 1

  * - 設定項目
    - 説明
  * - ``<includes>``
    - 変換対象とするglobパターン。子要素\ ``<include>``\ に記述する。入力ディレクトリからの相対パスに対して評価する。評価の対象は、変換元が\ Excel\ 形式のときはブックファイル、\ YAML\ 形式のときは\ YAML\ ファイルを含むディレクトリである。省略時は全件を対象とする
  * - ``<excludes>``
    - 変換対象から除外するglobパターン。子要素\ ``<exclude>``\ に記述する。評価の対象は\ ``<includes>``\ と同じである。省略時は除外しない
  * - ``<excludeSheets>``
    - 変換対象から除外するシート名。子要素\ ``<excludeSheet>``\ に記述する。テストデータの記法に従っていないシート（メモや作業用のシートなど）を除外するために使う。変換元が\ YAML\ 形式のときはシートの概念がないため無視される。省略時は除外しない

.. code-block:: xml

  <plugin>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-testing-converter</artifactId>
    <!-- <build><plugins> の内側に記述する -->
    <configuration>
      <excludeSheets>
        <excludeSheet>abnormalCase</excludeSheet>
      </excludeSheets>
    </configuration>
  </plugin>

Javaのコードから変換を呼び出す
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
変換を呼び出すクラスは\ ``nablarch.test.tool.converter.TestDataConverter``\ である。テストデータの形式変換を拡張する\ :java:extdoc:`nablarch.test.core.file.TestDataConverter <nablarch.test.core.file.TestDataConverter>`\ とは別のクラスである。変換元・変換先の形式と入出力ディレクトリだけを指定する場合は、4引数の\ ``convert``\ メソッドを呼び出す。戻り値は、変換したコンテナ（\ Excel\ 形式ではブック、\ YAML\ 形式ではディレクトリ。テストクラス1つ分のテストデータに相当する）の件数である。

.. code-block:: java

  int count = TestDataConverter.convert(
          DataFormat.XLS, DataFormat.YAML,
          Paths.get("src/test/java/com/example/batch"),
          Paths.get("src/test/java/com/example/batch"));

絞り込みや上書きの可否を指定する場合は、\ ``ConversionRequest``\ を組み立てて渡す。絞り込みの条件は、Mavenプラグインの\ ``<includes>``\ ・\ ``<excludes>``\ ・\ ``<excludeSheets>``\ に対応する\ ``include``\ ・\ ``exclude``\ ・\ ``excludeSheet``\ メソッドで1件ずつ追加する。まとめて渡す場合は\ ``includes``\ ・\ ``excludes``\ メソッドにリストを渡す。

.. code-block:: java

  ConversionRequest request = new ConversionRequest.Builder()
          .sourceFormat(DataFormat.XLS)
          .targetFormat(DataFormat.YAML)
          .inputPath(Paths.get("src/test/java/com/example/batch"))
          .outputPath(Paths.get("src/test/java/com/example/batch"))
          .overwrite(true)
          .include("**/*Test.xlsx")
          .excludeSheet("abnormalCase")
          .build();

  int count = TestDataConverter.convert(request);

.. tip::

  出力先に一時ディレクトリを渡せば、変換結果をバージョン管理下に置かずに済む。テストの実行のたびに\ Excel\ 形式のテストデータを\ YAML\ 形式へ変換して読ませる、といった使い方ができる。\ ``TestDataConverter``\ は出力先を引数で受け取るだけで一時か永続かを区別しないため、後始末はテストコード側で行う。

YAML形式のテストデータを検査する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``YamlTestDataValidator``\ のインスタンスを生成し、検査対象のディレクトリを指定して\ ``validate``\ メソッドを呼び出す。戻り値は、検出した問題を表す\ ``ValidationError``\ のリストである。問題がなければ空のリストを返す。

.. code-block:: java

  List<ValidationError> errors = new YamlTestDataValidator()
          .validate(Paths.get("src/test/java/com/example/batch/ProjectActionTest"));

.. important::

  指定したディレクトリの直下にある\ ``.yaml``\ ファイルだけを検査し、サブディレクトリはたどらない。テストクラス1つ分のテストデータが置かれたディレクトリを指定する。上位のディレクトリを指定すると、1件も検査しないまま空のリストが返る。

.. _testdata_converter-xls_format:

Excel形式の出力を整形する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
YAML\ 形式へ書き出す場合、本ツールは記法どおりに書くだけで、整形の設定を持たない。AIエージェントが読むことを前提としているためである。\ Excel\ 形式へ書き出す場合は、人が見て編集することを前提に、行の種別ごとの装飾やレイアウトを付けて読みやすく整える。この整形は設定で変更でき、設定しなかった項目にはデフォルト値が適用される。

設定できる項目とデフォルト値は次のとおりである。背景色は、Mavenプラグインでは\ Apache POI\ の\ ``IndexedColors``\ の列挙定数名で、\ Java\ のコードでは\ ``IndexedColors.AQUA.getIndex()``\ が返すインデックス値で指定する。

.. list-table::
  :widths: 26,18,20,36
  :header-rows: 1

  * - 設定項目
    - デフォルト
    - Java\ のメソッド
    - 説明
  * - ``testShotsHeaderColor``
    - ``LIME``
    - ``withTestShotsHeaderColor``
    - テストショット一覧（\ ``LIST_MAP``\ のうち識別子が\ ``testShots``\ のデータブロック）のヘッダ行の背景色
  * - ``setupHeaderColor``
    - ``PALE_BLUE``
    - ``withSetupHeaderColor``
    - ``SETUP_TABLE``\ ・\ ``SETUP_FIXED``\ ・\ ``SETUP_VARIABLE``\ のヘッダ行の背景色
  * - ``expectedHeaderColor``
    - ``LIGHT_YELLOW``
    - ``withExpectedHeaderColor``
    - ``EXPECTED_``\ で始まるデータブロックと\ ``RESPONSE_``\ で始まるデータブロックのヘッダ行の背景色
  * - ``otherHeaderColor``
    - ``LAVENDER``
    - ``withOtherHeaderColor``
    - ``MESSAGE``\ ・\ ``LIST_MAP``\ （識別子が\ ``testShots``\ 以外）のヘッダ行の背景色
  * - ``markerColumnColor``
    - ``LIGHT_ORANGE``
    - ``withMarkerColumnColor``
    - カラム名が0件のデータブロックに合成されるマーカーカラム（\ ``[EMPTY]``\ ）の背景色。入力に元からあったマーカーカラムは中間モデルに入らないため、着色の対象にならない
  * - ``autoColumnWidth``
    - ``true``
    - ``withAutoColumnWidth``
    - 各列の値の最大文字数に合わせて列幅を自動調整するかどうか
  * - ``maxColumnWidthChars``
    - ``20``
    - ``withMaxColumnWidthChars``
    - 列幅を自動調整する場合の上限文字数。1以上を指定する
  * - ``drawBlockBorder``
    - ``true``
    - ``withBlockBorder``
    - データブロックの外枠に細線の罫線を引くかどうか
  * - ``drawCellBorder``
    - ``true``
    - ``withCellBorder``
    - データブロック内のセル間に罫線を引くかどうか
  * - ``displayGridlines``
    - ``false``
    - ``withDisplayGridlines``
    - シートのグリッド線を表示するかどうか
  * - ``blankRowsBetweenBlocks``
    - ``1``
    - ``withBlankRowsBetweenBlocks``
    - データブロックの間に挿入する空行数。0以上を指定する

Mavenプラグインでは、pom.xmlの\ ``<configuration>``\ に\ ``<xlsOutput>``\ を追加し、設定項目名を要素名として記述する。

.. code-block:: xml

  <plugin>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-testing-converter</artifactId>
    <!-- <build><plugins> の内側に記述する -->
    <configuration>
      <xlsOutput>
        <setupHeaderColor>AQUA</setupHeaderColor>
        <drawCellBorder>false</drawCellBorder>
        <blankRowsBetweenBlocks>2</blankRowsBetweenBlocks>
      </xlsOutput>
    </configuration>
  </plugin>

Java\ のコードでは、\ ``ExcelFormatConfig.defaults()``\ を基点に、上表の「\ Java\ のメソッド」列のメソッドで値を差し替え、\ ``ConversionRequest``\ に渡す。

.. code-block:: java

  ExcelFormatConfig config = ExcelFormatConfig.defaults()
          .withSetupHeaderColor(IndexedColors.AQUA.getIndex())
          .withCellBorder(false)
          .withBlankRowsBetweenBlocks(2);

  ConversionRequest request = new ConversionRequest.Builder()
          .sourceFormat(DataFormat.YAML)
          .targetFormat(DataFormat.XLS)
          .inputPath(Paths.get("src/test/java/com/example/batch"))
          .outputPath(Paths.get("src/test/java/com/example/batch"))
          .overwrite(true)
          .excelFormatConfig(config)
          .build();
