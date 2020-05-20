===================================================
マルチレイアウトテーブル
===================================================
:doc:`table_row` は、行ごとに異なるカラム構成をもつテーブルである。
例えば、明細テーブルにおいて、特定のコード値のブレイク毎に小計を出力する場合や
1つのレコードに対して、複数行を出力するような場合に使用する。

.. tip::

  :doc:`table_row` は :doc:`table_plain` および :doc:`table_search_result` で使用することができる。
  :doc:`table_treelist` には対応していない。

.. tip::

  奇数行と偶数行のCSSスタイル切替え(nablarch_even/nablarch_odd)は、レコード単位で行う。
  すなわち、1つのレコードを2行で出力しているのであれば、スタイルの切替えも2行ごととなる。


コードサンプル
==================================
:doc:`table_row` を使用するには、まず :doc:`<table:plain> <table_plain>` もしくは :doc:`<table:search_result> <table_search_result>` の
`multipleRowLayout` 属性を `true` に設定する。
その上で、これらのタグの直接の子要素として `<table:row>` を配置する。

各 `<table:row>` タグの中では、通常のテーブルタグの場合と同様に `<column:xxx>` タグを使用して
行レイアウトを定義することができる。

また、 `<table:row>` の `cond` 属性値を指定することで、当該の行レイアウトを出力する条件を指定することができる。
省略した場合は全てのレコードに対して当該行を出力する。


**実装例1) 1レコードの内容を複数行で表示する例**

  **設計成果物(ローカル動作)**

  .. code-block:: jsp

    <table:plain
      title="1レコード複数行表示の記述例"
      sampleResults="4"
      multipleRowLayout="true">
      <!-- 上段の行レイアウト -->
      <table:row>
        <column:label title="ユーザID" rowspan="2" sample="001|002"></column:label>
        <column:label title="名前" sample="なまえ|なまえ２"></column:label>
        <column:label title="ポイント" sample="98090|3400"></column:label>
      </table:row>
      <!-- 下段の行レイアウト -->
      <table:row>
        <column:label title="メールアドレス" sample="001@example.com|002@example.com"></column:label>
        <column:label title="登録日" sample="2013/12/12|2014/01/05"></column:label>
      </table:row>
    </table:plain>




  **実装成果物(サーバ動作)**

  .. code-block:: jsp

    <table:plain
      title="1レコード複数行表示の記述例"
      resultSetName="result"
      sampleResults="4"
      multipleRowLayout="true">
      <!-- 上段の行レイアウト -->
      <table:row>
        <column:label key="id" title="ユーザID" rowspan="2" sample="001|002"></column:label>
        <column:label key="name" title="名前" sample="なまえ|なまえ２"></column:label>
        <column:label key="number" title="ポイント" sample="98090|3400"></column:label>
      </table:row>
      <!-- 下段の行レイアウト -->
      <table:row>
        <column:label key="mail" title="メールアドレス" sample="001@example.com|002@example.com"></column:label>
        <column:label key="date" title="登録日" sample="2013/12/12|2014/01/05"></column:label>
      </table:row>
    </table:plain>


**実装例2) 特定の位置に追加の行を表示する例**

  **設計成果物(ローカル動作)**

  .. code-block:: jsp

    <table:plain
      title="cond属性による行レイアウト制御の例"
      sampleResults="4"
      multipleRowLayout="true">
      <!-- 上段行レイアウト(レコード毎に出力) -->
      <table:row>
        <column:label title="ユーザID" sample="001|002" rowspan="2"></column:label>
        <column:label title="名前" sample="なまえ|なまえ２"></column:label>
        <column:label title="ポイント" sample="98090|3400" rowspan="2"></column:label>
      </table:row>
      <!-- 下段行レイアウト(レコード毎に出力) -->
      <table:row>
        <column:label title="メールアドレス" sample="001@example.com|002@example.com"></column:label>
      </table:row>
    </table:plain>

  **実装成果物(サーバ動作)**

  .. code-block:: jsp

    <table:plain
      title="cond属性による行レイアウト制御の例"
      resultSetName="result"
      sampleResults="4"
      multipleRowLayout="true">
      <!-- 上段行レイアウト(レコード毎に出力) -->
      <table:row>
        <column:label key="id" title="ユーザID" sample="001|002" rowspan="2"></column:label>
        <column:label key="name" title="名前" sample="なまえ|なまえ２"></column:label>
        <column:label key="number" title="ポイント" sample="98090|3400" rowspan="2"></column:label>
      </table:row>
      <!-- 下段行レイアウト(レコード毎に出力) -->
      <table:row>
        <column:label key="mail" title="メールアドレス" sample="001@example.com|002@example.com"></column:label>
      </table:row>
    </table:plain>

.. tip::

  行ごとの背景色の切替えは、表示するデータレコード毎に行われる。
  そのため、同じレコードのカラムを本機能により複数行で出力した場合、
  その背景色は同じである。

  背景色の制御は個別のCSSで行う。
  CSSでの背景色の指定方法は、table:rowのcssClass属性に任意のクラスを割り当て、
  そのクラスに対するスタイル定義にて行うことができる。

  以下に例を示す

  **table:rowの使用箇所**

  .. code-block:: jsp

    <table:row cssClass="total">
      <%-- 集計行を出力する処理 --%>
    </table:row>

  **スタイル定義**

  .. code-block:: css

    tr.total {
      background-color: #FFEEDC;
    }

仕様
=============================================

**属性値一覧**  [**◎** 必須属性 **○** 任意属性 **×** 無効(指定しても効果なし)]

========================= ================================ ============== ========== ========= ================================
名称                      内容                             タイプ         サーバ     ローカル  備考
========================= ================================ ============== ========== ========= ================================
cond                      各レコード対してこのレイアウト   真偽値         ○          ○           デフォルトは `true`
                          による行を出力するかどうか。                                           (全てのレコードについて出力)

cssClass                  行(tr要素)に適用するCSSクラス。  文字列         ○          ○

========================= ================================ ============== ========== ========= ================================


内部構造・改修時の留意点
============================================
本機能の実装は `<table:row>` ではなく `<table:plain>` および `<table:search_result>` 側にある。
このため、本機能の改修はこの2つのタグ双方に反映されるように実施するする必要がある。

**部品一覧**

============================================== ===============================================
パス                                           内容
============================================== ===============================================
/WEB-INF/tags/widget/table/plain.tag           一覧テーブルウィジェット

/WEB-INF/tags/widget/table/search_result.tag   検索結果テーブルウィジェット

/WEB-INF/tags/widget/table/row.tag             マルチレイアウトテーブル定義用ウィジェット

============================================== ===============================================



