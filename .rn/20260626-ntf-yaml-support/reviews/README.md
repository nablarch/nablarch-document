# reviews/ README — NTF解説書 YAML対応 レビューゲート参照文書

## 概要

このディレクトリは PR `feature/ntf-yaml-support`（NTF解説書 YAML対応）のレビュー成果物を格納している。
PRの正確性を検証するために、以下の3段階のゲートレビューを実施した。

---

## ゲート一覧

### ゲート① 章構成レビュー

- **成果物**: `gate1-structure.md`
- **目的**: `design.md` の章構成が PR の目的に適合しているかを判定する
- **総合判定**: 条件付き合格
- **検出逸脱**: 既知 5件（G1-01〜G1-05）全件検出済み
- **根拠**: A-1〜A-6・B-1〜B-6 各章の読者判定表（file:line 根拠付き）

---

### ゲート② 突合台帳

- **成果物**: `gate2-traceability.csv`（ヘッダー除く 2905行）、`gate2-findings.md`
- **目的**: 変更前と input の全項目が新構成のどこに移送されたかを1項目ずつ追跡する

#### verdict の定義と件数

| verdict | 意味 | 件数 |
|---|---|---|
| KEPT | 変更前と同じ内容が変更後も同じファイルに存在する | 2307件 |
| MISSING | 変更前または input に存在した内容が変更後に確認できない | 486件 |
| DUPLICATED | 変更前または input の内容が変更後に複数箇所に存在する | 80件 |
| MOVED | 変更前に存在した内容が変更後に別ファイルへ移動した | 29件 |
| MODIFIED | 内容が変更されて移送された | 3件 |

MISSING・DUPLICATED の対処案は `gate2-findings.md` に記載している。

---

### ゲート③ 記述規約の抽出と逸脱検出

- **成果物**: `gate3-conventions.md`（C-01〜C-15、15規約）、`gate3-findings.csv`（10件）
- **目的**: 新規追加ページ（B-1/B-2/A-3）が既存ページと同じ書きっぷりかを判定する

#### finding 件数内訳

| finding_id | 規約 | 件数 | 検出方法 |
|---|---|---|---|
| F-001〜F-008 | C-04（見出し階層） | 8件 | `check_headings.py` 自動生成 |
| F-101 | C-14（太字前後スペース） | 1件 | 手記述 |
| F-102 | C-15（導入文重複） | 1件 | 手記述 |

---

## インベントリ再生成コマンド

```bash
# リポジトリルートから実行
bash .rn/20260626-ntf-yaml-support/reviews/tools/build_inventory.sh
# 出力: inventory-before.csv (2686行), inventory-after.csv (3602行), inventory-input.csv (492行)
# ※行数はヘッダー含む
```

---

## check_headings.py の使い方

```bash
# 見出し構造レポート
python3 .rn/20260626-ntf-yaml-support/reviews/tools/check_headings.py <rst_file>

# C-04 逸脱の自動検出（gate3-findings.csv の C-04 行を再生成）
python3 .rn/20260626-ntf-yaml-support/reviews/tools/check_headings.py --findings <repo_root> <rst_file...>
```

C-04 標準体系（FL1=`=`upper+lower、FL2=`-`upper+lower、FL3=`=`under-only、FL4=`-`under-only、FL5=`~`under-only）に照らして逸脱を CSV 形式で出力する。

---

## 判定サマリー

全ゲートの件数が実際の成果物と一致していることを確認できる表。

| ゲート | 成果物 | 件数 |
|---|---|---|
| ゲート① | gate1-structure.md 逸脱 | 5件（G1-01〜G1-05） |
| ゲート② | gate2-traceability.csv | 2905行（ヘッダー除く） |
| ゲート② | gate2-findings.md: MISSING | 486件 |
| ゲート② | gate2-findings.md: DUPLICATED | 80件 |
| ゲート③ | gate3-findings.csv | 10件（F-001〜F-008, F-101, F-102） |
| ゲート③ | うち C-04 自動生成 | 8件（check_headings.py 出力） |

---

## 未対処事項

以下の事項は本レビューで検出したが、修正作業は完了していない（別タスクで対処が必要）。

1. **ゲート②の MISSING 486件**: 変更前・input に存在した内容の一部が新構成に移送されていない。対処案は `gate2-findings.md` を参照。
2. **ゲート②の DUPLICATED 80件**: 内容の重複。対処案は `gate2-findings.md` を参照。
3. **ゲート③の見出し体系逸脱（F-001〜F-008）**: `testdata/index.rst`・`testdata/examples.rst`・`06_TestFWGuide/index.rst` が C-04 標準体系（FL2=`-`upper+lower）から逸脱している。
4. **C-14・C-15 の finding（F-101/F-102）は手記述**: C-04 と異なりスクリプトによる自動生成ではないため、転記漏れが起こりうる。機械的な検証方法の整備が今後の課題。
