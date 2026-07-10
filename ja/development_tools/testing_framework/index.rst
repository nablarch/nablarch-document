==============================================
テスティングフレームワーク
==============================================


.. toctree::
   :maxdepth: 1
   :titlesonly:

   guide/development_guide/06_TestFWGuide/index
   guide/development_guide/05_UnitTestGuide/index

テスティングフレームワークの仕組み・設定・導入を行うアーキテクトは :ref:`testFWGuide` を、
テストの実装方法・テストデータの記述方法を確認する開発者は :ref:`unitTestGuide` を参照。

.. important::

  テスティングフレームワークは、以下の基盤やライブラリには対応していない。
  このため、これらの基盤やライブラリを使用するアプリケーションに対するテストは、 `JUnit(外部サイト、英語) <https://junit.org/junit5/>`_ などのテスティングフレームワークを使用して行うこと。

  * :ref:`Jakarta Batchに準拠したバッチアプリケーション <jsr352_batch>`

.. important::

  テスティングフレームワークは、マルチスレッド機能に対応していない。
  マルチスレッド機能のテストは、テスティングフレームワークを使用しないテスト(結合テストなど)で行うこと。
