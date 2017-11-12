Design decisions
================


Algorithms
----------

To encrypt the information, this software makes use of the **secret key encryption** of the
`PyNaCL package`_. Currently the `Salsa20`_ stream cipher is used for the encryption and
`Poly1305`_ for the data integrity. The **key derivation** currently is achieved using the
**scrypt** algorithm in combination with the **Salsa 20/8** core algorithm and the **Pbkdf2-SHA256**.
Salt is calculated on the fly, and there are no precomputed salts. This is the current kdf
function the PyNaCL package provides. In a future release this will be replaced by the
argon2i algorithm.


How magic happens
-----------------

When storing on server
~~~~~~~~~~~~~~~~~~~~~~

**Encryption**

- The server receives the plaintext and a password
- Using the password and the aforementioned key derivation function (kdf), a key is created
- With that **password derived key**, the server encrypts the plaintext and stores the encrypted payload on the database
- The server encrypts with the **server key** the primary key of the row that corresponds to the encrypted payload
- The server generates random bytes and encrypts them with the **server key** to use as a **duress key**
- The server sends back the server-key-encrypted primary key, the encryption key and the duress key, all url-safe encoded with base64


**Decryption**

- The server receives a payload and a key
- Decoding the payload, the server tries to decrypt it with the **server key** (if it fails, it assumes this is a no-store payload)
- Using the decoded and decrypted payload it finds the id that corresponds to the encrypted payload row
- The server tries to decrypt the **user provided key** with the **server key**
   - If that succeeds, it means this is a **duress key**. The server deletes the correspondin payload row and reports back that
     an invalid key / payload was provided. This is to completely hide the use of the duress key
   - If that fails, it means this is **not a duress key**. The server uses the **user provided key** to decrypt the payload
     and returns the plaintext


When **not** storing on server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Encryption**

- The server receives the plaintext and a password
- Using the password and the aforementioned key derivation function (kdf), a key is created.
- With that **password derived key**, the server encrypts the plaintext
- The server sends back the password-derived-key-encrypted payload and the encryption key, all url-safe encoded with base64

**Decryption**

- The server receives a payload and a key
- Decoding the payload, the server tries to decrypt it with the **server key**  and fails
- Using the decoded **user-key** it decrypts the encrypted payload
- The server returns to the user the plaintext

Notice here that there is no *duress key*. This is because the encrypted payload is not stored anywhere. This means that
**anyone** who holds the key, applying the decryption procedure mentioned above will be able to decrypt the payload. This can
happen at any time for as many times anyone wants. This information is persistent and the only way to stop this from happening
is to make the payload or the key disappear. **Be extremely careful when using this option**


Questions?
----------

For questions regarding these design choices, take a look at :doc:`qa` and if this doesn't satisfy you,
open an issue (for more details see :doc:`contributing`).

.. _PyNaCL package: https://pynacl.readthedocs.io/en/latest/
.. _Salsa20: https://en.wikipedia.org/wiki/Salsa20
.. _Poly1305: https://en.wikipedia.org/wiki/Poly1305
