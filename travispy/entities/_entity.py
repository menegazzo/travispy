#===================================================================================================
# Entity
#===================================================================================================
class Entity(object):
    '''
    Base class for all |travisci| entities.

    :type session: :class:`.Session`
    :param session:
        Internet session in which entity information will be requested.

    :ivar int id:
        The entity ID.
    '''

    __slots__ = [
        'id',
        '_session',
    ]

    def __init__(self, session):
        self._session = session


    @classmethod
    def one(cls):
        '''
        :rtype: str
        :returns:
            String representation for a single entity.
            Example: for :class:`.Account` will be ``account``.
        '''
        return cls.__name__.lower()


    @classmethod
    def many(cls):
        '''
        :rtype: str
        :returns:
            String representation for multiple entities.
            Example: for :class:`.Account` will be ``accounts``.
        '''
        return cls.one() + 's'


    def __getitem__(self, key):
        return getattr(self, key)
