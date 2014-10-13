from ._stateful import Stateful


class Branch(Stateful):
    '''
    :ivar int repository_id:
        Repository ID.

    :ivar str commit_id:
        Commit ID.

    :ivar str number:
        Build number.

    :ivar dict config:
        Build config (secure values and ssh key removed). It comes from ``.travis.yml`` file.

    :ivar str started_at:
        Time the build was started.

    :ivar str finished_at:
        Time the build finished.

    :ivar str duration:
        Build duration. It might not correspond to :attr:`finished_at` - :attr:`started_at` if the
        build was restarted at a later point.

    :ivar list(int) job_ids:
        List of job IDs in the build matrix.

    :ivar bool pull_request:
        Whether or not the build comes from a pull request.

    :ivar Commit commit:
        :class:`.Commit` information.
    '''

    __slots__ = [
        'repository_id',
        'commit_id',
        'number',
        'config',
        'started_at',
        'finished_at',
        'duration',
        'job_ids',
        'pull_request',
        'commit',
    ]

    @property
    def repository(self):
        '''
        :rtype: :class:`.Repo`
        :returns:
            A :class:`.Repo` object with information related to current ``repository_id``.
        '''
        from .repo import Repo
        return self._load_one_lazy_information(Repo, 'repository_id')

    @property
    def jobs(self):
        '''
        :rtype: list(:class:`.Job`)
        :returns:
            A list of :class:`.Job` objects with information related to current ``job_ids``.
        '''
        from .job import Job
        return self._load_many_lazy_information(Job)

    _FIND_MANY_EXCLUSIVE_PARAMETERS = ['repository_id', 'slug']

    @classmethod
    def many(cls):
        return 'branches'

    @classmethod
    def _find_one_command(cls, command, entity_id, **kwargs):
        repo_id_or_slug = kwargs['repo_id_or_slug']
        return '/repos/%s/%s/%s' % (repo_id_or_slug, cls.many(), entity_id)
