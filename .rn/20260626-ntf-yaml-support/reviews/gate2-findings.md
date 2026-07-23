# ゲート②検出結果と対処案

## サマリー

| 判定 | 件数 |
|---|---|
| MOVED | 29 |
| MISSING | 486 |
| DUPLICATED | 80 |
| KEPT | 2307 |
| MODIFIED | 3 |
| 合計 | 2905 |

---

## DUPLICATED 一覧

### DUP-001: `01_Abstract.rst` L195-579 — テストデータ記述内容が A-1 と B-1 に二重掲載（G1-01）

- **src**: `ja/.../06_TestFWGuide/01_Abstract.rst` L195-579（80件）
- **照合方法**: after の `01_Abstract.rst` に before L197-567 のテキストが残存するか grep 実測
- **照合結果**: after の `01_Abstract.rst` に L197-567 のテキストが残存している（grep 実測）。なお、B-1（`testdata/index.rst`）は新規執筆で文言が異なるため grep では行番号を特定できず（actual_line 空欄、note に照合パターン記録）。DUPLICATED の判定根拠は「src 側（A-1）に残存」かつ「design.md が B-1 集約を宣言しているにもかかわらず A-1 から未削除」である。
- **重複する節（代表）**:
  - L197 — `Excelによるテストデータ記述`
  - L204 — `命名規約`
  - L210 — `パス、ファイル名に関する規約`
  - L232 — `Excelシート名に関する規約`
  - L257 — `シート内の構造`
  - L327 — `コメント`
  - L349 — `マーカーカラム`
  - L392 — `セルの書式`
  - L404 — `日付の記述方法`
  - L447 — `セルへの特殊な記述方法`
- **対処案**: `01_Abstract.rst` の L197-567 セクション全体（`.. _how_to_write_excel:` ラベルから「セルへの特殊な記述方法」節末尾まで）を削除し、B-1（`testdata/index.rst`）への誘導文（`:ref:\`ntf_testdata\`` 参照）に置き換える。ラベル `how_to_write_excel` は B-1 の対応節へのエイリアスとして残す。

---

## MODIFIED 一覧

### MOD-001: `02_RequestUnitTest/index.rst` L621 — 用語変更

- **src**: `ja/.../05_UnitTestGuide/02_RequestUnitTest/index.rst` L621
- **照合方法**: after の同行番号テキスト比較
- **照合結果**: before=`* テストデータをExcelファイルから取得` → after=`* テストデータをテストデータファイルから取得`
- **対処案**: YAML 対応に伴う用語統一変更。内容は正しく更新されているため対処不要。

### MOD-002〜003: `03_Tips.rst` L441/788 — 用語変更

- **src**: `ja/.../06_TestFWGuide/03_Tips.rst`（2件）
- **照合方法**: after の同行番号テキスト比較

| item_id | 行番号 | kind | 変更内容（抜粋） |
|---|---|---|---|
| B-1892 | L441 | para | `Excelファイルに設定する値` → `テストデータファイルに設定する値` |
| B-1966 | L788 | para | `テストデータ用のExcelに記述されたデータ` → `テストデータファイルに記述されたデータ` |

- **対処案**: YAML 対応に伴う用語統一変更。内容は正しく更新されているため対処不要。

### 注記: `03_Tips.rst` の heading 変更（L77/146/243/390/663/819）

見出し「Excelファイル記述例」が「テストデータファイル記述例」に改題されたため、before インベントリとの見出し照合が不一致となり MISSING と判定した（B-1808/B-1819/B-1845/B-1878/B-1932/B-1975）。

---

## MISSING 一覧

### MISSING 概要

486件。before 由来 281件、input 由来 205件。

#### before 由来（281件）

| ファイル | 件数 | kind 内訳 | 主な原因 |
|---|---|---|---|
| `JUnit5_Extension.rst` | 32 | code=14, para=11, admonition=6, heading=1 | コードブロック内容が空、`:depth:` ディレクティブは dest に存在せず |
| `01_entityUnitTestWithBeanValidation.rst` | 29 | code=14, para=13, admonition=2 | コードブロック内容が空、用語変更済みの para |
| `index.rst`（RequestUnitTest） | 26 | toctree=5, code=6, admonition=12, para=1, heading=2 | toctree は照合対象外、一部は dest に存在せず |
| `03_Tips.rst` | 24 | heading=8, code=5, admonition=4, para=7 | 見出し改題（Excelファイル記述例→テストデータファイル記述例）、用語変更済みの para |
| `02_entityUnitTestWithNablarchValidation.rst` | 23 | code=12, para=9, admonition=2 | コードブロック内容が空、用語変更済みの para |
| `batch.rst` | 23 | code=7, para=11, admonition=5 | コードブロック内容が空、用語変更済みの para |
| `RequestUnitTest_rest.rst` | 15 | heading=5, code=6, admonition=4 | 短見出し（MIN_PATTERN_LEN未満）、コードブロック内容が空 |
| `02_RequestUnitTest.rst` | 13 | heading=4, admonition=3, code=6 | 短見出し（MIN_PATTERN_LEN未満）、コードブロック内容が空 |
| `send_sync.rst` | 12 | admonition=6, para=2, code=4 | コードブロック内容が空、用語変更済みの para |
| その他 | 85 | — | 同上または dest に存在せず |

**照合失敗の主因**:
- `code` kind のうち `detail` 列が空の項目（102件）はパターン生成不可。コード内容は after ファイルに存在すると見られるが機械照合ではヒットしない。
- `heading` kind で MIN_PATTERN_LEN（4文字）未満の短見出し（概要・特徴・全体像 など）は照合キーとして使用しない。
- `heading` kind で after ファイルに同一見出しが存在しない改題済み見出しは MISSING。

**対処案**: code kind で `detail` が空の項目については、インベントリ生成スクリプト改修でコードブロック先頭行を取得できれば照合可能となる。現時点の MISSING 判定は「照合手法の限界」であり「コード内容が消失している」ことを示さない。heading・para・admonition の MISSING は内容または移送先を人手確認すること。

#### input 由来（190件）

| ファイル | 件数 | design_dest | 照合結果 |
|---|---|---|---|
| `ntf-testdata-doc.md` | 63 | B-1 | 照合失敗 |
| `ntf-testdata-doc-examples-special.md` | 38 | B-2 | 照合失敗 |
| `ntf-testdata-doc-examples-file.md` | 25 | B-2 | 照合失敗 |
| `ntf-testdata-doc-examples-testshots.md` | 24 | B-2 | 照合失敗 |
| `ntf-testdata-doc-examples-messaging.md` | 17 | B-2 | 照合失敗 |
| `ntf-testdata-doc-examples-table.md` | 16 | B-2 | 照合失敗 |
| `ntf-testdata-doc-examples-overview.md` | 7 | B-2 | 照合失敗 |

**照合失敗の原因**:

- input の見出しは `1. 全体像`・`3.1 識別の構成要素` 等の番号付きフラット形式
- B-1/B-2 の見出しは `テストデータの全体像`・`識別の構成要素` 等に改題されている
- 短見出し（Excel・YAML・全体像 など）は MIN_PATTERN_LEN 未満または RST 見出しとして照合不一致
- コードブロックの言語指定行（`yaml`、`java` など）は照合キーから除外し本体行で照合

**対処案**: input ファイル由来の MISSING は、B-1/B-2 の各節と input 資料の対応を目次対照（人手確認）で検証すること。

---

## 既知の逸脱 G1-01 の検出確認

G1-01（`01_Abstract.rst` L195-579）は **DUPLICATED として80件検出**された。

- item_id: B-1423〜B-1502（`01_Abstract.rst` の L197-567 に対応する80項目）
- 検出根拠:
  1. after の `01_Abstract.rst` に L197-567 のテキストが残存していることを grep で確認（src 残存あり）
  2. design.md マッピング#2 が「テストデータ仕様は B-1 に集約」と宣言しているにもかかわらず、A-1 から未削除のため DUPLICATED と判定
  3. B-1（`testdata/index.rst`）内での actual_line は grep 不一致（新規執筆で文言変更）のため空欄、note に照合パターンを記録

G1-01 が DUPLICATED として台帳に記録されたことを確認した。

---

## 台帳精度に関する注記

### code kind の照合限界

インベントリの `code` kind 項目のうち `detail` 列が空の項目（102件）は、パターン生成不可のため MISSING と判定した。これはコードブロックの内容消失を意味しない。インベントリ生成スクリプトを改修してコードブロック先頭行を取得できれば、大半は KEPT に転じると見られる。

### heading kind の照合方式変更

照合ロジック改修（T3差し戻し修正）により、heading 種別の照合を「本文内部分一致」から「RST見出し行全体一致（行テキスト完全一致 + 次行アンダーライン確認）」に変更した。これにより、短い見出し語（Excel・YAML など）が本文中に出現しただけでは MOVED と判定されなくなった（偽陽性除去）。その副作用として、改題済み見出し（Excelファイル記述例→テストデータファイル記述例 等）および MIN_PATTERN_LEN（4文字）未満の短見出し（概要・特徴 等）が MISSING に転じた。

### toctree の照合除外

`toctree` kind（5件）は照合対象外とし MISSING とした。toctree エントリは after ファイルに存在する可能性があるが、本台帳の照合スコープ外とした。
