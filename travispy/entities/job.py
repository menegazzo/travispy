from ._restartable import Restartable
from datetime import datetime


class Job(Restartable):
    '''
    :ivar int build_id:
        Build ID.

    :ivar int repository_id:
        Repository ID.

    :ivar int commit_id:
        Commit ID.

    :ivar int log_id:
        Log ID.

    :ivar str number:
        Job number.

    :ivar dict config:
        Job config (secure values and ssh key removed). It comes from ``.travis.yml`` file.

    :ivar str started_at:
        Time the job was started.

    :ivar str finished_at:
        Time the job finished.

    :ivar str duration:
        Job duration. It might not correspond to :attr:`finished_at` - :attr:`started_at` if the
        job was restarted at a later point.

    :ivar str queue:
        Job queue.

    :ivar bool allow_failure:
        Whether or not the job state influences build state.

    :ivar list(int) annotation_ids:
        List of annotation IDs.

    :ivar Commit commit:
        :class:`.Commit` information.
    '''

    __slots__ = [
        'build_id',
        'repository_id',
        'commit_id',
        'log_id',
        'number',
        'config',
        'started_at',
        'finished_at',
        'duration',
        'queue',
        'allow_failure',
        'annotation_ids',
        'commit',
    ]

    _FIND_MANY_EXCLUSIVE_PARAMETERS = ['ids', 'state', 'queue']

    @property
    def build(self):
        '''
        :rtype: :class:`.Build`
        :returns:
            A :class:`.Build` object with information related to current ``build_id``.
        '''
        from .build import Build
        return self._load_one_lazy_information(Build)

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
    def log(self):
        '''
        :rtype: :class:`.Log`
        :returns:
            A :class:`.Log` object with information related to current ``log_id``.
        '''
        from .log import Log
        return self._load_one_lazy_information(Log)

    @classmethod
    def find_one(cls, session, entity_id, **kwargs):
        result = super(Job, cls).find_one(session, entity_id, **kwargs)
        if result is not None and not hasattr(result, 'duration'):
            format_ = '%Y-%m-%dT%H:%M:%SZ'

            started_at = result.started_at
            started_at = \
                datetime.strptime(started_at, format_) \
                if started_at is not None \
                else datetime.now()

            finished_at = result.finished_at
            finished_at = \
                datetime.strptime(finished_at, format_) \
                if finished_at is not None \
                else datetime.now()

            td = finished_at - started_at
            td = round((td.microseconds + (td.seconds + td.days * 24 * 3600) * 10 ** 6) / 10 ** 6)
            setattr(result, 'duration', int(td))
        return result
