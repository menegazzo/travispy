from ._entity import Entity


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

    @property
    def job(self):
        '''
        :rtype: :class:`.Job`
        :returns:
            A :class:`.Job` object with information related to current ``job_id``.
        '''
        from .job import Job
        return self._load_one_lazy_information(Job)
