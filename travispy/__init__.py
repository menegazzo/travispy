'''
|travispy| is a Python API for |travisci|. It follows the `official API`_ and is implemented as
similar as possible to `Ruby`_ implementation.

Experimental methods will not be supported until they become official.

For full documentation please refer to |travisci| `official API`_ documentation.

.. image:: http://img.shields.io/pypi/v/TravisPy.svg?style=flat
    :target: https://pypi.python.org/pypi/TravisPy
    :alt: Latest Version

.. image:: http://img.shields.io/badge/license-GPLv3-brightgreen.svg?style=flat
    :target: http://www.gnu.org/licenses/gpl-3.0-standalone.html
    :alt: License

.. image:: http://img.shields.io/travis/menegazzo/travispy/v0.3.5.svg?style=flat
    :target: https://travis-ci.org/menegazzo/travispy
    :alt: Build status

.. image:: http://img.shields.io/coveralls/menegazzo/travispy/v0.3.5.svg?style=flat
    :target: https://coveralls.io/r/menegazzo/travispy
    :alt: Coveralls
'''
from .entities import *
from .travispy import TravisPy
