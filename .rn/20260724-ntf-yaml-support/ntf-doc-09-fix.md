# 作業指示: `#9`「テストデータの書き方」の是正

対象ブランチ: `lovaizu/nablarch-document` の `work`（`a0d09aa` の続き）

`#9` は user review で**差し戻し**とする。本書の STEP 1〜5 をすべて実施したうえで、再度 user review に上げること。

---

## 背景

ユーザーレビューに上げた `decide` 3件のうち、A-3（必須カラムの出典対立）と B-F01（L4相当の表現）は、**実物確認で決着した**。判断を仰ぐ必要はない。D-4（`about/index.rst` の参照）は「`#9` の修正に同梱する」とユーザーが判断した。

加えて、観点Aが検出できていなかった**網羅性の欠落を1件**検出した。

したがって本書で扱うのは `must` 3件（STEP 1〜3）と、同梱と決まった1件（STEP 4）である。

---

## STEP 1 — testShots の必須カラム区分を是正する（`must`。事実誤り）

### 確認した事実

`nablarch/nablarch-testing` の `main`（コミット `e21bf67`、`nablarch-testing` 2.2.0、`release-6u2` マージ済み）を実際に読んで確認した。**同リポジトリに `6u3` のブランチ・タグは存在しない**（`git ls-remote origin` で確認）。

**(a) 「必須」の意味は、全処理方式で「カラム（キー）自体が存在すること」であり、値が空でもよい。**

- ウェブアプリケーション: `TestCaseInfo#getValue`（`TestCaseInfo.java:443-448`）が `row.containsKey` で判定し、無ければ `IllegalArgumentException("column 'X' is not defined.")` を投げる
- バッチ・メッセージング: `TestShot#executeTestShot`（`TestShot.java:77-78`）が `NablarchTestUtils.assertContainsRequiredKeys` でキーの存在のみを検査する
- エンティティバリデーション: `EntityTestSupport#checkRequiredColumns`（`EntityTestSupport.java:269-276`）が `columns.containsAll(required)` でキーの存在のみを検査する

**(b) `isValidToken` と `forwardUri` は必須である。**

- `isValidToken` — `TestCaseInfo#isValidToken()`（`TestCaseInfo.java:482-484`）が `getValue` 経由で読む。呼び出し元 `AbstractHttpRequestTestTemplate#executeTestCase:257` は**条件分岐の外**にあり、全テストケースで必ず評価される
- `forwardUri` — `TestCaseInfo#getExpectedForwardUri()`（`TestCaseInfo.java:237-239`）が同じく `getValue` 経由で読む。`assertForwardUri`（`AbstractHttpRequestTestTemplate.java:554-557`）は `assertAll:464` から**無条件に**呼ばれる
- 対照: `getExpectedContentLength()`（`TestCaseInfo.java:246-248`）は `testCaseParams.get(...)` を使い、カラムが無くても例外にならない。これが真の任意カラムである

したがって、現行解説書の表（`06_TestFWGuide` 削除前の `05_UnitTestGuide/02_RequestUnitTest/index.rst`）の「必須」欄が不完全であり、input資料（`ntf-testdata-doc-examples-testshots.md:62-70`）が正しい。

**(c) `requestParams` と `responseResult` は、そもそも testShots のカラムではない。**

`AbstractHttpRequestTestTemplate.java:74,77` で定数として宣言され、`:336-339` で `getCachedListMap(sheetName, REQUEST_PARAMS_LIST_MAP)` / `getCachedListMap(sheetName, EXPECTED_RESPONSE_LIST_MAP)` のように**リテラルのまま LIST_MAP の ID として使われる**。`getValue(testCaseParams, ...)` を経由しない。

対照として `context` は `:334-335` で `getValue(testCaseParams, TestCaseInfo.CONTEXT_LIST_MAP)` を経由しており、これは正真正銘の testShots カラムである（成果物の記載どおりで正しい）。

**両出典とも `requestParams` をカラムとして扱っており、誤っている。** 誤りの由来は `TestCaseInfo.java:333-338` の Javadoc（「LIST_MAP『testCases』の『requestParams』カラムで指定されている」）とみられるが、この Javadoc は同クラスの実コードと一致していない。

**(d) バッチ・メッセージング・エンティティバリデーションの表は、現状で正しい。** 変更しないこと。

- `TestShot.REQUIRED_COLUMNS`（`TestShot.java:385-387`）= `no` / `description` / `expectedStatusCode` / `diConfig` / `requestPath` / `userId`（`TITLE` の実体は `"description"`、`TestShot.java:351`）
- `EntityTestSupport.REQUIRED_COLUMNS_FOR_RELATIONAL_VALIDATION`（`EntityTestSupport.java:69-74`）= `title` / `expectedMessageId1` / `propertyName1`

### 実施すること

対象は `ja/development_tools/testing_framework/implementation/testdata_notation.rst` の「ウェブアプリケーションのカラム」表（現状 L553 以降）のみ。

1. **`isValidToken` 行**の「必須」列（現在は空）を `必須` にする
2. **`forwardUri` 行**の「必須」列（現在は空）を `必須` にする
3. **`requestParams` 行を表から削除する**（現在「必須」が付いている）
4. **`responseResult` 行を表から削除する**（現在は空）
5. 表の直前の導入文（現状 L551「エンティティバリデーションを除く各処理方式に共通する必須カラムは、以下のとおりである。」の後、ウェブアプリケーション表の導入文）に続けて、**「必須」の意味を1文で定義する。** 上記(a)のとおり「カラム自体を定義しておく必要があるという意味であり、値は空でもよい」旨。ページ内の4つのカラム表すべてに掛かる定義であるため、**共通カラム表の導入部に置き、各処理方式の表では繰り返さない**
6. 表の直後の地の文（現状 L615 以降、`requestParams` を説明している段落）を書き換え、**`requestParams` と `responseResult` が testShots のカラムではなく、読み込み単位内に置く予約 ID を持つ `LIST_MAP` であること**を明記する。既存の tip（リクエストパラメータは必ず記載する必要がある旨）と、行数不足時にエラーになる挙動（`TestCaseInfo#getRequestParameters`、`TestCaseInfo.java:342-351`）は、この地の文の側に残す
7. メッセージングの表の第3列見出しだけが `空の場合` になっている（現状 L681）。他3表は `必須` である。**この不統一は本書の対象外とする。触らないこと**

### この修正がマッピング違反にならない理由

`design.md` §11.7 は「事実誤り」を `must` と定めている。本件は出典に記載された事実そのものが実装と食い違っている事例であり、記述の訂正であって新規の主題内容の追加ではない。**`mapping.csv` は変更しない。**

あわせて、同種の対立が残り33ページでも起こりうるため、`design.md` §8「出典と確定設計が食い違う場合」の直後に、次の趣旨の短い項を追加すること（3〜5行、経緯は書かない）。

- 出典の記述が、検証可能な実装の挙動と食い違う場合は、実装を優先する
- 根拠として、確認した実装のファイル名・行番号・参照したコミットを `reviews/page-*.md` に記録する
- 実装を確認できない場合は `decide` としてユーザーに上げる

---

## STEP 2 — `searchResult` の欠落を補う（`must`。網羅性）

出典 `current-0081`（削除前の `05_UnitTestGuide/02_RequestUnitTest/index.rst:99-193`）は、`expectedSearch` の説明の中で「検索結果をリクエストスコープから取得する際のキーは `searchResult` である」と述べている。成果物の `expectedSearch` 行はこの記述を落としている。

実装でも `TestCaseInfo.java:72` に `DEFAULT_SEARCH_RESULT_KEY = "searchResult"` として存在し、`setSearchResultKey`（`TestCaseInfo.java:123-125`）で変更できる仕様である。

ウェブアプリケーションのカラム表の `expectedSearch` 行の説明に、リクエストスコープから取得する際の既定キーが `searchResult` である旨を追記すること。変更可能である旨まで書くかは著者判断でよい（出典に無いため、書く場合は実装を根拠として `reviews` に記録する）。

---

## STEP 3 — 太字疑似見出しを L4 見出しに格上げする（`must`）

### 確認した事実

`style.md` S-04 の「4階層目（L3のさらに下）に対応する記号（例: `^`）の使用は、確認した範囲（`tag.rst` を含む）では見つからなかった」という記述は、**確認範囲が `libraries/` 配下に限られていたことによる誤り**である。`ja/` 配下全体では `^` を下位レベルとして使う `.rst` が18ファイル存在する。うち `=` → `-` → `~` → `^` の4階層を本ページと同じ順序で使っているのは次の2ファイルである。

- `ja/application_framework/adaptors/lettuce_adaptor/redisstore_lettuce_adaptor.rst:4,20,41,48` — L4 のタイトルは `コンポーネント設定ファイルを修正する`（`:48`）・`環境設定値を修正する`（`:125`）で、**「〜する」形式**である
- `ja/biz_samples/12/index.rst:4,8,59,87`

一方、行頭太字の疑似見出しは `ja/application_framework/application_framework/libraries/` 配下に**0件**である。前例があるのは `^` 見出しの側である。

さらに、成果物は `.. _testdata_notation-column_omission:`（L398）を太字段落に付けている。見出しの無いアンカーであり、`:ref:` からタイトルを解決できない。

### 実施すること

1. `mapping/style.md` の S-04 に **L4（`^`）を追加する。** 「4階層目は見つからなかった」という記述は削除する。根拠として上記2ファイルの `file:line` を記載する（`#4` の基準に従い2件以上）。**S-04 以外の観点は変更しない。観点を8つから増やさない**
2. 成果物の**行頭太字7箇所を L4 見出し（`^`）に格上げする。** 対象は現状の L400・L508・L553・L628・L665・L677・L722。見出しタイトルは太字部分から句点を除いたものとする（例: `**カラムを省略する。**` → `カラムを省略する`）。アンダーラインの長さは既存の L3 に合わせて50文字に揃える
3. L398 の `testdata_notation-column_omission` ラベルは、格上げした見出しの直前に置かれる形になる。**削除しない**
4. 格上げした残り6見出しにも `:ref:` ラベルを付けるかは著者判断でよい。付ける場合は既存の命名（`testdata_notation-<英語snake_case>`）に揃える
5. 格上げ後、`make html` で `Title underline too short` および `Unexpected section title` が出ないことを確認する

---

## STEP 4 — `about/index.rst` の参照を見直す（ユーザー判断済み。`#9` に同梱）

`design.md` L74 が「本ページ作成後に本項の記述を見直すことを検討する」としていた宿題を、本タスクで閉じる。

1. `ja/development_tools/testing_framework/about/index.rst` の「利用目的に応じたテストデータ形式を選べる」節（現状 L24）に、**本ページへの `:ref:` 導線を追加する。** 既存の `テストデータ変換ツール` への参照は残す。第4部は変換ツールそのもの、第3部は Excel/YAML 両形式の記法という役割の違いが読者に分かる書き方にする
2. `design.md` L74 の「そちらの作成後に本項の記述を見直すことを検討する」という文を、**実施済みの結論に書き換える。** 検討の経緯は書かない（`steering.md` Rules L46・L47）
3. `about/index.rst` の他の箇所は変更しない。`mapping.csv` は変更しない

---

## STEP 6 — セクションタイトルを是正する（`must` 3件）

`style.md` のセクションタイトル規約（ページタイトル＋セクションタイトルの組だけで中身が分かること）と `design.md` §11.6 観点D（見出しと中身の一致）に照らして、3件の違反がある。

### 6-1. 「セルの値を特殊記法で記述する」（現状 L1169）— `glossary.md` 違反

`glossary.md:218` は、この概念について現行解説書の見出し `セルへの特殊な記述方法` を採らない理由を「現行解説書の見出しはExcelのセルを前提としており、YAML形式に使えない」と明記している。`glossary.md:233` も「`シート`・`セル` はExcel形式に固有であり、YAML形式には存在しない」と定めている。

成果物のタイトルは、この排除された前提をそのまま復活させている。**同じセクションの本文が「読み込んだ各セル・エントリ値を」と両形式を併記している**ことからも、タイトルだけが Excel に寄っている。

`glossary.md:240` の粒度対応（値1個 = Excel の1セルの値 / YAML のエントリ値）に従い、両形式を包含するタイトルに変更すること。`glossary.md` §5 の正表記 `特殊記法` を含める。タイトル案の決定は著者判断でよいが、`セル` を含めないこと。

### 6-2. 「テストケース一覧（testShots）を記述する」（現状 L447）— 見出しと中身の不一致

このセクションは295行あり、冒頭でまず `LIST_MAP` データタイプ全般の記法（Excel/YAML の書式、`TestSupport#getListMap`・`DbAccessTestSupport#getListMap`、ID の完全一致・先着一致・不在時の空データという解決規則）を説明している。本文自身が「この ID 解決規則は…``testShots`` 以外の用途でも共通である」と述べており、**`testShots` 固有ではない内容が `testShots` の見出しの下に埋没している。**

`LIST_MAP` の記法を探す読者は、この見出しからは到達できない。`LIST_MAP` 全般の記法を独立した L3 セクションとして切り出し、`testShots` のセクションはその後に置くこと。切り出し後の `testShots` セクションは STEP 3 の L4 見出し（`^`）を持つ構成のままでよい。

**内容の追加・削除は行わない。既存の記述の切り分けのみとする。**

### 6-3. 「テストデータファイルの構造を理解する」（現状 L19）— 見出しが中身を表していない

このセクションの中身は、外部ファイル方式を採る理由・テストクラスとテストデータファイルの1対1対応・シート名の命名（推奨と制約の区別）・Excel のセル書式の制約・1読み込み単位に3用途が共存すること・格納階層の図である。「構造を理解する」では、読者はここにファイルの単位と命名の決め方があることを判断できない。

加えて「テストデータファイル」はページタイトル `テストデータの書き方` と重複しており、組で読むと冗長である。

中身を表すタイトルに変更すること。なお **`理解する` で終わる見出しは `ja/application_framework` 配下に0件**であり、前例が無い（`扱う` は `web_service/rest/feature_details/resource_signature.rst:98,142` に2件、`確認する` は `libraries/authorization/role_check.rst:210` ほか2件あり、いずれも前例がある）。前例のある動詞形に寄せること。

本セクションは STEP 7 の統合先でもある。STEP 7 を先に適用してから、統合後の中身に照らしてタイトルを決めること。

---

## STEP 7 — 「テストの独立性を保つ」の独立見出しを廃止する（ユーザー判断済み）

### 判断

現状 L128 の L3 セクション「テストの独立性を保つ」（11行）は、**記法の仕様ではなくノウハウ**であり、`design.md` §4 が本ページに与えた役割（記法の仕様。どう書けばどう解釈されるか）にも「使用方法」という区分にも該当しない。**独立した見出しを持たせず、冒頭セクション（STEP 6-3 の対象、現状 L19）の中に注記として統合する。**（2026-08-06 ユーザー判断）

### 実施すること

1. L3 見出し `テストの独立性を保つ` とアンダーラインを削除する
2. 直前の `.. _testdata_notation-independence:` ラベル（L126）を削除する。**このラベルは本ページを含めどこからも参照されていない**ことを `grep -rn "testdata_notation-independence" ja/` で確認済みである。見出しの無いアンダーラインを残さない
3. 本文2段落と既存の tip を、冒頭セクションの末尾へ移す
4. **アドモニションの種別は `note` を使わない。** `style.md` S-06 は「`note` は FW解説書のライブラリで使用例が見つからなかったため、本解説書でも積極的には使わない」と定めており、同節の `grep` 根拠（`FW:libraries/*.rst` で0件）がある。S-06 の判定基準に従って次のとおり振り分ける
   - **実行順序に依存しないテストデータを書く必要がある**という段落 → `important`。無視するとテストが実行順序で偶発的に失敗し、原因の特定が困難になるため、S-06 の「無視すると不具合・データ不整合につながる、読者が必ず守るべき注意事項」に該当する
   - **マスタデータを共通ファイルに切り出して再利用するとよい**という段落と、マスタデータ投入ツール・マスタデータ復旧機能への既存の tip → `tip`。読まなくても機能は正しく使えるが知っておくと役立つ補足であり、S-06 の tip の基準に該当する
5. **本文の記述内容は変更しない。** 見出しの廃止と配置替え、およびアドモニション化に伴う最小限の接続のみとする。マスタデータ投入ツール・マスタデータ復旧機能への言及は `design.md` §2 の申し送りにより本ページが引き継いだものであり、削除しない
6. `mapping.csv` の `current-0175` の `dest_section` は `使用方法` のまま**変更しない。** 本ページの「使用方法」セクション内に留まるため、割当先は変わらない

---

## STEP 5 — 記録

1. `reviews/page-testdata_notation.md` に**ラウンド2**の表を追加する。既存のラウンド1の表は書き換えない
   - A-3・B-F01 は、ラウンド1の行の「対応内容」を書き換えず、ラウンド2の行として**判定が確定した旨と根拠**（本書の STEP 1・STEP 3 に記載した `file:line`、参照したコミット `e21bf67`）を記録する
   - D-4 はユーザー判断により `#9` に同梱した旨を記録する
   - STEP 1(c)（`requestParams`/`responseResult`）と STEP 2（`searchResult`）は、**観点Aが検出できなかった `must`** として新規の指摘 ID を採番して記録する
2. `checks/task-09.md` に本書の実施結果を追記する。差し戻し経緯は1〜2行のポインタにとどめる
3. `steering.md` の `#9` エントリは、user review 承認を受けるまで圧縮しない

---

## ゲート

すべて実行結果で確認し、`checks/task-09.md` に記録すること。

1. `python3 mapping/tools/verify_mapping.py` が `exit 0`、**594行 / 12,986 / 11,983 が不変**
2. `git diff a0d09aa -- .rn/20260724-ntf-yaml-support/mapping/mapping.csv .rn/20260724-ntf-yaml-support/mapping/_batch/` が**空**
3. `testdata_notation.rst` の行頭太字（`^\*\*`）が**0件**
4. `testdata_notation.rst` の `^` アンダーライン見出しが**7件**、`~` アンダーライン見出しが**10件**（STEP 6-2 の切り出しで+1、STEP 7 の廃止で-1、差し引き現状と同数）
4a. `~` 見出しのタイトルに `セル` が**含まれない**。`理解する` / `保つ` で終わる `~` 見出しが**0件**
4b. `testdata_notation-independence` ラベルが**0件**。`.. _` で始まる行の直後（空行1行を挟む）が見出しでない箇所が**0件**
4c. `.. note::` が `testdata_notation.rst` に**0件**（`style.md` S-06）
5. `testdata_notation.rst` に `requestParams` と `responseResult` が**カラム表の行として存在しない**（`* - ``requestParams``` の形で出現しない）。地の文には存在してよい
6. `testdata_notation.rst` に `searchResult` が**1箇所以上**出現する
7. `about/index.rst` の `:ref:` に `testdata_notation` が**1件**含まれる
8. `mapping/style.md` の S-04 に L4 と `^` の記載があり、根拠が2件以上ある
9. Docker でフルビルド（`-a`）し、`build succeeded` かつ警告が**既知の `db_double_submit.rst` 1件のみ**であること。ログの該当箇所を引用して記録する
10. 段落内に改行が無いこと（`steering.md` Rules L39）を、追加・変更した段落について確認する

---

## 禁止事項

- **`mapping.csv` / `_batch/*.csv` / `vocabulary.md` / `glossary.md` を変更しない**
- バッチ・メッセージング・エンティティバリデーションの3つのカラム表を変更しない（実装と一致していることを確認済み）
- メッセージング表の第3列見出し（`空の場合`）を他表に揃えない
- `style.md` の観点を8つから増やさない。S-04 以外を変更しない
- ラウンド1のレビュー記録を書き換えない。追記のみとする
- `#9` を自己判断で承認済みとして `#10` に着手しない。**user review の承認を受けるまで次ページに進まない**
- 本書で扱っていない `note`（D-3・D-5）を蒸し返さない。ラウンド1で「記録のみ」と判定済みである
- 実装を確認できなかった事項を、確認したかのように記録しない。参照したコミットは `e21bf67`、`6u3` との差分は未確認である旨を `reviews` に明記すること
