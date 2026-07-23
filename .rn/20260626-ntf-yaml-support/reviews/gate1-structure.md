# ゲート①章構成レビュー

## 判定基準

PR の背景に基づく判定基準は以下の4項目とする。

1. 変更前の「どこに何が書かれているか分からない」状態を解消できているか
2. アーキテクト向けとアプリ開発者向けに明確に分けられているか
3. アーキテクトは「NTFの全体構造・仕組み・設定」を知るためのページを見つけられるか
4. アプリ開発者は「テストの使い方・テストデータの書き方」を知るためのページを見つけられるか

---

## 章別読者判定表

| 章ID | 章タイトル | 実ファイルパス | 想定読者 | 判定 | 根拠（file:line） |
|---|---|---|---|---|---|
| A-1 | テスティングフレームワーク概要 | `ja/.../06_TestFWGuide/01_Abstract.rst` | アーキテクト | **逸脱** | L195-579: テストデータ記法（命名規約・データタイプ一覧・特殊記法）がB-1と二重掲載。L613: 「テストデータは全てExcelシートに記述する」見出しがYAML対応後と矛盾 |
| A-2 | テストクラスの設定 | `ja/.../06_TestFWGuide/02_DbAccessTest.rst`、`02_RequestUnitTest.rst`、`RequestUnitTest_batch.rst`、`RequestUnitTest_rest.rst`、`RequestUnitTest_real.rst`、`RequestUnitTest_send_sync.rst`、`RequestUnitTest_http_send_sync.rst` | アーキテクト | **逸脱** | `02_DbAccessTest.rst` L70・L101・L194・L221: 「テストソースコード実装例」「テストデータ記述例」がアーキ章に残存。`RequestUnitTest_batch.rst` L150・L158: 「パディング」「バイナリデータの記述方法」がB章内容 |
| A-3 | テストデータの形式 | `ja/.../06_TestFWGuide/testdata_format.rst` | アーキテクト | **適合** | L7: 「テストデータは Excel または YAML ファイルで記述できる。」。両形式の比較・使い分けを説明。L9: B-1（`ntf_testdata_overview`）へのref:リンクあり |
| A-4 | JUnit 5用拡張機能 | `ja/.../06_TestFWGuide/JUnit5_Extension.rst` | アーキテクト | **逸脱** | `01_Abstract.rst` L665-704: 「JUnit 5で自動テストフレームワークを動かす」節が A-4（JUnit5_Extension.rst）と主題重複。A-1 に未統合の状態で二重存在 |
| A-5 | マスタデータ復旧機能 | `ja/.../06_TestFWGuide/04_MasterDataRestore.rst` | アーキテクト | **適合** | L1〜: FW機能の説明として設定・仕組みを記述。開発者が操作に迷う内容を含まない |
| A-6 | テストツール | `ja/.../08_TestTools/index.rst` | アーキテクト | **適合** | `08_TestTools/index.rst` L1〜: ツール群の目次として機能。「プログラミング工程で使用するツール」の位置づけ |
| B-1 | テストデータの記述方法 | `ja/.../06_TestFWGuide/testdata/index.rst` | アプリ開発者 | **適合** | L1: ラベル `ntf_testdata`。L7: 「テストデータは Excel または YAML ファイルで記述できる。」。データブロック種別・testShots・テーブルデータ・ファイルデータ・メッセージング・値の記述方法を網羅 |
| B-2 | テストデータの記述例 | `ja/.../06_TestFWGuide/testdata/examples.rst` | アプリ開発者 | **適合** | L1: ラベル `ntf_testdata_examples`。L7: 「テストデータは Excel または YAML ファイルで記述できる。」。用途別の Excel/YAML 対比例を掲載 |
| B-3 | クラス単体テストの実施方法 | `ja/.../05_UnitTestGuide/01_ClassUnitTest/` 配下 | アプリ開発者 | **適合** | `01_ClassUnitTest/index.rst` L1〜: 「クラス単体テストの実施方法」。開発者向け実装手順を記述 |
| B-4 | リクエスト単体テストの実施方法 | `ja/.../05_UnitTestGuide/02_RequestUnitTest/` 配下 | アプリ開発者 | **適合** | `02_RequestUnitTest/index.rst` L1〜: 「リクエスト単体テストの実施方法」。テストクラス作成手順を開発者視点で記述 |
| B-5 | 取引単体テストの実施方法 | `ja/.../05_UnitTestGuide/03_DealUnitTest/` 配下 | アプリ開発者 | **適合** | `03_DealUnitTest/index.rst` L1〜: 「取引単体テストの実施方法」。手動操作のテスト手順を開発者視点で記述 |
| B-6 | 目的別API使用方法 | `ja/.../06_TestFWGuide/03_Tips.rst` | アプリ開発者 | **適合** | `03_Tips.rst` L1〜: 「目的別API使用方法」。開発者が目的ごとに APIを検索できる構成 |

---

## 逸脱詳細

### G1-01: テストデータ記法（L195-579）が A-1 と B-1 に二重掲載

**箇所**: `ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/01_Abstract.rst` L195-579

**問題**: 「Excelによるテストデータ記述」（L195〜L579）として、命名規約・シート内の構造・データタイプ一覧・コメント・マーカーカラム・セルの書式・日付の記述方法・セルへの特殊な記述方法の385行が残存している。design.md マッピング#2 では「テストデータ仕様は B-1 に集約」と宣言されているが、A-1 に未削除のまま残っており、`testdata/index.rst`（B-1）の同内容と二重掲載になっている。

**対処案**: A-1 の L195-579 のセクション全体（`.. _how_to_write_excel:` ラベルから「セルへの特殊な記述方法」の末尾まで）を削除し、B-1（`:ref:\`ntf_testdata\``）への参照リンクに置き換える。ラベル `how_to_write_excel` は B-1 に移植するか、B-1 の `ntf_testdata` ラベルへのリダイレクト参照として残す。

---

### G1-02: 「テストデータは全てExcelシートに記述する」見出しが YAML 対応後の記述として矛盾

**箇所**: `ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/01_Abstract.rst` L613-621

**問題**: 「テストデータは全てExcelシートに記述する」（L613）という見出しと、L616「テストデータは全てExcelシートに記載すること。」という本文が残存している。YAML 対応後の解説書として「ExcelシートまたはYAMLファイル」が正しい表現であり、task #9 の Excel 表現修正が A-1 に未適用の状態である。

**対処案**: 見出しを「テストデータは全てテストデータファイルに記述する」に変更し、本文の「Excelシート」を「テストデータファイル（ExcelまたはYAML）」に修正する。または、この注意事項節をそのまま B-6（`03_Tips.rst`）に移動し、A-1 からは削除する（design.md マッピング#11 と整合）。

---

### G1-03: 使い方（B章の内容）が A-2 各ファイルに残存

**箇所**: 
- `ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/02_DbAccessTest.rst` L70（テストソースコード実装例）、L101（テストデータ記述例）、L194（テストソースコード実装例）、L221（テストデータ記述例）、L270（データベーステストデータの省略記述方法）
- `ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_batch.rst` L150（パディング）、L158（バイナリデータの記述方法）

**問題**: A-2 はアーキテクト向けの「テストクラスの設定」として設計されているが、上記各ファイルには「テストソースコード実装例」「テストデータ記述例」「省略記述方法」「パディング」「バイナリデータの記述方法」等、アプリ開発者向けの実装詳細が混在している。design.md マッピング#3-4 では「§ API 使い方・記述例」は B-2 残置または参照化と記されており、未実施の状態である。

**対処案**: `02_DbAccessTest.rst` の「テストソースコード実装例」「テストデータ記述例」節を 05_UnitTestGuide 配下（B-3 または B-4）に移動し、A-2 からは `:ref:` 参照に置き換える。`RequestUnitTest_batch.rst` の「パディング」「バイナリデータの記述方法」節は B-1（`testdata/index.rst`）の固定長ファイルセクションへの参照リンクに置き換える。

---

### G1-04: 「JUnit 5で自動テストフレームワークを動かす」が A-4 と主題重複

**箇所**: `ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/01_Abstract.rst` L665-739

**問題**: A-1 の末尾（L665-739）に「JUnit 5で自動テストフレームワークを動かす」（JUnit Vintage 使用方法）が独立したセクション（`----` レベルの大見出し）として存在している。A-4 `JUnit5_Extension.rst` は「JUnit 5用拡張機能」として独立したページであり、両ページが JUnit 5 上での NTF 実行方法を説明しているため読者が混乱する。A-1 の L684 では「`:ref:\`ntf_junit5_extension\`` を参照」という tip が記されているが、A-1 自体も JUnit 5 節を持っている。

**対処案**: A-1 の L665-739 セクション（`.. _run_ntf_on_junit5_with_vintage_engine:` ラベル以降）を `JUnit5_Extension.rst`（A-4）の「JUnit Vintage」節として統合するか、A-1 側では `:ref:\`run_ntf_on_junit5_with_vintage_engine\`` への短い誘導文のみを残し本文を A-4 に移動する。ラベル `run_ntf_on_junit5_with_vintage_engine` は `JUnit5_Extension.rst` に移植し、既存の相互参照を維持する。

---

### G1-05: A-3（testdata_format.rst）から B-1 への読者導線が弱い

**箇所**: `ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/testdata_format.rst` L9

**問題**: `testdata_format.rst`（A-3）の L9 に「テストデータの構造（データブロックの種別・識別子など）は `:ref:\`ntf_testdata_overview\`` を参照。」という1行の参照がある。ただし、このリンクは冒頭の補足的1行にとどまり、読者が「形式を選んだ次のステップ（実際の記述方法）」として B-1 に誘導される明示的な導線がない。また `testdata_format.rst` への参照は `06_TestFWGuide/index.rst` の toctree のみであり（L49）、B-1 から A-3 への逆方向の参照も存在しない。開発者が B-1 から「形式選択の判断基準」を知るために A-3 に辿り着けない。

**対処案**: `testdata_format.rst` の末尾（または「使い分けの指針」セクション末）に「テストデータの記述方法については `:ref:\`ntf_testdata\`` を参照。」という誘導文を追加する。逆に `testdata/index.rst`（B-1）の冒頭に「形式の選択（Excel/YAML どちらを使うか）については `:ref:\`ntf_testdata_format\`` を参照。」という一文を追加することで双方向の導線を確立する。

---

## 総合判定

**判定**: 条件付き合格

**論拠**:

構成設計（A章＝アーキテクト向け、B章＝開発者向けの分離）は適切であり、A-3・A-5・A-6・B-1〜B-6 の8章は想定読者に対して適合している。

一方、以下の実装未完了が残存しており、現時点ではアーキテクト章（A-1・A-2）に開発者向けコンテンツが混在したままである。

- **G1-01・G1-02（A-1）**: テストデータ記法385行と Excel 固定の注意事項が未削除のため、A-1 が「アーキテクト向け FW 概要」として機能していない。読者は A-1 を読めば開発者向け仕様まで網羅されると誤解する。
- **G1-03（A-2）**: テストソースコード実装例・テストデータ記述例・パディング等がアーキ章に残存しており、A-2 が「設定・構成説明」として機能していない。
- **G1-04（A-1 vs A-4）**: JUnit 5 関連の記述が2箇所に分散しており、どちらを正として読めばよいか判断できない。
- **G1-05（A-3 ↔ B-1）**: 導線の弱さにより、開発者が「形式選択（A-3）→ 記述方法（B-1）」の流れを自力で辿れない。

設計自体の正当性は確認済みのため「不合格」ではなく「条件付き合格」とする。G1-01〜G1-05 の対処案を実施することが、合格（実装完了）への条件となる。
