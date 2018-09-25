Deployment how-to
=================


Deploying the backend
=====================

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

          location /config {
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


Deploying the frontend
======================

Using the packaged bundle

1. Download the latest release from [here](https://github.com/cenotes/cenotes-reaction/releases)
2. Extract, rename as you wish and serve the build folder
    - Example of an nginx configuration (build folder is renamed-> `cenotes-ui`)

    .. code-block:: bash

       server {
           listen 80;
           server_name <your server name / ip>;

           # CENOTES-FRONTEND
           root /var/www/html/cenotes-ui;
           index index.html index.htm;

           location ~* \.(?:manifest|appcache|html?|xml|json)$ {
             expires -1;
           }

           location ~* \.(?:css|js)$ {
             try_files $uri =404;
             expires 1y;
             access_log off;
             add_header Cache-Control "public";
           }

           # Any route containing a file extension (e.g. /devicesfile.js)
           location ~ ^.+\..+$ {
             try_files $uri =404;
           }

        # Any route that doesn't have a file extension (e.g. /devices)
        location / {
            try_files $uri $uri/ /index.html;
        }
       }
3. You will also need to include the endpoint of your backend application
    - If backend is running in the same machine as a uwsgi socket, see the instructions above
    - If backend is running running in another site

    .. code-block:: bash

       server {
           listen 80;
           server_name <your server name / ip>;
           # CENOTES-BACKEND
               location /notes {
                   proxy_pass http://<backend_url>:<port>;
               }

               location /config {
                   proxy_pass http://<backend_url>:<port>;
               }
       }
