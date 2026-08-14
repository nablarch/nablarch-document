# page-master_data_tool

対象ページ: `ja/development_tools/testing_framework/tools/master_data_tool.rst`（`#27-05`）
`dest_page` = マスタデータ投入ツール（13行 / 177行）

## 参照リポジトリ

| リポジトリ | 参照コミット | 用途 |
|---|---|---|
| `/home/tie303177/work/nablarch/nablarch-testing` | `e21bf67` | `MasterDataSetUpper` / `MasterDataRestorer` / `BasicTestDataParser` / `PoiXlsReader` |
| `/home/tie303177/work/nablarch/nablarch-testing-yaml` | `190cc9a` | `YamlTestDataParser` / `YamlLoader` |
| 配布物 `master-data-setup-tool.zip` | 本リポジトリ内（`2e501ad` 時点から md5 不変） | `master_data-build.xml` / `master_data-build.properties` / `MASTER_DATA*.xls` |

`e21bf67` は作業ツリー HEAD の祖先ではないため、参照はすべて `git show e21bf67:<path>` で行った。

## 出典行の消化

出典はすべて `git show 2e501ad:ja/development_tools/testing_framework/guide/development_guide/08_TestTools/02_MasterDataSetup/` 配下。

| mapping_id | 出典 | 行 | dest_section | 消化先 |
|---|---|---|---|---|
| current-0365 | `index.rst` | 4-21 | 機能概要 | tip（gsp）・マルチスレッドの1文。toctree は落とした |
| current-0353 | `01_MasterDataSetupTool.rst` | 9-13 | 機能概要 | 機能概要の地の文 |
| current-0354 | 〃 | 16-28 | 機能概要 | 特徴3項目・マルチスレッドの1文。脚注（バックアップ用スキーマ）は前提事項へ |
| current-0355 | 〃 | 34-36 | 使用方法 | REFERENCE。使用方法のリード文で `:ref:`導入 <master_data_tool-setup>`` を張った（G11） |
| current-0356 | 〃 | 39-42 | 使用方法 | 「マスタデータを記述する」 |
| current-0357 | 〃 | 45-71 | 使用方法 | 「Antビューからターゲットを実行する」。grid table は `list-table` に変換（S-07） |
| current-0358 | `02_ConfigMasterDataSetupTool.rst` | 4-8 | 導入 | 導入のリード文 |
| current-0359 | 〃 | 11-27 | 導入 | 前提事項 |
| current-0360 | 〃 | 30-68 | 導入 | 「依存jarを取得して配布物を展開する」。grid table は `list-table` に変換 |
| current-0361 | 〃 | 71-84 | 導入 | 「バックアップ用スキーマ名を設定する」 |
| current-0362 | 〃 | 87-90 | 導入 | 「AntビューにAntビルドファイルを登録する」のリード文 |
| current-0363 | 〃 | 93-101 | 導入 | 同節の手順1 |
| current-0364 | 〃 | 104-122 | 導入 | 同節の手順2・3 |

## 意図して落とした出典

| 出典 | 落とした内容 | 理由 |
|---|---|---|
| `index.rst:16-20` | toctree | 1ページ統合により不要（`design.md:352`） |
| `02_ConfigMasterDataSetupTool.rst:61-66` | `mvn compile` / `mvn dependency:copy-dependencies` の再掲 | 導入に1回だけ置いた。再コンパイルの必要性は使用方法のリード文に1文で残した |
| `02_ConfigMasterDataSetupTool.rst:118-121` | 「Antビューに登録したビルドファイルが表示されることを確認する」＋ `build_file_in_view.png` | 画像は使用方法で再利用。確認の1文は導入の末尾に残した |

## 出典と実物が食い違い、実物を採った箇所

`design.md` §8「出典と実装が食い違えば実装優先」に従い、以下は配布物の実物に合わせた。

| 出典の記述 | 実物 | 確認方法 |
|---|---|---|
| `MASTER_DATA.xlsx`（`01_MasterDataSetupTool.rst:40`） | `MASTER_DATA.xls` | `unzip -l master-data-setup-tool.zip` |
| `tool/db/data/` 配下の5ファイル、「ディレクトリ付きで展開」（`02_Config...:41,47-59`） | ディレクトリを持たない6ファイル（`MASTER_DATA-FOR_UI_TEST.xls` を含む） | 同上 |
| `masterdata.test.backup-schema=nablarch_test_master`（`02_Config...:78`） | `NABLARCH_TEST_MASTER` | 展開後の `master_data-build.properties:26` |

zip は `2e501ad` 時点のものと md5 が一致する（`b46396ea54401eed13669b62f17736e8`）。出典の記述が当時から実物と食い違っていた。

## 実装で確認した事実（出典に無い、または出典より詳しい）

| 事実 | 出典 |
|---|---|
| 投入対象は準備データ（`SETUP_TABLE`）のみ | `MasterDataSetUpper.java:191` → `BasicTestDataParser.java:50-57`（`DataType.SETUP_TABLE_DATA` 固定） |
| バックアップ用スキーマへは、マスタデータファイルに記述した全テーブルをコピーする | `MasterDataSetUpper.java:109-115` → `MasterDataRestorer.java:283-339`（`TableDuplicator` は `targetTableNames` を絞り込まない） |
| `masterdata.test.backup-schema` を空にするとバックアップ用スキーマへの投入を行わない | `MasterDataSetUpper.java:113-115`（`StringUtil.isNullOrEmpty`）、`master_data-build.xml:50`（`データ投入(main)` が空文字を渡す経路と同じ） |
| `testDataParser` が `YamlTestDataParser` のとき、投入対象が0件になりエラーにならない | `MasterDataSetUpper.java:185`（Excelのシート名は読める）→ `:188-191`（`SystemRepository` から `testDataParser` を取得）→ `YamlTestDataParser.java:102-111` → `YamlLoader.java:142-143`（`<dir>/MASTER_DATA/<シート名>.yaml` を `File#exists` で判定）→ 空リスト。`MasterDataSetUpper.java:106-116` で `tablesFinished` も空になり、`MasterDataRestorer.java:318-321` で複製も行われない |
| シートの読み込み順は保証されない | `PoiXlsReader.java:204-212`（`getSheetNames` は `HashSet` を返す） |
| 削除は全ファイル読み込み後にまとめて行う。ただし行が重複すれば一意性制約違反になる | `MasterDataSetUpper.java:105-116,142-150`、クラスJavadoc `:25-28`（「一意性制約違反が無い場合」） |
| 削除・挿入順はテーブル依存関係の解析で決まり、`nablarch.suppress-table-sort` で記述順になる | `MasterDataSetUpper.java:158,170` → `TableDataSorter.java:31,89` |
| 投入に失敗しても Ant は `BUILD SUCCESSFUL` を返す | `master_data-build.xml:77`（`<java ... fork="true">` に `failonerror` の指定が無い＝既定の `false`） |
| `main.classpath` は `src/main/resources` → `src/test/resources` の順。前者にコンポーネント設定ファイルが無ければ後者が使われる | `master_data-build.xml:29-39`、`master_data-build.properties:15`（`masterdata.config=classpath:unit-test.xml`） |
| 相対パスの基準はビルドファイルの位置 | `master_data-build.xml:2`（`basedir="."`）、`master_data-build.properties:2,17`（いずれも `./`） |
| `.xlsx` は既定パターン `MASTER_DATA*.xls` に一致しない | `master_data-build.properties:19`、`master_data-build.xml:65-67` |
| 配布物の2つのマスタデータファイルはサンプルアプリケーションの実データ | `MASTER_DATA.xls` 7シート（`SYSTEM_ACCOUNT` / `MESSAGE` / `REQUEST` / `ID_GENERATE` / `CODE_NAME` / `MAIL_TEMPLATE` / `FORMATTER_SAMPLE_INFO`）、`MASTER_DATA-FOR_UI_TEST.xls` 1シート116行（`SETUP_TABLE=REQUEST`） |

## 移送したアセット

| 移送元（`guide/` 配下） | 移送先 |
|---|---|
| `08_TestTools/02_MasterDataSetup/_image/open_ant_view.png` | `tools/images/master_data_tool/open_ant_view.png` |
| `08_TestTools/02_MasterDataSetup/_image/register_build_file.png` | `tools/images/master_data_tool/register_build_file.png` |
| `08_TestTools/02_MasterDataSetup/_image/select_build_file.png` | `tools/images/master_data_tool/select_build_file.png` |
| `08_TestTools/02_MasterDataSetup/_image/build_file_in_view.png` | `tools/images/master_data_tool/build_file_in_view.png` |
| `08_TestTools/02_MasterDataSetup/download/master-data-setup-tool.zip` | `tools/downloads/master_data_tool/master-data-setup-tool.zip` |

いずれも `git mv`。移送元ディレクトリは空になった。

## 4観点レビュー（QA / 設計 / クラフト / 検証）

4観点をそれぞれ別のサブエージェントで実施。指摘は延べ70件（QA 17件＝M2/S8/N7、設計 21件＝M3/S8/N7＋規約提案3、クラフト 20件＝M5/S8/N7、検証 12件＝NG2/未確認1/補足9）。うち44件を採用し、本文への是正33箇所に畳んだ。不採用は9件。残りは記録のみ、または他の指摘の是正で解消した。

### 採用した指摘

| 観点 | 指摘 | 対応 |
|---|---|---|
| QA M-1 | 前提事項が「バックアップ用スキーマにテーブルが作成済み」としか書いておらず、飛び先の tip は「監視対象テーブルのみでよい」。本ツールは全テーブルをコピーするので手順どおりだと失敗する | 前提事項を「マスタデータファイルに記述するすべてのテーブル」に改め、ターゲット表にもコピー範囲を明記 |
| QA M-2 | 投入対象は `SETUP_TABLE` のみだが、飛び先の節は4つのデータタイプを扱う | 「準備データ（`SETUP_TABLE`）として記述する」「期待値のデータタイプは投入の対象にならない」を明記 |
| 設計 M-2 | `testDataParser` が YAML 形式用のとき、無言で0件になる | `important` を新設 |
| 設計 M-1 / QA S-1 / クラフト M-2 | 前提事項（blank_project 必須）と tip（gsp を推奨）が同一ページ上で矛盾 | 前提事項を「Mavenの標準ディレクトリ構成（blank_project のアーキタイプはこれに該当）」に改め、tip を「gsp でマスタデータを管理する場合は本ツールを導入する必要はない」に限定 |
| 設計 S-1 / 検証 NG-10 | マルチスレッドの `important` はツール固有の制約ではなく、第1部が持つ NTF 全体の事実 | `important` をやめ、`:ref:`testing_framework_about`` への1文に置き換え |
| 検証 NG-3 / QA S-7 / クラフト N-7 | 「実行ディレクトリからの相対パス」は誤り。基準は `basedir` | tip を `master_data-build.xml:2` の `basedir="."` を根拠にした説明に書き換え |
| 設計 S-4 / QA N-5 | シート順は保証されない。一意性制約違反の但し書きも落ちている | tip から「先のシート／あとのシート」を外し、両方を追記 |
| 設計 S-3 | `nablarch.suppress-table-sort` への導線が無い（第2部からは一方向で参照されている） | tip に1文追加 |
| 設計 S-5 / 検証 #9 | `tablesTobeWatched` の指摘が片方向。影響も「再実行時」ではなく同一実行内の後続テスト | 双方向に書き直し、影響を「後続のテスト」に修正 |
| 設計 S-6 / QA S-2 | `masterdata.config` に触れておらず「その他は修正不要」が言い過ぎ | 1文追加 |
| QA S-3 | 「記述例が入っている」は過小。実データが入っており、そのまま実行すると全テーブルが置き換わる | 書き換え。用語 `記述例` の誤用も解消 |
| QA S-4 | `データ投入(main)` の説明は `src/main/resources` に設定ファイルがある場合にのみ成立 | フォールバックを明記 |
| QA S-5 | リード文が投入先2つと読めるが、既定ターゲットでは3スキーマ | 「アプリケーション用・自動テスト用・バックアップ用」に修正 |
| QA S-8 | 復旧機能を使わない読者の逃げ道が無い | 「この値を空にする」を追記 |
| QA S-6 / クラフト M-5 | 「同じディレクトリ」の指示語に先行詞が無い | `masterdata.dir` を明示 |
| クラフト M-3 / QA N-4 | Antビューのアイコン説明が位置だけで、たどり着けない | ボタン名（「ビルド・ファイルの追加(Add Buildfiles)」）と図柄を併記。画像を8倍に拡大して自分でも確認した |
| クラフト M-4 | 「ビルドファイルを開き」はAntビュー登録時の操作ではない。「展開」が zip の意味と衝突 | 手順を「展開した `master_data-build.xml` を選び」に修正 |
| クラフト M-1 | リード文が同語反復で、読者の利得が無い | 末尾に1文追加 |
| クラフト S-1 | 「テストデータと同じ形式」が4行後の YAML 除外と衝突 | 「同じ書式で Excel ファイルに記述する」に変更 |
| クラフト S-2 | 「同時に」の相手が書かれていない | 「同じターゲットの実行でまとめて」に変更 |
| クラフト S-3 | 「この投入を…ファイルから行う」が不自然 | 機能概要の地の文を書き換え |
| クラフト S-5 | 「自動テストで使用するスキーマ」は NTF 内で唯一の表記 | 「自動テスト用スキーマ」に統一 |
| クラフト S-6 | 2つのマスタデータファイルの説明が同一 | `MASTER_DATA-FOR_UI_TEST.xls` に `REQUEST` テーブルである旨を追記 |
| クラフト N-1 | 「APサーバ」13件 / 「アプリケーションサーバ」52件 | 「アプリケーションサーバ」に統一 |
| 検証 補足1 | 投入に失敗しても `BUILD SUCCESSFUL` になる | `important` を新設 |
| 設計 N-1 | tip（gsp）と important の順序が出典と逆 | tip を先に置いた |
| 設計 N-3 | 配布物のプロパティファイルのコメントは Unicode エスケープで、ページに載せた日本語コメントは実物と一致しない | コードブロックからコメント行を削除 |
| 設計 N-5 | `.xlsx` は既定パターンに一致しない | 1文追加 |
| 設計 N-6 | 前提事項がバックアップ用スキーマへのデータ投入を求めており、循環に見える | 「テーブルを作成しておくだけでよい」を追記 |
| 設計 N-7 | 導入と使用方法の L3 見出しが紛らわしい | 導入側を「AntビューにAntビルドファイルを登録する」に変更 |
| 設計 S-2 | `nablarch-testing` を依存関係に宣言する必要に触れていない | 前提事項に `:ref:`共通設定 <testing_framework_common>`` の1行を追加 |
| 設計 N-2 / QA N-2 | 登録後の確認手順が落ちている | 導入の末尾に1文追加 |
| QA N-3 | `tablesTobeWatched` を持つコンポーネント設定ファイル名が分からない | `masterdata.config`（既定 `classpath:unit-test.xml`）をページ内に書いたことで解消 |

### 採らなかった指摘

| 観点 | 指摘 | 判断 |
|---|---|---|
| 設計 S-7 / QA N-7 | L3 見出しの下線を `~` 49文字に揃える（多数派） | `style.md` S-04（`style.md:195`）は「タイトル文字列と同じ長さ以上」しか定めておらず違反ではない。`request_data_tool.rst` も50文字で、片方だけ直すと第4部内でさらに割れる。規約側の判断に回す（判断待ち参照） |
| 設計 N-4 | パスに空白が含まれると `<arg line>` が分割する | エージェント自身が「コードを読んだだけで実行未確認」としている。配布物の既定構成では再現条件が作れないため、記録のみ |
| クラフト S-7 | `MasterDataSetUpper` のソースがリポジトリに無く未確認 | 誤り。`e21bf67` で読める。検証観点も独立に確認済み |
| 検証 補足2・7・8 | 対象ファイルが0件でも成功する / `build/classes` が存在しない / `mvn compile` は `target/test-classes` を作らない | 配布物側の整理に関わる話で、ページの読者が取る行動を変えない。記録のみ |
| QA M-1 後段 | `master_data_restore.rst:59-61` の tip に但し書きを足す | 別ページ（`#27-01`）の変更になる。1ページ1コミットの原則により、判断待ちに回す |
| QA N-6 | `:ref:`gsp-dba-maven-plugin <gsp-maven-plugin>`` のリンク文字列が飛び先の見出し（`addin_gsp.rst:3-5`「gsp-dba-maven-plugin(DBA作業支援ツール)の初期設定方法」）と一致しない | 意図的な短縮。出典（`index.rst:9`）も同じ書き方で、`testdata_notation.rst:40` も同じ。記録のみ |

## ゲート

作業指示 §5 の G1〜G13。

| | 結果 | 根拠 |
|---|---|---|
| G1 | **PASS** | `git status --porcelain`（ディレクトリで絞らずに実行）は `R` 5件（`_image/` の png 4件と `download/master-data-setup-tool.zip` の `git mv`）と ` M ja/.../tools/master_data_tool.rst`。記録3本（本ファイル・`checks/task-27.md`・`steering.md`）を加えても想定内 |
| G2 | **PASS** | `design.md`・`mapping/style.md`・`mapping/glossary.md`・`mapping/vocabulary.md`・`ja/conf.py`・`mapping/input/` を明示指定した `git status --porcelain` が0行 |
| G3 | **PASS** | `locales/ja/LC_MESSAGES/sphinx.mo` は `git status --porcelain` に現れない。ビルド直後に `git checkout --` で戻している |
| G4 | **PASS** | `verify_mapping.py` が exit 0。`mapping.csv` は未変更 |
| G5 | **PASS** | Docker フルビルド（`sphinx-build -E`）が `build succeeded, 1 warning.`。警告は既知の `ja/application_framework/application_framework/libraries/db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test` 1件のみで、**新規0件**。是正を全件畳んだ後の最終本文で再実行して確認した |
| G6 | **PASS** | 禁止語（`不具合`・`バグ`・`将来`・`修正され`）0件。あわせて `本ページ\|下さい\|出来る\|事が\|以下の\|上記の\|利用\|前提条件\|スーパークラス` も0件、`.. note::`／`.. warning::` も0件（`tip` 2件・`important` 3件）。`です。`／`ます。` 0件 |
| G7 | **PASS** | ページ先頭ラベル `master_data_tool` が `mapping/style.md:348` と一致。`master_data_tool` / `master_data_tool-setup` はいずれも `ja/` 全体で一意 |
| G8 | **PASS** | `unicodedata.east_asian_width` で表示幅を測り、全10見出しについて「下線の文字数 ≥ 見出しの表示幅」を検査して NG 0件（下線は全件50、表示幅の最大は38） |
| G9 | **PASS** | `:ref:` 12件がすべて解決し、リンク文字列も飛び先の見出しと一致（例外は `gsp-dba-maven-plugin` の意図的な短縮1件。下記「採らなかった指摘」参照）。`:download:` 1件・`:java:extdoc:` 1件・`.. image::` 4件もビルドで解決 |
| G10 | **PASS** | 13行177行すべてを分類。落としたのは3件で、理由は「意図して落とした出典」に記載 |
| G11 | **PASS** | `disposition=REFERENCE` は `current-0355` 1件。使用方法のリード文で `:ref:`導入 <master_data_tool-setup>`` に変換し、節としては起こしていない |
| G12 | **PASS** | 枝分かれ（`-a`／`-b`）の `mapping_id` が無い。`src_file` 3本はいずれも本ページ専用 |
| G13 | **PASS** | `.. image::` 4件のファイルが `tools/images/master_data_tool/` に実在し、`:download:` の zip も `tools/downloads/master_data_tool/` にある。`git ls-files guide/development_guide/08_TestTools/02_MasterDataSetup/` が0件で、移送元ディレクトリは残っていない |

表形式は grid table 0件、`list-table` 2件でいずれも `:widths:` 指定あり（S-07）。`.. contents:: 目次` / `:depth: 3` / `:local:` も規約どおり（S-09）。

## 判断待ち

1. **L3 見出しの下線長**（設計 P-1）。`~` は 49文字が15ファイル、50文字が3ファイル（`testdata_examples` / `request_data_tool` / `master_data_tool`）。`style.md` S-04 に固定値を定めるかどうか。定める場合、既存ページの一括修正を伴う。
2. **第4部のセクション構成**（設計 P-2）。「前提事項」を機能概要配下（`testdata_converter.rst:57`）に置くか、導入配下（`request_data_tool.rst:26` / 本ページ）に置くかが割れている。`style.md` S-02 は第2部・第3部しか定めていない。
3. **承認済みページが持つ事実の重複**（設計 P-3）。`design.md:522` の「承認済みページが同じ事実を持つ場合は `:ref:` で導線を張る」は「出典に無い追記」の節にあり、出典由来の重複には適用されない。§5 に一般則として置くかどうか。
4. **`master_data_restore.rst:91` のスキーマ名**。本ページは配布物どおり `NABLARCH_TEST_MASTER`（大文字）、`master_data_restore.rst:91` の設定例は `nablarch_test_master`（小文字）。承認済みページの変更になるため保留。DB によるスキーマ名の大文字小文字の扱いの違いは未確認。
5. **`master_data_restore.rst:59-61` の tip**（QA M-1 後段）。「バックアップ用スキーマには監視対象テーブルのみでよい」は復旧機能単独では正しいが、本ツールを併用する場合はマスタデータファイルに記述した全テーブルが必要。本ページ側の前提事項で手当てしたが、承認済みページ側にも但し書きを足すかどうか。
6. **`testdata_notation.rst:40` の gsp への言及**（設計 P-3 後段）。`mapping.csv` 上、gsp の推奨（`current-0365`）は本ページにのみ割り当てられている。また出典（`01_Abstract.rst:607-609`）は gsp に触れていない。`testdata_notation.rst` 側を導線に絞るかどうか。承認済みページの変更になるため保留。
7. **`testDataParser` が YAML 形式用のときの挙動**（設計 M-2）。本ページには「本ツールを使用できない」と適用範囲として書いたが、投入対象が0件になりエラーにもならない挙動そのものを本体側で扱うかどうかは、本作業の範囲外として保留。
8. **配布物の整理**。`master_data-build.properties:7` のキー名 `protect.main.resources`（`project` の誤り。`master_data-build.xml:25` も同じ綴りで参照しているため片方だけ直すと壊れる）、`master_data-build.xml:84-85` の存在しない `build/classes` / `build/test-classes`。いずれもページの記述には影響しない。
