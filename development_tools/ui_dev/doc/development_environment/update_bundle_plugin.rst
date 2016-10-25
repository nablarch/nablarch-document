=========================================
Nablarch 標準プラグインの更新
=========================================
本節では、UI開発基盤を構築後にNablarch 標準プラグイン(以下標準プラグイン)をバージョンアップする手順を示す。
なお、この作業は、UI開発基盤の担当者が実施すればよく、各担当者が個別に実施する必要はない。

1. UI開発基盤の更新方針
===================================
UI開発基盤をPJで取り込んだ後も、Nablarchでは標準プラグインの不具合修正や機能追加を継続的に行う。
Nablarch側で行った標準プラグインの不具合修正や機能追加がPJ側でも必要と判断した場合は、
その変更内容をここで述べる手順に沿って取り込むことができる。

機能の修正や追加はプラグイン単位で行うことができるので、取り込みに要する作業工数や、
PJの既存機能に対する影響を極小化することができる。

.. tip::

 ただし、PJ側の拡張や既存機能への影響に関して、Nablarch側では把握することができないので、
 取り込み後の動作確認等はPJ側で担保する必要がある。



2. 作業時のディレクトリ構成
===================================
最新バージョンのNablarch標準プラグインのバンドルを取得し、
:doc:`./initial_setup` の **UI開発基盤の取得と展開** で述べたディレクトリ構造と同じ構造になるように配置する。


3. 標準プラグインの更新
======================================================

標準プラグインの変更内容を取り込む手順を以下に示す。

更新前のPJのUI開発基盤が依存している標準プラグインのうち、
更新されたプラグインを確認し、マージ作業をおこなう。

1. 現在のプラグインのバージョンの確認
------------------------------------------------------

標準プラグインバンドル配下にある `bin/update.bat` をPJのディレクトリ構造にあわせ修正し、
実行することで、現在のPJのプラグインとリリースされた標準プラグインのバージョン差異を確認することができる。

下記の構造の場合、 `PROJECT` は"../../xxx_project"、 `UI_PLUGIN` は"ui_plugins"となる。

 .. code-block:: bash

   プロジェクトルート/
        │
        ├── nablarch_plugins_bundle/
        │       ├── bin/
        │       │     └── update.bat
        │       ├── node_modules/
        │       │     ├── nablarch-css-base/
        │       │     ├── nablarch-css-color-default/
        │       │     ├── nablarch-css-common/
        │       │     │
        │       │ ## 後略 ##
        │       │
        │       └── package.json
        │
        └── xxx_project/           # PROJECT
                 ├── web/
                 ├── ui_demo/
                 ├── ui_test/
                 └── ui_plugins/   # UI_PLUGIN
                        ├── node_modules/
                        ├── pjconf.json
                        └── package.json
              


update.batを実行すると、ui_plugins/ で管理されている標準プラグインの内、
更新されているプラグインを `ui_plugins/updated_plugin.json` に出力する。

.. tip::

   標準プラグインの新規取込の場合、 `updated_plugin.json` には出力されないため、
   対象の標準プラグインをPJのUI開発基盤にコピーすること。

updated_plugin.jsonの出力例

.. code-block:: javascript

   {
      "nablarch-css-core" : "1.0.0"               // nablarch-css-coreが更新されていた場合
    , "web_project-dev-ui_test-support" : "1.0.1" // 後述する_fromで指定したプラグインが更新されていた場合
    , "web_project-dev-ui_test-support" : "1.0.0"
   }


PJでコピー(もしくは参照)して作成した場合、
コピーしたプラグインのpackage.jsonに `_from` を設定することでupdate.bat実行時に一覧に出力することができる。

.. tip::

 標準プラグインには `_from` が設定済みのため、コピーした時に削除しなければよい。


`_from` の指定例

.. code-block:: javascript

  { "name" : "web_project-dev-ui_test-support"
  , "description" : "プロジェクト向けにカスタマイズしたUI部品単体テストサポートプラグイン"
  , "version" : "1.0.0"
  , "_from" : "nablarch-dev-ui_test-support@1.0.0"
  }



2. プラグインのマージ
---------------------------------------------------
取り込むと判断したプラグインについて修正内容を取り込む。
下記に取込作業の手順を示す。

 1. 作業ディレクトリにUI開発基盤導入時のリビジョンをチェックアウトする

    .. code-block:: bash

     作業ディレクトリ/
           ├── nablarch_plugins_bundle/
           │        ├── node_modules/
           │        │      ├── nablarch-css-base/
           │        │      ├── nablarch-css-color-default/
           │        │      ├── nablarch-css-common/
           │        │      │
           │        │   ## 後略 ##
           │        │
           │        └── package.json
           │
           └── xxx_project/
                     ├── web/
                     ├── ui_plugins/
                     │        ├── node_modules/
                     │        │       ├── nablarch-css-base/
                     │        │       ├── nablarch-css-color-default/
                     │        │       ├── nablarch-css-common/
                     │        │       │
                     │        │   ## 後略 ##
                     │        │
                     │        └── package.json
                     ├── ui_demo/
                     └── ui_test/


 2. 標準プラグインとカスタマイズしたプラグイン(初期状態)を上書きする。

    カスタマイズしたプラグインについては競合する可能性があるため、競合を解消する。

       1. 新規(標準モジュールをコピーし、リネームした状態で)追加したリビジョンにアップデートする。
       2. `_from` 属性に設定されている標準モジュールの内容で上書きする。
       3. PJ側が修正したリビジョンにアップデートする。
       
        * 競合しない場合は、Nablarch側の修正を確認する。
        * 競合した場合は、競合を解決する。


  下記の場合、rev:10, rev:15で2回の競合の解消を行う。

       1. nablarch-css-color-defaultを上書きする。
       2. リビジョン10にアップデートする。
       3. xxx_project-css-color-defaultに `_from` に設定されているnablarch-css-color-defaultの修正内容を上書きする。
       4. リビジョン15にアップデートする。
       5. xxx_project-css-commonに `_from` に設定されているnablarch-css-commonの修正内容を上書きする。
       6. PJ側の修正したリビジョンまでアップデートする。

         
  .. code-block:: bash

     作業ディレクトリ/
           ├── nablarch_plugins_bundle/
           │        └── node_modules/
           │                 ├── nablarch-css-base/
           │                 ├── nablarch-css-color-default/
           │                 ├── nablarch-css-color-common/
           │                 │
           │              ## 後略 ##
           │
           └── xxx_project/
                     ├── web/
                     ├── ui_demo/
                     ├── ui_test/
                     └── ui_plugins/
                              └── node_modules/
                                        ├── nablarch-css-base/
                                        ├── nablarch-css-color-default/    # diff確認
                                        ├── nablarch-css-common/
                                        ├── xxx_project-css-color-default/ # rev:10 で追加(マージ対象)
                                        ├── xxx_project-css-common/        # rev:15 で追加(マージ対象)
                                        │
                                    ## 後略 ##

 3. trunkのリビジョンまでアップデートしたら、UI部品のビルドを行い、各部品のテストをする。

   .. tip::

     標準プラグインを新規に取り込んだ際、カスタマイズが必要になった場合は、一旦 `ui_plugins/pjconf.json` から対象プラグインを外し、
     カスタマイズは行わないこと。

     標準プラグインの取り込みが完了してから :doc:`modifying_code_and_testing` を参照し、カスタマイズすること。

 4. リポジトリにコミットする。

