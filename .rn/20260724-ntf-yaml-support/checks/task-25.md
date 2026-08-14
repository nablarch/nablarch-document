# `#25` self-check — 取引単体テストの設定（HTTPメッセージング）

対象: `ja/development_tools/testing_framework/setup/deal_unit_test/http_messaging.rst`（新規、35行）と `ja/development_tools/testing_framework/setup/index.rst` の `toctree` 1行追加。
着手時の HEAD: `a46ec49`（`chore: rn:ty — #23 を承認で閉じてエントリを圧縮し、#25 のエントリを起こす`）。

## ゲート1 — 着手時の `git status --porcelain`（実行順の先頭）

`a46ec49` を push した直後に実行し、**0件（クリーン）**。

## ゲート2 — 個別の作業指示を出す条件の判定

`steering.md` `#9〜` の3条件のいずれにも当たらないため、共通 Steps のみで進めた。

| 条件 | 判定 | 根拠 |
|---|---|---|
| (1) 出典が500 lines を超える | 該当しない | `mapping.csv` の当該行 `lines=20` |
| (2) `design.md` の確定事項どうし、または `design.md` と `mapping.csv` が食い違う | 該当しない | `design.md:198`・`:208`（取引単体テストの設定は実データのある3処理方式のみページ化）・`:932`（`setup/deal_unit_test/http_messaging.rst`）と `mapping.csv` の割当が一致 |
| (3) 出典が0行 | 該当しない | 出典 `:50-69` に本文がある |

## ゲート3 — マッピング全件（母集合を先に固定）

`csv.DictReader` で `mapping.csv` を全件読み、`dest_page` の**完全一致**で抽出した。母集合は全595行。`grep` でホワイトリスト的に絞っていない。

```
$ python3 -c "import csv; rows=list(csv.DictReader(open('mapping/mapping.csv'))); ..."
総行数: 595
当該dest_page: 1
current-0140 MOVE .../05_UnitTestGuide/03_DealUnitTest/http_send_sync.rst 50 69 20 user 使用方法
```

表記ゆれの確認として `取引単体テスト` を含む `dest_page` を全8種列挙し、当該ページが1種であることを確認した（`取引単体テストの設定（HTTPメッセージング）` / `…（MOMによるメッセージング）` / `…（RESTfulウェブサービス）` / `取引単体テスト（HTTPメッセージング）` / `…（MOMによるメッセージング）` / `…（Nablarchバッチアプリケーション）` / `…（RESTfulウェブサービス）` / `…（ウェブアプリケーション）`）。

### 反映先の対応表（`current-0140` の出典 `:50-69` を全件）

出典は `git show origin/develop:ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/http_send_sync.rst` で読んだ。

| 出典 | 内容 | 反映先 |
|---|---|---|
| `:51` | 「通常、これらの設定はアーキテクトが行うものでありアプリケーションプログラマが設定する必要はない。」 | `:15-17`（`.. tip::`） |
| `:54-55` | 小見出し「モックアップクラスの設定」 | `:19-20`「モックアップクラスを登録する」 |
| `:57` | 「コンポーネント設定ファイルに、取引単体テストで使用するモックアップクラスを設定する。」 | `:21` の末尾「コンポーネント設定ファイルに、次のとおり登録する。」 |
| `:59-65` | XMLコード例（コメント `<!-- HTTP通信用クライアント -->`、`name="defaultMessageSenderClient"`、`class="nablarch.test.core.messaging.MockMessagingClient"`、`charset="Shift-JIS"`） | `:23-29`（4要素すべて一致。出典のXMLは開始タグ末尾に余分な空白があるが、それは落とした） |
| `:67-68` | 「`charset` に文字コード名を指定することでログに出力する文字コードを変更できる。通常は省略可能で、省略した場合はUTF-8が使用される。」 | `:33` |

**落ちは0件。** 逆方向（ページ→出典）で典拠が出典に無いのは3件で、いずれも実装で裏づけを取った（`reviews/page-deal_unit_test_setting_http_messaging.md`「出典に無い追記」）。

### 越境していないことの確認

同じ出典ファイルの他行（`current-0137` DROP／`current-0138` `:6-15` 第3部機能概要／`current-0139` `:24-46` 第3部使用方法）の内容は本ページに取り込んでいない。Excelの書き方・画像・電文フォーマットの記載方法はいずれも不在。**判定: PASS。**

## ゲート4 — ページ先頭ラベル

`style.md:365` の一覧から引いた `deal_unit_test_setting_http_messaging` を使用。新たに考案していない。`grep -rn "^\.\. _deal_unit_test_setting_http_messaging:" ja/` は1件のみで重複0件。**判定: PASS。**

## ゲート5 — `verify_mapping.py`

```
$ python3 mapping/tools/verify_mapping.py   → exit 0 / OK: no errors
Loaded 595 rows from mapping.csv
lines total (all rows): 12986
lines total (excluding DROP): 11983
```

`#23` 時点（595行 / 12,986 / 11,983）から**不変**。`mapping/` に差分は無い。**判定: PASS。**

## ゲート6 — Docker フルビルド

README「環境構築」＞「Docker」の手順に従い、既存イメージ `nablarch-document-build` で3回実行した（初版・是正後・是正取り消し後）。

```
$ docker run --rm -v /home/tie303177/work/nablarch/nablarch-document:/root/document \
    nablarch-document-build /bin/bash -c \
    "cd /root/document; sphinx-build -a -d _build/.doctrees/ja -b html ja _build/html"
```

3回とも `build succeeded, 1 warning.` / `exit 0`。警告は既知の1件のみで**新規0件**。

```
/root/document/ja/application_framework/application_framework/libraries/db_double_submit.rst:108:
  WARNING: undefined label: how_to_set_token_in_request_unit_test
```

この警告は `checks/task-07.md`「リンク切れになる参照」の残り1件（`#last` で解消する）であり、本タスクの追加によるものではない。**判定: PASS。**

## ゲート7 — 4観点レビューと検証ラウンド

ラウンド1 は4観点（A:網羅性 / B:トンマナ / C:用語 / D:整合性）を**それぞれ別のサブエージェント**で実施。判定は A FAIL（`must` 1）／B PASS／C PASS／D FAIL（`must` 1）。重複除去後12件を triage し、4件を是正した。

続けて**是正差分に限定した検証観点**を別のサブエージェントで1回実施。判定 FAIL（`must` 1・`should` 4・`info` 2）で、**是正1・2 を取り消し、是正4 を修正**した。本文に残った是正は2件。

指摘→対応の対応表（全件）は `reviews/page-deal_unit_test_setting_http_messaging.md` に記録した（Rules「レビュー監査の記録は `reviews/page-*.md` にのみ書く」に従う）。**未対応で残した指摘は8件**で、うち3件は**判断待ち**として user review に上げる（同ファイル「判断待ち」節）。**判定: 実施・記録は完了。未対応の指摘の扱いはユーザー判断を待つ。**

## ゲート8 — 差分の範囲（`commit & push` の直前）

母集合は `git status --porcelain` の**全件**（`ja/` や特定ディレクトリに絞っていない）。

| # | 状態 | パス | 予定していた変更か |
|---|---|---|---|
| 1 | ` M` | `ja/development_tools/testing_framework/setup/index.rst` | 該当（`toctree` 1行追加） |
| 2 | `??` | `ja/development_tools/testing_framework/setup/deal_unit_test/http_messaging.rst` | 該当（新規ページ） |
| 3 | `??` | `.rn/20260724-ntf-yaml-support/reviews/page-deal_unit_test_setting_http_messaging.md` | 該当（新規レビュー記録） |
| 4 | `??` | `.rn/20260724-ntf-yaml-support/checks/task-25.md` | 該当（本ファイル） |

**予定外は0件。判定: PASS。**

### このゲートが検出した1件

**`locales/ja/LC_MESSAGES/sphinx.mo` の混入を検出し、`commit` 前に復元した。** Docker フルビルドのたびに再生成されるファイルで、Rules は「再生成された時点で戻す」と定めている。今回はビルドコマンドに `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を連結していたにもかかわらず戻っていなかった。**原因はシェルの作業ディレクトリが `.rn/20260724-ntf-yaml-support/` に移っており、相対パス指定の `git checkout` が対象を解決できずに失敗していたこと**（`2>/dev/null` を付けていたため失敗が見えなかった）。リポジトリルートで絶対パスを使って実行し直して復元した。

**`#26` 以降への申し送り**: ビルド直後の復元は、**リポジトリルートで実行するか絶対パスで指定し、`git status --porcelain` で消えたことを確認する**。エラーを握りつぶさない。

## 判断待ち（user review でユーザーに上げる3件）

1. `sendSyncTestData` と `messagingTestDataParser` の設定の置き場所（本ページの手順だけではモックアップクラスが動作しない）
2. 同一コンポーネント名 `defaultMessageSenderClient` の衝突（リクエスト単体テストと取引単体テストの併用時）
3. リード文に「テスト対象がウェブアプリケーションであり、HTTPメッセージ送信を伴う場合」という前提を明示するか（明示するなら `design.md:125` の適用範囲を第2部にも広げる改訂が要る）

いずれも詳細と選択肢は `reviews/page-deal_unit_test_setting_http_messaging.md`「判断待ち」節に記録した。
