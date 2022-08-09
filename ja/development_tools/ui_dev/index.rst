====================================
フロントエンド上級者向けのUI開発基盤
====================================

.. important::

  UI開発基盤を使用する際には、以下の知識が必要となる。
  これらの有識者がいない場合、UI開発基盤の使用は困難である。

  * `Node.js <https://nodejs.org/ja/>`_
  * `RequireJS <http://requirejs.org/>`_
  * `jQuery <https://jquery.com/>`_
  * `Sugar <https://sugarjs.com/>`_
  * `less <http://lesscss.org/>`_

  また、UI開発基盤は設計工程からJSPを作成するアプローチを採用しているが、以下の理由により、「設計工程用JSPと開発工程用JSPのダブルメンテナンス」が往々にして発生する

  * JSPに設計工程のみで必要な情報を埋め込むことになるため、開発工程での可読性が著しく低下する。
  * 開発時に分岐などのロジックが埋め込まれた場合、設計工程と開発工程で全く同じJSPは使用不可能である。


.. toctree::
  :maxdepth: 1

  doc/index
  guide/index
  guide/widget_usage/widget_list

`ソースコード <https://github.com/nablarch/nablarch-plugins-bundle>`_


.. |br| raw:: html

  <br />