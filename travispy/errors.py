class TravisError(Exception):
    '''
    Base error for all TravisPy errors.

    :param dict contents:
        The response contents. It may be used to create a better message.
    '''

    def __init__(self, contents):
        self._contents = contents
        Exception.__init__(self, self.message())

    def message(self):
        status_code = self._contents.pop('status_code')

        # Trying to get error message from "error/message" key.
        message = self._contents.get('error')
        if isinstance(message, dict):
            message = message.get('message')

        # Trying to get error message from "file" key.
        if message is None:
            message = self._contents.get('file')

        return '[%d] %s' % (status_code, message or 'Unknown error')
