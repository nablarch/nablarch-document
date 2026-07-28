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
