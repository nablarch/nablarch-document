==============================================
テスティングフレームワーク
==============================================


.. toctree::
   :maxdepth: 1
   :titlesonly:

   guide/development_guide/05_UnitTestGuide/index
   guide/development_guide/06_TestFWGuide/index
   guide/development_guide/08_TestTools/index

テスティングフレームワークを使用して機能のテストを実装するテストの実装者は :ref:`unitTestGuide` を、
テスティングフレームワークの導入をするアーキテクトは :ref:`testFWGuide` を参照してください。

.. important::

  テスティングフレームワークは、以下の基盤やライブラリには対応していない。
  このため、これらの基盤やライブラリを使用するアプリケーションに対するテストは、 `JUnit(外部サイト、英語) <http://junit.org>`_ などのテスティングフレームワークを使用して行うこと。

  * :ref:`JSR352に準拠したバッチアプリケーション <jsr352_batch>`
  * :ref:`Bean Validation <bean_validation>`

.. important::

  テスティングフレームワークは、マルチスレッド機能に対応していない。
  マルチスレッド機能のテストは、テスティングフレームワークを使用しないテスト(結合テストなど)で行うこと。
