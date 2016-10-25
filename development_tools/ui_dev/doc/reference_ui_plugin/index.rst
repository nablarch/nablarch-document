===============================
UIプラグイン一覧
===============================

サードパーティ製ライブラリ
======================================
これらのプラグインは Nablarch UI開発基盤が依存している外部ライブラリを含むものであり、
その性質上、プロジェクト側でのカスタマイズは想定していない。

なお、これらはUI開発基盤のリリース配布物に同梱していない。
:doc:`../development_environment/initial_setup` の手順に従って作業することで\
別途ダウンロードするようになっている。

================================== ============================= ============ ======================================================
プラグインID                       名称                          カスタマイズ 概要
================================== ============================= ============ ======================================================
es6-promise                        ES6 Promise API ポリフィル    不可         ES6標準の非同期処理APIであるPromiseライブラリの\
                                                                              ポリフィル
                                                                              一部の開発用コマンドの中で使用している。

font-awesome                       WebFontアイコン               不可         WebFontによるアイコン画像とそれを表示するための\
                                                                              スタイル定義。

jquery                             jQueryライブラリ              不可         W3C DOM APIの互換レイヤを提供するライブラリ。

less                               LESSコンパイラ                不可         LESS記法で記述されたスタイル定義を\
                                                                              通常のCSSに展開するツール

rquirejs                           AMDモジュールローダ\           不可        AMD(Asynchronous Module Definition)
                                   /コンパイラ                                形式で記述されたJavaScriptライブラリを管理する\
                                                                              ライブラリおよびminifyツール

requiejs-text                      テキストファイルAMD拡張       不可         通常のテキストファイルをAMDモジュールとして\
                                                                              管理するためのrequirejs 拡張

shelljs                            プラットフォーム互換コマンド  不可         cd/grep/ln などの主要基本コマンドのnode.jsによる実装。
                                                                              一部の開発用コマンドの中で使用している。

sugar                              JavaScriptコアAPI拡張         不可         String/Array/Number などのコアクラスを拡張する。
                                                                              また、Array.forEach など一部のES5標準APIの\
                                                                              ポリフィルを提供する。

================================== ============================= ============ ======================================================

CSS共通スタイルプラグイン
=================================
画面の表示制御を行うスタイル定義を含むプラグイン。
Nablarch UI開発基盤のスタイルは全て LESS記法を用いて記述している。

================================== =============================== ============ =====================================================================
プラグインID                       名称                            カスタマイズ 概要
================================== =============================== ============ =====================================================================
nablarch-css-core                  コアスタイル定義                不可         Nablarchのスタイル定義における共通基盤となる以下のファイルを含む。

                                                                                 **reset.less**
                                                                                   各ブラウザのHTML要素に対するデフォルトスタイルを一律除去する\
                                                                                   ことでブラウザ間の表示互換性を向上させる。

                                                                                 **grid.less**
                                                                                   グリッドフレームワークを定義する。

                                                                                 **css3.less**
                                                                                   CSS3プロパティに相当するブラウザ互換なクラス定義

nablarch-css-base                  HTML基本要素スタイル            非推奨       **reset.less** で除去されたHTMLの基本要素のスタイルを再定義する。
                                                                                修正時の影響が大きいので、カスタマイズは推奨しない。

nablarch-css-common                NAF既定CSSスタイル定義          可           精査エラーメッセージの表示色などNAF側で指定されている\
                                                                                CSSクラスの内容を定義する。

nablarch-css-color-default         カラースキーム定義              必須         画面全体の基本配色を定義する。

nablarch-css-conf-wide             ワイド表示モード定義            可           レスポンシブ対応画面におけるワイド表示モード\
                                                                                (デバイス/ウィンドウの横論理ピクセル数が1024超)\
                                                                                での画面レイアウトを定義する。\

nablarch-css-conf-compact          コンパクト表示モード定義        可           レスポンシブ対応画面におけるコンパクト表示モード\
                                                                                (デバイス/ウィンドウの横論理ピクセル数が640超 1024未満)\
                                                                                における画面レイアウトを定義する。

nablarch-css-conf-narrow           ナロー表示モード定義            可           レスポンシブ対応画面におけるナロー表示モード\
                                                                                (デバイス/ウィンドウの横論理ピクセル数が640未満)\
                                                                                における画面レイアウトを定義する。

nablarch-css-conf-multicol         マルチレイアウト表示モード定義  可           マルチレイアウト表示モード(本表示モードはワイドモードを\
                                                                                ベースとしている)における画面レイアウトを定義する。
                                                                                本モード使用時は、画面サイズに応じた表示モードの切替\
                                                                                (レスポンシブ対応)は使用できない。

================================== =============================== ============ =====================================================================


表示モード切替用プラグイン
=================================
:doc:`../internals/css_framework` の機能である表示モードを切り替えを実現するためのプラグイン。

================================== =============================== ============ =====================================================================
プラグインID                       名称                            カスタマイズ 概要
================================== =============================== ============ =====================================================================
nablarch-device-media_query        表示モード切替用プラグイン      可           MediaQueryによって、 表示モードを切り替える機能を実装する。|br|
                                                                                表示モード切替えの条件を変更する場合は、
                                                                                本プラグインをカスタマイズする。|br|
                                                                                プラグインは、/WEB-INF/tags/device/media.tag として実装されている。
================================== =============================== ============ =====================================================================




.. _nablarch-device-fix:

特定端末向けパッチプラグイン
===================================
UserAgent判定により、特定の端末のみで有効となるスクリプトやスタイル定義からなるプラグイン。
ただし、いわゆる feature-detection による判定を行うものについてはここには含まない。

.. important::

  システムサポート外の端末を対象としたプラグインは、あらかじめ除去しておくこと。
  ( :doc:`../development_environment/initial_setup` の「プロジェクトで使用するプラグインの選定」の項を参照。)

============================================ ============================= ============ =====================================================================
プラグインID                                 名称                          カスタマイズ 概要
============================================ ============================= ============ =====================================================================
nablarch-device-fix-base                     UserAgentによるデバイス判定   可           リクエストごとにサーバサイド処理でUserAgent判定を行い |br|
                                                                                        その結果をJavaScriptのグローバル変数および、<body>要素のクラス属性
                                                                                        に設定する。|br|
                                                                                        なお、ローカル表示ではJavaScriptによるUserAgent判定を行う。


nablarch-device-fix-ios                      ios向けパッチ                 可           iOSの標準ブラウザにおける表示不具合を回避するためのスクリプト\
                                                                                        およびスタイル定義。

nablarch-device-fix-android_browser          android向けパッチ             可           androidの標準ブラウザにおける表示不具合を回避するためのスクリプト\
                                                                                        およびスタイル定義。
============================================ ============================= ============ =====================================================================


開発用ツールプラグイン
===========================
開発作業において使用する各種ツールからなるプラグイン。

これらのツールの使用方法については :doc:`../development_environment/initial_setup` を参照すること。

============================================ =============================== ============ ===================================================================
プラグインID                                 名称                            カスタマイズ 概要
============================================ =============================== ============ ===================================================================
nablarch-dev-tool-installer                  Nablarch UI開発基盤             不可         Nablarch UI基盤標準プラグインをプロジェクト側にインストール\
                                             標準プラグインインストーラー                 するスクリプト。

nablarch-dev-tool-server                     Nablarch UI開発基盤             不可         Nablarch UI開発基盤自体の各種テストに用いる\
                                             テスト用簡易サーバー                         簡易アプリケーションサーバー


nablarch-dev-ui_test-support                 Nablarch UI開発基盤             不可         Nablarch UI開発基盤自体のテストケースで使用している\
                                             テストケース用資源                           テストツール類 (qunit.js など)

nablarch-dev-tool-uibuild                    ウェブアプリケーション資源      可           ウェブアプリケーション上で公開される資源を各プラグインから収集し、
                                             ビルドスクリプト                             サーブレットコンテキスト配下に配置するスクリプト。|br|
                                                                                          スクリプトのミニファイおよびスタイル定義の\
                                                                                          LESSコンパイルとミニファイも合わせて行う。

nablarch-dev-tool-update_support             Nablarch 標準プラグイン         不可         利用しているプラグインとリリース資材のプラグイン間で\
                                             更新補助スクリプト                           バージョンが異なるプラグイン名を出力するスクリプト。
============================================ =============================== ============ ===================================================================



業務画面JSPローカル表示機能プラグイン
=========================================
以下のプラグインには :doc:`../internals/inbrowser_jsp_rendering` およびその拡張機能を実現するための各種スクリプトなどが含まれる。

使用方法については **HTML/JSP作成ガイド** を参照すること。

======================================== ======================================================= ============ ===============================================================
プラグインID                                 名称                                                カスタマイズ 概要
======================================== ======================================================= ============ ===============================================================
nablarch-dev-ui_demo-core                    ローカル表示用JSPレンダラー                         不可           業務画面JSPをDOMに直接変換してプレビューを表示するJavaScript

nablarch-dev-ui_demo-config                  ローカル表示時変数定義                              必要           JSPのレンダリング時に参照する各種スコープ変数の値を設定する。
                                                                                                                (ログインユーザ名など)

nablarch-dev-ui_demo-core-lib                ローカル表示用タグライブラリ                        可             下記のタグのレンダリングを行うスクリプト群
                                             スタブ
                                                                                                                * JSP標準タグライブラリ( **<jsp:include>** など)
                                                                                                                * JSTLタグライブラリ( **<c:if>** など)
                                                                                                                * EL埋め込み関数( **${fn:replace}** など)
                                                                                                                * Nablarch標準タグライブラリ( **<n:form>** など)
                                                                                                                * その他特殊な対応が必要となるHTMLタグ( **<style>** など)

nablarch-dev-ui_tool-base-core           業務画面JSPローカル表示機能のベースコアプラグイン       不要           業務画面JSPローカル表示機能のベースとなる機能を実装する。

nablarch-dev-ui_tool-base-config         業務画面JSPローカル表示機能の\                          必須           業務画面JSPローカル表示機能のリソースを管理する。|br|
                                         ベースコンフィギュレーションプラグイン                                 リソースは、画面項目定義データ自動生成ツールを\
                                                                                                                使用して設計書から自動生成する。
                                                                                                                

nablarch-dev-ui_tool-jsp_verify          JSP検証ツールプラグイン                                 可             業務画面JSPローカル表示機能で使用される\
                                                                                                                JSPファイルの検証の実装。|br|
                                                                                                                ローカル表示や設計書表示用の\
                                                                                                                属性のチェックを行う。|br|
                                                                                                                IE8の場合は、検証処理は実行しない\
                                                                                                                (IE8には未対応)。

nablarch-dev-ui_tool-spec_view-core      設計書ビューコアプラグイン                              不要           :doc:`../internals/showing_specsheet_view` 
                                                                                                                の実装。

nablarch-dev-ui_tool-spec_view           設計書ビュープラグイン                                  不要           設計情報をJSPから取得する拡張機能。
                                                                                                                (jQueryの拡張プラグインとして提供する。) |br|
                                                                                                                画面設計書ViewなどJSPの値を取得、変換
                                                                                                                する際に本拡張機能が利用できる。

nablarch-dev-ui_tool-spec_view-resource  設計書ビュー用のリソース管理プラグイン                  可             表示される設計書のテンプレート。
                                                                                                                フォーマットを変更する場合は、
                                                                                                                本プラグインに含まれるSpecSheetTmeplate.xlsx
                                                                                                                を修正し、htm形式で保存する。
======================================== ======================================================= ============ ===============================================================


JavaScriptユーティリティプラグイン
========================================
JavaScriptのコアライブラリをサポートするユーティリティスクリプト。

============================================ =============================== ============ ====================================================================
プラグインID                                 名称                            カスタマイズ 概要
============================================ =============================== ============ ====================================================================
nablarch-js-util-bigdecimal                  簡易BigDecimalライブラリ        不可          JavaScriptのNumber型(32bit浮動少数)を使用した場合に発生する誤差を\
                                                                                           回避するために使用する簡易BigDecimal型実装クラス。|br|
                                                                                           ただし、内部的には32bit浮動少数を使用するため、
                                                                                           有効桁が15桁を超える場合は使用できない。

nablarch-js-util-date                        日付フォーマット変換ライブラリ  可            Javaのjava.util.SimpleDateFormatのサブセットとなる\
                                                                                           日付フォーマット変換を実装するユーティリティクラス。

nablarch-js-util-consumer                    簡易Tokenizer/Parser            不可          ミニ言語のパーサの実装に使用する簡易パーサ

============================================ =============================== ============ ====================================================================

UI部品ウィジェットプラグイン
========================================
:doc:`../internals/jsp_widgets` を実装するタグファイル・スクリプト・スタイル定義などを格納するプラグイン。

====================================== ==================================================================== ============ ========================================================
プラグインID                           名称                                                                 カスタマイズ 概要
====================================== ==================================================================== ============ ========================================================
nablarch-widget-core                   JSウィジェット基盤クラス                                             不可           :doc:`../reference_jsp_widgets/index`
                                                                                                                           の中で共通的に使用されるJavaScript部品を\
                                                                                                                           格納するプラグイン。
                                                                                                                           jQueryのカスタムセレクタもここに含まれる。

nablarch-widget-box-base               表示領域ウィジェット共通テンプレート                                 可             表示領域ウィジェットで共通的に使用されるCSS\
                                                                                                                           定義を実装する。

nablarch-widget-box-content            :doc:`../reference_jsp_widgets/box_content`                          可             左記ウィジェットの実装

nablarch-widget-box-img                :doc:`../reference_jsp_widgets/box_img`                              可             左記ウィジェットの実装

nablarch-widget-box-title              :doc:`../reference_jsp_widgets/box_title`                            可             左記ウィジェットの実装

nablarch-widget-button                 :doc:`../reference_jsp_widgets/button_submit`                        可             左記ウィジェットの実装

nablarch-widget-collapsible            開閉機能スクリプト                                                   非推奨         画面内の領域を開閉する機能を実装するスクリプト
                                                                                                                           :doc:`../reference_jsp_widgets/table_treelist`
                                                                                                                           などから使用される。

nablarch-widget-column-base            カラムウィジェット共通プラグイン                                     可             カラムウィジェットで使用される以下の共通的な
                                                                                                                           機能を実装する。
                                                                                                                             
                                                                                                                           * 共通的に使用されるCSS定義
                                                                                                                           * カラムウェジェットで使用するJSPローカル表示機能用ライブラリ

nablarch-widget-column-checkbox        :doc:`../reference_jsp_widgets/column_checkbox`                      可             左記ウィジェットの実装

nablarch-widget-column-code            :doc:`../reference_jsp_widgets/column_code`                          可             左記ウィジェットの実装

nablarch-widget-column-label           :doc:`../reference_jsp_widgets/column_label`                         可             左記ウィジェットの実装

nablarch-widget-column-link            :doc:`../reference_jsp_widgets/column_link`                          可             左記ウィジェットの実装

nablarch-widget-column-radio           :doc:`../reference_jsp_widgets/column_radio`                         可             左記ウィジェットの実装

nablarch-widget-field-base             :doc:`../reference_jsp_widgets/field_base`                           可             左記ウィジェットの実装

nablarch-widget-field-block            :doc:`../reference_jsp_widgets/field_block`                          可             左記ウィジェットの実装

nablarch-widget-field-calendar         :doc:`../reference_jsp_widgets/field_calendar`                       可             左記ウィジェットの実装

nablarch-widget-field-checkbox         :doc:`../reference_jsp_widgets/field_checkbox`                       可             左記ウィジェットの実装

nablarch-widget-field-file             :doc:`../reference_jsp_widgets/field_file`                           可             左記ウィジェットの実装

nablarch-widget-field-hint             :doc:`../reference_jsp_widgets/field_hint`                           可             左記ウィジェットの実装

nablarch-widget-field-label            :doc:`../reference_jsp_widgets/field_label`                          可             左記ウィジェットの実装

nablarch-widget-field-label_block      :doc:`../reference_jsp_widgets/field_label_block`                    可             左記ウィジェットの実装

nablarch-widget-field-label_id_value   :doc:`../reference_jsp_widgets/field_label_id_value`                 可             左記ウィジェットの実装

nablarch-widget-field-listbuilder      :doc:`../reference_jsp_widgets/field_listbuilder`                    可             左記ウィジェットの実装

nablarch-widget-field-password         :doc:`../reference_jsp_widgets/field_password`                       可             左記ウィジェットの実装

nablarch-widget-field-pulldown         :doc:`../reference_jsp_widgets/field_pulldown`                       可             左記ウィジェットの実装

nablarch-widget-field-radio            :doc:`../reference_jsp_widgets/field_radio`                          可             左記ウィジェットの実装

nablarch-widget-field-text             :doc:`../reference_jsp_widgets/field_text`                           可             左記ウィジェットの実装

nablarch-widget-field-textarea         :doc:`../reference_jsp_widgets/field_textarea`                       可             左記ウィジェットの実装

nablarch-widget-link                   :doc:`../reference_jsp_widgets/link_submit`                          可             左記ウィジェットの実装

nablarch-widget-multicol-cell          マルチレイアウト用列定義ウィジェット                                 可             マルチレイアウトで使用する列を表すタグ(layout:cell)
                                                                                                                           を実装する。|br|
                                                                                                                           詳細は :ref:`multicol_css_framework_example` を参照。

nablarch-widget-multicol-row           マルチレイアウト用行定義ウィジェット                                 可             マルチレイアウトで使用する行を表すタグ(layout:row)
                                                                                                                           を実装する。|br|
                                                                                                                           詳細は :ref:`multicol_css_framework_example` を参照。

nablarch-widget-placeholder            placeholder属性ポリフィル                                            非推奨         IEなどのplaceholder属性を実装していない\
                                                                                                                           ブラウザ向けのポリフィル実装

nablarch-widget-readonly               変更不可項目制御                                                     非推奨         readonly属性の拡張。
                                                                                                                           通常のreadonly属性とは異なり、プルダウンや\
                                                                                                                           チェックボックスの選択状態の変更も抑止できる。

nablarch-widget-slide-menu             スライドメニューウィジェット                                         必須           narrow,compact表示でメニューを省スペース化する\
                                                                                                                           サンプル機能。
                                                                                                                           JavaScript,LESSの定義はそのまま利用できるが、
                                                                                                                           JSPはPJ側で修正する必要がある。

nablarch-widget-spec                   :ref:`画面仕様記述用ウィジェット <reference_jsp_widgets_index_spec>` 可             画面仕様の情報を記述するタグの実装。|br|
                                                                                                                           設計書ビュー表示プラグインはこのタグから\
                                                                                                                           情報を取得した情報を使用する。|br|
                                                                                                                           このタグはサーバ表示には影響を与えない。

nablarch-widget-spec-meta_info         :ref:`メタ情報記述用ウィジェット <reference_jsp_widgets_index_spec>` 可             設計書作成者等の情報を記述するためのタグの\
                                                                                                                           実装。|br|
                                                                                                                           設計書ビュー表示プラグインは、このタグから
                                                                                                                           取得した情報を使用する。|br|
                                                                                                                           このタグはサーバ表示には影響を与えない。

nablarch-widget-tab                    :doc:`../reference_jsp_widgets/tab_group`                            可             左記ウィジェットの実装

nablarch-widget-table-base             テーブルウィジェットの共通プラグイン                                 可             テーブルウィジェットで使用される以下の共通的な\
                                                                                                                           機能が実装されている。

                                                                                                                           * 共通的に使用されるCSS定義
                                                                                                                           * 表示モードに応じたウィジェット表示内容の\
                                                                                                                             切り替え用CSS定義
                                                                                                                           * テーブルウェジェットで使用するJSPローカル表示機能用\
                                                                                                                             ライブラリ

nablarch-widget-table-plain            :doc:`../reference_jsp_widgets/table_plain`                          可             左記ウィジェットの実装

nablarch-widget-table-row              :doc:`../reference_jsp_widgets/table_row`                            可             左記ウィジェットの実装

nablarch-widget-table-search_result    :doc:`../reference_jsp_widgets/table_search_result`                  可             左記ウィジェットの実装

nablarch-widget-table-tree             :doc:`../reference_jsp_widgets/table_treelist`                       可             左記ウィジェットの実装

nablarch-widget-toggle-checkbox        チェックボックスの全選択/全解除プラグイン                            可             リンクやボタンにチェックボックス全選択/全解除\
                                                                                                                           の機能を持たせるためのプラグイン。

nablarch-widget-tooltip                ツールチップ表示プラグイン                                           可             マウスオーバーにより、補足情報をポップアップで\
                                                                                                                           表示する機能をもつプラグイン。
====================================== ==================================================================== ============ ========================================================


UIイベント制御部品プラグイン
========================================
画面上のイベント制御を宣言的に定義する各種ウィジェットを実装するプラグイン。

====================================== ======================================================= ============ ================================================
プラグインID                           名称                                                    カスタマイズ 概要
====================================== ======================================================= ============ ================================================
nablarch-js-submit                     Nablarchカスタムサブミットイベント                      不可           Nablarchフレームワークのサブミット時処理\
                                                                                                              (nablarch_submit)の実行前後に発火する\
                                                                                                              jQueryグローバルカスタムイベントを定義する。

nablarch-widget-event-base             イベントウィジェットベースプラグイン                    不可           イベントウィジェットのベースプラグイン。|br|
                                                                                                              JSPローカル表示時に、イベントの\
                                                                                                              エミュレーションを行うために必要な機能を\
                                                                                                              実装する。

nablarch-widget-event-listen           :doc:`../reference_jsp_widgets/event_listen`            不可           画面内で発生する指定されたイベントを監視し、
                                                                                                              各種イベントアクションを実行するウィジェット\
                                                                                                              の実装

nablarch-widget-event-autosum          `自動集計イベント`_                                     不可           左記イベントアクションの実装

nablarch-widget-event-dialog           ダイアログ表示イベントアクション                        不可           左記イベントアクションの実装 |br|
                                       :doc:`../reference_jsp_widgets/event_alert`                            ダイアログ表示は、アラート、確認ダイアログから使用される。
                                       :doc:`../reference_jsp_widgets/event_confirm`

nablarch-widget-event-send_request     :doc:`../reference_jsp_widgets/event_send_request`      不可           左記イベントアクションの実装


nablarch-widget-event-toggle           :doc:`../reference_jsp_widgets/event_toggle_disabled`   不可           左記イベントアクションの実装
                                       :doc:`../reference_jsp_widgets/event_toggle_property`
                                       :doc:`../reference_jsp_widgets/event_toggle_readonly`

nablarch-widget-event-window_close     :doc:`../reference_jsp_widgets/event_window_close`      不可           左記イベントアクションの実装

nablarch-widget-event-write_to         :doc:`../reference_jsp_widgets/event_write_to`          不可           左記イベントアクションの実装

====================================== ======================================================= ============ ================================================

.. _自動集計イベント: ../../../../_static/ui_dev/yuidoc/classes/nablarch.ui.AutoSum.html

業務画面テンプレートプラグイン
========================================
:doc:`../internals/jsp_page_templates` の実体となるタグファイルと、それに付随するスクリプトやスタイル定義から構成されるプラグイン。
また、各テンプレートからインクルードされる共通領域を描画するJSPのサンプルもここに含まれる。

====================================== ======================================================= ============ ================================================
プラグインID                           名称                                                    カスタマイズ 概要
====================================== ======================================================= ============ ================================================
nablarch-template-base                 :ref:`base_layout_tag`                                  可             左記テンプレートの実装。

nablarch-template-page                 :ref:`page_template_tag`                                可             左記テンプレートの実装。

nablarch-template-error                :ref:`errorpage_template_tag`                           可             左記テンプレートの実装。

nablarch-template-head                 HTML head要素定義インクルード                           可           head要素の内容を出力するJSP。
                                                                                                            :ref:`base_layout_tag` からインクルードされ、
                                                                                                            以下の内容を定義している。

                                                                                                            - <title>タグの内容
                                                                                                            - MediaQueryによる表示モード切替え
                                                                                                            - 外部CSSファイルのインクルード
                                                                                                            - <meta>タグの内容
                                                                                                              (IEの互換モード設定など)

nablarch-template-multicol-head        マルチレイアウト用HTML head要素定義インクルード         可           マルチレイアウト用のhead要素の内容を出力する\
                                                                                                            JSP。
                                                                                                            :ref:`base_layout_tag` からインクルードされ、
                                                                                                            以下の内容を定義している。

                                                                                                            - <title>タグの内容
                                                                                                            - 外部CSSファイルのインクルード
                                                                                                            - <meta>タグの内容
                                                                                                              (IEの互換モード設定など)

                                                                                                            使用方法は、
                                                                                                            :ref:`multicol_css_framework_setting_layout`
                                                                                                            を参照。

nablarch-template-js_include           HTML script要素定義インクルード                         可           scriptタグの内容を出力するJSP。
                                                                                                            :ref:`base_layout_tag` からインクルードされる。

                                                                                                            .. tip::

                                                                                                              :ref:`base_layout_tag` ではこのインクルードを\
                                                                                                              HTMLの最後(bodyタグの末端)に出力している。|br|
                                                                                                              これは、画面の描画とスクリプトのロードを\
                                                                                                              並行に実行し、ユーザの体感速度を
                                                                                                              向上させるためである。

nablarch-template-app_nav              アプリケーション共通ナビゲーションメニュー              必須           業務画面の共通ナビゲーション領域を描画する\
                                       サンプル                                                               JSPおよびスタイル定義などのリソース。
                                                                                                              JSPは :ref:`page_template_tag` から\
                                                                                                              インクルードされる。|br|
                                                                                                              内容はUI開発基盤用プロジェクトテンプレート\
                                                                                                              と同じものなので、PJ側で修正する必要がある。

nablarch-template-app_header           アプリケーション共通ヘッダー サンプル                   必須           業務画面の共通ヘッダー領域を描画するJSPおよび\
                                                                                                              スタイル定義などのリソース。
                                                                                                              JSPは :ref:`page_template_tag` から\
                                                                                                              インクルードされる。|br|
                                                                                                              内容はUI開発基盤用プロジェクトテンプレート\
                                                                                                              と同じものなので、PJ側で修正する必要がある。

nablarch-template-app_footer           アプリケーション共通フッターサンプル                    必須           業務画面の共通フッター領域を描画するJSPおよび\
                                                                                                              スタイル定義などのリソース。
                                                                                                              JSPは :ref:`page_template_tag` から\
                                                                                                              インクルードされる。|br|
                                                                                                              内容はUI開発基盤用プロジェクトテンプレート\
                                                                                                              と同じものなので、PJ側で修正する必要がある。

nablarch-template-app_aside            アプリケーション共通サイドメニューサンプル               必須          業務画面の共通サイドメニューを描画するJSPおよび\
                                                                                                              スタイル定義などのリソース。
                                                                                                              JSPは :ref:`page_template_tag` から\
                                                                                                              インクルードされる。|br|
                                                                                                              内容はUI開発基盤用プロジェクトテンプレート\
                                                                                                              と同じものなので、PJ側で修正する必要がある。

====================================== ======================================================= ============ ================================================


.. |br| raw:: html

  <br />
