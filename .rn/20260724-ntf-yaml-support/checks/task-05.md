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
