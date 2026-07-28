# #6 設計判断案（ユーザー承認待ち、2026-07-28提示）

`#6`着手にあたり実施した実データ調査と、`design.md`「12. 未確定事項」3件・関連する
`稼動環境`0件問題への判断案。ユーザーへ地の文で提示済み、まだ承認を得ていない。

## ① 稼動環境0件（第1部）

**実測**: `current-0180`（`01_Abstract.rst:698-739`「依存関係の追加」節、JUnit Vintageの
Maven依存追加）と`current-0267`（`JUnit5_Extension.rst:37-47`「モジュール一覧」節、
`nablarch-testing-junit5`の依存追加）が、design.md §2「依存関係は本ページ（稼動環境）に
集約する。処理方式ごとのページには置かない」に反し、第2部「JUnit 5用拡張機能」に留まって
いる。「Java・Jakarta EEの要件」に相当する記述は、current 47ファイル・input全域を
`grep -rnE "Jakarta ?EE|Java ?17|Java ?SE|Java ?11|Java ?8|JDK"`で検索し0件（唯一のヒットは
`input/testdata-converter-design.md:355`だがDROP・developer扱いの開発体制記述で無関係）。

**判断案（案A採用）**: `current-0180`/`current-0267`を第1部「稼動環境」へ移動する
（第2部JUnit5拡張機能 475→422行、第1部テスティングフレームワークとは 293→346行）。
「Java・Jakarta EEの要件」は出典がないため`design.md` §2の表からこの項目を削除する。

## ② テストデータの形式0件（第2部）

**実測**: 現行47rst＋input10md全文でYAMLに言及する194行を機械抽出し`mapping.csv`の
`dest_page`へ突合。内訳: テストデータの記載例70／テストデータの書き方70／DROP25／
UNMAPPED15（見出し行等）／テストデータ変換ツール11／テスティングフレームワークとは3。
第2部「テストデータの形式」への割当は**0行**。

**判断案**: ページを廃止し、`design.md` §3のツリーから削除する。Excel/YAML比較・使い分けの
説明は、既に内容が集まっている第3部「テストデータの書き方」冒頭に統合する（新規文章の
追加ではなく既存マッピング内容の再配置として扱う）。

## ③ 第2部のページ分割（未確定事項#1）＋ 取引単体テストのページ構成（未確定事項#2）

**実測**: `git ls-tree -r --name-only $BASE -- ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/`
（第2部の出典ディレクトリ）を確認すると、`RequestUnitTest_batch.rst` /
`RequestUnitTest_http_send_sync.rst` / `RequestUnitTest_real.rst` /
`RequestUnitTest_rest.rst` / `RequestUnitTest_send_sync.rst` の5処理方式分の設定ファイルが
存在するが、`DealUnitTest_*`という取引単体テスト専用の設定ファイルは**存在しない**。
取引単体テストの設定内容（volume.md: MOM 104行／RESTful 52行／HTTPメッセージング20行）は
`03_DealUnitTest/`の使用方法ファイル内に埋め込まれた設定記述の断片（例:
`current-0158` = `send_sync.rst:280-383`「モックアップクラス設定・Excel配置場所設定・
テストデータ解析クラス設定・pom.xml追加」）であり、ウェブアプリケーション・
Nablarchバッチアプリケーションにはこの種の記述が一切ない（0行はマッピング漏れではなく
実体の不在）。

**判断案**:
- **リクエスト単体テストの設定**: design.md暫定構成どおり6処理方式に分割する
  （第3部と対称。テーブルをキューとして使ったメッセージングは§6で確定済みの
  「導線のみ」を踏襲）。
- **取引単体テストの設定**: 実データがある**3処理方式のみ**ページ化する
  （MOMによるメッセージング／RESTfulウェブサービス／HTTPメッセージング）。
  ウェブアプリケーション・Nablarchバッチアプリケーション・テーブルをキューとして
  使ったメッセージングはページを設けない（出典なき「設定不要」の文言を新規に
  書き起こすのは「マッピングにない内容を追加しない」に反するため、ページ自体を
  作らない）。

## ④ ファイル名・ディレクトリ構成（未確定事項#3）

**根拠**: FW解説書ライブラリ（`ja/application_framework/application_framework/libraries/`）の
慣例を確認。英語snake_case、連番なし。

**判断案**:

```
ja/development_tools/testing_framework/
├── index.rst
├── about/                  第1部（1ページ + images）
├── setup/                  第2部
│   ├── common.rst / class_unit_test.rst / junit5_extension.rst / master_data_restore.rst
│   ├── request_unit_test/{web,rest,http_messaging,batch,mom,db_queue}.rst
│   └── deal_unit_test/{rest,http_messaging,mom}.rst
├── implementation/         第3部
│   ├── testdata_format.rst / testdata_examples.rst
│   ├── class_unit_test/{entity,component}.rst
│   ├── request_unit_test/{6処理方式}.rst
│   └── deal_unit_test/{6処理方式}.rst
└── tools/                  第4部
    └── {request_data_tool,testdata_converter,master_data_tool,html_check_tool}.rst
```

## 承認後に着手する`#6`のSteps

1. design.md更新（未確定事項節削除、確定構成を本文反映、上記①〜④を反映）
2. `mapping.csv`の`dest_page`を確定構成に更新（暫定29件の一括置換、
   テストデータの形式行の再配置、取引単体テストの設定2ページ分の再判定を含む）
3. `note`が「暫定。」で始まる全行の表記解消
4. `reference-only sections`全件（advisory 2件）の判断を本ファイルに追記
5. self-check
6. commit & push
7. user review
