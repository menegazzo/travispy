from ._entity import Entity



#===================================================================================================
# User
#===================================================================================================
class User(Entity):

    __slots__ = [
        'login',
        'name',
        'email',
        'gravatar_id',
        'is_syncing',
        'synced_at',
        'correct_scopes',
        'channels',
    ]
