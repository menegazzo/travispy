from entities.account import Account
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
        self._uri = uri
        self._session = session = requests.Session()
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
        response = self._session.get(self._uri + '/accounts', params={
            'all': all,
        })

        result = []

        contents = response.json()
        accounts = contents.get('accounts', [])
        for i_account in accounts:

            account = Account()
            for key, value in i_account.iteritems():
                setattr(account, key, value)
                
            result.append(account)

        return result


    def account(self, account_id):
        for account in self.accounts(all=True):
            if account.id == account_id:
                return account


    # Broadcasts -----------------------------------------------------------------------------------
    def broadcasts(self):
        pass


    # Builds ---------------------------------------------------------------------------------------
    def builds(self):
        pass


    def build(self, build_id):
        pass


    def cancel(self, build_id):
        pass


    def restart(self, build_id):
        pass


    # Hooks ----------------------------------------------------------------------------------------
    def hooks(self):
        pass


    def hook(self, hook_id):
        pass


    # Jobs -----------------------------------------------------------------------------------------
    def jobs(self):
        pass


    def job(self, job_id):
        pass


    # Log ------------------------------------------------------------------------------------------
    def log(self, log_id):
        return self.artifact(log_id)


    def artifact(self, artifact_id):
        pass


    # Repositories ---------------------------------------------------------------------------------
    def repos(self, **kwargs):
        pass


    def repo(self, id_or_slug):
        pass


#
# # # Authentication -----------------------------------------------------------------------------------
# # response = requests.get(host + '/users', headers=headers)
# # print response.json()
# #
# ## GitHub ------------------------------------------------------------------------------------------
# response = requests.post(PUBLIC + '/auth/github', headers=TravisPy._HEADERS, params={
#     "github_token": "9f6cce04ce8fee42519c256fe903836afc262833",
# })
# print response.json()
#
# headers = {'Authorization': 'token IVHjLjs8ni10wRF2YLuV5w'}
# headers.update(TravisPy._HEADERS)
# response = requests.get(PUBLIC + '/users', headers=headers)
# print response.json()
# #
# # # Entities -----------------------------------------------------------------------------------------
# #
# # ## Accounts ----------------------------------------------------------------------------------------
# # response = requests.get(host + '/accounts', headers=headers)
# # print response.json()
# #
# # response = requests.get(host + '/accounts', headers=headers, params={'all': 'true'})
# # print response.json()
# #
# # ## Branches ----------------------------------------------------------------------------------------
# # response = requests.get(host + '/repos/%s/branches' % 'menegazzo/watchsubs', headers=headers)
# # print response.json()
# #
# # response = requests.get(host + '/repos/%d/branches' % 2298605, headers=headers)
# # print response.json()
# #
# # response = requests.get(host + '/repos/%s/branches/master' % 'menegazzo/watchsubs', headers=headers)
# # print response.json()
# #
# # response = requests.get(host + '/repos/%d/branches/master' % 2298605, headers=headers)
# # print response.json()
# #
# # ## Broadcasts --------------------------------------------------------------------------------------
# # response = requests.get(host + '/broadcasts', headers=headers)
# # print response.json()
# #
# # ## Builds ------------------------------------------------------------------------------------------
# # response = requests.get(host + '/repos/%s/builds' % 'menegazzo/watchsubs', headers=headers)
# # print response.json()
# #
# # response = requests.get(host + '/builds', headers=headers, params={
# #     'slug': 'menegazzo/watchsubs',
# #     'after_number': 50,
# # })
# # print response.json()
