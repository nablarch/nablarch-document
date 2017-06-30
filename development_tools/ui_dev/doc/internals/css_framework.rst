====================
CSSフレームワーク
====================

-----------------
概要
-----------------
**CSSフレームワーク** は **UI標準** に定義されたレイアウト・デザインを実装する
スタイルシート群である。


.. _display_mode:

--------------------------
表示モード切替え
--------------------------
本フレームワークでは、以下の3つのCSSファイルを CSS Media Query の機能を用いて動的に切り替えることで、
UI標準の **「2.1 端末の画面サイズと表示モード」** の記載内容を実現している。

  - wide.css (ワイド表示用スタイル)
  - compact.css (コンパクト表示用スタイル)
  - narrow.css (ナロー表示用スタイル)


-----------------------
ファイル構成
-----------------------
CSSファイルは全て、LESSファイル形式で記述する。

LESS形式からCSSへのコンパイル及びファイルの結合は、\ :ref:`UI部品のビルドと配置<executing_ui_build>`\ で行う。
詳細は、\ :ref:`ui_genless` を参照

結合されたCSSファイルは\ **/css/built/**\ 配下に配置され、各画面から外部参照される。
この<link>タグは\ **/WEB-INF/tags/device/media.tag**\ (/include/html_head.jspから利用されているタグファイル)に以下のように定義されている。

  .. code-block:: jsp

    <%@tag pageEncoding="UTF-8" description="表示モードによってスタイルを読み込むウィジェット" %>
    <%@taglib prefix="n" uri="http://tis.co.jp/nablarch" %>
    <%@taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

    <%-- (本番用) --%>
    <!--[if lte IE 8]>
    <n:link rel="stylesheet" type="text/css" href="/css/built/wide-minify.css" />
    <![endif]-->

    <!--[if gte IE 9]>
    <n:link rel="stylesheet" type="text/css" href="/css/built/wide-minify.css"    media="screen and (min-width: 980px)" />
    <n:link rel="stylesheet" type="text/css" href="/css/built/compact-minify.css" media="screen and (min-width: 640px) and (max-width: 979px)" />
    <n:link rel="stylesheet" type="text/css" href="/css/built/narrow-minify.css"  media="screen and (max-width: 639px)" />
    <![endif]-->

    <!--[if !IE]> -->
    <n:link rel="stylesheet" type="text/css" href="/css/built/wide-minify.css"    media="screen and (min-width: 980px)" />
    <n:link rel="stylesheet" type="text/css" href="/css/built/compact-minify.css" media="screen and (min-width: 640px) and (max-width: 979px) and (orientation: portrait)" />
    <n:link rel="stylesheet" type="text/css" href="/css/built/compact-minify.css" media="screen and (min-width: 640px) and (max-width: 979px) and (max-height: 979px) and (orientation: landscape)" />
    <n:link rel="stylesheet" type="text/css" href="/css/built/narrow-minify.css"  media="screen and (max-width: 639px)" />
    <n:link rel="stylesheet" type="text/css" href="/css/built/wide-minify.css"    media="screen and (device-width: 768px) and (device-height: 1024px) and (orientation:landscape)" />
    <!-- <![endif]-->
    
各表示モードを切替える CSS Media Query が指定されたlinkタグを記載している。
なお、IE8以下では CSS Media Query をサポートしないため、IEコンディショナルコメントを使用し、常にワイドモードで表示する
ようにしている。


構成ファイル一覧
------------------------

============================ ======== ======= ========================================== ========================================================
名称                         動作環境 [#1]_   パス                                       内容                       
---------------------------- ---------------- ------------------------------------------ --------------------------------------------------------
_                            ローカル サーバ  _                                          _
============================ ======== ======= ========================================== ========================================================
**ビルド済みCSSファイル**
-------------------------------------------------------------------------------------------------------------------------------------------------
ワイドモードスタイル         ○ |br|   ○ |br|    /css/built/wide-minify.css |br|            ワイドモード時に使用するミニファイ済みCSSファイル |br|
                             ×        ×         /css/built/wide.css                        コンパイル済み/未ミニファイのもの [#minify]_

コンパクトモードスタイル     ○ |br|   ○ |br|    /css/built/compact-minify.css |br|         コンパクトモード時に使用するミニファイ済みCSSファイル |br|
                             ×        ×         /css/built/compact.css                     コンパイル済み/未ミニファイのもの [#minify]_

ナローモードスタイル         ○ |br|   ○ |br|    /css/built/narrow-minify.css |br|          ナローモード時に使用するミニファイ済みCSSファイル |br|
                             ×        ×         /css/built/narrow.css                      コンパイル済み/未ミニファイのもの [#minify]_

**LESSファイル**
-------------------------------------------------------------------------------------------------------------------------------------------------
CSS3互換ルール               △        △       /css/core/css3.less                        ブラウザ間で仕様の異なるスタイルについて、単一の |br|
                                                                                         記述で対応できるようにしたルール。

デフォルトスタイルリセット   △        △       /css/core/reset.less                       ブラウザ間で仕様の異なるデフォルトスタイルを全て |br|
                                                                                         リセットする。

グリッドレイアウトシステム   △        △       /css/core/grid.less                        後述のグリッドレイアウトを実装する基本ルール群。

基本スタイル定義             △        △       /css/style/base.less                       htmlの各タグのスタイル定義を標準化するための |br|
                                                                                         スタイル定義。

業務画面領域スタイル定義     △        △         /css/template/\*.less                    UI標準で定義された、各業務画面領域のスタイル定義。|br|
                                                                                         各表示モード(wide、compact、narrow)用のスタイル定 |br|
                                                                                         義も提供される。|br|
                                                                                         base-wide.less、base-compact.less、base-narrow.less |br|
                                                                                         のように表示モードを示すサフィックスが付加された |br|
                                                                                         LESSファイルが提供される。

UI部品ウィジェットスタイル   △        △         /css/button/\*.less |br|                 各UI部品ウィジェットのスタイル定義。|br|
                                                /css/field/\*.less |br|                  UI部品ウィジェットによっては、各表示モード用の    |br|
                                                /css/box/\*.less |br|                    スタイル定義も提供される。
                                                /css/table/\*.less |br|
                                                /css/column/\*.less

JavaScript UI部品スタイル    △        △       /css/ui/\*.less                            各JavaScript UI部品のスタイル定義。


============================ ======== ======= ========================================== ========================================================



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

.. [#minify]
 未ミニファイCSSファイルとミニファイ済みCSSファイルとの違いはコメントの有無のみである。
 ミニファイ済みCSSファイルを開発中から使用しても開発効率を落とすことはない。

 このため、\ `ファイル構成`_ \ にあるように、常にミニファイ済みファイルを使用し、
 未ミニファイ済みファイルを使用することはない。

----------------------------------
グリッドベースレイアウト
----------------------------------
**グリッドベースレイアウト** とは、ページ全体に渡る縦罫と横罫を定め、
それに沿ってコンテンツを配置するレイアウト手法である。  

本システムのワイド表示モードにおける業務画面は横幅965pxであり、
これを24のグリッドと呼ばれる単位に分割している。

次の図は、業務画面の基本構造をグリッド単位で表したものである。

  .. figure:: ../_image/app_grid.png
     :scale: 80
     :align: center

このように、画面内のオブジェクトの配置はグリッド単位で定められる。
グリッドを使用する対象は画面の基本構造だけではなく、
業務画面内に配置されるオブジェクトは原則としてグリッドを使用して配置するものとする。


.. tip:: 

  グリッドベースレイアウトの一般的な解説については、以下のサイトなどを参照すること。
  
    http://xdissent.github.com/grid-less/ 



グリッドレイアウトフレームワークの使用方法
----------------------------------------------------
グリッドレイアウトを使用するには、HTML中の要素に以下のCSSクラスを指定する。

  =============================  =================================================================================
  クラス名                       用途
  =============================  =================================================================================
  .grid-row                      グリッドの横列を定義するブロック要素に指定する。 |br|
                                 
                                 .. tip::

                                  本クラスは、ページの全幅分の領域を固定で確保する。|br|
                                  このため、業務コンテンツ部などのページの全幅より狭い領域で |br|
                                  使用すると、行が領域からはみ出し横スクロールバーが表示され |br|
                                  る原因となるため注意すること。

  .content-row                   業務コンテンツ部での横列を定義するブロック要素に指定する。 |br|

  .grid-col-(横幅)               グリッドの横列内に配置するコンテンツに指定する。 |br|
                                 (横幅)には、そのコンテンツが占める横幅をグリッド数で指定する。

  .grid-offset-(左余白)          グリッドの横列内に配置するコンテンツに指定する。 |br|
                                 (左余白) には、そのコンテンツの左側に開ける余白幅をグリッド数で指定する。

  =============================  =================================================================================

次の図は、メインコンテンツ内の入力フォームの配置を表したものである。

  .. figure:: ../_image/field_grid.png
     :scale: 80
     :align: center

これを実装するには、以下のように記述すればよい。

**JSP**

  .. code-block:: jsp

    <div class="content-row">
      <label class="grid-col-5">ログインID：</label>
      <n:text name      = "11AC_W11AC01.loginId"
              size      = "25"
              maxlength = "20"
              cssClass  = "grid-col-8"
      />
    </div>
 
    <div class="content-row">
      <label class="grid-col-5">パスワード：</label>
      <n:password name      =" 11AC_W11AC01.kanjiName"
                   size      = "25"
                   maxlength = "20"
                   cssClass  = "grid-col-8"
      />
      <n:error name="11AC_W11AC01.kanjiName"/>
    </div>

.. tip::
  上記ソースコードはあくまでグリッドレイアウトを説明するためのものである。
  通常は :doc:`../internals/jsp_widgets` を利用して実装するので、
  上記のようなソースコードを実際に記述することはない。

------------------------
アイコンの使用
------------------------
本機能では、下記のマークアップのように、 `<i>` タグに **class** 属性値に
\ `fa`\ と、\ `fa-`\ で始まるアイコン名を指定することにより、アイコンを表示することができる。

  .. code-block:: html 

    <h3>
      <i class="fa fa-bar-chart-o"></i> 統計表示
    </h3>

なお、これらのアイコンは画像ではなくフォントとして実装されており
通常の文字と同様にサイズ、色、配置を調整することができる。
使用可能なアイコン名については、以下のサイトを参照すること。

  http://fortawesome.github.io/Font-Awesome/icons/


.. |br| raw:: html

  <br />

