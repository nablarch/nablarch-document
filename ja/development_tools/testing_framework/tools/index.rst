.. _testing_framework_tools:

テスティングフレームワークの提供ツール
==================================================
この部では、テスティングフレームワークが提供する4つのツールの使い方を説明する。4つは互いに独立しており、使うツールのページだけを読めばよい。

:ref:`リクエスト単体データ作成ツール <request_data_tool>`\ と\ :ref:`HTMLチェックツール <html_check_tool>`\ は、リクエスト単体テスト（ウェブアプリケーション）が出力したHTMLダンプを入力とする。前者はテストデータのリクエストパラメータを作るために、後者は出力したHTMLの誤りを検出するために使う。

:ref:`マスタデータ投入ツール <master_data_tool>`\ は、テストデータと同じ書式で書いたマスタデータをデータベースへ投入する。\ :ref:`テストデータ変換ツール <testdata_converter>`\ は、テストデータを\ Excel\ 形式と\ YAML\ 形式の間で相互に変換する。

.. toctree::
   :maxdepth: 1

   request_data_tool
   master_data_tool
   html_check_tool
   testdata_converter
