# NTF解説書 用語集

## 1. 適用範囲と行番号の基準

本用語集は、再構築するNTF解説書の全ページで使用する表記の唯一の基準である。ページ作成時は本書の「正表記」を使い、「揺れ表記（使わない）」は使わない。

**適用対象は解説書のページ本文だけである。** 本用語集・`design.md`・`ntf-doc-rebuild-instruction.md`・`checks/` などの作業文書には適用しない。作業文書は「NTF解説書」「NTF」のような作業用の略称を使ってよい。

file:line の基準は取得元ごとに異なる。

| 記号 | 展開 | 行番号の基準 |
|---|---|---|
| `NTF:` | `ja/development_tools/testing_framework/guide/development_guide/` | 基準コミット `c2419060` 時点の内容。作業ツリーではない |
| `NTF-root:` | `ja/development_tools/testing_framework/` | 同上 |
| `FW:` | `ja/application_framework/application_framework/` | 作業ツリー |
| `S:` | `.rn/20260724-ntf-yaml-support/` | 作業ツリー |

基準コミットは `mapping/tools/detect_term_variants.py` の `DEFAULT_BASE_COMMIT` に定数として固定してある（環境変数 `NTF_BASE_COMMIT` で上書きできる）。実行時に `git merge-base origin/develop HEAD` を解決する方式は採らない。develop に変更が入った瞬間に、警告もエラーもなく全 `NTF:` 行番号がずれるためである。現行解説書の内容は `git show c24190607fef5d76c607aa08b36d2ab2f813efe5:<path>` で取得する。

### 「出現数」の定義

「出現数」は検出スクリプト `detect_term_variants.py scan` が数えたマッチ数である。次の3点に注意すること。

- **`mapping/tools/term_candidates.tsv` 相対の数である。** 1行内では最長一致で非重複にマッチさせるため、tsv に長い表記が載っていると短い表記はその位置で数えない。したがって生の `grep` の件数とは一致しない。現行解説書での実例: `電文` は46（生191）、`データ` は483（生828）、`単体テスト` は8（生201）。tsv に載せる表記の集合を変えると出現数も変わる。
- 1行に同じ表記が複数回現れる場合はその回数だけ数える。file:line は重複を除いて出す。
- コーパスは `current`（現行解説書）/ `input` / `fw`（FW解説書）/ `design` の4つ。表中では「現行N件」「inputN件」「FWN件」「designN件」と書く。

出現数と file:line の全件は `mapping/scan-terms.tsv` にコミットしてある。本書の表には代表1件だけを載せる。

### 検証

本書の記述は `mapping/tools/verify_glossary.py` で機械的に検査する。検査対象は「file:line 参照の実在と内容」「件数主張と `scan` 出力の一致」「§5 と §8 の整合」「`term_candidates.tsv` と §5 の整合」「§8 全行に適用条件があること」の5つ。

```
python3 mapping/tools/detect_term_variants.py scan --max-locations 0 -o mapping/scan-terms.tsv
python3 mapping/tools/verify_glossary.py
```

## 2. 採用の優先順位

`design.md` の「6. 用語」に従い、次の順で正表記を決めた。

1. FW解説書（`FW:`）に同じ概念の用語があれば、その表記を採用する
2. FW解説書にない場合、現行解説書・input資料のうち意味が明確で一貫しているものを採用する
3. いずれにもない場合、`design.md` の決定に従うか、新たに定義する

FW解説書と異なる表記を採用した用語は、採用根拠にその理由を記載した。該当するのは「スーパクラス」「前提事項」「単項目バリデーション」の3件である。

`input/ntf-doc-terms.md` は候補リストとして扱い、そのまま採用していない。突き合わせ結果は §9 に示す。§9 で「修正」「不採用」と判定した節があるため、個々の語の意味も `ntf-doc-terms.md` をそのまま引かず、本書に載せた語は本書の「意味」列を基準とする。

## 3. 掲載基準

次のいずれかに当てはまる用語を掲載した。**揺れが検出されたかどうかは掲載の条件ではない。** 骨格となる概念は揺れがなくても掲載する。

1. 処理方式・テストの種類・テストデータの構造など、複数ページに横断して現れる骨格の用語
2. ページのセクションタイトルに使う用語
3. 検出スクリプトが表記揺れを検出した用語

次のものは掲載していない。

- Javaのクラス名・メソッド名・カラム名・データタイプ名（`HttpRequestTestSupport`、`assertTableEquals`、`testShots`、`SETUP_TABLE` など）。これらは原文の識別子であり、表記の選択余地がない
- 1つの機能の説明の中に閉じており、他の機能のページから参照されない固有名詞（`Antビュー` はマスタデータ投入ツールの2ファイルのみ、`app-log.properties` はマスタデータ復旧機能とマスタデータ投入ツールのみ）
- 一般的な日本語語彙で、揺れが検出されなかったもの

## 4. 表記揺れの検出方法

検出は `mapping/tools/detect_term_variants.py` で行う。

```
# 正解リストを持たずに揺れを見つける（正規化してグループ化する）
python3 mapping/tools/detect_term_variants.py discover --rule punct
python3 mapping/tools/detect_term_variants.py discover --rule paren
python3 mapping/tools/detect_term_variants.py discover --rule longvowel
python3 mapping/tools/detect_term_variants.py discover --rule spacing

# 用語定義ファイルの表記を全コーパスから探し、出現数と file:line を出す
python3 mapping/tools/detect_term_variants.py scan --max-locations 0 -o mapping/scan-terms.tsv
```

`discover` の既定コーパスは `current,input,design` で、**FW解説書を含まない**（FW解説書はNTF以外の話題を大量に含み、正規化グループが実務と無関係な語で埋まるため）。一方 `scan` の既定は4コーパス全部である。したがって本書のFW件数を `discover` で再現することはできない。FW解説書を `discover` にかける場合は `--corpus fw` を明示する。

| ルール | 抽出単位 | 正規化 | 揺れと判定する軸 | 検出したグループ数 |
|---|---|---|---|---|
| `punct` | 見出しと本文の「」内の語 | `、` `,` `，` `・` `/` `／` 空白 と接続助詞「と」を除去 | 表記そのもの | 3 |
| `paren` | 同上（丸括弧を含むもの） | 丸括弧の中身をマスクし、全角・半角の差も伏せる | 使っている括弧の種類 | 2 |
| `longvowel` | カタカナ語（3文字以上） | `ー` を除去 | 表記そのもの | 6 |
| `spacing` | **本文の全行**から取った「英数字・カタカナ・漢字が半角空白1個を挟んで連なる塊」（英数字と日本語が混在するものに限る） | 半角空白を除去 | 表記そのもの | 60 |

### 検出できるもの／検出できないもの

網羅性の主張を循環させないため、検出器の限界を明記する。

- `punct` / `paren` / `longvowel` の3ルールが機械的に見つけた揺れは合計11グループにすぎない。§5 の「揺れ表記」約50件のうち残りは、**人手で作った `term_candidates.tsv` を `scan` にかけて数え直したもの**である。数え直しは機械が行っているが、**何を揺れ候補とするかの発見は人手**である。
- `spacing` はこの限界を埋めるために本タスクで追加した。散文・表セルにしか現れない `グループ ID`・`リクエスト ID`・`HTML ダンプ`・`Excel ファイル`・`RESTful ウェブサービス`・`FW 制御ヘッダ` は `punct` では1件も検出できていなかった（`punct` の抽出単位が見出しと「」内の語に限られるため）。`spacing` が60グループを報告し、うち用語として裁定したものを §5 に載せた。
- `paren` は、同じ型の見出しが1つしかない場合を原理的に検出できない。現行解説書で半角括弧を使う見出しは13件あるが、`paren` が報告するのは7件で、残り6件（`NTF:05_UnitTestGuide/01_ClassUnitTest/02_componentUnitTest.rst:161`、`:255`、`:310`、`NTF:05_UnitTestGuide/02_RequestUnitTest/delayed_send.rst:82`、`NTF:05_UnitTestGuide/02_RequestUnitTest/send_sync.rst:8`、`NTF:05_UnitTestGuide/02_RequestUnitTest/index.rst:489`）は対になる全角括弧の見出しがないため報告されない。
- 送り仮名・漢字/かなの揺れ（`出来る`／`できる` など）は、3ルールのどれでも同一キーに畳まれないため検出できない。これは §6 のとおり #4 の管轄とし、実測値を申し送る。

---

## 5. 用語

各表の列は次のとおり。

- **正表記** — 解説書で使う表記
- **意味** — 1〜2文。文末は体言止めに揃える
- **揺れ表記（使わない）** — 同じ概念を指す別表記。解説書では使わない。代表1件の file:line と出現数のみを載せる。全件は `mapping/scan-terms.tsv` を引く
- **別義・旧名称（文脈により使う）** — 同じ文字列だが別の概念を指すもの、または旧名称。FW解説書への言及や旧名称の説明では使ってよい
- **採用根拠** — なぜその表記を正としたか

「揺れなし」は同じ概念の別表記が見つからないこと、「未出現」はその表記が全コーパスに0件であることを指す。

### 5.1 全体・Nablarchの基本概念

| 正表記 | 意味 | 揺れ表記（使わない） | 別義・旧名称（文脈により使う） | 採用根拠 |
|---|---|---|---|---|
| `テスティングフレームワーク` | Nablarchアプリケーションのテストを補助する機能を提供するフレームワーク。本解説書が説明する対象 | `自動テストフレームワーク`（現行70件、`NTF:06_TestFWGuide/index.rst:4`）／`テストフレームワーク`（現行1件、`NTF:06_TestFWGuide/03_Tips.rst:825`）／`本フレームワーク`（現行14件、`NTF:05_UnitTestGuide/02_RequestUnitTest/mail.rst:10`）／`NTF`（input42件、`S:input/ntf-doc-terms.md:1`。現行2件、`NTF:05_UnitTestGuide/02_RequestUnitTest/http_real.rst:153`） | `本フレームワーク` はFW解説書ではNablarch自体を指す（FW10件、`FW:libraries/database/database.rst:442`） | FW解説書が `テスティングフレームワーク` を使う（FW8件、`FW:blank_project/CustomizeDB.rst:141`）。現行解説書の最上位ページ題も同じ（`NTF-root:index.rst:2`）。「機能の総称」ではなく「機能を提供するもの」と定義した。第1部の記載内容は「Nablarchに特化したテスト補助機能を提供すること」（`S:design.md:29`）であり、総称として定義すると「テスティングフレームワークを提供する」と書けなくなるため |
| `ハンドラキュー` | リクエストの処理を担うハンドラを直列に並べた構造 | 揺れなし（`ハンドラーキュー` は未出現） | なし | `ハンドラキュー` はFW解説書の基本用語（FW84件、`FW:batch/nablarch_batch/architecture.rst:48`）。`S:design.md:30` が第1部で使うと決めている（design2件）。現行解説書は `ハンドラキュー` を現行1件（`NTF:06_TestFWGuide/RequestUnitTest_rest.rst:320`）しか使っていないが、リクエスト単体テストの説明に不可欠なため掲載基準1で掲載する |
| `リクエストID` | 業務処理を一意に識別する文字列 | `リクエスト ID`（input13件、`S:input/ntf-doc-terms.md:52`） | なし | FW解説書120件（`FW:batch/nablarch_batch/architecture.rst:52`）、現行解説書47件（`NTF:05_UnitTestGuide/01_ClassUnitTest/02_componentUnitTest.rst:103`）がいずれも空白なし。`グループ ID` と同型の半角空白の揺れであり、`discover --rule spacing` が同一グループとして検出した |

### 5.2 処理方式

`design.md` の「5. 処理方式の名称」の7名称と一致する。名称はFW解説書の各章の題を採る。

FW解説書で「編」が付くのは**カテゴリ章とウェブサービスの下位章の計6見出し**である（`FW:batch/index.rst:3`、`FW:messaging/index.rst:3`、`FW:web/index.rst:3`、`FW:web_service/index.rst:3`、`FW:web_service/rest/index.rst:3`、`FW:web_service/http_messaging/index.rst:3`）。バッチ・メッセージングの下位章には付かない（`FW:batch/nablarch_batch/index.rst:3`、`FW:messaging/mom/index.rst:3`、`FW:messaging/db/index.rst:3`）。本解説書は処理方式をページ題に使うため、「編」は付けない。

| 正表記 | 意味 | 揺れ表記（使わない） | 別義・旧名称（文脈により使う） | 採用根拠 |
|---|---|---|---|---|
| `ウェブアプリケーション` | 画面を持つHTTPアプリケーション | 揺れなし（`WEBアプリケーション` は未出現） | `Webアプリケーション` はFW解説書自身が使う正用法（FW10件、`FW:batch/jsr352/architecture.rst:127`）。現行解説書・input資料には0件 | `FW:web/index.rst:3`。FW解説書では `ウェブアプリケーション` がFW83件に対し `Webアプリケーション` はFW10件で、前者が優勢 |
| `RESTfulウェブサービス` | REST APIを提供するウェブサービス | `RESTful ウェブサービス`（input2件、`S:input/ntf-doc-terms.md:420`） | なし | `FW:web_service/rest/index.rst:3`。FW解説書72件、現行解説書13件（`NTF:05_UnitTestGuide/02_RequestUnitTest/rest.rst:8`） |
| `HTTPメッセージング` | HTTPを使ったシステム間メッセージング | 揺れなし（`HTTP メッセージング` は未出現） | なし | `FW:web_service/http_messaging/index.rst:3`。FW解説書37件（`FW:handlers/http_messaging/http_messaging_error_handler.rst:3`）。現行解説書・input資料には0件だが、`S:design.md:120` が第3部の章に使うと決めている |
| `Nablarchバッチアプリケーション` | Nablarch独自のバッチアプリケーション | `バッチ処理`（現行14件、`NTF:05_UnitTestGuide/02_RequestUnitTest/batch.rst:40`） | `バッチアプリケーション`（FW81件、`FW:batch/functional_comparison.rst:23`）は、Nablarch製かJakarta Batch製かを問わないバッチ全般の意でFW解説書が使う | `FW:batch/nablarch_batch/index.rst:3`。「バッチ処理」はJakarta Batchを含みうるため、処理方式名としては使わない |
| `MOMによるメッセージング` | MOM（メッセージ指向ミドルウェア）を使ったメッセージング | `メッセージング処理`（現行12件、`NTF:05_UnitTestGuide/index.rst:49`） | `MOMメッセージング` はFW解説書のライブラリ章題として使われる正用法（FW35件、`FW:handlers/mom_messaging/index.rst:1`） | `FW:messaging/mom/index.rst:3`。処理方式の章題は「MOMによるメッセージング」、ライブラリの章題は「MOMメッセージング」であり、処理方式を指す場合は前者を使う |
| `テーブルをキューとして使ったメッセージング` | データベースのテーブルをキューとして使うメッセージング | 揺れなし | なし | `FW:messaging/db/index.rst:3`。FW解説書19件。現行解説書・input資料には0件 |
| `Jakarta Batchに準拠したバッチアプリケーション` | Jakarta Batch仕様に準拠したバッチアプリケーション。NTFの対象外 | 揺れなし | `JSR352に準拠したバッチアプリケーション` はNablarch5までの旧名称。FW解説書自身が旧名称として1件挙げている（`FW:batch/jsr352/index.rst:17`） | `FW:batch/jsr352/index.rst:3`。現行解説書も新名称を使う（`NTF-root:index.rst:22`） |

### 5.3 バッチの起動方式

処理方式ではなく、Nablarchバッチアプリケーションの起動のしかたの分類である（`design.md` の処理方式の表には含まれない）。

| 正表記 | 意味 | 揺れ表記（使わない） | 別義・旧名称（文脈により使う） | 採用根拠 |
|---|---|---|---|---|
| `常駐バッチ` | 起動後に常駐して処理を続けるバッチ | 揺れなし | なし | `FW:batch/nablarch_batch/architecture.rst:21`。FW解説書22件、現行解説書2件（`NTF:06_TestFWGuide/RequestUnitTest_batch.rst:184`）、input資料2件 |
| `都度起動バッチ` | 実行のたびに起動されるバッチ | 揺れなし | なし | `FW:batch/nablarch_batch/architecture.rst:16`。FW解説書28件。現行解説書には0件だが、常駐バッチとの対比に必要 |

### 5.4 メッセージング方式

現行解説書は末尾に「処理」を付けるが、FW解説書は付けない。FW解説書を採る。

| 正表記 | 意味 | 揺れ表記（使わない） | 別義・旧名称（文脈により使う） | 採用根拠 |
|---|---|---|---|---|
| `応答不要メッセージ送信` | 応答を待たずにメッセージを送信する方式 | `応答不要メッセージ送信処理`（現行8件、`NTF:05_UnitTestGuide/02_RequestUnitTest/delayed_send.rst:2`） | なし | 見出し「応答不要でメッセージを送信する(応答不要メッセージ送信)」（`FW:libraries/system_messaging/mom_system_messaging.rst:135`。原文は半角括弧）。`応答不要メッセージ送信` はFW7件。FW解説書にも `応答不要メッセージ送信処理` が1件ある（`FW:libraries/system_messaging/mom_system_messaging.rst:179`）ので「FW解説書は付けない」は例外なしではないが、見出しはすべて「処理」なし |
| `応答不要メッセージ受信` | 応答を返さずにメッセージを受信する方式 | `応答不要メッセージ受信処理`（現行5件、`NTF:05_UnitTestGuide/02_RequestUnitTest/delayed_receive.rst:2`） | なし | 見出し「応答不要でメッセージを受信する(応答不要メッセージ受信)」（`FW:libraries/system_messaging/mom_system_messaging.rst:470`。原文は半角括弧）。`応答不要メッセージ受信` はFW6件 |
| `同期応答メッセージ送信` | メッセージを送信し、応答を待つ方式 | `同期応答メッセージ送信処理`（現行32件、`NTF:05_UnitTestGuide/02_RequestUnitTest/http_send_sync.rst:117`。input4件） | なし | 見出し「同期応答でメッセージを送信する(同期応答メッセージ送信)」（`FW:libraries/system_messaging/mom_system_messaging.rst:330`。原文は半角括弧）。`同期応答メッセージ送信` はFW9件 |
| `同期応答メッセージ受信` | メッセージを受信し、応答を返す方式 | `同期応答メッセージ受信処理`（現行7件、`NTF:05_UnitTestGuide/02_RequestUnitTest/real.rst:4`）／`メッセージ受信処理`（現行2件、`NTF:06_TestFWGuide/RequestUnitTest_real.rst:2`） | なし | 見出し「同期応答でメッセージを受信する(同期応答メッセージ受信)」（`FW:libraries/system_messaging/mom_system_messaging.rst:638`。原文は半角括弧）。`同期応答メッセージ受信` はFW5件。「メッセージ受信処理」は応答不要受信と区別できないため使わない |
| `HTTPメッセージ送信` | HTTPで外部システムにメッセージを送信し、その応答を受信する方式 | `HTTP同期応答メッセージ送信処理`（現行8件、`NTF:05_UnitTestGuide/02_RequestUnitTest/http_send_sync.rst:4`）／`HTTP同期応答メッセージ送信`（現行1件、`NTF:06_TestFWGuide/RequestUnitTest_http_send_sync.rst:12`）／`HTTP 同期応答メッセージ送信`（input4件、`S:input/ntf-doc-terms.md:398`）／`HTTP 同期応答メッセージ送信処理`（input1件、`:424`） | なし | 見出し「メッセージを送信する(HTTPメッセージ送信)」（`FW:libraries/system_messaging/http_system_messaging.rst:132`。原文は半角括弧）。直後の本文「外部システムに対してメッセージを送信し、その応答を受信する」（`:134`）は、現行解説書の「HTTP同期応答メッセージ送信」と同じ動作を指す。`HTTPメッセージ送信` はFW5件。うち `FW:libraries/system_messaging/http_system_messaging.rst:40` は同ファイル冒頭の一覧表にある `:ref:` ラベルである。MOM側（上4行）と同じ見出しパターンであり、採用優先順位1をそのまま適用する |
| `HTTPメッセージ受信` | HTTPで外部システムからメッセージを受信し、その応答を送信する方式 | `HTTP同期応答メッセージ受信`（現行1件、`NTF:05_UnitTestGuide/02_RequestUnitTest/http_real.rst:23`）／`HTTP同期応答メッセージ受信処理`（現行3件、`NTF:05_UnitTestGuide/02_RequestUnitTest/http_real.rst:2`） | なし | 見出し「メッセージを受信する(HTTPメッセージ受信)」（`FW:libraries/system_messaging/http_system_messaging.rst:94`。原文は半角括弧）。`HTTPメッセージ受信` はFW4件。同上 |

### 5.5 テストの種類

| 正表記 | 意味 | 揺れ表記（使わない） | 別義・旧名称（文脈により使う） | 採用根拠 |
|---|---|---|---|---|
| `クラス単体テスト` | クラス単体を対象とし、JUnitで自動実行するテスト | 揺れなし（下の注記を参照） | `単体テスト`（現行8件、`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:7`）は3種を束ねた総称であり、クラス単体テストの別表記ではない | `クラス単体テスト` は現行解説書26件（`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:4`）、`S:design.md:31` |
| `リクエスト単体テスト` | 1リクエストを対象とし、ハンドラキューを通してJUnitで自動実行するテスト | 揺れなし | なし | 現行解説書106件（`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:587`）。FW解説書も `リクエスト単体テスト` を使う（FW6件、`FW:blank_project/MavenModuleStructures/index.rst:186`）。`S:design.md:30` |
| `取引単体テスト` | 複数リクエストにまたがる業務の流れを手動操作で確認するテスト | 揺れなし | なし | 現行解説書40件（`NTF:05_UnitTestGuide/02_RequestUnitTest/double_transmission.rst:9`）、`S:design.md:31` |
| `エンティティ単体テスト` | クラス単体テストのうち、FormクラスとEntityクラスのバリデーションを対象とするもの | `Form単体テスト`（現行5件、`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:6`）／`Entity単体テスト`（現行5件、`:6`）／`Form/Entity単体テスト`（現行4件、`:14`）／`Form/Entityの単体テスト`（現行1件、`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/index.rst:4`） | なし | `S:design.md:115`。読者がクラス名の組み合わせではなくテスト対象の種類で引けるようにするため、`design.md` の決定に従う。Formクラスを書く読者が「エンティティ」から辿り着けるよう、意味欄に対象クラスを明示し、§8 に略称4種の行を置く |
| `コンポーネント単体テスト` | クラス単体テストのうち、ActionクラスとComponentクラスを対象とするもの | `Action/Componentのクラス単体テスト`（現行2件、`NTF:05_UnitTestGuide/01_ClassUnitTest/02_componentUnitTest.rst:4`）／`Component単体テスト`（現行2件、`:6`）／`Action単体テスト`（現行1件、`:7`）／`Action/Component単体テスト`（現行1件、`:10`） | ここでいう「コンポーネント」はJavaのActionクラス・Componentクラスを指す。システムリポジトリに登録するコンポーネント（§5.12 `コンポーネント設定ファイル`）とは別義 | `S:design.md:116`。同上 |
| `データベースを使用するクラスのテスト` | クラス単体テストのうち、データベースアクセスを伴うクラスを対象とするもの | `DB アクセステスト`（input1件、`S:input/ntf-doc-terms.md:427`。`DBアクセステスト` は未出現） | なし | 現行解説書のページ題である（`データベースを使用するクラスのテスト` 現行1件、`NTF:06_TestFWGuide/02_DbAccessTest.rst:2`）。`DB アクセステスト` は `ntf-doc-terms.md` の造語で、完全一致の `DBアクセステスト` は全コーパスに0件。テストの種類の分類軸ではなくクラス単体テストの一形態のため、§5.5 の下位に置く |

**`単体テスト` 単独について。** 現行解説書に `単体テスト` は生で201件あるが、そのほとんどは `リクエスト単体テスト`・`取引単体テスト`・`クラス単体テスト`・`Form単体テスト` などの後半部分である。`term_candidates.tsv` に `単体テスト` を含むより長い表記を13種登録したうえで数えると、単独の `単体テスト` は現行8件まで減る。その8件も「両者はほぼ同じように単体テストを行える」（`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:7`）のように**3種を束ねた総称**として使われており、クラス単体テストの別表記ではない。「単体テスト実施方法」（`NTF:05_UnitTestGuide/index.rst:4`）も3種を束ねる親indexのページ題である。したがって `単体テスト` を「クラス単体テスト」の揺れ表記とはしない。§8 には条件付きの行を置く。

### 5.6 バリデーション

現行解説書は「精査」、FW解説書は「バリデーション」を使う。コーパス全体で最大の乖離であり、採用優先順位1が最も強く効くケースである。

| 正表記 | 意味 | 揺れ表記（使わない） | 別義・旧名称（文脈により使う） | 採用根拠 |
|---|---|---|---|---|
| `バリデーション` | 入力値が業務上の規則を満たすかを検証する処理 | `精査`（現行47件、`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:26`。FW4件） | なし | FW解説書316件（`FW:batch/jsr352/feature_details/run_batch_application.rst:44`）に対し `精査` はFW4件（`FW:libraries/validation/nablarch_validation.rst:303` ほか）。現行解説書も `バリデーション` を6件使っている |
| `相関バリデーション` | 複数の項目の値の関係を検証するバリデーション | `項目間精査`（現行7件、`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:430`） | なし | FW解説書34件（`FW:batch/nablarch_batch/application_design.rst:28`）。`FW:libraries/validation/bean_validation.rst:400` に「相関バリデーションを行う」というセクションタイトルがある |
| `単項目バリデーション` | 1つの項目の値だけを見て行うバリデーション | `単項目精査`（現行38件、`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:66`） | なし | **FW解説書に確立した表記がない。** FW解説書での用例は `単項目バリデーション` がコード中のコメント1件（`FW:web/getting_started/project_upload/index.rst:336`）、散文の「項目単体のバリデーション」が2件のみ。現行解説書は `単項目精査` をセクションタイトルに使っており、名詞句の形を保つ必要がある。`相関バリデーション`（FW34件）と対になる複合語の形を採り、採用優先順位3（新たに定義する）で確定した |
| `ドメインバリデーション` | ドメイン定義に基づいて行うバリデーション | 揺れなし | なし | FW解説書28件（`FW:libraries/code.rst:433`）。エンティティ単体テストの説明で参照するため掲載する |

### 5.7 テストの骨格

`design.md` が第3部のセクションタイトルに使うと決めている語である（「テストクラスを作成する」`S:design.md:136`、「テストメソッドを作成する」`S:design.md:137`）。揺れはないが、全ページに横断するため掲載基準1で掲載する。

| 正表記 | 意味 | 揺れ表記（使わない） | 別義・旧名称（文脈により使う） | 採用根拠 |
|---|---|---|---|---|
| `テストクラス` | テストを記述するJavaクラス。1つのテストデータファイル群と対応するもの | 揺れなし | なし | 現行解説書138件（`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:16`）、input資料9件、`S:design.md:30` |
| `テストメソッド` | テストクラス内の1つのテストを表すメソッド | 揺れなし | なし | 現行解説書70件（`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:62`）、input資料6件、`S:design.md:137` |
| `テストケース` | 1組の入力と期待値からなる、テストの1件分 | `テストショット`（現行10件、`NTF:05_UnitTestGuide/02_RequestUnitTest/double_transmission.rst:20`） | なし | 現行解説書155件（`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:26`）、input資料38件。「テストショット」はクラス名 `TestShot` の直訳であり、読者が意味を推測できない |

### 5.8 テストデータ

| 正表記 | 意味 | 揺れ表記（使わない） | 別義・旧名称（文脈により使う） | 採用根拠 |
|---|---|---|---|---|
| `テストデータ` | テストクラスとは別のファイルに記述する、準備データと期待値とテストケース一覧の総称 | 揺れなし | なし | `テストデータ` は現行解説書223件（`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:16`）、input資料32件で一貫している。テストケース一覧は準備データでも期待値でもないため、総称には3者を含める |
| `テストデータファイル` | テストデータを記述したファイル。Excel形式とYAML形式がある | 揺れなし | なし | input資料4件（`S:input/ntf-testdata-doc-examples-messaging.md:133`）。YAML形式の追加により「Excelファイル」では総称にならないため採用する |
| `Excel形式` | Excelブックにテストデータを記述する形式 | 揺れなし | なし | 現行解説書1件（`NTF:08_TestTools/01_HttpDumpTool/01_HttpDumpTool.rst:27`）。YAML形式との対比に必要な語であり、採用優先順位3で定義する |
| `YAML形式` | YAMLファイルにテストデータを記述する形式 | 揺れなし | なし | `S:design.md:52`。現行解説書・input資料に完全一致の用例はないが、`design.md` が第2部の章名（`S:design.md:65`）に使うと決めている |
| `読み込み単位` | 1つのテストクラスのテストデータを分割して読み込む単位。Excel形式では1シート、YAML形式では1ファイル | 揺れなし | なし | input資料6件（`S:input/ntf-testdata-doc.md:32`）。Excel形式とYAML形式で対応物が異なる階層に名前を与えるために必要 |
| `データブロック` | 読み込み単位の中に置く、1用途分のデータのまとまり。テストデータファイルの記述単位 | `セクション`（input30件、`S:input/ntf-doc-terms.md:347`） | `セクション` は文書のセクションの意でも使われる（design10件、`S:design.md:27`）。マッピングの section_id・heading_path 列もこの別義 | input資料34件（`S:input/ntf-testdata-doc-examples-messaging.md:5`）、`S:design.md:32`（第1部「テストデータ」に「データブロックの考え方」を置くと決めている）。他の用語に依存しない形で定義するため、「何によって識別されるか」ではなく「どこに置く何のまとまりか」で定義した。データタイプ・グループIDはデータブロックの属性である（下の注記を参照） |
| `データタイプ` | データブロックの用途を表す予約語。`SETUP_TABLE`、`EXPECTED_TABLE` など14種 | `データブロック種別`（input7件、`S:input/ntf-testdata-doc.md:96`） | ファイルデータの `データ型行`（§5.10）が示す「データ型」は、フィールドの型であって別概念 | 現行解説書43件（`NTF:05_UnitTestGuide/02_RequestUnitTest/batch.rst:74`）、input資料57件。Excel形式ではデータブロック先頭セルに書く文字列そのものであり、選択余地がない |
| `グループID` | 同じ読み込み単位に同じデータタイプのデータブロックを複数置くとき、それらを区別する標識 | `グループ ID`（input21件、`S:input/ntf-doc-terms.md:32`） | `groupId`（現行46件、`NTF:05_UnitTestGuide/01_ClassUnitTest/02_componentUnitTest.rst:259`。FW333件）はMavenのgroupId要素・参照ラベル tips_groupId・YAMLの group_id キー。FW解説書の `グループID` 22件のうち19件もMavenのグループID、3件は認可機能のグループID（`FW:libraries/authorization/permission_check.rst:92`、`:109`、`:131`）で、いずれも本用語とは別義 | 現行解説書73件（`NTF:05_UnitTestGuide/01_ClassUnitTest/02_componentUnitTest.rst:259`）が空白なし。書式は `データタイプ[グループID]=識別子の値` |
| `テストケース一覧` | 1テストクラスで実行するテストケースを列挙したデータブロック（`LIST_MAP=testShots`） | `テストショット一覧`（現行5件、`NTF:05_UnitTestGuide/02_RequestUnitTest/http_real.rst:13`）／`テストケース表`（現行9件、`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:110`）／`テストショット表`（現行2件、`NTF:05_UnitTestGuide/02_RequestUnitTest/http_real.rst:16`） | なし | `テストケース一覧` は現行解説書24件（`NTF:05_UnitTestGuide/01_ClassUnitTest/02_componentUnitTest.rst:14`）、input資料5件 |
| `準備データ` | テスト実行前にデータベース・ファイルへ投入するデータ | `事前準備データ`（現行1件、`NTF:05_UnitTestGuide/01_ClassUnitTest/02_componentUnitTest.rst:96`。input2件、`S:input/ntf-doc-terms.md:48`・`:50`）／`セットアップデータ`（input1件、`S:input/ntf-testdata-doc.md:188`） | なし | `準備データ` は現行解説書48件（`NTF:05_UnitTestGuide/02_RequestUnitTest/batch.rst:168`）、input資料4件。`セットアップデータ` は第1部の記載内容の説明中でdesign1件（`S:design.md:32`）使われているが、用語を定める節ではないため出現数の多い側を採る |
| `期待値` | テスト実行後に期待する状態を表すデータ | `想定結果`（現行6件、`NTF:05_UnitTestGuide/01_ClassUnitTest/02_componentUnitTest.rst:255`）／`想定値`（現行2件、`NTF:05_UnitTestGuide/01_ClassUnitTest/02_componentUnitTest.rst:310`） | なし | `期待値` は現行解説書88件（`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:576`）、input資料33件 |
| `特殊記法` | セル値・エントリ値を実値に変換する記法（`null`、`${systemTime}` など） | `セルへの特殊な記述方法`（現行1件、`NTF:06_TestFWGuide/01_Abstract.rst:446`） | なし | input資料20件（`S:input/ntf-doc-terms.md:22`）。現行解説書の見出しはExcelのセルを前提としており、YAML形式に使えない |
| `マーカーカラム` | 読み込み対象外とするカラム。カラム名を半角角括弧で囲むもの | 揺れなし | なし | 現行解説書4件（`NTF:06_TestFWGuide/01_Abstract.rst:348`）、input資料17件 |
| `必須カラム` | データブロックに必ず記述しなければならないカラム | 揺れなし | なし | input資料7件（`S:input/ntf-testdata-doc-examples-testshots.md:18`）。input資料が「テストデータの記載例」の反復見出しに使っており、第3部でそのまま引き継ぐ |
| `オプションカラム` | 省略できるカラム | 揺れなし | なし | input資料5件（`S:input/ntf-testdata-doc-examples-testshots.md:18`）。必須カラムと対になる |
| `ディレクティブ` | ファイル・電文のフォーマット定義を指定する設定行 | 揺れなし | なし | FW解説書24件（`FW:libraries/data_io/data_format/format_definition.rst:79`）、現行解説書40件、input資料47件 |
| `テーブルデータ` | データベースのテーブルに対応するテストデータ | 揺れなし | なし | input資料13件（`S:input/ntf-testdata-doc-examples-table.md:1`）、現行解説書1件。`ファイルデータ` と対になる分類語 |
| `ファイルデータ` | 固定長ファイル・可変長ファイルに対応するテストデータ | 揺れなし | なし | input資料28件（`S:input/ntf-doc-terms.md:20`）。§5.10 の行の名称が係る対象を指すため定義する |
| `固定長ファイル` | レコード長・フィールド長が固定のファイル | 揺れなし | なし | FW解説書15件、現行解説書21件（`NTF:05_UnitTestGuide/02_RequestUnitTest/batch.rst:183`）、input資料24件 |
| `可変長ファイル` | 区切り文字でフィールドを区切るファイル | 揺れなし | なし | FW解説書2件（`FW:libraries/data_io/data_format/format_definition.rst:324`）、現行解説書12件、input資料14件 |

**データブロックとその属性。** `データブロック` を「`データタイプ[グループID]=値` によって識別されるもの」と定義し、`データタイプ` を「データブロックの種別」、`グループID` を「データブロックを識別する標識」と定義すると循環する。本書は `データブロック` を置き場所（読み込み単位の中）と役割（1用途分のデータのまとまり）だけで定義し、`データタイプ`（用途を表す予約語）と `グループID`（同種を区別する標識）をその属性として定義した。

### 5.9 テストデータファイルの単位

`シート`・`セル` はExcel形式に固有であり、YAML形式には存在しない。粒度をそろえた対応は次のとおり。**「セル」の対応物は「データブロック」ではない。** 出典は `読み込み単位` を階層図と表で示した input資料（`S:input/ntf-testdata-doc.md:32`、`:53`）である。

| 粒度 | Excel形式 | YAML形式 | 形式に依存しない語 |
|---|---|---|---|
| 1テストクラス分のテストデータ全体 | 1つのExcelファイル（`.xls`） | 同名の1ディレクトリ | テストデータ |
| 分割して読み込む単位 | 1シート | 1つのYAMLファイル | 読み込み単位 |
| 1用途分のデータのまとまり | `データタイプ=値` で始まる矩形範囲 | トップレベルキーの下の1エントリ | データブロック |
| 値1個 | 1セルの値 | 1つのキーに対応する値（エントリ値） | — |

形式を限定しない記述では右端の列の語を使う。形式ごとの記述では左2列の語を使う。

| 正表記 | 意味 | 揺れ表記（使わない） | 別義・旧名称（文脈により使う） | 採用根拠 |
|---|---|---|---|---|
| `Excelファイル` | Excel形式のテストデータファイル。1テストクラス分のテストデータ全体を保持するもの | `Excel ファイル`（現行1件、`NTF:06_TestFWGuide/01_Abstract.rst:229`。input1件）／`ブック`（input3件、`S:input/ntf-testdata-doc.md:36`） | なし | `Excelファイル` は現行解説書86件（`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:24`）。「ブック」はinput資料だけの表記で、現行解説書に0件 |
| `シート` | Excelファイル内の1シート。読み込み単位に相当するもの | `データシート`（現行7件、`NTF:05_UnitTestGuide/02_RequestUnitTest/index.rst:344`）／`テストデータシート`（現行6件、`NTF:05_UnitTestGuide/02_RequestUnitTest/fileupload.rst:66`）／`準備データシート`（現行1件、`NTF:06_TestFWGuide/01_Abstract.rst:102`） | なし | `シート` は現行解説書101件（`NTF:06_TestFWGuide/03_Tips.rst:37`）、input資料38件。生の `データシート` 14件の内訳は、単独7件・`テストデータシート` の一部6件・`準備データシート` の一部1件。単独7件のうち2件はRSTのコメント行（`..` 始まり）であり、生きた本文ではない（`データシート`、`NTF:06_TestFWGuide/01_Abstract.rst:70`、`:77`） |
| `セル` | Excelのシート内の1つの枠。値1個を保持するもの | 揺れなし | なし | 現行解説書42件（`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/02_entityUnitTestWithNablarchValidation.rst:60`）、input資料54件 |
| `YAMLファイル` | YAML形式のテストデータファイル。読み込み単位に相当するもの | `YAML ファイル`（input2件、`S:input/ntf-testdata-doc.md:68`） | なし | `YAMLファイル` 自体は未出現（半角空白入りのみ2件）。`Excelファイル` と同じ形に揃え、§6 の申し送りにある「英数字と日本語の間に空白を入れない」現行の実態（現行解説書は `Excelファイル` 86件対 `Excel ファイル` 1件）に合わせる |
| `トップレベルキー` | YAMLファイルの最上位に置く、データタイプに対応するキー | 揺れなし | なし | input資料5件（`S:input/ntf-testdata-doc-examples-overview.md:83`）。YAML形式のデータブロック識別の説明に必要 |
| `エントリ` | トップレベルキーの下のリストの1要素。1つのデータブロックに対応するもの | 揺れなし | なし | input資料44件（`S:input/ntf-testdata-doc-examples-file.md:195`）。`セル` の対応物ではなく `データブロック` の対応物である点に注意 |
| `エントリ値` | エントリ内の1つのキーに対応する値。Excel形式の1セルの値に相当するもの | 揺れなし（未出現） | なし | 全コーパスに0件。`特殊記法` の定義が「セル値・エントリ値を実値に変換する記法」であるように、Excel形式の「セルの値」に対応するYAML側の語がないと形式非依存の記述ができないため、採用優先順位3で新たに定義する |

### 5.10 ファイルデータの行の名称

ファイルデータのレイアウトを表す行の名称である。現行解説書に該当語はなく、input資料の表記をそのまま採用する。`レコード種別行` だけが `ntf-doc-terms.md` のみに現れ、他の3語は複数のinput資料に現れる。

| 正表記 | 意味 | 揺れ表記（使わない） | 別義・旧名称（文脈により使う） | 採用根拠 |
|---|---|---|---|---|
| `レコード種別行` | レコード種別を示す行 | 揺れなし | なし | input資料3件、1ファイルのみ（`S:input/ntf-doc-terms.md:175`）。**根拠が弱い。** `:175` は図中のラベル `[レコード種別行]` であり、用語を定義した箇所ではない。マルチレイアウトのファイルデータを扱うページの執筆時に、実データの記述で置き換えられるか再確認する（§10 未解決事項3） |
| `フィールド名称行` | 各フィールドの名称を並べた行 | 揺れなし | なし | input資料15件、5ファイル（`S:input/ntf-doc-terms.md:176`） |
| `データ型行` | 各フィールドのデータ型を示す行 | 揺れなし | なし | input資料9件、4ファイル（`S:input/ntf-doc-terms.md:177`） |
| `フィールド長行` | 各フィールドのバイト長を示す行。固定長ファイルのみで使うもの | 揺れなし | なし | input資料11件、4ファイル（`S:input/ntf-doc-terms.md:178`） |

### 5.11 電文

| 正表記 | 意味 | 揺れ表記（使わない） | 別義・旧名称（文脈により使う） | 採用根拠 |
|---|---|---|---|---|
| `電文` | メッセージングで送受信するメッセージ | 揺れなし | なし | FW解説書122件、現行解説書46件（`NTF:05_UnitTestGuide/02_RequestUnitTest/delayed_receive.rst:15`）、input資料35件 |
| `要求電文` | 送信側から受信側へ送るメッセージ | `リクエストメッセージ`（現行8件、`NTF:05_UnitTestGuide/02_RequestUnitTest/http_real.rst:46`） | なし | FW解説書49件（`FW:handlers/http_messaging/http_messaging_request_parsing_handler.rst:11`）、現行解説書78件 |
| `応答電文` | 受信側から送信側へ返すメッセージ | `レスポンスメッセージ`（現行10件、`NTF:05_UnitTestGuide/02_RequestUnitTest/delayed_receive.rst:51`） | なし | FW解説書58件、現行解説書67件（`NTF:05_UnitTestGuide/02_RequestUnitTest/batch.rst:109`） |
| `フレームワーク制御ヘッダ` | 電文の先頭に付与する、Nablarchが解釈する制御情報 | `FW制御ヘッダ`（現行3件、`NTF:05_UnitTestGuide/03_DealUnitTest/send_sync.rst:73`。input4件）／`FW 制御ヘッダ`（input8件、`S:input/ntf-testdata-doc.md:441`） | なし | FW解説書65件（`FW:handlers/http_messaging/http_messaging_request_parsing_handler.rst:83`）、現行解説書13件 |
| `メッセージボディ` | フレームワーク制御ヘッダより後ろの、業務データの部分 | 揺れなし | なし | FW解説書38件（`FW:libraries/log/messaging_log.rst:134`）、現行解説書8件（`NTF:05_UnitTestGuide/02_RequestUnitTest/http_real.rst:39`）、input資料2件 |
| `フォーマット定義ファイル` | 電文・ファイルのレイアウトを定義するファイル | 揺れなし | なし | FW解説書55件、現行解説書9件（`NTF:05_UnitTestGuide/02_RequestUnitTest/batch.rst:231`）、input資料2件 |

### 5.12 設定・ツール

| 正表記 | 意味 | 揺れ表記（使わない） | 別義・旧名称（文脈により使う） | 採用根拠 |
|---|---|---|---|---|
| `コンポーネント設定ファイル` | システムリポジトリに登録するコンポーネントを定義するXMLファイル | 揺れなし（`DI設定ファイル` は未出現） | なし | FW解説書105件、現行解説書47件（`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:712`）、input資料5件 |
| `システムリポジトリ` | コンポーネントを保持し、名前で取得できるようにする仕組み | 揺れなし | なし | FW解説書58件、現行解説書10件（`NTF:06_TestFWGuide/02_RequestUnitTest.rst:232`） |
| `内蔵サーバ` | リクエスト単体テスト（ウェブアプリケーション・RESTfulウェブサービス）で使用するサーブレットコンテナ | `内蔵サーブレットコンテナ`（input1件、`S:input/ntf-doc-terms.md:450`） | なし | 現行解説書18件（`NTF:05_UnitTestGuide/03_DealUnitTest/rest.rst:92`）。FW解説書に該当語なし。`NTF:06_TestFWGuide/02_RequestUnitTest.rst:11` は「リクエスト単体テスト(ウェブアプリケーション)では」と限定しており、バッチ・メッセージングでは使わないため、意味欄で対象を限定した |
| `HTMLダンプ` | リクエスト単体テスト（ウェブアプリケーション）で出力する、レスポンスHTMLのファイル | `HTML ダンプ`（input3件、`S:input/ntf-doc-terms.md:252`） | なし | 現行解説書19件（`NTF:05_UnitTestGuide/02_RequestUnitTest/index.rst:115`）。内蔵サーバと同じくウェブアプリケーション向けの機能であるため、意味欄で対象を限定した |
| `リクエスト単体データ作成ツール` | ブラウザ操作からリクエスト単体テストのテストデータを作成するツール | 揺れなし（`HTTPダンプツール` は未出現） | なし | 現行解説書3件（`NTF:08_TestTools/01_HttpDumpTool/01_HttpDumpTool.rst:4`）、`S:design.md:113` |
| `マスタデータ投入ツール` | マスタデータをデータベースへ投入するツール | 揺れなし | なし | 現行解説書3件（`NTF:08_TestTools/02_MasterDataSetup/01_MasterDataSetupTool.rst:4`）、`S:design.md:69` |
| `マスタデータ復旧機能` | テストで変更されたマスタデータを元に戻す機能 | 揺れなし | なし | 現行解説書2件（`NTF:06_TestFWGuide/04_MasterDataRestore.rst:4`）、input資料1件、`S:design.md:68` |
| `HTMLチェックツール` | 出力HTMLの使用禁止タグ・属性を検査するツール | 揺れなし | なし | 現行解説書3件（`NTF:06_TestFWGuide/02_RequestUnitTest.rst:351`）、FW解説書2件。**`design.md` に受け皿のページがない**（§11 申し送り事項1） |
| `テストデータ変換ツール` | Excel形式とYAML形式のテストデータを相互変換するツール | 揺れなし | なし | input資料1件（`S:input/testdata-converter-design.md:1`）、`S:design.md:66` |
| `JUnit 5用拡張機能` | JUnit 5でテスティングフレームワークを使うための拡張機能 | 揺れなし | なし | 現行解説書1件（`NTF:06_TestFWGuide/JUnit5_Extension.rst:4`）、`S:design.md:67` |
| `JUnit 5` | JUnitのバージョン5 | 揺れなし | `JUnit5`（現行1件、`NTF:06_TestFWGuide/index.rst:20`）はtoctreeのファイル名 JUnit5_Extension の一部であり、表記揺れではない | `JUnit 5` は現行解説書23件（`NTF:06_TestFWGuide/01_Abstract.rst:18`）、`S:design.md:34`。散文としての `JUnit5` は現行解説書に0件で、識別子は掲載対象外（§3）のため揺れ表記から外した |
| `JUnit 4` | JUnitのバージョン4 | `JUnit4`（現行8件、`NTF:05_UnitTestGuide/02_RequestUnitTest/rest.rst:16`） | なし | 現行解説書16件（`NTF:06_TestFWGuide/01_Abstract.rst:673`）、`S:design.md:34`。`JUnit4` 8件はいずれも散文であり、`JUnit5` と扱いが異なる |

### 5.13 セクションタイトル

`design.md` の「3. 第2部 導入と設定」「4. 第3部 テストの実装方法」が定めるページのアウトラインで、**枠の名称**として使う語である。

| 正表記 | 意味 | 揺れ表記（使わない） | 別義・旧名称（文脈により使う） | 採用根拠 |
|---|---|---|---|---|
| `機能概要` | ページの最上位セクション。何ができるかを示す枠 | `概要`（現行15件、`NTF:05_UnitTestGuide/02_RequestUnitTest/delayed_receive.rst:6`） | なし | FW解説書のライブラリで見出しとして26件（`FW:libraries/authorization/permission_check.rst:27`）。`概要` はFW解説書に42件あるが、独立見出しとしての「概要」は7件でライブラリ配下には0件。`S:design.md:78` |
| `使用方法` | ページの最上位セクション。使い方の手順を示す枠 | `実施方法`（現行44件、`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:642`） | なし | `使用方法` はFW63件だが、**独立見出しとしては36件**（うち35件が libraries 配下）。残り27件は本文中の平文（「使用方法は下記の通り。」`FW:libraries/data_io/data_format.rst:483`。「Nablarchの機能の使用方法を示した実装例」`FW:web/getting_started/index.rst:12`）とライブラリ外の見出し（`使用方法`、`FW:handlers/web/SessionStoreHandler.rst:187`）。design4件（`S:design.md:82`） |
| `拡張例` | ページの最上位セクション。差し替え・独自実装の手順を示す枠 | 揺れなし（現行解説書に未出現） | なし | FW解説書20件（`FW:handlers/rest/jaxrs_response_handler.rst:101`）。`S:design.md:86` |
| `モジュール一覧` | 依存モジュールを列挙する枠 | 揺れなし | なし | FW解説書85件、現行解説書3件（`NTF:06_TestFWGuide/JUnit5_Extension.rst:35`）。`S:design.md:34` |
| `全体像` | 機能概要の下位セクション。図で構造を示す枠 | 揺れなし | なし | 現行解説書7件（`NTF:06_TestFWGuide/02_DbAccessTest.rst:16`）、input資料7件、FW解説書3件（`FW:nablarch/big_picture.rst:3`）。`S:design.md:29` |
| `主なクラスとリソース` | 機能概要の下位セクション。クラス・リソースの名称・役割・作成単位を表で示す枠 | `主なクラス, リソース`（現行6件、`NTF:06_TestFWGuide/02_DbAccessTest.rst:23`。`主なクラス、リソース` は未出現） | なし | `S:design.md:80`。半角カンマ＋空白は日本語の読点として不適切であり、`discover --rule punct` が両表記を同一グループとして検出した |
| `前提事項` | 機能概要の下位セクション。適用できないケースを示す枠 | `前提条件`（現行6件、`NTF:05_UnitTestGuide/02_RequestUnitTest/rest.rst:5`） | なし | **FW解説書と異なる表記を採用する。** FW解説書は本文で `前提条件` をFW8件使うが、`前提事項`・`前提条件` のいずれもセクションタイトルとしては0件で、先例がない。`前提事項` はdesign1件（`S:design.md:81`）の決定と現行4件（`NTF:06_TestFWGuide/02_RequestUnitTest.rst:63`）に従う |
| `稼動環境` | 第1部の下位セクション。動作要件を示す枠 | 揺れなし（`稼働環境` は未出現） | なし | `稼動環境` はFW解説書のページ題（FW3件、`FW:nablarch/platform.rst:3`）、design2件（`S:design.md:34`）。FW解説書には「稼働」も生で5件あるが、いずれも動詞（「並行稼働させる」）や別の複合語（「稼働サーバ」）であり、複合語 `稼動環境` とは競合しない |
| `記述例` | 設定・テストデータの実例を示す枠 | 揺れなし | なし | FW解説書28件、現行解説書32件（`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:645`）、input資料12件、`S:design.md:99` |
| `制約` | 使用上の制限を示す枠 | `制約・補足`（input5件、`S:input/ntf-testdata-doc-examples-messaging.md:5`） | なし | FW解説書は見出しとして `制約` 51件・`補足` 8件を**別々に**使う。input資料の反復見出し `制約・補足` は2つの枠に分ける。FW解説書81件、input資料26件 |
| `補足` | 本筋から外れる注意事項を示す枠 | 揺れなし | なし | FW解説書20件、現行解説書2件（`NTF:06_TestFWGuide/JUnit5_Extension.rst:145`）、input資料4件 |

**枠の名称と、その中に置く見出しは別である。** 上表の名詞形は**アウトラインの枠を指す名称**であり、これがセクションタイトルになる。`S:design.md:90`・`:145` が定める「〜する」形式は、`使用方法` の枠の**中に置く下位の見出し**（「テストクラスを作成する」「コンポーネントを設定する」など）に適用する。上表の名詞形がこの規則に反しているのではない。

### 5.14 一般表記

| 正表記 | 意味 | 揺れ表記（使わない） | 別義・旧名称（文脈により使う） | 採用根拠 |
|---|---|---|---|---|
| `スーパクラス` | 継承元のクラス | `スーパークラス`（現行22件、`NTF:05_UnitTestGuide/02_RequestUnitTest/rest.rst:15`。FW1件、`FW:handlers/web/http_rewrite_handler.rst:105`） | なし | **FW解説書と異なる表記を採用する。** FW解説書の用例は1件のみで、同じFW解説書内の他のカタカナ語は長音を省いている（`インタフェース` FW75件、`ユーザ` FW175件、`サーバ` FW122件）。1件の例外に合わせるより、長音を省く側に揃えるほうが文書全体の一貫性が高い。現行解説書は20件対22件で拮抗しており決め手にならない |
| `インタフェース` | 実装を持たない型 | `インターフェース`（現行3件、`NTF:05_UnitTestGuide/02_RequestUnitTest/real.rst:181`。input2件、FW5件） | なし | FW解説書75件（`FW:batch/jsr352/application_design.rst:33`）、現行解説書16件 |
| `オーバーライド` | スーパクラスのメソッドを再定義すること | `オーバライド`（現行1件、`NTF:06_TestFWGuide/RequestUnitTest_real.rst:124`。FW5件） | なし | FW解説書11件（`FW:batch/jsr352/getting_started/batchlet/index.rst:70`）、現行解説書11件。いずれのコーパスでも長音付きが多数 |
| `ユーザ` | システムの利用者 | 揺れなし（`ユーザー` は未出現） | なし | FW解説書175件、現行解説書47件 |
| `サーバ` | サービスを提供する計算機・プロセス | 揺れなし（`サーバー` は未出現） | なし | FW解説書122件、現行解説書13件 |
| `データ` | 処理の対象となる値の集まり | `データー`（現行1件、`NTF:06_TestFWGuide/01_Abstract.rst:112`。RSTのコメント行） | なし | FW解説書1282件、現行解説書483件 |
| `バイナリデータ` | 文字列として解釈しないデータ | `バイナリーデータ`（現行1件、`NTF:06_TestFWGuide/01_Abstract.rst:86`。RSTのコメント行） | なし | FW解説書7件（`FW:handlers/web/multipart_handler.rst:213`）、現行解説書4件、input資料5件 |
| `パーサ` | テストデータを構造化オブジェクトへ組み立てる処理 | `パーサー`（input1件、`S:input/ntf-testdata-doc-examples-table.md:120`） | なし | input資料8件のうち7件は `ntf-testdata-loading.md`（`S:design.md:230` が解説書対象外と宣言した資料）にある。解説書の対象になる資料に現れるのは `パーサー` 1件だけである。それでも掲載するのは、`パーサ` が「1機能内に閉じた固有名詞」（掲載基準の不掲載3項目め）ではなく**カタカナ語の長音の揺れ**であり、本節の他の項（`インタフェース`・`オーバーライド`・`バイナリデータ`）と同じ規則の対象だからである |

---

## 6. 記述様式は #4（`style.md`）の管轄

括弧の全角・半角、英数字と日本語の間の空白、送り仮名・漢字/かなの選択、セクションタイトルの「〜する」形式は、**用語ではなく記述様式**である。`ntf-doc-rebuild-instruction.md` の #4 が定める観点（文体／セクションタイトル形式／表の記法など）と重なるため、本用語集では規範的な決定をしない。#4 で `style.md` として定める。

以下は本タスクで実測したデータである。#4 への申し送りとして残す。

### 6.1 括弧の全角・半角

- FW解説書の `libraries/` 配下の見出しで丸括弧を使うものは、**半角26件に対し全角5件**。半角の例は「メールを送信する(メール送信バッチを実行する)」（`FW:libraries/mail.rst:463`）、「システム日時(OS日時)と業務日付の切り替えができる」（`FW:libraries/date.rst:13`）、「データベースアクセス(JDBCラッパー)」（`FW:libraries/database/database.rst:3`）。全角の例は「データサイズの大きいバイナリデータを登録（更新）する」（`FW:libraries/database/universal_dao.rst:399`）、「HTTPアクセスログ（RESTfulウェブサービス用）の出力」（`FW:libraries/log/jaxrs_access_log.rst:3`）。
- 現行解説書の見出しは逆に、半角12件に対し全角21件。開きが全角・閉じが半角の混在も1件ある（`NTF:05_UnitTestGuide/03_DealUnitTest/real.rst:2`）。
- `S:design.md:207` は「FW解説書のライブラリに揃える」と宣言している。ライブラリの実測が半角優勢である以上、「日本語の見出しでは全角括弧を使う」という規則を用語集で立てるのは `design.md` に反する。#4 で決めること。
- なお `discover --rule paren` の既定コーパスにFW解説書は含まれない。この実測はFW解説書の見出しを別途数えたものである。

### 6.2 英数字と日本語の間の空白

- `discover --rule spacing` が60グループを報告した。用語として裁定したものは §5 に反映済み（`グループ ID`・`リクエスト ID`・`HTML ダンプ`・`Excel ファイル`・`RESTful ウェブサービス`・`FW 制御ヘッダ`・`HTTP 同期応答メッセージ送信`・`YAML ファイル`）。
- 用語ではないものが多数残る。input資料は「1 シート」「2 行目」「Cookie 情報」「HTTP メソッド」のように数字・英字の後ろに空白を入れる傾向があり、現行解説書は入れない傾向がある。全件は `discover --rule spacing` の出力を引くこと。
- 製品名・仕様名の内部の空白は原典に従う（`JUnit 5`、`Jakarta Batch`）。これは §5.12 で用語として確定済み。

### 6.3 送り仮名・漢字/かな

現状どの節にも規定がなく、`glossary.md` が「唯一の基準」を名乗る以上は穴になっている。実測は次のとおり（生の出現数）。

| 揺れ | 現行解説書 | FW解説書 |
|---|---|---|
| 出来る／できる | 4 / 207 | 66 / 722 |
| 及び／および | 28 / 55 | 197 / 71 |
| 全て／すべて | 24 / 0 | 139 / 16 |
| 行なう／行う | 1 / 116 | 2 / 665 |
| 通り／とおり | 29 / 9 | 82 / 99 |

いずれもFW解説書自身が揺れているため、採用優先順位1では決まらない。#4 で決めること。

### 6.4 セクションタイトルの形式

`S:design.md:90`・`:145` が「〜する」形式を定めている。本用語集は §5.13 で**枠の名称**（`機能概要`・`使用方法` など）だけを確定し、その中の見出しの言い回しは #4 の管轄とする。

---

## 7. 数字・製品名の表記

- 製品名・仕様名の数字は原典の表記に従う（`JUnit 5`、`JUnit 4`、`Jakarta Batch`）。`Jakarta Batch` の旧名称 `JSR352` は、旧名称であることを説明する文脈でのみ使う（§5.2）
- バージョン番号・桁数などの数値は半角

---

## 8. 対応表（現行解説書・input資料の語 → 正表記）

ページ作成時の置き換え表である。**適用条件を満たす場合にだけ置き換える。** 無条件に置き換えると壊れる行があるため、全行に条件を明記した。

| 現行解説書・input資料の語 | 正表記 | 適用条件 |
|---|---|---|
| `自動テストフレームワーク` | `テスティングフレームワーク` | 無条件 |
| `テストフレームワーク` | `テスティングフレームワーク` | 単独で現れる場合に限る。`自動テストフレームワーク` の一部は上の行で処理済み |
| `本フレームワーク` | `テスティングフレームワーク` | 現行NTF解説書に由来する記述に限る。FW解説書を引用・参照する箇所の `本フレームワーク` はNablarchを指す（FW10件）ので置き換えない |
| `NTF` | `テスティングフレームワーク` | 解説書のページ本文に限る。本用語集・`design.md` などの作業文書は対象外（§1） |
| `ハンドラーキュー` | `ハンドラキュー` | 無条件（全コーパスに未出現） |
| `リクエスト ID` | `リクエストID` | 無条件 |
| `Webアプリケーション` | `ウェブアプリケーション` | 処理方式を指す場合に限る。FW解説書の記述をそのまま引用する箇所は残す |
| `WEBアプリケーション` | `ウェブアプリケーション` | 無条件（現行・inputに未出現） |
| `RESTful ウェブサービス` | `RESTfulウェブサービス` | 無条件 |
| `RESTful Webサービス` | `RESTfulウェブサービス` | 無条件（現行・inputに未出現） |
| `HTTP メッセージング` | `HTTPメッセージング` | 無条件（現行・inputに未出現） |
| `バッチ処理` | `Nablarchバッチアプリケーション` | 処理方式を指す場合に限る。「バッチ処理を行う」のような一般的な動作の記述は置き換えない |
| `バッチアプリケーション` | `Nablarchバッチアプリケーション` | Nablarch独自方式を指す場合に限る。Jakarta Batchを含む総称として使っている箇所は残す |
| `JSR352に準拠したバッチアプリケーション` | `Jakarta Batchに準拠したバッチアプリケーション` | 旧名称であることを説明する箇所を除く |
| `MOMメッセージング` | `MOMによるメッセージング` | 処理方式を指す場合に限る。FW解説書のライブラリ章題を指す箇所は残す |
| `メッセージング処理` | `MOMによるメッセージング` | MOMを指すことが文脈から確定できる場合に限る。`NTF:06_TestFWGuide/03_Tips.rst:19` の「メッセージング処理でテストデータに対し定型的な変換処理を追加したい」は `TestDataConverter` の話でMOM限定ではないので置き換えない |
| `応答不要メッセージ送信処理` | `応答不要メッセージ送信` | 無条件 |
| `応答不要メッセージ受信処理` | `応答不要メッセージ受信` | 無条件 |
| `同期応答メッセージ送信処理` | `同期応答メッセージ送信` | `HTTP同期応答メッセージ送信処理` の一部でない場合に限る |
| `同期応答メッセージ受信処理` | `同期応答メッセージ受信` | `HTTP同期応答メッセージ受信処理` の一部でない場合に限る |
| `メッセージ受信処理` | `同期応答メッセージ受信` | 単独で現れ、かつ同期応答受信を指すことが文脈から確定できる場合に限る |
| `HTTP同期応答メッセージ送信` | `HTTPメッセージ送信` | 無条件 |
| `HTTP同期応答メッセージ送信処理` | `HTTPメッセージ送信` | 無条件 |
| `HTTP 同期応答メッセージ送信` | `HTTPメッセージ送信` | 無条件 |
| `HTTP 同期応答メッセージ送信処理` | `HTTPメッセージ送信` | 無条件 |
| `HTTP同期応答メッセージ受信` | `HTTPメッセージ受信` | 無条件 |
| `HTTP同期応答メッセージ受信処理` | `HTTPメッセージ受信` | 無条件 |
| `HTTP 同期応答メッセージ受信` | `HTTPメッセージ受信` | 無条件（現行・inputに未出現） |
| `HTTP 同期応答メッセージ受信処理` | `HTTPメッセージ受信` | 無条件（現行・inputに未出現） |
| `単体テスト` | `クラス単体テスト` | **原則として置き換えない。** `リクエスト単体テスト` などの一部でなく、かつ3種の総称でもなく、クラス単体テストを指すことが文脈から確定できる場合に限る（§5.5 の注記） |
| `Form/Entity単体テスト` | `エンティティ単体テスト` | 無条件 |
| `Form/Entityの単体テスト` | `エンティティ単体テスト` | 無条件 |
| `Form単体テスト` | `エンティティ単体テスト` | 無条件 |
| `Entity単体テスト` | `エンティティ単体テスト` | 無条件 |
| `Action/Component単体テスト` | `コンポーネント単体テスト` | 無条件 |
| `Action/Componentのクラス単体テスト` | `コンポーネント単体テスト` | 無条件 |
| `Action単体テスト` | `コンポーネント単体テスト` | 無条件 |
| `Component単体テスト` | `コンポーネント単体テスト` | 無条件 |
| `DB アクセステスト` | `データベースを使用するクラスのテスト` | 無条件 |
| `DBアクセステスト` | `データベースを使用するクラスのテスト` | 無条件（全コーパスに未出現） |
| `精査` | `バリデーション` | `単項目精査`・`項目間精査` の一部でない場合に限る（下2行で処理する） |
| `単項目精査` | `単項目バリデーション` | 無条件 |
| `項目間精査` | `相関バリデーション` | 無条件 |
| `テストショット` | `テストケース` | `テストショット一覧`・`テストショット表` の一部でない場合に限る |
| `セクション` | `データブロック` | テストデータの単位を指す場合に限る。文書構造の意味（`design.md`・マッピングの `section_id`・§5.13「セクションタイトル」）は置き換えない |
| `データブロック種別` | `データタイプ` | 無条件 |
| `グループ ID` | `グループID` | 無条件 |
| `groupId` | `グループID` | テストデータのグループIDを指す場合に限る。Mavenの `<groupId>` 要素、参照ラベル `tips_groupId`、YAMLの `group_id` キーは識別子なので置き換えない |
| `テストショット一覧` | `テストケース一覧` | 無条件 |
| `テストケース表` | `テストケース一覧` | 無条件 |
| `テストショット表` | `テストケース一覧` | 無条件 |
| `事前準備データ` | `準備データ` | 無条件 |
| `セットアップデータ` | `準備データ` | 無条件 |
| `想定結果` | `期待値` | 無条件 |
| `想定値` | `期待値` | 無条件 |
| `セルへの特殊な記述方法` | `特殊記法` | 無条件 |
| `制約・補足` | `制約` | 見出しに限る。内容に応じて `制約` と `補足` の2つの枠に分ける |
| `データシート` | `シート` | 単独で現れる場合に限る。`テストデータシート`・`準備データシート` の一部は下2行で処理する |
| `テストデータシート` | `シート` | Excel形式の記述に限る。形式を限定しない記述では `テストデータファイル` を使う |
| `準備データシート` | `シート` | Excel形式の記述に限る |
| `Excel ファイル` | `Excelファイル` | 無条件 |
| `ブック` | `Excelファイル` | 無条件 |
| `YAML ファイル` | `YAMLファイル` | 無条件 |
| `リクエストメッセージ` | `要求電文` | 無条件 |
| `レスポンスメッセージ` | `応答電文` | 無条件 |
| `FW制御ヘッダ` | `フレームワーク制御ヘッダ` | 無条件 |
| `FW 制御ヘッダ` | `フレームワーク制御ヘッダ` | 無条件 |
| `DI設定ファイル` | `コンポーネント設定ファイル` | 無条件（現行・inputに未出現） |
| `内蔵サーブレットコンテナ` | `内蔵サーバ` | 無条件 |
| `HTML ダンプ` | `HTMLダンプ` | 無条件 |
| `HTTPダンプツール` | `リクエスト単体データ作成ツール` | 無条件（現行・inputに未出現） |
| `JUnit5` | `JUnit 5` | 散文に限る。現行解説書の1件はtoctreeのファイル名 `JUnit5_Extension` の一部なので置き換えない |
| `JUnit4` | `JUnit 4` | 散文に限る |
| `概要` | `機能概要` | セクションタイトルに限る。本文中の「〜の概要」のような一般語は置き換えない（無条件に置き換えると「機能概要」が「機能機能概要」になる） |
| `実施方法` | `使用方法` | ページ内のセクションタイトルに限る。ページ題（「単体テスト実施方法」「リクエスト単体テストの実施方法(バッチ)」）は処理方式名を含む別の名前に置き換えるため、この行では扱わない |
| `主なクラス, リソース` | `主なクラスとリソース` | 無条件 |
| `主なクラス、リソース` | `主なクラスとリソース` | 無条件（全コーパスに未出現） |
| `前提条件` | `前提事項` | セクションタイトルに限る。本文中の「前提条件」は置き換えない |
| `稼働環境` | `稼動環境` | 見出しに限る。動詞の「稼働する」「稼働サーバ」は置き換えない |
| `スーパークラス` | `スーパクラス` | 無条件 |
| `インターフェース` | `インタフェース` | 無条件 |
| `オーバライド` | `オーバーライド` | 無条件 |
| `ユーザー` | `ユーザ` | 無条件（全コーパスに未出現） |
| `サーバー` | `サーバ` | 無条件（全コーパスに未出現） |
| `データー` | `データ` | 無条件 |
| `バイナリーデータ` | `バイナリデータ` | 無条件 |
| `パーサー` | `パーサ` | 無条件 |

## 9. ntf-doc-terms.md の候補の突き合わせ結果

`input/ntf-doc-terms.md` の各節について、現行解説書・FW解説書と突き合わせた結果を示す。表中の `L` に続く数字は、すべて `S:input/ntf-doc-terms.md` の行番号である。

判定語の意味は次のとおり。

| 判定 | 意味 |
|---|---|
| 採用 | 表記・意味ともそのまま引き継ぐ |
| 表記変更 | 意味は引き継ぎ、表記だけ差し替える |
| 範囲限定 | 表記・意味は引き継ぐが、使ってよい文脈を限定する |
| 一部不採用 | 節の中に採用する語と採用しない語が混在する |
| 不採用 | その語を解説書で使わない |

| ntf-doc-terms.md の節 | 判定 | 理由 |
|---|---|---|
| データタイプ（L36） | 採用 | 現行解説書43件・input資料57件で一貫。データタイプ名は識別子であり表記の選択余地がない |
| シート・行・列・セル（L61） | 範囲限定 | `シート`・`セル` はExcel形式に固有。形式を限定しない記述では §5.9 の対応表の右端列（`テストデータ`・`読み込み単位`・`データブロック`）を使う。行の名称（1行目・2行目・3行目以降）はExcel形式の説明に限って使う |
| 特殊記法（L84） | 採用 | §5.8 に掲載。現行解説書の見出し「セルへの特殊な記述方法」を置き換える |
| マーカーカラム（L98） | 採用 | 現行解説書4件・input資料17件で一致 |
| コメント（L102） | 採用 | 表記揺れなし |
| 設計原則（L110）— テスト独立性・データ集約・データタイプまとめ記述 | 不採用 | 3語とも `ntf-doc-terms.md` の造語で、現行解説書・FW解説書に0件。現行解説書は「テストメソッドの実行順序に依存しないテストを作成する」（`NTF:06_TestFWGuide/01_Abstract.rst:585`）のように文で書いている。`design.md` のセクションタイトル「〜する」形式に合うため、文のまま引き継ぐ |
| グループ ID（L118） | 表記変更 | 空白を除いた `グループID` を正表記とする。現行解説書73件が空白なし |
| データタイプ別の行構造（L129） | 採用 | レコード種別行・フィールド名称行・データ型行・フィールド長行を §5.10 に掲載。現行解説書に該当語がないため、input資料の表記をそのまま採る |
| ディレクティブ（L213） | 採用 | FW解説書24件と一致 |
| testShots / requestParams（L234） | 採用 | `testShots` `requestParams` はデータブロックのIDであり識別子。日本語の総称は `テストケース一覧` を使う |
| メッセージング 基本用語（L327） | 一部不採用 | `電文`・`要求電文`・`応答電文`・`フレームワーク制御ヘッダ`・`メッセージボディ` はFW解説書と一致するため採用。「電文種別」はFW解説書・現行解説書に0件のため不採用とし、`要求電文`・`応答電文` で書き分ける |
| HTTP 同期応答メッセージ送信の用語読み替え（L398） | 一部不採用 | クラス名の対応表は識別子としてそのまま採用する。節題の「HTTP 同期応答メッセージ送信」はFW解説書の `HTTPメッセージ送信` に置き換える（§5.4） |
| テスト種別の正式名称（L414） | 表記変更 | 「リクエスト単体テスト（バッチ処理）」「（メッセージ受信処理）」「（RESTful ウェブサービス）」は処理方式名が `design.md` の正式名称と異なる。§5.2・§5.4 の正表記に置き換える |
| DB アクセステスト（L427） | 表記変更 | 完全一致の `DBアクセステスト` は全コーパスに0件で、`DB アクセステスト` は `ntf-doc-terms.md` の造語。現行解説書のページ題「データベースを使用するクラスのテスト」（`NTF:06_TestFWGuide/02_DbAccessTest.rst:2`）に置き換える。テストの種類の分類軸ではなくクラス単体テストの一形態のため、§5.5 の下位に置く |
| 主要クラス各節（L443 以降） | 採用 | クラス名は識別子。日本語の役割説明は `主なクラスとリソース` の表に集約する |
| その他のフレームワーク固有用語（L526） | 一部不採用 | `内蔵サーバ` は採用（現行解説書18件）。併記の `内蔵サーブレットコンテナ`（L450）は使わない。`nablarch.test.resource-root` などの設定キーは識別子であり掲載対象外 |

## 10. 未解決事項

用語集の中で決着させるべきだが、まだ決まっていないもの。

| # | 事項 | 内容 |
|---|---|---|
| 1 | `シート` を残す範囲 | YAML形式にはシートがない。Excel形式の説明でのみ `シート` を使う方針としたが、どのセクションをExcel形式限定の記述にするかはマッピング（タスク #5）で確定する |
| 2 | `テーブルデータ`・`ファイルデータ` の位置づけ | テストデータを「テーブル／ファイル／メッセージ」で分類する軸と、「準備データ／期待値／テストケース一覧」で分類する軸が交差する。第3部の「テストデータの書き方」（`S:design.md:151`）を1ページに集約すると `design.md` が決めているため、どちらを章立ての軸にするかはマッピング後に決める |
| 3 | `レコード種別行` の根拠の弱さ | input資料1ファイル・3件しかなく、うち代表出典（`S:input/ntf-doc-terms.md:175`）は図中のラベルで定義箇所ではない。マルチレイアウトのファイルデータを扱うページの執筆時に、実データの記述で置き換えられるか再確認する |

## 11. 申し送り事項

用語集の外で解決するもの。用語集としての判断は済んでいる。

### 11.1 #6（`design.md` の更新）へ

1. **`design.md` に受け皿のないページがある。** タスク #5 は「`dest_page` は `design.md` に存在するページのみ」を規則とするため、割当先がないまま #5 に入ると詰まる。実測で次の5件が該当する。
   - `HTMLチェックツール`（§5.12 で正表記化したが、`design.md` に一度も登場しない）
   - `NTF:05_UnitTestGuide/02_RequestUnitTest/mail.rst:4`（メール送信のリクエスト単体テスト）
   - `NTF:05_UnitTestGuide/02_RequestUnitTest/fileupload.rst:2`（ファイルアップロードのリクエスト単体テスト）
   - `NTF:05_UnitTestGuide/02_RequestUnitTest/double_transmission.rst:2`（二重サブミット防止機能のリクエスト単体テスト）
   - `NTF:06_TestFWGuide/02_DbAccessTest.rst:2`（データベースを使用するクラスのテスト）
2. **第3部のMOMページ分割。** `design.md` §4 は「MOMによるメッセージング」を1ページとして**確定**で記述している（`S:design.md:122`）。一方、現行解説書は応答不要送信・応答不要受信・同期応答送信・同期応答受信の4方式を別ページに持つ。`design.md` の未確定事項1は第2部のページ分割、2は取引単体テストのページ構成であり、第3部のMOMページは含まれない。用語集としては4方式の正表記を確定した（§5.4）。1ページに収めるか分割するかは、`design.md` の確定事項を開き直す論点として #6 で扱う。
3. **`データブロック` と `データタイプ` の関係の図示。** 現行解説書は `データタイプ` 1語で種別とデータのまとまりの両方を指している。本用語集は §5.8 でまとまりを `データブロック`、種別を `データタイプ` に分け、循環しない定義を与えた。定義自体は決着済みだが、この分割は現行解説書にもFW解説書にも先例がないため、第1部「テストデータ」の執筆時に両者の関係を図で示す必要がある。

### 11.2 #4（`style.md`）へ

§6 の実測データ（括弧の全角・半角、英数字と日本語の間の空白、送り仮名・漢字/かな、セクションタイトルの言い回し）をそのまま申し送る。用語集では規範的な決定をしていない。
