# 作業指示: `#6` レビュー指摘2件の対応

配置先: `.rn/20260724-ntf-yaml-support/ntf-doc-06-followup.md`

対象ブランチ: `lovaizu/nablarch-document` の `work`（`fb14975`）

判定: `#6` は**承認**。本書は差し戻しではなく、レビューで見つかった小さな漏れ2件の対応である。`#7` 着手前に片付ける。`design.md` / `mapping.csv` の判断内容は変更しない。

---

## 対応1: `[セクション境界]` note を advisory 全件に持たせる

### 問題

`check_intro_section_split` の advisory が `#5d` 時点の4件から**5件**に増えた（`#6` の分類7 SPLIT により `current-0128-a` が追加）。しかし `[セクション境界]` note を持つ行は4件のままで、`current-0128-a` にない。

`#8〜` のページ作成は `mapping.csv` の `note` を読む。note がないと、`current-0128-a`（導入文、`機能概要`）と `current-0128-b`（手順本体、`使用方法`）が別セクションに分かれている事実がページ作成者に伝わらない。

原因は指示側にある。`#5d` の指示が「該当4行の note に追記する」と件数を固定しており、advisory が増えた場合の扱いを書いていなかった。**個別に追記するのではなく、機械検査で担保する。**

### 実施

#### 1-1. `current-0128-a` の `note` に追記する

既存の note を残し、末尾に追記する。書式は既存4件（`input-0114` / `current-0060` / `current-0142` / `current-0148`）と揃える。

```
 [セクション境界] 本行は導入文であり、後続の本体行（current-0128-b）はdest_section=使用方法に
置かれている。ページ作成時、導入文と本体の接続をページ内で再構成すること（design.md §8
「出典の文面をそのまま流用しない」の範囲で対応可能）。
```

`_batch/*.csv` を編集し、`mapping.csv` は全30バッチの単純連結で再生成する。

#### 1-2. `verify_mapping.py` に検査を追加する

`check_intro_section_split` が advisory として報告した全行が `note` に `[セクション境界]` を含むことを検査する。含まない行は **ERROR（`exit 1`）** とする。

`check_intro_section_split` の戻り値に行オブジェクトを含める形に変えるか、`main()` 側で advisory の `mapping_id` から `note` を引く形にする。実装方法は問わないが、**advisory が将来増えても自動的に検出される**構造にすること。

```python
    intro_errors, intro_advisories = check_intro_section_split(rows)
    errors += intro_errors
    # advisory 全件が [セクション境界] note を持つことを担保する。
    # #5d では4件を個別に追記したが、#6 で advisory が5件に増えた際に追記漏れが発生した。
    # 件数固定の運用をやめ、機械検査で担保する（2026-07-28 #6 レビュー指摘）。
    errors += check_intro_note_present(rows, intro_advisories)
```

#### 1-3. 追加した検査で RED → GREEN を確認する

1-2 を先に入れて実行し、`current-0128-a` が ERROR として検出されること（`exit 1`）を確認して出力を記録する。そのうえで 1-1 を適用し、`exit 0` になることを確認する。順序を逆にしない。

#### 1-4. `#8〜` の Steps を確認する

`steering.md` の `#8〜` には既に「`note` の `[セクション境界]` が含まれる場合、導入文と本体の接続をページ内で再構成する」が入っている（`#5d` STEP 8 で追加済み）。件数に依存する記述がないか確認し、あれば直す。

---

## 対応2: `checks/task-06.md` の self-check 記述を実態に合わせる

### 問題

`checks/task-06.md:906` の完了条件チェックが「`task-06-proposal.md` が削除され、参照も残っていない ✅」となっているが、`checks/task-06.md` 内に `task-06-proposal.md` への参照が9件残っている。

ただし残っている参照はすべて「削除済みの旧 `checks/task-06-proposal.md`」という注記付きであり、**この扱い自体は妥当**（`git` 履歴への追跡性が残るため、ファイル名を消し去るより良い）。直すのは**チェック欄の文言**であって、参照の削除ではない。

### 実施

`checks/task-06.md:906` の行を、実態を表す記述に書き換える。

**Before**

```
| task-06-proposal.mdが削除され、参照も残っていない | ✅ |
```

**After**

```
| task-06-proposal.mdが削除され、残る言及はすべて「削除済みの旧ファイル」と注記されている（`checks/task-06.md`内9件、`steering.md`1件） | ✅ |
```

`ntf-doc-06-instruction.md` 内の参照（4件）は作業指示そのものの記録であり、書き換えない。

---

## ゲート

- `python3 mapping/tools/verify_mapping.py` が `exit 0`
- `check_intro_note_present` の ERROR が0件
- `intro section split advisories` が **5件**、その5件すべての `note` に `[セクション境界]` が含まれる（機械検証）
- **594行 / `lines` 全行 12,986 / DROP除く 11,983 が不変**（`note` の追記のみのため）
- `PENDING_ZERO` 0件、`stale allowlist` 0件
- `design.md` が無変更（`git diff` で確認）
- `mapping.csv` が `_batch/*.csv` の単純連結と一致

## commit と user review

- 1-2（検査追加・RED確認）と 1-1 + 1-4 + 対応2 で最低2コミットに分ける
- commit & push → **user review**。別セッションの Claude が独立検証する。CC は **commit SHA** と実行コマンド出力を報告して `/rn:dn` で中断し、承認まで `#7` に進まない

## 禁止事項

- `design.md` を変更しない。`#6` の判断内容は確定済み
- `mapping.csv` を直接編集しない（`_batch/*.csv` を編集して再生成）
- `note` の追記以外で `dest_*` / `disposition` / `audience` / 行範囲を変更しない
- `current-0128-a` に個別追記するだけで済ませない。**検査の追加が本体**である
