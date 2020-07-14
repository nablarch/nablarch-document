====================================================
How to Perform a Request Unit Test (File Upload)
====================================================


File upload test is a type of web application test.
Therefore, an :doc:`index` of the web application is assumed to execute the test file upload.

When testing a file upload, it is necessary to specify the upload file in the HTTP request parameter.
This section describes how to specify an upload file in the HTTP request parameters.



How to write the upload file
==============================

The upload file can be specified in the HTTP request parameter
by writing the following in the value of the HTTP request parameter.

.. code-block:: text

 ${Attach: File path}

.. tip::
 The file path is described as a **relative path from the current directory during test execution**,
 that is, a relative path from the project root directory.
 

For binary files
======================

To upload a binary file such as an image file,
place the file in advance and specify the path to the file.


In the following example, picture.png in the test/resources/images directory
under the project is uploaded with the key "uploadfile".

.. code-block:: text

  <project_root>
       + test
          + resources
             + images
                + picture.png

------


``LIST_MAP=requestParams``

+---------------------------------------------------+----------------------+-----------+
| uploadfile                                        | comment              | public    |
+===================================================+======================+===========+
| ``${attach:test/resources/images/picture.png}``   | Upload.              | ``false`` |
+---------------------------------------------------+----------------------+-----------+


------

In the case of fixed-length file or CSV file
=============================================

To upload a :ref:`fixed-length file<how_to_setup_fixed_length_file>`
or a :ref:`CSV file<how_to_setup_csv_file>`,
include the contents of the file in the test datasheet.
When the test is executed, the automated test framework creates a file based on this data.


In the following example, the member_list.csv file is created under the work directory
and specified as an upload target.

------

``LIST_MAP=requestParams``

+------------------------------------+-----------------------------------+
| uploadfile                         |  comment                          |
+====================================+===================================+
| ``${attach:work/member_list.csv}`` |  Register new members for October |
+------------------------------------+-----------------------------------+


``SETUP_FIXED=work/member_list.csv``


     
// Directive

+------------------+-------------+----------------------------+
|text-encoding     |Windows-31J  |                            |
+------------------+-------------+----------------------------+
|record-separator  |CRLF         |                            |
+------------------+-------------+----------------------------+

// Data

+-------------+-----+-----------------------------------------+
| name        | age |        address                          |
+=============+=====+=========================================+
| Yamada Taro |  30 |1-1 Shibaura, Minato-ku, Tokyo           |
+-------------+-----+-----------------------------------------+
| Tanaka Jiro |  20 |2-2 Higashidamachi, Kadoma City, Osaka   |
+-------------+-----+-----------------------------------------+

------

.. tip::
 Even when uploading a fixed-length or CSV file,
 it is possible to prepare the file in advance like in the case of a binary file,
 but it should be described in the test data sheet in consideration of the ease of maintenance of the test data.
 
