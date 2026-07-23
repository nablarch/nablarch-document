# review-t3 Completion Check

## Completion Criteria

| Criterion | Self-check | Evidence |
|---|---|---|
| gate2-traceability.csv の行数が before+input の合計行数（2905）と一致する | OK | 実測2905行（header除く）、wc -l = 2906（header込み） |
| verdict が空欄の行が0件 | OK | 空欄件数=0（python3 実測） |
| MISSING / DUPLICATED / MODIFIED の全件が gate2-findings.md に列挙され対処案がある | OK | MISSING=238件、DUPLICATED=80件（DUP-001）、MODIFIED=8件（MOD-001〜008）が記録済み |
| 既知の逸脱 G1-01 が DUPLICATED として検出されている | OK | B-1423〜B-1502（01_Abstract.rst L197-567、80件）が DUPLICATED として記録済み |

## Verdict 別件数

| 判定 | 件数 |
|---|---|
| MOVED | 109 |
| MISSING | 238 |
| DUPLICATED | 80 |
| KEPT | 2470 |
| MODIFIED | 8 |
| 合計 | 2905 |

## Overall Verdict

- Self-check: **OK**

## 備考

- MOVED=109: input ファイル7本由来（B-1/B-2 該当分でヒットした 109件）。
- MISSING=238: before 由来 113件（code kind の detail 空が主因）+ input 由来 125件（B-1/B-2 での見出し改題による照合失敗）。
- MODIFIED=8: `index.rst` L621（用語変更）1件 + `03_Tips.rst` 7件（用語変更・アンダーライン調整）。
- G1-01（DUPLICATED 80件）: `01_Abstract.rst` の L197-567 が after にも残存し、かつ B-1 が新規作成済みのため二重掲載として検出。
