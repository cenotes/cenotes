CENotes
=======

.. image:: https://travis-ci.org/ioparaskev/cenotes.svg?branch=master
        :target: https://travis-ci.org/ioparaskev/cenotes

.. image:: https://readthedocs.org/projects/cenotes/badge/?version=latest
        :target: https://cenotes.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

**C(ryptographical) E(xpendable) Notes**

* Free software: GNU General Public License v3
* Demo: https://cenot.es
* Documentation: https://cenotes.readthedocs.io
* Design: See :doc:`design`
* Release history: See :doc:`history`

What is this?
-------------
A **backend** project to support encryption/decryption of expendable notes

An example using this backend can be found at https://cenot.es

What this isn't
---------------
UI/Frontend. This is a **backend** project. Frontend solutions will be different projects.
The reason for this is to allow flexibility in frontend choice and to avoid huge bundle projects.

A **frontend** project that communicates with the **backend** can be found
`here <https://github.com/ioparaskev/cenotes-reaction>`_

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


How does this work?
-------------------

See :doc:`design`


How to run
----------

See :doc:`run`


How to deploy
-------------

See :doc:`deployment`

Features to be added sometime
-----------------------------

* Modification of a note's settings
   * Zero visit count
   * Change max visits option
   * Change expiration date
* Public key encryption and user database

Q&A
---

See :doc:`qa`


.. _pynacl: https://pynacl.readthedocs.io/en/latest/
