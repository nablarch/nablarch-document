====================================
フロントエンド上級者向けのUI開発基盤
====================================

.. important::

  UI開発基盤を使用する際には、以下の知識が必要となる。
  これらの有識者がいない場合、UI開発基盤の仕様は困難である。

  * `Node.js <https://nodejs.org/ja/>`_
  * `RequireJS <http://requirejs.org/>`_
  * `jQuery <https://jquery.com/>`_
  * `Sugar <https://sugarjs.com/>`_
  * `less <http://less-ja.studiomohawk.com/>`_

  また、UI開発基盤は、設計工程からJSPを作成するアプローチを採用しているため、「モックアップHTMLとJSPのダブルメンテナンス」が発生しないようにみえる。 |br|
  しかし、実際は設計工程と開発工程で全く同じJSPを使用することは困難であるため、「設計工程用JSPと開発工程用JSPのダブルメンテナンス」が往々にして発生するという点にも注意が必要である。


.. toctree::
  :maxdepth: 1

  doc/index
  guide/index
  guide/widget_usage/widget_list

`ソースコード <https://github.com/nablarch/nablarch-plugins-bundle>`_


.. |br| raw:: html

  <br />