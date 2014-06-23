from .entities import Account, Broadcast, Build, Hook, Job, Log, Repo, Session, User
import requests



#===================================================================================================
# Repository types
#===================================================================================================
PUBLIC = 'http://api.travis-ci.org'
PRIVATE = 'http://api.travis-ci.com'

# Replace "domain" with the domain TravisCI is running on.
# ENTERPRISE % {'domain': 'http://travis.example.com'}
ENTERPRISE = '%(domain)s/api'



#===================================================================================================
# TravisPy
#===================================================================================================
class TravisPy:
    '''
    This is an Python implementation of Travis-CI API.

    As Travis-CI API provides multiple ways to achieve the same result (to list builds of a specifid
    repository, for instance) a single and generic function will be available here for such purposes.

    Experimental methods will not be supported until they become official.

    For full documentation please refer to Travis-CI API documentation.

    .. seealso:: http://docs.travis-ci.com/api/
    '''

    _HEADERS = {
        'User-Agent': 'TravisPy',
        'Accept': 'application/vnd.travis-ci.2+json',
    }

    def __init__(self, token=None, uri=PUBLIC):
        '''
        :param str token:
            Travis-CI token linked to your GitHub account.
            Even if you have a public repository, some information are related to your user account
            and not the repository itself so if token is not provided an error will be returned.
            Required for private and enterprise repositories to access any information.

        :param str uri:
            URI where Travis-CI is running on.
            You may use the constants PUBLIC, PRIVATE or ENTERPRISE template.
        '''
        self._session = session = Session(uri)
        session.headers.update(self._HEADERS)
        if token is not None:
            session.headers['Authorization'] = 'token %s' % token


    @classmethod
    def github_auth(cls, token, uri=PUBLIC):
        response = requests.post(uri + '/auth/github', headers=cls._HEADERS, params={
            "github_token": token,
        })
        access_token = response.json()['access_token']
        return TravisPy(access_token, uri)


    # Accounts -------------------------------------------------------------------------------------
    def accounts(self, all=False):
        return self._session.find_many(Account, all=all)


    def account(self, account_id):
        for account in self.accounts(all=True):
            if account.id == account_id:
                return account


    # Broadcasts -----------------------------------------------------------------------------------
    def broadcasts(self):
        return self._session.find_many(Broadcast)


    # Builds ---------------------------------------------------------------------------------------
    def builds(self, **kwargs):
        exclusive_required_parameters = ['ids', 'repository_id', 'slug']
        for param in exclusive_required_parameters:
            if param in kwargs:
                break
        else:
            raise RuntimeError('You have to supply either "ids", "repository_id" or "slug".')

        return self._session.find_many(Build, **kwargs)


    def build(self, build_id):
        return self._session.find_one(Build, build_id)


    # Hooks ----------------------------------------------------------------------------------------
    def hooks(self):
        return self._session.find_many(Hook)


    # Jobs -----------------------------------------------------------------------------------------
    def jobs(self, **kwargs):
        exclusive_required_parameters = ['ids', 'repository_id', 'slug']
        provided_required_parameters = set(
            param
            for param in exclusive_required_parameters
            if param in kwargs
        )

        if len(provided_required_parameters) != 1:
            raise RuntimeError('You need to provide exactly one of the following parameters: "ids", "state" or "queue".')

        return self._session.find_many(Job, **kwargs)


    def job(self, job_id):
        return self._session.find_one(Job, job_id)


    # Log ------------------------------------------------------------------------------------------
    def log(self, log_id):
        return self._session.find_one(Log, log_id)


    # Repositories ---------------------------------------------------------------------------------
    def repos(self, **kwargs):
        return self._session.find_many(Repo, **kwargs)


    def repo(self, id_or_slug):
        return self._session.find_one(Repo, id_or_slug)

    # Users ----------------------------------------------------------------------------------------
    def user(self):
        return self._session.find_one(User, '')
