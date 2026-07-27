# task-02a Completion Check

## 修正の要点

### 1. 抽出ルール — 見出し階層のどこにも属さない本文を作らない

| ルール | `heading_path` |
|---|---|
| L3を持つL2 → 各L3を抽出（L4以下は畳み込み） | `L1 > L2 > L3` |
| L2直下でL3配下でない本文 | `L1 > L2 > (L2直下)` |
| L3を持たないL2 → L2自体を抽出 | `L1 > L2` |
| L1直下でL2配下でない本文 | `L1 > (L1直下)` |
| 最初の見出しより前の本文 | `(冒頭)` |

### 2. `lines` の定義変更（レビュー指摘対応）

**旧**: 本文行から末尾空行を除いた数 → 「どこまでカバーしているか」がCSVから読み取れず、取りこぼしの有無を外部から検証できなかった。

**新**: **当該セクションの本文開始行から、次のセクション開始行の直前までの全行数**。末尾空行を除く処理は廃止。`lines` がカバー範囲そのものになった。

### 3. カバー範囲をCSVに明示（`body_start_line` / `body_end_line` 列を追加）

指摘の誤検出は、カバー範囲を `[src_line, src_line + lines - 1]` と解釈したことで生じた。`src_line` は**見出し行**を指し、本文はその2行後（RSTはアンダーラインを挟む）から始まるため、2行ずれる。

範囲を推測させないよう、開始行と終了行を列として出力するようにした。

```
section_id, src_file, src_line, body_start_line, body_end_line, heading_path, lines, code_blocks, tables, figures
```

指摘された実例:

```
current-0004 src_line=22 body=24-34 lines=11
```

L24〜L34 をカバーしており、L32〜L33 は含まれている。次セクション `current-0005` は body=37 から始まり、間の L35〜L36 は見出し行（テキスト＋アンダーライン）。

### 4. 検証方法をバケット計数から集合演算に変更

`verify_coverage.py` は各セクションの `[body_start_line, body_end_line]` を**行番号の集合**として構築し、和集合を取り、全行集合との差分を取る。恒等式による間接確認をやめ、直接差集合を出す。

- `covered` = セクション範囲の和集合
- `uncovered` = 全行 − `covered`
- `uncovered − 見出し行` に残った行を**1行ずつ内容付きで列挙**
- 範囲の重複も検出（重複は取りこぼしを隠すため、`sum(lines) == len(covered)` を併せて確認）

## Completion Criteria

| Criterion | Self-check | Evidence |
|---|---|---|
| `lines` は開始行から次セクション開始行の直前までの全行数（末尾空行除去なし） | OK | `_build_sections.emit()` で `"lines": range_end - range_start`。テスト `TestBodyRangeColumns.test_range_width_equals_lines` が `body_end_line - body_start_line + 1 == lines` を全セクションで確認。 |
| カバー範囲を行番号の集合として構築し、全行がいずれかのセクションに属することを検証 | OK | 下表参照。`sum(lines) == covered`（current 9,783 / input 3,203）で範囲の重複なしも確認。 |
| 未カバー行は見出し行のみ。それ以外は行と理由を列挙 | OK | 非空行の未カバーは **0件**。空行のみ current 49行 / input 19行が残り、下記に全件列挙。 |
| 抽出対象ファイル数が RST 47・MD 10、セクション0件のファイルなし | OK | ログ `RST files found: 47` / `MD files found: 10`。CSVの `src_file` ユニーク数 = 47 / 10。 |
| 2回実行して同一CSV（md5一致） | OK | `sections-current.csv` = `d77abd49f2140e615d26362eec8fff0e`、`sections-input.csv` = `762714ba70a1a46841af6cae91145b2c`。2回実行して `diff` 差分なし。 |

## 行の帰属（集合演算の結果）

| | current (RST 47) | input (MD 10) |
|---|---:|---:|
| 総行数 | 10,732 | 3,443 |
| セクションがカバー | **9,783** | **3,203** |
| 未カバー: 見出し行 | 900 | 221 |
| 未カバー: 空行 | 49 | 19 |
| **未カバー: 非空行** | **0** | **0** |
| カバー + 未カバー | 10,732 ✅ | 3,443 ✅ |
| `lines` 列の合計 | 9,783（= covered ✅） | 3,203（= covered ✅） |

`lines` 列の合計がカバー行数と一致することは、セクション範囲が互いに重複していないことを意味する。重複があれば合計がカバー数を上回る。

## 未カバーの空行 全件（理由: 空行のみの区間）

見出しとその最初の子見出しの間、またはファイル冒頭から最初の見出しまでの間が**空行のみ**の場合、セクションを生成していない。本文が存在しないため。

これらをセクション化すれば未カバーは見出し行のみになるが、`lines=1` の空行だけのレコードが 68 件 `mapping.csv` に混入し、タスク #5 で全 `section_id` に `disposition` を付ける作業を無意味に増やすため、生成しない判断とした。

**current（計 49 行 / 23 ファイル）**

- `guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/batch.rst` — L6, L486, L539, L540, L541
- `guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/delayed_receive.rst` — L4
- `guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/delayed_send.rst` — L4
- `guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/http_real.rst` — L12
- `guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/http_send_sync.rst` — L19
- `guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/index.rst` — L6, L7, L337
- `guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/mail.rst` — L6
- `guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/real.rst` — L6, L257
- `guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/rest.rst` — L4
- `guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/send_sync.rst` — L6, L7
- `guide/development_guide/05_UnitTestGuide/03_DealUnitTest/http_send_sync.rst` — L19, L20
- `guide/development_guide/06_TestFWGuide/01_Abstract.rst` — L6, L10, L584, L668
- `guide/development_guide/06_TestFWGuide/02_DbAccessTest.rst` — L4, L499, L500
- `guide/development_guide/06_TestFWGuide/02_RequestUnitTest.rst` — L6, L81
- `guide/development_guide/06_TestFWGuide/03_Tips.rst` — L1
- `guide/development_guide/06_TestFWGuide/RequestUnitTest_batch.rst` — L6, L7, L57, L58, L183
- `guide/development_guide/06_TestFWGuide/RequestUnitTest_real.rst` — L4, L5, L65, L66
- `guide/development_guide/06_TestFWGuide/RequestUnitTest_rest.rst` — L6
- `guide/development_guide/06_TestFWGuide/RequestUnitTest_send_sync.rst` — L4, L5, L70, L71
- `guide/development_guide/08_TestTools/01_HttpDumpTool/01_HttpDumpTool.rst` — L6
- `guide/development_guide/08_TestTools/02_MasterDataSetup/01_MasterDataSetupTool.rst` — L6, L31
- `guide/development_guide/08_TestTools/03_HtmlCheckTool/index.rst` — L85
- `guide/development_guide/08_TestTools/index.rst` — L1

**input（計 19 行 / 5 ファイル）**

- `ntf-doc-terms.md` — L130, L326, L413
- `ntf-testdata-doc-examples-special.md` — L8, L122, L207
- `ntf-testdata-doc-examples-testshots.md` — L61, L139, L200
- `ntf-testdata-doc.md` — L93, L164, L212, L335, L433, L529, L638, L699
- `testdata-converter-design.md` — L11, L339

## 抽出結果の変化

| | 旧（L3のみ） | 新 |
|---|---:|---:|
| sections-current.csv レコード数 | 212 | **377** |
| sections-input.csv レコード数 | 152 | **202** |
| `lines` 合計 current | 7,318 | **9,783** |
| `lines` 合計 input | 2,494 | **3,203** |
| セクション0件のRSTファイル | 16 | **0** |

レコード数は `csv.DictReader` でカウントした値。旧ロジックでセクション0件だったRST 16ファイルは、ユーザー指摘の16ファイルと一致。

### 新セクションの内訳

| 種別 | current | input |
|---|---:|---:|
| 見出しセクション | 280 | 169 |
| `(L2直下)` | 53 | 23 |
| `(L1直下)` | 18 | 10 |
| `(冒頭)` | 26 | 0 |
| 合計 | 377 | 202 |

### 総行数と `wc -l` の1行差

`wc -l` は current = 10,731、input = 3,442 を返すが、これは末尾に改行がないファイルの最終行を数えないため。`str.splitlines()` による総行数 10,732 / 3,443 が正。該当ファイルは各1件:

- `ja/development_tools/testing_framework/guide/development_guide/08_TestTools/01_HttpDumpTool/02_SetUpHttpDumpTool.rst`
- `.rn/20260724-ntf-yaml-support/input/testdata-converter-design.md`

## テスト

`python3 -m pytest test_extract_sections.py -q` → **54 passed, 96 subtests passed**。

新規・更新したテスト:

| テスト | 内容 |
|---|---|
| `TestNoBodyLineLost.test_no_uncovered_non_blank_line` | 全22サンプルで、カバー集合の差分に非空行が残らないこと |
| `TestNoBodyLineLost.test_section_ranges_are_disjoint` | セクション範囲が重複しないこと |
| `TestNoBodyLineLost.test_covered_plus_uncovered_equals_total` | カバー＋未カバーが総行数に一致すること |
| `TestNoBodyLineLost.test_sum_of_lines_column_equals_covered` | `lines` 合計がカバー行数に一致すること |
| `TestBodyRangeColumns.test_range_width_equals_lines` | `body_end_line - body_start_line + 1 == lines` |
| `TestBodyRangeColumns.test_next_section_starts_after_previous_range` | 後続セクションの開始行が直前セクションの終了行より後 |
| `TestDirectBodySections` | `(L1直下)` / `(L2直下)` の生成、空行のみの直下はセクション化しないこと |
| `TestPreambleSections` | `(冒頭)` の生成、見出しが1つもないファイルが1セクションになること |
| `test_no_l3_extracts_the_l2_itself` / `test_no_h3_extracts_the_h2_itself` | 旧「0件期待」から、L2/H2自体が1セクションになる期待に変更 |
| `test_h2_direct_body_becomes_its_own_section` | H2直下本文が `(L2直下)` になること |

`lines` の定義変更に伴い、既存テストの期待値を末尾空行を含む値に更新した（例: RST_SIMPLE の L3見出し1 は 3 → 4）。

## QA Expert Review

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Verification approach meaningful to the objective | OK | 前回はバケット分類の恒等式で「合計が合う」ことを見ていたため、分類が誤れば取りこぼしを見逃す構造だった（指摘のとおり）。今回は行番号の集合の差分を直接取り、残った行を内容付きで列挙する。分類の正しさに依存しない。加えて `sum(lines) == covered` で範囲の重複も封じた。 |
| 外部からの独立検証が可能か | OK | `body_start_line` / `body_end_line` をCSVに出力したので、CSVだけで範囲の集合を再構築できる。範囲を `src_line` から推測する必要がなくなり、今回の食い違いは再発しない。 |

## Expert Reviews

### Design Expert

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Approach/structure fits | OK | 抽出ルールを RST/MD 共通の `_build_sections()` に集約。`lines` がカバー範囲そのものになったことで、`volume.md`（タスク #5）の文量集計も「ページの実際の行数」と直結する。 |
| System-wide integrity | OK | CSV列を2列追加。タスク #5 は `src_section_id` で全 `section_id` の被覆を、`body_*_line` で行レベルの被覆を機械検証できる。 |

### Craft Expert (coding)

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Medium-specific best practice | OK | 標準ライブラリのみ。`Heading` を `NamedTuple` に正規化し、RSTのオーバーライン形式（3行）とMD（1行）の差を `start` / `text_line` / `body_start` で吸収。`write_csv` は `extrasaction="ignore"` で内部キーを落とす。 |
| Consistency with existing style | OK | 既存の型アノテーション・docstring・定数分離を踏襲。カウント関数群は無変更。 |

### Verification Expert (test)

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Artifact actually checked | OK | 54テスト＋96サブテストが全パス。実コーパス（47+10ファイル、14,175行）で非空行の未カバー0件を確認。`build_mapping.sh` から自動実行され、`set -e` により回帰時はビルドが失敗する。 |
| Coverage (edge cases) | OK | 見出しなしファイル、冒頭本文、L1直下、L2直下、空行のみの直下、同レベル見出しの並び、L4畳み込み、コードフェンス内の `###` をカバー。 |

## Overall Verdict

- Self-check: OK
- QA: OK
- Design expert: OK
- Craft expert: OK
- Verification expert: OK
- Ready to check off: Yes（user review 待ち）
