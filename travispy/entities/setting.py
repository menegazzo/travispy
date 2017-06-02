from ._stateful import Stateful


class Setting(Stateful):
    '''
    :ivar str description:
        key description.

    :ivar str fingerprint:
        key fingerprint
    '''

    __slots__ = [
        'description',
        'fingerprint',
        'repo_id',
    ]

    @classmethod
    def one(cls):
        return 'ssh_key'

    @classmethod
    def many(cls):
        return 'ssh_key'

    @classmethod
    def find_one(cls, session, entity_id, **kwargs):
        try:
            result = super(Setting, cls).find_one(session, entity_id, **kwargs)
        except Exception as error:
            if (error.status_code == 404 and
               "Could not find a requested setting" in error.message()):
                result = cls._load({'description': None,
                                    'fingerprint': None}, session)[0]
            else:
                raise error
        return result

    def path_ssh_key(self, description, value):
        data = {'ssh_key': {'description': description, 'value': value}}
        uri = self._session.uri + '/settings/ssh_key/{}'.format(self.repo_id)
        response = self._session.patch(uri, json=data)
        result = response.json()
        if response.status_code == 200:
            result = self._load(result['ssh_key'], self._session)[0]
        return result

    @classmethod
    def _find_one_command(cls, command, entity_id, **kwargs):
        cls.repo_id = kwargs['repo_id_or_slug']
        return '/settings/%s/%s' % (cls.many(), cls.repo_id)
