効率的なJava静的チェック
=========================

.. contents:: 目次
  :depth: 2
  :local:

コードの品質と保守性を高めるために次の３つを実践する。

* :ref:`code-analysis`
* :ref:`code-format`
* :ref:`api-analysis`

上記を行うために、NablarchではJetBrains社製のIDEである `IntelliJ IDEA(外部サイト) <https://www.jetbrains.com/idea/>`_ の使用を推奨している。
本ページでは、IntelliJ IDEAを用いた効率的なJava静的チェックの方法を説明する。

.. _code-analysis:

構文チェックを行う
------------------

構文のチェックには、IntelliJ IDEAの静的検査機能(Inspection)を使用する。
Inspectionは、Javaコーディングの慣例に沿っているか、潜在的なバグが含まれていないかなどをチェックし、リアルタイムに警告する機能である。
    
.. tip::

   InspectionはPJで必要に応じてカスタマイズすることができ、カスタマイズした設定は ``PROJECT_ROOT/.idea/inspectionProfiles`` 配下に設定ファイルとして追加される。
   Nablarchでは、Nablarch開発に使用したInspectionの設定ファイルを提供しており、
   Nablarchアーキタイプから生成した :ref:`blank_project` に設定ファイルが含まれている。
    
~~~~~~~~~~~~~~~~~
IDEでチェックする
~~~~~~~~~~~~~~~~~

IntelliJ IDEAのInspectionはデフォルトで設定が有効になっており、コードを書いた際にリアルタイムに実行される。
詳細は、IntelliJの `マニュアル <https://www.jetbrains.com/idea/documentation/>`_ を参照。


~~~~~~~~~~~~~~~~
CIでチェックする
~~~~~~~~~~~~~~~~

IntelliJ IDEAのInspectionは、CI(Jenkins)サーバでも実行することができる。
設定方法は `こちら(外部サイト) <http://siosio.hatenablog.com/entry/2016/12/23/212140>`_ を参照。

.. _code-format:

フォーマットを統一する
----------------------

フォーマットを統一するためには、IntelliJ IDEAのデフォルトのCode Styleを使用してフォーマットを行う。

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
コミット前に自動でフォーマットを統一する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
IntelliJ IDEAでは、VCSへのコミット時にコミット対象のファイルに対してフォーマット処理を行う機能を有している。
これを有効活用することで、確実にCode Styleに従ったコードをコミットできる。

詳細は、IntelliJの `マニュアル <https://www.jetbrains.com/idea/documentation/>`_ を参照。

.. _api-analysis:

許可していないAPIが使用されていないかチェックする
-------------------------------------------------

このチェックには、 `nablarch-intellij-plugin <https://github.com/nablarch/nablarch-intellij-plugin>`_ を使用する。
nablarch-intellij-pluginはNablarch開発を支援するためのIntelliJ IDEA用のプラグインであり、下記の機能を有している。

* Nablarch非公開APIが使用されている場合に警告を出す
* ブラックリストに登録したJava APIが使用されている場合に警告を出す

