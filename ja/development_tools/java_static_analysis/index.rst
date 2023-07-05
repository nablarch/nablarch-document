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

Inspectionを行う
------------------

IntelliJ IDEAには静的検査を行う `Inspection機能(外部サイト) <https://www.jetbrains.com/help/idea/code-inspection.html>`_ があり、Javaコーディングの慣例に沿っているか、潜在的なバグが含まれていないかなどをチェックし、リアルタイムに警告してくれる。

Inspectionはデフォルトで、一般的に注意すべき点について警告する設定となっている。

プロジェクトで規約を策定している場合は、プロジェクトに適した設定に変更することで、Inspectionをより有効に活用することができる。
変更した設定はエクスポートおよびインポートすることで、プロジェクトの開発者間で共有することができる。
エクスポートおよびインポートの方法については `プロファイルの構成(外部サイト) <https://www.jetbrains.com/help/idea/customizing-profiles.html>`_ を参照。

.. _code-format:

フォーマットを統一する
----------------------

IntelliJ IDEAのコードフォーマッター機能を使用することで、プロジェクトでコードスタイルを統一することができる。
使用方法については `JavaスタイルガイドのJavaコードフォーマッター解説 <https://github.com/Fintan-contents/coding-standards/blob/main/java/code-formatter.md>`_ を参照。

.. _api-analysis:

許可していないAPIが使用されていないかチェックする
-------------------------------------------------

このチェックにはIntelliJ IDEAのプラグインとIntelliJ IDEAに依存しないSpotBugsプラグインの2種類のツールを提供している。

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
nablarch-intellij-pluginを使用する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
`nablarch-intellij-plugin <https://github.com/nablarch/nablarch-intellij-plugin>`_ はNablarch開発を支援するためのIntelliJ IDEA用のプラグインであり、下記の機能を有している。

* Nablarch非公開APIが使用されている場合に警告を出す
* ブラックリストに登録したJava APIが使用されている場合に警告を出す

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
使用不許可APIチェックツールを使用する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
使用不許可APIチェックツールはSpotBugsのプラグインとして作成されたツールである。
詳細な仕様と実行方法は `Javaスタイルガイドの使用不許可APIチェックツール解説 <https://github.com/Fintan-contents/coding-standards/blob/main/java/staticanalysis/unpublished-api/README.md>`_ を参照。

なお、ブランクプロジェクトには `Mavenで実行するための設定 <https://github.com/Fintan-contents/coding-standards/blob/main/java/staticanalysis/spotbugs/docs/Maven-settings.md>`_ をあらかじめ設定してあるため、すぐにチェックを実施することが可能である。
