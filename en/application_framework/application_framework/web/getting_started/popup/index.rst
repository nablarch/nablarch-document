.. _`client_popup`:

ポップアップ画面の作成
==========================================
Exampleアプリケーションを元にポップアップ画面の作成方法の解説を行う。

ポップアップ画面は、 :ref:`tag-submit_popup` に記載がある通り別ウィンドウ化ではなくダイアログ形式で作成する。

作成する機能の説明
  1. プロジェクト詳細画面の変更ボタンを押下する。

    .. image:: ../images/popup/popup-project_update_btn.png
      :scale: 80

  2. 顧客欄の検索ボタンを押下する。

    .. image:: ../images/popup/popup-project_update.png
      :scale: 75

  3. 顧客検索画面がダイアログで表示される。検索ボタンを押下する。

    .. image:: ../images/popup/popup-popup_init.png
      :scale: 60

  4. 検索結果の顧客IDのリンクを押下する。

    .. image:: ../images/popup/popup-popup_search.png
      :scale: 80

  5. 顧客検索画面が閉じられ、プロジェクト変更画面の顧客ID及び顧客名に選択した値が設定される。

    .. image:: ../images/popup/popup-complete.png
      :scale: 80

ポップアップ(ダイアログ)画面を表示する
------------------------------------------------
ポップアップ(ダイアログ)の表示はOSS(Bootstrap)を使用して実現している。
詳細は、 `Bootstrapのドキュメント(外部サイト、英語) <http://fezvrasta.github.io/bootstrap-material-design/>`_ を参照。

.. _`popup-action`:

業務アクションメソッドの作成
  顧客を検索し、選択の結果を親画面に引き渡す。
  
  本機能は、ダイアログからのAjax呼び出しにより検索処理を実現している。
  アクションクラスの実装方法については、 :ref:`restful_web_service` を参照。

.. _`popup-popup_jsp`:

ポップアップ画面のJSPの作成
  jQueryを使用して、Ajax呼び出しの結果を元にDOMを構築し結果を表示する。
  jQueryを使用しているため、詳細な解説は省略する。
  
  jQueryについては、 `ドキュメント(外部サイト、英語) <https://jquery.com/>`_ を参照。

.. _`popup-parent_hand_over`:

ポップアップ画面から親ウィンドウへ値を引き渡すJavaScript関数の作成
  jQueryを使用してダイアログ内の情報を顧客名と顧客ID部に設定する。
  jQueryを使用しているため、詳細な解説は省略する。
  
  jQueryについては、 `ドキュメント(外部サイト、英語) <https://jquery.com/>`_ を参照。
  
ポップアップ画面の解説は以上。

:ref:`Getting Started TOPページへ <getting_started>`