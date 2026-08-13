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

本用語集の役割は「ページ作成時に表記を揃えるための参照物」である。掲載する用語の網羅性の証明は求めない。表記の一貫性は #8 以降のページ作成時、観点C（用語）のレビューで担保する（`steering.md` #3差し戻し）。

次のいずれかに当てはまる用語のみを掲載する。

1. 表記揺れが実在し、正表記を確定した用語（複数の表記が現行解説書・input資料に存在するもの）
2. `design.md` が章・セクション名として使う用語（処理方式の正式名称7件、テスト種別3件、ページアウトラインのセクション名）

上記のいずれにも該当しない候補は掲載しない。`mapping/term-candidates.csv` の母集団のうち上記2種類に該当しないものは、§5.15 で一括して「今回は判定しない」と記録する（候補ごとの個別理由は付けない）。

次のものも掲載していない。

- Javaのクラス名・メソッド名・カラム名・データタイプ名（`HttpRequestTestSupport`、`assertTableEquals`、`testShots`、`SETUP_TABLE` など）。これらは原文の識別子であり、表記の選択余地がない
- 1つの機能の説明の中に閉じており、他の機能のページから参照されない固有名詞（`Antビュー` はマスタデータ投入ツールの2ファイルのみ、`app-log.properties` はマスタデータ復旧機能とマスタデータ投入ツールのみ）

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
- `scan` は部分文字列の衝突を検出できない。`セル` は `エクセル` の部分文字列であるため、`エクセル`（またはその表記ゆれ）を含む行が `セル` の出現としても数えられる。この種の衝突は「データ」対「データベース」、「サーバ」対「サーバー」でも起こりうる。回避するには衝突元の語（`エクセル`・`データベース` など）を `term_candidates.tsv` に登録して最長一致で吸収させる必要があるが、本タスクでは `セル` の代表引用を実際に単独で使われている箇所に差し替えるにとどめ、件数の再検証は行っていない。

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
| `テスティングフレームワーク` | Nablarchアプリケーションのテストを補助する機能を提供するフレームワーク。本解説書が説明する対象 | `自動テストフレームワーク`（現行70件、`NTF:06_TestFWGuide/index.rst:4`）／`テストフレームワーク`（現行1件、`NTF:06_TestFWGuide/03_Tips.rst:825`）／`本フレームワーク`（現行14件、`NTF:05_UnitTestGuide/02_RequestUnitTest/batch.rst:617`）／`NTF`（input42件。現行2件、`NTF:05_UnitTestGuide/02_RequestUnitTest/http_real.rst:153`） | `本フレームワーク` はFW解説書ではNablarch自体を指す（FW10件、`FW:libraries/database/database.rst:442`） | FW解説書が `テスティングフレームワーク` を使う（FW8件、`FW:blank_project/CustomizeDB.rst:141`）。現行の最上位ページ題も同じ。「特化したテスト補助機能を提供すること」（`S:design.md:29`）を総称の意味で使うと書けないため機能提供と定義した |
| `ハンドラキュー` | リクエストの処理を担うハンドラを直列に並べた構造 | 揺れなし（`ハンドラーキュー` は未出現） | なし | `ハンドラキュー` はFW解説書の基本用語（FW84件、`FW:batch/nablarch_batch/architecture.rst:48`）。`S:design.md:30` が第1部で使うと決めている。現行は現行1件のみだが、リクエスト単体テストの説明に不可欠なため掲載基準1で掲載する |
| `リクエストID` | 業務処理を一意に識別する文字列 | `リクエスト ID`（input13件、`S:input/ntf-doc-terms.md:52`） | なし | FW解説書120件（`FW:batch/nablarch_batch/architecture.rst:52`）、現行解説書47件がいずれも空白なし。`グループ ID` と同型の半角空白の揺れで、`discover --rule spacing` が同一グループとして検出した |

### 5.2 処理方式

`design.md` の「5. 処理方式の名称」の7名称と一致する。名称はFW解説書の各章の題を採る。

FW解説書で「編」が付くのは**カテゴリ章とウェブサービスの下位章の計6見出し**である（`FW:batch/index.rst:3`、`FW:messaging/index.rst:3`、`FW:web/index.rst:3`、`FW:web_service/index.rst:3`、`FW:web_service/rest/index.rst:3`、`FW:web_service/http_messaging/index.rst:3`）。バッチ・メッセージングの下位章には付かない（`FW:batch/nablarch_batch/index.rst:3`、`FW:messaging/mom/index.rst:3`、`FW:messaging/db/index.rst:3`）。本解説書は処理方式をページ題に使うため、「編」は付けない。

| 正表記 | 意味 | 揺れ表記（使わない） | 別義・旧名称（文脈により使う） | 採用根拠 |
|---|---|---|---|---|
| `ウェブアプリケーション` | 画面を持つHTTPアプリケーション | 揺れなし（`WEBアプリケーション` は未出現） | `Webアプリケーション` はFW解説書自身が使う正用法（FW10件、`FW:batch/jsr352/architecture.rst:127`）。現行解説書・input資料には0件 | `FW:web/index.rst:3`。FW解説書では `ウェブアプリケーション` がFW83件に対し `Webアプリケーション` はFW10件で、前者が優勢 |
| `RESTfulウェブサービス` | REST APIを提供するウェブサービス | `RESTful ウェブサービス`（input2件、`S:input/ntf-doc-terms.md:420`） | なし | `FW:web_service/rest/index.rst:3`。FW解説書72件、現行解説書13件（`NTF:05_UnitTestGuide/02_RequestUnitTest/rest.rst:8`） |
| `HTTPメッセージング` | HTTPを使ったシステム間メッセージング | 揺れなし（`HTTP メッセージング` は未出現） | なし | `FW:web_service/http_messaging/index.rst:3`。FW解説書37件。現行解説書・input資料には0件だが、`S:design.md:120` が第3部の章に使うと決めている |
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
| `応答不要メッセージ送信` | 応答を待たずにメッセージを送信する方式 | `応答不要メッセージ送信処理`（現行8件、`NTF:05_UnitTestGuide/02_RequestUnitTest/delayed_send.rst:2`） | なし | 見出し「応答不要でメッセージを送信する(応答不要メッセージ送信)」（`FW:libraries/system_messaging/mom_system_messaging.rst:135`）。`応答不要メッセージ送信`FW7件。本文に`応答不要メッセージ送信処理`もFW1件あるが見出しは「処理」なし |
| `応答不要メッセージ受信` | 応答を返さずにメッセージを受信する方式 | `応答不要メッセージ受信処理`（現行5件、`NTF:05_UnitTestGuide/02_RequestUnitTest/delayed_receive.rst:2`） | なし | 見出し「応答不要でメッセージを受信する(応答不要メッセージ受信)」（`FW:libraries/system_messaging/mom_system_messaging.rst:470`。原文は半角括弧）。`応答不要メッセージ受信` はFW6件 |
| `同期応答メッセージ送信` | メッセージを送信し、応答を待つ方式 | `同期応答メッセージ送信処理`（現行32件・input4件、`NTF:05_UnitTestGuide/02_RequestUnitTest/send_sync.rst:4`）／`メッセージ同期送信処理`（語順違い・現行8件、`NTF:05_UnitTestGuide/02_RequestUnitTest/batch.rst:107`）／`メッセージ同期送信`（語順違い・現行2件・input2件、`NTF:05_UnitTestGuide/03_DealUnitTest/send_sync.rst:181`） | なし | 見出し「同期応答でメッセージを送信する(同期応答メッセージ送信)」（`FW:libraries/system_messaging/mom_system_messaging.rst:330`。原文は半角括弧）。`同期応答メッセージ送信` はFW9件 |
| `同期応答メッセージ受信` | メッセージを受信し、応答を返す方式 | `同期応答メッセージ受信処理`（現行7件、`NTF:05_UnitTestGuide/02_RequestUnitTest/real.rst:4`）／`メッセージ受信処理`（現行2件、`NTF:06_TestFWGuide/RequestUnitTest_real.rst:2`） | なし | 見出し「同期応答でメッセージを受信する(同期応答メッセージ受信)」（`FW:libraries/system_messaging/mom_system_messaging.rst:638`）。`同期応答メッセージ受信`FW5件。「メッセージ受信処理」は応答不要受信と区別できないため使わない |
| `HTTPメッセージ送信` | HTTPで外部システムにメッセージを送信し、その応答を受信する方式 | `HTTP同期応答メッセージ送信処理`（現行8件、`NTF:05_UnitTestGuide/02_RequestUnitTest/http_send_sync.rst:4`）／`HTTP同期応答メッセージ送信`（現行1件、`NTF:06_TestFWGuide/RequestUnitTest_http_send_sync.rst:12`）／`HTTP 同期応答メッセージ送信`（input計5件、`S:input/ntf-doc-terms.md:406`）・`HTTP 同期応答メッセージ送信処理`（`S:input/ntf-doc-terms.md:424`）／`HTTPメッセージ同期送信処理`（現行4件、`NTF:05_UnitTestGuide/02_RequestUnitTest/batch.rst:111`）／`HTTP メッセージ同期送信`（input2件、`S:input/ntf-doc-terms.md:268`） | なし | 見出し「メッセージを送信する(HTTPメッセージ送信)」（`FW:libraries/system_messaging/http_system_messaging.rst:132`）。直後の本文は現行と同動作。`HTTPメッセージ送信`FW5件。MOM側と同型のため優先順位1を適用 |
| `HTTPメッセージ受信` | HTTPで外部システムからメッセージを受信し、その応答を送信する方式 | `HTTP同期応答メッセージ受信`（現行1件、`NTF:05_UnitTestGuide/02_RequestUnitTest/http_real.rst:23`）／`HTTP同期応答メッセージ受信処理`（現行3件、`NTF:05_UnitTestGuide/02_RequestUnitTest/http_real.rst:2`） | なし | 見出し「メッセージを受信する(HTTPメッセージ受信)」（`FW:libraries/system_messaging/http_system_messaging.rst:94`。原文は半角括弧）。`HTTPメッセージ受信` はFW4件。同上 |
| `モックアップクラス` | 同期応答メッセージ送信・HTTPメッセージ送信で、外部システムの代わりに応答電文を返すクラス。リクエスト単体テスト・取引単体テストの双方で使い、実体は別のクラスである | 揺れなし | なし | 現行解説書21件、4ファイル（`NTF:05_UnitTestGuide/03_DealUnitTest/send_sync.rst:7`）。うち3件は見出し「モックアップクラスの設定」（`:286`ほか）。取引単体テストの実施に不可欠な骨格語のため掲載基準1で掲載する |

### 5.5 テストの種類

| 正表記 | 意味 | 揺れ表記（使わない） | 別義・旧名称（文脈により使う） | 採用根拠 |
|---|---|---|---|---|
| `クラス単体テスト` | クラス単体を対象とし、JUnitで自動実行するテスト | 揺れなし（下の注記を参照） | `単体テスト`（現行8件、`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:7`）は3種を束ねた総称であり、クラス単体テストの別表記ではない | `クラス単体テスト` は現行解説書26件（`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:4`）、`S:design.md:31` |
| `リクエスト単体テスト` | 1リクエストを対象とし、ハンドラキューを通してJUnitで自動実行するテスト | 揺れなし | なし | 現行解説書106件（`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:587`）。`リクエスト単体テスト`はFW6件も使う。`S:design.md:30` |
| `取引単体テスト` | 複数リクエストにまたがる業務の流れを手動操作で確認するテスト | 揺れなし | なし | 現行解説書40件（`NTF:05_UnitTestGuide/02_RequestUnitTest/double_transmission.rst:9`）、`S:design.md:31` |
| `エンティティ単体テスト` | クラス単体テストのうち、FormクラスとEntityクラスのバリデーションを対象とするもの | `Form単体テスト`（現行5件、`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:6`）／`Entity単体テスト`（現行5件、`:6`）／`Form/Entity単体テスト`（現行4件、`:14`）／`Form/Entityの単体テスト`（現行1件、`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/index.rst:4`） | なし | `S:design.md:115`。読者がクラス名の組み合わせではなくテスト対象の種類で引けるようにするため、`design.md` の決定に従う。Formクラスを書く読者が「エンティティ」から辿り着けるよう、意味欄に対象クラスを明示し、§8 に略称4種の行を置く |
| `コンポーネント単体テスト` | クラス単体テストのうち、ActionクラスとComponentクラスを対象とするもの | `Action/Componentのクラス単体テスト`（現行2件、`NTF:05_UnitTestGuide/01_ClassUnitTest/02_componentUnitTest.rst:4`）／`Component単体テスト`（現行2件、`:6`）／`Action単体テスト`（現行1件、`:7`）／`Action/Component単体テスト`（現行1件、`:10`） | ここでいう「コンポーネント」はJavaのActionクラス・Componentクラスを指す。システムリポジトリに登録するコンポーネント（§5.12 `コンポーネント設定ファイル`）とは別義 | `S:design.md:116`。同上 |
| `データベースを使用するクラスのテスト` | クラス単体テストのうち、データベースアクセスを伴うクラスを対象とするもの | `DB アクセステスト`（input1件、`S:input/ntf-doc-terms.md:427`。`DBアクセステスト` は未出現） | なし | 現行解説書のページ題（`データベースを使用するクラスのテスト`現行1件、`NTF:06_TestFWGuide/02_DbAccessTest.rst:2`）。`DB アクセステスト`は造語で、完全一致の`DBアクセステスト`は全コーパスに0件。分類軸ではなく一形態のため§5.5の下位に置く |

**`単体テスト` 単独について。** 現行解説書に `単体テスト` は生で201件あるが、そのほとんどは `リクエスト単体テスト`・`取引単体テスト`・`クラス単体テスト`・`Form単体テスト` などの後半部分である。`term_candidates.tsv` に `単体テスト` を含むより長い表記を13種登録したうえで数えると、単独の `単体テスト` は現行8件まで減る。この8件の性格は一様ではない。

明確に**総称**（クラス単体テストの別表記ではない）と言えるのは2件のみである。「両者はほぼ同じように単体テストを行える」（`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:7`、および同型の `NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/02_entityUnitTestWithNablarchValidation.rst:7`）は、直前で述べたFormクラスとEntityクラスの両方を指しており、クラス単体テストの意味に限定されない。

残り6件は個別の文脈依存の用法であり、一様に総称とは言えない。特に「データベースアクセスクラスの単体テストを行う場合」（`NTF:06_TestFWGuide/03_Tips.rst:558`）は文脈から明確に**クラス単体テスト**（`データベースを使用するクラスのテスト`）を指しており、§8の「クラス単体テストを指すことが文脈から確定できる場合に限る」というルールに該当する用例である。他の5件は、`リクエスト単体テスト` を指す省略表現（「他の単体テストの実施方法と同様に」`NTF:05_UnitTestGuide/02_RequestUnitTest/mail.rst:28`、「RESTfulウェブサービスの単体テストにおいては」`NTF:06_TestFWGuide/RequestUnitTest_rest.rst:139`）、一般名詞としての見出し（「単体テストライブラリ」`NTF:05_UnitTestGuide/03_DealUnitTest/send_sync.rst:364`）、クラス単体テスト・リクエスト単体テスト・取引単体テストの3ガイドを束ねるページ題（「単体テスト実施方法」`NTF:05_UnitTestGuide/index.rst:4`）、および表セル1件（「クエスト単体テストのテストソース」`NTF:06_TestFWGuide/02_RequestUnitTest.rst:50`。RSTの行折り返しで「リクエスト単体テスト」の「リ」が前の行に分かれ、この行だけを見ると `単体テスト` が単独に見える）である。

したがって `単体テスト` を「クラス単体テスト」の揺れ表記とはしない。§8 には条件付きの行を置く。

### 5.6 バリデーション

現行解説書は「精査」、FW解説書は「バリデーション」を使う。コーパス全体で最大の乖離であり、採用優先順位1が最も強く効くケースである。

| 正表記 | 意味 | 揺れ表記（使わない） | 別義・旧名称（文脈により使う） | 採用根拠 |
|---|---|---|---|---|
| `バリデーション` | 入力値が業務上の規則を満たすかを検証する処理 | `精査`（現行47件、`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:26`。FW4件） | なし | FW解説書316件（`FW:batch/jsr352/feature_details/run_batch_application.rst:44`）に対し `精査` はFW4件。現行解説書も `バリデーション` を6件使っている |
| `相関バリデーション` | 複数の項目の値の関係を検証するバリデーション | `項目間精査`（現行7件、`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:430`） | なし | FW解説書34件（`FW:batch/nablarch_batch/application_design.rst:28`）。`FW:libraries/validation/bean_validation.rst:400` に「相関バリデーションを行う」というセクションタイトルがある |
| `単項目バリデーション` | 1つの項目の値だけを見て行うバリデーション | `単項目精査`（現行38件、`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:66`） | なし | **FW解説書に確立表記がない。** 用例はコード中のコメント1件・散文2件のみ（`FW:web/getting_started/project_upload/index.rst:336`）。現行は `単項目精査` を見出しに使い名詞句が要る。`相関バリデーション`と対になる形を優先順位3で確定 |
| `ドメインバリデーション` | ドメイン定義に基づいて行うバリデーション | 揺れなし | なし | FW解説書28件（`FW:libraries/code.rst:433`）。エンティティ単体テストの説明で参照するため掲載する |

### 5.7 テストの骨格

`design.md` が第3部のセクションタイトルに使うと決めている語である（「テストクラスを作成する」`S:design.md:136`、「テストメソッドを作成する」`S:design.md:137`）。揺れはないが、全ページに横断するため掲載基準1で掲載する。

| 正表記 | 意味 | 揺れ表記（使わない） | 別義・旧名称（文脈により使う） | 採用根拠 |
|---|---|---|---|---|
| `テストクラス` | テストを記述するJavaクラス。1つのテストデータファイル群と対応するもの | 揺れなし | なし | 現行解説書138件（`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:16`）、input資料9件、`S:design.md:30` |
| `テストコード` | テストクラス・テストメソッドを実装するJavaのソースコード。テストデータファイルとは別に存在するもの | `テストソースコード`（現行解説書26件、`NTF:06_TestFWGuide/01_Abstract.rst:206`） | なし | input資料4件（`S:input/ntf-testdata-doc.md:24`）は全て`テストコード`で`テストソースコード`は0件。現行解説書は`テストコード`14件・`テストソースコード`26件で表記が割れており一貫しない（掲載基準・優先順位2「意味が明確で一貫しているものを採用する」により、割れている現行解説書ではなく一貫したinput資料側を採る）。`S:design.md:65`の`#8`確定文（「テストコードは定型・少量で済む」）も`テストコード`を使用し、`about/index.rst`（`#8`）で採用済み |
| `テストメソッド` | テストクラス内の1つのテストを表すメソッド | 揺れなし | なし | 現行解説書70件（`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:62`）、input資料6件、`S:design.md:137` |
| `テストショット` | 1回の実行（リクエスト送信・バッチ起動・バリデーション実行など）に対応する、1組の入力と期待値。テストショット一覧（§5.8）の1エントリがこれにあたる。プロジェクトのテスト仕様書上のテストケース1件が複数のテストショットになることがあり、両者は層が異なる | `テストケース`（現行155件、`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:26`。input資料38件）。**NTF解説書の本文に現れるテストケースはすべてこの揺れ表記であり、右欄の別義には当たらない。常に正表記側（§8 の対応表が定める置換先）に置き換える** | **解説書の外で使われる別義**。プロジェクトのテスト仕様書上のテストケース（業務上のテスト項目1件）を指す用法であり、NTF解説書の本文にはこの用法が現れないため、左隣の揺れ表記欄が定める置換の対象にならない。用語集・設計文書が業務上のテストケースと `テストショット` の層の違いを対比するときにだけこの語を使う | 現行解説書10件（`NTF:05_UnitTestGuide/02_RequestUnitTest/double_transmission.rst:20`）。予約ID `testShots` が現行のIDであり、旧称 `testCases` も動作する（`S:input/ntf-testdata-doc.md:167`。`testdata_notation.rst` の `testShots本体を記述する` で採用済み）。この位置づけのうち**未照合なのは次の2点に限る**。(a) `testCases` が下位互換のフォールバックであることの実装上の位置（`AbstractHttpRequestTestTemplate.java:222`）、(b) 公開クラス名が `TestShot`（`@Published`）であること。**この2点は作業指示 `S:ntf-doc-terminology.md:18`（2026-08-07 ユーザー提示）に由来する主張であり、`nablarch-testing` は本リポジトリ外のため本リポジトリでは未照合である。** `テストケース` のままでは、プロジェクトのテスト仕様書上のテストケースと同じ語になり現場で混同が起きるため、#5 の判断（`テストケース` を正表記、`テストショット` を揺れ表記）を覆した（2026-08-07 ユーザー判断）。なお `@Test` を付けたメソッドそのものを名指しする文脈では `テストメソッド` を、何を検証するかを述べる文脈では普通名詞の `テスト` を使う（後者は項を立てない）。**本項の定義と本文の定義セルの関係**: 本項の定義は用語そのものの意味を述べたものである。一方 `testdata_notation.rst` の `データブロックとデータタイプ` の表は、1つの読み込み単位に共存する3つの用途（テストショット・準備データ・期待値）を排他に分けることを目的とする別の表であり、そこでは兄弟行の `準備データ`（入力）・`期待値`（実行後の状態）と重ならないよう、同じ概念を `実行条件` の側から言い表している（`1回の実行に対応する、1エントリ分の実行条件`）。**両者は同じものを指す。** 残り32ページでも、用語そのものを説明する場面では本項の定義を、3つの用途を対比する表では `実行条件` 側の言い方を使う |

### 5.8 テストデータ

| 正表記 | 意味 | 揺れ表記（使わない） | 別義・旧名称（文脈により使う） | 採用根拠 |
|---|---|---|---|---|
| `テストデータ` | テストクラスとは別のファイルに記述する、準備データと期待値とテストショット一覧の総称 | 揺れなし | なし | `テストデータ` は現行223件（`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:16`）、input32件で一貫。準備データでも期待値でもなく3者含める |
| `テストデータファイル` | テストデータを記述したファイル。Excel形式とYAML形式がある | 揺れなし | なし | input資料4件（`S:input/ntf-testdata-doc-examples-messaging.md:133`）。YAML形式の追加により「Excelファイル」では総称にならないため採用する |
| `Excel形式` | Excelファイルにテストデータを記述する形式 | 揺れなし | なし | 現行解説書1件（`NTF:08_TestTools/01_HttpDumpTool/01_HttpDumpTool.rst:27`）。YAML形式との対比に必要な語であり、採用優先順位3で定義する |
| `YAML形式` | YAMLファイルにテストデータを記述する形式 | 揺れなし | なし | `S:design.md:52` の本文で `nablarch-testing-yaml` の説明に使う（design.md中ここ1箇所）。現行・inputに完全一致なし。`S:design.md:65` の章名に文字列自体は現れない。優先順位3で定義 |
| `読み込み単位` | 1つのテストクラスのテストデータを分割して読み込む単位。Excel形式では1シート、YAML形式では1ファイル | 揺れなし | なし | input資料6件（`S:input/ntf-testdata-doc.md:32`）。Excel形式とYAML形式で対応物が異なる階層に名前を与えるために必要 |
| `データブロック` | 読み込み単位の中に置く、1用途分のデータのまとまり。テストデータファイルの記述単位 | `セクション`（input30件、`S:input/ntf-doc-terms.md:347`） | `セクション` は文書のセクションの意でも使われる（design10件、`S:design.md:27`）。マッピングの section_id・heading_path 列もこの別義 | input資料34件（`S:input/ntf-testdata-doc-examples-messaging.md:5`）、`S:design.md:32`（第1部にデータブロックの考え方を置くと決めている）。他語に依存しないよう「どこに置く何のまとまりか」で定義した（下の注記も参照） |
| `データタイプ` | データブロックの用途を表す予約語。`SETUP_TABLE`、`EXPECTED_TABLE` など14種 | `データブロック種別`（input7件、`S:input/ntf-testdata-doc.md:96`） | ファイルデータの `データ型行`（§5.10）が示す「データ型」は、フィールドの型であって別概念 | 現行解説書43件（`NTF:05_UnitTestGuide/02_RequestUnitTest/batch.rst:74`）、input資料57件。Excel形式ではデータブロック先頭セルに書く文字列そのものであり、選択余地がない |
| `グループID` | 同じ読み込み単位に同じデータタイプのデータブロックを複数置くとき、それらを区別する標識 | `グループ ID`（input21件、`S:input/ntf-doc-terms.md:32`） | `groupId`（現行46件、FW333件）はMavenのgroupId要素等の識別子。FW`グループID`22件中19件Maven、3件は認可機能（`FW:libraries/authorization/permission_check.rst:92`）で別義 | 現行解説書73件（`NTF:05_UnitTestGuide/01_ClassUnitTest/02_componentUnitTest.rst:259`）が空白なし。書式は `データタイプ[グループID]=識別子の値` |
| `テストショット一覧` | 1テストクラスで実行するテストショットを列挙したデータブロック（`LIST_MAP=testShots`） | `テストケース一覧`（現行24件、`NTF:05_UnitTestGuide/01_ClassUnitTest/02_componentUnitTest.rst:14`。input資料5件）／`テストケース表`（現行9件、`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:110`）／`テストショット表`（現行2件、`NTF:05_UnitTestGuide/02_RequestUnitTest/http_real.rst:16`） | なし | `テストショット一覧` は現行解説書5件（`NTF:05_UnitTestGuide/02_RequestUnitTest/http_real.rst:13`）。§5.7 で `テストショット` を正表記としたことに合わせ、その一覧を表す語も `テストショット一覧` に揃える |
| `エンティティバリデーション` | テストショット一覧の入力カラム体系の一つ。`EntityTestSupport` が扱う、ウェブアプリケーション・Nablarchバッチアプリケーション・メッセージングとは別体系のカラム構成 | 揺れなし | `エンティティ単体テスト`（§5.5）はFormクラス・Entityクラスのバリデーションを対象とする**テストの種類**を指す語であり、`エンティティバリデーション` は**テストショット一覧のカラム体系**を指す別の軸の語である | input2ファイル・5件、見出し「エンティティバリデーション」（`S:input/ntf-testdata-doc-examples-testshots.md:251`）。テストショット一覧でウェブ等と並ぶカテゴリとして扱う。現行に該当語なし |
| `準備データ` | テスト実行前にデータベース・ファイルへ投入するデータ | `事前準備データ`（現行1件、`NTF:05_UnitTestGuide/01_ClassUnitTest/02_componentUnitTest.rst:96`。input2件）／`セットアップデータ`（input1件、`S:input/ntf-testdata-doc.md:188`） | なし | `準備データ` は現行解説書48件（`NTF:05_UnitTestGuide/02_RequestUnitTest/batch.rst:168`）、input4件。`セットアップデータ` はdesign1件使われるが用語を定める節ではないため出現数の多い側を採る |
| `期待値` | テスト実行後に期待する状態を表すデータ | `想定結果`（現行6件、`NTF:05_UnitTestGuide/01_ClassUnitTest/02_componentUnitTest.rst:255`）／`想定値`（現行2件、`NTF:05_UnitTestGuide/01_ClassUnitTest/02_componentUnitTest.rst:310`） | なし | `期待値` は現行解説書88件（`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:576`）、input資料33件 |
| `特殊記法` | セル値・エントリ値を実値に変換する記法（`null`、`${systemTime}` など） | `セルへの特殊な記述方法`（現行1件、`NTF:06_TestFWGuide/01_Abstract.rst:446`） | なし | input資料20件（`S:input/ntf-doc-terms.md:22`）。現行解説書の見出しはExcelのセルを前提としており、YAML形式に使えない |
| `マーカーカラム` | 読み込み対象外とするカラム。カラム名を半角角括弧で囲むもの | 揺れなし | なし | 現行解説書4件（`NTF:06_TestFWGuide/01_Abstract.rst:348`）、input資料17件 |
| `必須カラム` | データブロックに必ず記述しなければならないカラム | 揺れなし | なし | input資料7件（`S:input/ntf-testdata-doc-examples-testshots.md:18`）。input資料が「テストデータの記載例」の反復見出しに使っており、第3部でそのまま引き継ぐ |
| `オプションカラム` | 省略できるカラム | 揺れなし | なし | input資料5件（`S:input/ntf-testdata-doc-examples-testshots.md:18`）。必須カラムと対になる |
| `ディレクティブ` | ファイル・電文のフォーマットに関する属性を、キー名と値の2要素で指定するもの | 揺れなし | なし | FW解説書24件（`FW:libraries/data_io/data_format/format_definition.rst:79`）、現行解説書40件、input資料47件 |
| `テーブルデータ` | データベースのテーブルに対応するテストデータ | 揺れなし | なし | input資料13件（`S:input/ntf-testdata-doc-examples-table.md:1`）、現行解説書1件。`ファイルデータ` と対になる分類語 |
| `ファイルデータ` | 固定長ファイル・可変長ファイルに対応するテストデータ | 揺れなし | なし | input資料28件（`S:input/ntf-doc-terms.md:20`）。§5.10 の行の名称が係る対象を指すため定義する |
| `固定長ファイル` | レコード長・フィールド長が固定のファイル | 揺れなし | なし | FW解説書15件、現行解説書21件（`NTF:05_UnitTestGuide/02_RequestUnitTest/batch.rst:183`）、input資料24件 |
| `可変長ファイル` | 区切り文字でフィールドを区切るファイル | 揺れなし | なし | FW解説書2件（`FW:libraries/data_io/data_format/format_definition.rst:324`）、現行解説書12件、input資料14件 |
| `複数レコードレイアウト` | 1つの読み込み単位内にレコード種別が異なる複数のレコードを混在させるファイルデータの構造 | 揺れなし | なし | input2ファイル・5件、見出し「複数レコードレイアウト」（`S:input/ntf-testdata-doc-examples-file.md:284`）。現行に該当語なし。旧版の「マルチレイアウト」は出典のない造語のため、input資料に実在する表記に置換 |
| `型名称` | フィールドのデータ型をテストデータに記述するときの日本語名（`符号無数値` など）。外部インタフェース設計書の表記をそのまま使う | 揺れなし | なし | input1ファイル・6件（`S:input/ntf-testdata-doc.md:618`）。現行解説書0件・FW解説書0件（実測）。`型記号` と対であり、両者を取り違えると動かない名前（`TEST_{型名称}`）を書くことになる。`S:input/ntf-testdata-doc.md:633` が実際にその誤りを持ち、承認済みページへ波及していた。正表記と適用範囲を確定して掲載する（掲載基準1、`#20` で確定） |
| `型記号` | フレームワークがデータ型を識別する記号（`X9` など）。`型名称` から変換して得られる | 揺れなし | なし | input1ファイル・2件（`S:input/ntf-testdata-doc.md:349`・`:620`）。現行解説書0件・FW解説書0件（実測）。変換表は実装の `BasicDataTypeMapping` の `DEFAULT_TABLE`（`符号無数値`→`X9`）。テスト用データ型の名前は型記号に `TEST_` を前置する（`DataFileFragment.java:70`・`:238-240`）。同上（掲載基準1、`#20` で確定） |

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
| `Excelファイル` | Excel形式のテストデータファイル。1テストクラス分のテストデータ全体を保持するもの | `Excel ファイル`（現行1件、`NTF:06_TestFWGuide/01_Abstract.rst:229`。input1件）／`ブック`（input3件、`S:input/ntf-testdata-doc.md:36`） | なし | `Excelファイル` は現行解説書86件（`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:24`）。「ブック」はinput限定の表記で現行に0件 |
| `シート` | Excelファイル内の1シート。読み込み単位に相当するもの | `データシート`（現行7件、`NTF:05_UnitTestGuide/02_RequestUnitTest/index.rst:344`）／`テストデータシート`（現行6件、`NTF:05_UnitTestGuide/02_RequestUnitTest/fileupload.rst:66`）／`準備データシート`（現行1件、`NTF:06_TestFWGuide/01_Abstract.rst:102`。RSTのコメント行） | なし | `シート` は現行101件（`NTF:06_TestFWGuide/03_Tips.rst:37`）、input38件。生の`データシート`14件は単独7件・`テストデータシート`の一部6件・`準備データシート`の一部1件。単独7件中2件はRSTコメント行で生きた本文ではない |
| `セル` | Excelのシート内の1つの枠。値1個を保持するもの | 揺れなし | なし | 現行解説書42件（`NTF:05_UnitTestGuide/02_RequestUnitTest/batch.rst:224`「ディレクティブ名のセルの右のセルに設定値を記載する」）、input資料54件 |
| `YAMLファイル` | YAML形式のテストデータファイル。読み込み単位に相当するもの | `YAML ファイル`（input2件、`S:input/ntf-testdata-doc.md:68`） | なし | `YAMLファイル` 自体は未出現（半角空白入りのみ2件）。`Excelファイル` と同じ形に揃え、§6 の申し送りにある「英数字と日本語の間に空白を入れない」現行の実態（現行解説書は `Excelファイル` 86件対 `Excel ファイル` 1件）に合わせる |
| `トップレベルキー` | YAMLファイルの最上位に置く、データタイプに対応するキー | 揺れなし | なし | input資料5件（`S:input/ntf-testdata-doc-examples-overview.md:83`）。YAML形式のデータブロック識別の説明に必要 |
| `エントリ` | トップレベルキーの下のリストの1要素。1つのデータブロックに対応するもの | 揺れなし | なし | input資料44件（`S:input/ntf-testdata-doc-examples-file.md:195`）。`セル` の対応物ではなく `データブロック` の対応物である点に注意 |
| `エントリ値` | エントリ内の1つのキーに対応する値。Excel形式の1セルの値に相当するもの | 揺れなし（未出現） | なし | 全コーパスに0件。`特殊記法` の定義が「セル値・エントリ値を実値に変換する記法」であるように、Excel形式の「セルの値」に対応するYAML側の語がないと形式非依存の記述ができないため、採用優先順位3で新たに定義する |

### 5.10 ファイルデータの行の名称

ファイルデータのレイアウトを表す行の名称である。現行解説書に該当語はなく、input資料の表記をそのまま採用する。`レコード種別行` だけが `ntf-doc-terms.md` のみに現れ、他の3語は複数のinput資料に現れる。

| 正表記 | 意味 | 揺れ表記（使わない） | 別義・旧名称（文脈により使う） | 採用根拠 |
|---|---|---|---|---|
| `レコード種別行` | レコード種別を示す行 | 揺れなし | なし | input資料3件、1ファイルのみ（`S:input/ntf-doc-terms.md:175`）。**根拠が弱い。** `:175` は図中のラベルで定義箇所ではない。`複数レコードレイアウト` のページ執筆時に実データの記述で置き換えられるか再確認（§10未解決事項3） |
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
| `内蔵サーバ` | リクエスト単体テスト（ウェブアプリケーション・RESTfulウェブサービス）で使用するサーブレットコンテナ | `内蔵サーブレットコンテナ`（input1件、`S:input/ntf-doc-terms.md:450`） | なし | 現行解説書18件（`NTF:05_UnitTestGuide/03_DealUnitTest/rest.rst:92`）。FWに該当語なし。`NTF:06_TestFWGuide/02_RequestUnitTest.rst:11`がウェブアプリ限定と明記するため意味欄で対象を限定 |
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
| `使用方法` | ページの最上位セクション。使い方の手順を示す枠 | `実施方法`（現行44件、`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:642`） | なし | `使用方法` はFW63件だが独立見出しは36件（うち35件がlibraries配下）。残り27件は本文中の平文とライブラリ外の見出し1件（`FW:handlers/web/SessionStoreHandler.rst:187`）。design4件 |
| `拡張例` | ページの最上位セクション。差し替え・独自実装の手順を示す枠 | 揺れなし（現行解説書に未出現） | なし | FW解説書20件（`FW:handlers/rest/jaxrs_response_handler.rst:101`）。`S:design.md:86` |
| `モジュール一覧` | 依存モジュールを列挙する枠 | 揺れなし | なし | FW解説書85件、現行解説書3件（`NTF:06_TestFWGuide/JUnit5_Extension.rst:35`）。`S:design.md:34` |
| `全体像` | 機能概要の下位セクション。図で構造を示す枠 | 揺れなし | なし | 現行解説書7件（`NTF:06_TestFWGuide/02_DbAccessTest.rst:16`）、input資料7件、FW解説書3件（`FW:nablarch/big_picture.rst:3`）。`S:design.md:29` |
| `主なクラスとリソース` | 機能概要の下位セクション。クラス・リソースの名称・役割・作成単位を表で示す枠 | `主なクラス, リソース`（現行6件、`NTF:06_TestFWGuide/02_DbAccessTest.rst:23`。`主なクラス、リソース` は未出現） | なし | `S:design.md:80`。半角カンマ＋空白は日本語の読点として不適切であり、`discover --rule punct` が両表記を同一グループとして検出した |
| `前提事項` | 機能概要の下位セクション。適用できないケースを示す枠 | `前提条件`（現行6件、`NTF:05_UnitTestGuide/02_RequestUnitTest/rest.rst:5`） | なし | **FW解説書と異なる表記を採用する。** FWは本文で `前提条件` をFW8件使うが、セクションタイトルとしては両表記とも0件で先例がない。`前提事項` はdesign1件（`S:design.md:81`）と現行4件に従う |
| `稼動環境` | 第1部の下位セクション。動作要件を示す枠 | 揺れなし（`稼働環境` は未出現） | なし | `稼動環境` はFW解説書のページ題（FW3件、`FW:nablarch/platform.rst:3`）、design2件。FWには「稼働」も生5件あるが動詞や別複合語（「稼働サーバ」）で、`稼動環境` とは競合しない |
| `記述例` | 設定・テストデータの実例を示す枠 | 揺れなし | なし | FW解説書28件、現行解説書32件（`NTF:05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst:645`）、input資料12件、`S:design.md:99` |
| `制約` | 使用上の制限を示す枠 | `制約・補足`（input5件、`S:input/ntf-testdata-doc-examples-messaging.md:5`） | なし | FW解説書は見出しとして `制約` 51件・`補足` 8件を**別々に**使う。input資料の反復見出し `制約・補足` は2つの枠に分ける。FW解説書81件、input資料26件 |
| `補足` | 本筋から外れる注意事項を示す枠 | 揺れなし | なし | FW解説書20件、現行解説書2件（`NTF:06_TestFWGuide/JUnit5_Extension.rst:145`）、input資料4件 |

**枠の名称と、その中に置く見出しは別である。** 上表の名詞形は**アウトラインの枠を指す名称**であり、これがセクションタイトルになる。`S:design.md:90`・`:145` が定める「〜する」形式は、`使用方法` の枠の**中に置く下位の見出し**（「テストクラスを作成する」「コンポーネントを設定する」など）に適用する。上表の名詞形がこの規則に反しているのではない。

### 5.14 一般表記

| 正表記 | 意味 | 揺れ表記（使わない） | 別義・旧名称（文脈により使う） | 採用根拠 |
|---|---|---|---|---|
| `スーパクラス` | 継承元のクラス | `スーパークラス`（現行22件、`NTF:05_UnitTestGuide/02_RequestUnitTest/rest.rst:15`。FW1件、`FW:handlers/web/http_rewrite_handler.rst:105`） | なし | **FW解説書と異なる表記を採用する。** FW用例は1件のみで、他のカタカナ語は長音を省く（`インタフェース`FW75件等）。例外に合わせるより省く側に揃える方が一貫性が高い。現行は20対22で拮抗し決め手にならない |
| `インタフェース` | 実装を持たない型 | `インターフェース`（現行3件、`NTF:05_UnitTestGuide/02_RequestUnitTest/real.rst:181`。input2件、FW5件） | なし | FW解説書75件（`FW:batch/jsr352/application_design.rst:33`）、現行解説書16件 |
| `オーバーライド` | スーパクラスのメソッドを再定義すること | `オーバライド`（現行1件、`NTF:06_TestFWGuide/RequestUnitTest_real.rst:124`。FW5件） | なし | FW解説書11件（`FW:batch/jsr352/getting_started/batchlet/index.rst:70`）、現行解説書11件。いずれのコーパスでも長音付きが多数 |
| `ユーザ` | システムの利用者 | 揺れなし（`ユーザー` は未出現） | なし | FW解説書175件、現行解説書47件 |
| `サーバ` | サービスを提供する計算機・プロセス | 揺れなし（`サーバー` は未出現） | なし | FW解説書122件、現行解説書13件 |
| `データ` | 処理の対象となる値の集まり | `データー`（現行1件、`NTF:06_TestFWGuide/01_Abstract.rst:112`。RSTのコメント行） | なし | FW解説書1282件、現行解説書483件 |
| `バイナリデータ` | 文字列として解釈しないデータ | `バイナリーデータ`（現行1件、`NTF:06_TestFWGuide/01_Abstract.rst:86`。RSTのコメント行） | なし | FW解説書7件（`FW:handlers/web/multipart_handler.rst:213`）、現行解説書4件、input資料5件 |
| `パーサ` | テストデータを構造化オブジェクトへ組み立てる処理 | `パーサー`（input1件、`S:input/ntf-testdata-doc-examples-table.md:120`） | なし | input資料8件中7件は `ntf-testdata-loading.md`（`S:design.md:230` が対象外と宣言）にあり、対象資料の用例は `パーサー` 1件のみ。それでも掲載するのは**カタカナ語の長音の揺れ**であり、本節の他項と同じ規則の対象だからである |

### 5.15 `term-candidates.csv` との対応（母集団の全件判定）

`mapping/tools/extract_terms.py` が現行解説書の見出し・`input/ntf-doc-terms.md` の見出し・`design.md` の見出しと処理方式名から機械的に抽出した母集団 `mapping/term-candidates.csv`（339行・331種類の表記）の全候補を、次の3値のいずれかに判定する。

- **採用**（36件、§5.15.1） — §3 の掲載基準に該当し、§5（用語）のいずれかのコードスパンと文字列一致する候補
- **不採用（理由付き）** — 個別に不採用の理由を記す候補（今回は該当なし。将来、個別の理由を要する候補が生じた場合はこの区分を使う）
- **一括：今回は判定しない**（295件、§5.15.2） — §3 の掲載基準の2種類のいずれにも該当しない候補。候補ごとの個別理由は付けず一括して記録する

`verify_glossary.py` の `population` 検査が、`term-candidates.csv` の全行がこの3値のいずれかに過不足なく対応すること（未判定0件）を機械検査する。

採用の行は、§5の当該用語が `term-candidates.csv` のどの候補に由来するかの相互参照を兼ねる（§2で求める「既存の用語→候補」と本節の「候補→既存の用語」は同じ対応関係の両方向であり、表は1つにまとめている）。

#### 5.15.1 採用（36件）

`term-candidates.csv` の表記が、そのまま §5（用語）のいずれかのコードスパンと文字列一致する候補である。

| 候補 | 出典 | §5での扱い |
|---|---|---|
| `Action/Componentのクラス単体テスト` | current-heading | §5.5 テストの種類 の揺れ表記 |
| `DB アクセステスト` | ntf-doc-terms-heading | §5.5 テストの種類 の揺れ表記 |
| `Form/Entityの単体テスト` | current-heading | §5.5 テストの種類 の揺れ表記 |
| `HTMLチェックツール` | current-heading | §5.12 設定・ツール の正表記 |
| `HTTPメッセージング` | design-scheme | §5.2 処理方式 の正表記 |
| `JUnit 5用拡張機能` | current-heading | §5.12 設定・ツール の正表記 |
| `Jakarta Batchに準拠したバッチアプリケーション` | design-scheme | §5.2 処理方式 の正表記 |
| `MOMによるメッセージング` | design-scheme | §5.2 処理方式 の正表記 |
| `Nablarchバッチアプリケーション` | design-scheme | §5.2 処理方式 の正表記 |
| `RESTfulウェブサービス` | design-scheme | §5.2 処理方式 の正表記 |
| `ウェブアプリケーション` | design-scheme | §5.2 処理方式 の正表記 |
| `グループ ID` | ntf-doc-terms-heading | §5.8 テストデータ の揺れ表記 |
| `セルへの特殊な記述方法` | current-heading | §5.8 テストデータ の揺れ表記 |
| `テスティングフレームワーク` | current-heading | §5.1 全体・Nablarchの基本概念 の正表記 |
| `テストケース一覧` | current-heading | §5.8 テストデータ の揺れ表記 |
| `テストショット一覧` | current-heading | §5.8 テストデータ の正表記 |
| `テストデータ` | current-heading | §5.8 テストデータ の正表記 |
| `テーブルをキューとして使ったメッセージング` | design-heading・design-scheme | §5.2 処理方式 の正表記 |
| `ディレクティブ` | ntf-doc-terms-heading | §5.8 テストデータ の正表記 |
| `データベースを使用するクラスのテスト` | current-heading | §5.5 テストの種類 の正表記 |
| `マスタデータ復旧機能` | current-heading・ntf-doc-terms-heading | §5.12 設定・ツール の正表記 |
| `マスタデータ投入ツール` | current-heading | §5.12 設定・ツール の正表記 |
| `マーカーカラム` | current-heading・ntf-doc-terms-heading | §5.8 テストデータ の正表記 |
| `モジュール一覧` | current-heading | §5.13 セクションタイトル の正表記 |
| `リクエスト単体データ作成ツール` | current-heading | §5.12 設定・ツール の正表記 |
| `主なクラス, リソース` | current-heading | §5.13 セクションタイトル の揺れ表記 |
| `使用方法` | current-heading | §5.13 セクションタイトル の正表記 |
| `全体像` | current-heading | §5.13 セクションタイトル の正表記 |
| `前提事項` | current-heading | §5.13 セクションタイトル の正表記 |
| `前提条件` | current-heading | §5.13 セクションタイトル の揺れ表記 |
| `可変長ファイル` | current-heading | §5.8 テストデータ の正表記 |
| `同期応答メッセージ送信処理` | current-heading | §5.4 メッセージング方式 の揺れ表記 |
| `固定長ファイル` | current-heading | §5.8 テストデータ の正表記 |
| `概要` | current-heading | §5.13 セクションタイトル の揺れ表記 |
| `特殊記法` | ntf-doc-terms-heading | §5.8 テストデータ の正表記 |
| `自動テストフレームワーク` | current-heading | §5.1 全体・Nablarchの基本概念 の揺れ表記 |

#### 5.15.2 一括：今回は判定しない（295件）

用語集の役割を「ページ作成時に表記を揃えるための参照物」に縮小したため（`steering.md` #3差し戻し。ユーザー判断: `#5`（マッピング）が全量保証の唯一の根拠であり、用語集に網羅性の証明は求めない）、掲載基準（§3）の2種類（表記揺れが実在し正表記を確定した用語／`design.md` が章・セクション名として使う用語）のいずれにも該当しない候補について、候補ごとの個別の理由は付けない。一括して「今回は判定しない」と記録する。

内訳（出典は `mapping/term-candidates.csv` の `source` 列）:

| 出典 | 件数 | 備考 |
|---|---|---|
| design-heading（`design.md` 自身の章・セクション見出し） | 20件 | 文書構成を示すメタ見出しであり、処理方式・テスト種別・ページアウトラインの枠名称ではない |
| ntf-doc-terms-heading（`input/ntf-doc-terms.md` の節見出し） | 39件 | 複数語をまとめる節見出し・識別子を含む見出し・一般語彙・中核語が既に§5採用済みの節など |
| current-heading（現行解説書の見出し、複数ファイルに再出現するもの） | 39件 | 手順見出し・現行独自の節枠・識別子・ページ固有の説明的な題など |
| current-heading（現行解説書の見出し、1ファイルにのみ出現するもの） | 197件 | 識別子14件を含む。個々の出現数・file:line は `mapping/term-candidates.csv` を参照 |

対象の候補は次のとおり。`term-candidates.csv` の `term` 列と文字列一致で機械的に参照できる（1セルに複数の候補を束ねた行は、表を圧縮するため複数まとめて記載したもの）。

| 候補 |
|---|
| `1. 読者と構成`、`10. 未確定事項`、`1ページごとにレビューする`、`2. 第1部 テスティングフレームワークとは`、`3. 第2部 導入と設定`、`4. 第3部 テストの実装方法` |
| `5. 処理方式の名称`、`6. 用語`、`7. トンマナ`、`8. 対象外とするもの`、`9. 作業方針`、`「〜したい」形式の見出しを廃止する` |
| `「テストの種類」に置く対比`、`テストデータの2ページ`、`ページのアウトライン`、`マッピングを唯一の基準とする`、`モジュール一覧の集約`、`用語集を作成する` |
| `白紙から作成する`、`記載範囲` |
| `DB 系（SETUP_TABLE / EXPECTED_TABLE / EXPECTED_COMPLETE_TABLE / LIST_MAP）`、`FwHeaderDefinition / fwHeaderDefinition`、`HTML ダンプ出力`、`HTTP 同期応答メッセージ送信の用語読み替え`、`requestParams の仕様`、`testShots / requestParams（テストケース一覧）` |
| `testShots カラム一覧（ウェブアプリケーション）`、`testShots カラム一覧（バッチ処理）`、`testShots カラム一覧（メッセージング受信）`、`その他のフレームワーク固有用語`、`カラム省略の制約`、`コメント` |
| `コンポーネント設定の主要項目`、`シート・行・列・セル`、`セル値の解釈規則（特殊記法・マーカーカラム・コメント）`、`タイムスタンプ形式`、`テスト種別と主要クラス`、`テスト種別の正式名称` |
| `デフォルト値`、`データタイプ別の行構造`、`データタイプ（Data Types）`、`ファイルデータのフィールド定義用語`、`メッセージデータタイプ（同期応答メッセージ送信）`、`メッセージデータ構造（受信: setUpMessages / expectedMessages）` |
| `メッセージング`、`リクエスト単体テスト（RESTful ウェブサービス）`、`リクエスト単体テスト（ウェブアプリケーション）の主要クラス`、`リクエスト単体テスト（バッチ処理）`、`リクエスト単体テスト（メッセージ受信処理）`、`リクエスト単体テスト（同期応答メッセージ送信処理）` |
| `ログ検証（expectedLog）`、`制約事項（同期応答メッセージ送信）`、`可変長ファイル（SETUP_VARIABLE / EXPECTED_VARIABLE）`、`固定長ファイル（SETUP_FIXED / EXPECTED_FIXED）`、`基本用語`、`日付記述フォーマット` |
| `用語ドメインの全体像`、`設計原則（用語として登場する概念）`、`障害系テスト用特殊値` |
| `AbstractHttpRequestTestTemplate`、`Excelファイルの書き方`、`Form/Entity単体テストの書き方`、`MainForRequestTesting`、`StandaloneTestSupportTemplate`、`TestDataConvertor` |
| `TestShot`、`setter、getterに対するテストケース`、`その他の単項目精査のテストケース`、`コンポーネント設定ファイル設定項目一覧`、`スーパクラスについて`、`スーパクラスのメソッド呼び出し` |
| `テストの実施方法`、`テストクラスで共通のデータベース初期値`、`テストクラスの作成`、`テストクラスの書き方`、`テストデータの作成`、`テストデータの書き方` |
| `テストメソッドの書き方`、`テストメソッド作成`、`テストメソッド分割`、`テスト対象の成果物`、`テスト結果検証`、`テスト起動方法` |
| `フレームワークで使用するクラスの設定`、`モックアップクラスを使用した取引単体テストの実施方法`、`リクエスト単体テストの実施方法`、`取引単体テストの実施方法`、`各種期待値`、`各種準備データ` |
| `各種設定値`、`実行`、`提供方法`、`文字種と文字列長の単項目精査テストケース`、`構造`、`注意事項` |
| `特徴`、`結果確認`、`自動テストフレームワーク設定値` |
| `BasicHttpRequestTestTemplate`、`BatchRequestTestSupport`、`FileSupport`、`HttpRequestTestSupport`、`MQSupport`、`MessageSender` |
| `MessagingReceiveTestSupport`、`MessagingRequestTestSupport`、`RequestTestingMessagingProvider`、`RestTestSupport`、`SimpleRestTestSupport`、`TestCaseInfo` |
| `RequestResponseProcessor の実装クラスを作成する`、`コンポーネント設定ファイルに defaultProcessor という名前で実装クラスを設定する`、`1シートに複数ケースを含める場合`、`1テストケースを複数シートに分割する場合`、`Action/Component単体テストの書き方`、`Antビュー起動` |
| `BasicHttpRequestTest の使い方の補足`、`BasicHttpRequestTestTemplateを拡張する場合はアノテーションも作成する`、`Bean Validationに対応したForm/Entityのクラス単体テスト`、`Cookieなど前のレスポンスの情報を引き継ぐ方法`、`Cookie情報`、`DBに準備データのカラムを省略する場合` |
| `DB期待値のカラムを省略する場合`、`Eclipseとの連携`、`Eclipseとの連携設定`、`Excelによるテストデータ記述`、`Excelダウンロード`、`Excelファイルから、入力パラメータや戻り値に対する期待値などを取得したい` |
| `Excelファイルに記述できるカラムのデータ型に関する注意点`、`Excelファイル記述例`、`ExtendWithでテストクラスに適用する`、`Extension クラスと合成アノテーションの一覧`、`HTML4.01との相違点`、`HTMLダンプ出力` |
| `HTMLダンプ出力結果`、`HTMLチェック内容の変更`、`HTMLチェック実行要否の設定方法`、`HTMLファイルからの起動方法`、`HTTP同期応答メッセージ送信処理を伴う取引単体テストの実施方法`、`JUnit 4のTestRuleを再現する` |
| `JUnit 5で自動テストフレームワークを動かす`、`JUnit Vintage`、`JUnit4のアノテーションを使用する`、`JUnit4ベース`、`Nablarch Validationに対応したForm/Entityのクラス単体テスト`、`Nablarchに特化したテスト補助機能を提供` |
| `RegisterExtensionで使用する`、`ThreadContextにユーザID、リクエストIDなどを設定したい`、`ThreadContextへの値設定は不要`、`assertSqlResultSetEqualsメソッドに関する注意点`、`assertTableEqualsメソッドに関する注意点`、`setUpDbメソッドに関する注意点` |
| `その他の設定`、`アップロードファイルの記述方法`、`クエリパラメータ情報`、`クラスのプロパティを検証したい`、`クラス単体テストにおける登録・更新系テストの注意点`、`クラス単体テストの実施方法` |
| `コンストラクタに対するテストケース`、`コンポーネント設定ファイルに監視対象テーブルを記載`、`コンポーネント設定ファイルの記述例`、`システムリポジトリ登録例`、`システムリポジトリ登録内容`、`システム日時を任意の値に固定したい` |
| `シーケンスオブジェクトを使った採番のテストをしたい`、`シート内の構造`、`セルの書式`、`ダウンロードファイルのテスト`、`ツール起動`、`テストクラスでのトランザクション制御は不要` |
| `テストケース分割方針`、`テストケース実行のパターン分け`、`テストソースコード実装例`、`テストデータとテストクラスの作成`、`テストデータに空白、空文字、改行やnullを記述したい`、`テストデータに空行を記述したい` |
| `テストデータの外部化`、`テストデータは全てExcelシートに記述する`、`テストデータ記述例`、`テストデータ読み込みディレクトリを変更したい`、`テストメソッドの実行順序に依存しないテストを作成する`、`テストメソッド毎のデータベース初期値` |
| `テストメソッド記述方法`、`テスト実施`、`テスト実行前後に共通処理を行いたい。`、`テスト実行時指摘確認方法`、`テスト準備`、`テスト結果エビデンスの収集` |
| `テスト結果確認（目視）`、`ディレクティブのデフォルト値`、`デフォルト以外のトランザクションを使用したい`、`デフォルト値の変更方法`、`データベースの結果検証`、`データベーステストデータの省略記述方法` |
| `データベース関連機能`、`データ作成方法`、`データ入力`、`データ編集`、`バイナリファイルの場合`、`バックアップ用スキーマの作成、データ投入` |
| `バリデーションメソッドのテストケース`、`ビルドファイル登録`、`ファイルの結果検証`、`フレームワークで用意されたテストクラスのスーパークラスを継承する`、`プログラミング工程で使用するツール`、`プロパティファイルの書き換え` |
| `マスタデータを変更してテストを行いたい`、`マスタデータ投入ツール インストールガイド`、`メッセージ`、`メッセージング処理でテストデータに対し定型的な変換処理を追加したい`、`メール送信処理の構造とテスト範囲`、`モックアップを使用するための記述` |
| `モックアップクラスの設定`、`ユーザ情報`、`リクエストを送信する`、`リクエストパラメータ`、`リクエスト単体テストでの二重サブミット防止機能のテスト実施方法`、`リクエスト単体テストの実施方法(HTTP同期応答メッセージ送信処理)` |
| `リクエスト単体テストの実施方法(バッチ)`、`リクエスト単体テストの実施方法(ファイルアップロード)`、`リクエスト単体テストの実施方法(メール送信)`、`リクエスト単体テストの実施方法(同期応答メッセージ受信処理)`、`リクエスト単体テストの実施方法(同期応答メッセージ送信処理)`、`リクエスト単体テストの実施方法（HTTP同期応答メッセージ受信処理）` |
| `リクエスト単体テストの実施方法（応答不要メッセージ受信処理）`、`リクエスト単体テストの実施方法（応答不要メッセージ送信処理）`、`リクエスト単体テストクラス作成時の注意点`、`リクエスト単体テスト（HTTP同期応答メッセージ送信処理）`、`リクエスト単体テスト（RESTfulウェブサービス）`、`リクエスト単体テスト（ウェブアプリケーション）` |
| `リクエスト単体データ作成ツール インストールガイド`、`ログの結果検証`、`ログ出力設定`、`一つのシートに複数テストケースのデータを記載したい`、`事前処理・事後処理を実装する`、`事前準備補助機能` |
| `事前準備補助機能を使ってリクエストを生成する`、`二重サブミット防止機能のテスト実施方法`、`仕様`、`任意のディレクトリのExcelファイルを読み込みたい`、`使用禁止タグ・属性のカスタマイズ方法`、`依存関係の追加` |
| `入力となるHTML生成`、`具体例`、`出力ライブラリ(同期応答メッセージ送信処理)の構造とテスト範囲`、`動作イメージ`、`単体テスト実施方法`、`参照系のテスト` |
| `取引単体テストでの二重サブミット防止機能のテスト実施方法`、`取引単体テストのテストクラス例`、`取引単体テストの実施方法（バッチ）`、`取引単体テストの実施方法（同期応答メッセージ受信処理)`、`取引単体テストの実施方法（応答不要メッセージ受信処理）`、`取引単体テストの実施方法（応答不要メッセージ送信処理）` |
| `同じテストメソッドをテストデータを変えて実行したい`、`同期応答メッセージ送信処理を伴う取引単体テストの実施方法`、`命名規約`、`固定長ファイル、CSVファイルの場合`、`基本的なテスト方法`、`基本的な使い方` |
| `基本的な記述方法`、`外部キーが設定されたテーブルにデータをセットアップしたい`、`外部キーが設定されたテーブルを使用する場合について`、`外部プログラム選択`、`実行方法`、`実装するインタフェース` |
| `常駐バッチのテスト用ハンドラ構成`、`必要となるスキーマ`、`日付の記述方法`、`更新系のテスト`、`本フレームワークのクラスを継承せずに使用したい`、`注意点` |
| `独自の拡張を加える`、`独自拡張クラスを作成する`、`独自拡張用のExtensionを作成する`、`環境構築`、`目的`、`目的別API使用方法` |
| `結果を確認する`、`自動テストフレームワークの使用方法`、`自動テストフレームワークの構成`、`複数のデータタイプ使用時はデータタイプごとにまとめてデータを記述する`、`複雑なテストケースの場合`、`要求電文のアサート` |
| `要求電文のログ出力`、`要求電文の期待値および、返却する応答電文（レスポンスメッセージ）の準備`、`設定`、`設定ファイルの例`、`設定ファイル例`、`設定画面起動` |
| `起動用バッチファイル（シェルスクリプト）選択`、`電文を1回送信する場合の要求電文の期待値および、返却する応答電文（レスポンスメッセージ）の例`、`電文を2回以上送信する場合の要求電文の期待値および、返却する応答電文（レスポンスメッセージ）の例`、`非常に簡単なテストケースの場合`、`項目間精査のテストケース` |

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
| `本フレームワーク` | `テスティングフレームワーク` | 現行解説書に由来する記述に限る。FW解説書を引用・参照する箇所の `本フレームワーク` はNablarchを指す（FW10件）ので置き換えない |
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
| `メッセージング処理` | `MOMによるメッセージング` | MOMを指すことが文脈から確定できる場合に限る。`NTF:06_TestFWGuide/03_Tips.rst:786` の「メッセージング処理でテストデータに対し定型的な変換処理を追加したい」は `TestDataConverter` の話でMOM限定ではないので置き換えない |
| `応答不要メッセージ送信処理` | `応答不要メッセージ送信` | 無条件 |
| `応答不要メッセージ受信処理` | `応答不要メッセージ受信` | 無条件 |
| `同期応答メッセージ送信処理` | `同期応答メッセージ送信` | `HTTP同期応答メッセージ送信処理` の一部でない場合に限る |
| `メッセージ同期送信処理` | `同期応答メッセージ送信` | 無条件（語順違いの表記揺れ。`HTTPメッセージ同期送信処理` の一部でない場合に限る） |
| `メッセージ同期送信` | `同期応答メッセージ送信` | 無条件（語順違いの表記揺れ。`HTTP メッセージ同期送信` の一部でない場合に限る） |
| `同期応答メッセージ受信処理` | `同期応答メッセージ受信` | `HTTP同期応答メッセージ受信処理` の一部でない場合に限る |
| `メッセージ受信処理` | `同期応答メッセージ受信` | 単独で現れ、かつ同期応答受信を指すことが文脈から確定できる場合に限る |
| `HTTP同期応答メッセージ送信` | `HTTPメッセージ送信` | 無条件 |
| `HTTP同期応答メッセージ送信処理` | `HTTPメッセージ送信` | 無条件 |
| `HTTP 同期応答メッセージ送信` | `HTTPメッセージ送信` | 無条件 |
| `HTTP 同期応答メッセージ送信処理` | `HTTPメッセージ送信` | 無条件 |
| `HTTPメッセージ同期送信処理` | `HTTPメッセージ送信` | 無条件（語順違いの表記揺れ） |
| `HTTP メッセージ同期送信` | `HTTPメッセージ送信` | 無条件（語順違いの表記揺れ） |
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
| `テストケース` | `テストショット` | `テストケース一覧`・`テストケース表` の一部でない場合に限る（これらは `テストショット一覧` への置換ルールで処理する）。`@Test` メソッドそのものを名指しする場合は `テストメソッド`、何を検証するかを述べる場合は普通名詞の `テスト` に置き換える。**業務上のテストケース（プロジェクトのテスト仕様書上のテスト項目1件）を指す場合は置き換えない**（§5.7 の別義）。**ただしこの例外は、用語集・設計文書がNTFの `テストショット` と対比するために別義へ言及する場合に限る。NTF解説書の本文には該当する用法が存在しない**（マッピング対象範囲内の `テストケース` 196件を実物で全数確認した結果、すべて `testShots` のエントリを指すか、何を検証するかを述べるかのいずれかであった。`S:ntf-doc-terminology.md:19`。**この196という数は本リポジトリでは再現できず、未照合である。** 実測は、マッピング対象範囲内 215件〈現行174・input41〉／出典ファイル全体 234件〈現行191・input43〉／対象3ページ 77件〈notation 42・examples 33・about 2〉であり、いずれも196にならない。`テストケース` を含む現行解説書は `#7` で削除済みのため `6bf8cfb^` 時点の内容で計数した。**主張の出所は作業指示 `S:ntf-doc-terminology.md:19` であり、§5.7 の未照合注記と同じ扱いとする**）。**したがって解説書のページ本文では例外が成立せず、常に置き換える。ページ本文に `テストケース` を残してよいという意味ではない**（各ページのゲートは `テストケース` 0件を求める） |
| `セクション` | `データブロック` | テストデータの単位を指す場合に限る。文書構造の意味（`design.md`・マッピングの `section_id`・§5.13「セクションタイトル」）は置き換えない |
| `データブロック種別` | `データタイプ` | 無条件 |
| `グループ ID` | `グループID` | 無条件 |
| `groupId` | `グループID` | テストデータのグループIDを指す場合に限る。Mavenの `<groupId>` 要素、参照ラベル `tips_groupId`、YAMLの `group_id` キーは識別子なので置き換えない |
| `テストケース一覧` | `テストショット一覧` | 無条件 |
| `テストケース表` | `テストショット一覧` | 無条件 |
| `テストショット表` | `テストショット一覧` | 無条件 |
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
| 設計原則（L110）— テスト独立性・データ集約・データタイプまとめ記述 | 不採用 | 3語とも造語で、現行・FW解説書に0件。現行は「テストメソッドの実行順序に依存しないテストを作成する」（`NTF:06_TestFWGuide/01_Abstract.rst:585`）のように文で書く。design.mdの「〜する」形式に合うため文のまま引き継ぐ |
| グループ ID（L118） | 表記変更 | 空白を除いた `グループID` を正表記とする。現行解説書73件が空白なし |
| データタイプ別の行構造（L129） | 採用 | レコード種別行・フィールド名称行・データ型行・フィールド長行を §5.10 に掲載。現行解説書に該当語がないため、input資料の表記をそのまま採る |
| ディレクティブ（L213） | 採用 | FW解説書24件と一致 |
| testShots / requestParams（L234） | 採用 | `testShots` `requestParams` はデータブロックのIDであり識別子。日本語の総称は `テストショット一覧` を使う |
| メッセージング 基本用語（L327） | 一部不採用 | `電文`・`要求電文`・`応答電文`・`フレームワーク制御ヘッダ`・`メッセージボディ` はFW解説書と一致するため採用。「電文種別」はFW解説書・現行解説書に0件のため不採用とし、`要求電文`・`応答電文` で書き分ける |
| HTTP 同期応答メッセージ送信の用語読み替え（L398） | 表記変更 | クラス名の対応表は識別子としてそのまま採用する（掲載基準の対象外）。節題「HTTP 同期応答メッセージ送信」はFW解説書の `HTTPメッセージ送信` に置き換える（§5.4）。不採用の要素はないため「表記変更」とする |
| テスト種別の正式名称（L414） | 表記変更 | 「リクエスト単体テスト（バッチ処理）」「（メッセージ受信処理）」「（RESTful ウェブサービス）」は処理方式名が `design.md` の正式名称と異なる。§5.2・§5.4 の正表記に置き換える |
| DB アクセステスト（L427） | 表記変更 | 完全一致の `DBアクセステスト` は全コーパスに0件で、`DB アクセステスト` は造語。現行解説書のページ題「データベースを使用するクラスのテスト」（`NTF:06_TestFWGuide/02_DbAccessTest.rst:2`）に置換。分類軸ではなく一形態のため§5.5の下位に置く |
| 主要クラス各節（L443 以降） | 採用 | クラス名は識別子。日本語の役割説明は `主なクラスとリソース` の表に集約する |
| その他のフレームワーク固有用語（L526） | 一部不採用 | `内蔵サーバ` は採用（現行解説書18件）。併記の `内蔵サーブレットコンテナ`（L450）は使わない。`nablarch.test.resource-root` などの設定キーは識別子であり掲載対象外 |

## 10. 未解決事項

用語集の中で決着させるべきだが、まだ決まっていないもの。

| # | 事項 | 内容 |
|---|---|---|
| 1 | `シート` を残す範囲 | YAML形式にはシートがない。Excel形式の説明でのみ `シート` を使う方針としたが、どのセクションをExcel形式限定の記述にするかはマッピング（タスク #5）で確定する |
| 2 | `テーブルデータ`・`ファイルデータ` の位置づけ | 「テーブル／ファイル／メッセージ」で分類する軸と「準備データ／期待値／テストショット一覧」で分類する軸が交差する。第3部「テストデータの書き方」（`S:design.md:151`）を1ページに集約すると決めているため、章立ての軸はマッピング後に決める |
| 3 | `レコード種別行` の根拠の弱さ | input資料1ファイル・3件しかなく、うち代表出典（`S:input/ntf-doc-terms.md:175`）は図中のラベルで定義箇所ではない。`複数レコードレイアウト`（§5.8）のファイルデータを扱うページの執筆時に、実データの記述で置き換えられるか再確認する |

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
