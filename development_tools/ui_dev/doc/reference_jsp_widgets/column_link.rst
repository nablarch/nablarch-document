=============================================================
リンク表示用カラムウィジェット
=============================================================
:doc:`column_link` は、 **UI標準 UI部品 テーブル** において、
「レコード毎リンク」 として定義されているリンクを出力するウィジェットである。
:doc:`table_search_result` や、 :doc:`table_plain` 、 :doc:`table_treelist`
と組み合わせて使用し、これらのウィジェットが表示する一覧テーブルから後続処理の対象行を一行選択し、
処理を継続するための画面に遷移するリンクを出力する。


コードサンプル
==================================

**設計成果物(ローカル動作)**

  .. code-block:: jsp

    <table:search_result
      title         = "検索結果"
      sampleResults = "15">

      <column:checkbox
        title = "選択">
      </column:checkbox>

      <column:link
        title  = "ログインID"
        sample = "user001|user002|user003">
      </column:link>

    </table:search_result>


**実装成果物(サーバ動作)**

  .. code-block:: jsp

    <table:search_result
      title               = "検索結果"
      searchUri           = "/action/ss11AC/W11AC01Action/RW11AC0102"
      listSearchInfoName  = "11AC_W11AC01"
      resultSetName       = "searchResult"
      sampleResults       = "15">

      <column:checkbox
        title    = "選択"
        key      = "userId"
        name     = "W11AC05.systemAccountEntityArray[${count-1}].userId"
        offValue = "0000000000">
      </column:checkbox>

      <column:link
        title  = "ログインID"
        key    = "loginId"
        uri    = "/action/ss11AC/W11AC01Action/RW11AC0103"
        sample = "user001|user002|user003">
        <n:param paramName="11AC_W11AC01.systemAccount.userId" name="row.userId"></n:param>
      </column:link>

    </table:search_result>


仕様
=============================================

**ローカル動作時の挙動**
  カラムの内容には **sample** 属性に指定した **"|"** 区切りの文字列を順に表示する。
  (テーブルのsampleResultsに指定された件数の方が多い場合はループする。)


**属性値一覧**  [**◎** 必須属性 **○** 任意属性 **×** 無効(指定しても効果なし)]

==================== ============================== ============== ========== ========= ================================
名称                 内容                           タイプ         サーバ     ローカル  備考
==================== ============================== ============== ========== ========= ================================
key                  リンク文字列とする値を、\      文字列         ○          ×
                     行データから取得するキー

title                カラムヘッダーに表示する文字列 文字列         ◎          ◎

value                リンクテキスト文字列           文字列         ○          ○           指定されない場合は、行データ
                                                                                          から、key属性に指定した名前で
                                                                                          取得した値を利用する。

domain               データのドメイン型             文字列         ○          ○           指定されたドメイン型は、
                                                                                          リンク表示部のCSSとして
                                                                                          利用する。

cssClass             各カラムに指定するCSSクラス    文字列         ○          ○

sortable             カラムのソートリンクを表示\    文字列         ○          ○         デフォルトは'false'。
                     するかどうか                                                       :doc:`table_search_result` でのみ利用可能

uri                  リンク対象URI                  文字列         ◎          ×

inactive             リンクを非活性とするか\        真偽値         ○          ○         デフォルト値は'false'
                     どうか。
                     trueの場合にはリンクを非活\
                     性とし、ラベル表示される。

colspan              横方向に結合するカラム数       数値           ○          ○         使用方法は、\ :doc:`table_row`\を参照

rowspan              縦方向に結合するカラム数       数値           ○          ○         使用方法は、\ :doc:`table_row`\を参照


sample               テスト用のダミー表示値         文字列         ×          ○         "|" 区切りで複数指定する。

dummyUri             テスト用のダミー遷移先         文字列         ×          ○

width                カラムの横幅の指定             文字列         ○          ○         

dataFrom             表示するデータの取得元         文字列         ×          ×          画面項目定義に記載する、
                                                                                         「表示情報取得元」.「表示項目名」
                                                                                         の形式で設定する。

comment              リンクについての備考           文字列         ×          ×          設計書の表示時に、
                                                                                         画面項目定義の項目定義一覧で、
                                                                                         「備考」に表示される。

initialValueDesc     初期表示内容に関する説明       文字列         ×          ×          設計書の表示時に、
                                                                                         画面項目定義の項目定義一覧で、
                                                                                         「備考」に表示される。
==================== ============================== ============== ========== ========= ================================


内部構造・改修時の留意点
============================================

**部品一覧**

============================================== ==================================================
パス                                           内容
============================================== ==================================================
/WEB-INF/tags/widget/column/link.tag           :doc:`column_link`

/WEB-INF/tags/listSearchResult/\*.tag          Nablarch検索結果テーブルタグファイル

/js/jsp/taglib/nablarch.js                     `<n:submitLink>` のエミュレーション機能を実装する
                                               タグライブラリスタブJS

/css/style/nablarch.less                       Nablarch関連スタイル定義 |br|
                                               テーブルの配色などを定義している。

/css/style/base.less                           基本HTMLの要素のスタイル定義。|br|
                                               リンクに関する定義もここに含まれる。

============================================== ==================================================

.. |br| raw:: html

  <br />