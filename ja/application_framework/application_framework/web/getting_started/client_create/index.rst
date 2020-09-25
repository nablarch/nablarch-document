.. _`client_create`:

登録機能の作成(ハンズオン形式)
==========================================
Nablarchを使用したウェブアプリケーションでの登録機能の開発方法を、
Exampleアプリケーションへ顧客情報の登録機能の実装を実際に行いながら解説する。

作成する機能の説明
  1. ヘッダメニューの「顧客登録」リンクを押下する。

    .. image:: ../images/client_create/header_menu.png

  2. 顧客登録画面が表示される。

    .. image:: ../images/client_create/input_display.png

  3. 顧客名に全角文字列を入力し、業種プルダウンで任意の値を選択して「登録」ボタンを押下する。

    .. image:: ../images/client_create/input_name_select.png

  4. 登録確認画面が表示される。

    .. image:: ../images/client_create/confirm_display.png

  5. 「確定」ボタンを押下し、データベースに顧客を登録して完了画面を表示する。

    .. image:: ../images/client_create/complete_display.png

顧客登録機能の仕様
------------------------------------------
顧客登録機能の各処理と、URL及び業務アクションメソッドのマッピングを以下に示す。

.. image:: ../images/client_create/client_create.png

=== ================== ====================== ====================== ============
NO. 処理名             URL                    Action                 HTTPメソッド
=== ================== ====================== ====================== ============
1   初期表示           /action/client/        ClientAction#input     GET
2   登録内容の確認     /action/client/confirm ClientAction#confirm   POST
3   登録画面に戻る     /action/client/back    ClientAction#back      POST
4   登録処理の実行     /action/client/create  ClientAction#create    POST
=== ================== ====================== ====================== ============

利用するテーブルの定義を以下に示す。

  .. image:: ../images/client_create/client_table.png

----

登録機能の解説は以下4章で構成される。

.. toctree::
  :maxdepth: 1

  client_create1
  client_create2
  client_create3
  client_create4