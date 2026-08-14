# 作業指示 — 週末の連続作成キュー（user review を挟まずに21ページ書く）

宛先: CC

## 0. このタスクの目的と終了条件

**残り21ページの「初版と自己レビューまで」を、user review を挟まずに順番に片づける。これで第2部〜第4部の全ページが揃う。**

Kiyo さんは週明けまで不在である。承認は返ってこない。**承認を待つ状態を作らないこと。** 1ページずつ「初版 → 4観点レビュー → 是正 → ゲート → 記録 → コミット → 次のページ」で完結させ、キューの先頭から順に進む。

**終了条件は、`#27-00`（スタブ一括作成）と21ページすべてがコミット済みであること。** 週明けにレビュー役が全ページを独立検証し、そのあと Kiyo さんがまとめて user review を行う。

**このタスク番号は `#27` とする。** キュー内の各ページはサブ項目（`#27-00` 〜 `#27-21`）として `steering.md` に持つ。ページごとにタスクを起こさない。

**10ページには個別指示がある。着手したら本書より個別指示を優先する。** 食い違ったら個別指示が正である。

| 個別指示 | 対象 |
|---|---|
| `ntf-doc-27-small-3rd.md` | `#27-07`・`#27-10`・`#27-11`・`#27-15`（出典50行未満の第3部4ページ） |
| `ntf-doc-27-db-queue.md` | `#27-16`〜`#27-18`（テーブルをキューとして使ったメッセージング3ページ） |
| `ntf-doc-27-large-pages.md` | `#27-19`〜`#27-21`（出典500行超の3ページ） |

## 0-1. 着手前にやること（`#27-01` より先に、この順で）

**`#27` のエントリはそのまま使う。取り消さない。** `fadec16` で起こしたキューは作業指示より前に書いたものだが、エントリ自体は残してよい。中身だけ作り直す。

1. **未コミットの作業指示4本を、中身を変えずにコミットする。** 現在 `ntf-doc-weekend-queue.md` が変更済み、`ntf-doc-27-small-3rd.md`・`ntf-doc-27-db-queue.md`・`ntf-doc-27-large-pages.md` が未追跡である。**4本ともユーザー資材であり、1バイトも編集しない。** コミットせずに進むと、以降の作業で失われる可能性がある。件名は `chore: #27 の作業指示4本を受け入れる`。

2. **`steering.md` の `#27` キューを作り直す。** 現在登録されている18件は**番号も並び順も本書と食い違っており、そのまま走らせると個別指示が別のページに当たる。** 例えば現在の `#27-16`〜`#27-18` はコンポーネント単体テスト・リクエスト単体テスト（ウェブアプリケーション）・エンティティ単体テストだが、本書の `#27-16`〜`#27-18` はテーブルをキューとして使ったメッセージングの3ページである。**既存18件を破棄し、本書 §3 のキュー表（`#27-00` ＋ 21ページ）をそのまま写す。** 見出しも「週末の連続作成キュー（`#27-00` ＋21ページ。user review を挟まない）」に直す。

3. **`steering.md` の `Rules` に、`#27` 用の1行を足す。** 現在 `steering.md:44` に「user review の承認を受けるまで次タスクに着手しない」がある。**この規則は本書 §1-1「user review を待たない」と正面から矛盾しており、この矛盾を残したまま走ると、1ページごとに承認待ちで止まる。** 次の1行を `Rules` の末尾に足すこと。

   > - **`#27` のサブ項目（`#27-00`〜`#27-21`）はタスクではない。`#27` 全体が1タスクである。** サブ項目の境界で user review を待たず、次のサブ項目に着手する。上の「user review の承認を受けるまで次タスクに着手しない」はタスク単位の規則であり、サブ項目の境界には適用しない（`#27` の作業指示 `ntf-doc-weekend-queue.md` §1-1 による）。

   rn プラグイン自身も `references/task-execute-workflow.md` で「The per-task boundary is **not** a user gate for ordinary build tasks」と規定しており、ユーザーが署名するのは Plan / Design / Evaluation の3ゲートだけである。上の1行はその規定に戻すものである。

4. **`#27-00` に着手する。** 以降は §3 の順に進む。

## 1. 止まらないための規則（最重要）

**この節が守られないと、週末の時間がまるごと無駄になる。**

1. **user review を待たない。** `/rn:ty` も `/rn:gm` も来ない。1ページ終えたら次のページに着手する。
2. **判断が必要になっても止まらない。** その場で**最も出典に忠実な選択**を採って書き、判断の内容と採った選択を `reviews/page-*.md` の「判断待ち」節に記録して先へ進む。週明けにまとめて判定する。
3. **規約ファイルを書き換えない。** `design.md`・`style.md`・`mapping/glossary.md`・`mapping/vocabulary.md` は変更しない。変更が要ると判断した場合も、そのページは**現行の規約のまま**書き、必要な変更を `decide` として記録するだけにする。規約を変えると後続の全ページに波及し、週明けに巻き戻せない。
4. **`mapping.csv` を直接編集しない。** SPLIT や再割当が要る場合は `_batch/*.csv` を1本足して再生成する（`#20`・`#26` と同じ手順）。
5. **`glossary.md` §5.15 の証拠一覧は書き換えない。** 参照するときは行番号ではなく節見出しで指す。
6. **ゲートが赤くなったら、そのページを `blocked` として記録し、次のページへ進む。** そのページで粘らない。
7. **是正ラウンドが3回を超えたら、その時点の版をコミットして次へ進む。** 残った指摘は `decide` に上げる。`#24` は4ラウンド回ってその日の大半を使った。週末にそれをやると後続が止まる。
8. **セッションが切れたら `/rn:dn` で止める。** State の `Next` に**次に着手すべきキュー番号（例: `#27-07`）**を必ず書く。Kiyo さんが見に来て `/rn:up` する。
9. **作業ディレクトリの外を見に行かない。** 出典・実装・規約はすべてこのリポジトリと `/home/tie303177/work/nablarch/` 配下の参照リポジトリにある。
10. **各ページの着手時に、本書と該当する個別指示を読み直す。** 長時間の連続稼働では自動圧縮が走り、本書の内容がコンテキストから落ちる。**記憶ではなくファイルを読み直してから書き始めること。** 圧縮が起きても、この規則さえ守れば作業は狂わない。

## 2. この指示が先回りして答えている判断

**以下はレビュー役が決めた。CC は判断せずこのとおりにする。**

- **ページ先頭ラベルは `style.md` S-08 の一覧から引く。** 新たに考案しない。34ページ分が確定済みである。
- **第2部のページは「使用方法」のみ必須**（`style.md:45-47`）。「機能概要」「拡張例」は出典が無ければ見出しごと置かない。置く場合の順は「機能概要 → 使用方法 → 拡張例」。
- **リード文は目次の直後、最初のL2見出しより前に置く**（`style.md` S-02）。見出しは付けない。
- **`#27-09` 取引単体テスト（MOM）・`#27-10` 取引単体テスト（HTTPメッセージング）の2ページは、リード文で「テスト対象がウェブアプリケーションであり、そのアプリケーションが（HTTP）同期応答メッセージ送信処理を伴う場合」という前提を明示する**（`design.md:125`）。**この規定は第3部のこの2ページだけに掛かる。他のページに広げない。** 同じ `design.md:125` が、`#27-09` だけが自動実行とモックアップの両方を抱え、`#27-10` には自動実行の説明が無いことも実測付きで述べている。
- **`#27-01` 以降は、すべて既存ファイル（スタブ）への追記である。新規作成ではない。** 既に6本のスタブがあり（`setup/junit5_extension.rst`・`setup/master_data_restore.rst`・`implementation/request_unit_test/web.rst`・`tools/testdata_converter.rst`・`tools/master_data_tool.rst`・`tools/html_check_tool.rst`）、残り15本は `#27-00` で作る。**スタブが持つページ先頭ラベルとタイトルを変えない。**
- **第4部の4ページのうち2ページは「導入」を持たない。** `design.md` §5 が明記している — `#27-06` HTMLチェックツール（リクエスト単体テストに標準で組み込まれ、インストール手順を持たない）と `#27-03` テストデータ変換ツール（出典全362行に該当記述が無いことを実測済み）。**残る `#27-04`・`#27-05` は、現行解説書の本体ページとインストールガイドの2ページを1ページに統合し、「導入」セクションに収める。**
- **`setup/junit5_extension.rst` の出典に第1部の `01_Abstract.rst` が混ざっているのは食い違いではない。** `design.md:157-178`（見出し「モジュール一覧は第1部に置かない。『稼動環境』は対応バージョンの premise 1文＋`:ref:`のみとする」）が `#6` の「依存関係を第1部に集約する」方針そのものを取り消し、`current-0180`・`current-0267` を第2部「JUnit 5用拡張機能」の使用方法へ差し戻したと明記している。そのまま第2部のページに書く。
- **`implementation/request_unit_test/web.rst` には `how_to_set_token_in_request_unit_test` というラベルを定義する。** 削除された現行解説書のラベルで、`ja/application_framework/application_framework/libraries/db_double_submit.rst:106` がいまも参照している。`style.md` S-08 の命名規則の例外として改名しない。**このページで定義しないと未解決参照が残り続ける。**
- **画像は `<そのページの .rst があるディレクトリ>/images/<ページのファイル名（拡張子なし）>/` に置く**（`design.md:897`）。現行解説書の画像は `guide/` から `git mv` する（`design.md:907`）。該当ページと枚数は §3「画像を持つページ」を見る。
- **設定項目表の「デフォルト値」は、デフォルト設定を読み込んだ実効値を書く**（`design.md` §8）。クラスのフィールド初期値ではない。
- **出典が欠いている、実装上必須の設定は書き足してよい**（`design.md` §8）。根拠の `file:line` と参照コミットハッシュを `reviews/page-*.md` に記録する。参照コミットは `nablarch-testing` = `e21bf67`、`nablarch-testing-yaml` = `190cc9a`。
- **出典と実装が食い違う場合は実装を優先する**（`design.md` §8）。ただし**本体の不具合が疑われる場合は書かずに `decide` に上げる**。`expected_tables:` の `rows: []` が偽陰性になる件（未解決）と同型のものは、仕様どおりに書いて実装の穴を読者に肩代わりさせない。

## 3. 実施順（キュー）

**上から順に進める。順番を変えない。** 小さいページを先に置いてあるのは、規約の運用を早く安定させるためと、途中で止まっても損失を小さくするためである。

出典は `mapping/mapping.csv` を `dest_page` 列で絞って全件取る。**`dest_page` はページのタイトルであってファイルパスではない。** パスで grep すると0件になる。

| # | ページ（`dest_page` の値） | ファイル | 部 | 出典行 | 個別指示 |
|---|---|---|---|---:|---|
| **00** | **未作成15ページのスタブ一括作成**（§3-1） | — | — | — | 本書 §3-1 |
| 01 | マスタデータ復旧機能 | `setup/master_data_restore.rst` | 2 | 193 | |
| 02 | JUnit 5用拡張機能 | `setup/junit5_extension.rst` | 2 | 475 | |
| 03 | テストデータ変換ツール | `tools/testdata_converter.rst` | 4 | 75 | |
| 04 | リクエスト単体データ作成ツール | `tools/request_data_tool.rst` | 4 | 163 | |
| 05 | マスタデータ投入ツール | `tools/master_data_tool.rst` | 4 | 177 | |
| 06 | HTMLチェックツール | `tools/html_check_tool.rst` | 4 | 214 | |
| 07 | 取引単体テスト（RESTfulウェブサービス） | `implementation/deal_unit_test/rest.rst` | 3 | 32 | **small-3rd** |
| 08 | 取引単体テスト（Nablarchバッチアプリケーション） | `implementation/deal_unit_test/batch.rst` | 3 | 168 | |
| 09 | 取引単体テスト（MOMによるメッセージング） | `implementation/deal_unit_test/mom.rst` | 3 | 175 | |
| 10 | 取引単体テスト（HTTPメッセージング） | `implementation/deal_unit_test/http_messaging.rst` | 3 | 33 | **small-3rd** |
| 11 | 取引単体テスト（ウェブアプリケーション） | `implementation/deal_unit_test/web.rst` | 3 | 48 | **small-3rd** |
| 12 | リクエスト単体テスト（RESTfulウェブサービス） | `implementation/request_unit_test/rest.rst` | 3 | 262 | |
| 13 | リクエスト単体テスト（MOMによるメッセージング） | `implementation/request_unit_test/mom.rst` | 3 | 461 | |
| 14 | リクエスト単体テスト（Nablarchバッチアプリケーション） | `implementation/request_unit_test/batch.rst` | 3 | 384 | |
| 15 | リクエスト単体テスト（HTTPメッセージング） | `implementation/request_unit_test/http_messaging.rst` | 3 | 28 | **small-3rd** |
| 16 | リクエスト単体テストの設定（テーブルをキューとして使ったメッセージング） | `setup/request_unit_test/db_queue.rst` | 2 | 0 | **db-queue** |
| 17 | リクエスト単体テスト（テーブルをキューとして使ったメッセージング） | `implementation/request_unit_test/db_queue.rst` | 3 | 0 | **db-queue** |
| 18 | 取引単体テスト（テーブルをキューとして使ったメッセージング） | `implementation/deal_unit_test/db_queue.rst` | 3 | 0 | **db-queue** |
| 19 | コンポーネント単体テスト | `implementation/class_unit_test/component.rst` | 3 | 770 | **large-pages** |
| 20 | リクエスト単体テスト（ウェブアプリケーション） | `implementation/request_unit_test/web.rst` | 3 | 914 | **large-pages** |
| 21 | エンティティ単体テスト | `implementation/class_unit_test/entity.rst` | 3 | 1,344 | **large-pages** |

ファイルパスはいずれも `ja/development_tools/testing_framework/` からの相対である。

### この順番の理由（変えてはいけない依存関係）

**出典の本文には、まだ作っていないページを指す `:ref:` が多数ある。** 削除前の現行解説書（`2e501ad`）のラベル定義を全件索引して `mapping.csv` の割当先と突き合わせた結果、キュー内のページ間に11本の参照関係がある。**そのうち次の4本は、参照先を読まないと本文が書けない性質のものであり、順番で解決してある。**

| このページ | 参照先 | 理由 |
|---|---|---|
| `#27-15` リクエスト単体テスト（HTTPメッセージング） | `#27-13` リクエスト単体テスト（MOM） | 出典が `real_request_test`・`message_sendSyncMessage_test` への参照文しか持たない。**差分ページであり、参照先が無いと書く内容が存在しない** |
| `#27-10` 取引単体テスト（HTTPメッセージング） | `#27-09` 取引単体テスト（MOM） | 同上（`dealUnitTest_send_sync` への参照＋読み替え） |
| `#27-11` 取引単体テスト（ウェブアプリケーション） | `#27-09` 取引単体テスト（MOM） | `current-0142` が `dealUnitTest_send_sync` を参照 |
| `#27-16`〜`#27-18` | `#27-08`・`#27-14` | 導線のみのページで、参照先が本文のすべて |

**残る7本は順番では解決できない。** 参照関係に循環があるためである（リクエスト単体テスト（ウェブアプリケーション）とリクエスト単体テスト（Nablarchバッチアプリケーション）が相互に参照している）。**これが `#27-00` を置く理由である（§3-1）。**

**`#27-19`〜`#27-21` を最後尾に置いてあるのは、ここまでで週末の時間を使い切っても損が出ないようにするためである。** 3ページとも大きいので、1ページに粘らず §1-7 の3ラウンド上限を守る。

### `#27-00` 未作成15ページのスタブ一括作成

**キューの1ページ目に着手する前に、まだ存在しない15ファイルを「ページ先頭ラベル＋タイトル」だけの状態で作り、`toctree` に登録し、1コミットで push する。**

**なぜやるか。** これをやらないと、`#27-01` 以降で書いたページの `:ref:` が未作成ページを指し、フルビルドが `undefined label` を出す。**ゲート G5（新規 warning 0件）が赤になり、§1-6 に従って11ページが `blocked` になる。** スタブを先に置けば、`:ref:` は最初から解決し、G5 は最後まで厳格なまま運用できる。

**前例がある。** `tools/testdata_converter.rst` ほか6ファイルが既に同じ方法で作られている（`design.md:72`、`steering.md` の「前方参照によるスタブページ」）。本手順はそれを残り15ファイルに広げるだけである。

**作る15ファイル**（`ja/development_tools/testing_framework/` からの相対。ラベルは `style.md:372-391` の一覧から引く）

| ファイル | ラベル |
|---|---|
| `implementation/class_unit_test/entity.rst` | `entity_unit_test` |
| `implementation/class_unit_test/component.rst` | `component_unit_test` |
| `implementation/request_unit_test/rest.rst` | `request_unit_test_rest` |
| `implementation/request_unit_test/http_messaging.rst` | `request_unit_test_http_messaging` |
| `implementation/request_unit_test/batch.rst` | `request_unit_test_batch` |
| `implementation/request_unit_test/mom.rst` | `request_unit_test_mom` |
| `implementation/request_unit_test/db_queue.rst` | `request_unit_test_db_queue` |
| `implementation/deal_unit_test/web.rst` | `deal_unit_test_web` |
| `implementation/deal_unit_test/rest.rst` | `deal_unit_test_rest` |
| `implementation/deal_unit_test/http_messaging.rst` | `deal_unit_test_http_messaging` |
| `implementation/deal_unit_test/batch.rst` | `deal_unit_test_batch` |
| `implementation/deal_unit_test/mom.rst` | `deal_unit_test_mom` |
| `implementation/deal_unit_test/db_queue.rst` | `deal_unit_test_db_queue` |
| `setup/request_unit_test/db_queue.rst` | `request_unit_test_setting_db_queue` |
| `tools/request_data_tool.rst` | `request_data_tool` |

**`setup/deal_unit_test/db_queue.rst` は作らない。**`design.md:386`・`:891` が意図した非対称であると明記している。欠落と誤認しないこと。

**中身は既存スタブ（`tools/master_data_tool.rst` など、いずれも4行）と同じ形にする。** ラベル行・空行・タイトル・下線だけである。実物を開いて形を合わせること。

**`toctree` の並びは `design.md:837-886` のファイルツリーの順にする。** `setup/index.rst`・`implementation/index.rst`・`tools/index.rst` の3本をここで最終形にしておけば、以降のページ作成コミットは自分の `.rst` と記録ファイルだけを触ることになる。

**この時点でフルビルドを1回通す。** `build succeeded` で、警告が既知の1件（`db_double_submit.rst:108` の `undefined label: how_to_set_token_in_request_unit_test`）だけであることを確認してから `#27-01` に進む。ここで増えていたらスタブの作り方が間違っている。

**`#27-20` に到達すると、解説書全体で唯一残っているビルド警告が0件になる。** `implementation/request_unit_test/web.rst` が `how_to_set_token_in_request_unit_test` を定義するためである。詳細は個別指示 `ntf-doc-27-large-pages.md` §3-1。**スタブでは解決しない。** これはページ先頭ラベルではなく、ページ内の節ラベルだからである。

### 画像を持つページ（実測）

**12ページが出典に画像を持つ。合計53枚である。** 移動元は `guide/` 配下に現存している（実測108ファイル）。**該当ページのタスクで `git mv` する**（`design.md:907`）。置き場所は `<そのページの .rst があるディレクトリ>/images/<ページのファイル名（拡張子なし）>/`（`design.md:897`）。既存例は `setup/images/common/`（1枚）と `setup/request_unit_test/images/web/`（4枚）である。

| ページ | 枚数 |
|---|---:|
| `#27-01` マスタデータ復旧機能 | 2 |
| `#27-04` リクエスト単体データ作成ツール | 5 |
| `#27-05` マスタデータ投入ツール | 5 |
| `#27-06` HTMLチェックツール | 1 |
| `#27-09` 取引単体テスト（MOM） | 4 |
| `#27-10` 取引単体テスト（HTTPメッセージング） | 1 |
| `#27-12` リクエスト単体テスト（RESTful） | 1 |
| `#27-13` リクエスト単体テスト（MOM） | 4 |
| `#27-14` リクエスト単体テスト（Nablarchバッチ） | 3 |
| `#27-19` コンポーネント単体テスト | 7 |
| `#27-20` リクエスト単体テスト（ウェブアプリケーション） | 6 |
| `#27-21` エンティティ単体テスト | 14 |

**出典の `.. image::` のパス表記は `_images/`・`./_image/`・`../_image/` の3種が混在している。** 実ファイルの所在を `find` で確かめてから `git mv` すること。

### `#27-09` にある出典分割（`#27-19` の `02_DbAccessTest.rst` と同型）

**`current-0156` は3分割されており、このページに来るのは `-b`（`03_DealUnitTest/send_sync.rst:173-198`）だけである。** `-a`（`:67-172`）と `-c`（`:199-220`）は `テストデータの書き方` に行っており、そのページは既に作成・承認済みである。**`:67-220` をまとめて読んで写すと、公開済みのページと同じ内容が二重に載る。** `-b` の範囲だけを本文にし、前後は `:ref:` で `testdata_notation` へ送る。

## 4. 1ページあたりの手順

`#25`・`#26` と同じ共通 Steps でよい。要点だけ再掲する。

1. `mapping.csv` を `dest_page` で絞り、`DROP` を除く全行を取る。`src_file` と `src_body_start`〜`src_body_end` を**実際に開いて読む**。要約や `note` 欄を根拠にしない。
2. 出典が参照している実装を、参照リポジトリで確かめる。`nablarch-testing` は `e21bf67`、`nablarch-testing-yaml` は `190cc9a`。
3. ページ先頭ラベルを `style.md` S-08 から引き、リード文を置き、節を組む。
4. 4観点レビュー（QA / Design / Craft / Verification）を回す。**push 前に是正まで畳む。** `#23`・`#25`・`#26` と同じく、是正を別コミットに割らなくてよい。
5. §5 のゲートを全件通す。
6. `checks/task-27.md` にゲート結果を、`reviews/page-<ラベル>.md` にレビュー結果と `decide` を記録する。
7. 1ページ1コミットで push する。件名は `docs: <ページ名>のページを作成する — #27-NN`。`#27-00` だけは `chore: 未作成15ページのスタブを作成して toctree に登録する — #27-00` とする。

## 5. 毎ページのゲート

**全件通してからコミットする。1つでも赤ければ §1-6 に従って `blocked` にして次へ進む。**

| | 内容 |
|---|---|
| G1 | `git status --porcelain` の**全件**を確認する。ディレクトリで絞らない。`git diff` は未追跡ファイルを出さないので母集合に使わない |
| G2 | 禁止ファイルの差分が0行 — `design.md`・`mapping/style.md`・`mapping/glossary.md`・`mapping/vocabulary.md`・`ja/conf.py`・`mapping/input/` |
| G3 | `locales/ja/LC_MESSAGES/sphinx.mo` がコミットに含まれていない。ビルドが再生成するので `git checkout --` で戻す |
| G4 | `verify_mapping.py` が exit 0。`mapping.csv` を触った場合は `_batch` からの再生成がバイト一致すること |
| G5 | Docker フルビルドが `build succeeded`。**新規の warning が0件。** 既知は `db_double_submit.rst:108` の `undefined label` 1件のみで、`#27-20` に到達するとこれも0件になる。**`#27-00` でスタブを作ってあるため、未作成ページを指す `undefined label` は出ない。出たらスタブの作り漏れなので、そのページを `blocked` にせず先にスタブを直す。** 実測でフルビルドは約97秒である |
| G6 | 禁止語0件 — `不具合`・`バグ`・`将来`・`修正され` |
| G7 | ページ先頭ラベルが `style.md` S-08 の一覧と一致する |
| G8 | 見出し下線がタイトルの表示幅以上（`style.md:195`）。同じページ内で基準幅を揃える |
| G9 | 本文中の `:ref:` の飛び先が実在し、リンク文字列が飛び先の見出しと一致する |
| G10 | 出典の全行が、本文に反映されたか意図して落としたかのどちらかに分類され、落とした分は理由付きで `reviews/page-*.md` に記録されている |
| G11 | **`disposition=REFERENCE` の行が本文を持っていない**（`design.md:722`）。`:ref:` の導線に変換するだけで、節として起こさない。該当は9ページ12件 — `#27-05`（`current-0355`）・`#27-09`（`current-0135`・`current-0136`）・`#27-10`（`current-0138`）・`#27-12`（`current-0121`）・`#27-13`（`current-0049`・`current-0104`・`current-0330`）・`#27-14`（`current-0035`）・`#27-15`（`current-0064`・`current-0069`）・`#27-19`（`current-0196`）・`#27-21`（`current-0020`） |
| G12 | **同じ `src_file` の同じ行範囲が、作成済みページと二重に載っていない。** `mapping_id` に `-a`／`-b`／`-c` の枝があるときは、**自分の枝の行範囲だけ**を本文にする。相方の行き先が作成済みページなら `:ref:` で送る。**該当は `#27-09`（`current-0156-b`）と `#27-19`（`current-0184-a`・`current-0185-a`）の2ページのみ** — いずれも相方は作成済みの `テストデータの書き方` |
| G13 | 本ページの `.. image::` が指すファイルが実在し、`git mv` の移動元が `guide/` 配下に残っていないこと（画像を持つページのみ） |

## 6. 記録の書き方

- **`checks/task-27.md` は1本にまとめる。** ページごとに節を分ける。ページごとにファイルを作らない。
- **`reviews/page-<ラベル>.md` はページごとに1本。** これは従来どおり。
- **`steering.md` は1ページ終えるごとに `#27-NN` の消し込みだけ書く。** 経緯や試行錯誤を残さない。
- **`decide`（週明けに判定してほしい項目）は `reviews/page-*.md` の「判断待ち」節に書く。** 上申文に `file:line` を引くときは、**書く前に必ず実物を開いて確かめる。** `#21` は開かずに書いた行番号が禁止領域を指していた。

## 7. 進捗の見え方

Kiyo さんは数時間おきに様子を見に来る。**いま何番まで終わったかが `steering.md` の State を見れば分かる状態を保つこと。** `Next` には必ず次のキュー番号を書く。止まっていた場合は `/rn:up` で再開される。

## 8. 補足 — `#26` の申し送り1件

`#26` は承認する。本文の変更は不要である。ただし1件だけ週明けに扱う項目がある。

`setup/common.rst` に追加した `nablarch-testing-yaml` の依存関係は、バージョンを書かない形になっている。他のページの記述（`setup/request_unit_test/rest.rst:24-37` など）と揃っており、書き方としては正しい。ただしこのモジュールは `1.0.0-SNAPSHOT` で（`nablarch-testing-yaml` の `pom.xml:17` を実測）、BOM に収録されるまでは読者がそのまま貼っても解決できない。**リリース時に BOM 収録を確認する項目として `reviews/page-testing_framework_common.md` に申し送りを残すこと。** 本文はいま変えなくてよい。
