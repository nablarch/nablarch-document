How to Specify the Transition Destination When an Error Occurs
===============================================================

.. _forward_error_page-handler:

Define common behavior of handlers
--------------------------------------------------
Transition destination when an error occurs is basically specified by configuring on :ref:`on_error_interceptor` or :ref:`on_errors_interceptor` for the action method.

However when the transition destination screens are to be unified throughout the system,
specifying the annotations for a particular action method may cause omissions or wrong specifications in the transition destination page.
Also, it is very expensive (or is not realistic) to detect errors as it is necessary to make sure that the transition destination is correct for all functions.

Therefore for transitioning to common error page in the system, a handler to manage the transition destination during an error can be added
instead of specifying the transition destination for every particular action.

An example is shown below.

In this example, :java:extdoc:`NoDataException <nablarch.common.dao.NoDataException>` and :java:extdoc:`javax.persistence.OptimisticLockException` are thrown, and then transitions to the dedicated error screen.

.. code-block:: java

  public class ExampleErrorForwardHandler implements Handler<Object, Object> {

    @Override
    public Object handle(Object data, ExecutionContext context){
      try{
        return context.handleNext(data);
      } catch (NoDataException e){
        // When a "no data" error occurs in universal DAO,
        // it moves to the "not found" page.
        throw  new HttpErrorResponse(
            404, "/WEB-INF/view/common/errorPages/pageNotFoundError.jsp", e);
      } catch (OptimisticLockException e){
        // When an optimistic lock occurs, transitions to the screen
        // notifying that the process could not completed due to an update from another user.
        throw  new HttpErrorResponse(
            400, "/WEB-INF/view/common/errorPages/optimisticLockError.jsp", e);
      }
    }
  }

.. _forward_error_page-try_catch:

Implementation method when there are multiple transition destinations for a single exception class
----------------------------------------------------------------------------------------------------
The transition screen during an error may have to be switched depending on where the business exception ( :java:extdoc:`ApplicationException <nablarch.core.message.ApplicationException>` ) occurred.
However, with :ref:`on_error_interceptor`, as only one transition destination can be specified for one exception class,
multiple transition destination screens cannot be specified for :java:extdoc:`ApplicationException <nablarch.core.message.ApplicationException>`.

In such cases, it is necessary to catch the exception and configure the transition destination screen when an error occurs by using ``try-catch`` in the action method.

An example is shown below.

.. code-block:: java

    @InjectForm(form = ClientSearchForm.class, prefix = "form")
    @OnError(type = ApplicationException.class, path = "forward://new")
    public HttpResponse list(HttpRequest request, ExecutionContext context) {

      // Omitted

      try {
        service.save(entity);
      } catch (ApplicationException e) {
        // If an ApplicationException is thrown in save,
        // the screen transitions to a different screen from the one for exceptions thrown elsewhere.
        throw new HttpErrorResponse("forward://index", e);
      }

      return new HttpResponse("/WEB-INF/view/client/complete.jsp");
    }

