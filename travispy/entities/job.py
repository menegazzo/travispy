from ._restartable import Restartable



#===================================================================================================
# Job
#===================================================================================================
class Job(Restartable):

    __slots__ = [
        'build_id',
        'repository_id',
        'commit_id',
        'log_id',
        'number',
        'config',
        'state',
        'started_at',
        'finished_at',
        'duration',
        'queue',
        'allow_failure',
        'annotation_ids',
    ]
