Settings
========


Project Settings
----------------

This project needs two things to be set as **environment variables**:

* **DB_URI**: An `RFC-1738`_ url that points to the database. For more info see `sqlalchemy engines`_
* **SERVER_ENCRYPTION_KEY** *(optional)* : A 32-bytes key that will be used by the server
  to encrypt the stored notes index number (not used in on-the-fly notes). Base64 keys that are
  decoded as 32-bytes are also supported. If no key is set, backend generates one and prints
  it in the console. **You need to have this key consistent, for stored-notes to work!**



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
