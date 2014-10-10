from ._entity import Entity


class Commit(Entity):
    '''
    There is no API endpoint for resolving commits, however commit data might be included in other
    API entities, like :class:`.Build` or :class:`.Job`.

    :ivar str sha:
        Commit SHA.

    :ivar str branch:
        Branch the commit is on.

    :ivar str message:
        Commit message.

    :ivar str committed_at:
        Commit date.

    :ivar str author_name:
        Author name.

    :ivar str author_email:
        Author email.

    :ivar str committer_name:
        Committer name.

    :ivar str committer_email:
        Committer email.

    :ivar str compare_url:
        Link to diff on GitHub.

    :ivar str tag:
        Tag name.

    :ivar int pull_request_number:
        Pull request number.
    '''

    __slots__ = [
        'sha',
        'branch',
        'message',
        'committed_at',
        'author_name',
        'author_email',
        'committer_name',
        'committer_email',
        'compare_url',
        'tag',
        'pull_request_number',
    ]
