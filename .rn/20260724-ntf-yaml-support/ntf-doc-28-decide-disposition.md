# 作業指示: `#28` `#27` の判断待ち110件の処理

宛先: rn / CC

配置先: `.rn/20260724-ntf-yaml-support/ntf-doc-28-decide-disposition.md`

`#pre-last` と `#last` の間に置く。`#pre-last` の Completion criteria（`steering.md:610-634`）は「`ja/` 配下の `.rst` の差分が横断の是正2件に由来するものだけである」と縛っているため、本タスクの本文差分をそこへ混ぜない。**`#pre-last` を先に終わらせ、承認を得てから本タスクに着手する。**

---

## 0. 位置づけと検証環境

`#27` の21ページが `checks/task-27.md` と `reviews/page-*.md` に上げた判断待ちは**110件**である。レビュー役が全件を一次情報で確認し、次の5つに仕分けた。

| 区分 | 件数 | 扱い |
|---|---|---|
| §1 判定不要（クローズ） | 24 | 本書で理由を記録して閉じる。作業なし |
| §2 本文の是正 | 31 | 本タスクで直す |
| §3 規約ファイルの是正 | 18 | 本タスクで直す |
| §4 記録の是正・未確認の解消 | 15 | 本タスクで直す |
| §5 残骸の整理 | 4 | user 判断が出てから実施（§6-3） |
| §6 user 判断に上げた | 18 | **本書では扱わない。** 判断が返るまで着手しない |

合計 110。

レビュー役が確認に使った環境は次のとおり。本書に「確認済み」と書いた事実は、すべてこの環境でレビュー役自身がコマンドを実行して得たものである。

| 対象 | 参照 |
|---|---|
| 解説書 | `nablarch/nablarch-document` `ntf-yaml-support` の `7e19f68`。削除前の現行解説書は `2e501ad` |
| `nablarch-testing` | `e21bf67` |
| `nablarch-testing-converter` | HEAD が `2f21bce` → `45194f9` に移動している（§4-4） |

**「未確認」と書いた項目は、レビュー役が確認できなかったものである。CC は着手前に自分で確認し、確認結果を `reviews/` に記録すること。確認できないまま本文を書かない。**

---

## §1 判定不要としてクローズする24件

**作業は無い。** `checks/task-28.md` に「§1 の24件は `ntf-doc-28-decide-disposition.md` の理由により閉じた」と1行書けばよい。

### 1-1. 飛び先スタブ 6件 — 解消済み

`#27-07 decide-2`／`#27-08 decide-6`／`#27-11 decide-3`／`#27-12`（2ページ分）／`#27-13` が上げた「`:ref:` の飛び先が4行のスタブである」は、`#27` の完了により全ページが実体化して解消した。

レビュー役が `7e19f68` で確認: `guide/` を除く `.rst` は38件で、スタブ表記の残存は0件。フルビルド（`sphinx-build -a`）で WARNING・ERROR ともに0件。

`#27-11 decide-3` の申し送り「`current-0057` を必ず本文化すること」も、`implementation/request_unit_test/web.rst` が552行の実体になったことで消化されている。

### 1-2. 第3部への `style.md` S-02 適用 2件 — 規約側で処理する

`#27-07 decide-1`（第3部に「出典が無い場合は見出し自体を置かない」を適用したこと）と `#27-08 decide-1`（L3を出典に合わせ3つにしたこと）は同一事象である。個別ページの是正ではなく規約の明文化で閉じる。**§3-1 に統合した。**

### 1-3. `setup/request_unit_test/web.rst:31` の `webBaseDir` — `#18` で決着済み

`#27-04 decide-4` は「ドキュメントは `src/main/webapp`、実装は `HttpTestConfiguration.java:29` の `../main/web` で食い違う」と上げているが、**これは食い違いではない。**

`#18`（`ntf-doc-18-default-value-basis.md:21-30`）が「設定項目表のデフォルト値の基準は**実効値**（配布されるデフォルト設定が入れる値）であり、クラスのフィールド初期値ではない」と確定している。同 `:59` が `webBaseDir` について「フィールド初期値 `../main/web` ／ 実効値 `src/main/webapp`（`http-request-test.xml:15` → `http-request-test.config:1`）」と明記しており、現在の記述が確定どおりである。

レビュー役が `nablarch-testing@e21bf67` の `HttpTestConfiguration.java:29` に `private String webBaseDir = "../main/web";` があることと、`setup/request_unit_test/web.rst:31` が `src/main/webapp` であることの両方を実物で確認した。**両立する。**

### 1-4. `HttpMessagingClient.SYNCMESSAGE_STATUS_CODE` — 実在を確認した

`#27-10 decide-5` の未確認事項。レビュー役が `nablarch-testing@e21bf67` で確認した。

- `src/main/java/nablarch/test/core/messaging/RequestTestingMessagingClient.java:154-156` — 応答電文のヘッダに当該キーが無い場合、`"200"` を設定する
- 同 `:175` — 設定された値を読み出してステータスコードとして扱う
- `src/main/java/nablarch/test/core/messaging/MockMessagingClient.java:76-78`・`:118` — 取引単体テストのモックアップ側も同じ扱い

定数は実在し、既定値は `"200"` である。本文の記述と矛盾しない。

### 1-5. `#27-11 decide-5` tip1 を `important` にしなかったこと — 規約どおり

`style.md:232` の `important` の条件は「無視すると不具合・非推奨機能の誤用・データ不整合につながる」ものである。当該 tip はこれに当たらない。CC の判断が規約に合っている。**変更しない。**

### 1-6. `#27-16 decide-5` 参照実装にDBキュー専用クラスが無いこと — 事実の記録のみ

導線のみ3ページの内容に影響しない。記録として残すだけでよい。

### 1-7. `#27-17 decide-4` 食い違いが旧解説書からの引き継ぎであること — 由来の記録のみ

`#27-17 decide-1` の是正（§2-19）で解消するため、由来の記録として閉じる。

### 1-8. `#27-18 decide-4` `about/index.rst:77` — 設計違反ではない

CC 自身が「設計違反ではない」と結論している。レビュー役も同意する。閉じる。

### 1-9. `#27-21 decide-5` `#27-20` からの申し送りの充足 — 充足を確認した

レビュー役が `implementation/class_unit_test/entity.rst`（567行）に「setterとgetter」のL4があること、および `implementation/request_unit_test/web.rst` の「リクエストスコープの値を確認する」から到達できることを確認した。

### 1-10. 残り9件

`#27-09 decide-3`（節名「テストを実行する」）・`#27-09 decide-4`（`#27-11` への申し送り＝消化済み）・`#27-10 decide-1`（第3部アウトライン適用＝1-2 と同一）・`#27-12 decide-3` の2ページ分の残り・`#27-13 decide-3`・`#27-19 decide-6` の一部・`#27-20 decide-5` の重複分・`#27-21 decide-4`（出典行数の一致は `checks/task-27.md` G10 で PASS 済み）。いずれも他項目に吸収されるか、既に消化されている。

---

## §2 本文の是正 31件

**承認済みページを含む。** 事実が実装またはFW解説書と食い違うものは、承認済みであっても直す。`design.md` §8「出典どうしが食い違う場合、および出典と実装が食い違う場合は実装を優先する」による。

各項目は「現状（`file:line`）／是正内容／根拠」の3つを持つ。**根拠に挙げた `file:line` は、着手前に必ず自分で開いて確認すること。**

### 2-1. `implementation/deal_unit_test/batch.rst` の `expectedStatusCode: "100"` を `"0"` に直す（10箇所）

- 現状: `implementation/deal_unit_test/batch.rst:350`・`:360`・`:370`・`:400`・`:416`・`:432`・`:450`・`:460`・`:470`・`:480` がいずれも `expectedStatusCode: "100"`
- 是正: すべて `"0"` に直す。あわせて `:112`・`:184`・`:213`・`:242`・`:272` の Excel 形式の表の該当セルも確認し、`100` があれば `0` にする
- 根拠:
  - FW解説書 `ja/application_framework/application_framework/handlers/standalone/status_code_convert_handler.rst:39-41` が「アプリケーションのエラー処理でステータスコードを指定する場合は、100～199を使用する」と `important` で定めている。同 `:44-56` の変換表で `0～199` は変換されずそのままプロセス終了コードになる。**`100` は正常終了の値ではない**
  - 本ページの記載例3件（ファイル入力・ユーザ削除・ファイル出力）はいずれも正常系である
  - 承認済み `implementation/testdata_examples.rst:561`・`:568`（Nablarchバッチの例）は `"0"` である
  - `nablarch-example-batch` の実データ `src/test/java/com/nablarch/example/app/batch/action/ImportZipCodeFileActionRequestTest/testNormalEnd.yaml:7` および `testAbNormalEnd.yaml:7` はいずれも `expectedStatusCode: "0"`
- `#27-08 decide-4`。出典（旧解説書）の `100` を実装・FW解説書に合わせて変える是正である。**`reviews/page-deal_unit_test_batch.md` に「出典から変えた点」として追記すること**

### 2-2. `implementation/testdata_notation.rst:531`・`:534` の「（必須）」を実装に合わせる

- 現状: 「メッセージングのカラムを記述する」（`:517`）配下の表で、`:531` が「``requestPath`` … 常駐プロセスを実行する際のリクエストパスを記載する（必須）」、`:534` が「``userId`` … 実行ユーザ ID を記載する（必須）」
- 是正: メッセージングのテストでは両カラムを省略でき、省略した場合は `test` が補われることを書く。「（必須）」を外す。`:528` の `diConfig`（必須）は正しいので触らない
- 根拠（`nablarch-testing@e21bf67`、レビュー役が確認済み）:
  - `src/main/java/nablarch/test/core/messaging/MessagingRequestTestSupport.java:89-91` — `beforeExecuteTestShot` が `shot.putIfAbsent(TestShot.REQUEST_PATH, "test")`・`putIfAbsent(TestShot.USER_ID, "test")` を実行する
  - `src/main/java/nablarch/test/core/standalone/StandaloneTestSupportTemplate.java:164`・`:166` — `beforeExecuteTestShot(testShot)` が `testShot.executeTestShot()` **より先**に呼ばれる
  - `src/main/java/nablarch/test/core/standalone/TestShot.java:73-74` — 必須カラムの存在チェックは `executeTestShot()` の先頭で行われる
  - したがって補完が先に効き、記述しなくてもチェックを通る
- `#27-13 decide-8`

### 2-3. `implementation/testdata_notation.rst:63` のパス表記を `:48` と揃える

- 現状: `:48-51` の `code-block:: text` は `src/test/java/com/example/` を示すが、`:60-66` の表は「テストソースファイル … ``<PROJECT_ROOT>/test/jp/co/tis/example/db/``」と、`src/` を欠き、旧パッケージ名 `jp.co.tis` を使っている
- 是正: 表側を `code-block` に揃える。ディレクトリは `src/test/java/com/example/db/`、ファイル名は据え置き
- 根拠: 同一ページ内の不整合。レビュー役が `:46-66` を実物で確認した
- `#27-12 decide-6`

### 2-4. `setup/request_unit_test/web.rst:154-155` の `htmlCheckerConfig` の値を実効値に直す

- 現状: `:154-155` の記述例が `<property name="htmlCheckerConfig" value="test/resources/httprequesttest/html-check-config.csv"/>` と旧レイアウトのパスを持つ。同ページ `:70` のデフォルト値は `src/test/resources/nablarch/test/http-request-test/html-check-config.csv`
- 是正: `:155` の値を `src/test/resources/nablarch/test/http-request-test/html-check-config.csv` に直す
- 根拠: `#18`（`ntf-doc-18-default-value-basis.md:93`）が「記述例（`:104`〜`:155`）は表と矛盾しない値に直す。デフォルト値と異なる値を意図的に示している項目（`xmlComponentFile`・`tempDirectory` の `webTemp` など）は、そう読めるようにしてよい」と定めている。`htmlCheckerConfig` はその例外に挙げられていない。**`#18` の取りこぼしである**（同 `:59` の `webBaseDir` は `src/main/webapp` に直っていることをレビュー役が確認した）
- `#27-06 decide-2`

### 2-5. `about/index.rst:20` の禁止語「不具合」を置き換える

- 現状: 「…経路に起因する不具合を早期に見つけられる。」
- 是正: 「不具合」を「問題」に置き換える。1語のみ
- 根拠: G6 の禁止語は `不具合`・`バグ`・`将来`・`修正され`（`ntf-doc-weekend-queue.md:205`）。レビュー役が `ja/development_tools/testing_framework/`（`guide/` を除く）全体を走査し、**残存は本行の1件のみ**であることを確認した
- `#27-00` の判断待ち1

### 2-6. `implementation/class_unit_test/component.rst:89-92` の設定の記述を第2部へ移す

- 現状: `:89` に「テスト用のコンポーネント設定ファイルに `SimpleDbTransactionManager` を登録し、環境設定ファイルの `dbAccessTest.dbTransactionName` にそのコンポーネント名を記述する」という設定手順があり、`:91-92` に `code-block:: properties` の記述例がある
- 是正: この記述と `code-block` を `setup/class_unit_test.rst` へ移し、第3部からは `:ref:` で送る。第3部には「デフォルトのトランザクション以外も使う場合は第2部の設定が要る」という事実だけを地の文で残す
- 根拠: `design.md:725` 観点D「第3部に設定が混入していないか」。`ntf-doc-13-standing-rules.md` STEP 1「第2部にはコンポーネント設定ファイル・環境設定ファイルの設定項目と記述例、拡張方法を置く」
- `#27-19 decide-3`

### 2-7. `setup/request_unit_test/rest.rst:53` の記述範囲を確認して直す

- 現状: 「``nablarch-testing-jetty12`` は内蔵サーバの実装を提供するだけで、コンポーネントの登録までは行わない。」
- 是正: `nablarch-testing-jetty12` にリクエストデータ作成ツールの実装（`nablarch.test.core.http.dump.RequestDumpServer`・`HtmlReplacerForRequestUnitTesting`）が含まれるかを確認し、含まれるなら「内蔵サーバの実装を提供するだけで」を実態に合わせて改める
- 根拠と**未確認の範囲**: レビュー役は `nablarch-testing@e21bf67` に `nablarch.test.core.http.dump` の Java 実装が**無い**こと（あるのは `src/main/resources/nablarch/test/core/http/dump/template.xls` のみ）を確認した。しかし **`nablarch-testing-jetty12` は本作業環境に clone されていないため、どのモジュールが持っているかは未確認である。** CC は当該リポジトリを clone して確認し、参照コミットを記録すること。確認できない場合は本項を実施せず、その旨を記録する
- `#27-04 decide-3`

### 2-8. `setup/master_data_restore.rst:91` のスキーマ名の大小を配布物に合わせる

- 現状（`#27-05` の報告）: 小文字 `nablarch_test_master`。配布物は大文字
- 是正: 配布物 `ja/development_tools/testing_framework/tools/downloads/master_data_tool/master-data-setup-tool.zip` の中身を展開して実際の綴りを確認し、それに合わせる
- **未確認**: レビュー役は zip の中身を確認していない。CC が確認してから直すこと
- `#27-05` の判断待ち①

### 2-9. `setup/master_data_restore.rst:59-61` の tip を実態に合わせる

- 現状（`#27-05` の報告）: マスタデータ投入ツール併用時はマスタデータファイルに記述した全テーブルが必要である旨が抜けている
- 是正: 実装で条件を確認したうえで tip に追記する
- **未確認**: レビュー役は未確認。`nablarch-testing@e21bf67` の `src/main/java/nablarch/test/core/db/MasterDataRestorer.java` および `TableDuplicator` を読んで確認すること
- `#27-05` の判断待ち②

### 2-10. `implementation/testdata_notation.rst:40` の gsp-dba-maven-plugin への言及を整理する

- 現状: `:40` の tip が「blank_project のアーキタイプでプロジェクトを構築した場合は…マスタデータの投入はマスタデータ投入ツールより gsp-dba-maven-plugin の使用を優先する」と述べている
- 是正: `mapping.csv` 上、gsp の推奨は `tools/master_data_tool.rst` にのみ割り当てられている。`testdata_notation.rst` 側は「マスタデータの投入は :ref:`マスタデータ投入ツール <master_data_tool>` を参照」に寄せ、gsp の推奨は `master_data_tool.rst` 側に一本化する
- 根拠: 出典 `01_Abstract.rst:607-609` は gsp に触れていない（`#27-05` の報告）。**この出典の中身はレビュー役未確認。** `2e501ad` で開いて確認すること
- `#27-05` の判断待ち③

### 2-11. `tools/master_data_tool.rst` の配布物の記述を直す

- 現状（`#27-05` の報告）: 綴りが `protect.main.resources`（`project` の誤り）。存在しない `build/classes` を挙げている
- 是正: 配布物 zip の中身と照合して直す
- **未確認**: 2-8 と同じ zip を展開して確認すること
- `#27-05` の判断待ち⑧

### 2-12. `implementation/deal_unit_test/mom.rst:62` の前半を落とす

- 現状: `:62`「同期応答メッセージ送信を伴うウェブアプリケーションを対象とする場合、テストクラスの作り方はウェブアプリケーションの取引単体テストと同じである。モックアップクラスはコンポーネント設定ファイルで登録するため、テストクラスに記述することはない。」
- 是正: 前半（1文目）を削除し、2文目だけ残す
- 根拠: 委譲先の `implementation/deal_unit_test/web.rst` は手動操作のページであり、テストクラスに一切触れていない（`ntf-doc-27-small-3rd.md:110`「『テストクラスを作成する』『テストメソッドを作成する』は書けない。書かない」）。**読者は飛び先で答えを得られない。** 2文目だけで文意が通ることをレビュー役が `:58-62` を読んで確認した
- `#27-11 decide-2`（`#27-09` の判断待ち④の続き）

### 2-13. `implementation/request_unit_test/batch.rst:183` の条件節の帰属を直す

- 現状: `:183`「テスト対象が常駐バッチの場合は、あわせてリクエストスレッド内ループ制御ハンドラの置き換えが必要である（:ref:`…<request_unit_test_setting_batch>`）。」
- 是正: `#27-17 decide-1` の指摘に従い、条件節が掛かる範囲を明確にする
- 根拠: `setup/request_unit_test/batch.rst:16-17` が同じ事実を「常駐バッチのリクエスト単体テストは、本番用のハンドラ構成のままでは実施できない」と述べている。レビュー役が両行を実物で確認した
- `#27-17 decide-1`

### 2-14. `setup/request_unit_test/batch.rst:17` の「常駐バッチ」の範囲を確認して直す

- 現状: `:15` のL3見出しが「常駐バッチのリクエストスレッド内ループ制御ハンドラを置き換える」、`:17` が「:ref:`常駐バッチ <nablarch_batch-resident_batch>` のリクエスト単体テストは…:ref:`リクエストスレッド内ループ制御ハンドラ <request_thread_loop_handler>` は…」
- 指摘（`#27-16 decide-2`）: FW解説書では、リクエストスレッド内ループ制御ハンドラは常駐バッチのハンドラ構成に含まれず、DBキュー／MOM側に属する
- 是正: FW解説書の当該ハンドラ構成図（`ja/application_framework/application_framework/batch/nablarch_batch/architecture.rst` および `ja/application_framework/application_framework/messaging/db/architecture.rst`）を開いて所属を確認し、記述を実態に合わせる
- **未確認**: レビュー役は `setup/request_unit_test/batch.rst:12-22` の本文は確認したが、FW解説書側のハンドラ構成の所属は確認していない。CC が確認すること
- `#27-16 decide-2`・`decide-3`

### 2-15. `implementation/deal_unit_test/batch.rst` に `setUpTable: default` の意味を1文足す

- 現状: 記載例の全テストショットに `setUpTable: default` が付いているが、本文に説明が無い
- 是正: 「テストショットごとに準備データが再投入される」旨を1文足す
- 根拠: `nablarch-testing@e21bf67` `src/main/java/nablarch/test/core/standalone/TestShot.java:149-162`（`#27-08` の報告）。**レビュー役未確認。** 該当行を開いて確認してから書くこと
- `#27-08 decide-3`

### 2-16. `implementation/deal_unit_test/batch.rst` に分割例と非分割例の検証範囲の違いを1文足す

- 現状: 分割例と非分割例で `expectedTable` の有無が違い、検証範囲が異なるが、本文で触れていない
- 是正: 違いが意図的であることを1文で示す
- 根拠: `TestShot.java:193-213`（`#27-08` の報告）。**レビュー役未確認**
- `#27-08 decide-2`

### 2-17. `implementation/deal_unit_test/batch.rst` の `expectedTable: fileInputBatch` を整合させる

- 現状: 出典 `:76` の `expectedTable: fileInputBatch` に対応するデータブロックが出典にも本ページにも無い
- 是正: 対応するデータブロックを足すか、当該セルを空にする。**空にする方を推奨する**（出典側の欠落であり、無いデータブロックを創作しない）
- `#27-08 decide-5`

### 2-18. `implementation/deal_unit_test/mom.rst` に `MockMessagingContext` の制約を書く

- 現状: モックアップの制約が本文に無い
- 是正: `UnsupportedOperationException` を投げるメソッドと no-op のメソッドがあることを書く
- 根拠: `nablarch-testing@e21bf67` の `MockMessagingContext`（`#27-09` の報告では `:148-151`・`:120-123`）。**レビュー役未確認。** ファイルパスと行を自分で特定して確認すること
- `#27-09 decide-5`

### 2-19. 導線文の動詞を統一する

- 現状: 導線のみ3ページの導線文が「同じ方法で行う」と「同じ方法で実施する」（`implementation/request_unit_test/http_messaging.rst:15`）で割れている
- 是正: 「同じ方法で行う」に統一する
- 根拠: 承認済みの同型導線文（`implementation/deal_unit_test/batch.rst:20`・`rest.rst:22`）に揃える
- `#27-17 decide-3`

### 2-20. `implementation/testdata_notation.rst:1251` 周辺のMOM限定の記述を限定する

- 現状（`#27-10 decide-4`）: MOM限定にすべき記述が全般の記述として書かれている
- 是正: 適用範囲を限定する
- **未確認**: レビュー役は `:1246-1256` を読んだが、どの文がMOM限定であるべきかは `reviews/page-deal_unit_test_http_messaging.md` の decide-4 の記述に依っており、実装で裏を取っていない。CC が確認すること
- `#27-10 decide-4`

### 2-21. `implementation/testdata_notation.rst:1154` と `implementation/testdata_examples.rst:1802` を直す

- 現状（`#27-13 decide-2`）: リクエスト単体テストの文脈で誤っている
- 是正: 実装で確認して直す
- **未確認**: レビュー役未確認
- `#27-13 decide-2`

### 2-22. `implementation/testdata_notation.rst:392` の `description` の説明を補う

- 現状: 「ウェブアプリケーションのリクエスト単体テストでは、出力される HTML ダンプのファイル名にも使用される」
- 是正: 実際のファイル名が `読み込み単位の名前_Shot番号_説明.html` であることを書き足す
- 根拠: `#27-20` の §4 の6。レビュー役が `:392` の現在の文言を確認した。**組み立て規則そのものは未確認。** 実装で確認してから書くこと
- `#27-20 decide-4`

### 2-23. `implementation/request_unit_test/mom.rst` の tip の重複を解く

- 現状: `implementation/deal_unit_test/mom.rst:72-73` と逐語同一の tip がある
- 是正: 片方を残し、もう片方は `:ref:` で送る。**第3部の記述量が少ない側（`deal_unit_test/mom.rst`）から `request_unit_test/mom.rst` へ送る**
- 根拠: `design.md:522`「承認済みページが同じ事実を持つ場合は `:ref:`」
- `#27-13 decide-1`

### 2-24. `implementation/request_unit_test/mom.rst` に節ラベルを足す

- 現状: 節ラベルが無く、他ページから節単位で参照できない
- 是正: `style.md` S-08 の命名に従って足す
- `#27-13 decide-4`

### 2-25. `implementation/request_unit_test/rest.rst` に `setBody` の説明を足す

- 現状: 触れていない
- 是正: 実装で確認して1文足す
- **未確認**: レビュー役未確認
- `#27-12 decide-4`

### 2-26〜2-29. 導線（`:ref:`）を足す 4件

`design.md:360`「第2部・第3部からツールに言及する場合は `:ref:` で参照する」による。

| # | 追加箇所 | 飛び先 | 出典 | 判断待ち |
|---|---|---|---|---|
| 2-26 | `implementation/request_unit_test/web.rst` | `request_data_tool` | 旧 `05_UnitTestGuide/02_RequestUnitTest/index.rst:249-250` に逆方向のリンクがあった。現状 `request_data_tool` を指すのは `tools/index.rst:9` の toctree だけ | `#27-04 decide-5` |
| 2-27 | `setup/deal_unit_test/rest.rst` | `deal_unit_test_rest` | 第2部から第3部への逆導線が無い | `#27-07 decide-3` |
| 2-28 | `setup/request_unit_test/http_messaging.rst` | `request_unit_test_http_messaging` | 同上 | `#27-15 decide-3` |
| 2-29 | `implementation/deal_unit_test/mom.rst` | `request_unit_test_batch` | `mom.rst` から本ページへの導線が無い | `#27-14 decide-6` |

### 2-30. JUnit 5 用拡張機能への導線を第3部の該当ページに足す

- 現状: `#27-12`・`#27-13`・`#27-14` がそれぞれ「JUnit 5 導線が無い」と上げている
- 是正: 3ページ（`implementation/request_unit_test/rest.rst`・`mom.rst`・`batch.rst`）から `:ref:`JUnit 5用拡張機能 <junit5_extension>`` へ導線を張る。**同じ文型で揃えること**
- `#27-12 decide-5`・`#27-13 decide-9`・`#27-14 decide-4`

### 2-31. `implementation/deal_unit_test/db_queue.rst` の `OneShotLoopHandler` への導線を短くする

- 現状: `OneShotLoopHandler` の置き換え情報に到達するまで3ホップ要る
- 是正: 導線を1ホップ短くする。ただし個別指示 `ntf-doc-27-db-queue.md:52`「『同じ方法で行う』以上のことを書かない」に抵触しない範囲にとどめる
- `#27-18 decide-2`

---

## §3 規約ファイルの是正 18件

`style.md`・`glossary.md`・`design.md` を変更する。**`glossary.md` §5.15（`:331-456`）の証拠一覧は書き換えてはならない。** §5.15 以外は変更してよい（レビュー役が `mapping/glossary.md` の見出し構造を確認した）。

### 3-1. `style.md` S-02 に第3部の但し書きを足す

- 現状: S-02 は第2部について「『機能概要』『拡張例』は出典が無い場合は見出し自体を置かない」と定めるが、第3部に同じ明文が無い
- 是正: 第3部にも同じ扱いを適用する旨を明文化する。`design.md:281-296` の第3部アウトライン5節は「標準的な手順の並びであって、全ページに5つ揃えることを求めるものではない」ことを併記する
- 根拠: `ntf-doc-27-small-3rd.md:26`・`:28` が本指示で同じ扱いを適用すると定め、`decide` に上げるよう求めていた
- `#27-07 decide-1`・`#27-08 decide-1`・`#27-10 decide-1`（§1-2 から統合）

### 3-2. `style.md` S-04 に L5 の記号を定義する

- 現状: `style.md:189-193` の見出し記号表は L1 `=`／L2 `-`／L3 `~`／L4 `^` の4行で終わっており、**L5 の行が無い**（レビュー役が実物で確認）
- 是正: L5 の記号を1行足す。`ja/biz_samples/12/index.rst:85-87` が `^` を上下線で使う例として `style.md:210` に挙がっているため、L5 は別記号にする
- `#27-19`・`#27-20`・`#27-21` で3回上申されている

### 3-3. `style.md:193` の L4 の使用条件を判定可能な形に改める

- 現状: `:193`「L4（L3のさらに下の細分）／`^`／L3配下をさらに細分する見出し。**用例が薄いページでのみ使う**」
- 問題: 「用例が薄い」が判定基準にならない。実測では `implementation/request_unit_test/web.rst` が18本、`implementation/class_unit_test/component.rst` が6本、`implementation/deal_unit_test/rest.rst` が2本で、条文と逆の分布になっている
- 是正: 「L3が3つ以上の独立した操作に分かれる場合に使う」のような、開いて数えれば判定できる条件に改める
- `#27-19 decide-1`・`#27-20 decide-1`

### 3-4. `style.md:343`・`:344` の「（スタブ）」を外す

- 現状: S-08 のラベル一覧で `:343`「JUnit 5用拡張機能（スタブ）」、`:344`「マスタデータ復旧機能（スタブ）」（レビュー役が実物で確認）
- 是正: 両ページとも実体化しているため「（スタブ）」を外す
- `#27-02 decide-4`・`#27-05` の関連

### 3-5. `style.md:413-417` S-09 の適用外に導線のみ3ページを足す

- 現状: `:413-417` の適用外は `index.rst`・`setup/index.rst`・`implementation/index.rst`・`tools/index.rst` の4件のみ（レビュー役が実物で確認）
- 是正: `setup/request_unit_test/db_queue.rst`・`implementation/request_unit_test/db_queue.rst`・`implementation/deal_unit_test/db_queue.rst` の3ページ（各6行、L2セクションを持たない）を適用外に足す。S-02 についても同様に例外を明記する
- `#27-16 decide-4`・`#27-17 decide-5`

### 3-6. `style.md` に「見出し下線の直後に空行を置かない」を明文化する

- 根拠: `#27-04` の実測 203/207。**レビュー役は再計測していない。** CC が再計測して数を記録すること
- `#27-04 decide-6` の1つ目

### 3-7. `style.md` S-05 にコマンド例の言語指定を明記する

- 是正: コマンド例は `text` ではなく `bash` を使う旨を書く
- `#27-04 decide-6` の2つ目

### 3-8. `style.md` にキャプチャのUI言語の規則を書く

- 現状: `tools/request_data_tool.rst` のキャプチャは英語ロケール、`setup/request_unit_test/web.rst` は日本語ロケール
- 是正: どちらに揃えるか、または併記（「日本語(English)」）の規則を書く。**既存のキャプチャを撮り直さない範囲で決めること**
- `#27-04 decide-6` の4つ目

### 3-9. `style.md` に `\ ` エスケープの規範を書く

- 現状: 規範が無く、ページごとに揺れる余地がある
- 是正: 日本語と inline literal の境界で `\ ` を置く条件を明文化する
- `#27-14 decide-7`

### 3-10. `style.md` に表内で `literal` と `:java:extdoc:` を使い分ける基準を書く

- `#27-14 decide-5`

### 3-11. `style.md` にL3見出しの下線長を固定する

- 現状: 明文が無く `#27-05` で揺れた。`style.md:195` は「タイトル文字列と同じ長さ以上」としか定めていない（レビュー役が実物で確認）
- 是正: 「50文字固定」など、実測で確認できる形に定める。**既存38ページの実測分布を採ってから決めること**
- `#27-05` の判断待ち（規約側の手当て1件目）

### 3-12. `style.md` S-02 に第4部のセクション構成を定義する

- 現状: S-02 は第2部・第3部のみ明文で、第4部（`tools/` 4ページ）が未定義
- 是正: 実在する4ページ（`master_data_tool.rst`・`request_data_tool.rst`・`html_check_tool.rst`・`testdata_converter.rst`）の構成を実測し、それを規約化する
- `#27-05` の判断待ち（規約側の手当て2件目）

### 3-13. `glossary.md:309` の「前提事項」の定義を第4部に合わせる

- 現状: `:309` は「前提事項」を「機能概要の下位セクション」と定義するが、第4部では `mapping.csv`（`current-0344`）に従って「導入」配下に置いている
- 是正: 定義を広げるか、第4部の例外を明記する。**§5.15 の範囲外なので変更してよい**
- `#27-04 decide-6` の1件目

### 3-14. `glossary.md:201`・`:556` の断定を実測に合わせて緩める

- 現状: 両行が「業務上のテストケースを指す用法は NTF解説書の本文に現れない」と断定している
- 反例（レビュー役が一次情報で確認済み）: `2e501ad:ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/index.rst:12`「テストケース毎に以下の手順でテストを実施する。」および同 `:27`「テストケースに従ってテストを実施する。」。いずれも**手動でアプリケーションを操作するテストの手順**（同 `:7-8`）であり、`testShots` のエントリを指し得ない
- 是正: 断定を「解説書のページ本文（新規作成分）には現れない。ただし出典（旧解説書）の手動テスト手順には実例がある」に改める。**置換ルール自体は変えない**（CC は当該箇所を普通名詞の「テスト」に置き換えて処理しており、この処理は正しい）
- `:201` は §5.7、`:556` は §8 にあり、いずれも §5.15 の範囲外である（レビュー役が見出し構造を確認した）
- `#27-11 decide-6`

### 3-15. `glossary.md` に「通信先」の語の扱いを書く

- `#27-10 decide-3`

### 3-16. `design.md` §5 のテストデータ変換ツールの「導入」に関する記述を更新する

- 現状: `design.md:330-360` が「テストデータ変換ツールも『導入』を持たない。出典に該当する記述が存在しないため」としている
- 問題: `tools/testdata_converter.rst` は実装から Maven プラグインの追加手順と `<dependency>` を書き足したため、実質的な導入手順が「使用方法」配下に入っている
- 是正: `design.md` の記述を実態に合わせるか、当該節を「導入」に移す。**「導入」に移す方を推奨する**（第4部の他ページと構成が揃う）
- `#27-03 decide-2`

### 3-17. `design.md` §3「記載範囲」に、設定項目名への言及の可否を書く

- 現状: 「設定の話は第2部」という線引きが、設定項目名に言及すること自体を禁じているのか、説明を書くことだけを禁じているのかを読み取れない
- 是正: 「設定項目名を挙げて `:ref:` で送るのはよい。値・既定値・記述例を第3部に書かない」のように明文化する
- `#27-20 decide-2`

### 3-18. `style.md` S-03 の内容条件と `ntf-doc-27-small-3rd.md` の指定の関係を整理する

- 現状: `implementation/deal_unit_test/web.rst` のL3「テストを準備する」「テストを実施する」が `style.md:155-156`（S-03 の内容条件）に反するが、`ntf-doc-27-small-3rd.md:129-132` の指定を優先した
- 是正: 個別指示が規約に優先する条件を `style.md` に1行書く。見出し自体は変えない
- `#27-11 decide-4`

---

## §4 記録の是正・未確認の解消 15件

`ja/` 配下の `.rst` は変更しない。

### 4-1〜4-5. `mapping.csv` の `dest_section` と `note` の是正 5件

`mapping.csv` の直接編集は Rule §1-4 で禁止されている。**`_batch/` 経由の正規の手順で直すか、直さずに `checks/task-28.md` に逸脱として記録するかを CC が選び、選んだ理由を書くこと。**

| # | 対象 | 内容 | 判断待ち |
|---|---|---|---|
| 4-1 | `current-0178` | `dest_section` と実際の配置が違う | `#27-02 decide-1` |
| 4-2 | `current-0269` | 同上 | `#27-02 decide-2` |
| 4-3 | `input-0027` | 部分不採用が反映されていない | `#27-15 decide-1` |
| 4-4 | `current-0069` | `dest_section` と実際の配置が違う | `#27-15 decide-2` |
| 4-5 | `input-0198-b` | `note` が「YAML OUT 後にスキーマ検証を行うリンター」とするが、実装ではリンタが変換の処理経路に組み込まれていない。`disposition` は `MERGE` のまま | `#27-03 decide-5` |

### 4-6. `current-0196`（`REFERENCE`）の飛び先粒度を決める

- `#27-19 decide-2`

### 4-7. `nablarch-testing-converter` の参照コミットをピンする

- 現状: 作業指示の参照リポジトリ表に本リポジトリの記載が無く、執筆中に HEAD が `e80a4dd` → `2f21bce` へ動いた
- **レビュー役が現在の HEAD を確認した: `45194f9`（`docs(coverage): レビュー指摘を台帳へ反映し、実測と食い違う数値を直す`）。さらに動いている**
- 是正: `steering.md` の参照リポジトリ表に `nablarch-testing-converter` を足し、コミットをピンする。同時に `nablarch-testing-yaml` も確認すること（**レビュー役の確認時点で `e69b69f`。`190cc9a` から動いている**）
- `#27-03 decide-4`

### 4-8. surefire 2.22.0 の一次情報を確認する

- 現状: `setup/junit5_extension.rst` が surefire 2.22.0 を前提としているが、一次情報が未確認
- 是正: `nablarch-testing@e21bf67` の `pom.xml` および親POM `nablarch-parent` で確認する。**親POM は本作業環境に無い**ため、確認できない場合はその旨を記録する
- `#27-02 decide-5`

### 4-9. HTTPメッセージ受信の実行経路を確認する

- `#27-15 decide-4`。**レビュー役未確認**

### 4-10. `implementation/class_unit_test/component.rst:125` の原因を確認する

- 現状: 原因をアノテーションとして書いているが、実際はメソッド隠蔽である疑い
- 是正: 実装で確認し、違っていれば本文を直す（その場合は §2 に移す）
- **未確認**: レビュー役未確認
- `#27-19 decide-4`

### 4-11. `implementation/deal_unit_test/batch.rst:10`・`:15` の前提がDBキューに成立するかを確認する

- 現状: 「複数バッチ処理で1取引」という前提が、DBキューにも成立するかが未確認。`ja/application_framework/application_framework/messaging/db/` に「取引」は0件（`#27-18` の報告）
- 是正: 確認し、成立しないなら `implementation/deal_unit_test/db_queue.rst` の導線文を見直す
- `#27-18 decide-1`

### 4-12. `implementation/request_unit_test/db_queue.rst` の飛び先の妥当性を記録する

- 現状: 飛び先 `implementation/request_unit_test/batch.rst` の記述例の8割が応答不要メッセージ送信で、DBキューに該当しない
- 是正: 個別指示 `ntf-doc-27-db-queue.md:52` の縛りにより本文は変えられない。**この制約が読者に与える影響を `checks/task-28.md` に記録し、`#last` で再判定する**
- `#27-17 decide-2`

### 4-13. `implementation/deal_unit_test/db_queue.rst` の飛び先の妥当性を記録する

- 現状: 飛び先の記述例6件がすべてファイル入出力だが、DBキューの入力は `SqlRow` である
- 是正: 4-12 と同じ扱い
- `#27-18 decide-3`

### 4-14. `setup/request_unit_test/db_queue.rst` の飛び先の妥当性を記録する

- 現状: 飛び先3設定のうちDBキューに該当するのは1件のみ
- 是正: 4-12 と同じ扱い
- `#27-16 decide-1`

### 4-15. 個別指示の出典件数表を `mapping.csv` の実測に合わせる

- 現状: `ntf-doc-27-large-pages.md` §3-2 の出典件数表が `mapping.csv` の実測と合わない。同種のずれが他ページの個別指示にもある可能性がある
- 是正: `#27` の全個別指示（`ntf-doc-27-db-queue.md`・`ntf-doc-27-large-pages.md`・`ntf-doc-27-small-3rd.md`）の件数表を `mapping.csv` で再計算し、ずれを `checks/task-28.md` に一覧する。**指示書本体は書き換えない**（履歴として残す）
- `#27-20 decide-6`

---

## §5 残骸の整理 4件 — **user 判断が返るまで着手しない**

`guide/` 配下の追跡ファイルの削除は不可逆である。レビュー役が実測した件数は次のとおり（`7e19f68`、`git ls-files ja/development_tools/testing_framework/guide`）。

| 対象 | 件数 | 内訳 | 判断待ち |
|---|---|---|---|
| `guide/` 配下 全体 | **88** | png 71・xlsx 8・java 6・jpg 2・JPG 1。`.rst` は0件 | `#27` 独立検証の申し送り2 |
| うち `05_UnitTestGuide/02_RequestUnitTest/_image/` | **37** | （`#27-20 decide-5` の「36件」は実測と1件ずれる） | `#27-20 decide-5` |
| うち `05_UnitTestGuide/03_DealUnitTest/_images/` | **9** | | `#27-09 decide-6` |
| うち `05_UnitTestGuide/01_ClassUnitTest/_download/` | **10** | java 6・xlsx 4（うち1件は日本語ファイル名） | `#27-21 decide-3` |

**新ページから参照されているのは1件のみである。** `about/index.rst:108` が `../guide/development_guide/06_TestFWGuide/_images/abstract_structure.png` を参照している。残り87件は未参照。

**`en/` 配下は本作業で一度も触れていない。** レビュー役が確認した: `en/development_tools/testing_framework/` に旧解説書の `.rst` が47件、追跡ファイルが177件、独立した `en/conf.py` とともに残っている。`design.md`・`steering.md` に `en/` への言及は1件も無い。`ja/guide/` を削除しても `en/` には影響しない（別ディレクトリで、画像も別に持つ）。

判断は §6-3 に上げた。

---

## §6 user 判断に上げた18件 — **本書では扱わない**

次の18件は、レビュー役がチャットで user に判断を求めた。**判断が返るまで着手しないこと。** 判断が返ったら本書に追記する。

| 群 | 件数 | 判断待ち |
|---|---|---|
| 6-1 NTF本体の不具合疑い | 7 | `#27-03 decide-1`・`decide-3`／`#27-04 decide-1`・`decide-2`／`#27-02 decide-3`／`#27-09 decide-1`／`#27-05` の判断待ち⑦ |
| 6-2 解説書に手順が存在しない欠落 | 6 | `#27-12 decide-1`／`#27-13 decide-5`・`decide-6`／`#27-14 decide-1`・`decide-3`／`#27-19 decide-5` |
| 6-3 `guide/` 残骸88件の処分 | 1 | §5 |
| 6-4 `design.md:360` と `:522` の衝突 | 1 | `#27-06 decide-1`（`#27-05` の判断待ち③と同根） |
| 6-5 図・画像5件の扱い | 2 | `#27-09 decide-2`／`#27-10 decide-2`／`#27-13 decide-7`／`#27-12 decide-2`／`#27-14 decide-2` を2群にまとめた |
| 6-6 「現在検討中」の tip | 1 | `#27-11 decide-1` |

---

## ゲート

`checks/task-28.md` に記録すること。

1. §1 の24件を閉じたことの記録が1行ある
2. §2 の31件それぞれについて、**着手前に根拠の `file:line` を自分で開いて確認した**ことと、確認結果（一致・不一致）が記録されている。「未確認」と本書に書かれた項目は、確認できたか／できなかったかが明記されている
3. §2-1 の `expectedStatusCode` が `implementation/deal_unit_test/batch.rst` 全体で `"100"` 0件・`"0"` 10件以上であること（`grep -c` の実測値を書く）
4. §3 の18件が `style.md`・`glossary.md`・`design.md` に反映され、**`glossary.md` の `:331-456`（§5.15）に差分が0行**であること
5. `python3 mapping/tools/verify_mapping.py` が `exit 0`
6. `python3 mapping/tools/verify_glossary.py` の不一致件数が `#pre-last` 完了時点から増えていないこと
7. Docker でフルビルドし、WARNING・ERROR がともに0件であること。**ビルド後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行すること**
8. §5・§6 の22件に着手していないこと（`git diff` に該当する変更が無いこと）

## 禁止事項

- **§5・§6 の22件に着手しない。** user 判断が返るまで待つ
- `glossary.md` §5.15（`:331-456`）を1行も変更しない
- 本書に「未確認」と書かれた事実を、自分で確認しないまま本文に書かない。確認できない場合は本文を変えず、その旨を記録する
- `ja/conf.py` を変更しない
- `guide/` 配下のファイルを削除・移動しない
- `en/` 配下を変更しない
- user review の承認を受けるまで次タスクに着手しない
