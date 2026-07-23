# task-null-fix Completion Check

## Completion Criteria

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| examples.rst L410 の「クォートすると文字列として格納される」が削除され、クォートしても Java null になる旨に置き換えられている | OK | L410: `- NULL 値は Excel では ``Null``（大文字小文字不問）、YAML ではアンクォートの ``null`` で記述する（ ``"null"`` とクォートしても同じく Java null になる）。` | | |
| examples.rst L1023 の表現が L410 修正後と整合している | OK | L1023: `- NULL 値は Excel では ``NULL``（大文字小文字不問）、YAML ではアンクォートの ``null`` で記述する（ ``"null"`` とクォートしても同じく Java null になる）。` — L410 と同形式、NULL のみ大文字で元と同様 | | |
| examples.rst 内に他の誤記（同種）が残っていない | OK | `grep -n "クォートすると文字列として格納"` の結果が 0 件 | | |
| 変更前後で修正対象外の行が変わっていない | OK | L409・L411 および L1022・L1024 の前後行に変更なし | | |

## QA Expert Review

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| 検証アプローチが目的に対して意味があるか | OK | 完了基準4項目すべてを実コード・grep・diff で直接確認。NullInterpreter 実装との論理検証も実施。01_Abstract.rst の Excel 専用記述との矛盾もなし |

## Expert Reviews

### Craft Expert (writing)

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| 文章ベストプラクティス（明確さ・正確さ） | OK | だ・である調。括弧補足の位置・書き方は index.rst L980 と同一パターンで自然 |
| 既存スタイルとの一貫性 | OK | index.rst L980 の基準文と逐語的に一致。事実変更の意図は Verification expert が NullInterpreter 実装と照合して解消済み |

### Verification Expert (fact-check)

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| 各主張が実装と照合して検証されているか | OK | アンクォート null・クォート "null"・Excel 大文字小文字不問の3主張すべてを NullInterpreter 実装と突き合わせ確認。YAML パーサ→NullInterpreter の2段階処理も追跡 |
| 未検証の主張が残っていないか | OK | 旧記述「クォートすると文字列として格納される」の削除正当性も確認済み |

## Overall Verdict

- Self-check: OK
- QA: OK
- Craft expert: OK
- Verification expert: OK
- Ready to check off: Yes
