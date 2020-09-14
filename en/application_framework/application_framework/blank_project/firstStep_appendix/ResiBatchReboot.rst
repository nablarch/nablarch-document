===============================================================================================
To Restart Messaging Using Tables as Queues
===============================================================================================

Summary
============

If messaging that has used a table as a queue is to be restarted after it has been terminated once, then the processing complete flag of the data to be processed must be reconfigured.


Step
============

You can reset the data in the following ways.

1. Execute h2/bin/h2.bat.

.. tip::

  Be sure to launch the h2.bat file that is included in the batch project whose data is to check be checked.


2. After a while, the browser will start, now enter each item as follows and click the [Test Connection] button.

============= ========================= ============================================================================
Item          Value                     Supplementary notes
============= ========================= ============================================================================
JDBC URL      ``jdbc:h2:../db/SAMPLE``  As shown on the left, it is necessary to specify the data file location
                                        with a relative path from h2.bat.
User Name     ``SAMPLE``
Password      ``SAMPLE``
============= ========================= ============================================================================

3. Check that "Test successful" is displayed at the bottom of the screen.

4. Re-enter the Password field and click the [Connect] button.

.. important ::

  When the [Connect] button is clicked, if the H2 data file does not exist at the specified URL, a new H2 data file is created.

  To avoid trouble, be sure to click on [Test Connection] as shown in Step 2 to confirm the existence of the data file.


5. Since the upper part of the right pane is the space for entering SQL, enter the following SQL in this part.

.. code-block:: sql

  DELETE FROM SAMPLE_USER WHERE USER_INFO_ID = '00000000000000000001';

  INSERT INTO SAMPLE_USER(
    USER_INFO_ID
    , LOGIN_ID
    , KANA_NAME
    , KANJI_NAME
    , STATUS
  ) VALUES (
    '00000000000000000001'
    , 'tarou'
    , 'Tarou'
    , 'TAROU'
    , '0' -- 0: Not processed
  );

  COMMIT;


.. tip ::

  The SQL above sets the state of the records to be processed for messaging using the table as a queue to "Unprocessed".


6. Click the [Run] button (green button) at the top of the screen.

7. Disconnect by clicking the upper left disconnect button (button with the icon written in red).

.. important ::

  Projects generated from the archetype use the built-in mode of H2.

  When using the built-in mode, it will only accept connections from a single process.

  Therefore, **if you forget to disconnect, your application will not be able to connect to H2**.


.. |br| raw:: html

  <br />