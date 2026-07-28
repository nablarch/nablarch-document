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

## STEP 7: `check_intro_section_split` の追加と是正

### 実装

`ntf-doc-05d-addendum.md`の仕様どおり`check_intro_section_split`を追加した。ただし比較対象は
`(dest_page, dest_section)`のタプルではなく**`dest_section`単独**とした。理由: `steering.md` #5
Stepsの既存ルール文言は「同じ親を持つ配下セクションと同じ**dest_section**に置く」であり、
dest_pageの一致までは求めていない。実際にタプル一致で実装すると、design.md §4の記法統合方針に
基づき意図的にdest_pageを分離している正当なケース（例: current-0049・current-0079 — 導入文は
ページ固有の`使用方法`に残し、記法本体は`テストデータの書き方`ページへ送る設計）を誤ってERROR
検出してしまうことを実測で確認した（4件誤検出）。dest_section単独比較に変更したところ、
`ntf-doc-05d-addendum.md`記載の「現状（レビュー時の実測。6件）」の表（ERROR 2件・advisory 4件、
対象mapping_id・dest_section値とも完全一致）を過不足なく再現した。

Evidence（実装直後、是正前の実測）:

```
intro section split advisories: 4 (not auto-fixed)
 - input-0114 ((L1直下)): dest_section='使用方法' not among sibling dest_section values ['テストデータ']
 - current-0060 ((L1直下)): dest_section='機能概要' not among sibling dest_section values ['使用方法']
 - current-0142 ((L1直下)): dest_section='機能概要' not among sibling dest_section values ['使用方法']
 - current-0148 ((L1直下)): dest_section='機能概要' not among sibling dest_section values ['使用方法']

2 error(s):
 - current-0150 ((L2直下)): dest_section='機能概要' not among sibling dest_section values ['使用方法', '拡張例']
 - current-0269 ((L2直下)): dest_section='機能概要' not among sibling dest_section values ['使用方法']
EXIT: 1
```

`ntf-doc-05d-addendum.md`の実測表と対象・値とも一致（ERROR: current-0150/current-0269、
advisory: input-0114/current-0060/current-0142/current-0148）。

### ERROR 2件の是正

`git show c24190607fef5d76c607aa08b36d2ab2f813efe5:<src_file>`で当該セクションと同階層セクションを
全文通読して判定した。`dest_page`/`disposition`/`audience`は変更していない（`git diff`で
`dest_section`と`note`のみが変わっていることを確認済み）。

**current-0269**（`JUnit5_Extension.rst` 101-144行、「Extension クラスと合成アノテーションの一覧」
のL2直下）: 同階層行はcurrent-0270（`BasicHttpRequestTestの使い方の補足`、147-168行）1件のみで、
dest_section=`使用方法`。addendumの指示どおり「1つに定まる場合はそれに合わせる」を適用し、
`機能概要`→`使用方法`に変更した。

**current-0150**（`rest.rst` 40-43行、「Cookieなど前のレスポンスの情報を引き継ぐ方法」のL2直下）:
同階層行はcurrent-0151（`RequestResponseProcessorの実装クラスを作成する`、46-65行、`拡張例`）と
current-0152（`コンポーネント設定ファイルに...実装クラスを設定する`、68-95行、`使用方法`）の2件。
本文（rest.rst 39-40行）「先行するリクエストのレスポンスとしてサーバから受け取った値を次の
リクエストに含めたい場合がある。そのような場合は以下の方法で実現できる。」は機能の必要性を
述べる前提説明であり、technical howto手順そのものではない。current-0151の`拡張例`分類は
その内容が「独自インタフェース実装クラスを作成する拡張方法」（design.md#4記載範囲表の
「拡張方法」）という技術手順に限定されるためで、前提説明の性質はそれよりも、機能への入口となる
操作手順一般を扱う`使用方法`に近い。よって`機能概要`→`使用方法`に変更した。

是正後の再実行（Evidence）:

```
$ python3 mapping/tools/verify_mapping.py
Loaded 593 rows from mapping.csv
...
intro section split advisories: 4 (not auto-fixed)
 - input-0114 ((L1直下)): dest_section='使用方法' not among sibling dest_section values ['テストデータ']
 - current-0060 ((L1直下)): dest_section='機能概要' not among sibling dest_section values ['使用方法']
 - current-0142 ((L1直下)): dest_section='機能概要' not among sibling dest_section values ['使用方法']
 - current-0148 ((L1直下)): dest_section='機能概要' not among sibling dest_section values ['使用方法']

OK: no errors
EXIT: 0
```

ERROR 0件、`intro section split`のERROR分は解消。是正の副作用として`取引単体テストの設定
（RESTfulウェブサービス） > 機能概要`セクションがcurrent-0150の移動により0件になり
`check_unused_vocabulary`のERRORとして新たに検出されたため、`PENDING_ZERO`に登録した
（他のHTTP/MOM設定ページの機能概要/拡張例と同型、`#6`未確定事項#2の確定と合わせて判断）。

`lines`合計は不変（12,986 / DROP除く 11,983、593行）。`dest_section`以外のフィールドは無変更
（`git diff`で確認）。

### advisory 4件のnote追記

`ntf-doc-05d-addendum.md`のテンプレートどおり、マッピングは変更せず`note`末尾に
`[セクション境界]`を追記した（既存noteは削除していない）。

| mapping_id | 後続の本体行 | dest_section |
|---|---|---|
| input-0114 | input-0116 | テストデータ |
| current-0060 | current-0061, current-0062, current-0063 | 使用方法 |
| current-0142 | current-0143, current-0144, current-0145 | 使用方法（addendum記載の具体例と一致） |
| current-0148 | current-0149 | 使用方法 |

### commit

STEP7はSTEP6と同一コミットにせず、STEP7単独でcommitする（`ntf-doc-05d-addendum.md`の
指示「commit」に従う）。
