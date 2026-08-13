# レビュー記録 — 取引単体テストの設定（RESTfulウェブサービス）

対象ページ: `ja/development_tools/testing_framework/setup/deal_unit_test/rest.rst`
ページ先頭ラベル: `deal_unit_test_setting_rest`（`mapping/style.md` S-08 の表 `:355` から引用。新規考案なし）
タスク: `#22`
本文コミット: 本記録と同一のコミット

## 1. 出典（`mapping.csv` の全件）

`dest_page=取引単体テストの設定（RESTfulウェブサービス）` は3行。`csv.DictReader` で全595行を読んで完全一致で抽出した（`wc -l` は使っていない）。`DROP` 0件・計52 lines・`audience` はすべて `user`。

| `mapping_id` | `src_file` | 範囲 | `lines` | `disposition` | `dest_section` |
|---|---|---|---|---|---|
| `current-0150` | `.../05_UnitTestGuide/03_DealUnitTest/rest.rst` | `40`〜`43` | 4 | MERGE | 使用方法 |
| `current-0151` | 同上 | `46`〜`65` | 20 | MERGE | 拡張例 |
| `current-0152` | 同上 | `68`〜`95` | 28 | MERGE | 使用方法 |

出典の実物は、現行解説書が本ブランチで削除済みのため
`git show c241906:ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/rest.rst`
で読んだ（全95行）。`mapping.csv` の `note` 欄は根拠にしていない。

## 2. 実装で確認した事実

### 参照した成果物とコミット

| 成果物 | 取得元 | 参照コミット |
|---|---|---|
| `nablarch/nablarch-testing-rest` | `/home/tie303177/work/nablarch/nablarch-testing-rest` の `origin/main` | `b7729dfb980076a36ee80e88cf8ce4b038a7721d` |
| `nablarch-fw-web`（`Set-Cookie` の確認のみ） | `~/.m2/.../nablarch-fw-web/6-NEXT-SNAPSHOT/nablarch-fw-web-6-NEXT-20260327.010729-33.jar` | 上記スナップショット |
| `nablarch-testing`（`MockHttpRequest` の確認のみ） | `~/.m2/.../nablarch-testing/6-NEXT-SNAPSHOT/nablarch-testing-6-NEXT-SNAPSHOT-sources.jar` | 上記スナップショット |

`nablarch-testing-rest` のローカル作業ツリーは別ブランチ（`fix-testdataparser-usage`）にあり未追跡ファイルも持つため、**すべて `git show origin/main:<path>` で読んだ。** 作業ツリーのファイルは使っていない。パスはいずれも `src/main/java/nablarch/test/core/http/` 配下。

### 確認した事実（ページの主張と `file:line` の全件）

行番号は是正ラウンド1適用後の `rest.rst` のもの。

| # | ページの記述（`rest.rst` の行） | 実装での裏付け（`file:line`） |
|---|---|---|
| 1 | コンポーネント名は `defaultProcessor`（`:19`・`:39`・`:62`） | `SimpleRestTestSupport.java:47`（`DEFAULT_PROCESSOR_KEY = "defaultProcessor"`）、`:97`（`SystemRepository.get(DEFAULT_PROCESSOR_KEY)`） |
| 2 | 内蔵サーバへのリクエスト送信前に `processRequest` が実行される（`:19`） | `SimpleRestTestSupport.java:226`（`request = processor.processRequest(request)`）→ `:228`（`server.handle(request, context)`） |
| 3 | レスポンス受信後に `processResponse` が実行される（`:19`） | 同 `:228` の直後 `:229`（`return processor.processResponse(request, response)`） |
| 4 | 上記が `defaultProcessor` に対して起きる（`:19`） | `SimpleRestTestSupport.java:186-188`（`sendRequest(request, defaultProcessor)`）・`:210-212`（`sendRequestWithContext(request, context, defaultProcessor)`） |
| 5 | インタフェースのメソッドは `processRequest` / `processResponse` / `reset` の3つ（`:19`・`:66`） | `RequestResponseProcessor.java:17`・`:25`・`:37` |
| 6 | `RequestResponseCookieManager` はレスポンスのクッキーから `cookieName` に指定した名前のものを取り出す（`:21`） | `RequestResponseCookieManager.java:45`（`response.getHttpCookies()`）・`:47-52`（`cookie.containsKey(cookieName)` で一致したものを `cookieValue` に保持） |
| 6a | そのクッキーは `Set-Cookie` ヘッダに現れるものである（`:21`） | `HttpResponse.getHttpCookies()` はフィールド `cookies`（`List<jakarta.servlet.http.Cookie>`）を反復し `HttpCookie.fromServletCookie` で変換して返す。この `cookies` の供給元の1つが `Set-Cookie` ヘッダの解析で、`HttpResponse.scanHttpResponseHeader(String)` が `ldc_w // String Set-Cookie` → `String.equalsIgnoreCase` → `HttpCookie.fromSetCookieHeader(String)` → `addCookie(HttpCookie)` と処理する（`nablarch-fw-web` 6-NEXT スナップショットの `nablarch/fw/web/HttpResponse.class` を `javap -p -c` で確認）。実装自身も同じ語を使う: `RequestResponseCookieManager.java:55`（`logDebug("Set-Cookie header value does not contain " + cookieName + ".")`）・`NablarchSIDManager.java:5`（Javadoc「セッションIDをレスポンスの"Set-Cookie"ヘッダーから抽出し」） |
| 7 | 取り出した値を次のリクエストに設定する（`:21`） | `RequestResponseCookieManager.java:25-37`（`RestMockHttpRequest#getCookie` → `cookie.put(cookieName, cookieValue)` → `setCookie`） |
| 7a | 設定先がリクエストの `Cookie` ヘッダである（`:21`） | `RestMockHttpRequest.java:131-133`（`setCookie` は `super.setCookie` へ委譲）→ `nablarch-testing` 6-NEXT スナップショットの `nablarch/fw/web/MockHttpRequest.java:333`（`this.headers.put("Cookie", cookie.toString());`）。取得側も同 `:322`（`headers.get("Cookie")`） |
| 8 | `cookieName` はプロパティである（`:21`・`:25`・`:30`・`:49`） | `RequestResponseCookieManager.java:69-71`（`setCookieName(String)`） |
| 9 | `cookieName` 未指定だとレスポンスの処理時に例外が発生する（`:25`） | 同 `:41-43`（`processResponse` の冒頭で `IllegalStateException("cookieName must be set.")`） |
| 10 | `NablarchSIDManager` はクッキー名の初期値に `NABLARCH_SID` を持ち、`cookieName` の指定が不要（`:33`） | `NablarchSIDManager.java:8`（`extends RequestResponseCookieManager`）・`:9-11`（コンストラクタで `setCookieName("NABLARCH_SID")`） |
| 11 | `NABLARCH_SID` がセッション変数保存ハンドラのデフォルトのクッキー名である（`:33`） | 解説書側の一次情報。`ja/application_framework/application_framework/handlers/web/SessionStoreHandler.rst:127`（`:クッキー名: NABLARCH_SID`）・`:150`（`<property name="cookieName" value="NABLARCH_SID" />`）、`ja/application_framework/application_framework/libraries/session_store.rst:13`（`クッキー( NABLARCH_SID (変更可))`） |
| 12 | `ComplexRequestResponseProcessor` のプロパティ名は `processors`（`:39`・`:46`） | `ComplexRequestResponseProcessor.java:43-45`（`setProcessors(List<RequestResponseProcessor>)`） |
| 13 | 列挙した実装クラスは、リクエスト・レスポンスのいずれも記述した順に実行される（`:41`） | 同 `:16-21`（`processRequest` が `processors` を先頭から反復）・`:23-29`（`processResponse` も同じ順で反復） |
| 14 | `defaultProcessor` として登録したインスタンスはシステムリポジトリ上でシングルトンとなる（`:64`） | 解説書側の一次情報。`ja/application_framework/application_framework/libraries/repository.rst:23`（「構築されるオブジェクトは **シングルトン** となる。」）・`:130`（「生成されるインスタンスはシングルトンとなる。」）。取得側は `SimpleRestTestSupport.java:97` |
| 15 | テスティングフレームワークは各テストメソッドの開始時に `reset()` を呼び出す（`:66`） | `SimpleRestTestSupport.java:84-86`（`@Before public void setUp()` が `setupDefaultProcessor()` を呼ぶ）→ `:103`（`defaultProcessor.reset()`） |
| 16 | 内部状態を持たない場合・共有したい場合は `reset()` を何もしないメソッドにしてよい（`:66`） | `RequestResponseProcessor.java:33-35`（Javadoc「内部状態を持たない場合や、複数のテストケースをまたいで内部状態を共有したい場合は、中身が空のメソッドを実装するだけで良い。」）。`SimpleRestTestSupport.java:61-76` の `NOP_PROCESSOR` も `reset()` を空実装にしている |
| 17 | `ComplexRequestResponseProcessor` を `defaultProcessor` に登録する記述例（`:45-55`）が実在の形と一致する | `nablarch-testing-rest` 自身の `src/test/resources/unit-test.xml:53-59`（`<component name="defaultProcessor" class="...ComplexRequestResponseProcessor">` の下に `<property name="processors"><list>…`） |
| 18 | テスティングフレームワークが生成するリクエストは `RestMockHttpRequest` である（本文には書いていない。§5の未確認解消） | `SimpleRestTestSupport.java:126`（`newRequest`）・`:136`（`get`）・`:146`（`post`）・`:156`（`put`）・`:166`（`delete`）・`:176`（`patch`）がいずれも戻り値型 `RestMockHttpRequest` |

### 確認したが本文に書かなかったこと

- `defaultProcessor` が登録されていない場合は何もしない実装（`SimpleRestTestSupport.java:61-76` の `NOP_PROCESSOR`）が使われる（`:96-102`）。出典にもマッピングにも無く、これが無くてもページの手順は成立するため書かなかった。
- 対象4クラスはいずれも `@Published` を持たない（`git grep -c "@Published" origin/main -- src/main/java` のヒットは `RestMockHttpRequest` / `RestTestSupport` / `SimpleRestTestSupport` の3ファイルのみ）。**ただし承認済みの `setup/request_unit_test/rest.rst:61` が同じく `@Published` を持たない `RestTestConfiguration` を `:java:extdoc:` で参照しており、先行ページの書き方に合わせて `:java:extdoc:` をそのまま使った**（タスク指示 §3.5' に一致）。生成HTMLでリンクが javadoc サイトのURLに解決することは確認済み。

## 3. 出典と実装が食い違った点（全件・2件）

`design.md` §8「出典と実装が食い違う場合は実装を優先する」を適用した。

### 3-1. 出典 `:70-72` のXMLが構文として不正

出典は開始タグを `/>` で自己閉じしたうえで子要素と閉じタグを書いている。

```
<component name="defaultProcessor" class="nablarch.test.core.http.RequestResponseCookieManager"/>
  <property name="cookieName" value="JSESSIONID"/>
</component>
```

`xml.etree.ElementTree` でパースすると `ParseError: mismatched tag: line 3, column 2` になる。開始タグの `/` を落として是正した（`rest.rst:29-31`）。是正後は同じパーサで解析できる。

### 3-2. 出典 `:83-85` のXMLが同型で不正

`ComplexRequestResponseProcessor` の記述例の中の `RequestResponseCookieManager` が同じ形で壊れている。`:80-90` 全体をパースすると `ParseError: mismatched tag: line 6, column 8` になる。同じく開始タグの `/` を落として是正した（`rest.rst:48-50`）。出典 `:86` の `NablarchSIDManager`・`:87` の `CSRFTokenManager` は子要素を持たない自己閉じタグであり正しいので、そのままにした。

なお、是正後の形は `nablarch-testing-rest` 自身の `src/test/resources/unit-test.xml:53-59`（`origin/main`）と同じ形である。

### 3-3（撤回）. 「`Set-Cookie` ヘッダから抽出」は食い違いではない

**是正ラウンド1で撤回した。** 初版はこれを食い違いとして扱い、`Set-Cookie` / `Cookie` というヘッダ名を本文から落としていたが、その根拠が誤りだった。詳細は §5 に記録した測定の誤りを参照。

出典 `:52`（「レスポンスの `Set-Cookie` ヘッダから…リクエストの `Cookie` ヘッダに値を引き継ぐ」）・`:55`（「`Set-Cookie` ヘッダからクッキーを抽出する」）は、実装と整合する。裏付けは §2 の事実表 6a・7a に置いた。ヘッダ名は読者にとって具体的な手がかりになるため、本文 `rest.rst:21` に戻した（文面は出典の写しではなく書き直し）。

## 4. 判断

### D-1. 出典 `:51-56`（フレームワーク提供の実装2つ）を `使用方法` に置いた

**結論**: `使用方法` に置いた（`rest.rst:21`・`:33`）。`拡張例` には出典 `:46-49` と `:58-64`（自分で `RequestResponseProcessor` を実装する話）だけを置いた。

**根拠**: このページに来た読者が最初に欲しい答えは「先行するリクエストのレスポンスの値を、どうすれば次のリクエストに引き継げるか」である。`RequestResponseCookieManager` と `NablarchSIDManager` はコンポーネント設定ファイルに登録するだけで使え、クラスを書く必要がない。`design.md:200-210` の記載範囲表で `使用方法` 側の「コンポーネント設定ファイルの設定項目一覧」「設定ファイルの記述例」に当たり、`拡張例` 側の「拡張方法（クラス差し替え、独自Extension等）」には当たらない。加えて `使用方法` に置く記述例（出典 `:70-72`・`:80-90`）はこの2クラスを直接 `class` 属性に書くため、2クラスの説明を `拡張例` に置くと、記述例が後続セクションでしか説明されないクラス名を先に示すことになる。

`mapping.csv` は変更していない（`current-0151` の `dest_section` は `拡張例` のまま）。`MERGE` 行は出典の切れ目とセクションの切れ目が一致しないことを想定している。

### D-2. `使用方法` を2つのL3に分けた

**結論**: `前のレスポンスの値を次のリクエストに引き継ぐ`（`:15`）と `複数の値をまとめて引き継ぐ`（`:37`）の2つに分けた。

**根拠**: 「セッションIDだけ引き継げばよい」読者と「セッションIDとCSRFトークンの両方が要る」読者では必要な設定が違い、後者だけが `ComplexRequestResponseProcessor` を要する。目次（`.. contents::`）に両方が並ぶことで、後者の読者が自分の設定に直接辿り着ける。`style.md` S-03 の内容条件（ページタイトルとの組で中身が分かる／同一ページ内で重複しない）を満たす。

### D-3. `テストケース` を `テストメソッド` に置き換えた

**結論**: 出典 `:61`・`:62`・`:64` の `テストケース` は `テストメソッド` にした（`rest.rst:64`・`:66`）。

**根拠**: `glossary.md` §8 の `テストケース` の行が「`@Test` メソッドそのものを名指しする場合は `テストメソッド`」と定めている。`reset()` を呼ぶのは `@Before` が付いた `setUp()`（`SimpleRestTestSupport.java:84-86`）であり、JUnitのテストメソッドごとの実行を指す。テストデータの `testShots` のエントリを指す `テストショット` ではない。

### D-4. `インターフェース` → `インタフェース`（是正ラウンド1で該当語が消滅）

出典 `:47` の `インターフェース` は `glossary.md` §8 の無条件置換に従い `インタフェース` にしていた。同じ出典の `:49` は元から `インタフェース` であり、出典の中で割れていた。

**是正ラウンド1で D-8 の書き直しを行った結果、`拡張例` からクラスの役割説明そのものが消え、本ページに `インタフェース` という語は残っていない**（`grep -c` で0件）。`glossary.md` の判断自体は変えていない。

### D-5. `RESTfulウェブサービス実行基盤向けテスティングフレームワーク` を `テスティングフレームワーク` にした

出典 `:46` の長い呼称は、ページ自体がRESTfulウェブサービス専用であるため冗長になる。`glossary.md` §5.12・§8 の正表記 `テスティングフレームワーク` を使った（`rest.rst:10`・`:21`・`:62`・`:66`）。`nablarch-testing-rest` というモジュール名は、先行ページ `setup/request_unit_test/rest.rst:17-26` が既に扱っている。

### D-6. 第3部への `:ref:` を張っていない

**結論**: 張っていない。

**根拠**: 本ページのマッピング3行（出典 `:40-43`・`:46-65`・`:68-95`）にテストソースコードの実装例・テストデータの記述例は含まれない（出典のJavaコード例は `:14-36` にあり、本ページの範囲外で別のマッピング行が持つ）。導線を張るべき対象が無い。加えて第3部の `implementation/deal_unit_test/rest.rst` は未作成であり、`:ref:deal_unit_test_rest` を書くと `undefined label` の新規警告になる。

### D-7. `cookieName` が必須である旨を書き足した

出典は `cookieName` が必須かどうかを書いていない。未指定だと `processResponse` の冒頭で `IllegalStateException` が送出される（`RequestResponseCookieManager.java:41-43`）。`design.md` §8「出典が欠いている、実装上必須の設定の追記」に当たるため、1文だけ書き足した（是正ラウンド1で `important` に移した。`rest.rst:23-25`）。あわせて `NablarchSIDManager` では指定が不要であることを書いた（`NablarchSIDManager.java:9-11`。`rest.rst:33`）。

### D-8. `拡張例` をクラス説明の再掲ではなく手順として書き直した（是正ラウンド1）

**結論**: `rest.rst:62` を「独自の実装クラスを作成する。拡張するには `RequestResponseProcessor` を実装し、…`defaultProcessor` という名前で登録する。」という手順の形にした。初版にあった「リクエストとレスポンスを操作するためのインタフェースである `RequestResponseProcessor`」というクラスの役割説明は削除した。

**根拠**: `design.md:198` が「同じクラスの説明を拡張例で再掲しない。拡張例では『拡張するには〇〇を継承する』と手順として記載する」と定めている。初版は `使用方法`（`:17`）と `拡張例` で `RequestResponseProcessor` の役割を二度説明していた。役割説明は `使用方法` 側（`rest.rst:17`）に残した。承認済みの兄弟ページも同じ形である（`setup/request_unit_test/mom.rst:35`「拡張するには `TestDataConverter` を実装する。」、`setup/request_unit_test/web.rst:227`「テストデータの書き方を変える場合は、… を継承する。」— いずれも実物を開いて確認した）。

### D-9. `important` は `cookieName` の必須性に置き、`reset()` の未実装には置かなかった（是正ラウンド1）

**結論**: `rest.rst:23-25` に `important` を1件置いた。`:64` の「明示的に初期化しないと、複数のテストメソッドの間で内部状態が引き継がれてしまう」は地の文のままにした。

**根拠**: `style.md` S-06 は `important` を「無視すると不具合・非推奨機能の誤用・データ不整合につながる、読者が必ず守るべき注意事項」と定める。`cookieName` は**必ず指定しなければならず**、欠けると例外になる（`RequestResponseCookieManager.java:41-43`）。承認済みの `setup/request_unit_test/rest.rst:51-53`（`httpServerFactory` を登録していないと内蔵サーバの生成時に例外）・`setup/class_unit_test.rst:44-46`（省略すると例外が発生する）と同型で、第2部の `important` の主用途に一致する。

一方 `reset()` は「必ず守るべき」ではない。実装しない選択も正しく、`RequestResponseProcessor.java:33-35` の Javadoc が「内部状態を持たない場合や、複数のテストケースをまたいで内部状態を共有したい場合は、中身が空のメソッドを実装するだけで良い」と明示している（`SimpleRestTestSupport.java:61-76` の `NOP_PROCESSOR` が実例）。条件付きの選択肢であり、`important` の性質を満たさないため地の文に残した。

### D-10. `:31`（現 `:41`）の「記述した順に実行される」は §8 の「出典が書いていない適用範囲・副作用の追記」に当たる（是正ラウンド1）

**結論**: `design.md:479-505`「出典が書いていない適用範囲・副作用の追記」の類型として記録する。「実装上必須の設定の追記」（`design.md:465-478`）ではない。

**根拠**: これは設定項目の追加ではなく、既に本文にある `processors` プロパティの**値の書き方が結果に及ぼす意味**の説明である。`design.md` は同節で「値の書式の制約」（`reader.fwHeaderfields` の空白の扱い）を同じ類型の例として挙げており、本件はこれと同じ性質にあたる。実行順が不定だと考える読者は、順序に依存する組み合わせ（例: あるプロセッサが設定した値を後段が使う）を安全に組めない。実装は `ComplexRequestResponseProcessor.java:16-21`（`processRequest`）・`:23-29`（`processResponse`）がいずれも `processors` を先頭から反復しており、`<list>` の記述順がそのまま実行順になる。

### D-11. `processors` 未設定時の NPE は本文に書かなかった（是正ラウンド1）

**結論**: 書かない。`cookieName` の必須性は書き、`processors` については触れない非対称を意図的に残した。

**根拠**: `ComplexRequestResponseProcessor.processRequest` は `processors` が未設定（`null`）だと拡張for文の反復開始時に NPE になる（`ComplexRequestResponseProcessor.java:13` でフィールドが初期値 `null`、`:17` で反復）。ただし `processors` はこのクラスの唯一のプロパティ（`:43-45` の `setProcessors` だけ）であり、**それを設定することがこのクラスを使う手順そのもの**である。本文 `rest.rst:39` は既に「使用する実装クラスを `processors` プロパティに列挙する」と手順として指示しており、記述例（`:45-55`）も `processors` を持つ。未設定は「手順を実行しなかった」状態であり、手順に従う読者が誤りうる分岐が無い。

`cookieName` は事情が違う。同じ `RequestResponseCookieManager` を親に持つ `NablarchSIDManager` では指定が不要であり（`NablarchSIDManager.java:9-11`）、本ページはその非対称を `:33` で説明している。必須性を書かないと、読者が `RequestResponseCookieManager` でも省略できると誤りうる。`design.md:465-478` は追記を「無いとページに書かれた手順が動かない設定」に限るとしており、手順そのものに含まれる `processors` はこれに当たらない。

### D-12. リード文と本文を書き直し、段落を刻んだ（是正ラウンド1）

**結論**: リード文（`:10`）と `使用方法` 冒頭（`:17`）を書き直し、初版で1段落だった説明を `:17` / `:19` / `:21` の3段落に、`複数の値をまとめて引き継ぐ` を `:39` / `:41` の2段落に、`拡張例` を `:62` / `:64` / `:66` の3段落に分けた。

**根拠**: 初版は出典の文面が素通しになっていた。role 記法を表示テキストへ展開し、英数字（クラス名・プロパティ名）を除いた日本語だけで最長共通部分文字列を測ると、初版は `:17` と出典 `:40-41` が50字だった。書き直し後は本文の各段落と出典 `:40-95` 全体との最長共通部分文字列が最大24字（`:33` の「がセッションIDを保持する際のデフォルトのクッキー名」。クッキー名という事実そのものの記述）まで下がった。リード文と本文の重複も、初版は `:17` と39字だったが、書き直し後は最大20字（`:62`）で、既存7ページの上限（`mom.rst` の29字）の内側に収まる。

段落分けの根拠は1文あたりの可視文字数である。同じ展開方法で測ると初版は `max=142`（`:31`）だったが、書き直し後は `max=94` となり、既存ページ（`class_unit_test.rst` 103／`common.rst` 101／`request_unit_test/web.rst` 112／`request_unit_test/rest.rst` 87）の範囲に収まる。

## 5. 未確認・申し送り

### 解消済み

- **（解消）リクエストが常に `RestMockHttpRequest` か。** `RequestResponseCookieManager#processRequest` が値を設定するのは `RestMockHttpRequest` の場合のみである（`RequestResponseCookieManager.java:26`）。テスティングフレームワークが提供するリクエスト生成メソッドは、`SimpleRestTestSupport.java:126`（`newRequest`）・`:136`（`get`）・`:146`（`post`）・`:156`（`put`）・`:166`（`delete`）・`:176`（`patch`）のすべてが `RestMockHttpRequest` を返す。他の実装を作る手段は同クラスに無い。ただし `sendRequest` / `sendRequestWithContext` の引数型は `HttpRequest` であり（`:186`・`:197`・`:210`・`:224`）、利用者が自前の `HttpRequest` 実装を渡した場合はこの分岐に入らない。**フレームワークの手順に従う限り常に `RestMockHttpRequest` である**ため、本文でこの分岐に触れないという初版の判断は変えない。

### 測定の誤り（以降のタスクへの申し送り）

- **バイナリを含むディレクトリの `grep` に `-a` を付けず、0件と誤認した。** 初版 §3-3 は「jarを展開して全ファイルを `grep` した結果 `Set-Cookie` は0件」と書いたが、`grep -rl` は `.class` などのバイナリを黙って読み飛ばす。`grep -arl "Set-Cookie"` で `nablarch/fw/web/HttpResponse.class`・`nablarch/fw/web/HttpCookie.class` の2件がヒットする（再実測済み）。**jar を展開した木や `.class` を含むディレクトリを走査するときは必ず `-a` を付ける。** 「0件」を根拠に出典を否定する前に、測り方が対象を読めているかを確かめる。

### 他タスクへの申し送り

- **第3部 `implementation/deal_unit_test/rest.rst` を作るタスクへ。** そのページを作ったら、本ページから `:ref:deal_unit_test_rest`（ラベルは `style.md:372` の表で予約済み）を張ること。本ページは D-6 のとおり現時点では `:ref:` を張っていないが、これは対象ページが未作成で `undefined label` になるためであり、恒久的な判断ではない。張り先は `使用方法` の冒頭（`rest.rst:17` 付近）が適切と考える。
- **`implementation/testdata_notation.rst` を扱うタスクへ。** 同ファイル `:414` が地の文で `Cookie` を2回使っている（「必要となる `Cookie` 情報を記載した `LIST_MAP` 名。省略した場合は `Cookie` なしとして扱われる」）。本ページおよびFW解説書の地の文は `クッキー`（`ja/application_framework/application_framework/libraries/session_store.rst:13`）であり、表記が割れている。**本タスクの対象外ファイルのため是正していない。** `glossary.md` の判断を確認のうえ揃えること。

### その他

- 出典 `:1-37`（表題・リード文・取引単体テストのテストクラス例）は本ページの範囲外であり、別のマッピング行が持つ。本ページはそれらを扱っていない。
