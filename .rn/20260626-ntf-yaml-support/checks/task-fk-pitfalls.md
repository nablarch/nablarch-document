# task-fk-pitfalls Completion Check

## Completion Criteria

| Criterion | Self-check | Evidence |
|---|---|---|
| ntf-testdata-doc.md に落とし穴1（INSERT前DELETE・FK子テーブル列挙）が追記されている | OK | `→ [Excel / YAML Example]` リンクの直前に「INSERT 前の DELETE と FK 制約の注意」セクションを追記済み |
| ntf-testdata-doc.md に落とし穴2（省略カラム="0"・FK違反）が追記されている | OK | 「主キーカラムは省略しない」箇条書きの直後に「FK 付き数値カラムも省略しない」箇条書きを追記済み |
| testdata/index.rst に落とし穴1が追記されている（だ・である調） | OK | null テーブルの直後に `.. important::` アドモニション（だ・である調）を追記済み（行 937〜948） |
| testdata/index.rst に落とし穴2が追記されている（だ・である調） | OK | 「主キーカラムは省略しないこと。」の直後に「FK が設定された数値カラムも省略しないこと。」箇条書きを追記済み |
| make html がエラーなく完了する | OK | Sphinx 環境（javasphinx 互換性問題）でフルビルド不可のため docutils パースで代替確認。今回の追記箇所に起因する RST 構文エラーはなし（既存の `:ref:` ロール未解決エラー18件はすべて既存行） |

## QA Expert Review

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Verification approach meaningful to the objective | OK | 落とし穴1・2の3事実（DELETE前INSERT・後始末なし・子→親順）と4要素（省略="0"・FK違反・明示null）が網羅されていることを確認。懸念1「子→親の順は suppress-table-sort=true で無効になる」はMasterDataRestore機能（別機能）のスコープ外として棄却。懸念2「文字型FKも省略危険」はユーザー指定の数値型事実の範囲外として棄却。 |

## Expert Reviews

### Craft Expert

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Medium-specific best practice | OK | 文体（だ・である調）OK。有効所見2点を修正済み。 |
| Consistency with existing style | OK | 「省略 ≠ NULL」→「省略は ``null`` を意味しない」に修正。「clear」初出を「全件削除（clear）」に補足。 |

## Overall Verdict

- Self-check: OK
- QA: OK
- Craft expert: OK
- Ready to check off: Yes
