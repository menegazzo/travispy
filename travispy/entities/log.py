from ._entity import Entity



#===================================================================================================
# Log
#===================================================================================================
class Log(Entity):
    '''
    :ivar int job_id:
        Jod ID.

    :ivar str body:
        Log body.

    :ivar str type:
    '''

    __slots__ = [
        'job_id',
        'body',
        'type',
    ]
