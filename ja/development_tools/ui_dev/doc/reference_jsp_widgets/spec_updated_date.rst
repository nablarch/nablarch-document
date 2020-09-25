===================================================
設計書更新日付情報ウィジェット
===================================================
:doc:`spec_updated_date` は当該画面の更新日付の情報を記述するタグである。

本タグの内容は、設計書ビューのヘッダー部分の「変更」欄に表示される。

.. tip::

  この部品はJSPのサーバ表示の内容には一切影響しない。
  実装工程以降も削除する必要はない。


コードサンプル
==================================

  .. code-block:: jsp

    <spec:author>TIS 田嶋 岩魚</spec:author>
    <spec:updated_by>TIS 名部 楽太郎</spec:updated_by>
    <spec:created_date>2014/01/04</spec:created_date>
    <spec:updated_date>2014/01/08</spec:updated_date>


仕様
=============================================
本タグに属性値は定義されていない。
ボディ部に設定された文字列を設計書ビューの変更欄にそのまま表示する。


内部構造・改修時の留意点
============================================
サーバ表示で動作するタグファイル(updated_date.tag) は、JSPコンパイルを通すためだけの
空ファイルである。

設計書ビューはテンプレートファイルである SpecSheetTemplate.xlsx と、
各項目の表示内容を制御する SpecSheetInterpreter.js によって構成される。

**部品一覧**

================================================== ===============================================
パス                                               内容
================================================== ===============================================
/WEB-INF/tags/widget/spec/updated_date.tag         :doc:`spec_updated_date` のタグファイル

/js/jsp/taglib/spec.js                             ローカル表示用スタブ

/js/devtool/SpecSheetView.js                       設計書ビューJavaScriptUI部品

/js/devtool/SpecSheetInterpreter.js                設計書ビュー表示内容制御スクリプト

/tools/specsheet_template/SpecSheetTemplate.xlsx   設計書ビューテンプレートファイル

/tools/specsheet_template/SpecSheetTemplate.files  設計書ビューテンプレートファイル
                                                   (上記ファイルをHTML形式で保存したもの)

================================================== ===============================================
  
  

