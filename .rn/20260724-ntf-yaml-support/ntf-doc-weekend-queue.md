# 作業指示 — 週末の連続作成キュー（user review を挟まずに18ページ書く）

宛先: CC

## 0. このタスクの目的と終了条件

**残り18ページの「初版と自己レビューまで」を、user review を挟まずに順番に片づける。**

Kiyo さんは週明けまで不在である。承認は返ってこない。**承認を待つ状態を作らないこと。** 1ページずつ「初版 → 4観点レビュー → 是正 → ゲート → 記録 → コミット → 次のページ」で完結させ、キューの先頭から順に進む。

**終了条件は、キューの18ページすべてがコミット済みであること。** 週明けにレビュー役が全ページを独立検証し、そのあと Kiyo さんがまとめて user review を行う。

**このタスク番号は `#27` とする。** キュー内の各ページはサブ項目（`#27-01` 〜 `#27-18`）として `steering.md` に持つ。ページごとにタスクを起こさない。

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

## 2. この指示が先回りして答えている判断

**以下はレビュー役が決めた。CC は判断せずこのとおりにする。**

- **ページ先頭ラベルは `style.md` S-08 の一覧から引く。** 新たに考案しない。34ページ分が確定済みである。
- **第2部のページは「使用方法」のみ必須**（`style.md:45-47`）。「機能概要」「拡張例」は出典が無ければ見出しごと置かない。置く場合の順は「機能概要 → 使用方法 → 拡張例」。
- **リード文は目次の直後、最初のL2見出しより前に置く**（`style.md` S-02）。見出しは付けない。
- **第3部の `取引単体テスト（MOMによるメッセージング）`・`取引単体テスト（HTTPメッセージング）` の2ページは、リード文で前提を明示する**（`design.md:125`）。この規定は第3部のこの2ページだけに掛かる。他のページに広げない。
- **前方参照スタブがあるページは、新規作成ではなく既存ファイルへの追記として扱う。** 該当は `setup/junit5_extension.rst`・`setup/master_data_restore.rst`・`implementation/request_unit_test/web.rst`・`tools/testdata_converter.rst`・`tools/master_data_tool.rst`・`tools/html_check_tool.rst` の6本。
- **`setup/junit5_extension.rst` の出典に第1部の `01_Abstract.rst` が混ざっているのは食い違いではない。** `design.md:118-136` が `#6` の「依存関係を第1部に集約する」方針を取り消し、第2部へ差し戻したと明記している。そのまま第2部のページに書く。
- **`implementation/request_unit_test/web.rst` には `how_to_set_token_in_request_unit_test` というラベルを定義する。** 削除された現行解説書のラベルで、`ja/application_framework/application_framework/libraries/db_double_submit.rst:106` がいまも参照している。`style.md` S-08 の命名規則の例外として改名しない。**このページで定義しないと未解決参照が残り続ける。**
- **画像は `images/<ページのファイル名>/` に置く**（`design.md` §13）。現行解説書の画像は `guide/` から `git mv` する。`#26` が `setup/images/common/` に移した形が手本である。
- **設定項目表の「デフォルト値」は、デフォルト設定を読み込んだ実効値を書く**（`design.md` §8）。クラスのフィールド初期値ではない。
- **出典が欠いている、実装上必須の設定は書き足してよい**（`design.md` §8）。根拠の `file:line` と参照コミットハッシュを `reviews/page-*.md` に記録する。参照コミットは `nablarch-testing` = `e21bf67`、`nablarch-testing-yaml` = `190cc9a`。
- **出典と実装が食い違う場合は実装を優先する**（`design.md` §8）。ただし**本体の不具合が疑われる場合は書かずに `decide` に上げる**。`expected_tables:` の `rows: []` が偽陰性になる件（未解決）と同型のものは、仕様どおりに書いて実装の穴を読者に肩代わりさせない。

## 3. 実施順（キュー）

**上から順に進める。順番を変えない。** 小さいページを先に置いてあるのは、規約の運用を早く安定させるためと、途中で止まっても損失を小さくするためである。

出典は `mapping/mapping.csv` を `dest_page` 列で絞って全件取る。**`dest_page` はページのタイトルであってファイルパスではない。** パスで grep すると0件になる。

| # | ページ（`dest_page` の値） | ファイル | 部 | 出典行 |
|---|---|---|---|---:|
| 01 | マスタデータ復旧機能 | `setup/master_data_restore.rst` | 2 | 193 |
| 02 | JUnit 5用拡張機能 | `setup/junit5_extension.rst` | 2 | 475 |
| 03 | テストデータ変換ツール | `tools/testdata_converter.rst` | 4 | 75 |
| 04 | リクエスト単体データ作成ツール | `tools/request_data_tool.rst` | 4 | 163 |
| 05 | マスタデータ投入ツール | `tools/master_data_tool.rst` | 4 | 177 |
| 06 | HTMLチェックツール | `tools/html_check_tool.rst` | 4 | 214 |
| 07 | リクエスト単体テスト（HTTPメッセージング） | `implementation/request_unit_test/http_messaging.rst` | 3 | 28 |
| 08 | 取引単体テスト（RESTfulウェブサービス） | `implementation/deal_unit_test/rest.rst` | 3 | 32 |
| 09 | 取引単体テスト（HTTPメッセージング） | `implementation/deal_unit_test/http_messaging.rst` | 3 | 33 |
| 10 | 取引単体テスト（ウェブアプリケーション） | `implementation/deal_unit_test/web.rst` | 3 | 48 |
| 11 | 取引単体テスト（Nablarchバッチアプリケーション） | `implementation/deal_unit_test/batch.rst` | 3 | 168 |
| 12 | 取引単体テスト（MOMによるメッセージング） | `implementation/deal_unit_test/mom.rst` | 3 | 175 |
| 13 | リクエスト単体テスト（RESTfulウェブサービス） | `implementation/request_unit_test/rest.rst` | 3 | 262 |
| 14 | リクエスト単体テスト（Nablarchバッチアプリケーション） | `implementation/request_unit_test/batch.rst` | 3 | 384 |
| 15 | リクエスト単体テスト（MOMによるメッセージング） | `implementation/request_unit_test/mom.rst` | 3 | 461 |
| 16 | コンポーネント単体テスト | `implementation/class_unit_test/component.rst` | 3 | 770 |
| 17 | リクエスト単体テスト（ウェブアプリケーション） | `implementation/request_unit_test/web.rst` | 3 | 914 |
| 18 | エンティティ単体テスト | `implementation/class_unit_test/entity.rst` | 3 | 1,344 |

ファイルパスはいずれも `ja/development_tools/testing_framework/` からの相対である。

**16〜18 は出典500行超で、本来は個別の作業指示を先に用意すると決めていたページである。** 指示は間に合っていない。**最後尾に置いてあるのは、ここまでで週末の時間を使い切っても損が出ないようにするためである。** 到達したら共通 Steps だけで初版を作り、迷った点はすべて `decide` に上げる。初版が的外れでも書き直せばよい。

**キューから外したページが3つある。** `setup/request_unit_test/db_queue.rst`・`implementation/request_unit_test/db_queue.rst`・`implementation/deal_unit_test/db_queue.rst`。いずれも出典0行で、白紙から設計する必要がある。指示なしで書かせると手戻りが確実なので、週明けに個別指示を出してから着手する。**このキューでは触らない。**

## 4. 1ページあたりの手順

`#25`・`#26` と同じ共通 Steps でよい。要点だけ再掲する。

1. `mapping.csv` を `dest_page` で絞り、`DROP` を除く全行を取る。`src_file` と `src_body_start`〜`src_body_end` を**実際に開いて読む**。要約や `note` 欄を根拠にしない。
2. 出典が参照している実装を、参照リポジトリで確かめる。`nablarch-testing` は `e21bf67`、`nablarch-testing-yaml` は `190cc9a`。
3. ページ先頭ラベルを `style.md` S-08 から引き、リード文を置き、節を組む。
4. 4観点レビュー（QA / Design / Craft / Verification）を回す。**push 前に是正まで畳む。** `#23`・`#25`・`#26` と同じく、是正を別コミットに割らなくてよい。
5. §5 のゲートを全件通す。
6. `checks/task-27.md` にゲート結果を、`reviews/page-<ラベル>.md` にレビュー結果と `decide` を記録する。
7. 1ページ1コミットで push する。件名は `docs: <ページ名>のページを作成する — #27-NN`。

## 5. 毎ページのゲート

**全件通してからコミットする。1つでも赤ければ §1-6 に従って `blocked` にして次へ進む。**

| | 内容 |
|---|---|
| G1 | `git status --porcelain` の**全件**を確認する。ディレクトリで絞らない。`git diff` は未追跡ファイルを出さないので母集合に使わない |
| G2 | 禁止ファイルの差分が0行 — `design.md`・`mapping/style.md`・`mapping/glossary.md`・`mapping/vocabulary.md`・`ja/conf.py`・`mapping/input/` |
| G3 | `locales/ja/LC_MESSAGES/sphinx.mo` がコミットに含まれていない。ビルドが再生成するので `git checkout --` で戻す |
| G4 | `verify_mapping.py` が exit 0。`mapping.csv` を触った場合は `_batch` からの再生成がバイト一致すること |
| G5 | Docker フルビルドが `build succeeded`。**新規の warning が0件。** 既知は `db_double_submit.rst:108` の `undefined label` 1件のみ（`#27-17` でラベルを定義すると、これが0件になる）。実測でフルビルドは約97秒である |
| G6 | 禁止語0件 — `不具合`・`バグ`・`将来`・`修正され` |
| G7 | ページ先頭ラベルが `style.md` S-08 の一覧と一致する |
| G8 | 見出し下線がタイトルの表示幅以上（`style.md:195`）。同じページ内で基準幅を揃える |
| G9 | 本文中の `:ref:` の飛び先が実在し、リンク文字列が飛び先の見出しと一致する |
| G10 | 出典の全行が、本文に反映されたか意図して落としたかのどちらかに分類され、落とした分は理由付きで `reviews/page-*.md` に記録されている |

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
