# task-05b self-check

## STEP 1: `check_unused_vocabulary` の追加とREDの確認

`mapping/tools/verify_mapping.py` に `check_unused_vocabulary`（`SECTION_TEMPLATE` /
`EXPECTED_ZERO_PAGES` / `EXPECTED_ZERO_SECTIONS` / `PENDING_ZERO` を使った3分類判定）
を追加し、`main()` に組み込んだ。

### 実行結果

```
$ python3 mapping/tools/verify_mapping.py > /tmp/red_output.txt 2>&1; echo "EXIT: $?"
EXIT: 1
```

```
Loaded 591 rows from mapping.csv

pending zero assignments: 0 (awaiting #6 decision)
lines total (all rows): 12986
lines total (excluding DROP): 11973

candidate duplicate destinations: 44 (advisory only, not auto-fixed)
...(check_duplicate_destinationsの既存出力。#5から変更なし)...

28 error(s):
 - page [第2部 導入と設定 > テストデータの形式]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_PAGES / PENDING_ZERO)
 - page [第2部 導入と設定 > 取引単体テストの設定（Nablarchバッチアプリケーション）]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_PAGES / PENDING_ZERO)
 - page [第2部 導入と設定 > 取引単体テストの設定（ウェブアプリケーション）]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_PAGES / PENDING_ZERO)
 - section [第1部 テスティングフレームワークとは > テスティングフレームワークとは > 稼動環境]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > クラス単体テストの設定 > 機能概要]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > クラス単体テストの設定 > 拡張例]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > マスタデータ復旧機能 > 拡張例]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > リクエスト単体テストの設定（HTTPメッセージング） > 機能概要]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > リクエスト単体テストの設定（HTTPメッセージング） > 拡張例]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > リクエスト単体テストの設定（MOMによるメッセージング） > 機能概要]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > リクエスト単体テストの設定（Nablarchバッチアプリケーション） > 機能概要]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > リクエスト単体テストの設定（Nablarchバッチアプリケーション） > 拡張例]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > リクエスト単体テストの設定（RESTfulウェブサービス） > 機能概要]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > リクエスト単体テストの設定（RESTfulウェブサービス） > 拡張例]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > リクエスト単体テストの設定（ウェブアプリケーション） > 機能概要]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > 共通設定 > 機能概要]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > 共通設定 > 拡張例]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > 取引単体テストの設定（HTTPメッセージング） > 機能概要]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > 取引単体テストの設定（HTTPメッセージング） > 拡張例]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > 取引単体テストの設定（MOMによるメッセージング） > 機能概要]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第2部 導入と設定 > 取引単体テストの設定（MOMによるメッセージング） > 拡張例]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第3部 テストの実装方法 > テストデータの書き方 > 機能概要]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第3部 テストの実装方法 > テストデータの記載例 > 機能概要]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第3部 テストの実装方法 > リクエスト単体テスト（HTTPメッセージング） > 機能概要]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第3部 テストの実装方法 > 取引単体テスト（HTTPメッセージング） > 機能概要]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第3部 テストの実装方法 > 取引単体テスト（Nablarchバッチアプリケーション） > 機能概要]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第3部 テストの実装方法 > 取引単体テスト（ウェブアプリケーション） > 機能概要]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
 - section [第4部 ツール > テストデータ変換ツール > 導入]: 0 non-DROP rows assigned (not registered in EXPECTED_ZERO_SECTIONS / PENDING_ZERO)
```

`lines total (all rows): 12986` / `lines total (excluding DROP): 11973` / `Loaded 591 rows` は
`#5` 完了時点と不変。

### 件数の差異（作業指示「17件」）についての調査

作業指示の要約行は「ページ単位0件: 3件」「セクション単位0件: 14件」（計17件）としていたが、
実測は28件（ページ3件・セクション25件）だった。原因を切り分けるため、作業指示の詳細部分
（STEP 2の16行の表＋別記の「マスタデータ復旧機能」＋STEP 4「第1部『稼動環境』」）と
実測結果を突合した。

- ページ単位: 3件（作業指示の要約と一致）
- セクション単位: 作業指示のSTEP 2詳細表（16行）を「不足」列で展開すると
  `機能概要`単独7・`拡張例`単独0・両方9`（1行あたり2件）` … 実際に1行ずつ数えると
  23件、それに「マスタデータ復旧機能 > 拡張例」1件を加えて24件。これは作業指示が
  STEP 4で別扱いにすると明記した「第1部『稼動環境』」を含んでいない数。
  実測のセクション単位25件は、この24件に「第1部 > テスティングフレームワークとは >
  稼動環境」を加えた数と**完全一致**した。

つまり作業指示本文の「14件」という要約値は、詳細な16行表・マスタデータ復旧機能の
言及・STEP 4で扱うとされた稼動環境の存在と整合しておらず、要約行自体の誤記（下位互換の
概算値）と判断する。詳細な列挙内容（STEP 2の16行表＋マスタデータ復旧機能＋STEP 4の
稼動環境）と実測は1件の過不足もなく一致するため、`check_unused_vocabulary` の実装を
そのまま維持し、STEP 2 に進む。

以下、実測28件と作業指示に列挙された項目の対応表（すべて一致）。

| 実測での分類 | 実測の (dest_part, dest_page[, dest_section]) | 作業指示での対応箇所 |
|---|---|---|
| page | 第2部 > テストデータの形式 | STEP 2ページ単位要約・STEP 4報告項目2 |
| page | 第2部 > 取引単体テストの設定（ウェブアプリケーション） | STEP 2ページ単位要約・STEP 4報告項目3 |
| page | 第2部 > 取引単体テストの設定（Nablarchバッチアプリケーション） | STEP 2ページ単位要約・STEP 4報告項目3 |
| section | 第1部 > テスティングフレームワークとは > 稼動環境 | STEP 4報告項目1（STEP 2表には含まれない旨が明記されている） |
| section | 第2部 > クラス単体テストの設定 > 機能概要 | STEP 2表 #1 |
| section | 第2部 > クラス単体テストの設定 > 拡張例 | STEP 2表 #1 |
| section | 第2部 > 共通設定 > 機能概要 | STEP 2表 #2 |
| section | 第2部 > 共通設定 > 拡張例 | STEP 2表 #2 |
| section | 第2部 > リクエスト単体テストの設定（ウェブアプリケーション） > 機能概要 | STEP 2表 #3 |
| section | 第2部 > リクエスト単体テストの設定（RESTfulウェブサービス） > 機能概要 | STEP 2表 #4 |
| section | 第2部 > リクエスト単体テストの設定（RESTfulウェブサービス） > 拡張例 | STEP 2表 #4 |
| section | 第2部 > リクエスト単体テストの設定（HTTPメッセージング） > 機能概要 | STEP 2表 #5 |
| section | 第2部 > リクエスト単体テストの設定（HTTPメッセージング） > 拡張例 | STEP 2表 #5 |
| section | 第2部 > リクエスト単体テストの設定（Nablarchバッチアプリケーション） > 機能概要 | STEP 2表 #6 |
| section | 第2部 > リクエスト単体テストの設定（Nablarchバッチアプリケーション） > 拡張例 | STEP 2表 #6 |
| section | 第2部 > リクエスト単体テストの設定（MOMによるメッセージング） > 機能概要 | STEP 2表 #7 |
| section | 第2部 > 取引単体テストの設定（HTTPメッセージング） > 機能概要 | STEP 2表 #8 |
| section | 第2部 > 取引単体テストの設定（HTTPメッセージング） > 拡張例 | STEP 2表 #8 |
| section | 第2部 > 取引単体テストの設定（MOMによるメッセージング） > 機能概要 | STEP 2表 #9 |
| section | 第2部 > 取引単体テストの設定（MOMによるメッセージング） > 拡張例 | STEP 2表 #9 |
| section | 第2部 > マスタデータ復旧機能 > 拡張例 | STEP 2「マスタデータ復旧機能の拡張例0件も検査に引っかかる」 |
| section | 第3部 > テストデータの書き方 > 機能概要 | STEP 2表 #10 |
| section | 第3部 > テストデータの記載例 > 機能概要 | STEP 2表 #11 |
| section | 第3部 > リクエスト単体テスト（HTTPメッセージング） > 機能概要 | STEP 2表 #12 |
| section | 第3部 > 取引単体テスト（ウェブアプリケーション） > 機能概要 | STEP 2表 #13 |
| section | 第3部 > 取引単体テスト（Nablarchバッチアプリケーション） > 機能概要 | STEP 2表 #14 |
| section | 第3部 > 取引単体テスト（HTTPメッセージング） > 機能概要 | STEP 2表 #15 |
| section | 第4部 > テストデータ変換ツール > 導入 | STEP 2表 #16 |

28行すべてに対応する記述が作業指示にあり、逆に実測にない項目（作業指示にあるのに
検出されないもの）も0件。過不足なし。
