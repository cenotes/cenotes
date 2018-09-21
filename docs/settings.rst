Settings
========


Project Settings
----------------

This project needs one thing to be set as **environment variables**:

* **DB_URI**: An `RFC-1738`_ url that points to the database. For more info see `sqlalchemy engines`_

**Optionally** four extra variables can be set:

* **SERVER_ENCRYPTION_KEY** : A 32-bytes key that will be used by the server
  to encrypt the stored notes index number (not used in on-the-fly notes). Base64 keys that are
  decoded as 32-bytes are also supported. If no key is set, backend generates one and prints
  it in the console. **You need to have this key consistent, for stored-notes to work!**
* **SUPPORTED_ALGORITHM_PARAMS**: A valid json that contains the algorithms that will be supported
  for the key generation and their hardness. If not set, the application will automatically figure
  which algorithms are supported and their hardness. To see a valid setting that is supported on
  your system, run:

     .. code-block:: bash

        cenotes settings --keygen

  or if you're cloning the repo, run:

     .. code-block:: bash

        python manage.py settings --keygen

* **FALLBACK_ALGORITHM**: An algorithm (scrypt/argon2i if supported) that will be
  used when the request contains no instruction about what algorithm to use in the
  key generation. If not set, this will be automatically set to **scrypt**
* **FALLBACK_ALGORITHM_HARDNESS**: The hardness of the algorithm that will be
  used when the request contains no instruction about what hardness to use in the
  key generation. If not set, this will be automatically set to **interactive**

Database schema
---------------

As mentioned above, you'll need a database connection. The database schema is
simple enough if you want to create it on your own:

   .. code-block:: sql

      CREATE TABLE note (
              id INTEGER NOT NULL,
              max_visits INTEGER,
              visits_count INTEGER,
              payload BLOB NOT NULL,
              expiration_date DATE,
              PRIMARY KEY (id)
      );


.. _RFC-1738: https://www.ietf.org/rfc/rfc1738.txt
.. _sqlalchemy engines: http://docs.sqlalchemy.org/en/latest/core/engines.html
