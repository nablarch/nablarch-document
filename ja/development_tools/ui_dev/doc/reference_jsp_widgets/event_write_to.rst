===================================================
項目内容変更イベントアクション
===================================================
:doc:`event_write_to` は :doc:`event_listen` 及び :doc:`event_listen_subwindow`
が監視するイベントが発生した際に、特定の要素の内容(表示文字列もしくは入力値)を
動的に書き換えるイベントアクションである。

コードサンプル
==================================
以下のソースコードは、画面内のAjaxリクエストの完了時に、
そのレスポンスの内容を使って画面内の特定項目を書き換える例である。


  .. code-block:: jsp

    <event:listen
      title = "Ajaxリクエスト成功時の処理"
      event = "ajaxSuccess">
      <event:write_to
        title     = "レスポンスボディのテーブル中のユーザIDの値を入力欄に設定する。"
        target    = "input.user_id"
        condition = ":has(tr td)"
        format    = "{td.user_id:first}">
      </event:write_to>
    </event:listen>


仕様
=============================================
このアクションを実行するイベントは :doc:`event_listen`
(もしくは :doc:`event_listen_subwindow` ) を用いて定義する必要がある。

このアクションが実行されると、まず、イベントの発生元要素が `condition` 属性の
セレクタにマッチするかをチェックし、マッチしなかった場合はなにもしない。

マッチした場合、このタグと同じ `<event:listen>` タグ内に存在し、
`target` 属性のセレクタにマッチする全ての要素の内容を `format` 属性の内容に書き換える。

具体的には、対象要素が入力項目(input/select/textarea)であった場合は、そのvalue属性に設定し、
それ以外の要素の場合は、テキストノードの内容を書き換える。


**属性値一覧**  [**◎** 必須属性 **○** 任意属性 **×** 無効(指定しても効果なし)]

========================= ================================ ============== ========== ========= ===========================================================
名称                      内容                             タイプ         サーバ     ローカル  備考
========================= ================================ ============== ========== ========= ===========================================================
title                     実行する処理の簡単な説明         文字列         ×          ×         設計書表示用

target                    値を書き換える要素を指定する     文字列         ◎          ◎
                          セレクタ式

format                    targetで指定した要素に設定する   文字列         ○          ○         埋め込み文字{}内にセレクタを指定することで、|br|
                          値を定めるフォーマット式 |br|                                        その要素の内容を埋め込むことができる。|br|
                          省略時した場合は値の設定                                             **記述例**
                          自体が行われない。                                                     
                                                                                                   ユーザID: {span.prefix}-{span.code}

condition                 本アクションを実行する事前条件。 文字列         ○          ○
                          イベント発生元要素が満た |br|
                          すべきセレクタ式の形式で指定
                          する。

addClass                  targetで指定した要素に追加する   文字列         ○          ○         空白区切りで複数のclass名を指定できる。
                          class属性値。

removeClass               targetで指定した要素から除去する 文字列         ○          ○         空白区切りで複数のclass名を指定できる。
                          class属性値。

========================= ================================ ============== ========== ========= ===========================================================



内部構造・改修時の留意点
============================================
本ウィジェットは以下のファイルによって実装されている。

**部品一覧**

================================================= =====================================================
パス                                              内容
================================================= =====================================================
/WEB-INF/tags/widget/event/write_to.tag           このウィジェットの実体となるタグファイル

/js/nablarch/ui/event/WriteAction.js              本機能を実装するイベントアクション

================================================= =====================================================

.. |br| raw:: html

  <br />