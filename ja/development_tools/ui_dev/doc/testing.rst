=====================================
基盤部品のテスト実施項目
=====================================
本節では、UI開発基盤が提供する各種部品に対して実施しているテストの内容について述べる。

.. tip::
  **プロジェクト側のカスタマイズに伴うテストの実施について**
    各プロジェクトにおいて、既存の部品を修正もしくは新規に追加した場合は、
    その内容にもよるが、基本的に下記に示すものと同等の観点でテストを実施する必要がある。

.. tip::
  現状のテスト実施内容は打鍵作業に大きく依存しているが、
  今後サポートデバイス増加に伴うリグレッションテストの工数を抑えるために、自動化を進めることを計画している。
  このため、以下で述べる作業内容は今後変更される可能性がある。
  また、自動化されたテストケースはプロジェクト側でカスタマイズを行った際のリグレッションテストとして流用可能となる予定である。



-------------------------------
テスト方針
-------------------------------
基本的には :doc:`internals/jsp_widgets` に対するブラックボックステスト [#]_ を実施する。
すなわち、各ウィジェットが :doc:`reference_jsp_widgets/index` で定義される外部仕様を満たし、
**UI標準** に準拠した表示となることを検証する。

各ウィジェットが内部的に使用する :doc:`internals/js_framework` :doc:`internals/css_framework` については
上記のテストの実施によって間接的に検証されるものとし、個別のテストは行わない。

また、上記に加えて、性能テスト、サンプルアプリケーションを用いた結合テストを実施する。

.. [#]
  以下の事由によりホワイトボックス的なテストケースの抽出は行っていない。
   
  :doc:`internals/js_framework` , :doc:`internals/inbrowser_jsp_rendering` 
    現状ではJavaScriptで実装された部分のカバレッジを集計する方法が確立しておらず
    効率的なテストケース抽出および、テスト網羅性の評価が実施できないため、今回のリリースでは実施を見送っている。
    今後、テスト基盤を整備し実施する予定である。
   
  :doc:`internals/jsp_widgets` 
    各ウィジェットの実体はJSPタグファイルであるため、そもそも複雑なロジックは記述できない。
    ブラックボックステストで十分な網羅性が得られると判断できるため。




.. _ui_testing_environment:

-------------------------------
テスト実施環境
-------------------------------
UI開発基盤が提供する各モジュールは、以下の環境でテストを実施している。

+----------------------+-----------------------+------------------------+-------------------+--------------------------------------+
| 端末                 | OS                    | ブラウザ               | 表示モード        | 実施テストパターン                   |
+======================+=======================+========================+===================+======================================+
| PC                   | Windows 10 Pro |br|   | IE11                   | ワイド            | **A**                                |
|                      | (ビルド番号16299)     +------------------------+-------------------+--------------------------------------+
|                      |                       | Firefox                | ワイド            | **A**                                |
|                      |                       +------------------------+-------------------+--------------------------------------+
|                      |                       | Chrome                 | ワイド            | **A**                                |
+----------------------+-----------------------+------------------------+-------------------+--------------------------------------+
| Macintosh            | OSX 10.9.5            | safari                 | ワイド            | **A**                                |
+----------------------+-----------------------+------------------------+-------------------+--------------------------------------+
| iPhone 5             | iOS 10.3.3            | mobile safari          | ナロー(縦、横)    | **B**                                |
+----------------------+-----------------------+------------------------+-------------------+--------------------------------------+
| iPad (第4世代)       | iOS 10.3.3            | mobile safari          | コンパクト(縦)    | **B**                                |
+                      +                       +                        +-------------------+                                      +
|                      |                       |                        | ワイド(横)        |                                      |
+----------------------+-----------------------+------------------------+-------------------+--------------------------------------+
| Nexus 7 (2012)       | Android 5.1.1         | Chrome                 | ナロー(縦)        | **B**                                |
+                      +                       +                        +-------------------+                                      +
|                      |                       |                        | コンパクト(横)    |                                      |
+----------------------+-----------------------+------------------------+-------------------+--------------------------------------+


==================== ============================================
実施テストパターン   実施テスト                                  
==================== ============================================
**A**                - UI部品ウィジェット機能テスト             
                     - UI部品ウィジェット性能テスト
                     - UI部品ウィジェット組み合わせテスト
                     - 結合テスト 
                     - ローカル表示テスト 

**B**                - UI部品ウィジェット機能テスト               
                     - UI部品ウィジェット性能テスト
                     - UI部品ウィジェット組み合わせテスト
                     - 結合テスト 
                     - 表示方向切替えテスト

==================== ============================================


-------------------------------
実施テスト内容
-------------------------------
各実施テストの内容は以下のとおり。


UI部品ウィジェット機能テスト
---------------------------------
:doc:`internals/jsp_widgets` に対し以下の観点による単体テストを行う。

- 各ウィジェットの挙動が :doc:`reference_jsp_widgets/index` で記述している外部仕様に準拠していること。
- 各ウィジェットの表示が **UI標準** に記載されている対応するUI部品の仕様に準拠すること。

機能テストは、各ウィジェットに定義されている属性値ごとに実施し、少なくとも以下の内容を確認する。

- HTMLの属性値が期待通りに設定されていることを、画面ソースコード、もしくはインスペクタを使用して確認する。
- ウィジェットの表示が仕様に従っていることを目視確認する。

なお、一部のテストケースでは前者の確認作業を自動化している。
その場合は後者の表示確認のみを行えばよい。


UI部品ウィジェット性能テスト
-----------------------------------
:doc:`internals/jsp_widgets` を1画面内に非常に多く配置した場合でも問題なく動作することを検証するテストを行う。
具体的には、以下の基準を満たすことを検証する。

画面内に300個のウィジェットを配置した画面について、

1. 画面ロードが完了しユーザ操作が可能となるまで1秒以内で完了すること。
   (ロード時間は、リクエストの発行からロードイベントの発火までの時間をブラウザのデフォルトプロファイラを用いて計測する。
   サーバ処理は単に折り返すのみとし、ローカルサーバを使用する。 

2. 画面ロード後の画面操作で、JavaScriptスレッドの処理待ち(カーソルが渦巻き型に変化する)が発生しないこと。
  
.. tip::
 **性能テストにおける画面項目数の基準値について**

 一般的に入力項目数が極端に増加すると、ユーザビリティが極端に低下する。
 (1ページあたりの入力項目が多いと、ユーザの離脱率が高まる。また、
 画面を誤ってクローズした場合などに入力項目が全て消失する危険性がある)
 このため、 **UI標準** では、一画面内の入力項目の上限を100件程度としており、
 これに3倍の安全率をかけた数値をテスト基準値としている。
   

UI部品ウィジェット組み合わせテスト
-----------------------------------------
他のUI部品の干渉する可能性のある部品について組み合わせて使用しても問題が発生しないことを検証する。
(例: タブと開閉可能領域、readonly機能とプレースホルダー機能など)


結合テスト
-----------------
Nablarchのサンプルアプリケーションを用いて、サーバサイドの完全な実装を含んだアプリケーションとしての
ストーリーテストを実施する。


ローカル表示テスト
----------------------
:doc:`internals/inbrowser_jsp_rendering` によるローカル表示のテストを行う。
テスト内容は **UIウィジェット機能テスト** のテストJSPをローカル表示し
:doc:`reference_jsp_widgets/index` で記載されている仕様どおりに動作することを検証する。


表示方向切替えテスト
---------------------------
各モバイルデバイスについて、縦持ち、横持ちを切替えた際に
画面の表示モードが **UI標準** で定義された表示モードに切り替わることを確認する。


.. |br| raw:: html

  <br />