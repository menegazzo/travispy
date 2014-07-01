TravisPy
========

TravisPy is a Python API for Travis CI. It follows the `official API <http://docs.travis-ci.com/api/>`_ and is implemented as similar as possible to `Ruby implementation <https://github.com/travis-ci/travis.rb#ruby-library>`_.

.. image:: http://img.shields.io/pypi/v/travispy.svg?style=flat
    :target: https://pypi.python.org/pypi/travispy
    :alt: Latest Version

.. image:: http://img.shields.io/badge/license-GPLv3-brightgreen.svg?style=flat
    :target: https://pypi.python.org/pypi/travispy
    :alt: License

.. image:: http://img.shields.io/travis/menegazzo/travispy.svg?style=flat
    :target: https://travis-ci.org/menegazzo/travispy
    :alt: Build status

.. image:: http://img.shields.io/coveralls/wackou/travispy.svg?style=flat
    :target: https://coveralls.io/r/menegazzo/travispy?branch=master
    :alt: Coveralls

Install
-------

To install TravisPy all it takes is one command line::

    pip install travispy

Usage
-----

TravisPy works just as Travis CI: it authenticates against GitHub. So as a `requirement <http://docs.travis-ci.com/api/#external-apis>`_ you must have a `GitHub Personal access token <https://github.com/settings/applications>`_ with the following scopes:

* read:org
* user:email
* repo_deployment
* repo:status
* write:repo_hook

With your token in hands all is easy::

    >>> from travispy import TravisPy
    >>> t = TravisPy.github_auth(<your_token>)
    >>> t.user()
    <travispy.entities.user.User object at 0x02C26C48>

Please refer to the offical API to learn more about which `entities <http://docs.travis-ci.com/api/#entities>`_ are supported. Soon a specific and detailed documentation related to this library will be available.

Support
-------

Need help? Click `here <https://github.com/menegazzo/travispy/issues?state=open>`_ and open a new issue. You'll get your answer ASAP.

Contribute
----------

TravisPy is under development, so if you want to join the team, you are welcome.

* Feel free to `open issues <https://github.com/menegazzo/travispy/issues?state=open>`_ related to bugs or ideas.

* If you are a developer:

  - Fork TravisPy before making any changes.

  - Write tests.

  - Create a *Pull Request* so changes can be merged.

License
-------

TravisPy is licensed under `GPL v3.0 license <http://www.gnu.org/licenses/gpl.html>`_.