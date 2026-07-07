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
| 文体（だ・である調） | OK | 全説明文でだ・である調を使用。「〜決まる。」「〜記述する。」「〜省略する。」等。コードブロック内の「正しく更新されます」はテストデータの値であり対象外。 |
| 冒頭文 | OK | ファイル冒頭7行目に「テストデータは Excel または YAML ファイルで記述できる。」が記載。 |
| Excelの場合/YAMLの場合 並列見出し | OK | 全カテゴリ（テスト全体像・グループID・testShots 4方式・テーブル3種・ファイル4パターン・メッセージング2種・特殊値4種）で並列見出し分けを実施。sphinx-tabs は未使用。 |
| RST 見出しレベル | OK | CLAUDE.md の規約通り（= 上下=ページ題、- 上下=大見出し、= 下のみ=中見出し、- 下のみ=小見出し）。アンダーライン長も日本語全角2幅計算で全件 OK。 |
| コードブロック記法 | OK | `.. code-block:: text` / `.. code-block:: yaml` を使用。インデント 4 スペース。 |
| 用語（CLAUDE.md 用語対応表） | OK | `testShots` / `LIST_MAP` 等の識別子は既存ページ表記に準拠。`group_id` キー（テーブル・ファイルセクション用）と `id` キー（list_maps エントリ用）の使い分けは ntf-testdata-doc.md 正典に準拠し正確。 |
| Consistency with existing style | OK | overview.rst との文体・構造・用語が一致。見出し区切り、コードブロック前の説明文パターン（「以下に〜を示す。」「〜で決まる。」）も既存ページに準拠。 |

### Verification Expert (fact-check)

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Examples match input source files | OK | 全カテゴリ（全体像・groupId・testShots 4方式・テーブル3種・ファイル4パターン・メッセージング2種・特殊値4種）のキー名・値・フィールド名・データ型をソースと照合済み。不一致 0 件。[要確認] タグ箇所（overviewのdescription食い違い・specialの${updateTime}/${setUpTime}未定義）は適切に処理されている。 |

## Overall Verdict

- Self-check: OK
- QA: NG→Fix済み（7セクション欠落を修正後 OK）
- Craft expert: OK
- Verification expert: OK
- Ready to check off: Yes
