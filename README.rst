CENotes
=======

.. image:: https://travis-ci.org/ioparaskev/cenotes.svg?branch=master
        :target: https://travis-ci.org/ehloonion/cenotes

.. image:: https://readthedocs.org/projects/cenotes/badge/?version=latest
        :target: https://cenotes.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

**C(ryptographical) E(xpendable) Notes**

* Free software: GNU General Public License v3
* Documentation: https://cenotes.readthedocs.io

What is this?
-------------
A **backend** project to support encryption/decryption of expendable notes

Features
--------

* Symmetric encryption of notes using the `pynacl`_ project
* On the fly encryption/decryption
   * Notes can be encrypted/decrypted on the fly without storing anything on the server
* Expiration date notes
   * After that date, the notes are deleted and cannot be retrieved (default is never)
* Notes that are deleted after N visits
   * After N retrievals of a note, the note is deleted (default is 1)
* Persistent visit notes
   * Notes can be marked as "persistent visit" so that that they are not deleted based on visit count


What this isn't
---------------
UI/Frontend. This is a **backend** project. Frontend solutions will be different projects.
The reason for this is to allow flexibility in frontend choice and to avoid huge bundle projects.


How to run
----------
Many ways to run this:

* Cloning the repo

   1. Clone the repo

      .. code-block:: python

         git clone https://github.com/ioparaskev/cenotes.git

   2. Install the requirements

      * With pipenv (suggested)

        .. code-block:: python

           pip install pipenv
           pipenv install

      * With pip (not suggested):

        .. code-block:: python

           pip install -r requirements-dev.txt

   3. Set the environment variables as shown in settings_
   4. Check your database table as shown in db_schema_ is up-to-date

      .. code-block:: python

         python manage.py db upgrade


   5. Run the backend

      .. code-block:: python

         python run_backend.py --help

* Installing the package

   1. Install the package

      .. code-block:: python

         sudo pip install cenotes

   2. Set the environment variables as shown in settings_
   3. Run the backend

      .. code-block:: python

         cenotes --help


.. _settings:

Project Settings
----------------

This project needs two things to be set as **environment variables**:

* **DB_URI**: An `RFC-1738`_ url that points to the database. For more info see `sqlalchemy engines`_
* **SERVER_ENCRYPTION_KEY** *(optional)* : A 32-bytes key that will be used by the server
  to encrypt the stored notes index number (not used in on-the-fly notes). Base64 keys that are
  decoded as 32-bytes are also supported. If no key is set, backend generates one and prints
  it in the console. **You need to have this key consistent, for stored-notes to work!**


.. _db_schema:

Database schema
---------------

As mentioned in settings_, you'll need a database connection. The database schema is
simple enough:

   .. code-block:: sql

      CREATE TABLE note (
              id INTEGER NOT NULL,
              max_visits INTEGER,
              visits_count INTEGER,
              payload BLOB NOT NULL,
              expiration_date DATE,
              PRIMARY KEY (id)
      );


Features to be added soon
-------------------------

* Modification of a note's settings
   * Zero visit count
   * Change max visits option
   * Change expiration date
* Triggering manual deletion of a note (bypass note settings and delete immediately)
* Public key encryption and user database


.. _pynacl: https://pynacl.readthedocs.io/en/latest/
.. _RFC-1738: https://www.ietf.org/rfc/rfc1738.txt
.. _sqlalchemy engines: http://docs.sqlalchemy.org/en/latest/core/engines.html
