===============
Endpoint routes
===============


Currently available routes and methods
--------------------------------------
* decrypt_note
    * /notes/<enote_id_or_payload>/<key>
    * HEAD,OPTIONS,GET
* delete_note
    * /notes/<enote_id>
    * /notes/<enote_id>/<key>
    * DELETE,OPTIONS
* encrypt_note
    * /notes/encrypt/
    * /notes/encrypt/<key>/
    * OPTIONS,POST
* index
    * /notes/
    * HEAD,OPTIONS,GET
* modify_note
    * /notes/<enote_id>
    * /notes/<enote_id>/<key>
    * OPTIONS,PATCH


Finding routes and accepted methods
-----------------------------------

You can see available endpoints and methods through manage.py

.. code-block:: python

    python manage.py routes
