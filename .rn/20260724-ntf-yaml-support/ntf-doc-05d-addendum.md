# 作業指示（追補）: `#5d` の拡張 — セクション境界の検査追加と是正

対象ブランチ: `lovaizu/nablarch-document` の `work`（PR #730 head）

前提: `#5b` は `ca1e9cf` で user review 承認済み。本追補は `#5d` に STEP を追加するもので、`#5b` は再オープンしない。

## 背景

`#5b` のレビュー（`ca1e9cf` に対する独立検証）で2点の欠陥を検出した。いずれも `verify_mapping.py` が検出できない種類であり、**検査を足さない限り再発しても気づけない。**

1. `check_unused_vocabulary` は「非DROP行が1件以上」でセクション充足と判定する。`disposition=REFERENCE` は本文を持たないため、**参照リンクだけのセクションが GREEN になる**
2. 導入文（`(L1直下)` / `(L2直下)` / `(冒頭)`）が本体と別の `dest_section` に分かれている行がある。うち2件は `steering.md` #5 Steps の既存ルール **「`heading_path` が `(L2直下)` で終わる行は、同じ親を持つ配下セクションと同じ `dest_section` に置く」に違反**している

2 は `#5` 由来の既存欠陥で、`#5b` が作り込んだものではない。

## `#5d` の定義変更

`steering.md` の `#5d` を次のとおり改める。

**Before**

```
### #5d: 記録の整合

**Purpose**: `#5` までの成果物に残った記録上の不整合を解消する。データの判断は変更しない。
```

**After**

```
### #5d: 記録の整合とセクション境界の是正

**Purpose**: `#5` までの成果物に残った記録上の不整合を解消し、あわせて `#5b` のレビューで
検出したセクション境界の欠陥を、機械検査の追加と既存ルールに基づく是正で解消する。
既存の割当判断（dest_page / disposition / audience）は変更しない。
```

既存の STEP 1〜5 はそのまま残し、以下の STEP 6〜8 を追加する。commit は STEP 1〜5 と STEP 6〜8 で分ける。

---

## STEP 6: `check_reference_only_sections` を追加する

### 目的

必須セクションが `REFERENCE` のみで充足されている状態を検出する。`REFERENCE` はページに本文を持たず参照導線だけを置く `disposition` であり（`design.md` §11.6 観点A「`REFERENCE` が本文を持っていないか」）、それだけでセクションが成立するかは判断が要る。

### 仕様

`mapping/tools/verify_mapping.py` に追加する。

- 本文を持つ `disposition` を `CONTENT_BEARING = {"MOVE", "MERGE", "SPLIT"}` と定義する
- `mapping.csv` で使われている全 `(dest_part, dest_page, dest_section)` について、`CONTENT_BEARING` の行が1件も無いものを列挙する
- **advisory 出力とし `exit 1` しない**（内容として妥当な場合があるため。判定は人が行う）
- `check_duplicate_destinations` と同じ位置づけで `main()` から呼び、件数と一覧を出力する

```python
    ref_only = check_reference_only_sections(rows)
    print(f"\nreference-only sections: {len(ref_only)} (advisory only, not auto-fixed)")
    for part, page, section, n in ref_only:
        print(f" - [{part} > {page} > {section}]: {n} row(s), all non content-bearing")
```

### 現状（レビュー時の実測。件数が違う場合は先に原因を突き止める）

| dest_part | dest_page | dest_section | 行数 | 該当 mapping_id |
|---|---|---|---|---|
| 第3部 テストの実装方法 | リクエスト単体テスト（HTTPメッセージング） | 機能概要 | 2 | current-0064 / current-0069 |
| 第3部 テストの実装方法 | 取引単体テスト（HTTPメッセージング） | 機能概要 | 1 | current-0138 |

### 判断はしない

この2件は `#5b` STEP 2 で `使用方法` → `機能概要` に変更した行である。**再変更しない。** 両ページとも実体が「他ページとの差分のみを解説する」構成であり、機能概要が参照導線になること自体は内容に即している可能性が高い。`#6` で確定させる。

### `#6` への引き継ぎ（宛先を明示する）

`steering.md` `#6` の Steps に次を追加する。

```
- [ ] `verify_mapping.py` の `reference-only sections` の全件について、
      「本文なしで成立するページ構成として確定する」か「本文を持つ行を割り当てる」かを
      判断し、結果を `checks/task-06.md` に記録する
```

`#6` の Completion criteria に次を追加する。

```
- `reference-only sections` の全件に判断が記録されている（0件にする必要はない）
```

---

## STEP 7: 導入文と本体の `dest_section` 分断を是正する

### 目的

導入文の行だけが本体と別セクションに置かれると、ページ上で導入文とその後続手順が分断される。`steering.md` #5 Steps は `(L2直下)` についてこれを禁じるルールを持つが、機械検査が無いため違反が残っていた。

### 仕様: `check_intro_section_split` を追加する

- `heading_path` が `(L1直下)` / `(L2直下)` / `(冒頭)` で終わる非DROP行を「導入文行」とする
- 同じ `src_file` かつ同じ親 `heading_path`（末尾要素を除いた部分）を持つ他の非DROP行を「同階層行」とする
- 導入文行の `(dest_page, dest_section)` が、同階層行のどの `(dest_page, dest_section)` とも一致しない場合に検出する
- `(L2直下)` の違反は **ERROR（`exit 1`）**。`steering.md` #5 の明文ルール違反であるため
- `(L1直下)` / `(冒頭)` は **advisory 出力**。明文ルールが無く、ページ作成時の書き直しで吸収できる場合があるため

### 現状（レビュー時の実測。6件）

| 種別 | mapping_id | heading_path | 現在の dest_section | 同階層行の dest_section |
|---|---|---|---|---|
| ERROR | current-0150 | 取引単体テストの実施方法 > Cookieなど前のレスポンスの情報を引き継ぐ方法 > (L2直下) | 機能概要 | 使用方法 / 拡張例 |
| ERROR | current-0269 | JUnit 5用拡張機能 > Extension クラスと合成アノテーションの一覧 > (L2直下) | 機能概要 | 使用方法 |
| advisory | input-0114 | NTF テストデータ リファレンス > (L1直下) | 使用方法 | テストデータ |
| advisory | current-0060 | リクエスト単体テストの実施方法(ファイルアップロード) > (L1直下) | 機能概要 | 使用方法 |
| advisory | current-0142 | 取引単体テストの実施方法 > (L1直下) | 機能概要 | 使用方法 |
| advisory | current-0148 | 取引単体テストの実施方法 > (L1直下) | 機能概要 | 使用方法 |

### 是正手順（ERROR 2件）

1. `git show c241906:<src_file>` で当該セクションと同階層セクションを**全文通読する**。
2. `steering.md` #5 Steps のルール「`(L2直下)` 行は、同じ親を持つ配下セクションと同じ `dest_section` に置く」を適用する。
3. 同階層行の `dest_section` が1つに定まる場合（current-0269 は `使用方法` のみ）はそれに合わせる。
4. 同階層行の `dest_section` が複数ある場合（current-0150 は `使用方法` と `拡張例`）は、**導入文が実際にどちらの内容を導いているか**を実ファイルで確認して決める。行数の多寡で決めない。
5. `_batch/*.csv` を編集し、`mapping.csv` を全30バッチの単純連結で再生成する。
6. `note` に是正の根拠を追記する。書式は `#5b` の変更行と揃える（旧→新、根拠 file:line）。

**`dest_page` / `disposition` / `audience` は変更しない。** 変更が必要と判断した場合は変更せずに報告し、`#6` に上げる。

### advisory 4件の扱い

**マッピングを変更しない。** ただし記録を残す先は `checks/` ではなく `mapping.csv` の `note` とする。`design.md` §11.3 が「作成するページの内容は `mapping.csv` に従う」と定めており、ページ作成タスク（`#8〜`）が読むのは `mapping.csv` だからである。

該当4行の `note` の**末尾に**次を追記する（既存の note は削除しない）。

```
 [セクション境界] 本行は導入文であり、後続の本体行（<同階層の mapping_id をカンマ区切りで列挙>）は
dest_section=<同階層の dest_section> に置かれている。ページ作成時、導入文と本体の接続を
ページ内で再構成すること（design.md §8「出典の文面をそのまま流用しない」の範囲で対応可能）。
```

具体例（current-0142）:

```
 [セクション境界] 本行は導入文であり、後続の本体行（current-0143, current-0144, current-0145）は
dest_section=使用方法 に置かれている。ページ作成時、導入文と本体の接続をページ内で再構成すること。
```

### ゲート

- `python3 mapping/tools/verify_mapping.py` が `exit 0`
- `check_intro_section_split` の ERROR が **0件**
- advisory が 4件で、4件すべての `note` に `[セクション境界]` が含まれる（機械検証）
- 591行 / `lines` 全行 12,986 / DROP除く 11,973 が不変
- `dest_page` / `disposition` / `audience` の分布が変化していない（`git diff` で確認。変更は `dest_section` と `note` のみ）

---

## STEP 8: ページ作成タスクにチェック項目を足す

`steering.md` の `### #8〜: ページの作成` の Steps に次を追加する。**この2行が、STEP 6・STEP 7 の検出結果をページ作成時に必ず読ませるための宛先である。**

```
- [ ] 当該 `dest_page` の行に `note` の `[セクション境界]` が含まれる場合、導入文と本体の
      接続をページ内で再構成する（出典の分断をそのまま持ち込まない）
- [ ] 当該 `dest_page` に `reference-only sections`（`verify_mapping.py` の advisory）が
      該当する場合、`#6` で確定した方針に従う
```

---

## `#5d`（拡張後）の Completion criteria

既存の3項目に加えて次を満たすこと。

- `check_reference_only_sections` / `check_intro_section_split` が `verify_mapping.py` に実装され、コミットされている
- `check_intro_section_split` の ERROR が0件
- `reference-only sections` の advisory 件数が2件で、`#6` の Steps・Completion criteria に引き継ぎが追記されている
- `[セクション境界]` の `note` 追記が4件あり、対象 `mapping_id` がレビュー時の実測と一致する
- 591行 / 12,986 / 11,973 が不変
- `design.md` が無変更（`git diff` で確認）
- `checks/task-05d.md` に、是正した2行の旧→新と根拠 file:line、advisory 4件の判断理由が記録されている

## user review

`#5b` と同じ扱い。別セッションの Claude が push 済みブランチを独立検証する。CC は commit SHA と実行コマンド出力を報告して `/rn:dn` で中断し、承認まで `#6` に進まない。

## 禁止事項（`#5b` と共通、再掲）

- `design.md` を変更しない
- `mapping.csv` を直接編集しない（`_batch/*.csv` を編集して再生成）
- `note` の記述を根拠にしない。参照関係・同階層関係は実ファイルを開いて確認する
- 検出件数が本書の実測値と違う場合、先に原因を突き止めてから是正に入る
- 検査を advisory にして件数を減らす方向で「解消」しない。ERROR は是正で0にする
