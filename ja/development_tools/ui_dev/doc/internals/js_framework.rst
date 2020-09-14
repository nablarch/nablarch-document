==================================
JavaScript UI部品
==================================

-----------
概要
-----------
:doc:`js_framework` は、カレンダー表示やページ内タブページのように、
通常のHTMLの範疇では実現できないUI機能を実装するJavaScript部品群である。
これらの部品群は、以下の指針に基づき、独自実装されている。

- Nablarchフレームワークの動作を前提とし、エラー時の入力データ復帰や、
  非活性項目・変更不可項目など、サーバ処理との連携の整合性を重視する。
   
- 可能な限りJavaScriptを直接記述しなくてもカスタマイズできるようにする。  

- UI標準に準じた挙動、統一的なデザインが実現されること。

利用可能な各部品の仕様については :doc:`../reference_js_framework` を参照すること。

使用例
---------------------
以下のソースコードは、画面内の入力要素に対してカレンダー入力部品を使用している例である。

.. code-block:: jsp

    <div class="field">
      <label>適用開始日：</label>
      <input id="effectiveDate" type="text" value="" />
      <button class="nablarch_DatePicker
                    -format yyyy/MM/dd
                    -locale ja
                    -input  effectiveDate">
        <i class="fa fa-calendar"></i>
      </button>
    </div>

`<button>` 要素に指定された **class** 属性の内容に注目してほしい。
ここでは、 `<button>` 要素に適用する :doc:`js_framework` を指定する **マーカCSS** と呼ばれる識別子(**nablarch_DatePicker**)
の後に当該の部品の挙動を定義する各種オプション(**-format yyyy/MM/dd -locale ja -input effectiveDate**)
が続いている。
このように :doc:`js_framework` の利用するには上記のようなCSSの指定のみを行えばよく、JavaScriptを直接記述する必要はない。


**注)**  :doc:`js_framework` は基本的には :doc:`jsp_widgets` 内で使用することを想定しており、
一般の業務画面実装者がこれらのAPIを直接使用することは想定していない。

依存ライブラリ
----------------------
本機能は、以下の外部ライブラリに依存している。

  ============= =================================================== =============
  ライブラリ名  用途                                                ライセンス
  ============= =================================================== =============
  require.js    JavaScriptの分割モジュール管理                      MIT          
  sugar.js      ECMAScript5互換関数を含むユーティリティAPI群の提供  ライセンスフリー    
  jQuery        DOM関連APIの簡易化およびブラウザ互換レイヤの提供    MIT
  ============= =================================================== =============

---------------------------
初期処理
---------------------------
:doc:`js_framework` の初期処理は各業務画面のJSPから参照している `/js/nablarch.js` もしくは
それをミニファイした `/js/nablarch-minify.js` によって行われる。

.. tip::
  本番環境では、処理性能を最大化するため、全てのJavaScriptを事前にミニファイし、単一のJavaScriptとして
  ロードするが、開発環境では、開発効率性を重視するため、各スクリプトは個別に動的ロード(XHR)される。

初期処理は上記スクリプトのロードが完了した時点に行われる処理と、
業務画面JSPのDOM構造が確定した時点(ドキュメントロード)の処理の2段階に分けて実行される。

スクリプトロード時の挙動
----------------------------
:doc:`js_framework` は AMD(Asynchronous Module Definition) 形式に沿って実装されており、
AMDモジュール管理ライブラリである **require.js** により、動的にロードもしくは事前にミニファイされる。

:doc:`js_framework` のロードは `/js/nablarch.js` 内の以下の処理によって開始される。

.. code-block:: javascript

  // 初期ロード対象コンポーネント
  require(["nablarch/ui"], function(ui) {
    $(function() {
      ui.Widget.init(); //ドキュメントロード後の初期化処理を実行
    });
  });

上記ソースコードによってロードされるモジュールが `/js/nablarch/ui.js <../../../../_static/ui_dev/yuidoc/files/js_nablarch_ui.js.html>`_ である。
このモジュールは、プロジェクトで使用する全UI部品を以下のように依存モジュールとして定義している。

.. code-block:: javascript

  define([
    "nablarch/ui/Widget"
  , "nablarch/ui/event"  
  , "nablarch/ui/ListBuilder"
  , "nablarch/ui/DatePicker"
  , "nablarch/ui/AutoSum"
  , "nablarch/ui/Collapsible"  
  , "nablarch/ui/TreeList"
  , "nablarch/ui/readonly"
  , "nablarch/ui/Placeholder"
  , "nablarch/ui/Tab"
  ], function(Widget) { "use strict";
    return {
      Widget: Widget
    };
  });

各UI部品側では、先に述べた **マーカCSS** の宣言と、UI部品の登録処理
(`Widget.register() <../../../../_static/ui_dev/yuidoc/classes/nablarch.ui.Widget.html>`_)を呼び出す。
以下は `/js/nablarch/ui/DatePicker.js <../../../../_static/ui_dev/yuidoc/classes/nablarch.ui.DatePicker.html>`_ の例である。

.. code-block:: javascript

  DatePicker.widgetType = "nablarch_DatePicker"; //マーカCSS
  Widget.register(DatePicker); // UI部品の登録

このように全てのUI部品の初期化と登録が完了すると、最初の `/js/nablarch.js` に制御が戻り
`Widget.init() <../../../../_static/ui_dev/yuidoc/classes/nablarch.ui.Widget.html>`_ をドキュメントロード後に呼び出す。
(イベントハンドラ登録する。)


ドキュメントロード時の挙動
-----------------------------
ドキュメントロード後に呼び出される
`Widget.init() <../../../../_static/ui_dev/yuidoc/classes/nablarch.ui.Widget.html>`_ では、各UI部品に対して以下の初期処理を実行する。

1. **マーカCSS** にマッチするドキュメント上の各要素に対してUI部品のインスタンスを作成する。
   この際、要素のNodeインスタンスおよびマーカCSSに付随するオプションをパースしたオブジェクトが
   コンストラクタの引数として渡される。

2. 生成したインスタンスを当該要素の **data-** プロパティとして設定し
   UI部品のインスタンスがGCの対象とならないようにする。
   なお、1. の初期化処理の前に、この **data-** プロパティの内容をチェックするので
   同じ要素に対して複数回初期化が行われることはない。


UI部品の再初期化
------------------------------------
JavaScriptのテンプレート処理などによって、画面ロード完了後に **マーカCSS** を含むドキュメントノードを
動的に追加しても、そのままでは上で述べた初期化処理は実行されず、期待された動作とならない。
このような場合は明示的に `Widget.init() <../../../../_static/ui_dev/yuidoc/classes/nablarch.ui.Widget.html>`_
を呼び出す必要がある。

上で述べたように、既に初期化されている要素に対しては何もしないので、複数回実行しても
既にドキュメント上に存在しているUI部品に影響を与えることはない。

-------------------------
ファイル構成
-------------------------

**構成ファイル一覧**

============================ ======== ======= ============================ ==========================================================================
名称                         動作環境 [#1]_   パス                         内容                       
---------------------------- ---------------- ---------------------------- --------------------------------------------------------------------------
_                            ローカル サーバ  _                            _
============================ ======== ======= ============================ ==========================================================================
初期ロードスクリプト         ○        △       /js/nablarch.js              AMDロードパスを設定し、PJで使用するUIモジュールの初期化ルーチンを実行する。 |br|
                                                                           また、スクリプトロード直後でしか実行できない処理をあわせて行う。 |br|
                                                                           (iPadでの画面ロードサイズに関する問題の対処スクリプトの適用など)

ミニファイ済みスクリプト     ×        ○       /js/nablarch-minify.js       初期ロードスクリプトの依存ライブラリを全て結合し、ミニファイした
                                                                           スクリプト。
                                                                           本番環境では、このスクリプトと require.js のみを使用する。

AMDスクリプトローダ          △        ○       /js/require.js               AMD形式で記述されたJavaScript部品のローダ

テキストリソースローダ       ○        △       /js/text.js                  require.js の拡張プラグイン。JavaScript以外のテキストリソースを
                                                                           XHR経由で動的にロードする。

jQueryライブラリ             ○        △       /js/jquery.js                DOM操作API/イベント管理APIのブラウザ間互換レイヤーを提供する。

sugar.js                     ○        △       /js/sugar.js                 ECMAScript5互換関数および、その他のユーティリティ系API群の提供

簡易BigDecimal               ○        △       /js/nablarch/util/           JavaScriptによる簡易BigDecimal実装。
                                              BigDecimal.js

簡易SimpleDateFormat         ○        △       /js/nablarch/util/           Java SDK SimpleDateFormat の仕様のうち、
                                              SimpleDateFormat.js          日付に関する処理のサブセットを実装する。 

日付ライブラリ               ○        △       /js/nablarch/util/           JavaScriptネイティブ日付型(Date)と
                                              DateUtil.js                  日付文字列との相互変換を行うためのライブラリ。

UI部品共通プロトタイプ       ○        △       /js/nablarch/ui/             UI部品の実装に必要な共通機能(HTMLノードへのバインド
                                              Widget.js                    /イベント定義/画面ロード時処理の起動)などを実装
                                                                           する共通プロトタイプ。

自動集計                     ○        △       /js/nablarch/ui/             入出力項目の自動集計を行うUI部品。
                                              AutoSum.js                 

日付入力部品                 ○        △       /js/nablarch/ui/             カレンダーを用いた日付入力を実装するUI部品
                                              DatePicker.js

カレンダーテンプレート       △        △       /js/nablarch/ui/             日付入力部品のカレンダー部分に表示する
                                              DatePicker.template          HTMLを記述するテキストファイル。

リストビルダー部品           ○        △       /js/nablarch/ui/             2つのセレクトボックスを用いた、複数選択用のUI
                                              ListBuilder.js

リストビルダーテンプレート   △        △       /js/nablarch/ui/             リストビルダーの制御ボタン部分に表示する
                                              ListBuilder.template         HTMLを記述するテキストファイル。

タブ切り替え部品             ○        △       /js/nablarch/ui/             JavaScriptによるページ内タブ切り替えUIを実装する部品。
                                              Tab.js

Nablarchサブミット連動       ○        △       /js/nablarch/ui/             Nablarchのサブミット制御管理機構に連動して、
                                              event.js                     画面サブミットの前後に発火するカスタムイベントを
                                                                           定義する。

============================ ======== ======= ============================ ==========================================================================

.. [#1]
  **「サーバ」:**
    実働環境にデプロイして使用するかどうか
  **「ローカル」:**
    ローカル動作時に使用するかどうか
  **○ :**
    使用する 
  **△ :**
    直接は使用しないがミニファイしたファイルの一部として使用する。
  **× :**
    使用しない

---------------------------------------
新規 JavaScript UI部品の作成方法
---------------------------------------
本ドキュメントでは、UI部品カタログに収録されている既存のもの以外の
UI部品を作成する方法について解説する。

作成するファイル
---------------------
標準的なUI部品は以下の3つのファイルから構成される。

**1. モジュール定義ファイル(.js)**
  ウィジェットの処理を記述したJavaScriptファイルである。
  以下の場所に配置する。::

    (コンテキストルート)/js/(PJ名)/ui/(ウィジェット名).js

**2. テンプレートファイル(.template)**
  ウィジェット内のUIを定義するHTMLファイルである。
  モジュール定義ファイルと同じ場所に配置する。::

    (コンテキストルート)/js/(PJ名)/ui/(ウィジェット名).template

**3. スタイル定義(.less)**
  ウィジェットのスタイルを定義するCSS(LESS)ファイルである。
  以下の場所に配置する。::

    (コンテキストルート)/css/ui/(ウィジェット名).less

ウィジェットの実装例
---------------------------------------
以下のソースコードは、単純なモーダルダイアログを実装するサンプルである。

.. code-block:: javascript

  // ==============================================
  // モジュール定義
  // ===============================================
  // グローバル関数define() によりモジュールを定義する。
  //
  // 依存関係の定義
  // -----------------------------------
  // この関数の第一引数には、このモジュールが依存するモジュールのパスの配列を指定する。
  // モジュールのパスは、(コンテキストルート)/js/ からの相対パスを指定する。
  // また、"./"で始まるパスは、このソースファイルからの相対パスとみなされる。
  // パスの先頭に"text!"を指定した場合、当該のファイルはJavaScriptとして評価されず、
  // ファイルの内容を文字列として読み込む。
  // 
  define([
    "jquery"                       // jQueryライブラリ
  , "nablarch/ui/Widget"           // ウィジェットの共通基底クラス
  , "text!./ModalDialog.template"  // モーダルダイアログのHTML
  , "nablarch/ui/event"            // nablarchの動作に関連したイベントの定義
  , "sugar"                        // sugar.js
  ],
  // ----------------------------------
  // モジュールの初期化
  // ----------------------------------
  // define の第2引数には、このモジュールの初期化を行う関数を指定する。
  // この初期化関数の引数には、defineの第1引数に指定した各モジュールの内容が渡される。
  // 
  function($, Widget, template) { "use strict";
    //
    // モジュール定義を行う関数
    // =================================
    // モジュールの初期化を行う関数を冒頭に定義し、この関数の最後で呼び出す。
    // (このコードが冒頭に記述することで、モジュールの内容を把握し易くなる。)
    function define() {
      // jQueryプラグインメソッド $.fn.widgets() を使用して、マーカCSSが指定された
      // 各ノードに対して画面上のウィジェットを初期化する。
      // マーカCSSの名称は (プロジェクト名)_(ウィジェット名) とする。
      $(function() {
        $(".sample_ModalDialog.-content").widgets(ModalDialog);
      });
      // このモジュールの内容(=ウィジェットのコンストラクタ関数)をリターンする。
      return ModalDialog;
    }
    
    // ウィジェットクラスのプロトタイプ定義
    // ========================================
    // 本PJでのクラス定義はJavaScriptの言語仕様のみを用いたオーソドックスなスタイルで行う。
    // 下記のように、ウィジェットのプロトタイプを定義する。
    //
    ModalDialog.prototype = Object.merge(new Widget(), {   // Widgetコンストラクタのプロトタイプを継承する。
      // コンストラクタ
      constructor : ModalDialog   // instanceof 演算子を正常に動作させるために必要。 
      // プロパティ
    , $dialog   : null
    , contentId : null
    , isActive  : null
      // メソッド
    , show : ModalDialog_show
    , hide : ModalDialog_hide
    });

    // イベント定義
    // ============================================
    // ウィジェットおよび、ウィジェットのプロパティとして定義されたノード上のイベントと、
    // それを処理するイベントハンドラとの対応を以下の書式に従って記述する。
    // 
    //   1. "(イベント名)" : (イベントハンドラ)
    //   2. "(セレクタ式) (イベント名)" : (イベントハンドラ)
    //   3. "(コンテキストノード) (イベント名)" : (イベントハンドラ)
    //   4. "(コンテキストノード) (セレクタ式) (イベント名)" : (イベントハンドラ)
    // 
    // 1.ではマーカCSSを指定したノード(this.$node)上で発生するイベントに対するハンドラを登録する。
    // また2.のようにセレクタ式を指定することで、イベントの発生元がセレクタに合致する場合のみ処理を
    // 行うようにすることができる。(event deligation)
    // 
    // 3. 4. では、(コンテキストノード)に指定したノード内で発生したイベントが対象となる。
    // (コンテキストノード)には $で開始されるプロパティ名もしくは "document" を指定する。
    // 
    // (イベントハンドラ) には文字列および関数を使用できる。
    // 文字列の場合は、このウィジェットの同名のメソッドを呼び出す。
    // 関数の場合は、このウィジェットをbind()したものが呼び出される。
    //
    ModalDialog.event = {
      // 1. 起動要素がクリックされたらモーダルダイアログを開く
      //   -> this.$node.on("click", function(evt) { return this.show(evt) }) と等価
      //
      "click" : "show" 

      // 2. ダイアログの閉じるボタンが押されたらダイアログを閉じる。
      //   -> this.$dialog.on("click", "button.close", function(evt) { return this.hide(evt) }) と等価
      //
    , "$dialog button.close click" : "hide" 

      // 3. ダイアログが開いている間は画面上のサブミット処理を全て無効化する。
      //   -> $(document).on("beforeSubmit", (function() {return false}).bind(this)) と等価
      //   ※  カスタムイベント "beforeSubmit.nablarch" は "nablarch/ui/event" の中で定義されており、
      //      グローバル関数 nablarch_submit() によってサブミットが行われる直前に呼ばれる。
      //
    , "document beforeSubmit" : function() { return !isActive } 
    };

    // ウィジェットの識別子
    // ===================================
    // 内部的に使用される。
    // マーカCSSと同じ (PJ名)_(ウィジェット名) とする。
    ModalDialog.widgetType = "sample_ModalDialog";  

    // ウィジェットのコンストラクタ関数
    // ===============================================
    // 第1引数にウィジェットのマーカCSSを指定したDOMノード、
    // 第2引数にはマーカCSSの後に指定したオプションが渡される。
    // なお、JavaScriptでは親クラスのコンストラクタは呼ばれないので、明示的に呼び出す必要がある。
    //
    function ModalDialog(element, option) {

      // プロパティの初期化
      // -------------------------------------------
      // 各プロパティの初期化を行う。
      // 特に、ノードプロパティの初期化Widgetコンストラクタの呼び出しよりも先に行う必要がある。
      // ※  ノードの内容は後でカスタマイズしやすいように、テンプレートファイルを使用すること。
      this.contentId = option.content
      this.isActive  = false;
      this.$dialog   = $(template).css({
                         display   : "none"
                       , position  : "absolute"
                       , "z-index" : "5"
                       }).appendTo(document); 
      
      // Widgetコンストラクタの呼び出し
      // --------------------------------------------------
      // 共通初期化処理を行う。
      // (詳細な内容については、 nablarch/ui/Widget.js 内のドキュメントを参照)
      Widget.call(this, element);

      // -content オプションに指定されたidの内容をダイアログの内容として取り込む。
      this.$dialog.find("div.content").append("#" + contentId);
    }


    // ウィジェットのメソッド、イベントハンドラの定義
    // ===============================================
    // イベントハンドラとして登録した場合、第一引数にはイベントオブジェクト(jQuery.Event) が渡される。
    // イベントオブジェクトのtarget属性には、イベントの発生元のDOMノードオブジェクトが設定されている。
    // また、明示的にfalseをリターンすることで、イベントのプロパゲーションとデフォルトアクションの実行を抑止する
    // ことができる。
    
    function ModalDialog_show(event) {
      this.isActive = true;
      this.$dialog.slideDown("fast");
      return false; // デフォルトアクションを抑止する。
    }

    function ModalDialog_hide(event) {
      this.isActive = false;
      this.$dialog.slideUp("fast");
      return false; // デフォルトアクションを抑止する。
    }

    return define();  // モジュールの内容をリターンする。
  });


.. |br| raw:: html

  <br />

