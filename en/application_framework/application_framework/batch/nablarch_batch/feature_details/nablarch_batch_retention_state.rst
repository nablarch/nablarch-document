.. _nablarch_batch_retention_state:

Retain the Execution Status in Batch Application
==================================================
Sometimes, retaining the status of the batch application during execution may be necessary.
For example, cases when it is necessary to retain the number of registrations or number of updates performed in the batch action.
In such a case, the state is retained in the batch action.

Implementation example of an action that retains the number of registrations is shown below.

For batches that are executed in multiple threads, it is necessary to make sure that the batch
is thread safe in the application. In this example, thread safe is guaranteed by using
:java:extdoc:`AtomicInteger <java.util.concurrent.atomic.AtomicInteger>`.

.. code-block:: java

  public class BatchActionSample extends BatchAction<Object> {

      /** Registration count */
      private AtomicInteger insertedCount = new AtomicInteger(0);

      @Override
      public Result handle(final Object inputData, final ExecutionContext ctx) {
          // Business process

          // Increment of registration count
          insertedCount.incrementAndGet();

          return new Result.Success();
      }
  }

.. tip::

  Using the scope of :java:extdoc:`ExecutionContext <nablarch.fw.ExecutionContext>`,
  the same process as the above implementation example can be realized.
  However, when :java:extdoc:`ExecutionContext <nablarch.fw.ExecutionContext>` is used,
  the disadvantage is that it is difficult to understand what type of value is held.
  Therefore instead of using :java:extdoc:`ExecutionContext <nablarch.fw.ExecutionContext>`,
  retaining the conditions in the batch action as shown in the above implementation example is recommended.

  When :java:extdoc:`ExecutionContext <nablarch.fw.ExecutionContext>` is used, the concept of scope is as follows:

  :Request scope: Area that holds the state for each thread
  :Session scope: Area that holds the state for the entire batch

