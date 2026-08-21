# 作業指示 #32: #31 の是正打ち切りと、残TODOの整理、利用側ページの構成物記述の見直し

対象リポジトリ: nablarch/nablarch-document、ブランチ ntf-yaml-support
記録先: .rn/20260724-ntf-yaml-support/checks/task-32.md

以下、パスは ja/development_tools/testing_framework/ からの相対。
行番号は現在の作業ツリー（#31 の fe0c775）のもの。#31 は tools/testdata_converter.rst
しか変更していないため、それ以外のファイルの行番号は 65a1756 と同じである。
同一ファイル内で複数箇所を消す手順は、行番号がずれないよう下から順に行うこと。

モジュール側リポジトリは作業ディレクトリの外にあるため、見に行かなくてよい。
必要な一次情報は本指示に逐語で引用してある。

---

## 0. #31 を閉じる

user 裁定: 是正ラウンド上限3回に対し、4ラウンド目を1回だけ認める。
ただし「削る」だけに限定する。埋め合わせの説明を書き足さないこと。
上限が防いでいるのは推敲の無限ループであり、実測がまさにそれを示しているため
（user が git show | sed -n | wc -m で実測。checks/task-last.md:433 は
7c38797 527字 → a9f915f 961字 → fe0c775 955字。checks/task-28.md:460 は
a9f915f 471字 → fe0c775 526字）。

0-1. checks/task-31.md「未解決の指摘（是正ラウンド上限後）」の 指摘3・6・7・8・9 だけを直す。
     いずれも「記録が事実と食い違っている」誤記であり、次のとおり削るだけで直る。

  指摘3  「判定の内訳（3事象）」の「checks/task-last.md §8 の削除記録の段落にも、
         同じ趣旨を1文で書いてある。」という文を削除する。
  指摘6  「申し送り」1 の「複数の観点が独立に検出した（検出者の内訳は本作業ディレクトリ内に
         記録が無く未確認である）。」という文を削除する。
  指摘8  「Method」表の XLS-05・XLS-27 の行から「本作業ディレクトリ内に出典が無い」の句を
         削除する。user が示した文面は steering.md の #31「根拠」にあるため。
  指摘9  「判定の内訳（3事象）」(b) の記法上の裏づけの段落から、「是正した
         tools/testdata_converter.rst:37 の1行は、これと逆の含意を与えていた」を削除する。
  指摘7  「申し送り」3 を、次の1行だけに置き換える。
           **3. 表に残した「マーカーカラム」「空欄のレコード種別」の検証。** #32 の手順1で処置する。

0-2. 「申し送り」1 も、次の1行だけに置き換える。
       **1. 「意味を持たない情報」の行に残る「外側」という限定。** #32 の手順1で処置する。

0-3. 指摘1・2・4 は直さない。#30 Step 6 のマージ直前の一括処置へ送る。
     指摘5 は処置不要。手順1で本文を直すことで、指摘5 が指す未決点
     （:39 の「外側」の限定、未検証のまま残した「マーカーカラム」）そのものが消えるため。
     この2点を「未解決の指摘」の表の下に、合わせて2行で記す。

0-4. 「申し送り」2・4 と、無効と判定した1件は現状のまま。

0-5. #31 を check-off する。

---

## 1. 中間モデルの表を直し、前提事項に1文足す

対象: tools/testdata_converter.rst

1-1. :37 と :39 を書き換える。

  変更前
    :37     - 無損失で保持する。マーカーカラム、空欄のレコード種別が該当する
    :39     - 保持しない。コメント、データブロックの外側にある空行、行末の空セルは除去する

  変更後
    :37     - 無損失で保持する。空欄のレコード種別が該当する
    :39     - 保持しない。コメント、マーカーカラム、空エントリ、データブロックの外側にある空行、行末の空セルは除去する

  #31 の指示で「マーカーカラム」を :37 に残したのは誤りだった。また :39 の「外側」という
  限定は、対の「内側」を #31 で外したため宙に浮いていた。この書き換えで両方が片づく。

  根拠（nablarch-testing-converter、コミット 229201f。以下すべて逐語）:

  - マーカーカラムは中間モデルに入らない
      src/main/java/nablarch/test/core/reader/TestCoreReaderAdapter.java:129
          return Arrays.asList(header.getEffectiveColumnNames());
      getEffectiveColumnNames はマーカーカラムを除いたカラム名を返す。
      .rn/ntf-test-data-converter/steering.md:475（完了条件）
          - マーカーカラム（`[no]` 等）が変換後のYAML / Excelに含まれない（除外が機能している）

  - 空エントリは中間モデルに入らない
      src/main/java/nablarch/test/tool/converter/xls/XlsFormatReader.java:566
          private static List<List<String>> dropEmptyEntries(List<List<String>> rows) {
      同 :583
          private static boolean isEmptyEntry(List<String> row) {
      呼び出しは同ファイルの :162 と :193。

  - 空欄のレコード種別は中間モデルに保持される（:37 に残す根拠）
      src/main/java/nablarch/test/tool/converter/xls/XlsFormatReader.java:308
          String recordType = emptyToNull(bodyLines.get(idx).get(0));
      同 :327-329
          private static String emptyToNull(String recordType) {
              return recordType == null || recordType.isEmpty() ? null : recordType;
          }
      src/main/java/nablarch/test/tool/converter/model/RecordLayout.java:66
          /** @return レコード種別（省略時は {@code null}） */
      空セルは中間モデルで null として保持される。

1-2. :67 の段落（「ただし\ Excel\ 形式のクォート記法…」）の直後に、空行1行を挟んで
     次の段落を足す。

  マーカーカラムと空エントリも、往復すると消える。マーカーカラムはテスティングフレームワークが読み込み対象から除外し、空エントリは読み飛ばすため、どちらも中間モデルに入らない。テストの実行結果は変わらないが、変換後のテストデータには残らない。

  「前提事項」の既存の段落は、いずれも往復すると見た目が変わるものを具体例つきで挙げている
  （:67 の「\ ``"abc"``\ と書いたセルは往復後に\ ``abc``\ になる」がその型）。マーカーカラムは
  利用者が読みやすさのために置いた列がまるごと消えるため、この節に要る。

1-3. 手順1-1 の根拠（上の逐語3組）を checks/task-32.md に記録する。
     これで checks/task-31.md「申し送り」1・3 は解消となる。

---

## 2. NTF-MOD-02-2 を外す

対象: setup/request_unit_test/rest.rst

2-1. :51-54（TODOブロック3行と直後の空行）を削除する。:55 以降の .. important:: は変更しない。

2-2. checks/task-32.md に次の実測を記録する。

     計測対象: ~/.m2/repository/com/nablarch/framework/nablarch-testing-jetty12/1.1.0/
               nablarch-testing-jetty12-1.1.0.jar

     - 含まれるクラスは12件のみ。
       nablarch/test/core/http/dump/ … SimpleReplacer, RequestDumpServlet, RequestDumpAgent,
         RequestDumpServerShutdownFilter, RequestDumpServer, RequestDumpServer$1,
         HtmlReplacerForRequestUnitTesting（7件）
       nablarch/fw/web/httpserver/ … HttpServerFactoryJetty12, HttpServerJetty12,
         LazySessionInvalidationFilter, LazySessionInvalidationFilter$RequestWrapper,
         LazySessionInvalidationFilter$SessionWrapper（5件）
     - コンポーネント定義ファイル（.xml / .config）は同梱されていない
       （META-INF/maven 配下の pom.xml と pom.properties のみ）。
     - nablarch.test.core.http.dump は nablarch-testing 1.2.0 の jar には存在し、
       1.3.0・1.4.0・1.7.0・2.0.0・6u3・6-NEXT-SNAPSHOT の jar には存在しない。

     これにより :57 の .. important:: の記述は裏付けられた。

---

## 3. NTF-SRC-01 を外す

対象: setup/junit5_extension.rst

3-1. :73-76（TODOブロック4行）を削除する。:77 の空行と :78 の本文は残す。

3-2. checks/task-32.md に次の出典を記録する。

     - JUnit 5.3.0 リリースノート
       https://docs.junit.org/5.3.0/release-notes/index.html
       節「Deprecations and Breaking Changes」より逐語:
         "The JUnit Platform Surefire Provider (`junit-platform-surefire-provider`) is now
          deprecated in favor of the native support for the JUnit Platform provided by
          Maven Surefire 2.22.0 and later versions."
     - Apache Maven Surefire Plugin 2.22.0 リリース告知（2018-06-17）
       https://blogs.apache.org/maven/entry/apache-maven-surefire-plugin-2
       New Features より逐語:
         "SUREFIRE-1330 – JUnit 5 surefire-provider code donation"

---

## 4. NTF-SRC-02 を外し、UI項目名を併記に直す

### 4-1. setup/request_unit_test/web.rst

次の5行を書き換える。

  :190
    変更前  * メニューバーの「実行」から「実行構成」を開く。
    変更後  * メニューバーの「実行(Run)」から「実行構成(Run Configuration)」を開く。

  :191
    変更前  * 「引数」タブの「VM 引数」欄に、上記のオプションを記述する。
    変更後  * 「引数(Arguments)」タブの「VM 引数(VM Arguments)」欄に、上記のオプションを記述する。

  :198
    変更前  * 「インストール済みのJRE」で、使用するJREを選んで「編集」を押す。
    変更後  * 「インストール済みのJRE(Installed JREs)」で、使用するJREを選んで「編集(Edit)」を押す。

  :202
    変更前  * 「デフォルトの VM 引数」欄に、前述のオプションを記述する。
    変更後  * 「デフォルトの VM 引数(Default VM Arguments)」欄に、前述のオプションを記述する。

  :222
    変更前  Eclipseで指定する場所は、JVMオプションと同じ実行構成の「VM 引数」欄である。
    変更後  Eclipseで指定する場所は、JVMオプションと同じ実行構成の「VM 引数(VM Arguments)」欄である。
    （文の後半「この欄にシステムプロパティを記述する。」は変更しない）

そのうえで :162-165（TODOブロック3行と直後の空行）を削除する。

英語名の出典（本リポジトリ内、コミット 65a1756）:
  en/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/02_RequestUnitTest.rst
    :499  * Select "Run(実行)" > "Run Configuration(実行構成)" from the menu bar.
    :501  * In the "Run Configuration(実行構成)" window, click on the "Arguments(引数)" tab
          and specify the above options in the "VM Arguments(VM引数)" field.
    :507  * Select "Window(ウィンドウ)" > "Settings(設定)" from the menu bar. In the
          "Settings(設定)" window that is displayed, select "Installed JREs(インストール済みのJRE)".
    :509  * Select the JRE you want to use from the list of installed JREs that is displayed,
          and click the "Edit(編集)" button.

「デフォルトの VM 引数」だけは en 側 :513 が "VM argument(VM引数)" となっており、
:204 の画面ショット images/web/edit_jre.png に写っている「デフォルトの VM 引数(V):」と
一致しないため、en を根拠にしない。Eclipse公式ヘルプを出典とする。

  https://help.eclipse.org/latest/topic/org.eclipse.jdt.doc.user/tasks/task-add_new_jre.htm
  逐語: "In the Default VM Arguments field, you can add/edit the default arguments that
         will be passed to the VM when launching."

### 4-2. tools/request_data_tool.rst

:100 を書き換える。「Open With」の日本語名は一次情報が取得できなかったため、
項目名を書かない言い回しにする。

  変更前
    Eclipseのパッケージエクスプローラなどから、生成されたHTMLダンプを右クリックし、「Open With」→「httpDump」を選ぶとツールが起動する。
  変更後
    Eclipseのパッケージエクスプローラなどから、生成されたHTMLダンプを右クリックし、\ ``httpDump``\ で開くとツールが起動する。

:106 の .. image:: images/request_data_tool/04_Eclipse_OpenWith.png は残す。

そのうえで :102-105（TODOブロック3行と直後の空行）を削除する。

### 4-3. 記録

checks/task-32.md に、4-1 の出典（en の該当行とEclipse公式ヘルプのURL・逐語）と、
「Open With」の日本語名が取得できず項目名を書かない言い回しにしたことを記録する。
これにより checks/task-last.md §5-5 の「S-12 規約4 未達9件」は解消となる。

---

## 5. 利用側ページの構成図を全廃する

利用側のページに、テスティングフレームワークの内部構造を示すUMLクラス図は置かない。
利用者はNTFの内部の作りを知らなくてもテストを書けるため。

### 5-1. TODOで印を付けてある4件

次のTODOブロックと直後の空行を削除する。本文は変更しない。

  implementation/request_unit_test/mom.rst   :35-40  NTF-FIG-02
  implementation/request_unit_test/mom.rst   :17-21  NTF-FIG-03
  implementation/request_unit_test/rest.rst  :17-22  NTF-FIG-01
  implementation/request_unit_test/batch.rst :17-22  NTF-FIG-04

### 5-2. まだ残っている図3件

  implementation/request_unit_test/web.rst
    :17-18（.. image:: images/web/request_unit_test_structure.png と直後の空行）を削除する。
    :15 の本文は図に言及していないため変更しない。

  implementation/class_unit_test/component.rst
    :15 の末尾「全体像を次に示す。」を削る（直前の「…テストロジックだけを書く。」で文を終える）。
    :17-18（.. image:: images/component/class_structure.png と直後の空行）を削除する。

  about/index.rst
    :106 の末尾「構成物どうしの関係は、次の図のとおり。」を削る
    （直前の「…テスティングフレームワーク経由で読み取って使用する。」で文を終える）。
    :108-110（.. image:: images/index/abstract_structure.png、:scale: 80、直後の空行）を削除する。

    この図を落とす理由は、図中のノードに glossary.md が禁止する「自動テストフレームワーク」が
    使われていること、作図元ファイルが無く直せないこと、図の内容が :106 の本文に既に
    書かれていることの3点。

---

## 6. 参照されなくなった画像と作図元を削除する

手順5の後、ja/ のどこからも参照されなくなる次の9ファイルを削除する。
en/ 配下の同名ファイルは削除しない。

  ja/development_tools/testing_framework/implementation/request_unit_test/images/batch/batch_request_test_class.png
  ja/development_tools/testing_framework/implementation/request_unit_test/images/mom/real_request_test_class.png
  ja/development_tools/testing_framework/implementation/request_unit_test/images/mom/send_sync.png
  ja/development_tools/testing_framework/implementation/request_unit_test/images/mom/send_sync.xlsx
  ja/development_tools/testing_framework/implementation/request_unit_test/images/rest/rest_request_unit_test_structure.png
  ja/development_tools/testing_framework/implementation/request_unit_test/images/rest/rest_request_unit_test_structure.xlsx
  ja/development_tools/testing_framework/implementation/request_unit_test/images/web/request_unit_test_structure.png
  ja/development_tools/testing_framework/implementation/class_unit_test/images/component/class_structure.png
  ja/development_tools/testing_framework/about/images/index/abstract_structure.png

なお tools/images/request_data_tool/image.xlsx は、他の解説書と同じ作図元の置き方であり
対象外とする。

---

## 7. 「主なクラスとリソース」の表から、利用者が書かないクラスを落とす

利用者がテストコード・テストデータ・コンポーネント設定のいずれにも名前を書かず、
このページの手順でも意識しないクラスは、表に載せない。手順5と同じ理由による。

### 7-1. 表から削る行（7行）

  implementation/request_unit_test/web.rst   :40-42  ``HttpServer``
  implementation/request_unit_test/rest.rst  :46-48  ``HttpServer``
  implementation/request_unit_test/batch.rst :57-59  ``TestShot``
  implementation/request_unit_test/batch.rst :51-53  ``StandaloneTestSupportTemplate``
  implementation/request_unit_test/mom.rst   :93-95  ``TestShot``
  implementation/request_unit_test/mom.rst   :84-86  ``AbstractHttpRequestTestTemplate``
  implementation/request_unit_test/mom.rst   :81-83  ``StandaloneTestSupportTemplate``

mom.rst の ``AbstractHttpRequestTestTemplate`` は「ウェブアプリケーションのリクエスト単体
テストの実行環境を提供する」と書かれており、MOMによるメッセージングのページの内容ではない。

次のクラスは残す。いずれも利用者が名前を書く、または意識する。
  ``TestCaseInfo``（web.rst:210-211 ほかコード例に出る）
  ``AbstractHttpRequestTestTemplate``・``BasicHttpRequestTestTemplate``（web.rst:78・88 で継承する）
  ``HttpRequestTestSupport``（setup/junit5_extension.rst:52 でインジェクション対象になる）
  ``RequestTestingMessagingProvider``（setup/request_unit_test/mom.rst:44 で設定に書く）
  ``MessageSender``（テスト対象の Action が使う）
  ``MainForRequestTesting``（batch.rst:192・mom.rst:210 に独立した説明がある）
  ``DbAccessTestSupport``・``FileSupport``・``MQSupport``・``EntityTestSupport``
  ``RestTestSupport``・``BatchRequestTestSupport``・``MessagingRequestTestSupport``
  ``MessagingReceiveTestSupport``

class_unit_test/component.rst と class_unit_test/entity.rst の表は変更しない。

### 7-2. 本文から同じクラス名を落とす

  implementation/request_unit_test/rest.rst :23
    「内蔵サーバ（\ ``HttpServer``\ ）を保持し」を「内蔵サーバを保持し」に置き換える。
    他は変更しない。

  implementation/request_unit_test/batch.rst :23
    変更前
      テストクラスは、\ ``StandaloneTestSupportTemplate``\ を継承した\ ``BatchRequestTestSupport``\ を継承して作成する。テストデータを読み取り、テストショット1件分の情報を保持する\ ``TestShot``\ を1件ずつ実行する。テスト用のメインクラス\ ``MainForRequestTesting``\ を通じて\ Nablarch Application Framework\ が起動され、テスト対象のアプリケーションが実行される。準備データの投入とテスト結果の確認は、テーブルについては\ ``DbAccessTestSupport``\ が、ファイルについては\ ``FileSupport``\ が行う。
    変更後
      テストクラスは、\ ``BatchRequestTestSupport``\ を継承して作成する。スーパクラスがテストデータを読み取り、テストショットを1件ずつ実行する。テスト用のメインクラス\ ``MainForRequestTesting``\ を通じて\ Nablarch Application Framework\ が起動され、テスト対象のアプリケーションが実行される。準備データの投入とテスト結果の確認は、テーブルについては\ ``DbAccessTestSupport``\ が、ファイルについては\ ``FileSupport``\ が行う。

  implementation/request_unit_test/mom.rst :22
    変更前
      テストクラスは、同期応答メッセージ受信では\ ``MessagingRequestTestSupport``\ を、応答不要メッセージ受信では\ ``MessagingReceiveTestSupport``\ を継承して作成する。\ ``MessagingRequestTestSupport``\ は\ ``StandaloneTestSupportTemplate``\ を継承しており、テストデータを読み取ってテストショットを1件ずつ実行する。\ ``MessagingReceiveTestSupport``\ は、さらに\ ``MessagingRequestTestSupport``\ を継承したクラスである。1件のテストショットの情報は\ ``TestShot``\ が保持し、テスト用のメインクラス\ ``MainForRequestTesting``\ を通じて\ Nablarch Application Framework\ が起動され、テスト対象のアプリケーションが実行される。準備データの投入とテスト結果の確認は、データベースについては\ ``DbAccessTestSupport``\ が、キューについては\ ``MQSupport``\ が行う。
    変更後
      テストクラスは、同期応答メッセージ受信では\ ``MessagingRequestTestSupport``\ を、応答不要メッセージ受信では\ ``MessagingReceiveTestSupport``\ を継承して作成する。\ ``MessagingReceiveTestSupport``\ は\ ``MessagingRequestTestSupport``\ を継承したクラスである。スーパクラスがテストデータを読み取り、テストショットを1件ずつ実行する。テスト用のメインクラス\ ``MainForRequestTesting``\ を通じて\ Nablarch Application Framework\ が起動され、テスト対象のアプリケーションが実行される。準備データの投入とテスト結果の確認は、データベースについては\ ``DbAccessTestSupport``\ が、キューについては\ ``MQSupport``\ が行う。

  implementation/request_unit_test/mom.rst :41
    変更前の冒頭
      テストクラスは、\ ``StandaloneTestSupportTemplate``\ を継承した\ :java:extdoc:`BatchRequestTestSupport <nablarch.test.core.batch.BatchRequestTestSupport>`\ を継承して作成する。テストデータを読み取り、テストショット1件分の情報を保持する\ ``TestShot``\ を1件ずつ実行する。
    変更後の冒頭
      テストクラスは、\ :java:extdoc:`BatchRequestTestSupport <nablarch.test.core.batch.BatchRequestTestSupport>`\ を継承して作成する。スーパクラスがテストデータを読み取り、テストショットを1件ずつ実行する。
    以降（「テスト用のメインクラス…」から末尾まで）は変更しない。

mom.rst :162-163 の独自拡張用スーパクラスの一覧は、拡張する利用者が書くものなので変更しない。

---

## 8. NTF-MOD-03-1 の文言を実状に合わせる

対象: setup/junit5_extension.rst :400-402

判定は済んでおり、不具合として nablarch-testing-junit5 を修正する方針が確定した。
修正後に解説書へ反映するため、TODO自体は残す。文言を次に置き換える。

  変更前
    .. TODO(NTF-MOD-03-1): resolveTestRules() に登録したTimeoutがテスト本体に効かない。判定待ち。
       依頼書 .rn/20260724-ntf-yaml-support/ntf-mod-03-nablarch-testing-junit5.md §2。
       仕様と判定された場合は本文を書き直す。

  変更後
    .. TODO(NTF-MOD-03-1): resolveTestRules() に登録したTimeoutがテスト本体に効かない。
       不具合と判定済みで、nablarch-testing-junit5 側で修正予定・未着手。
       依頼書 .rn/20260724-ntf-yaml-support/ntf-mod-03-nablarch-testing-junit5.md §2。
       修正後に本文へ反映する。

---

## 9. TODO台帳を作り直す

checks/task-32.md に、手順1〜8の後のTODO台帳を作る。
節見出しで指す方式（行番号では指さない）を用いること。
末尾に次のコマンドの実測を貼ること。

  grep -rho 'TODO(NTF-[A-Z0-9-]*)' ja/ | sort | uniq -c

---

## 完了条件

1. 上のコマンドの結果が5件・5ID になる。
   NTF-MOD-01-2 / NTF-MOD-01-3 / NTF-MOD-02-3 / NTF-MOD-02-4 / NTF-MOD-03-1 の各1件。
2. tools/testdata_converter.rst に「意図のある情報」の行として
   「無損失で保持する。空欄のレコード種別が該当する」があり、「マーカーカラム」は
   「意味を持たない情報」の行にだけ現れる。
   grep -n 'マーカーカラム' ja/development_tools/testing_framework/tools/testdata_converter.rst
   のヒットが「意味を持たない情報」の行と「前提事項」の新段落の2件だけになる。
3. 削除した9ファイルへの参照が ja/ 配下に残っていない。
   grep -rn 'batch_request_test_class\|real_request_test_class\|send_sync\|rest_request_unit_test_structure\|request_unit_test_structure\|class_structure\|abstract_structure' ja/
   の結果が0件。
4. python3 mapping/tools/verify_glossary.py が RESULT: OK。
5. python3 mapping/tools/verify_mapping.py が OK: no errors。
6. python3 -m pytest mapping/tools -q が 183 passed, 96 subtests passed。
7. Docker でフルビルドし、grep -cE 'WARNING:|ERROR:|SEVERE:' build.log が 0。
   ビルド直後に git checkout -- locales/ja/LC_MESSAGES/sphinx.mo を必ず実行する。
8. checks/task-32.md に、手順1-3・2-2・3-2・4-3 の記録と、手順9の台帳がある。
9. #31 が check-off されている（手順0）。
