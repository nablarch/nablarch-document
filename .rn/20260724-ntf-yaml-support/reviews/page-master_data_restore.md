# `setup/master_data_restore.rst`（マスタデータ復旧機能）

`#27-01` のレビュー記録。対象は `mapping.csv` の `dest_page=マスタデータ復旧機能` の10行（すべて `MERGE`、合計193行）。出典は `origin/develop` の `ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/04_MasterDataRestore.rst`（9行）と `03_Tips.rst`（1行）で、いずれも `#7` で削除済み。`git show 2e501ad:<path>` で読む。

## 出典行の消化

| `mapping_id` | 出典 | `lines` | 反映先 |
|---|---|---:|---|
| `current-0254` | `04_MasterDataRestore.rst:13-27` | 15 | 機能概要 の第1・第2段落（`:14`・`:16`） |
| `current-0255` | `:30-35` | 6 | 機能概要 の箇条書き3件（`:20-22`） |
| `current-0256` | `:38-56` | 19 | 機能概要 > 必要となるスキーマ（`:34-47`） |
| `current-0257` | `:59-74` | 16 | 機能概要 > マスタデータを復旧する流れ（`:24-32`。画像2点を含む） |
| `current-0258` | `:77-81` | 5 | 使用方法 の導入文（`:51`） |
| `current-0259` | `:84-93` | 10 | 使用方法 > バックアップ用スキーマを作成する（`:55-61`） |
| `current-0260` | `:96-108` | 13 | 使用方法 > テーブルの依存関係の解析を抑止する（`:161-175`） |
| `current-0261` | `:111-167` | 57 | 使用方法 > 監視対象テーブルを登録する（`:65-115`） |
| `current-0262` | `:170-215` | 46 | 使用方法 > SQLログを出力する（`:117-157`） |
| `current-0245` | `03_Tips.rst:725-730` | 6 | **落とした**（下記「判断待ち」1） |

`verify_mapping.py` は変更していない（`mapping.csv` は無変更）。

## 実装で確認した事実

参照コミット: `nablarch/nablarch-testing` = `e21bf67`。読み方は `git -C /home/tie303177/work/nablarch/nablarch-testing show e21bf67:<path>`。作業ツリーの HEAD は別コミットなので直接読まないこと。

| 本文の記述 | 実装上の根拠 |
|---|---|
| 設定項目は `backupSchema` と `tablesTobeWatched` の2つ（`:76-81`） | `MasterDataRestorer.java` の public setter は `setTablesTobeWatched`（`:180`）・`setBackupSchema`（`:190`）・`setUpdateSqlKeywords`（`:200`）の3つのみ。`setTestEventListeners` は存在しない（`git show e21bf67:src/main/java/nablarch/test/core/db/MasterDataRestorer.java \| grep -n "public void set"`） |
| `testEventListeners` に登録しないと復旧が行われない（`:113`） | `testEventListeners` は `MasterDataRestorer` のプロパティではなく、`TestEventDispatcher` がシステムリポジトリから引くキーである。テストメソッド終了の通知はこの一覧に登録されたオブジェクトにしか届かない（`TestEventDispatcher.java:135-149`） |
| `RepositoryInitializer` もこの一覧に登録しないとリポジトリの復元が行われない（`:115`。記述例 `:107` に含めた） | `RepositoryInitializer.afterTestClass()`（`e21bf67:src/main/java/nablarch/test/RepositoryInitializer.java:161-162`）が `revertDefaultRepository()`（`:47-53`）を呼ぶ。通知は `testEventListeners` に登録されたオブジェクトにしか届かない。**リポジトリの初期化**（`:38-44`）のほうは `RepositoryInitializer` の静的初期化子（`:32-34`）と `TestEventDispatcher` から直接呼ばれるため登録は不要で、登録が要るのは**復元**のためだけである。記述例の並びは `e21bf67:src/test/resources/unit-test.xml:70-74`（`RepositoryInitializer` が `:72`、`masterDataRestorer` が `:73`）に合わせた。`/home/tie303177/work/nablarch/nablarch-example-batch/src/test/resources/unit-test.xml:51-56` にも同じ並びの記述があるが、こちらはコメントアウトされている |
| 復旧は、変更があったテーブルのレコードをすべて削除したうえで、バックアップ用スキーマの同じテーブルからすべて挿入する（`:30`） | `MasterDataRestorer.java:322-338`。削除を対象テーブル分まとめて行ったあとに挿入を行う。テーブルごとに削除→挿入を繰り返す形ではない |
| デフォルトではJDBCの機能でテーブルの依存関係を解析し、削除は子テーブルから、挿入は親テーブルから行う（`:163`） | `MasterDataRestorer.java:349` が `TableDataSorter.sort(...)` を呼び、`EntityDependencyParser.java:34-48` が `DatabaseMetaData#getImportedKeys` で親子関係を組み立てる |
| `nablarch.suppress-table-sort` はマスタデータの復旧以外にも適用される（`:175`） | `git grep -n "TableDataSorter\." e21bf67 -- src/main` の全ヒットは4件。`DbAccessTestSupport.java:193`・`:198`（準備データの投入）、`MasterDataSetUpper.java:158`・`:170`（マスタデータ投入ツール）。判定はグローバル設定1つで行われる |
| SQLログの監視には `DEBUG` を指定する。`INFO` 以上では検出できない（`:157`） | 検出のフックは `SqlLogWatchingFormatter` にあり、SQLログが出力されなければ呼ばれない。`TRACE` でも動作するが、出典（`:188`）が「デバッグレベル以上」と述べているため `DEBUG` を指定する記述にした |
| `NopLogWriter` はログライターである（`:127`・`:139`） | `nablarch.test.core.log.NopLogWriter` は `LogWriter` の実装クラスであり、ロガーではない |

## 出典から変えた点

| 出典 | 変更 | 理由 |
|---|---|---|
| `:115-141` の設定項目一覧に `testEventListeners` の行がある | 表から落とし、`MasterDataRestorer` のプロパティ2件だけにした。導入文を「主な設定項目は次のとおりである」とし、`testEventListeners` は表の外の地の文（`:83`）と `important`（`:111-115`）に移した | `testEventListeners` は `MasterDataRestorer` のプロパティではないため、同じ表に並べると誤読させる（上表参照）。「主な設定項目は」の言い回しは承認済みの `setup/request_unit_test/rest.rst:63` に先例がある |
| `:145-166` の設定例に `testEventListeners` の記述が無い | `<list name="testEventListeners">` を記述例に加え、`RepositoryInitializer` を含めた（`:105-109`） | 出典は「ここに登録することで復旧が行われる」と表で述べながら、設定例にその記述が無く、写しても動かない。`RepositoryInitializer` を落とすとリポジトリの復元が行われなくなる（上表参照） |
| `:78`「以下の環境構築を実施し、自動テストフレームワークのマスタデータ復旧機能を有効にする。」 | 「バックアップ用スキーマの作成・監視対象テーブルの登録・SQLログの出力設定の3つをすべて行うと有効になる。テーブルの依存関係の解析の抑止は、必要な場合にだけ行う。」に改めた（`:51`） | 出典は4つの節を並列に並べているが、`nablarch.suppress-table-sort` は未設定が既定動作であり必須ではない。必須のものと任意のものを区別して述べた |
| `:94` の節「外部キーが設定されたテーブルを使用する場合について」が「環境構築」の2番目にある | 「テーブルの依存関係の解析を抑止する」に改題し、「使用方法」の末尾（`:161`）へ移した | `style.md` S-03（セクションタイトルは「〜する」形式）。任意の設定を必須の設定より先に置くと、読者が必須と誤解する |
| `:36` の節「必要となるスキーマ」が `:57` の節「動作イメージ」より前にある | 順序を入れ替え、「マスタデータを復旧する流れ」（図）を先、「必要となるスキーマ」（表）を後にした（`:24`・`:34`） | `design.md:216-226` の第2部アウトラインが、機能概要の並びを「全体像（図）→ 主なクラスとリソース（表）」と定めている |
| `:57` の節「動作イメージ」 | 「マスタデータを復旧する流れ」に改めた | `style.md` S-03。「イメージ」は何が書かれているか伝わらない |
| `:33`「バックアップ用スキーマからテーブル毎に一括で復旧するので、1件ずつINSERTする場合に比べて高速に復旧できる。」 | 「バックアップ用スキーマからテーブル単位で一括してコピーするので、1件ずつ挿入する場合に比べて高速である。」（`:22`） | `glossary.md` の和文表記に合わせ、`INSERT` を「挿入」にした |
| `:68-69`「テーブルを復旧する際、いったんテーブル内のレコードを全件削除する。その後、バックアップ用スキーマのテーブルからレコードを全件挿入する。」 | 「変更があったテーブルのレコードをすべて削除したうえで、あらかじめ用意しておいたバックアップ用スキーマの同じテーブルからレコードをすべて挿入する。」（`:30`） | 実装は対象テーブル全体をまとめて削除してから挿入する（`MasterDataRestorer.java:322-338`）。出典の書き方はテーブルごとのループとも読める |
| `:100`「slow test問題が発生する場合がある」 | 「テストの実行時間が長くなることがある」（`:165`） | `ja/` 配下に `slow test` の用例が無く、定義もされていない |
| `:189-190`「専用のロガー（何もしないロガー）」／コード内コメント `# 【説明】何もしないロガー` | 「何も出力しないログライター」（`:127`・`:139`） | `NopLogWriter` は `LogWriter` の実装であってロガーではない |
| `:180`・`:192` の `.. code-block:: none` | `.. code-block:: properties` にした（`:123`・`:129`・`:167`） | `style.md` S-06（コードブロックは言語を指定する） |
| `:192-215` のコードブロック内の行末の連続タブと `# 【説明】` 付き行内コメント | 行末の空白を落とし、行内コメントを直前行のコメントに移した（`:139`） | 出典のタブは体裁の崩れであり、内容ではない |
| `:88-91` の tip「マスタデータ復旧用スキーマには全てのテーブルを作成する必要はない。マスタデータ復旧対象とするテーブルのみ存在すればよい（復旧対象以外のテーブルがあっても問題ない）。」 | 「監視対象テーブルとして登録するテーブルのみ存在すればよい」に改めた（`:61`） | 「復旧対象」はページ内で定義していない語。実体は `tablesTobeWatched` に列挙したテーブルであり、本文の語（監視対象テーブル）に揃えた |
| `:1` のラベル `master_data_backup`、`:73` のラベル `master_data_backup_settings`、`:92` のラベル `MasterDataRestore-fk_key`、`:142` のラベル `MasterDataRestore-configuration` | 引き継がず、ページ先頭を `master_data_restore`、節ラベルを `master_data_restore-backup_schema`・`master_data_restore-watched_tables`・`master_data_restore-suppress_table_sort` とした | `style.md` S-08 の命名規則。S-08 の例外（名前を変えない外部被参照ラベル）は `checks/task-07.md`「リンク切れになる参照」の表に載るものだけで、この4件は含まれない。`en/` 側は同名ラベルを自前で定義しているため（`en/.../06_TestFWGuide/04_MasterDataRestore.rst:1`・`:73`・`:92`）影響しない |
| `:41-55` の表と `:118-141` の表の `:class: white-space-normal` | 落とし、`:widths:` のみにした | `style.md` S-05（表は `list-table` ＋ `:widths:`） |
| `:118-141` の表のデフォルト値「なし」 | 「該当なし」にした（`:78`・`:81`） | 承認済みの `setup/request_unit_test/web.rst:34` の表記に合わせた |

### 節ラベルを新設した根拠（前方参照の受け皿）

削除済みの現行解説書に、このページの節を指す `ja/` 側の参照が2件ある。いずれも `#27` の後続ページに割り当たっているため、受け皿となるラベルを先に置いた。

| 参照元（`2e501ad:` 配下） | 参照先ラベル | 参照元の `mapping_id` / `dest_page` | 新設したラベル |
|---|---|---|---|
| `.../06_TestFWGuide/02_DbAccessTest.rst:547`「詳細は :ref:`MasterDataRestore-fk_key` を参照。」 | `MasterDataRestore-fk_key`（`04_MasterDataRestore.rst:92`、外部キーの節） | `current-0196` / コンポーネント単体テスト（`#27-19`、`disposition=REFERENCE`） | `master_data_restore-suppress_table_sort`（`:159`） |
| `.../08_TestTools/02_MasterDataSetup/02_ConfigMasterDataSetupTool.rst:24`「『:doc:`../../06_TestFWGuide/04_MasterDataRestore`』の :ref:`master_data_backup_settings` を参照。」 | `master_data_backup_settings`（`:73`、環境構築） | `current-0359` / マスタデータ投入ツール（`#27-05`） | `master_data_restore-backup_schema`（`:53`） |

`master_data_restore-watched_tables`（`:63`）は、同一ページ内の `:165` からの参照に使っている（出典 `:101` の `:ref:`MasterDataRestore-configuration`` に対応）。

## 4観点レビュー ラウンド1

QA（網羅性）／設計（構成）／クラフト（文章）／検証（実装との一致）を、それぞれ別のサブエージェントで実施した（`steering.md` `Rules`）。依頼プロンプトには3点（実測コマンドで裏付ける／付属の検証スクリプトを正解にしない／敵対的にレビューする）を入れた。

判定: **4観点とも FAIL**。重複を除いた `must` は3件。

### 是正した指摘

| # | 観点 | 指摘 | 是正 |
|---|---|---|---|
| R1-1（`must`） | QA・設計・クラフトの3観点が独立に指摘 | `:51` の「以下の設定をすべて行うことで有効になる」が事実に反する。`nablarch.suppress-table-sort` は任意であり、出典 `:78` も「すべて」とは書いていない | 導入文を必須3件と任意1件に分け、任意の節を「使用方法」の末尾へ移した（上表参照） |
| R1-2（`must`） | QA3・クラフト2・検証6 | `testEventListeners` を `MasterDataRestorer` の設定項目として表に並べていた。実装上このクラスに `setTestEventListeners` は無い | 表を実プロパティ2件に限定し、`testEventListeners` を地の文と `important` に移した（上表参照） |
| R1-3（`must`） | 検証3 | XMLの記述例に `RepositoryInitializer` が無く、そのまま写すとリポジトリの復元が失われる | 記述例に `RepositoryInitializer` を加え、`important` の第2段落（`:115`）で理由を述べた。**この段落の文面は検証ラウンドの V-1 でさらに直している（下記）** |
| R1-4（`should`） | 設計2 | 機能概要の節順が `design.md:216-226`（全体像の図 → 表）に反していた | 「マスタデータを復旧する流れ」を先に、「必要となるスキーマ」を後にした |
| R1-5（`should`） | 検証10 | 復旧の手順を「テーブルを復旧する際、いったん全件削除し、その後全件挿入する」と書いており、テーブルごとのループとも読める | `:30` を「変更があったテーブルのレコードをすべて削除したうえで…すべて挿入する」に改めた |
| R1-6（`should`） | 検証4 | `nablarch.suppress-table-sort` の影響範囲がマスタデータの復旧に限られるように読める。実際は準備データの投入とマスタデータ投入ツールにも及ぶ | `:175` に第2段落を追加した。呼び出し元4件を `git grep` で自分で確認した（上表参照） |
| R1-7（`should`） | 検証11 | `loggers.sql.level` の `important` が「`DEBUG` でなければならない」と読める。`TRACE` でも動作する | 「`DEBUG` を指定する。`INFO` 以上を指定するとSQLログが出力されず、マスタデータの変更を検出できない。」に改めた |
| R1-8（`should`） | クラフト3 | `NopLogWriter` を「ロガー」と呼んでいた | 本文とコード内コメントを「何も出力しないログライター」に改めた |
| R1-9（`should`） | クラフト4 | tip の「復旧対象」がページ内で未定義 | 「監視対象テーブルとして登録するテーブル」に改めた |
| R1-10（`should`） | クラフト7 | `slow test問題` が `ja/` 配下に用例が無い | 「テストの実行時間が長くなることがある」に改めた |
| R1-11（`should`） | クラフト11 | デフォルト値欄の「なし」が承認済みページの表記（「該当なし」）と割れていた | `setup/request_unit_test/web.rst:34` に合わせた |
| R1-12（`info`） | クラフト5 | `:26` の「コンポーネント設定ファイルより」が古い言い回し | 「から」に改めた |
| R1-13（`info`） | クラフト6・設計3 | 「テーブルの依存関係の解析を抑止する」の見出しの語が本文に現れない | 本文を「テーブルの依存関係を解析し」に改め、見出しと本文をつないだ |
| R1-14（`info`） | クラフト9 | 見出しと第1文が同語反復（「バックアップ用スキーマを作成する」の直後に同じ文） | 第1文を短くし、続く文で作業内容を述べる形にした |
| R1-15（`info`） | クラフト12 | `sqlLogFormatter` に指定するクラスを「本機能の提供クラス」としか書いておらず、地の文でクラス名を名乗っていない | `:121` で `SqlLogWatchingFormatter` を名乗るようにした |
| R1-16（`info`） | クラフト13・14 | 1段落に「JDBCの機能」3回、「復旧」3回 | `:163`・`:165` を書き直して重複を減らした |
| R1-17（`info`） | 設計5 | 「以下の」を使っていた | 全件を落とした（現在0件） |

### 対応せず記録に留めた指摘

| # | 観点 | 指摘 | 対応しない理由 |
|---|---|---|---|
| R1-18 | 検証1 | `updateSqlKeywords`（`MasterDataRestorer.java:200-206`、既定は `:54-59` の `INSERT, DELETE, UPDATE, MERGE, TRUNCATE`）が設定項目一覧に無い | 出典の設定項目一覧にも無い。既定値を持つ任意設定であり、出典の範囲外である |
| R1-19 | 検証7 | SQL文の検出は部分一致であり、キーワードを含むだけの文字列（コメント・リテラル）でも変更と判定する（`MasterDataRestorer.java:161-172`、Javadoc `:36-44`） | 出典に記述が無く、動作の正常系を説明する本ページの範囲を超える。下記「判断待ち」3に回す |
| R1-20 | 検証5 | テストクラスが `TestEventDispatcher` を継承していること、および `testTran`（`SimpleDbTransactionManager`）が登録されていることが前提だが、本文が述べていない（`TestEventDispatcher.java:135-149`、`DbAccessTestSupport.java:42`、`MasterDataRestorer.java:322`） | いずれもテスティングフレームワーク全体の前提であり、このページ固有ではない。第2部の共通設定・第3部の各ページが扱う範囲である |
| R1-21 | クラフト10 | 「自動テスト」が新しい体系で定義されていない | 出典自身の語であり（`:39`・`:85`）、`必要となるスキーマ` の表の項目名でもある。語の入れ替えは横断で決める事柄 |
| R1-22 | 検証8 | 外部キーの解析が空文字のスキーマに対して行われる（`MasterDataRestorer.java:131`・`:313-315`・`:349`、`EntityDependencyParser.java:34-48`）。Oracle・PostgreSQL・SQL Server での挙動はレビュー側も **未確認** と記録している | 未確認の事項は本文に書けない。下記「判断待ち」4に回す |

### 是正後の確認

- 是正はすべて `ja/development_tools/testing_framework/setup/master_data_restore.rst` の1ファイルに畳んだ（`#27-01` のコミットに含める。是正を別コミットに割っていない）
- L1・L2 の下線は50、L3 の下線は6本とも49。`unicodedata.east_asian_width` で表示幅を測って確認した（タイトルの表示幅は20、最長のL3見出しは34）
- 全角括弧の直後にインラインリテラルを置いた箇所（`（\ ``testEventListeners``\ ）`）は、`setup/common.rst:51`・`:124`・`:147`・`:181` と同じエスケープ形にした

## 検証ラウンド（是正差分のみ）

是正差分に限定した検証観点を別のサブエージェントで1回実施した（`steering.md` `#10` の共通 Steps「是正ラウンド2以降は、是正差分に限定した検証観点のみを回す」に従う）。依頼プロンプトには Rules の3点を入れた。

判定: **FAIL（`must` 1件・`should` 2件・`info` 6件）**。是正の範囲は逸脱なし（`git status --porcelain` の全件が3エントリ、禁止ファイルの差分0行）。`must` を是正して閉じた。

| # | 種別 | 指摘 | 対応 |
|---|---|---|---|
| V-1 | `must` | R1-3 の `important` 第2段落「``testEventListeners`` は一覧ごと置き換わるため、既に登録しているクラスがある場合は、それらを残したまま追記する」が裏付けられない。置き換えの対象となる既存の一覧が存在しない | **是正した。** 自分でも確認した。`nablarch-testing-default-configuration-6u3.jar` を全展開して `grep -rl "testEventListeners"` が**0件**。`git grep -n "testEventListeners" e21bf67` の main 側ヒットは `TestEventDispatcher.java:25` の定数のみで、未登録なら `getListeners()` が空リストを返す（`TestEventDispatcher.java` の `getListeners()`）。機構の説明を落とし、`RepositoryInitializer` を書く理由を機能で述べる形（`:115`）に改めた |
| V-2 | `should` | デフォルト値「該当なし」の基準がページに書かれておらず、承認済みの `setup/request_unit_test/web.rst:17`・`rest.rst:61`（いずれも「デフォルト値の欄には、デフォルト設定を読み込んだ状態で有効になる値を示す。」）と不揃いである。デフォルト設定には `nablarch/test/master-data-restorer.xml` が同梱されている | **対応せず。** 下記「判断待ち」6に回す |
| V-3 | `should` | 記述例が、雛形に既に `masterDataRestorer` がある状態と接続していない | **対応せず。** 下記「判断待ち」7に回す |
| V-4 | `info` | 是正 R1-4 の根拠に挙げた `design.md:216-226` は、実際のコードブロックが `:216-229`。該当行は `:220`（全体像の図）・`:221`（主なクラスとリソース） | 記録側の行番号のみの問題。本ページの記述に影響しない。本ファイルの該当箇所は `design.md:216-226` のまま残す（節順の根拠は `:220`・`:221`） |
| V-5 | `info` | 「バックアップ用スキーマ」の語が `:22`・`:30` で使われたあと `:46-47` で定義される | 出典（`2e501ad:04_MasterDataRestore.rst:35` と `:53`）にも同じ前方使用があり、節順の入れ替えが作った不整合ではない |
| V-6 | `info` | `:175` の `:ref:`master_data_tool`` の飛び先は現在スタブである | `#27-05` で本文を作る。`#27-00` でスタブを作ってあるためビルドは通る |
| V-7 | `info` | 追加した2ラベルの被参照はまだ成立していない（`#27-05`・`#27-19` が未作成） | 意図どおり。上記「節ラベルを新設した根拠」のとおり、受け皿を先に置いた |
| V-8 | `info` | `:157` の `important` が `TRACE` でも動く点に触れていない | 指示形（「`DEBUG` を指定する」）であり誤りではない。R1-7 で判断済み |
| V-9 | `info` | 表が `updateSqlKeywords` を載せていない | 導入文が「主な設定項目」と限定しているため整合する。R1-18 で判断済み |

### 検証ラウンドが独立に確認した事実（いずれも本文と一致）

- `SystemRepository.getBoolean` は未登録なら `false` を返すため、`nablarch.suppress-table-sort` が任意設定であること
- `TableDataSorter` の `src/main` 側呼び出しが3クラス（`DbAccessTestSupport`・`MasterDataSetUpper`・`MasterDataRestorer`）に限られ、判定がグローバルであること
- `BasicSqlPStatement.java:1282` の `if (SQL_LOGGER.isDebugEnabled())` と `LogLevel.java:8` の順序（`FATAL > ERROR > WARN > INFO > DEBUG > TRACE`）から、`INFO` 以上では検出できないこと
- `NopLogWriter implements LogWriter` であること
- 削除済み解説書からの被参照が2件のみ実在し、`style.md:314-316` の改名しない例外には当たらないこと。新設した2ラベルは `ja/` 配下で重複0件
- `MasterDataRestorer.TableDuplicator.restoreAll()` が全件削除→全件コピーの順で、テーブル単位のループではないこと

### 検証ラウンド後の再ビルド

V-1 の是正後に Docker フルビルド（`sphinx-build -E`）を再実行し、`build succeeded, 1 warning.`（既知の `db_double_submit.rst:108` のみ・新規0件）。ビルド直後に `sphinx.mo` を復元した。

## ゲート

`checks/task-27.md` の `#27-01` の節を参照。

## 判断待ち（週明けに判定してほしい項目）

1. **`current-0245`（`03_Tips.rst:725-730`）を落とした。** 実物を開いて確認したところ、「:doc:`04_MasterDataRestore` を参照」の1文だけで構成される、このページへの導線用の節である。移す本文が無いため `#27-01` では消化していない。同等のリンクは承認済みの `implementation/testdata_notation.rst:40` が既に持っている。G10 の意図的な取りこぼしとして扱ってよいか判定してほしい。
2. **`TableDataSorter.java:16-18` の Javadoc に「（DBにFKが設定されていない場合にのみ使用すること。）」とある。** 一方で出典 `:94-107` は、この設定を「外部キーが設定されたテーブルを使用する場合について」の節に置き、外部キーがある場合の運用として説明している。作業指示 §1-2 に従い、最も出典に忠実な選択（外部キーがある場合も、列挙順を親→子にすれば使える）を採った。Javadoc が正なら本文の `important`（`:173`）を「外部キーが設定されている場合は使用しない」に変える必要がある。
3. **SQL文の検出が部分一致であること（R1-19）を書くかどうか。** 出典に記述が無い。書く場合は「機能概要 > マスタデータを復旧する流れ」に注記を足すことになる。
4. **外部キー解析のスキーマ指定（R1-22）。** `MasterDataRestorer.java:131` が空文字のスキーマ名で `DatabaseMetaData#getImportedKeys` を呼ぶ。H2 以外のDBでの挙動が未確認であり、本文には書いていない。DB製品ごとの検証が必要かどうか判定してほしい。
5. **`style.md:344` がこのページを「マスタデータ復旧機能（スタブ）」と書いたままである。** `style.md` は G2 の変更禁止ファイルのため触っていない。`#pre-last` で一括して直すか、都度直すかを決めてほしい。
6. **デフォルト値「該当なし」の基準を書くかどうか（V-2）。** 実物を確認したところ、デフォルト設定 `nablarch-testing-default-configuration-6u3.jar` には `nablarch/test/master-data-restorer.xml` が同梱されており、`backupSchema=${nablarch.masterDataRestorer.backupSchema}`（値は同梱の `master-data-restorer.config` で `nablarch_test_master`）と17テーブルの `tablesTobeWatched` を定義している。ただし `nablarch-example-batch/src/test/resources/unit-test.xml` はこれを `<import>` しておらず（`:16-17` で読むのは `nablarch/test/test-data.xml` と `nablarch/test/test-transaction.xml` のみ）、`:38-49` で `masterDataRestorer` を自前で定義している。出典もデフォルト値を「なし」としているため「該当なし」のままにした。承認済みの `setup/request_unit_test/web.rst:17`・`rest.rst:61` は基準を1文で明示しており、そちらに揃えるなら「このコンポーネントはデフォルト設定を読み込んでも登録されないため、どちらも明示的に指定する」旨を足すことになる。あわせて、同梱の `master-data-restorer.xml` を読者に案内するかどうかも判定してほしい（17テーブルはNablarch側のサンプル用テーブルであり、そのまま使える性質のものではない）。
7. **記述例を、雛形がある前提に書き換えるかどうか（V-3）。** `nablarch-example-batch/src/test/resources/unit-test.xml` は `masterDataRestorer` を `:38-49` に持ち、`testEventListeners` の一覧を `:51-56` にコメントアウトで持っている。読者の作業は「書き足す」より「値を埋めてコメントを外す」に近い。出典（`:145-166`）は一から書き起こす形なので、出典に忠実な現状のままにした。なお `nablarch-web-archetype` の jar はこの環境の `~/.m2/repository` に存在せず、アーキタイプが生成する `unit-test.xml` の内容は **未確認** である。
