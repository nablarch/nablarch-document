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
- `dest_part` / `dest_page` / `dest_section` が design.md から機械抽出した closed vocabulary のいずれかと完全一致すること（不一致が1件でもあれば失敗）
- 既定の完了条件: 行範囲の集合演算（隙間・重複ゼロ）、`disposition` / `audience` 空欄0件、`lines` 合計12,986

## 次にやること（承認後）

1. design.md から `dest_part` / `dest_page` / `dest_section` の closed vocabulary を機械抽出する
2. 上記30バッチを実装エージェントにディスパッチする（split-plan.md該当行は5バッチのみに同梱）
3. `mapping/tools/verify_mapping.py` を作成し、上記4項目を機械検証する
4. 以降は steering.md #5 の残り Steps（disposition/audience付与、暫定dest_pageルール、volume.md作成、3観点レビュー等）に従う
