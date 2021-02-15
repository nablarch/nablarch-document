
===========================================================
Procedure for Changing the Message ID and Message Content
===========================================================

Summary
================================================================

The default configuration of the message IDs and messages to be notified to users is described in the projects generated from the archetype.

It is necessary to change these message IDs and messages after checking the content.

For the message management function in Nablarch, see :doc:`../../libraries/message`.


How to change the link between error content and message ID
============================================================

Error content is linked to the message ID in src/main/resources/common.properties

In common.properties, the item described as "Message ID of XXX (XXXのメッセージID)" in the comment, is the item that links the error content to the message ID.

For example, in the following statement, M000000017 is the message ID.

.. code-block:: text

  # Message ID when a non-full-width character is entered
  # (change the set value in accordance with the ID system of TODO PJ) (TODO PJのID体系に併せて設定値を変更)
  nablarch.zenkakuCharset.messageId=M000000017


By changing the value of the item, the link between the error content and the message ID can be changed.


How to change the link between message ID and message
=======================================================

By default, message IDs and messages are linked in src/main/resources/messages.properties.

By editing this file, you can change the links.

