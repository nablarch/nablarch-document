# task-02 Completion Check

## Completion Criteria

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| build_mapping.sh を2回実行して同一CSV（md5一致） | OK | Run 1: current=`756dd044f705c73c9ffe50e65364890e`, input=`15424d91d680f47be9abafd1c23191c9` / Run 2: 同値 — 完全一致。src_file 列にgit相対パスを使用し一時ディレクトリ依存を排除。 | OK | 37→40テスト全パス。オーバーライン境界・simple table回帰含む。 |
| 抽出対象ファイル数が実ファイル数と一致 | OK | RST: `git ls-tree` → **47ファイル**、ログ `RST files found: 47` と一致。MD: `find input/` → **10ファイル**、ログ `MD files found: 10` と一致。 | OK | ファイルリスト取得ロジックを確認。RST は git ls-tree でソート済み、MD は find+sort。 |
| CSVのレコード数を csv.DictReader でカウント | OK | sections-current.csv = **212レコード**、sections-input.csv = **152レコード** | OK | `csv.DictReader` ラウンドトリップテスト（TestWriteCSVRoundtrip）でヘッダ含むRW確認済み。 |
| セクション数が独立カウントの見出し数と一致 | OK | 独立カウントスクリプト実行: RST L3=**212**、MD H3=**152**。CSVレコード数と完全一致。 | OK | build_mapping.sh と extract_sections.py の独立実行で同結果を確認。 |

## QA Expert Review

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Verification approach meaningful to the objective (checks the right thing, not just "passed") | OK | Completion criteria 4項目を個別に検証。md5一致は再現性を、DictReaderカウントは仕様通りの計測を、独立カウント照合は抽出ロジックの正確性を確認している。「実行した」ではなく「正しい値が出た」を確認している。 |

## Expert Reviews (axes the task needs)

### Design Expert

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Approach/structure fits | OK | L3抽出単位はマッピング作業の粒度として適切。section_id の参照問題（#4完了条件との矛盾）はタスク#4着手前にエスカレーション済み。 |
| System-wide integrity (interfaces, cross-doc consistency) | OK | CSV列構成（section_id, src_file, src_line, heading_path, lines, code_blocks, tables, figures）は後続タスクで使用可能な形式。 |

### Craft Expert (coding)

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Medium-specific best practice | OK | Python標準ライブラリのみ使用。エラーハンドリング（UnicodeDecodeError, ValueError, OSError）、命名、sorted()、split(":",1) すべて修正済み。 |
| Consistency with existing style | OK | 型アノテーション、docstring、定数分離など一貫したスタイル。 |

### Verification Expert (test)

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Artifact actually checked (tests run / claims verified / flow traced) | OK | 40テスト全パス。GWT形式導入、assertEqual具体値アサーション、統合テスト（write_csv RT、CLI、決定性）あり。 |
| Coverage (edge cases / claims / steps) | OK | ~^文字、4個以上backtickfence、複数シンプルテーブル、空セクション、ファイル不存在、MDコードブロック内###をカバー。 |

## Overall Verdict

- Self-check: OK
- QA: OK
- Design expert: OK
- Craft expert: OK
- Verification expert: OK
- Ready to check off: Yes
