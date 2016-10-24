class TravisError(Exception):
    '''
    Base error for all TravisPy errors.

    :param dict contents:
        The response contents. It may be used to create a better message.
    '''

    def __init__(self, contents):
        self._contents = contents
        self.status_code = contents['status_code']
        Exception.__init__(self, self.message())

    def message(self):
        # Trying to get error message from "error/message" key.
        message = self._contents.get('error')
        if isinstance(message, dict):
            message = message.get('message')

        # Trying to get error message from "file" key.
        if message is None:
            message = self._contents.get('file')

        return '[%d] %s' % (self.status_code, message or 'Unknown error')
