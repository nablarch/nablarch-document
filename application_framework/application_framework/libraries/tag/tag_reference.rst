.. _tag_reference:

==================================================
タグリファレンス
==================================================

フォーム
 | :ref:`tag-form_tag` (フォーム)

.. _tag_reference_input:

入力
 | :ref:`tag-text_tag` (テキスト)
 | :ref:`tag-textarea_tag` (テキストエリア)
 | :ref:`tag-password_tag` (パスワード)
 | :ref:`tag-radio_tag` (ラジオボタン)
 | :ref:`tag-checkbox_tag` (チェックボックス)
 | :ref:`tag-file_tag` (ファイル)
 | :ref:`tag-plain_hidden_tag` (hidden)
 | :ref:`tag-select_tag` (プルダウン)
 | :ref:`tag-composite_key_radio_button_tag` (複合キーに対応したラジオボタン)
 | :ref:`tag-composite_key_checkbox_tag` (複合キーに対応したチェックボックス)
 | :ref:`tag-radio_buttons_tag` (複数のラジオボタン)
 | :ref:`tag-checkboxes_tag` (複数のチェックボックス)
 | :ref:`tag-code_select_tag` (コード値のプルダウン)
 | :ref:`tag-code_checkbox_tag` (コード値のチェックボックス)
 | :ref:`tag-code_radio_buttons_tag` (コード値の複数のラジオボタン)
 | :ref:`tag-code_checkboxes_tag` (コード値の複数のチェックボッス)
 | :ref:`tag-hidden_tag` (hidden暗号化)
 | :ref:`tag-hidden_store_tag` (HIDDENストア)

.. _tag_reference_submit:

サブミット
 フォームのサブミット
  | :ref:`tag-submit_tag` (inputタグのボタン)
  | :ref:`tag-button_tag` (buttonタグのボタン)
  | :ref:`tag-submit_link_tag` (リンク)

 別ウィンドウを開いてサブミット(ポップアップ)
  | :ref:`tag-popup_submit_tag` (inputタグのボタン)
  | :ref:`tag-popup_button_tag` (buttonタグのボタン)
  | :ref:`tag-popup_link_tag` (リンク)

 ダウンロード用のサブミット
  | :ref:`tag-download_submit_tag` (inputタグのボタン)
  | :ref:`tag-download_button_tag` (buttonタグのボタン)
  | :ref:`tag-download_link_tag` (リンク)

 サブミット制御
  | :ref:`tag-param_tag` (サブミット時に追加するパラメータの指定)
  | :ref:`tag-change_param_name_tag` (ポップアップ用のサブミット時にパラメータ名の変更)

.. _tag_reference_output:

出力
 値
  | :ref:`tag-write_tag` (オブジェクトの値)
  | :ref:`tag-pretty_print_tag` (オブジェクトの値。修飾系のHTML(bタグなど)のみエスケープしない)
  | :ref:`tag-raw_write_tag` (オブジェクトの値。HTMLエスケープしない)
  | :ref:`tag-code_tag` (コード値)
 メッセージ
  | :ref:`tag-message_tag` (メッセージ)
 エラー
  | :ref:`tag-errors_tag` (エラーメッセージの一覧表示)
  | :ref:`tag-error_tag` (エラーメッセージの個別表示)

URIを指定するHTMLタグ(コンテキストパスの付加とURLリライト)
 | :ref:`tag-a_tag`
 | :ref:`tag-img_tag`
 | :ref:`tag-link_tag`
 | :ref:`tag-script_tag`

ユーティリティ
 | :ref:`tag-no_cache_tag` (ブラウザのキャッシュを抑制する)
 | :ref:`tag-set_tag` (変数に値を設定する)
 | :ref:`tag-include_tag` (インクルード)
 | :ref:`tag-include_param_tag` (インクルード時に追加するパラメータの指定)
 | :ref:`tag-confirmation_page_tag` (入力画面と確認画面を共通化)
 | :ref:`tag-ignore_confirmation_tag` (部分的に確認画面の画面状態を無効化する)
 | :ref:`tag-for_input_page_tag` (入力画面のみボディを出力)
 | :ref:`tag-for_confirmation_page_tag` (確認画面のみボディを出力)

共通属性
========================
各カスタムタグの定義でここで定義した共通属性を参照する。

.. _tag-generic_attributes_tag:

全てのHTMLタグ
-------------------------

.. table::
   :class: tag-reference

   ============================= ==========================================================================================
   属性                          説明
   ============================= ==========================================================================================
   id                            XHTMLのid属性。
   cssClass                      XHTMLのclass属性。
   style                         XHTMLのstyle属性。
   title                         XHTMLのtitle属性。
   lang                          XHTMLのlang属性。
   xmlLang                       XHTMLのxml:lang属性。
   dir                           XHTMLのdir属性。
   onclick                       XHTMLのonclick属性。
   ondblclick                    XHTMLのondblclick属性。
   onmousedown                   XHTMLのonmousedown属性。
   onmouseup                     XHTMLのonmouseup属性。
   onmouseover                   XHTMLのonmouseover属性。
   onmousemove                   XHTMLのonmousemove属性。
   onmouseout                    XHTMLのonmouseout属性。
   onkeypress                    XHTMLのonkeypress属性。
   onkeydown                     XHTMLのonkeydown属性。
   onkeyup                       XHTMLのonkeyup属性。
   ============================= ==========================================================================================

.. _tag-focus_attributes_tag:

フォーカスを取得可能なHTMLタグ
--------------------------------------------------

.. table::
   :class: tag-reference

   ============================= ==========================================================================================
   属性                          説明
   ============================= ==========================================================================================
   accesskey                     XHTMLのaccesskey属性。
   tabindex                      XHTMLのtabindex属性。
   onfocus                       XHTMLのonfocus属性。
   onblur                        XHTMLのonblur属性。
   ============================= ==========================================================================================

個別属性
======================================================

.. _tag-form_tag:

formタグ
-------------------------

.. table::
   :class: tag-reference
      
   ====================================== ==========================================================================================
   属性                                     説明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`      
   name                                   XHTMLのname属性。
   action                                 XHTMLのaction属性。
   method                                 XHTMLのmethod属性。
                                          デフォルトは ``post`` 。
   enctype                                XHTMLのenctype属性。
   onsubmit                               XHTMLのonsubmit属性。
   onreset                                XHTMLのonreset属性。
   accept                                 XHTMLのaccept属性。
   acceptCharset                          XHTMLのaccept-charset属性。
   target                                 XHTMLのtarget属性。
   autocomplete                           HTML5のautocomplete属性。
   windowScopePrefixes                    ウィンドウスコープ変数のプレフィックス。
                                          複数指定する場合はカンマ区切り。
                                          指定されたプレフィックスがマッチするリクエストパラメータをhiddenタグとして出力する。
   useToken                               トークンを設定するか否か。
                                          トークンを設定する場合は ``true`` 、設定しない場合は ``false`` 。
                                          デフォルトは ``false`` 。
                                          :ref:`tag-confirmation_page_tag` が指定された場合は、デフォルトが ``true`` となる。
   secure                                 URIをhttpsにするか否か。
                                          httpsにする場合は ``true`` 、しない場合は ``false`` 。
   preventPostResubmit                    POST再送信防止機能を使用するか否か。
                                          デフォルトは ``false`` 。
                                          使用する場合は ``true`` 、しない場合は ``false`` 。
   ====================================== ==========================================================================================

.. _tag-text_tag:

textタグ
-------------------------

.. table::
   :class: tag-reference
      
   ====================================== ====================================================================================================================
   属性                                   説明
   ====================================== ====================================================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必須``                          XHTMLのname属性。
   disabled                               XHTMLのdisabled属性。
   readonly                               XHTMLのreadonly属性。
   size                                   XHTMLのsize属性。
   maxlength                              XHTMLのmaxlength属性。
   onselect                               XHTMLのonselect属性。
   onchange                               XHTMLのonchange属性。
   autocomplete                           HTML5のautocomplete属性。
   autofocus                              HTML5のautofocus属性。
   placeholder                            HTML5のplaceholder属性。
   errorCss                               エラーレベルのメッセージに使用するCSSクラス名。
                                          デフォルトは ``nablarch_error`` 。
   nameAlias                              name属性のエイリアスを設定する。
                                          複数指定する場合はカンマ区切り。
   valueFormat                            出力時のフォーマット。
                                          指定内容は、 :ref:`tag-format_value` を参照。
   ====================================== ====================================================================================================================

.. _tag-textarea_tag:

textareaタグ
-------------------------

.. table::
   :class: tag-reference
         
   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必須``                          XHTMLのname属性。
   rows ``必須``                          XHTMLのrows属性。
   cols ``必須``                          XHTMLのcols属性。
   disabled                               XHTMLのdisabled属性。
   readonly                               XHTMLのreadonly属性。
   onselect                               XHTMLのonselect属性。
   onchange                               XHTMLのonchange属性。
   autofocus                              HTML5のautofocus属性。
   placeholder                            HTML5のplaceholder属性。
   maxlength                              HTML5のmaxlength属性。
   errorCss                               エラーレベルのメッセージに使用するCSSクラス名。
                                          デフォルトは ``nablarch_error`` 。
   nameAlias                              name属性のエイリアスを設定する。
                                          複数指定する場合はカンマ区切り。
   ====================================== ==========================================================================================

.. _tag-password_tag:

passwordタグ
-------------------------

.. table::
   :class: tag-reference
            
   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必須``                          XHTMLのname属性。
   disabled                               XHTMLのdisabled属性。
   readonly                               XHTMLのreadonly属性。
   size                                   XHTMLのsize属性。
   maxlength                              XHTMLのmaxlength属性。
   onselect                               XHTMLのonselect属性。
   onchange                               XHTMLのonchange属性。
   autocomplete                           HTML5のautocomplete属性。
   autofocus                              HTML5のautofocus属性。
   placeholder                            HTML5のplaceholder属性。
   restoreValue                           入力画面の再表示時に入力データを復元するか否か。
                                          復元する場合は ``true`` 、復元しない場合は ``false`` 。
                                          デフォルトは ``false`` 。
   replacement                            確認画面用の出力時に使用する置換文字。
                                          デフォルトは ``*`` 。
   errorCss                               エラーレベルのメッセージに使用するCSSクラス名。
                                          デフォルトは ``nablarch_error`` 。
   nameAlias                              name属性のエイリアスを設定する。
                                          複数指定する場合はカンマ区切り。
   ====================================== ==========================================================================================

.. _tag-radio_tag:

radioButtonタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`
   :ref:`tag-focus_attributes_tag`
   name ``必須``                          XHTMLのname属性。
   value ``必須``                         XHTMLのvalue属性。
   label ``必須``                         ラベル。
   disabled                               XHTMLのdisabled属性。
   onchange                               XHTMLのonchange属性。
   autofocus                              HTML5のautofocus属性。
   errorCss                               エラーレベルのメッセージに使用するCSSクラス名。
                                          デフォルトは ``nablarch_error`` 。
   nameAlias                              name属性のエイリアスを設定する。
                                          複数指定する場合はカンマ区切り。
   ====================================== ==========================================================================================

.. _tag-checkbox_tag:

checkboxタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必須``                          XHTMLのname属性。
   value                                  XHTMLのvalue属性。
                                          チェックありの場合に使用する値。
                                          デフォルトは ``1`` 。
   autofocus                              HTML5のautofocus属性。
   label                                  チェックありの場合に使用するラベル。
                                          入力画面では、このラベルが表示される。
   useOffValue                            チェックなしの値設定を使用するか否か。
                                          デフォルトは ``true`` 。
   offLabel                               チェックなしの場合に使用するラベル。
   offValue                               チェックなしの場合に使用する値。
                                          デフォルトは ``0`` 。
   disabled                               XHTMLのdisabled属性。
   onchange                               XHTMLのonchange属性。
   errorCss                               エラーレベルのメッセージに使用するCSSクラス名。
                                          デフォルトは ``nablarch_error`` 。
   nameAlias                              name属性のエイリアスを設定する。
                                          複数指定する場合はカンマ区切り。
   ====================================== ==========================================================================================
 
.. _tag-composite_key_checkbox_tag:

compositeKeyCheckboxタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必須``                          XHTMLのname属性。
   valueObject ``必須``                   XHTMLのvalue属性の代わりに使用するオブジェクト。
                                          keyNames属性で指定したプロパティを持つ必要がある。
   keyNames ``必須``                      複合キーのキー名。
                                          キー名をカンマ区切りで指定する。
   namePrefix ``必須``                    リクエストパラメータに展開する際に使用するプレフィクス。
                                          通常のname属性と異なり、この名称に ``.`` と\
                                          keyNames属性で指定したキー名と合致する値を通常のname属性と同様に取り扱う。
                                          例えばnamePrefix属性に ``form`` 、keyNames属性に ``key1`` 、 ``key2`` を指定した場合、\
                                          表示時には ``form.key1`` 、 ``form.key2`` で\
                                          リクエストスコープに含まれる値を使用してこのチェックボックスの値を出力する。
                                          また、サブミットしたリクエストの処理では、\
                                          ``form.key1`` 、 ``form.key2`` というリクエストパラメータから選択された値が取得できる。
                                          なお、name属性は、namePrefix属性とkeyNames属性で指定した\
                                          キーの組み合わせと異なる名称にしなければならない特殊な制約がある。\
                                          実装時はこの点に十分注意すること。
   autofocus                              HTML5のautofocus属性。
   label                                  チェックありの場合に使用するラベル。
                                          入力画面では、このラベルが表示される。
   disabled                               XHTMLのdisabled属性。
   onchange                               XHTMLのonchange属性。
   errorCss                               エラーレベルのメッセージに使用するCSSクラス名。
                                          デフォルトは ``nablarch_error`` 。
   nameAlias                              name属性のエイリアスを設定する。
                                          複数指定する場合はカンマ区切り。
   ====================================== ==========================================================================================

.. _tag-composite_key_radio_button_tag:

compositeKeyRadioButtonタグ
---------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必須``                          XHTMLのname属性。
   valueObject ``必須``                   XHTMLのvalue属性の代わりに使用するオブジェクト。
                                          keyNames属性で指定したプロパティを持つ必要がある。
   keyNames ``必須``                      複合キーのキー名。
                                          キー名をカンマ区切りで指定する。
   namePrefix ``必須``                    リクエストパラメータに展開する際に使用するプレフィクス。
                                          通常のname属性と異なり、この名称に ``.`` と\
                                          keyNames属性で指定したキー名と合致する値を通常のname属性と同様に取り扱う。
                                          例えばnamePrefix属性に ``form`` 、keyNames属性に ``key1`` 、 ``key2`` を指定した場合、\
                                          表示時には ``form.key1`` 、 ``form.key2`` で\
                                          リクエストスコープに含まれる値を使用してこのチェックボックスの値を出力する。
                                          また、サブミットしたリクエストの処理では、\
                                          ``form.key1`` 、 ``form.key2`` というリクエストパラメータから選択された値が取得できる。
                                          なお、name属性は、namePrefix属性とkeyNames属性で指定した\
                                          キーの組み合わせと異なる名称にしなければならない特殊な制約がある。\
                                          実装時はこの点に十分注意すること。
   autofocus                              HTML5のautofocus属性。
   label                                  チェックありの場合に使用するラベル。
                                          入力画面では、このラベルが表示される。
   disabled                               XHTMLのdisabled属性。
   onchange                               XHTMLのonchange属性。
   errorCss                               エラーレベルのメッセージに使用するCSSクラス名。
                                          デフォルトは ``nablarch_error`` 。
   nameAlias                              name属性のエイリアスを設定する。
                                          複数指定する場合はカンマ区切り。
   ====================================== ==========================================================================================

.. _tag-file_tag:

fileタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必須``                          XHTMLのname属性。
   disabled                               XHTMLのdisabled属性。
   readonly                               XHTMLのreadonly属性。
   size                                   XHTMLのsize属性。
   maxlength                              XHTMLのmaxlength属性。
   onselect                               XHTMLのonselect属性。
   onchange                               XHTMLのonchange属性。
   accept                                 XHTMLのaccept属性。
   autofocus                              HTML5のautofocus属性。
   multiple                               HTML5のmultiple属性。
   errorCss                               エラーレベルのメッセージに使用するCSSクラス名。
                                          デフォルトは ``nablarch_error`` 。
   nameAlias                              name属性のエイリアスを設定する。
                                          複数指定する場合はカンマ区切り。
   ====================================== ==========================================================================================

.. _tag-hidden_tag:

hiddenタグ
-------------------------
HTMLタグの出力を行わず、ウィンドウスコープに値を出力する。

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必須``                          XHTMLのname属性。
   disabled                               XHTMLのdisabled属性。
   ====================================== ==========================================================================================

.. _tag-plain_hidden_tag:

plainHiddenタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必須``                          XHTMLのname属性。
   disabled                               XHTMLのdisabled属性。
   ====================================== ==========================================================================================

.. _tag-hidden_store_tag:

hiddenStoreタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`
   :ref:`tag-focus_attributes_tag`
   name ``必須``                          XHTMLのname属性。
   disabled                               XHTMLのdisabled属性。
   ====================================== ==========================================================================================

.. _tag-select_tag:

selectタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ======================================================================================================================
   属性                                   説明
   ====================================== ======================================================================================================================
   :ref:`tag-generic_attributes_tag`    
   name ``必須``                          XHTMLのname属性。
   listName ``必須``                      選択肢リストの名前。
                                          カスタムタグはこの名前を使用してリクエストスコープから選択肢リストを取得する。
   elementLabelProperty ``必須``          リスト要素からラベルを取得するためのプロパティ名。
   elementValueProperty ``必須``          リスト要素から値を取得するためのプロパティ名。
   size                                   XHTMLのsize属性。
   multiple                               XHTMLのmultiple属性。
   disabled                               XHTMLのdisabled属性。
   tabindex                               XHTMLのtabindex属性。
   onfocus                                XHTMLのonfocus属性。
   onblur                                 XHTMLのonblur属性。
   onchange                               XHTMLのonchange属性。
   autofocus                              HTML5のautofocus属性。
   elementLabelPattern                    ラベルを整形するためのパターン。
                                          プレースホルダを下記に示す。
                                          ``$LABEL$`` : ラベル
                                          ``$VALUE$`` : 値
                                          デフォルトは ``$LABEL$`` 。
   listFormat                             リスト表示時に使用するフォーマット。
                                          下記のいずれかを指定する。
                                          br(brタグ)
                                          div(divタグ)
                                          span(spanタグ)
                                          ul(ulタグ)
                                          ol(olタグ)
                                          sp(スペース区切り)
                                          デフォルトはbr。
   withNoneOption                         リスト先頭に選択なしのオプションを追加するか否か。
                                          追加する場合は ``true`` 、追加しない場合は ``false`` 。
                                          デフォルトは ``false`` 。
   noneOptionLabel                        リスト先頭に選択なしのオプションを追加する場合に使用するラベル。
                                          この属性は、withNoneOptionに ``true`` を指定した場合のみ有効となる。
                                          デフォルトは ``""``。
   errorCss                               エラーレベルのメッセージに使用するCSSクラス名。
                                          デフォルトは ``nablarch_error`` 。
   nameAlias                              name属性のエイリアスを設定する。
                                          複数指定する場合はカンマ区切り。
   ====================================== ======================================================================================================================

.. _tag-radio_buttons_tag:

radioButtonsタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ======================================================================================================================
   属性                                   説明
   ====================================== ======================================================================================================================
   :ref:`tag-generic_attributes_tag`      id属性は指定不可。
   :ref:`tag-focus_attributes_tag`        accesskey属性は指定不可。
   name ``必須``                          XHTMLのname属性。
   listName ``必須``                      選択肢リストの名前。
                                          カスタムタグはこの名前を使用してリクエストスコープから選択肢リストを取得する。
   elementLabelProperty ``必須``          リスト要素からラベルを取得するためのプロパティ名。
   elementValueProperty ``必須``          リスト要素から値を取得するためのプロパティ名。
   disabled                               XHTMLのdisabled属性。
   onchange                               XHTMLのonchange属性。
   autofocus                              HTML5のautofocus属性。
                                          選択肢のうち、先頭要素のみautofocus属性を出力する。
   elementLabelPattern                    ラベルを整形するためのパターン。
                                          プレースホルダを下記に示す。
                                          ``$LABEL$`` : ラベル
                                          ``$VALUE$`` : 値
                                          デフォルトは ``$LABEL$`` 。
   listFormat                             リスト表示時に使用するフォーマット。
                                          下記のいずれかを指定する。
                                          br(brタグ)
                                          div(divタグ)
                                          span(spanタグ)
                                          ul(ulタグ)
                                          ol(olタグ)
                                          sp(スペース区切り)
                                          デフォルトはbr。
   errorCss                               エラーレベルのメッセージに使用するCSSクラス名。
                                          デフォルトは ``nablarch_error`` 。
   nameAlias                              name属性のエイリアスを設定する。
                                          複数指定する場合はカンマ区切り。
   ====================================== ======================================================================================================================

.. _tag-checkboxes_tag:

checkboxesタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`      id属性は指定不可。
   :ref:`tag-focus_attributes_tag`        accesskey属性は指定不可。
   name ``必須``                          XHTMLのname属性。
   listName ``必須``                      選択肢リストの名前。
                                          カスタムタグはこの名前を使用してリクエストスコープから選択肢リストを取得する。
   elementLabelProperty ``必須``          リスト要素からラベルを取得するためのプロパティ名。
   elementValueProperty ``必須``          リスト要素から値を取得するためのプロパティ名。
   disabled                               XHTMLのdisabled属性。
   onchange                               XHTMLのonchange属性。
   autofocus                              HTML5のautofocus属性。
                                          選択肢のうち、先頭要素のみautofocus属性を出力する。
   elementLabelPattern                    ラベルを整形するためのパターン。
                                          プレースホルダを下記に示す。
                                          ``$LABEL$`` : ラベル
                                          ``$VALUE$`` : 値
                                          デフォルトは ``$LABEL$`` 。
   listFormat                             リスト表示時に使用するフォーマット。
                                          下記のいずれかを指定する。
                                          br(brタグ)
                                          div(divタグ)
                                          span(spanタグ)
                                          ul(ulタグ)
                                          ol(olタグ)
                                          sp(スペース区切り)
                                          デフォルトはbr。
   errorCss                               エラーレベルのメッセージに使用するCSSクラス名。
                                          デフォルトは ``nablarch_error`` 。
   nameAlias                              name属性のエイリアスを設定する。
                                          複数指定する場合はカンマ区切り。
   ====================================== ==========================================================================================

.. _tag-submit_tag:

submitタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name                                   XHTMLのname属性。
   type ``必須``                          XHTMLのtype属性。
   uri ``必須``                           URI。
                                          :ref:`tag-specify_uri` を参照。
   disabled                               XHTMLのdisabled属性。
   value                                  XHTMLのvalue属性。
   src                                    XHTMLのsrc属性。
   alt                                    XHTMLのalt属性。
   usemap                                 XHTMLのusemap属性。
   align                                  XHTMLのalign属性。
   autofocus                              HTML5のautofocus属性。
   allowDoubleSubmission                  二重サブミットを許可するか否か。
                                          許可する場合は ``true`` 、許可しない場合は ``false`` 。
                                          デフォルトは ``true`` 。
   secure                                 URIをhttpsにするか否か。
                                          httpsにする場合は ``true`` 、しない場合は ``false`` 。
   displayMethod                          認可判定とサービス提供可否判定の結果に応じて表示制御を行う場合の表示方法。
                                          下記のいずれかを指定する。
                                          NODISPLAY (非表示)
                                          DISABLED (非活性)
                                          NORMAL (通常表示)
   ====================================== ==========================================================================================

.. _tag-button_tag:

buttonタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name                                   XHTMLのname属性。
   uri ``必須``                           URI。
                                          :ref:`tag-specify_uri` を参照。
   value                                  XHTMLのvalue属性。
   type                                   XHTMLのtype属性。
   disabled                               XHTMLのdisabled属性。
   autofocus                              HTML5のautofocus属性。
   allowDoubleSubmission                  二重サブミットを許可するか否か。
                                          許可する場合は ``true`` 、許可しない場合は ``false`` 。
                                          デフォルトは ``true`` 。
   secure                                 URIをhttpsにするか否か。
                                          httpsにする場合は ``true`` 、しない場合は ``false`` 。
   displayMethod                          認可判定とサービス提供可否判定の結果に応じて表示制御を行う場合の表示方法。
                                          下記のいずれかを指定する。
                                          NODISPLAY (非表示)
                                          DISABLED (非活性)
                                          NORMAL (通常表示)
   ====================================== ==========================================================================================

.. _tag-submit_link_tag:

submitLinkタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name                                   XHTMLのname属性。
   uri ``必須``                           URI。
                                          :ref:`tag-specify_uri` を参照。
   shape                                  XHTMLのshape属性。
   coords                                 XHTMLのcoords属性。
   allowDoubleSubmission                  二重サブミットを許可するか否か。
                                          許可する場合は ``true`` 、許可しない場合は ``false`` 。
                                          デフォルトは ``true`` 。
   secure                                 URIをhttpsにするか否か。
                                          httpsにする場合は ``true`` 、しない場合は ``false`` 。
   displayMethod                          認可判定とサービス提供可否判定の結果に応じて表示制御を行う場合の表示方法。
                                          下記のいずれかを指定する。
                                          NODISPLAY (非表示)
                                          DISABLED (非活性)
                                          NORMAL (通常表示)
   ====================================== ==========================================================================================

.. _tag-popup_submit_tag:

popupSubmitタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name                                   XHTMLのname属性。
   type ``必須``                          XHTMLのtype属性。
   uri ``必須``                           URI。
                                          :ref:`tag-specify_uri` を参照。
   disabled                               XHTMLのdisabled属性。
   value                                  XHTMLのvalue属性。
   src                                    XHTMLのsrc属性。
   alt                                    XHTMLのalt属性。
   usemap                                 XHTMLのusemap属性。
   align                                  XHTMLのalign属性。
   autofocus                              HTML5のautofocus属性。
   secure                                 URIをhttpsにするか否か。
                                          httpsにする場合は ``true`` 、しない場合は ``false`` 。
   popupWindowName                        ポップアップのウィンドウ名。
                                          新しいウィンドウを開く際にwindow.open関数の第2引数(JavaScript)に指定する。
   popupOption                            ポップアップのオプション情報。
                                          新しいウィンドウを開く際にwindow.open関数の第3引数(JavaScript)に指定する。
   displayMethod                          認可判定とサービス提供可否判定の結果に応じて表示制御を行う場合の表示方法。
                                          下記のいずれかを指定する。
                                          NODISPLAY (非表示)
                                          DISABLED (非活性)
                                          NORMAL (通常表示)
   ====================================== ==========================================================================================

.. _tag-popup_button_tag:

popupButtonタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name                                   XHTMLのname属性。
   uri ``必須``                           URI。
                                          :ref:`tag-specify_uri` を参照。
   value                                  XHTMLのvalue属性。
   type                                   XHTMLのtype属性。
   disabled                               XHTMLのdisabled属性。
   autofocus                              HTML5のautofocus属性。
   secure                                 URIをhttpsにするか否か。
                                          httpsにする場合は ``true`` 、しない場合は ``false`` 。
   popupWindowName                        ポップアップのウィンドウ名。
                                          新しいウィンドウを開く際にwindow.open関数の第2引数(JavaScript)に指定する。
   popupOption                            ポップアップのオプション情報。
                                          新しいウィンドウを開く際にwindow.open関数の第3引数(JavaScript)に指定する。
   displayMethod                          認可判定とサービス提供可否判定の結果に応じて表示制御を行う場合の表示方法。
                                          下記のいずれかを指定する。
                                          NODISPLAY (非表示)
                                          DISABLED (非活性)
                                          NORMAL (通常表示)
   ====================================== ==========================================================================================

.. _tag-popup_link_tag:

popupLinkタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name                                   XHTMLのname属性。
   uri ``必須``                           URI。
                                          :ref:`tag-specify_uri` を参照。
   shape                                  XHTMLのshape属性。
   coords                                 XHTMLのcoords属性。
   secure                                 URIをhttpsにするか否か。
                                          httpsにする場合は ``true`` 、しない場合は ``false`` 。
   popupWindowName                        ポップアップのウィンドウ名。
                                          新しいウィンドウを開く際にwindow.open関数の第2引数(JavaScript)に指定する。
   popupOption                            ポップアップのオプション情報。
                                          新しいウィンドウを開く際にwindow.open関数の第3引数(JavaScript)に指定する。
   displayMethod                          認可判定とサービス提供可否判定の結果に応じて表示制御を行う場合の表示方法。
                                          下記のいずれかを指定する。
                                          NODISPLAY (非表示)
                                          DISABLED (非活性)
                                          NORMAL (通常表示)
   ====================================== ==========================================================================================

.. _tag-download_submit_tag:

downloadSubmitタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name                                   XHTMLのname属性。
   type ``必須``                          XHTMLのtype属性。
   uri ``必須``                           URI。
                                          :ref:`tag-specify_uri` を参照。
   disabled                               XHTMLのdisabled属性。
   value                                  XHTMLのvalue属性。
   src                                    XHTMLのsrc属性。
   alt                                    XHTMLのalt属性。
   usemap                                 XHTMLのusemap属性。
   align                                  XHTMLのalign属性。
   autofocus                              HTML5のautofocus属性。
   allowDoubleSubmission                  二重サブミットを許可するか否か。
                                          許可する場合は ``true`` 、許可しない場合は ``false`` 。
                                          デフォルトは ``true`` 。
   secure                                 URIをhttpsにするか否か。
                                          httpsにする場合は ``true`` 、しない場合は ``false`` 。
   displayMethod                          認可判定とサービス提供可否判定の結果に応じて表示制御を行う場合の表示方法。
                                          下記のいずれかを指定する。
                                          NODISPLAY (非表示)
                                          DISABLED (非活性)
                                          NORMAL (通常表示)
   ====================================== ==========================================================================================

.. _tag-download_button_tag:

downloadButtonタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name                                   XHTMLのname属性。
   uri ``必須``                           URI。
                                          :ref:`tag-specify_uri` を参照。
   value                                  XHTMLのvalue属性。
   type                                   XHTMLのtype属性。
   disabled                               XHTMLのdisabled属性。
   autofocus                              HTML5のautofocus属性。
   allowDoubleSubmission                  二重サブミットを許可するか否か。
                                          許可する場合は ``true`` 、許可しない場合は ``false`` 。
                                          デフォルトは ``true`` 。
   secure                                 URIをhttpsにするか否か。
                                          httpsにする場合は ``true`` 、しない場合は ``false`` 。
   displayMethod                          認可判定とサービス提供可否判定の結果に応じて表示制御を行う場合の表示方法。
                                          下記のいずれかを指定する。
                                          NODISPLAY (非表示)
                                          DISABLED (非活性)
                                          NORMAL (通常表示)
   ====================================== ==========================================================================================

.. _tag-download_link_tag:

downloadLinkタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name                                   XHTMLのname属性。
   uri ``必須``                           URI。
                                          :ref:`tag-specify_uri` を参照。
   shape                                  XHTMLのshape属性。
   coords                                 XHTMLのcoords属性。
   allowDoubleSubmission                  二重サブミットを許可するか否か。
                                          許可する場合は ``true`` 、許可しない場合は ``false`` 。
                                          デフォルトは ``true`` 。
   secure                                 URIをhttpsにするか否か。
                                          httpsにする場合は ``true`` 、しない場合は ``false`` 。
   displayMethod                          認可判定とサービス提供可否判定の結果に応じて表示制御を行う場合の表示方法。
                                          下記のいずれかを指定する。
                                          NODISPLAY (非表示)
                                          DISABLED (非活性)
                                          NORMAL (通常表示)
   ====================================== ==========================================================================================

.. _tag-param_tag:

paramタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   paramName ``必須``                     サブミット時に使用するパラメータの名前。
   name                                   値を取得するための名前。
                                          リクエストスコープなどスコープ上のオブジェクトを参照する場合に指定する。
                                          name属性とvalue属性のどちらか一方を指定する。
   value                                  値。
                                          直接値を指定する場合に使用する。
                                          name属性とvalue属性のどちらか一方を指定する。
   ====================================== ==========================================================================================

.. _tag-change_param_name_tag:

changeParamNameタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   paramName ``必須``                     サブミット時に使用するパラメータの名前。
   inputName ``必須``                     変更元となる元画面のinput要素のname属性。
   ====================================== ==========================================================================================

.. _tag-a_tag:

aタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   charset                                XHTMLのcharset属性。
   type                                   XHTMLのtype属性。
   name                                   XHTMLのname属性。
   href                                   XHTMLのhref属性。
                                          :ref:`tag-specify_uri` を参照。
   hreflang                               XHTMLのhreflang属性。
   rel                                    XHTMLのrel属性。
   rev                                    XHTMLのrev属性。
   shape                                  XHTMLのshape属性。
   coords                                 XHTMLのcoords属性。
   target                                 XHTMLのtarget属性。
   secure                                 URIをhttpsにするか否か。
                                          httpsにする場合は ``true`` 、しない場合は ``false`` 。
   ====================================== ==========================================================================================

.. _tag-img_tag:

imgタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   src ``必須``                           XHTMLのcharsrc属性。
                                          :ref:`tag-specify_uri` を参照。
   alt ``必須``                           XHTMLのalt属性。
   name                                   XHTMLのname属性。
   longdesc                               XHTMLのlongdesc属性。
   height                                 XHTMLのheight属性。
   width                                  XHTMLのwidth属性。
   usemap                                 XHTMLのusemap属性。
   ismap                                  XHTMLのismap属性。
   align                                  XHTMLのalign属性。
   border                                 XHTMLのborder属性。
   hspace                                 XHTMLのhspace属性。
   vspace                                 XHTMLのvspace属性。
   secure                                 URIをhttpsにするか否か。
                                          httpsにする場合は ``true`` 、しない場合は ``false`` 。
   ====================================== ==========================================================================================

.. _tag-link_tag:

linkタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   charset                                XHTMLのcharset属性。
   href                                   XHTMLのhref属性。
                                          :ref:`tag-specify_uri` を参照。
   hreflang                               XHTMLのhreflang属性。
   type                                   XHTMLのtype属性。
   rel                                    XHTMLのrel属性。
   rev                                    XHTMLのrev属性。
   media                                  XHTMLのmedia属性。
   target                                 XHTMLのtarget属性。
   secure                                 URIをhttpsにするか否か。
                                          httpsにする場合は ``true`` 、しない場合は ``false`` 。
   ====================================== ==========================================================================================

.. _tag-script_tag:

scriptタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   type ``必須``                          XHTMLのtype属性。
   id                                     XHTMLのid属性。
   charset                                XHTMLのcharset属性。
   language                               XHTMLのlanguage属性。
   src                                    XHTMLのsrc属性。
                                          :ref:`tag-specify_uri` を参照。
   defer                                  XHTMLのdefer属性。
   xmlSpace                               XHTMLのxml:space属性。
   secure                                 URIをhttpsにするか否か。
                                          httpsにする場合は ``true`` 、しない場合は ``false`` 。
   ====================================== ==========================================================================================

.. _tag-errors_tag:

errorsタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== =================================================================================================
   属性                                   説明
   ====================================== =================================================================================================
   cssClass                               リスト表示においてulタグに使用するCSSクラス名。
                                          デフォルトは"nablarch_errors"。
   infoCss                                情報レベルのメッセージに使用するCSSクラス名。
                                          デフォルトは"nablarch_info"。
   warnCss                                警告レベルのメッセージに使用するCSSクラス名。
                                          デフォルトは"nablarch_warn"。
   errorCss                               エラーレベルのメッセージに使用するCSSクラス名。
                                          デフォルトは ``nablarch_error`` 。
   filter                                 リストに含めるメッセージのフィルタ条件。
                                          下記のいずれかを指定する。
                                          all(全てのメッセージを表示する)
                                          global(入力項目に対応しないメッセージのみを表示)
                                          デフォルトは ``all`` 。
                                          globalの場合、\
                                          :java:extdoc:`ValidationResultMessage<nablarch.core.validation.ValidationResultMessage>`\
                                          のプロパティ名が入っているメッセージを取り除いて出力する。
   ====================================== =================================================================================================

.. _tag-error_tag:

errorタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   name ``必須``                          エラーメッセージを表示する入力項目のname属性。
   errorCss                               エラーレベルのメッセージに使用するCSSクラス名。
                                          デフォルトは ``nablarch_error`` 。
   messageFormat                          メッセージ表示時に使用するフォーマット。
                                          下記のいずれかを指定する。
                                          div(divタグ)
                                          span(spanタグ)
                                          デフォルトはdiv。
   ====================================== ==========================================================================================

.. _tag-no_cache_tag:

noCacheタグ
-------------------------
属性なし。

.. _tag-code_select_tag:

codeSelectタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   name ``必須``                          XHTMLのname属性。
   codeId ``必須``                        コードID。
   size                                   XHTMLのsize属性。
   multiple                               XHTMLのmultiple属性。
   disabled                               XHTMLのdisabled属性。
   tabindex                               XHTMLのtabindex属性。
   onfocus                                XHTMLのonfocus属性。
   onblur                                 XHTMLのonblur属性。
   onchange                               XHTMLのonchange属性。
   autofocus                              HTML5のautofocus属性。
   pattern                                使用するパターンのカラム名。
                                          デフォルトは指定なし。
   optionColumnName                       取得するオプション名称のカラム名。
   labelPattern                           ラベルを整形するパターン。
                                          プレースホルダを下記に示す。
                                          ``$NAME$`` : コード値に対応するコード名称
                                          ``$SHORTNAME$`` : コード値に対応するコードの略称
                                          ``$OPTIONALNAME$`` : コード値に対応するコードのオプション名称
                                          ``$VALUE$``: コード値
                                          ``$OPTIONALNAME$`` を使用する場合は、optionColumnName属性の指定が必須となる。
                                          デフォルトは ``$NAME$`` 。
   listFormat                             リスト表示時に使用するフォーマット。
                                          下記のいずれかを指定する。
                                          br(brタグ)
                                          div(divタグ)
                                          span(spanタグ)
                                          ul(ulタグ)
                                          ol(olタグ)
                                          sp(スペース区切り)
                                          デフォルトはbr。
   withNoneOption                         リスト先頭に選択なしのオプションを追加するか否か。
                                          追加する場合は ``true`` 、追加しない場合は ``false`` 。
                                          デフォルトは ``false`` 。
   noneOptionLabel                        リスト先頭に選択なしのオプションを追加する場合に使用するラベル。
                                          この属性は、withNoneOptionに ``true`` を指定した場合のみ有効となる。
                                          デフォルトは ``""`` 。
   errorCss                               エラーレベルのメッセージに使用するCSSクラス名。
                                          デフォルトは ``nablarch_error`` 。
   nameAlias                              name属性のエイリアスを設定する。
                                          複数指定する場合はカンマ区切り。
   ====================================== ==========================================================================================


.. _tag-code_radio_buttons_tag:

codeRadioButtonsタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`      id属性は指定不可。
   :ref:`tag-focus_attributes_tag`        accesskey属性は指定不可。
   name ``必須``                          XHTMLのname属性。
   codeId ``必須``                        コードID。
   disabled                               XHTMLのdisabled属性。
   onchange                               XHTMLのonchange属性。
   autofocus                              HTML5のautofocus属性。
                                          選択肢のうち、先頭要素のみautofocus属性を出力する。
   pattern                                使用するパターンのカラム名。
                                          デフォルトは指定なし。
   optionColumnName                       取得するオプション名称のカラム名。
   labelPattern                           ラベルを整形するパターン。
                                          プレースホルダを下記に示す。
                                          ``$NAME$`` : コード値に対応するコード名称
                                          ``$SHORTNAME$`` : コード値に対応するコードの略称
                                          ``$OPTIONALNAME$`` : コード値に対応するコードのオプション名称
                                          ``$VALUE$``: コード値
                                          ``$OPTIONALNAME$`` を使用する場合は、optionColumnName属性の指定が必須となる。
                                          デフォルトは ``$NAME$`` 。
   listFormat                             リスト表示時に使用するフォーマット。
                                          下記のいずれかを指定する。 
                                          br(brタグ)
                                          div(divタグ)
                                          span(spanタグ)
                                          ul(ulタグ)
                                          ol(olタグ)
                                          sp(スペース区切り) 
                                          デフォルトはbr。
   errorCss                               エラーレベルのメッセージに使用するCSSクラス名。
                                          デフォルトは ``nablarch_error`` 。
   nameAlias                              name属性のエイリアスを設定する。
                                          複数指定する場合はカンマ区切り。
   ====================================== ==========================================================================================

.. _tag-code_checkboxes_tag:

codeCheckboxesタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`      id属性は指定不可。
   :ref:`tag-focus_attributes_tag`        accesskey属性は指定不可。
   name ``必須``                          XHTMLのname属性。
   codeId ``必須``                        コードID。
   disabled                               XHTMLのdisabled属性。
   onchange                               XHTMLのonchange属性。
   autofocus                              HTML5のautofocus属性。
                                          選択肢のうち、先頭要素のみautofocus属性を出力する。
   pattern                                使用するパターンのカラム名。
                                          デフォルトは指定なし。
   optionColumnName                       取得するオプション名称のカラム名。
   labelPattern                           ラベルを整形するパターン。
                                          プレースホルダを下記に示す。
                                          ``$NAME$`` : コード値に対応するコード名称
                                          ``$SHORTNAME$`` : コード値に対応するコードの略称
                                          ``$OPTIONALNAME$`` : コード値に対応するコードのオプション名称
                                          ``$VALUE$``: コード値
                                          ``$OPTIONALNAME$`` を使用する場合は、optionColumnName属性の指定が必須となる。
                                          デフォルトは ``$NAME$`` 。
   listFormat                             リスト表示時に使用するフォーマット。
                                          下記のいずれかを指定する。 
                                          br(brタグ)
                                          div(divタグ)
                                          span(spanタグ)
                                          ul(ulタグ)
                                          ol(olタグ)
                                          sp(スペース区切り) 
                                          デフォルトはbr。
   errorCss                               エラーレベルのメッセージに使用するCSSクラス名。
                                          デフォルトは ``nablarch_error`` 。
   nameAlias                              name属性のエイリアスを設定する。
                                          複数指定する場合はカンマ区切り。
   ====================================== ==========================================================================================

.. _tag-code_checkbox_tag:

codeCheckboxタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   :ref:`tag-generic_attributes_tag`    
   :ref:`tag-focus_attributes_tag`      
   name ``必須``                          XHTMLのname属性。
   value                                  XHTMLのvalue属性。
                                          チェックありの場合に使用するコード値。
                                          デフォルトは ``1`` 。
   autofocus                              HTML5のautofocus属性。
   codeId ``必須``                        コードID。
   optionColumnName                       取得するオプション名称のカラム名。
   labelPattern                           ラベルを整形するパターン。
                                          プレースホルダを下記に示す。
                                          ``$NAME$`` : コード値に対応するコード名称
                                          ``$SHORTNAME$`` : コード値に対応するコードの略称
                                          ``$OPTIONALNAME$`` : コード値に対応するコードのオプション名称
                                          ``$VALUE$``: コード値
                                          ``$OPTIONALNAME$`` を使用する場合は、optionColumnName属性の指定が必須となる。
                                          デフォルトは ``$NAME$`` 。
   offCodeValue                           チェックなしの場合に使用するコード値。
                                          offCodeValue属性が指定されない場合は、
                                          codeId属性の値からチェックなしの場合に使用するコード値を検索する。
                                          検索結果が2件、かつ1件がvalue属性の値である場合は、
                                          残りの1件をチェックなしのコード値として使用する。
                                          検索で見つからない場合は、デフォルト値の ``0`` を使用する。
   disabled                               XHTMLのdisabled属性。
   onchange                               XHTMLのonchange属性。
   errorCss                               エラーレベルのメッセージに使用するCSSクラス名。
                                          デフォルトは ``nablarch_error`` 。
   nameAlias                              name属性のエイリアスを設定する。
                                          複数指定する場合はカンマ区切り。
   ====================================== ==========================================================================================

.. _tag-code_tag:

codeタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   name                                   表示対象のコード値を変数スコープから取得する際に使用する名前
                                          省略した場合は、コードID属性とpattern属性にて絞り込んだコードの一覧を表示する。
   codeId ``必須``                        コードID。
   pattern                                使用するパターンのカラム名。
                                          デフォルトは指定なし。
   optionColumnName                       取得するオプション名称のカラム名。
   labelPattern                           ラベルを整形するパターン。
                                          プレースホルダを下記に示す。
                                          ``$NAME$`` : コード値に対応するコード名称
                                          ``$SHORTNAME$`` : コード値に対応するコードの略称
                                          ``$OPTIONALNAME$`` : コード値に対応するコードのオプション名称
                                          ``$VALUE$``: コード値
                                          ``$OPTIONALNAME$`` を使用する場合は、optionColumnName属性の指定が必須となる。
                                          デフォルトは ``$NAME$`` 。
   listFormat                             リスト表示時に使用するフォーマット。
                                          下記のいずれかを指定する。 
                                          br(brタグ)
                                          div(divタグ)
                                          span(spanタグ)
                                          ul(ulタグ)
                                          ol(olタグ)
                                          sp(スペース区切り) 
                                          デフォルトはbr。
   ====================================== ==========================================================================================

.. _tag-message_tag:

messageタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   messageId ``必須``                     メッセージID。
   option0～option9                       メッセージフォーマットに使用するインデックスが0～9のオプション引数。
                                          最大10個までオプション引数が指定できる。
   language                               メッセージの言語。
                                          デフォルトはスレッドコンテキストに設定された言語。
   var                                    リクエストスコープに格納する際に使用する変数名。
                                          var属性が指定された場合はメッセージを出力せずにリクエストスコープに設定する。
                                          リクエストスコープに設定する場合はHTMLエスケープとHTMLフォーマットを行わない。
   htmlEscape                             HTMLエスケープをするか否か。
                                          HTMLエスケープをする場合は ``true`` 、しない場合は ``false`` 。
                                          デフォルトは ``true`` 。
   withHtmlFormat                         HTMLフォーマット(改行と半角スペースの変換)をするか否か。
                                          HTMLフォーマットはHTMLエスケープをする場合のみ有効となる。
                                          デフォルトは ``true`` 。
   ====================================== ==========================================================================================

.. _tag-write_tag:

writeタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ======================================================================================================================
   属性                                   説明
   ====================================== ======================================================================================================================
   name ``必須``                          表示対象の値を変数スコープから取得する際に使用する名前
   withHtmlFormat                         HTMLフォーマット(改行と半角スペースの変換)をするか否か。
                                          HTMLフォーマットはHTMLエスケープをする場合のみ有効となる。
                                          デフォルトは ``true`` 。
   valueFormat                            出力時のフォーマット。
                                          指定内容は、 :ref:`tag-format_value` を参照。
   ====================================== ======================================================================================================================


.. _tag-pretty_print_tag:

prettyPrintタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   name ``必須``                          表示対象の値を変数スコープから取得する際に使用する名前
   ====================================== ==========================================================================================



.. _tag-raw_write_tag:

rawWriteタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   name ``必須``                          表示対象の値を変数スコープから取得する際に使用する名前
   ====================================== ==========================================================================================


.. _tag-set_tag:

setタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   var ``必須``                           リクエストスコープに格納する際に使用する変数名。
   name                                   値を取得するための名前。name属性とvalue属性のどちらか一方を指定する。
   value                                  値。直接値を指定する場合に使用する。name属性とvalue属性のどちらか一方を指定する。
   scope                                  変数を格納するスコープを設定する。
                                          指定できるスコープを下記に示す。
                                          page: ページスコープ
                                          request: リクエストスコープ
                                          デフォルトはリクエストスコープ。
   bySingleValue                          name属性に対応する値を単一値として取得するか否か。
                                          デフォルトは ``true`` 。
   ====================================== ==========================================================================================

.. _tag-include_tag:

includeタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   path ``必須``                          インクルードするリソースのパス。
   ====================================== ==========================================================================================

.. _tag-include_param_tag:

includeParamタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   paramName ``必須``                     インクルード時に使用するパラメータの名前。
   name                                   値を取得するための名前。name属性とvalue属性のどちらか一方を指定する。
   value                                  値。直接値を指定する場合に使用する。name属性とvalue属性のどちらか一方を指定する。
   ====================================== ==========================================================================================

.. _tag-confirmation_page_tag:

confirmationPageタグ
-------------------------

.. table::
   :class: tag-reference

   ====================================== ==========================================================================================
   属性                                   説明
   ====================================== ==========================================================================================
   path                                   フォワード先（入力画面）のパス。
   ====================================== ==========================================================================================

.. _tag-ignore_confirmation_tag:

ignoreConfirmationタグ
-------------------------
属性なし。

.. _tag-for_input_page_tag:

forInputPageタグ
-------------------------
属性なし。
 
.. _tag-for_confirmation_page_tag:

forConfirmationPageタグ
-------------------------
属性なし。
