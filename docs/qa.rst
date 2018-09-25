Questions and answers
=====================


Less technical questions
------------------------

- What is the license for this project?
   **GNU GENERAL PUBLIC LICENSE Version 3**
- This project seems interesting. Can I see a demo somewhere?
   Sure you can! Checkout https://cenot.es which uses the `cenotes-reaction`_ frontend
   using this project as backend
- How can I run this project to experiment?
   See :doc:`run`
- Can I deploy my own server backend?
   Sure you can! See :doc:`deployment`
- Can I learn more about what encryption is used for all these?
   Of course! See :doc:`design`
- I ran / deployed the project, but all I see is text! WTF?
   You probably ran/deployed the backend project. You can write your own frontend to use this functionality or
   use an existing solution such as `cenotes-reaction`_
- Why are there two different projects instead of one complete?
   Splitting the backend from the frontend allows us

   1. To have multiple frontend solutions
   2. To be independent when issuing releases
   3. To be smaller in size
   4. To be able to serve the backend in different machine than the frontend
- Can I contribute to this project somehow?
   Of course, and you're more than welcome! See :doc:`contributing` for more info
- I found a bug! Where do I report?
   See :doc:`contributing` for more info


More technical questions
------------------------
Make sure to check :doc:`design` before reading this

- Why does the user have to use a key that is different than the originally provided password?
   A password is useful to create an encryption and decryption key. The other thing needed is a salt.
   This helps solve attacks with precomputed keys based on passwords. Check about `rainbow tables`_ for more info.
   Thus, to be able to use the password for decryption, you will also have to know the salt. This is the only way
   to create the exact same key that will decrypt the encrypted note. There are a couple of ways to be able to do
   this (which were considered and rejected) because I wanted to minimize the trust on the server:

   1. Have a set of precomputed salts to use

      It is a bad practice to reuse the salts. This will allow attack on multiple notes at the
      same time (since there will be a specifc subset of salts). The server will also have to store
      the salts (which means more trust on the server side). Even if the server is 100% trusted, having the same
      salts, means that you will never be able to change salts (in case of a leak for example), since changing the
      salts will render the old encrypted notes, completely useless.

   2. Store the salt alongside the payload

      Again you put more trust on the server. In case the database is stolen, your encrypted note will be at
      risk, since the attack will be able to create precomputed keys based on that salt. In cases of encrypted
      notes that are not stored on the server, you will have to share the salt somehow secretly along with the
      password (more on this below).

   3. Share the salt in the payload

      The payload in cases of stored notes is simply the index of the encrypted note row in the database.
      The payload is encrypted with the server encryption key and can be shared publicly. Having the salt
      shared in the payload, would mean that someone knowing the server encryption key would be able to find out
      what the salt is. It would also mean that you trust that the server encryption key is good enough to encrypt
      the salt and share it publicly. Whereas now even if the server encryption key is not really good, the only risk
      is leaking and index number of the encrypted note. Which is not a real risk because encryption relies on the fact
      that the adversary **can** have access to the ciphertext. Security through obscurity is never a good idea. In cases
      of encrypted notes that are not stored on the server, the payload is the ciphertext (aka the encrypted note). So you
      would need another part of the url to contain the salt. The only part available is the key part (check below)

   4. Share the salt and the password somehow

      This would not really solve the problem since you cannot share the salt publicly. So this would mean that would
      need to share 2 -instead of 1- things privately. Even if you have aggreed on a specific password, you would still
      need to share 1 thing (the salt) privately. So in the best case, you need to share at least 1 thing privately. Why not
      share the key then?

   5. Did I forget any other scenario?

      If yes, please open an issue (check :doc:`contributing` for more info).
      I prefer to discuss these openly to allow more opinions to be heard and discussed.

- Who am I trusting when using this?
   You trust the server serving the backend and the server serving the frontend (if not the same).
   You trust that the code in the frontend and the backend will not leak your key or note somehow.
- Why not use a front end solution like JS?
   Using a front end solution does not remove the trust factor completely. Unless every time you
   visit a site you thoroughly check the JS running and make sure it won't leak any information.
- Why should I trust the server?
   Anything said will never be 100% sufficient. I cannot prove that you should trust me 100% or the code served.
- I don't trust your server for my notes but I want to use this. What can I do?
   Download the backend code and the frontend code (`cenotes-reaction`_) and set up your own server serving this.
- I don't trust any internet solution (frontend/backend) for encryption operations. What can I do?
   You can use `cenotes-cli`_ which relies on the same encryption modules and supports local encryption before storing remotely.
   With `cenotes-cli` you can even encrypt a note without uploading it and pass it to someone who will be able to decrypt it
   through the site (bare in mind though that this means, that in that case you have a persistent note).
   Otherwise use some other offline encryption solution like PGP, AES etc.
- I tried `cenotes-cli`_ and I really don't understand why when I locally encrypt, I end up with 2 different keys and payloads!
   cenotes backend cannot know if you are uploading an encrypted note or a plaintext note. So the server will always
   encrypt any note you upload. This means that now (since the real note is encrypted with another key), you can share the direct site
   link publicly. The receiver will have to know the extra key (the first one you got) to decrypt the real note.
   For security reasons **there will not be an option to support note uploading without server encryption**. If you want to
   upload your encrypted note without the server making any other actions, encrypt your note locally and use one of the
   thousand note (without encryption) sharing sites to pass it on.
- Why using the duress key results in a message that the note was not found?
   Usage a duress key should be kept secret from the adversary. This means that an adversary should not understand if they used the
   real key but the note was already destroyed, or if they used the duress key. This serves in cases where the "destruction of evidence"
   would result is some kind of punishment.
- What are these algorithm parameters (argon2i min, scrypt interactive, etc) I see?
   As mentioned in the :doc:`design` there are two key derivation algorithms supported: Argon2i and Scrypt.
   Both of these algorithms take some parameters related to how much memory and cpu they are allowed to use.
   Although these are of most importance for storage operations, we chose to expose them to our scenario as well.
   For more information you can read the `pynacl hashing`_ entry or see the `libsodium documentation`_



.. _cenotes-reaction: https://github.com/cenotes/cenotes-reaction
.. _cenotes-cli: https://github.com/cenotes/cenotes-cli
.. _rainbow tables: https://en.wikipedia.org/wiki/Rainbow_table
.. _pynacl hashing: https://pynacl.readthedocs.io/en/stable/password_hashing/#module-level-constants-for-operation-and-memory-cost-tweaking
.. _libsodium documentation: https://libsodium.gitbook.io/doc/
