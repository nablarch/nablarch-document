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

Nablarch開発に使用したInspectionの設定ファイルをプロジェクト向けに提供している。
以下のファイルをダウンロードし ``PROJECT_ROOT/.idea/inspectionProfiles`` 配下に配置することでInspectionの設定が適用される。

:download:`設定ファイル<download/Project_Default.xml>`

.. important::
  開発者間で同一の構文チェックが行われるようにするため、Inspectionの設定ファイルはVCSの管理対象とすること。
  
.. important::
  Inspectionの設定内容は、警告された箇所から参照可能で、IDE上で効率よく確認できる。そのため、チェック内容の一覧など、別資料を作らないこと。

.. tip::
  InspectionはPJで必要に応じてカスタマイズすることができる。
  カスタマイズした設定は ``PROJECT_ROOT/.idea/inspectionProfiles`` 配下の設定ファイルに反映される。

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
詳細は、IntelliJの `マニュアル <https://www.jetbrains.com/idea/documentation/>`_ を参照。

.. important::
  Code Styleの設定内容は、IDE上で効率よく確認できる。そのため、コーディング規約など、別資料を作らないこと。

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
コミット前に自動でフォーマットを統一する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
IntelliJ IDEAでは、VCSへのコミット時にコミット対象のファイルに対してフォーマット処理を行う機能を有している。
これを有効活用することで、確実にCode Styleに従ったコードをコミットできる。

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
詳細な仕様と実行方法は `Nablarchスタイルガイドの解説 <https://github.com/nablarch-development-standards/nablarch-style-guide/blob/master/java/staticanalysis/unpublished-api/README.md>`_ を参照。
なお、ブランクプロジェクトには `Mavenで実行するための設定 <https://github.com/nablarch-development-standards/nablarch-style-guide/blob/master/java/staticanalysis/spotbugs/docs/Maven-settings.md>`_ をあらかじめ設定してあるため、すぐにチェックを実施することが可能である。
