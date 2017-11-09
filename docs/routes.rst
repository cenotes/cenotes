===============
Endpoint routes
===============


Currently available routes and methods
--------------------------------------
* decrypt_note
    * /notes/<enote_id_or_payload>/<key>
    * HEAD,OPTIONS,GET
* decrypt_json_note
    * /notes/
    * POST,OPTIONS
* encrypt_note
    * /notes/encrypt/
    * /notes/encrypt/<key>/
    * OPTIONS,POST
* **currently not working**
    * modify_note
        * /notes/<enote_id>
        * /notes/<enote_id>/<key>
        * OPTIONS,PATCH
    * delete_note
        * /notes/<enote_id>
        * /notes/<enote_id>/<key>
        * DELETE,OPTIONS

Finding routes and accepted methods
-----------------------------------

You can see available endpoints and methods through manage.py

.. code-block:: python

    python manage.py routes
