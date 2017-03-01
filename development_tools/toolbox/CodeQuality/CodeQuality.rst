
==========================
コード品質と保守性を高める
==========================

.. contents:: 目次
  :depth: 1
  :local:

--------
概要
--------

コードの品質と保守性を高めるための観点として下記の３つが挙げられる。

* Javaコーディングの慣例に沿っていること
* 正しいインデントが施されていること
* 許可したAPIのみが使用されていること

これらのチェックに、従来ではCheckStyleやFindbugsを用いていたが、フィートバックが遅いという問題点があった。
そこでIDEの機能を活用し、コーディング中にリアルタイムに警告を出すことで手戻りを無くし、品質と保守性を高めていくといった方法を推奨している。
それを実現するために :ref:`intellij-idea` と :ref:`nab-intellij-plugin` を使用する。

.. _intellij-idea:

--------------
IntelliJ IDEA
--------------

Nablarchでは、JetBrains社製のIDEである `IntelliJ IDEA(外部サイト) <https://www.jetbrains.com/idea/>`_ の使用を推奨している。
IntelliJ IDEAの下記機能を用いることにより、冒頭で述べた「Javaコーディングの慣例に沿っていること」及び「正しいインデントが施されていること」が担保できる。
なお、これらの機能はPJで必要に応じてカスタマイズすることができる。

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 1,2

  * - 機能
    - 概要
  * - 静的検査機能
    - ソースコードの構文が正しいか、潜在的なバグが含まれていないかなどをチェックしリアルタイムに警告する機能。
  * - フォーマット機能
    - ソースコードに適切なインデントを施す機能。コミット時に自動でフォーマットをかけるなどの設定も行える。
    
.. tip::
   Nablarchアーキタイプから生成した :ref:`blank_project` には、Nablarch開発で使用した静的検査機能の設定が適用されている。
   
.. tip::
   静的検査機能をCI(Jenkins)で実行することができる。設定方法は、 `こちら(外部サイト) <http://siosio.hatenablog.com/entry/2016/12/23/212140>`_ を参照。

.. _nab-intellij-plugin:

----------------------------
nablarch-intellij-plugin
----------------------------

nablarch-intellij-pluginは許可していないAPIが使用されていないことをチェックするIntelliJ IDEA用のプラグインである。
Nablarchの非公開APIとブラックリストに登録したJava APIが使用されていないかをチェックする。

詳細は、 `nablarch-intellij-plugin <https://github.com/nablarch/nablarch-intellij-plugin>`_ を参照。

