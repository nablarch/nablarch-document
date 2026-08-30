# `#48` 指示書 — 図の作成（PlantUML 21枚）・既存画像の処置・README「図の作成方法」

宛先: 解説書（`nablarch-document`）担当CC

**性格**: 作る図の一覧（§3）と規則（§2）は user 承認済み（2026-08-30）で確定している。探索は不要。
判断が要るのは「図に必要な事実が本文に無い」と分かったときだけで、そのときは本文を足さずに止めて報告する（§6）。
**4観点レビューは回さない**（user 確認 2026-08-30。図の中身は承認済みの表で決まり、図と本文・実装の整合は
ディレクターが `.puml` をピンと本文に突き合わせて全件検証する）。

---

## 0. 渡すときの文面

```
図の作業を依頼します。指示書 ntf-doc-48-figures.md に、作る図21枚・既存画像の処置・README の規則が
確定済みで載っています。探索は不要です。

作業場: /home/tie303177/work/nablarch/nablarch-document（ブランチ ntf-yaml-support、e8f0602f）
指示書: .rn/20260724-ntf-yaml-support/ntf-doc-48-figures.md（origin/ntf-yaml-support に入っています）

解説書の本文は a6da1f6 を参照点にしてください（ja/ は a6da1f6 から HEAD まで無変更です）。
実装は指示書 §1 のピンを git show <pin>:<path> で読み、作業ツリーを読まないでください。

指示書の §2〜§9 に従ってください。特に次を落とさないでください。
- 図は本文の可視化です。本文に無い事実を図に入れないでください（§6）。足りなければ止めて報告
- .puml と .rst に解説書への参照（file:line・節見出し・リポジトリ名）を書かないでください
- 1ページ分（図・.rst・旧画像の削除）を1コミットにし、都度 push してください（§7）
- 完了したら §10 の形で報告し、停止してください
```

---

## 1. やること

| 誰が | 何を |
|---|---|
| CC（本指示書） | README「図の作成方法」の追記（§2）／`.puml` 21本と `.png` 21枚の作成（§3・§5）／`.rst` への `.. image::` 挿入と旧画像の処置（§3・§4）／本文の逐語差し替え（§6）／記録（§7）／完了条件の実測（§8）／報告（§10） |
| ディレクター | 各 `.puml` を本文と実装のピンに突き合わせる独立検証・`.png` の再生成一致・Docker ビルドの再実行 |

### 参照点（ピン）

| 対象 | ピン | 読み方 |
|---|---|---|
| 解説書 `ja/` | `a6da1f6`（HEAD `e8f0602f` と `ja/` は同一。`git diff --stat a6da1f6 HEAD -- ja/` が空） | 本指示書の `file:line` はすべてこのピン。パスは `ja/development_tools/testing_framework/` からの相対 |
| `nablarch-testing` | `3c4bd2a`（ブランチ `convert-testdata-excel-to-text`） | `git -C /home/tie303177/work/nablarch/nablarch-testing show 3c4bd2a:<path>` |
| `nablarch-testing-rest` | `ec718a2`（ブランチ `fix-testdataparser-usage`） | 同上 `nablarch-testing-rest` |
| `nablarch-testing-junit5` | `c06ebe8`（ブランチ `worktree-fix-resolveTestRules`） | 同上 `nablarch-testing-junit5` |
| `nablarch-testing-converter` | `d611bec`（ブランチ `ntf-test-data-converter`） | 同上 `nablarch-testing-converter` |

実装のピンは、図に書くクラス名・継承関係が実在することの確認に使う。**図の内容は本文から起こす**（§6）。

### 規則（全部に掛かる）

- 置き場所はページと同じ階層の `images/<ページ名>/`（現行どおり。`design.md` §13「画像の配置」）
- 原本 `<name>.puml` と生成物 `<name>.png` を同じディレクトリに同名で置く。**両方コミットする**（Docker ビルドは図を生成しない。ビルド環境は触らない）
- 名前は `<見せるもの>_<種類>`。英小文字 snake_case・ASCII のみ。種類は `class`・`sequence`・`layout`・`components`・`flow` の5つに固定。日本語・camelCase・連番は使わない
- **同種ページの同じ図は同じファイル名**（`request_test_components.png` は `web/`・`rest/`・`batch/`・`mom/` で同名、`execute_sequence.png` は `web/`・`batch/`・`mom/` で同名）
- 画面キャプチャ13件は触らない。名前も変えない
- `.puml`・`.rst` に解説書への参照（`file:line`・節見出し・`nablarch-document`）を書かない。根拠は `checks/task-48.md` に書く（§7）
- 禁止語（`mapping/glossary.md` §8「対応表」の左列の語）を `.puml` に書かない。正表記は同表の右列（例: 「自動テストフレームワーク」→「テスティングフレームワーク」、「NAF」は本文どおり「Nablarch Application Framework」）

---

## 2. README「図の作成方法」（逐語）

リポジトリ直下 `README.md` の `## ドキュメントのビルド方法` の節の直後（`## textlintの実行方法` の前）に、次を挿入する。

````markdown
## 図の作成方法
図はPlantUMLで作成します。原本（`.puml`）と生成物（`.png`）を、ページと同じ階層の`images/<ページ名>/`に同じ名前で置き、両方をコミットします。ドキュメントのビルドは図を生成しません。

### 前提
* Java 17
* plantuml.jar（`https://github.com/plantuml/plantuml/releases/download/v1.2025.4/plantuml-1.2025.4.jar`）
* 日本語フォント Noto Sans JP（`https://github.com/notofonts/noto-cjk/raw/main/Sans/Variable/TTF/Subset/NotoSansJP-VF.ttf`をフォントディレクトリに置き、`fc-cache -f`を実行する）

Graphvizは不要です。各`.puml`の先頭に`!pragma layout smetana`と`skinparam defaultFontName "Noto Sans JP"`を書きます。

### 生成
```bash
java -Djava.awt.headless=true -jar plantuml.jar -tpng -charset UTF-8 <ディレクトリ>/*.puml
```

### 規則
* ファイル名は`<見せるもの>_<種類>`。英小文字のsnake_case・ASCIIのみ。種類は`class`・`sequence`・`layout`・`components`・`flow`の5つ
* 同じ種類のページの同じ図は同じファイル名にする（例: `implementation/request_unit_test/images/{web,batch,mom}/execute_sequence.png`）
* 図は本文の可視化であり、本文に無い事実を入れない
* 用語は`.rn/20260724-ntf-yaml-support/mapping/glossary.md`の正表記に従う
* 画面キャプチャ（`.png`のみ）は本規則の対象外
````

---

## 3. 作る図（21枚）

置く位置の `file:line` は `a6da1f6`。「置く位置」に既存の `.. image::` があるものは、その行を新しい図に差し替える（旧画像は §4 で削除）。
「導入文」欄が「無し」の図は、直前の段落が図の内容を述べているので導入文を置かない。「有り」の図は逐語を §6 に置く。
**図に入れる要素は「見せるもの」欄の語だけ**で、いずれも「本文」欄の行に現れる語である。クラス名は本文に現れるものだけを書く。

| # | ページ | ファイル名 | 置く位置 | 導入文 | 見せるもの | 本文 |
|---|---|---|---|---|---|---|
| 1 | `about/index.rst` | `images/index/architecture_components` | 「アーキテクチャ」（`:104`）の段落 `:106` の直後 | 無し | テストクラス→テスト対象クラス（直接呼び出してテストする）／テスト対象クラス→Nablarch Application Framework（介して動作する）／Nablarch Application Framework←コンポーネント設定ファイル・環境設定ファイル（読み取る）／テストデータ→テスティングフレームワーク→テストクラス。本番同等の基盤の上でテストできることが1枚で分かる構図 | `:106` |
| 2 | `about/index.rst` | `images/index/test_support_class` | 図1の直後 | 有り（§6 (f)） | 利用者が継承するサポートクラスの系譜。`TestEventDispatcher`（抽象）配下の13クラス（`nablarch-testing` 11・`nablarch-testing-rest` 2。後者はステレオタイプで所属モジュールを示す）の継承関係。どのテストがどれを継承するかを `note` で添える（ウェブ＝`BasicHttpRequestTestTemplate`、RESTful＝`RestTestSupport`／`SimpleRestTestSupport`、バッチ＝`BatchRequestTestSupport`、MOM受信＝`MessagingRequestTestSupport`／`MessagingReceiveTestSupport`、コンポーネント単体＝`DbAccessTestSupport`、エンティティ単体＝`EntityTestSupport`）。付録の `p1_class.puml` が同じ内容の見本 | `:106`。継承関係の実在は `nablarch-testing@3c4bd2a` の各クラスの `extends` 句（`TestSupport.java:27`・`DbAccessTestSupport.java:36`・`EntityTestSupport.java:48`・`HttpRequestTestSupport.java:72`・`AbstractHttpRequestTestTemplate.java:62`・`BasicHttpRequestTestTemplate.java:15`・`StandaloneTestSupportTemplate.java:21`・`BatchRequestTestSupport.java:26`・`MessagingRequestTestSupport.java:48`・`MessagingReceiveTestSupport.java:13`・`IntegrationTestSupport.java:16`。いずれも `src/main/java/nablarch/test/` 配下）と `nablarch-testing-rest@ec718a2` の `SimpleRestTestSupport.java:39`・`RestTestSupport.java:26`（`src/main/java/nablarch/test/core/http/`）。どのテストがどれを継承するかは各ページ（`implementation/request_unit_test/web.rst:35`・`rest.rst:17`・`batch.rst:17`・`mom.rst:17`、`implementation/class_unit_test/component.rst`・`entity.rst` の「主なクラスとリソース」） |
| 3 | `setup/common.rst` | `images/common/send_sync_testdata_layout` | `:170` の段落（「…それぞれについて後述する。」）の直後、`.. tip::`（`:172`）の前 | 有り（§6 (g)） | ベースディレクトリ（`sendSyncTestData`）配下の読み込み単位を両形式で対比。Excel: `<ベースディレクトリ>/<リクエストID>.xlsx`（拡張子は `fileExtensions` の設定による）の `message` シート／YAML: `<ベースディレクトリ>/<リクエストID>/message.yaml` | `:166`-`:170`・`:219`・`:264`、`implementation/deal_unit_test/mom.rst:72` |
| 4 | `setup/junit5_extension.rst` | `images/junit5_extension/extension_class` | `:20` の段落（「インジェクションは…」）の直後、`.. tip::`（`:22`）の前 | 無し | 並行する2つの継承系列と、その間の生成・注入。Support 系列: `TestSupport` ← `CustomTestSupport`／Extension 系列: `TestEventDispatcherExtension` ← `TestSupportExtension` ← `CustomTestSupportExtension`。`createSupport()` が `CustomTestSupport` のインスタンスを生成し、テストクラスのフィールドへインジェクションする関係。`CustomTestSupport`・`CustomTestSupportExtension` は本文の拡張例の名前（利用者が作るクラスであることを `note` で示す） | `:16`-`:20`・`:227`-`:231`・`:241`・`:262`・`:271`。実在は `nablarch-testing-junit5@c06ebe8` の `src/main/java/nablarch/test/junit5/extension/TestSupportExtension.java:14`（`extends TestEventDispatcherExtension`） |
| 5 | `setup/master_data_restore.rst` | `images/master_data_restore/restore_flow` | `:30` の段落の直後（現行 `:32` の位置） | 無し | テストメソッド1回分の流れ。コンポーネント設定ファイルから監視対象テーブル名一覧を取得→テストメソッドを実行（SQLログを監視）→監視対象テーブルを変更する SQL 文が発行されたか（分岐）→はい: 変更があったテーブルのレコードをすべて削除→バックアップ用スキーマからテーブル単位でコピー／いいえ: 何もしない。付録の `p5_activity.puml` が見本 | `:26`-`:32` |
| 6 | `implementation/class_unit_test/component.rst` | `images/component/select_sequence` | 現行 `:153` | 無し | 参照系の手順1〜3を、テストクラス・テスティングフレームワーク・テスト対象クラス・テストデータ・データベースの間の時間順で示す | `:147`-`:153` |
| 7 | `implementation/class_unit_test/component.rst` | `images/component/update_sequence` | 現行 `:191` | 無し | 更新系の手順1〜4（コミットを含む）を同じ参加者で示す | `:176`-`:191` |
| 8 | `implementation/request_unit_test/web.rst` | `images/web/request_test_components` | `:42` の段落（「…同一の JVM 上で動作する。」）の直後 | 無し | 同一 JVM の枠の中に、テストクラス（`BasicHttpRequestTestTemplate` を継承）→内蔵サーバ（Nablarch Application Framework→テスト対象クラス（Action））→データベース。テストデータ→テストクラス。内蔵サーバ→HTMLダンプ（出力） | `:13`-`:44` |
| 9 | `implementation/request_unit_test/web.rst` | `images/web/execute_sequence` | `:98` の箇条書きの直後 | 無し | テストクラスの `execute()` 1回の手順。`setUpDb` の投入（繰り返しの前に1回）→テストショット一覧の取得→ショットごとに: 準備データの投入→`ExecutionContext`・`HttpRequest` の生成→トークンの設定（`isValidToken` が `true` の場合）→`beforeExecute`→リクエストの送信→実行結果の検証→`afterExecute`。参加者はテストクラス（スーパクラス）・テストデータ・データベース・テスト対象（内蔵サーバ）。付録の `p2_sequence.puml` が見本 | `:87`-`:98`・`:191`-`:200` |
| 10 | `implementation/request_unit_test/web.rst` | `images/web/mail_request_components` | 現行 `:531` | 無し | 業務アプリケーション→メール送信要求の API→メール送信要求テーブル・メール送信先テーブル・メール添付ファイルテーブル→（メール送信バッチ→メールの送信）。リクエスト単体テストで確認する範囲が3テーブルまでであることを枠で示す | `:529`-`:533` |
| 11 | `implementation/request_unit_test/web.rst` | `images/web/html_dump_layout` | 現行 `:539` | 無し | ダンプディレクトリ配下の構成。`<ダンプディレクトリ>/<テストクラス名>/読み込み単位の名前_Shot番号_説明.html`、同じディレクトリに HTML リソース（スタイルシート・画像）、既存時のバックアップ `<ダンプディレクトリ名>_bk` | `:541`-`:543` |
| 12 | `implementation/request_unit_test/rest.rst` | `images/rest/request_test_components` | `:17` の段落の直後 | 無し | テストクラス（`RestTestSupport` ← `SimpleRestTestSupport` のどちらかを継承）。`SimpleRestTestSupport` が内蔵サーバを保持、`RestTestSupport` が `DbAccessTestSupport` を保持。内蔵サーバ上の Nablarch Application Framework→テスト対象の Action→テーブル。テストデータ（期待値）→照合 | `:13`-`:17`・`:93` |
| 13 | `implementation/request_unit_test/batch.rst` | `images/batch/request_test_components` | `:17` の段落の直後、`.. tip::`（`:19`）の前 | 無し | テストクラス（`BatchRequestTestSupport` を継承）→テスト用のメインクラス `MainForRequestTesting`→Nablarch Application Framework→テスト対象のバッチ。準備データの投入と結果の確認: テーブル＝`DbAccessTestSupport`、ファイル＝`FileSupport`。テストデータ→テストクラス | `:13`-`:21` |
| 14 | `implementation/request_unit_test/batch.rst` | `images/batch/execute_sequence` | `:173` の段落の直後 | 無し | テストショット1件の手順。入力データの準備（データベースへの準備データの投入・入力ファイルの作成・期待するログの登録・要求電文の期待値の登録）→メインクラスの起動（`MainForRequestTesting`）→出力結果の確認（ステータスコード・データベース・出力ファイル・要求電文・ログ） | `:167`-`:173`・`:177`-`:184` |
| 15 | `implementation/request_unit_test/mom.rst` | `images/mom/request_test_components` | `:17` の段落の直後 | 無し | メッセージ受信。テストクラス（`MessagingRequestTestSupport`、応答不要受信はそのサブクラス `MessagingReceiveTestSupport`）→`MainForRequestTesting`→Nablarch Application Framework→テスト対象のアプリケーション。準備データの投入と結果の確認: データベース＝`DbAccessTestSupport`、キュー＝`MQSupport`。テストデータ→テストクラス | `:13`-`:17` |
| 16 | `implementation/request_unit_test/mom.rst` | `images/mom/execute_sequence` | `:178` の段落の直後 | 無し | メッセージ受信のテストショット1件の手順。入力データの準備（テストデータから作成した要求電文を受信キューへ PUT）→メインクラスの起動（`MainForRequestTesting`）→出力結果の確認（応答電文・データベース・ログ） | `:178`・`:186`-`:194` |
| 17 | `implementation/request_unit_test/mom.rst` | `images/mom/send_sync_sequence` | 現行 `:39`（`:41` の文と `:43` の画像も除く。§6 (d)） | 無し（`:37` の文がそのまま導入文） | 同期応答メッセージ送信の1〜5。テスティングフレームワークが Nablarch Application Framework を起動→Nablarch Application Framework が Action の入力を渡す→Action が同期応答メッセージ送信を実行→テスティングフレームワークが要求電文をアサート（キューに PUT しない）→応答電文を生成して Action へ返す（キューから GET しない）。凡例は PlantUML の `legend` で図の中に置く。キューを使わないことを `note` で示す | `:30`・`:37`-`:51` |
| 18 | `implementation/deal_unit_test/mom.rst` | `images/mom/send_sync_mock_components` | 現行 `:21`（`:19`-`:27` を導入文1文と図1枚に置き換える。§6 (a)） | 有り（§6 (a)） | 上下2段の対比。本番: 画面（ウェブアプリケーション）→Nablarch Application Framework→本番用のメッセージングプロバイダ→送信キュー・受信キュー。取引単体テスト: 画面→Nablarch Application Framework→モックアップクラス（同じコンポーネント名で登録）→テストデータ（応答電文）。キューへ接続しないことを示す | `:17`・`:31`・`:35` |
| 19 | `implementation/testdata_notation.rst` | `images/testdata_notation/testdata_layout` | `:28` の段落の直後、`:30` の前（§6 (e) で `:46`-`:51`・`:85`-`:90`・`:119`-`:124` を除く） | 無し（`:28` が導入文） | 両形式の対比。テストクラス `FooTest.java` ⇄ Excel: 同名の1ファイル `FooTest.xls`／YAML: 同名の1ディレクトリ `FooTest/`。読み込み単位 ⇄ Excel: シート `case01`・`case02`／YAML: ファイル `case01.yaml`・`case02.yaml`。読み込み単位の中にデータブロック（データタイプ＋識別子の値）、その中にレコード定義・フィールド・データ。付録の `p3_layout.puml` が見本（4段目を足す） | `:26`-`:28`・`:44`-`:51`・`:83`-`:90`・`:98`・`:117`-`:124` |
| 20 | `tools/request_data_tool.rst` | `images/request_data_tool/tool_components` | 現行 `:90` | 無し（`:88` が導入文） | 全体の流れ。リクエスト単体テストの実行→HTMLダンプ→本ツール（HTMLダンプから起動、ブラウザで画面を操作してサブミット）→Excelファイルのダウンロード→リクエスト単体テストのテストデータへコピー。`:92`-`:118` の5つの見出しの順 | `:88`-`:118` |
| 21 | `tools/testdata_converter.rst` | `images/testdata_converter/converter_components` | `:16` の段落の直後、`.. tip::`（`:18`）の前 | 無し | Excel 形式 ⇄ 中間モデル ⇄ YAML 形式（読み込み・書き出しの4本の矢印）。中間モデルに `:24`-`:39` の表の4区分（構造＝解析済みで保持／値＝未変換のまま保持／意図のある情報＝無損失で保持／意味を持たない情報＝保持しない）を `note` で添える。付録の `p4_component.puml` が見本 | `:14`-`:16`・`:22`-`:39` |

`:scale:` は、生成した `.png` の横幅が本文幅を超えて表示が崩れる場合だけ付ける（付けた図と値を報告に書く）。

---

## 4. 既存画像の処置

**削除する13件**（`git rm`。§3 で同名に置き換わる `select_sequence.png`・`update_sequence.png` は上書きで、この13件に含めない。§12 で 15→13 に訂正）:

| ディレクトリ | ファイル | 理由 |
|---|---|---|
| `setup/images/common/` | `send_sync_test_data_structure.png` | 図3に置き換え |
| `setup/images/master_data_restore/` | `modification_detected.png`・`copy_from_backup.png` | 図5に置き換え |
| `implementation/request_unit_test/images/mom/` | `send_sync_base.png`・`hanrei.png` | 図17に置き換え |
| `implementation/request_unit_test/images/web/` | `mail_overview.jpg`・`htmlDumpDir.png` | 図10・図11に置き換え |
| `implementation/deal_unit_test/images/mom/` | `send_sync_online_base.png`・`send_sync_online_mock.png` | 図18に置き換え |
| `implementation/deal_unit_test/images/mom/` | `send_sync_test_data_no.png` | 同じ例が `implementation/testdata_examples.rst:1924`-`:1983` にあるため `:ref:` に置き換え（§6 (b)） |
| `implementation/deal_unit_test/images/mom/` | `send_sync_response_count_change.png` | `:83` の文で足りる（§6 (c)） |
| `tools/images/request_data_tool/` | `requestDumpToolAbstract.png` | 図20に置き換え |
| `tools/images/request_data_tool/` | `image.xlsx` | `.rst` からの参照が0件 |

**触らない13件**（画面キャプチャ）: `setup/request_unit_test/images/web/` の `vmoptions`・`installed_jre`・`edit_jre`・`skip_resource_copy`／`tools/images/master_data_tool/` の4件／`tools/images/request_data_tool/` の `01`〜`04_Eclipse_*`／`tools/images/html_check_tool/how-to-trace-html`。

---

## 5. `.puml` の書き方

全 `.puml` の先頭:

```
@startuml
!pragma layout smetana
skinparam shadowing false
skinparam defaultFontName "Noto Sans JP"
```

- クラス図は `hide members`・`skinparam classAttributeIconSize 0`、抽象クラスは `abstract class`、モジュールの所属は `<<nablarch-testing-rest>>` のステレオタイプ
- シーケンス図は `skinparam sequenceMessageAlign left`。参加者名が長い場合は `\n` で改行
- 対応図（layout）・構成図（components）は `left to right direction`、`rectangle`／`file`／`folder`／`card`／`database` を使い分ける
- 凡例は `legend` ブロック、補足は `note`。**図の外に凡例画像を作らない**
- `title` は日本語で図の内容を1行（例: 「テストサポートクラスの継承関係」）

生成（`plantuml.jar` は `~/.local/share/plantuml/plantuml-1.2025.4.jar`、フォントは `~/.fonts/NotoSansJP-Regular.ttf` に導入済み。`fc-list :lang=ja family` が `Noto Sans JP` を返すこと）:

```bash
JAVA_HOME=/usr/lib/jvm/temurin-17-jdk-amd64 \
  $JAVA_HOME/bin/java -Djava.awt.headless=true \
  -jar ~/.local/share/plantuml/plantuml-1.2025.4.jar -tpng -charset UTF-8 <ディレクトリ>/*.puml
```

生成後、`file <name>.png` が `PNG image data` を返すこと、文字化け（豆腐）が無いことを画像を開いて目視すること。

付録の見本5本（`p1`〜`p5`）は書き方の参考にする。**置き先と内容は §3 で決め直す**（見本のクラス名・文言をそのまま使わない。本文の語に合わせる）。

---

## 6. 本文の変更

**図は本文の可視化である。本文に無い事実を図に入れない。図に必要な事実が本文に無いと分かったら、本文を足さずに、その図を作らずに止めて報告する**（本文の追記は新しい公開本文になるため、ディレクターが別に扱う）。

`.rst` に加えてよい変更は、`.. image::` の挿入・差し替え・削除と、次の (a)〜(h) の逐語だけである。それ以外の本文は1文字も変えない。

- **(a) `implementation/deal_unit_test/mom.rst:19`-`:27`**（導入文2つと画像2枚）を、次の1文と図18の `.. image::` に置き換える:

  ```
  同期応答メッセージ送信を伴うウェブアプリケーションの通常の処理フローと、モックアップクラスを使用して取引単体テストを行う場合の処理フローを次に示す。
  ```

- **(b) `implementation/deal_unit_test/mom.rst:78`** の第4文「次に、応答電文を2件記述した場合の例を\ Excel\ 形式で示す。」を次に置き換え、`:80`-`:81` の画像を削除する。第5文「1回目の同期送信では1件目が、2回目の同期送信では2件目が返る。」は残す:

  ```
  応答電文を2件記述した例は\ :ref:`同期応答メッセージ送信の応答電文を配置する <testdata_examples-send_sync_response>`\ を参照。
  ```

  あわせて `implementation/testdata_examples.rst:1924`（L3 見出し「同期応答メッセージ送信の応答電文を配置する」）の直前に、空行を挟んでラベル `.. _testdata_examples-send_sync_response:` を置く（`ja/` 全体で同名0件を確認済み。追加前に自分でも `grep` する）
- **(c) `implementation/deal_unit_test/mom.rst:83`** の末尾の文「テストデータを編集してテストをやり直す場合の例を次に示す。」を削除し、`:85`-`:86` の画像を削除する
- **(d) `implementation/request_unit_test/mom.rst:41`**「図の凡例を次に示す。」と `:43` の画像を削除する（凡例は図17の中）
- **(e) `implementation/testdata_notation.rst`**: `:46`-`:51`・`:85`-`:90`・`:119`-`:124` の `.. code-block:: text` 3つを（前後の空行を整えて）削除し、`:117` の末尾「次の図のとおりである。」を次に置き換える:

  ```
  \ :ref:`テストクラスとテストデータの対応 <testdata_notation-file_structure>`\ の図のとおりである。
  ```

- **(f) `about/index.rst`**: 図2の直前に導入文を1行置く:

  ```
  テストクラスが継承するクラスの系譜を次に示す。
  ```

- **(g) `setup/common.rst`**: 図3の直前に導入文を1行置く:

  ```
  ベースディレクトリ配下のテストデータの配置と読み込み単位の対応を次に示す。
  ```

- **(h) `setup/common.rst:219`** の第3文「ベースディレクトリの配下は次の図のとおりで、リクエストIDごとに1つのファイルを置く。」を次に置き換える。第1文・第2文はそのまま。`:221` の `.. image::` は §4 のとおり削除する（`:220`-`:222` の空行を1つにする）:

  ```
  ベースディレクトリの配下には、リクエストIDごとに1つのファイルを置く。
  ```

段落は1行で書く（`steering.md` Rules）。`\ ` のエスケープは `mapping/style.md` S-13 に従う。

---

## 7. 記録と順序

1コミット＝1ページ（そのページの `.puml`・`.png`・`.rst`・旧画像の削除）。README・記録はそれぞれ別コミット。**都度 push する**（`git checkout --` にディレクトリを渡さない）。

- `design.md` §「「アーキテクチャ」は本文のみとし、図も構成物一覧の表も置かない」の冒頭（見出しの直後）に、次の段落を足す:

  ```
  **2026-08-30、`#48` で本節の決定を上書きした。** §「利用側ページに内部構造の構成図を置かない」冒頭の user 判断（利用者への説明に必要な図は作る）に従い、「アーキテクチャ」節に構成図 `architecture_components` と継承の系譜 `test_support_class` を置く。継承の全体図は `about/index.rst` の1枚だけとし、各ページには置かない。以下は `#32` 当時の記録として残す。
  ```

- `design.md` §13「画像の配置」の末尾に、次の1文を段落として足す:

  ```
  図の原本（`.puml`）と生成物（`.png`）の規則は、リポジトリ直下の `README.md`「図の作成方法」に置く（`#48`）。
  ```

- `steering.md` `#33` の「処置状況」に `(b) 処置済み（`#48`）。残置図はすべて PlantUML で描き直し、画面キャプチャ13件だけを残した` を足し、「残るのは (b)…」の行を (e-1) だけに改める
- `steering.md` `#48` の Steps を check off し、State を更新する
- `checks/task-48.md` を新規作成し、次を書く: 図ごとに「本文の行」と「実装の `file:line`＋ピン」（§3 の表を実測で埋め直す）／`.rst` の差分の全件表（`git diff --numstat a6da1f6..HEAD -- ja/` の全行と、各 hunk が §3 の挿入・§4 の削除・§6 の (a)〜(h) のどれか）／削除13件と `git rm` の実行結果／§8 の完了条件の実測（コマンドと出力）／`git status --porcelain` の全件（空であること）

`mapping.csv`・`_batch/`・`mapping/glossary.md` §5.15・`ja/conf.py`・`en/`・`Dockerfile` は変更しない。`mapping.csv` の `note` に `#48` を足さない（図を落とした7行の `note` は `design.md` の節を指しており、その節に上書きを明記するため）。

---

## 8. 完了条件（すべて実測して `checks/task-48.md` に貼る）

1. `find ja/development_tools/testing_framework -path '*/images/*' -type f | sort` が **55件**: `.puml` 21・`.png` 34（キャプチャ13＋新図21）。`.jpg`・`.xlsx` は0件。21組の `.puml`／`.png` のパスが §3 の「ページ」「ファイル名」と一致する
2. `grep -rn '\.\. image::' ja/development_tools/testing_framework --include=*.rst` が **34件**で、各参照先のファイルが実在する（スクリプトで全件を突き合わせる）。§4 の削除13件への参照が0件
3. `ls ja/development_tools/testing_framework/implementation/request_unit_test/images/*/request_test_components.png` が `batch`・`mom`・`rest`・`web` の4件、同 `execute_sequence.png` が `batch`・`mom`・`web` の3件
4. 全21枚について、コミット済みの `.png` を §5 のコマンドで `.puml` から別ディレクトリへ再生成し `cmp` でバイト一致する（一致しないものがあれば PlantUML の版とともに報告）
5. `mapping/glossary.md` §8「対応表」の左列の語を機械抽出し、全 `.puml` に0件。`grep -rn 'nablarch-document\|\.rst\|:[0-9][0-9]*\b' --include=*.puml ja/` のうち解説書参照に当たるものが0件
6. Docker フルビルド（`README.md` の手順。`-a` 付き）が `build succeeded.`、`grep -cE 'WARNING:|ERROR:|SEVERE:' build.log` が 0。`_build/html/development_tools/testing_framework/` 配下に21枚の `.png` が出力されている。直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行し、`build.log` を消す
7. `python3 mapping/tools/verify_mapping.py` が `OK: no errors`（597行 / 12,986 / 11,983）、`verify_glossary.py` が `RESULT: OK`。`mapping.csv`・`_batch/`・`ja/conf.py`・`en/`・`Dockerfile`・`glossary.md` §5.15 に差分0行
8. `git diff a6da1f6..HEAD -- ja/` の hunk がすべて §3 の挿入・§4 の削除・§6 の (a)〜(h) のいずれかに分類され、それ以外が0件
9. `README.md` に `## 図の作成方法` が §2 の逐語で入り、`## ドキュメントのビルド方法` と `## textlintの実行方法` の間にある
10. `design.md` の2箇所、`steering.md` の `#33` (b)・`#48`・State、`checks/task-48.md` が §7 のとおり
11. `git status --porcelain` が空。全コミットが `origin/ntf-yaml-support` に push 済み

---

## 9. やらないこと

- 図の追加・削除・置き先の変更（表にある21枚だけ。増やさない・減らさない）
- 本文の追記・言い換え（§6 の (a)〜(h) 以外）。「図に必要な事実が本文に無い」ときは止めて報告する
- 画面キャプチャ13件の変更・改名・禁止語の点検（点検は user が行う）
- `.puml`・`.rst`・`README.md` への解説書参照（`file:line`・節見出し）の記入
- `en/` の変更、`Dockerfile`・ビルド環境の変更、`mapping.csv` の変更
- 4観点レビュー

---

## 10. 報告

次の順で書き、停止する。

1. 完了条件1〜11 の実測（コマンドと出力。`checks/task-48.md` と同じでよい）
2. 図ごとの表: ファイル名／本文の行／実装の `file:line`＋ピン／`:scale:` の有無
3. 「図に必要な事実が本文に無い」で止めた図（あれば。何が無いかを本文の行で示す）
4. `.rst` の差分の全件表（完了条件8）
5. コミット一覧（ハッシュ・1行メッセージ）

---

## 付録: 見本 `.puml`（2026-08-30 に生成を実測済み。書き方の参考。置き先・文言は §3 に従う）

### p1_class.puml（図2の見本）

```
@startuml
!pragma layout smetana
skinparam classAttributeIconSize 0
skinparam shadowing false
skinparam defaultFontName "Noto Sans JP"
hide members
title テストサポートクラスの継承関係（どれを継承するか）
abstract class TestEventDispatcher
class TestSupport
class DbAccessTestSupport
class EntityTestSupport
class HttpRequestTestSupport
abstract class AbstractHttpRequestTestTemplate
abstract class BasicHttpRequestTestTemplate
abstract class StandaloneTestSupportTemplate
class BatchRequestTestSupport
class MessagingRequestTestSupport
class MessagingReceiveTestSupport
class IntegrationTestSupport
class SimpleRestTestSupport <<nablarch-testing-rest>>
class RestTestSupport <<nablarch-testing-rest>>
TestEventDispatcher <|-- TestSupport
TestEventDispatcher <|-- DbAccessTestSupport
TestEventDispatcher <|-- EntityTestSupport
TestEventDispatcher <|-- HttpRequestTestSupport
TestEventDispatcher <|-- StandaloneTestSupportTemplate
TestEventDispatcher <|-- IntegrationTestSupport
TestEventDispatcher <|-- SimpleRestTestSupport
HttpRequestTestSupport <|-- AbstractHttpRequestTestTemplate
AbstractHttpRequestTestTemplate <|-- BasicHttpRequestTestTemplate
StandaloneTestSupportTemplate <|-- BatchRequestTestSupport
StandaloneTestSupportTemplate <|-- MessagingRequestTestSupport
MessagingRequestTestSupport <|-- MessagingReceiveTestSupport
SimpleRestTestSupport <|-- RestTestSupport
note bottom of BasicHttpRequestTestTemplate : ウェブのリクエスト単体テストはこれを継承する
note bottom of BatchRequestTestSupport : バッチのリクエスト単体テスト
@enduml
```

### p2_sequence.puml（図9の見本）

```
@startuml
skinparam shadowing false
skinparam defaultFontName "Noto Sans JP"
skinparam sequenceMessageAlign left
title リクエスト単体テスト execute() が1回の呼び出しで行うこと
actor "テストコード" as T
participant "BasicHttpRequest\nTestTemplate" as B
participant "テストデータ\n（読み込み単位）" as D
database "DB" as DB
participant "アプリケーション\n（内蔵サーバ）" as A
T -> B : execute()
B -> D : setUpDb 読み込み単位を読む
B -> DB : SETUP_TABLE を投入
B -> D : testShots 一覧を読む
loop テストショットごと
  B -> DB : テストショットの SETUP_TABLE を投入
  B -> B : beforeExecuteRequest()（拡張ポイント）
  B -> A : HTTP リクエストを送る
  A --> B : HTTP レスポンス
  B -> D : EXPECTED_* を読む
  B -> DB : 期待値と DB を突き合わせる
  B -> B : afterExecuteRequest()（拡張ポイント）
end
@enduml
```

（見本の `beforeExecuteRequest`／`afterExecuteRequest` は本文と違う。本文 `web.rst:95`・`:98` の `beforeExecute`／`afterExecute` に合わせること）

### p3_layout.puml（図19の見本）

```
@startuml
!pragma layout smetana
skinparam shadowing false
skinparam defaultFontName "Noto Sans JP"
left to right direction
title テストクラスとテストデータの対応（Excel 形式と YAML 形式）
rectangle "Excel 形式" as E {
  file "FooTest.java" as EJ
  file "FooTest.xlsx" as EX
  card "シート setUpDb" as ES0
  card "シート case01" as ES1
  card "シート case02" as ES2
  EJ .. EX : 同じディレクトリ・同じ名前
  EX -- ES0
  EX -- ES1
  EX -- ES2
}
rectangle "YAML 形式" as Y {
  file "FooTest.java" as YJ
  folder "FooTest/" as YD
  file "setUpDb.yaml" as YS0
  file "case01.yaml" as YS1
  file "case02.yaml" as YS2
  YJ .. YD : 同じディレクトリ・同じ名前
  YD -- YS0
  YD -- YS1
  YD -- YS2
}
legend right
  テストクラス = Excel: 1ファイル / YAML: 1ディレクトリ
  読み込み単位 = Excel: 1シート / YAML: 1ファイル
endlegend
@enduml
```

### p4_component.puml（図21の見本）

```
@startuml
!pragma layout smetana
skinparam shadowing false
skinparam defaultFontName "Noto Sans JP"
left to right direction
title テストデータ変換ツールの構成（両形式の間に中間モデルを置く）
file "Excel 形式\n（.xlsx）" as X
file "YAML 形式\n（.yaml）" as Y
rectangle "中間モデル\n（テスティングフレームワークの\n仕様上の意味だけを持つ）" as M
X --> M : 読み込み
M --> X : 書き出し
Y --> M : 読み込み
M --> Y : 書き出し
note bottom of M
  保持する: 構造・値・意図のある情報
  保持しない: セルの色や書式・コメント・マーカーカラム
end note
@enduml
```

### p5_activity.puml（図5の見本）

```
@startuml
skinparam shadowing false
skinparam defaultFontName "Noto Sans JP"
title マスタデータ復旧の流れ（テストメソッド1回分）
start
:コンポーネント設定ファイルから
監視対象テーブル名一覧を取得;
:テストメソッドを実行;
:SQL ログを監視;
if (監視対象テーブルを変更する SQL 文が発行されたか) then (はい)
  :変更があったテーブルの
  レコードをすべて削除;
  :バックアップ用スキーマから
  テーブル単位でコピー;
else (いいえ)
  :何もしない;
endif
stop
@enduml
```

---

## 11. 回答（2026-08-30。CC の質問: `setup/common.rst:219` の「次の図」が §4 の削除で指す先を失う）

**§6 に (h) を足した。(h) のとおり末尾を詰めて進める。** 完了条件8・§7 の差分分類・§9 は (a)〜(h) に改めた。

- 理由: 図3は `:170` に置くので、`:219` の「次の図」が指す先は無くなる。「上の図」は50行上の親節（Excel の設定ブロックの前）を指すことになり、YAML 側の対応箇所（`:264`-`:266`）に図への参照が無いので非対称になる。落とすだけで前後が成立するので詰める
- 原因は指示書の穴（§4 で `send_sync_test_data_structure.png` を消すのに、§6 が `:219` を扱っていなかった）。§4 の13件のうち、置き換え位置が元の画像とずれるのはこの1件だけ。他は同じ位置に差し替えるか (a)〜(d) で文ごと処置済み（ディレクターが `a6da1f6` で `git grep '次の図\|上の図\|下図'` と各画像の前後の段落を実測。`testdata_notation.rst:117` は (e) で処置済み）
- `checks/task-48.md` の差分の全件表では、この hunk を「§6 (h)」に分類する

---

## 12. 回答（2026-08-30。State `eb428946` の (2)・(3)。どちらも指示書の誤りで、CC の現況把握のとおり）

- **(2) §4 の「15件」は「13件」の誤り。** §4・§7・§8-2・§11 の数字を 13 に訂正した。`a6da1f6` の `images/` 配下は 28件 ＝ 削除13 ＋ キャプチャ13 ＋ 上書き2（`git ls-tree -r --name-only a6da1f6 -- ja/development_tools/testing_framework | grep /images/` で実測）。§8-1 の 55件（`.puml` 21 ＋ `.png` 34）はそのまま
- **(3) 図8（`web/request_test_components`）に `Nablarch Application Framework` を入れる。CC の方針どおり。** 根拠は、図の規則「本文に無い事実を入れない」の本文が解説書全体を指すこと（`about/index.rst:20`・`:106` に既出）と、同名の4枚（`web`・`rest`・`batch`・`mom`）を揃える規則。`rest.rst:17`・`batch.rst:17`・`mom.rst:17` は本文欄の範囲内に同語がある。`checks/task-48.md` の図8 の「本文の行」に `about/index.rst:106` を足す。`web.rst` の本文は変えない
- 着手を止める要因は無い。§2〜§10 のとおり Step 1 から通しで進め、完了したら §10 の形で報告して停止する

---

## 13. 判定（2026-08-30。`272a24f5` をディレクターが独立検証。是正ラウンド1・差分限定）

**検証結果: (A)〜(E) と記録はすべて合格。** scratchpad の clone で実測した（CC の報告・`checks/task-48.md` は根拠にしていない）。
(A) `images/` 55件・`.. image::` 34件で参照先全件実在・同名7件・削除13件消滅／(B) 21本の `.puml` を §3「本文」欄の行と実装ピン（13クラスの `extends` 句・`abstract` 4件・`TestSupportExtension.java:14`）に突き合わせて矛盾なし。`.rst` の hunk 27件（`-U0`）がすべて §3・§4・§6 (a)〜(h)／(C) 禁止語ヒットは複合語の一部か既に正表記のみ、解説書参照 0件／(D) 21枚とも再生成して `cmp` 一致／(E) Docker ビルド `build succeeded.`・WARNING 0・`_build/html/_images/` に出力・`<img>` 34件リンク切れ0／README は §2 と逐語一致、`design.md` 2箇所・`#33` (b)・`#48`・`checks/task-48.md` は §7 のとおり。`verify_glossary.py` の `refs 不一致 133` は `e52b2b1b` でも 133 で、本タスクの変更によるものではない。

**§8-6 の文言は指示書の誤り。** Sphinx は画像を `_build/html/_images/` に集約するので、「21枚が `_images/` に出力され、`<img src>` 34件にリンク切れ0」を条件6の判定とする（CC の読み替えどおり）。

### 是正（この2件だけ。他は触らない。修正意図ごとに1コミット、push）

- **(i) `implementation/testdata_notation.rst` の現 `:46`・`:78`**（`a6da1f6` の `:44`・`:83`。§10 の報告 3 の件）: 各行の末尾の一文「ディレクトリ構成の対応は、以下のとおりである。」を落とす。前の文はそのまま。落とすだけで前後が成立するため（図19が `:30` で両形式の対比を示している）。§6 に **(i)** として加え、完了条件8 の分類は (a)〜(i) と読み替える
- **(j) `about/images/index/architecture_components.puml:21`** の注記「本番と同じ基盤の上で」を「本番相当の基盤の上で」に改め、`.png` を再生成する。本文 `about/index.rst:106` の語は「本番相当の基盤の上でテスト対象クラスの動作を検証できる」であり、図は本文の語で構成する規則（§3）による
- あわせて `checks/task-48.md` §3 の本文「hunk は22件」を **27件**（表の行数。`git diff -U0` の実測）に直し、§5 に (i) の処置を追記する。§4 の条件6・8 も上記に合わせて更新する

### 完了条件（是正分）

1. `git diff 272a24f5..HEAD -- ja/` の hunk が (i) 2件・(j) の `.puml` 1件＋`.png` 1件だけ
2. (j) の `.png` を §5 のコマンドで再生成して `cmp` 一致
3. `git grep -n '以下のとおりである' HEAD -- ja/development_tools/testing_framework/implementation/testdata_notation.rst` が 0件
4. `git status --porcelain` 空、push 済み。報告は差分（コミット一覧と `git diff --stat`）だけでよい。停止する

