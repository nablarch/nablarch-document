==============================================
大規模開発向け重厚なテスティングフレームワーク
==============================================


.. toctree::
   :maxdepth: 1
   :numbered:
   :titlesonly:

   guide/development_guide/05_UnitTestGuide/index
   guide/development_guide/06_TestFWGuide/index
   guide/development_guide/08_TestTools/index

.. important::

  テスティングフレームワークは、以下の基盤やライブラリには対応していない。
  このため、これらの基盤やライブラリを使用するアプリケーションに対するテストは、 `JUnit(外部サイト、英語) <http://junit.org>`_ などのテスティングフレームワークを使用して行うこと。

  * :ref:`RESTfulウェブサービス <restful_web_service>`
  * :ref:`JSR352に準拠したバッチアプリケーション <jsr352_batch>`
  * :ref:`Bean Validation <bean_validation>`
