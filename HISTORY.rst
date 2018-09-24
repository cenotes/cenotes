=======
History
=======
0.8.1 (2018-09-24)
------------------
* Add test discovery and inclusion to setup.py

0.8.0 (2018-09-21)
------------------
* Add support to choose algorithm and hardness for the key generation. This allows
  user to choose how paranoid and willing to wait they are for an encrypted note

0.7.5 (2018-05-08)
------------------
* Fix flask 1.+ issues with json

0.7.4 (2018-05-07)
------------------
* Change long description to README.md for pypi view

0.7.3 (2018-05-07)
------------------
* Add long_description content type in setup.py

0.7.2 (2018-05-07)
------------------
* Add include of tests and README.md and LICENSE in MANIFEST

0.7.1 (2017-12-14)
------------------
* Custom 500 error handler
* Catching errors in case of malformed json
* QA update for cenotes-cli

0.7.0 (2017-12-14)
------------------
* Use the external package cenotes-lib

0.6.0 (2017-12-12)
------------------
* Use the external package cenotes-cli that provides cenotes_lib
* Officially drop py < 3.4 support

0.5.3 (2017-11-12)
------------------

* Big updates in documentation about design choices, and better documentation structure
* Updates obsolete HISTORY file

0.5.2 (2017-11-11)
------------------

* Fix MANIFEST typo

0.5.1 (2017-11-10)
------------------

* Add cleanup command for expired notes

0.5.0 (2017-11-09)
------------------

* Add duress key support to allow an immediate deletion in cases of emergency
* Update documentation

0.4.0 (2017-11-09)
------------------

* Allow post request for decrypt mode to have shorter urls in no-store cases
* Update documentation

0.3.0 (2017-10-23)
------------------

* Fixes on the packaged version

0.2.2 (2017-10-23)
------------------

* First release
