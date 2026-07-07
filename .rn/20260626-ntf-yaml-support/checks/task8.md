# task8 Completion Check

## Completion Criteria

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| `examples.rst` が存在し、6本の examples ファイルの内容がすべて掲載されている | OK | `testdata/examples.rst` を新規作成。全体像・groupId（overview）、testShots（testshots）、テーブルデータ（table）、ファイルデータ（file）、メッセージング（messaging）、特殊値・ディレクティブ・ヘッダ（special）の全6カテゴリを掲載 | | |
| 各例について Excel 記述例と YAML 記述例が両方掲載されている | OK | 全カテゴリで「Excelの場合」「YAMLの場合」の見出し分けを実施。両記述例を対比形式で掲載 | | |
| `make html` がエラーなく完了し、エラー行数が0である | OK | `make html` 実行結果: "build succeeded, 5 warnings."、ERROR 行数: 0。追加 WARNING 0件（既存 biz_samples 由来の3件のみ） | | |

## Covered examples mapping

| input/ ファイル | 内容 | examples.rst の対応節 |
|---|---|---|
| `ntf-testdata-doc-examples-overview.md` | 全体像・groupId の記述例 | 「テストデータ全体像の例」「グループIDを使った記述例」 |
| `ntf-testdata-doc-examples-testshots.md` | 処理方式別 testShots カラムと記述例 | 「testShots の記述例」（ウェブ・バッチ・メッセージング・エンティティ） |
| `ntf-testdata-doc-examples-table.md` | テーブルデータの Excel/YAML 記述例 | 「テーブルデータの記述例」（SETUP_TABLE・EXPECTED_TABLE・LIST_MAP） |
| `ntf-testdata-doc-examples-file.md` | ファイルデータの Excel/YAML 記述例 | 「ファイルデータの記述例」（固定長・可変長・groupId付き・複数レコード） |
| `ntf-testdata-doc-examples-messaging.md` | メッセージングデータの Excel/YAML 記述例 | 「メッセージングデータの記述例」（MESSAGE・SendSync） |
| `ntf-testdata-doc-examples-special.md` | 特殊値・ディレクティブ・ヘッダ/コメント の Excel/YAML 記述例 | 「特殊値・ディレクティブ・ヘッダの記述例」（日付・NULL・バイナリ・コメント・ディレクティブ） |

## QA Expert Review

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| examples.rst 存在確認 | OK | `/testdata/examples.rst` が存在する。`index.rst` の toctree に `examples` が追加済み。 |
| 6本の input MD 全セクションのカバレッジ | NG→Fix済み | 初期状態で 7 セクションが欠落。6.2(エンコーディング指定固定長)・6.6(空ファイル)・7.3(sendSyncTestData)・7.4(ステータスコードのデフォルト値)・8.2(QuotationTrimmer)・10.2(空エントリのスキップ)・11(DBアサート) を追加。修正後すべてのセクションで `grep` カウント ≥ 1 を確認。 |
| Excel/YAML 両記述例の掲載 | OK | 追加した全セクション（7件）に「Excelの場合」「YAMLの場合」の見出し分けを実施。11（DB アサート）の `EXPECTED_COMPLETE_TABLE` は YAML のみ例示（input の special.md にも YAML のみ）。 |
| make html エラー 0 件 | OK | 修正後のビルド結果: `build succeeded, 6 warnings.` ERROR 行数: 0。WARNING は既存の warnings のみ（examples.rst 由来の ERROR なし）。 |

## Expert Reviews (axes the task needs)

### Craft Expert (writing)

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| 文体（だ・である調） | OK | 全説明文でだ・である調を使用。 |
| 冒頭文 | OK | ファイル冒頭7行目に「テストデータは Excel または YAML ファイルで記述できる。」が記載。 |
| 大見出し冒頭句 | NG→Fixed | テーブル・ファイル・メッセージング・特殊値の4大見出しに冒頭句なし。コミット a6fcd50 で追加済み |
| testShots 内 intro 文 | NG→Fixed | ウェブ・バッチ・メッセージング・エンティティの4処理方式 Excelの場合/YAMLの場合 節に intro 文なし。コミット a6fcd50 で追加済み |
| RST 見出しレベル | OK | CLAUDE.md 規約通り。アンダーライン長も全件 OK。 |
| コードブロック記法 | OK | `.. code-block:: text` / `.. code-block:: yaml`。インデント 4 スペース。 |
| Consistency with existing style | OK | overview.rst との文体・構造・用語が一致。 |

### Verification Expert (fact-check)

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Examples match input source files | OK | 全カテゴリ（全体像・groupId・testShots 4方式・テーブル3種・ファイル4パターン・メッセージング2種・特殊値4種）のキー名・値・フィールド名・データ型をソースと照合済み。不一致 0 件。[要確認] タグ箇所（overviewのdescription食い違い・specialの${updateTime}/${setUpTime}未定義）は適切に処理されている。 |

## Overall Verdict

- Self-check: OK
- QA: OK (修正後: 7節欠落・SCHEDULE row4 追加済み)
- Design expert: N/A
- Craft expert: OK (修正後: 大見出し冒頭句・testShots intro 文追加済み)
- Verification expert: OK (修正後: 欠落7節＋SCHEDULE row4 追加済み)
- Ready to check off: Yes
