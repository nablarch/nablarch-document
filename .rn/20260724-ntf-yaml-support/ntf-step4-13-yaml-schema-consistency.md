# Step 4 指示書 — nablarch-testing-yaml スキーマ description と解説書（SSoT）の全件突合

宛先: `nablarch-testing-yaml` 担当CC
**送付はカバレッジ指示（`ntf-step4-10`）の完了後**（user 指示 2026-08-31）。

**目的**: スキーマの `description` は SSoT の適用範囲である（user 確定 2026-08-25）。`#45` では点検で見つかった3件（`:108`・`:136`・`:410`）だけを直したが、**全 description を解説書と突き合わせる網羅的な確認はまだ行っていない**。`#54` で解説書側の SSoT 内部矛盾が1件見つかったため（変換ツールページの旧文。スキーマは正しい側だった）、残りにズレが無いことを全件で確認する。

## 0. 渡すときの文面

```
スキーマ description と解説書の全件突合を依頼します。
git -C /home/tie303177/work/nablarch/nablarch-document fetch origin してから
git show origin/ntf-yaml-support:.rn/20260724-ntf-yaml-support/ntf-step4-13-yaml-schema-consistency.md
を読み、指示書どおり実施して報告・停止してください。
突合は「主張1件ずつ」です。description 単位で「概ね一致」とまとめないでください。
```

## 1. やること

対象: `src/main/resources/nablarch/test/ntf-testdata-yaml-schema.json` の**全 description**（`$defs` 10件とトップレベル・全プロパティ。母集合は `description` キーの機械抽出で先に固定し、件数を報告に書く）。

解説書の参照点: `nablarch-document` `origin/ntf-yaml-support` の **`ed3de95f`**。`git show ed3de95f:<path>` で読む（作業ツリーを読まない）。

各 description を**文単位の主張に分解**し、1主張ずつ次を判定する:

| 判定 | 意味 | 処置 |
|---|---|---|
| 一致 | 解説書に同旨の記述がある | 対応表に解説書の `file:line` を書く |
| 解説書に記述なし | スキーマだけが述べている（実装・スキーマ制約の説明等） | 実装の `file:line` を根拠に付け、解説書に**あるべき**内容かの所見を1行書く（追記はしない） |
| 矛盾 | 解説書と食い違う | **スキーマ側を解説書の逐語に合わせて是正**（解説書が正）。ただし**解説書側が誤っている疑いがあるものは直さず、根拠を添えて報告して止まる** |

構造制約（type・required・pattern・maxItems 等）も同様に、対応する解説書の記述と突き合わせる（例: `records` の `maxItems: 1` ⇔ `notation.rst` の「レコードレイアウトは1つ」）。

## 2. やらないこと

- 解説書を変更しない。description 以外の構造制約の変更は、矛盾として報告して止まる（検証挙動が変わるため）
- ソースに解説書への参照を書かない（description の文言は解説書に**合わせる**が、`file:line` や節名は書かない）
- force push・`--amend` をしない

## 3. 完了条件

1. 母集合（description の件数・主張の件数）が機械抽出コマンドつきで報告にあり、**全主張**が対応表に載っている（サンプリングしない）
2. 「矛盾」の全件に処置（是正コミット or 解説書側の疑いとしての報告）が付いている
3. description のみの変更であることを `git diff` で確認（構造制約に差分なし）。是正した description は解説書の該当記述と突き合わせた逐語根拠つき
4. `JAVA_HOME=/usr/lib/jvm/temurin-17-jdk-amd64 mvn clean test` 全件緑（318件基準）・`git status --short` 空・push
5. 報告して停止

## 4. 報告とレビュー

報告は ①結論（矛盾の件数と内訳）②対応表（全件）③是正の差分 ④解説書側の疑い（あれば1件ずつ）、の順。レビューは回さない（成果は対応表であり、ディレクターが対応表の全行を実物で突き合わせて独立検証する）。
