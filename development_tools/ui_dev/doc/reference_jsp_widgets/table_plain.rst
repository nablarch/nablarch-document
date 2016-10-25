===================================================
一覧テーブルウィジェット
===================================================
:doc:`table_plain` は **UI標準 UI部品 テーブル** の内容に準拠した
簡素な一覧テーブルを画面に表示するUI部品である。
テーブル内の各カラムの内容は、カラムの種別ごとに用意された個別のウィジェットを配置することによって定義する。

本機能は単純な一覧テーブルを表示するためのものである。
以下に挙げる機能を必要とする場合は :doc:`table_search_result` を利用すること。

- 検索結果件数の自動表示
- ページング処理
- 各カラムの値に沿ったソート処理

なお、各カラムウィジェットの詳細については、以下を参照すること。

- :doc:`column_label`
- :doc:`column_code`
- :doc:`column_link`
- :doc:`column_checkbox`
- :doc:`column_radio`


コードサンプル
==================================

**設計成果物(ローカル動作)**

  .. code-block:: jsp

    <table:plain
      title         = "アカウント選択"
      sampleResults = "15">

      <column:checkbox
        title = "選択">
      </column:checkbox>

      <column:link
        title  = "ログインID"
        sample = "user001|user002|user003">
      </column:link>

    </table:plain>


**実装成果物(サーバ動作)**

  .. code-block:: jsp

    <table:plain
      title         = "アカウント選択"
      searchUri     = "/action/ss11AC/W11AC01Action/RW11AC0102"
      resultSetName = "searchResult"
      sampleResults = "15">

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

    </table:plain>


仕様
=============================================

**ローカル動作時の挙動**
  ローカル動作では **sampleResults** に指定した件数分だけデータ行を表示する。
  カラムの内容は各カラムウィジェットの **sample** 属性に指定した
  **"|"** 区切りの文字列を順に表示する。(レコード件数の方が多い場合はループする。)

  なお、現状では **sampleResults** の値が1ページの表示総件数を越えた場合でも
  ページ遷移リンクの表示は常に1となる。

**属性値一覧**  [**◎** 必須属性 **○** 任意属性 **×** 無効(指定しても効果なし)]

========================= ================================ ============== ========== ========= ================================
名称                      内容                             タイプ         サーバ     ローカル  備考
========================= ================================ ============== ========== ========= ================================
title                     見出し文字列                     文字列         ◎          ◎

showTitle                 見出し文字列を表示するか否か     真偽値         ○          ○         デフォルトは 'true'

id                        テーブルを一意に識別するid       文字列         ○          ○           ページ内に、複数のテーブルが
                                                                                                 存在する場合は必須。|br|
                                                                                                 id属性は、tableをラップするdivタグに設定される。

resultSetName             検索結果を格納する変数名         文字列         ○          ×         [#result]_

resultNumName             検索結果件数を格納する変数名     文字列         ○          ×         [#result]_

resultSetCss              検索結果表示領域に適用する\      文字列         ○          ○
                          CSSクラス
sampleResults             サンプルで表示する件数           数値           ×          ◎

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
============================================
テーブル機能は内部的に Nabalrchが提供している **<listSearchResult:table>** タグで実装されており、
Nablarch側の設定の変更によって、ページングリストの出力パターンなどを変更することができる。
詳細は、「Nablarch アーキテクチャ解説書」を参照。


**部品一覧**

============================================== ===============================================
パス                                           内容
============================================== ===============================================
/WEB-INF/tags/widget/table/plain.tag           一覧テーブルウィジェット

/WEB-INF/tags/widget/column/\*.tag             テーブルカラムウィジェット群

/WEB-INF/tags/listSearchResult/\*.tag          Nablarch検索結果テーブルタグファイル

/css/style/nablarch.less                       Nablarch関連スタイル定義
                                               テーブルの配色などを定義している。

/css/style/content.less                        業務画面領域スタイル定義
                                               テーブルサイズを定義している。

============================================== ===============================================



.. |br| raw:: html

  <br />