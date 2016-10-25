.. _`getting_started_batchlet`:

対象テーブルのデータを削除するバッチの作成(Batchletステップ)
================================================================
Exampleアプリケーションを元に、 :ref:`batchletステップ<jsr352-batch_type_Batchlet>` で対象テーブルのデータを削除するバッチの解説を行う。

作成する機能の説明
  1. 現在のDBの状態の確認

     H2のコンソールから下記SQLを実行する。

     .. code-block:: sql

       SELECT * FROM ZIP_CODE_DATA;
       SELECT * FROM ZIP_CODE_DATA_WORK;

     データが登録されていない場合は 2の手順を実施する。

  2. (データが登録されていない場合)住所登録バッチを実行

    コマンドプロンプトから下記コマンドを実行する。

    .. code-block:: bash

      $cd {nablarch-example-batch-eeシステムリポジトリ}
      $java -cp .\target\*;.\target\dependency\* ^
          com.nablarch.example.app.main.ExampleMain ^
          etl-zip-code-csv-to-db-chunk

    .. _`getting_started_batchlet-main_class`:

    .. tip::
     ExampleMainクラスは、Example用に作成したバッチアプリケーションの起動クラスである。
     起動クラスは、アプリケーション要件に応じてアーキテクトが作成する。
     バッチ起動用クラスの詳細は、 :ref:`jsr352_run_batch_application` を参照。

    H2のコンソールから下記SQLを実行してデータが登録されたことを確認する。

    .. code-block:: sql

      SELECT * FROM ZIP_CODE_DATA;
      SELECT * FROM ZIP_CODE_DATA_WORK;

  3. 住所テーブル削除バッチを実行

    コマンドプロンプトから下記コマンドを実行する。

    .. code-block:: bash

      $cd {nablarch-example-batch-eeシステムリポジトリ}
      $java -cp .\target\*;.\target\dependency\* ^
          com.nablarch.example.app.main.ExampleMain ^
          zip-code-truncate-table

  4. 対象テーブルのデータが削除されていることを確認

     H2のコンソールから下記SQLを実行し、データが削除されていることを確認する。

     .. code-block:: sql

       SELECT * FROM ZIP_CODE_DATA;
       SELECT * FROM ZIP_CODE_DATA_WORK;

対象テーブルのデータを削除する
---------------------------------
住所情報を削除するバッチの実装方法を説明する。

処理フローについては、 :ref:`Batchletステップのバッチの処理フロー<jsr352-batch_flow_batchlet>` を参照。
責務配置については :ref:`Batchletステップの責務配置<jsr352-batchlet_design>` を参照。

  #. :ref:`Batchletの作成<getting_started_batchlet_create>`
  #. :ref:`JOB設定ファイルの作成<getting_started_batchlet_job>`

.. _`getting_started_batchlet_create`:

Batchletの作成
  住所情報を削除するバッチのBatchletクラスを作成する。

  実装すべきインタフェースとその責務
    Batchletクラスに以下のインタフェースを実装してバッチ処理を作成する。オーバーライドしたメソッドは、Batch Runtimeによって適切なタイミングで呼び出される。

   ==================================================================   =============================================================================================
   インタフェース                                                       実装
   ==================================================================   =============================================================================================
   :java:extdoc:`Batchlet<javax.batch.api.Batchlet>`                    バッチ処理を実装する。

                                                                        デフォルト実装を提供する :java:extdoc:`AbstractBatchlet<javax.batch.api.AbstractBatchlet>` を継承する。

                                                                          * `Batchlet#process`
                                                                          * `Batchlet#stop`
   ==================================================================   =============================================================================================

  .. tip::

    バッチ処理は、上記のインタフェースの実装に加えて、トランザクション制御などの共通的な処理を提供するリスナーによって構成する。
    リスナーの詳細は :ref:`バッチアプリケーションで使用するリスナー<jsr352-listener>` 及び :ref:`リスナーの指定方法<jsr352-listener_definition>` を参照。

  TruncateTableBatchlet.java
    .. code-block:: java

      @Dependent
      @Named
      public class TruncateTableBatchlet extends AbstractBatchlet {

          @Inject
          @BatchProperty
          private String tableName;

          @Override
          public String process() {

              final AppDbConnection conn = DbConnectionContext.getConnection();
              final SqlPStatement statement
                  = conn.prepareStatement("TRUNCATE TABLE " + tableName);
              statement.executeUpdate();

              return "SUCCESS";
          }
      }

    この実装のポイント
      * :java:extdoc:`AbstractBatchlet<javax.batch.api.AbstractBatchlet>` を継承し、 `process` メソッドで業務処理を行う。

      .. _getting_started_batchlet-cdi:

      * :java:extdoc:`Named<javax.inject.Named>` と :java:extdoc:`Dependent<javax.enterprise.context.Dependent>` をクラスに付与する。 |br|
        Named及びDependentアノテーションを設定することで、Batchlet実装クラスをCDIの管理Beanにできる。
        これにより、ジョブ定義に指定するBatchletクラス名をCDIの管理名で記述出来るようになる。 |br|
        (CDI管理Beanとしなかった場合は、完全修飾名(FQCN)で記述する)

      * :ref:`データベースアクセス<database>` を使用してTRUNCATE文を実行する。

.. _`getting_started_batchlet_job`:

ジョブ定義ファイルの作成
  ジョブの実行設定を定義したファイルを作成する。

  zip-code-truncate-table.xml
    .. code-block:: xml

     <job id="zip-code-truncate-table" xmlns="http://xmlns.jcp.org/xml/ns/javaee" version="1.0">
       <listeners>
         <listener ref="nablarchJobListenerExecutor" />
       </listeners>

       <step id="step1" next="step2">
         <listeners>
           <listener ref="nablarchStepListenerExecutor" />
         </listeners>
         <batchlet ref="truncateTableBatchlet">
           <properties>
             <property name="tableName" value="ZIP_CODE_DATA" />
           </properties>
         </batchlet>
       </step>
       <step id="step2">
         <listeners>
           <listener ref="nablarchStepListenerExecutor" />
         </listeners>
         <batchlet ref="truncateTableBatchlet">
           <properties>
             <property name="tableName" value="ZIP_CODE_DATA_WORK" />
           </properties>
         </batchlet>
       </step>
     </job>

  この実装のポイント
    * ジョブ定義ファイルは、`/src/main/resources/META-INF/batch-jobs/` 配下に配置する。
    * `job` 要素 の `id` 属性で、ジョブ名称を指定する。
    * 複数ステップで構成されるバッチジョブの場合は、 `step` 要素を複数定義し、処理を順次実行する。
    * `batchlet` 要素の `ref` 属性には、Batchletクラス名の頭文字を小文字にした名称を指定する。
    * `property` 要素で、Batchletクラスのプロパティにインジェクトする値を指定する。
    * 設定ファイルの詳細な記述方法は `JSR352 Specification(外部サイト、英語) <https://jcp.org/en/jsr/detail?id=352>`_ を参照

.. |jsr352| raw:: html

  <a href="https://jcp.org/en/jsr/detail?id=352" target="_blank">JSR352(外部サイト、英語)</a>

.. |br| raw:: html

  <br />
