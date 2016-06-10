from ._stateful import Stateful


class Repo(Stateful):
    '''
    :ivar str slug:
        Repository slug.

    :ivar str description:
        Description on |github|.

    :ivar int last_build_id:
        Build ID of the last executed build.

    :ivar str last_build_number:
        Build number of the last executed build.

    :ivar str last_build_state:
        Build state of the last executed build.

    :ivar str last_build_duration:
        Build duration of the last executed build.

    :ivar str last_build_started_at:
        Build started at of the last executed build.

    :ivar str last_build_finished_at:
        Build finished at of the last executed build.

    :ivar str github_language:
        Language on |github|.

    :ivar bool active:
        Whether or not the repository is active on |travisci|.
    '''

    __slots__ = [
        'slug',
        'description',
        'last_build_id',
        'last_build_number',
        'last_build_state',
        'last_build_duration',
        'last_build_started_at',
        'last_build_finished_at',
        'last_build_language',
        'github_language',
        'active',
    ]

    @property
    def state(self):
        '''
        :class:`.Repo` state is given through ``last_build_state``.

        .. seealso:: :class:`.Stateful` for ``state`` full documentation.
        '''
        return self.last_build_state

    @property
    def last_build(self):
        '''
        :rtype: :class:`.Build`
        :returns:
            A :class:`.Build` object with information related to current ``last_build_id``.
        '''
        from .build import Build
        return self._load_one_lazy_information(Build, 'last_build_id')

    @classmethod
    def find_one(cls, session, entity_id, **kwargs):
        result = super(Repo, cls).find_one(session, entity_id, **kwargs)
        return result

    def _set_hook(self, flag):
        response = self._session.put(
            self._session.uri + '/hooks/{}'.format(self.id),
            json={"hook": {"active": flag}},
        )
        result = response.status_code == 200
        if result:
            self.active = flag
        return result

    def disable(self):
        '''
        Disable Travis CI for the repository.

        :rtype: bool
        :returns:
            ``True`` if API call was successful.
            ``False`` if API call was unsuccessful.
        '''
        return self._set_hook(False)

    def enable(self):
        '''
        Enable Travis CI for the repository

        :rtype: bool
        :returns:
            ``True`` if API call was successful
            ``False`` if API call was unsuccessful
        '''
        return self._set_hook(True)
