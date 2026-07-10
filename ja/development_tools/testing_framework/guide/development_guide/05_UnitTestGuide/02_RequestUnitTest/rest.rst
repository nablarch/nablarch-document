=================================
リクエスト単体テストの実施方法
=================================

前提条件
-----------

RESTfulウェブサービス実行基盤向けのテストでは、他の実行基盤向けテスティングフレームワークに加え
依存するモジュールを追加する必要がある。
詳細は :ref:`自動テストフレームワークの使用方法 <rest_testing_fw>` 参照。

テストクラスの書き方
-------------------------------

* :ref:`フレームワークで用意されたテストサポートクラスをインジェクションする。 <rest_test_extends_superclass>`
* JUnit 5のアノテーションを使用する (テストメソッドに @Test アノテーションを付与する)
* :ref:`事前準備補助機能 <rest_test_helper>` を使ってリクエストを生成する
* :ref:`リクエストを送信 <rest_test_execute>` する
* :ref:`結果を確認 <rest_test_assert>` する

.. code-block:: java

    import nablarch.fw.web.HttpResponse;
    import nablarch.fw.web.RestMockHttpRequest;
    import nablarch.test.core.http.RestTestSupport;
    import nablarch.test.junit5.extension.http.RestTest;
    import org.json.JSONException;
    import org.junit.jupiter.api.Test;
    import org.skyscreamer.jsonassert.JSONAssert;
    import org.skyscreamer.jsonassert.JSONCompareMode;

    import static com.jayway.jsonpath.matchers.JsonPathMatchers.hasJsonPath;
    import static org.hamcrest.MatcherAssert.assertThat;
    import static org.hamcrest.Matchers.hasSize;

    @RestTest  //合成アノテーションを付与する
    class SampleTest {

        RestTestSupport support;  //RestTestSupport型のフィールドを宣言する（インスタンスがインジェクションされる）

        @Test  //アノテーションを付与する
        void プロジェクト一覧が取得できること() throws JSONException {
            String message = "プロジェクト一覧取得";

            RestMockHttpRequest request = support.get("/projects");               //リクエストを生成する
            HttpResponse response = support.sendRequest(request);                 //リクエストを送信する
            support.assertStatusCode(message, HttpResponse.Status.OK, response);  //結果を確認する

            assertThat(response.getBodyString(), hasJsonPath("$", hasSize(10)));    //json-path-assertを使ったレスポンスボディの検証

            JSONAssert.assertEquals(message, support.readTextResource(SampleTest.class, "プロジェクト一覧が取得できること.json")
                    , response.getBodyString(), JSONCompareMode.LENIENT);                  //JSONAssertを使ったレスポンスボディの検証
        }
    }

.. _rest_test_extends_superclass:

フレームワークで用意されたテストサポートクラスをインジェクションする
====================================================================

合成アノテーション :java:extdoc:`RestTest <nablarch.test.junit5.extension.http.RestTest>` をテストクラスに付与し、 ``nablarch.test.core.http.RestTestSupport`` 型のフィールドを宣言する（インスタンスは拡張機能が自動的にインジェクションする）。
テストデータの投入とデータベースのアサートが不要な場合は、合成アノテーション :java:extdoc:`SimpleRestTest <nablarch.test.junit5.extension.http.SimpleRestTest>` と ``nablarch.test.core.http.SimpleRestTestSupport`` 型のフィールドを使用する。
その場合は以下の :ref:`テストデータの書き方 <rest_test_data>` は読み飛ばして良い。

それぞれのテストサポートクラスの詳細は :ref:`自動テストフレームワークの使用方法 <rest_test_superclasses>` 参照。

.. tip::
  テストサポートクラスの ``protected`` メソッドは、インジェクション方式ではテストクラスから呼び出せない。
  リソースファイルの読み込みには、public版の ``readTextResource(Class, String)`` のようにテストクラスを引数で渡すメソッドを使用する。

JUnit 5のアノテーションを使用する
=================================
テスト対象メソッドに ``@Test`` アノテーション（ ``org.junit.jupiter.api.Test`` ）を付与する。

事前準備補助機能を使ってリクエストを生成する
===================================================
テストサポートクラスに用意された :ref:`事前準備補助機能 <rest_test_helper>` を使ってリクエストを生成する。

リクエストを送信する
=======================
テストサポートクラスに用意された :ref:`リクエスト送信メソッド <rest_test_execute>` を呼び出すことでリクエストを送信する。

結果を確認する
=================
ステータスコードは、テストサポートクラスに用意された :ref:`メソッド <rest_test_assert>` を呼び出すことで検証する。
レスポンスボディについては任意のライブラリを使用してアプリケーションに合わせて検証する。

.. _rest_test_data:

テストデータの書き方
--------------------

:ref:`how_to_write_excel` に記載された方法で、テストデータを記述できる。
ただし、RESTfulウェブサービス実行基盤向けのテストで自動的に読み込まれるデータは以下のみとなる。

* テストクラスで共通のデータベース初期値
* テストメソッド毎のデータベース初期値

.. important::
    RESTfulウェブサービス実行基盤以外のテストの場合テストクラス一つにつきExcelファイルが必ず一つ必要であったが、
    RESTfulウェブサービス実行基盤向けのテストではExcelファイルが存在しない場合でも、エラーとはならず単にデータベースへの
    データ投入がスキップされるだけとなっている。

.. important::
    上記以外のテストデータをExcelファイルに記載可能だが、記載した場合は
    :ref:`how_to_get_data_from_excel` に記載の方法で、テストクラスに値を取得する処理を記述する必要がある。
    テストクラスの記述量を減らすためにテストサポートクラス ``RestTestSupport`` では以下のメソッドを
    提供する。

    .. code-block:: java

        List<Map<String, String>> getListMap(String sheetName, String id)
        List<Map<String, String[]>> getListParamMap(String sheetName, String id)
        Map<String, String[]> getParamMap(String sheetName, String id)

テストクラスで共通のデータベース初期値
========================================

:ref:`request_test_setup_db` 参照。

テストメソッド毎のデータベース初期値
====================================

テストデータを記載したExcelファイルに\ **テストメソッドの名前**\ でシートを用意し、
\ **SETUP_TABLES**\のデータタイプでデータベース初期値を記載する。
ここに記載されたデータは、フレームワークによりテストメソッド実行時に投入される。

