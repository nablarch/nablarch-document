# review-t3 Completion Check

## Completion Criteria

| Criterion | Self-check | Evidence |
|---|---|---|
| gate2-traceability.csv の行数が before+input の合計行数（2905）と一致する | OK | 実測2905行（header除く）、wc -l = 2906（header込み） |
| verdict が空欄の行が0件 | OK | 空欄件数=0（python3 実測） |
| MISSING / DUPLICATED / MODIFIED の全件が gate2-findings.md に列挙され対処案がある | OK | MISSING=471件、DUPLICATED=80件（DUP-001）、MODIFIED=3件（MOD-001〜003）が記録済み |
| 既知の逸脱 G1-01 が DUPLICATED として検出されている | OK | B-1423〜B-1502（01_Abstract.rst L197-567、80件）が DUPLICATED として記録済み |

## Verdict 別件数

| 判定 | 件数 |
|---|---|
| MOVED | 44 |
| MISSING | 471 |
| DUPLICATED | 80 |
| KEPT | 2307 |
| MODIFIED | 3 |
| 合計 | 2905 |

## Overall Verdict

- Self-check: **OK**

## 備考

- MOVED=44（前回109→偽陽性除去後44）: input ファイル由来の code 種別44件。YAML 固有キー（`setup_files:`・`expected_tables:` 等）の本体行で照合した真陽性のみ残存。
- MISSING=471: before 由来 281件 + input 由来 190件。
  - code kind の detail 空（102件）は照合手法の限界。コード内容消失を示さない。
  - heading の短見出し（MIN_PATTERN_LEN=4文字未満）は照合キーとして不使用（概要・特徴 等）。
  - heading の改題済み見出し（Excelファイル記述例→テストデータファイル記述例 等）は MISSING。
- MODIFIED=3: `index.rst` L621（用語変更）1件 + `03_Tips.rst` L441/788（用語変更）2件。
- G1-01（DUPLICATED 80件）: `01_Abstract.rst` の L197-567 が after にも残存し、かつ B-1 が新規作成済みのため二重掲載として検出。
