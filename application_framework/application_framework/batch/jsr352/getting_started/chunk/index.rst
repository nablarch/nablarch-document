.. _`getting_started_chunk`:

データを導出するバッチの作成(Chunkステップ)
===============================================================
Exampleアプリケーションを元に、既存データから計算を行い新たにデータを導出する :ref:`Chunkステップ<jsr352-batch_type_chunk>` 方式のバッチの解説を行う。

作成する機能の概要
  .. image:: ../images/chunk/overview.png

動作確認手順
  1. 登録対象テーブル(賞与テーブル)のデータを削除

     H2のコンソールから下記SQLを実行し、賞与テーブルのデータを削除する。

     .. code-block:: sql

       TRUNCATE TABLE BONUS;

  2. 賞与計算バッチを実行

     コマンドプロンプトから賞与計算バッチを実行する。
     ExampleMainクラスについては、 :ref:`ExampleMainクラスの説明<getting_started_batchlet-main_class>` を参照。

    .. code-block:: bash

      $cd {nablarch-example-batch-eeシステムリポジトリ}
      $java -cp .\target\*;.\target\dependency\* ^
           com.nablarch.example.app.main.ExampleMain bonus-calculate

  5. バッチ実行後の状態の確認

    H2のコンソールから下記SQLを実行し、賞与情報が登録されたことを確認する。

    .. code-block:: sql

        SELECT * FROM BONUS;

データを導出する
-------------------
既存データから計算を行い、新たにデータを導出するバッチの実装方法を以下の順に説明する。

#. :ref:`getting_started_chunk-read`
#. :ref:`getting_started_chunk-business_logic`
#. :ref:`getting_started_chunk-persistence`
#. :ref:`getting_started_chunk-job`

処理フローについては、 :ref:`Chunkステップのバッチの処理フロー<jsr352-batch_flow_chunk>` を参照。
責務配置については :ref:`Chunkステップの責務配置<jsr352-chunk_design>` を参照。

バッチ処理は、 |jsr352| で規定されたインターフェースの実装に加えて、トランザクション制御などの共通的な処理を提供するリスナーによって構成する。
リスナーの詳細は :ref:`バッチアプリケーションで使用するリスナー<jsr352-listener>` 及び :ref:`リスナーの指定方法<jsr352-listener>` を参照。

.. _`getting_started_chunk-read`:

入力データソースからデータを読み込む
+++++++++++++++++++++++++++++++++++++
計算に必要なデータを取得する処理を実装する。

#. :ref:`フォームの作成<getting_started_chunk-form>`
#. :ref:`ItemReaderの作成<getting_started_chunk-reader>`

.. _`getting_started_chunk-form`:

フォームの作成
  Chunkステップでは、 :java:extdoc:`ItemReader<javax.batch.api.chunk.ItemReader>` と
  :java:extdoc:`ItemProcessor<javax.batch.api.chunk.ItemProcessor>` とのデータ連携にフォームを利用する。

  EmployeeForm.java
    .. code-block:: java

      public class EmployeeForm {

          //一部のみ抜粋

          /** 社員ID */
          private Long employeeId;

          /**
           * 社員IDを返します。
           *
           * @return 社員ID
           */
          public Long getEmployeeId() {
              return employeeId;
          }

          /**
           * 社員IDを設定します。
           *
           * @param employeeId 社員ID
           */
          public void setEmployeeId(Long employeeId) {
              this.employeeId = employeeId;
          }
      }

.. _`getting_started_chunk-reader`:

ItemReaderの作成
  :java:extdoc:`AbstractItemReader<javax.batch.api.chunk.AbstractItemReader>` を継承し、データの読み込みを行う。

    ==================================================================   =============================================================================================
    インタフェース名                                                       責務
    ==================================================================   =============================================================================================
    :java:extdoc:`ItemReader<javax.batch.api.chunk.ItemReader>`          データの読み込みを行う。

                                                                         空実装を提供する :java:extdoc:`AbstractItemReader<javax.batch.api.chunk.AbstractItemReader>` を継承する。

                                                                           * `ItemReader#open`
                                                                           * `ItemReader#readItem`
                                                                           * `ItemReader#close`
    ==================================================================   =============================================================================================

  EmployeeSearchReader.java
    .. code-block:: java

      @Dependent
      @Named
      public class EmployeeSearchReader extends AbstractItemReader {

          /** 社員情報のリスト */
          private DeferredEntityList<EmployeeForm> list;

          /** 社員情報を保持するイテレータ */
          private Iterator<EmployeeForm> iterator;

          @Override
          public void open(Serializable checkpoint) throws Exception {
              list = (DeferredEntityList<EmployeeForm>) UniversalDao.defer()
                      .findAllBySqlFile(EmployeeForm.class, "SELECT_EMPLOYEE");
              iterator = list.iterator();
          }

          @Override
          public Object readItem() {
              if (iterator.hasNext()) {
                  return iterator.next();
              }
              return null;
          }

          @Override
          public void close() throws Exception {
              list.close();
          }
      }

  EmployeeForm.sql
    .. code-block:: java

      SELECT_EMPLOYEE=
      SELECT
          EMPLOYEE.EMPLOYEE_ID,
          EMPLOYEE.FULL_NAME,
          EMPLOYEE.BASIC_SALARY,
          EMPLOYEE.GRADE_CODE,
          GRADE.BONUS_MAGNIFICATION,
          GRADE.FIXED_BONUS
      FROM
          EMPLOYEE
      INNER JOIN GRADE ON EMPLOYEE.GRADE_CODE = GRADE.GRADE_CODE

  この実装のポイント
    * :java:extdoc:`Named<javax.inject.Named>` と :java:extdoc:`Dependent<javax.enterprise.context.Dependent>` をクラスに付与する。
      詳細は、 :ref:`BatchletのNamedとDependentの説明 <getting_started_batchlet-cdi>` を参照。
    * `open` メソッドで処理対象のデータを読み込む。
    * SQLファイルの配置場所や作成方法などは、 :ref:`universal_dao-sql_file` を参照。
    * 大量のデータを読み込む場合は、メモリの逼迫を防ぐために :java:extdoc:`UniversalDao#defer <nablarch.common.dao.UniversalDao.defer()>` を使用して
      検索結果を :ref:`遅延ロード<universal_dao-lazy_load>` する。
    * `readItem` メソッドで読み込んだデータから一行分のデータを返却する。
      このメソッドで返却したオブジェクトが、後続する :java:extdoc:`ItemWriter<javax.batch.api.chunk.ItemProcessor>` の `processItem` メソッドの引数として与えられる。

.. _`getting_started_chunk-business_logic`:

業務ロジックを実行する
++++++++++++++++++++++
賞与の計算等の業務ロジックを実装する。

ItemProcessorの作成
  :java:extdoc:`ItemProcessor<javax.batch.api.chunk.ItemProcessor>` を実装し、
  業務ロジックを行う(永続化処理は :java:extdoc:`ItemWriter<javax.batch.api.chunk.ItemWriter>` の責務であるため実施しない)。

    ==================================================================   =============================================================================================
    インタフェース名                                                       責務
    ==================================================================   =============================================================================================
    :java:extdoc:`ItemProcessor<javax.batch.api.chunk.ItemProcessor>`    一行分のデータに対する業務処理を行う。

                                                                           * `ItemProcessor#processItem`
    ==================================================================   =============================================================================================

  BonusCalculateProcessor.java
    .. code-block:: java

      @Dependent
      @Named
      public class BonusCalculateProcessor implements ItemProcessor {

          @Override
          public Object processItem(Object item) {

              EmployeeForm form = (EmployeeForm) item;
              Bonus bonus = new Bonus();
              bonus.setEmployeeId(form.getEmployeeId());
              bonus.setPayments(calculateBonus(form));

              return bonus;
          }

          /**
           * 社員情報をもとに賞与計算を行う。
           *
           * @param form 社員情報Form
           * @return 賞与
           */
          private static Long calculateBonus(EmployeeForm form) {
              if (form.getFixedBonus() == null) {
                  return form.getBasicSalary() * form.getBonusMagnification() / 100;
              } else {
                  return form.getFixedBonus();
              }
          }
      }

  この実装のポイント
    * `processItem` メソッドで一定数( :ref:`getting_started_chunk-job` にて設定方法を解説)のエンティティを返却した時点で、
      後続する :java:extdoc:`ItemWriter<javax.batch.api.chunk.ItemWriter>` の `writeItems` メソッドが実行される。

.. _`getting_started_chunk-persistence`:

永続化処理を行う
++++++++++++++++++++
DB更新等の、永続化処理を実装する。

ItemWriterの作成
  :java:extdoc:`ItemWriter<javax.batch.api.chunk.ItemWriter>` を実装し、データの永続化を行う。

    ==================================================================   =============================================================================================
    インタフェース名                                                        責務
    ==================================================================   =============================================================================================
    :java:extdoc:`ItemWriter<javax.batch.api.chunk.ItemWriter>`          データを永続化する。

                                                                           * `ItemWriter#writeItems`
    ==================================================================   =============================================================================================

  BonusWriter.java
    .. code-block:: java

      @Dependent
      @Named
      public class BonusWriter extends AbstractItemWriter {

          @Override
          public void writeItems(List<Object> items) {
              UniversalDao.batchInsert(items);
          }
      }

  この実装のポイント
    * :java:extdoc:`UniversalDao#batchInsert <nablarch.common.dao.UniversalDao.batchInsert(java.util.List)>` を使用してエンティティのリストを一括登録する。
    * `writeItems` メソッド実行後にトランザクションがコミットされ、新たなトランザクションが開始される。
    * `writeItems` メソッド実行後、バッチ処理が `readItem` メソッド実行から繰り返される。

.. _`getting_started_chunk-job`:

JOB設定ファイルを作成する
+++++++++++++++++++++++++
JOBの実行設定を記載したファイルを作成する。

  bonus-calculate.xml
    .. code-block:: xml

     <job id="bonus-calculate" xmlns="http://xmlns.jcp.org/xml/ns/javaee" version="1.0">
       <listeners>
         <listener ref="nablarchJobListenerExecutor" />
       </listeners>

       <step id="step1">
         <listeners>
           <listener ref="nablarchStepListenerExecutor" />
           <listener ref="nablarchItemWriteListenerExecutor" />
         </listeners>

         <chunk item-count="1000">
           <reader ref="employeeSearchReader" />
           <processor ref="bonusCalculateProcessor" />
           <writer ref="bonusWriter" />
         </chunk>
       </step>
     </job>

  この実装のポイント
    * ジョブ定義ファイルは `/src/main/resources/META-INF/batch-jobs/` 配下に配置する。
    * `job` 要素 の `id` 属性で、ジョブ名称を指定する。
    * `chunk` 要素の `item-count` 属性で `writeItems` 一回当たりで処理する件数を設定する。
    * 設定ファイルの詳細な記述方法は `JSR352 Specificationを参照(外部サイト、英語) <https://jcp.org/en/jsr/detail?id=352>`_ を参照。

.. |jsr352| raw:: html

  <a href="https://jcp.org/en/jsr/detail?id=352" target="_blank">JSR352(外部サイト、英語)</a>
