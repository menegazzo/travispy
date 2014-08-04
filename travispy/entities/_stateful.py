from ._entity import Entity



#===================================================================================================
# Stateful
#===================================================================================================
class Stateful(Entity):
    '''
    Base class for stateful entities such as :class:`.Repo`, :class:`.Build` and :class:`.Job`.

    :ivar str state:
        Current state. Possible values are:

            - created
            - queued
            - started
            - passed
            - failed
            - errored
            - canceled
            - ready
    '''

    __slots__ = ['state']

    # States ---------------------------------------------------------------------------------------
    CANCELED = 'canceled'
    CREATED = 'created'
    ERRORED = 'errored'
    FAILED = 'failed'
    PASSED = 'passed'
    QUEUED = 'queued'
    READY = 'ready'
    STARTED = 'started'

    # Colors ---------------------------------------------------------------------------------------
    GREEN = 'green'
    YELLOW = 'yellow'
    RED = 'red'

    @property
    def created(self):
        self._check_state()
        return hasattr(self, 'state')


    @property
    def queued(self):
        self._check_state()
        return self.state != self.CREATED


    @property
    def started(self):
        self._check_state()
        return self.state not in [self.CREATED, self.QUEUED]


    @property
    def passed(self):
        self._check_state()
        return self.state == self.PASSED


    @property
    def failed(self):
        self._check_state()
        return self.state == self.FAILED


    @property
    def errored(self):
        self._check_state()
        return self.state == self.ERRORED


    @property
    def canceled(self):
        self._check_state()
        return self.state == self.CANCELED


    @property
    def ready(self):
        return self.state == self.READY


    @property
    def pending(self):
        self._check_state()
        return self.state in [self.CREATED, self.STARTED, self.QUEUED]


    @property
    def running(self):
        return self.state == self.STARTED


    @property
    def finished(self):
        return not self.pending


    @property
    def successful(self):
        return self.passed


    @property
    def unsuccessful(self):
        return self.errored or self.failed or self.canceled


    @property
    def color(self):
        self._check_state()
        if self.passed or self.ready:
            return self.GREEN

        elif self.pending:
            return self.YELLOW

        elif self.unsuccessful:
            return self.RED


    @property
    def green(self):
        return self.color == self.GREEN


    @property
    def yellow(self):
        return self.color == self.YELLOW


    @property
    def red(self):
        return self.color == self.RED

    def _check_state(self):
        if self.state not in [
            self.CANCELED,
            self.CREATED,
            self.ERRORED,
            self.FAILED,
            self.PASSED,
            self.QUEUED,
            self.READY,
            self.STARTED,
            ]:
            raise ValueError('unknown state %s for %s' % (self.state, self.__class__.__name__))
