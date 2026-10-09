# 意味的差分検証器 (semdiff)

nablarch-document のビルド環境現代化 (cmd_707) において、新旧2つのビルド済み
HTMLツリーを意味レベルで比較し、合否条件

- (a) テキストの欠損・欠落・文字化けが **1件もない** こと
- (b) 内部リンク・アンカー・画像・ダウンロード資材の破損が **1件もない** こと

を機械検証するツール。

## 構成

| ファイル | 役割 |
|---|---|
| `semdiff.py` | 検証器本体 (V1テキスト保全 / V2リンク保全 / V3仕分け / 被覆率canary) |
| `canary_suite.py` | 検証器の自己検証 (故意破壊テスト: 真陽性9 + 真陰性5 + 被覆率全数) |

依存: Python 3.12 + lxml (ホスト環境で確認済み)。

## 使い方

```bash
# 合否検証 (旧ツリー vs 新ツリー)。exit 0=PASS / 2=意味的差異あり
python3 semdiff.py verify OLD_TREE NEW_TREE --json report.json

# 本文抽出セレクタの被覆率検査 (穴1対策canary)。exit 0=100%被覆
python3 semdiff.py coverage TREE --json coverage.json

# 検証器の自己検証 (基準ビルドを故意破壊して真陽性/真陰性を確認)
python3 canary_suite.py BASELINE_TREE WORK_DIR
```

ツリーは `_build/html` を指す (ja がルート直下、`en/` が英語版という
本リポジトリの出力配置のまま丸ごと比較できる)。

## 検証内容

### ページの3区分

| 区分 | 判定方法 |
|---|---|
| 通常ページ (rst由来・テーマ構造あり) | V1/V2 意味比較 |
| 逐語コピーページ (`_static/**/*.html`、yuidoc生成のJS APIドキュメント等 約320枚) | Sphinxは変換せず複製するため **バイト同一 (より厳格)** で照合 |
| 生成系UIページ (genindex.html / search.html) | 存在のみ確認 (本文はrst由来でないため) |

### V1: テキスト保全 (包含照合)

- 本文コンテナ `*[role="main"]` からブロック要素単位で可読テキストを抽出。
  script/style/パーマリンク(¶)は除去。正規化は **連続空白の畳み込みのみ**
  (Unicode正規化は情報改変になり得るため不採用 = 設計書の判断を踏襲)。
- 旧ページの各テキスト片が新ページに全量存在するか照合 (多重集合の
  完全一致 → だめならページ全文への部分文字列出現回数で救済)。
  見つからない片は `text-missing` として **NG**。
- 新側にのみある追加テキスト (テーマUI文言等) は許容 (包含照合)。
- 文字はバイト等価で比較するため **文字化けも text-missing として検出** される。

### V2: リンク・アンカー・画像・DL資材の保全

- 本文域から `a[href]` / `img[src]` / `object[data]` 等を全数列挙。
- **資材 (画像・DL資材) は「各ビルド内で解決したhref (参照経路)」をキーに
  内容SHA-256の多重集合で照合する。新旧間の絶対ファイル名一致は判定に
  使わない** (Sphinxは版間でファイル名ハッシュ規則を変えることがあるため。
  ファイル名だけ変わって内容同一なら合格、内容が失われれば
  `asset-content-lost` でNG)。
- 内部リンク・アンカーは「新ビルド内で解決するか」(サイト内自己整合) を
  検査。**旧ビルドに元から存在する破損は除外し、新規リグレッションのみNG**
  (`unresolved-page-link` / `unresolved-anchor` / `unresolved-asset`)。
- 旧IDが新ビルドに存在しない差分 (外部からの深リンク切れの可能性) は
  合否に含めず `report_only.anchor_id_diffs` に全件記録 (設計書 §4.3)。
- 外部URL (`http(s)://`) は「旧と同一のURL文字列が新にも出力されている」
  ことのみ確認 (`external-url-lost`)。到達性は linkcheck の既存運用に委ねる。

### V3: 仕分け

各ページを NG (意味的差異) / gray (テキスト移動・本文コンテナ未検出等の
人手判定) / display-only (テキスト完全一致で構造のみ差) / byte-identical /
text-pass (新側追加のみ) に分類し、JSONレポートに全件出力する。

### 穴1対策: 本文抽出セレクタの被覆率検査 (`coverage`)

抽出セレクタが本文を取り漏らすと、その領域の本物の欠損を V1 が見逃す
(false-PASS)。これを防ぐため、全ページの全可読テキストノードについて
「本文コンテナ配下 ∪ 既知チューム (nav / breadcrumbs / footer / 検索UI /
サイドバー等の許容リスト) 配下」のいずれかに属することを構造的に検査し、
どちらにも属さないテキストが1ノードでもあれば NG とする。
基準ビルド全988ページで被覆率100%を確認済み (下記結果)。

## 自己検証 (canary) の内容

真陽性 (破壊を検出できること):

| ケース | 破壊内容 | 期待NG |
|---|---|---|
| TP1 | 新側の一文の後半を削除 | `text-missing` |
| TP2 | 新側からページ1枚削除 | `page-missing` |
| TP3 | 新側から参照画像ファイル削除 | `asset-content-lost` / `unresolved-asset` |
| TP4 | 新側の参照画像を別内容に差替 | `asset-content-lost` |
| TP5 | 新側の内部リンクを実在しない先へ改変 | `unresolved-page-link` / `page-link-lost` |
| TP6 | 新側でリンク先アンカーidを削除 | `unresolved-anchor` |
| TP7 | 新側からDL資材(`_downloads`)を削除 | `asset-content-lost` / `unresolved-asset` |
| TP8 | 新側本文に文字化け(U+FFFD)を注入 | `text-missing` |
| TP9 | 本文コンテナ外にテキストを注入 | coverage検査が被覆漏れ検出 |

真陰性 (無害な差異を誤検出しないこと):

| ケース | 無害な差異 | 期待 |
|---|---|---|
| TN1 | 完全同一コピー | PASS (NG 0件) |
| TN2 | span分割・class追加・本文域へのUI文言追加 | PASS |
| TN3 | 画像ファイル名変更+href整合更新 (内容同一) | PASS (**穴2対策の実証**) |
| TN4 | アンカーidをビルド内で整合的に改名 | PASS + report-onlyに記録 |
| TN5 | 旧側から削除 (旧⊂新の方向) | PASS (包含照合の仕様確認) |

## P2-1 実行結果 (2026-07-24)

- 基準ビルド: origin/develop `c241906` を旧環境 (リポジトリ同梱Dockerfile =
  python:3.10.20-slim + Sphinx 1.3.6 + parser互換シム) でja+enフルビルド。
  **2378ファイル / ja 495 + en 493 HTML / 全17トップレベルセクション /
  _static・ルートindexあり** — 設計書§4.1の実測値と完全一致。
  保全先: セッションscratchpad `cmd707p21/nabdoc-baseline/_build/html`
  (root所有のため誤改変からも保護。恒久複製は不要の方針)。
- 自己検証 (基準 vs 基準): PASS。通常666ページ全byte-identical・NG 0件。
- 被覆率検査: 全ページ 100.0000%・被覆漏れ0ノード。
- canary全ケースの結果は本ディレクトリの `canary_results.txt` を参照。

## P2-3 での使い方 (新環境ビルドへの本適用)

```bash
python3 semdiff.py coverage NEW_TREE --json cov_new.json   # 新テーマでも被覆100%を先に確認
python3 semdiff.py verify OLD_TREE NEW_TREE --json report.json
# exit 0 かつ report.json の ng==[] が合格条件。gray は全件人手判定へ。
```
