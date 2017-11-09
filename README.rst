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

An example using this backend can be found at https://cenot.es

Features
--------

* Symmetric encryption of notes using the `pynacl`_ project
* On the fly encryption/decryption
   * Notes can be encrypted/decrypted on the fly without storing anything on the server
* Expiration date notes
   * After that date, the notes are deleted and cannot be retrieved (default is never)
* Notes that are deleted after N visits
   * After N retrievals of a note, the note is deleted (default is 1)
* Duress key for immediate note deletion
   * Using the duresss key instead of the real decryption key will delete the note and respond as if
     the note didn't exist (to avoid indicating the use of the duress key)
* Persistent visit notes
   * Notes can be marked as "persistent visit" so that that they are not deleted based on visit count


What this isn't
---------------
UI/Frontend. This is a **backend** project. Frontend solutions will be different projects.
The reason for this is to allow flexibility in frontend choice and to avoid huge bundle projects.

A **frontend** project that communicates with the **backend** can be found
`here <https://github.com/ioparaskev/cenotes-reaction>`_


How to run
----------
Many ways to run this:

* Cloning the repo

   1. Clone the repo

      .. code-block:: bash

         git clone https://github.com/ioparaskev/cenotes.git

   2. Install the requirements

      * With pipenv (suggested)

        .. code-block:: bash

           pip install pipenv
           pipenv install

      * With pip (not suggested):

        .. code-block:: bash

           pip install -r requirements-dev.txt

   3. Set the environment variables as shown in settings_
   4. Set your `PYTHONPATH` to include the project
      .. code-block:: bash

         export PYTHONPATH=<path-to-the-cloned-repo>:$PYTHONPATH

   5. Check your database table as shown in db_schema_ is up-to-date

      .. code-block:: bash

         python manage.py db upgrade


   6. Run the backend

      .. code-block:: bash

         python run_backend.py --help

* Installing the package

   1. Install the package

      .. code-block:: bash

         sudo pip install cenotes

   2. Set the environment variables as shown in settings_
   3. Run the backend

      .. code-block:: bash

         cenotes --help


How to deploy
-------------

Example uwsgi file to use to serve the backend:

   .. code-block:: python

      from cenotes import create_app

      application = create_app()

      if __name__ == "__main__":
          application.run()


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


Maintenance
-----------
To avoid having expired unvisited notes hanging around your database, you will need
to schedule a cleanup to run periodically (cronjob or other way) that will delete
the expired notes. This can be done easily:

* If you have cloned the repo

   .. code-block:: bash

      python cenotes/cli.py --cleanup

* If you have installed the package

   .. code-block:: bash

      cenotes --cleanup


Features to be added sometime
-----------------------------

* Modification of a note's settings
   * Zero visit count
   * Change max visits option
   * Change expiration date
* Public key encryption and user database


.. _pynacl: https://pynacl.readthedocs.io/en/latest/
.. _RFC-1738: https://www.ietf.org/rfc/rfc1738.txt
.. _sqlalchemy engines: http://docs.sqlalchemy.org/en/latest/core/engines.html
