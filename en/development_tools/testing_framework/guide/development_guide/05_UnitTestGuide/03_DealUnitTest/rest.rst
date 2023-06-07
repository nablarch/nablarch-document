======================================
How to Perform a Subfunction Unit Test
======================================

In web services, mostly subfunctions are completed in one request. If one request = one subfunction, there is no need to perform subfunction unit testing.

If a subfunction is made by multiple requests, a subfunction unit test can be performed by running a series of tests for each request.

Subfunction Unit Test Class Example
-----------------------------------

An example is shown below. Get the target of the update, create the update form from the acquired data, and perform the update. Verify that it is updated as expected.

.. code-block:: java

    @Test
    public void projectUpdateSubfunction() {
        String message1 = "Get the target of the update.";
        RestMockHttpRequest request001 = get("/projects?projectName=Project001");
        HttpResponse response001 = sendRequest(request001);
        assertStatusCode(message1, HttpResponse.Status.OK, response001);
        // Modify the data to be updated retrieved and create a form for the update
        Project project = parseProject(response001).setProjectName("Project888");
        ProjectUpdateForm updateForm = new ProjectUpdateForm(project);

        String message2 = "Project updates.";
        RestMockHttpRequest updateRequest = put("/projects").setBody(updateForm);
        HttpResponse updateResponse = sendRequest(updateRequest);
        assertStatusCode(message2, HttpResponse.Status.OK, updateResponse);

        String message3 = "The project retrieved should match the modified content.";
        RestMockHttpRequest request888 = get("/projects?projectName=Project888");
        HttpResponse response888 = sendRequest(request888);
        assertStatusCode(message3, HttpResponse.Status.OK, response888);
        assertProjectEquals(project, parseProject(response888));
    }

How to take over the information of the previous response, such as cookies
--------------------------------------------------------------------------
In the case of a subfunction unit test, you may want to include the value received from the server as a response to a preceding request, such as a session ID or CSRF token,
in the next request.
In such cases, this can be done in the following ways.

Creates an implementation class for ``RequestResponseProcessor``
****************************************************************
The testing framework for the RESTful web service runtime platform provides :java:extdoc:`RequestResponseProcessor<nablarch.test.core.http.RequestResponseProcessor>` interface
to manipulate the request and response.

Create an implementation class of this interface to fit the requirements of each application.

The framework provides the :java:extdoc:`RequestResponseCookieManager<nablarch.test.core.http.RequestResponseCookieManager>` as a frequently used implementation.
This implementation is able to extract the Cookie with the name specified by the property from the ``Set-Cookie`` header of the response and pass the value to the ``Cookie`` header of the request.

Among the implementations that handle cookies, the framework also provides :java:extdoc:`NablarchSIDManager<nablarch.test.core.http.NablarchSIDManager>` as a specialized implementation for session IDs of the :ref:`session_store` .
This implementation extracts the cookie from the ``Set-Cookie`` header with the default cookie name ``NABLARCH_SID`` of the session ID held by the :ref:`session_store_handler` .
If the cookie name for the session ID is changed from the default, use :java:extdoc:`RequestResponseCookieManager<nablarch.test.core.http.RequestResponseCookieManager>` and specify the cookie name explicitly.

``RequestResponseProcessor`` is used to pass the value of a response received earlier during the execution of one subfunction unit test case to the next request.
At that time, the values extracted from the response are held as states internally to be passed on to the request.
However, if the component is configured in the following way, Nablarch's DI container treats the instance as a singleton,
so the state is shared between multiple test cases unless you explicitly initialize the state.
To prevent this, the framework calls :java:extdoc:`RequestResponseProcessor#reset<nablarch.test.core.http.RequestResponseProcessor.reset()>` for each test case.
If don't want the state to be passed down between test cases, need to implement a ``reset()`` initialization process.
If don't have any internal state or if want to share state between multiple test cases, can make the ``reset()`` method a do-nothing method.

Configure the implementation class with the name ``defaultProcessor`` in the component configuration file
*********************************************************************************************************
.. code-block:: xml

  <component name="defaultProcessor" class="nablarch.test.core.http.RequestResponseCookieManager"/>
    <property name="cookieName" value="JSESSIONID"/>
  </component>


And if want to set up multiple ``RequestResponseProcessor``, can do so by using :java:extdoc:`ComplexRequestResponseProcessor<nablarch.test.core.http.ComplexRequestResponseProcessor>`.

.. code-block:: xml

  <component name="defaultProcessor" class="nablarch.test.core.http.ComplexRequestResponseProcessor">
    <property name="processors">
      <list>
        <component class="nablarch.test.core.http.RequestResponseCookieManager"/>
          <property name="cookieName" value="JSESSIONID"/>
        </component>
        <component class="nablarch.test.core.http.NablarchSIDManager"/>
        <component class="com.example.test.CSRFTokenManager"/>
      </list>
    </property>
  </component>

``RequestResponseProcessor``, named ``defaultProcessor``, will execute :java:extdoc:`RequestResponseProcessor#processRequest<nablarch.test.core.http.RequestResponseProcessor.processRequest(nablarch.fw.web.HttpRequest)>`
before sending the request to the built-in server and :java:extdoc:`RequestResponseProcessor#processResponse<nablarch.test.core.http.RequestResponseProcessor.processResponse(nablarch.fw.web.HttpRequest-nablarch.fw.web.HttpResponse)>`
after receiving the response.
