=================================================
画像表示ウィジェット
=================================================
:doc:`box_img` は、画像を表示するウィジェットである。 |br|
表示デバイスのppiに応じて切り替えることができ、業務画面内画面内に画像を表示する場合に使用する。(共通ヘッダ内のロゴは対象外)


コードサンプル
==================================

**実装成果物(サーバ動作)**

.. code-block:: jsp

      <box:img id="imageSample"
               file="sample.png">
      </box:img>

仕様
=============================================
id属性を設定した要素を出力し、CSSのbackground-imageプロパティを使用して画像を切替、出力する。

ローカル動作とサーバ動作の挙動は同じである。

**高解像度・低解像度の位置づけ**

 * 低解像度画像 : 主に一般的なPCディスプレイ(デバイスピクセル比=1:1)で表示する画像。

 * 高解像度画像 : ratinaディスプレイ(デバイスピクセル比=2:1)などの高解像度ディスプレイをもつデバイスで表示する画像。

本ウィジェットのデフォルトの設定では、デバイスピクセル比が1.25:1より大きいデバイスでは高解像度画像、それより小さい場合は低解像度画像を使用すること。

**表示する画像ファイルパス**

本ウィジェットでは **画面の表示モード(narrow or wide)** と **解像度への対応(high or low)** の組合せで画像を切り替えることが可能である。

ひとつの画像コンテンツを表示する場合、各表示モードと解像度向けに下記の4つのパスのファイルが対応するデバイスで参照される。

 * img/wide/high

    wide,compactモードかつ高解像度で表示される画像を格納するフォルダ。

 * img/wide/low

    wide,compactモードかつ低解像度で表示される画像を格納するフォルダ。

 * img/narrow/high

    narrowモードかつ高解像度で表示される画像を格納するフォルダ。

 * img/narrow/low

    narrowモードかつ低解像度で表示される画像を格納するフォルダ。


**静的ファイルの用意**

 表示モードのディレクトリは **画面の表示モード(narrow or wide)** と **解像度への対応(high or low)** の組合せで用意する必要がある。

 リソースの切替が必要ない場合は、img/wide/high配下にファイルを配置し、img展開.batにて各ディレクトリに配置する。
 (※画像を切替えない場合は同一ファイルを表示モード領域に展開し、実質同一の画像を参照させる。)

 画像切替のリソースを高解像度向けの画像などに置き換える場合は、基点となるパス配下のファイルを上書きすればよい。


**imgファイルの展開**

 img展開.batで展開されるファイルは下記の優先順位によって展開される。
 ※基本的にファイルはimg/wide/highに配置する。

  1. 対象のフォルダにすでにファイルが存在する場合、ファイルは展開されない。

  2. 対象のフォルダに存在しない場合、同一の表示モード(wide, narrow)の高解像度画像が展開される。

  3. 同一の表示モードに存在しない場合はデフォルトとして、img/wide/highの画像が展開される。


**属性値一覧**  [**◎** 必須属性 **○** 任意属性 **×** 無効(指定しても効果なし)]

==================== ============================== ============== ========== ========= ==================================================================
名称                 内容                           タイプ         サーバ     ローカル  備考
==================== ============================== ============== ========== ========= ==================================================================
cssClass             定義領域の                     文字列         ○          ○
                     class属性を指定する。

id                   ウィジェットを定義する要素\    文字列         ◎          ◎
                     のid属性

file                 表示する画像の相対パス。       文字列         ◎          ◎         画像の切替え用ディレクトリのimg/(wide|narrow)/(high|low)/
                                                                                        からの相対パスを指定する。

==================== ============================== ============== ========== ========= ==================================================================

内部構造・改修時の留意点
============================================
当ウィジェットでは静的ファイルへのリクエストを CSS Media Query を使用して切替える。


 **参照される画像のパス**

   file属性に指定したパスは下記のようにパス解決され、タグに画像が出力される。
   画像を配置し、確認する場合は下記を参照。

   **{contextPath}/{表示モード対応ディレクトリ}/{指定したfile属性のパス}**


 **ブレークポイントや表示モードなどの拡張方法**

   | ブレークポイントや画像のURLはtemplateで指定されるstyleに依存している。
     改修する場合、基本的にtemplateを変更すればよい。
   | 画面のデバイスピクセル比の値(-webkit-min-device-pixel-ratioなど)を変更する場合、
     サポート対象のデバイスのピクセル比を確認すること。
   | templateに渡すパラメータが増える場合、tagファイルの-{placeholder名}で指定する。

 **tagとテンプレートのコード例**

   tag

   .. code-block:: none

     <div id="<n:write name='id' withHtmlFormat='false'/>"
        class="nablarch_ResponsibleImage
               -filepath    '<n:write name="file" withHtmlFormat="false" />'
               -id          '<n:write name="id" withHtmlFormat="false"/>'
               -contextPath '<n:write name="contextPath" withHtmlFormat="false"/>'"></div>


   template

   .. code-block:: html

       @media screen and (min-width: 640px) and (-webkit-min-device-pixel-ratio:1.25)
            , screen and (min-width: 640px) and (-moz-min-device-pixel-ratio:1.25)
            , screen and (min-width: 640px) and (min-resolution:120dpi) {
          #{id} > div {
             background-image : url("{contextPath}/img/wide/high/{filepath}");
          }
        }
       @media screen and (max-width: 639px) and (-webkit-min-device-pixel-ratio:1.25)
            , screen and (min-width: 639px) and (-moz-min-device-pixel-ratio:1.25)
            , screen and (max-width: 639px) and (min-resolution:120dpi) {
          #{id} > div {
             background-image : url("{contextPath}/img/narrow/high/{filepath}");
          }
       }


  .. tip::

    デフォルトの設定では、デバイスピクセル比が1:1のものを低解像度とし、それ以上のものを高解像度用の画像を表示する設定としている。

    実際の端末ではデバイスピクセル比が1.25以下のものは存在しないため、境界値を1.25としている。

    ただし、IEではresolutionの単位としてデバイスピクセル比(dppx)を使用することが出来ないため、1dppx=96dpiで換算して指定している。


**部品一覧**

+----------------------------------------------------------------+------------------------------------------------------------+
| パス                                                           | 内容                                                       |
+================================================================+============================================================+
| /WEB-INF/tags/widget/box/img.tag                               | :doc:`box_img` の実体となるタグファイル。                  |
+----------------------------------------------------------------+------------------------------------------------------------+
| /WEB-INF/include/html_head.jsp                                 | contextPathを解決する。                                    |
+----------------------------------------------------------------+------------------------------------------------------------+
| /js/ui/nablarch/ResponsibleImage.js                            | 画像のパスを解決するためのJS｡                              |
+----------------------------------------------------------------+------------------------------------------------------------+
| /js/ui/nablarch/ResponsibleImage.template                      | 背景画像のスタイルを定義するためのテンプレート｡            |
+----------------------------------------------------------------+------------------------------------------------------------+
| /js/ui/nablarch/ResponsibleImageUnsupportRatio.template        | ピクセル比が判定できないブラウザ向けのテンプレート｡        |
+----------------------------------------------------------------+------------------------------------------------------------+
| /js/ui/nablarch/ResponsibleImageUnsupportMatchMedia.template   | メディアクエリが効かない場合ブラウザ用テンプレート｡        |
+----------------------------------------------------------------+------------------------------------------------------------+
| /css/img/base.less                                             | 画像表示のless。                                           |
+----------------------------------------------------------------+------------------------------------------------------------+
| /css/img/wide.less                                             | ワイド画像指定less。                                       |
+----------------------------------------------------------------+------------------------------------------------------------+
| /css/img/narrow.les                                            | ナロー画像指定less。                                       |
+----------------------------------------------------------------+------------------------------------------------------------+
| /js/jsp/taglib/box.js                                          | :doc:`box_img` をローカルレンダリングするスタブファイル｡   |
+----------------------------------------------------------------+------------------------------------------------------------+
| /tools/img展開.bat                                             | /WEB-INF/img/配下のファイルを\                             |
|                                                                | 表示モードディレクトリに配置するためのスクリプト｡          |
+----------------------------------------------------------------+------------------------------------------------------------+
| /img/resource                                                  | 配下の画像を各表示モード対応ディレクトリに配置する。       |
+----------------------------------------------------------------+------------------------------------------------------------+
| /img/wide/high |br|                                            | 表示モード対応ディレクトリ。  |br|                         |
| /img/wide/low  |br|                                            | wide=>compact or wide表示モード向け  |br|                  |
| /img/narrow/high |br|                                          | narrow=>narrow表示モード向け  |br|                         |
| /img/narrow/low                                                | high=>高解像度向け  |br|                                   |
|                                                                | low=>PCなどの低解像度向け                                  |
+----------------------------------------------------------------+------------------------------------------------------------+

.. |br| raw:: html

  <br />