============================================
階層(ツリー)表示テーブルウィジェット
============================================
:doc:`table_treelist` はデータベースなどからの検索結果を
**UI標準 UI部品 階層(ツリー)表示** の内容に準拠した階層テーブルを画面に出力するUI部品である。
検索結果を特定のカラムの値によって自動的にソート・階層化して表示することができるが、
仕様上、ページング機能には対応していない。

テーブル内の各カラムの内容は、カラムの種別ごとに用意された個別のウィジェットを配置することによって定義する。

- :doc:`column_label`
- :doc:`column_code`
- :doc:`column_link`
- :doc:`column_checkbox`
- :doc:`column_radio`

:doc:`column_label` については、tree_indent属性をtrueに指定することでカラム内の表示項目が階層の深さに応じて
インデントされて表示される。

なお、階層表示を利用するためには、少なくとも一つのカラムが、tree_toggler属性がtrueに指定されている
:doc:`column_link` である必要がある。

コードサンプル
==================================

**設計成果物(ローカル動作)**

  .. code-block:: jsp

    <table:treelist
      title="リクエストID一覧"
      name="treeStatus"
      key="id"
      hierarchy="chars:6|2|2"
      sampleResults="5">

      <column:label
        title="リクエストID"
        key="id"
        tree_indent="true"
        tree_toggler="true"
        sample="RW11AA|RW11AA0101|RW11AA0102|RW11AB|RW11AB0101">
      </column:label>

      <column:label
        title="リクエスト名"
        key="name"
        tree_indent="true"
        sample="ログイン機能|ログイン画面初期表示処理|ログイン処理|メニュー|メニュー表示処理">
      </column:label>

      <column:checkbox
        title="閉局中"
        name="availableRequestIds"
        key="id">
      </column:checkbox>

    </table:treelist>


**設計成果物(サーバ動作)**

  .. code-block:: jsp

    <table:treelist
      title="リクエストID一覧"
      name="formdata.treeStatus"
      key="id"
      hierarchy="chars:6|2|2"
      resultSetName="searchResult"
      sampleResults="5">

      <column:label
        title="リクエストID"
        key="id"
        tree_indent="true"
        tree_toggler="true"
        sample="RW11AA|RW11AA0101|RW11AA0102|RW11AB|RW11AB0101">
      </column:label>

      <column:label
        title="リクエスト名"
        key="name"
        tree_indent="true"
        sample="ログイン機能|ログイン画面初期表示処理|ログイン処理|メニュー|メニュー表示処理">
      </column:label>

      <column:checkbox
        title="閉局中"
        name="formdata.availableRequestIds"
        key="id">
      </column:checkbox>

    </table:treelist>

仕様
=============================================

**階層構造の定義**

検索結果は **key** 属性値に指定したカラムの値に従って、自動的にソート・階層化して表示する。
階層構造は **hirarchy** 属性値に指定した定義式によって定まり、以下の2つの書式のいずれかによって定義する。

1. chars:(数値)|(数値)|...|(数値)
   各要素のid属性値を先頭からの文字数で分割し階層を決定する方法。

2. separator:(区切り文字列)
   各要素のid属性値を区切り文字列で分割し階層を決定する方法。


**ローカル動作時の挙動**
  ローカル動作では **sampleResults** に指定した件数分だけデータ行を表示する。
  カラムの内容は各カラムウィジェットの **sample** 属性に指定した
  **"|"** 区切りの文字列を順に表示する。(レコード件数の方が多い場合はループする。)

**属性値一覧**  [**◎** 必須属性 **○** 任意属性 **×** 無効(指定しても効果なし)]

========================= ================================ ============== ========== ========= ================================
名称                      内容                             タイプ         サーバ     ローカル  備考
========================= ================================ ============== ========== ========= ================================
title                     見出し文字列                     文字列         ◎          ◎
id                        テーブルを一意に識別するid       文字列         ×          ×           ページ内に、複数のテーブルが
                                                                                                 存在する場合は必須。
name                      ツリーの開閉状態を保持する\      文字列         ◎          ◎
                          フォーム要素名
key                       階層構造を決定するレコード\      文字列         ◎          ◎
                          の属性名
hirarchy                  階層構造を決定する定義式         文字列         ◎          ◎
resultSetName             検索結果を格納する変数名         文字列         ◎          ×
resultSetCss              検索結果表示領域に適用する       文字列         ○          ○
                          CSSクラス
sampleResults             サンプルで表示する件数           数値           ×          ◎
sortCondition             テーブルの初期ソート条件         文字列         ×          ×           設計書の表示時に、
                                                                                                 画面概要の一覧表示のリストで、
                                                                                                 「ソート条件」に表示される。
comment                   テーブルについての備考           文字列         ×          ×           設計書の表示時に、
                                                                                                 画面概要の一覧表示のリストで、
                                                                                                 「備考」に表示される。
estimatedMaxSearchResults 検索結果として想定される最大件数 文字列         ×          ×           設計書の表示時に、
                                                                                                 画面概要の一覧表示のリストで、
                                                                                                 「想定検索最大件数」に表示
                                                                                                 される。

========================= ================================ ============== ========== ========= ================================


内部構造・改修時の留意点
============================================
テーブル機能は内部的に Nabalrchが提供している **<listSearchResult:table>** タグで実装されており、
Nablarch側の設定の変更によって、ページングリストの出力パターンなどを変更することができる。
詳細は、「Nablarch アーキテクチャ解説書」を参照。


**部品一覧**

============================================== ===============================================
パス                                           内容
============================================== ===============================================
/WEB-INF/tags/widget/table/treelist.tag        ツリーリストウィジェット

/WEB-INF/tags/widget/column/\*.tag             テーブルカラムウィジェット群

/WEB-INF/tags/listSearchResult/\*.tag          Nablarch検索結果テーブルタグファイル

/css/style/nablarch.less                       Nablarch関連スタイル定義
                                               テーブルの配色などを定義している。

/css/style/content.less                        業務画面領域スタイル定義
                                               テーブルサイズを定義している。

/js/nablarch/ui/TreeList.js                    ツリーリストUI部品

/css/ui/treelist.less                          ツリーリストのスタイル定義
                                               各階層ごとの配色などを定義している。

============================================== ===============================================



