.. _validation:

入力値のチェック
==================================================
クライアントから送信されるユーザ入力値や、システム間連携により外部システムから送信される値が妥当かを検証するための機能を提供する。

入力値のチェックでは以下のことを行う。

* 入力値が妥当な形式かどうか(例えば、桁数や文字種などのチェック)
* システムの状態に適合しているかどうか(例えば、アカウントの重複登録チェック)

※入力値のチェックでエラーとなった場合に表示するメッセージの定義方法は、 :doc:`message` を参照。

Nablarchでは、以下の2種類のバリデーション機能を提供している。

.. toctree::
  :maxdepth: 1

  Java EE7のBean Validation(JSR349)に準拠したバリデーション機能 (Bean Validation) <validation/bean_validation>
  Nablarch独自のバリデーション機能 (Nablarch Validation) <validation/nablarch_validation>

どちらの機能を使用しても入力値のチェックは行えるが、以下の理由によりJava EE7に準拠した機能を使用することを推奨する。

* Bean ValidationはJava EEで仕様が定められており情報が豊富である。
* 開発者がNablarch独自のバリデーションの使い方などを覚える必要がない。

.. tip::
 :ref:`bean_validation` と :ref:`nablarch_validation` で提供している機能の違いは、 :ref:`validation-functional_comparison` を参照。

.. toctree::
  :hidden:

  validation/functional_comparison
