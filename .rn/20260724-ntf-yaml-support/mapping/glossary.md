# NTF解説書 用語集

本用語集は、再構築するNTF解説書の全ページで使用する表記の唯一の基準である。ページ作成時は本書の「正表記」を使い、「揺れ表記」は使わない。

## 1. 行番号の基準

file:line の基準は取得元ごとに異なる。

| 記号 | 展開 | 行番号の基準 |
|---|---|---|
| `NTF:` | `ja/development_tools/testing_framework/guide/development_guide/` | develop との merge-base（`c2419060`）時点の内容。作業ツリーではない |
| `NTF-root:` | `ja/development_tools/testing_framework/` | 同上 |
| `FW:` | `ja/application_framework/application_framework/` | 作業ツリー |
| `S:` | `.rn/20260724-ntf-yaml-support/` | 作業ツリー |

merge-base は `git merge-base origin/develop HEAD` で求める。現行解説書の内容は `git show <base>:<path>` で取得する。`mapping/tools/build_mapping.sh` と同じ方式である。

「出現数」は後述の検出スクリプトが数えたマッチ数である。1行に同じ表記が複数回現れる場合はその回数だけ数える。

## 2. 採用の優先順位

`design.md` の「6. 用語」に従い、次の順で正表記を決めた。

1. FW解説書（`FW:`）に同じ概念の用語があれば、その表記を採用する
2. FW解説書にない場合、現行解説書・input資料のうち意味が明確で一貫しているものを採用する
3. いずれにもない場合、`design.md` の決定に従うか、新たに定義する

FW解説書と異なる表記を採用した用語は、採用根拠にその理由を記載した。該当するのは「スーパクラス」「前提事項」の2件である。

`input/ntf-doc-terms.md` は候補リストとして扱い、そのまま採用していない。突き合わせ結果は「9. ntf-doc-terms.md の候補の突き合わせ結果」に示す。

## 3. 掲載基準

次のいずれかに当てはまる用語を掲載した。

- 検出スクリプトが表記揺れを検出した用語
- 処理方式・テストの種類・テストデータの構造など、複数ページに横断して現れる骨格の用語
- ページのセクションタイトルに使う用語

次のものは掲載していない。

- Javaのクラス名・メソッド名・カラム名・データタイプ名（`HttpRequestTestSupport`、`assertTableEquals`、`testShots`、`SETUP_TABLE` など）。これらは原文の識別子であり、表記の選択余地がない。個々の意味は `input/ntf-doc-terms.md` を引く
- 1つの機能の説明の中に閉じており、他の機能のページから参照されない固有名詞（`Antビュー` はマスタデータ投入ツールの2ファイルのみ、`app-log.properties` はマスタデータ復旧機能とマスタデータ投入ツールのみ）
- 一般的な日本語語彙で、揺れが検出されなかったもの

## 4. 表記揺れの検出方法

検出は `mapping/tools/detect_term_variants.py` で行う。手作業のgrep結果は根拠に使っていない。

```
# 正解リストを持たずに揺れを見つける（正規化してグループ化する）
python3 mapping/tools/detect_term_variants.py discover --rule punct
python3 mapping/tools/detect_term_variants.py discover --rule paren
python3 mapping/tools/detect_term_variants.py discover --rule longvowel

# 用語定義ファイルの表記を全コーパスから探し、出現数と file:line を出す
python3 mapping/tools/detect_term_variants.py scan --max-locations 0
```

`discover` の正規化ルールは次のとおり。

| ルール | 正規化 | 揺れと判定する軸 | 検出できるもの |
|---|---|---|---|
| `punct` | 見出しと「」内の語から `、` `,` `，` `・` `/` `／` 空白 と接続助詞「と」を除去 | 表記そのもの | 読点・接続の揺れ |
| `paren` | 丸括弧の中身と全角・半角の差を `（…）` に伏せる | 使っている括弧の種類 | 括弧の全角・半角の揺れ |
| `longvowel` | カタカナ語から `ー` を除去 | 表記そのもの | 長音記号の揺れ |

`scan` の入力は `mapping/tools/term_candidates.tsv`（category / canonical / surface の3列）である。1行内では長い表記を優先して非重複にマッチさせるため、「自動テストフレームワーク」がマッチした位置で「テストフレームワーク」は数えない。

いずれのコマンドも出力を辞書順に整列するため、同じ入力に対して同じ出力を返す。

---

## 5. 用語

### 5.1 全体

| 正表記 | 意味 | 揺れ表記（file:line） | 採用根拠 |
|---|---|---|---|
| テスティングフレームワーク | Nablarchが提供するテスト補助機能の総称。本解説書が対象とするもの | `自動テストフレームワーク`（`NTF:06_TestFWGuide/01_Abstract.rst:4` ほか現行70件）／`テストフレームワーク`（`NTF:06_TestFWGuide/03_Tips.rst:825`）／`本フレームワーク`（`NTF:05_UnitTestGuide/02_RequestUnitTest/mail.rst:10` ほか現行14件）／`NTF`（`S:input/ntf-doc-terms.md:1` ほかinput42件、`S:design.md:1` ほか5件） | FW解説書が「テスティングフレームワーク」を使う（`FW:libraries/db_double_submit.rst:106`、`FW:blank_project/CustomizeDB.rst:498` ほか計8件）。現行解説書の最上位ページ題も同じ（`NTF-root:index.rst:2`）。`NTF` は作業用の略称であり、解説書本文では使わない |

### 5.2 処理方式

`design.md` の「5. 処理方式の名称」の表と一致する。名称はFW解説書の各章の題を採る。FW解説書はウェブ系3章にだけ「編」を付けているが（`FW:web/index.rst:3`、`FW:web_service/rest/index.rst:3`、`FW:web_service/http_messaging/index.rst:3`）、バッチ系・メッセージング系には付けていない（`FW:batch/nablarch_batch/index.rst:3`、`FW:messaging/mom/index.rst:3`、`FW:messaging/db/index.rst:3`）。本解説書では「編」を付けない。

| 正表記 | 意味 | 揺れ表記（file:line） | 採用根拠 |
|---|---|---|---|
| ウェブアプリケーション | 画面を持つHTTPアプリケーション | `Webアプリケーション`（FW解説書に10件。`FW:libraries/stateless_web_app.rst:3`、`FW:handlers/web/csrf_token_verification_handler.rst:10`。現行解説書・input資料には0件） | `FW:web/index.rst:3`。FW解説書での出現数はウェブアプリケーション83件に対しWebアプリケーション10件 |
| RESTfulウェブサービス | REST APIを提供するウェブサービス | `RESTful ウェブサービス`（`S:input/ntf-doc-terms.md:420`、`:473`） | `FW:web_service/rest/index.rst:3`。FW解説書72件、現行解説書13件 |
| HTTPメッセージング | HTTPを使ったシステム間メッセージング | なし（現行解説書・input資料に0件） | `FW:web_service/http_messaging/index.rst:3`。ライブラリ側の章題も同じ（`FW:libraries/system_messaging/http_system_messaging.rst:3`） |
| Nablarchバッチアプリケーション | Nablarch独自のバッチアプリケーション | `バッチ処理`（`NTF:06_TestFWGuide/RequestUnitTest_batch.rst:4`、`NTF:05_UnitTestGuide/02_RequestUnitTest/batch.rst:40` ほか現行14件） | `FW:batch/nablarch_batch/index.rst:3`。「バッチ処理」はJakarta Batchを含みうるため、処理方式名としては使わない |
| MOMによるメッセージング | MOM（メッセージ指向ミドルウェア）を使ったメッセージング | `メッセージング処理`（`NTF:05_UnitTestGuide/index.rst:49`、`NTF:06_TestFWGuide/01_Abstract.rst:286` ほか現行12件）／`MOMメッセージング`（FW解説書35件。`FW:libraries/system_messaging/mom_system_messaging.rst:3`） | `FW:messaging/mom/index.rst:3`。処理方式の章題は「MOMによるメッセージング」、ライブラリの章題は「MOMメッセージング」であり、処理方式を指す場合は前者を使う |
| テーブルをキューとして使ったメッセージング | データベースのテーブルをキューとして使うメッセージング | なし（現行解説書・input資料に0件） | `FW:messaging/db/index.rst:3`。FW解説書19件 |
| Jakarta Batchに準拠したバッチアプリケーション | Jakarta Batch仕様に準拠したバッチアプリケーション。NTFの対象外 | `JSR352に準拠したバッチアプリケーション`（`FW:batch/jsr352/index.rst:17`。Nablarch5までの旧名称としてFW解説書自身が明記） | `FW:batch/jsr352/index.rst:3`。現行解説書も新名称を使う（`NTF-root:index.rst:22`） |
| 常駐バッチ | 起動後に常駐して処理を続けるバッチ | なし | `FW:batch/nablarch_batch/architecture.rst:21`。FW解説書23件、現行解説書3件（`NTF:06_TestFWGuide/RequestUnitTest_batch.rst:184` ほか） |
| 都度起動バッチ | 実行のたびに起動されるバッチ | なし | `FW:batch/nablarch_batch/architecture.rst:16`。FW解説書36件。現行解説書には0件だが、常駐バッチとの対比に必要 |

### 5.3 メッセージング方式

現行解説書は末尾に「処理」を付けるが、FW解説書は付けない。FW解説書を採る。

| 正表記 | 意味 | 揺れ表記（file:line） | 採用根拠 |
|---|---|---|---|
| 応答不要メッセージ送信 | 応答を待たずにメッセージを送信する方式 | `応答不要メッセージ送信処理`（`NTF:05_UnitTestGuide/02_RequestUnitTest/delayed_send.rst:2`、`:8` ほか現行8件） | `FW:libraries/system_messaging/mom_system_messaging.rst:135`（見出し「応答不要でメッセージを送信する(応答不要メッセージ送信)」）。FW解説書7件 |
| 応答不要メッセージ受信 | 応答を返さずにメッセージを受信する方式 | `応答不要メッセージ受信処理`（`NTF:05_UnitTestGuide/02_RequestUnitTest/delayed_receive.rst:2`、`NTF:05_UnitTestGuide/03_DealUnitTest/delayed_receive.rst:2` ほか現行5件） | `FW:libraries/system_messaging/mom_system_messaging.rst:470`。FW解説書6件 |
| 同期応答メッセージ送信 | メッセージを送信し、応答を待つ方式 | `同期応答メッセージ送信処理`（`NTF:05_UnitTestGuide/02_RequestUnitTest/http_send_sync.rst:117` ほか現行32件、input5件） | `FW:libraries/system_messaging/mom_system_messaging.rst:330`。FW解説書9件 |
| 同期応答メッセージ受信 | メッセージを受信し、応答を返す方式 | `同期応答メッセージ受信処理`（`NTF:05_UnitTestGuide/02_RequestUnitTest/real.rst:4`、`NTF:05_UnitTestGuide/03_DealUnitTest/real.rst:2` ほか現行7件）／`メッセージ受信処理`（`NTF:06_TestFWGuide/RequestUnitTest_real.rst:2`、`:9`、`S:input/ntf-doc-terms.md:422`、`:500`） | `FW:libraries/system_messaging/mom_system_messaging.rst:638`。FW解説書5件。「メッセージ受信処理」は応答不要受信と区別できないため使わない |
| HTTP同期応答メッセージ送信 | HTTPメッセージングにおける同期応答メッセージ送信 | `HTTP同期応答メッセージ送信処理`（`NTF:05_UnitTestGuide/02_RequestUnitTest/http_send_sync.rst:4` ほか現行8件） | FW解説書に該当語なし。同期応答メッセージ送信に接頭辞`HTTP`を付ける形を、現行解説書（`NTF:06_TestFWGuide/RequestUnitTest_http_send_sync.rst:12` に「HTTP同期応答メッセージ送信」1件）に合わせて採用する |
| HTTP同期応答メッセージ受信 | HTTPメッセージングにおける同期応答メッセージ受信 | `HTTP同期応答メッセージ受信処理`（`NTF:05_UnitTestGuide/02_RequestUnitTest/http_real.rst:2`、`NTF:05_UnitTestGuide/index.rst:68` ほか現行3件） | 同上（`NTF:05_UnitTestGuide/02_RequestUnitTest/http_real.rst:23` に「HTTP同期応答メッセージ受信」1件） |

### 5.4 テストの種類

| 正表記 | 意味 | 揺れ表記（file:line） | 採用根拠 |
|---|---|---|---|
| クラス単体テスト | クラス単体を対象とし、JUnitで自動実行するテスト | `単体テスト`（単独で使われるもの。`NTF:05_UnitTestGuide/index.rst:4` ほか現行21件） | 現行解説書26件（`NTF:05_UnitTestGuide/01_ClassUnitTest/index.rst:4` ほか）。`S:design.md:31`、`:42` |
| リクエスト単体テスト | 1リクエストを対象とし、ハンドラキューを通してJUnitで自動実行するテスト | なし | 現行解説書106件。FW解説書も同じ表記を使う（`FW:handlers/web/csrf_token_verification_handler.rst:155`）。`S:design.md:31`、`:43` |
| 取引単体テスト | 複数リクエストにまたがる業務の流れを手動操作で確認するテスト | なし | 現行解説書40件（`NTF:05_UnitTestGuide/03_DealUnitTest/index.rst:4` ほか）。`S:design.md:31`、`:44` |
| エンティティ単体テスト | クラス単体テストのうち、Form・Entityのバリデーションを対象とするもの | `Form/Entity単体テスト`（`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:14` ほか現行4件）／`Form/Entityの単体テスト`（`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/index.rst:4`） | `S:design.md:115`。読者がクラス名の組み合わせではなく対象の種類で引けるようにするため、`design.md` の決定に従う |
| コンポーネント単体テスト | クラス単体テストのうち、Action・Componentを対象とするもの | `Action/Component単体テスト`（`NTF:05_UnitTestGuide/01_ClassUnitTest/02_componentUnitTest.rst:10`）／`Action/Componentのクラス単体テスト`（`NTF:05_UnitTestGuide/01_ClassUnitTest/02_componentUnitTest.rst:4` ほか現行2件） | `S:design.md:116`。同上 |

### 5.5 テストデータ

| 正表記 | 意味 | 揺れ表記（file:line） | 採用根拠 |
|---|---|---|---|
| テストデータ | テストクラスの外部ファイルに記述する、準備データと期待値の総称 | なし | 現行解説書229件、input資料32件で一貫している |
| テストデータファイル | テストデータを記述したファイル。Excel形式とYAML形式がある | なし | input資料4件（`S:input/ntf-testdata-doc.md:24`、`:436` ほか）。YAML形式の追加により「Excelファイル」では総称にならないため採用する |
| データブロック | テストデータファイル内で `データタイプ[グループID]=値` によって識別される1かたまりのデータ | `セクション`（input資料30件。`S:input/ntf-testdata-doc-examples-overview.md:93`、`S:input/ntf-testdata-doc-examples-messaging.md:7`） | `S:design.md:32`（第1部「テストデータ」に「データブロックの考え方」を置くと決めている）。input資料46件。現行解説書はこの単位に名前を与えておらず、「データタイプ」で代用している。なお `S:design.md` の「セクション」10件は文書のセクションの意であり、別義である |
| データタイプ | データブロックの種別を表すキーワード。`SETUP_TABLE`、`EXPECTED_TABLE` など | なし | 現行解説書43件、input資料57件で一貫している。データブロックの「種別」を指す語として使い、データブロックそのものを指す用法では使わない |
| グループID | 同一ファイル内の複数のデータブロックを識別する標識 | `グループ ID`（input資料21件。`S:input/ntf-doc-terms.md:118`、`:124`）／`groupId`（input資料52件。`S:input/ntf-testdata-doc-examples-file.md:33` ほか） | 現行解説書73件（`NTF:05_UnitTestGuide/01_ClassUnitTest/02_componentUnitTest.rst:259` ほか）。現行解説書の `groupId` 46件はMavenの `<groupId>` 要素と参照ラベル `tips_groupId` であり、本用語の用例ではない。FW解説書の「グループID」22件もMavenのグループIDを指す別義（`FW:blank_project/MavenModuleStructures/index.rst:17`） |
| シート | Excel形式のテストデータファイル内の1シート。テストメソッドに対応する | `データシート`（現行解説書7件。`NTF:06_TestFWGuide/01_Abstract.rst:70`、`NTF:05_UnitTestGuide/02_RequestUnitTest/index.rst:344` ほか。`テストデータシート`の一部として現れるものは含まない） | 現行解説書108件、input資料38件。YAML形式ではシートに相当する単位をファイルが担うため、形式に依存する記述では「シート」を、しない記述では「テストデータファイル」を使う |
| テストケース一覧 | 1テストクラスで実行するテストケースを列挙したデータブロック（`LIST_MAP=testShots`） | `テストショット一覧`（`NTF:05_UnitTestGuide/02_RequestUnitTest/real.rst:54`、`NTF:05_UnitTestGuide/02_RequestUnitTest/http_real.rst:13` ほか現行5件）／`テストケース表`（`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:110` ほか現行9件） | 現行解説書24件、input資料5件。「テストショット」はクラス名 `TestShot` の直訳であり、読者が意味を推測できない |
| 準備データ | テスト実行前にデータベース・ファイルへ投入するデータ | `事前準備データ`（`NTF:05_UnitTestGuide/01_ClassUnitTest/02_componentUnitTest.rst:96`、`S:input/ntf-doc-terms.md:48`）／`セットアップデータ`（`S:input/ntf-testdata-doc.md:188`、`S:design.md:32`） | 現行解説書49件、input資料4件。`S:design.md:32` は第1部の記載内容の説明中で「セットアップデータ」を1度使っているが、用語を定める節ではないため、出現数の多い「準備データ」を採る |
| 期待値 | テスト実行後に期待する状態を表すデータ | `想定結果`（`NTF:05_UnitTestGuide/01_ClassUnitTest/02_componentUnitTest.rst:255` ほか現行6件）／`想定値`（`NTF:05_UnitTestGuide/01_ClassUnitTest/02_componentUnitTest.rst:310` ほか現行2件） | 現行解説書88件、input資料33件 |
| 特殊記法 | セル値・エントリ値を実値に変換する記法（`null`、`${systemTime}` など） | `セルへの特殊な記述方法`（`NTF:06_TestFWGuide/01_Abstract.rst:446`） | input資料20件。現行解説書の見出しはExcelのセルを前提としており、YAML形式に使えない |
| マーカーカラム | 読み込み対象外とするカラム。カラム名を半角角括弧で囲む | なし | 現行解説書4件（`NTF:06_TestFWGuide/01_Abstract.rst:348` ほか）、input資料17件 |
| ディレクティブ | ファイル・電文のフォーマット定義を指定する設定行 | なし | FW解説書24件（`FW:libraries/data_io/data_format/format_definition.rst:79` ほか）、現行解説書40件、input資料47件 |
| 固定長ファイル | レコード長・フィールド長が固定のファイル | なし | FW解説書15件、現行解説書21件、input資料24件 |
| 可変長ファイル | 区切り文字でフィールドを区切るファイル | なし | FW解説書2件（`FW:libraries/data_io/data_format/format_definition.rst:324` ほか）、現行解説書12件、input資料14件 |
| Excelファイル | Excel形式のテストデータファイル | `Excel ファイル`（`NTF:06_TestFWGuide/01_Abstract.rst:229`、`S:input/ntf-testdata-doc.md:593`） | 現行解説書86件 |

ファイルデータの行の名称は、input資料 `ntf-doc-terms.md` だけに現れる。現行解説書には該当語がないため、input資料の表記をそのまま採用する。

| 正表記 | 意味 | 揺れ表記 | 採用根拠 |
|---|---|---|---|
| レコード種別行 | レコード種別を示す行 | なし | `S:input/ntf-doc-terms.md:175`（input資料3件） |
| フィールド名称行 | 各フィールドの名称を並べた行 | なし | `S:input/ntf-doc-terms.md:176`（input資料15件） |
| データ型行 | 各フィールドのデータ型を示す行 | なし | `S:input/ntf-doc-terms.md:177`（input資料9件） |
| フィールド長行 | 各フィールドのバイト長を示す行。固定長ファイルのみ | なし | `S:input/ntf-doc-terms.md:178`（input資料11件） |

### 5.6 電文

| 正表記 | 意味 | 揺れ表記（file:line） | 採用根拠 |
|---|---|---|---|
| 電文 | メッセージングで送受信するメッセージ | なし | FW解説書122件、現行解説書46件、input資料35件 |
| 要求電文 | 送信側から受信側へ送るメッセージ | `リクエストメッセージ`（`NTF:05_UnitTestGuide/02_RequestUnitTest/http_real.rst:46`、`:49` ほか現行8件） | FW解説書49件（`FW:handlers/http_messaging/http_messaging_request_parsing_handler.rst:11` ほか）、現行解説書78件 |
| 応答電文 | 受信側から送信側へ返すメッセージ | `レスポンスメッセージ`（`NTF:05_UnitTestGuide/02_RequestUnitTest/delayed_receive.rst:51`、`:56` ほか現行10件） | FW解説書58件、現行解説書67件 |
| フレームワーク制御ヘッダ | 電文の先頭に付与する、Nablarchが解釈する制御情報 | `FW制御ヘッダ`（`NTF:05_UnitTestGuide/03_DealUnitTest/send_sync.rst:73`、`:74` ほか現行3件、`S:input/ntf-doc-terms.md:21` ほかinput4件） | FW解説書65件（`FW:handlers/http_messaging/http_messaging_request_parsing_handler.rst:83` ほか）、現行解説書13件 |
| メッセージボディ | フレームワーク制御ヘッダより後ろの、業務データの部分 | なし | FW解説書38件（`FW:libraries/log/messaging_log.rst:134` ほか）、現行解説書8件（`NTF:05_UnitTestGuide/02_RequestUnitTest/http_real.rst:39` ほか）、input資料2件 |
| フォーマット定義ファイル | 電文・ファイルのレイアウトを定義するファイル | なし | FW解説書55件、現行解説書9件、input資料2件 |

### 5.7 設定・ツール

| 正表記 | 意味 | 揺れ表記（file:line） | 採用根拠 |
|---|---|---|---|
| コンポーネント設定ファイル | システムリポジトリに登録するコンポーネントを定義するXMLファイル | なし | FW解説書105件、現行解説書47件、input資料5件 |
| システムリポジトリ | コンポーネントを保持し、名前で取得できるようにする仕組み | なし | FW解説書58件、現行解説書10件 |
| 内蔵サーバ | リクエスト単体テストで使用するサーブレットコンテナ | `内蔵サーブレットコンテナ`（`S:input/ntf-doc-terms.md:450`） | 現行解説書18件（`NTF:06_TestFWGuide/02_RequestUnitTest.rst:11` ほか）。FW解説書に該当語なし |
| HTMLダンプ | リクエスト単体テストで出力する、レスポンスHTMLのファイル | `HTML ダンプ`（`S:input/ntf-doc-terms.md:252`、`:457` ほかinput3件） | 現行解説書19件 |
| リクエスト単体データ作成ツール | ブラウザ操作からリクエスト単体テストのテストデータを作成するツール | なし | 現行解説書3件（`NTF:08_TestTools/01_HttpDumpTool/01_HttpDumpTool.rst:4` ほか）、`S:design.md:113` |
| マスタデータ投入ツール | マスタデータをデータベースへ投入するツール | なし | 現行解説書3件（`NTF:08_TestTools/02_MasterDataSetup/01_MasterDataSetupTool.rst:4` ほか）、`S:design.md:69` |
| マスタデータ復旧機能 | テストで変更されたマスタデータを元に戻す機能 | なし | 現行解説書2件（`NTF:06_TestFWGuide/04_MasterDataRestore.rst:4` ほか）、input資料1件、`S:design.md:68` |
| HTMLチェックツール | 出力HTMLの使用禁止タグ・属性を検査するツール | なし | 現行解説書3件（`NTF:08_TestTools/03_HtmlCheckTool/index.rst:4` ほか）、FW解説書2件 |
| テストデータ変換ツール | Excel形式とYAML形式のテストデータを相互変換するツール | なし | `S:input/testdata-converter-design.md:1`、`S:design.md:66` |
| JUnit 5用拡張機能 | JUnit 5でテスティングフレームワークを使うための拡張機能 | なし | 現行解説書1件（`NTF:06_TestFWGuide/JUnit5_Extension.rst:4`）、`S:design.md:67` |
| JUnit 5 | JUnitのバージョン5 | `JUnit5`（`NTF:06_TestFWGuide/index.rst:20`） | 現行解説書23件（`NTF:06_TestFWGuide/01_Abstract.rst:666` ほか）、`S:design.md:34` |
| JUnit 4 | JUnitのバージョン4 | `JUnit4`（`NTF:05_UnitTestGuide/02_RequestUnitTest/rest.rst:16`、`:62` ほか現行8件） | 現行解説書16件（`NTF:06_TestFWGuide/01_Abstract.rst:673` ほか）、`S:design.md:34` |

### 5.8 セクションタイトル

`design.md` の「3. 第2部 導入と設定」「4. 第3部 テストの実装方法」が定めるページのアウトラインで使う語である。

| 正表記 | 意味 | 揺れ表記（file:line） | 採用根拠 |
|---|---|---|---|
| 機能概要 | ページの最上位セクション。何ができるかを示す | `概要`（`NTF:05_UnitTestGuide/02_RequestUnitTest/delayed_receive.rst:6` ほか現行15件） | FW解説書のライブラリで26件（`FW:libraries/authorization/permission_check.rst:27` ほか）。`S:design.md:78`、`:134` |
| 使用方法 | ページの最上位セクション。使い方の手順を示す | `実施方法`（`NTF:05_UnitTestGuide/02_RequestUnitTest/index.rst:4` ほか現行44件） | FW解説書63件（`FW:libraries/...` 各ライブラリの見出し）。`S:design.md:82`、`:135` |
| 拡張例 | ページの最上位セクション。差し替え・独自実装の手順を示す | なし（現行解説書に0件） | FW解説書20件（`FW:libraries/authorization/permission_check.rst:256` ほか）。`S:design.md:86`、`:92` |
| モジュール一覧 | 依存モジュールを列挙するセクション | なし | FW解説書85件、現行解説書3件（`NTF:06_TestFWGuide/JUnit5_Extension.rst:35` ほか）。`S:design.md:34`、`:48` |
| 全体像 | 機能概要の下位セクション。図で構造を示す | なし | 現行解説書7件（`NTF:06_TestFWGuide/02_RequestUnitTest.rst:16` ほか）、input資料7件、FW解説書3件（`FW:nablarch/big_picture.rst:3`）。`S:design.md:79` |
| 主なクラスとリソース | 機能概要の下位セクション。クラス・リソースの名称・役割・作成単位を表で示す | `主なクラス, リソース`（現行解説書6件。`NTF:06_TestFWGuide/02_DbAccessTest.rst:23`、`NTF:06_TestFWGuide/02_RequestUnitTest.rst:24`、`NTF:06_TestFWGuide/RequestUnitTest_batch.rst:24`、`NTF:06_TestFWGuide/RequestUnitTest_real.rst:23`、`NTF:06_TestFWGuide/RequestUnitTest_rest.rst:20`、`NTF:06_TestFWGuide/RequestUnitTest_send_sync.rst:37`） | `S:design.md:80`、`:92`。半角カンマ＋空白は日本語の読点として不適切であり、`discover --rule punct` が両表記を同一グループとして検出した |
| 前提事項 | 機能概要の下位セクション。適用できないケースを示す | `前提条件`（現行解説書6件。`NTF:05_UnitTestGuide/02_RequestUnitTest/rest.rst:5`、`NTF:06_TestFWGuide/01_Abstract.rst:689` ほか） | `S:design.md:81`。FW解説書は本文で「前提条件」を8件使うが（`FW:batch/nablarch_batch/getting_started/getting_started.rst:13` ほか）、ライブラリのセクションタイトルとしては使っていない。セクションタイトルとしての先例がFW解説書にないため、`design.md` の決定と現行解説書4件（`NTF:06_TestFWGuide/02_RequestUnitTest.rst:63` ほか）に従う |

セクションタイトルは「〜する」形式とする（`S:design.md:90`、`:145`）。上表の名詞形は、アウトラインの枠を指す名称として使う。

### 5.9 一般表記

| 正表記 | 揺れ表記（file:line） | 採用根拠 |
|---|---|---|
| スーパクラス | `スーパークラス`（現行解説書22件。`NTF:05_UnitTestGuide/02_RequestUnitTest/rest.rst:15`、`:53` ほか。FW解説書1件 `FW:handlers/web/http_rewrite_handler.rst:105`） | **FW解説書と異なる表記を採用する。** FW解説書の用例は `http_rewrite_handler.rst:105` の1件のみで、同じFW解説書内の他のカタカナ語は長音を省いている（インタフェース75件、ユーザ175件、サーバ122件、いずれも長音付きの形は5件以下）。1件の例外に合わせるより、長音を省く側に揃えるほうが文書全体の一貫性が高い。現行解説書は20件対22件で拮抗しており、決め手にならない |
| インタフェース | `インターフェース`（現行解説書3件、input資料2件、FW解説書5件。`NTF:05_UnitTestGuide/02_RequestUnitTest/real.rst:181`、`S:input/ntf-doc-terms.md:483`、`FW:handlers/web/csrf_token_verification_handler.rst:128`） | FW解説書75件（`FW:batch/jsr352/application_design.rst:33` ほか）、現行解説書16件 |
| オーバーライド | `オーバライド`（現行解説書1件 `NTF:06_TestFWGuide/RequestUnitTest_real.rst:124`、FW解説書5件 `FW:handlers/web/http_character_encoding_handler.rst:82` ほか） | FW解説書11件、現行解説書11件。いずれのコーパスでも長音付きが多数 |
| ユーザ | 検出なし（`ユーザー` は全コーパスで0件） | FW解説書175件、現行解説書47件 |
| サーバ | 検出なし（`サーバー` は全コーパスで0件） | FW解説書122件、現行解説書13件 |
| データ | `データー`（`NTF:06_TestFWGuide/01_Abstract.rst:112`。コメントアウト行の1件） | FW解説書1,283件、現行解説書485件 |
| バイナリデータ | `バイナリーデータ`（`NTF:06_TestFWGuide/01_Abstract.rst:86`。コメントアウト行の1件） | FW解説書7件（`FW:handlers/web/multipart_handler.rst:213` ほか）、現行解説書4件（`NTF:06_TestFWGuide/RequestUnitTest_batch.rst:158` ほか）、input資料5件 |
| パーサ | `パーサー`（`S:input/ntf-testdata-doc-examples-table.md:120`） | input資料8件、FW解説書1件（`FW:libraries/tag.rst:1940`） |

---

## 6. 括弧の表記

`discover --rule paren` が、同じ型の見出しで括弧の全角・半角が混在していることを検出した。

| 見出しの型 | 半角括弧の例 | 全角括弧の例 |
|---|---|---|
| `リクエスト単体テストの実施方法（…）` | `NTF:05_UnitTestGuide/02_RequestUnitTest/batch.rst:4`、`NTF:05_UnitTestGuide/02_RequestUnitTest/mail.rst:4`、`NTF:05_UnitTestGuide/02_RequestUnitTest/real.rst:4`、`NTF:05_UnitTestGuide/02_RequestUnitTest/send_sync.rst:4`、`NTF:05_UnitTestGuide/02_RequestUnitTest/fileupload.rst:2`、`NTF:05_UnitTestGuide/02_RequestUnitTest/http_send_sync.rst:4` | `NTF:05_UnitTestGuide/02_RequestUnitTest/http_real.rst:2`、`NTF:05_UnitTestGuide/02_RequestUnitTest/delayed_receive.rst:2`、`NTF:05_UnitTestGuide/02_RequestUnitTest/delayed_send.rst:2` |
| `取引単体テストの実施方法（…）` | 開きが全角・閉じが半角の混在が1件（`NTF:05_UnitTestGuide/03_DealUnitTest/real.rst:2`） | `NTF:05_UnitTestGuide/03_DealUnitTest/batch.rst:2`、`NTF:05_UnitTestGuide/03_DealUnitTest/delayed_receive.rst:2`、`NTF:05_UnitTestGuide/03_DealUnitTest/delayed_send.rst:2` |

**日本語の文・見出しの中では全角括弧 `（）` を使う。** 半角括弧はソースコード・識別子・英字の中でのみ使う。

## 7. 数字・英字の表記

- 製品名・仕様名の数字は原典の表記に従う（`JUnit 5`、`Jakarta Batch`、`HTML4.01`）
- 半角英数字と日本語の間に空白を入れない（`Excelファイル`、`HTMLダンプ`）。`discover --rule punct` はこの空白を除去して比較するため、`HTML ダンプ出力`（`S:input/ntf-doc-terms.md:457`）と `HTMLダンプ出力`（`NTF:06_TestFWGuide/02_RequestUnitTest.rst:280`）、`RESTful ウェブサービス`（`S:input/ntf-doc-terms.md:473`）と `RESTfulウェブサービス`（`NTF:06_TestFWGuide/RequestUnitTest_rest.rst:4`）を同一グループとして検出した

## 8. 対応表（現行解説書の主要な語 → 正表記）

ページ作成時の置き換え表である。左の語を見つけたら右に直す。

| 現行解説書・input資料の語 | 正表記 |
|---|---|
| 自動テストフレームワーク／テストフレームワーク／本フレームワーク／NTF | テスティングフレームワーク |
| バッチ処理（処理方式を指す場合） | Nablarchバッチアプリケーション |
| メッセージング処理（処理方式を指す場合） | MOMによるメッセージング |
| 応答不要メッセージ送信処理／受信処理 | 応答不要メッセージ送信／受信 |
| 同期応答メッセージ送信処理／受信処理／メッセージ受信処理 | 同期応答メッセージ送信／受信 |
| Form/Entity単体テスト | エンティティ単体テスト |
| Action/Component単体テスト | コンポーネント単体テスト |
| セクション（テストデータの単位） | データブロック |
| グループ ID／groupId | グループID |
| テストショット一覧／テストケース表 | テストケース一覧 |
| 事前準備データ／セットアップデータ | 準備データ |
| 想定結果／想定値 | 期待値 |
| セルへの特殊な記述方法 | 特殊記法 |
| リクエストメッセージ／レスポンスメッセージ | 要求電文／応答電文 |
| FW制御ヘッダ | フレームワーク制御ヘッダ |
| 内蔵サーブレットコンテナ | 内蔵サーバ |
| 概要 | 機能概要 |
| 実施方法 | 使用方法 |
| 主なクラス, リソース | 主なクラスとリソース |
| 前提条件 | 前提事項 |
| スーパークラス | スーパクラス |
| インターフェース | インタフェース |
| データシート | シート |

## 9. ntf-doc-terms.md の候補の突き合わせ結果

`input/ntf-doc-terms.md` の各節について、現行解説書・FW解説書と突き合わせた結果を示す。表中の `L` に続く数字は、すべて `S:input/ntf-doc-terms.md` の行番号である。

| ntf-doc-terms.md の節 | 判定 | 理由 |
|---|---|---|
| データタイプ（L36） | 採用 | 現行解説書43件・input資料57件で一貫。データタイプ名は識別子であり表記の選択余地がない |
| シート・行・列・セル（L61） | 修正 | 「シート」「セル」はExcel形式に固有の語である。YAML形式を含めて記述する箇所では「データブロック」「テストデータファイル」を使う。行の名称（1行目・2行目・3行目以降）はExcel形式の説明に限って使う |
| 特殊記法（L84） | 採用 | 5.5に「特殊記法」として掲載。現行解説書の見出し「セルへの特殊な記述方法」を置き換える |
| マーカーカラム（L98） | 採用 | 現行解説書4件・input資料17件で一致 |
| コメント（L102） | 採用 | 表記揺れなし |
| 設計原則（L110）— テスト独立性・データ集約・データタイプまとめ記述 | 不採用 | 3語とも `ntf-doc-terms.md` の造語で、現行解説書・FW解説書に0件。現行解説書は「テストメソッドの実行順序に依存しないテストを作成する」（`NTF:06_TestFWGuide/01_Abstract.rst:585`）のように文で書いている。`design.md` のセクションタイトル「〜する」形式に合うため、文のまま引き継ぐ |
| グループ ID（L118） | 修正 | 空白を除いた「グループID」を正表記とする。現行解説書73件が空白なし |
| データタイプ別の行構造（L129） | 採用 | レコード種別行・フィールド名称行・データ型行・フィールド長行を5.5に掲載。現行解説書に該当語がないため、input資料の表記をそのまま採る |
| ディレクティブ（L213） | 採用 | FW解説書24件と一致 |
| testShots / requestParams（L234） | 採用（識別子として） | `testShots` `requestParams` はデータブロックのIDであり識別子。日本語の総称は「テストケース一覧」を使う |
| メッセージング 基本用語（L327） | 修正 | 「電文」「要求電文」「応答電文」「フレームワーク制御ヘッダ」「メッセージボディ」はFW解説書と一致するため採用。「電文種別」はFW解説書・現行解説書に0件のため不採用とし、「要求電文」「応答電文」で書き分ける |
| HTTP 同期応答メッセージ送信の用語読み替え（L398） | 採用 | クラス名の対応表であり、表記の選択余地がない |
| テスト種別の正式名称（L414） | 修正 | 「リクエスト単体テスト（バッチ処理）」「（メッセージ受信処理）」「（RESTful ウェブサービス）」は処理方式名が `design.md` の正式名称と異なる。5.2・5.3の正表記に置き換える |
| DB アクセステスト（L427） | 不採用（用語として） | 「DBアクセステスト」は `ntf-doc-terms.md` の造語で、現行解説書は「データベースを使用するクラスのテスト」（`NTF:06_TestFWGuide/02_DbAccessTest.rst:2`）としている。テストの種類の分類軸ではなくクラス単体テストの一形態であるため、テストの種類には加えない |
| 主要クラス各節（L443 以降） | 採用（識別子として） | クラス名は識別子。日本語の役割説明は「主なクラスとリソース」の表に集約する |
| その他のフレームワーク固有用語（L526） | 修正 | 「内蔵サーバ」は採用（現行解説書18件）。併記の「内蔵サーブレットコンテナ」（L450）は使わない。`nablarch.test.resource-root` などの設定キーは識別子であり掲載対象外 |

## 10. 未解決事項

| # | 事項 | 内容 |
|---|---|---|
| 1 | 「データブロック」と「データタイプ」の役割分担 | 現行解説書は「データタイプ」1語で種別とデータのかたまりの両方を指している。本用語集はかたまりを「データブロック」、種別を「データタイプ」に分けたが、この分割は現行解説書にもFW解説書にも先例がない。第1部「テストデータ」の執筆時に、両語の関係を図で示す必要がある |
| 2 | 「シート」を残す範囲 | YAML形式にはシートがない。Excel形式の説明でのみ「シート」を使う方針としたが、どのセクションをExcel形式限定の記述にするかはマッピング（タスク #5）で確定する |
| 3 | メッセージング方式4種と処理方式ページの対応 | `design.md` の第3部は「MOMによるメッセージング」を1ページとしているが、現行解説書は応答不要送信・応答不要受信・同期応答受信・同期応答送信の4方式を別ページに持つ。1ページに収めるか分割するかは `design.md` の未確定事項1・2と同じくマッピング後の文量集計で判断する。用語集としては4方式の正表記を確定した |
| 4 | HTTPメッセージングの送信側・受信側の名称 | 「HTTP同期応答メッセージ送信／受信」はFW解説書に用例がなく、現行解説書にも各1件しかない。FW解説書 `libraries/system_messaging/http_system_messaging.rst` の見出しと突き合わせて、第2部・第3部の執筆時に再確認する |
