# `#6` レビュー指摘対応（`ntf-doc-06-followup.md`）self-check

判定: `#6` は承認。差し戻しではなく、レビューで見つかった小さな漏れ2件の対応。
詳細な作業指示は `.rn/20260724-ntf-yaml-support/ntf-doc-06-followup.md` を参照。

## 対応1: `[セクション境界]` note を advisory 全件に持たせる

### 1-2: `check_intro_note_present` 追加・RED確認

`mapping/tools/verify_mapping.py` に `check_intro_note_present(rows, intro_advisories)` を追加した。
`check_intro_section_split` の advisory を `{"msg": ..., "mapping_id": ...}` の辞書リストに変更し、
`main()` 側で `mapping_id` から該当行の `note` を引いて `[セクション境界]` の有無を判定する
（advisory が将来増減しても件数に依存せず自動検出される）。

先に検査を追加した状態（`current-0128-a` の `note` 未追記）で実行し、RED を確認した。

```
$ python3 mapping/tools/verify_mapping.py
...
intro section split advisories: 5 (not auto-fixed)
 - input-0114 ((L1直下)): dest_section='機能概要' not among sibling dest_section values ['テストデータ']
 - current-0060 ((L1直下)): dest_section='機能概要' not among sibling dest_section values ['使用方法']
 - current-0128-a ((L1直下)): dest_section='機能概要' not among sibling dest_section values ['使用方法']
 - current-0142 ((L1直下)): dest_section='機能概要' not among sibling dest_section values ['使用方法']
 - current-0148 ((L1直下)): dest_section='機能概要' not among sibling dest_section values ['使用方法']
...
1 error(s):
 - current-0128-a: intro section split advisory is missing a '[セクション境界]' note
```

`EXIT: 1`。期待通り `current-0128-a` のみが ERROR として検出された。

### 1-1: `current-0128-a` の `note` に追記

`mapping/_batch/batch-20.csv` の `current-0128-a` 行の `note` 末尾に、既存4件
（`input-0114` / `current-0060` / `current-0142` / `current-0148`）と同じ書式で追記した。

```
 [セクション境界] 本行は導入文であり、後続の本体行（current-0128-b）はdest_section=使用方法に置かれている。ページ作成時、導入文と本体の接続をページ内で再構成すること（design.md §8「出典の文面をそのまま流用しない」の範囲で対応可能）。
```

`mapping/mapping.csv` は `_batch/batch-01.csv`〜`batch-30.csv` をバッチ番号順に単純連結して再生成した
（`#6` STEP2-7 と同じ方式）。`git diff` は `current-0128-a` の `note` 1行のみ（`_batch/batch-20.csv` と
`mapping.csv` それぞれ1行差分）。

### 1-3: GREEN確認

```
$ python3 mapping/tools/verify_mapping.py
Loaded 594 rows from mapping.csv

pending zero assignments: 0 (awaiting #6 decision)
lines total (all rows): 12986
lines total (excluding DROP): 11983
...
intro section split advisories: 5 (not auto-fixed)
 - input-0114 ((L1直下)): dest_section='機能概要' not among sibling dest_section values ['テストデータ']
 - current-0060 ((L1直下)): dest_section='機能概要' not among sibling dest_section values ['使用方法']
 - current-0128-a ((L1直下)): dest_section='機能概要' not among sibling dest_section values ['使用方法']
 - current-0142 ((L1直下)): dest_section='機能概要' not among sibling dest_section values ['使用方法']
 - current-0148 ((L1直下)): dest_section='機能概要' not among sibling dest_section values ['使用方法']
...
OK: no errors
```

`EXIT: 0`。`check_intro_note_present` の ERROR 0件。advisory 5件すべてに `[セクション境界]` note が
存在することを確認した。`PENDING_ZERO` 0件・`stale allowlist` 0件（エラーなし）。
594行 / `lines` 全行 12,986 / DROP除く 11,983 は不変。

`design.md` に差分がないことを確認した。

```
$ git diff --stat -- .rn/20260724-ntf-yaml-support/design.md
(差分なし)
```

### 1-4: `#8〜` の Steps 確認

`steering.md` `#8〜` の該当行（line 519）は
「当該 `dest_page` の行に `note` の `[セクション境界]` が含まれる場合、導入文と本体の接続をページ内で
再構成する」であり、件数に依存する記述は含まれていない。修正不要と確認した。

## 対応2: `checks/task-06.md` の self-check 記述を実態に合わせる

`checks/task-06.md:906` の完了条件チェック行を以下のとおり書き換えた。

Before: `| task-06-proposal.mdが削除され、参照も残っていない | ✅ |`

After: `| task-06-proposal.mdが削除され、残る言及はすべて「削除済みの旧ファイル」と注記されている（\`checks/task-06.md\`内9件、\`steering.md\`1件） | ✅ |`

`checks/task-06.md` 内の参照件数と `steering.md` 内の参照件数を実測した。

```
$ grep -c "task-06-proposal" .rn/20260724-ntf-yaml-support/checks/task-06.md
9
$ grep -c "task-06-proposal" .rn/20260724-ntf-yaml-support/steering.md
1
$ grep -c "task-06-proposal" .rn/20260724-ntf-yaml-support/ntf-doc-06-instruction.md
4
```

`ntf-doc-06-instruction.md` 内の4件は作業指示そのものの記録のため書き換えていない。

## ゲート結果

| 項目 | 結果 |
|---|---|
| `python3 mapping/tools/verify_mapping.py` が `exit 0` | ✅ |
| `check_intro_note_present` の ERROR が0件 | ✅ |
| `intro section split advisories` が5件、全件に `[セクション境界]` note | ✅ |
| 594行 / `lines` 全行 12,986 / DROP除く 11,983 が不変 | ✅ |
| `PENDING_ZERO` 0件、`stale allowlist` 0件 | ✅ |
| `design.md` が無変更 | ✅（`git diff` で確認） |
| `mapping.csv` が `_batch/*.csv` の単純連結と一致 | ✅（594行、同方式で再生成） |
