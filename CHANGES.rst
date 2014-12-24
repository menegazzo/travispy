Changes
=======

v0.3.3 (2014-12-24)
-------------------

* Providing proper access to ``Repo.active`` when this is not returned from API.
* Providing proper access to ``Job.duration`` when this is not returned from API.

v0.3.2 (2014-10-20)
-------------------

* Handling unexpected errors (such as JSON decode error or connection timeout).

v0.3.1 (2014-10-16)
-------------------

* Raising errors when API response status code is different than 200.

v0.3.0 (2014-10-13)
-------------------

* Added new entities Branch and Commit.
* Now each entity class knows how to retrieve information from Travis CI
  instead addressing it to Session.
* PEP8 was applied to all code.

v0.2.0 (2014-08-05)
-------------------

* Added support for loading objects from lazy information
* Now Repo, Build and Job entities are stateful

v0.1.1 (2014-06-30)
-------------------

* Added support for Python 2.6, 2.7, 3.2, 3.3, 3.4 and PyPy
* Fixed error when trying to access Travis with and invalid GitHub token
* Removed package "_tests" from distribution

v0.1.0 (2014-06-23)
-------------------

* Initial beta release
