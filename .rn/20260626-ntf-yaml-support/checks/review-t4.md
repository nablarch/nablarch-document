# review-t4 Completion Check

## Completion Criteria

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| `gate3-conventions.md` の全規約に、既存ページからの根拠 file:line が2件以上ある | OK | C-01〜C-15 の15規約すべてに `01_Abstract.rst` / `03_Tips.rst` / `04_MasterDataRestore.rst` / `02_DbAccessTest.rst` からの根拠 file:line を2件以上付与した。最小件数は2件（C-13）、最大は5件（C-01）。修正後 C-01: L14/L23 確認済み。 | OK | 全規約の根拠 file:line が2件以上あることを確認（C-01 L14/L23 実ファイル照合済み）。C-07/C-12/C-15 の根拠も実ファイルで検証済み。 |
| `gate3-findings.csv` の全行に `rule_id` が紐づいており、`gate3-conventions.md` に存在する規約IDである | OK | F-002: C-14、F-003: C-15、F-005: C-05 — いずれも gate3-conventions.md に定義済みのIDである（F-001/F-004 は誤検出のため取り下げ）。 | OK | F-002=C-14, F-003=C-15, F-005=C-05 — 全3行のrule_idが gate3-conventions.md に存在することを確認。F-001/F-004 取り下げ・F-005 追加後も rule_id の整合性が保たれている。 |
| 検査対象6ファイルすべてについて検査実施済みであることが Evidence に記載されている | OK | 機械照合（check_headings.py）による全6ファイルの見出し構造確認済み。(1) `testdata/index.rst` — FL1: = over+under, FL2: = under-only, FL3: - under-only, FL4: ~ under-only, FL5: ^ under-only。C-05逸脱なし（体系一貫）。(2) `testdata/examples.rst` — FL1: = over+under, FL2: - over+under, FL3: ~ under-only, FL4: ^ under-only。F-005: testdata/index.rst と異なる記法体系（C-05逸脱）。F-003（C-15逸脱）も検出済み。(3) `testdata_format.rst` — FL1: = over+under, FL2: - over+under, FL3: = under-only, FL4: - under-only。F-002（C-14逸脱）検出済み。(4) `06_TestFWGuide/index.rst` — FL1: = over+under, FL2: = under-only, FL3: - under-only。C-04/C-05の観点では旧F-004は誤検出（= under-only が当ファイルのFL2として一貫使用）— 取り下げ済み。(5) `05_UnitTestGuide/index.rst` — FL1: = over+under のみ（索引構造のみ）、逸脱なし。(6) `03_Tips.rst` — FL1: = over+under, FL2: - over+under, FL3: = under-only, FL4: - under-only。標準体系と一致、逸脱なし。 | OK | 6ファイルの検査実施がself-checkのEvidence列に記載されていることを確認。check_headings.py による機械照合結果を Evidence に追記済み。F-001/F-004 取り下げ・F-005 追加の根拠が Evidence で確認できる。 |

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
