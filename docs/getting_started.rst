.. |travispy| replace:: **TravisPy**
.. |travisci| replace:: *Travis CI*
.. |github| replace:: *GitHub*

.. _official API: http://docs.travis-ci.com/api/
.. _Ruby: https://github.com/travis-ci/travis.rb#ruby-library
.. _requirement: http://docs.travis-ci.com/api/#external-apis
.. _access token: https://github.com/settings/applications
.. _entities: http://docs.travis-ci.com/api/#entities
.. _open issues: https://github.com/menegazzo/travispy/issues?state=open

===============
Getting started
===============

|travispy| works just as |travisci|: it authenticates against |github|. So as a `requirement`_ you
must have a |github| `access token`_ with the following scopes:

* read:org
* user:email
* repo_deployment
* repo:status
* write:repo_hook

With your token in hands all is easy::

    >>> from travispy import TravisPy
    >>> t = TravisPy.github_auth(<your_github_token>)
    >>> user = t.user()
    >>> user
    <travispy.entities.user.User object at 0x02C26C48>

Now you can access information related to user current logged in::

    >>> user.login
    'travispy'
    >>> user['login']
    'travispy'

To get the list of repositories that you are member of::

    >>> repos = t.repos(member=user.login)
    >>> len(repos) # Ordered by recent activity
    5
    >>> repos[0]
    <travispy.entities.repo.Repo object at 0x02C26C49>
    >>> repos[0].slug
    'travispy/on_py34'

Or simply request for repository you want::

    >>> repo = r.repo('travispy/on_py34')
    <travispy.entities.repo.Repo object at 0x02C26C51>

And finally, getting build information::

    >>> build = t.build(repo.last_build_id)
    >>> build
    <travispy.entities.build.Build object at 0x02C26C50>
    >>> build.restart()
    True
    >>> build.cancel()
    True
    >>> build.cancel() # As build was already cancelled it will return False.
    False

Please refer to the `official API`_ to learn more about which `entities`_ are supported. Soon a
specific and detailed documentation related to this library will be available.
