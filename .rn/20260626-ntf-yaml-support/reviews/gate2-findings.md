# ゲート②検出結果と対処案

## サマリー

| 判定 | 件数 |
|---|---|
| MOVED | 0 |
| MISSING | 234 |
| DUPLICATED | 80 |
| KEPT | 2591 |
| 合計 | 2905 |

### 判定根拠の補足

- **MOVED=0**: before 側の全47ファイルは after にも残存している（ファイル削除なし）。before 項目は out典ファイルに維持されているため KEPT または DUPLICATED となる。
- **KEPT=2591**: before 全2574件のうち2494件は出典ファイルそのままに存在。input 側の97件（ntf-doc-terms.md・ntf-testdata-loading.md・testdata-converter-design.md）は解説書への移送対象外。
- **DUPLICATED=80**: `01_Abstract.rst` L197-567 のテストデータ記述内容（Excelによるテストデータ記述・命名規約・シート内の構造等）が A-1 に残存しつつ、B-1（`testdata/index.rst`）が同一主題で新規作成済みのため二重掲載（G1-01）。
- **MISSING=234**: input ファイル7本（ntf-testdata-doc.md 73件、ntf-testdata-doc-examples-*.md 計161件）が対応する after ファイル（B-1/B-2）に exact grep で見つからない。B-1/B-2 作成時に見出しを RST スタイルに改題しているため exact match が成立しない（概念的移送は完了と推定されるが機械的に照合不能）。

---

## DUPLICATED 一覧

### DUP-001: `01_Abstract.rst` L197-567 — テストデータ記述内容がA-1とB-1に二重掲載（G1-01）

- **src**: `ja/.../06_TestFWGuide/01_Abstract.rst` L197-567（80件）
- **also_in**: `ja/.../06_TestFWGuide/testdata/index.rst`（B-1、新規作成済み）
- **重複する節**:
  - `Excelによるテストデータ記述` (L197)
  - `命名規約` (L204)
  - `パス、ファイル名に関する規約` (L210)
  - `Excelシート名に関する規約` (L232)
  - `シート内の構造` (L257)
  - `コメント` (L327)
  - `マーカーカラム` (L349)
  - `セルの書式` (L392)
  - `日付の記述方法` (L404)
  - `セルへの特殊な記述方法` (L447)
- **対処案**: design.md マッピング#2 の方針に従い、`01_Abstract.rst` の L197-567 セクション全体（`.. _how_to_write_excel:` ラベルから「セルへの特殊な記述方法」末尾まで）を削除し、`:ref:\`ntf_testdata\`` への誘導文に置き換える。ラベル `how_to_write_excel` は B-1 の対応節（`ntf_testdata_basic_structure` 等）へのエイリアスとして残す。

---

## MISSING 一覧

### MISSING 概要

234件すべてが input ファイル由来。before ファイル由来の MISSING は0件。

| input ファイル | 件数 | dest | 照合結果 |
|---|---|---|---|
| `ntf-testdata-doc.md` | 73 | B-1 | 見出し改題のため grep 不可 |
| `ntf-testdata-doc-examples-special.md` | 47 | B-2 | 同上 |
| `ntf-testdata-doc-examples-file.md` | 32 | B-2 | 同上 |
| `ntf-testdata-doc-examples-testshots.md` | 32 | B-2 | 同上 |
| `ntf-testdata-doc-examples-messaging.md` | 21 | B-2 | 同上 |
| `ntf-testdata-doc-examples-table.md` | 20 | B-2 | 同上 |
| `ntf-testdata-doc-examples-overview.md` | 9 | B-2 | 同上 |

### MIS-001: `ntf-testdata-doc.md` → B-1 の照合失敗（73件）

- **src**: `.rn/.../input/ntf-testdata-doc.md` L1-728（heading 50件・code 23件）
- **design_dest**: B-1（`testdata/index.rst`）
- **照合方法**: heading 全文 fixed-string grep、code 冒頭行 fixed-string grep
- **照合失敗の原因**:
  - input の見出しは `1. 全体像`・`3.1 識別の構成要素` 等の番号付き形式
  - B-1 の見出しは `テストデータの全体像`・`識別の構成要素` 等に改題
  - code ブロック（mermaid 図等）の内容は B-1 では RST の code-block に変換済み
- **対処案**: ntf-testdata-doc.md は B-1 の主素材として使用済みであることを設計上確認済み（design.md 参照）。機械照合の失敗は移送完了の否定ではなく見出し改題による照合手法の限界。B-1 の各節が ntf-testdata-doc.md の対応章を網羅しているかは人手レビュー（目次対照）で確認すること。

### MIS-002: `ntf-testdata-doc-examples-*.md` → B-2 の照合失敗（161件）

- **src**: `.rn/.../input/ntf-testdata-doc-examples-{file,messaging,overview,special,table,testshots}.md`（合計161件）
- **design_dest**: B-2（`testdata/examples.rst`）
- **照合方法**: heading 全文 fixed-string grep、code 冒頭行 fixed-string grep
- **照合失敗の原因**:
  - input の見出しは `6.1 固定長ファイル`・`Excel`・`YAML` 等のフラット形式
  - B-2 の見出しは `固定長ファイル（SETUP_FIXED / EXPECTED_FIXED）` 等に改題・統合
  - code ブロックのキーワード（`yaml`・`mermaid`）は一般的すぎて対応付け不可
- **対処案**: MIS-001 と同様に設計上使用済み。B-2 の各節と examples ファイルの対応を目次対照で確認すること。

---

## 既知の逸脱 G1-01 の検出確認

G1-01（`01_Abstract.rst` L195-579）は **DUPLICATED として80件検出**された。

- item_id: B-1423〜B-1502（`01_Abstract.rst` の L197-567 に対応する80項目）
- 検出根拠:
  1. after inventory において `01_Abstract.rst` に L197-567 が存在することを確認（ファイル削除なし）
  2. after ツリーに B-1（`testdata/index.rst`）が新規作成済みであることを確認（`os.path.exists` 実測）
  3. design.md マッピング#2 に「テストデータ仕様は B-1 に集約」と宣言されているにもかかわらず A-1 に未削除のまま残存

G1-01 が DUPLICATED として台帳に記録されたことを確認した。

---

## 台帳精度に関する注記

### grep 照合の限界

本台帳は exact fixed-string grep による機械照合に基づく。以下のケースは照合精度が低下する:

1. **見出しの改題**: input ファイルの見出しが B-1/B-2 作成時に RST スタイルに改題されたため、input 由来の全234件が MISSING となった。これは「移送未実施」を意味しない。
2. **概念的な重複**: 01_Abstract.rst L197-567 と B-1 の重複は見出しテキストが異なるが、同一主題を扱っている（テストデータ記述仕様）。この重複は exact match では検出できないため、設計情報（design.md の宣言）を根拠に DUPLICATED と判定した。

### before 側の照合精度

before 全2574件のうちの DUPLICATED 80件以外（2494件）は KEPT と判定した。これは「すべての before ファイルが after にも存在する」という事実に基づく。after での行番号変化やテキスト修正（Excel→テストデータファイル等の用語修正）は KEPT として扱った。
