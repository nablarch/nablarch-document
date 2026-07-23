# ゲート②検出結果と対処案

## サマリー

| 判定 | 件数 |
|---|---|
| MOVED | 109 |
| MISSING | 238 |
| DUPLICATED | 80 |
| KEPT | 2470 |
| MODIFIED | 8 |
| 合計 | 2905 |

---

## DUPLICATED 一覧

### DUP-001: `01_Abstract.rst` L195-579 — テストデータ記述内容が A-1 と B-1 に二重掲載（G1-01）

- **src**: `ja/.../06_TestFWGuide/01_Abstract.rst` L195-579（80件）
- **照合方法**: after の `01_Abstract.rst` にテキスト残存確認 + B-1（`testdata/index.rst`）ファイル存在確認
- **照合結果**: after の `01_Abstract.rst` に L197-567 のテキストが残存している。かつ `testdata/index.rst`（B-1）が新規作成済みである（`os.path.exists` 実測）。
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

### MOD-002〜008: `03_Tips.rst` L77/146/390/441/663/788/819 — 用語変更・アンダーライン調整

- **src**: `ja/.../06_TestFWGuide/03_Tips.rst`（7件）
- **照合方法**: after の同行番号テキスト比較

| item_id | 行番号 | kind | 変更内容（抜粋） |
|---|---|---|---|
| B-1808 | L77 | heading | アンダーライン長変更（`=` 19→26文字） |
| B-1819 | L146 | heading | アンダーライン長変更（`=` 19→26文字） |
| B-1878 | L390 | heading | アンダーライン長変更（`=` 19→26文字） |
| B-1892 | L441 | para | `Excelファイルに設定する値` → `テストデータファイルに設定する値` |
| B-1932 | L663 | heading | アンダーライン長変更（`=` 24→26文字） |
| B-1966 | L788 | para | `テストデータ用のExcelに記述されたデータ` → `テストデータファイルに記述されたデータ` |
| B-1975 | L819 | heading | アンダーライン長変更（`=` 20→26文字） |

- **対処案**: YAML 対応に伴う用語統一変更およびアンダーライン修正。内容は正しく更新されているため対処不要。

---

## MISSING 一覧

### MISSING 概要

238件。before 由来 113件、input 由来 125件。

#### before 由来（113件）

| ファイル | 件数 | kind 内訳 | 主な原因 |
|---|---|---|---|
| `JUnit5_Extension.rst` | 25 | code=20, para=5 | コードブロック内容が空（パターン生成不可）、`:depth:` ディレクティブは dest に存在せず |
| `index.rst`（RequestUnitTest） | 11 | toctree=5, para=6 | toctree は照合対象外、一部 para は dest ディレクトリ内に存在せず |
| `01_entityUnitTestWithBeanValidation.rst` | 9 | code=9 | コードブロック内容が空（パターン生成不可） |
| `batch.rst` | 8 | code=8 | コードブロック内容が空（パターン生成不可） |
| `03_Tips.rst` | 8 | code=7, para=1 | コードブロック内容が空（パターン生成不可）、用語変更済みの para |
| `02_entityUnitTestWithNablarchValidation.rst` | 7 | code=7 | コードブロック内容が空（パターン生成不可） |
| `02_RequestUnitTest.rst` | 6 | code=5, para=1 | コードブロック内容が空（パターン生成不可） |
| `04_MasterDataRestore.rst` | 6 | code=6 | コードブロック内容が空（パターン生成不可） |
| `02_componentUnitTest.rst` | 5 | code=5 | コードブロック内容が空（パターン生成不可） |
| `RequestUnitTest_rest.rst` | 5 | code=5 | コードブロック内容が空（パターン生成不可） |
| その他 | 19 | code=17, para=1, heading=1 | 同上または dest に存在せず |

**照合失敗の主因**: `code` kind のほとんどはインベントリの `detail` 列が空（コードブロック先頭行が取得できていない）ため、パターン生成不可で MISSING と判定されている。コード内容は after ファイルに存在すると見られるが機械照合ではヒットしない。

**対処案**: code kind で `detail` が空の項目（90件）については、インベントリ生成スクリプトの改修でコードブロック先頭行を取得できれば照合可能となる。現時点の MISSING 判定は「照合手法の限界」であり「コード内容が消失している」ことを示さない。残りの 23件（para/heading/toctree）は内容または移送先を人手確認すること。

#### input 由来（125件）

| ファイル | 件数 | design_dest | 照合結果 |
|---|---|---|---|
| `ntf-testdata-doc.md` | 65 | B-1 | 照合失敗 |
| `ntf-testdata-doc-examples-special.md` | 21 | B-2 | 照合失敗 |
| `ntf-testdata-doc-examples-testshots.md` | 11 | B-2 | 照合失敗 |
| `ntf-testdata-doc-examples-messaging.md` | 9 | B-2 | 照合失敗 |
| `ntf-testdata-doc-examples-file.md` | 8 | B-2 | 照合失敗 |
| `ntf-testdata-doc-examples-table.md` | 8 | B-2 | 照合失敗 |
| `ntf-testdata-doc-examples-overview.md` | 3 | B-2 | 照合失敗 |

**照合失敗の原因**:

- input の見出しは `1. 全体像`・`3.1 識別の構成要素` 等の番号付きフラット形式
- B-1/B-2 の見出しは `テストデータの全体像`・`識別の構成要素` 等に改題されている
- コードブロックのキーワード（`yaml`、`mermaid` など）は汎用的で対応付け不可

**対処案**: input ファイル由来の MISSING は、B-1/B-2 の各節と input 資料の対応を目次対照（人手確認）で検証すること。

---

## 既知の逸脱 G1-01 の検出確認

G1-01（`01_Abstract.rst` L195-579）は **DUPLICATED として80件検出**された。

- item_id: B-1423〜B-1502（`01_Abstract.rst` の L197-567 に対応する80項目）
- 検出根拠:
  1. after の `01_Abstract.rst` に L197-567 のテキストが残存していることを確認
  2. after ツリーに B-1（`testdata/index.rst`）が新規作成済みであることを確認（`os.path.exists` 実測）

G1-01 が DUPLICATED として台帳に記録されたことを確認した。

---

## 台帳精度に関する注記

### code kind の照合限界

インベントリの `code` kind 項目のうち `detail` 列が空の項目（90件）は、パターン生成不可のため MISSING と判定した。これはコードブロックの内容消失を意味しない。インベントリ生成スクリプトを改修してコードブロック先頭行を取得できれば、大半は KEPT に転じると見られる。

### toctree の照合除外

`toctree` kind（5件）は照合対象外とし MISSING とした。toctree エントリは after ファイルに存在する可能性があるが、本台帳の照合スコープ外とした。
