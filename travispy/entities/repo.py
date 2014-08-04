from ._stateful import Stateful



#===================================================================================================
# Repo
#===================================================================================================
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
        This property must be overiden as soon as support to load "lazy" information is implemented.
        '''
        return self.CREATED
