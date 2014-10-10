from ._entity import Entity


class Stateful(Entity):
    '''
    Base class for stateful entities such as :class:`.Repo`, :class:`.Build` and :class:`.Job`.

    .. attribute:: CANCELED

        Constant representing state ``canceled``. Should not be changed.

    .. attribute:: CREATED

        Constant representing state ``created``. Should not be changed.

    .. attribute:: QUEUED

        Constant representing state ``queued``. Should not be changed.

    .. attribute:: STARTED

        Constant representing state ``started``. Should not be changed.

    .. attribute:: PASSED

        Constant representing state ``passed``. Should not be changed.

    .. attribute:: FAILED

        Constant representing state ``failed``. Should not be changed.

    .. attribute:: ERRORED

        Constant representing state ``errored``. Should not be changed.

    .. attribute:: READY

        Constant representing state ``ready``. Should not be changed.

    .. attribute:: GREEN

        Constant representing state color ``green``. Should not be changed.

    .. attribute:: YELLOW

        Constant representing state color ``yellow``. Should not be changed.

    .. attribute:: RED

        Constant representing state color ``red``. Should not be changed.

    :ivar str state:

        Current state. Possible values are:

            - :attr:`.CANCELED`
            - :attr:`.CREATED`
            - :attr:`.QUEUED`
            - :attr:`.STARTED`
            - :attr:`.PASSED`
            - :attr:`.FAILED`
            - :attr:`.ERRORED`
            - :attr:`.READY`
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
        '''
        :rtype: bool
        :returns:
            ``True`` if entity build process was created successfully.

        .. seealso:: :meth:`.check_state`
        '''
        self.check_state()
        return hasattr(self, 'state')

    @property
    def queued(self):
        '''
        :rtype: bool
        :returns:
            ``True`` if entity was already queued sometime in the build process.

        .. seealso:: :meth:`.check_state`
        '''
        self.check_state()
        return self.state != self.CREATED

    @property
    def started(self):
        '''
        :rtype: bool
        :returns:
            ``True`` if entity was already started sometime in the build process.

        .. seealso:: :meth:`.check_state`
        '''
        self.check_state()
        return self.state not in [self.CREATED, self.QUEUED]

    @property
    def passed(self):
        '''
        :rtype: bool
        :returns:
            ``True`` if build process was finished successfully.

        .. seealso:: :meth:`.check_state`
        '''
        self.check_state()
        return self.state == self.PASSED

    @property
    def failed(self):
        '''
        :rtype: bool
        :returns:
            ``True`` if build process failed. This is usually related to failures on tests.

        .. seealso:: :meth:`.check_state`
        '''
        self.check_state()
        return self.state == self.FAILED

    @property
    def errored(self):
        '''
        :rtype: bool
        :returns:
            ``True`` if build process got errors.

        .. seealso:: :meth:`.check_state`
        '''
        self.check_state()
        return self.state == self.ERRORED

    @property
    def canceled(self):
        '''
        :rtype: bool
        :returns:
            ``True`` if build process was canceled.

        .. seealso:: :meth:`.check_state`
        '''
        self.check_state()
        return self.state == self.CANCELED

    @property
    def ready(self):
        '''
        :rtype: bool
        :returns:
            ``True`` if build process is ready.

        .. seealso:: :meth:`.check_state`
        '''
        self.check_state()
        return self.state == self.READY

    @property
    def pending(self):
        '''
        :rtype: bool
        :returns:
            ``True`` if build was scheduled but was not finished.

        .. seealso:: :meth:`.check_state`
        '''
        self.check_state()
        return self.state in [self.CREATED, self.STARTED, self.QUEUED]

    @property
    def running(self):
        '''
        :rtype: bool
        :returns:
            ``True`` if build process is running.

        .. seealso:: :meth:`.check_state`
        '''
        self.check_state()
        return self.state == self.STARTED

    @property
    def finished(self):
        '''
        :rtype: bool
        :returns:
            ``True`` if build process is finished.
        '''
        return not self.pending

    @property
    def successful(self):
        '''
        .. seealso:: :attr:`.passed`
        '''
        return self.passed

    @property
    def unsuccessful(self):
        '''
        :rtype: bool
        :returns:
            ``True`` if build process was finished unsuccessfully.
        '''
        return self.errored or self.failed or self.canceled

    @property
    def color(self):
        '''
        :rtype: bool
        :returns:
           The color related to current build state. Possible values are:

               - :attr:`.GREEN`: when build has passed or it is ready.
               - :attr:`.YELLOW`: when build process is running.
               - :attr:`.RED`: when build has failed somehow.
        '''
        if self.passed or self.ready:
            return self.GREEN

        elif self.pending:
            return self.YELLOW

        elif self.unsuccessful:
            return self.RED

    @property
    def green(self):
        '''
        :rtype: bool
        :returns:
            ``True`` if build :attr:`.color` is :attr:`.GREEN`.
        '''
        return self.color == self.GREEN

    @property
    def yellow(self):
        '''
        :rtype: bool
        :returns:
            ``True`` if build :attr:`.color` is :attr:`.YELLOW`.
        '''
        return self.color == self.YELLOW

    @property
    def red(self):
        '''
        :rtype: bool
        :returns:
            ``True`` if build :attr:`.color` is :attr:`.RED`.
        '''
        return self.color == self.RED

    def check_state(self):
        '''
        Method responsible for checking and validating current :attr:`.state`.

        :raises AttributeError: when :attr:`.state` does not exist.
        :raises ValueError: when :attr:`.state` value is not supported.
        '''
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
