#===================================================================================================
# Entity
#===================================================================================================
class Entity(object):

    __slots__ = [
        'id',
        '_session',
    ]

    def __init__(self, session):
        self._session = session


    @classmethod
    def one(cls):
        return cls.__name__.lower()


    @classmethod
    def many(cls):
        return cls.one() + 's'


    def __getitem__(self, key):
        return getattr(self, key)
