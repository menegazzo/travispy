from ._entity import Entity


class User(Entity):
    '''
    :ivar str login:
        User login on |github|.

    :ivar str name:
        User name on |github|.

    :ivar str email:
        Primary email address on |github|.

    :ivar str gravatar_id:
        Avatar ID.

    :ivar bool is_syncing:
        Whether or not user account is currently being synced.

    :ivar str synced_at:
        Last synced at.

    :ivar bool correct_scopes:
        Whether or not |github| token has the correct scopes.

    :ivar str channels:
        Pusher channels for this user.

    :ivar str created_at:
        When account was created.

    :ivar str locale:
        User main locale.
    '''

    __slots__ = [
        'login',
        'name',
        'email',
        'gravatar_id',
        'is_syncing',
        'synced_at',
        'correct_scopes',
        'channels',
        'created_at',
        'locale',
    ]

    def sync (self):
        '''
        Triggers a new sync with GitHub. Might return status 409 if user is currently syncing.

        :rtype: bool
        :returns:
            ``True`` if sync request was send successfuly to |travisci| and response code is 200
            ``False`` if a sync is already is progress
        '''
        response = self._session.post(self._session.uri + '/users/sync')
        return response.status_code == 200
