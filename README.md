# CENotes

[![image](https://travis-ci.org/cenotes/cenotes.svg?branch=master)](https://travis-ci.org/cenotes/cenotes)
[![Documentation
Status](https://readthedocs.org/projects/cenotes/badge/?version=latest)](https://cenotes.readthedocs.io/en/latest/?badge=latest)

**C(ryptographical) E(xpendable) Notes**

  - Free software: GNU General Public License v3

  - [Demo](https://cenot.es)

  - Source code:
        
    - [Backend](https://github.com/cenotes/cenotes)
    - [Frontend](https://github.com/cenotes/cenotes-reaction)
    - [CLI](https://github.com/cenotes/cenotes-cli)
    - [Libraries](https://github.com/cenotes/cenotes-lib)

  - [Documentation](https://cenotes.readthedocs.io)

  - [Design](https://cenotes.readthedocs.io/en/latest/design.html)

  - [Release history](https://cenotes.readthedocs.io/en/latest/history.html)

## What is this?

A **backend** project to support encryption/decryption of expendable
notes

An example using this backend can be found at <https://cenot.es>

## What this isn't

UI/Frontend. This is a **backend** project. Frontend solutions will be
different projects. The reason for this is to allow flexibility in
frontend choice and to avoid huge bundle projects.

- A **frontend** project that communicates with the **backend** can be
found [here](https://github.com/cenotes/cenotes-reaction)

- A **cli** project to test the encrypt/decrypt actions offline can be found 
[here](https://github.com/cenotes/cenotes-cli). Backend project uses this package 
for every crypto action

## Features

  - Symmetric encryption of notes using the
    [pynacl](https://pynacl.readthedocs.io/en/latest/) project

  - On the fly encryption/decryption
      - Notes can be encrypted/decrypted on the fly without storing
        anything on the server
  - Expiration date notes
    
      - After that date, the notes are deleted and cannot be
        retrieved (default is never)
  - Notes that are deleted after N visits
      - After N retrievals of a note, the note is deleted (default
        is 1)
  - Duress key for immediate note deletion
      - Using the duress key instead of the real decryption key
        will delete the note and respond as if the note didn't exist
        (to avoid indicating the use of the duress key)
  - Persistent visit notes
      - Notes can be marked as "persistent visit" so that that they
        are not deleted based on visit count

## How does this work?

See [design](https://cenotes.readthedocs.io/en/latest/design.html)

## How to run

See [how to run](https://cenotes.readthedocs.io/en/latest/run.html)

## How to deploy

See [deployment](https://cenotes.readthedocs.io/en/latest/deployment.html)

## Features to be added sometime

  - Modification of a note's settings
    - Zero visit count
    - Change max visits option
    - Change expiration date
  - Public key encryption and user database

## Q\&A

See [Questions and answers](https://cenotes.readthedocs.io/en/latest/qa.html)
