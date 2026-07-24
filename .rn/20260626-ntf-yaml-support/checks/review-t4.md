# review-t4 Completion Check

## Completion Criteria

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| `gate3-conventions.md` の全規約に、既存ページからの根拠 file:line が2件以上ある | OK | C-01〜C-15 の15規約すべてに `01_Abstract.rst` / `03_Tips.rst` / `04_MasterDataRestore.rst` / `02_DbAccessTest.rst` からの根拠 file:line を2件以上付与した。最小件数は2件（C-13）、最大は5件（C-01）。修正後 C-01: L14/L23 確認済み。 | OK | 全規約の根拠 file:line が2件以上あることを確認（C-01 L14/L23 実ファイル照合済み）。C-07/C-12/C-15 の根拠も実ファイルで検証済み。 |
| `gate3-findings.csv` の全行に `rule_id` が紐づいており、`gate3-conventions.md` に存在する規約IDである | OK | C-04: F-001〜F-008（8行）、C-14: F-101、C-15: F-102 — 全10行のrule_idが gate3-conventions.md に定義済み。C-04行はスクリプト自動生成のため転記誤りなし。 | OK | 全10行のrule_idが gate3-conventions.md に存在することを確認。 |
| 検査対象6ファイルすべてについて検査実施済みであることが Evidence に記載されている | OK | `reviews/tools/check_headings.py --findings` による機械照合（全6ファイル）。スクリプト出力C-04行数=8、CSV C-04行数=8（一致）。判定結果: (1) `testdata/index.rst` — FL2〜FL5 全逸脱（F-001〜F-004）。(2) `testdata/examples.rst` — FL3/FL4 逸脱（F-005/F-006）、F-102（C-15）も検出。(3) `testdata_format.rst` — C-04適合。F-101（C-14）検出。(4) `06_TestFWGuide/index.rst` — FL2/FL3 逸脱（F-007/F-008）。(5) `05_UnitTestGuide/index.rst` — FL1のみ、逸脱なし。(6) `03_Tips.rst` — C-04標準と一致、逸脱なし。再現コマンド: `python3 reviews/tools/check_headings.py --findings <repo_root> <6ファイル>` | OK | 6ファイル全件の機械照合結果とスクリプト出力/CSV行数の一致がEvidence列に記載されている。 |

## QA Expert Review

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Verification approach meaningful to the objective (checks the right thing, not just "passed") | OK | 規約の根拠を実ファイルで照合し、逸脱を実際の行で確認した。F-003/F-004 の rule_id・framing 誤りを検出・修正済み。 |

## Expert Reviews

### Craft Expert (writing)

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Medium-specific best practice | OK | gate3-conventions.md は明確・一貫した prose で記述されており、gate3-findings.csv は actionable な fix_proposal を持つ。 |
| Consistency with existing style | OK | だ・である調・用語は既存ページと一致。C-15 も同スタイルで追加された。 |

## Overall Verdict

- Self-check: OK
- QA: OK
- Design expert: N/A
- Craft expert: OK
- Verification expert: N/A
- Ready to check off: Yes
