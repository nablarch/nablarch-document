.. _authentication_pbkdf2:

====================================================
Sample Password Encryption Function Using PBKDF2
====================================================

This is an implementation sample that encrypts the password using `PBKDF2 <https://www.ietf.org/rfc/rfc2898.txt>`_.


-----------------
Delivery package
-----------------

The sample is provided in the following package.

  *please.change.me.*\ **common.authentication.encrypt**


------------
Summary
------------

An sample implementation of the function to encrypt passwords with salt addition and stretching using PBKDF2 is provided.

This sample is intended to be used in :doc:`../index`.


------------
Request
------------

Implemented
========================

* Even if the same password is being used by multiple users, different values can be used for the encrypted password.
* The string length before encryption can be set to a sufficient length for preventing password cracking using rainbow tables.
* By changing the time required to calculate the encrypted password once, it is possible to take measures against password cracking using brute force.


Not yet considered
========================

* A random salt can be added to each user.
* The salt can be kept in a secure storage outside the database.


-------------------------------------------------------
Details of the password encryption function
-------------------------------------------------------

This function uses one of the key derivation functions `PBKDF2 <https://www.ietf.org/rfc/rfc2898.txt>`_ to encrypt the password.
The encrypted password is returned as a Base64-encoded character string.

This function uses a byte sequence that concatenates "system common fixed value" and "user ID" as a salt,
so that even if different users use the same password, the encrypted password will be different.

The `fixedSalt` property described below can be used to provide salt of sufficient length as a measure against rainbow table,
and the `iterationCount` property to provide a stretching count as a measure against brute-force.

See :ref:`pbkdf2IterationCount` for reference information on how to examine stretching counts.


------------------
How to configure
------------------

This section describes how to configure the function.

.. code-block:: xml

  <!-- Configuring the password encryption module -->
  <component name="passwordEncryptor"
             class="please.change.me.common.authentication.encrypt.PBKDF2PasswordEncryptor">

    <!-- Configure a fixed string to be used shared for salts in the system.Set a string of 20 bytes or more. -->
    <property name="fixedSalt" value=" !!! please.change.me !!! TODO: MUST CHANGE THIS VALUE." />

    <!-- Configure the stretching count so that the calculation time is about 10000 times more than the SHA-256 hash calculation. -->
    <property name="iterationCount" value="3966" />

    <!-- Configure the length (number of bits) of the encrypted password. -->
    <property name="keyLength" value="256" />
  </component>


A description of the property is given below.

===================== ===================================================================================================================================================================================
property name         Settings
===================== ===================================================================================================================================================================================
fixedSalt (required)  A fixed string is used for the salt that is common to all systems. The actual salt is a sequence of bytes that concatenates this string with the user ID.

                      .. important::

                        This configuration value is related to the encryption strength of the password. If the value is set too short,
                        it leaves the user vulnerable to password decryption using the rainbow table.

                        Since salt concatenates the user ID,  ensure that the byte sequence concatenating this string and the user ID is **more than 20 bytes** [#]_ in length.
                        (It is recommended to secure 20 bytes with just this configuration alone.)

iterationCount        Number of times password encryption is stretched.Default value is 3966. [#]_

                      Considering the fact that several thousand to tens of thousands of stretching times are generally recommended and load on the system,
                      the number of times stretching is preformed should be set so that the calculation time is about 10000 times longer than the calculation time with a hash function such as SHA-256.

                      :ref:`pbkdf2IterationCount` provides reference information on how to consider stretching counts.

                      .. tip::

                        The stretching process is a process with high CPU load.

                        Specify ``1`` for systems that are not complaint with PCI DSS and special security is not required.

keyLength             The length of the encrypted password (bits). Default value is 256.

                      Since the hash function used internally is SHA-256, set the value to 256 or more.

                      The length of the string generated by using this function is the length obtained
                      by encoding the byte string of the length specified here with Base64.
===================== ===================================================================================================================================================================================

.. [#]

   As of January 2014, since it has been confirmed that a rainbow table supporting a string of 14 characters or more has been sold, 20 characters or more is recommended here.
   Before using it in a project, be sure to check the latest information and set a salt length that can be assumed to be sufficient.

.. [#]

   Although the number 3966 has no particular meaning, the value is a stretching number that serves the purpose, and it has been configured considering that the threat of password decryption
   can be mitigated by configuring a value that is not easy to guess, rather than specifying a convenient number that is easy to guess.


.. _pbkdf2IterationCount:

Configuration value of stretching count
========================================

How the default value of the stretching count was arrived at in this sample implementation is described.

As a basic policy, the number of stretching times is determined based on the following information.

1. How many seconds does it take to complete a brute-force operation if the password is hashed without SHA-256 stretching?
2. Determine the target value for the time required to complete the brute force,
   and how many times of the time taken to hash a password once is needed to achieve the target value in the case of SHA-256.

The following information has been collected for examination in the above policy.

**Number of hash value calculations per second**
  In November 2013, a server capable of computing 100,000,000,000,000 times of SHA-256 per second was available for sale.

**Password strength**
  When a password of "more than 8 mixed alphanumeric characters" is enforced, it takes 62^8 calculations to complete a brute force attack.

**Target time to complete a brute force attack**
  1 year

From the above information, the following is obtained if we calculate how many times the calculation time of one hash value in PBKDF2
should be set as the calculation time for one hash value in SHA-256.

1. Time to complete password brute force process without SHA-256/stretching::

     (62^8) / (10^11) ~= 2183 (s)

2. To extend the above time to the target value, how many times should the time to calculate the hash value of the password be in the case of SHA-256?:

     (60*60*24*365) / ((62^8) / (10^11)) ~= 14444

From this value, it is clear that the `iterationCount` should be set so that the calculation time for PBKDF2 is about 15,000 times or more than that for SHA-256.

According to the measurement results on the development PC (CPU: Intel(R) Core(TM) i7-4770 3.40GHz), the calculation time of PBKDF2 is about 15,000 times longer than SHA-256,
and it can take one year to complete a brute-force attack if the iteration count is about 3500 to 4000 times.

In the measurement with the above PC, the calculation time of once for PBKDF2 when iterationCount was set to 4000 was about 15 ms to 20 ms.
This value is adopted as the default value because it is not considered to be a bottleneck for login processes
where a response time of about one second is assumed.

While the PBKDF2 encryption process is being executed, this process almost occupies the CPU.
Verify whether the time that the encryption process occupies the CPU in the actual operating environment is within the allowable time.
