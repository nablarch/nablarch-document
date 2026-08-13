# 作業指示（追補）: `#5c` に STEP 0 を追加する

対象ブランチ: `lovaizu/nablarch-document` の `work`（PR #730 head）

前提: `990c8e1` は user review 承認済み。本追補は `#5c`（`DROP` 全件レビュー）の先頭に STEP 0 を追加するもので、`#5b` / `#5d` の定義は変更しない。

## 背景

`990c8e1` のレビューで、`check_unused_vocabulary` に穴があることを検出した。

実装は各キーについて「使用数 > 0 なら `continue`」で始まるため、**`EXPECTED_ZERO_PAGES` / `EXPECTED_ZERO_SECTIONS` / `PENDING_ZERO` に0件として登録済みの組み合わせが、後から非0になっても何も報告しない。**

`#5c` は `DROP` 判定を覆す可能性がある（`#5` の3観点レビューで `current-0121` が実際に `DROP` → `REFERENCE` に変わった前例がある）。覆した行の割当先が現在0件のページ・セクションだった場合、次の3つが誰にも気づかれないまま古くなる。

- `verify_mapping.py` の `PENDING_ZERO` 25件
- `mapping/volume.md` の0行7ページ
- `checks/task-05b.md` の STEP 4 調査報告

`#5c` のデータ変更に入る前に検出手段を用意する。`#5b` STEP 1 と同じ「検査を先に足す」順序である。

## STEP 0: 許可リストの陳腐化検出を追加する

### 実装

`mapping/tools/verify_mapping.py` の `check_unused_vocabulary` の末尾（`return errors, pending` の直前）に追加する。

**Before**

```python
            errors.append(
                f"section [{dp} > {pg} > {sec}]: 0 non-DROP rows assigned "
                "(not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)"
            )

    return errors, pending
```

**After**

```python
            errors.append(
                f"section [{dp} > {pg} > {sec}]: 0 non-DROP rows assigned "
                "(not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)"
            )

    # 許可リストの陳腐化検出。0件として登録済みのキーに行が入った場合、
    # 許可リスト・volume.md・checks/task-05b.md が古くなったまま気づけない
    # （上のループはいずれも「使用数>0ならcontinue」で始まるため素通りする）。
    # 2026-07-28 #5c STEP 0 で追加。
    for key in list(EXPECTED_ZERO_PAGES) + [k for k in PENDING_ZERO if len(k) == 2]:
        n = used_pages.get(key, 0)
        if n > 0:
            errors.append(
                f"stale allowlist: page [{key[0]} > {key[1]}] has {n} non-DROP row(s) "
                "but is registered as zero (EXPECTED_ZERO_PAGES / PENDING_ZERO)"
            )
    for key in list(EXPECTED_ZERO_SECTIONS) + [k for k in PENDING_ZERO if len(k) == 3]:
        n = used_page_sections.get(key, 0)
        if n > 0:
            errors.append(
                f"stale allowlist: section [{key[0]} > {key[1]} > {key[2]}] has {n} "
                "non-DROP row(s) but is registered as zero "
                "(EXPECTED_ZERO_SECTIONS / PENDING_ZERO)"
            )

    return errors, pending
```

ERROR（`exit 1`）とする。非0になった場合、許可リストから外して `volume.md` と `checks/task-05b.md` を更新するのが正しい対応であり、放置を許さないため。advisory にしない。

### 実行と記録

追加直後に実行する。

```bash
python3 mapping/tools/verify_mapping.py; echo "EXIT: $?"
```

**現状は `stale allowlist` の ERROR が0件**になるはずである（許可リスト30件＝`EXPECTED_ZERO_PAGES` 4／`EXPECTED_ZERO_SECTIONS` 1／`PENDING_ZERO` 25 のすべてが実際に0件であることを、レビュー時に独立検証で確認済み）。

- ERROR 0件・`EXIT: 0` を確認し、実行出力をそのまま `checks/task-05c.md` に貼る
- **ERROR が出た場合は `#5c` 本体に入らず、原因を報告して中断する**（`#5b` の成果と現データが既に食い違っていることになるため）

### commit

この STEP だけで1コミットにする。`DROP` レビューの変更と混ぜない。

## `#5c` Completion criteria への追加

`steering.md` の `#5c` Completion criteria に次を追加する。

```
- `check_unused_vocabulary` に許可リストの陳腐化検出が実装され、コミットされている
- `DROP` 判定を覆した行がある場合、`stale allowlist` の ERROR が0件になるまで
  許可リスト（`EXPECTED_ZERO_*` / `PENDING_ZERO`）・`mapping/volume.md`・
  `checks/task-05b.md` を更新済みであること
```

## 禁止事項（既存の作業指示と共通、再掲）

- `design.md` を変更しない
- `mapping.csv` を直接編集しない（`_batch/*.csv` を編集して全30バッチの単純連結で再生成）
- 検査を advisory に落として ERROR 件数を減らす方向で「解消」しない
- 検出件数が本書の記載と違う場合、先に原因を突き止めてから先に進む

## user review

`#5c` 全体の完了時にまとめて受ける。STEP 0 単独では中断しない。
