# 作業指示: #5b / #5c / #5d — `#6` 着手前の是正

対象ブランチ: `lovaizu/nablarch-document` の `work`（PR #730 head）

基準コミット: `c241906`

## 背景

`#5` 完了後の横断点検で、機械検証できる範囲（台帳の網羅性・`mapping.csv` の整合・語彙突合）は欠陥ゼロだった。一方で、`dest_section=導入` が0件だった件と**同型の欠陥**が他にも残っていることが判明した。

根本原因は `verify_mapping.py` の `check_vocabulary` が「使われている値が語彙に含まれるか」しか見ておらず、**「語彙が定義しているのに1件も使われていない」を検出しない**こと。個別に潰すのではなく、まず検査を追加して機械的に検出できる状態を作る。

## タスクの位置づけ

`steering.md` の `#5` と `#6` の間に3タスクを挿入する。`#6` の Prerequisites を `#5` から `#5d` に変更する。

| タスク | 内容 | 想定セッション |
|---|---|---|
| `#5b` | 割当先0件問題の解消（検査の追加 → 再判定 → volume.md 補完 → 未解決分の調査報告） | 1セッション |
| `#5c` | `DROP` 全件レビュー（`design.md` §11.8 の未達分） | 1セッション（96行と重いため単独） |
| `#5d` | 記録の整合（`split-plan.md` 未更新ほか） | 1セッション |

## user review と中断のポイント

**user review は CC の自己申告ではない。** 別セッションの Claude が push 済みブランチを clone し、`_batch/*.csv`・`mapping.csv`・実ファイルを独立に突合して判定する。CC が書いた検証スクリプトや self-check の結論は使わない。

したがって各タスクの user review は**セッションの終端**である。CC は次のとおり振る舞う。

1. 成果物を commit & push する（push まで完了していないものはレビュー対象にならない）
2. 報告を出す。内容は次の3点だけでよい
   - push した commit SHA
   - 完了条件のどれをどう満たしたか（実行コマンドと出力）
   - 判断が割れた箇所・未解決のまま残した箇所
3. `/rn:dn` で中断する。**承認を待たずに次タスクへ進まない**
4. 承認後は新しいセッション（`/clear` 済み）で `/rn:up` から再開する

`#5b` は STEP 1（検査追加・RED確認）と STEP 2〜5 で最低2コミットに分けるが、**中断点は STEP 5 の user review 1箇所**とする。STEP 1 だけで中断しない（RED のまま放置しない）。

`#5b` → `#5c` → `#5d` → `#6` の各境界が `/clear` のポイントになる。

---

# `#5b`: 割当先0件問題の解消

**Purpose**: 「語彙が定義しているのに割当が0件」を機械検出できる状態にし、再判定で解消できるものを解消し、`#6` のユーザー判断が必要なものを調査報告として残す。

**Prerequisites**: `#5`

## STEP 1: 検査を追加して RED を確認する

`mapping/tools/verify_mapping.py` に `check_unused_vocabulary` を追加する。

### 仕様

`vocabulary.md` の語彙のうち、`mapping.csv` で1件も使われていない組み合わせを検出する。ただし2種類の許可リストで分類する。

| 分類 | 意味 | 判定 |
|---|---|---|
| `EXPECTED_ZERO` | `design.md` が0件になることを設計として定めている | OK（出力もしない） |
| `PENDING_ZERO` | `#6` のユーザー判断を待っている | WARN（件数と一覧を出力するが `exit 1` しない） |
| 上記以外 | 未検出の欠陥 | ERROR（`exit 1`） |

検査対象は2階層。

1. **ページ単位** — `vocabulary.md` の全 `(dest_part, dest_page)` について、`disposition != DROP` の行が1件以上あること
2. **セクション単位** — `mapping.csv` で使われている全 `(dest_part, dest_page)` について、その `dest_part` のテンプレートが定める全 `dest_section` に行が1件以上あること

テンプレートは `design.md` のページアウトラインに従う。

```python
SECTION_TEMPLATE = {
    "第1部 テスティングフレームワークとは": ["全体像", "アーキテクチャ", "テストの種類", "テストデータ", "対象範囲", "稼動環境"],
    "第2部 導入と設定": ["機能概要", "使用方法", "拡張例"],
    "第3部 テストの実装方法": ["機能概要", "使用方法"],
    "第4部 ツール": ["機能概要", "導入", "使用方法"],
}
```

### `EXPECTED_ZERO` の初期値（理由は `design.md` の該当箇所を必ず引用する）

```python
# (dest_part, dest_page) — ページ単位
EXPECTED_ZERO_PAGES = {
    ("第2部 導入と設定", "リクエスト単体テストの設定（テーブルをキューとして使ったメッセージング）"):
        "design.md §6「中身は導線のみとする」。独自の設定内容を持たない",
    ("第2部 導入と設定", "取引単体テストの設定（テーブルをキューとして使ったメッセージング）"): "同上",
    ("第3部 テストの実装方法", "リクエスト単体テスト（テーブルをキューとして使ったメッセージング）"): "同上",
    ("第3部 テストの実装方法", "取引単体テスト（テーブルをキューとして使ったメッセージング）"): "同上",
}

# (dest_part, dest_page, dest_section) — セクション単位
EXPECTED_ZERO_SECTIONS = {
    ("第4部 ツール", "HTMLチェックツール", "導入"):
        "design.md §5「インストール手順を持たないため『導入』セクションは設けず」",
}
```

`PENDING_ZERO` は空の辞書で作る。STEP 2・STEP 4 の結果を受けて追記する。

### main への組み込み

**Before**（`verify_mapping.py` `main()` 内）

```python
    if files == [MAPPING_CSV]:
        # 取りこぼし検証・vocabulary突合はmapping.csv統合後のみ意味を持つ
        # （バッチ単位では対象セクションの一部しか含まれないため）。
        errors += check_coverage(rows)
        errors += check_vocabulary(rows)
```

**After**

```python
    if files == [MAPPING_CSV]:
        # 取りこぼし検証・vocabulary突合はmapping.csv統合後のみ意味を持つ
        # （バッチ単位では対象セクションの一部しか含まれないため）。
        errors += check_coverage(rows)
        errors += check_vocabulary(rows)
        unused_errors, unused_pending = check_unused_vocabulary(rows)
        errors += unused_errors
        print(f"\npending zero assignments: {len(unused_pending)} (awaiting #6 decision)")
        for p in unused_pending:
            print(" -", p)
```

### ゲート（このSTEPを抜ける条件）

`python3 mapping/tools/verify_mapping.py` を実行し、**ERROR が出て `exit 1` すること**を確認する。この時点で GREEN になったら検査が効いていない。実行結果をそのまま `checks/task-05b.md` に貼る。

期待される検出は次の17件（点検時の実測値）。件数が違う場合は先に原因を突き止めてから STEP 2 に進む。

- ページ単位0件: 3件 — `第2部 テストデータの形式` / `第2部 取引単体テストの設定（ウェブアプリケーション）` / `第2部 取引単体テストの設定（Nablarchバッチアプリケーション）`
- セクション単位0件: 14件 — 下表のとおり

このSTEPだけで commit する（検査の追加とデータの修正を同じコミットに混ぜない）。

## STEP 2: `機能概要` / `導入` 0件を再判定する

### 対象

`dest_section` 0件のページは次の14件。第1部「稼動環境」は STEP 4 で扱う（design.md 側の判断が要るため）。

| # | dest_part | dest_page | 不足 | 該当ページの全行数 |
|---|---|---|---|---|
| 1 | 第2部 | クラス単体テストの設定 | 機能概要, 拡張例 | 3 |
| 2 | 第2部 | 共通設定 | 機能概要, 拡張例 | 5 |
| 3 | 第2部 | リクエスト単体テストの設定（ウェブアプリケーション） | 機能概要 | 6 |
| 4 | 第2部 | リクエスト単体テストの設定（RESTfulウェブサービス） | 機能概要, 拡張例 | 4 |
| 5 | 第2部 | リクエスト単体テストの設定（HTTPメッセージング） | 機能概要, 拡張例 | 3 |
| 6 | 第2部 | リクエスト単体テストの設定（Nablarchバッチアプリケーション） | 機能概要, 拡張例 | 3 |
| 7 | 第2部 | リクエスト単体テストの設定（MOMによるメッセージング） | 機能概要 | 8 |
| 8 | 第2部 | 取引単体テストの設定（HTTPメッセージング） | 機能概要, 拡張例 | 1 |
| 9 | 第2部 | 取引単体テストの設定（MOMによるメッセージング） | 機能概要, 拡張例 | 1 |
| 10 | 第3部 | テストデータの書き方 | 機能概要 | 136 |
| 11 | 第3部 | テストデータの記載例 | 機能概要 | 65 |
| 12 | 第3部 | リクエスト単体テスト（HTTPメッセージング） | 機能概要 | 3 |
| 13 | 第3部 | 取引単体テスト（ウェブアプリケーション） | 機能概要 | 5 |
| 14 | 第3部 | 取引単体テスト（Nablarchバッチアプリケーション） | 機能概要 | 7 |
| 15 | 第3部 | 取引単体テスト（HTTPメッセージング） | 機能概要 | 2 |
| 16 | 第4部 | テストデータ変換ツール | 導入 | 5 |

`第2部 マスタデータ復旧機能` の `拡張例` 0件も検査に引っかかる。同じ手順で扱う。

### 判断基準（`design.md` の定義をそのまま使う。独自解釈を足さない）

| dest_part | dest_section | 定義 | 出典 |
|---|---|---|---|
| 第2部 | 機能概要 | 全体像（図）／主なクラスとリソース／前提事項 | design.md §3 ページのアウトライン |
| 第2部 | 使用方法 | テストを実行できるようにする／コンポーネントを設定する／`<個別設定>`する | 同上 |
| 第2部 | 拡張例 | `<拡張手順>`する | 同上 |
| 第3部 | 機能概要 | このページで何ができるようになるか | design.md §4 ページのアウトライン |
| 第3部 | 使用方法 | テストクラスを作成する／テストメソッドを作成する／テストデータを作成する／テストを実行する／テスト結果を確認する | 同上 |
| 第4部 | 機能概要 | 何ができるか。どの場面で使うか | design.md §5 ページのアウトライン |
| 第4部 | 導入 | インストール手順、依存関係、設定 | 同上 |
| 第4部 | 使用方法 | `<操作手順>`する | 同上 |

### 手順

1. 対象16ページの `mapping.csv` 該当行を機械抽出する。

   ```bash
   python3 - <<'EOF'
   import csv, collections
   m = list(csv.DictReader(open('mapping/mapping.csv', encoding='utf-8')))
   TARGET = [...]  # 上表の (dest_part, dest_page)
   for key in TARGET:
       rs = [r for r in m if (r['dest_part'], r['dest_page']) == key and r['disposition'] != 'DROP']
       for r in sorted(rs, key=lambda r: (r['src_file'], int(r['src_body_start']))):
           print(key[1], r['mapping_id'], r['src_file'], r['src_body_start'], r['src_body_end'], r['dest_section'], r['heading_path'], sep='\t')
   EOF
   ```

2. **抽出した全行の出典を実ファイルで通読する。** current側は `git show c241906:<path>`、input側は作業ツリー。`heading_path` だけで判定しない。
3. 上表の定義に照らして `dest_section` を1行ずつ判定する。**機械的な一括変更をしない。**
4. `機能概要` に該当する行が1件も無いページは、**行を無理に動かさない**。「出典なし」として STEP 4 の調査報告に回す。
5. 変更した行は `_batch/*.csv` を直接編集し、`mapping.csv` は**全30バッチの単純連結で再生成**する（`#5` と同じ統合方式。`mapping.csv` を直接編集しない）。
6. 変更した行・変更しなかった行の**両方**について、`mapping_id` / 内容 / 旧→新 / 根拠（file:line 付き）の表を `checks/task-05b.md` に残す。「導入」0件対応（`checks/task-05.md` 467-486行）と同じ粒度で書く。

### 参考: 各ページの `機能概要` 候補行（点検時の機械抽出。これで確定させず、必ず実ファイルを読むこと）

| dest_page | 候補 mapping_id | 出典 |
|---|---|---|
| リクエスト単体テストの設定（RESTfulウェブサービス） | current-0310 / current-0311 | `RequestUnitTest_rest.rst` 49-93「概要 > モジュール一覧 / 設定」 |
| テストデータの書き方 | input-0098 / input-0099 / input-0114 | `...testshots.md` 2-43、`ntf-testdata-doc.md` 2-6 |
| テストデータの記載例 | input-0036 / input-0037 / input-0058 / input-0076〜0082 / input-0093 | 各 `...examples-*.md` の (L1直下) と「全体像」 |
| リクエスト単体テスト（HTTPメッセージング） | current-0064 / current-0069 | `http_real.rst` 4-8、`http_send_sync.rst` 6-15（いずれも (L1直下) の導入文） |
| 取引単体テスト（HTTPメッセージング） | current-0138 | `http_send_sync.rst` 6-15 |
| 取引単体テスト（Nablarchバッチアプリケーション） | current-0128 | `batch.rst` 4-25 |
| 取引単体テスト（ウェブアプリケーション） | current-0142 | `03_DealUnitTest/index.rst` 6-13 |
| テストデータ変換ツール（導入） | input-0183 / input-0184 / input-0190 | `testdata-converter-design.md` 13-33, 106-115 |
| 第2部の各設定ページ | 明確な候補なし | 出典が `03_Tips.rst` 由来の断片中心。STEP 4 行き濃厚 |

### 注意（`#5` の同種対応で実際に間違えた点）

- `heading_path` に「概要」「前提条件」とあっても、実体が `:ref:` 参照先として他セクションから指定されている場合は移動しない（`current-0350` の前例）。移動前に `grep -rn ':ref:' ` で参照関係を確認する。
- `(L2直下)` で終わる行は、同じ親を持つ配下セクションと同じ `dest_section` に置く（`steering.md` #5 Steps のルール）。

### ゲート

- `python3 mapping/tools/verify_mapping.py` が **591行・`lines` 合計 12,986・DROP除く 11,973** を維持していること（`dest_section` の変更のみのため数値は不変）
- `check_coverage` / `check_vocabulary` がエラー0件
- `check_unused_vocabulary` の ERROR が減っていること。残った分は STEP 4 で `PENDING_ZERO` に登録する

## STEP 3: `volume.md` に0行ページを追加する

`volume.md` は行のあるページ32件しか載せていないため、`#6` の文量判断が0件ページを見落とす。

1. 集計表に `lines = 0` の行を追加する（`vocabulary.md` の全 `(dest_part, dest_page)` を母集合にする）。`0` の行には `EXPECTED_ZERO` / `PENDING_ZERO` の区別を備考列で示す。
2. あわせて次の記述誤りを修正する。

   **Before**（`volume.md` 68行）

   ```
   - disposition内訳: MOVE 239 / MERGE 226 / DROP 96 / SPLIT 16（4セクション×3〜4分割） / REFERENCE 14
   ```

   **After**

   ```
   - disposition内訳: MOVE 239 / MERGE 226 / DROP 96 / SPLIT 16（6セクション。current-0037/0066/0106/0156が各3行、current-0184/0185が各2行） / REFERENCE 14
   ```

3. `dest_section` 単位の集計表も追加する（`#5` の「導入」0件・今回の「機能概要」0件が、いずれも `dest_page` 単位の集計では見えなかったため）。

### ゲート

`volume.md` の `lines` 合計が 11,973 のまま変わらないこと。`vocabulary.md` の全ページが表に現れること（機械検証を `checks/task-05b.md` に記録）。

## STEP 4: 未解決の0件を調査報告にまとめる（`design.md` は変更しない）

`#6` はユーザーレビューで確定させるタスクである。**CC は `design.md` を書き換えない。** 選択肢と実測根拠だけを `checks/task-05b.md` に提示する。

### 報告項目1: 第1部「稼動環境」0件

実測して次を報告する。

- `design.md` §2「モジュール一覧の集約」は「依存関係は第1部『稼動環境』に集約する。処理方式ごとのページには置かない」と定めている
- 現状 `current-0267`（`JUnit5_Extension.rst` 37-47、`nablarch-testing-junit5` の依存定義）は 第2部 JUnit 5用拡張機能 > 使用方法 に、`current-0180`（`01_Abstract.rst` 698-739、JUnit Vintage の依存追加）も同ページに割当
- `current-0310`（RESTful のモジュール一覧）は §2 が認める例外に該当する
- 「Java・Jakarta EE の要件」に相当する記述は current 47 rst・input 10 md に**存在しない**（`Jakarta EE` / `Java 17` / `Java SE` 等で grep しヒット0件。grep コマンドと結果を報告に載せる）

提示する選択肢:

| 案 | 内容 | 影響 |
|---|---|---|
| A | `current-0180` / `current-0267` を第1部 稼動環境 へ移す | `design.md` §2 の集約ルールどおり。第2部 JUnit 5用拡張機能 が 475→400行台に減る |
| B | §2 の集約ルールを撤回し、依存関係は各ページに置く | `design.md` 改訂が必要。第1部 稼動環境 は JUnit 4/5 の記述のみになる |
| C | 稼動環境セクション自体を第1部から外す | `design.md` §2 の表を改訂。出典のない「Java・Jakarta EE の要件」問題も同時に解消 |

「Java・Jakarta EE の要件」については、出典がないため**別途ユーザー判断が要る**旨を明記する（「マッピングにない内容を追加しない」の例外にするか、項目から外すか）。

### 報告項目2: 第2部「テストデータの形式」0件

- `design.md` §3 はこのページを「Excel / YAML の比較、使い分け、YAML使用時の設定」と定義している
- 割当0行。YAML に言及する204行の行先は 第3部 テストデータの書き方74／第3部 テストデータの記載例64／DROP 52／第4部 テストデータ変換ツール5／その他9
- `nablarch-testing-yaml` の記述は input 全体で `ntf-testdata-doc.md:70`（JSON Schema 同梱の説明）の1箇所のみで、第3部 テストデータの書き方 に MERGE 済み

提示する選択肢（ページを新設するか、第3部に統合するか、`#6` のページ分割確定と併せて判断する旨）を書く。**CC が勝手に行を移さない。**

### 報告項目3: 第2部 取引単体テストの設定 2ページの0件

`取引単体テストの設定（ウェブアプリケーション）` `同（Nablarchバッチアプリケーション）` は語彙に存在するが割当0行。`#6` 未確定事項#1・#2 の判断対象であることを明記する。

### STEP 4 の成果物

`PENDING_ZERO` に上記を登録し、`verify_mapping.py` が WARN として毎回出力する状態にする。理由文字列には必ず `#6` のどの未確定事項に対応するかを書く。

## STEP 5: self-check と commit

- `checks/task-05b.md` を作成する（STEP 1〜4 の記録、実行コマンドと出力をそのまま貼る）
- `steering.md` に `#5b` を追記し、`#6` の Prerequisites を更新する
- `#6` Completion criteria に次を追加する

  ```
  - `verify_mapping.py` の `PENDING_ZERO` が0件であること（#6 で全件が確定または EXPECTED_ZERO へ移動）
  ```

- commit & push（STEP 1 と STEP 2〜5 で最低2コミットに分ける）
- **user review** — 別セッションの Claude が push 済みブランチを独立検証する。CC は commit SHA と実行コマンド出力を報告して `/rn:dn` で中断し、承認まで `#5c` に進まない（サブエージェントレビューは実施しない）

## `#5b` の Completion criteria

- `verify_mapping.py` に `check_unused_vocabulary` が実装され、コミットされている
- `EXPECTED_ZERO` の全エントリに `design.md` の該当箇所の引用が理由として付いている
- `PENDING_ZERO` の全エントリに `#6` のどの未確定事項に対応するかが書かれている
- `check_unused_vocabulary` の ERROR が0件（残りは `EXPECTED_ZERO` か `PENDING_ZERO` に分類済み）
- `lines` 合計 12,986 / DROP除く 11,973 / 591行 が不変
- `checks/task-05b.md` に、`dest_section` を変更した行と変更しなかった行の両方が根拠付きで列挙されている
- `volume.md` に0行ページと `dest_section` 単位の集計が載っている
- `design.md` が変更されていない（`git diff` で確認）

---

# `#5c`: `DROP` 全件レビュー

**Purpose**: `design.md` §11.8「`DROP` は件数の多寡にかかわらず全件を対象とする」の未達分を解消する。

**Prerequisites**: `#5b`

## 背景

3観点レビューの記録（`checks/task-05.md` 332-336行）では `DROP` 94件中74件（空/TOC/アンカー37・開発者向け27・重複10）が検査対象。ユーザー差し戻しの再検証は20行以上の13件のみ。現在96件あり、**約20件に個別レビューの記録がない。**

## Steps

1. `mapping.csv` の `disposition=DROP` 全96行を抽出する。
2. `checks/task-05.md` の既存レビュー記録（「batch-02〜15 DROP一覧」節、3観点レビュー表、ユーザー差し戻し対応表）と突合し、**レビュー済み / 未レビュー**を機械的に分類する。分類根拠（どの節のどの行に記録があるか）を残す。
3. 未レビュー分について、出典を実ファイルで通読し、次の観点で判定する。

   | 観点 | 判定内容 |
   |---|---|
   | 理由の妥当性 | `note` の理由が実内容と合っているか |
   | 重複DROP | 重複先に本当に同内容があるか。**重複先の実ファイルを開いて確認する**（`note` の記述を信じない） |
   | 開発者向けDROP | `design.md` §9 の「利用者向けの仕様が含まれる可能性」に該当しないか |
   | 空/TOC/アンカー | 本文が実際に空・TOC・アンカーのみか |

4. 全96行の判定結果を1つの表にまとめて `checks/task-05c.md` に記録する（レビュー済み分は既存記録への参照でよいが、行は落とさない）。
5. 判定が覆った行があれば `_batch/*.csv` を修正し `mapping.csv` を再生成する。
6. commit & push → **user review** — 別セッションの Claude が独立検証する。CC は commit SHA を報告して `/rn:dn` で中断し、承認まで `#5d` に進まない（サブエージェントレビューは実施しない）

## Completion criteria

- `DROP` 96行すべてが `checks/task-05c.md` の表に現れる
- 各行に「レビュー済み（記録の所在）」または「今回レビュー（判定と根拠 file:line）」のいずれかがある
- 判定が覆った行は `_batch/*.csv` を修正し、`verify_mapping.py` がエラー0件
- `lines` 合計 12,986 が不変

---

# `#5d`: 記録の整合

**Purpose**: `#5` までの成果物に残った記録上の不整合を解消する。データの判断は変更しない。

**Prerequisites**: `#5c`

## Steps

### 1. `split-plan.md` に `input-0016` / `input-0030` を追記する

`steering.md` #4a 注記「`lines < 100` のセクションでも分割が必要と判明した場合は `split-plan.md` に追記し `rationale` を残す」が未実施。`checks/task-05.md` 347・349行に記録がある内容を `split-plan.md` の表形式（`section_id, heading_path, lines, split, parts, rationale`）に転記する。

| section_id | parts |
|---|---|
| input-0016 | 214-226 → 第3部 テストデータの書き方 > 使用方法（MERGE）／227-233 → DROP（重複先 current-0292） |
| input-0030 | 444-462 → 第3部 リクエスト単体テスト（ウェブアプリケーション）> 使用方法（MERGE）／463-472 → DROP（重複先 current-0211） |

`split-plan.md` 冒頭の対象定義（`lines >= 100` の23件）に、`#5` 中に追加した2件がある旨を追記する。

### 2. 暫定行の一覧を作る

`steering.md` #5 Steps「暫定扱いとしたセクションを `checks/task-05.md` に一覧化する」が未達。`note` が「暫定」で始まる27行のうち20行の `mapping_id` が `task-05.md` に現れない。

`checks/task-05.md` に「暫定扱い一覧」節を新設し、27行全件を `mapping_id / dest_page / 暫定の理由 / #6 で必要な判断` の表にする。

### 3. `HTMLチェックツール` 8行の `note` を更新する

`current-0367`〜`current-0375` の `note` は「design.md の第2部・第3部いずれのページツリーにも受け皿が存在しない」と書いているが、第4部新設で解消済み。**`#6` の「暫定。」一括解消では判断不要で文言更新だけで済む行**である旨を、`checks/task-05.md` の暫定一覧に明記する（`note` 自体の書き換えは `#6` で行う）。

### 4. `design.md` §12 未確定事項#3 の確定時期

「ファイル名・ディレクトリ構成」の確定時期が「マッピング作成時に決定」だが `#5` 完了時点で未決定。**`design.md` は `#6` で更新するため、ここでは変更しない。** `checks/task-05d.md` に申し送りとして記録するにとどめる。

### 5. commit & push → **user review**

別セッションの Claude が独立検証する。CC は commit SHA を報告して `/rn:dn` で中断し、承認まで `#6` に進まない。

## Completion criteria

- `split-plan.md` に `input-0016` / `input-0030` の行があり、`parts` の行範囲が `mapping.csv` と一致する（機械検証）
- `checks/task-05.md` の暫定一覧に27行全件が現れる（機械検証: `note` が「暫定」で始まる行の `mapping_id` 全件が一覧表に存在する）
- `design.md` / `mapping.csv` / `_batch/*.csv` に差分がない（`git diff` で確認）

---

# 全タスク共通の禁止事項

- **`design.md` を変更しない。** `#6` のユーザー判断対象である
- **`mapping.csv` を直接編集しない。** `_batch/*.csv` を編集して全30バッチの単純連結で再生成する
- **`note` の記述を根拠にしない。** 重複先・参照関係は必ず実ファイルを開いて確認する
- **推測で件数を書かない。** 報告する数値はすべて実行したコマンドの出力で裏付ける
- **亜種ファイルを作らない。** 検証は `mapping/tools/verify_mapping.py` に足す。使い捨てスクリプトを別ディレクトリに残さない
- コンテキストが70%に近づいたら報告して `/rn:dn` で中断する
- **user review で自己弁護しない。** 指摘を受けたら実測で再検証し、覆る場合は根拠を出す。覆らない場合は素直に直す
- **user review の直前に自分の作業を要約し直さない。** レビューは push 済みの実物に対して行われる。報告は commit SHA と実行出力に留める
