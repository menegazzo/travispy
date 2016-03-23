from ._entity import Entity


class Hook(Entity):
    '''
    :ivar str name:
        Hook name.

    :ivar str description:
        Hook description.

    :ivar str owner_name:
        Owner name.

    :ivar str active:
        Whether or not the hook is active.

    :ivar str private:
        Whether or not the hook is private.

    :ivar bool admin:
        Whether or not current user has administrator privileges.
    '''

    __slots__ = [
        'name',
        'description',
        'owner_name',
        'active',
        'private',
        'admin',
    ]
