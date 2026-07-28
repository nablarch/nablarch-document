# task-05c self-check

## STEP 0: 許可リストの陳腐化検出を追加する

`.rn/20260724-ntf-yaml-support/ntf-doc-05c-addendum.md` の指示に基づき、
`mapping/tools/verify_mapping.py` の `check_unused_vocabulary` に「0件として登録済みの
キーが非0になったこと」を検出する処理を追加した。既存のループはいずれも
「使用数 > 0 なら `continue`」で始まるため、`EXPECTED_ZERO_PAGES` /
`EXPECTED_ZERO_SECTIONS` / `PENDING_ZERO` に登録済みのキーが後から非0になっても
何も報告しない穴があった。`#5c` は `DROP` 判定を覆す可能性があり、覆した行の割当先が
現在0件のページ・セクションだった場合に許可リスト・`volume.md`・`checks/task-05b.md`
が誰にも気づかれないまま古くなるため、`#5c` のデータ変更に入る前に検出手段を追加した。

追加箇所: `check_unused_vocabulary` の末尾（`return errors, pending` の直前）。
`EXPECTED_ZERO_PAGES` と `PENDING_ZERO` の2-tuple（ページ単位）キー、
`EXPECTED_ZERO_SECTIONS` と `PENDING_ZERO` の3-tuple（セクション単位）キーそれぞれに
ついて `used_pages` / `used_page_sections` の実測値を突合し、非0であれば
`stale allowlist` の ERROR を追加する。ERROR（`exit 1`）とし、advisory にはしていない。

### 実行結果

```
$ python3 mapping/tools/verify_mapping.py; echo "EXIT: $?"
```

```
Loaded 591 rows from mapping.csv

pending zero assignments: 25 (awaiting #6 decision)
 - page [第2部 導入と設定 > テストデータの形式]: design.md §3はExcel/YAMLの比較・使い分け・YAML設定を役割とするが実測0行。既存の関連記述は第3部テストデータの書き方/記載例へMERGE済み。ページ新設か第3部への統合かは#6未確定事項#1（第2部のページ分割）確定時に判断する。
 - page [第2部 導入と設定 > 取引単体テストの設定（Nablarchバッチアプリケーション）]: 同上（#6未確定事項#2）。
 - page [第2部 導入と設定 > 取引単体テストの設定（ウェブアプリケーション）]: #6未確定事項#2（取引単体テストのページ構成）の確定待ち。current-0158と同様、取引単体テスト設定の受け皿ページ自体が暫定語彙であり、内容の有無以前にページ構成が未確定。
 - section [第1部 テスティングフレームワークとは > テスティングフレームワークとは > 稼動環境]: design.md §2「モジュール一覧の集約」は依存関係を本セクションに集約すると定めるが、該当候補(current-0180/current-0267)は既に第2部JUnit5用拡張機能ページに割当済みで移動の要否は#6未確定事項#1（第2部のページ分割）と連動する。『Java・Jakarta EEの要件』は出典なし（grep 0件）。#6でA/B/C案（checks/task-05b.md）から選択し確定する。
 - section [第2部 導入と設定 > クラス単体テストの設定 > 機能概要]: 出典なし（実ファイル通読済み、checks/task-05b.md）。#6未確定事項#1の確定と合わせて判断。
 - section [第2部 導入と設定 > クラス単体テストの設定 > 拡張例]: 出典なし（同上）。#6未確定事項#1の確定と合わせて判断。
 - section [第2部 導入と設定 > マスタデータ復旧機能 > 拡張例]: 出典なし。04_MasterDataRestore.rst全215行は機能概要4行・使用方法6行のみで構成され、拡張（クラス差し替え等）に相当する記述が存在しない（実ファイル全文確認、checks/task-05b.md）。#6未確定事項#1の確定と合わせて、拡張例を持たないページとして扱うか判断する。
 - section [第2部 導入と設定 > リクエスト単体テストの設定（HTTPメッセージング） > 機能概要]: 出典なし（設定内容のみ、checks/task-05b.md）。#6未確定事項#1の確定と合わせて判断。
 - section [第2部 導入と設定 > リクエスト単体テストの設定（HTTPメッセージング） > 拡張例]: 出典なし（同上）。#6未確定事項#1の確定と合わせて判断。
 - section [第2部 導入と設定 > リクエスト単体テストの設定（MOMによるメッセージング） > 機能概要]: 出典なし（拡張例は既存7行で充足済み、機能概要のみ出典なし）。#6未確定事項#1の確定と合わせて判断。
 - section [第2部 導入と設定 > リクエスト単体テストの設定（Nablarchバッチアプリケーション） > 機能概要]: 出典なし（同上）。#6未確定事項#1の確定と合わせて判断。
 - section [第2部 導入と設定 > リクエスト単体テストの設定（Nablarchバッチアプリケーション） > 拡張例]: 出典なし（同上）。#6未確定事項#1の確定と合わせて判断。
 - section [第2部 導入と設定 > リクエスト単体テストの設定（RESTfulウェブサービス） > 機能概要]: 出典なし。同様に概要相当(current-0307〜0309)は第3部側に割当済み。current-0310/0311はモジュール一覧・設定というdesign.md使用方法定義の内容で機能概要には該当しない。#6未確定事項#1の確定と合わせて判断。
 - section [第2部 導入と設定 > リクエスト単体テストの設定（RESTfulウェブサービス） > 拡張例]: 出典なし。#6未確定事項#1の確定と合わせて判断。
 - section [第2部 導入と設定 > リクエスト単体テストの設定（ウェブアプリケーション） > 機能概要]: 出典なし。概要/全体像/主なクラス相当の内容(current-0199〜0202)は第3部リクエスト単体テスト（ウェブアプリケーション）に割当済みで重複させられない。#6未確定事項#1の確定と合わせて判断。
 - section [第2部 導入と設定 > 共通設定 > 機能概要]: 出典なし（03_Tips.rst由来の個別設定断片のみ、checks/task-05b.md）。#6未確定事項#1の確定と合わせて判断。
 - section [第2部 導入と設定 > 共通設定 > 拡張例]: 出典なし（同上）。#6未確定事項#1の確定と合わせて判断。
 - section [第2部 導入と設定 > 取引単体テストの設定（HTTPメッセージング） > 機能概要]: 出典なし（設定内容のみ、checks/task-05b.md）。#6未確定事項#2の確定と合わせて判断。
 - section [第2部 導入と設定 > 取引単体テストの設定（HTTPメッセージング） > 拡張例]: 出典なし（同上）。#6未確定事項#2の確定と合わせて判断。
 - section [第2部 導入と設定 > 取引単体テストの設定（MOMによるメッセージング） > 機能概要]: 出典なし（同上）。#6未確定事項#2の確定と合わせて判断。
 - section [第2部 導入と設定 > 取引単体テストの設定（MOMによるメッセージング） > 拡張例]: 出典なし（同上）。#6未確定事項#2の確定と合わせて判断。
 - section [第3部 テストの実装方法 > テストデータの書き方 > 機能概要]: design.md §4「テストデータの2ページ」に機能概要の定義がない（#5時点で承認済みの解釈）。一方でinput-0098/0099/0114（各資料のL1直下導入文・全体像節）が機能概要の定義「このページで何ができるようになるか」に適合しうる。新規未確定事項として#6提示。詳細はchecks/task-05b.md参照。
 - section [第3部 テストの実装方法 > テストデータの記載例 > 機能概要]: 同上。候補: input-0036/0037/0058/0082/0093（各記述例ドキュメントのL1直下導入文）。新規未確定事項として#6提示。
 - section [第3部 テストの実装方法 > 取引単体テスト（Nablarchバッチアプリケーション） > 機能概要]: current-0128（batch.rst 4-25、(L1直下)）はページ冒頭2行のみ概要的記述で、残り大部分（8-24行）はテストクラス作成条件・命名規則・コード例という使用方法の内容が同一セクションに混在する。#4a/#5bの対象外である新規SPLITを本タスクの権限で追加しないため無理に分割・移動しない。#6で新規SPLIT対象として扱うか、機能概要なしのページとして扱うかを判断する。
 - section [第4部 ツール > テストデータ変換ツール > 導入]: design.md §5はHTMLチェックツールのみ導入セクション省略を明記しており、テストデータ変換ツールへの同様の言及はない。実ファイル通読（testdata-converter-design.md全362行）の結果、インストール手順・依存関係・設定に該当する記述は存在しない（該当候補input-0183/0184/0190は『解くべき課題』『形式に依存するか否か』という設計思想の説明で機能概要が正しい）。HTMLチェックツールと同様の例外をEXPECTED_ZERO_SECTIONSに追加するか、#6でdesign.md §5に明記するかを判断する。
lines total (all rows): 12986
lines total (excluding DROP): 11973

candidate duplicate destinations: 44 (advisory only, not auto-fixed)
...(check_duplicate_destinationsの既存出力。#5b/#5cで変更なし)...

OK: no errors
EXIT: 0
```

### 判定

- `stale allowlist` の ERROR は **0件**（許可リスト30件＝`EXPECTED_ZERO_PAGES` 4／
  `EXPECTED_ZERO_SECTIONS` 1／`PENDING_ZERO` 25 は全件、実測でも0件のまま）
- `EXIT: 0` を確認。`lines` 合計 12,986（DROP除く 11,973）・591行も不変
- 現時点で `#5c` 本体の DROP 判定を覆す変更はまだ行っていないため、この結果は
  「STEP 0 追加時点の許可リストと実データが食い違っていない」ことの確認である。
  `#5c` 本体で `DROP` を覆す行が出た場合は、この検査を再実行して確認する

### commit

この STEP のみで1コミットにする（`mapping/tools/verify_mapping.py` の変更と本ファイル）。
`DROP` レビューの変更とは混ぜない。

## `#5c` 本体: `DROP` 全96行レビュー

`mapping.csv` の `disposition=DROP` は96行（`python3` で `disposition == 'DROP'` を実測カウント）。
`design.md` §11.8「`DROP` は件数の多寡にかかわらず全件を対象とする」の未達分を解消するため、
96行全件を「レビュー済み（既存記録への参照）」または「今回レビュー（実ファイル通読による新規判定）」の
いずれかに分類し、全行を1つの表にまとめた。

### 分類方法（機械的、`#5c`差し戻し対応で修正）

**修正の経緯**: 初版の分類基準は「`mapping_id` または `src_section_id` が
`checks/task-05.md` に文字列として出現するか」のみで、記録の中身が「判定確定」か
「判定保留」かを区別しなかった。その結果、`input-0178`（`checks/task-05.md:352`、
結論は「対応不要（証拠不十分のため見送り）」で判定を確定していない）と
`input-0198`（`checks/task-05.md:135`、DROP根拠が`task-05.md:353`の指摘10で
不正確と実測済み）の2行が、保留を引用しただけで「レビュー済み・DROP維持」として
閉じられていた。`design.md` §11.8「`DROP`は内容が失われるかどうかを決める最後の砦」に
反するとして差し戻された。

修正後の基準は、機械マッチに加えて**その記録が当該行自身について判定を確定しているか**を
判定条件に加える。該当行を指す記録に、その行自身についての保留表現
（`証拠不十分`/`見送り`/`申し送り`/`再判断`/`保留`）が含まれる場合、「レビュー済み」に
分類しない。ただし保留表現が**別の行について**書かれている場合（同じbatchログ行に
複数`mapping_id`が並ぶケース）は該当しない。この切り分けは機械判定だけでなく記録の
文面を読んで行った。

```
$ python3 -c "... (mapping.csv の DROP行 96件について checks/task-05.md を mapping_id/src_section_id で grep) ..."
Total DROP rows: 96
Reviewed (mentioned in task-05.md): 63
Unreviewed: 33
```

**既知の限界（発見・対応済み）**: `current-0312` は `checks/task-05.md:256` に
「`DROP2件（current-0306/0312）はアンカーのみ`」という短縮表記で言及されているが、
`current-0312` という文字列そのものは出現しない（`current-0306/0312` の `/0312` 部分のみ）ため、
機械分類では「未レビュー」側に分類された。安全側に倒れる誤分類（見落としではなく過検出）であり、
結果的に今回レビューのグループAで独立に実ファイル検証済み（下表参照）。

**保留表現の機械フラグと文面確認（`#5c`差し戻し対応STEP R1）**: 上記機械分類で
「レビュー済み」63行のうち、マッチした行のテキストに保留キーワードを含むものを
再スキャンしたところ8行がヒットした。

```
$ python3 -c "...（reviewed 63行のマッチテキストに証拠不十分/見送り/申し送り/再判断/保留を含むかをスキャン）..."
=== Flagged (matched line contains hold keyword) ===
input-0198 / input-0198 @ line 353   … 「軽微のため一括修正の対象外とし…申し送り事項として記録」
input-0030-b / input-0030 @ line 146 … 「**batch-10申し送り事項を解決**」
input-0031 / input-0031 @ line 256   … 「**batch-10申し送り事項を解決**」
current-0293 / current-0293 @ line 144 … 「**batch-10申し送り事項を解決**」
current-0351 / current-0351 @ line 144 … 「**batch-10申し送り事項を解決**」
current-0198 / current-0198 @ line 146 … 「**batch-10申し送り事項を解決**」
current-0306 / current-0306 @ line 256 … （同一行内の別項目=input-0031に関する言及に付随してマッチ）
input-0178 / input-0178 @ line 352   … 「証拠不十分のため見送り」
```

このうち`input-0030-b`・`input-0031`・`current-0293`・`current-0351`・`current-0198`・
`current-0306`の6行は、`task-05.md:144/146/256`の当該行全文を読むと「batch-10の**申し送り
事項を解決**」という文脈で、その行自身については確定した結論（例:
「current-0293をDROP」「current-0198/0056はアンカーのみでDROP」「input-0031をMOVEから
DROPへ変更」）が明記されている誤検出（機械キーワードでは拾うが文面を読むと保留ではない）。
残る`input-0178`・`input-0198`の2行のみが、その行自身についての保留が確定せず閉じられた
真の保留行だった。

再分類の結果:

```
Total DROP rows: 96
Reviewed (mentioned in task-05.md, confirmed verdict): 61
Unreviewed (incl. STEP R1 hold override): 35
Hold override applied to (moved from reviewed to unreviewed): ['input-0178', 'input-0198']
```

新たに「未レビュー」に移った行は`input-0178`・`input-0198`の2行で、差し戻し指摘のとおり
一致した。既に「今回レビュー」で実測済みの33行は再実施していない。

### 今回レビューの実施

未レビュー33行を3グループに分け、それぞれ独立したサブエージェントに実ファイル通読による検証を
指示した（本タスクの Rules「レビューを依頼するサブエージェント…」の3点をすべて含めたプロンプトを使用）。

- **グループA**（18行）: 「空/TOC/アンカーのみ」が理由の行。`git show c241906:<file> | sed -n '<range>p'`
  で実際の本文範囲を読み、RSTアンカー・`.. contents::`・HTMLアンカーコメント・空行以外の地の文が
  ないことを確認させた。
- **グループB**（9行）: `input/ntf-testdata-loading.md` 由来で `audience=developer` の行。
  `design.md` §9「対象外とするもの」の定義（読み込みの4段階・状態機械・キャッシュという内部処理説明）
  に照らして、利用者向け仕様が混入していないかを確認させた。
- **グループC**（6行）: 旧ファイル `05_UnitTestGuide/.../rest.rst` 由来で「新ファイルの詳細な記述と
  重複するため」が理由の行。重複先として `note` に記載された行を実際に開かせ、重複の実在を確認させた
  （重複先の記述を信じず独立に開く、という本タスクのRulesに従った）。

3グループとも「実測した結果、DROP判定を覆す必要はない」という結論で、全33行についてDROP維持の
判定と具体的な実測根拠（引用文・比較結果）を得た。**33行中、判定が覆った行は0件。**

### 全96行の判定結果

| mapping_id | 出典ファイル | 行数 | heading_path | 分類 | 判定 | 根拠 |
|---|---|---|---|---|---|---|
| current-0076 | index.rst | 2 | (冒頭) | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:91`）: - disposition内訳: MOVE 20 / DROP 1（current-0076 = `.. _requestUnitTest:` という空のRSTアンカーのみで実体記述なし） |
| input-0182 | testdata-converter-design.md | 8 | NTF テストデータ変換ツール 設計書 > (L1直下) | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:162`）: あわせて、他の(L1直下)/(L2直下)のDROP行（8件: input-0182・input-0187・input-0195(batch-02), current-0214(batch-04), input-0001・input-0005・input-0017(batch-06… |
| input-0185 | testdata-converter-design.md | 19 | NTF テストデータ変換ツール 設計書 > 1. 何を作るか（背景と決定） > 保持するか捨てるかの判断基準 | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:194`）: \| input-0185 \| 19 \| batch-02 \| 開発者向け内部情報 \| input-0184 \| NTF テストデータ変換ツール 設計書 > 1. 何を作るか（背景と決定） > 保持するか捨てるかの判断基準 \| |
| input-0186 | testdata-converter-design.md | 7 | NTF テストデータ変換ツール 設計書 > 1. 何を作るか（背景と決定） > 制約 | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:195`）: \| input-0186 \| 7 \| batch-02 \| 開発者向け内部情報 \| — \| NTF テストデータ変換ツール 設計書 > 1. 何を作るか（背景と決定） > 制約 \| |
| input-0187 | testdata-converter-design.md | 7 | NTF テストデータ変換ツール 設計書 > 2. どう作るか（設計判断） > (L2直下) | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:162`）: あわせて、他の(L1直下)/(L2直下)のDROP行（8件: input-0182・input-0187・input-0195(batch-02), current-0214(batch-04), input-0001・input-0005・input-0017(batch-06… |
| input-0188 | testdata-converter-design.md | 22 | NTF テストデータ変換ツール 設計書 > 2. どう作るか（設計判断） > 判断 A：Excel 経路 — アダプタで… | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:197`）: \| input-0188 \| 22 \| batch-02 \| 開発者向け内部情報 \| — \| NTF テストデータ変換ツール 設計書 > 2. どう作るか（設計判断） > 判断 A：Excel 経路... \| |
| input-0189 | testdata-converter-design.md | 11 | NTF テストデータ変換ツール 設計書 > 2. どう作るか（設計判断） > 判断 B：YAML 経路 — 本体の構造解… | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:198`）: \| input-0189 \| 11 \| batch-02 \| 開発者向け内部情報 \| — \| NTF テストデータ変換ツール 設計書 > 2. どう作るか（設計判断） > 判断 B：YAML 経路 ... \| |
| input-0191 | testdata-converter-design.md | 12 | NTF テストデータ変換ツール 設計書 > 2. どう作るか（設計判断） > 共通：器の中身を読む手段 | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:199`）: \| input-0191 \| 12 \| batch-02 \| 開発者向け内部情報 \| — \| NTF テストデータ変換ツール 設計書 > 2. どう作るか（設計判断） > 共通：器の中身を読む手段 \| |
| input-0192 | testdata-converter-design.md | 12 | NTF テストデータ変換ツール 設計書 > 2. どう作るか（設計判断） > 共通：器が正規化する値の原文復元 | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:200`）: \| input-0192 \| 12 \| batch-02 \| 開発者向け内部情報 \| — \| NTF テストデータ変換ツール 設計書 > 2. どう作るか（設計判断） > 共通：器が正規化する値の原文復元 \| |
| input-0193 | testdata-converter-design.md | 11 | NTF テストデータ変換ツール 設計書 > 2. どう作るか（設計判断） > 重複実装を避ける：ロジックの共通化 | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:168`）: - **input-0193**（batch-02）・**input-0005**（batch-06）: noteに「重複」という語を含んでいたが、実際の理由は重複ではなかった（input-0193はコード実装の一元化に関する内部設計方針、input-0005は出典表記1行のみで… |
| input-0195 | testdata-converter-design.md | 3 | NTF テストデータ変換ツール 設計書 > 3. 構造 > (L2直下) | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:162`）: あわせて、他の(L1直下)/(L2直下)のDROP行（8件: input-0182・input-0187・input-0195(batch-02), current-0214(batch-04), input-0001・input-0005・input-0017(batch-06… |
| input-0196 | testdata-converter-design.md | 37 | NTF テストデータ変換ツール 設計書 > 3. 構造 > 中間モデル | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:203`）: \| input-0196 \| 37 \| batch-02 \| 開発者向け内部情報 \| — \| NTF テストデータ変換ツール 設計書 > 3. 構造 > 中間モデル \| |
| input-0197 | testdata-converter-design.md | 57 | NTF テストデータ変換ツール 設計書 > 3. 構造 > IN（形式 → 中間モデル） | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:204`）: \| input-0197 \| 57 \| batch-02 \| 開発者向け内部情報 \| — \| NTF テストデータ変換ツール 設計書 > 3. 構造 > IN（形式 → 中間モデル） \| |
| input-0198 | testdata-converter-design.md | 26 | NTF テストデータ変換ツール 設計書 > 3. 構造 > OUT（中間モデル → 形式） | 今回レビュー（差し戻し対応） | **判定変更**: 3分割（input-0198-a/-b/-c）。a(273-294,22行)=DROP維持／b(295,1行)=**DROP→MERGE**（第4部ツール>テストデータ変換ツール>機能概要）／c(296-298,3行)=DROP維持 | 元note「input-0194で既にカバー」は誤り。input-0194（155-171、実測: `git show`で全文確認）は書き出しの整形方針（YAML全値クォート・Excel整形設定表）のみでスキーマ検証には無言及。b(295行)の`YamlTestDataValidator`によるYAML OUT後の自動スキーマ検証（不正時は`ValidationError`リストを返す）は別トピックで、design.md§9ただし書き（利用者向け仕様は解説書へ移す）の対象。a/cはmermaidクラス図と実装クラス参照のみで内部構造説明のためDROP維持。詳細根拠は本ファイル末尾「`#5c`差し戻し対応」節参照 |
| input-0200 | testdata-converter-design.md | 10 | NTF テストデータ変換ツール 設計書 > 4. 品質担保 | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:206`）: \| input-0200 \| 10 \| batch-02 \| 開発者向け内部情報 \| — \| NTF テストデータ変換ツール 設計書 > 4. 品質担保 \| |
| input-0201 | testdata-converter-design.md | 9 | NTF テストデータ変換ツール 設計書 > 5. 開発とバージョン展開 > 開発とリポジトリ分割の手順 | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:207`）: \| input-0201 \| 9 \| batch-02 \| 開発者向け内部情報 \| — \| NTF テストデータ変換ツール 設計書 > 5. 開発とバージョン展開 > 開発とリポジトリ分割の手順 \| |
| input-0202 | testdata-converter-design.md | 13 | NTF テストデータ変換ツール 設計書 > 5. 開発とバージョン展開 > 過去バージョンへの展開 | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:208`）: \| input-0202 \| 13 \| batch-02 \| 開発者向け内部情報 \| — \| NTF テストデータ変換ツール 設計書 > 5. 開発とバージョン展開 > 過去バージョンへの展開 \| |
| current-0161 | 01_Abstract.rst | 2 | (冒頭) | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:209`）: \| current-0161 \| 2 \| batch-03 \| 空/TOC/アンカーのみ \| — \| (冒頭) \| |
| current-0214 | 03_Tips.rst | 23 | 目的別API使用方法 > (L1直下) | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:137`）: - **batch-04**（`03_Tips.rst#1` 19件 + `delayed_receive.rst`(取引) 1件、commit `08217a6`）: MERGE 18 / DROP 1 / REFERENCE 1。全行user。Tips特別ルール（独立ページ化… |
| input-0001 | ntf-doc-terms.md | 10 | NTF 解説書（v6）用語リファレンス > (L1直下) | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:162`）: あわせて、他の(L1直下)/(L2直下)のDROP行（8件: input-0182・input-0187・input-0195(batch-02), current-0214(batch-04), input-0001・input-0005・input-0017(batch-06… |
| input-0003 | ntf-doc-terms.md | 24 | NTF 解説書（v6）用語リファレンス > データタイプ（Data Types） | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:212`）: \| input-0003 \| 24 \| batch-06 \| 重複 \| current-0169 \| NTF 解説書（v6）用語リファレンス > データタイプ（Data Types） \| |
| input-0004 | ntf-doc-terms.md | 18 | NTF 解説書（v6）用語リファレンス > シート・行・列・セル | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:213`）: \| input-0004 \| 18 \| batch-06 \| 重複 \| current-0080, current-0168, current-0169 \| NTF 解説書（v6）用語リファレンス > シート・行・列・セル \| |
| input-0005 | ntf-doc-terms.md | 3 | NTF 解説書（v6）用語リファレンス > セル値の解釈規則（特殊記法・マーカーカラム・コメント） > (L2直下) | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:162`）: あわせて、他の(L1直下)/(L2直下)のDROP行（8件: input-0182・input-0187・input-0195(batch-02), current-0214(batch-04), input-0001・input-0005・input-0017(batch-06… |
| input-0006 | ntf-doc-terms.md | 13 | NTF 解説書（v6）用語リファレンス > セル値の解釈規則（特殊記法・マーカーカラム・コメント） > 特殊記法 | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:156`）: `csv.DictReader`で読むと、note/heading_pathフィールド内の無エスケープのカンマ・二重引用符によって8行（batch-03のcurrent-0174、batch-04のcurrent-0215/0217、batch-05のcurrent-0237、b… |
| input-0007 | ntf-doc-terms.md | 3 | NTF 解説書（v6）用語リファレンス > セル値の解釈規則（特殊記法・マーカーカラム・コメント） > マーカーカラム | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:214`）: \| input-0005 \| 3 \| batch-06 \| 空/TOC/アンカーのみ \| input-0006, input-0007, input-0008, input-0009, input-0010 \| NTF 解説書（v6）用語リファレンス > セル値の解釈規… |
| input-0008 | ntf-doc-terms.md | 3 | NTF 解説書（v6）用語リファレンス > セル値の解釈規則（特殊記法・マーカーカラム・コメント） > コメント | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:214`）: \| input-0005 \| 3 \| batch-06 \| 空/TOC/アンカーのみ \| input-0006, input-0007, input-0008, input-0009, input-0010 \| NTF 解説書（v6）用語リファレンス > セル値の解釈規… |
| input-0009 | ntf-doc-terms.md | 3 | NTF 解説書（v6）用語リファレンス > セル値の解釈規則（特殊記法・マーカーカラム・コメント） > 日付記述フォーマ… | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:214`）: \| input-0005 \| 3 \| batch-06 \| 空/TOC/アンカーのみ \| input-0006, input-0007, input-0008, input-0009, input-0010 \| NTF 解説書（v6）用語リファレンス > セル値の解釈規… |
| input-0010 | ntf-doc-terms.md | 7 | NTF 解説書（v6）用語リファレンス > セル値の解釈規則（特殊記法・マーカーカラム・コメント） > 設計原則（用語と… | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:214`）: \| input-0005 \| 3 \| batch-06 \| 空/TOC/アンカーのみ \| input-0006, input-0007, input-0008, input-0009, input-0010 \| NTF 解説書（v6）用語リファレンス > セル値の解釈規… |
| input-0016-b | ntf-doc-terms.md | 7 | NTF 解説書（v6）用語リファレンス > データタイプ別の行構造 > ディレクティブ | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:139`）: - **batch-06**（`ntf-doc-terms.md#1` 18件 + `entityUnitTest/index.rst` 2件、commit `beb9bf6`）: MERGE 8 / DROP 12。**新パターン**: ntf-doc-termsはcurren… |
| input-0017 | ntf-doc-terms.md | 10 | NTF 解説書（v6）用語リファレンス > testShots / requestParams（テストケース一覧） > … | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:162`）: あわせて、他の(L1直下)/(L2直下)のDROP行（8件: input-0182・input-0187・input-0195(batch-02), current-0214(batch-04), input-0001・input-0005・input-0017(batch-06… |
| input-0018 | ntf-doc-terms.md | 31 | NTF 解説書（v6）用語リファレンス > testShots / requestParams（テストケース一覧） > … | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:220`）: \| input-0017 \| 10 \| batch-06 \| 重複 \| current-0081, current-0085, input-0018 \| NTF 解説書（v6）用語リファレンス > testShots / requestParams（テストケ... \| |
| current-0022 | index.rst | 2 | (冒頭) | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:139`）: - **batch-06**（`ntf-doc-terms.md#1` 18件 + `entityUnitTest/index.rst` 2件、commit `beb9bf6`）: MERGE 8 / DROP 12。**新パターン**: ntf-doc-termsはcurren… |
| current-0023 | index.rst | 7 | Form/Entityの単体テスト | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:223`）: \| current-0023 \| 7 \| batch-06 \| 空/TOC/アンカーのみ \| — \| Form/Entityの単体テスト \| |
| current-0029 | index.rst | 2 | (冒頭) | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:140`）: - **batch-07**（`ntf-testdata-doc.md#1` 18件 + `ClassUnitTest/index.rst` 2件、commit `4b2a5ee`）: MERGE 16 / DROP 4。全行user。DROP4件はTOC・アンカーのみ（curr… |
| current-0030 | index.rst | 8 | クラス単体テストの実施方法 | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:225`）: \| current-0030 \| 8 \| batch-07 \| 空/TOC/アンカーのみ \| current-0023 \| クラス単体テストの実施方法 \| |
| input-0115 | ntf-testdata-doc.md | 14 | NTF テストデータ リファレンス > 目次 | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:140`）: - **batch-07**（`ntf-testdata-doc.md#1` 18件 + `ClassUnitTest/index.rst` 2件、commit `4b2a5ee`）: MERGE 16 / DROP 4。全行user。DROP4件はTOC・アンカーのみ（curr… |
| input-0123 | ntf-testdata-doc.md | 10 | NTF テストデータ リファレンス > 4. テストケース定義 > 4.2 testShots のカラム仕様 | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:173`）: - **input-0123**（testShotsのカラム仕様、10行）: 実体は「カラムは処理方式によって異なる」の1文+4処理方式への:refリンク一覧のみで、独自の記法情報を持たないナビゲーションと判明。リンク先（ntf-testdata-doc-examples-tes… |
| current-0159 | index.rst | 2 | (冒頭) | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:141`）: - **batch-08**（`ntf-testdata-doc.md#2` 18件 + `05_UnitTestGuide/index.rst` 2件、commit `d3dfdfa`）: MERGE 18 / DROP 2。全行user。current-0159/0160はア… |
| current-0160 | index.rst | 101 | 単体テスト実施方法 | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:141`）: - **batch-08**（`ntf-testdata-doc.md#2` 18件 + `05_UnitTestGuide/index.rst` 2件、commit `d3dfdfa`）: MERGE 18 / DROP 2。全行user。current-0159/0160はア… |
| current-0097 | mail.rst | 2 | (冒頭) | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:230`）: \| current-0097 \| 2 \| batch-09 \| 空/TOC/アンカーのみ \| — \| (冒頭) \| |
| input-0025 | ntf-doc-terms.md | 8 | NTF 解説書（v6）用語リファレンス > メッセージング > 障害系テスト用特殊値 | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:231`）: \| input-0025 \| 8 \| batch-10 \| 重複 \| input-0141 \| NTF 解説書（v6）用語リファレンス > メッセージング > 障害系テスト用特殊値 \| |
| input-0029 | ntf-doc-terms.md | 15 | NTF 解説書（v6）用語リファレンス > テスト種別と主要クラス > DB アクセステスト | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:232`）: \| input-0029 \| 15 \| batch-10 \| 重複 \| current-0182, current-0192, current-0193, current-0194 \| NTF 解説書（v6）用語リファレンス > テスト種別と主要クラス > DB アクセステスト … |
| input-0030-b | ntf-doc-terms.md | 10 | NTF 解説書（v6）用語リファレンス > テスト種別と主要クラス > リクエスト単体テスト（ウェブアプリケーション）の… | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:146`）: - **batch-13**（`02_RequestUnitTest.rst` 16件 + `double_transmission.rst` 4件、commit `9892ea9`）: MOVE 15 / MERGE 2 / DROP 3。全行user。**batch-10申し… |
| input-0031 | ntf-doc-terms.md | 13 | NTF 解説書（v6）用語リファレンス > テスト種別と主要クラス > リクエスト単体テスト（RESTful ウェブサー… | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:256`）: - **batch-17**（`RequestUnitTest_rest.rst` 15件 + `02_RequestUnitTest/delayed_receive.rst` 5件、commit `ba665a9`）: MOVE 17 / DROP 2 / REFERENCE … |
| current-0331 | index.rst | 2 | (冒頭) | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:233`）: \| current-0331 \| 2 \| batch-10 \| 空/TOC/アンカーのみ \| current-0022 \| (冒頭) \| |
| current-0332 | index.rst | 17 | 自動テストフレームワークの使用方法 | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:234`）: \| current-0332 \| 17 \| batch-10 \| 空/TOC/アンカーのみ \| current-0023 \| 自動テストフレームワークの使用方法 \| |
| current-0293 | RequestUnitTest_http_send_sync.rst | 20 | リクエスト単体テスト（HTTP同期応答メッセージ送信処理） | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:144`）: - **batch-11**（`ntf-testdata-doc-examples-messaging.md` 17件 + `RequestUnitTest_http_send_sync.rst` 1件 + `HttpDumpTool/index.rst` 1件 + `Maste… |
| current-0351 | index.rst | 7 | リクエスト単体データ作成ツール | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:144`）: - **batch-11**（`ntf-testdata-doc-examples-messaging.md` 17件 + `RequestUnitTest_http_send_sync.rst` 1件 + `HttpDumpTool/index.rst` 1件 + `Maste… |
| input-0155 | ntf-testdata-doc.md | 3 | NTF テストデータ リファレンス > 8. 値の書き方 > 8.8 バイナリデータの記述 | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:145`）: - **batch-12**（`ntf-testdata-doc.md#3` 17件 + `08_TestTools/index.rst` 1件 + `testing_framework/index.rst` 1件、commit `ef330ac`）: MERGE 16 / MO… |
| input-0161 | ntf-testdata-doc.md | 13 | NTF テストデータ リファレンス > 9. ディレクティブ > 9.4 デフォルトディレクティブの DI 設定 | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:346`）: \| 3 \| 割当先: input-0161（DIキー3種の一覧）が第3部テストデータの書き方へMERGEされているが、design.mdは「コンポーネント設定ファイルの設定項目一覧」を第2部に記載するとしている \| 実測でcurrent-0292（`Reque… |
| current-0376 | index.rst | 8 | プログラミング工程で使用するツール | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:145`）: - **batch-12**（`ntf-testdata-doc.md#3` 17件 + `08_TestTools/index.rst` 1件 + `testing_framework/index.rst` 1件、commit `ef330ac`）: MERGE 16 / MO… |
| current-0198 | 02_RequestUnitTest.rst | 2 | (冒頭) | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:146`）: - **batch-13**（`02_RequestUnitTest.rst` 16件 + `double_transmission.rst` 4件、commit `9892ea9`）: MOVE 15 / MERGE 2 / DROP 3。全行user。**batch-10申し… |
| current-0056 | double_transmission.rst | 2 | (冒頭) | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:240`）: \| current-0056 \| 2 \| batch-13 \| 空/TOC/アンカーのみ \| — \| (冒頭) \| |
| current-0263 | JUnit5_Extension.rst | 2 | (冒頭) | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:147`）: - **batch-14**（`JUnit5_Extension.rst` 16件 + `fileupload.rst` 4件、commit `3ba158a`）: MOVE 17 / MERGE 1 / DROP 2。全行user。batch-03のcurrent-0178/0… |
| current-0264 | JUnit5_Extension.rst | 5 | JUnit 5用拡張機能 > (L1直下) | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:162`）: あわせて、他の(L1直下)/(L2直下)のDROP行（8件: input-0182・input-0187・input-0195(batch-02), current-0214(batch-04), input-0001・input-0005・input-0017(batch-06… |
| input-0104 | ntf-testdata-doc-examples-testshots.md | 9 | NTF テストデータ解説書 — testShots カラム一覧 > バッチ処理（BatchRequestTestSupp… | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:173`）: - **input-0123**（testShotsのカラム仕様、10行）: 実体は「カラムは処理方式によって異なる」の1文+4処理方式への:refリンク一覧のみで、独自の記法情報を持たないナビゲーションと判明。リンク先（ntf-testdata-doc-examples-tes… |
| input-0105 | ntf-testdata-doc-examples-testshots.md | 12 | NTF テストデータ解説書 — testShots カラム一覧 > バッチ処理（BatchRequestTestSupp… | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:172`）: - **input-0105**（バッチ処理のオプションカラム、12行）: setUpDbはcurrent-0080、残り（setUpTable/expectedTable/setUpFile/expectedFile/expectedLog/args[n]）はinput-001… |
| input-0107 | ntf-testdata-doc-examples-testshots.md | 9 | NTF テストデータ解説書 — testShots カラム一覧 > メッセージング（MessagingRequestTe… | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:173`）: - **input-0123**（testShotsのカラム仕様、10行）: 実体は「カラムは処理方式によって異なる」の1文+4処理方式への:refリンク一覧のみで、独自の記法情報を持たないナビゲーションと判明。リンク先（ntf-testdata-doc-examples-tes… |
| current-0031 | batch.rst | 2 | (冒頭) | 今回レビュー・A（空/TOC/アンカー実測） | DROP維持 | RSTアンカー(.. _`batch_request_test`:)+空行のみ、プローズなし |
| current-0024 | 02_componentUnitTest.rst | 2 | (冒頭) | 今回レビュー・A（空/TOC/アンカー実測） | DROP維持 | RSTアンカー(.. _componentUnitTest:)+空行のみ、プローズなし |
| current-0306 | RequestUnitTest_rest.rst | 2 | (冒頭) | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:256`）: - **batch-17**（`RequestUnitTest_rest.rst` 15件 + `02_RequestUnitTest/delayed_receive.rst` 5件、commit `ba665a9`）: MOVE 17 / DROP 2 / REFERENCE … |
| current-0312 | RequestUnitTest_rest.rst | 3 | リクエスト単体テスト（RESTfulウェブサービス） > 構造 > (L2直下) | 今回レビュー・A（空/TOC/アンカー実測） | DROP維持 | 「構造」節直下、RSTアンカー(.. _rest_test_superclasses:)+空行のみ。実文はL100以降で範囲外 |
| input-0167 | ntf-testdata-loading.md | 9 | NTF テストデータ読み込み機構 > (L1直下) | 今回レビュー・B（ntf-testdata-loading.md 開発者向け実測） | DROP維持 | 本書の位置づけ宣言のみ（利用者向け文書との対比、対象範囲がNTF本体の読み込み経路に限定される旨）。具体的仕様なし |
| input-0168 | ntf-testdata-loading.md | 55 | NTF テストデータ読み込み機構 > 1. 読み込みの4段階 | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:383`）: \| input-0197/0168/0169/0196/0175/0198/0188/0174（開発者向け8件） \| 各20〜57 \| design.md §9冒頭の「開発者向け内部実装は含めない」原則に合致。うちinput-0168/0169/0175/0174はさらに§9本文… |
| input-0169 | ntf-testdata-loading.md | 49 | NTF テストデータ読み込み機構 > 2. データタイプと組み立て方の対応 | 今回レビュー・B（ntf-testdata-loading.md 開発者向け実測） | DROP維持 | パーサ継承ツリー図＋データタイプ別パーサクラス名対応表。内部クラス名の説明のみ |
| input-0170 | ntf-testdata-loading.md | 4 | NTF テストデータ読み込み機構 > 3. 値の変換と整形 > (L2直下) | 今回レビュー・B（ntf-testdata-loading.md 開発者向け実測） | DROP維持 | ③④への導入文のみ。具体的な変換ルールを含まない |
| input-0173 | ntf-testdata-loading.md | 10 | NTF テストデータ読み込み機構 > 3. 値の変換と整形 > ③は不可逆、④は非破壊 | 今回レビュー・B（ntf-testdata-loading.md 開発者向け実測） | DROP維持 | ③不可逆/④非破壊というキャッシュ実装依存の可逆性説明。ntf-testdata-doc.mdをgrepしたが対応概念なし＝利用者向け文書に相当箇所なし＝内部専用と確認 |
| input-0174 | ntf-testdata-loading.md | 20 | NTF テストデータ読み込み機構 > 4. 状態機械による組み立て（ファイル・メッセージ） > (L2直下) | 今回レビュー・B（ntf-testdata-loading.md 開発者向け実測） | DROP維持 | 状態機械の遷移図・条件。利用者向けの帰結（先頭セル空/値ありでのデータ行・新規レコードレイアウト判定）はntf-testdata-doc.md §6.4/§6.5に既出と確認、抽出漏れなし |
| input-0175 | ntf-testdata-loading.md | 27 | NTF テストデータ読み込み機構 > 4. 状態機械による組み立て（ファイル・メッセージ） > 組み立て先のデータモデル… | 今回レビュー・B（ntf-testdata-loading.md 開発者向け実測） | DROP維持 | DataFile/DataFileFragment等の内部クラス名と保持構造の説明のみ |
| input-0177 | ntf-testdata-loading.md | 11 | NTF テストデータ読み込み機構 > 5. ヘッダ行＋データ行による組み立て（テーブル・LIST_MAP） > 組み立て… | 今回レビュー・B（ntf-testdata-loading.md 開発者向け実測） | DROP維持 | TableData/List<Map>という内部クラス名と保持構造の説明のみ |
| input-0178 | ntf-testdata-loading.md | 9 | NTF テストデータ読み込み機構 > 6. 入口 API がまとめる単位 | 今回レビュー（差し戻し対応） | **判定変更**: DROP→MERGE、audience developer→user（第4部ではなく第3部テストの実装方法>テストデータの書き方>使用方法へMERGE） | 実装確認（`nablarch/nablarch-testing` commit `e21bf67`、`src/main/java/nablarch/test/core/reader/TestDataParser.java:21`）: インタフェース宣言に`@Published(tag="architect")`が付与され利用者向け公開APIと確認。`tag="architect"`は内部専用の意味ではない（`nablarch-core` commit `fcb40bb`、`nablarch/core/util/annotation/Published.java:33-39`のJavadoc:「アーキテクト向けに公開したい場合」に付与するタグ）。現行解説書`current-0233`/`current-0234`（`git show c241906:.../03_Tips.rst` 485-507で本文確認）は同インタフェースの兄弟メソッド`getListMap`を`SystemRepository`経由で直接呼び出す具体的コード例をアプリ開発者向けに既に説明しており、`tag="architect"`が本解説書でのuser判定を妨げない先例が存在。SETUP_FIXED/SETUP_VARIABLE・EXPECTED_TABLE/EXPECTED_COMPLETE_TABLEの結合仕様は「どう書けばどう解釈されるか」という記法仕様のためテストデータの書き方の使用方法へMERGE |
| input-0180 | ntf-testdata-loading.md | 6 | NTF テストデータ読み込み機構 > 8. 再解析を避けるキャッシュ | 今回レビュー・B（ntf-testdata-loading.md 開発者向け実測） | DROP維持 | ファイル名/シート名キーのキャッシュ機構というdesign.md名指しの除外対象そのもの |
| input-0181 | ntf-testdata-loading.md | 6 | NTF テストデータ読み込み機構 > さいごに | 今回レビュー・B（ntf-testdata-loading.md 開発者向け実測） | DROP維持 | ①〜④の要約とスコープ限定文のみ。新規仕様情報なし |
| current-0279 | RequestUnitTest_batch.rst | 2 | (冒頭) | 今回レビュー・A（空/TOC/アンカー実測） | DROP維持 | RSTアンカー(.. _request-util-test-batch:)+空行のみ、プローズなし |
| current-0141 | index.rst | 2 | (冒頭) | 今回レビュー・A（空/TOC/アンカー実測） | DROP維持 | RSTアンカー(.. _dealUnitTest:)+空行のみ、プローズなし |
| current-0146 | index.rst | 10 | 取引単体テストの実施方法 > テスト結果エビデンスの収集 | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:260`）: - **batch-19**（`RequestUnitTest_batch.rst` 14件 + `03_DealUnitTest/index.rst` 6件、commit `91cbe78`）: MOVE 16 / DROP 3 / REFERENCE 1。全行user。DRO… |
| current-0100 | real.rst | 2 | (冒頭) | 今回レビュー・A（空/TOC/アンカー実測） | DROP維持 | RSTアンカー(.. _`real_request_test`:)+空行のみ、プローズなし |
| current-0068 | http_send_sync.rst | 2 | (冒頭) | 今回レビュー・A（空/TOC/アンカー実測） | DROP維持 | RSTアンカー(.. _`message_httpSendSyncMessage_test`:)+空行のみ、プローズなし |
| current-0011 | 02_entityUnitTestWithNablarchValidation.rst | 2 | Nablarch Validationに対応したForm/Entityのクラス単体テスト > (冒頭) | 今回レビュー・A（空/TOC/アンカー実測） | DROP維持 | RSTアンカー(.. _entityUnitTest:)+空行のみ、プローズなし |
| current-0252 | 04_MasterDataRestore.rst | 2 | マスタデータ復旧機能 > (冒頭) | 今回レビュー・A（空/TOC/アンカー実測） | DROP維持 | RSTアンカー(.. _`master_data_backup`:)+空行のみ、プローズなし |
| current-0253 | 04_MasterDataRestore.rst | 5 | マスタデータ復旧機能 > (L1直下) | 今回レビュー・A（空/TOC/アンカー実測） | DROP維持 | .. contents:: 目次（:depth: 2 :local:）のTOCディレクティブのみ、プローズなし。直後L11以降の実文（概要節）は範囲外で切り取り漏れなし |
| input-0075 | ntf-testdata-doc-examples-overview.md | 3 | NTF テストデータ解説書 — 記述例（概要・groupId） > (L1直下) | 既存記録 | DROP維持 | レビュー済み（`checks/task-05.md:258`）: **batch-24**（`ntf-testdata-doc-examples-file.md#1` 11件 + `ntf-testdata-doc-examples-overview.md` 7件、commit `5102bd8`）: MERGE 17 / DROP 1。全行u… |
| current-0153 | send_sync.rst | 2 | (冒頭) | 今回レビュー・A（空/TOC/アンカー実測） | DROP維持 | RSTアンカー(.. _dealUnitTest_send_sync:)+空行のみ、プローズなし |
| current-0352 | 01_MasterDataSetupTool.rst | 2 | (冒頭) | 今回レビュー・A（空/TOC/アンカー実測） | DROP維持 | RSTアンカー(.. _master_data_setup_tool:)+空行のみ、プローズなし |
| current-0001 | 01_entityUnitTestWithBeanValidation.rst | 2 | (冒頭) | 今回レビュー・A（空/TOC/アンカー実測） | DROP維持 | RSTアンカー(.. _entityUnitTestWithBeanValidation:)+空行のみ、プローズなし |
| current-0113 | rest.rst | 5 | リクエスト単体テストの実施方法 > 前提条件 | 今回レビュー・C（rest.rst 重複実測） | DROP維持 | current-0307/0310（依存モジュール追加の具体的説明・pom.xml例）に主張内容が具体例付きで包含済みと確認 |
| current-0115 | rest.rst | 7 | リクエスト単体テストの実施方法 > テストクラスの書き方 > フレームワークで用意されたテストクラスのスーパークラスを継… | 今回レビュー・C（rest.rst 重複実測） | DROP維持 | current-0313/0314（継承関係・dbInfo/testDataParser要否の詳細）に主張内容が包含済みと確認 |
| current-0116 | rest.rst | 2 | リクエスト単体テストの実施方法 > テストクラスの書き方 > JUnit4のアノテーションを使用する | 今回レビュー・C（rest.rst 重複実測） | DROP維持 | 01_Abstract.rst「テストメソッド記述方法」節と文言レベルでほぼ完全一致、コード例まで付加され上回ると確認 |
| current-0117 | rest.rst | 2 | リクエスト単体テストの実施方法 > テストクラスの書き方 > 事前準備補助機能を使ってリクエストを生成する | 今回レビュー・C（rest.rst 重複実測） | DROP維持 | current-0316（get/post/put/patch/delete/newRequestの各メソッドシグネチャ・使用例）に包含済みと確認 |
| current-0118 | rest.rst | 2 | リクエスト単体テストの実施方法 > テストクラスの書き方 > リクエストを送信する | 今回レビュー・C（rest.rst 重複実測） | DROP維持 | current-0317（sendRequestメソッドシグネチャ）に包含済みと確認 |
| current-0119 | rest.rst | 5 | リクエスト単体テストの実施方法 > テストクラスの書き方 > 結果を確認する | 今回レビュー・C（rest.rst 重複実測） | DROP維持 | current-0318（assertStatusCode・JSONAssert等ライブラリ名・readTextResource・ファイル配置表）に包含済みと確認 |
| current-0333 | 01_HttpDumpTool.rst | 2 | (冒頭) | 今回レビュー・A（空/TOC/アンカー実測） | DROP維持 | RSTアンカー(.. _`http_dump_tool`:)+空行のみ、プローズなし |
| current-0366 | index.rst | 2 | (冒頭) | 今回レビュー・A（空/TOC/アンカー実測） | DROP維持 | RSTアンカー(.. _html_check_tool:)+空行のみ、プローズなし |
| current-0123 | send_sync.rst | 2 | (冒頭) | 今回レビュー・A（空/TOC/アンカー実測） | DROP維持 | RSTアンカー(.. _`message_sendSyncMessage_test`:)+空行のみ、プローズなし |
| input-0094 | ntf-testdata-doc-examples-table.md | 3 | NTF テストデータ解説書 — 記述例（テーブルデータ） > 5.1 テーブルデータの基本形式 > (L2直下) | 今回レビュー・A（空/TOC/アンカー実測） | DROP維持 | HTMLアンカー(<a name="setup-table"></a>)+空行のみ、プローズなし。直後の実文（SETUP_TABLE記述例）は範囲外 |
| current-0137 | http_send_sync.rst | 2 | (冒頭) | 今回レビュー・A（空/TOC/アンカー実測） | DROP維持 | RSTアンカー(.. _dealUnitTest_http_send_sync:)+空行のみ、プローズなし |

### 判定サマリ（`#5c`差し戻し対応前の初回レビュー時点）

- 96行中、**判定が覆った行は0件**（63行=既存記録によるDROP維持の確認、33行=今回の実ファイル通読によるDROP維持の確認）
- `_batch/*.csv` の編集は発生していない（判定を覆した行がないため）
- **この判定は`#5c`差し戻しで一部無効化された。** `input-0178`/`input-0198`は「既存記録」
  に分類されていたが、当該記録は判定を保留したまま閉じられており根拠にならないと指摘された。
  詳細・修正後の判定は下記「`#5c`差し戻し対応」節を参照。

### 再検証（差し戻し対応前・データ変更なしの確認）

```
$ python3 mapping/tools/verify_mapping.py; echo "EXIT: $?"
Loaded 591 rows from mapping.csv
...
lines total (all rows): 12986
lines total (excluding DROP): 11973
...
OK: no errors
EXIT: 0
```

- `lines` 合計 12,986（DROP除く 11,973）・591行はSTEP 0時点から不変
- `stale allowlist` のERRORは0件
- `design.md` は無変更（`git diff` で確認済み。差分なし）

---

## `#5c` 差し戻し対応（保留2件の確定）

`.rn/20260724-ntf-yaml-support/ntf-doc-05c-rework.md` の指示に基づく。対象は上記96行レビューの
うち判定を保留したまま「DROP維持」に分類されていた`input-0178`・`input-0198`の2行。

### STEP R1: 分類基準の修正・再分類

上記「分類方法（機械的、`#5c`差し戻し対応で修正）」節に実施内容・スクリプト出力を記載済み。
機械分類「レビュー済み」63行のうち保留キーワードを含む8行を文面確認し、`input-0178`・
`input-0198`の2行のみが真の保留と確認。他6行（`input-0030-b`・`input-0031`・`current-0293`・
`current-0351`・`current-0198`・`current-0306`）は「申し送り事項を**解決**」という文脈の
誤検出で、当該行自身は確定判定を持つためレビュー済みのまま維持した。

### STEP R2: `input-0178` の確定

**判定: `audience=developer→user`、`disposition=DROP→MERGE`。**
割当先: 第3部 テストの実装方法 > テストデータの書き方 > 使用方法。

**実測根拠**:

1. `nablarch/nablarch-testing`（commit `e21bf67`）を clone し、
   `src/main/java/nablarch/test/core/reader/TestDataParser.java:21` を確認したところ、
   インタフェース宣言に `@Published(tag = "architect")` が付与されていた（`getSetupFile`/
   `getExpectedTableData` はメソッド個別のアノテーションを持たないが、インタフェース宣言への
   付与は全メンバに及ぶ——`nablarch-core`（commit `fcb40bb`）
   `nablarch/core/util/annotation/Published.java` のJavadoc「クラスの全てのAPIを公開APIと
   する場合は、本アノテーションをクラス宣言に付与している」）。
2. `tag = "architect"` の意味を同Javadoc（`Published.java:33-39`）で確認: 「アーキテクト向けに
   公開したい場合は、`@Published(tag = "architect")` というようにタグを付与する」——Nablarch
   内部専用という意味ではなく、NTF解説書の読者区分の一方である「アーキテクト」（design.md §1）
   向け公開APIであることを示す。
3. 現行解説書 `current-0233`/`current-0234`（`git show c241906:ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/03_Tips.rst`
   485-507行で本文確認）は、同じ`TestDataParser`インタフェースの兄弟メソッド`getListMap`を
   `SystemRepository.getObject("testDataParser")`経由で直接呼び出す具体的コード例を、
   アプリ開発者向けページ（コンポーネント単体テスト > 使用方法）で既に説明している。
   `tag="architect"`であることが本解説書でのuser判定を妨げない先例が既存解説書に存在する。
4. `input-0178`本文（`getSetupFile`がSETUP_FIXED/SETUP_VARIABLEを1つのリストにまとめる、
   `getExpectedTableData`がEXPECTED_TABLE/EXPECTED_COMPLETE_TABLEをマージする、という仕様）は
   「複数シートがどう1つの結果にまとまるか」という記法の解釈規則そのもので、design.md §9
   ただし書き（利用者向け仕様は解説書へ移す）に該当。同じ`ntf-testdata-loading.md`由来で
   同様に判断された`input-0171`/`input-0172`/`input-0176`/`input-0179`（すべて
   audience=user、テストデータの書き方>使用方法へMERGE/MOVE）と同型の判断とした。

`_batch/batch-18.csv`のinput-0178行を編集（audience/dest_part/dest_page/dest_section/disposition/noteを更新、コミットハッシュ・引用箇所を含む）。

### STEP R3: `input-0198` の確定

**判定: 3分割。**

| 分割後ID | 範囲 | 行数 | 判定 |
|---|---|---|---|
| input-0198-a | 273-294 | 22 | DROP維持（mermaidクラス図: `TestDataFormatWriter`/`YamlFormatWriter`/`XlsFormatWriter`/`ExcelFormatConfig`/`YamlTestDataValidator`の実装関係のみ） |
| input-0198-b | 295 | 1 | **DROP→MERGE**（第4部 ツール > テストデータ変換ツール > 機能概要） |
| input-0198-c | 296-298 | 3 | DROP維持（`YamlFormatWriter`/`XlsFormatWriter`の整形実装参照のみ） |

**実測根拠**:

1. `input/testdata-converter-design.md`を`nl -ba`で行番号確認のうえ全文読解（270-300行）。
   295行「`YamlTestDataValidator`（`ValidationError`と対）はYAML OUT後にスキーマ検証を行う
   リンターで、不正なYAMLが生成された場合は`ValidationError`リストを返す。」が唯一の
   利用者向け機能情報で、前後（273-294のmermaidクラス図、296-298の`XlsFormatWriter`整形実装
   参照）は内部構造説明。current-0156と同型の「サンドイッチ型」3分割とした。
2. 元noteの誤り確認: `input-0194`（`testdata-converter-design.md` 155-171、
   「書き出し（OUT）の整形方針」節）を実際に読んだところ、内容はYAML OUT（全値クォート）・
   Excel OUT（背景色/列幅/罫線/データブロック間の空行の設定表）という**整形方針のみ**で、
   `YamlTestDataValidator`・スキーマ検証・`ValidationError`への言及は一切ない。元note
   「書き出し整形方針の要点はinput-0194で既にカバー」は295行（スキーマ検証）には当てはまらず、
   296-298行（`XlsFormatWriter`の整形実装参照）についてのみ正しかった。
3. `TestDataConverter#convert(from,to,input,output)`という利用の入口（298-320行、
   「利用の入口」節）を読み、ツール利用者（NTF利用PJ・Nablarch開発チーム）は
   `TestDataConverter`をプログラムから直接呼び出す構成であることを確認。YAML変換実行時に
   自動でスキーマ検証が走り不正な場合にエラーが返る、という挙動は「何ができるか」
   （design.md §5 機能概要の定義）に該当する利用者向け情報と判断した。
4. `mapping_id`は`input-0198-a`/`-b`/`-c`とし、`src_section_id`は`input-0198`のまま維持
   （分割手順は`#5`の`input-0016`/`input-0030`に倣う）。ただしdisposition値は
   `input-0016`/`input-0030`の先例（`SPLIT`ではなくMERGE/DROPを直接使用）を踏襲した。
   `mapping/split-plan.md`に本分割の経緯を追記済み（`#5d` STEP1と重複してよい）。

`_batch/batch-02.csv`のinput-0198行を3行に分割編集（コミットハッシュ・引用箇所を含む）。

### STEP R4: 再検証

`mapping.csv`を全30バッチの単純連結で再生成（591行→593行、`input-0198`の1行→3行分割で+2）。

```
$ python3 mapping/tools/verify_mapping.py; echo "EXIT: $?"
Loaded 593 rows from mapping.csv

pending zero assignments: 25 (awaiting #6 decision)
...(STEP0時点から変化なし。input-0178/input-0198の割当先はいずれも既に非0だったページ・
セクションのため、新たに0件が埋まったケースはない)...
lines total (all rows): 12986
lines total (excluding DROP): 11983

candidate duplicate destinations: 44 (advisory only, not auto-fixed)
...(既存出力から変化なし)...

OK: no errors
EXIT: 0
```

- `lines` 合計（全行）は **12,986で不変**
- `DROP除く`合計は 11,973 → **11,983**（input-0178の9行、input-0198-bの1行が非DROPに）
- `disposition`内訳: MERGE 226→228 / DROP 96（行数不変。input-0178が1行DROP脱退、
  input-0198が1行→2行DROPに増加で相殺） / MOVE 239・SPLIT 16・REFERENCE 14は不変
- `audience`内訳: user 563→565 / developer 28（不変。input-0178が1行developer脱退、
  input-0198が1行→2行developerに増加で相殺）
- `stale allowlist`のERRORは0件。`input-0178`（テストデータの書き方>使用方法、既存136行）・
  `input-0198-b`（テストデータ変換ツール>機能概要、既存で非0）とも割当先ページ・セクションは
  元々0件ではなかったため、`EXPECTED_ZERO_*`/`PENDING_ZERO`・`checks/task-05b.md`の
  許可リスト更新は不要
- `mapping/volume.md`を更新（dest_page別: テストデータの書き方3307→3316、テストデータ変換
  ツール74→75。dest_section別: 第3部使用方法8818→8827、第4部機能概要162→163。DROP除く合計
  11,973→11,983。DROP理由別: 開発者向け内部情報480→470、DROP合計1,013→1,003。disposition内訳
  MERGE226→228。audience内訳user563→565。マッピング行数591→593）
- `design.md`は無変更（`git diff`で確認）

### Completion criteria 充足確認（差し戻し対応後）

- 分類基準が「記録に当該行自身の保留表現が含まれる場合はレビュー済みとしない」を含む
  （上記「分類方法（機械的、`#5c`差し戻し対応で修正）」節）
- `input-0178`・`input-0198`を含む全96行（分割後は98行相当）に、保留ではない確定した
  判定がある
- `input-0198`の`note`から、実測で否定された理由（「input-0194で既にカバー」）が除かれている
  （`input-0198-a`/`-b`/`-c`いずれのnoteも新しい実測根拠に差し替え済み）
- `DROP`解除（`input-0178`・`input-0198-b`）があり、`volume.md`・許可リスト・
  `checks/task-05b.md`が更新され、`stale allowlist`のERRORが0件
  （許可リストは元々非0だったため`checks/task-05b.md`自体の変更は不要と確認済み）
