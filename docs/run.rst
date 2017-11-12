How to run
==========

**You will need Python 3** *(Python 2 is not supported sorry)*

Many ways to run this:

* Cloning the repo

   1. Clone the repo

      .. code-block:: bash

         git clone https://github.com/ioparaskev/cenotes.git

   2. Install the requirements

      * With pipenv (suggested)

        .. code-block:: bash

           pip install pipenv
           pipenv --three install

      * With pip (not suggested):

        .. code-block:: bash

           pip install -r requirements-dev.txt

   3. Set the environment variables as shown in :doc:`settings`
   4. Set your `PYTHONPATH` to include the project

      .. code-block:: bash

         export PYTHONPATH=<path-to-the-cloned-repo>:$PYTHONPATH

   5. Check your database table as shown in :doc:`settings` is up-to-date

      .. code-block:: bash

         python manage.py db upgrade


   6. Run the backend

      .. code-block:: bash

         python run_backend.py --help

* Installing the package

   1. Install the package

      .. code-block:: bash

         sudo pip install cenotes

   2. Set the environment variables as shown in :doc:`settings`
   3. Run the backend

      .. code-block:: bash

         cenotes --help


