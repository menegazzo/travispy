from ._entity import Entity


class Broadcast(Entity):
    '''
    :ivar str message:
        Broadcast message.
    '''

    __slots__ = [
        'message',
    ]
