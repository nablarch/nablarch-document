.. -*- mode: rst; coding: utf-8-unix -*-

===============================================
JDK7及び8でFindBugsを使用するための設定について
===============================================

.. contents:: 目次
  :depth: 2
  :local:

アーキタイプから生成したブランクプロジェクトには、JDK7及び8でFindBugsが使用できるように設定されている。

しかし、使用するJDKのバージョンによって、Findbugsの設定は変更が必要となる可能性があるため、デフォルトでどのように設定されているかについて説明する。



設定内容
===========================

----------------------------
pom.xmlの設定
----------------------------

依存するFindBugsのバージョンの設定
----------------------------------

dependencies要素内にFindBugsへの依存が記述されている。

以下にデフォルトの設定内容を示す。

.. code-block:: xml

  <dependencies>
    <!-- 中略 -->
    <dependency>
      <groupId>com.google.code.findbugs</groupId>
      <artifactId>findbugs</artifactId>
      <version>3.0.1</version>
      <scope>test</scope>
    </dependency>
  </dependencies>

.. tip::

  Nablarchのアーキタイプで生成したプロジェクトは、FindBugsをAnt経由で実行するように構成されているため、dependencies要素に依存が記述されている。


-------------------------------------
tools/nablarch-findbugs.xmlの設定
-------------------------------------

参照するライブラリの設定
--------------------------------

nablarch-findbugs.xmlにFindbugs用のクラスパス設定( ``path id="classpath.findbugs"`` の要素)が存在する。

以下にデフォルトの設定内容を示す。

.. code-block:: xml

  <path id="classpath.findbugs">
    <pathelement location="${com.google.code.findbugs:findbugs:jar}" />
    <pathelement location="${com.google.code.findbugs:bcel-findbugs:jar}" />
    <pathelement location="${com.google.code.findbugs:jFormatString:jar}" />
    <pathelement location="${com.google.code.findbugs:jsr305:jar}" />

    <pathelement location="${org.ow2.asm:asm:jar}" />
    <pathelement location="${org.ow2.asm:asm-commons:jar}" />
    <pathelement location="${org.ow2.asm:asm-tree:jar}" />

    <pathelement location="${commons-lang:commons-lang:jar}" />
    <pathelement location="${dom4j:dom4j:jar}" />
    <pathelement location="${jaxen:jaxen:jar}" />
  </path>
