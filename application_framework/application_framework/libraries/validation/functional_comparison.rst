.. _`validation-functional_comparison`:

Bean ValidationとNablarch Validationの機能比較
----------------------------------------------------------------------------------------------------
ここでは、Nablarchの提供するバリデーション機能と |jsr349| の機能比較を示す。

.. list-table:: 機能比較（○：提供あり　△：一部提供あり　×：提供なし　－:対象外）
  :header-rows: 1
  :class: something-special-class

  * - 機能
    - Bean |br| Validation
    - Nablarch |br| Validation
    - JSR 349
  * - バリデーション対象の項目を指定できる
    - ○ [#property_validation]_
    - ○ |br| :ref:`解説書へ <nablarch_validation-execute>`
    - ○
  * - 階層構造を持つJava Beansオブジェクトに |br| 対してバリデーションできる
    - ○ [#jsr]_
    - ○ |br| :ref:`解説書へ <nablarch_validation-nest_bean>`
    - ○
  * - メソッドの引数、戻り値に対してバリデーションできる
    - × [#method]_
    - × [#method]_
    - ○
  * - 相関バリデーションができる
    - ○ |br| :ref:`解説書へ <bean_validation-correlation_validation>`
    - ○ |br| :ref:`解説書へ <nablarch_validation-correlation_validation>`
    - ○
  * - バリデーションの実行順序を指定できる
    - × [#order]_
    - ○ |br| :ref:`解説書へ <nablarch_validation-execute>`
    - ○
  * - 特定の項目の値を条件に |br| バリデーション項目を切り替えることが出来る
    - ○ [#conditional]_
    - ○ |br| :ref:`解説書へ <nablarch_validation-conditional>`
    - ○
  * - エラーメッセージに埋め込みパラメータを使用できる
    - ○ [#parameter]_ |br| :ref:`解説書へ <message>`
    - ○ |br| :ref:`解説書へ <message>`
    - ○
  * - ドメインバリデーションができる
    - ○ |br| :ref:`解説書へ <bean_validation-domain_validation>`
    - ○ |br| :ref:`解説書へ <nablarch_validation-domain_validation>`
    - ×
  * - 値の型変換ができる
    - × [#type_converter]_
    - ○ |br| :ref:`解説書へ <nablarch_validation-definition_validator_convertor>`
    - ×
  * - 値の正規化ができる
    - × [#normalized]_
    - ○ |br| :ref:`解説書へ <nablarch_validation-definition_validator_convertor>`
    - ×
  * - エラーメッセージに項目名を埋め込むことができる
    - ○ |br| :ref:`解説書へ <bean_validation-property_name>`
    - ○ |br| :ref:`解説書へ <nablarch_validation-property_name>`
    - ×

.. [#property_validation] Formの全ての項目に対してバリデーションを行うことで、不正な入力値の受付を防ぐことが出来る。 |br|
    このため、Bean Validationでは、項目指定のバリデーション実行は推奨していない。 |br|
    どうしても指定の項目に対してのみバリデーションを行いたい場合には、
    :java:extdoc:`ValidatorUtil#validate <nablarch.core.validation.ee.ValidatorUtil.validate(java.lang.Object, java.lang.String...)>` を使用すること。
    
.. [#jsr] 対応方法は、 |jsr349| の仕様に準拠する。
.. [#method] Nablarchでは外部からデータを受け付けたタイミングで必ずバリデーションを行うため、
   メソッドの引数や戻り値に対するバリデーションには対応していない。
.. [#order] バリデーションの実行順を制御することはできないため、バリデーションの実行順序を期待するような実装は行わないこと。
   例えば、項目毎のバリデーション後に相関バリデーションが実行されるといったことを期待してはならない。
.. [#conditional]  |jsr349| のクラスレベルのバリデーション機能を使用して、ロジックによりバリデーション項目を切り替えること。
.. [#parameter] Bean Validationでは、EL式を使用してパラメータを埋め込むこともできる。
.. [#type_converter] Bean Validationでは、プロパティの型は全てStringとして定義する(:ref:`Stringで定義する理由 <bean_validation-form_property>`)ため型変換は行わない。
   型変換が必要な場合には、バリデーション実施後に :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` を使って型変換を行う。
.. [#normalized] 正規化は、Bean Validationの機能ではなくハンドラとして提供している。正規化が必要な場合には、 :ref:`normalize_handler` を使用して行う。

.. |jsr349| raw:: html

   <a href="https://jcp.org/en/jsr/detail?id=349" target="_blank">JSR349(外部サイト、英語)</a>

.. |br| raw:: html

   <br />
