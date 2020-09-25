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
  これらの有識者がいない場合、UI開発基盤の使用は困難である。

  * `Node.js <https://nodejs.org/ja/>`_
  * `RequireJS <http://requirejs.org/>`_
  * `jQuery <https://jquery.com/>`_
  * `Sugar <https://sugarjs.com/>`_
  * `less <http://lesscss.org/>`_

  また、UI開発基盤は、設計工程からJSPを作成するアプローチを採用しているが、以下の理由により、「設計工程用JSPと開発工程用JSPのダブルメンテナンス」が往々にして発生する

  * JSPに設計工程のみで必要な情報を埋め込むことになるため、開発工程での可読性が著しく低下する。
  * 開発時に分岐などのロジックが埋め込まれた場合、設計工程と開発工程で全く同じJSPを使用することは不可能である。


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


.. |br| raw:: html

  <br />