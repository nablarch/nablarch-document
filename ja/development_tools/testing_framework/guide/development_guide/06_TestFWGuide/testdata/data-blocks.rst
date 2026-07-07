.. _ntf_testdata_data_blocks:

====================
データブロック
====================

テストデータは Excel または YAML ファイルで記述できる。

各データブロックは **データブロック種別** と **識別子の値** の2要素で識別される。

--------------
識別の構成要素
--------------

データブロックの識別方法を以下に示す。

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - 形式
     - 記述方法
   * - Excel
     - データブロック先頭セルに ``データブロック種別=識別子の値`` と記述する。種別名で始まれば合致（前方一致）。例: ``SETUP_TABLE=USER_MASTER``
   * - YAML
     - 種別ごとの専用トップレベルキーを使用する。完全一致のため前方一致は発生しない

YAML のトップレベルキーとデータブロック種別の対応を以下に示す。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - データブロック種別
     - YAML キー
   * - ``SETUP_TABLE``
     - ``setup_tables``
   * - ``EXPECTED_TABLE``
     - ``expected_tables``
   * - ``EXPECTED_COMPLETE_TABLE``
     - ``expected_complete_tables``
   * - ``LIST_MAP``
     - ``list_maps``
   * - ``SETUP_FIXED`` / ``SETUP_VARIABLE``
     - ``setup_files``
   * - ``EXPECTED_FIXED`` / ``EXPECTED_VARIABLE``
     - ``expected_files``
   * - ``MESSAGE``
     - ``messages``
   * - ``EXPECTED_REQUEST_HEADER_MESSAGES``
     - ``expected_request_header_messages``
   * - ``EXPECTED_REQUEST_BODY_MESSAGES``
     - ``expected_request_body_messages``
   * - ``RESPONSE_HEADER_MESSAGES``
     - ``response_header_messages``
   * - ``RESPONSE_BODY_MESSAGES``
     - ``response_body_messages``

YAML での記述例を以下に示す。

.. code-block:: yaml

    setup_tables:
      - table: USER_MASTER
        rows: ...

同種データブロックの記述ルール
==============================

- **YAML**: 同一ファイル内のトップレベルキーの重複は禁止である。同種データは同一キーにリストとして並べる（重複時はエラー）。
- **Excel**: 同一シート内に同種データブロックを複数記述できる。DataType により全件収集または先着一致で収集される（下記 :ref:`ntf_testdata_data_blocks_notes` 参照）。

--------------------------
データブロック種別の一覧
--------------------------

使用できる種別は以下の14種である。

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - データブロック種別
     - 用途
     - 同一 ID が複数ある場合
   * - ``SETUP_TABLE``
     - INSERT 用テーブルデータ
     - 同じグループのものをすべて収集
   * - ``EXPECTED_TABLE``
     - 比較用テーブルデータ（省略カラムは比較対象外）
     - 同じグループのものをすべて収集
   * - ``EXPECTED_COMPLETE_TABLE``
     - 比較用テーブルデータ（省略カラムにデフォルト値補完）
     - 同じグループのものをすべて収集
   * - ``LIST_MAP``
     - キーバリュー形式の汎用データ（テストケース定義・期待値等）
     - 最初の1件のみ有効（2件目以降は無視）
   * - ``SETUP_FIXED``
     - 固定長ファイルの入力データ
     - 同じグループのものをすべて収集
   * - ``EXPECTED_FIXED``
     - 固定長ファイルの期待値データ
     - 同じグループのものをすべて収集
   * - ``SETUP_VARIABLE``
     - 可変長ファイルの入力データ
     - 同じグループのものをすべて収集
   * - ``EXPECTED_VARIABLE``
     - 可変長ファイルの期待値データ
     - 同じグループのものをすべて収集
   * - ``MESSAGE``
     - メッセージング電文データ
     - 最初の1件のみ有効（2件目以降は無視）
   * - ``EXPECTED_REQUEST_HEADER_MESSAGES``
     - 要求電文ヘッダの期待値
     - groupId 指定時は全件収集、ID 直接指定時は最初の1件
   * - ``EXPECTED_REQUEST_BODY_MESSAGES``
     - 要求電文ボディの期待値
     - groupId 指定時は全件収集、ID 直接指定時は最初の1件
   * - ``RESPONSE_HEADER_MESSAGES``
     - 応答電文ヘッダデータ
     - groupId 指定時は全件収集、ID 直接指定時は最初の1件
   * - ``RESPONSE_BODY_MESSAGES``
     - 応答電文ボディデータ
     - groupId 指定時は全件収集、ID 直接指定時は最初の1件
   * - ``DEFAULT``
     - フレームワーク内部用（通常使用しない）
     - —

.. _ntf_testdata_data_blocks_notes:

----------------------------------------------------------------------
同一ファイル（シート）内に複数のデータブロックを書く場合の注意
----------------------------------------------------------------------

- **複数テーブルの INSERT**: ``setup_tables`` などの全件収集タイプは同一 groupId のものをすべて収集する。複数テーブルデータを並べて記述できる。
- **データタイプの混在順序（YAML）**: YAML はトップレベルのセクションキー（ ``expected_tables`` / ``expected_complete_tables`` 等）ごとに独立して取得する。記述順序や異なるセクションの交互記述に関わらず正しく読み込まれる。
- **``LIST_MAP`` / ``MESSAGE`` の重複 ID**: 同一 ID が複数ある場合は最初の1件のみ有効。2件目以降は無視される。

.. note::

  **Excel との違い**: Excel（旧形式）は行を順に読む方式のため、同一シート内で別のデータタイプを挟むと後半が読み込まれない制約があった。YAML はセクションキーで構造化されるためこの制約はなく、移行時にデータタイプごとにまとめ直す必要はない。

グループの指定方法（groupId）は :ref:`ntf_testdata_testshots` を参照。
