Deployment how-to
=================


UWSGI-NGINX
-----------

* Example uwsgi file to use to serve the backend:

   .. code-block:: python

      from cenotes import create_app

      application = create_app()

      if __name__ == "__main__":
          application.run()


   In this case you will also need the uwsgi package to run python code
   (i.e in Debian `uwsgi-plugin-python3`)

* Example uwsgi configuration file to use:

   .. code-block:: bash

      [uwsgi]
      uid = <a ui for the user that will run this>
      gid = <a group id for the group that will have access to this>

      plugin = python3
      chdir = <path where you will serve the backend>

      virtualenv = <path to your virtualenv if you use one>
      master = true
      process   = <number of processes to serve>
      wsgi-file = <path where you will serve the backend>/uwsgi.py

      buffer-size= <the maximum buffer size your backend will accept (default is 4096)>

      socket = /run/uwsgi/app/cenotes/cenotes.sock # or some other path to serve the unix socket
      chmod-socket = 666

      vacuum = true
      die-on-term = true

      env = DB_URI=<your db uri to the database>
      env = SERVER_ENCRYPTION_KEY=<your server encryption key which must be consistent>

* Example of nginx configuration to serve the above

   .. code-block:: bash

      server {
          listen 80;
          server_name <your server ip/domain name>;

          charset     utf-8;

          # CENOTES-BACKEND
          location /notes {
              include uwsgi_params;
              uwsgi_pass  unix:/run/uwsgi/app/cenotes/cenotes.sock;
          }
      }

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
