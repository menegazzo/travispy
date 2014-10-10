import requests


class Session(requests.Session):
    '''
    Internet session created to perform requests to |travisci|.

    :param str uri:
        URI where session will start.
    '''

    def __init__(self, uri):
        requests.Session.__init__(self)
        self.uri = uri
