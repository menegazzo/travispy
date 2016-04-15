'''
.. data:: PUBLIC
    :annotation: = URI for Travis CI free service.

.. data:: PRIVATE
    :annotation: = URI for Travis CI paid service for GitHub private repositories.

.. data:: ENTERPRISE
    :annotation: = URI template for Travis CI service running under a personal domain. Usage will be
                 something like ENTERPRISE % {'domain': 'http://travis.example.com'}.
'''
from ._helpers import get_response_contents
from .entities import Account, Branch, Broadcast, Build, Hook, Job, Log, Repo, Session, User
import requests


PUBLIC = 'https://api.travis-ci.org'
PRIVATE = 'https://api.travis-ci.com'

# Replace "domain" with the domain TravisCI is running on.
# ENTERPRISE % {'domain': 'http://travis.example.com'}
ENTERPRISE = '%(domain)s/api'


class TravisPy:
    '''
    Instances of this class are responsible for comunicating with |travisci|, sending requests and
    handling responses properly. You can create as much instances as you want since each one will
    create a separated session.

    :type token: str | None
    :param token:
        |travisci| token linked to your |github| account.

        Even if you have a public repository, some information are related to your user account
        and not the repository itself so if token is not provided an error will be returned.

        Required for private and enterprise repositories to access any information.

    :type uri: :data:`PUBLIC` | :data:`PRIVATE` | :data:`ENTERPRISE` | str
    :param uri:
        URI where Travis CI service is running.

    .. note::
        Do not confuse ``token`` with the one found on your profile page.
    '''

    _HEADERS = {
        'User-Agent': 'TravisPy',
        'Accept': 'application/vnd.travis-ci.2+json',
    }

    def __init__(self, token=None, uri=PUBLIC):
        self._session = session = Session(uri)
        session.headers.update(self._HEADERS)
        if token is not None:
            session.headers['Authorization'] = 'token %s' % token

    @classmethod
    def github_auth(cls, token, uri=PUBLIC):
        '''
        :param str token:
            GitHub access token.

        :param uri:
            See :meth:`__init__`

        :rtype: :class:`.TravisPy`
        :returns:
            A :class:`.TravisPy` instance authenticated with GitHub account.

        :raises TravisError: when authentication against GitHub fails.
        '''
        response = requests.post(uri + '/auth/github', headers=cls._HEADERS, params={
            "github_token": token,
        })
        contents = get_response_contents(response)
        access_token = contents['access_token']
        return TravisPy(access_token, uri)

    def accounts(self, all=False):
        '''
        :param bool all:
            Whether or not to include accounts the user does not have admin access to.

        :rtype: list(:class:`.Account`)
        :returns:
            Information of all accounts that the user might have access.This is usually the account
            corresponding to the user directly and one account per |github| organization.

        .. note::
            This request always needs to be authenticated.
        '''
        return Account.find_many(self._session, all=all)

    def account(self, account_id):
        '''
        :param int account_id:
            ID of the account to obtain information.

        :rtype: :class:`.Account`

        .. note::
            This request always needs to be authenticated.
        '''
        for account in self.accounts(all=True):
            if account.id == account_id:
                return account

    def branches(self, **kwargs):
        '''
        :keyword int repository_id:
            Repository id the build belongs to.

        :keyword str slug:
            Repository slug the build belongs to.

        :rtype: list(:class:`.Branch`)

        .. note::
            You have to supply either ``repository_id`` or ``slug``.
        '''
        return Branch.find_many(self._session, **kwargs)

    def branch(self, name, repo_id_or_slug, **kwargs):
        '''
        :param str name:
            Branch name that should be retrieved.

        :type repo_id_or_slug: int | str
        :param repo_id_or_slug:
            Repository where branch is located.

        :rtype: :class:`.Branch`
        '''
        kwargs['repo_id_or_slug'] = repo_id_or_slug
        return Branch.find_one(self._session, name, **kwargs)

    def broadcasts(self):
        '''
        :rtype: list(:class:`.Broadcast`)

        .. note::
            This request always needs to be authenticated.
        '''
        return Broadcast.find_many(self._session)

    def builds(self, **kwargs):
        '''
        :keyword list(int) ids:
            List of build ids to fetch.

        :keyword int repository_id:
            Repository id the build belongs to.

        :keyword str slug:
            Repository slug the build belongs to.

        :keyword str number:
            Filter by build number, requires ``slug`` or ``repository_id``.

        :keyword str after_number:
            List build after a given build number (use for pagination), requires ``slug`` or
            ``repository_id``.

        :keyword str event_type:
            Limit build to given event type (``push`` or ``pull_request``).

        :rtype: list(:class:`.Build`)

        .. note::
            You have to supply either ``ids``, ``repository_id`` or ``slug``.
        '''
        return Build.find_many(self._session, **kwargs)

    def build(self, build_id):
        '''
        :param int build_id:
            ID of the build to obtain information.

        :rtype: :class:`.Build`
        '''
        return Build.find_one(self._session, build_id)

    def hooks(self):
        '''
        :rtype: list(:class:`.Hook`)
        :returns:
            Returns list of existing hooks that user have access.

        .. note::
            This request always needs to be authenticated.
        '''
        return Hook.find_many(self._session)

    def jobs(self, **kwargs):
        '''
        :keyword list(int) ids:
            List of jobs IDs.

        :keyword str state:
            Job state to filter by. Possible values are ``passed``, ``canceled``, ``failed`` and
            ``errored``.

        :keyword str queue:
            Job queue to filter by.

        :rtype: list(:class:`.Job`)

        .. note::
            You need to provide exactly one of the above parameters. If you provide ``state`` or
            ``queue``, a maximum of 250 jobs will be returned.
        '''
        return Job.find_many(self._session, **kwargs)

    def job(self, job_id):
        '''
        :param int job_id:
            ID of the job to obtain information.

        :rtype: :class:`.Job`
        '''
        return Job.find_one(self._session, job_id)

    def log(self, log_id):
        '''
        :param int log_id:
            ID of the log to obtain information.

        :rtype: :class:`.Log`
        '''
        return Log.find_one(self._session, log_id)

    def repos(self, **kwargs):
        '''
        :keyword list(int) ids:
            List of repository ids to fetch, cannot be combined with other parameters.

        :keyword str member:
            Filter by user that has access to it (|github| login).

        :keyword str owner_name:
            Filter by owner name (first segment of slug).

        :keyword str slug:
            Filter by slug.

        :keyword str search:
            Filter by search term.

        :keyword bool active:
            If ``True``, will only return repositories that are enabled. Default is ``False``.

        :rtype: list(:class:`.Repo`)

        .. note::
            If no parameters are given, a list of repositories with recent activity is returned.
        '''
        return Repo.find_many(self._session, **kwargs)

    def repo(self, id_or_slug):
        '''
        :type id_or_slug: int | str
        :param id_or_slug:
            ID of slug of repository to obtain information.

        :rtype: :class:`.Repo`
        '''
        return Repo.find_one(self._session, id_or_slug)

    def user(self):
        '''
        :rtype: :class:`.User`
        :returns:
            Information about user currently logged in.

        .. note::
            This request always needs to be authenticated.
        '''
        return User.find_one(self._session, '')
