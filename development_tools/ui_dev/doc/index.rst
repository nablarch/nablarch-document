======================================================
Nablarch UI開発基盤 解説書
======================================================

.. toctree::
  :glob:
  :hidden:

  *
  */*
  
.. important::

  UI開発基盤を使用する際には、以下の知識が必要となる。
  これらの有識者がいない場合、UI開発基盤が提供する部品のカスタマイズや追加を行うことは難しく、生産性低下の原因となる。
  
  * `Node.js <https://nodejs.org/ja/>`_
  * `RequireJS <http://requirejs.org/>`_
  * `jQuery <https://jquery.com/>`_
  * `Sugar <https://sugarjs.com/>`_
  * `less <http://less-ja.studiomohawk.com/>`_

  部品の仕様を少しでも変更したい場合であっても、難易度の高いカスタマイズが必要である。
  特に、部品を縦に並べて画面を構成しない場合（:doc:`internals/multicol_css_framework` を使用する場合）は画面デザインの難易度が高い。

  また、UI開発基盤はNablarch1.4をベースに構築されている。
  このため、Nablarch5から追加された機能には対応していないものがある。
  例えば、 :ref:`universal_dao` に対応していない問題や、 非推奨機能の :ref:`ウィンドウスコープ <tag-window_scope>` が前提となっている問題がある。

  これらの点を考慮してUI開発基盤の使用を検討すること。

**目次**

:doc:`about_this_book`

:doc:`book_layout`

:doc:`related_documents`

**I: はじめに**
  1. :doc:`introduction/intention`
  2. :doc:`introduction/grand_design`
  3. :doc:`introduction/ui_development_workflow`

**II: 開発作業手順**
  4. :doc:`development_environment/initial_setup`
  5. :doc:`development_environment/redistribution`
  6. :doc:`development_environment/modifying_code_and_testing`
  7. :doc:`development_environment/update_bundle_plugin`

**III: プロジェクトのファイル構成と変更管理**
  8.  :doc:`structure/directory_layout`
  9.  :doc:`structure/plugins`

**IV: アーキテクチャ詳説**
  10. :doc:`internals/architecture_overview`
  11. :doc:`internals/jsp_page_templates`
  12. :doc:`internals/jsp_widgets`
  13. :doc:`internals/css_framework`
  14. :doc:`internals/multicol_css_framework`
  15. :doc:`internals/js_framework`
  16. :doc:`internals/inbrowser_jsp_rendering`
  17. :doc:`internals/showing_specsheet_view`
  18. :doc:`plugin_build`

**V: リファレンス**
  19. :doc:`reference_ui_standard/index`
  20. :doc:`reference_jsp_widgets/index`
  21. :doc:`reference_js_framework`
  22. :doc:`reference_ui_plugin/index`

**VI: 補足資料**
  23. :doc:`testing`
  24. :doc:`known_issues`

