# self-check: #5d 記録の整合とセクション境界の是正

## STEP 1〜5: 記録の整合

### `split-plan.md`への`input-0016`/`input-0030`追記

`mapping.csv`には`input-0016-a/-b`・`input-0030-a/-b`として分割済みで反映されていたが、
`split-plan.md`「`#5c`差し戻し対応での追加分割」節への記載が漏れていた（`input-0198`のみ
記載され、「`disposition`はinput-0016/input-0030の先例に倣い」と本文中で参照されているにも
かかわらず、その2件自体の行が表になかった）。

対応: `split-plan.md`に`input-0016`・`input-0030`の行を追加し、冒頭の対象定義を「3件・計75行」に
更新した。`parts`の行範囲は`mapping.csv`の実測値と完全一致することを機械検証済み（Evidence参照）。

Evidence:

```
$ python3 -c "
import csv
with open('mapping/mapping.csv') as f:
    rows = list(csv.DictReader(f))
for sid in ['input-0016','input-0030']:
    print(sid, [(r['mapping_id'], r['src_body_start'], r['src_body_end']) for r in rows if r['src_section_id']==sid])
"
input-0016 [('input-0016-a', '214', '226'), ('input-0016-b', '227', '233')]
input-0030 [('input-0030-a', '444', '462'), ('input-0030-b', '463', '472')]
```

`split-plan.md`記載の`parts`（214-226/227-233、444-462/463-472）と一致。
`sections-input.csv`の`body_start_line`/`body_end_line`（input-0016: 214-233、input-0030: 444-472）とも
一致し、隙間・重複ゼロ。

### `checks/task-05.md`の「暫定扱い一覧」節

`mapping.csv`の`note`が「暫定」で始まる行を機械抽出し27件（グループ1〜6）として表にした。

Evidence:

```
$ python3 -c "
import csv
with open('mapping/mapping.csv') as f:
    rows = list(csv.DictReader(f))
prov = [r for r in rows if r['note'].startswith('暫定')]
print(len(prov))
"
27
```

一覧表とのつき合わせ（全27件が表に存在することを機械検証）:

```
missing from table: []
```

### `HTMLチェックツール`8行の受け皿問題解消の明記

`checks/task-05.md`の暫定一覧グループ6に、design.md第4部「ツール」新設により受け皿問題が
解消済みであり、`#6`では`note`冒頭の「暫定。」除去のみで済む旨を明記した
（`dest_page`/`dest_section`の変更は不要）。

### `design.md` §12 未確定事項#3 の確定時期のズレ

`design.md` §12は次のとおり定める。

| # | 事項 | 確定時期 |
|---|---|---|
| 3 | ファイル名・ディレクトリ構成 | マッピング作成時に決定。連番（`01_`, `02_`）は使用しない |

しかし`#5`（マッピングリストの作成、`#5b`・`#5c`を含め完了済み）の成果物である
`mapping.csv`は`dest_part`/`dest_page`/`dest_section`という論理的な章構成のみを列として持ち、
実ファイル名・ディレクトリパスの列は存在しない（`mapping_id,src_section_id,src_type,src_file,
src_body_start,src_body_end,heading_path,lines,audience,dest_part,dest_page,dest_section,
disposition,note` — Evidence: `head -1 mapping/mapping.csv`）。したがって「マッピング作成時に決定」
としていた確定時期は実際には到来しておらず、ファイル名・ディレクトリ構成は依然未確定のまま
`#6`（未確定事項の確定と design.md 更新）に持ち越されている。

`design.md`は変更しない（本追記は申し送りの記録のみ。`git diff design.md`で無変更を確認）。
`#6`のタスクでファイル名・ディレクトリ構成も合わせて確定させる必要がある。

### commit

STEP1〜5はSTEP6〜8と別コミットとする（`ntf-doc-05d-addendum.md`の指示どおり）。

## STEP 6: `check_reference_only_sections` の追加

`mapping/tools/verify_mapping.py`に`check_reference_only_sections`を追加した。仕様は
`ntf-doc-05d-addendum.md`「STEP 6」のとおり: `CONTENT_BEARING = {"MOVE", "MERGE", "SPLIT"}`
を定義し、`mapping.csv`が使う全`(dest_part, dest_page, dest_section)`のうち`CONTENT_BEARING`の
行が1件も無いものを列挙する（advisory出力、`exit 1`しない）。`check_duplicate_destinations`と
同じ位置づけで`main()`から呼び出す。

`#6`のSteps・Completion criteriaへの引き継ぎは、`steering.md` `#6`に既に記載済みであることを
確認した（line 466「`reference-only sections`の全件について...判断し`checks/task-06.md`に記録する」、
line 479「`reference-only sections`の全件に判断が記録されている（0件にする必要はない）」）。

Evidence（レビュー時の実測と一致することを確認）:

```
$ python3 mapping/tools/verify_mapping.py
...
reference-only sections: 2 (advisory only, not auto-fixed)
 - [第3部 テストの実装方法 > リクエスト単体テスト（HTTPメッセージング） > 機能概要]: 2 row(s), all non content-bearing
 - [第3部 テストの実装方法 > 取引単体テスト（HTTPメッセージング） > 機能概要]: 1 row(s), all non content-bearing
...
OK: no errors
EXIT: 0
```

`ntf-doc-05d-addendum.md`記載の実測値（current-0064/0069→リクエスト単体テスト（HTTPメッセージング）
機能概要2行、current-0138→取引単体テスト（HTTPメッセージング）機能概要1行）と件数・宛先が一致。
この2件は`#5b` STEP 2で`使用方法`→`機能概要`に変更した行であり、**本STEPでは再変更しない**
（追補の指示どおり）。判断は`#6`で行う。
