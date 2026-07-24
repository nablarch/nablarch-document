# review-t4 Completion Check

## Completion Criteria

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| `gate3-conventions.md` の全規約に、既存ページからの根拠 file:line が2件以上ある | OK | C-01〜C-15 の15規約すべてに `01_Abstract.rst` / `03_Tips.rst` / `04_MasterDataRestore.rst` / `02_DbAccessTest.rst` からの根拠 file:line を2件以上付与した。最小件数は2件（C-13）、最大は5件（C-01）。修正後 C-01: L14/L23 確認済み。 | OK | 全規約の根拠 file:line が2件以上あることを確認（C-01 L14/L23 実ファイル照合済み）。C-07/C-12/C-15 の根拠も実ファイルで検証済み。 |
| `gate3-findings.csv` の全行に `rule_id` が紐づいており、`gate3-conventions.md` に存在する規約IDである | OK | F-001: C-04、F-002: C-14、F-003: C-15、F-004: C-04 — いずれも gate3-conventions.md に定義済みのIDである。 | OK | F-001=C-04, F-002=C-14, F-003=C-15, F-004=C-04 — 全4行のrule_idが gate3-conventions.md に存在することを確認。 |
| 検査対象6ファイルすべてについて検査実施済みであることが Evidence に記載されている | OK | 以下の6ファイルを全件 Read で読み込んで検査した。(1) `testdata/index.rst` — C-04逸脱(F-001)を検出。(2) `testdata/examples.rst` — C-15逸脱(F-003)を検出。(3) `testdata_format.rst` — C-14逸脱(F-002)を検出。(4) `06_TestFWGuide/index.rst` — C-04逸脱(F-004)を検出。(5) `05_UnitTestGuide/index.rst` — 逸脱なし（索引構造のみ）。(6) `03_Tips.rst` — 逸脱なし（だ・である調・見出し構造・コードブロック・アドモニション、すべて適合）。 | OK | 6ファイルの検査実施がself-checkのEvidence列に記載されていることを確認。CSV未掲載の2ファイル（05_UnitTestGuide/index.rst・03_Tips.rst）は「逸脱なし」として明示記録済み。 |

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
