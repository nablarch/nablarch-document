.. tip::

  When the above command is executed in PowerShell, the arguments starting with ``-D`` are interpreted by PowerShell and the command fails.
  To execute the command in PowerShell, enclose each argument in double quotes as shown below.
  This notation also works as is in the Command Prompt.

  .. code-block:: bat

    mvn archetype:generate "-DarchetypeGroupId=com.nablarch.archetype" "-DarchetypeArtifactId=<artifactId of the archetype>" "-DarchetypeVersion=<version of the archetype>"
