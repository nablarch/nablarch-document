=====================================
バリデーション機能の拡張
=====================================

.. important::

  本サンプルは、Nablarch 1.4系に準拠したAPIを使用している。

  Nablarch 1.4系より新しいNablarchと組み合わせる場合は、必要に応じてカスタマイズすること。


本サンプルで提供するバリデーション機能の仕様を解説する。

バリデーション機能の概要、基本となるバリデーションに関する詳細は、Nablarch Application Framework解説書のバリデーションに関する解説を参照すること。

`ソースコード <https://github.com/nablarch/nablarch-biz-sample-all>`_

----------------------------
提供パッケージ
----------------------------

本機能は、下記のパッケージで提供される。

  *please.change.me.* **core.validation.validator**


.. _ExtendedValidation_mailAddressValidator:

----------------------------
メールアドレスバリデーション
----------------------------
メールアドレスに関する精査機能を解説する。

  .. list-table::
   :widths: 100 200
   :header-rows: 1

   * - バリデータクラス名
     - 対応するアノテーション
   * - MailAddressValidator
     - @MailAddress

バリデータに設定可能な設定値は下記のとおりである。

  .. list-table::
   :widths: 100 200
   :header-rows: 1

   * - property名
     - 設定内容
   * - messageId(必須)
     - メールアドレスに精査エラーがあった場合のメッセージID

       例 : "{0}は有効なメールアドレスではありません。"

.. tip::

  メールアドレスの入力項目がローカル部とドメイン部に分かれている場合など、アノテーションによる精査が利用できない場合には、
  以下のユーティリティを利用してメールアドレス精査を実行できる。

      .. class:: VariousValidationUtil
      .. function:: boolean isValidMailAddress

        :param value: 精査対象のメールアドレス
        :return: 有効なメールアドレスである場合はtrue

メールアドレス精査仕様
==============================

メールアドレスの構成を下記に示す。 ::

  "ローカル部" @ "ドメイン部"

メールアドレスに使用できる文字はRFC 5321、RFC 5322により定められている。

しかし、ローカル部に関しては、RFC違反のメールアドレスも使用されている。

そのため、ローカル部に対して厳密なチェックを行うと、ユーザーがメールアドレスを登録できない危険性がある。

よって、ローカル部に対して行う精査は、桁数と文字種に関する精査のみである。

メールアドレスに関する精査仕様は下記のとおりである。

* メールアドレス全体に関する精査仕様

  * 必須精査は行わない。
  * メールアドレスとして有効な文字種のみで構成されていること。メールアドレスとして有効な文字種は下記のとおりである。

    * 大文字アルファベット 　A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
    * 小文字アルファベット 　a b c d e f g h i j k l m n o p q r s t u v w x y z
    * 数字　 0 1 2 3 4 5 6 7 8 9
    * その他記号 　! # $ % & \ * + - . / = ? @ ^ _ ` { | } ~

  * '@'（アットマーク）が存在し、1つのみであること。
  * JavaMailでメールを送信する際に形式チェックでエラーとならないこと。

  .. tip::
    メールアドレスとして無効なアスキー文字は下記のとおりである。また、スペースも無効とする。  ::

        " ( ) , : ; < > [ \ ]

    RFC 5322にて規定されているquoted-stringという記法を用いるとこれらの無効な文字も使用することができる。
    しかし、メールアドレスにこれらの記法が使用されることは稀であるため、本機能では無効とする。

* ローカル部に関する精査仕様

  * メールアドレスの先頭が'@'（アットマーク）ではないこと。（ローカル部が存在すること。）
  * ローカル部が64文字以下であること。

* ドメイン部に関する精査仕様

  * メールアドレスの末尾が'@'（アットマーク）ではないこと。（ドメイン部が存在すること。）
  * ドメイン部が255文字以下であること。
  * ドメイン部の末尾が'.'（ドット）ではないこと。
  * ドメイン部に'.'（ドット）が存在すること。
  * ドメイン部の先頭が'.'（ドット）ではないこと。
  * ドメイン部にて'.'（ドット）が連続していないこと。

  .. tip:: 本機能ではRFCにて定められているローカル部、ドメイン部の桁数チェックのみを行う。
    登録できるメールアドレスの全桁数に関しては、プロジェクト毎にて決めることが通常であるため、本機能では精査を行わない。

.. _ExtendedValidation_japaneseTelNumberValidator:

---------------------------
日本電話番号バリデーション
---------------------------
日本の電話番号に関する精査を解説する。日本の電話番号をユーザーに入力させる場合は次の2通りの方法がある。

* 電話番号が市外局番等のフィールドに分かれておらず、一つの文字列として入力される場合
* 市外局番、市内局番、加入者番号をそれぞれ別の入力項目として入力する場合

以下では、これらの精査別に精査方法を解説する。


単項目の電話番号に対する精査
==============================

電話番号が市外局番等のフィールドに分かれておらず、一つの文字列として入力される場合の精査機能を解説する。
この場合、単項目精査機能にて実現する。

  .. list-table::
   :widths: 100 200
   :header-rows: 1

   * - バリデータクラス名
     - 対応するアノテーション
   * - JapaneseTelNumberValidator
     - @JapaneseTelNumber

バリデータに設定可能な設定値は下記のとおりである。

  .. list-table::
   :widths: 100 200
   :header-rows: 1

   * - property名
     - 設定内容
   * - messageId(必須)
     - 電話番号に精査エラーがあった場合のメッセージID

       例 : "{0}は有効な電話番号ではありません。"

精査仕様
------------

精査仕様は下記のとおりである。

* 必須精査は行わない。
* 先頭が「0」で始まること。
* ハイフンと数字のみで構成されていること。
* 桁数のパターンが次のいずれかであること。

    .. list-table::
     :widths: 100 200
     :header-rows: 1

     * - "市外局番桁数" - "市内局番桁数" - "加入者番号桁数"
       - 例
     * - "3桁" - "3桁" - "4桁"
       - 012-345-6789
     * - "3桁" - "4桁" - "4桁"
       - 012-3456-7890
     * - "4桁" - "2桁" - "4桁"
       - 0123-45-6789
     * - "5桁" - "1桁" - "4桁"
       - 01234-5-6789
     * - "2桁" - "4桁" - "4桁"
       - 01-2345-6789
     * - "11桁"
       - 01234567890
     * - "10桁"
       - 0123456789


複数項目で表される電話番号に対する精査
========================================

市外局番、市内局番、加入者番号をそれぞれ別の入力項目として入力する場合の精査機能を解説する。
この場合の精査に対して、Nablarchは次の精査ユーティリティを提供する。

  .. class:: VariousValidationUtil
  .. function:: boolean isValidJapaneseTelNum

   :param areaCode: 市外局番
   :param cityCode: 市内局番
   :param subscriberNumber: 加入者番号
   :return: 有効な日本の電話番号である場合はtrue


精査仕様
-----------

精査仕様は下記のとおりである。

* 全ての項目が入力されていることのチェックは行わない。
* 先頭が「0」で始まること。
* ハイフンと数字のみで構成されていること。
* 桁数のパターンが次のいずれかであること。

    .. list-table::
     :widths: 100 200
     :header-rows: 1

     * - "市外局番桁数" - "市内局番桁数" - "加入者番号桁数"
       - 例
     * - "3桁" - "3桁" - "4桁"
       - 012-345-6789
     * - "3桁" - "4桁" - "4桁"
       - 012-3456-7890
     * - "4桁" - "2桁" - "4桁"
       - 0123-45-6789
     * - "5桁" - "1桁" - "4桁"
       - 01234-5-6789
     * - "2桁" - "4桁" - "4桁"
       - 01-2345-6789

  .. important::

    全ての引数がnullまたは空文字列の場合、trueを返却する。
    市外局番、市内局番、加入者番号の３項目が全て未入力のケースを許容しない場合は、本精査処理の呼び出し元で必須精査を行うこと。（下記の :ref:`telNum_fields_code` を参照。）

.. _telNum_fields_code:

実装例
-----------

  .. code-block:: java

    @ValidateFor("registerCompany")
    public static void validateForRegisterCompany(
                          ValidationContext<CompanyEntity> context) {
        // 単項目精査
        ValidationUtil.validateWithout(context, REGISTER_COMPANY_SKIP_PROPS);
        if (!context.isValid()) {
            return;
        }

        // 項目間精査
        CompanyEntity companyEntity = context.createObject();
        // 全ての項目が入力されていることのチェック
        // このチェックは必要な場合のみ行うこと。
        if (StringUtil.isNullOrEmpty(companyEntity.getAreaCode,
                                     companyEntity.getCityCode,
                                     companyEntity.getSubscriberNumber)) {
            // コンテキストにメッセージ追加
            // 省略
        }
        // 電話番号精査
        if (!VariousValidationUtil.isValidJapaneseTelNum(
                                     companyEntity.getAreaCode,
                                     companyEntity.getCityCode,
                                     companyEntity.getSubscriberNumber)) {
            // コンテキストにメッセージ追加
            // 省略
        }

----------------------------
コード値精査
----------------------------
コード値精査は、複数の機能から異なるパターンを指定して精査を行うことが想定される。
このため、本サンプルではパターンを指定してコード値精査を行うためのユーティリティを提供する。

.. tip::

  コード値精査の詳細は、Nablarchアプリケーションフレームワーク解説書のコード管理の章を参照すること。

ユーティリティの提供するメソッド
========================================
以下の2つのメソッドを提供する。

  .. function:: void validate()

   :param context: 精査コンテキスト
   :param codeId: コードID
   :param pattern: パターン
   :param propertyName: 精査対象のプロパティ

  .. function:: void validate()

   :param context: 精査コンテキスト
   :param codeId: コードID
   :param pattern: パターン
   :param propertyName: 精査対象のプロパティ
   :param messageId: メッセージID（デフォルトのメッセージIDを指定されたメッセージIDで上書きする）



ユーティリティの使用例
===========================
ユーティリティの使用例を以下に示す。

.. code-block:: java

    
    // 【説明】CodeValidationUtil#validateメソッドを使用してコード値精査を行う。
    CodeValidationUtil.validate(context, "0001", "PATTERN1", "gender");

    // 【説明】メッセージIDを上書きする場合には、第5引数にメッセージIDを指定する。
    CodeValidationUtil.validate(context, "0001", "PATTERN1", "gender", "message_id");
  