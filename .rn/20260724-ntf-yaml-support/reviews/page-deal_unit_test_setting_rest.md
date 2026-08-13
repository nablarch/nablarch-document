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

`nablarch-testing-rest` のローカル作業ツリーは別ブランチ（`fix-testdataparser-usage`）にあり未追跡ファイルも持つため、**すべて `git show origin/main:<path>` で読んだ。** 作業ツリーのファイルは使っていない。パスはいずれも `src/main/java/nablarch/test/core/http/` 配下。

### 確認した事実（ページの主張と `file:line` の全件）

| # | ページの記述（`rest.rst` の行） | 実装での裏付け（`file:line`） |
|---|---|---|
| 1 | コンポーネント名は `defaultProcessor`（`:17`・`:31`・`:52`） | `SimpleRestTestSupport.java:47`（`DEFAULT_PROCESSOR_KEY = "defaultProcessor"`）、`:97`（`SystemRepository.get(DEFAULT_PROCESSOR_KEY)`） |
| 2 | 内蔵サーバへのリクエスト送信前に `processRequest` が実行される（`:17`） | `SimpleRestTestSupport.java:226`（`request = processor.processRequest(request)`）→ `:228`（`server.handle(request, context)`） |
| 3 | レスポンス受信後に `processResponse` が実行される（`:17`） | 同 `:228` の直後 `:229`（`return processor.processResponse(request, response)`） |
| 4 | 上記が `defaultProcessor` に対して起きる（`:17`） | `SimpleRestTestSupport.java:186-188`（`sendRequest(request, defaultProcessor)`）・`:210-212`（`sendRequestWithContext(request, context, defaultProcessor)`） |
| 5 | インタフェースのメソッドは `processRequest` / `processResponse` / `reset` の3つ（`:17`・`:54`） | `RequestResponseProcessor.java:17`・`:25`・`:37` |
| 6 | `RequestResponseCookieManager` はレスポンスに設定されたクッキーから `cookieName` に指定した名前のものを取り出す（`:19`） | `RequestResponseCookieManager.java:45`（`response.getHttpCookies()`）・`:47-52`（`cookie.containsKey(cookieName)` で一致したものを `cookieValue` に保持） |
| 7 | 取り出した値を次のリクエストのクッキーに設定する（`:19`） | 同 `:25-37`（`RestMockHttpRequest#getCookie` → `cookie.put(cookieName, cookieValue)` → `setCookie`） |
| 8 | `cookieName` はプロパティである（`:19`・`:24`・`:39`） | 同 `:69-71`（`setCookieName(String)`） |
| 9 | `cookieName` 未指定だとレスポンスの処理時に例外が発生する（`:19`） | 同 `:41-43`（`processResponse` の冒頭で `IllegalStateException("cookieName must be set.")`） |
| 10 | `NablarchSIDManager` はクッキー名の初期値に `NABLARCH_SID` を持ち、`cookieName` の指定が不要（`:27`） | `NablarchSIDManager.java:8`（`extends RequestResponseCookieManager`）・`:9-11`（コンストラクタで `setCookieName("NABLARCH_SID")`） |
| 11 | `NABLARCH_SID` がセッション変数保存ハンドラのデフォルトのクッキー名である（`:27`） | 解説書側の一次情報。`ja/application_framework/application_framework/handlers/web/SessionStoreHandler.rst:127`（`:クッキー名: NABLARCH_SID`）・`:150`（`<property name="cookieName" value="NABLARCH_SID" />`）、`ja/application_framework/application_framework/libraries/session_store.rst:13`（`クッキー( NABLARCH_SID (変更可))`） |
| 12 | `ComplexRequestResponseProcessor` のプロパティ名は `processors`（`:31`・`:36`） | `ComplexRequestResponseProcessor.java:43-45`（`setProcessors(List<RequestResponseProcessor>)`） |
| 13 | 列挙した実装クラスは、リクエスト・レスポンスのいずれも記述した順に実行される（`:31`） | 同 `:16-21`（`processRequest` が `processors` を先頭から反復）・`:23-29`（`processResponse` も同じ順で反復） |
| 14 | `defaultProcessor` として登録したインスタンスはシステムリポジトリ上でシングルトンとなる（`:54`） | 解説書側の一次情報。`ja/application_framework/application_framework/libraries/repository.rst:23`（「構築されるオブジェクトは **シングルトン** となる。」）・`:130`（「生成されるインスタンスはシングルトンとなる。」）。取得側は `SimpleRestTestSupport.java:97` |
| 15 | テスティングフレームワークは各テストメソッドの開始時に `reset()` を呼び出す（`:54`） | `SimpleRestTestSupport.java:84-86`（`@Before public void setUp()` が `setupDefaultProcessor()` を呼ぶ）→ `:103`（`defaultProcessor.reset()`） |
| 16 | 内部状態を持たない場合・共有したい場合は `reset()` を何もしないメソッドにしてよい（`:54`） | `RequestResponseProcessor.java:33-35`（Javadoc「内部状態を持たない場合や、複数のテストケースをまたいで内部状態を共有したい場合は、中身が空のメソッドを実装するだけで良い。」）。`SimpleRestTestSupport.java:61-76` の `NOP_PROCESSOR` も `reset()` を空実装にしている |
| 17 | `ComplexRequestResponseProcessor` を `defaultProcessor` に登録する記述例（`:35-45`）が実在の形と一致する | `nablarch-testing-rest` 自身の `src/test/resources/unit-test.xml:53-59`（`<component name="defaultProcessor" class="...ComplexRequestResponseProcessor">` の下に `<property name="processors"><list>…`） |

### 確認したが本文に書かなかったこと

- `defaultProcessor` が登録されていない場合は何もしない実装（`SimpleRestTestSupport.java:61-76` の `NOP_PROCESSOR`）が使われる（`:96-102`）。出典にもマッピングにも無く、これが無くてもページの手順は成立するため書かなかった。
- 対象4クラスはいずれも `@Published` を持たない（`git grep -c "@Published" origin/main -- src/main/java` のヒットは `RestMockHttpRequest` / `RestTestSupport` / `SimpleRestTestSupport` の3ファイルのみ）。**ただし承認済みの `setup/request_unit_test/rest.rst:61` が同じく `@Published` を持たない `RestTestConfiguration` を `:java:extdoc:` で参照しており、先行ページの書き方に合わせて `:java:extdoc:` をそのまま使った**（タスク指示 §3.5' に一致）。生成HTMLでリンクが javadoc サイトのURLに解決することは確認済み。

## 3. 出典と実装が食い違った点（全件・3件）

`design.md` §8「出典と実装が食い違う場合は実装を優先する」を適用した。

### 3-1. 出典 `:70-72` のXMLが構文として不正

出典は開始タグを `/>` で自己閉じしたうえで子要素と閉じタグを書いている。

```
<component name="defaultProcessor" class="nablarch.test.core.http.RequestResponseCookieManager"/>
  <property name="cookieName" value="JSESSIONID"/>
</component>
```

`xml.etree.ElementTree` でパースすると `ParseError: mismatched tag: line 3, column 2` になる。開始タグの `/` を落として是正した（`rest.rst:23-25`）。是正後は同じパーサで解析できる。

### 3-2. 出典 `:83-85` のXMLが同型で不正

`ComplexRequestResponseProcessor` の記述例の中の `RequestResponseCookieManager` が同じ形で壊れている。`:80-90` 全体をパースすると `ParseError: mismatched tag: line 6, column 8` になる。同じく開始タグの `/` を落として是正した（`rest.rst:38-40`）。出典 `:86` の `NablarchSIDManager`・`:87` の `CSRFTokenManager` は子要素を持たない自己閉じタグであり正しいので、そのままにした。

なお、是正後の形は `nablarch-testing-rest` 自身の `src/test/resources/unit-test.xml:53-59`（`origin/main`）と同じ形である。

### 3-3. 「`Set-Cookie` ヘッダから抽出」という説明

出典 `:52`・`:55` は `RequestResponseCookieManager` / `NablarchSIDManager` が「レスポンスの `Set-Cookie` ヘッダからクッキーを抽出する」と書いている。実装が読むのは `HttpResponse#getHttpCookies()` が返すクッキーのリストであり（`RequestResponseCookieManager.java:45`）、ヘッダ文字列の解析は行っていない。`getHttpCookies()` は `HttpResponse` が保持する `jakarta.servlet.http.Cookie` のリストを `HttpCookie` に変換して返すだけである（`nablarch-fw-web` 6-NEXT スナップショットの `HttpResponse.getHttpCookies()` を `javap -c` で確認）。加えて、当該jarを展開して全ファイルを `grep` した結果、文字列 `Set-Cookie` は0件だった。

そのため本文では「レスポンスに設定されたクッキーから」と書いた（`rest.rst:19`）。出典の言う挙動（レスポンスのクッキーを次のリクエストへ引き継ぐ）自体は変えていない。

## 4. 判断

### D-1. 出典 `:51-56`（フレームワーク提供の実装2つ）を `使用方法` に置いた

**結論**: `使用方法` に置いた（`rest.rst:19`・`:27`）。`拡張例` には出典 `:46-49` と `:58-64`（自分で `RequestResponseProcessor` を実装する話）だけを置いた。

**根拠**: このページに来た読者が最初に欲しい答えは「先行するリクエストのレスポンスの値を、どうすれば次のリクエストに引き継げるか」である。`RequestResponseCookieManager` と `NablarchSIDManager` はコンポーネント設定ファイルに登録するだけで使え、クラスを書く必要がない。`design.md:200-210` の記載範囲表で `使用方法` 側の「コンポーネント設定ファイルの設定項目一覧」「設定ファイルの記述例」に当たり、`拡張例` 側の「拡張方法（クラス差し替え、独自Extension等）」には当たらない。加えて `使用方法` に置く記述例（出典 `:70-72`・`:80-90`）はこの2クラスを直接 `class` 属性に書くため、2クラスの説明を `拡張例` に置くと、記述例が後続セクションでしか説明されないクラス名を先に示すことになる。

`mapping.csv` は変更していない（`current-0151` の `dest_section` は `拡張例` のまま）。`MERGE` 行は出典の切れ目とセクションの切れ目が一致しないことを想定している。

### D-2. `使用方法` を2つのL3に分けた

**結論**: `前のレスポンスの値を次のリクエストに引き継ぐ`（`:15`）と `複数の値をまとめて引き継ぐ`（`:29`）の2つに分けた。

**根拠**: 「セッションIDだけ引き継げばよい」読者と「セッションIDとCSRFトークンの両方が要る」読者では必要な設定が違い、後者だけが `ComplexRequestResponseProcessor` を要する。目次（`.. contents::`）に両方が並ぶことで、後者の読者が自分の設定に直接辿り着ける。`style.md` S-03 の内容条件（ページタイトルとの組で中身が分かる／同一ページ内で重複しない）を満たす。

### D-3. `テストケース` を `テストメソッド` に置き換えた

**結論**: 出典 `:61`・`:62`・`:64` の `テストケース` は `テストメソッド` にした（`rest.rst:54`）。

**根拠**: `glossary.md` §8 の `テストケース` の行が「`@Test` メソッドそのものを名指しする場合は `テストメソッド`」と定めている。`reset()` を呼ぶのは `@Before` が付いた `setUp()`（`SimpleRestTestSupport.java:84-86`）であり、JUnitのテストメソッドごとの実行を指す。テストデータの `testShots` のエントリを指す `テストショット` ではない。

### D-4. `インターフェース` → `インタフェース`

出典 `:47` の `インターフェース` は `glossary.md` §8 の無条件置換に従い `インタフェース` にした（`rest.rst:52`）。同じ出典の `:49` は元から `インタフェース` であり、出典の中で割れていた。

### D-5. `RESTfulウェブサービス実行基盤向けテスティングフレームワーク` を `テスティングフレームワーク` にした

出典 `:46` の長い呼称は、ページ自体がRESTfulウェブサービス専用であるため冗長になる。`glossary.md` §5.12・§8 の正表記 `テスティングフレームワーク` を使った（`rest.rst:19`・`:52`・`:54`）。`nablarch-testing-rest` というモジュール名は、先行ページ `setup/request_unit_test/rest.rst:17-26` が既に扱っている。

### D-6. 第3部への `:ref:` を張っていない

**結論**: 張っていない。

**根拠**: 本ページのマッピング3行（出典 `:40-43`・`:46-65`・`:68-95`）にテストソースコードの実装例・テストデータの記述例は含まれない（出典のJavaコード例は `:14-36` にあり、本ページの範囲外で別のマッピング行が持つ）。導線を張るべき対象が無い。加えて第3部の `implementation/deal_unit_test/rest.rst` は未作成であり、`:ref:deal_unit_test_rest` を書くと `undefined label` の新規警告になる。

### D-7. `cookieName` が必須である旨を書き足した

出典は `cookieName` が必須かどうかを書いていない。未指定だと `processResponse` の冒頭で `IllegalStateException` が送出される（`RequestResponseCookieManager.java:41-43`）。`design.md` §8「出典が欠いている、実装上必須の設定の追記」に当たるため、1文だけ書き足した（`rest.rst:19`）。あわせて `NablarchSIDManager` では指定が不要であることを書いた（`NablarchSIDManager.java:9-11`）。

## 5. 未確認・申し送り

- `RequestResponseCookieManager#processRequest` が値を設定するのは `RestMockHttpRequest` の場合のみである（`RequestResponseCookieManager.java:26`）。RESTfulウェブサービスのテストではリクエストが常に `RestMockHttpRequest` であるかどうかは確認していない。本文はこの分岐に触れていない。
- 出典 `:1-37`（表題・リード文・取引単体テストのテストクラス例）は本ページの範囲外であり、別のマッピング行が持つ。本ページはそれらを扱っていない。
