How to run
==========


How to run the backend
----------------------

**You will need Python >= 3.4** *(Python 2 is not supported sorry)*

Many ways to run this:

* Cloning the repo

   1. Clone the repo

      .. code-block:: bash

         git clone https://github.com/cenotes/cenotes.git

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


How to run the cli
------------------

**You will need python >= 3.3**

1. Cloning the repo

   -  Clone the repo

      .. code-block:: bash

        git clone https://github.com/cenotes/cenotes-cli.git

   -  Install the requirements with pipenv

      .. code-block:: bash

         pip install pipenv
         pipenv install

   -  Set your **PYTHONPATH** to include the project

     -  For linux:

      .. code-block:: bash

         export PYTHONPATH=<path-to-the-cloned-repo>:$PYTHONPATH

   -  See available options

      .. code-block:: bash

         python cenotes_cli/cli.py --help

2. Installing the python package

   -  Ideally inside a virtualenv

      .. code-block:: bash

         pip install cenotes-cli

  -  See available options

      .. code-block:: bash

         cenotes-cli --help


How to run the frontend
-----------------------

Cloning the repo and running the NodeJS server with the React components
1. Clone the repo

   .. code-block:: bash

      git clone https://github.com/cenotes/cenotes-reaction.git

2. Install the dependencies

   .. code-block:: bash

      npm install

3. Start the server

   .. code-block:: bash

      npm run start
