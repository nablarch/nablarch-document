# task-22 Completion Check

対象: `ja/development_tools/testing_framework/setup/deal_unit_test/rest.rst`（第2部「取引単体テストの設定（RESTfulウェブサービス）」・新規作成）

着手時の HEAD: `7494b66`。作業ツリーは着手時点でクリーン（`git status --porcelain` が0行）。
本文コミット: `c8c937e`（`ntf-yaml-support` へ push 済み。`7494b66..c8c937e`）。`reviews/page-deal_unit_test_setting_rest.md` も同一コミットに含む。本ファイル（`checks/task-22.md`）は指示どおりコミットしていない。

## §1 マッピング全件の反映対応表（母集合を先に固定。ホワイトリストで切り出さない）

母集合は `mapping.csv` の**全595行**を `csv.DictReader` で読み、`dest_page` が
`取引単体テストの設定（RESTfulウェブサービス）` に**完全一致**する行を抽出した（`wc -l` は使っていない）。
抽出条件に `mapping_id` の列挙は使っていない。

```
$ python3 -c "
import csv
rows=[r for r in csv.DictReader(open('.rn/20260724-ntf-yaml-support/mapping/mapping.csv'))]
t=[r for r in rows if r['dest_page']=='取引単体テストの設定（RESTfulウェブサービス）']
print('all',len(rows),'target',len(t),'DROP',len([r for r in t if r['disposition']=='DROP']),'lines',sum(int(r['lines']) for r in t))
for r in t: print(r['mapping_id'],r['src_body_start'],r['src_body_end'],r['lines'],r['disposition'],r['dest_section'],r['audience'])
"
all 595 target 3 DROP 0 lines 52
current-0150 40 43 4 MERGE 使用方法 user
current-0151 46 65 20 MERGE 拡張例 user
current-0152 68 95 28 MERGE 使用方法 user
```

抽出結果は**3行**（`DROP` 0件・計52 lines・すべて `audience=user`）。3行すべてが下表に現れる。
`src_file` は3行とも
`ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/rest.rst`。
出典は削除済みのため `git show c241906:<src_file>`（全95行）で実読した。

| `mapping_id` | 出典の行範囲 | `lines` | `disposition` | `dest_section` | 反映先セクション | 反映した内容と反映先の行 |
|---|---|---:|---|---|---|---|
| `current-0150` | `40`–`43` | 4 | MERGE | 使用方法 | 使用方法 > 前のレスポンスの値を次のリクエストに引き継ぐ | セッションIDやCSRFトークンなど、先行するリクエストのレスポンスとしてサーバから受け取った値を次のリクエストに含めたい場合がある旨と、その実現方法があること（`rest.rst:17` の第1文・第2文）。出典 `:42-43` の「そのような場合は以下の方法で実現できる」は、実現方法そのもの（`defaultProcessor` への登録）に接続した |
| `current-0151` | `46`–`65` | 20 | MERGE | 拡張例 | **使用方法**（出典 `:51-56`）と **拡張例**（出典 `:46-49`・`:58-64`）に分割 | (a) `:46-49` インタフェース `RequestResponseProcessor` を各アプリケーションの要件に合わせて実装する → `rest.rst:52`。(b) `:51-52` `RequestResponseCookieManager` の役割と `cookieName` → `rest.rst:19`。(c) `:54-56` `NablarchSIDManager` とデフォルトのクッキー名 `NABLARCH_SID`、変更時は `RequestResponseCookieManager` でクッキー名を明示 → `rest.rst:27`。(d) `:58-64` 内部状態・DIコンテナのシングルトン・`reset()` の呼び出しと実装方針 → `rest.rst:54`。分割の根拠は `reviews/page-deal_unit_test_setting_rest.md` §4 D-1 |
| `current-0152` | `68`–`95` | 28 | MERGE | 使用方法 | 使用方法 > 前のレスポンスの値を次のリクエストに引き継ぐ／複数の値をまとめて引き継ぐ | (a) `:68-72` `defaultProcessor` に `RequestResponseCookieManager` を設定するXML例 → `rest.rst:21-25`（XML是正あり）。(b) `:75-90` 複数使用したい場合は `ComplexRequestResponseProcessor` を使う旨とXML例 → `rest.rst:31`・`:33-45`（XML是正あり）。(c) `:92-95` `defaultProcessor` という名前で設定された実装は、リクエスト送信前に `processRequest`、レスポンス受信後に `processResponse` が実行される → `rest.rst:17` の第2文・第3文 |

### §1-2 出典の各要素とページ内の対応（落としていないことの確認）

出典 `:40-43`・`:46-65`・`:68-95` を1文ずつ辿り、対応先を全件で確認した（`§5 Method` の適用結果）。

| 出典の行 | 出典が述べていること | ページの反映先 | 照合した根拠 |
|---|---|---|---|
| `:40-42` | 取引単体テストではセッションIDやCSRFトークンなど、先行するリクエストのレスポンスとしてサーバから受け取った値を次のリクエストに含めたい場合がある | `rest.rst:17` 第1文 | 出典 |
| `:42-43` | そのような場合は以下の方法で実現できる | `rest.rst:17` 第2文（`defaultProcessor` への登録として具体化） | 出典＋`SimpleRestTestSupport.java:47`・`:97` |
| `:46-47` | テスティングフレームワークは `RequestResponseProcessor` というリクエスト・レスポンスを操作するためのインタフェースを用意している | `rest.rst:52`（`拡張例`）・`rest.rst:17`（`使用方法` 側でも実装クラスとして言及） | 出典＋`RequestResponseProcessor.java:9`・`:17`・`:25`・`:37` |
| `:49` | 各アプリケーションの要件に合わせてこのインタフェースの実装クラスを作成する | `rest.rst:52` | 出典 |
| `:51-52` | よく使われる実装として `RequestResponseCookieManager` を提供。レスポンスの `Set-Cookie` ヘッダからプロパティで指定した名前のクッキーを抽出し、リクエストの `Cookie` ヘッダに引き継ぐ | `rest.rst:19` | 出典＋`RequestResponseCookieManager.java:45`・`:47-52`・`:25-37`・`:69-71`。`Set-Cookie` の語は実装優先で改めた（`reviews` §3-3） |
| `:54-55` | セッションIDに特化した実装として `NablarchSIDManager` を提供。セッション変数保存ハンドラがセッションIDを保持する際のデフォルトのクッキー名 `NABLARCH_SID` で抽出する | `rest.rst:27` | 出典＋`NablarchSIDManager.java:8-11`、`SessionStoreHandler.rst:127`・`:150` |
| `:56` | クッキー名をデフォルトから変更した場合は `RequestResponseCookieManager` を使用しクッキー名を明示する | `rest.rst:27` 末尾 | 出典＋`RequestResponseCookieManager.java:69-71` |
| `:58-59` | `RequestResponseProcessor` は先に受信したレスポンスの値を次のリクエストに受け渡すため、内部に状態を持つことになる | `rest.rst:54` 第1文 | 出典＋`RequestResponseCookieManager.java:20`（`cookieValue` フィールド） |
| `:60-61` | DIコンテナではインスタンスがシングルトンとなるため、明示的に初期化しないと複数のテストケース間で状態が引き継がれる | `rest.rst:54` 第2文 | 出典＋`repository.rst:23`・`:130`、`SimpleRestTestSupport.java:97` |
| `:62` | これを防ぐためフレームワークはテストケースごとに `reset()` を呼び出している | `rest.rst:54` 第3文 | 出典＋`SimpleRestTestSupport.java:84-86`・`:103` |
| `:63` | 状態を引き継ぎたくない場合は `reset()` に初期化する処理を実装する必要がある | `rest.rst:54` 第4文 | 出典＋`RequestResponseProcessor.java:27-37` |
| `:64` | 状態を持たない場合・共有したい場合は `reset()` を何もしないメソッドとしてもよい | `rest.rst:54` 第5文 | 出典＋`RequestResponseProcessor.java:33-35`、`SimpleRestTestSupport.java:61-76` |
| `:66-72` | コンポーネント設定ファイルに `defaultProcessor` という名前で実装クラスを設定する（`RequestResponseCookieManager` + `cookieName`） | `rest.rst:17`・`:21-25` | 出典＋`SimpleRestTestSupport.java:47`。XMLは是正（`reviews` §3-1） |
| `:75-76` | 複数の `RequestResponseProcessor` を設定したい場合は `ComplexRequestResponseProcessor` で実現できる | `rest.rst:31` | 出典＋`ComplexRequestResponseProcessor.java:11`・`:43-45` |
| `:78-90` | `ComplexRequestResponseProcessor` のXML例（`RequestResponseCookieManager` + `NablarchSIDManager` + 独自 `CSRFTokenManager`） | `rest.rst:33-45` | 出典＋`unit-test.xml:53-59`（`origin/main`）。XMLは是正（`reviews` §3-2） |
| `:92-95` | `defaultProcessor` という名前で設定された実装は、内蔵サーバへのリクエスト送信前に `processRequest`、レスポンス受信後に `processResponse` が実行される | `rest.rst:17` 第3文 | 出典＋`SimpleRestTestSupport.java:226`・`:228`・`:229`・`:186-188`・`:210-212` |

**出典から落とした事実: 0件。** 出典 `:44-45`・`:50`・`:53`・`:57`・`:65`・`:67`・`:73-74`・`:77`・`:91` は空行・見出し下線・`.. code-block::` 行・見出し行であり、事実を持たない。

### §1-3 ページ → 典拠（逆方向の全件表）

ページ本文の各段落について、典拠を持たない記述が無いことを確認した。

| `rest.rst` の行 | 記述 | 典拠 |
|---|---|---|
| `:10`（リード文） | RESTfulウェブサービスの取引単体テストでは、レスポンスの値を次のリクエストへ引き継ぐ設定を行う。提供実装から選べるほか独自実装に差し替えられる | 出典 `:40-43`・`:51-56`（提供実装）・`:46-49`（独自実装）の要約。新規の主題は追加していない |
| `:17` | 取引単体テストで値を引き継ぎたい場合がある／`defaultProcessor` に登録すると実現できる／`processRequest`・`processResponse` の実行タイミング | 出典 `:40-43`・`:66`・`:92-95`。実装は `SimpleRestTestSupport.java:47`・`:97`・`:186-188`・`:210-212`・`:226`・`:228`・`:229` |
| `:19` | `RequestResponseCookieManager` の役割／`cookieName` プロパティ／未指定時に例外 | 出典 `:51-52`。実装は `RequestResponseCookieManager.java:45`・`:47-52`・`:25-37`・`:69-71`・`:41-43`。「未指定時に例外」は `design.md` §8「実装上必須の設定の追記」による追記（`reviews` §4 D-7） |
| `:21-25` | XML記述例（`RequestResponseCookieManager`） | 出典 `:68-72` を是正したもの（`reviews` §3-1） |
| `:27` | `NablarchSIDManager` の役割／`NABLARCH_SID`／`cookieName` 不要／変更時は `RequestResponseCookieManager` | 出典 `:54-56`。実装は `NablarchSIDManager.java:8-11`。`NABLARCH_SID` がハンドラのデフォルトである点は `SessionStoreHandler.rst:127`・`:150` |
| `:31` | 複数使用する場合は `ComplexRequestResponseProcessor` を `defaultProcessor` に登録し `processors` に列挙する／記述した順に実行される | 出典 `:75-76`。実装は `ComplexRequestResponseProcessor.java:43-45`・`:16-21`・`:23-29` |
| `:33-45` | XML記述例（`ComplexRequestResponseProcessor`） | 出典 `:78-90` を是正したもの（`reviews` §3-2）。形は `unit-test.xml:53-59` と一致 |
| `:52` | 提供実装で要件を満たせない場合は `RequestResponseProcessor` を実装し `defaultProcessor` に登録する | 出典 `:46-49`＋`:66`。実装は `RequestResponseProcessor.java:9`、`SimpleRestTestSupport.java:47` |
| `:54` | 内部状態／シングルトン／`reset()` の呼び出しと実装方針 | 出典 `:58-64`。実装は `SimpleRestTestSupport.java:84-86`・`:103`、`RequestResponseProcessor.java:27-37`、`repository.rst:23` |

**典拠を持たない記述: 0件。**

## §2 ページ先頭ラベル

`style.md` S-08「NTF解説書のページ先頭ラベル一覧」の表から引用した。**新規考案なし。**

```
$ grep -n "deal_unit_test_setting_rest" .rn/20260724-ntf-yaml-support/mapping/style.md
355:| 取引単体テストの設定（RESTfulウェブサービス） | `setup/deal_unit_test/rest.rst` | `deal_unit_test_setting_rest` |
```

ファイルパスも `design.md:818`（ツリー全体の `deal_unit_test/` 配下の `rest.rst`）・`design.md:892`（1対1対応表の `setup/deal_unit_test/rest.rst`）と一致する。
`ja/` 全体に同名ラベルが存在しないことを確認した。

```
$ grep -rn "^\.\. _\`\?deal_unit_test_setting_rest\`\?:" --include=*.rst ja/
ja/development_tools/testing_framework/setup/deal_unit_test/rest.rst:1:.. _deal_unit_test_setting_rest:
```

本ページ以外0件。

## §3 実装で確認した項目

参照コミット: `nablarch/nablarch-testing-rest` = `b7729dfb980076a36ee80e88cf8ce4b038a7721d`（`origin/main`）。
**すべて `git -C /home/tie303177/work/nablarch/nablarch-testing-rest show origin/main:<path>` で読んだ。**
ローカル作業ツリーは別ブランチ（`fix-testdataparser-usage`）にあり未追跡ファイルも持つため使っていない。
確認項目17件の全件表は `reviews/page-deal_unit_test_setting_rest.md` §2 にある。主なものは次のとおり。

| # | 主張 | 確認した `file:line` |
|---|---|---|
| 1 | コンポーネント名は `defaultProcessor` | `SimpleRestTestSupport.java:47`・`:97` |
| 2 | `processRequest` は内蔵サーバへの送信前、`processResponse` は受信後 | 同 `:226`・`:228`・`:229`。`defaultProcessor` が渡るのは `:186-188`・`:210-212` |
| 3 | `RequestResponseCookieManager` はレスポンスのクッキーから `cookieName` の名前のものを取り出し次のリクエストに設定する | `RequestResponseCookieManager.java:45`・`:47-52`・`:25-37`・`:69-71` |
| 4 | `cookieName` 未指定は例外 | 同 `:41-43`（`IllegalStateException("cookieName must be set.")`） |
| 5 | `NablarchSIDManager` のデフォルトのクッキー名は `NABLARCH_SID` | `NablarchSIDManager.java:8`・`:9-11` |
| 6 | `ComplexRequestResponseProcessor` のプロパティ名は `processors`、実行はリスト順 | `ComplexRequestResponseProcessor.java:43-45`・`:16-21`・`:23-29` |
| 7 | `reset()` は各テストメソッドの開始時に呼ばれる | `SimpleRestTestSupport.java:84-86`（`@Before setUp()`）→ `:103` |
| 8 | 是正後のXMLの形が実在する | `src/test/resources/unit-test.xml:53-59`（`origin/main`） |
| 9 | `NABLARCH_SID` がセッション変数保存ハンドラのデフォルト | `ja/.../handlers/web/SessionStoreHandler.rst:127`・`:150`、`ja/.../libraries/session_store.rst:13` |
| 10 | システムリポジトリ上のオブジェクトはシングルトン | `ja/.../libraries/repository.rst:23`・`:130` |

出典と実装が食い違ったのは**3件**（XML構文2件・`Set-Cookie` の説明1件）。全件を
`reviews/page-deal_unit_test_setting_rest.md` §3 に記載した。

## §4 Docker フルビルド

`docker build` は前タスク（`#21`）と同じ理由（pypi.org への TLS 接続が中間証明書で遮断される）で失敗するため、既存イメージ `nablarch-document-build:latest` を使用した。イメージの作成日時は `2026-08-07T09:34:28+09:00`（`docker image inspect --format '{{.Created}}'`）で、`Dockerfile`・`requirements.txt` の最終変更コミット `c241906`（2026-07-23）より新しい。

```
$ docker run --rm -v /home/tie303177/work/nablarch/nablarch-document:/root/document nablarch-document-build \
    /bin/bash -c "cd /root/document; sphinx-build -a -d _build/.doctrees/ja -b html ja _build/html"
build succeeded, 1 warning.
```

ログ中の警告行は1行のみで、既知の1件である。

```
$ grep -n "WARNING\|ERROR\|SEVERE" build.log
320:generating indices... genindex/root/document/ja/application_framework/application_framework/libraries/db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test (if the link has no caption the label must precede a section header)
```

- **新規警告0件。** `deal_unit_test/rest.rst`・`setup/index.rst` に関する警告・エラーは0件
- `Title underline too short` 0件・`Malformed table` 0件
- 生成HTML `_build/html/development_tools/testing_framework/setup/deal_unit_test/rest.html` で参照の解決を確認した
  - `:ref:` 3件 — `../../../../application_framework/application_framework/libraries/session_store.html#session-store`、`.../handlers/web/SessionStoreHandler.html#session-store-handler`、`.../libraries/repository.html#repository`
  - `:java:extdoc:` 7件 — `RequestResponseProcessor.html`、同 `#processRequest(nablarch.fw.web.HttpRequest)`、同 `#processResponse(nablarch.fw.web.HttpRequest,nablarch.fw.web.HttpResponse)`、同 `#reset()`、`RequestResponseCookieManager.html`、`NablarchSIDManager.html`、`ComplexRequestResponseProcessor.html`
  - `.. contents::` 目次の項目は「使用方法 / 前のレスポンスの値を次のリクエストに引き継ぐ / 複数の値をまとめて引き継ぐ / 拡張例 / リクエストとレスポンスの操作を実装する」の5件
  - `setup/index.html` に `deal_unit_test/rest.html">取引単体テストの設定（RESTfulウェブサービス）` が現れる

ビルドは2回実行した（1回目はログ未保存、2回目はログ保存）。**いずれの直後にも
`git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行して戻した。** 2回とも `sphinx.mo` は再生成されており、戻さなければ通算8回目・9回目の混入になっていた。

**パスの訂正（タスク指示への申し送り）**: レビュー役の指示書は戻す対象を `ja/locales/...` と書いているが、実物はリポジトリ直下の `locales/ja/LC_MESSAGES/sphinx.mo` である。`git status --porcelain` で再生成されるパスを実測して確認した。`ja/locales/` は存在しない。

## §5 差分の範囲（`commit & push` の直前）

母集合は `git status --porcelain` の**全件**。`git diff` は未追跡ファイルを出さないため使っていない。

```
$ git status --porcelain
 M ja/development_tools/testing_framework/setup/index.rst
?? .rn/20260724-ntf-yaml-support/checks/task-22.md
?? .rn/20260724-ntf-yaml-support/reviews/page-deal_unit_test_setting_rest.md
?? ja/development_tools/testing_framework/setup/deal_unit_test/
```

| # | パス | 状態 | 予定 | 判定 |
|---|---|---|---|---|
| 1 | `ja/development_tools/testing_framework/setup/index.rst` | ` M` | `toctree` に `deal_unit_test/rest` を1行追加 | 予定どおり |
| 2 | `ja/development_tools/testing_framework/setup/deal_unit_test/`（配下は `rest.rst` の1ファイルのみ） | `??` | 新規作成 | 予定どおり |
| 3 | `.rn/20260724-ntf-yaml-support/reviews/page-deal_unit_test_setting_rest.md` | `??` | 新規作成 | 予定どおり |
| 4 | `.rn/20260724-ntf-yaml-support/checks/task-22.md` | `??` | 新規作成（**コミットしない**） | 予定どおり |

**予定外のファイル0件。** `locales/ja/LC_MESSAGES/sphinx.mo` は現れていない（各ビルド直後に戻した）。

## §6 ゲート1〜9 の実行結果

| ゲート | 内容 | 結果 | 証拠 |
|---|---|---|---|
| 1 | `git status --porcelain` の全件が意図した差分だけ | PASS | §5 の全件表。4件すべて予定どおり、予定外0件 |
| 2 | `ja/` の差分は `setup/deal_unit_test/rest.rst`（新規）と `setup/index.rst`（1行追加）の2ファイルのみ | PASS | `git status --porcelain -- ja/` が上記2エントリのみ。`setup/deal_unit_test/` 配下は `rest.rst` の1ファイルのみ。`git diff -- ja/development_tools/testing_framework/setup/index.rst` は `+   deal_unit_test/rest` の1行追加のみ |
| 3 | `mapping.csv`・`mapping/_batch`・`volume.md`・`glossary.md`・`design.md` に差分が無い | PASS | `git status --porcelain -- .rn/20260724-ntf-yaml-support/mapping/mapping.csv .rn/20260724-ntf-yaml-support/mapping/_batch .rn/20260724-ntf-yaml-support/volume.md .rn/20260724-ntf-yaml-support/mapping/glossary.md .rn/20260724-ntf-yaml-support/design.md` が0行 |
| 4 | `verify_mapping.py` が 595行 / 12,986 / 11,983 で exit 0 | PASS | `Loaded 595 rows from mapping.csv` / `lines total (all rows): 12986` / `lines total (excluding DROP): 11983` / `OK: no errors` / `exit=0` |
| 5 | `既定` が `about`／`setup`／`implementation`／`tools` 配下に0件 | PASS | `grep -ro "既定" ja/development_tools/testing_framework/{about,setup,implementation,tools} \| wc -l` → `0` |
| 6 | 新ページが `デフォルト設定` の語を作っていない | PASS | `grep -o "デフォルト設定" ja/.../deal_unit_test/rest.rst \| wc -l` → `0`。あわせて `テストケース` 0件・`インターフェース` 0件・`既定` 0件 |
| 7 | 見出し下線を実測則で再計算（L1 `max(50, 表示幅)` / L2 50固定 / L3 `max(49, 表示幅)`）。表示幅は `unicodedata.east_asian_width` | PASS | L1「取引単体テストの設定（RESTfulウェブサービス）」幅45→下線50 OK。L2「使用方法」幅8→50 OK、「拡張例」幅6→50 OK。L3「前のレスポンスの値を次のリクエストに引き継ぐ」幅44→49 OK、「複数の値をまとめて引き継ぐ」幅26→49 OK、「リクエストとレスポンスの操作を実装する」幅38→49 OK（6件すべて実測一致） |
| 8 | Docker フルビルド（`-a`）で新規警告0件 | PASS | §4。`build succeeded, 1 warning.`。警告は既知の `db_double_submit.rst:108` 1件のみ |
| 9 | 貼り付けたXMLが構文として妥当 | PASS | `xml.etree.ElementTree.fromstring` でコードブロック2件をパース。`line 21: PARSE OK (3 lines)` / `line 33: PARSE OK (11 lines)`。是正前の出典 `:70-72` は `ParseError: mismatched tag: line 3, column 2`、`:80-90` は `ParseError: mismatched tag: line 6, column 8` |

### §6-2 その他の規約チェック

| 項目 | 結果 | 証拠 |
|---|---|---|
| `style.md` S-09 目次 | OK | `rest.rst:6-8` にタイトル下線（`:4`）の直後 `.. contents:: 目次` / `:depth: 3` / `:local:` |
| `style.md` S-02 リード文の位置 | OK | `rest.rst:10`。目次（`:6-8`）の直後、最初のL2見出し `使用方法`（`:12`）より前。「ここでは、」で始まっていない |
| `style.md` S-02 第2部のセクション順 | OK | `使用方法`（`:12`）→ `拡張例`（`:47`）。`機能概要` は置いていない（作成済み第2部7ページと同じ形） |
| `style.md` S-03 セクションタイトル | OK | L3 3件すべて動詞終止形「〜する／〜引き継ぐ」。同一ページ内で重複なし。`概要`・`設定する` のような無情報語なし |
| `style.md` S-04 下線記法 | OK | `=`→L1、`-`→L2、`~`→L3。L4なし |
| `style.md` S-05 コードブロック | OK | `.. code-block:: xml` 2件。いずれも内容が2字下げ。無指定の `code-block::` は0件 |
| `style.md` S-07 表の記法 | OK | 表を持たない（simple table・`list-table`・grid table いずれも0件） |
| `style.md` S-10 Excel/YAML の書き分け | 該当なし | 本ページはテストデータの記述方法を扱わないため、形式差に触れる箇所が0件 |
| 段落内で改行しない | OK | コードブロック外で連続する本文行0件（機械判定） |
| `design.md` §3 記載範囲 | OK | テストソースコードの実装例0件・テストデータの記述例0件。コンポーネント設定ファイルの記述例2件と拡張方法のみ |

## Completion Criteria

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| `mapping.csv` の当該 `dest_page` の全行（3行）が反映されている | OK | `csv.DictReader` で全595行から `dest_page` 完全一致で抽出した3行（`DROP` 0件・52 lines）が §1 の表に全件現れ、それぞれ反映先の行番号を持つ。出典の各要素との突合は §1-2（落とした事実0件）、逆方向は §1-3（典拠を持たない記述0件）。**是正ラウンド1で出典 `:52`・`:55` の `Set-Cookie` / `Cookie` というヘッダ名を本文 `rest.rst:21` に戻したため、反映漏れはさらに減っている**（初版はこれを「出典と実装の食い違い」と誤認して落としていた。撤回の記録は `reviews` §3-3） | | |
| 当該 `dest_page` のマッピング行が全件、ページのどこに反映されたかの対応表が `checks/task-22.md` にある | OK | §1 の表（`mapping_id` ごとに反映先セクションと反映内容・反映先の行）。3行すべて記載。**是正ラウンド1で本文の行番号が動いたため、§1・§1-2・§1-3・§3・§5・§6 に書かれた `rest.rst:NN` は初版時点の値である**（本ファイルは指示により Completion Criteria と Overall Verdict の `Self-check` 以外を書き換えていない）。是正後の行番号は `reviews/page-deal_unit_test_setting_rest.md` §2 の事実表が全件を持つ | | |
| 全件表を求める項目が、ゲートの実行順の先頭に置かれている（母集合をホワイトリストで切り出していない） | OK | 全件表は本ファイルの冒頭 §1 にあり、他のすべての節より前に置いた。抽出条件は `dest_page` の完全一致のみで `mapping_id` の列挙は使っていない。§5 の差分の全件表も `git status --porcelain` を母集合にしている。是正ラウンド1でも母集合は `git status --porcelain` の全件（3エントリ: `reviews/page-*.md` `M`・`setup/deal_unit_test/rest.rst` `M`・`checks/task-22.md` `??`） | | |
| 未対応の指摘が残っていない、または残す判断とその理由が記録されている | OK | 判断は**12件**（D-1〜D-12）を `reviews/page-deal_unit_test_setting_rest.md` §4 に理由・根拠つきで記録。是正ラウンド1で D-8（拡張例を手順に書き直し）・D-9（`important` を `cookieName` に置き `reset()` に置かない判断）・D-10（「記述した順に実行される」は `design.md` §8 の適用範囲・副作用の類型）・D-11（`processors` の NPE を本文に書かない判断）・D-12（リード文と本文の書き直しと段落分け）を追加。§5 の未確認1件（リクエストが常に `RestMockHttpRequest` か）は `SimpleRestTestSupport.java:126`・`:136`・`:146`・`:156`・`:166`・`:176` の戻り値型で解消済み。申し送りは3件（`grep -a` の測定の誤り・第3部からの `:ref:deal_unit_test_rest`・`testdata_notation.rst:414` の `Cookie` 表記） | | |
| `make html`（Docker フルビルド）が当該ページについてエラーを出さない | 未再実行 | 初版時点では §4 のとおり `build succeeded, 1 warning.`（既知の `db_double_submit.rst:108` 1件のみ、新規0件）。**是正ラウンド1の変更後は Docker ビルドを実行していない**（本ラウンドの指示で実行を禁じられており、コーディネータが実施する）。是正後の本文で新たに増えた RST 構文要素は `.. important::` 1件のみで、`:ref:` 3件・`:java:extdoc:` 7件の対象は初版から変わっていない | | |
| ゲート1〜9 が実行結果で記録されている | OK | §6 の表は初版のゲート結果。**是正ラウンド1のゲート1〜9 は本ラウンドのサマリで報告した。** 内訳: 1 PASS（`git status --porcelain` 3エントリすべて予定どおり）／2 PASS（`ja/` の差分は `setup/deal_unit_test/rest.rst` の1ファイルのみ）／3 PASS（保護対象5パスの差分0件）／4 PASS（`Loaded 595 rows` / `12986` / `11983` / `OK: no errors` / exit 0）／5 PASS（`既定` 0件）／6 PASS（`デフォルト設定`・`テストケース`・`インターフェース` すべて0件）／7 PASS（見出し6件すべて実測則と一致。L1 幅45→50、L2 幅8→50・幅6→50、L3 幅44→49・幅26→49・幅38→49）／8 PASS（`xml.etree.ElementTree.fromstring` でXMLブロック2件をパース成功）／9 PASS（段落内改行0件）。**8 の Docker ビルドは本ラウンドの対象外**（上記のとおり実行禁止） | | |

## Overall Verdict

- Self-check: OK（是正ラウンド1を適用。是正1〜6 をすべて処理し、判断は D-1〜D-12 として `reviews` §4 に、申し送り3件と解消済み1件を同 §5 に記録した。出典と実装の食い違いは初版の3件から**2件**（XML構文のみ）に減った — `Set-Cookie` の1件は `grep` に `-a` を付けなかった測定の誤りに基づく誤認で、撤回して本文にヘッダ名を戻した。ゲート1〜9 のうち Docker ビルド以外はすべて PASS。**Docker ビルドは本ラウンドの指示により未実行であり、この点は未確認である。**）
