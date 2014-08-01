from ._entity import Entity



#===================================================================================================
# Stateful
#===================================================================================================
class Stateful(Entity):
    '''
    Base class for stateful entities such as :class:`.Repo`, :class:`.Build` and :class:`.Job`.
    '''
    
    CANCELED = 'canceled'
    CREATED = 'created'
    ERRORED = 'errored'
    FAILED = 'failed'
    PASSED = 'passed'
    QUEUED = 'queued'
    READY = 'ready'
    STARTED = 'started'
    
    STATES = [
        'canceled',
        'created',
        'errored',
        'failed',
        'passed',
        'queued',
        'ready',
        'started',
    ]

    __slots__ = [
        'created?',
        'errored?',
        'failed?',
        'finished?',
        'green?',
        'passed?',
        'pending?',
        'queued?',
        'red?',
        'running?',
        'started?',
        'successful?',
        'unsuccessful?',
        'yellow?',
        'color',
        'state',
    ]

    @property
    def ready(self):
        return self.state == self.READY


    @property
    def pending(self):
        return self.state in [self.CREATED, self.STARTED, self.QUEUED]


    @property
    def started(self):
        return self.state not in [self.CREATED, self.QUEUED]


    @property
    def queued(self):
        return self.state != self.CREATED


    @property
    def finished(self):
        return not self.pending


    @property
    def passed(self):
        return self.state == self.PASSED


    @property
    def errored(self):
        return self.state == self.ERRORED


    @property
    def failed(self):
        return self.state == self.FAILED


    @property
    def canceled(self):
        return self.state == self.CANCELED


    @property
    def unsuccessful(self):
        return self.errored or self.failed or self.canceled
