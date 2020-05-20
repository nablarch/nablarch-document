.. _multicol_mode:

======================================
マルチレイアウト用CSSフレームワーク
======================================

------------
概要
------------
マルチレイアウト用CSSフレームワークは、\ :doc:`css_framework`\ の\
ワイドモードをベースとしたスタイルシート群で以下のことが実現可能である。

* UI部品ウィジェットを複数個並べて配置することができる(画面ごと自由にレイアウトできる)
* UI部品ウィジェットの出力幅を指定できる

**マルチレイアウトモードを使用した場合の画面表示例**

.. image:: ../_image/multicol/multicol_1.png
  :scale: 70

--------------------------
制約事項
--------------------------

表示モードの切替機能は提供しない
==================================
本フレームワークでは、画面サイズに応じた表示モードの切替機能は以下の理由から提供しない。画面サイズを変更した場合でも、表示モードは常にワイドモードベースの状態となる。

* ワイドモードベースで複数のUI部品を並べた画面を、別モードで同じレイアウトで表示することは不可能である

  モードを切り替えると画面幅が狭り、複数のUI部品を並べた画面でレイアウト崩れが発生する。

* 各モードでレイアウト崩れの発生を防止するためには、設計時に各モードごとのレイアウトテストを完了させる必要がある

  本フレームワークの特徴は、画面ごとに自由にUI部品を配置することにある。
  モードの切替を行った場合、各モード毎とのレイアウト定義及びテストを設計者が画面毎に実施する必要がある。

  これは、設計時のコストが非常に高くなり、UI開発基盤を使用するメリットが損なわれる事になる。


**画面幅を狭くした場合の表示例**

画面幅が狭くなった場合でも、ワイドモードベースの表示のままとなる。
非表示の部分は、画面下部の横スクロールバーを使用して表示させることになる。

.. image:: ../_image/multicol/multicol_2.png
  :scale: 75

一部UI部品ウィジェットは出力幅の指定機能を提供しない
=====================================================
タイトル部を出力するようなUI部品ウィジェット(以下のウィジェット)は、幅の指定機能は提供しない。

これらのウィジェットは、ページ内の情報を区切るためのタイトル行を出力する。
タイトル行はページ内での行を表すため、常に業務コンテンツ領域と同じ幅で出力される。

* :doc:`../reference_jsp_widgets/field_block` (\ */WEB-INF/tags/widget/field/block.tag*\ )
* テーブル関連のウィジェット (\ */WEB-INF/tags/widget/table/\*.tag*\ )

  * :doc:`../reference_jsp_widgets/table_plain`
  * :doc:`../reference_jsp_widgets/table_search_result`
  * :doc:`../reference_jsp_widgets/table_treelist`

* :doc:`../reference_jsp_widgets/tab_group` (\ */WEB-INF/tags/widget/tab/\*.tag*\ )

.. _apply-multicol-layout:

---------------------------------------
マルチレイアウトモードの適用方法
---------------------------------------
マルチレイアウトモードをプロジェクトに適用する手順を示す。

**1. マルチレイアウト用プラグインをプロジェクト側に取り込む**

  プロジェクトの\ *ui_plugins/package.json*\ を修正し、 マルチレイアウト用プラグインをプロジェクト側の\ *ui_plugins*\ に取り込む。

  以下に修正例を示す。

  .. code-block:: javascript

    { "name"   : "xxxx_project"
    , "version": "1.0.0"
    , "private": true

    , "dependencies":
      { "requirejs"    : "2.1.11"
      , "sugar"        : "1.4.1"
      , "jquery"       : "1.11.0"
      , "requirejs-text": "2.0.10"
      , "font-awesome": "4.0.3"
      
      // ----- 省略 ----- //

      , "nablarch-css-conf-multicol": "1.0.0"            // A. multicol用の変数定義プラグインを選択する
      , "nablarch-css-base": "1.0.0"
      , "nablarch-css-common": "1.0.0"

      // ----- 省略 ----- //

      , "nablarch-template-app_aside": "1.0.0"
      , "nablarch-template-app_header": "1.0.0"
      , "nablarch-template-base": "1.0.0"
      , "nablarch-template-multicol-head": "1.0.0"       // B. multicol用のhtml headプラグインを選択する
      , "nablarch-template-js_include": "1.0.0"
      , "nablarch-template-page": "1.0.0"
      , "nablarch-widget-multicol-row": "1.0.0"          // C. multicol用の行及び列を定義する
      , "nablarch-widget-multicol-cell": "1.0.0"         //   プラグインを選択する
      }

    // ----- 省略 ----- //
    }

  A.multicol用の変数定義プラグインを選択する::

    マルチレイアウト表示モードプラグイン(nablarch-css-conf-multicol)を選択する。

    本プラグインを選択することで、マルチレイアウト用のグリッド数定義や画面幅定義が行われる。

    ※各表示モード用のプラグイン(nablarch-css-conf-wide、compact、narrow)は選択しない。（記述されている場合は削除する）

  B.multicol用のhtml headプラグインを選択する::

    HTML headタグを出力するプラグインで、マルチレイアウト用のプラグイン(nablarch-template-multicol-head)を選択する。

    本プラグインを選択することで、マルチレイアウト用のCSSフレームワークが使用可能となる。また、表示モードの切替機能が無効化される。

    ※マルチレイアウト用ではないHTML headタグ出力プラグイン(nablarch-template-head)は選択しない。（記述されている場合は削除する）

  C.multicol用の行及び列を定義するプラグインを選択する::

    マルチレイアウト用の行、列を定義するためのプラグイン(nablarch-widget-multicol-row、nablarch-widget-multicol-cell)を選択する。

    本プラグインを選択することで、業務コンテンツ部に行及び列を定義できるようになり、UI部品ウィジェットの配置を自由に行うことが可能となる。

**2. ビルド用コマンド用設定ファイルの修正**

  プロジェクトの\ *ui_plugins/pjconf.json*\ を修正し、プロジェクトのWEBディレクトリ配下にUI部品（ウィジェット、JavaScript、スタイルシートなど）が展開されるようにする。

  詳細は、\ :ref:`pjconf_json`\ を参照

  以下に修正例を示す。

  .. code-block:: javascript

    {
      "pathSettings" :
      { "projectRootPath"   : "../.."
      , "webProjectPath"    : "xxxxxx/main/web"
      , "demoProjectPath"   : "ui_demo"
      , "testProjectPath"   : "ui_test"
      , "pluginProjectPath" : "ui_plugins"
      }

    , "cssMode" : ["multicol"]                            // A. CSSモードで「multicol」を選択する

    , "plugins" :
      [ { "pattern": "nablarch-css-.*" }
      , { "pattern": "nablarch-device-.*" }
      , { "pattern": "nablarch-js-util-.*" }
      , { "pattern": "nablarch-js-.*" }
      , { "pattern": "nablarch-widget-.*" }
      , { "pattern": "nablarch-template-.*" }
      , { "pattern": "nablarch-template-multicol-head" }  // B. マルチレイアウト用のHTML headタグが使用されるようにする
      , { "pattern": "nablarch-dev-.*" }
      , { "pattern": "nablarch-js-test-support" }
      , { "pattern": "web_project-widget-.*" }
      , { "pattern": "requirejs" }
      , { "pattern": "sugar" }
      , { "pattern": "jquery" }
      , { "pattern": "requirejs-text" }
      , { "pattern": "font-awesome" }
      , { "pattern": "less" }
      ]

      // ----- 省略 -----
    }

  A.CSSモードで「multicol」を選択する::

    本フレームワークは、「multicol」モードとして提供されるため、CSSモードに「multicol」と設定する。

  B.マルチレイアウト用のHTML headタグが使用されるようにする::

    マルチレイアウト用のHTML headタグを出力するプラグインが使用されるようにする。

    ※nablarch-template-multicol-headは、1つ上の行で定義されている「nablarch-template-.*」に含まれるが、
    通常モードの「nablarch-template-head」が使用されないように、明示的に「nablarch-template-multicol-head」を定義して上書きしている。
    (本設定ファイルは、下に書いた設定が必ず優先される)

**3.lessインポート定義ファイルの修正**

  プロジェクトの\ *ui_plugins/css/ui_public(または、ui_local)/multicol.less*\ を修正し、マルチレイアウト用CSSファイルがビルドできるようにする。

  multicol.lessは、自動生成した雛形を修正する。
  自動生成方法及び修正方法の詳細は、以下を参照すること。
  
  * :ref:`ui_genless`
  * :ref:`lessImport_less`

  :download:`サンプルのmulticol.lessのダウンロード <download/multicol.less>`

**4.uiビルドコマンドの実行**

  プロジェクトの\ *ui_plugins/bin/ui_build.bat*\ を実行する。

  これにより、マルチカラム用のlessファイルがビルドされ、各ウェブプロジェクトにマルチカラム用CSS(multicol.css、multicol-minify.css)が生成される。
  また、各種UI部品が各ウェブプロジェクトに展開される。

.. _multicol_css_framework_setting_layout:

--------------------------
レイアウトの調整方法
--------------------------
プロジェクトの要件で、画面の表示領域の幅等を変更したい場合には、本手順を参考にして変更を行うこと。

マルチカラム用のグリッド数や画面幅の定義は、プラグイン(\ *nablarch-css-conf-multicol*\ 、\ *nablarch-template-app_aside*\ )としてデフォルトの設定が提供される。
このプラグインをプロジェクト側にコピーし、プロジェクト用プラグインとして修正することで画面幅などを変更することができる。

プラグインの作成方法は、\ :ref:`add_plugin`\ を参照。

以下に修正ポイントを示す。

**nablarch-css-conf-multicol**

* 業務画面部全体の幅を変更する場合には、@columnsの定義を変更する
* 業務コンテンツ部の幅を変更する場合には、@contentGridSpanの定義を変更する
  
  @fieldGridSpanと@tableGridSpanも業務コンテンツ部の幅に合わせて変更する

.. code-block:: css

  @columns      : 64;         // 1ページ内のグリッド数
  @trackWidth   : 13px;       // 1グリッドのグリッド幅
  @gutterWidth  : 2px;        // 1グリッドあたりのマージン幅
  @totalWidth   : @columns * (@trackWidth + @gutterWidth);  // 1ページの横幅

  @smallestFontSize : 11px;
  @smallerFontSize  : 12px;
  @baseFontSize     : 14px;
  @largerFontSize   : 16px;
  @largestFontSize  : 18px;

  // グリッド数(デフォルトのグリッド数）
  @labelGridSpan  : 10;       // ラベル部のグリッド数
  @inputGridSpan  : 21;       // 入力欄のグリッド数
  @buttonGridSpan : 8;        // 標準ボタンのグリッド数
  @unitGridSpan   : 3;        // 単位表示部のグリッド数

  @fieldGridSpan  : 45;       // 業務画面部に配置する要素のグリッド数
  @tableGridSpan  : 45;       // 標準テーブルのグリッド数
  @contentGridSpan: 45;       // 業務面部のグリッド数
  @contentWidth   : @contentGridSpan * (@trackWidth + @gutterWidth);   // 業務領域の幅

**nablarch-template-app_aside**

* サイドバーの幅を変更する場合には、\ *#aside*\ 部の.grid-colに指定している値を変更する
* メニューを使用しない画面でサイドバー部のマージン調整を行う場合には、\ *#aside.noMenu*\ 部の.grid-colに指定している値を変更する

.. code-block:: css

  #aside {
    .grid-col(16);
    min-height: 350px;
    padding-top: 15px;
    li a {
      display : block;
      width   : 100%;
      padding : 5px 10px;
    }
  }

  // メニューがない場合の領域の定義
  #aside.noMenu {
    .grid-col(8);
  }

.. _multicol_css_framework_example:

--------------------------
使用例
--------------------------
幾つかのレイアウトパターンを使用してJSPの作成方法について解説する。

マルチレイアウトモードを使用する際には、以下の点が重要なポイントとなる。

* UI部品ウィジェットは、必ず行内(\ *layout:row*\ )に配置する [#row]_
* 各UI部品ウィジェット使用時には、そのウィジェットの幅(グリッド数)を指定する
* 行内に配置するUI部品ウィジェットの幅(グリッド数)の合計は、業務コンテンツ部の幅(グリッド数)以内とする [#grid-count]_

  業務コンテンツ部のグリッド数は、\ `レイアウトの調整方法`_\ の\ *@contentGridSpan*\ で定義された値

.. [#row] 

  `一部UI部品ウィジェットは出力幅の指定機能を提供しない`_ で説明したUI部品ウィジェットは、
  これ自体が行を表しているため行内に配置する必要はない。

.. [#grid-count]

  幅(グリッド数)の合計が業務コンテンツ部の幅を超えた場合には、自動的に折り返され次の行に出力される。

  折り返し位置は、指定することが出来ずブラウザ依存となるため、業務コンテンツ部の幅に収まるようにUI部品ウィジェットを配置すること。


1行に複数のUI部品を並べる場合
===============================
1行に複数のUI部品ウィジェットを並べる方法を解説する。

**実装ポイント**

* UI部品ウィジェットを並べる場合には、行(\ *layout:row*\ )を定義する

  この例では、入力欄と画面遷移用ボタンで3行を定義している。

* タイトル部、入力部の幅を統一する場合には変数に切り出す

  この例のように、入力系UI部品ウィジェットのタイトル部、入力部の幅を固定化する場合、そのサイズを変数に切り出すと良い。
  これにより、タイトル部や入力部のサイズ変更時には、変数の値を変更するのみでよくなる。

* 並べるUI部品にマージンを設ける場合は、空の列(\ *layout:cell*\ )を配置する

  空の列(\ *layout:cell*\ )に対して幅(gridSize)を指定することで、マージン幅を指定できる。


**画面表示例**

.. image:: ../_image/multicol/multicol_sample_1.png
  :scale: 75

**JSP実装例**

.. code-block:: jsp

  <n:form windowScopePrefixes="user">
    <%-- タイトル部、入力部の幅定義 --%>
    <n:set var="titleSize" value="10" />
    <n:set var="inputSize" value="10" />

    <tab:group name="userTab">
      <tab:content title="ユーザ情報" value="userInfo" selected="true">

        <%-- 行を配置する(1行目) --%>
        <layout:row>

          <%-- 入力部品は、タイトル部と入力部の幅を指定して配置する --%>
          <field:text
              title="郵便番号"
              required="true"
              name="user.postNo"
              titleSize="${titleSize}"
              inputSize="${inputSize}">
          </field:text>

          <%--
          入力部品とボタンの間のマージン

          マージンは、要素のない列(layout:cell)を使用することで、
          好きな位置に挿入することができる。
          --%>
          <layout:cell gridSize="10"></layout:cell>

          <%-- ボタンは幅指定をして配置する --%>
          <n:forInputPage>
            <button:submit label="住所検索" uri="dummy" size="10"></button:submit>
          </n:forInputPage>
        </layout:row>

        <%-- 行を配置する(2行目) --%>
        <layout:row>
          <field:pulldown
              title="都道府県"
              name="user.address1"
              required="true"
              listName="都道府県リスト"
              elementLabelProperty="name"
              elementValueProperty="cd"
              titleSize="${titleSize}"
              inputSize="${inputSize}">
          </field:pulldown>
          <field:text
              title="市区郡町村名"
              name="user.address2"
              required="true"
              titleSize="${titleSize}"
              inputSize="${inputSize}">
          </field:text>
        </layout:row>

      </tab:content>
      <tab:content title="勤務先情報" value="officeInfo">
      </tab:content>
    </tab:group>

    <%-- 行を配置する(3行目) --%>
    <layout:row>
      <n:forInputPage>
        <%-- ボタンの表示位置調整のためのマージン --%>
        <layout:cell gridSize="17"></layout:cell>
        <button:check
            size="10"
            uri="./確認画面_ページ.jsp">
        </button:check>
      </n:forInputPage>
      <n:forConfirmationPage>
        <%-- ボタンの表示位置調整のためのマージン --%>
        <layout:cell gridSize="10"></layout:cell>
        <button:back uri="./登録画面.jsp" size="10"></button:back>
        <%-- ボタンの表示位置調整のためのマージン --%>
        <layout:cell gridSize="5"></layout:cell>
        <button:confirm uri="dummy" size="10"></button:confirm>
      </n:forConfirmationPage>
    </layout:row>
  </n:form>

列によって異なる行数を定義する場合
======================================
行内に配置する列によって、異なる行数(htmlのtableのrowspanのイメージ)を定義する方法を解説する。

**実装ポイント**

* 列ごと異なる行数を定義する場合には、行内にネストした行を定義する

  画面表示例のように行内に列(\ *layout:cell*\ )を定義し、列内にネストした行を配置することで特定の列に複数の行を定義できるようになる。

* ネストした行内に配置するUI部品の幅の合計は、列(\ *layout:cell*\ )の幅(gridSize)を超えてはならない


**画面表示例**

.. image:: ../_image/multicol/multicol_sample_2.png
  :scale: 70

**JSP実装例**

.. code-block:: jsp

  <%-- 行定義 --%>
  <layout:row>

    <%--
    ネストした行を配置するための列を定義する
    列には明示的に幅(gridSize)を指定する。
    --%>
    <layout:cell gridSize="20">

      <%-- ネストした行の定義(1行目) --%>
      <layout:row>
        <%--
        入力欄の配置
        
        入力欄の幅の合計は、列(layout:cell)に定義した幅(gridSize)を超えてはならない
        --%>
        <field:text
            title="漢字氏名"
            name="user.kanjiName"
            required="true"
            titleSize="10"
            inputSize="10">
        </field:text>
      </layout:row>

      <%-- ネストした行の定義(2行目) --%>
      <layout:row>
        <%--
        入力欄の配置
        
        入力欄の幅の合計は、列(layout:cell)に定義した幅(gridSize)を超えてはならない
        --%>
        <field:text
            title="カナ氏名"
            name="user.kanaName"
            required="true"
            titleSize="10"
            inputSize="10">
        </field:text>
      </layout:row>

    </layout:cell>

    <%--
    2列目の性別選択欄は、外側の列内に配置することで、1列目(layout:cell)の隣に表示される
    --%>
    <field:radio
        title="性別"
        name="user.sex"
        required="true"
        listName="sexList"
        listFormat="br"
        elementLabelProperty="name"
        elementValueProperty="cd"
        titleSize="${titleSize}"
        inputSize="${inputSize}">
    </field:radio>
  </layout:row>

