# Step 4 指示書 — nablarch-testing-converter マーカーカラムだけのブロックの行を保つ（解説書 #54 への追随）

宛先: `nablarch-testing-converter` 担当CC
**送付はカバレッジ指示（`ntf-step4-09`）の完了後**（user 指示 2026-08-31）。

## 0. 渡すときの文面

```
解説書の仕様変更（#54）への追随を依頼します。
git -C /home/tie303177/work/nablarch/nablarch-document fetch origin してから
git show origin/ntf-yaml-support:.rn/20260724-ntf-yaml-support/ntf-step4-12-converter-marker-rows.md
を読み、指示書どおり実施して報告・停止してください。
是正は判断済みです。範囲の判断を持たないでください。
本体・yaml を正解（oracle）にしたテストを含めてください。
```

## 1. 背景（確定済みの事実）

**解説書（SSoT）が `ed3de95f` で変わった。** `tools/testdata_converter.rst:65` の逐語（変更後）:

> ただし、カラム名の行をマーカーカラムだけで構成したデータブロックは例外として、マーカーカラムとその値を保ったまま変換する。このブロックの各エントリはフィールドを持たないが、テストショット一覧と行の順序で対応付ける用途では、エントリの数と並びが意味を持つためである。

旧文「マーカーカラムだけで構成したデータブロックは…データ行も残らない」は SSoT 内部矛盾（記法ページ `:1486`・`:427`・スキーマ description と矛盾）として取り下げられた。現行実装はこの旧文どおりであり、結合テスト（`nablarch-testing-integration` の `AbstractHttpRequestTestTemplateYamlTest`）で7件の赤として実測されている（`requestParams`＝マーカーカラム `[no]` のみ・データ4行 → `rows: []` に潰れ、本体 `TestCaseInfo.java:344-351`（`3c4bd2a`）の位置インデックスが引けない）。

**現行実装の該当箇所**（`a5f006c` 実測。ディレクター確認済み）:

1. `XlsFormatReader.java:619` `rowCount` — `columnNames.isEmpty() ? 0 : rowCount` が行を落とす（`1915207` で導入）
2. `YamlFormatWriter.java:268`-`:270` `emitMapRows` — カラム0件の行を `- {}` と書く（`{}` は読み戻しでスキップされるため、1 を直すだけではここで壊れる）
3. YAML 読み・Excel 書きの対称側（`YamlFormatReader.java:495`-`:498` はマーカーキーをカラム名から除く。マーカーだけの行の扱いを 1・2 と対称にする）

**YAML 側の表現は実在する**: スキーマの `rows` 要素は `additionalProperties`（キー名無制約）で `- "[no]": "1"` が妥当。yaml 実装もマーカーだけの行を残す（`YamlSection.java:227`-`:228`・`:265`。`4837713`）。yaml・本体・解説書の記法ページは変更不要。

## 2. やること

**カラム名の行がマーカーカラムだけのデータブロック（テーブル・`LIST_MAP`）は、マーカーカラム（名前と各行の値）を保って両方向に変換する。** 設計はまかせるが、観測可能な挙動を次のテストで固定する。

1. **oracle テスト（Excel→YAML）**: マーカーだけのブロック（例: `[no]` / `[1]`〜`[4]`）を本体 `BasicTestDataParser`（Excel）で読んだエントリ数と、変換後 YAML を `YamlTestDataParser` で読んだエントリ数・並びが一致すること。converter 自身の reader を正解にしない
2. **往復テスト**: Excel→YAML→Excel と YAML→Excel→YAML でマーカーカラムの名前・値・行数が保たれること（実ファイル起点。解釈後の値で比較）
3. **スキーマ検証**: 変換後 YAML が `ntf-testdata-yaml-schema.json` の検証を通ること
4. 実データカラムを持つブロックのマーカーは従来どおり消えること（既存挙動の非回帰）
5. `1915207` が新設した `XlsMarkerOnlyEntryTest` 等、旧仕様を期待する既存テストは新仕様に合わせて直す（変更の全件を報告に列挙）

## 3. やらないこと

- 解説書・本体・yaml・integration を変更しない
- ソース・記録に解説書への参照を書かない（`file:line`・節見出し・逐語とも不可）
- force push・`--amend` をしない

## 4. 完了条件

1. §2 のテスト1〜4 が存在して緑。1・2 は**是正を意図的に壊すと落ちること**（例: rowCount を旧実装に戻す）を実測し、コマンドと結果を報告に書く
2. 旧仕様を期待していた既存テストの変更が全件列挙されている
3. `JAVA_HOME=/usr/lib/jvm/temurin-17-jdk-amd64 mvn clean test` 全件緑・`@Ignore` 0件
4. **カバレッジ基準（未達0。`ntf-step4-09` と同じ）を新規コードにも適用**: 同指示書の手順で測定し、本是正が持ち込んだ未達が0であることを報告
5. `git status --short` 空・修正意図ごとに1コミットで push・報告して停止
6. `grep -rn "nablarch-document\|\.rst" src/` が0件

## 5. 報告とレビュー

報告は ①差分の要約 ②テスト1〜4 と変異確認 ③既存テスト変更の全件 ④カバレッジ、の順。レビューは回さない（是正は確定済み・oracle と変異確認が観点Dを代替し、ディレクターが独立再実行＋integration 再検証で確認する）。
