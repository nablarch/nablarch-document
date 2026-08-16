# レビュー記録 — リクエスト単体テストの設定（MOMによるメッセージング）

対象ページ: `ja/development_tools/testing_framework/setup/request_unit_test/mom.rst`
ページ先頭ラベル: `request_unit_test_setting_mom`（`style.md` S-08 の表 `:353` から引用。新規考案なし）
タスク: `#21`
本文コミット: `8b956cd`

## 1. 出典（`mapping.csv` の全件）

`dest_page=リクエスト単体テストの設定（MOMによるメッセージング）` は8行。`csv.DictReader` で全595行を読んで抽出した（`wc -l` は使っていない）。`DROP` 0件。

| `mapping_id` | `src_file` | 範囲 | `lines` | `disposition` | `dest_section` |
|---|---|---|---|---|---|
| `current-0106-b` | `.../05_UnitTestGuide/02_RequestUnitTest/real.rst` | `167`〜`177` | 11 | SPLIT | 使用方法 |
| `current-0247` | `.../06_TestFWGuide/03_Tips.rst` | `788`〜`794` | 7 | MERGE | 拡張例 |
| `current-0248` | `.../06_TestFWGuide/03_Tips.rst` | `797`〜`799` | 3 | MERGE | 拡張例 |
| `current-0249` | `.../06_TestFWGuide/03_Tips.rst` | `802`〜`809` | 8 | MERGE | 拡張例 |
| `current-0250` | `.../06_TestFWGuide/03_Tips.rst` | `812`〜`818` | 7 | MERGE | 拡張例 |
| `current-0251` | `.../06_TestFWGuide/03_Tips.rst` | `821`〜`832` | 12 | MERGE | 拡張例 |
| `current-0303` | `.../06_TestFWGuide/RequestUnitTest_real.rst` | `168`〜`181` | 14 | MOVE | 拡張例 |
| `current-0328` | `.../06_TestFWGuide/RequestUnitTest_send_sync.rst` | `127`〜`140` | 14 | MOVE | 拡張例 |

計 76 lines。出典の実物は、現行解説書が本ブランチで削除済みのため `git show c241906:<src_file>` で読んだ。`note` 欄の説明文は根拠にしていない。

`拡張例` の7行は3つの出典に分かれるが、主題は `TestDataConverter` の1つに集約される（`current-0303` と `current-0328` はほぼ同文、`current-0247`〜`0251` が同じ主題をより詳しく書く）。`steering.md` Acceptance criteria「重複がない。参照で解決する」に従い、1つの L3 セクションに統合した。

## 2. 実装で確認した事実

### 参照した成果物とコミット

| 成果物 | 取得元 | 参照コミット |
|---|---|---|
| `nablarch/nablarch-testing` | クローン（`main`） | `e21bf67` |
| `nablarch/nablarch-testing-yaml` | クローン（`feature/ntf-yaml`） | `a966ab9` |

リポジトリ直下のビルド残骸 `nablarch/test/core/reader/MessageParser.java`（git の追跡下にない）は使っていない。

### 確認した事実

| ページの記述 | 実装での裏付け（`file:line`） |
|---|---|
| インタフェースの正式名は `TestDataConverter` | `nablarch-testing` `src/main/java/nablarch/test/core/file/TestDataConverter.java:17`。`TestDataConvertor` は追跡下のソース全体で0件（`grep -rn "TestDataConvertor" .` が0件） |
| `:java:extdoc:` で参照できる公開APIである | 同 `:16`（`@Published`） |
| 実装するメソッドは `convertData` と `createDefinition` の2つ | 同 `:37`（`convertData(LayoutDefinition, DataRecord, Charset)`）・`:27`（`createDefinition(LayoutDefinition, DataRecord, Charset)`）。呼び出し順は `convertData` → `createDefinition`（`MessagePool.java:122-124`・`:148-152`） |
| コンポーネント名は `TestDataConverter_` に `file-type` の値を続けたもの | `FixedLengthFile.java:155-158`（`directives.get("file-type")` を取り、`SystemRepository.get("TestDataConverter_" + fileType)` で引く） |
| 登録先はテスト用のコンポーネント設定ファイル | `SystemRepository.get` はコンポーネントを返す。実配置例は `src/test/resources/nablarch/test/core/messaging/web/web-component-configuration.xml:50-54`・`web-component-configuration-request-testing.xml:42`（いずれも `<component name="TestDataConverter_...">`）。`current-0303`/`current-0328` の「テスト用のコンポーネント設定ファイル」が正しく、`current-0247` の「システムリポジトリに登録する」とも矛盾しない |
| 変換が効くのは電文のテストデータ | `FixedLengthFile.createDefinition`／`convertData` の呼び出し元は `MessagePool.java:244`・`:253` のみ（`src/main/java` を全走査）。`MessagePool` を使うのは `RequestTestingMessagePool.java:87`・`:126`、`SendSyncSupport.java:299`・`:330`、`RequestTestingMessagingClient.java:412`・`:414` で、いずれも電文の経路。ファイルデータの入出力経路では呼ばれない |
| 変換前の値は `text-encoding` に指定したエンコーディングでバイト列になる | `DataFile.java:300-302`（`TEXT_ENCODING` の値を `Charset.forName` で保持）、`FixedLengthFile.java:131`・`:147`（`getEncodingFromDirectives()` をコンバータに渡す） |
| `reader.fwHeaderfields` にフレームワーク制御ヘッダのフィールド名をカンマ区切りで指定する | `MessageParser.java:33`（キー名）・`:107-110`（`SystemRepository.getString` を `makeArray` で分割） |
| 既定は `requestId`・`userId`・`resendFlag`・`resultCode` の4つ | 同 `:109` |
| 環境設定ファイル（properties）に書く | 同 `:108`・`:110` が `SystemRepository.getString`（コンポーネントではなく文字列）で引く。`#11` の `nablarch.test.resource-root`（`setup/common.rst:17`）と同型 |
| MOM のメッセージ受信のテストで使われる | `MessagingRequestTestSupport.java:82`／`MessagingReceiveTestSupport.java:42` → `MQSupport.java:87` → `BasicTestDataParser.java:82-85`（`new MessageParser(...)`） |
| 同期応答メッセージ送信では、キーと値の組として記述したフレームワーク制御ヘッダは使用されない | 経路は2つあり、いずれも解析結果を捨てる。(a) `RequestTestingSendSyncSupport.java:157` → `BasicTestDataParser.java:113-117`（`GroupMessageParser`）→ `GroupMessageParser.java:43`（委譲先は `SendSyncMessageParser`）・`:58`（`Collections.emptyMap()`。コメント「FWヘッダ取得機能は使用しないので、何も設定しない」）。(b) `SendSyncSupport.java:421` → `BasicTestDataParser.java:99-103`（`SendSyncMessageParser`）→ `SendSyncMessageParser.java:35-44`（`getFwHeader()` が `UnsupportedOperationException`。Javadoc「MessageParserが提供するFWヘッダの解析機能は使用しない」） |
| `file-type` の値は応答電文のアサート方式にも影響する | `MessagePool.java:54`（`messaging.assertAsMapFileType`）・`:154-158`（未設定時は `"Fixed"` のみ）・`:160-163` |

### 出典と実装が食い違った点（全件）

| # | 出典 | 実装 | ページでの扱い |
|---|---|---|---|
| 1 | 見出しが `TestDataConvertor`（`RequestUnitTest_real.rst:166`・`RequestUnitTest_send_sync.rst:125`） | `TestDataConverter`（`TestDataConverter.java:17`）。同じ出典の本文（`:179`・`:138`）とキー名は `TestDataConverter_` で、見出しだけが誤り | `TestDataConverter` を採用 |
| 2 | 「Excelに記述されたデータ」「Excelから読み込んだテストデータ」（`03_Tips.rst:789`・`RequestUnitTest_real.rst:169`・`RequestUnitTest_send_sync.rst:128`）。`TestDataConverter.java:12` の Javadoc も「エクセルファイルに記述された」 | 形式を問わない。`YAML` 経路も `FixedLengthFile` を組み立てて `file-type` を含むディレクティブを適用し（`nablarch-testing-yaml` `YamlMessageBuilder.java:186-190` → `YamlFileBuilder.java:245-252`）、その `FixedLengthFile` が `RequestTestingMessagePool` の `source` になる（`YamlMessageBuilder.java:63-64`・`:89`）。`file-type` は `YAML` スキーマにも `directives` のキーとして定義されている（`ntf-testdata-yaml-schema.json` の `"file-type"`） | `Excel`／`YAML` のいずれにも触れず「電文のテストデータ」と書いた（`design.md` §8「出典と実装が食い違う場合は実装を優先する」）。形式差が無いため `style.md` S-10 規約3 の形式別 L4 も作らない |
| 3 | 「システムリポジトリに登録する」（`03_Tips.rst:793`・`:800`）と「テスト用のコンポーネント設定ファイルに登録する」（`RequestUnitTest_real.rst:179`・`RequestUnitTest_send_sync.rst:138`）で表現が割れる | 実体は `<component>` 定義（上表の実配置例） | 後者を採用。`#11` の同型の是正（`nablarch.test.resource-root` の設定先）と同じ判断基準 |

| 4 | 「編集したデータを**読み込むための**レイアウト定義データを動的に生成する」（`RequestUnitTest_real.rst:175`・`RequestUnitTest_send_sync.rst:134`）。`createDefinition` の用途を「読み込み」に限定している | `createDefinition` が返すレイアウト定義は、**書き出しと読み込みの双方に使われる。** 書き出しは `MessagePool.java:122`（`convertByFileType`）→ `:124`（`createLayoutFromDataRecord`。中身は `:252-254` の `source.createDefinition(defaultLayout, dataRecord)`）→ `:130`（`msg.setFormatter(formatter.setDefinition(ld)).addRecord(currentData)`）で、`RequestTestingMessagePool.java:87-96` も同型（応答電文のバイナリ生成）。読み込みは `MessagePool.java:148-152`（同じ手順で `ld` を得る）→ `:165`（`responseMessage.setFormatter(formatter.setDefinition(ld)).readRecords()`）で、APが実際に出力した応答電文を同じ `ld` で読み込む。したがって出典のように方向を「読み込み」に限定するのも、逆に「書き出し」に限定するのも実装と合わない。インタフェースの Javadoc（`TestDataConverter.java:20`「現在処理中のテストデータに**対応した**レイアウト定義データを生成します」）も方向を限定していない | 「変換後のデータに対応するレイアウト定義を動的に生成する」に改めた（`mom.rst:46`。**ラウンド2・是正1**）。方向を限定しない Javadoc の表現に合わせた。`design.md` §8「出典と実装が食い違う場合は実装を優先する」の適用 |

食い違いは以上の4件（うち4はラウンド2で追加）で、他は出典と実装が一致した。

### デフォルト値の基準（`design.md` §8）

本ページには「デフォルト値」の欄を持つ設定項目表を置いていない。設定は2件（`reader.fwHeaderfields` と `TestDataConverter_*` の登録）で、いずれも「値を変える設定項目」ではなく「登録するかどうか」の設定である。`reader.fwHeaderfields` の未設定時の実効値（`requestId`・`userId`・`resendFlag`・`resultCode`）は `MessageParser.java:109` で確認したが、その一覧は承認済みの `testdata_notation.rst:1137` が既に持っているため、本ページは `:ref:` で導線を張るにとどめた（重複を作らない）。

## 3. 作成時の判断（レビュー前に確定したもの）

### D-1（判断1）`reader.fwHeaderfields` は本ページにも書く。ただし `http_messaging.rst` の記述を複製しない

**結論**: 作業指示の既定の方針を採る。本ページの `使用方法` に、MOM のメッセージ受信という文脈に限定して簡潔に書く。`http_messaging.rst` への `:ref:` は張らない。

**理由**:

1. `mapping.csv`（唯一の基準）が `current-0106-b` を本ページの `使用方法` に割り当てている。落とすと「マッピングにある内容を落とさない」に抵触する。`使用方法` は第2部のページアウトラインで唯一の必須セクションであり（`design.md:194`）、ここを他ページへの `:ref:` 1行にすると必須セクションが実質的に空になる。
2. ~~適用範囲が同一ではない。`http_messaging.rst:37` は「HTTPメッセージ受信のテスト」を条件にしており、本ページは MOM のメッセージ受信を条件にする。~~ **この根拠は取り消す（ラウンド1・R-1）。実装で否定された。** 訂正の内容は下記「R-1 の訂正」を参照。
3. 複製は避けた。`http_messaging.rst:44-46` が `important` として持つ `Excel`／`YAML` の差は、本ページでは段落中の1文に畳んだ（`mom.rst:17`）。コード例は出典 `current-0106-b`（`real.rst:174-175`）そのものであり、両ページとも同じ出典由来の同じ例を持つ。

**R-1 の訂正（ラウンド1）**: 上記 2 は誤りである。実装を追い直したところ、両ページの対象は**同一コードパス・同一設定**であった。

- HTTPメッセージ受信のリクエスト単体テストに専用のテストサポートクラスは存在しない。現行解説書の `05_UnitTestGuide/02_RequestUnitTest/http_real.rst:5` が「リクエスト単体テストの実施方法は `real_request_test` を参照すること」として同期応答メッセージ受信のページに委ね、そこで継承すべきクラスとして `MessagingRequestTestSupport` を指している（`05_UnitTestGuide/02_RequestUnitTest/real.rst:15`。ただしパッケージ名 `nablarch.test.core.http` は誤りで、実体は `nablarch.test.core.messaging`）。`nablarch-testing` の追跡下 `src/main/java` に `MessagingRequestTestSupport` を継承するクラスは `MessagingReceiveTestSupport.java:13` の1件のみで、HTTP専用のサブクラスは存在しない。
- `MESSAGE=setUpMessages` を読む経路は1つしかない。`TestDataParser#getMessage` の `src/main/java` 内の呼び出し元は `MQSupport.java:87` のみ（`DbLessTestDataParser.java:55-56` は同名メソッドへの委譲）。その `MQSupport` を生成するのは `MessagingRequestTestSupport.java:82` と `MessagingReceiveTestSupport.java:42` の2箇所だけである。
- したがって `reader.fwHeaderfields` を読む `MessageParser`（`BasicTestDataParser.java:82-83`）に至る経路は、MOM も HTTPメッセージング受信も完全に同一である。適用範囲の差は無い。

参照コミット: `nablarch/nablarch-testing` = `e21bf67`。

**結論は変えない。** D-1 の理由1（`mapping.csv` が本ページの `使用方法` に割り当てており、落とすと第2部で唯一必須のセクションが空になる）と理由3（複製を避ける）は成立しているため、本ページにも書く。集約先の判断は引き続き `decide` として上申する。むしろ、適用範囲が同一だと確定したことで、集約の検討はより強く必要になった。

**`decide` 候補として上申する。** 承認済みの `http_messaging.rst` と本ページに、同じキー・同じ既定値・同じコード例が並ぶ。寄せるなら (a) 第2部に「メッセージングのリクエスト単体テストの共通設定」を作る、(b) `http_messaging.rst` 側に集約して MOM から `:ref:` する、(c) 現状（各ページで自己完結）のいずれかを選ぶ必要がある。作成側の判断は (c) だが、採否はコーディネータ／ユーザーの判断に委ねる。`#19` の申し送り5（`testdata_notation.rst:1137` との重複）と同根の問題である。

### D-2（判断2）Excel記述例の画像2枚は載せない。セル格子の表にも置き換えない

**結論**: `data_convert_example.png`・`data_convert_internal.png` は移設せず、`git mv` も行わない。セル格子の `list-table` にも置き換えない。事実は地の文に残した（`mom.rst:56`）。

**理由**:

1. `design.md:200-207` の記載範囲表は、第2部に「テストデータの記述例」を**記載しない**と定めている。両画像は Excel のセル格子そのもの（識別子行 `MESSAGE=setUpMessages`・ディレクティブ行 `file-type` / `text-encoding`・列名行・データ行）を写したもので、記述例に当たる。
2. `style.md` S-10 規約2 に従ってセル格子の `list-table` に描き直すことは技術的には可能だが、それは記述例を第2部に置くことにほかならず、1の判断と衝突する。`#20` で削った数値記述例を第3部へ移した判断（`steering.md` `#20` の `decide` 2）と同じ基準である。
3. 同じ例は既に `ja/biz_samples/04/0401_ExtendedDataFormatter.rst:174-204` が持っている（`FormUrlEncodedTestDataConverter` の登録例・Excel の画像・変換後データ）。新解説書側で再掲する必要がない。

**出典の事実が地の文に残っていることの確認**: `current-0251` が画像で示していた事実は「上記で指定したコンバータでセル内の各データにURLエンコーディングを行うように実装した場合、テストフレームワーク内部では以下のデータを記述した場合と同様に扱われる」（`03_Tips.rst:824-825`）である。`mom.rst:56` の「URLエンコードを行うコンバータを実装しておけば、テストデータに日本語のまま記述した値が、URLエンコード済みの値を記述した場合と同じように扱われる」がこれに対応する。加えて `mom.rst:56` の前半で、`file-type` に指定した値（画像1枚目の `FormUrlEncoded`）がコンポーネント名の後半と対応することも述べている。

**残る論点**: 両画像は `ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/_images/` に残ったままになる。`design.md:842` は「削除前の現行解説書が持っていた画像は、該当ページのタスクで `git mv` して移す」「`guide/` 配下は全ページの移設完了後にディレクトリごと無くなる」としているため、**どのページにも移らない画像の最終的な扱いは `#last` で決める**。本タスクでは削除しない。

### D-3（判断3）サンプルクラスの完全修飾名は `com.example` を使う

**結論**: `com.example.test.core.file.FormUrlEncodedTestDataConverter`（`mom.rst:54`）。出典の `please.change.me.test.core.file.FormUrlEncodedTestDataConverter`（`03_Tips.rst:817`）は採らない。

**根拠**:

1. NTF新解説書は `#11` の是正で `com.example` を採用済みである（`setup/common.rst:61` の `com.example.common.idgenerator.OracleSequenceIdGenerator`）。同一書内で2つの慣習を混在させない。
2. `ja/` 配下の追跡下 `.rst` での実測（`git grep`。`ja/_build/` は含まない）は `com.example` が69件・20ファイル、`please.change.me` が45件・12ファイルで、`com.example` が多数派である。
3. パッケージの並びは `#11` と同じく「Nablarch側のパッケージ構成を `com.example` に置き換える」形にした（`nablarch.common.idgenerator` → `com.example.common.idgenerator` と同様に、`nablarch.test.core.file` → `com.example.test.core.file`）。出典の `please.change.me.test.core.file` とも構成が一致する。

**留意点として記録する**: `please.change.me.test.core.file.FormUrlEncodedTestDataConverter` は架空のクラス名ではなく、業務サンプル `ja/biz_samples/04/0401_ExtendedDataFormatter.rst:26-30`・`:191` が実際に提供するクラスである。同ページ `:181` は「テストデータコンバータについてはプログラミング・単体テストガイドの自動テストフレームワークの使用方法を参照すること」と地の文で NTF解説書を指しているが、`:ref:` は張られていない。**業務サンプルとの相互リンクを張るかどうかは本タスクの範囲外**（マッピングにも `design.md` にも規定が無い）として、`#last` へ回す。

### D-4（判断4）ファイル入出力・電文まわりの導線

**結論**: `testdata_notation-messaging_data` への `:ref:` を2箇所に張る（`mom.rst:17`・`:60`）。`request_unit_test_setting_batch` への導線は**張らない**。

**`testdata_notation-messaging_data` を張る理由と確認**:

- `design.md:209` が「『使い方』に該当するものは第3部に置き、第2部からは `:ref:` で参照する」と定めている。本ページが触れる「フレームワーク制御ヘッダのフィールド名」「電文のテストデータのディレクティブ `file-type`」は、いずれも参照先の `testdata_notation.rst:1115-1272` が扱っている。
- **参照先の本文を読み、本ページの記述・実装と矛盾しないことを確認した**（`#19` の申し送り2）。
  - `testdata_notation.rst:1137`「既定値は `requestId`・`userId`・`resendFlag`・`resultCode` の4種だが固定ではなく、`SystemRepository` の `reader.fwHeaderfields` キーでプロジェクトが任意の名前に変更できる」— `MessageParser.java:109` と一致。
  - `testdata_notation.rst:1177`・`:1183-1189`「応答電文のアサート方式は、ディレクティブの `file-type` の値、または `SystemRepository` の `messaging.assertAsMapFileType` キーの設定によって切り替わる。未設定時のデフォルトは `"Fixed"` 形式」— `MessagePool.java:154-163` と一致。
  - `testdata_notation.rst:1161`「ディレクティブには、`file-type`（テスティングフレームワークが固定長のみに対応するため）と `record-length` を記載する必要はない」— 「必要はない」であって「書けない」ではなく、`:1177` 自身が `file-type` を書いた場合の挙動を述べている。本ページの「`file-type` に指定した値をコンポーネント名に使う」と矛盾しない。
  - `testdata_notation.rst:1263`「`fw_header:` に記載したキーは全てフレームワーク制御ヘッダとして扱われ、`reader.fwHeaderfields` でフィルタして取り捨てられることはない」— 本ページ `mom.rst:17` の後半と一致し、実装（`nablarch-testing-yaml` の追跡下 `src/main/java` に `fwHeaderfields` の参照0件）とも一致。
  - **既知の食い違いが1件残る。** `testdata_notation.rst:1244`「キー名は固定ではなく、`reader.fwHeaderfields` の設定に合わせる」は `YAML` 形式の `fw_header:` の説明であり、同ファイル `:1263` とも実装とも食い違う。`#19` の申し送り4・7 が既に記録しており、`testdata_notation.rst` は user review 承認済みのため本タスクでは是正しない。本ページは実装に合う側（`YAML` ではこの設定を使わない）で書いた。
- ラベルの実在を確認した（`testdata_notation.rst:1115`）。
- ~~参照が2箇所になるのを避け、`mom.rst:60` の `tip` で「記述方法」と「アサート方式への影響」をまとめて1つの `:ref:` にした。~~ **記述が実態と食い違っていた（ラウンド1・R-2）。** 実際には `testdata_notation-messaging_data` への `:ref:` は `mom.rst:17` と `mom.rst:60` の**2箇所**にあり、「1つの `:ref:` にした」わけではない。`mom.rst:60` の `tip` で「記述方法」と「アサート方式への影響」を1つの `:ref:` にまとめた、というのが正しい記述である（生成HTMLでも `href="../../implementation/testdata_notation.html#testdata-notation-messaging-data"` が2件出ることを確認した）。
- **同一ラベルへの2箇所参照は規約違反ではない。** 承認済みページに同じ形が既に2件ある（`git grep -n` で確認）。
  - `setup/request_unit_test/batch.rst:78`・`:82` — いずれも `:ref:`ファイルのデータを記述する `<testdata_notation-file_data>``
  - `setup/request_unit_test/rest.rst:74`・`:85` — いずれも `:ref:`Webフロントコントローラ `<web_front_controller>``
  したがって「参照が2箇所になるのを避ける」という制約自体が存在しない。`style.md` S-08 は `:ref:` ラベルの命名規則のみを定めており、参照回数の制限は置いていない。

**`request_unit_test_setting_batch` へ張らない理由**:

- 本ページが扱う2件の設定は、`batch.rst` が持つ `defaultDirectives` / `fixedLengthDirectives` / `variableLengthDirectives` および `TEST_X9` / `TEST_SX9` と、設定上の依存関係を持たない。本ページはファイル入出力に触れていない（`#20` の申し送り1 の条件「ファイル入出力に触れるときは」に当たらない）。
- `TestDataConverter` の鍵になる `file-type` は、**`defaultDirectives` では設定できない**。`DataFile.java:91-92` が、共通の既定値を適用した**後**に `setDirective("file-type", getFileType())` で上書きするためである。したがって「既定値でまとめて指定できる」という導線は本ページの主題に対して成立しない。
- 主題のつながらない先へリンクすると、`steering.md` Rules が `#8` で問題にした「行き来するだけのリンク」になる。

**申し送りとして残す**: `defaultDirectives` の説明は `batch.rst:41-78` にしかなく、`#20` の申し送り1 が指摘するとおり電文経路（`FixedLengthFile` のコンストラクタ）でも効く。MOM だけを読む読者がこの設定に辿り着く導線は依然として無い。ページ横断の構造の問題であり、`#last` で扱う。

### D-5 `機能概要` の見出しは置かない

出典0行のため。`design.md:194`「『使用方法』のみ必須とし、『機能概要』『拡張例』は出典が無い場合は見出し自体を置かない」に従う。`verify_mapping.py` は0件を advisory として出す（`optional since #6`）。

### D-6 `使用方法` に「アーキテクトが行う」の `tip` を置かない

`http_messaging.rst:15-17` は `使用方法` の直下にこの `tip` を持つが、本ページには置かなかった。`current-0106-b` の `audience` は `mapping.csv` 上 `user`（`note` に「3観点レビュー対応 audienceをdeveloperからuserへ修正」とある）であり、`common.rst`・`class_unit_test.rst`・`web.rst`・`rest.rst`・`batch.rst` のいずれもこの `tip` を持たない。`拡張例` 側は出典が明示的に「アーキテクトが実装する」と述べているため（`RequestUnitTest_real.rst:170`・`RequestUnitTest_send_sync.rst:129`）、地の文に残した（`mom.rst:35`）。

### D-7 リード文に「MOM固有の設定ではない」と書いた

`TestDataConverter` の適用範囲は電文のテストデータ全般であり、MOM に限定されない（§2 の実装確認）。`glossary.md:522` も、出典の見出し「メッセージング処理でテストデータに対し定型的な変換処理を追加したい」について「`TestDataConverter` の話でMOM限定ではないので置き換えない」と明記している。マッピングは本ページにのみ割り当てているため設定手順は本ページに置き、適用範囲はリード文に書いた。`batch.rst:10` が同型の書き方（「後の2つはNablarchバッチアプリケーションに固有の設定ではなく、…」）で承認済みである。

### D-8 `file-type` がアサート方式にも影響することを `tip` で補った

出典・マッピングのいずれにも無い。`file-type` に `Fixed` 以外の値を指定するとコンバータが有効になる一方、応答電文のアサートが電文全体の文字列比較に切り替わる（`MessagePool.java:154-163`）。本ページの手順どおりに設定した読者が、意図せずアサート方式を変えてしまう経路がそのまま存在する。`design.md` §8「出典が欠いている、実装上必須の設定」（`#17` の `decide` 1 で規定化）に当たると判断し、新しい事実を書き下ろすのではなく、既に承認済みの `testdata_notation.rst:1177-1189` へ `:ref:` で導線を張る形にした。**`decide` 候補として上申する**（追記の可否と、`design.md` §8 のどの類型に当たるか）。

### D-9 出典の「作業効率」を落とした

`03_Tips.rst:791` は「可読性や保守性、作業効率といった面で現実的ではない」と書く。`ja/` の追跡下 `.rst` で `作業効率` は1件（`biz_samples/04/0401_ExtendedDataFormatter.rst:178`。同じ出典由来の文）しかなく、`可読性` 10件・`保守性` 8件と比べて定着していないため落とした。判断に必要な内容（現実的ではない理由）は残っている。

## 4. 是正ラウンド1

4観点の独立レビュー（A: 網羅性 / B: トンマナ / C: 用語 / D: 整合性）で確定した指摘への対応を記録する。本文の指摘は10件（F-1〜F-10）、記録の指摘は5件（R-1〜R-5）。是正コミット: `2c9be08`（`ntf-yaml-support` へ push 済み）。

### 4.1 件数と観点

| 区分 | 件数 | 重み別 |
|---|---|---|
| 本文（F-1〜F-10） | 10 | `must` 2件（F-1・F-2）／`should` 6件（F-3・F-4・F-5・F-6・F-7・F-10）／`note` 2件（F-8・F-9） |
| 記録（R-1〜R-5） | 5 | すべて記録の是正（本文への影響なし） |

観点別の内訳（F-1 は A・B・C の3観点が別々の理由で同じ2行を指摘したもの）。

| 観点 | 該当する指摘 | 件数 |
|---|---|---|
| A 網羅性 | F-1・F-3・F-5 | 3 |
| B トンマナ | F-1・F-6・F-8・F-9・F-10 | 5 |
| C 用語 | F-1・F-2・F-7 | 3 |
| D 整合性 | F-4・R-1・R-2・R-3・R-4 | 5 |

### 4.2 各指摘への対応

| # | 重み | 観点 | 指摘 | 対応 | 是正後の位置 |
|---|---|---|---|---|---|
| F-1 | `must` | A・B・C | `:24-26` の `tip` が出典外の追記で、記述方法（第3部の担当）に踏み込み、かつ `データタイプ`＝予約語という `glossary.md:213` の定義と矛盾する | `tip` を削除。適用範囲だけを `important` に集約し、`:17` 3文目の Excel/YAML の書き分けもここへ移した。姉妹ページ `http_messaging.rst:44-46` と同じ形にした | `mom.rst:24-26` |
| F-2 | `must` | C | `メッセージ受信` が `glossary.md` §5.4 の正表記でない（応答不要受信と区別できない） | `同期応答メッセージ受信・応答不要メッセージ受信` に改めた（2箇所）。両方式に効くことを実装で確認済み（4.3 の #1・#2） | `mom.rst:10`・`:17` |
| F-3 | `should` | A | `reader.fwHeaderfields` が既定を**置き換える**ことが書かれておらず、例 `requestId,addHeader` を「追加」と読むと受信テストが壊れる | 「既定のフィールド名に追加されるのではなく、既定のフィールド名をすべて置き換える」「名前を変更していないフィールドも含めて、使用するフィールド名をすべて列挙する」の2文を追加。既定の4件は列挙しない（理由は 4.4） | `mom.rst:17` |
| F-4 | `should` | D | リード文3文目の主語「変換処理」が設定ではないため係り受けが破綻 | 「変換処理の追加は」に改めた。`batch.rst:10` と同じ型になった | `mom.rst:10` |
| F-5 | `should` | A | 出典から3語が落ちていた | 「作業効率」（`03_Tips.rst:791`）・「必要に応じて」（`RequestUnitTest_real.rst:170`）・「動的に」（`RequestUnitTest_real.rst:175`）を戻した。D-9 の判断（作業効率を落とす）は撤回する | `mom.rst:33`・`:35`・`:46` |
| F-6 | `should` | B | 出典の「変換されるのみである」（`03_Tips.rst:789`）の限定が「そのまま」では弱い。`text-encoding` が裸で出ている | 「既定では…変換されるだけである」に改め、`テストデータのディレクティブ`\ ``text-encoding`` と種別を添えた（`:48` の `file-type` と同じ形） | `mom.rst:33` |
| F-7 | `should` | C | `データの形式` はページ内にしかない新語 | `データ形式` に改めた。`git grep` で `データの形式` が `mom.rst:35` の1件のみ、`データ形式` が `about/index.rst:26`・`testdata_notation.rst:555`・`:559`・`:1135` にあることを確認 | `mom.rst:35` |
| F-8 | `note` | B | 「実装する」が3文連続 | F-5・F-7 とあわせて「…を実装する。…必要に応じてアーキテクトが用意する。実装するメソッドは次の2つである。」に整理した | `mom.rst:35` |
| F-9 | `note` | B | 「この例では」の指示対象が曖昧（直前のコードブロックはコンポーネント定義で `file-type` を含まない） | 「登録したコンバータは、``file-type`` に ``FormUrlEncoded`` を指定した電文のテストデータに適用される。」に書き換えた | `mom.rst:56` |
| F-10 | `should` | B | `拡張例` 配下のL3が効果を述べており、手段になっていない | `テストデータの変換処理を実装する` に改題。下線は実測則 `max(49, 表示幅)` を満たす（表示幅32、下線49で変更不要）。リード文2文目「定型的な変換処理を加える」との繋がりを確認した | `mom.rst:31-32` |
| R-1 | — | D | D-1 の根拠2（適用範囲が同一ではない）が実装で否定される | §3 D-1 に取り消し線を引き、「R-1 の訂正」として実装で確認した `file:line` を添えて訂正した。結論（本ページにも書く／`decide` として上申）は変えていない | `reviews` §3 D-1 |
| R-2 | — | D | D-4 の「1つの `:ref:` にした」が実態と異なる（実際は2箇所） | §3 D-4 に取り消し線を引いて訂正。あわせて同一ラベルへの2箇所参照が規約違反でないことを `batch.rst:78,82`・`rest.rst:74,85` の実例で記録した | `reviews` §3 D-4 |
| R-3 | — | D | `checks/task-21.md` の `DataFile.java:88-90` が実際は `:91-92` | `grep -n` で確認して訂正した（`:91` が `prepareDefaultDirectives(DEFAULT_DIRECTIVES)`、`:92` が `setDirective("file-type", getFileType())`）。主張自体は正しい | `checks/task-21.md` §6 |
| R-4 | — | D | 「出典 → ページ」の一方向しか記録がなく、出典外の追記1件が漏れた | `checks/task-21.md` に §1-3「ページ → 典拠（逆方向の全件表）」を追加した。母集合はページの実ファイルから機械的に切り出した11要素（段落6・アドモニション2・コードブロック2・表1） | `checks/task-21.md` §1-3 |
| R-5 | — | — | 是正ラウンドの効果測定用の記録がない | 本節（§4）を追加した | `reviews` §4 |

### 4.3 ラウンド1で新たに実装を確認した項目

参照コミット: `nablarch/nablarch-testing` = `e21bf67`（`main`）、`nablarch/nablarch-testing-yaml` = `a966ab9`（`feature/ntf-yaml`）。いずれもスクラッチパッド配下にクローンして読んだ。リポジトリ直下のビルド残骸 `nablarch/test/core/reader/MessageParser.java`（git の追跡下にない）は使っていない。

| # | 主張 | 確認した `file:line` | 参照コミット |
|---|---|---|---|
| 1 | `reader.fwHeaderfields` は**同期応答メッセージ受信**のテストに効く | `MessagingRequestTestSupport.java:33`（Javadoc「メッセージ同期応答用のテストサポートクラス」）・`:82`（`new MQSupport(testClass)`）→ `MQSupport.java:87` → `BasicTestDataParser.java:82-83` → `MessageParser.java:33`・`:107-110` | `e21bf67` |
| 2 | `reader.fwHeaderfields` は**応答不要メッセージ受信**のテストにも効く | `MessagingReceiveTestSupport.java:8`（Javadoc「メッセージ応答なし受信処理用のテストサポートクラス」）・`:13`（`extends MessagingRequestTestSupport`）・`:42`（`new MQSupport(testClass)`）→ 以降 #1 と同じ経路 | `e21bf67` |
| 3 | `reader.fwHeaderfields` は既定を**追加**するのではなく**置き換える** | `MessageParser.java:107-110`。三項演算子で、キーが未設定または空なら `NablarchTestUtils.asSet("requestId", "userId", "resendFlag", "resultCode")`、設定済みなら `NablarchTestUtils.asSet(NablarchTestUtils.makeArray(...))` を `fwHeaderFields` に代入する。両者の合成は行われない。判定は `isFrameworkHeader`（`:101-103`）が `fwHeaderFields.contains(name)` で行う | `e21bf67` |
| 4 | HTTPメッセージ受信のリクエスト単体テストも同一コードパス・同一設定である（R-1） | `MessagingRequestTestSupport` を継承するクラスは `src/main/java` 全体で `MessagingReceiveTestSupport.java:13` の1件のみ。`TestDataParser#getMessage` の `src/main/java` 内の呼び出し元は `MQSupport.java:87` のみ（`DbLessTestDataParser.java:55-56` は委譲）。`MQSupport` の生成は `MessagingRequestTestSupport.java:82`・`MessagingReceiveTestSupport.java:42` の2箇所のみ | `e21bf67` |
| 5 | `defaultDirectives` の適用後に `file-type` が上書きされる（R-3 の行番号訂正） | `DataFile.java:91`（`prepareDefaultDirectives(DEFAULT_DIRECTIVES)`）・`:92`（`setDirective("file-type", getFileType())`）。`prepareDefaultDirectives` の本体は `:68-81` | `e21bf67` |

### 4.4 F-3 で既定の4件を列挙しなかった理由

`reader.fwHeaderfields` の既定値（`requestId`・`userId`・`resendFlag`・`resultCode`）は、承認済みの `implementation/testdata_notation.rst:1137` が既に列挙している。本ページ `:17` の同じ文の中に `:ref:`フレームワーク制御ヘッダのフィールド名 `<testdata_notation-messaging_data>`` があり、そのラベル（`testdata_notation.rst:1115`）の節が `:1137` を含む。読者は同じ文からたどれる。

「置き換えである」という危険は、値の一覧ではなく**演算の性質**を書けば防げる。是正後の2文（追加ではなく置き換えであること／変更していないフィールドも含めて全部書くこと）はこの性質を述べており、既定値の一覧に依存しない。既定値を本ページにも書くと、`#19` 申し送り5 と D-1 が問題にしている「同じ既定値が3ページに並ぶ」状態をさらに広げることになるため、列挙しない。

### 4.5 `decide` 候補（本タスクでは手を付けていない）

以下4件は、コーディネータがユーザーに上申する。**本文・`glossary.md`・`testdata_notation.rst`・`design.md` のいずれも変更していない。**

| # | 論点 | 現状 | 選択肢 |
|---|---|---|---|
| 1 | `reader.fwHeaderfields` の記述が `http_messaging.rst` と重複している。R-1 で**適用範囲も同一**（同一コードパス・同一設定）と確定したため、重複を残す積極的な理由は消えた | `setup/request_unit_test/http_messaging.rst:35-46` と `setup/request_unit_test/mom.rst:15-26` に、同じキー・同じコード例・ほぼ同じ `important` が並ぶ | (a) `setup/common.rst` に寄せて両ページから `:ref:` する／(b) `http_messaging.rst` に寄せて `mom.rst` から `:ref:` する／(c) 現状維持（各ページで自己完結）。作成側の推奨は (a)。両ページとも第2部で唯一必須の `使用方法` が実質1項目になるため、(b) は `mom.rst` の `使用方法` を空にする |
| 2 | 承認済み `implementation/testdata_notation.rst:1244` が実装および同ファイル `:1263` と矛盾している | `:1244`「（`fw_header:` の）キー名は固定ではなく、``reader.fwHeaderfields`` の設定に合わせる」。`:1263`「``fw_header:`` に記載したキーは全てフレームワーク制御ヘッダとして扱われ、``reader.fwHeaderfields`` でフィルタして取り捨てられることはない」。実装は `:1263` 側（`nablarch-testing-yaml` の追跡下 `src/main/java` に `fwHeaderfields` の参照0件、`a966ab9`） | (a) `:1244` の当該1文を削除／(b) `:1244` を `:1263` に合わせて書き換え／(c) 承認済みのため触らない。`#19` 申し送り4・7 が既に記録済み |
| 3 | `mom.rst:60` の `tip`（`file-type` がアサート方式にも影響する旨）の扱いと、`design.md` §8 への類型追加 | 出典・マッピングのいずれにも無い追記（D-8）。`design.md` §8 の4類型（確定設計優先／実装優先／デフォルト値の基準／実装上必須の設定）のどれにも厳密には当たらない。実装上は `MessagePool.java:54`・`:154-163` で裏付けられる | (a) `tip` を残し、`design.md` §8 に「手順どおり設定すると別の挙動が変わる場合の注意喚起」の類型を追加／(b) `tip` を削除して第3部だけに置く／(c) 現状維持（類型は未整理のまま） |
| 4 | `glossary.md` の行追加・是正3件 | (i) `環境設定ファイル` の項が無い。`mom.rst:17`・`common.rst`・`http_messaging.rst:37` が使っている語で、`コンポーネント設定ファイル`（§5.12 にある）との使い分けが用語集から引けない。(ii) §8 対応表に `TestDataConvertor` → `TestDataConverter` の置換行が無い（出典の見出しが誤っており、§2 食い違い1 で実装優先とした）。(iii) `デフォルト値` と `既定値` が揺れている（`glossary.md:408` は `デフォルト値` を掲載語として挙げるが、作成済みページの本文は `既定値`／`既定` を使う。`design.md:440` の節題は「デフォルト値の基準」） | (a) 3件とも `glossary.md` に反映／(b) (i)(ii) のみ反映し (iii) は `#last` へ／(c) すべて `#last` へ |

**あわせて申し送る（新たに気づいた問題）**:

1. **F-1 で `important` に残した「同期応答メッセージ送信のテストでは、この設定は使用されない」も、出典・マッピングのいずれにも無い追記である。** 実装で裏付けられる（`SendSyncMessageParser.java:35-44` が `getFwHeader()` で `UnsupportedOperationException`、`GroupMessageParser.java:58` が `Collections.emptyMap()`）が、`design.md` §8 の類型としては上記 `decide` 3 と同じ位置にある。`decide` 3 の判断は本件にも及ぶ。
2. **F-10 の指示にあった前例2件が、ディスク上の実態と一致しない。** 作業指示は「`拡張例` を持つ既存2ページは手段を見出しにしている（`class_unit_test.rst:91`「バリデーションのテスト方法を差し替える」、`web.rst:113`「テストクラスの共通処理を差し替える」）」としているが、`ja/development_tools/testing_framework/` 配下で `^拡張例$` を持つページは `setup/request_unit_test/web.rst:222` と本ページの2件のみで、`class_unit_test.rst` は `拡張例` の見出しを持たない。`web.rst` の `拡張例` 配下のL3は `:225`「テストデータの書き方を拡張する」であり、指示が挙げた文言とは異なる（`差し替える` で終わる見出しは同配下に0件）。**改題そのものは妥当**（`web.rst:225` も手段形であり、`design.md:198` が「拡張例では手順として記載する」と定めている）ため指示どおり実施したが、前例の記述は訂正が必要である。

## 5. 是正ラウンド2

### 5.1 ラウンド2で回した検証と結果

| 検証 | 結果 |
|---|---|
| 是正差分の範囲検証（ラウンド1の是正コミット `2c9be08` が指摘の範囲に収まっているか） | **PASS**。`must` 0件 |
| 新規記述のファクトチェック（ラウンド1で新たに書き足した記述を実装と突き合わせる） | **不一致1件**（`mom.rst:46` の `createDefinition` の説明。下記 是正1） |

これに加えて、ラウンド2の2本のレビューがともに `mom.rst:21` のコメント行を指摘した（`should`。下記 是正2）。是正はこの2箇所のみで、本文の他の行・`design.md`・`mapping/` 配下・`ja/` の他ファイルには手を付けていない。

### 5.2 是正の対応と根拠

参照コミット: `nablarch/nablarch-testing` = `e21bf67`。本節の `file:line` は作業ツリー（`fdf55d4`）で確認したが、`src/main/java/nablarch/test/core/messaging/`・`.../http/`・`NablarchTestUtils.java`・`TestDataConverter.java` は `git diff --stat e21bf67 HEAD` が空で、`e21bf67` と同一である（差分があるのは `core/reader/` の4ファイルのみで、うち `MessageParser.java` は含まれない）。

| # | 重み | 対象 | 是正前 | 是正後 | 根拠（`file:line`） |
|---|---|---|---|---|---|
| 是正1 | `must` | `mom.rst:46`（`list-table` の `createDefinition` のセル） | 変換後のデータを**読み込むための**レイアウト定義を動的に生成する | 変換後のデータに**対応する**レイアウト定義を動的に生成する | 返されるレイアウト定義は**書き出しと読み込みの双方に使われる**ため、方向を限定しない Javadoc の表現に合わせた。書き出しは `MessagePool.java:122`（`convertByFileType`）→ `:124`（`createLayoutFromDataRecord`。実体は `:252-254` の `source.createDefinition(...)`）→ `:130`（`msg.setFormatter(formatter.setDefinition(ld)).addRecord(currentData)`）で、`RequestTestingMessagePool.java:87-96` も同型（`SendingMessage` でバイナリ化して `getBodyBytes()`）。読み込みは `MessagePool.java:148-152` で得た同じ `ld` を `:165`（`responseMessage.setFormatter(formatter.setDefinition(ld)).readRecords()`）に渡す経路である。`TestDataConverter.java:20` の Javadoc も「対応した」で方向を限定していない。**`/rn:ty`（`#21` 承認、2026-08-13）`should` 3 による根拠の是正。是正の結論（本文の文言）は変わらない** |
| 是正2 | `should` | `mom.rst:21`（コードブロック内のコメント行） | `# フレームワーク制御ヘッダのフィールド名をカンマ区切りで指定する。` | `# 使用するフレームワーク制御ヘッダのフィールド名を、すべてカンマ区切りで列挙する。` | ラウンド1・F-3 で `:17` に「名前を変更していないフィールドも含めて、使用するフィールド名をすべて列挙する」を加えた結果、直後の例が「すべて列挙」の実例に見えなくなっていた（`requestId,addHeader` は既定の `userId`・`resendFlag`・`resultCode` が消える設定）。実装の裏付けは `MessageParser.java:107-110`（三項演算子で既定と設定値を合成せず置き換える）・`:101-103` |

**値 `reader.fwHeaderfields=requestId,addHeader`（`mom.rst:22`）は変更していない。** 出典（`real.rst:175`）そのものである。是正1 は `design.md` §8「出典と実装が食い違う場合は実装を優先する」の適用であり、§2 の「出典と実装が食い違った点」に**4件目**として追加した。

### 5.3 申し送り（本タスクでは是正しない）

1. **`NablarchTestUtils.makeArray` はカンマ分割のみでトリムしない。** `src/main/java/nablarch/test/NablarchTestUtils.java:45-49` が本体で、`null`／空文字列なら長さ0の配列、それ以外は `COMMA.split(str)` を返す。`COMMA` は同ファイル `:36` の `Pattern.compile(",")` で、空白の除去はどこにも無い。`MessageParser.java:110` はこの結果をそのまま `NablarchTestUtils.asSet(...)` に渡し、判定は `:103` の `fwHeaderFields.contains(name)` である。したがって `reader.fwHeaderfields=requestId, addHeader` のように空白を入れると `" addHeader"` という先頭に空白を含むフィールド名になり、`contains` が一致せず**無言で失敗する**（例外も警告も出ない）。本ページは空白を入れない例しか示しておらず、注意喚起も無い。
2. **承認済み `ja/development_tools/testing_framework/setup/request_unit_test/http_messaging.rst:37` には、`reader.fwHeaderfields` が既定を置き換えるという記述が無い。** 本ページ `mom.rst:17` はラウンド1・F-3 で「追加ではなく置き換え」「使用するフィールド名をすべて列挙する」の2文を持つ。同じ実装（`MessageParser.java:107-110`）を指しているのに、記述の深度が2ページで非対称になった。`decide` 1（重複の寄せ先）と同じ範囲の問題であり、寄せ方を決める際に併せて解消する必要がある。
3. **未確認の論点: `reader.fwHeaderfields` が HTTPメッセージング受信のテストに実際に効くかどうか。** ラウンド2のレビュアー間で判断が割れており、**本タスクでは確定していない**。両論と、それぞれが挙げた根拠だけを記す。

   | 立場 | 主張 | 挙げられた根拠（`file:line`） |
   |---|---|---|
   | A（効く） | HTTPメッセージング受信のリクエスト単体テストも `MessagingRequestTestSupport` を使うため、MOM と同一経路である | `MessagingRequestTestSupport.java:82`（`new MQSupport(testClass)`）→ `MQSupport.java:87`（`getTestDataParser().getMessage(...)`）→ `BasicTestDataParser.java:82-85`（`new MessageParser(...)`）→ `MessageParser.java:33`・`:107-110`。`MessagingRequestTestSupport` を継承するのは `MessagingReceiveTestSupport.java:13` の1件のみ（ラウンド1・§4.3 #4） |
   | B（効かない可能性） | `nablarch/test/core/http/` 配下から `getMessage` を呼ぶ経路が見当たらない | `src/main/java/nablarch/test/core/http/` の10ファイル（`AbstractHttpRequestTestTemplate.java`・`BasicHttpRequestTestTemplate.java`・`HttpRequestTestSupport.java` ほか）に `getMessage(` の出現0件。`TestDataParser#getMessage` の呼び出し元は `MQSupport.java:87` のみで、`DbLessTestDataParser.java:55-56` は委譲 |

   両者が挙げた `file:line` は**いずれも実物で再確認して存在する**（`e21bf67` と同一の作業ツリーで確認）。争点は「HTTPメッセージング受信のテストが `MessagingRequestTestSupport`／`MQSupport` を経由するか」であり、この一点の確認が済んでいない。**推測で結論を書かない。** 本ページ `mom.rst` は MOM のページであり、この論点の結論に関わらず記述は変わらないが、`decide` 1（`http_messaging.rst` との重複の寄せ先）の判断には影響する。

## 6. user review（`/rn:ty` 承認）後の反映

2026-08-13 の `/rn:ty` で公開本文が承認され、`decide` 5件の回答と `should` 3件が示された。本節はその反映結果を記録する。参照コミットは `nablarch/nablarch-testing` = `e21bf67`（本節が引く4ファイルは作業ツリー `fdf55d4` との `git diff` が空で `e21bf67` と同一）、`nablarch/nablarch-document` の出典 = `c2419060`。

### 6.1 `decide` の回答と反映先

| # | 回答 | 反映先 |
|---|---|---|
| 1 | **(c) 現状維持。** `reader.fwHeaderfields` は `http_messaging.rst` と `mom.rst` の両方に置く。集約しない | 本文の変更なし。非対称の解消は `should` 1 で実施 |
| 2 | **是正する。** `implementation/testdata_notation.rst:1244` の1行 | `:1244` を「キー名は固定ではなく、プロジェクトが使用するフレームワーク制御ヘッダのフィールド名を記載する。」に差し替え |
| 3 | **(a) 2件とも残す。** `design.md` §8 に類型を1つ追加 | `design.md` §8 に「出典が書いていない適用範囲・副作用の追記」を追加。本文の変更なし |
| 4 | **(i)(ii)(iii) の3件とも反映** | `glossary.md` §5.12 に1行・§5.14 に1行・§8 に3行。`ja/` 4ファイルの `既定`→`デフォルト` 置換26箇所 |
| 5 | **いま確定させる。`reader.fwHeaderfields` は HTTPメッセージング受信のテストにも効く** | `http_messaging.rst:37-42` は正しい。§5.3 申し送り3 を閉じる（下記 6.3） |

`decide` 1 の判断根拠は、この設定を読む経路が `MessageParser` だけであり、そこへ至るのが `MQSupport.java:87` の1箇所、`MQSupport` を生成するのが `MessagingRequestTestSupport.java:82` と `MessagingReceiveTestSupport.java:42` の2箇所だけであること（`src/main/java` 全走査）。**メッセージング受信のテストに紐づいており、ウェブ・バッチ・RESTful・クラス単体のテストには効かない。** `setup/common.rst`（全テストに共通する設定を置くページ。`common.rst:10`・`S:design.md:153`）へ移すと、読者に「共通設定なので自分のテストにも効く」と読ませることになる。

### 6.2 `should` の反映

| # | 対象 | 内容 | 根拠（`file:line`） |
|---|---|---|---|
| 1 | `http_messaging.rst:37`・`:41` | `mom.rst:17` と同じ2文（「デフォルトのフィールド名に追加されるのではなく、すべて置き換える」「使用するフィールド名をすべて列挙する」）を追加し、コードブロックのコメントを `mom.rst:21` と同文にした | `MessageParser.java:107-110`（三項演算子。未設定ならデフォルト4件の `Set`、設定済みなら設定値だけの `Set` を代入し、合成しない）・`:109`（デフォルトは `requestId`・`userId`・`resendFlag`・`resultCode`） |
| 2 | `mom.rst:17`・`http_messaging.rst:37` | 「値に空白を含めると、空白も含めてフィールド名として扱われるため、カンマの前後に空白を入れない。」を両ページの同じ位置に追加した | `NablarchTestUtils.java:36`（`COMMA = Pattern.compile(",")`）・`:45-49`（`makeArray` は `COMMA.split(str)` をそのまま返し、トリムしない）。判定は `MessageParser.java:103` の `fwHeaderFields.contains(name)` で、`reader.fwHeaderfields=requestId, addHeader` と書くと `" addHeader"` というフィールド名になり一致しない。いずれも実物で確認済み |
| 3 | 本記録 §2 食い違い4・§5.2 是正1 | 「書き出しにのみ使われる」を「書き出しと読み込みの双方に使われる」に是正した。**是正の結論（公開本文の文言）は変わらない** | `MessagePool.java:148-152`（読み込み経路でも同じ手順で `ld` を得る）→ `:165`（`responseMessage.setFormatter(formatter.setDefinition(ld)).readRecords()`）。実物で確認済み |

`should` 1・2 の追記は、`design.md` §8 に新設した類型「出典が書いていない適用範囲・副作用の追記」の適用である。

### 6.3 §5.3 申し送り3 の決着 — `reader.fwHeaderfields` は HTTPメッセージング受信のテストにも効く

立場A（効く）が正しい。決め手は、ラウンド2のレビュアーA・Bのいずれも挙げていなかった次の一次情報である。

- HTTPメッセージング受信のテストデータの識別子行は `MESSAGE=setUpMessages`（応答側は `MESSAGE=expectedMessages`）で固定である（`c2419060:ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/http_real.rst:56`・`:105`・`:168`）
- この2つのIDを読む経路は `MQSupport.java:73-74`・`:63-64`（`getMessages(sheetName, "setUpMessages")`／`getMessages(sheetName, "expectedMessages")`）の1つだけであり、そこから `BasicTestDataParser.java:82-85` の `new MessageParser(..., DataType.MESSAGE)` に至る。したがって HTTPメッセージング受信のテストデータは必ず `MessageParser` が解析する
- `http_real.rst:63` は、共通情報の行に `requestId` をキーとして書く例をそのまま載せている。この行がフレームワーク制御ヘッダとして扱われるのは `MessageParser.java:102-103` の `fwHeaderFields.contains("requestId")` が真だからであり、`reader.fwHeaderfields` でこの名前を落とせば同じ行はフィールド名称行として扱われる（`DataFileParser.java:140-143`）

立場Bの「`nablarch/test/core/http/` から `getMessage` を呼ぶ経路が無い」は事実だが結論には効かない。HTTPメッセージング受信のテストは `nablarch.test.core.http` のクラスではなく `MessagingRequestTestSupport` を使う（`http_real.rst:5` が `real_request_test` に委ね、`real.rst:15` がそのクラスを指定する）。**適用範囲は MOM と同一であり、承認済み `http_messaging.rst:37` の記述は正しい。**

**残る申し送り**: `real.rst:15` はこのクラスのパッケージ名を `nablarch.test.core.http` と書いているが、実体は `nablarch.test.core.messaging` である。`design.md` §8「実装優先」に従い、**第3部「リクエスト単体テスト（MOMによるメッセージング）」を書くタスク（`current-0295`〜`0301`）で是正する。** 本タスクでは何もしない。

### 6.4 §5.3 申し送り1・2 の決着

- 申し送り1（空白を入れると無言で失敗する）→ `should` 2 で両ページに1文を追加。**閉じた**
- 申し送り2（`http_messaging.rst` に「置き換えである」旨が無い非対称）→ `should` 1 で解消。**閉じた**

## 7. `#28` §6-2-1・6-2-2 の追記（実装上必須の設定）

`design.md` §8「出典が欠いている、実装上必須の設定の追記」の適用。**反映コミット `b29b68d`**。根拠はすべて `nablarch/nablarch-testing` の作業ツリー `fdf55d4` を自分で開いて確認した。

### 7.1 §6-2-1 メッセージ受信用のメッセージングプロバイダを登録する

| 本文に書いた事実 | 根拠（`file:line`） |
|---|---|
| コンポーネント名は `messagingProvider` 固定。別名で登録すると実行時に例外 | `MessagingRequestTestSupport.java:108-109`（`ConfigurationBrowser.require(diConfig, "messagingProvider", false)`）→ `repository/ConfigurationBrowser.java:49-56`（取得できない場合 `IllegalArgumentException`） |
| 取得元はテストショット一覧の `diConfig` に指定した設定ファイル | `MessagingRequestTestSupport.java:107`（`testShot.getDiConfig()` を `require` の第1引数に渡す） |
| キュー名は要求電文 `TEST.REQUEST`・応答電文 `TEST.RESPONSE` の固定で変更できない | `MessagingRequestTestSupport.java:185-186`（`setDestination("TEST.REQUEST").setReplyTo("TEST.RESPONSE")`）・`:197`（`receiveSync("TEST.RESPONSE", 10000)`）。いずれもリテラル |
| 内蔵のメッセージングサーバを使う（外部MOM不要） | `MessagingRequestTestSupport.java:96-97`（`afterExecuteTestShot` が無条件に `EmbeddedMessagingProvider.stopServer()` を呼ぶ）・`EmbeddedMessagingProvider.java:33`（`JmsMessagingProvider` を継承し、`Server` を内蔵） |
| `queueNames` にリストで指定する | `EmbeddedMessagingProvider.java:86`（`setQueueNames(List<String> names)`） |

### 7.2 §6-2-2 同期応答メッセージ送信用のメッセージングプロバイダに差し替える

| 本文に書いた事実 | 根拠（`file:line`） |
|---|---|
| 要求電文のアサートと応答電文の返却は `RequestTestingMessagingProvider` が行う | `RequestTestingMessagingProvider.java:130`（`sendSync`）・`:149`（`SENDING_MESSAGE_CACHE.add(message)`）・`:230`（`assertSendingMessage`） |
| 差し替えないと期待値との照合が成立しない | `TestShot.java:167` が `RequestTestingMessagingContext.assertSendingMessage(..., get("expectedMessage"))` を無条件に呼ぶ。キャッシュが空だと `RequestTestingMessagingProvider.java:331-338` の件数不一致で `Assertion.fail` |
| コンポーネント名は `messageSender.<リクエストID>.messagingProviderName`（未指定時は `messageSender.DEFAULT.messagingProviderName`）に合わせる | 既存の承認済み本文 `setup/deal_unit_test/mom.rst:29` と同一の記述に揃えた |
