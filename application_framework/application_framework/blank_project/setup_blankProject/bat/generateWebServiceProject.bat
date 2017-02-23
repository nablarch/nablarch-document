if "%5" EQU "" (
  set package=%2
) else (
  set package=%5
)

mvn org.apache.maven.plugins:maven-archetype-plugin:2.4:generate -DinteractiveMode=false -DarchetypeGroupId=com.nablarch.archetype -DarchetypeArtifactId=nablarch-jaxrs-archetype -DarchetypeVersion=%1 -DgroupId=%2 -DartifactId=%3 -Dversion=%4 -Dpackage=%package%
