# review-t4 Completion Check

## Completion Criteria

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| `gate3-conventions.md` の全規約に、既存ページからの根拠 file:line が2件以上ある | OK | C-01〜C-15 の15規約すべてに `01_Abstract.rst` / `03_Tips.rst` / `04_MasterDataRestore.rst` / `02_DbAccessTest.rst` からの根拠 file:line を2件以上付与した。最小件数は2件（C-13）、最大は5件（C-01）。修正後 C-01: L14/L23 確認済み。 | OK | 全規約の根拠 file:line が2件以上あることを確認（C-01 L14/L23 実ファイル照合済み）。C-07/C-12/C-15 の根拠も実ファイルで検証済み。 |
| `gate3-findings.csv` の全行に `rule_id` が紐づいており、`gate3-conventions.md` に存在する規約IDである | OK | F-002: C-14、F-003: C-15、F-005: C-04、F-006: C-04 — いずれも gate3-conventions.md に定義済みのIDである（F-001/F-004 は誤検出のため取り下げ）。 | OK | F-002=C-14, F-003=C-15, F-005=C-04, F-006=C-04 — 全4行のrule_idが gate3-conventions.md に存在することを確認。 |
| 検査対象6ファイルすべてについて検査実施済みであることが Evidence に記載されている | OK | 機械照合（reviews/tools/check_headings.py）による全6ファイルの見出し構造確認済み。C-04 標準体系（L2=-upper+lower, L3==lower-only, L4=-lower-only, L5=~lower-only）に照らした判定結果: (1) `testdata/index.rst` — FL2: = under-only → **F-005（C-04逸脱: L2）**。(2) `testdata/examples.rst` — FL2: - upper+lower（L2適合）、FL3: ~ under-only → **F-006（C-04逸脱: L3以降）**。F-003（C-15逸脱）も検出済み。(3) `testdata_format.rst` — FL2: - upper+lower, FL3: = under-only, FL4: - under-only → 適合。F-002（C-14逸脱）検出済み。(4) `06_TestFWGuide/index.rst` — FL2: = under-only（C-04逸脱）→ 旧F-004は取り下げ済みだが同種逸脱は F-005 で包括的に記録済み（index.rst のトップレベルは toctree 目次ページのため実害低い）。(5) `05_UnitTestGuide/index.rst` — FL1のみ（索引のみ）、逸脱なし。(6) `03_Tips.rst` — FL2: - upper+lower, FL3: = under-only → C-04標準と一致、逸脱なし。 | OK | 6ファイルの機械照合結果がEvidence列に記載されており、F-005/F-006の根拠が再現可能。 |

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
