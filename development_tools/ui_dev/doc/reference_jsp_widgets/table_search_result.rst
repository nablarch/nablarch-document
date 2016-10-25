===================================================
検索結果テーブルウィジェット
===================================================
:doc:`table_search_result` はデータベースなどからの検索結果を
**UI標準 UI部品 テーブル** の内容に準拠した一覧テーブルを画面に出力するUI部品である。
:doc:`table_search_result` では :doc:`table_plain` が実装する基本機能に加え、
ページ間の移動やカラムの値に沿ったソートを行うリンクや、検索結果件数を自動的に表示することができる。


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
        title    = "ログインID"
        key      = "loginId"
        uri      = "/action/ss11AC/W11AC01Action/RW11AC0103"
        sortable = "true"
        sample   = "user001|user002|user003">
        <n:param paramName="11AC_W11AC01.systemAccount.userId" name="row.userId"></n:param>
      </column:link>

    </table:search_result>


仕様
=============================================
**ローカル動作時の挙動**
  (:doc:`table_plain` と同じ)


**属性値一覧**  [**◎** 必須属性 **○** 任意属性 **×** 無効(指定しても効果なし)]

========================= ================================ ============== ========== ========= ================================
名称                      内容                             タイプ         サーバ     ローカル  備考
========================= ================================ ============== ========== ========= ================================
title                     見出し文字列                     文字列         ◎          ◎

showTitle                 見出し文字列を表示するか否か     真偽値         ○          ○         デフォルトは 'true'

id                        テーブルを一意に識別するid       文字列         ×          ○           ページ内に、複数のテーブルが
                                                                                                 存在する場合は必須。|br|
                                                                                                 id属性は、tableをラップするdivタグに設定される。

searchUri                 検索処理を行うリクエストのURI    文字列         ○          ×           ページング及びソート機能を使用
                                                                                                 する場合は必須。
listSearchInfoName        検索条件を格納する変数名         文字列         ◎          ×

resultSetName             検索結果を格納する変数名         文字列         ○          ×         [#result]_

resultNumName             検索結果件数を格納する変数名     文字列         ○          ×         [#result]_

resultSetCss              検索結果表示領域に適用する\      文字列         ○          ○
                          CSSクラス
usePaging                 ページングを使用するか否か       真偽値         ○          ○         デフォルト="true":使用する
sampleResults             サンプルで表示する件数           数値           ×          ◎
sortCondition             テーブルの初期ソート条件         文字列         ×          ×           設計書の表示時に、
                                                                                                 画面概要の一覧表示のリストで、
                                                                                                 「ソート条件」に表示される。

multipleRowLayout         複数行レイアウト機能を有効に     真偽値         ○          ○           詳細は :doc:`table_row`
                          するかどうか。                                                         を参照。

comment                   テーブルについての備考           文字列         ×          ×           設計書の表示時に、
                                                                                                 画面概要の一覧表示のリストで、
                                                                                                 「備考」に表示される。
estimatedMaxSearchResults 検索結果として想定される最大件数 文字列         ×          ×           設計書の表示時に、
                                                                                                 画面概要の一覧表示のリストで、
                                                                                                 「想定検索最大件数」に表示
                                                                                                 される。

========================= ================================ ============== ========== ========= ================================

.. [#result]

  resultSetNameとresultNumNameはどちらか一方は必ず設定する必要がある。

内部構造・改修時の留意点
================================

(:doc:`table_plain` と同じ)

**部品一覧**

============================================== ===============================================
パス                                           内容
============================================== ===============================================
/WEB-INF/tags/widget/table/search_result.tag   検索結果テーブルウィジェット
============================================== ===============================================

以下 :doc:`table_plain` と同じ


.. |br| raw:: html

  <br />
