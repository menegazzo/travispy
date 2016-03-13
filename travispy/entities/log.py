from ._entity import Entity


class Log(Entity):
    '''
    :ivar int job_id:
        Jod ID.

    :ivar str type:
    '''

    __slots__ = [
        'job_id',
        '_body',
        'type',
    ]

    def __init__(self, session):
        super(Log, self).__init__(session)
        self._body = None

    def get_archived_log(self):
        '''
        :rtype: str
        :returns:
            The archived log.
        '''
        header_overrides = {
            'Accept': 'text/plain; version=2'
        }

        r = self._session.get(
            self._session.uri + ('/jobs/%s/log' % self.job_id),
            headers=header_overrides,
        )
        return r.content.decode('utf-8')

    @property
    def body(self):
        '''
        :rtype: str
        :returns:
            The raw log text fetched on demand.
        '''
        if self._body is None:
            self._body = self.get_archived_log()

        return self._body

    @property
    def job(self):
        '''
        :rtype: :class:`.Job`
        :returns:
            A :class:`.Job` object with information related to current ``job_id``.
        '''
        from .job import Job
        return self._load_one_lazy_information(Job)
