from ._entity import Entity
import json


class Hook(Entity):
    '''
    :ivar str name:
        Hook name.

    :ivar str description:
        Hook description.

    :ivar str owner_name:
        Owner name.

    :ivar str active:
        Whether or not the hook is active.

    :ivar str private:
        Whether or not the hook is private.

    :ivar bool admin:
        Whether or not current user has administrator privileges.
    '''

    __slots__ = [
        'name',
        'description',
        'owner_name',
        'active',
        'private',
        'admin',
    ]

    def _set_hook(self, flag):
        '''

        '''
        url = self._session.uri + '/hooks/{}'.format(self.id)
        data = {
            "hook": {
                "active": flag
            }
        }

        response = self._session.put(url, json = data)

        return response.status_code == 200


    def disable(self):
        if self._set_hook(False):
            self.active = False


    def enable(self):
        if self._set_hook(True):
            self.active = True

