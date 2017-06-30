.. _utility:

汎用ユーティリティ
==================================================

.. contents:: 目次
  :depth: 3
  :local:

本フレームワークで提供している、汎用的に利用できるユーティリティクラスを以下に示す。

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 20,20,60

  * - クラス名
    - モジュール名
    - 概要

  * - :java:extdoc:`DateUtil <nablarch.core.util.DateUtil>`
    - nablarch-core
    - 日付に関する機能を提供する

  * - :java:extdoc:`FileUtil <nablarch.core.util.FileUtil>`
    - nablarch-core
    - ファイルの取り扱いに関する機能を提供する

  * - :java:extdoc:`ObjectUtil <nablarch.core.util.ObjectUtil>`
    - nablarch-core
    - オブジェクトの取り扱いに関する機能を提供する

  * - :java:extdoc:`StringUtil <nablarch.core.util.StringUtil>`
    - nablarch-core
    - 文字列に関する機能を提供する

  * - :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>`
    - nablarch-core-beans
    - Java Beansクラスに関する機能を提供する。プロパティを扱う際の型変換ルールについては :ref:`utility-conversion` を参照。

  * - :java:extdoc:`Base64Util <nablarch.core.util.Base64Util>`
    - nablarch-fw
    - Base64エンコーディングに関する機能を提供する

  * - :java:extdoc:`BinaryUtil <nablarch.core.util.BinaryUtil>`
    - nablarch-fw-web-extension
    - バイナリに関する機能を提供する

.. _utility-conversion:

BeanUtilの型変換ルール
--------------------------------------------------
:java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` では、Java BeansオブジェクトやMapオブジェクトから
別のJava Beansオブジェクトにデータ移行する際にプロパティの型変換を行っている。

なお、MapオブジェクトからJava Beansオブジェクトにデータ移行する場合、
Mapオブジェクトのキーに ``.`` が含まれていればそのプロパティをネストオブジェクトとして扱う。

型変換ルールについては、 :java:extdoc:`nablarch.core.beans.converter` パッケージ配下に配置されている
:java:extdoc:`Converter <nablarch.core.beans.Converter>` 実装クラスをそれぞれ参照すること。

.. important::

  デフォルトで提供する型変換ルールでは、精度の小さい型への変換を行った場合(例えばLongからIntegerへの変換)で、変換先の精度を超えるような値を指定しても正常に処理を終了する。
  このため、BeanUtilを使用してコピーを行う際には、コピーする値がシステムで許容されているかどうかを :ref:`validation` によって事前に検証しておく必要がある。
  検証を行わなかった場合、不正な値がシステムに取り込まれ障害の原因となる可能性がある。

.. _utility-conversion-add-rule:

型変換ルールを追加する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

型変換ルールを追加するには、以下の手順が必要となる。

1. :java:extdoc:`Converter <nablarch.core.beans.Converter>` の実装クラスを作成し、:java:extdoc:`Converter#convert <nablarch.core.beans.Converter.convert(java.lang.Object)>` に変換処理を実装する。
2. :java:extdoc:`ConversionManager <nablarch.core.beans.ConversionManager>` の実装クラスを作成する。
   今回は標準の型変換ルールに追加でルールを設定するため、 :java:extdoc:`ConversionManager <nablarch.core.beans.ConversionManager>` をプロパティとして持つ、
   :java:extdoc:`ConversionManager <nablarch.core.beans.ConversionManager>` の実装クラスを作成する。

  .. code-block:: java

    public class SampleConversionManager implements ConversionManager {

        private ConversionManager delegateManager;

        @Override
        public Map<Class<?>, Converter<?>> getConverters() {
            Map<Class<?>, Converter<?>> converters = new HashMap<Class<?>, Converter<?>>();

            // 標準のコンバータ
            converters.putAll(delegateManager.getConverters());

            // 今回作成したコンバータ
            converters.put(BigInteger.class, new CustomConverter());

            return Collections.unmodifiableMap(converters);
        }

        public void setDelegateManager(ConversionManager delegateManager) {
            this.delegateManager = delegateManager;
        }
    }

3. コンポーネント設定ファイルに、 :java:extdoc:`ConversionManager <nablarch.core.beans.ConversionManager>` の実装クラスを設定する。

   ポイント
    * コンポーネント名は **conversionManager** とすること。

   .. code-block:: xml

    <component name="conversionManager" class="sample.SampleConversionManager">
      <property name="delegateManager">
        <component class="nablarch.core.beans.BasicConversionManager" />
      </property>
    </component>