# #5 Completion Check

## バッチ分割案（ディスパッチ前 user review 待ち — 2026-07-27 提示）

`/rn:up` 再開直後、ディスパッチ前に以下4点をユーザーから追加指示された（着手前の user review を要求）。以下はその回答としてまとめた案。**まだユーザー承認を得ていない。次回はこの案の承認可否から再開する。**

### 1. `mapping/_batch/` の扱い

残す。`.gitignore` に入れず、各バッチの出力CSVをそのままコミットする。理由: どのバッチがどのセクションを担当したか追跡でき、指摘が出たときに再実行の単位が明確になる（ユーザー指示どおり採用）。

### 2. バッチ分割案（30バッチ、579セクション全件）

`mapping/sections-current.csv`（377件・47ファイル）と `mapping/sections-input.csv`（202件・10ファイル）をファイル単位でビンパッキング（cap=20の first-fit-decreasing）し、1バッチ10〜20セクションに収めた。22セクション超の4ファイル（`03_Tips.rst` 38件、`ntf-testdata-doc.md` 53件、`ntf-doc-terms.md` 35件、`ntf-testdata-doc-examples-file.md` 22件）のみ、セクションID境界（`section_id` が連番であることを確認済み）で分割。分割してもファイル本文は各サブバッチに全文渡す。

分布: 最小9・最大21・平均19.3。21が2件（`RequestUnitTest/index.rst` 21件、`testdata-converter-design.md` 21件 — 単一ファイルで20をわずかに超えるが分割の必要性なしと判断し許容）、9が1件（batch-30、ビンパッキングの端数）。それ以外は10〜20の範囲内で、極端な偏りはない。

再現手順: `python3` でCSVを読み込み、ファイル単位のsection_idリストを構築 → 4ファイルのみ均等分割 → 残り58ユニットをfirst-fit-decreasing（cap 20）でビン詰め。同一ロジックを再実行すれば同じ30バッチが得られる。

| batch | 計 | 担当ファイル（セクション数） |
|---|---|---|
| 01 | 21 | 05_UnitTestGuide/02_RequestUnitTest/index.rst (21) |
| 02 | 21 | testdata-converter-design.md (21) |
| 03 | 20 | 06_TestFWGuide/01_Abstract.rst (20) |
| 04 | 20 | 06_TestFWGuide/03_Tips.rst#1 (19); 03_DealUnitTest/delayed_receive.rst (1) |
| 05 | 20 | 06_TestFWGuide/03_Tips.rst#2 (19); 03_DealUnitTest/delayed_send.rst (1) |
| 06 | 20 | ntf-doc-terms.md#1 (18); 01_ClassUnitTest/01_entityUnitTest/index.rst (2) |
| 07 | 20 | ntf-testdata-doc.md#1 (18); 05_UnitTestGuide/01_ClassUnitTest/index.rst (2) |
| 08 | 20 | ntf-testdata-doc.md#2 (18); 05_UnitTestGuide/index.rst (2) |
| 09 | 20 | **06_TestFWGuide/02_DbAccessTest.rst (17) ← split-yes: current-0184, current-0185**; 02_RequestUnitTest/mail.rst (3) |
| 10 | 20 | ntf-doc-terms.md#2 (17); 06_TestFWGuide/index.rst (2); 03_DealUnitTest/real.rst (1) |
| 11 | 20 | ntf-testdata-doc-examples-messaging.md (17); RequestUnitTest_http_send_sync.rst (1); 01_HttpDumpTool/index.rst (1); 02_MasterDataSetup/index.rst (1) |
| 12 | 19 | ntf-testdata-doc.md#3 (17); 08_TestTools/index.rst (1); testing_framework/index.rst (1) |
| 13 | 20 | 06_TestFWGuide/02_RequestUnitTest.rst (16); 02_RequestUnitTest/double_transmission.rst (4) |
| 14 | 20 | 06_TestFWGuide/JUnit5_Extension.rst (16); 02_RequestUnitTest/fileupload.rst (4) |
| 15 | 20 | ntf-testdata-doc-examples-testshots.md (16); **02_RequestUnitTest/http_real.rst (4) ← split-yes: current-0066** |
| 16 | 20 | **02_RequestUnitTest/batch.rst (15) ← split-yes: current-0037**; 01_ClassUnitTest/02_componentUnitTest.rst (5) |
| 17 | 20 | 06_TestFWGuide/RequestUnitTest_rest.rst (15); 02_RequestUnitTest/delayed_receive.rst (5) |
| 18 | 20 | ntf-testdata-loading.md (15); 02_RequestUnitTest/delayed_send.rst (5) |
| 19 | 20 | 06_TestFWGuide/RequestUnitTest_batch.rst (14); 03_DealUnitTest/index.rst (6) |
| 20 | 20 | **02_RequestUnitTest/real.rst (13) ← split-yes: current-0106**; 03_DealUnitTest/batch.rst (7) |
| 21 | 20 | 06_TestFWGuide/RequestUnitTest_real.rst (12); 02_RequestUnitTest/http_send_sync.rst (8) |
| 22 | 19 | 01_entityUnitTestWithNablarchValidation.rst (11); 01_HttpDumpTool/02_SetUpHttpDumpTool.rst (8) |
| 23 | 18 | 06_TestFWGuide/04_MasterDataRestore.rst (11); 02_MasterDataSetup/02_ConfigMasterDataSetupTool.rst (7) |
| 24 | 18 | ntf-testdata-doc-examples-file.md#1 (11); ntf-testdata-doc-examples-overview.md (7) |
| 25 | 17 | ntf-testdata-doc-examples-file.md#2 (11); **03_DealUnitTest/send_sync.rst (6) ← split-yes: current-0156** |
| 26 | 17 | ntf-testdata-doc-examples-special.md (11); 02_MasterDataSetup/01_MasterDataSetupTool.rst (6) |
| 27 | 20 | 01_entityUnitTestWithBeanValidation.rst (10); 02_RequestUnitTest/rest.rst (10) |
| 28 | 20 | 06_TestFWGuide/RequestUnitTest_send_sync.rst (10); 01_HttpDumpTool/01_HttpDumpTool.rst (10) |
| 29 | 20 | 03_HtmlCheckTool/index.rst (10); 02_RequestUnitTest/send_sync.rst (5); 03_DealUnitTest/rest.rst (5) |
| 30 | 9 | ntf-testdata-doc-examples-table.md (5); 03_DealUnitTest/http_send_sync.rst (4) |

全パスは `ja/development_tools/testing_framework/guide/development_guide/` 配下（current, `.rst`）または `.rn/20260724-ntf-yaml-support/input/`（input, `.md`）からの相対省略表記。`#1`/`#2`/`#3` は元ファイルを `section_id` の連番境界で均等分割したサブバッチ（元ファイルの内容は各サブバッチに全文渡す）。

### 3. `split-plan.md` の該当行の受け渡し

split=yes の6セクション（`current-0037`, `current-0066`, `current-0106`, `current-0156`, `current-0184`, `current-0185`）はいずれも分割されずに元ファイルのまま単一バッチに収まった。該当は batch-09・15・16・20・25（上表★印）。この5バッチのプロンプトには `split-plan.md` の該当行を必ず含める。他の25バッチには渡さない。

### 4. 統合後の検証（`verify_mapping.py`）

目視確認はしない。以下を機械検証する。
- `mapping/_batch/` 配下の全CSVを `csv.DictReader` で読み、レコード数の合計が `mapping.csv` のレコード数と一致すること
- `dest_part` / `dest_page` / `dest_section` が `mapping/vocabulary.md` の語彙（確定・暫定を合わせたもの）のいずれかと完全一致すること（不一致が1件でもあれば失敗）
- 既定の完了条件: 行範囲の集合演算（隙間・重複ゼロ）、`disposition` / `audience` 空欄0件、`lines` 合計12,986

## user review（2026-07-27 承認）

30バッチ案・上記4点の対応方針を承認。あわせて以下を指示された。

- 「表中★印の4バッチ」という記述誤りの指摘 — 本ファイル §2/§3 は元々「5バッチ」（09・15・16・20・25）と正しく記載しており、修正対象の誤記述はチャット上の口頭サマリのみだった（ファイルには存在しない）。念のためここに記録する。
- ディスパッチ前に `mapping/vocabulary.md`（closed vocabulary）を先にコミットし、design.mdとの一致を検証できる状態にすること → 対応済み（`mapping/tools/extract_vocabulary.py` で機械抽出、`mapping/vocabulary.md` に確定/暫定を区別して記載）。抽出中に第3部「取引単体テスト」の暫定語彙の扱いで判断が必要になり、ユーザーに確認した（次項）。
- batch-01の出力のみで一度停止し、user reviewに上げること → 対応する。残り29バッチは承認後に続行する。

### 追加判断: 第3部「取引単体テスト」の暫定dest_page

design.md未確定事項#2（構成はマッピング作成後に確定）配下のセクション（`03_DealUnitTest/`等、40件超見込み）について、暫定dest_pageの形式をユーザーに確認した。

処理方式付きの仮ページ名（`取引単体テスト（MOMによるメッセージング）`等、`split-plan.md` current-0156の既存precedentと同形式）を採用。理由: 由来をdest_pageの値自体に保持させないと、#6での再分離に全行の読み直しが必要になり非現実的なため。あわせてcurrent-0158の暫定値も「第2部 導入と設定 > 取引単体テストの設定（MOMによるメッセージング）」に修正（旧「リクエスト単体テストの設定」は由来を失うため撤回）。`steering.md` #5 Steps・#6 Completion criteriaに反映済み。詳細は `mapping/vocabulary.md` を参照。

## 次にやること（承認後）

1. ~~design.md から `dest_part` / `dest_page` / `dest_section` の closed vocabulary を機械抽出する~~ → 完了（`mapping/vocabulary.md`）
2. ~~上記30バッチのうち **batch-01のみ** を実装エージェントにディスパッチし、出力をuser reviewに上げる~~ → 完了（`mapping/_batch/batch-01.csv`、下記「batch-01 結果」参照）。**user review待ちでここまでで停止中。** 承認後に残り29バッチを継続する
3. `mapping/tools/verify_mapping.py` を作成し、上記4項目を機械検証する
4. 以降は steering.md #5 の残り Steps（disposition/audience付与、暫定dest_pageルール、volume.md作成、3観点レビュー等）に従う

## batch-01 結果（user review待ち、2026-07-27）

対象: `05_UnitTestGuide/02_RequestUnitTest/index.rst`（21セクション、split=yes対象なし）。

- 出力: `mapping/_batch/batch-01.csv`（21行、全セクション網羅を確認済み）
- disposition内訳: MOVE 20 / DROP 1（current-0076 = `.. _requestUnitTest:` という空のRSTアンカーのみで実体記述なし）
- audience: 全21行 `user`（本ファイルはNablarch開発者向け内部実装の説明を含まない）
- dest_page内訳: `ウェブアプリケーション` 13件 / `テストデータの書き方` 7件（すべて確定語彙。暫定語彙の使用なし）
- 機械検証: 全行の `dest_part`/`dest_page`/`dest_section` が `mapping/vocabulary.md` に存在すること、`lines` = `src_body_end - src_body_start + 1` の整合を確認済み
- current-0089（255行、#4a対象の大セクション）は `split-plan.md` の既承認判定（split=no、第3部 > ウェブアプリケーション > 使用方法）をそのまま採用し、再判断していない

**ユーザーに確認してほしい判断粒度の例**: current-0080〜0086（テストデータ記法：setUpDbシート、LIST_MAPのテストケース一覧、ユーザ情報/Cookie情報/クエリパラメータ情報/リクエストパラメータ/各種期待値の各列定義）を、ウェブアプリケーションページではなく共通の「テストデータの書き方」ページへMOVEする判断。#4a の current-0184/0185/0126 と同型の判断（記法はテストデータの書き方ページへ集約、手順・挙動説明は元ページに残す）。

**この方式で29バッチを続行してよいか、承認をお願いします。**
