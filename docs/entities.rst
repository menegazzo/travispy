.. |travispy| replace:: **TravisPy**
.. |travisci| replace:: *Travis CI*
.. |github| replace:: *GitHub*

.. _official API: http://docs.travis-ci.com/api/
.. _Ruby: https://github.com/travis-ci/travis.rb#ruby-library
.. _requirement: http://docs.travis-ci.com/api/#external-apis
.. _access token: https://github.com/settings/applications
.. _entities: http://docs.travis-ci.com/api/#entities
.. _open issues: https://github.com/menegazzo/travispy/issues?state=open

========
Entities
========

This document brings information about all entities that are used by |travispy| API.

.. autoclass:: Session
    :no-show-inheritance:

.. module:: travispy.entities._entity
.. autoclass:: Entity
    :no-show-inheritance:

.. module:: travispy.entities._restartable
.. autoclass:: Restartable

.. module:: travispy.entities
.. autoclass:: Account

.. autoclass:: Broadcast

.. autoclass:: Build

.. autoclass:: Hook

.. autoclass:: Job

.. autoclass:: Log

.. autoclass:: Repo

.. autoclass:: User
