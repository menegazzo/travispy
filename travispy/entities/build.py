from ._restartable import Restartable



#===================================================================================================
# Build
#===================================================================================================
class Build(Restartable):

    __slots__ = [
        'repository_id',
        'commit_id',
        'number',
        'pull_request',
        'pull_request_title',
        'pull_request_number',
        'config',
        'state',
        'started_at',
        'finished_at',
        'duration',
        'job_ids',
    ]
