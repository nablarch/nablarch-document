# task4 Completion Check

## Completion Criteria

| Criterion | Self-check | Evidence |
|---|---|---|
| A章・B章が toctree に現れており、`make html` の HTML 出力で両章が確認できる | OK | 06_TestFWGuide/index.rst タイトルを「Nablarchテスティングフレームワークとは」に変更。05_UnitTestGuide/index.rst タイトルを「テストの実装方法」に変更。HTML 出力 `<h1>` で両タイトルを確認済み。 |
| `make html` がエラーなく完了し、エラー行数が0であること | OK | `build succeeded, 3 warnings.` エラー0件。警告3件はいずれも既存ファイル（biz_samples/03、biz_samples/13）由来で今回の変更と無関係。 |
| 既存ファイルへの toctree 参照が壊れていない | OK | 既存の toctree エントリ（01_Abstract, 02_DbAccessTest, 02_RequestUnitTest, RequestUnitTest_* など）はそのまま保持。全 HTML 生成を確認。 |

## 変更ファイル一覧

| ファイル | 変更内容 |
|---|---|
| `06_TestFWGuide/index.rst` | タイトルを `Nablarchテスティングフレームワークとは` に変更 |
| `05_UnitTestGuide/index.rst` | タイトルを `テストの実装方法` に変更。B-1 スタブ（`../06_TestFWGuide/testdata/index`）への toctree エントリを追加 |
| `06_TestFWGuide/testdata/index.rst` | 新規作成。`.. _ntf_testdata:` ラベル付き B-1 スタブ（toctree は空、#5 で充填） |
| `testing_framework/index.rst` | エントリ順を A章（06_TestFWGuide）→ B章（05_UnitTestGuide）→ ツール（08_TestTools）に変更。誘導文を修正 |

## ビルド実行詳細

- 実行コマンド: `LC_ALL=C.UTF-8 LANG=C.UTF-8 make html SPHINXBUILD=/tmp/sphinx_env/bin/sphinx-build`
- 使用 Sphinx: v1.8.6（/tmp/sphinx_env）
- ビルド結果: `build succeeded, 3 warnings.`
- 新規生成 HTML: `06_TestFWGuide/testdata/index.html` 確認済み

## Overall Verdict

- Self-check: OK
- Ready for next step: Yes（#5 B-1 新規作成 へ）
