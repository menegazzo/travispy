from ._entity import Entity



#===================================================================================================
# Restartable
#===================================================================================================
class Restartable(Entity):

    def cancel(self):
        response = self._session.post(self._session.uri + '/%s/%d/cancel' % (self.many(), self.id))
        return response.status_code == 204


    def restart(self):
        response = self._session.post(self._session.uri + '/%s/%d/restart' % (self.many(), self.id))
        contents = response.json()
        return contents['result']
