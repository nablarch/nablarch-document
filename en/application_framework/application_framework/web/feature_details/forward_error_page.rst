エラー時の遷移先の指定方法
==================================================

.. _forward_error_page-handler:

ハンドラで共通の振る舞いを定義する
--------------------------------------------------
エラー発生時の遷移先は、基本的にアクションのメソッドに対して :ref:`on_error_interceptor` や :ref:`on_errors_interceptor` を設定して指定する。

しかし、システム全体で遷移先の画面を統一したい場合に、個別のアクションメソッドに対してアノテーションを指定するやり方では、
漏れが発生したり遷移先のページの指定ミスが発生する可能性がある。
また、誤りを検知するには全機能に対して遷移先が正しいことを確認する必要があり、非常にコストが高くなる(またこれは現実的ではない)。

このため、システムで共通のエラーページに遷移させる場合には、個別のアクションに対して遷移先を指定するのではなく、
エラー時の遷移先を制御するハンドラを追加して対応すると良い。

以下に例を示す。

この例では、 :java:extdoc:`NoDataException <nablarch.common.dao.NoDataException>` と :java:extdoc:`javax.persistence.OptimisticLockException` が発生した場合に、専用のエラー画面へ遷移させている。

.. code-block:: java

  public class ExampleErrorForwardHandler implements Handler<Object, Object> {

    @Override
    public Object handle(Object data, ExecutionContext context){
      try{
        return context.handleNext(data);
      } catch (NoDataException e){
        // ユニバーサルDAOで対象データなしエラーが発生した場合は、
        // not foundを表すページに遷移する。
        throw  new HttpErrorResponse(
            404, "/WEB-INF/view/common/errorPages/pageNotFoundError.jsp", e);
      } catch (OptimisticLockException e){
        // 楽観ロックエラーが発生した場合は、他のユーザに更新されたため処理が
        // 完了できなかったことを通知する画面に遷移する。
        throw  new HttpErrorResponse(
            400, "/WEB-INF/view/common/errorPages/optimisticLockError.jsp", e);
      }
    }
  }

.. _forward_error_page-try_catch:

1つの例外クラスに対して複数の遷移先がある場合の実装方法
---------------------------------------------------------
業務例外( :java:extdoc:`ApplicationException <nablarch.core.message.ApplicationException>` )が発生した箇所によって、エラー時の遷移先画面を切り替えたい場合がる。
しかし、 :ref:`on_error_interceptor` では、例外クラスに対して1つの遷移先しか指定することができないため、
:java:extdoc:`ApplicationException <nablarch.core.message.ApplicationException>` に対して複数の遷移先の画面を指定することができない。

このような場合は、アクションのメソッド内で ``try-catch`` を用いて、例外を捕捉しエラー時の遷移先画面を設定する必要がある。

以下に例を示す。

.. code-block:: java

    @InjectForm(form = ClientSearchForm.class, prefix = "form")
    @OnError(type = ApplicationException.class, path = "forward://new")
    public HttpResponse list(HttpRequest request, ExecutionContext context) {

      // 省略

      try {
        service.save(entity);
      } catch (ApplicationException e) {
        // saveで発生したApplicationExceptionは、
        // 他の箇所で発生した時とは異なる画面に遷移させる
        throw new HttpErrorResponse("forward://index", e);
      }

      return new HttpResponse("/WEB-INF/view/client/complete.jsp");
    }

