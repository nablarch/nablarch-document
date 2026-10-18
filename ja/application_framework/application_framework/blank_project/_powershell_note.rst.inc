.. tip::

  PowerShellで上記のコマンドを実行すると、 ``-D`` で始まる引数がPowerShellに解釈されるため、コマンドの実行に失敗する。
  PowerShellで実行する場合は、以下のように各引数をダブルクォートで囲むこと。
  この書き方は、コマンドプロンプトでもそのまま実行できる。

  .. code-block:: bat

    mvn archetype:generate "-DarchetypeGroupId=com.nablarch.archetype" "-DarchetypeArtifactId=<アーキタイプのartifactId>" "-DarchetypeVersion=<アーキタイプのバージョン>"
