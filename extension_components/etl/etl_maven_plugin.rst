ETL Mavenプラグイン
====================================================================================================

.. contents:: 目次
  :depth: 3
  :local:

:ref:`etl` のExtractフェーズで使用する、Oracle SQL*Loader用のコントロールファイルの自動生成を行うMavenプラグインを提供する。

このプラグインを使用することで、入力ファイル及びワークテーブルに対応した
Java Beansクラスを元に、Oracle SQL*Loader用のコントロールファイルが生成できる。
また、本プラグインはMavenプラグインとして提供するため、buildプロセス上に本プラグインを組み込むことができる。

なお、本プラグインはCSVフォーマット以外の形式には対応していない。

プラグインの実行イメージは以下のとおり。

.. image:: images/etl_maven_plugin.png
  :scale: 80

|

モジュール一覧
---------------------------------------------------------------------
.. code-block:: xml

  <plugin>
    <groupId>com.nablarch.etl</groupId>
    <artifactId>nablarch-etl-maven-plugin</artifactId>
  </plugin>

使用方法
---------------------------------------------------------------------

コントロールファイルを生成するための設定を行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

指定したJava Beansクラスに設定された情報から、コントロールファイルを生成するために必要な情報を取得する。

Java Beansクラスから取得する情報は以下のとおり。

========================================  ==================================================
取得する情報                              取得元
========================================  ==================================================
ワークテーブル名                          :java:extdoc:`Table <javax.persistence.Table>` のname属性より取得する。

入力ファイルの文字コード                  :java:extdoc:`Csv <nablarch.common.databind.csv.Csv>` のtype属性より取得する。

入力ファイルのヘッダレコードの有無        :java:extdoc:`Csv <nablarch.common.databind.csv.Csv>` のtype属性より取得する。

入力ファイルの項目の囲み文字              :java:extdoc:`Csv <nablarch.common.databind.csv.Csv>` のtype属性より取得する。

入力ファイルのフィールドの区切り文字      :java:extdoc:`Csv <nablarch.common.databind.csv.Csv>` のtype属性より取得する。

入力ファイルのレコードの区切り文字        :java:extdoc:`Csv <nablarch.common.databind.csv.Csv>` のtype属性より取得する。

入力ファイルの項目名リスト                :java:extdoc:`Csv <nablarch.common.databind.csv.Csv>` のproperties属性より取得する。
========================================  ==================================================

Java Beansクラスの実装例を以下に示す。

.. code-block:: java

  @Entity
  @Table(name = "sample_work")
  @Csv(
          type = CsvType.DEFAULT,
          properties = {"userId", "name"}
  )
  public class Sample extends WorkItem {

      private String userId;

      private String name;

      // getter、setterは省略
  }


続いて、pom.xmlにプラグインの設定を行う。

pom.xmlへの設定例を以下に示す。

ポイント
  * ``classes`` にはコントロールファイル生成対象のJava Beansクラス名をFQCNで指定する。
  * ``outputPath`` にはコントロールファイルの出力先ディレクトリを指定する。
    未指定の場合は、``target/etl/ctrl-file`` に出力される。

.. code-block:: xml

  <plugin>
    <groupId>com.nablarch.etl</groupId>
    <artifactId>nablarch-etl-maven-plugin</artifactId>
    <version>1.0.0</version>
    <configuration>
      <!-- JavaBeansクラス名(FQCN) -->
      <classes>
        <param>sample.Bean1</param>
        <param>sample.Bean2</param>
      </classes>
      <!-- 出力先ディレクトリ -->
      <outputPath>etl/ctrl-file</outputPath>
    </configuration>
  </plugin>

コントロールファイルを生成する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

本プラグインの ``generate-ctrl-file`` ゴールを実行することでコントロールファイルが生成される。

.. code-block:: bat

  mvn nablarch-etl:generate-ctrl-file

.. important::

  本プラグインは、Java Beansクラスのclassファイルを元にコントロールファイルを生成する。
  そのため、プラグイン実行前に必ずcompileを実施すること。

コンパイル時に自動的にコントロールファイルを生成する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

コンパイル時に自動的に本プラグインを実行するように設定することで、
入力ファイルの仕様変更等でJava Beansクラスの定義を修正するたびに手動で本プラグインを実行する手間を省くことができる。

pom.xmlへの設定例を以下に示す。

.. code-block:: xml

  <plugin>
    <groupId>com.nablarch.etl</groupId>
    <artifactId>nablarch-etl-maven-plugin</artifactId>
    <version>1.0.0</version>
    <configuration>
      <!-- 省略 -->
    </configuration>
    <executions>
      <execution>
        <id>generate-ctrl-file</id>
        <phase>compile</phase>
        <goals>
          <goal>generate-ctrl-file</goal>
        </goals>
      </execution>
    </executions>
  </plugin>
