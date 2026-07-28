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

## batch-01 差し戻し（2026-07-27）と対応

上記に対しユーザーから2点の指摘を受け、batch-01を差し戻された。残り29バッチは未着手のまま停止。

### 指摘①: `vocabulary.md` 第3部 dest_page（リクエスト単体テスト系）に処理方式のみの値を使っていた

第3部の確定dest_page「ウェブアプリケーション」等6件（処理方式名のみ）は、値単体からリクエスト単体テストに属することが判別できず、同じ`vocabulary.md`にある暫定値「取引単体テスト（ウェブアプリケーション）」と非対称だった。取引単体テストで処理方式付きの仮ページ名を採用した理由（由来を保持し#6で一括置換できる）はリクエスト単体テストにも同じく当てはまるとの指摘。

対応: `mapping/vocabulary.md` を修正。
- リクエスト単体テストの6処理方式ページを「確定（12件）」から外し「確定（6件）」に縮小
- 同6件を「暫定」区分に `リクエスト単体テスト（ウェブアプリケーション）` 等の形式で追加（design.md上はページ名確定済みだが、`dest_page`単体でテスト種別を判別できるようにする由来保持の暫定表記。`#6`でdesign.md記載の正式名称＝プレフィックスなしに一括置換する）
- `status`列の説明・出典の注記を上記に合わせて更新
- `mapping/_batch/batch-01.csv` の `dest_page = ウェブアプリケーション` 13行（current-0077/078/079/087〜096）を `リクエスト単体テスト（ウェブアプリケーション）` に一括置換。`テストデータの書き方` 7行（current-0080〜086）は変更なし

### 指摘②: current-0094 の dest_section が配下と分断していた

`リクエスト単体テストクラス作成時の注意点 > (L2直下)`（4行の導入文、current-0094）を「機能概要」に割り当てていたが、配下のcurrent-0095/0096は「使用方法」であり、親子でセクションが分かれ内容が分断されていた。同じ`(L2直下)`パターンのcurrent-0079・current-0092は配下と一致（使用方法）しており、current-0094のみ不一致だった。

対応: `mapping/_batch/batch-01.csv` の current-0094 の `dest_section` を「機能概要」→「使用方法」に修正（current-0095/0096と統一）。noteに記載の通りcurrent-0094は後続2小見出しへの橋渡しの導入文であり、使用方法配下に置くのが妥当。

### 確認事項（残り29バッチへの申し送り）

`(L2直下)`のセクション（親L2見出し直下・子L3を持たない導入文相当）は、配下セクションと同じ`dest_section`に置くのが原則。batch-01ではcurrent-0079・current-0092は既に配下と一致していたが、current-0094のみ不一致だった。**残り29バッチのディスパッチ・レビューでも、`heading_path`が`(L2直下)`で終わる行について、同じ親を持つ配下セクションの`dest_section`と一致しているかを確認すること。**

### 判断粒度についてのユーザー承認

current-0080〜0086（setUpDbシート・テストケース一覧・各種パラメータ列定義）を「テストデータの書き方」へMOVEした判断は妥当と承認。#4aで承認したcurrent-0184/0185/0126と同型で、記法は共通ページに集約し手順はページに残す方針に一致している。

**修正後、再度batch-01のみでuser reviewに上げる。承認後に残り29バッチへ進む。**

## バッチ実行ログ（batch-02〜、2026-07-27 `/rn:up` 再開後）

コーディネーターが各バッチのコミット差分を確認済み。詳細な判断根拠は各 `note` 列を参照。

- **batch-02**（`testdata-converter-design.md` 21件、commit `eb547fd`）: MOVE 5 / DROP 16（developer）。変換ツールの内部アーキテクチャ設計書のため大半developer判定。MOVEは目的・入出力の可逆性仕様・出力整形設定・呼び出し方法の4トピック。**要確認**: input-0198（OUT構造図）はYamlTestDataValidatorによる自動スキーマ検証という利用者向け事実を含むが、クラス図中心のためDROPとした（境界判断、batch-15チェックポイントで報告）。
- **batch-03**（`06_TestFWGuide/01_Abstract.rst` 20件、commit `70b9e48`）: MOVE 19 / DROP 1（RSTアンカーのみ）。全行user。current-0164/0174はsplit-plan.mdの既承認判定（no split）をそのまま採用。current-0167〜0174（Excel記法の(L2直下)+子7件）はルール2によりテストデータの書き方へMOVE。**要確認**: current-0166（JUnitアノテーションの基本的な書き方）は処理方式非依存の総論のため第1部/全体像に配置したが、対応する確定vocabulary項目がなく境界判断（batch-15チェックポイントで報告）。
- **batch-04**（`03_Tips.rst#1` 19件 + `delayed_receive.rst`(取引) 1件、commit `08217a6`）: MERGE 18 / DROP 1 / REFERENCE 1。全行user。Tips特別ルール（独立ページ化せず該当ページの使用方法へMERGE）を適用、内容の実体（サンプルコードの形）で宛先を判断（コンポーネント単体テスト7件／テストデータの書き方6件／共通設定5件）。current-0135はREFERENCE（実体は「real参照」の一文のみ）。**要確認**: current-0214（Tips.rstのファイル冒頭、1文+16件への:ref:リンク一覧のみのTOC）をDROPとした。Tips特別ルールは「独立ページにしない」という趣旨で個々の項目のMERGEを求めるものだが、TOC自体は実体的なコンテンツを持たないためルール3（アンカーのみDROP）の趣旨を拡張適用。実際に確認済み（`git show`でTOC内容を確認、単なる:ref:箇条書きのみ）。他バッチで同型のTOCが出た場合も同じ扱いとする。
- **batch-05**（`03_Tips.rst#2` 19件 + `delayed_send.rst`（取引）1件、commit `47fa35e`）: MERGE 19 / REFERENCE 1。全行user。DROPなし（ファイル中間部のためTOCなし）。dest_page内訳: コンポーネント単体テスト7／リクエスト単体テスト（ウェブアプリケーション）2／テストデータの書き方3／共通設定1／マスタデータ復旧機能1／リクエスト単体テストの設定（MOMによるメッセージング）5（拡張例）／current-0136はREFERENCE。**要確認**: current-0233/0234（任意ディレクトリのExcel読込）・current-0235/0236（JUnitの@Before/@After基本動作）は処理方式非依存でコンポーネント単体テストに配置したが弱い根拠（batch-15チェックポイントで報告）。自己チェックでlines列の転記ミス3件を自己修正済み。
- **batch-06**（`ntf-doc-terms.md#1` 18件 + `entityUnitTest/index.rst` 2件、commit `beb9bf6`）: MERGE 8 / DROP 12。**新パターン**: ntf-doc-termsはcurrent側RSTの用語リファレンス版であるため、内容がbatch-01/03/04/05で既にMOVE/MERGE済みのcurrent-XXXX行と重複するものはDROP（noteに重複元current-IDを明記）。重複がない部分（用語ドメイン全体図・グループIDのdefault挙動・DB系デフォルト値/カラム省略制約等、未処理ファイルとの重複可能性あり）はMERGE。current-0022/0023（entityUnitTest/index.rst）はアンカーのみ・TOCのみでDROP。**要確認**: input-0012・input-0016は末尾数行が別ページ（マスタデータ復旧機能／リクエスト単体テストの設定）に属する内容を含むが分割せず単一宛先とした（分割候補、batch-15チェックポイントで報告）。独立検証（python3で重複行なし・lines整合・DROP行のdest空欄を確認）済み。
- **batch-07**（`ntf-testdata-doc.md#1` 18件 + `ClassUnitTest/index.rst` 2件、commit `4b2a5ee`）: MERGE 16 / DROP 4。全行user。DROP4件はTOC・アンカーのみ（current-0029/0030、input-0115/0123）。**新パターン**: batch-06と異なり、ntf-testdata-doc.mdの多くのセクションはcurrent側と部分重複（Excel記法は既出だがYAML記法は新規）のため、丸ごとDROPではなくセクション全体をMERGEし、noteに重複元と新規部分を書き分けた（分割はしない）。dest_page: テストデータの書き方15／テスティングフレームワークとは1。**要確認**: input-0126（FK/DELETE-cascade注記）はマスタデータ復旧機能寄りの内容を含むが単一宛先（テストデータの書き方）のまま（batch-15チェックポイントで報告）。独立検証済み。
- **batch-08**（`ntf-testdata-doc.md#2` 18件 + `05_UnitTestGuide/index.rst` 2件、commit `d3dfdfa`）: MERGE 18 / DROP 2。全行user。current-0159/0160はアンカー・toctreeのみでDROP（current-0160はsplit-plan.mdの既承認判定どおり）。**要確認**: input-0146（SystemRepositoryのmessaging.assertAsMapFileTypeキー説明）は本来第2部の設定項目一覧寄りだが3行の小規模言及のため単一宛先（テストデータの書き方）のまま（分割候補、batch-15チェックポイントで報告）。独立検証済み。
- **batch-09**（`02_DbAccessTest.rst` 17件[split: current-0184/0185] + `mail.rst` 3件、commit `d8cd335`）: MOVE 16 / SPLIT 4（2セクション） / DROP 1 / REFERENCE 1。全行user。current-0184/0185はsplit-plan.mdの既承認範囲どおりに分割、独立検証で範囲の隙間・重複ゼロを確認。current-0189（省略記法の具体例）はテストデータの書き方へMOVE（split箇所と同型）。**要確認**: (1) mail.rst（メール送信）はdesign.mdに専用ページがなく、リクエスト単体テスト（ウェブアプリケーション）に暫定配置。(2) current-0191（デフォルト値の変更方法）はdesign.mdに02_DbAccessTest.rst専用ページがなく、内容から第2部クラス単体テストの設定に配置。いずれもglossary.md §11.1の既知ギャップに該当（batch-15チェックポイントで報告）。独立検証済み。
- **batch-10**（`ntf-doc-terms.md#2` 17件 + `06_TestFWGuide/index.rst` 2件 + `03_DealUnitTest/real.rst` 1件、commit `97533d2`）: MOVE 8 / MERGE 9 / DROP 3。全行user。**重要・後続バッチへの申し送り**: batch-06/07/08と逆方向の重複が発生 — input-0019〜0034の多くは`06_TestFWGuide/RequestUnitTest_batch.rst`・`RequestUnitTest_real.rst`・`RequestUnitTest_rest.rst`・`RequestUnitTest_send_sync.rst`・`RequestUnitTest_http_send_sync.rst`・`02_RequestUnitTest.rst`の要約だが、これらのcurrent側ファイルはbatch-01〜10未処理（batch-11以降で登場、具体的にはbatch-13=02_RequestUnitTest.rst、batch-17=RequestUnitTest_rest.rst、batch-19=RequestUnitTest_batch.rst、batch-21=RequestUnitTest_real.rst、batch-28=RequestUnitTest_send_sync.rst）。そのため今回は重複なしと判断しMOVE/MERGEしたが、**これらのバッチをディスパッチする際は本batch-10のinput-00xx行との重複を確認し、重複する側（通常はより詳細なcurrent側を残しinput側の簡略な記述を差し戻すか、逆に判断すること）をDROPすること**。current-0147（DealUnitTest/real.rst）は内容を持つためREFERENCEでなくMOVE（取引単体テスト（MOMによるメッセージング）/使用方法）。独立検証済み。
- **batch-11**（`ntf-testdata-doc-examples-messaging.md` 17件 + `RequestUnitTest_http_send_sync.rst` 1件 + `HttpDumpTool/index.rst` 1件 + `MasterDataSetup/index.rst` 1件、commit `2f5b254`）: MERGE 17 / DROP 2 / MOVE 1。全行user。**batch-10申し送り事項を解決**: current-0293（用語読み替え表）とbatch-10のinput-0027は内容完全一致を確認、input-0027（既MERGE確定）を残しcurrent-0293をDROP。ntf-testdata-doc-examples-messaging.mdは全件「テストデータの記載例」ページへMERGE（design.md §4の書き方/記載例の2ページ構成に対応、batch-08の記法説明との重複は想定内として許容）。current-0351（HttpDumpTool/index.rst）はtoctreeのみでDROP、current-0365（MasterDataSetup/index.rst）はtip/important含みMOVE。独立検証済み。
- **batch-12**（`ntf-testdata-doc.md#3` 17件 + `08_TestTools/index.rst` 1件 + `testing_framework/index.rst` 1件、commit `ef330ac`）: MERGE 16 / MOVE 1 / DROP 2。全行user。current-0376はtoctreeのみでDROP。current-0377（最上位index.rst）はJakarta Batch・マルチスレッド機能非対応の2件のimportant（他バッチ未出）を含み、第1部/対象範囲へMOVE（今回初めて対象範囲に内容が入った）。input-0155はbatch-06のinput-0013と重複でDROP。独立検証済み。
- **batch-13**（`02_RequestUnitTest.rst` 16件 + `double_transmission.rst` 4件、commit `9892ea9`）: MOVE 15 / MERGE 2 / DROP 3。全行user。**batch-10申し送り事項を解決**: batch-10のinput-0030との重複は全て部分重複と判明（current側がより詳細）、ルール5によりcurrent側を維持しMOVE/MERGE（丸ごとDROPなし）。current-0211（設定項目一覧19件）がinput-0030の5件抜粋の正本と確認。current-0198/0056はアンカーのみでDROP。current-0057（二重サブミット防止の橋渡し文、L1直下）は子2件（current-0058/0059）で異なる宛先ページに分かれるため単一宛先を持たずDROP（要確認）。独立検証済み。
- **batch-14**（`JUnit5_Extension.rst` 16件 + `fileupload.rst` 4件、commit `3ba158a`）: MOVE 17 / MERGE 1 / DROP 2。全行user。batch-03のcurrent-0178/0179/0180との重複を確認: current-0266（前提条件）はcurrent-0179と一部重複するがMERGE（新規情報あり）、current-0267（モジュール一覧）はcurrent-0180と別アーティファクトのため重複なし。current-0263/0264はアンカー・TOCのみでDROP。独立検証済み（vocabulary全値照合含む）。
- **batch-15**（`ntf-testdata-doc-examples-testshots.md` 16件 + `http_real.rst` 4件[split: current-0066 3分割]、commit `520526e`）: MERGE 15 / SPLIT 3（1セクション3分割） / DROP 3 / REFERENCE 1。audience: user21/developer1。current-0066はsplit-plan.mdの3分割（44-119/120-129[developer, 第2部]/130-159）どおりに分割、独立検証で範囲の隙間・重複ゼロを確認。DROP3件はbatch-10のinput-0019/0020と重複。current-0064はREFERENCE（batch-04のcurrent-0135型）。**バッチ02〜15ディスパッチはここで一区切り。次はuser reviewへ。**

## batch-02〜15 差し戻し対応（2026-07-28）

user reviewでbatch-02〜15が差し戻された。指摘2点＋完了条件追加1点に対応。

### 対応①: CSVの機械的破損を修正（指摘の前提として発見）

`csv.DictReader`で読むと、note/heading_pathフィールド内の無エスケープのカンマ・二重引用符によって8行（batch-03のcurrent-0174、batch-04のcurrent-0215/0217、batch-05のcurrent-0237、batch-06のinput-0006、batch-09のcurrent-0182、batch-12のinput-0152、batch-13のcurrent-0201）が誤ってフィールドずれを起こしていた（`csv.writer`で正しい引用符に再シリアライズして修正）。これは指摘②の「重複先を検証できない」問題を機械的に悪化させていた実例（input-0006の重複先current-0174はnote内に記載されていたが、CSV破損によりDictReaderでは読み取れなかった）。

### 対応②: 指摘① current-0057のDROPを再検討

current-0057（二重サブミット防止機能の橋渡し導入文、L1直下）は、「サーバサイド/クライアントサイド双方で機能するためテスト方法が異なる」という両ページの関係説明の唯一の記述であり、子節current-0058・current-0059のいずれにも再掲されていないことを実ファイル（`double_transmission.rst`）で確認した。DROPを撤回し、先に実施されるcurrent-0058側（リクエスト単体テスト（ウェブアプリケーション）/使用方法）へMERGE。current-0059側のnoteに「ページ作成時はこの説明への:ref:参照を使用方法冒頭に置き、再掲しない」という申し送りを追加（重複を作らない）。

あわせて、他の(L1直下)/(L2直下)のDROP行（8件: input-0182・input-0187・input-0195(batch-02), current-0214(batch-04), input-0001・input-0005・input-0017(batch-06), current-0264(batch-14)）を実ファイルで再点検した。いずれもcurrent-0057と異なり、(a) 変換ツール設計書自身の内部設計方針（developer向け、input-0182/0187/0195/0001）、(b) 生成TOC・アンカーラベルのみで地の文を持たない（current-0214/0264）、(c) 実体のない出典表記1行のみ（input-0005）、(d) 既存箇所への重複で新規情報が識別子的言及に留まる（input-0017、重複先は既にnoteに記載）のいずれかであり、「2ページに分岐する関係を説明する唯一の記述」には該当しないことを確認した。対応不要。

### 対応③: 指摘② 重複を理由とするDROPに重複先を明記

note内に「重複」（または同義の「再掲であり新規情報を含まない」等）を含むDROP行は batch-02〜15で16件。全件についてnoteに重複先の`current-XXXX`/`input-XXXX`を明記した（CSV破損修正で1件（input-0006→current-0174）が復元、他15件は元から記載済みだが2件は`重複`という語の誤用を是正）。

- **input-0193**（batch-02）・**input-0005**（batch-06）: noteに「重複」という語を含んでいたが、実際の理由は重複ではなかった（input-0193はコード実装の一元化に関する内部設計方針、input-0005は出典表記1行のみで実体がない）。誤解を避けるため文言を是正し、input-0005は子5節の`section_id`（input-0006〜0010）を明記した。

ユーザーが名指しした3件を実ファイル突合で個別検証:
- **input-0006**（特殊記法、13行）: current-0174（`01_Abstract.rst` 448-580、133行）と比較し、null/"null"/""/${systemTime}/${setUpTime}/${文字種,文字数}/${binaryFile:パス}/\r/\nの9規則すべてがcurrent-0174によりexample・注記付きでカバー済みであることを確認。重複DROPは妥当（重複先: current-0174）。
- **input-0105**（バッチ処理のオプションカラム、12行）: setUpDbはcurrent-0080、残り（setUpTable/expectedTable/setUpFile/expectedFile/expectedLog/args[n]）はinput-0019（batch-10、既MOVE済み）に全項目が含まれることをinput-0019の実note突合で確認。重複DROPは妥当（重複先: current-0080, input-0019）。
- **input-0123**（testShotsのカラム仕様、10行）: 実体は「カラムは処理方式によって異なる」の1文+4処理方式への:refリンク一覧のみで、独自の記法情報を持たないナビゲーションと判明。リンク先（ntf-testdata-doc-examples-testshots.md、batch-15）の実体的なカラム仕様（web: input-0100〜0103、バッチ: input-0104〜0106、メッセージング: input-0107〜0109、エンティティ: input-0110〜0113）はすべて個別にマッピング済みであることを確認し、noteを4処理方式分の重複先を明記する形に修正（旧noteはウェブアプリケーション分のcurrent-0081のみ言及で不完全だった）。「テストデータの書き方」への再配置は不要（実体がリンク一覧のみのため）。

### 対応④: 完了条件に追加 — verify_mapping.pyの新規作成

`mapping/tools/verify_mapping.py`を新規作成。`mapping.csv`が存在しない現段階では`mapping/_batch/batch-*.csv`全件を対象に以下を検証する（`mapping.csv`統合後は自動的にそちらを対象にする）。

- disposition=DROPかつnoteに「重複」を含む行は、noteに`current-XXXX`/`input-XXXX`形式の重複先が記載されていること（**今回の追加項目**）
- disposition/audienceが空欄の行が0件であること
- DROP行にnoteが必ず記載されていること
- `lines`合計（全行・DROP除く）の参考出力

実行結果: `python3 mapping/tools/verify_mapping.py` → 305行（batch-01〜15）を読み込み、エラー0件。

### batch-02〜15 DROP一覧（53件、対応後）

batch-01〜15全体のDROPは、current-0057のMERGE化により55件→54件に減った。うちbatch-01のDROP1件を除いたbatch-02〜15のDROPが、同じ変更で54件→53件になった（`python3`で`disposition == 'DROP'`をカウントして実測: 全体54件、batch-01のみ1件、差分のbatch-02〜15が53件）。


| src_section_id | lines | batch | 理由分類 | 重複先 | heading_path |
|---|---|---|---|---|---|
| input-0182 | 8 | batch-02 | 開発者向け内部情報 | input-0183 | NTF テストデータ変換ツール 設計書 > (L1直下) |
| input-0185 | 19 | batch-02 | 開発者向け内部情報 | input-0184 | NTF テストデータ変換ツール 設計書 > 1. 何を作るか（背景と決定） > 保持するか捨てるかの判断基準 |
| input-0186 | 7 | batch-02 | 開発者向け内部情報 | — | NTF テストデータ変換ツール 設計書 > 1. 何を作るか（背景と決定） > 制約 |
| input-0187 | 7 | batch-02 | 開発者向け内部情報 | — | NTF テストデータ変換ツール 設計書 > 2. どう作るか（設計判断） > (L2直下) |
| input-0188 | 22 | batch-02 | 開発者向け内部情報 | — | NTF テストデータ変換ツール 設計書 > 2. どう作るか（設計判断） > 判断 A：Excel 経路... |
| input-0189 | 11 | batch-02 | 開発者向け内部情報 | — | NTF テストデータ変換ツール 設計書 > 2. どう作るか（設計判断） > 判断 B：YAML 経路 ... |
| input-0191 | 12 | batch-02 | 開発者向け内部情報 | — | NTF テストデータ変換ツール 設計書 > 2. どう作るか（設計判断） > 共通：器の中身を読む手段 |
| input-0192 | 12 | batch-02 | 開発者向け内部情報 | — | NTF テストデータ変換ツール 設計書 > 2. どう作るか（設計判断） > 共通：器が正規化する値の原文復元 |
| input-0193 | 11 | batch-02 | 開発者向け内部情報 | — | NTF テストデータ変換ツール 設計書 > 2. どう作るか（設計判断） > 重複実装を避ける：ロジック... |
| input-0195 | 3 | batch-02 | 開発者向け内部情報 | — | NTF テストデータ変換ツール 設計書 > 3. 構造 > (L2直下) |
| input-0196 | 37 | batch-02 | 開発者向け内部情報 | — | NTF テストデータ変換ツール 設計書 > 3. 構造 > 中間モデル |
| input-0197 | 57 | batch-02 | 開発者向け内部情報 | — | NTF テストデータ変換ツール 設計書 > 3. 構造 > IN（形式 → 中間モデル） |
| input-0198 | 26 | batch-02 | 開発者向け内部情報 | input-0194 | NTF テストデータ変換ツール 設計書 > 3. 構造 > OUT（中間モデル → 形式） |
| input-0200 | 10 | batch-02 | 開発者向け内部情報 | — | NTF テストデータ変換ツール 設計書 > 4. 品質担保 |
| input-0201 | 9 | batch-02 | 開発者向け内部情報 | — | NTF テストデータ変換ツール 設計書 > 5. 開発とバージョン展開 > 開発とリポジトリ分割の手順 |
| input-0202 | 13 | batch-02 | 開発者向け内部情報 | — | NTF テストデータ変換ツール 設計書 > 5. 開発とバージョン展開 > 過去バージョンへの展開 |
| current-0161 | 2 | batch-03 | 空/TOC/アンカーのみ | — | (冒頭) |
| current-0214 | 23 | batch-04 | 空/TOC/アンカーのみ | — | 目的別API使用方法 > (L1直下) |
| input-0001 | 10 | batch-06 | 開発者向け内部情報 | — | NTF 解説書（v6）用語リファレンス > (L1直下) |
| input-0003 | 24 | batch-06 | 重複 | current-0169 | NTF 解説書（v6）用語リファレンス > データタイプ（Data Types） |
| input-0004 | 18 | batch-06 | 重複 | current-0080, current-0168, current-0169 | NTF 解説書（v6）用語リファレンス > シート・行・列・セル |
| input-0005 | 3 | batch-06 | 空/TOC/アンカーのみ | input-0006, input-0007, input-0008, input-0009, input-0010 | NTF 解説書（v6）用語リファレンス > セル値の解釈規則（特殊記法・マーカーカラム・コメント） > ... |
| input-0006 | 13 | batch-06 | 重複 | current-0174 | NTF 解説書（v6）用語リファレンス > セル値の解釈規則（特殊記法・マーカーカラム・コメント） > ... |
| input-0007 | 3 | batch-06 | 重複 | current-0171 | NTF 解説書（v6）用語リファレンス > セル値の解釈規則（特殊記法・マーカーカラム・コメント） > ... |
| input-0008 | 3 | batch-06 | 重複 | current-0170 | NTF 解説書（v6）用語リファレンス > セル値の解釈規則（特殊記法・マーカーカラム・コメント） > ... |
| input-0009 | 3 | batch-06 | 重複 | current-0173 | NTF 解説書（v6）用語リファレンス > セル値の解釈規則（特殊記法・マーカーカラム・コメント） > ... |
| input-0010 | 7 | batch-06 | 重複 | current-0175, current-0177 | NTF 解説書（v6）用語リファレンス > セル値の解釈規則（特殊記法・マーカーカラム・コメント） > ... |
| input-0017 | 10 | batch-06 | 重複 | current-0081, current-0085, input-0018 | NTF 解説書（v6）用語リファレンス > testShots / requestParams（テストケ... |
| input-0018 | 31 | batch-06 | 重複 | current-0081, current-0085 | NTF 解説書（v6）用語リファレンス > testShots / requestParams（テストケ... |
| current-0022 | 2 | batch-06 | 空/TOC/アンカーのみ | — | (冒頭) |
| current-0023 | 7 | batch-06 | 空/TOC/アンカーのみ | — | Form/Entityの単体テスト |
| current-0029 | 2 | batch-07 | 空/TOC/アンカーのみ | current-0022, current-0161 | (冒頭) |
| current-0030 | 8 | batch-07 | 空/TOC/アンカーのみ | current-0023 | クラス単体テストの実施方法 |
| input-0115 | 14 | batch-07 | 空/TOC/アンカーのみ | input-0116 | NTF テストデータ リファレンス > 目次 |
| input-0123 | 10 | batch-07 | 空/TOC/アンカーのみ | input-0100, input-0104, input-0107, input-0110 | NTF テストデータ リファレンス > 4. テストケース定義 > 4.2 testShots のカラム仕様 |
| current-0159 | 2 | batch-08 | 空/TOC/アンカーのみ | current-0022, current-0029 | (冒頭) |
| current-0160 | 101 | batch-08 | 空/TOC/アンカーのみ | — | 単体テスト実施方法 |
| current-0097 | 2 | batch-09 | 空/TOC/アンカーのみ | — | (冒頭) |
| input-0025 | 8 | batch-10 | 重複 | input-0141 | NTF 解説書（v6）用語リファレンス > メッセージング > 障害系テスト用特殊値 |
| input-0029 | 15 | batch-10 | 重複 | current-0182, current-0192, current-0193, current-0194 | NTF 解説書（v6）用語リファレンス > テスト種別と主要クラス > DB アクセステスト |
| current-0331 | 2 | batch-10 | 空/TOC/アンカーのみ | current-0022 | (冒頭) |
| current-0332 | 17 | batch-10 | 空/TOC/アンカーのみ | current-0023 | 自動テストフレームワークの使用方法 |
| current-0293 | 20 | batch-11 | 重複 | input-0027 | リクエスト単体テスト（HTTP同期応答メッセージ送信処理） |
| current-0351 | 7 | batch-11 | 空/TOC/アンカーのみ | current-0160 | リクエスト単体データ作成ツール |
| input-0155 | 3 | batch-12 | 重複 | input-0013 | NTF テストデータ リファレンス > 8. 値の書き方 > 8.8 バイナリデータの記述 |
| current-0376 | 8 | batch-12 | 空/TOC/アンカーのみ | current-0160, current-0351 | プログラミング工程で使用するツール |
| current-0198 | 2 | batch-13 | 空/TOC/アンカーのみ | — | (冒頭) |
| current-0056 | 2 | batch-13 | 空/TOC/アンカーのみ | — | (冒頭) |
| current-0263 | 2 | batch-14 | 空/TOC/アンカーのみ | — | (冒頭) |
| current-0264 | 5 | batch-14 | 空/TOC/アンカーのみ | — | JUnit 5用拡張機能 > (L1直下) |
| input-0104 | 9 | batch-15 | 重複 | input-0019 | NTF テストデータ解説書 — testShots カラム一覧 > バッチ処理（BatchRequest... |
| input-0105 | 12 | batch-15 | 重複 | current-0080, input-0019 | NTF テストデータ解説書 — testShots カラム一覧 > バッチ処理（BatchRequest... |
| input-0107 | 9 | batch-15 | 重複 | input-0020 | NTF テストデータ解説書 — testShots カラム一覧 > メッセージング（MessagingR... |

内訳: 開発者向け内部情報 17件（すべてbatch-02のtestdata-converter-design.md 16件 + batch-06のinput-0001） / 空・TOC・アンカーのみ 20件 / 重複（重複先を上表に明記） 16件。

**この対応内容をuser reviewに上げる。承認後にbatch-16〜30へ進む。**

指摘①②の対応（current-0057のMERGE化、重複DROP14件全件への重複先明記）はuser reviewで承認された（2026-07-28）。「54→53件」の根拠記載の誤り（全バッチ合計の54件とbatch-02〜15単体の54件が同じ数値で混同されていた）も指摘を受けて修正済み（正: 全体55→54、batch-02〜15単体54→53、`python3`での実測値: 全体54・batch-01のみ1・差分53）。以降、batch-16〜30は個別のuser reviewを経ず、全30バッチ統合後にまとめてuser reviewへ提示する（ユーザー指示、2026-07-28）。

## batch-16〜30 バッチ実行ログ

- **batch-16**（`02_RequestUnitTest/batch.rst` 15件[split: current-0037 3分割] + `01_ClassUnitTest/02_componentUnitTest.rst` 5件、commit `ff7d10a`）: MOVE 16 / SPLIT 3（1セクション3分割） / DROP 2 / REFERENCE 1。全行user。current-0037はsplit-plan.mdの3分割（170-262/263-316/317-446）どおりに採用、独立検証で範囲の隙間・重複ゼロを確認。current-0037-a/cとbatch-09のinput-0013/0014（固定長・可変長ファイル記法の抽象要約）が部分重複するが、current-0037側がディレクティブ表・制約・具体例付きでより詳細なため判断ルール5によりcurrent側を維持（重複先をnoteに明記）。current-0028（314行、テストデータとテストクラスの作成）はsplit-plan.mdの既承認判定（no split）どおり採用、DbAccessTestSupport等の用語がbatch-09と重なるが実践チュートリアルとして区別し採用。**要確認**: current-0043（データベースの結果検証）の本文に「ファイル出力結果を確認できる」という直後の節との文言混同とみられる記述があるが、原文どおり転記した（意味の修正はしていない）。verify_mapping.py: batch-01〜16全327行でエラー0件。
- **batch-17**（`RequestUnitTest_rest.rst` 15件 + `02_RequestUnitTest/delayed_receive.rst` 5件、commit `ba665a9`）: MOVE 17 / DROP 2 / REFERENCE 1。全行user。DROP2件（current-0306/0312）はアンカーのみ。current-0049はREFERENCE（batch-15のcurrent-0064型）。**batch-10申し送り事項を解決**: input-0031（RESTfulウェブサービスの主要クラス要約13行）とRequestUnitTest_rest.rstを実際に読み比べ、重複を確認（主なクラス表→current-0309、モジュール一覧→current-0310、SimpleRestTestSupport→current-0313、RestTestSupport→current-0314、事前準備補助機能→current-0316、結果確認→current-0318のいずれも現行側がメソッドシグネチャ・コード例付きでより詳細）。判断ルール5によりinput-0031をMOVEからDROPへ変更（`batch-10.csv`を修正、重複先をnoteに明記）。verify_mapping.py: batch-01〜17全347行でエラー0件。

**batch-24**（`ntf-testdata-doc-examples-file.md#1` 11件 + `ntf-testdata-doc-examples-overview.md` 7件、commit `5102bd8`）: MERGE 17 / DROP 1。全行user。DROP1件（input-0075）はL1直下がアンカーのみ。batch-11の記載例MERGE先例（design.md第3部「テストデータの記載例」）を踏襲。**要確認**: input-0078（YAML節）の本文末尾に、input資料自身が残した既知の不整合指摘（`description`カラムの文言がExcel例とYAML例で食い違う、という原資料の`[要確認]`コールアウト）が含まれる。MERGEはしたが、ページ作成時（#8〜）にどちらかの文言に統一する後工程対応が必要。

- **batch-19**（`RequestUnitTest_batch.rst` 14件 + `03_DealUnitTest/index.rst` 6件、commit `91cbe78`）: MOVE 16 / DROP 3 / REFERENCE 1。全行user。DROP3件のうちcurrent-0146は、実測でcurrent-0145と見出し・本文が完全一致（旧解説書のコピペミス）と判明したため重複DROP。**要確認**: current-0142（`03_DealUnitTest/index.rst`のL1直下、取引単体テストの共通総論）は、design.mdが処理方式ごとの取引単体テストページ構成をマッピング作成後の文量集計で確定するとしている（§10未確定事項#2）ため割当先が未確定。基準コミット時点のtoctreeで本ファイルが「ウェブアプリケーション」グループに属していたことを根拠に暫定的に「取引単体テスト（ウェブアプリケーション）」使用方法へ配置、noteを「暫定。」で開始。#6で処理方式共通ページとして独立させるか判断が必要。
- **batch-21**（`RequestUnitTest_real.rst` 12件 + `02_RequestUnitTest/http_send_sync.rst` 8件、commit `94379bd`+`fd544fb`）: MOVE 12 / MERGE 6 / DROP 1 / REFERENCE 1。全行user。**要確認**: プロンプト指示は`http_send_sync.rst`をMOMによるメッセージングとしていたが、実測で本文が「送信キュー/受信キューを通信先と読み替える」というHTTP固有の記述であることを確認し、batch-15のhttp_real.rst（HTTPメッセージング処理方式ページに割当済み）との整合を優先してHTTPメッセージングへ割当を変更（current-0069のnoteに理由を明記）。並行実行中にbatch-22.csvが誤ってbatch-21のコミットに混入する事故が発生したが、`fd544fb`で追跡解除しworking tree上のbatch-22.csvは無傷のまま維持された（batch-22は別途単独コミットdb63853で正常に記録）。
- **batch-22**（`entityUnitTestWithNablarchValidation.rst` 11件 + `SetUpHttpDumpTool.rst` 8件、commit `db63853`）: MOVE 17 / DROP 1 / REFERENCE 1。全行user。current-0020はBeanValidation版ファイルへの`:ref:`参照のみでREFERENCE。SetUpHttpDumpTool.rstはdesign.md第3部「リクエスト単体データ作成ツール」へ配置。current-0021（自動テストフレームワーク設定値、XML設定例）はdesign.mdの記載範囲表（コンポーネント設定ファイルの設定項目一覧は第2部）に従い第2部「クラス単体テストの設定」（暫定語彙）へMOVE。
- **batch-23**（`04_MasterDataRestore.rst` 11件 + `02_ConfigMasterDataSetupTool.rst` 7件、commit `3989db1`※後述）: MERGE 16 / DROP 2。全行user。dest_page整合: batch-11で`02_MasterDataSetup/index.rst`が`マスタデータ投入ツール`へMOVE済みであることを確認し、`02_ConfigMasterDataSetupTool.rst`（インストールガイド）も同じdest_pageを継続使用。※並行実行の副作用でbatch-23.csvが単独コミットされず、コーディネーターのbatch-24レビュー記録コミット（`3989db1`）に束ねられて記録された（batch-23担当エージェントがorigin上の内容が自分の作成物と完全一致することを確認済み。データの欠落・破損なし）。
- **batch-26**（`ntf-testdata-doc-examples-special.md` 11件 + `MasterDataSetupTool.rst` 6件、commit `d0a6bc7`）: MERGE 11 / MOVE 4 / REFERENCE 1 / DROP 1。全行user。DBアサート節（11.1/11.2）は原文が「記法仕様は別資料（テストデータの書き方）が担う、ここでは固有の挙動のみ」と明言しているため記法との重複はなく、具体例として「テストデータの記載例」へMERGE。**要確認**: input-0083本文中にinput資料自身の`[要確認]`記載（`${updateTime}`/`${setUpTime}`の値定義が本ファイルになく`${systemTime}`との違いが未確認）が残る。ページ作成時に別途確認要。current-0354（マルチスレッド非対応のimportant）はbatch-11のcurrent-0365と文言が重複する可能性があるが、箇条書き自体は固有情報のためMOVEとし、noteに重複統合要と記載。

- **batch-20**（`02_RequestUnitTest/real.rst` 13件[split: current-0106 3分割] + `03_DealUnitTest/batch.rst` 7件、commit `3176f19`※batch-28と同一コミットに束ねられた）: MOVE 17 / SPLIT 3（1セクション3分割） / DROP 1 / REFERENCE 1。全行user。current-0106はsplit-plan.mdの3分割（99-166/167-177/178-208）どおりに採用、独立検証で範囲の隙間・重複ゼロを確認。
- **batch-28**（`RequestUnitTest_send_sync.rst` 10件 + `01_HttpDumpTool.rst` 10件、commit `3176f19`）: MOVE 18 / REFERENCE 1 / DROP 1。全行user。担当ファイルの実パスがプロンプト指定と異なり（`08_TestTools/01_HttpDumpTool/`が正、`sections-current.csv`で実測確認）、そちらを採用。**要確認**: current-0328（TestDataConvertor）はbatch-13のcurrent-0204/0205前例に倣い、使用方法ではなく第2部「リクエスト単体テストの設定（MOMによるメッセージング）」拡張例へ割当（アーキテクトが実装する拡張点のため）。並行実行によりbatch-20.csvとbatch-28.csvが同一コミット（`3176f19`）に混入したが、両ファイルとも内容は無傷でverify_mapping.py（batch-01〜28、521行）でエラー0件を確認済み。

- **batch-25**（`ntf-testdata-doc-examples-file.md#2` 11件 + `03_DealUnitTest/send_sync.rst` 6件[split: current-0156 3分割]、commit `65f695d`）: MERGE 11 / MOVE 4 / SPLIT 3 / DROP 1。全行user。current-0156はsplit-plan.mdの3分割（67-172/173-198/199-220）どおりに採用、独立検証で範囲の隙間・重複ゼロを確認。**要確認**: input-0051（YAML記載例、quoting-delimiterディレクティブの根拠引用ブロック）をページ執筆時に転記するかは要判断。current-0154/0155/0156-b/0157/0158は取引単体テスト（MOMによるメッセージング）の暫定語彙を使用、noteは「暫定。」で開始。
- **batch-27**（`entityUnitTestWithBeanValidation.rst` 10件 + `05_UnitTestGuide/02_RequestUnitTest/rest.rst` 10件、commit `1bb0b55`）: MOVE 12 / DROP 8。全行user。プロンプト指示によりbatch-17（`RequestUnitTest_rest.rst`）との重複確認を実施（この1件に限り例外的に指示）: rest.rst（旧世代、05_UnitTestGuide配下）の7件がbatch-17既処理内容の簡略な要約・参照と判明しDROP（重複先をnoteに明記）。新規内容のcurrent-0114/0120/0122のみMOVE。
- **batch-29**（`03_HtmlCheckTool/index.rst` 10件 + `02_RequestUnitTest/send_sync.rst` 5件 + `03_DealUnitTest/rest.rst` 5件、commit `1973594`）: MERGE 18 / DROP 2。全行user。**要確認**: design.mdのページツリーに「HTMLチェックツール」の受け皿がなく（glossary.md §11.1が既知ギャップとして申し送り済み）、兄弟ツール（HttpDumpTool→第3部、MasterDataSetup→第2部）の前例に倣い第2部に暫定ページ「HTMLチェックツール」を新設（vocabulary.md未掲載の新規暫定語彙）。#6でdesign.md確定時に正式ページとして採用するか既存ページへ統合するか判断要。
- **batch-30**（`ntf-testdata-doc-examples-table.md` 5件 + `03_DealUnitTest/http_send_sync.rst` 4件、commit `ba17aa8`。**579セクション全件のマッピング作成が完了**）: MERGE 5 / DROP 2 / REFERENCE 1 / MOVE 1。全行user。current-0139（Excelファイルの書き方）は記法仕様が同型のsend_sync.rst側（current-0156）に既にあるため単一宛先のままMERGE。**要確認**: current-0139中の画像（`_images/http_send_sync_test_data.png`）はテキスト化不可のため、ページ化時にスクリーンショット素材の要否を別途判断する必要あり。

**batch-16〜30完了**: 全13バッチ、579セクション全件のマッピング作成が完了。`verify_mapping.py`（batch-01〜30、589行）でエラー0件を確認済み。

**並行実行に伴うgit運用上の注意（2026-07-28）**: batch-16〜30を`run_in_background`で並行ディスパッチした結果、同一ワーキングツリー・同一`.git/index`を複数エージェントが共有するため、`git add`/`git commit`のタイミングが競合し、他バッチのファイルが意図しないコミットに混入する事象が複数回発生した（batch-21↔batch-22、batch-23↔batch-24のレビュー記録コミット）。いずれも作業ツリー上のファイル内容は無傷で、後続のコミットで正しく追跡状態に収束していることをpython3での再読み込みおよび`git show`で確認済み。データの欠落・破損は発生していない。

**2026-07-28、ユーザー指示によりbatch-16〜30の実行方針を変更**: バッチ間の重複チェック（batch-06〜12で試みていた「先行バッチとの重複確認」）は並行実行では機能せず、順次実行でも防げていなかった（batch-17のinput-0031のように差し戻しで事後修正）。以後は各バッチのディスパッチ時に他バッチとの重複チェックを求めず、`verify_mapping.py`に追加した`check_duplicate_destinations`（heading_path末尾一致・本文先頭40文字一致で同一内容が複数dest_pageにMOVE/MERGEされていないかを検出、自動DROPはせず一覧出力のみ）で統合後に一括検出する方針に変更した。batch-16〜30は担当ファイルが重ならず出力先も別ファイルのため、以後は並行実行する。

- **batch-18**（`ntf-testdata-loading.md` 15件 + `02_RequestUnitTest/delayed_send.rst` 5件、commit `05bf6a4`）: DROP 11 / MOVE 4 / MERGE 5。audience: developer10/user10。design.md §8のuser/developer判定を個別に適用: 内部実装（4段階パイプライン・状態機械・キャッシュ機構等）10件をdeveloper・DROP、入出力仕様（特殊記法変換表・デフォルト補完表・マーカーカラム記法・Single/Group選択方式の注意）4件をuser・MOVE/MERGEに分類（機械的な一括DROPを避けた）。delayed_send.rst（current-0051〜0055）は全件user、リクエスト単体テスト（Nablarchバッチアプリケーション）へMOVE/MERGE。verify_mapping.py: batch-01〜18全367行でエラー0件（重複候補28組はadvisoryのみ）。

## 全30バッチ統合（mapping.csv作成、2026-07-28）

`mapping/_batch/batch-01.csv`〜`batch-30.csv`（589行）を`mapping_id`の重複なしを確認のうえ`mapping/mapping.csv`へ統合した。

### verify_mapping.pyへの機能追加

`mapping.csv`統合を受けて、steering.md #5の未実装項目だった2点を`verify_mapping.py`に追加した。

- `check_coverage`: `sections-current.csv`/`sections-input.csv`の全`section_id`が`mapping.csv`に最低1回現れ、紐づく全マッピング行の`[src_body_start, src_body_end]`の和集合が元セクションの`[body_start_line, body_end_line]`と過不足なく一致することを検証（SPLIT行は`mapping_id`が`-a`/`-b`/`-c`サフィックス付きでも`src_section_id`は元のIDのまま、という既存の書式を前提に集約）
- `check_vocabulary`: `vocabulary.md`の全マークダウン表から`dest_part`/`dest_page`/`dest_section`の許容値集合を機械抽出し、disposition=MOVE/MERGE/SPLITの行の値がすべて許容値に含まれることを検証

`mapping.csv`が存在する場合のみこの2検証を実行する（バッチ単体では対象セクションの一部しか含まれないため）。

### 統合直後に検出・修正した不具合

1. **batch-22の`src_body_start`列の混同（実測バグ）**: `check_coverage`が14件の`coverage mismatch (extra=...)`を検出。原因は`entityUnitTestWithNablarchValidation.rst`・`SetUpHttpDumpTool.rst`の一部セクションで、`sections-current.csv`の`src_line`列（見出し行番号）を`body_start_line`列（本文開始行番号）と取り違えていたため（両者が一致するセクションでは症状が出ず、見出し+アンダーラインの2行分ずれがあるセクションでのみ顕在化）。`sections-current.csv`を正として`batch-22.csv`の該当14行の`src_body_start`/`lines`を修正し、`mapping.csv`を再統合して解消を確認した。
2. **`HTMLチェックツール`のvocabulary未掲載**: batch-29が新設した暫定dest_page（design.mdに受け皿がないため）が`vocabulary.md`に未転記だった。`vocabulary.md`の第2部暫定8ページの表に追記し、由来と`#6`での判断要求を明記した。

### 修正後の検証結果

```
python3 mapping/tools/verify_mapping.py
Loaded 589 rows from mapping.csv
lines total (all rows): 12986
lines total (excluding DROP): 12000
OK: no errors
```

- lines合計12,986は`sections-current.csv`（9,783）+`sections-input.csv`（3,203）と一致（取りこぼしゼロ、steering.md #5 Completion criteria該当項目を満たす）
- disposition内訳: MOVE 239 / MERGE 227 / DROP 94 / SPLIT 16 / REFERENCE 13
- audience内訳: user 558 / developer 31
- 重複先候補（advisory）: 44組検出。いずれも複数処理方式ページでの同名見出し・類似定型文の並行構造であり、内容の誤重複ではないことを目視確認済み（詳細は次のセクション参照）

`mapping/volume.md`にdest_page別文量集計とDROP理由別集計を記載した（DROP除く合計12,000行、DROP合計986行）。

### 重複先候補（advisory 44組）の目視確認

`check_duplicate_destinations`が検出した44組全件を確認した。まず「dest_pageのベース名（末尾の（処理方式名）を除いた部分）が全メンバーで一致する」組を機械分類し、26組を「複数の処理方式ページが同名の見出し（全体像・主なクラス,リソース等）を独立に持つ」設計上想定内のパターンとして除外した。残り18組は個別にnoteと実内容を確認し、以下のいずれかに分類されることを確認した。内容の誤った重複配置は0件だった。

- 別ページ・別ツールの同名見出し（前提条件・前提事項・概要・特徴・モジュール一覧・注意事項）で、実体は別内容（JUnit5用拡張機能／リクエスト単体データ作成ツール／マスタデータ投入ツール／HTMLチェックツールなど、ツールごとに固有の前提条件・依存モジュール）
- 現行解説書の「目的別API使用方法」由来の「テストソースコード実装例」7件（batch-04/05でMERGE済み）はいずれも直前の技法セクションに対応する別々の具体的コード例
- 複数の処理方式ページに同一の定型文（「Excelファイルはテストソースコードと同じディレクトリ・同じ名前で格納する」「これらの設定は通常アーキテクトが行う」「以下の設定をすることでEclipseから起動できる」等）が独立に存在するが、いずれも原文が処理方式・ツールごとに同じ文言を繰り返す構成になっており、design.md第3部テンプレートの「テストデータを作成する（`テストデータの書き方`への:ref:）」のような各ページ固有の導線として意図された繰り返しである
- input側の「出典: ...」で始まる本文（ntf-doc-terms.mdの各セクションが機械的に付与する出典引用行）が本文先頭40文字一致で拾われた誤検出。実際の内容（groupIdのデフォルト挙動・主要クラス表など）はnoteで個別に新規性を確認済み

**唯一、内容面で軽い要observationとして残るのはcurrent-0204/current-0325（いずれも`AbstractHttpRequestTestTemplate`の説明）**: ウェブアプリケーション版は拡張ポイントとして第2部拡張例へ、MOMメッセージング版はスーパクラス選定の説明として第3部使用方法へ、と同じクラス名を異なる文脈で説明している。誤重複ではないが、ページ作成時（#8〜）に相互参照（`:ref:`）を検討する価値がある旨をここに記録する。

## 3観点レビュー（2026-07-28）

`mapping.csv`（589行、統合直後）に対し、割当先の妥当性・dispositionの妥当性・audienceの妥当性の3観点を、それぞれ別のサブエージェントで実施した。Rules「レビューを依頼するサブエージェント…」の3点（実測で裏付け・検証スクリプトを信頼せず独立に組む・敵対的にレビュー）を全プロンプトに含めた。

### 検査規模

- 割当先: 第2部使用方法/拡張例の全69行、拡張例18行全件、Part3の設定関連キーワード該当20行、要確認自己申告21行全件、処理方式サンプル25行（延べ約130行）
- disposition: DROP94件中「空/TOC/アンカーのみ」37件・「開発者向け内部情報」27件全件、「重複」10件、REFERENCE13件全件、SPLIT16件全件、MOVE/MERGEサンプル20件
- audience: `audience=developer`31行全件、`audience=user`かつMOVE/MERGEの25件、2ファイルの全audience境界

### 指摘と対応

コーディネーターが全指摘を実測で再検証し、以下のとおり対応した。

| # | 指摘 | 検証 | 対応 |
|---|---|---|---|
| 1 | audience: current-0066-b/current-0106-b/current-0140が`developer`のままだが、disposition=SPLIT/MOVEで解説書に残る内容（第2部の設定情報）。developer=Nablarch開発者向け内部情報の定義に該当しない | 実測（`git show`）で3件ともアーキテクト向け設定情報と確認。current-0140のnote自身が「current-0074/0075と同型」と認めながら、user判定のそれらと矛盾していた | audienceを`user`へ修正（3行） |
| 2 | disposition: current-0121が`DROP`だが、同一パターンの1文参照節（current-0035/current-0104）は`REFERENCE`として参照導線を残している | 実測（`git show`）で3件が同一の`:ref:`request_test_setup_db``参照文と確認 | `REFERENCE`へ変更、リクエスト単体テスト（RESTfulウェブサービス）使用方法へ |
| 3 | 割当先: input-0161（DIキー3種の一覧）が第3部テストデータの書き方へMERGEされているが、design.mdは「コンポーネント設定ファイルの設定項目一覧」を第2部に記載するとしている | 実測でcurrent-0292（`RequestUnitTest_batch.rst`225-262、同じ3キーをXML設定例付きでより詳細に説明、第2部MOVE済み）と完全重複と確認 | 判断ルール5によりDROP（重複先: current-0292） |
| 4 | 割当先: input-0016（214-233）の末尾がinput-0161と同型のDIキー列挙で第2部相当 | 実測で227-233行のみがcurrent-0292と重複と確認、214-226行（ディレクティブキー表）は記法仕様で第3部相当のまま | input-0016-a（214-226、MERGE維持）/input-0016-b（227-233、DROP・重複先current-0292）に分割 |
| 5 | 割当先: current-0229（Excelファイル記述例）が第2部共通設定にMERGEされているが、design.md§3記載範囲表は「テストデータの記述例」を第2部に記載しないとしている | 実測（`git show`）でSETUP_TABLE=TEST_SBN_TBL等の具体的Excel値を伴う記述例そのものと確認 | dest_partを第3部テストデータの記載例へ変更（採番機能の設定説明は第2部共通設定に残置） |
| 6 | disposition: input-0030（444-472）の末尾「コンポーネント設定の主要項目」表（5項目）がcurrent-0211（14項目、第2部MOVE済み）と重複 | 実測でhtmlDumpDir等5項目・デフォルト値が完全一致と確認 | input-0030-a（444-462、MERGE維持）/input-0030-b（463-472、DROP・重複先current-0211）に分割 |
| 7 | 割当先: current-0037-b（263-316のtip後半）にテストデータの記述例（数値表現対応表）が混在し第2部に配置されている | `split-plan.md`のcurrent-0037分割理由を確認したところ、「263-316行は`.. tip::`ディレクティブ1つ分であり、途中で割ると2つの新tipに再構成する暗黙の作業を要する無効な境界」と明記され、#4aの時点で既にこのより細かい分割案が検討・却下されていたことが判明 | **対応不要（既存の承認済み判断を再確認）**。入力側input-0156との軽微な内容重複はRSTディレクティブの構造上の制約として許容する、という既存方針を維持 |
| 8 | disposition: current-0214（Tips.rst冒頭TOC文）のDROPが自己申告の「要確認」のまま未解消 | レビュー自身が「実害は小さい」と評価 | 対応不要。既存のDROP判断を維持（`checks/task-05.md`の対応③参照） |
| 9 | audience: input-0178（TestDataParserのgetSetupFile/getExpectedTableData挙動）が`developer`だが、既存解説書に`TestDataParser`を直接使う例（`getListMap`、current-0233/0234相当）がある | 実測すると引用された実例は`getListMap`であり、input-0178が扱う`getSetupFile`/`getExpectedTableData`とは別メソッド。同一クラスの別メソッドが利用者向け公開APIかどうかは実装（Javaソース）を見ないと確定できず、証拠不十分 | **対応不要（証拠不十分のため見送り）**。#8以降のページ作成時、該当箇所執筆前に実装を確認のうえ再判断することを申し送る |
| 10 | audience: input-0198（YamlTestDataValidatorのスキーマ検証挙動）のDROP根拠「input-0194で既にカバー」が不正確 | 実測するとinput-0194はExcel/YAML整形方針のみでスキーマ検証には触れていないと確認 | 軽微のため一括修正の対象外とし、`mapping/vocabulary.md`の暫定語彙同様に申し送り事項として記録。変換ツール解説自体が入力資料側の参考情報でありDROPの実害は小さい |

指摘10件中6件を修正、4件は実測の結果「対応不要」と判断した（うち1件は既存の承認済み判断の再確認、1件は証拠不十分、2件は実害僅少）。

### 修正後の検証結果

```
python3 mapping/tools/verify_mapping.py
Loaded 591 rows from mapping.csv
lines total (all rows): 12986
lines total (excluding DROP): 11973
OK: no errors
```

- 行数は589→591（input-0016・input-0030をそれぞれ2行に分割したため+2）
- lines合計は12,986のまま変わらず（取りこぼしゼロを維持）
- `mapping/volume.md`を再集計して更新（DROP除く合計12,000→11,973、DROP合計986→1,013、REFERENCE 13→14、audience developer 31→28）

## ユーザー差し戻し対応（2026-07-28）

3観点レビュー結果の提示に対し、ユーザーから2件の差し戻し指示を受けた。

### 指示1: DROP見直し（20行以上13件・492行）

13件全件を実測で再検証した。結果、**12件はDROP維持が妥当**、**1件（current-0293）はユーザーの取消指示自体を実測で覆した**。

| mapping_id | 行数 | 判定根拠 |
|---|---|---|
| input-0018（testShots全19カラム） | 31 | 重複先current-0081（`05_UnitTestGuide/02_RequestUnitTest/index.rst` 99-193行）を実測、19カラム全件が説明文付きで存在すると確認。DROP維持 |
| current-0160（単体テスト実施方法の章題+toctree） | 101 | 実測すると本文は処理方式カテゴリの見出しラベルとtoctreeのみで説明文ゼロ。カテゴリ体系自体はdesign.md §4の第3部ツリー図が独自に確定済みで配下ページは個別マッピング済み。DROP維持 |
| input-0197/0168/0169/0196/0175/0198/0188/0174（開発者向け8件） | 各20〜57 | design.md §9冒頭の「開発者向け内部実装は含めない」原則に合致。うちinput-0168/0169/0175/0174はさらに§9本文が`ntf-testdata-loading.md`の「読み込みの4段階・状態機械」を名指しで対象外と明記。input-0196「グロッサリ5.9で別途定義済み」・input-0198「書き出し整形方針はinput-0194で既にカバー」の重複主張も実測で確認。DROP維持 |
| input-0003（データタイプ14種一覧表） | 24 | 重複先current-0169（`06_TestFWGuide/01_Abstract.rst` 258-325行）を実測、14種全件がより詳しい説明・脚注付きで存在すると確認。DROP維持 |
| current-0214（目的別API使用方法の扉部分） | 23 | 実測すると本文は1文の紹介文+16項目への:ref:リンク列挙のみ。配下16項目（current-0215〜0251）は全件個別にMERGE確定済みと確認。note自身の「要確認」を解消。DROP維持 |
| current-0293（HTTP同期応答メッセージ送信処理） | 20 | ユーザーは「他所にない情報」としてMOVE取消を指示したが、実測するとinput-0027（batch-10、`ntf-doc-terms.md`由来）が既に同一のクラス読み替え表（MockMessagingContext→MockMessagingClient・RequestTestingMessagingProvider→RequestTestingMessagingClient）を第3部「リクエスト単体テスト（HTTPメッセージング）」使用方法へMERGE確定済みと判明。表内容の完全一致を実ファイル突合で確認。MOVEすると重複が生じるためDROP維持を提案し、ユーザー承認を得た |

対応: マッピングデータの変更なし。

### 指示2: 第4部「ツール」新設対応

design.md改訂（第4部新設、章番号1〜12に振り直し）を受け、以下を実施した。

1. `vocabulary.md`に第4部の確定語彙を追加（dest_part 1件・dest_page 4件・dest_section 3件、うちHTMLチェックツールは「導入」を持たない例外を明記）。同時に、旧・第3部確定リストにあった「リクエスト単体データ作成ツール」が第4部へ移動したことと、旧・第2部暫定リストにあった「テストデータ変換ツール」「マスタデータ投入ツール」「HTMLチェックツール」が第4部確定へ格上げされたことを反映（第2部暫定ページは8件→5件）。
2. `mapping/tools/extract_vocabulary.py`がdesign.md改訂前の章構成（`第[123]部`固定・§5=処理方式の名称等）のままだったため、第4部抽出関数を追加し章番号のずれに追随させた。再実行してassert全通過を確認。
3. 対象行を機械抽出: `08_TestTools/`配下・`testdata-converter-design.md`を出典とする65行のうちDROP済み21件を除く**44行（628行分）**が対象と判明。バッチ内訳: batch-02（5行・テストデータ変換ツール）／batch-11（1行・マスタデータ投入ツール）／batch-22（8行・リクエスト単体データ作成ツール）／batch-23（7行・マスタデータ投入ツール）／batch-26（5行・マスタデータ投入ツール）／batch-28（9行・リクエスト単体データ作成ツール）／batch-29（9行・HTMLチェックツール）。着手前にユーザーへ提示し承認を得た。
4. `_batch/`の該当7バッチCSVの`dest_part`のみを第2部/第3部→第4部へ機械的に付け替え（`dest_page`は不変）、`mapping.csv`を全30バッチの単純連結で再生成（従来と同じ統合方式）。差分は意図した44行のみであることを`git diff`で確認。
5. `verify_mapping.py`を実行し、591行・エラー0件（coverage/vocabulary突合含む）を確認。
6. `design.md §`参照の章番号ずれ（旧§5処理方式の名称→新§6、旧§10未確定事項→新§12）を`split-plan.md`・`vocabulary.md`・`extract_vocabulary.py`で修正。`glossary.md`等の`§`表記は同ファイル内の独自章番号であり対象外と判断。
7. `volume.md`のdest_part表記を4ツール分について第4部へ同期し、HTMLチェックツールの受け皿ギャップ解消済みの旨に注記を更新。

対応後の再検証:

```
python3 mapping/tools/verify_mapping.py
Loaded 591 rows from mapping.csv
lines total (all rows): 12986
lines total (excluding DROP): 11973
OK: no errors
python3 mapping/tools/extract_vocabulary.py  # assert全通過
```

lines合計は12,986のまま変化なし（`dest_part`のみの変更のため取りこぼし・重複は生じない）。ユーザーより両指示とも承認済み。
