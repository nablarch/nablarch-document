# #6 設計判断案（訂正版、2026-07-28再提示）

`checks/task-06-proposal.md`（初版）への `/rn:gm` 差し戻し指摘を受けた訂正版。
①③の結論は独立検証で裏付けが取れているため変更していない。②は数値と表現を実測に
訂正し、③は未処理2件（`PENDING_ZERO` 26件の仕分けを含む）を追加提示し、④はツリー
全体と1対1対応表を再提示する。**本書はユーザー判断のための材料であり、design.md /
mapping.csv はまだ変更していない。**

---

## ① 稼動環境0件（第1部）— 訂正なし

`checks/task-05b.md`「報告項目1」のA/B/C案のうちA案採用を維持する。

- `current-0180`（`01_Abstract.rst:698-739`「依存関係の追加」、42行）+
  `current-0267`（`JUnit5_Extension.rst:37-47`「モジュール一覧」、11行）= 53行。
  第2部「JUnit 5用拡張機能」（現状475行）から除くと422行、第1部
  「テスティングフレームワークとは」（現状293行）に加えると346行になる。
- 「Java・Jakarta EEの要件」に相当する記述は current 47ファイル・input 10ファイル
  全域を次のコマンドで再検索し、0件を再確認した。

```
$ git ls-tree -r --name-only c24190607fef5d76c607aa08b36d2ab2f813efe5 \
    ja/development_tools/testing_framework/guide/development_guide | grep '\.rst$' | \
  while read f; do
    git show "c24190607fef5d76c607aa08b36d2ab2f813efe5:$f" | \
      grep -nE "Jakarta ?EE|Java ?17|Java ?SE|Java ?11|Java ?8|JDK" && echo "  ^^ in $f"
  done
（current側47ファイル: 出力なし = 0件）

$ grep -rnE "Jakarta ?EE|Java ?17|Java ?SE|Java ?11|Java ?8|JDK" input/*.md
input/testdata-converter-design.md:355: ...（YAML対応の過去バージョン展開に関する開発体制の記述、DROP・developer扱い）
```

**判断案（A案採用）**: `current-0180`/`current-0267`を第1部「稼動環境」へ移動する。
「Java・Jakarta EEの要件」は出典がないため`design.md` §2の表からこの項目を削除する。
確定はユーザー判断。承認後、`design.md`/`mapping.csv`の変更は`#6`のコミットで行う。

---

## ② テストデータの形式0件（第2部）— 数値と表現を訂正

### 訂正1: YAML言及行の集計

初版（`checks/task-06-proposal.md`）の「194行のうち140行は第3部、11行は第4部」は
再現しない。実測は以下のとおり。**2種類の抽出方法を独立に試し、一方に方法論上の欠陥を
発見したため、両方を併記する。**

#### 方法A: `heading_path` / `src_file` / `note` のいずれかに `yaml`（大小無視）を含む行

```
$ python3 - <<'EOF'
import csv, re
from collections import defaultdict
with open('mapping/mapping.csv') as f:
    rows = list(csv.DictReader(f))
def has_yaml(row, fields):
    return any(re.search(r'yaml', row.get(f) or '', re.IGNORECASE) for f in fields)
matched = [r for r in rows if has_yaml(r, ['heading_path','note','src_file'])]
print('matched rows:', len(matched))
agg = defaultdict(int)
for r in matched:
    key = r['disposition'] if r['disposition']=='DROP' else (r['dest_part'], r['dest_page'])
    agg[key] += 1
for k,v in sorted(agg.items(), key=lambda x:-x[1]):
    print(' ', k, v)
EOF
```

出力:

```
matched rows: 206
  ('第3部 テストの実装方法', 'テストデータの書き方') 75
  ('第3部 テストの実装方法', 'テストデータの記載例') 64
  DROP 52
  ('第4部 ツール', 'テストデータ変換ツール') 6   （lines合計75）
  ('第1部 テスティングフレームワークとは', 'テスティングフレームワークとは') 3
  ('第3部 テストの実装方法', 'リクエスト単体テスト（ウェブアプリケーション）') 2
  ('第3部 テストの実装方法', 'リクエスト単体テスト（MOMによるメッセージング）') 2
  ('第3部 テストの実装方法', 'リクエスト単体テスト（HTTPメッセージング）') 1
  ('第3部 テストの実装方法', 'リクエスト単体テスト（Nablarchバッチアプリケーション）') 1
```

合計206行・第3部139行（75+64）・第4部6行/75 lines・DROP 52行。この方法では
**指摘された数値（206/139/6・75/52）を再現できた。**

**ただしこの方法には欠陥がある。** `src_file`を条件に含めているため、input資料の
行はすべて機械的にヒットする。input資料のパスは全件
`.rn/20260724-ntf-yaml-support/input/...`であり、ディレクトリ名
`20260724-ntf-yaml-support`自体に部分文字列`yaml`を含むため、本文がYAMLに言及して
いるかどうかに関わらず**input由来の206行全件が無条件で一致する**。実際に検証すると、

```
$ python3 - <<'EOF'
import csv, re
with open('mapping/mapping.csv') as f:
    rows = list(csv.DictReader(f))
input_rows = [r for r in rows if r['src_type']=='input']
def has_yaml(row, fields):
    return any(re.search(r'yaml', row.get(f) or '', re.IGNORECASE) for f in fields)
matched = [r for r in rows if has_yaml(r, ['heading_path','note','src_file'])]
print('input総行数:', len(input_rows))
print('方法Aで一致した行数:', len(matched))
print('一致行のうちcurrent由来:', len([r for r in matched if r['src_type']=='current']))
EOF
```

```
input総行数: 206
方法Aで一致した行数: 206
一致行のうちcurrent由来: 0
```

**方法Aの「206」は「input資料の全行数（206）」と数学的に同一であり、current側
（現行47rst）からは1行も拾えていない。** 「YAMLに言及する行」という指標としては
成立しない。指摘された数値は再現できたが、再現できた理由がディレクトリ名の偶然の
部分一致であるため、この方法は採用しない。

#### 方法B: 実際の本文（`src_body_start`〜`src_body_end`の実テキスト）に`yaml`を含むか

出典の実ファイル（current側は`git show <base>:<path>`、input側は作業ツリー）を取得し、
各マッピング行の行範囲の本文そのものを検索する。メタデータではなく内容を見る。

```
$ python3 - <<'EOF'
import csv, re, subprocess
from collections import defaultdict
BASE = 'c24190607fef5d76c607aa08b36d2ab2f813efe5'
with open('mapping/mapping.csv') as f:
    rows = list(csv.DictReader(f))
cache = {}
def get_lines(src_type, src_file):
    key = (src_type, src_file)
    if key in cache: return cache[key]
    if src_type == 'current':
        out = subprocess.run(['git','show', f'{BASE}:{src_file}'], capture_output=True, text=True)
        lines = out.stdout.splitlines()
    else:
        with open(src_file, encoding='utf-8') as fh:
            lines = fh.read().splitlines()
    cache[key] = lines
    return lines
matched = []
for r in rows:
    start, end = int(r['src_body_start']), int(r['src_body_end'])
    lines = get_lines(r['src_type'], r['src_file'])
    body = '\n'.join(lines[start-1:end])
    if re.search(r'yaml', body, re.IGNORECASE):
        matched.append(r)
print('matched rows:', len(matched))
agg = defaultdict(int)
for r in matched:
    key = r['disposition'] if r['disposition']=='DROP' else (r['dest_part'], r['dest_page'])
    agg[key] += 1
for k,v in sorted(agg.items(), key=lambda x:-x[1]):
    print(' ', k, v)
EOF
```

出力:

```
matched rows: 90
  ('第3部 テストの実装方法', 'テストデータの記載例') 35   （499行）
  ('第3部 テストの実装方法', 'テストデータの書き方') 32   （1052行）
  DROP 16   （234行）
  ('第4部 ツール', 'テストデータ変換ツール') 6   （75行）
  ('第1部 テスティングフレームワークとは', 'テスティングフレームワークとは') 1   （26行）
```

本文検索では90行（第3部合計67行・1551行分、第4部6行/75行、DROP16行、第1部1行）。
**第4部「テストデータ変換ツール」の6行/75行だけは、方法A・方法Bのどちらでも一致した
（このページの全行が実際にYAMLに言及している）。** それ以外の数値は方法によって
大きく変わる。

**この節の実質的な結論は、どちらの集計方法でも変わらない。** 第2部「テストデータの
形式」への割当が0行であることは、YAML言及行の集計とは独立に、`mapping.csv`の
`dest_page`列を直接集計することで確認できる事実であり（`mapping/volume.md`参照、
`verify_mapping.py`の`PENDING_ZERO`にも登録済み）、YAML抽出条件の選び方に依存しない。
**訂正すべきは「194行」という数値そのものであり、廃止判断の根拠ではない。**

`checks/task-06.md`（本書）には方法Bの数値（90行/1886行）を実測値として記載し、
方法Aは「指摘値を再現したが方法論上不成立」として参考記載にとどめる。

### 訂正2: 「第3部冒頭に統合する」という表現

実測では、Excel/YAMLの**比較**に相当する内容は既に第3部「テストデータの書き方」に
ある。移す作業は発生しない。

```
$ python3 -c "
import csv
with open('mapping/mapping.csv') as f:
    rows = {r['mapping_id']: r for r in csv.DictReader(f)}
for mid in ['input-0148','input-0117']:
    r = rows[mid]
    print(mid, '->', r['dest_part'], '|', r['dest_page'], '|', r['dest_section'], '| lines=', r['lines'])
"
input-0148 -> 第3部 テストの実装方法 | テストデータの書き方 | 使用方法 | lines= 23
input-0117 -> 第3部 テストの実装方法 | テストデータの書き方 | 使用方法 | lines= 32
```

- `input-0148`「8. 値の書き方 > 8.1 値の種類と Excel / YAML 対比」23行 →
  既に第3部 テストデータの書き方 > 使用方法（`MERGE`済み）
- `input-0117`「2. テストデータの基本構造 > (L2直下)」32行 → 同上

一方、**「使い分け」（どちらの形式を選ぶかの判断指針）に相当する出典は見つからな
かった。** `使い分け`という語で`mapping.csv`の`heading_path`/`note`を検索すると
5件ヒットするが、いずれもgroupIdによるテストケースの使い分けであり、Excel/YAML
形式の選択指針とは無関係。

```
$ python3 -c "
import csv
with open('mapping/mapping.csv') as f:
    rows = list(csv.DictReader(f))
for r in rows:
    if '使い分け' in (r['heading_path'] or '') or '使い分け' in (r['note'] or ''):
        print(r['mapping_id'], '|', r['dest_page'], '|', r['note'][:50])
"
input-0124   | テストデータの書き方   | 複数テストケースで異なるセットアップ・期待値を使い分けるgroupIdの仕組み...
current-0134 | 取引単体テスト（Nablarchバッチアプリケーション） | 通常のケースと入力データが0件のケースの2テス...
current-0072 | テストデータの書き方   | testShotsのexpectedMessageByClientおよびresponseMessageByClientに...
input-0044   | テストデータの記載例   | テストケースごとに異なる入力ファイルを使い分けるケース...
input-0079   | テストデータの記載例   | テストケースごとに異なるセットアップ／検証データを使い分けるシナリオ...
```

近いのは`input-0184`「基準は『形式』ではなく NTF 仕様上の意味」17行だが、
`第4部 ツール > テストデータ変換ツール > 機能概要`に割当済み（下記）で、これは
変換ツールの設計思想であり、利用者が「Excelで書くかYAMLで書くか」を選ぶ指針では
ない。

```
input-0184 -> 第4部 ツール | テストデータ変換ツール | 機能概要 | lines= 17
```

記述を次のように直す。

- **Before**: 「Excel/YAML比較・使い分けの説明は…第3部『テストデータの書き方』
  冒頭に統合する（新規文章の追加ではなく既存マッピング内容の再配置）」
- **After**: 「比較に相当する内容（`input-0148`/`input-0117`）は既に第3部
  テストデータの書き方にあり、移動は発生しない。『使い分け』に相当する出典は
  存在しないため記述しない（『マッピングにない内容を追加しない』に従う）」

`dest_page`の再配置が発生しないため、`mapping.csv`の変更は発生しない。作業計画
から外す。

**②の結論（ページ廃止、design.md §3の表から削除）は変更なし。**

---

## ③ ページ分割・取引単体テストの構成 — 訂正なし。未処理2件を提示

### 裏付け（再確認）

```
$ git ls-tree -r --name-only c24190607fef5d76c607aa08b36d2ab2f813efe5 \
    ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/
```

`RequestUnitTest_batch.rst` / `RequestUnitTest_http_send_sync.rst` /
`RequestUnitTest_real.rst` / `RequestUnitTest_rest.rst` /
`RequestUnitTest_send_sync.rst` の5ファイルが存在する。同様に
`05_UnitTestGuide/03_DealUnitTest/`配下を確認すると`batch.rst` / `http_send_sync.rst`
/ `real.rst` / `rest.rst` / `send_sync.rst` / `delayed_send.rst` / `delayed_receive.rst`
はあるが、`DealUnitTest_`という接頭辞を持つファイルは1件も存在しない
（`grep -i DealUnitTest`が`03_DealUnitTest/`というディレクトリ名にのみ一致し、
ファイル名としては0件）。

取引単体テストの設定の実データは`volume.md`のとおり MOM 104行 / RESTfulウェブ
サービス 52行 / HTTPメッセージング 20行。ウェブアプリケーション・
Nablarchバッチアプリケーションは0行（マッピング漏れではなく実体の不在、
`checks/task-05b.md`で実ファイル通読済み）。

**判断案（変更なし）**:
- リクエスト単体テストの設定: design.md暫定構成どおり6処理方式に分割する
- 取引単体テストの設定: 実データがある3処理方式のみページ化する
  （MOMによるメッセージング／RESTfulウェブサービス／HTTPメッセージング）。
  ウェブアプリケーション・Nablarchバッチアプリケーション・テーブルをキューとして
  使ったメッセージングはページを設けない

### 未処理1: `取引単体テストの設定（RESTfulウェブサービス）> 機能概要` が0件

**発生経緯**: `#5d` STEP 7 で`current-0150`（`(L2直下)`導入文）を
`check_intro_section_split`のERROR是正により`機能概要`→`使用方法`へ変更した結果、
本セクションが0件になった（`checks/task-05d.md`参照）。

```
$ python3 -c "
import csv
with open('mapping/mapping.csv') as f:
    rows = list(csv.DictReader(f))
for r in rows:
    if r['dest_page']=='取引単体テストの設定（RESTfulウェブサービス）':
        print(r['mapping_id'], r['dest_section'], r['lines'])
"
current-0150 使用方法 4
current-0151 拡張例  20
current-0152 使用方法 28
```

ページ合計52行のうち`拡張例`は20行あり0件ではない。0件なのは`機能概要`のみ。
このページを作る方針（③・変更なし）である以上、`#6`で明示的に決める必要がある。

**この論点は単独ではなく、第2部の設定ページ全体に及ぶ構造的な論点である。**
`機能概要`が0件のページは、このRESTful取引単体テスト設定を含めて**10ページ**、
`拡張例`が0件のページは**8ページ**ある（次表、`verify_mapping.py`の
`PENDING_ZERO`出力より）。

| dest_page | 機能概要0件 | 拡張例0件 |
|---|---|---|
| 共通設定 | ○ | ○ |
| クラス単体テストの設定 | ○ | ○ |
| マスタデータ復旧機能 | | ○ |
| リクエスト単体テストの設定（ウェブアプリケーション） | ○ | |
| リクエスト単体テストの設定（RESTfulウェブサービス） | ○ | ○ |
| リクエスト単体テストの設定（HTTPメッセージング） | ○ | ○ |
| リクエスト単体テストの設定（Nablarchバッチアプリケーション） | ○ | ○ |
| リクエスト単体テストの設定（MOMによるメッセージング） | ○ | |
| 取引単体テストの設定（RESTfulウェブサービス） | ○ | |
| 取引単体テストの設定（HTTPメッセージング） | ○ | ○ |
| 取引単体テストの設定（MOMによるメッセージング） | ○ | ○ |
| **合計** | **10ページ** | **8ページ** |

選択肢（判断はユーザー）:

| 案 | 内容 |
|---|---|
| a | `HTMLチェックツール > 導入`と同じ扱いで、この10ページ・8ページを個別に
      `EXPECTED_ZERO_SECTIONS`へ移し、「機能概要（または拡張例）を持たない
      ページ」として1件ずつ確定する |
| b | 第2部のページには`機能概要`・`拡張例`を必須としないよう`design.md` §3の
      ページアウトラインを改訂する（設定量が薄い処理方式別ページで
      機能概要・拡張例が構造的に欠落しやすいことを踏まえ、テンプレート自体を
      見直す） |

a案は個別ページごとの例外として記録し続けるコストが10+8=18件分発生する。b案は
`design.md`の改訂を伴うが、以後同種のページが増えても再度PENDING_ZEROとして
扱わずに済む。**いずれもdesign.md §3への影響があるため、ユーザー判断が必要。**

### 未処理2: 第3部 取引単体テストの小規模ページ

`#6`未確定事項#2は「文量集計で確定する」としているが、`checks/task-06-proposal.md`
の提示は第2部だけを扱っていた。第3部 取引単体テストの文量（`volume.md`より）:

| ページ | 行数 |
|---|---:|
| 取引単体テスト（MOMによるメッセージング） | 175 |
| 取引単体テスト（Nablarchバッチアプリケーション） | 168 |
| 取引単体テスト（ウェブアプリケーション） | 48 |
| 取引単体テスト（HTTPメッセージング） | 33 |
| 取引単体テスト（RESTfulウェブサービス） | 32 |
| 取引単体テスト（テーブルをキューとして使ったメッセージング） | 0（EXPECTED_ZERO、design.md §6「中身は導線のみ」） |

第2部の取引単体テストの設定とは異なり、**この5ページはいずれも実データが存在する**
（0行のページはdb_queueのみで、これはdesign.md §6が最初から「導線のみ」と
定義している）。したがって「実体のある処理方式のみページ化する」という③と同じ
基準を単純適用しても、5ページとも残る。`volume.md`「傾向」節が指摘するとおり、
実際の論点は**HTTPメッセージング（33行）・RESTfulウェブサービス（32行）・
ウェブアプリケーション（48行）という小規模ページを、他ページに統合するかどうか**
である。

選択肢（判断はユーザー）:

| 案 | 内容 |
|---|---|
| A | 第2部と対称に6処理方式（db_queueの導線ページを含む）をすべて独立ページとして
      揃える。処理方式間の文量差（32〜175行）はそのまま許容する |
| B | 実体で判断し、小規模な3ページ（HTTPメッセージング33行・RESTfulウェブ
      サービス32行・ウェブアプリケーション48行）を統合または他ページへの
      `:ref:`参照に置き換える。統合先・統合単位は改めて検討する |

### `PENDING_ZERO` 26件の仕分け

`#6`のCompletion criteriaは「`PENDING_ZERO`が0件」。26件全件の行き先を次のとおり
仕分ける。

#### 分類1: ①の判断（承認されれば解消） — 1件

| # | 対象 |
|---|---|
| 1 | section [第1部 テスティングフレームワークとは > テスティングフレームワークとは > 稼動環境] |

#### 分類2: ②の判断（承認されれば解消。ページ自体が構成から消える） — 1件

| # | 対象 |
|---|---|
| 2 | page [第2部 導入と設定 > テストデータの形式] |

#### 分類3: ③の判断（承認されれば解消。ページ自体が構成から消える） — 2件

| # | 対象 |
|---|---|
| 3 | page [第2部 導入と設定 > 取引単体テストの設定（ウェブアプリケーション）] |
| 4 | page [第2部 導入と設定 > 取引単体テストの設定（Nablarchバッチアプリケーション）] |

#### 分類4: 未処理1の判断が必要（第2部設定ページの機能概要0件） — 10件

| # | 対象 |
|---|---|
| 5 | section [共通設定 > 機能概要] |
| 6 | section [クラス単体テストの設定 > 機能概要] |
| 7 | section [リクエスト単体テストの設定（ウェブアプリケーション） > 機能概要] |
| 8 | section [リクエスト単体テストの設定（RESTfulウェブサービス） > 機能概要] |
| 9 | section [リクエスト単体テストの設定（HTTPメッセージング） > 機能概要] |
| 10 | section [リクエスト単体テストの設定（Nablarchバッチアプリケーション） > 機能概要] |
| 11 | section [リクエスト単体テストの設定（MOMによるメッセージング） > 機能概要] |
| 12 | section [取引単体テストの設定（RESTfulウェブサービス） > 機能概要]（未処理1本体） |
| 13 | section [取引単体テストの設定（HTTPメッセージング） > 機能概要] |
| 14 | section [取引単体テストの設定（MOMによるメッセージング） > 機能概要] |

#### 分類5: 未処理1と同一論点（第2部設定ページの拡張例0件） — 8件

| # | 対象 |
|---|---|
| 15 | section [共通設定 > 拡張例] |
| 16 | section [クラス単体テストの設定 > 拡張例] |
| 17 | section [マスタデータ復旧機能 > 拡張例] |
| 18 | section [リクエスト単体テストの設定（RESTfulウェブサービス） > 拡張例] |
| 19 | section [リクエスト単体テストの設定（HTTPメッセージング） > 拡張例] |
| 20 | section [リクエスト単体テストの設定（Nablarchバッチアプリケーション） > 拡張例] |
| 21 | section [取引単体テストの設定（HTTPメッセージング） > 拡張例] |
| 22 | section [取引単体テストの設定（MOMによるメッセージング） > 拡張例] |

分類4・5は同じ選択肢（a/b、前掲）で一括判断できる。

#### 分類6: 新規論点（第3部テストデータ2ページの機能概要の要否） — 2件

| # | 対象 | 候補となる出典 |
|---|---|---|
| 23 | section [テストデータの書き方 > 機能概要] | input-0098/0099/0114（各資料の冒頭導入文・全体像節） |
| 24 | section [テストデータの記載例 > 機能概要] | input-0036/0037/0058/0082/0093（各記述例文書の冒頭導入文） |

design.md §4「テストデータの2ページ」はこの2ページの役割を定義しているが、
一般の第3部ページアウトライン（`機能概要`＋`使用方法`）をそのまま適用するかは
明記していない。選択肢:

| 案 | 内容 |
|---|---|
| a | 候補出典（上表）を`機能概要`として新たに割り当て、一般の第3部ページと
      同じ構成にする |
| b | この2ページは`機能概要`を持たない例外ページとして確定する
      （役割の説明は design.md §4 の「テストデータの2ページ」表に譲る） |

#### 分類7: 新規論点（`取引単体テスト（Nablarchバッチアプリケーション）> 機能概要`の分割要否） — 1件

| # | 対象 | 実測 |
|---|---|---|
| 25 | section [取引単体テスト（Nablarchバッチアプリケーション） > 機能概要] | `current-0128`（`batch.rst:4-25`、`(L1直下)`）は冒頭2行のみ概要的記述で、残り（8-24行）はテストクラス作成条件・命名規則・コード例という使用方法の内容が同一セクションに混在する |

`#4a`/`#5`の対象外である新規`SPLIT`を今回の判断だけで追加してよいかが論点。
選択肢:

| 案 | 内容 |
|---|---|
| a | `current-0128`を新規`SPLIT`対象とし、冒頭2行を`機能概要`、残りを`使用方法`
      に分割する |
| b | 分割せず、このページを`機能概要`なしのページとして確定する |

#### 分類8: 新規論点（`テストデータ変換ツール > 導入`の要否の明文化） — 1件

| # | 対象 | 実測 |
|---|---|---|
| 26 | section [テストデータ変換ツール > 導入] | `testdata-converter-design.md`全362行を通読したが、インストール手順・依存関係・設定に該当する記述は存在しない。候補`input-0183/0184/0190`は「解くべき課題」「形式に依存するか否か」という設計思想の説明で`機能概要`が正しい割当 |

design.md §5は`HTMLチェックツール`のみ「導入」省略を明記しており、
`テストデータ変換ツール`への同様の言及はない。選択肢:

| 案 | 内容 |
|---|---|
| a | `HTMLチェックツール`と同様の例外として`EXPECTED_ZERO_SECTIONS`に追加する |
| b | design.md §5に`テストデータ変換ツール`も「導入」を持たない旨を明記する |

#### 仕分けの集計

分類1(1) + 分類2(1) + 分類3(2) + 分類4(10) + 分類5(8) + 分類6(2) + 分類7(1) +
分類8(1) = **26件**。`verify_mapping.py`の`PENDING_ZERO`件数と一致する。

---

## ④ ファイル名・ディレクトリ構成 — ツリー全体と1対1対応表を再提示

前回提示（`checks/task-06-proposal.md`）は`{a,b,c}.rst`のような省略記法を含み、
ユーザーが受領した表示では一部が欠落・未読了だった。今回は省略記法を使わず、
`vocabulary.md`の全38ページ（確定9＋暫定29）を1行ずつファイルパスに対応付ける。

### ツリー全体

```
ja/development_tools/testing_framework/
├── index.rst
├── about/
│   └── index.rst                      第1部（1ページ）
├── setup/                             第2部
│   ├── common.rst
│   ├── class_unit_test.rst
│   ├── junit5_extension.rst
│   ├── master_data_restore.rst
│   ├── request_unit_test/
│   │   ├── web.rst
│   │   ├── rest.rst
│   │   ├── http_messaging.rst
│   │   ├── batch.rst
│   │   ├── mom.rst
│   │   └── db_queue.rst
│   └── deal_unit_test/
│       ├── rest.rst
│       ├── http_messaging.rst
│       └── mom.rst                    （web/batch/db_queueはページを作らない＝③）
├── implementation/                    第3部
│   ├── testdata_format.rst
│   ├── testdata_examples.rst
│   ├── class_unit_test/
│   │   ├── entity.rst
│   │   └── component.rst
│   ├── request_unit_test/
│   │   ├── web.rst
│   │   ├── rest.rst
│   │   ├── http_messaging.rst
│   │   ├── batch.rst
│   │   ├── mom.rst
│   │   └── db_queue.rst
│   └── deal_unit_test/                未処理2の確定待ち（下表参照）
│       ├── web.rst
│       ├── rest.rst
│       ├── http_messaging.rst
│       ├── batch.rst
│       ├── mom.rst
│       └── db_queue.rst
└── tools/                             第4部
    ├── request_data_tool.rst
    ├── testdata_converter.rst
    ├── master_data_tool.rst
    └── html_check_tool.rst
```

命名規則の根拠: FW解説書ライブラリ（`ja/application_framework/application_framework/
libraries/`）が英語snake_case・連番なしであることを確認済み（`bean_util.rst`、
`db_double_submit.rst`、`file_path_management.rst`等）。

### 1対1対応表（`dest_part` / `dest_page` / ファイルパス / 行数）

`vocabulary.md`の全38ページを母集合とする。行数は`volume.md`（DROP除く、①未承認
時点の現状値）。「備考」に廃止・統合・確定待ちを明記する。

#### 第1部（確定・1件）

| dest_page | ファイルパス | 行数 | 備考 |
|---|---|---:|---|
| テスティングフレームワークとは | `about/index.rst` | 293 | ①承認後346（+53） |

#### 第2部（確定なし。5＋12＝17件、うち3件は廃止提案）

| dest_page | ファイルパス | 行数 | 備考 |
|---|---|---:|---|
| 共通設定 | `setup/common.rst` | 129 | |
| クラス単体テストの設定 | `setup/class_unit_test.rst` | 193 | |
| テストデータの形式 | （ファイルなし） | 0 | ②で廃止提案 |
| JUnit 5用拡張機能 | `setup/junit5_extension.rst` | 475 | ①承認後422（-53） |
| マスタデータ復旧機能 | `setup/master_data_restore.rst` | 193 | |
| リクエスト単体テストの設定（ウェブアプリケーション） | `setup/request_unit_test/web.rst` | 250 | |
| リクエスト単体テストの設定（RESTfulウェブサービス） | `setup/request_unit_test/rest.rst` | 125 | |
| リクエスト単体テストの設定（HTTPメッセージング） | `setup/request_unit_test/http_messaging.rst` | 30 | |
| リクエスト単体テストの設定（Nablarchバッチアプリケーション） | `setup/request_unit_test/batch.rst` | 129 | |
| リクエスト単体テストの設定（MOMによるメッセージング） | `setup/request_unit_test/mom.rst` | 76 | |
| リクエスト単体テストの設定（テーブルをキューとして使ったメッセージング） | `setup/request_unit_test/db_queue.rst` | 0 | EXPECTED_ZERO（design.md §6「導線のみ」） |
| 取引単体テストの設定（ウェブアプリケーション） | （ファイルなし） | 0 | ③で廃止提案 |
| 取引単体テストの設定（RESTfulウェブサービス） | `setup/deal_unit_test/rest.rst` | 52 | 機能概要0件（未処理1） |
| 取引単体テストの設定（HTTPメッセージング） | `setup/deal_unit_test/http_messaging.rst` | 20 | 機能概要・拡張例0件 |
| 取引単体テストの設定（Nablarchバッチアプリケーション） | （ファイルなし） | 0 | ③で廃止提案 |
| 取引単体テストの設定（MOMによるメッセージング） | `setup/deal_unit_test/mom.rst` | 104 | 機能概要・拡張例0件 |
| 取引単体テストの設定（テーブルをキューとして使ったメッセージング） | （ファイルなし） | 0 | ③で廃止提案（design.md §6の「導線のみ」すら設けない） |

#### 第3部（確定4＋暫定12＝16件、うちdeal_unit_test 6件は未処理2の確定待ち）

| dest_page | ファイルパス | 行数 | 備考 |
|---|---|---:|---|
| テストデータの書き方 | `implementation/testdata_format.rst` | 3316 | 機能概要0件（分類6） |
| テストデータの記載例 | `implementation/testdata_examples.rst` | 1350 | 機能概要0件（分類6） |
| エンティティ単体テスト | `implementation/class_unit_test/entity.rst` | 1344 | |
| コンポーネント単体テスト | `implementation/class_unit_test/component.rst` | 770 | |
| リクエスト単体テスト（ウェブアプリケーション） | `implementation/request_unit_test/web.rst` | 914 | |
| リクエスト単体テスト（RESTfulウェブサービス） | `implementation/request_unit_test/rest.rst` | 262 | |
| リクエスト単体テスト（HTTPメッセージング） | `implementation/request_unit_test/http_messaging.rst` | 28 | reference-only advisory（機能概要2行、本文性なし） |
| リクエスト単体テスト（Nablarchバッチアプリケーション） | `implementation/request_unit_test/batch.rst` | 384 | |
| リクエスト単体テスト（MOMによるメッセージング） | `implementation/request_unit_test/mom.rst` | 461 | |
| リクエスト単体テスト（テーブルをキューとして使ったメッセージング） | `implementation/request_unit_test/db_queue.rst` | 0 | EXPECTED_ZERO（design.md §6「導線のみ」） |
| 取引単体テスト（ウェブアプリケーション） | `implementation/deal_unit_test/web.rst`（未処理2確定待ち） | 48 | 未処理2 B案なら統合対象候補 |
| 取引単体テスト（RESTfulウェブサービス） | `implementation/deal_unit_test/rest.rst`（未処理2確定待ち） | 32 | 未処理2 B案なら統合対象候補 |
| 取引単体テスト（HTTPメッセージング） | `implementation/deal_unit_test/http_messaging.rst`（未処理2確定待ち） | 33 | 未処理2 B案なら統合対象候補、reference-only advisory（機能概要1行） |
| 取引単体テスト（Nablarchバッチアプリケーション） | `implementation/deal_unit_test/batch.rst`（未処理2確定待ち） | 168 | 機能概要0件・分割要否未定（分類7） |
| 取引単体テスト（MOMによるメッセージング） | `implementation/deal_unit_test/mom.rst`（未処理2確定待ち） | 175 | |
| 取引単体テスト（テーブルをキューとして使ったメッセージング） | `implementation/deal_unit_test/db_queue.rst` | 0 | EXPECTED_ZERO（design.md §6「導線のみ」、未処理2の対象外） |

#### 第4部（確定・4件）

| dest_page | ファイルパス | 行数 | 備考 |
|---|---|---:|---|
| リクエスト単体データ作成ツール | `tools/request_data_tool.rst` | 163 | |
| テストデータ変換ツール | `tools/testdata_converter.rst` | 75 | 導入0件（分類8） |
| マスタデータ投入ツール | `tools/master_data_tool.rst` | 177 | |
| HTMLチェックツール | `tools/html_check_tool.rst` | 214 | design.md §5により導入を持たない例外として確定済み |

#### 集計確認

9（確定）＋17（第2部）＋16（第3部）＋4（第4部の再掲は第2部に含めず別カウント）
の内訳を数え直すと、確定9件は上記各表に個別に現れているため二重計上しないよう
注意する。`vocabulary.md`の母集合との対応:

- 確定9件: 第1部1・第3部4（テストデータの書き方/記載例/エンティティ単体テスト/
  コンポーネント単体テスト）・第4部4 → 上表すべてに掲載済み
- 暫定29件: 第2部5＋第2部処理方式12（リクエスト6＋取引6）＋第3部処理方式12
  （リクエスト6＋取引6）→ 上表すべてに掲載済み
- 合計 9+29 = **38件、過不足なし**

---

## 進め方

1. ①〜④について、ユーザーが承認または追加の修正指示を行う
2. 承認された範囲から`design.md`更新→`mapping.csv`更新→暫定表記解消→
   `reference-only sections`判断→self-check→commit & push→user reviewに進む

**この段階では`design.md`と`mapping.csv`を変更していない。** 判断が下りてから
着手する。
