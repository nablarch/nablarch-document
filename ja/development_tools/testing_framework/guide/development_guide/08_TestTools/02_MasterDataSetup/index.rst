=======================
 マスタデータ投入ツール
=======================

.. tip::

  :ref:`blank_project` を使用してプロジェクトを構築した場合、 データベース関連のツールとして :ref:`gsp-dba-maven-plugin <gsp-maven-plugin>` が設定される。

  このため、データベースに対するマスタデータの投入は、本ツールではなく :ref:`gsp-dba-maven-plugin  <gsp-maven-plugin>` の使用を推奨する。

.. important::

  本ツールは、マルチスレッド機能には対応していない。
  マルチスレッド機能のテストは、テスティングフレームワークを使用しないテスト(結合テストなど)で行うこと。

.. toctree::
   :maxdepth: 1
   
   ./01_MasterDataSetupTool
   ./02_ConfigMasterDataSetupTool

