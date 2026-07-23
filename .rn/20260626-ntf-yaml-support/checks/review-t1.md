# review-t1 Completion Check

## Completion Criteria

| Criterion | Self-check | Evidence |
|---|---|---|
| `bash reviews/tools/build_inventory.sh` を2回実行して同一のCSVが生成される（冪等） | OK | diff 結果: before/after/input の全3ファイルで差分なし（空diff）— 2回目も同一 |
| 3本のCSVの行数が Evidence に記録されている | OK | before=2574, after=3252, input=331（Python `csv.reader` によるレコード数カウント・ヘッダー除く）— list-table修正後の最新値 |
| 抽出対象ファイル数が対象ディレクトリの rst / md 実ファイル数と一致 | OK | rst(before/base)=47 files, rst(after/current)=50 files; md(input)=10 files。inventory-before.csv のユニークファイル数=47（Python csv.DictReader で検証）、inventory-after.csv のユニークファイル数=50、inventory-input.csv のユニークファイル数=10 — すべて実ファイル数と一致 |

## T1 差し戻し修正 Evidence — 2回目（2026-07-23）

### 修正内容（2回目）

1. **extract_rst.py — ディレクティブ形式テーブル検出追加**: `list-table` / `csv-table` / `table` ディレクティブを `kind=table` として抽出するロジックを追加。
   - `title`: ディレクティブ行末尾のタイトル文字列（なければ空文字）
   - `detail`: オプション行（`:widths:` / `:header-rows:` 等）を `;` 区切りで列挙

### ディレクティブ監査（merge-base 時点の before）

merge-base（`564ed530`）時点の対象 RST ファイルに含まれるディレクティブ一覧:

| ディレクティブ | 件数 | 扱い |
|---|---|---|
| `image` | 87 | 抽出済み（`figure` 種別） |
| `tip` | 85 | 抽出済み（`admonition` 種別） |
| `important` | 24 | 抽出済み（`admonition` 種別） |
| `toctree` | 18 | 抽出済み（`toctree` 種別） |
| `contents` | 2 | 対象外 — ページ内目次を生成するメタディレクティブ。本文コンテンツではないため除外 |
| `warning` | 1 | 抽出済み（`admonition` 種別） |

※ `list-table` は after ツリーの新規ファイル（`index.rst` / `testdata_format.rst` 等）および既存ファイルに含まれる。before ツリーでは `04_MasterDataRestore.rst`（2件）・`JUnit5_Extension.rst`（1件）= 計3件。

現作業ツリー（after）の集計（ファイル単位でなく種別単位）:

| ディレクティブ | 扱い |
|---|---|
| `image` (87) | 抽出済み（`figure`） |
| `tip` (85) | 抽出済み（`admonition`） |
| `important` (25) | 抽出済み（`admonition`） |
| `toctree` (27) | 抽出済み（`toctree`） |
| `note` (6) | 抽出済み（`admonition`） |
| `contents` (3) | 対象外（ページ内目次） |
| `warning` (1) | 抽出済み（`admonition`） |
| `list-table` | 抽出済み（`table` 種別、今回追加） |

### kind別件数（修正後・Python csv.DictReader 実測値）

| kind | before | after |
|---|---|---|
| heading | 492 | 753 |
| toctree | 18 | 27 |
| para | 1609 | 1858 |
| admonition | 110 | 117 |
| table | 97 | 128 |
| code | 161 | 282 |
| figure | 87 | 87 |
| **合計** | **2574** | **3252** |

table 内訳（after）:
- 罫線表（グリッド / シンプル）: 94件
- ディレクティブ形式（list-table 等）: 34件（既存ファイル 3件 + after 新規ファイル 31件）
- **合計: 128件**

before CSV の table 内訳:
- 罫線表: 94件
- ディレクティブ形式（list-table）: 3件（修正により今回初めて抽出）
- **合計: 97件** ← 期待値（罫線94 + ディレクティブ3）に一致

### 3件の漏れが抽出されたことの確認

```
04_MasterDataRestore.rst L41   kind=table  detail=:header-rows: 1;:class: white-space-normal;:widths: 2,6
04_MasterDataRestore.rst L118  kind=table  detail=:header-rows: 1;:class: white-space-normal;:widths: 3,7,2
JUnit5_Extension.rst    L105  kind=table  title=拡張機能が提供するExtensionクラスと合成アノテーションの一覧  detail=:header-rows: 1
```

### CSV レコード数（修正後）

| ファイル | レコード数（ヘッダー除く） |
|---|---|
| inventory-before.csv | 2574 |
| inventory-after.csv | 3252 |
| inventory-input.csv | 331 |

### 冪等確認

2回連続実行: before/after/input 全3ファイルで md5sum が一致（差分なし）:

```
cc94f65c7ae66aa9841074d31251d1fa  inventory-before.csv  (1回目 == 2回目)
1de56a116768f0e24c7b38aaece088bd  inventory-after.csv   (1回目 == 2回目)
23af068e18ba55006897b5c01c4336a2  inventory-input.csv   (1回目 == 2回目)
```

---

## T1 差し戻し修正 Evidence — 1回目（2026-07-23）

### 修正内容

1. **build_inventory.sh カウント方法修正**: `tail -n +2 | wc -l` を Python `csv.reader` によるレコード数カウントに変更。改行を含むセルの複数行カウント誤りを解消。
2. **extract_rst.py ネストコードブロック対応**: アドモニション（`tip`/`note`/`important` 等）本文収集ループ内で、ネストされた `.. code-block::` を検出・抽出するロジックを追加。

### kind別件数（Python csv.DictReader 実測値）

| kind | before | after |
|---|---|---|
| heading | 492 | 753 |
| toctree | 18 | 27 |
| para | 1620 | 1931 |
| admonition | 110 | 117 |
| table | 94 | 94 |
| code | 161 | 282 |
| figure | 87 | 87 |
| **合計** | **2582** | **3291** |

### code 件数検証

- **after CSV code 件数**: 282件（指定の160件以上を満たす）
- **before CSV code 件数**: 161件（修正前154件 + 漏れ7件 = 161件）
- `01_entityUnitTestWithBeanValidation.rst` L104, L333, L503 が before CSV に含まれることを Python csv.DictReader で確認済み

### 冪等確認

- 2回連続実行: before/after/input 全3ファイルで `diff` 結果が空（差分なし）

## Overall Verdict

- Self-check: OK
