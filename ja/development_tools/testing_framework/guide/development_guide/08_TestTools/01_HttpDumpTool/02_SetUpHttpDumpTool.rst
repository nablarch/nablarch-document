=================================================
リクエスト単体データ作成ツール インストールガイド
=================================================

:doc:`index`\ のインストール方法について説明する。

.. _http_dump_tool_prerequisite:

前提事項
========

本ツールを使用する際、以下の前提事項を満たす必要がある。

* 以下のツールがインストール済みであること

  * Java
  * Maven

* プロジェクトがMavenで管理されていること
* htmlファイルがブラウザに関連付けされていること
* ブラウザのプロキシ設定で、localhostが除外されていること

提供方法
==================

本ツールは以下のjarにて提供する。

* nablarch-testing-XXX.jar
* nablarch-testing-jetty12-XXX.jar

そのため、pom.xmlのdependencies要素以下の記述があることを確認する。

.. code-block:: xml

  <dependencies>
    <!-- 中略 -->
    <dependency>
      <groupId>com.nablarch.framework</groupId>
      <artifactId>nablarch-testing</artifactId>
      <scope>test</scope>
    </dependency>
    <dependency>
      <groupId>com.nablarch.framework</groupId>
      <artifactId>nablarch-testing-jetty12</artifactId>
      <scope>test</scope>
    </dependency>
    <!-- 中略 -->
  </dependencies>

プロジェクトのディレクトリで以下のコマンドを実行し、jar ファイルをダウンロードする。

.. code-block:: text

  mvn dependency:copy-dependencies -DoutputDirectory=lib


以下のファイルをプロジェクトのpom.xmlと同じディレクトリに配置する。

* :download:`httpDump.bat <download/httpDump.bat>`


Eclipseとの連携
===============

以下の設定をすることでEclipseから本ツールを起動できる。


設定画面起動
------------

ツールバーから、ウィンドウ(Window)→設定(Prefernce)を選択する。
左側のペインから一般(General)→エディタ(Editors)→ファイルの関連付け(File Associations)
を選択、右側のペインから*.htmlを選択し、追加(Add)ボタンを押下する。

.. image:: ./_image/01_Eclipse_Preference.png
   :scale: 100

 
外部プログラム選択
------------------

ラジオボタンから外部プログラム(External program)を選択し、参照(Browse)ボタンを押下する。

.. image:: ./_image/02_Eclipse_EditorSelection.png
   :scale: 100


起動用バッチファイル（シェルスクリプト）選択
--------------------------------------------

Windowsの場合はバッチファイル(httpDump.bat)を、
Linuxの場合はシェルスクリプト(httpDump.sh)を選択する。

.. image:: ./_image/03_Eclipse_OpenFile.png
   :width: 100%


.. _howToExecuteFromEclipse:

HTMLファイルからの起動方法
--------------------------

Eclipseのパッケージエクスプローラ等からHTMLファイルを右クリックし、
httpDumpで開くことでツールを起動できる。

.. image:: ./_image/04_Eclipse_OpenWith.png
   :scale: 100

.. |br| raw:: html

  <br/>