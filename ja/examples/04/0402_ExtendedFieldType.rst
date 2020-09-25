======================================================
データフォーマッタ機能におけるフィールドタイプの拡張
======================================================

本サンプルで提供するフォーマッタ機能の仕様を解説する。

フォーマッタ機能の概要、基本となる汎用データフォーマット機能に関する詳細は、Nablarch Application Framework解説書の汎用データフォーマット機能に関する解説を参照すること。

----------------------------
概要
----------------------------

EBCDIC（CP930）のダブルバイト文字をデータ連携する場合に、
項目の前後にシフトコードを付与することがあるが、
ホストコンピュータとのデータ連携などでは、ダブルバイト文字であってもシフトアウト状態で始まっていることを想定しシフトコードを付与しないこともある。

このように、接続先のシステムとのインターフェースにより、シフトコードが付与される場合とされない場合があるため、それぞれに対応する必要がある。

そこで、本サンプルではシフトコード付きEBCDIC（CP930）のダブルバイト文字に対応するデータタイプクラスと、
シフトコード無しEBCDIC（CP930）のダブルバイト文字に対応するデータタイプクラスを提供する。

なお、Nablarchがデフォルトで提供しているダブルバイト文字列のデータタイプ(DoubleByteCharacterString)は、
ファイルの文字コードがShift_JISやMS932の場合に全角文字（ダブルバイト文字）フィールドの入出力に使用することを想定しているため、
EBCDIC（CP930）を扱う際には、各プロジェクトによる拡張が必要となる。

（シフトコードが付与されるかどうかは、JDKに依存するものであり、
JDKで使用されるCP930はダブルバイト文字に対して必ずシフトコードが付加されている必要がある。）

このデータタイプを使用すると、透過的にシフトコードの付加および除去を行うため、上記の差を吸収して文字列化したりバイトシーケンスにエンコードすることが可能となる。



提供パッケージ
--------------------------------------------------------------------

本機能は、下記のパッケージで提供される。

  *please.change.me.* **core.dataformat.convertor.datatype**


フィールドタイプの構成
--------------------------------------------------------------------

本サンプルでは、EBCDIC（CP930）の固定長ファイルの全角文字列の項目に
シフトコードが付与されている場合といない場合の両方に対応することを想定しているため、
下記のフィールドタイプのクラスを追加することとなる。

以下に本機能で使用するクラス一覧を記す。

  .. list-table::
   :widths: 130 150 200
   :header-rows: 1

   * - パッケージ名
     - クラス名
     - 概要
   * - *please.change.me.* **core.dataformat.** **convertor.datatype**
     - EbcdicDoubleByteCharacterString
     - | EBCDIC(CP930)のダブルバイト文字列に対応したデータタイプクラス。
       | 固定長のデータフォーマットの全角文字（ダブルバイト文字）フィールドの入出力に利用する。
       | 入出力のバイトデータに **シフトコードが付与されるケース** を想定しているデータタイプとして実装する。
   * - *please.change.me.* **core.dataformat.** **convertor.datatype**
     - EbcdicNoShiftCodeDoubleByteCharacterString
     - | EBCDIC(CP930)のダブルバイト文字列に対応したデータタイプクラス。
       | 固定長のデータフォーマットの全角文字（ダブルバイト文字）フィールドの入出力に利用する。
       | 入出力のバイトデータに **シフトコードが付与されないケース** を想定しているデータタイプとして実装する。



フィールドタイプの使用方法
--------------------------------------------------------------------
  追加したデータタイプクラスを使用する場合、以下の設定を行う必要がある。
  下記のサンプルでは、デフォルトの設定に、"ESN"と"EN"のデータタイプを追加している。

  .. code-block:: xml
  
    <component name="fixedLengthConvertorSetting"
        class="nablarch.core.dataformat.convertor.FixedLengthConvertorSetting">
      <property name="convertorTable">
        <map>
          <!-- EBCDIC(CP930)用のデータタイプ ESN, EN を追加する -->
          <entry key="ESN" value="please.change.me.core.dataformat.convertor.datatype.EbcdicDoubleByteCharacterString"/>
          <entry key="EN" value="please.change.me.core.dataformat.convertor.datatype.EbcdicNoShiftCodeDoubleByteCharacterString"/>
          
          <!-- 以下はデフォルト設定 -->
          <entry key="X" value="nablarch.core.dataformat.convertor.datatype.SingleByteCharacterString"/>
          <entry key="N" value="nablarch.core.dataformat.convertor.datatype.DoubleByteCharacterString"/>
          <entry key="XN" value="nablarch.core.dataformat.convertor.datatype.ByteStreamDataString"/>
          <entry key="Z" value="nablarch.core.dataformat.convertor.datatype.ZonedDecimal"/>
          <entry key="SZ" value="nablarch.core.dataformat.convertor.datatype.SignedZonedDecimal"/>
          <entry key="P" value="nablarch.core.dataformat.convertor.datatype.PackedDecimal"/>
          <entry key="SP" value="nablarch.core.dataformat.convertor.datatype.SignedPackedDecimal"/>
          <entry key="B" value="nablarch.core.dataformat.convertor.datatype.Bytes"/>
          <entry key="X9" value="nablarch.core.dataformat.convertor.datatype.NumberStringDecimal"/>
          <entry key="SX9" value="nablarch.core.dataformat.convertor.datatype.SignedNumberStringDecimal"/>
          <entry key="pad" value="nablarch.core.dataformat.convertor.value.Padding"/>
          <entry key="encoding" value="nablarch.core.dataformat.convertor.value.UseEncoding"/>
          <entry key="_LITERAL_" value="nablarch.core.dataformat.convertor.value.DefaultValue"/>
          <entry key="number" value="nablarch.core.dataformat.convertor.value.NumberString"/>
          <entry key="signed_number" value="nablarch.core.dataformat.convertor.value.SignedNumberString"/>
          <entry key="replacement" value="nablarch.core.dataformat.convertor.value.CharacterReplacer"/>
        </map>
      </property>
    </component>



フィールドタイプ・フィールドコンバータ定義一覧
--------------------------------------------------------------------
  追加したフィールドタイプについて解説する。

  **フィールドタイプ**

  .. list-table::
   :widths: 130 150 200
   :header-rows: 1

   * - タイプ識別子
     - Java型
     - 内容
   * - ESN
     - String
     - | ダブルバイト文字列 (バイト長 = 文字数 × 2 + 2(シフトコード分))
       | 本サンプルは、デフォルトでは全角空白による右トリム・パディングを行う。
       | 入力時はシフトアウト・シフトインのコードを付加された状態を想定し特になにもせず文字列化を行い、
       |  出力時はシフトアウト・シフトインのコードを自動で付加する。
       | サンプル実装クラス: please.change.me.core.dataformat.converter.datatype.EbcdicDoubleByteCharacterString
       | 引数: バイト長(数値、必須指定)
   * - EN
     - String
     - | ダブルバイト文字列 (バイト長 = 文字数 × 2)
       | 本サンプルは、デフォルトでは全角空白による右トリム・パディングを行う。
       | 入力時はシフトアウト・シフトインのコードを内部で補完して文字列化を行い、
       | 出力時はシフトアウト・シフトインのコードを付加しない。
       | サンプル実装クラス: please.change.me.core.dataformat.converter.datatype.EbcdicNoShiftCodeDoubleByteCharacterString
       | 引数: バイト長(数値、必須指定)
