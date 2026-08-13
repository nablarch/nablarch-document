# task-05b self-check

## STEP 1: `check_unused_vocabulary` の追加とREDの確認

`mapping/tools/verify_mapping.py` に `check_unused_vocabulary`（`SECTION_TEMPLATE` /
`EXPECTED_ZERO_PAGES` / `EXPECTED_ZERO_SECTIONS` / `PENDING_ZERO` を使った3分類判定）
を追加し、`main()` に組み込んだ。

### 実行結果

```
$ python3 mapping/tools/verify_mapping.py > /tmp/red_output.txt 2>&1; echo "EXIT: $?"
EXIT: 1
```

```
Loaded 591 rows from mapping.csv

pending zero assignments: 0 (awaiting #6 decision)
lines total (all rows): 12986
lines total (excluding DROP): 11973

candidate duplicate destinations: 44 (advisory only, not auto-fixed)
...(check_duplicate_destinationsの既存出力。#5から変更なし)...

28 error(s):
 - page [第2部 導入と設定 > テストデータの形式]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_PAGES / PENDING_ZERO)
 - page [第2部 導入と設定 > 取引単体テストの設定（Nablarchバッチアプリケーション）]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_PAGES / PENDING_ZERO)
 - page [第2部 導入と設定 > 取引単体テストの設定（ウェブアプリケーション）]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_PAGES / PENDING_ZERO)
 - section [第1部 テスティングフレームワークとは > テスティングフレームワークとは > 稼動環境]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > クラス単体テストの設定 > 機能概要]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > クラス単体テストの設定 > 拡張例]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > マスタデータ復旧機能 > 拡張例]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > リクエスト単体テストの設定（HTTPメッセージング） > 機能概要]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > リクエスト単体テストの設定（HTTPメッセージング） > 拡張例]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > リクエスト単体テストの設定（MOMによるメッセージング） > 機能概要]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > リクエスト単体テストの設定（Nablarchバッチアプリケーション） > 機能概要]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > リクエスト単体テストの設定（Nablarchバッチアプリケーション） > 拡張例]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > リクエスト単体テストの設定（RESTfulウェブサービス） > 機能概要]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > リクエスト単体テストの設定（RESTfulウェブサービス） > 拡張例]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > リクエスト単体テストの設定（ウェブアプリケーション） > 機能概要]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > 共通設定 > 機能概要]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > 共通設定 > 拡張例]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > 取引単体テストの設定（HTTPメッセージング） > 機能概要]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > 取引単体テストの設定（HTTPメッセージング） > 拡張例]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > 取引単体テストの設定（MOMによるメッセージング） > 機能概要]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > 取引単体テストの設定（MOMによるメッセージング） > 拡張例]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第3部 テストの実装方法 > テストデータの書き方 > 機能概要]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第3部 テストの実装方法 > テストデータの記載例 > 機能概要]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第3部 テストの実装方法 > リクエスト単体テスト（HTTPメッセージング） > 機能概要]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第3部 テストの実装方法 > 取引単体テスト（HTTPメッセージング） > 機能概要]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第3部 テストの実装方法 > 取引単体テスト（Nablarchバッチアプリケーション） > 機能概要]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第3部 テストの実装方法 > 取引単体テスト（ウェブアプリケーション） > 機能概要]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第4部 ツール > テストデータ変換ツール > 導入]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
```

`lines total (all rows): 12986` / `lines total (excluding DROP): 11973` / `Loaded 591 rows` は
`#5` 完了時点と不変。

### 件数の差異（作業指示「17件」）についての調査

作業指示の要約行は「ページ単位0件: 3件」「セクション単位0件: 14件」（計17件）としていたが、
実測は28件（ページ3件・セクション25件）だった。原因を切り分けるため、作業指示の詳細部分
（STEP 2の16行の表＋別記の「マスタデータ復旧機能」＋STEP 4「第1部『稼動環境』」）と
実測結果を突合した。

- ページ単位: 3件（作業指示の要約と一致）
- セクション単位: 作業指示のSTEP 2詳細表（16行）を「不足」列で展開すると
  `機能概要`単独7・`拡張例`単独0・両方9`（1行あたり2件）` … 実際に1行ずつ数えると
  23件、それに「マスタデータ復旧機能 > 拡張例」1件を加えて24件。これは作業指示が
  STEP 4で別扱いにすると明記した「第1部『稼動環境』」を含んでいない数。
  実測のセクション単位25件は、この24件に「第1部 > テスティングフレームワークとは >
  稼動環境」を加えた数と**完全一致**した。

つまり作業指示本文の「14件」という要約値は、詳細な16行表・マスタデータ復旧機能の
言及・STEP 4で扱うとされた稼動環境の存在と整合しておらず、要約行自体の誤記（下位互換の
概算値）と判断する。詳細な列挙内容（STEP 2の16行表＋マスタデータ復旧機能＋STEP 4の
稼動環境）と実測は1件の過不足もなく一致するため、`check_unused_vocabulary` の実装を
そのまま維持し、STEP 2 に進む。

以下、実測28件と作業指示に列挙された項目の対応表（すべて一致）。

| 実測での分類 | 実測の (dest_part, dest_page[, dest_section]) | 作業指示での対応箇所 |
|---|---|---|
| page | 第2部 > テストデータの形式 | STEP 2ページ単位要約・STEP 4報告項目2 |
| page | 第2部 > 取引単体テストの設定（ウェブアプリケーション） | STEP 2ページ単位要約・STEP 4報告項目3 |
| page | 第2部 > 取引単体テストの設定（Nablarchバッチアプリケーション） | STEP 2ページ単位要約・STEP 4報告項目3 |
| section | 第1部 > テスティングフレームワークとは > 稼動環境 | STEP 4報告項目1（STEP 2表には含まれない旨が明記されている） |
| section | 第2部 > クラス単体テストの設定 > 機能概要 | STEP 2表 #1 |
| section | 第2部 > クラス単体テストの設定 > 拡張例 | STEP 2表 #1 |
| section | 第2部 > 共通設定 > 機能概要 | STEP 2表 #2 |
| section | 第2部 > 共通設定 > 拡張例 | STEP 2表 #2 |
| section | 第2部 > リクエスト単体テストの設定（ウェブアプリケーション） > 機能概要 | STEP 2表 #3 |
| section | 第2部 > リクエスト単体テストの設定（RESTfulウェブサービス） > 機能概要 | STEP 2表 #4 |
| section | 第2部 > リクエスト単体テストの設定（RESTfulウェブサービス） > 拡張例 | STEP 2表 #4 |
| section | 第2部 > リクエスト単体テストの設定（HTTPメッセージング） > 機能概要 | STEP 2表 #5 |
| section | 第2部 > リクエスト単体テストの設定（HTTPメッセージング） > 拡張例 | STEP 2表 #5 |
| section | 第2部 > リクエスト単体テストの設定（Nablarchバッチアプリケーション） > 機能概要 | STEP 2表 #6 |
| section | 第2部 > リクエスト単体テストの設定（Nablarchバッチアプリケーション） > 拡張例 | STEP 2表 #6 |
| section | 第2部 > リクエスト単体テストの設定（MOMによるメッセージング） > 機能概要 | STEP 2表 #7 |
| section | 第2部 > 取引単体テストの設定（HTTPメッセージング） > 機能概要 | STEP 2表 #8 |
| section | 第2部 > 取引単体テストの設定（HTTPメッセージング） > 拡張例 | STEP 2表 #8 |
| section | 第2部 > 取引単体テストの設定（MOMによるメッセージング） > 機能概要 | STEP 2表 #9 |
| section | 第2部 > 取引単体テストの設定（MOMによるメッセージング） > 拡張例 | STEP 2表 #9 |
| section | 第2部 > マスタデータ復旧機能 > 拡張例 | STEP 2「マスタデータ復旧機能の拡張例0件も検査に引っかかる」 |
| section | 第3部 > テストデータの書き方 > 機能概要 | STEP 2表 #10 |
| section | 第3部 > テストデータの記載例 > 機能概要 | STEP 2表 #11 |
| section | 第3部 > リクエスト単体テスト（HTTPメッセージング） > 機能概要 | STEP 2表 #12 |
| section | 第3部 > 取引単体テスト（ウェブアプリケーション） > 機能概要 | STEP 2表 #13 |
| section | 第3部 > 取引単体テスト（Nablarchバッチアプリケーション） > 機能概要 | STEP 2表 #14 |
| section | 第3部 > 取引単体テスト（HTTPメッセージング） > 機能概要 | STEP 2表 #15 |
| section | 第4部 > テストデータ変換ツール > 導入 | STEP 2表 #16 |

28行すべてに対応する記述が作業指示にあり、逆に実測にない項目（作業指示にあるのに
検出されないもの）も0件。過不足なし。

## STEP 2: `機能概要`/`拡張例`/`導入` 0件の再判定

対象16ページ＋マスタデータ復旧機能（拡張例）の全該当行を機械抽出し、`git show
c24190607fef5d76c607aa08b36d2ab2f813efe5:<path>`（current）または作業ツリー（input）で
出典を通読して1行ずつ判定した。機械的な一括変更はしていない。

### 変更した行（4行）

| mapping_id | ページ | 旧→新 | 根拠（file:line） |
|---|---|---|---|
| current-0142 | 第3部 取引単体テスト（ウェブアプリケーション） | 使用方法→機能概要 | `03_DealUnitTest/index.rst:6-13`。本文は「取引単体テストでは、テスト対象のアプリケーションをアプリケーションサーバにデプロイし、手動でアプリケーションを操作しテストを行う」という取引単体テストの定義と「テストケース毎に以下の手順でテストを実施する」という後続手順への橋渡し文のみ。後続の「テスト準備」「テスト実施」（current-0143〜0145、手順そのもの）とは独立したページ冒頭のスコープ説明であり、design.md §4「機能概要＝このページで何ができるようになるか」に合致する。 |
| current-0138 | 第3部 取引単体テスト（HTTPメッセージング） | 使用方法→機能概要 | `03_DealUnitTest/http_send_sync.rst:6-15`。モックアップクラス使用の方針と参照先`dealUnitTest_send_sync`との差分（送信キュー/受信キューを通信先と読み替え）の説明のみ。後続の具体的な手順（`current-0139`「モックアップクラスを使用した取引単体テストの実施方法」）とは別のページ冒頭説明。 |
| current-0064 | 第3部 リクエスト単体テスト（HTTPメッセージング） | 使用方法→機能概要 | `05_UnitTestGuide/02_RequestUnitTest/http_real.rst:4-8`。「リクエスト単体テストの実施方法は`:ref:real_request_test`を参照すること。本項では同ページと記述方法が異なる箇所を解説する」のみで、ページの位置づけを示す冒頭文。disposition=REFERENCEは維持。 |
| current-0069 | 第3部 リクエスト単体テスト（HTTPメッセージング） | 使用方法→機能概要 | `05_UnitTestGuide/02_RequestUnitTest/http_send_sync.rst:6-15`。current-0064と同型のページ冒頭スコープ説明（送信キュー/受信キューを通信先に読み替える旨の案内）。disposition=REFERENCEは維持。 |

### 変更しなかった行・ページ（実ファイル通読の結果、出典なしまたは設計上未確定と判断）

以下はすべて `mapping/tools/verify_mapping.py` の `PENDING_ZERO` に理由付きで登録し、
`#6`のユーザー判断待ちとした（ERRORからWARNへ）。

| # | dest_page（dest_section） | 実ファイル確認結果 | 出典 file:line |
|---|---|---|---|
| 1 | 第2部 クラス単体テストの設定（機能概要・拡張例） | 3行（current-0010/0021/0191）はいずれも「設定項目一覧」「コンポーネント設定ファイルの記述例」という個別設定の内容で、design.md §3の機能概要（全体像図/主なクラスとリソース/前提事項）にも拡張例（拡張手順）にも該当しない。 | `01_entityUnitTestWithBeanValidation.rst:704-770`、`02_entityUnitTestWithNablarchValidation.rst:688-763`、`02_DbAccessTest.rst:446-495` |
| 2 | 第2部 共通設定（機能概要・拡張例） | 5行（current-0225/0226/0227/0228/0246）はすべて`03_Tips.rst`の「目的別API使用方法」由来の個別設定断片（日時固定・採番・読み込みディレクトリ変更）で、ページ全体の概要や拡張手順に相当する記述がない。 | `06_TestFWGuide/03_Tips.rst:304-388, 734-784` |
| 3 | 第2部 リクエスト単体テストの設定（ウェブアプリケーション）（機能概要） | `02_RequestUnitTest.rst`の「概要／全体像／主なクラス，リソース／前提事項」（1-77行）は既にcurrent-0199〜0202として第3部リクエスト単体テスト（ウェブアプリケーション）の機能概要へ割当済み。本ページ（設定）専用の別の概要記述は存在せず、重複させると「重複がない」というAcceptance criteriaに反する。 | `06_TestFWGuide/02_RequestUnitTest.rst:1-92`（mapping.csv上のcurrent-0199〜0202の割当を確認） |
| 4 | 第2部 リクエスト単体テストの設定（RESTfulウェブサービス）（機能概要・拡張例） | 同様に「概要／全体像／主なクラス」（`RequestUnitTest_rest.rst:9-46`）はcurrent-0307〜0309として第3部側へ割当済み。current-0310/0311（モジュール一覧・設定＝Mavenのdependency追加とXMLインポート）はdesign.md使用方法「コンポーネントを設定する」の内容そのもので機能概要には該当しない（作業指示の候補ヒントは内容確認の結果不適合と判断）。拡張手順に該当する記述もない。 | `RequestUnitTest_rest.rst:49-93` |
| 5 | 第2部 リクエスト単体テストの設定（HTTPメッセージング）（機能概要・拡張例） | current-0074/0075はモックアップクラスの設定手順のみ（`http_send_sync.rst:143-164`）。概要・拡張手順に相当する記述なし。 | `05_UnitTestGuide/02_RequestUnitTest/http_send_sync.rst:135-165` |
| 6 | 第2部 リクエスト単体テストの設定（Nablarchバッチアプリケーション）（機能概要・拡張例） | current-0291/0292は常駐バッチのハンドラ差し替え設定・ディレクティブのデフォルト値設定（`RequestUnitTest_batch.rst:186-262`）で、いずれも設定内容。概要・拡張手順に相当する記述なし。 | `06_TestFWGuide/RequestUnitTest_batch.rst:186-262` |
| 7 | 第2部 リクエスト単体テストの設定（MOMによるメッセージング）（機能概要） | 拡張例は既存7行（current-0247〜0251,0303,0328、TestDataConvertorの拡張）で充足済み。機能概要のみ0件で、残る使用方法行（current-0106-b、各種準備データ）に概要相当の記述はない。 | `06_TestFWGuide/03_Tips.rst:788-832`、`RequestUnitTest_real.rst:168-181`、`RequestUnitTest_send_sync.rst:127-140` |
| 8 | 第2部 取引単体テストの設定（HTTPメッセージング）（機能概要・拡張例） | current-0140（`http_send_sync.rst:50-69`、DealUnitTest）はモックアップクラスの設定手順のみ。概要・拡張手順に相当する記述なし。 | `05_UnitTestGuide/03_DealUnitTest/http_send_sync.rst:50-69` |
| 9 | 第2部 取引単体テストの設定（MOMによるメッセージング）（機能概要・拡張例） | current-0158（`send_sync.rst:280-383`、DealUnitTest）はモックアップクラス設定・Excel配置場所設定・テストデータ解析クラス設定・pom.xml追加という設定内容のみ。 | `05_UnitTestGuide/03_DealUnitTest/send_sync.rst:280-383` |
| 10 | 第2部 マスタデータ復旧機能（拡張例） | `04_MasterDataRestore.rst`は全215行が機能概要4行・使用方法6行のみで構成され、215行目でファイルが終わる（拡張・クラス差し替えに相当する記述が存在しない）。 | `06_TestFWGuide/04_MasterDataRestore.rst`（全215行、末尾まで確認） |
| 11 | 第3部 テストデータの書き方（機能概要） | 候補input-0098/0099/0114（各資料のL1直下導入文・全体像節）は内容的に機能概要の定義「このページで何ができるようになるか」に適合しうる。ただし`#5`時点で作成された既存note（input-0037側、batch-11由来）に「この特殊2ページには機能概要相当のアウトラインがdesign.mdに定義されていないため」との明記があり、3観点レビューを経て承認済み。design.md §4「テストデータの2ページ」節は役割表のみで機能概要/使用方法のページアウトラインへの言及がない。既承認の解釈を#5bで独自に覆さず、候補の存在とdesign.md記載の欠落を#6に提示する。 | `ntf-testdata-doc-examples-testshots.md:2-43`、`ntf-testdata-doc.md:2-6`／design.md §4 |
| 12 | 第3部 テストデータの記載例（機能概要） | 同上の理由。候補input-0036/0037/0058/0082/0093（各記述例ドキュメントのL1直下導入文）。なお同種の候補input-0076・0079（examples-overview.md）は個別の例（「1. NTFテストデータ」「4.3 セクションのグループ化」）のローカルな導入文でありページ全体の概要ではないため候補から除外した。 | `ntf-testdata-doc-examples-file.md:2-50`、`-messaging.md:2-6`、`-special.md:2-6`、`-table.md:2-6` |
| 13 | 第3部 取引単体テスト（Nablarchバッチアプリケーション）（機能概要） | current-0128（`batch.rst:4-25`、L1直下）の4-6行目はページ冒頭の概要的記述だが、8-24行目はテストクラスのパッケージ・命名規則・コード例という使用方法の内容が同一セクションに混在しており、機能概要相当の部分だけを分離するには新規SPLITが必要。`#4a`/`#5b`のいずれの権限でも新規SPLIT対象として認められていない（`#4a`は`lines>=100`が対象、本セクションは22行）ため、無理に分割・移動しない。 | `05_UnitTestGuide/03_DealUnitTest/batch.rst:4-25` |
| 14 | 第4部 テストデータ変換ツール（導入） | `testdata-converter-design.md`全362行を通読。候補input-0183/0184/0190（「解くべき課題」「基準は形式ではなくNTF仕様上の意味」「特殊記法の扱い」）は設計思想・背景の説明であり、design.md §5の導入定義「インストール手順、依存関係、設定」には該当しない（現在の機能概要への割当が正しい）。ファイル全体にインストール手順・依存関係・設定に相当する記述は存在しない（開発体制の章「5. 開発とバージョン展開」はdeveloper・DROP）。design.md §5はHTMLチェックツールのみ導入省略の明記があり、本ツールへの同様の記載はない。 | `input/testdata-converter-design.md`（全362行、見出し一覧で確認） |

STEP 4で扱う3件（第1部稼動環境、第2部テストデータの形式、第2部取引単体テストの設定2ページの
ページ単位0件）は次節を参照。

### ゲート確認

```
$ python3 mapping/tools/verify_mapping.py
Loaded 591 rows from mapping.csv

pending zero assignments: 25 (awaiting #6 decision)
...(25件の一覧。すべてEXPECTED_ZERO/PENDING_ZERO登録済みでexit 0)...
lines total (all rows): 12986
lines total (excluding DROP): 11973
...
OK: no errors
```

591行・`lines`合計12,986・DROP除く11,973は不変。`check_coverage`/`check_vocabulary`は
エラー0件。`check_unused_vocabulary`はERROR 0件・PENDING_ZERO 25件（内訳: ページ単位3件、
セクション単位22件）。

## STEP 3: `volume.md` の0行ページ・dest_section集計の補完

`vocabulary.md`の`dest_page`は確定9件＋暫定29件の計38件だが、旧版`volume.md`は行のある
31件しか掲載していなかった（機械カウント: `git show HEAD:...volume.md`の表の行数）。
機械抽出（`vocabulary.md`の`## dest_page`配下の全表 vs `mapping.csv`の
`disposition!=DROP`行の`lines`集計）で母集合との差を取った結果、0行のページは以下7件
だった。

```
$ python3 - <<'EOF'
（vocabulary.mdの全dest_pageとmapping.csvのlines集計の差分を抽出するスクリプト。
実行結果は mapping/volume.md の対応テーブルに転記済み）
EOF

total vocab pages: 38
zero-line pages: 7
('第2部 導入と設定', 'テストデータの形式')
('第2部 導入と設定', 'リクエスト単体テストの設定（テーブルをキューとして使ったメッセージング）')
('第2部 導入と設定', '取引単体テストの設定（ウェブアプリケーション）')
('第2部 導入と設定', '取引単体テストの設定（Nablarchバッチアプリケーション）')
('第2部 導入と設定', '取引単体テストの設定（テーブルをキューとして使ったメッセージング）')
('第3部 テストの実装方法', 'リクエスト単体テスト（テーブルをキューとして使ったメッセージング）')
('第3部 テストの実装方法', '取引単体テスト（テーブルをキューとして使ったメッセージング）')
```

内訳: `EXPECTED_ZERO`4件（処理方式「テーブルをキューとして使ったメッセージング」、
design.md §6「中身は導線のみ」）、`PENDING_ZERO`3件（テストデータの形式、取引単体テストの
設定×2）。31（非0）+7（0）=38で`vocabulary.md`の母集合と一致する。`volume.md`の
dest_page別集計表に全38件を掲載し、0行の7件に備考列で区分を明記した。

`disposition内訳`の記述誤り（「SPLIT 16（4セクション×3〜4分割）」）も修正した。実際は
`current-0037/0066/0106/0156`が各3分割・`current-0184/0185`が各2分割の計6セクション・
16行であることを`mapping.csv`から再集計して確認した。

```
$ python3 - <<'EOF'
（SPLIT行をsrc_section_id別に集計）
current-0037 3 ['current-0037-a', 'current-0037-b', 'current-0037-c']
current-0066 3 ['current-0066-a', 'current-0066-b', 'current-0066-c']
current-0106 3 ['current-0106-a', 'current-0106-b', 'current-0106-c']
current-0156 3 ['current-0156-a', 'current-0156-b', 'current-0156-c']
current-0184 2 ['current-0184-a', 'current-0184-b']
current-0185 2 ['current-0185-a', 'current-0185-b']
total SPLIT rows: 16
total sections split: 6
EOF
```

`dest_section`単位の集計表（`design.md`のページアウトラインが定めるテンプレート14種）も
新設した。`第1部 稼動環境`が0行であることが、この集計で初めて可視化された
（`dest_page`単位の集計では第1部が1ページしかないため見えなかった）。

### ゲート確認

```
$ python3 mapping/tools/verify_mapping.py
Loaded 591 rows from mapping.csv
...
lines total (all rows): 12986
lines total (excluding DROP): 11973
...
OK: no errors
```

`volume.md`のDROP除く合計は11,973のまま不変。`vocabulary.md`の全38ページが集計表に
現れることを上記スクリプトで機械確認した。

## STEP 4: 未解決の0件の調査報告（`design.md`は変更していない。`git diff design.md`で確認可能）

### 報告項目1: 第1部「稼動環境」0件

**実測1: 現状の割当**

```
$ python3 - <<'EOF'
（mapping_id current-0180/current-0267/current-0310の割当を抽出）
current-0180 .../01_Abstract.rst 698 739 第2部 導入と設定 JUnit 5用拡張機能 使用方法
current-0267 .../JUnit5_Extension.rst 37 47 第2部 導入と設定 JUnit 5用拡張機能 使用方法
current-0310 .../RequestUnitTest_rest.rst 49 74 第2部 導入と設定 リクエスト単体テストの設定（RESTfulウェブサービス） 使用方法
EOF
```

実ファイル確認: `current-0180`（`01_Abstract.rst:698-739`「依存関係の追加」節、JUnit
VintageのためのMaven依存追加）と`current-0267`（`JUnit5_Extension.rst:37-47`「モジュール
一覧」節、`nablarch-testing-junit5`の依存追加）はいずれも第2部JUnit 5用拡張機能ページの
使用方法に割当済みで、design.md §2「依存関係は本ページ（稼動環境）に集約する。処理方式
ごとのページには置かない」に反する状態にある。`current-0310`（RESTfulの`nablarch-testing-rest`
等モジュール一覧）は§2が明示する例外（「処理方式固有の依存があるものだけ、当該ページに
記載する」「現時点で該当するのはRESTfulウェブサービス」）に該当し、問題ない。

**実測2: 「Java・Jakarta EEの要件」相当の記述の有無**

```
$ git ls-tree -r --name-only c24190607fef5d76c607aa08b36d2ab2f813efe5 \
    ja/development_tools/testing_framework/guide/development_guide | grep '\.rst$' | \
  while read f; do
    git show "c24190607fef5d76c607aa08b36d2ab2f813efe5:$f" | \
      grep -nE "Jakarta ?EE|Java ?17|Java ?SE|Java ?11|Java ?8|JDK" && echo "  ^^ in $f"
  done
（current側47ファイル、出力なし = 0件）

$ grep -rnE "Jakarta ?EE|Java ?17|Java ?SE|Java ?11|Java ?8|JDK" input/*.md
input/testdata-converter-design.md:355:- **v5・v1.4〜v1.2（過去展開）**：YAML 対応はフォークで作成（対象バージョンに合わせ JDK と NTF バージョンを変える）。...
```

current側47ファイルは0件。input側の唯一のヒットはテストデータ変換ツールの過去バージョン
展開に関する開発体制の記述（disposition=DROP・developer扱いのセクション内）であり、NTF
利用者向けの「Java・Jakarta EEの要件」とは無関係。**「Java・Jakarta EEの要件」に相当する
記述は現行資料に実在しない。**

**提示する選択肢**（`checks/task-05b.md`記載のとおり、design.mdは変更しない）:

| 案 | 内容 | 影響 |
|---|---|---|
| A | `current-0180`/`current-0267`を第1部稼動環境へ移す | design.md §2の集約ルールどおり。`current-0180`（42行）+`current-0267`（11行）=53行を第2部JUnit 5用拡張機能ページ（現状475行、`volume.md`参照）から除くと422行に、第1部テスティングフレームワークとはページ（現状293行）に53行加わり346行になる |
| B | §2の集約ルールを撤回し、依存関係は各ページに置く | design.md改訂が必要。現状の割当（第2部JUnit 5用拡張機能に集約）をそのまま追認する形になる |
| C | 稼動環境セクション自体を第1部から外す | design.md §2の表を改訂。出典のない「Java・Jakarta EEの要件」も同時に解消できる |

「Java・Jakarta EEの要件」は出典が無いため、`design.md` §2の表からこの項目自体を削除するか、
「マッピングにない内容を追加しない」の例外として新規に文章を起こすかを別途#6でユーザー判断
する必要がある旨を明記する。

### 報告項目2: 第2部「テストデータの形式」0件

design.md §3はこのページを「Excel / YAML の比較、使い分け、YAML使用時の設定」と定義しているが、
実測は0行である。

**実測: YAMLに言及する行の宛先内訳**（現行47rst＋input10md全文を対象に、行単位で
`YAML`/`yaml`を含む行を機械抽出し、その行番号を`mapping.csv`の`[src_body_start,
src_body_end]`に紐づけて`dest_page`を集計）

```
$ python3 <上記スクリプト>
total lines containing YAML: 194
テストデータの記載例 70
テストデータの書き方 70
DROP 25
UNMAPPED 15    ← 見出し行・アンカー行など本文行範囲外に該当（body範囲はheading除く仕様のため）
テストデータ変換ツール 11
テスティングフレームワークとは 3   （第1部「テストデータ」セクションのYAML言及）
```

194行中、第2部「テストデータの形式」への割当は**0行**。大半（140行）は第3部の
テストデータの書き方／記載例ページへ、25行はDROP、11行は第4部テストデータ変換ツール、
3行は第1部テスティングフレームワークとはページへ割り当てられている。

```
$ grep -rn "nablarch-testing-yaml" input/*.md
input/testdata-converter-design.md:347:...（nablarch-testing-yaml／nablarch-testing-converter）へ分割
input/ntf-testdata-doc.md:70:YAML テストデータには JSON Schema が定義されており、`nablarch-testing-yaml` の jar に...
```

`nablarch-testing-yaml`（モジュール名としての言及）は input 全体で2箇所のみ。うち
`ntf-testdata-doc.md:70`は第3部テストデータの書き方へMERGE済み（`input-0117`）、
`testdata-converter-design.md:347`は開発体制に関するDROP行内（developer向け）。

**選択肢**（design.mdは変更しない。判断材料のみ提示）:

- ページを新設せず、design.mdからこのページ自体を削除し、Excel/YAMLの使い分け説明は
  第3部テストデータの書き方ページの冒頭に統合する
- ページを維持し、第3部から一部内容を戻す形で0行を解消する（ただし「重複がない」という
  Acceptance criteriaとの整合が必要）
- `#6`のページ構成確定（未確定事項#1）と合わせて判断する

いずれもユーザー判断が必要なため、`design.md`は変更せず`PENDING_ZERO`に登録するにとどめた。

### 報告項目3: 第2部 取引単体テストの設定 2ページの0件

`取引単体テストの設定（ウェブアプリケーション）`・`取引単体テストの設定（Nablarchバッチ
アプリケーション）`はvocabulary.mdの暫定語彙に存在するが、`mapping.csv`に割当行が0件
（`volume.md`のdest_page別集計表で確認済み）。`design.md` §12未確定事項#2「取引単体テストの
ページ構成」の確定待ちであり、`current-0158`（取引単体テストの設定（MOMによるメッセージング）
への暫定割当。`steering.md` #5参照）と同種の問題である。`#6`で取引単体テストのページ構成が
確定した時点で、他の処理方式（HTTPメッセージング・MOM）に相当する内容が実在するかどうかを
含めて再判定が必要。

### STEP 4 成果物

上記3項目は`verify_mapping.py`の`PENDING_ZERO`に理由付きで登録済み（STEP 2で登録した
リストに含まれる。詳細は本ファイルの「STEP 1」節の`PENDING_ZERO`実行結果を参照）。理由
文字列にはそれぞれ`#6`未確定事項#1・#2、または新規論点である旨を明記した。
