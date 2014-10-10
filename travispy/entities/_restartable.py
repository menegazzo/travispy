from ._stateful import Stateful


class Restartable(Stateful):
    '''
    Base class for restartable entities such as :class:`.Build` and :class:`.Job`.
    '''

    def cancel(self):
        '''
        Method responsible for canceling current action of this object.

        :rtype: bool
        :returns:
            ``True`` if cancel request was send successfuly to |travisci|.
        '''
        response = self._session.post(self._session.uri + '/%s/%d/cancel' % (self.many(), self.id))
        return response.status_code == 204

    def restart(self):
        '''
        Method responsible for restarting the last action executed by this action.

        :rtype: bool
        :returns:
            ``True`` if restart request was send successfuly to |travisci|.
        '''
        response = self._session.post(self._session.uri + '/%s/%d/restart' % (self.many(), self.id))
        contents = response.json()
        return contents['result']
