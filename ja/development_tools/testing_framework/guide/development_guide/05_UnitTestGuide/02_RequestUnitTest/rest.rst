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

* :ref:`フレームワークで用意されたテストクラスのスーパークラスを継承する。 <rest_test_extends_superclass>`
* JUnit4のアノテーションを使用する (テストメソッドに @Test アノテーションを付与する)
* :ref:`事前準備補助機能 <rest_test_helper>` を使ってリクエストを生成する
* :ref:`リクエストを送信 <rest_test_execute>` する
* :ref:`結果を確認 <rest_test_assert>` する

.. code-block:: java

    import nablarch.fw.web.HttpResponse;
    import nablarch.fw.web.RestMockHttpRequest;
    import nablarch.test.core.http.RestTestSupport;
    import org.json.JSONException;
    import org.junit.Test;
    import org.skyscreamer.jsonassert.JSONAssert;
    import org.skyscreamer.jsonassert.JSONCompareMode;

    import static com.jayway.jsonpath.matchers.JsonPathMatchers.hasJsonPath;
    import static org.hamcrest.Matchers.hasSize;
    import static org.junit.Assert.assertThat;

    public class SampleTest extends RestTestSupport { //RestTestSupportを継承する
        @Test  //アノテーションを付与する
        public void プロジェクト一覧が取得できること() throws JSONException {
            String message = "プロジェクト一覧取得";

            RestMockHttpRequest request = get("/projects");               //リクエストを生成する
            HttpResponse response = sendRequest(request);                 //リクエストを送信する
            assertStatusCode(message, HttpResponse.Status.OK, response);  //結果を確認する

            assertThat(response.getBodyString(), hasJsonPath("$", hasSize(10)));    //json-path-assertを使ったレスポンスボディの検証

            JSONAssert.assertEquals(message, readTextResource("プロジェクト一覧が取得できること.json")
                    , response.getBodyString(), JSONCompareMode.LENIENT);                  //JSONAssertを使ったレスポンスボディの検証
        }
    }

.. _rest_test_extends_superclass:

フレームワークで用意されたテストクラスのスーパークラスを継承する
=================================================================

テストクラスのスーパークラスとして ``nablarch.test.core.http.RestTestSupport`` クラスを継承する。
テストデータの投入とデータベースのアサートが不要な場合は ``nablarch.test.core.http.SimpleRestTestSupport`` クラスを継承する。
その場合は以下の :ref:`テストデータの書き方 <rest_test_data>` は読み飛ばして良い。

それぞれのスーパークラスの詳細は :ref:`自動テストフレームワークの使用方法 <rest_test_superclasses>` 参照。

JUnit4のアノテーションを使用する
=================================
テスティングフレームワークはJUnit4をベースとしているため、テスト対象メソッドに ``@Test`` アノテーションを付与する。

事前準備補助機能を使ってリクエストを生成する
===================================================
スーパークラスに用意された :ref:`事前準備補助機能 <rest_test_helper>` を使ってリクエストを生成する。

リクエストを送信する
=======================
スーパークラスに用意された :ref:`リクエスト送信メソッド <rest_test_execute>` を呼び出すことでリクエストを送信する。

結果を確認する
=================
ステータスコードは、スーパークラスに用意された :ref:`メソッド <rest_test_assert>` を呼び出すことで検証する。
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
    テストクラスの記述量を減らすためにスーパークラス ``RestTestSupport`` では以下のメソッドを
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

