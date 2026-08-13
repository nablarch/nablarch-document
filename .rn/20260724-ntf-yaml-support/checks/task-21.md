# task-21 Completion Check

対象: `ja/development_tools/testing_framework/setup/request_unit_test/mom.rst`（第2部「リクエスト単体テストの設定（MOMによるメッセージング）」・新規作成）

着手時の HEAD: `67bdafc`。作業ツリーは着手時点でクリーン。本文コミット: `8b956cd`（`ntf-yaml-support` へ push 済み）。

**是正ラウンド1を実施した（HEAD `8b956cd` に対する差分）。** 本文の指摘10件（F-1〜F-10）と記録の指摘5件（R-1〜R-5）に対応した。行番号は**是正後**のものに更新してある。指摘ごとの対応は `reviews/page-request_unit_test_setting_mom.md` §4 を参照。

## §1 マッピング全件の反映対応表（母集合を先に固定。ホワイトリストで切り出さない）

母集合は `mapping.csv` の**全595行**を `csv.DictReader` で読み、`dest_page` が
`リクエスト単体テストの設定（MOMによるメッセージング）` に**完全一致**する行を抽出した（`wc -l` は使っていない）。
抽出条件に `mapping_id` の列挙は使っていない。

```
$ python3 -c "
import csv
rows=[r for r in csv.DictReader(open('.rn/20260724-ntf-yaml-support/mapping/mapping.csv'))]
t=[r for r in rows if r['dest_page']=='リクエスト単体テストの設定（MOMによるメッセージング）']
print('all',len(rows),'target',len(t),'DROP',len([r for r in t if r['disposition']=='DROP']),'lines',sum(int(r['lines']) for r in t))
"
all 595 target 8 DROP 0 lines 76
```

抽出結果は**8行**（`DROP` 0件・計 76 lines）。8行すべてが下表に現れる。

| `mapping_id` | 出典（`src_file` の行範囲） | `lines` | `disposition` | 反映先セクション | 反映した内容と反映先の行 |
|---|---|---|---|---|---|
| `current-0106-b` | `05_UnitTestGuide/02_RequestUnitTest/real.rst` 167–177 | 11 | SPLIT | 使用方法 > フレームワーク制御ヘッダのフィールド名を指定する | フレームワーク制御ヘッダの項目を変更している場合に `reader.fwHeaderfields` でフィールド名をカンマ区切りで指定する手順と、そのコード例（`mom.rst:15-22`）。適用範囲（同期応答メッセージ受信・応答不要メッセージ受信）は `:17`、形式と対象外の方式は `:24-26` の `important` |
| `current-0247` | `06_TestFWGuide/03_Tips.rst` 788–794 | 7 | MERGE | 拡張例 > テストデータの変換処理を実装する | 「テストデータの値は指定エンコーディングでバイト列に変換されるのみ」「URLエンコード済みの値を書くのは可読性・保守性の面で現実的ではない」という課題と、「インタフェースを実装して登録すれば定型的な変換処理を追加できる」という解決（`mom.rst:33`） |
| `current-0248` | `06_TestFWGuide/03_Tips.rst` 797–799 | 3 | MERGE | 拡張例 > テストデータの変換処理を実装する | 実装対象が `nablarch.test.core.file.TestDataConverter` であること（`mom.rst:35` の `:java:extdoc:`） |
| `current-0249` | `06_TestFWGuide/03_Tips.rst` 802–809 | 8 | MERGE | 拡張例 > テストデータの変換処理を実装する | 登録キー名が `TestDataConverter_<データ種別>` であること、データ種別がテストデータの `file-type` に指定した値であること（`mom.rst:48`）。出典は2行の simple table だが、キーと値の対が1組のみのため表を置かず地の文にした（`style.md` S-07 の趣旨・`#20` の同型判断） |
| `current-0250` | `06_TestFWGuide/03_Tips.rst` 812–818 | 7 | MERGE | 拡張例 > テストデータの変換処理を実装する | `TestDataConverter_FormUrlEncoded` のコンポーネント定義例（`mom.rst:50-54`）。クラスの完全修飾名は `com.example` に変更（判断3・`reviews` D-3） |
| `current-0251` | `06_TestFWGuide/03_Tips.rst` 821–832 | 12 | MERGE | 拡張例 > テストデータの変換処理を実装する | 変換前後の対応。画像2枚は載せず、事実を地の文に残した（`mom.rst:56`。判断2・`reviews` D-2） |
| `current-0303` | `06_TestFWGuide/RequestUnitTest_real.rst` 168–181 | 14 | MOVE | 拡張例 > テストデータの変換処理を実装する | インタフェースの位置づけ（テストデータを編集するためのインタフェース）・データ種別ごとにアーキテクトが実装すること（`mom.rst:35`）・実装する2機能（`mom.rst:37-46` の表）・テスト用のコンポーネント設定ファイルへの登録（`mom.rst:48`） |
| `current-0328` | `06_TestFWGuide/RequestUnitTest_send_sync.rst` 127–140 | 14 | MOVE | 拡張例 > テストデータの変換処理を実装する | `current-0303` とほぼ同文。同じ L3 セクションに統合した（Acceptance criteria「重複がない。参照で解決する」） |

反映漏れ**0件**。出典の実物は、現行解説書が本ブランチで削除済みのため `git show c241906:<src_file>` で読んだ。
`note` 欄の説明文は根拠にしていない。

### §1-2 出典の各要素とページ内の対応（落としていないことの確認）

| 出典の要素 | 出典の `file:line` | ページでの扱い |
|---|---|---|
| フレームワーク制御ヘッダの項目をPJで変更している場合の設定が必要な旨 | `real.rst:169-170` | `mom.rst:17` |
| `reader.fwHeaderfields=requestId,addHeader` の properties 例 | `real.rst:172-175` | `mom.rst:19-22` |
| Excelのデータは指定エンコーディングでバイト列に変換される**のみ**である | `03_Tips.rst:789` | `mom.rst:33`（「変換されるだけである」。`text-encoding` は「テストデータのディレクティブ」と種別を添えて名指しした。`DataFile.java:300-302`。ラウンド1・F-6） |
| URLエンコード済みの値をExcelに書くのは可読性・保守性・**作業効率**の面で非現実的 | `03_Tips.rst:790-791` | `mom.rst:33`（ラウンド1・F-5 で「作業効率」を戻した。`reviews` D-9 の判断は撤回） |
| インタフェース実装＋リポジトリ登録で変換処理を追加できる | `03_Tips.rst:793` | `mom.rst:33` 末尾・`:35`・`:48` |
| 実装するインタフェース `nablarch.test.core.file.TestDataConverter` | `03_Tips.rst:798` | `mom.rst:35` |
| 登録キー `TestDataConverter_<データ種別>` と「データ種別はテストデータのfile-typeに指定した値」 | `03_Tips.rst:803-808` | `mom.rst:48` |
| コンポーネント定義のXML例 | `03_Tips.rst:813-817` | `mom.rst:50-54` |
| 変換前のExcel記述例（画像） | `03_Tips.rst:822` | 画像・セル格子の表とも置かない。`file-type` の値がコンポーネント名と対応する事実は `mom.rst:56` 前半（`reviews` D-2） |
| 「コンバータでURLエンコーディングを行うように実装した場合、内部では以下のデータを記述した場合と同様に扱われる」 | `03_Tips.rst:824-825` | `mom.rst:56` 後半 |
| 変換後のデータ（画像） | `03_Tips.rst:827` | 同上。地の文に残した（`reviews` D-2） |
| Excelから読み込んだテストデータを編集するためのインタフェース | `RequestUnitTest_real.rst:169`／`send_sync.rst:128` | `mom.rst:33` 末尾・`:35`。形式には触れない書き方にした（`reviews` §2 食い違い2） |
| **必要に応じて**XMLやJSONなどのデータ種別ごとにアーキテクトが実装する | `RequestUnitTest_real.rst:170`／`send_sync.rst:129` | `mom.rst:35`（ラウンド1・F-5 で「必要に応じて」を戻した） |
| 実装クラスが担う2機能の箇条書き（レイアウト定義データを**動的に**生成する） | `RequestUnitTest_real.rst:174-175`／`send_sync.rst:133-134` | `mom.rst:37-46`（`list-table`）。ラウンド1・F-5 で `:46` に「動的に」を戻した |
| Excelの日本語データをURLエンコーディングする等の処理を追加できる | `RequestUnitTest_real.rst:177`／`send_sync.rst:136` | `mom.rst:56` |
| `"TestDataConverter_<データ種別>"` というキー名でテスト用のコンポーネント設定ファイルに登録する | `RequestUnitTest_real.rst:179`／`send_sync.rst:138` | `mom.rst:48` |

**出典で落とした表現は0件**（ラウンド1・F-5 で「作業効率」「必要に応じて」「動的に」の3語を戻したため）。事実の欠落も0件。

### §1-3 ページ → 典拠（逆方向の全件表。ラウンド1・R-4 で追加）

§1・§1-2 は「出典 → ページ」の一方向しかなく、**出典に無い追記がページ側に残っても検出できない**。実際、旧 `:24-26` の `tip` はこの表が無かったために記録から漏れた（ラウンド1・F-1 で削除）。逆方向の表を追加する。

**母集合はページの実ファイルから機械的に切り出した。** ホワイトリストで選んでいない。切り出しは次のスクリプトで行い、`ラベル`・`見出し`・`ディレクティブ`・`段落` の4種にすべての非空行を分類した。

```
$ python3 - <<'EOF'
import re
L=open('ja/development_tools/testing_framework/setup/request_unit_test/mom.rst').read().split('\n')
i=0; n=len(L)
while i<n:
    if not L[i].strip(): i+=1; continue
    if i+1<n and re.fullmatch(r'[=~^-]{4,}', L[i+1].strip()):
        print('見出し', i+1, L[i]); i+=2; continue
    if L[i].startswith('.. _'): print('ラベル', i+1, L[i]); i+=1; continue
    m=re.match(r'\.\. (\w[\w-]*)::', L[i])
    if m:
        st=i+1; i+=1
        while i<n and (not L[i].strip() or L[i].startswith(' ')): i+=1
        print(f'ディレクティブ {m.group(1)}', st, i); continue
    st=i
    while i<n and L[i].strip() and not re.match(r'\.\. ',L[i]) and not (i+1<n and re.fullmatch(r'[=~^-]{4,}', L[i+1].strip())): i+=1
    print('段落', st+1, i)
EOF
```

切り出し結果は**18要素**。うち作業指示が母集合と定めた4種（段落・アドモニション・コードブロック・表）は**11要素**（段落6・アドモニション2・コードブロック2・表1）で、残る7要素は構造要素（ラベル1・見出し5・`contents` 1）である。**11要素すべてが下表に現れる。**

| # | 種別 | 行 | 先頭 | 典拠 |
|---|---|---|---|---|
| 1 | 段落（リード文） | `:10` | MOMによるメッセージングのリクエスト単体テストでは… | 1文目 `current-0106-b`（`real.rst:169-170`）。「同期応答メッセージ受信・応答不要メッセージ受信」の限定は実装（`MessagingRequestTestSupport.java:33,82`・`MessagingReceiveTestSupport.java:8,13,42` → `MQSupport.java:87`）と `glossary.md` §5.4 の正表記。2文目 `current-0247`（`03_Tips.rst:793`）。3文目は本ページ本文の要約で、適用範囲は実装（`MessagePool.java:244`・`:253` の呼び出し元が電文経路のみ）。リード文を置くこと自体は `style.md` S-02、型は `batch.rst:10` |
| 2 | 段落 | `:17` | 同期応答メッセージ受信・応答不要メッセージ受信のテストで… | 1文目 `current-0106-b`（`real.rst:169-170`）。2文目・3文目（既定を置き換えること）は `design.md` §8「出典が欠いている、実装上必須の設定の追記」（`design.md:465-473`）。出典の例 `requestId,addHeader` をそのまま「追加」と読むと `userId`・`resendFlag`・`resultCode` が落ち、出典の手順どおりに設定した読者の受信テストが壊れる。実装は `MessageParser.java:107-110`・`:101-103` |
| 3 | コードブロック `properties` | `:19-22` | `reader.fwHeaderfields=requestId,addHeader` | 設定行 `:22` は `current-0106-b`（`real.rst:175`）そのもの（**未変更**）。コメント行 `:21` は出典（`real.rst:174`「フレームワーク制御ヘッダ名をカンマ区切りで指定する。」）を、直前の `:17` が求める「すべて列挙する」の実例として読めるよう「使用するフレームワーク制御ヘッダのフィールド名を、すべてカンマ区切りで列挙する。」に改めた（**ラウンド2・是正2**）。根拠は実装（`MessageParser.java:107-110` の三項演算子が既定と設定値を合成せず置き換える） |
| 4 | アドモニション `important` | `:24-26` | この設定が必要なのは、Excel 形式の… | 1・2文目（Excel／YAML の書き分け）は `style.md` S-10 規約1（形式の対応関係そのものを理解しないと概念が掴めないもの）と実装（`nablarch-testing-yaml` の追跡下 `src/main/java` に `fwHeaderfields` の参照0件、`a966ab9`）。承認済み `testdata_notation.rst:1263` および `http_messaging.rst:44-46` と同じ事実。3文目（同期応答メッセージ送信では使用されない）は実装（`SendSyncMessageParser.java:35-44` の `UnsupportedOperationException`、`GroupMessageParser.java:58` の `Collections.emptyMap()`）。**`design.md` §8 の4類型のいずれにも厳密には当たらない適用範囲の注記であり、`reviews` §4.5 の申し送り1 として上申する** |
| 5 | 段落 | `:33` | 電文のテストデータに記述した値は、既定では… | `current-0247`（`03_Tips.rst:789`・`:790-791`・`:793`）。`text-encoding` の名指しは実装（`DataFile.java:300-302`・`FixedLengthFile.java:131`・`:147`）。「テストデータのディレクティブ」の種別付けは `:48` の `file-type` に揃えた（ラウンド1・F-6） |
| 6 | 段落 | `:35` | 拡張するには TestDataConverter を実装する… | `current-0248`（`03_Tips.rst:798`）＋ `current-0303`（`RequestUnitTest_real.rst:169-170`）／`current-0328`（`send_sync.rst:128-129`）。インタフェース名は実装優先（`TestDataConverter.java:17`。`reviews` §2 食い違い1）。`データ形式` の語は既存ページに合わせた（`about/index.rst:26`・`testdata_notation.rst:555`・`:559`・`:1135`。ラウンド1・F-7） |
| 7 | 表 `list-table` | `:37-46` | メソッド／実装する内容 | `current-0303`（`RequestUnitTest_real.rst:174-175`）／`current-0328`（`send_sync.rst:133-134`）。メソッド名は実装（`TestDataConverter.java:27`・`:37`）。記法は `style.md` S-07（セルにコードリテラルと日本語が混在するため `list-table`）。**`createDefinition` のセル `:46` は出典の「編集したデータを読み込むためのレイアウト定義データを動的に生成する」（`RequestUnitTest_real.rst:175`・`send_sync.rst:134`）が実装と食い違うため、「変換後のデータに対応するレイアウト定義を動的に生成する」に改めた**（**ラウンド2・是正1**。`design.md` §8「出典と実装が食い違う場合は実装を優先する」。`reviews` §2 食い違い4）。実装は `MessagePool.java:122-130`（`convertByFileType` → `createLayoutFromDataRecord` → `setFormatter(...).addRecord(...)` で書き出しにのみ使う）・`RequestTestingMessagePool.java:87-96`（同じく書き出し）・`TestDataConverter.java:20`（Javadoc「現在処理中のテストデータに対応したレイアウト定義データを生成します」で方向を限定していない） |
| 8 | 段落 | `:48` | 実装したクラスは、テスト用のコンポーネント設定ファイルに… | `current-0249`（`03_Tips.rst:803-808`）＋ `current-0303`（`RequestUnitTest_real.rst:179`）／`current-0328`（`send_sync.rst:138`）。「テスト用のコンポーネント設定ファイル」は実装優先（`reviews` §2 食い違い3）。キー名の組み立ては `FixedLengthFile.java:155-158` |
| 9 | コードブロック `xml` | `:50-54` | `<component name="TestDataConverter_FormUrlEncoded" …>` | `current-0250`（`03_Tips.rst:813-817`）。完全修飾名を `please.change.me` → `com.example` に変更（`reviews` D-3） |
| 10 | 段落 | `:56` | 登録したコンバータは、file-type に FormUrlEncoded を… | `current-0251`（`03_Tips.rst:822`・`:824-825`・`:827`。画像2枚は地の文に畳んだ。`reviews` D-2）＋ `current-0303`（`RequestUnitTest_real.rst:177`）／`current-0328`（`send_sync.rst:136`）。指示対象を明確にする書き換えはラウンド1・F-9 |
| 11 | アドモニション `tip` | `:58-60` | `file-type` の値は、応答電文のアサート方式にも影響する… | **出典・マッピングのいずれにも無い追記**（`reviews` D-8）。実装は `MessagePool.java:54`・`:154-158`・`:160-163`。導線先は承認済み `testdata_notation.rst:1177-1189`。**`design.md` §8 のどの類型に当たるかが未確定であり、`reviews` §4.5 の `decide` 3 として上申する** |

構造要素7件（母集合の外。参考）。

| 種別 | 行 | 内容 | 典拠 |
|---|---|---|---|
| ラベル | `:1` | `.. _request_unit_test_setting_mom:` | `style.md` S-08 の表（`style.md:353`）。新規考案なし |
| 見出し L1 | `:3-4` | リクエスト単体テストの設定（MOMによるメッセージング） | `vocabulary.md` の確定ページ名・`design.md:155-158` |
| ディレクティブ `contents` | `:6-8` | 目次 | `style.md` S-09 |
| 見出し L2 | `:12-13` | 使用方法 | `style.md` S-02・`design.md:194`（第2部で唯一必須） |
| 見出し L3 | `:15-16` | フレームワーク制御ヘッダのフィールド名を指定する | `style.md` S-03。下線49（表示幅48） |
| 見出し L2 | `:28-29` | 拡張例 | `style.md` S-02 |
| 見出し L3 | `:31-32` | テストデータの変換処理を実装する | `style.md` S-03・`design.md:198`（拡張例は手順として記載する）。ラウンド1・F-10 で `テストデータに変換処理を追加する` から改題。下線49（表示幅32。実測則 `max(49, 表示幅)` を満たす） |

**出典外の追記は2件**（#4 の3文目・#11）。いずれも実装で裏付けたうえで `decide` として上申する。§1・§1-2 の一方向表では検出できなかった種類の記述である。

## §2 ページ先頭ラベル

`style.md` S-08「NTF解説書のページ先頭ラベル一覧」の表から引用した。**新規考案なし。**

- ページ: `リクエスト単体テストの設定（MOMによるメッセージング）`（`style.md:353`）
- ファイル: `setup/request_unit_test/mom.rst`（S-08 の表・`design.md:789`・`:864` と一致）
- ラベル: `request_unit_test_setting_mom`（S-08 の表と一致）

`ja/` 全体に同名ラベルが存在しないことを確認した。

```
$ grep -rn "^\.\. _\`\?request_unit_test_setting_mom\`\?:" --include=*.rst ja/
ja/development_tools/testing_framework/setup/request_unit_test/mom.rst:1:.. _request_unit_test_setting_mom:
```

本ページ以外0件。

## §3 実装で確認した項目

参照コミット: `nablarch/nablarch-testing` = `e21bf67`（`main`）、`nablarch/nablarch-testing-yaml` = `a966ab9`（`feature/ntf-yaml`）。
いずれも
`/tmp/claude-1000/-home-tie303177-work-nablarch-nablarch-document/aacd451e-f4bb-4b00-8c7a-c01c7fc3b955/scratchpad/`
配下にクローンした。リポジトリ直下のビルド残骸 `nablarch/test/core/reader/MessageParser.java`（git の追跡下にない）は使っていない。

| # | 主張 | 確認した `file:line` | 参照コミット |
|---|---|---|---|
| 1 | インタフェースの正式名は `TestDataConverter`（`TestDataConvertor` ではない） | `src/main/java/nablarch/test/core/file/TestDataConverter.java:17`。`grep -rn "TestDataConvertor" .` が全体で0件 | `e21bf67` |
| 2 | 公開API（`:java:extdoc:` で参照できる） | 同 `:16`（`@Published`） | `e21bf67` |
| 3 | 実装するメソッドは `convertData` と `createDefinition` の2つ | 同 `:37`・`:27`。呼び出し順は `convertData` → `createDefinition`（`MessagePool.java:122-124`・`:148-152`） | `e21bf67` |
| 4 | 登録キー名は `TestDataConverter_` + `file-type` の値 | `FixedLengthFile.java:155-158` | `e21bf67` |
| 5 | 「データ種別はテストデータの `file-type` に指定した値」が正しい | 同 `:156`（`directives.get("file-type")`） | `e21bf67` |
| 6 | 登録先はテスト用のコンポーネント設定ファイル（`<component>` 定義） | `src/test/resources/nablarch/test/core/messaging/web/web-component-configuration.xml:50-54`・`web-component-configuration-request-testing.xml:42` | `e21bf67` |
| 7 | 変換が効くのは電文のテストデータ（ファイル入出力では呼ばれない） | `FixedLengthFile.createDefinition`／`convertData` の呼び出し元は `MessagePool.java:244`・`:253` のみ。`MessagePool` の利用は `RequestTestingMessagePool.java:87`・`:126`、`SendSyncSupport.java:299`・`:330`、`RequestTestingMessagingClient.java:412`・`:414` | `e21bf67` |
| 8 | 変換前の値は `text-encoding` のエンコーディングでバイト列になる | `DataFile.java:300-302`、`FixedLengthFile.java:131`・`:147` | `e21bf67` |
| 9 | コンバータは `Excel` 形式に限らず `YAML` 形式でも効く | `nablarch-testing-yaml` `YamlMessageBuilder.java:186-190` → `YamlFileBuilder.java:245-252`（`file-type` を含むディレクティブを `FixedLengthFile` に適用）、`YamlMessageBuilder.java:63-64`・`:89`（その `FixedLengthFile` が `RequestTestingMessagePool` の `source` になる） | `a966ab9` |
| 10 | `reader.fwHeaderfields` のキー名と分割方法 | `MessageParser.java:33`・`:107-110` | `e21bf67` |
| 11 | 未設定時の実効値は `requestId`・`userId`・`resendFlag`・`resultCode` | 同 `:109` | `e21bf67` |
| 12 | 設定先は環境設定ファイル（`SystemRepository.getString` で読む文字列） | 同 `:108`・`:110` | `e21bf67` |
| 13 | 同期応答メッセージ受信（`MessagingRequestTestSupport.java:33` の Javadoc「メッセージ同期応答用」）と応答不要メッセージ受信（`MessagingReceiveTestSupport.java:8` の Javadoc「メッセージ応答なし受信処理用」、`:13` で前者を継承）の**両方**のテストで使われる | `MessagingRequestTestSupport.java:82`／`MessagingReceiveTestSupport.java:42` → `MQSupport.java:87` → `BasicTestDataParser.java:82-83` | `e21bf67` |
| 13-2 | `reader.fwHeaderfields` は既定を**追加**するのではなく**置き換える**（ラウンド1・F-3） | `MessageParser.java:107-110` の三項演算子。未設定なら4件の既定、設定済みなら `makeArray` の結果のみを `fwHeaderFields` に代入する。合成は行われない。判定は `:101-103`（`fwHeaderFields.contains(name)`） | `e21bf67` |
| 13-3 | HTTPメッセージ受信のリクエスト単体テストも同一コードパス・同一設定（ラウンド1・R-1） | `MessagingRequestTestSupport` を継承するのは `MessagingReceiveTestSupport.java:13` の1件のみ。`TestDataParser#getMessage` の `src/main/java` 内の呼び出し元は `MQSupport.java:87` のみ（`DbLessTestDataParser.java:55-56` は委譲）。`MQSupport` の生成は `MessagingRequestTestSupport.java:82`・`MessagingReceiveTestSupport.java:42` の2箇所のみ | `e21bf67` |
| 14 | 同期応答メッセージ送信では、キーと値の組のフレームワーク制御ヘッダは使用されない | (a) `RequestTestingSendSyncSupport.java:157` → `BasicTestDataParser.java:113-117` → `GroupMessageParser.java:43`・`:58`（`Collections.emptyMap()`）／(b) `SendSyncSupport.java:421` → `BasicTestDataParser.java:99-103` → `SendSyncMessageParser.java:35-44`（`UnsupportedOperationException`） | `e21bf67` |
| 15 | `YAML` 形式は `reader.fwHeaderfields` を参照しない | `nablarch-testing-yaml` の追跡下 `src/main/java` に `fwHeaderfields` の参照0件（ヒットするのは `src/test` と `ntf-testdata-yaml-schema.json:215`・`:430` の説明文のみ） | `a966ab9` |
| 16 | `file-type` の値は応答電文のアサート方式にも影響する | `MessagePool.java:54`・`:154-158`・`:160-163` | `e21bf67` |
| 17 | `defaultDirectives` では `file-type` を設定できない（判断4の根拠） | `DataFile.java:91-92`（`:91` が `prepareDefaultDirectives(DEFAULT_DIRECTIVES)`、`:92` が `setDirective("file-type", getFileType())`。既定値を適用した後に上書きする）。`prepareDefaultDirectives` の本体は `:68-81` | `e21bf67` |
| 18 | `createDefinition` が返すレイアウト定義は、変換後のテストデータを電文のバイト列へ**書き出す**ために使う（読み込みではない。ラウンド2・是正1） | `MessagePool.java:122`（`convertByFileType`）→ `:124`（`createLayoutFromDataRecord`。実体は `:252-254`）→ `:130`（`msg.setFormatter(formatter.setDefinition(ld)).addRecord(currentData)`）。`RequestTestingMessagePool.java:87-96` も `SendingMessage` に書き出して `getBodyBytes()`。`MessagePool.java:165` の `readRecords()` は AP が出力した応答電文が対象で、`:174-177` の期待値側は再び書き出し。`TestDataConverter.java:20` の Javadoc は「対応した」で方向を限定しない | `e21bf67` |
| 19 | `NablarchTestUtils.makeArray` はカンマ分割のみで**トリムしない**（ラウンド2の申し送り1） | `NablarchTestUtils.java:45-49`（`COMMA.split(str)`。`null`／空文字列は長さ0の配列）・`:36`（`private static final Pattern COMMA = Pattern.compile(",")`）。空白除去は無い。結果は `MessageParser.java:110` で `asSet` に渡され、判定は `:103` の `contains` | `e21bf67` |

出典と実装が食い違ったのは4件（インタフェース名／`Excel` 限定の表現／登録先の表現／`createDefinition` の記述方向。4件目はラウンド2で追加）。全件を
`reviews/page-request_unit_test_setting_mom.md` §2「出典と実装が食い違った点（全件）」に記載した。

**#18・#19 の `file:line` は作業ツリー（`fdf55d4`）で確認したが、`git diff --stat e21bf67 HEAD` で `src/main/java/nablarch/test/core/messaging/`・`.../http/`・`.../file/TestDataConverter.java`・`NablarchTestUtils.java`・`core/reader/MessageParser.java` に差分が無いことを確認済みであり、`e21bf67` の行番号と同一である**（差分があるのは `core/reader/` の `DataFileParser.java`・`ListMapParser.java`・`TableDataParser.java`・`TestDataParsingTemplate.java` の4ファイルのみ）。

## §4 Docker フルビルド

```
$ docker build -t nablarch-document-build .
ERROR: failed to build: failed to solve: process "/bin/sh -c pip install --no-cache-dir setuptools==57.5.0 wheel     && pip install --no-cache-dir --no-build-isolation -r requirements.txt" did not complete successfully: exit code: 1
（原因: pypi.org への TLS 接続が中間証明書で遮断される
  `SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain'))`。
  ネットワーク側の事情であり、リポジトリの `Dockerfile` の問題ではない）
```

既存イメージ `nablarch-document-build:latest` を使用した。**イメージは `Dockerfile` に対して最新である**ことを確認した。

- イメージの作成日時: `2026-08-07T09:34:28+09:00`（`docker image inspect --format '{{.Created}}'`）
- `Dockerfile`・`requirements.txt` の最終変更: `c241906`（2026-07-23）

```
$ docker run --rm -v /home/tie303177/work/nablarch/nablarch-document:/root/document nablarch-document-build \
    /bin/bash -c "cd /root/document; sphinx-build -a -d _build/.doctrees/ja -b html ja _build/html"
build succeeded, 1 warning.
```

ログの警告行は1行のみで、既知の1件である。

```
/root/document/ja/application_framework/application_framework/libraries/db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test (if the link has no caption the label must precede a section header)
```

- **新規警告0件。** `mom.rst`・`setup/index.rst` に関する警告・エラーは0件
- `undefined label` の新規発生0件（上記1件は `#7` から継続する既知のもの）
- `Title underline too short` 0件・`Malformed table` 0件
- 生成物で `:ref:`・`:java:extdoc:` の解決を確認した
  - `href="../../implementation/testdata_notation.html#testdata-notation-messaging-data"`（2箇所とも）
  - `href="https://nablarch.github.io/docs/6-NEXT-SNAPSHOT/javadoc/nablarch/test/core/file/TestDataConverter.html"`

ビルドは2回実行した（1回目は `mom.rst:26` の `tip` の推敲前、2回目は最終版）。**いずれの直後にも
`git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行して戻した。** 2回とも `sphinx.mo` は
再生成されており、戻さなければ通算5回目・6回目の混入になっていた。

### §4-2 是正ラウンド1のフルビルド

同じコマンドで再度フルビルドした。

```
$ docker run --rm -v /home/tie303177/work/nablarch/nablarch-document:/root/document nablarch-document-build \
    /bin/bash -c "cd /root/document; sphinx-build -a -d _build/.doctrees/ja -b html ja _build/html"
build succeeded, 1 warning.
```

- 警告行は1行のみで、既知の `db_double_submit.rst:108`（`undefined label: how_to_set_token_in_request_unit_test`）である。**新規警告0件。**
- **直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行して戻した**（実行後の `git status --porcelain` に当該ファイルが現れないことを確認）。
- **`.. contents::` 目次への影響を生成HTMLで確認した。** `_build/html/development_tools/testing_framework/setup/request_unit_test/mom.html` の `<div class="contents local topic">` に並ぶのは「使用方法 > フレームワーク制御ヘッダのフィールド名を指定する」「拡張例 > テストデータの変換処理を実装する」の4項目で、F-10 の改題が反映されている。F-1 の `tip` 削除は目次に影響しない（アドモニションは見出しではないため元から目次に現れない）。`<h2>`・`<h3>` の抽出結果も同じ4件で、階層は L2×2・L3×2 のままである。
- アドモニションの生成結果は `important` 1件・`tip` 1件（F-1 前は `tip` 2件・`important` 0件）。
- `:ref:` は `href="../../implementation/testdata_notation.html#testdata-notation-messaging-data"` が2件、`:java:extdoc:` は `href="https://nablarch.github.io/docs/6-NEXT-SNAPSHOT/javadoc/nablarch/test/core/file/TestDataConverter.html"` が1件、いずれも解決している。
- `Title underline too short` 0件・`Malformed table` 0件。

### §4-3 是正ラウンド2のフルビルド

同じコマンドで再度フルビルドした。

```
$ docker run --rm -v /home/tie303177/work/nablarch/nablarch-document:/root/document nablarch-document-build \
    /bin/bash -c "cd /root/document; sphinx-build -a -d _build/.doctrees/ja -b html ja _build/html"
build succeeded, 1 warning.
```

- 警告行は1行のみで、既知の `db_double_submit.rst:108`（`undefined label: how_to_set_token_in_request_unit_test`）である。**新規警告0件。**
- **直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行して戻した**（実行後の `git status --porcelain` に当該ファイルが現れないことを確認）。
- **生成HTMLが今回の是正を反映していることを確認した。** `_build/html/development_tools/testing_framework/setup/request_unit_test/mom.html` に「変換後のデータに対応するレイアウト定義を動的に生成する」（是正1）と「使用するフレームワーク制御ヘッダのフィールド名を、すべてカンマ区切りで列挙する。」（是正2）がそれぞれ1件現れ、是正前の文字列「変換後のデータを読み込むための…」は0件である。
- 是正は既存の表セル1行とコメント行1行の書き換えのみで、構成は変えていない。生成HTMLで実測した値はラウンド1（§4-2）と同じである。`<div class="contents local topic">` の項目は「使用方法」「フレームワーク制御ヘッダのフィールド名を指定する」「拡張例」「テストデータの変換処理を実装する」の4件、`class="admonition important"` 1件・`class="admonition tip"` 1件、`href=".../testdata_notation.html#testdata-notation-messaging-data"` 2件、`:java:extdoc:` の `javadoc/nablarch/test/core/file/TestDataConverter.html` 1件。

## §5 差分の範囲（`commit & push` の直前）

母集合は `git status --porcelain` の**全件**。`ja/` や特定ディレクトリに絞っていない。
`git diff` は未追跡ファイルを出さないため母集合に使っていない。

```
$ git status --porcelain
 M ja/development_tools/testing_framework/setup/index.rst
?? .rn/20260724-ntf-yaml-support/checks/task-21.md
?? .rn/20260724-ntf-yaml-support/reviews/page-request_unit_test_setting_mom.md
?? ja/development_tools/testing_framework/setup/request_unit_test/mom.rst
```

| 状態 | パス | 判定 |
|---|---|---|
| ` M` | `ja/development_tools/testing_framework/setup/index.rst` | 予定どおり（`toctree` に `request_unit_test/mom` を1行追加。追加1行・削除0行） |
| `??` | `.rn/20260724-ntf-yaml-support/checks/task-21.md` | 予定どおり（self-check。**コミットしない**） |
| `??` | `.rn/20260724-ntf-yaml-support/reviews/page-request_unit_test_setting_mom.md` | 予定どおり（レビュー記録。**コミットしない**） |
| `??` | `ja/development_tools/testing_framework/setup/request_unit_test/mom.rst` | 予定どおり（新規ページ） |

予定外**0件**。`locales/ja/LC_MESSAGES/sphinx.mo` は §4 のとおりビルド直後に戻しており、この表に現れていない。
`mapping/`・`design.md`・`ja/conf.py`・既存の承認済み `.rst` への差分は0件。

### §5-2 是正ラウンド1の差分の範囲（`commit & push` の直前）

母集合は `git status --porcelain` の**全件**。`ja/` や特定ディレクトリに絞っていない。

```
$ git status --porcelain
 M ja/development_tools/testing_framework/setup/request_unit_test/mom.rst
?? .rn/20260724-ntf-yaml-support/checks/task-21.md
?? .rn/20260724-ntf-yaml-support/reviews/page-request_unit_test_setting_mom.md
```

| 状態 | パス | 判定 |
|---|---|---|
| ` M` | `ja/development_tools/testing_framework/setup/request_unit_test/mom.rst` | 予定どおり（F-1〜F-10 の是正。**コミットする**） |
| `??` | `.rn/20260724-ntf-yaml-support/checks/task-21.md` | 予定どおり（self-check。R-3・R-4 を反映。**コミットしない**） |
| `??` | `.rn/20260724-ntf-yaml-support/reviews/page-request_unit_test_setting_mom.md` | 予定どおり（レビュー記録。R-1・R-2・R-5 と `decide` 候補を反映。**コミットしない**） |

予定外**0件**。`locales/ja/LC_MESSAGES/sphinx.mo` は §4-2 のとおりビルド直後に戻しており、この表に現れていない。
`ja/development_tools/testing_framework/setup/index.rst` は `#21` 本体（`8b956cd`）で既にコミット済みのため、ラウンド1の差分には現れない。
`mapping/`・`design.md`・`glossary.md`・`style.md`・`ja/conf.py`・既存の承認済み `.rst`（`http_messaging.rst`・`testdata_notation.rst` を含む）への差分は0件。
`git add` は `ja/development_tools/testing_framework/setup/request_unit_test/mom.rst` のみを明示的に指定した（`git add -A` / `git add .` は使っていない）。

### §5-3 是正ラウンド2の差分の範囲（`commit & push` の直前）

母集合は `git status --porcelain` の**全件**。`ja/` や特定ディレクトリに絞っていない。

```
$ git status --porcelain
 M ja/development_tools/testing_framework/setup/request_unit_test/mom.rst
?? .rn/20260724-ntf-yaml-support/checks/task-21.md
?? .rn/20260724-ntf-yaml-support/reviews/page-request_unit_test_setting_mom.md
```

| 状態 | パス | 判定 |
|---|---|---|
| ` M` | `ja/development_tools/testing_framework/setup/request_unit_test/mom.rst` | 予定どおり（是正1・是正2 の2箇所のみ。追加2行・削除2行。**コミットする**） |
| `??` | `.rn/20260724-ntf-yaml-support/checks/task-21.md` | 予定どおり（self-check。§1-3 の #3・#7、§4-3、§5-3 を反映。**コミットしない**） |
| `??` | `.rn/20260724-ntf-yaml-support/reviews/page-request_unit_test_setting_mom.md` | 予定どおり（レビュー記録。§2 食い違い4 と §5 を追加。**コミットしない**） |

予定外**0件**。`locales/ja/LC_MESSAGES/sphinx.mo` は §4-3 のとおりビルド直後に戻しており、この表に現れていない。
`git diff` の変更行は `mom.rst:21`（コメント行）と `mom.rst:46`（`createDefinition` のセル）の2行のみで、`mom.rst:22` の設定値 `reader.fwHeaderfields=requestId,addHeader` は変更していない。
`mapping/`（`glossary.md`・`style.md`・`mapping.csv` を含む）・`design.md`・`ja/conf.py`・既存の承認済み `.rst`（`http_messaging.rst`・`testdata_notation.rst` を含む）への差分は0件。
`git add` は `ja/development_tools/testing_framework/setup/request_unit_test/mom.rst` のみを明示的に指定した（`git add -A` / `git add .` は使っていない）。

## §6 判断1〜4 の結論

詳細（理由・根拠 `file:line`）は `reviews/page-request_unit_test_setting_mom.md` §3 の D-1〜D-9。

| 判断 | 結論 | 一言の理由 |
|---|---|---|
| 1 `reader.fwHeaderfields` の重複 | **本ページにも書く。ただし複製しない**（MOM の文脈に限定し、`Excel`／`YAML` の差は `important` ではなく段落中の1文に畳む。`http_messaging.rst` への `:ref:` は張らない） | `mapping.csv` が本ページの `使用方法` に割り当てており、落とすと唯一の必須セクションが空になる。適用範囲も同一ではない。**`decide` 候補として上申**（D-1） |
| 2 Excel記述例の画像2枚 | **載せない。セル格子の表にも置き換えない。事実は地の文に残す** | `design.md:200-207` の記載範囲が第2部に「テストデータの記述例」を置かないと定めている。同じ例は `biz_samples/04/0401_ExtendedDataFormatter.rst:174-204` が既に持つ。画像の最終的な扱いは `#last`（D-2） |
| 3 サンプルクラスの完全修飾名 | **`com.example.test.core.file.FormUrlEncodedTestDataConverter`** | NTF新解説書は `#11` で `com.example` を採用済み（`common.rst:61`）。`ja/` の追跡下 `.rst` でも `com.example` 69件が `please.change.me` 45件を上回る（D-3） |
| 4 導線 | **`testdata_notation-messaging_data` へ2箇所張る。`request_unit_test_setting_batch` へは張らない** | 前者は `design.md:209` の要請で、参照先本文を読んで矛盾が無いことを確認した。後者は本ページがファイル入出力に触れず、`file-type` が `defaultDirectives` では設定できない（`DataFile.java:91-92`）ため主題がつながらない（D-4） |

判断2 で残した「出典の事実が地の文から失われていないこと」の確認は §1-2 の表（`03_Tips.rst:822`・`:824-825`・`:827` の3行）に記載した。

## Completion Criteria

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| `mapping.csv` の当該 `dest_page` の全行が反映されている（`DROP` を除く） | OK | `csv.DictReader` で全595行から `dest_page` 完全一致で抽出した8行（`DROP` 0件・76 lines）が §1 の表に全件現れ、それぞれ反映先の行番号を持つ。出典の各要素との突合は §1-2 | OK | 観点A（網羅性）が母集合を独立に再抽出（595行→8行・`DROP` 0・76 lines、前後空白違い0件）し、出典を `git show c241906:<src_file>` で全8範囲実読したうえで「事実の欠落0件」と判定。観点C・Dも同じ8行を独立抽出して一致。コーディネータも `dest_page` 完全一致で再抽出し8行を確認 |
| 当該 `dest_page` のマッピング行が全件、ページのどこに反映されたかの対応表が `checks/task-21.md` にある | OK | §1 の表（`mapping_id` ごとに反映先セクションと反映内容）。8行すべて記載 | OK | 観点A・Cが、自身の独立抽出結果と §1 の表を突き合わせて「1行の過不足なく一致」と判定 |
| 全件表を求める項目が、ゲートの実行順の先頭に置かれている（母集合をホワイトリストで切り出していない） | OK | 全件表は本ファイルの冒頭 §1 にあり、他のすべての節より前に置いた。抽出条件は `dest_page` の完全一致のみで、`mapping_id` の列挙は使っていない | OK | 観点Aが §1 がファイル冒頭（他の全節より前）にあること、抽出条件が完全一致のみであることを確認。あわせて観点Aの `should-4`（「出典→ページ」の一方向しか無く逆方向の全件表が欠けている）を受け、ラウンド1で §1-3「ページ→典拠」の逆方向全件表を追加した。**前ラウンドで出典外の追記1件が記録から漏れた直接の原因がこの欠落だった** |
| 4観点のレビューがすべて実施・記録されている | — | 本タスクの担当外（コーディネータが実施）。`reviews/page-request_unit_test_setting_mom.md` は §1〜§3 のみ作成済み | OK | ラウンド1で A:網羅性 / B:トンマナ / C:用語 / D:整合性 を**それぞれ別のサブエージェント**で実施（4観点とも FAIL）。ラウンド2は `steering.md` の規定に従い是正差分限定で2本（範囲検証＝PASS・`must` 0／新規記述のファクトチェック＝不一致1件）。各ラウンドの件数・観点・対応は `reviews` §4・§5 |
| 未対応の指摘が残っていない、または残す判断とその理由が記録されている | OK | 作成時の判断9件（D-1〜D-9）を `reviews` §3 に理由・根拠つきで記録。ユーザー判断に回す候補は D-1・D-8 の2件（および D-2・D-3 の `#last` 送り2件）で、いずれも記録済み | OK | ラウンド1の `must` 3件（重複除去後）と `should`・`note` はすべて是正またはユーザー判断へ上申。ラウンド2の不一致1件も是正済み。残置は `decide` 5件で、いずれも承認済みページ・`glossary.md`・`design.md` の変更を伴うためスコープ外として上申（`reviews` §4.5・§5.3） |
| `make html` が当該ページについてエラーを出さない | OK | §4。`build succeeded, 1 warning.`。警告は既知の `db_double_submit.rst:108` 1件のみで新規0件。`mom.rst`・`setup/index.rst` の警告・エラーは0件。`:ref:`・`:java:extdoc:` の解決を生成HTMLで確認 | OK | **コーディネータが自分で Docker フルビルドを実行して確認**（`8b956cd` 時点と最終 `346171d` 時点の2回）。いずれも `build succeeded, 1 warning.`、警告は `db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test` の既知1件のみで新規0件。観点A・B・Dとラウンド2の範囲検証も独立にビルドして同結果 |

## Overall Verdict

- 是正ラウンド2: OK（是正は指示どおり2箇所のみ。是正1（`must`・`mom.rst:46`）は `createDefinition` の用途を実コード（`MessagePool.java:122-130`・`RequestTestingMessagePool.java:87-96`・`TestDataConverter.java:20`）で確認したうえで実装優先に改め、`reviews` §2 に出典との食い違い4件目として記録。是正2（`should`・`mom.rst:21`）はコメント行のみ書き換え、出典そのものの設定値 `:22` は不変。フルビルドは `build succeeded, 1 warning.` で新規警告0件、生成HTMLで両是正の反映を確認、`sphinx.mo` は戻し済み。差分は予定3件のみで予定外0件。申し送り3件（`makeArray` がトリムしない／`http_messaging.rst:37` との記述深度の非対称／HTTPメッセージング受信への適用可否は**未確定**）を `reviews` §5.3 に記録し、本文の他の行・`design.md`・`mapping/`・`ja/` の他ファイルには手を付けていない）
- 是正ラウンド1: OK（本文の指摘10件 F-1〜F-10 と記録の指摘5件 R-1〜R-5 をすべて対応。フルビルドは `build succeeded, 1 warning.` で新規警告0件、`sphinx.mo` は戻し済み。差分は予定3件のみで予定外0件。実装で新たに5項目を確認（§3 の #13・#13-2・#13-3、`reviews` §4.3）。ユーザー判断に回す `decide` 候補4件と新たに気づいた申し送り2件を `reviews` §4.5 に記録し、本文・`glossary.md`・`testdata_notation.rst`・`design.md` には手を付けていない）
- Self-check: OK（完了条件のうち作成担当分5件すべて OK。マッピング8行の反映漏れ0件、出典と実装の食い違い3件は全件を実装優先で解消して記録、Docker フルビルドは `build succeeded, 1 warning.` で新規警告0件、差分範囲は予定4件のみで予定外0件。判断1〜4 はすべて結論と理由を記録し、両論併記にしていない）
- QA（コーディネータの独立検証）: OK — 母集合（`dest_page` 完全一致8行）を自分で再抽出して一致を確認。Docker フルビルドを自分で実行（`8b956cd` 時点と最終 `346171d` 時点）し、いずれも `build succeeded, 1 warning.`（既知の `db_double_submit.rst:108` のみ・新規0件）。最終ビルドの生成HTMLで是正2件の反映を確認。`git status --porcelain` の全件が未追跡の記録2件のみで `sphinx.mo` の混入0件（各ビルドの直後に戻している）。見出し下線を `unicodedata.east_asian_width` で実測し L1=53（幅53）・L2=50×2・L3=49（幅48/32）が実測則どおりであることを確認。段落内改行0件
- Design expert（観点D:整合性）: OK（是正後） — ラウンド1は FAIL。技術的主張は全8件が実装と一致していたが、`使用方法` が承認済み `http_messaging.rst` と重複している点を `must` とした。この重複は本タスクで解消せず `decide` 1 として上申する（承認済みページと `common.rst` の変更を伴うため）。`design.md` §3 のアウトライン・記載範囲、§13、`toctree` の並び順はいずれも適合と判定
- Craft expert（観点B:トンマナ）: OK（是正後） — ラウンド1は FAIL。`tip` の使い分け・リード文の主語・出典から落ちた語・`データの形式` の新語・L3見出しの形式を指摘。全件是正済み。**ただしBが `must` の根拠として挙げた前例2件（`class_unit_test.rst:91`「バリデーションのテスト方法を差し替える」・`web.rst:113`「テストクラスの共通処理を差し替える」）は実在しない**（コーディネータが実測。`^拡張例$` を持つのは `web.rst:222` と本ページのみ、`差し替える` で終わる見出しは `ja/` 配下0件）。改題は `design.md` §3「拡張例は手順として記載する」と実在する `web.rst:225`「テストデータの書き方を拡張する」を根拠として維持し、Bの引用は取り消す
- Verification expert（観点A:網羅性 / 観点C:用語 / ラウンド2のファクトチェック）: OK（是正後） — ラウンド1はいずれも FAIL。Aは出典外の追記1件が記録から漏れている点、Cは `メッセージ受信` が `glossary.md:157` の禁止と同じ曖昧さを持つ点を `must` とした。ラウンド2のファクトチェックは18主張中16件一致・1件不一致（`createDefinition` の「読み込むための」）・1件確認不能（「アーキテクトが用意する」＝出典由来の役割記述でコードに現れない情報のため保持）。不一致1件は実装優先で是正済み
- Ready to check off: **No** — user review 待ち。`steering.md` の「#9〜: ページの作成」共通 Steps はページ作成タスクの最終ステップに user review を課しており（`#17`〜`#20` と同じ）、`/rn:ty` の承認をもって閉じる。あわせて `decide` 5件（`reviews` §4.5・§5.3）の回答が必要

## §7 user review（`/rn:ty` 承認）後の反映とゲート

2026-08-13 の `/rn:ty` で公開本文が承認され、`decide` 5件の回答と `should` 3件が示された。本節はその反映結果とゲート10件の実行結果を記録する。反映内容そのものは `reviews/page-request_unit_test_setting_mom.md` §6 にある。

### §7-1 `既定` → `デフォルト` の全件表（母集合を先に固定）

母集合は `grep -ro "既定" ja/development_tools/testing_framework/` の**出現数**（行数ではない）。ホワイトリストで切り出していない。

| ファイル | 出現数 | 該当行 |
|---|---|---|
| `setup/request_unit_test/batch.rst` | 13 | `:10`・`:39`（L3見出し）・`:41`×2・`:60`・`:65`・`:70`・`:76`×3・`:78`・`:88`・`:96` |
| `implementation/testdata_notation.rst` | 6 | `:429`・`:871`・`:1131`・`:1137`・`:1236`・`:1513` |
| `setup/request_unit_test/mom.rst` | 5 | `:10`・`:17`×3・`:33` |
| `setup/request_unit_test/http_messaging.rst` | 2 | `:10`・`:37` |
| **計** | **26** | — |

**`/rn:ty` の内訳（`batch.rst` 12・`testdata_notation.rst` 7）とは2ファイルで1件ずつ食い違うが、合計26は一致する。** 本表はコーディネータが `grep -o` で数え直した実測値である。

置換の形は `既定`→`デフォルト` の1対1で、例外は `testdata_notation.rst:429` の `既定キー`→`デフォルトのキー` のみ（`デフォルトキー` は `ja/` 全体で0件、`デフォルトのキー` は1件〈`FW:handlers/common/thread_context_handler.rst:151`〉であるため既存の用例に合わせた）。`既定から変更している`→`デフォルトから変更している` も FW解説書に2件の用例がある（`FW:libraries/data_io/data_format.rst:557`・`FW:nablarch/policy.rst:64`）。

### §7-2 語彙の実測（`glossary.md` §5.14 の採用根拠）

| コーパス | `デフォルト` | `既定` |
|---|---|---|
| FW解説書（`ja/application_framework/application_framework/`、作業ツリー） | 630 | 4 |
| `ja/` の NTF 以外 | 755 | 4 |
| 現行解説書（`c2419060` の `guide/development_guide/**/*.rst`） | 58 | **0** |
| input資料 | 47 | 5 |
| NTF新ページ（是正前） | 64 | 26 |
| NTF新ページ（是正後） | 90 | **0** |

**現行解説書に `既定` は0件である。** この語は出典由来ではなく新ページで生じた揺れであり、`デフォルト` に寄せることに反証はない。いずれも `grep -o` による実測で、`scan-terms.tsv` の出現数ではない（3語とも `term_candidates.tsv` に未登録）。

### §7-3 ゲート1〜10 の実行結果

| # | ゲート | 結果 | 実行結果 |
|---|---|---|---|
| 1 | `ja/` の差分は4ファイルに限る | **PASS** | `git status --porcelain` の `ja/` 配下は `implementation/testdata_notation.rst`・`setup/request_unit_test/mom.rst`・`http_messaging.rst`・`batch.rst` の4件のみ。`batch.rst` の差分は語の置換13箇所だけで、他の変更を含まない（`git diff` 全行を目視） |
| 2 | `既定` の残存0件 | **PASS** | `grep -rn "既定" ja/development_tools/testing_framework/` が0件（`about`・`setup`・`implementation`・`tools` を含むディレクトリ全体。`guide/` は `#7` で削除済みのため存在しない） |
| 3 | `デフォルト設定` が新たに生じていない | **PASS** | `git diff ja/ \| grep "^+" \| grep -c "デフォルト設定"` = 0。`batch.rst:96` の `既定の対応表` は `デフォルトの対応表` になっている |
| 4 | `glossary.md` の差分は §5.12 1行・§5.14 1行・§8 3行の追加に限る | **PASS** | `git diff --numstat` = `5 0`（追加5・削除0）。ハンク位置は `@@ -283,0 +284 @@`・`@@ -326,0 +328 @@`・`@@ -578,0 +581,2 @@`・`@@ -597,0 +602 @@` の4つで、**§5.15.2 の一覧（`:403`〜`:449`）は1つのハンクにも含まれない** |
| 5 | `design.md` の差分は §8 への類型1件の追加に限る | **PASS** | `git diff --numstat` = `26 0`。ハンクは `@@ -478,0 +479,26 @@` の1つのみ（§8 末尾、`## 9. 対象外とするもの` の直前） |
| 6 | `mapping.csv`・`mapping/_batch/`・`volume.md` に差分が無い | **PASS** | `git status --porcelain` の対象3パスが空 |
| 7 | `verify_mapping.py` が 595行 / 12,986 / 11,983 で exit 0 | **PASS** | `Loaded 595 rows` / `lines total (all rows): 12986` / `lines total (excluding DROP): 11983` / `OK: no errors` / `exit=0` |
| 8 | Docker フルビルド（`-a`）で新規警告0件 | **PASS** | `build succeeded, 1 warning.`。警告は `db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test` の既知1件のみ。**直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行済み。** 生成HTMLで4ファイルの反映と `既定` 残存0件を確認 |
| 9 | 見出し下線が実測則を満たす | **PASS** | `unicodedata.east_asian_width` で `ja/development_tools/testing_framework/**/*.rst` の全見出しを実測。`batch.rst:39` は表示幅 32→38 に増えたが下線は49のままで、L3の則 `max(49, 表示幅)` を満たす（**`/rn:ty` は「表示幅が2増える」としているが実測は6増（`既定値`6→`デフォルト値`12）。いずれにせよ49未満で下線の変更は不要**）。他に置換で表示幅が変わる見出しは無い |
| 10 | 差分の範囲を `git status --porcelain` の**全件**で確認 | **PASS** | 全件7件 = `ja/` 4件（ゲート1）＋ `.rn/` 3件（`design.md`・`mapping/glossary.md`・`reviews/page-request_unit_test_setting_mom.md`）。予定外0件。未追跡ファイル0件。`locales/ja/LC_MESSAGES/sphinx.mo` は**ビルド直後に戻したため差分に現れていない** |

**`checks/task-21.md`（本ファイル）自身の差分は本節の追加のみ**であり、ゲート10の母集合には commit 直前の再確認時に現れる。

### §7-4 反映しなかったもの・限界

- **`verify_glossary.py` は本タスクの前から失敗しており、本タスクでも通していない。ただし本タスクで7件増えた。** 実測は次のとおり（`git stash` で `glossary.md` だけを HEAD に戻して前後を比較した）。

  | | 変更前 | 変更後 | 差 |
  |---|---|---|---|
  | `[ref]`（`design.md` の行番号ずれ） | 13 | 13 | 0 |
  | `[section]`（揺れ表記が §8 に無い） | 1 | 1 | 0 |
  | `[term]`（`term_candidates.tsv` に無く件数を検証できない） | 4 | 9 | **+5** |
  | `[count]`（件数主張が `scan` 出力に無い） | 0 | 2 | **+2** |
  | **合計** | **18** | **25** | **+7** |

  増えた7件はすべて、今回追加した3語（`環境設定ファイル`・`デフォルト`・`既定`）と揺れ表記2語（`propertiesファイル`・`プロパティファイル`）が `mapping/tools/term_candidates.tsv` に未登録であることに起因する。**`term_candidates.tsv` に登録すれば解消するが、§1 が「tsv に載せる表記の集合を変えると出現数も変わる」（最長一致・非重複のため）と明記しており、既存の全件数主張を再計算する作業になる。** `/rn:ty` のゲート一覧に本スクリプトは含まれず、`term_candidates.tsv` の更新も指示されていないため、**本タスクでは触れていない。** `[ref]` 13件と合わせて別タスクで一括して直す必要がある。なお `glossary.md` §5.14 の揺れ表記欄は、当初 `既定値`・`既定では`・`既定の〜` を個別のコードスパンで書いたため `[section]` が3件増えたが、`既定` の1語にまとめて解消済み（意味は変わらない）
- `nablarch-testing-yaml` のスキーマ説明文（`ntf-testdata-yaml-schema.json`）の見直しは PR #75 側の話であり、本タスクの範囲外（`/rn:ty` §4 の明示）
- `real.rst:15` のパッケージ名の誤り（`nablarch.test.core.http` → `nablarch.test.core.messaging`）は、第3部「リクエスト単体テスト（MOMによるメッセージング）」を書くタスク（`current-0295`〜`0301`）で是正する。本タスクでは何もしていない
