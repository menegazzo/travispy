from ._entity import Entity


class Account(Entity):
    '''
    A user might have access to multiple accounts. This is usually the account corresponding to the
    user directly and one account per |github| organization.

    :ivar str name:
        User or organization id.

    :ivar str login:
        Account name on |github|.

    :ivar str type:
        Account login on |github|.

    :ivar int repos_count:
        Number of repositories.

    :ivar bool subscribed:
        Whether or not the account has a valid subscription.
        Only available on *Travis Pro*.

    :ivar str avatar_url:
        Link to avatar.
    '''

    __slots__ = [
        'name',
        'login',
        'type',
        'repos_count',
        'subscribed',
        'avatar_url',
    ]
