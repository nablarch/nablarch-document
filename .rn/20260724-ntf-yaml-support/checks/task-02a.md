# task-02a Completion Check

## 修正の要点

抽出単位を「L3のみ」から「見出し階層のどこにも属さない本文を作らない」ルールに変更した。

| ルール | 実装 | `heading_path` |
|---|---|---|
| L3を持つL2 → 各L3を抽出 | `walk()` が深さ3で葉として確定（L4以下は畳み込み） | `L1 > L2 > L3` |
| L2直下でL3配下でない本文 | `walk()` が最初の子の前を独立セクション化 | `L1 > L2 > (L2直下)` |
| L3を持たないL2 → L2自体を抽出 | 子を持たない見出しは葉として確定 | `L1 > L2` |
| L1直下でL2配下でない本文 | 同上（深さ1） | `L1 > (L1直下)` |
| 最初の見出しより前の本文 | `_build_sections()` の preamble 処理 | `(冒頭)` |

検証は `mapping/tools/verify_coverage.py` が担当し、`build_mapping.sh` から自動実行される。

## Completion Criteria

| Criterion | Self-check | Evidence |
|---|---|---|
| `lines` 合計と総行数の差分が全行「見出し行」「空行」に分類され、未説明の非空行が0件 | OK | 下記「行の帰属」参照。**UNEXPLAINED = 0**（current / input とも）。バケット合計が総行数に完全一致。 |
| 抽出対象ファイル数が RST 47・MD 10、セクション0件のファイルが存在しない | OK | ログ `RST files found: 47` / `MD files found: 10`。CSVの `src_file` ユニーク数 = 47 / 10。旧ロジックでセクション0件だったRST **16ファイル**が全て解消（ユーザー指摘の16ファイルと一致）。MDは旧から0件。 |
| 2回実行して同一CSV（md5一致） | OK | Run1/Run2 とも `sections-current.csv` = `f4129dee97dfdf65d9a9857028089f14`、`sections-input.csv` = `c79dcfea61056a4ea2e2b6fc09917421`。`diff` 差分なし。 |

## 行の帰属（`verify_coverage.py` 出力）

すべての行を排他的な4バケットに分類し、`counted + trailing_blank + heading + gap_blank == total` が成立することを確認した。

### current（現行解説書 RST 47ファイル）

| 区分 | 行数 | 説明 |
|---|---:|---|
| counted（CSV `lines` の合計） | 9,211 | セクション本文として計上された行 |
| trailing blank | 572 | セクション末尾の空行（`lines` から除外） |
| heading lines | 900 | 見出し行そのもの（オーバーライン／テキスト／アンダーライン） |
| blank-only gaps | 49 | どのセクションにも属さない空行のみの区間 |
| **UNEXPLAINED** | **0** | — |
| 合計 | **10,732** | = 総行数 10,732 ✅ |

### input（input資料 MD 10ファイル）

| 区分 | 行数 | 説明 |
|---|---:|---|
| counted（CSV `lines` の合計） | 3,011 | セクション本文として計上された行 |
| trailing blank | 192 | セクション末尾の空行 |
| heading lines | 221 | 見出し行そのもの |
| blank-only gaps | 19 | どのセクションにも属さない空行のみの区間 |
| **UNEXPLAINED** | **0** | — |
| 合計 | **3,443** | = 総行数 3,443 ✅ |

### `lines` 合計が総行数と一致しない理由（差分の内訳）

`lines` 列は「本文行から末尾空行を除いた数」であり、見出し行を含まない。したがって差分は必ず生じる。その差分の全行が上表の `trailing blank` / `heading lines` / `blank-only gaps` のいずれかに分類され、**分類できない非空行は0件**である。これが取りこぼしゼロの機械的な証明になる。

- current: 10,732 − 9,211 = 1,521 = 572 + 900 + 49 ✅
- input: 3,443 − 3,011 = 432 = 192 + 221 + 19 ✅

### 総行数と `wc -l` の1行差について

`wc -l` は current = 10,731、input = 3,442 を返すが、これは末尾に改行がないファイルの最終行を数えないため。`str.splitlines()` による正しい総行数は 10,732 / 3,443。該当ファイルは各1件:

- `ja/development_tools/testing_framework/guide/development_guide/08_TestTools/01_HttpDumpTool/02_SetUpHttpDumpTool.rst`
- `.rn/20260724-ntf-yaml-support/input/testdata-converter-design.md`

## 抽出結果の変化

| | 旧（L3のみ） | 新 | 差分 |
|---|---:|---:|---:|
| sections-current.csv レコード数 | 212 | **377** | +165 |
| sections-input.csv レコード数 | 152 | **202** | +50 |
| `lines` 合計 current | 7,318 | **9,211** | **+1,893** |
| `lines` 合計 input | 2,494 | **3,011** | **+517** |
| セクション0件のRSTファイル | 16 | **0** | −16 |

レコード数は `csv.DictReader` でカウントした値。

### 新セクションの内訳

| 種別 | current | input |
|---|---:|---:|
| 見出しセクション | 280 | 169 |
| `(L2直下)` | 53 | 23 |
| `(L1直下)` | 18 | 10 |
| `(冒頭)` | 26 | 0 |
| 合計 | 377 | 202 |

## テスト

`python3 -m pytest test_extract_sections.py -q` → **50 passed, 44 subtests passed**。

新仕様に合わせて更新したテスト:

| テスト | 変更内容 |
|---|---|
| `test_no_l3_extracts_the_l2_itself` | 旧 `test_no_l3_returns_empty`（0件期待）→ L2自体が1セクションになることを確認 |
| `test_no_h3_extracts_the_h2_itself` | 旧 `test_no_h3_returns_empty` → 同上 |
| `test_h2_direct_body_becomes_its_own_section` | 旧 `test_h2_not_standalone_section` → H2直下本文が `(L2直下)` になることを確認 |
| `test_overline_boundary_no_bleed` | 全見出しが同レベルの場合、各々が葉セクションになる（0件 → 4件） |

追加したテスト:

- `TestDirectBodySections` — `(L1直下)` / `(L2直下)` の生成、`src_line` が本文開始行を指すこと、空行のみの直下はセクション化しないこと
- `TestPreambleSections` — `(冒頭)` の生成、見出しが1つもないファイルが1セクションになること
- `TestNoBodyLineLost` — 全22サンプルについて未説明行0・範囲重複0・バケット合計一致を検証（サブテスト）
- `TestWriteCSVDropsPrivateKeys` — `_range_start` / `_range_end` がCSVに出力されないこと

## QA Expert Review

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Verification approach meaningful to the objective | OK | 「L3を持たないページを追加した」だけでは L2直下の本文漏れを検出できない、というユーザー指摘に対し、全行の排他的分類と `counted + trailing_blank + heading + gap_blank == total` の恒等式で応えた。未説明の非空行が1行でもあれば `verify_coverage.py` が exit 1 を返し、`build_mapping.sh` が `set -e` で失敗する。検証が回帰防止として常時働く。 |

## Expert Reviews

### Design Expert

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Approach/structure fits | OK | 抽出ルールを RST/MD 共通の `_build_sections()` に集約し、言語差分は見出しパーサとカウンタのみに閉じた。マーカーは `(冒頭)` / `(L{n}直下)` で実見出しと区別可能。 |
| System-wide integrity | OK | CSV列構成は不変（`section_id, src_file, src_line, heading_path, lines, code_blocks, tables, figures`）。後続タスク #5 は `src_section_id` で全 `section_id` の被覆を機械的に検証できる。 |

### Craft Expert (coding)

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Medium-specific best practice | OK | 標準ライブラリのみ。`Heading` を `NamedTuple` に正規化し、RST のオーバーライン形式（見出しが3行）と MD（1行）の差を `start` / `text_line` / `body_start` で吸収した。`write_csv` は `extrasaction="ignore"` で内部キーを落とす。 |
| Consistency with existing style | OK | 既存の型アノテーション・docstring・定数分離を踏襲。カウント関数群は無変更。 |

### Verification Expert (test)

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Artifact actually checked | OK | 50テスト＋44サブテストが全パス。実コーパス（47+10ファイル、14,175行）に対して UNEXPLAINED = 0 を確認済み。 |
| Coverage (edge cases) | OK | 見出しなしファイル、冒頭本文、L1直下、L2直下、空行のみの直下、同レベル見出しの並び、L4畳み込み、コードフェンス内の `###` をカバー。 |

## Overall Verdict

- Self-check: OK
- QA: OK
- Design expert: OK
- Craft expert: OK
- Verification expert: OK
- Ready to check off: Yes（user review 待ち）
